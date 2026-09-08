from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path('.').resolve()
PROD = 'https://xjtlu-korea.netlify.app'
PREVIEW = 'https://deploy-preview-6--xjtlu-korea.netlify.app'
UA = 'TNS-Predeploy-Audit/1.0'

errors: list[str] = []
warnings: list[str] = []
notes: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)
    print('ERROR:', msg)


def warn(msg: str) -> None:
    warnings.append(msg)
    print('WARN :', msg)


def note(msg: str) -> None:
    notes.append(msg)
    print('OK   :', msg)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.titles: list[str] = []
        self._in_title = False
        self._title_parts: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.h1_count = 0
        self.h1_texts: list[str] = []
        self._h1_depth = 0
        self._h1_parts: list[str] = []
        self.ids: set[str] = set()
        self.jsonld_parts: list[str] = []
        self._in_jsonld = False
        self._jsonld_buf: list[str] = []
        self.html_lang: str | None = None
        self.visible_text_parts: list[str] = []
        self._hidden_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        a = {k.lower(): (v or '') for k, v in attrs}
        tag = tag.lower()
        if tag == 'html':
            self.html_lang = a.get('lang')
        if 'id' in a and a['id']:
            self.ids.add(a['id'])
        if 'name' in a and a['name']:
            self.ids.add(a['name'])
        if tag == 'title':
            self._in_title = True
            self._title_parts = []
        if tag == 'h1':
            self.h1_count += 1
            self._h1_depth += 1
            if self._h1_depth == 1:
                self._h1_parts = []
        if tag == 'meta':
            self.meta.append(a)
        if tag in {'a', 'img', 'script', 'link', 'iframe', 'source'}:
            self.links.append({'tag': tag, **a})
        if tag == 'script' and a.get('type', '').lower() == 'application/ld+json':
            self._in_jsonld = True
            self._jsonld_buf = []
        if tag in {'style', 'script', 'noscript'}:
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == 'title' and self._in_title:
            self._in_title = False
            self.titles.append(' '.join(''.join(self._title_parts).split()))
        if tag == 'h1' and self._h1_depth:
            self._h1_depth -= 1
            if self._h1_depth == 0:
                self.h1_texts.append(' '.join(''.join(self._h1_parts).split()))
        if tag == 'script' and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld_parts.append(''.join(self._jsonld_buf).strip())
            self._jsonld_buf = []
        if tag in {'style', 'script', 'noscript'} and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._h1_depth:
            self._h1_parts.append(data)
        if self._in_jsonld:
            self._jsonld_buf.append(data)
        elif self._hidden_depth == 0:
            t = ' '.join(data.split())
            if t:
                self.visible_text_parts.append(t)


def meta_value(p: PageParser, key: str, value: str, content_key='content') -> list[str]:
    out = []
    for m in p.meta:
        if m.get(key, '').lower() == value.lower():
            out.append(m.get(content_key, ''))
    return out


def canonical_values(p: PageParser) -> list[str]:
    vals = []
    for l in p.links:
        if l.get('tag') == 'link' and 'canonical' in l.get('rel', '').lower().split():
            vals.append(l.get('href', ''))
    return vals


def normalize_local(raw: str, current: Path) -> tuple[Path | None, str | None]:
    if not raw:
        return None, None
    raw = raw.strip()
    if raw.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        if raw.startswith('#'):
            return current, raw[1:]
        return None, None
    u = urllib.parse.urlsplit(raw)
    if u.scheme in {'http', 'https'}:
        host = u.netloc.lower()
        if host not in {'xjtlu-korea.netlify.app', 'deploy-preview-6--xjtlu-korea.netlify.app'}:
            return None, None
        path = urllib.parse.unquote(u.path)
    elif u.scheme:
        return None, None
    else:
        path = urllib.parse.unquote(u.path)
    frag = u.fragment or None
    if not path:
        return current, frag
    if path.startswith('/'):
        rel = Path(path.lstrip('/'))
    else:
        rel = current.parent / path
    if str(rel).endswith('/'):
        rel = rel / 'index.html'
    elif rel.suffix == '':
        html_candidate = Path(str(rel) + '.html')
        if (ROOT / html_candidate).exists():
            rel = html_candidate
        elif (ROOT / rel / 'index.html').exists():
            rel = rel / 'index.html'
    try:
        rel = Path(rel).resolve().relative_to(ROOT)
    except Exception:
        return None, frag
    return rel, frag


html_files = sorted(
    p.relative_to(ROOT)
    for p in ROOT.rglob('*.html')
    if '.git' not in p.parts and '.github' not in p.parts and not p.name.startswith('google')
)

if not html_files:
    err('No HTML pages found')
    sys.exit(1)

pages: dict[Path, PageParser] = {}
texts: dict[Path, str] = {}
indexable: set[Path] = set()
all_internal_targets: defaultdict[Path, list[tuple[Path, str | None]]] = defaultdict(list)
inbound = Counter()
external_anchors: set[str] = set()
local_assets: set[Path] = set()

titles_seen: defaultdict[str, list[Path]] = defaultdict(list)
canon_seen: defaultdict[str, list[Path]] = defaultdict(list)
h1_seen: defaultdict[str, list[Path]] = defaultdict(list)

print(f'Found {len(html_files)} HTML pages')

for rel in html_files:
    text = (ROOT / rel).read_text(encoding='utf-8')
    texts[rel] = text
    p = PageParser()
    p.feed(text)
    pages[rel] = p

    if p.html_lang != 'ko':
        err(f'{rel}: html lang should be ko, found {p.html_lang!r}')

    if len(p.titles) != 1 or not p.titles[0]:
        err(f'{rel}: expected exactly one non-empty <title>, found {len(p.titles)}')
    else:
        title = p.titles[0]
        titles_seen[title].append(rel)
        if not (20 <= len(title) <= 75):
            warn(f'{rel}: title length {len(title)} is outside 20-75 chars')

    descriptions = meta_value(p, 'name', 'description')
    if len(descriptions) != 1 or not descriptions[0].strip():
        err(f'{rel}: expected exactly one meta description, found {len(descriptions)}')
    elif not (50 <= len(descriptions[0]) <= 180):
        warn(f'{rel}: meta description length {len(descriptions[0])} is outside 50-180 chars')

    robots = meta_value(p, 'name', 'robots')
    noindex = any('noindex' in r.lower() for r in robots)
    if not noindex:
        indexable.add(rel)
        if len(robots) != 1:
            err(f'{rel}: expected one meta robots tag for indexable page, found {len(robots)}')
        elif 'index' not in robots[0].lower():
            warn(f'{rel}: robots content is {robots[0]!r}, expected explicit index')

    cans = canonical_values(p)
    if len(cans) != 1:
        err(f'{rel}: expected exactly one canonical, found {len(cans)}')
    else:
        can = cans[0]
        canon_seen[can].append(rel)
        expected = PROD + ('/' if rel.as_posix() == 'index.html' else '/' + rel.as_posix())
        if can != expected:
            err(f'{rel}: canonical {can!r} != expected {expected!r}')

    if p.h1_count != 1:
        err(f'{rel}: expected exactly one H1, found {p.h1_count}')
    elif p.h1_texts:
        h1_seen[p.h1_texts[0]].append(rel)

    for prop in ('og:title', 'og:description', 'og:url'):
        vals = meta_value(p, 'property', prop)
        if len(vals) != 1 or not vals[0].strip():
            err(f'{rel}: missing or duplicate {prop}')
    og_urls = meta_value(p, 'property', 'og:url')
    if og_urls and cans and og_urls[0] != cans[0]:
        err(f'{rel}: og:url does not match canonical')

    for i, raw in enumerate(p.jsonld_parts, start=1):
        if not raw:
            err(f'{rel}: empty JSON-LD block #{i}')
            continue
        try:
            json.loads(raw)
        except Exception as e:
            err(f'{rel}: invalid JSON-LD block #{i}: {e}')

    visible = ' '.join(p.visible_text_parts)
    if 'FAQPage' in text and not re.search(r'FAQ|자주 묻는|질문', visible, re.I):
        warn(f'{rel}: FAQPage schema exists but no obvious visible FAQ heading/text was found')

    for item in p.links:
        tag = item.get('tag')
        attr = 'href' if tag in {'a', 'link'} else 'src'
        raw = item.get(attr, '')
        if not raw:
            continue
        if tag == 'a':
            u = urllib.parse.urlsplit(raw)
            if u.scheme in {'http', 'https'} and u.netloc.lower() not in {'xjtlu-korea.netlify.app', 'deploy-preview-6--xjtlu-korea.netlify.app'}:
                external_anchors.add(raw)
                if item.get('target') == '_blank' and 'noopener' not in item.get('rel', '').lower().split():
                    err(f'{rel}: external target=_blank link missing rel=noopener: {raw}')
                low = raw.lower()
                if any(k in low for k in ('/apply', 'application-portal', 'how-to-apply', 'apply-now')):
                    warn(f'{rel}: possible direct-application external link present: {raw}')
                continue
        target, frag = normalize_local(raw, rel)
        if target is not None:
            if tag == 'a':
                all_internal_targets[rel].append((target, frag))
                if target != rel:
                    inbound[target] += 1
            elif tag in {'img', 'script', 'link', 'source'}:
                # Only file-like local resources. Ignore anchor-ish stylesheet edge cases handled by existence check.
                local_assets.add(target)

    for raw in re.findall(r'url\(\s*["\']?([^"\')]+)', text, flags=re.I):
        target, _ = normalize_local(raw, rel)
        if target is not None:
            local_assets.add(target)

for value, rels in titles_seen.items():
    if len(rels) > 1:
        err(f'Duplicate title across pages {rels}: {value!r}')
for value, rels in canon_seen.items():
    if len(rels) > 1:
        err(f'Duplicate canonical across pages {rels}: {value!r}')
for value, rels in h1_seen.items():
    if value and len(rels) > 1:
        warn(f'Duplicate H1 text across pages {rels}: {value!r}')

for src, targets in all_internal_targets.items():
    for target, frag in targets:
        target_abs = ROOT / target
        if not target_abs.exists():
            err(f'{src}: broken internal link -> {target}' + (f'#{frag}' if frag else ''))
            continue
        if target.suffix == '.html' and frag:
            tp = pages.get(target)
            if tp is None:
                try:
                    raw = target_abs.read_text(encoding='utf-8')
                    tp = PageParser(); tp.feed(raw)
                except Exception:
                    tp = None
            if tp is not None and frag not in tp.ids:
                err(f'{src}: missing anchor #{frag} in {target}')

for asset in sorted(local_assets):
    if asset.suffix.lower() in {'.html', '.htm'}:
        continue
    if not (ROOT / asset).exists():
        err(f'Broken local asset reference: {asset}')

for rel in sorted(indexable):
    if rel.as_posix() != 'index.html' and inbound[rel] == 0:
        err(f'Orphan indexable page with no inbound internal links: {rel}')

# Sitemap audit
sitemap_path = ROOT / 'sitemap.xml'
if not sitemap_path.exists():
    err('sitemap.xml missing')
    sitemap_urls = set()
else:
    try:
        tree = ET.parse(sitemap_path)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        loc_nodes = tree.findall('.//sm:loc', ns)
        sitemap_urls = {n.text.strip() for n in loc_nodes if n.text}
        if len(sitemap_urls) != len(loc_nodes):
            err('sitemap.xml contains duplicate or empty <loc> entries')
        expected_urls = {
            PROD + ('/' if rel.as_posix() == 'index.html' else '/' + rel.as_posix())
            for rel in indexable
        }
        missing = sorted(expected_urls - sitemap_urls)
        extra = sorted(sitemap_urls - expected_urls)
        for u in missing:
            err(f'sitemap missing indexable page: {u}')
        for u in extra:
            err(f'sitemap contains non-indexable/nonexistent page: {u}')
        for lm in tree.findall('.//sm:lastmod', ns):
            if lm.text and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lm.text.strip()):
                warn(f'sitemap lastmod not YYYY-MM-DD: {lm.text!r}')
    except Exception as e:
        err(f'Invalid sitemap.xml: {e}')
        sitemap_urls = set()

# robots audit
robots_path = ROOT / 'robots.txt'
if not robots_path.exists():
    err('robots.txt missing')
else:
    robots_text = robots_path.read_text(encoding='utf-8')
    if not re.search(r'(?im)^User-agent:\s*\*\s*$', robots_text):
        err('robots.txt missing User-agent: *')
    if re.search(r'(?im)^Disallow:\s*/\s*$', robots_text):
        err('robots.txt blocks the entire site')
    if not re.search(r'(?im)^Sitemap:\s*https://xjtlu-korea\.netlify\.app/sitemap\.xml\s*$', robots_text):
        err('robots.txt missing exact production sitemap URL')

# Search verification
index_text = texts.get(Path('index.html'), '')
for token in ('google-site-verification', 'naver-site-verification'):
    if token not in index_text:
        err(f'Homepage missing {token} meta verification')
if not any(ROOT.glob('google*.html')):
    warn('No Google HTML verification file found')

# Deleted/obsolete page references
for needle in ('university-of-liverpool-vietnam.html', '리버풀대학교의 아시아 네트워크', '리버풀대학교의 베트남·아시아 네트워크'):
    hits = [str(rel) for rel, text in texts.items() if needle in text]
    if hits:
        err(f'Obsolete Liverpool Vietnam/Korea reference {needle!r} remains in {hits}')

# Homepage should not visibly link to generic XJTLU official/apply URLs.
home = pages.get(Path('index.html'))
if home:
    for item in home.links:
        if item.get('tag') != 'a':
            continue
        href = item.get('href', '')
        low = href.lower()
        if 'xjtlu.edu.cn' in low:
            err(f'Homepage contains visible official XJTLU external link: {href}')
        if any(k in low for k in ('/apply', 'application-portal', 'how-to-apply', 'apply-now')):
            err(f'Homepage contains direct application link: {href}')

# Live Preview checks for every sitemap URL plus robots/sitemap/verification file.
def fetch_status(url: str, timeout=15) -> tuple[int | None, str]:
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return getattr(r, 'status', 200), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'

for prod_url in sorted(sitemap_urls):
    parsed = urllib.parse.urlsplit(prod_url)
    preview_url = PREVIEW + (parsed.path or '/')
    status, final = fetch_status(preview_url)
    if status != 200:
        err(f'Preview URL not 200: {preview_url} -> {status} ({final})')

for path in ('/robots.txt', '/sitemap.xml'):
    status, final = fetch_status(PREVIEW + path)
    if status != 200:
        err(f'Preview system file not 200: {PREVIEW + path} -> {status} ({final})')

for vf in ROOT.glob('google*.html'):
    status, final = fetch_status(PREVIEW + '/' + vf.name)
    if status != 200:
        warn(f'Preview Google verification file not 200: {vf.name} -> {status} ({final})')

# Soft-check external anchor URLs. 404/410 are hard errors; anti-bot statuses are warnings.
for url in sorted(external_anchors):
    status, final = fetch_status(url, timeout=10)
    if status in {404, 410}:
        err(f'External link appears dead ({status}): {url}')
    elif status is None or (status >= 400 if status else False):
        warn(f'External link could not be cleanly verified ({status}): {url} -> {final}')

print('\n=== PREDEPLOY AUDIT SUMMARY ===')
print(f'HTML pages: {len(html_files)}')
print(f'Indexable pages: {len(indexable)}')
print(f'Sitemap URLs: {len(sitemap_urls)}')
print(f'External anchor URLs checked: {len(external_anchors)}')
print(f'Errors: {len(errors)}')
print(f'Warnings: {len(warnings)}')

if warnings:
    print('\nWARNINGS:')
    for x in warnings:
        print('-', x)
if errors:
    print('\nERRORS:')
    for x in errors:
        print('-', x)
    sys.exit(1)

print('\nPASS: no blocking predeploy errors found.')
