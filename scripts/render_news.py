from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "news" / "news-data.json"
NEWS_INDEX_PATH = ROOT / "news" / "index.html"
HOME_PATH = ROOT / "index.html"
SITEMAP_PATH = ROOT / "sitemap.xml"
SITE_URL = "https://xjtlu-korea.netlify.app"
VISIBLE_STATUSES = {"preview_ready", "approved", "published"}

HOME_START = "<!-- NEWS_ITEMS_START -->"
HOME_END = "<!-- NEWS_ITEMS_END -->"
INDEX_START = "<!-- NEWS_INDEX_ITEMS_START -->"
INDEX_END = "<!-- NEWS_INDEX_ITEMS_END -->"
JSON_START = "<!-- NEWS_ITEMLIST_JSON_START -->"
JSON_END = "<!-- NEWS_ITEMLIST_JSON_END -->"


def load_data() -> dict:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if data.get("site") != "xjtlu-korea" or data.get("language") != "ko":
        raise ValueError("news-data.json의 site/language 값이 올바르지 않습니다")
    if not isinstance(data.get("items"), list):
        raise ValueError("news-data.json의 items는 배열이어야 합니다")
    return data


def safe_text(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def validate_item(item: dict) -> dict:
    required = ["id", "title", "summary", "date", "source_date", "source_url", "category", "status", "sections"]
    missing = [key for key in required if not item.get(key)]
    if missing:
        raise ValueError(f"뉴스 항목 필수값 누락 ({item.get('id', 'unknown')}): {', '.join(missing)}")

    slug = str(item["id"])
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError(f"뉴스 id는 영문 소문자·숫자·하이픈만 사용할 수 있습니다: {slug}")

    for key in ("date", "source_date"):
        try:
            date.fromisoformat(str(item[key]))
        except ValueError as exc:
            raise ValueError(f"{slug}의 {key}는 YYYY-MM-DD 형식이어야 합니다") from exc

    source = urlparse(str(item["source_url"]))
    if source.scheme != "https" or source.netloc != "www.xjtlu.edu.cn" or not source.path.startswith("/en/news/"):
        raise ValueError(f"{slug}의 출처는 XJTLU 공식 뉴스 상세 주소여야 합니다")

    if item.get("personal_story") is True:
        raise ValueError(f"개인 학생·졸업생 사례는 자동 뉴스에 게시할 수 없습니다: {slug}")
    if item.get("content_type", "official_update") != "official_update":
        raise ValueError(f"허용되지 않은 content_type입니다: {slug}")
    if not isinstance(item["sections"], list) or not item["sections"]:
        raise ValueError(f"{slug}에는 최소 한 개의 본문 섹션이 필요합니다")

    item = dict(item)
    item["url"] = f"/news/{slug}.html"
    return item


def replace_between(text: str, start: str, end: str, body: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"렌더링 마커가 없거나 중복되었습니다: {start} / {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{body}\n{end}{after}"


def render_card(item: dict, compact: bool = False) -> str:
    summary = safe_text(item["summary"])
    if compact and len(summary) > 130:
        summary = summary[:127].rstrip() + "…"
    return (
        '<article class="news-card">'
        f'<div class="news-meta">{safe_text(item["source_date"])} · {safe_text(item["category"])}</div>'
        f'<h3><a href="{safe_text(item["url"])}">{safe_text(item["title"])}</a></h3>'
        f'<p>{summary}</p>'
        f'<a class="news-more" href="{safe_text(item["url"])}">기사 자세히 보기 →</a>'
        "</article>"
    )


def render_empty(message: str) -> str:
    return f'<div class="news-empty">{safe_text(message)}</div>'


def render_article(item: dict) -> str:
    sections = []
    for section in item["sections"]:
        heading = safe_text(section.get("heading"))
        paragraphs = section.get("paragraphs") or []
        if not heading or not isinstance(paragraphs, list) or not paragraphs:
            raise ValueError(f"{item['id']}의 각 섹션에는 heading과 paragraphs가 필요합니다")
        body = "".join(f"<p>{safe_text(p)}</p>" for p in paragraphs)
        sections.append(f"<section><h2>{heading}</h2>{body}</section>")

    canonical = f"{SITE_URL}{item['url']}"
    article_json = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": item["title"],
        "description": item["summary"],
        "datePublished": item["date"],
        "dateModified": item.get("reviewed_at") or item["date"],
        "mainEntityOfPage": canonical,
        "inLanguage": "ko-KR",
        "publisher": {"@type": "Organization", "name": "TNS유학 ㈜티앤에스월드와이드"},
        "isBasedOn": item["source_url"],
    }
    json_ld = json.dumps(article_json, ensure_ascii=False, separators=(",", ":"))

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{safe_text(item['title'])} | XJTLU 뉴스 | TNS유학</title>
<meta name="description" content="{safe_text(item['summary'])}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="XJTLU Korea | TNS유학">
<meta property="og:title" content="{safe_text(item['title'])}">
<meta property="og:description" content="{safe_text(item['summary'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ko_KR">
<script type="application/ld+json">{json_ld}</script>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--navy:#14213d;--gold:#c9a84c;--cream:#faf8f4;--ink:#171a21;--mid:#667085;--rule:#e4e7ec}}*{{box-sizing:border-box}}body{{margin:0;font-family:'Noto Sans KR',sans-serif;color:var(--ink);line-height:1.85;word-break:keep-all;background:var(--cream)}}.top{{background:#0e1a2e;color:#d7dce6;padding:9px 5vw;font-size:12px}}nav{{height:68px;background:#fff;border-bottom:1px solid var(--rule);display:flex;align-items:center;justify-content:space-between;padding:0 5vw}}nav a{{color:var(--navy);text-decoration:none;font-weight:700}}.brand{{font-size:22px;font-weight:900}}.brand span{{color:var(--gold)}}header{{background:linear-gradient(120deg,#0e1a2e,#243a63);color:#fff;padding:78px 0}}.wrap{{width:min(850px,90vw);margin:auto}}.eyebrow{{font-family:'DM Mono',monospace;color:var(--gold);font-size:11px;letter-spacing:.15em}}h1{{font-size:clamp(34px,5vw,54px);line-height:1.25;margin:15px 0 18px}}header p{{color:rgba(255,255,255,.76);font-size:17px}}main{{padding:65px 0}}section{{margin-bottom:46px}}h2{{color:var(--navy);font-size:27px;line-height:1.4}}p{{font-size:16px;color:#3f4755}}.source{{border-top:1px solid var(--rule);padding-top:20px;font-size:13px;color:var(--mid)}}.source a{{color:#596273}}.notice{{background:#fff;border-left:4px solid var(--gold);padding:20px 22px;font-size:13px;color:#596273}}.links{{background:#fff;border:1px solid var(--rule);padding:24px}}.links a{{display:inline-block;margin:5px 12px 5px 0;color:var(--navy);font-weight:700}}.cta{{background:var(--navy);color:#fff;padding:35px;text-align:center}}.cta h2{{color:#fff}}.btn{{display:inline-block;background:#fee500;color:#151000;text-decoration:none;font-weight:700;padding:12px 22px;margin:6px}}.btn.phone{{background:#fff;color:var(--navy)}}footer{{background:#0a0d18;color:#9ca3af;padding:30px 5vw;font-size:12px}}@media(max-width:620px){{header{{padding:55px 0}}main{{padding:45px 0}}h1{{font-size:34px}}}}
</style>
</head>
<body>
<div class="top">XJTLU 한국어 입학 안내 · TNS유학</div>
<nav><a class="brand" href="/">XJTLU <span>Korea</span></a><a href="/news/">뉴스 목록</a></nav>
<header><div class="wrap"><div class="eyebrow">XJTLU OFFICIAL NEWS · KOREAN EDITORIAL</div><h1>{safe_text(item['title'])}</h1><p>{safe_text(item['summary'])}</p></div></header>
<main class="wrap">
<div class="notice">이 글은 XJTLU 공식 발표를 한국 독자가 이해하기 쉽게 핵심 내용과 배경을 다시 정리한 TNS유학의 편집 콘텐츠입니다. 원문 전체 번역은 아니며, 최종 내용은 아래 공식 출처에서 확인할 수 있습니다.</div>
{''.join(sections)}
<section class="source"><strong>자료 출처</strong> · 원문 게시일 {safe_text(item['source_date'])}<br><a href="{safe_text(item['source_url'])}" target="_blank" rel="noopener">XJTLU 공식 뉴스 원문 확인 →</a></section>
<section class="links"><strong>함께 확인할 안내</strong><br><a href="/xjtlu-admission-requirements-korea-2027.html">입학조건·편입</a><a href="/xjtlu-tuition-scholarships-2027.html">학비·장학금</a><a href="/xjtlu-dual-degree-liverpool-2plus2.html">복수학위·2+2</a><a href="/xjtlu-programmes-careers-graduate-destinations.html">전공·진로</a></section>
<section class="cta"><h2>XJTLU 지원 가능성 확인</h2><p style="color:rgba(255,255,255,.75)">현재 학교·성적·희망 전공을 알려주시면 지원 절차를 안내해 드립니다.</p><a class="btn" href="https://open.kakao.com/o/slehLvKi" target="_blank" rel="noopener">카카오톡 무료 상담</a><a class="btn phone" href="tel:01051500105">전화상담 010-5150-0105</a></section>
</main>
<footer>© 2026 TNS Worldwide Co., Ltd. · 공식 발표의 변경·정정 여부는 원문에서 최종 확인해 주세요.</footer>
</body>
</html>
'''


def update_sitemap(items: list[dict]) -> None:
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    root = ET.parse(SITEMAP_PATH).getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    wanted = {f"{SITE_URL}/news/": date.today().isoformat()}
    wanted.update({f"{SITE_URL}{item['url']}": item["date"] for item in items})
    existing = {}
    for url_node in root.findall(f"{ns}url"):
        loc = url_node.find(f"{ns}loc")
        if loc is not None and loc.text:
            existing[loc.text] = url_node
    for loc, lastmod in wanted.items():
        node = existing.get(loc)
        if node is None:
            node = ET.SubElement(root, f"{ns}url")
            ET.SubElement(node, f"{ns}loc").text = loc
        lm = node.find(f"{ns}lastmod")
        if lm is None:
            lm = ET.SubElement(node, f"{ns}lastmod")
        lm.text = lastmod
    ET.indent(root, space="  ")
    SITEMAP_PATH.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main(check: bool = False) -> int:
    data = load_data()
    items = [validate_item(item) for item in data["items"] if item.get("status") in VISIBLE_STATUSES]
    items.sort(key=lambda item: (item["source_date"], int(item.get("priority", 0)), item["id"]), reverse=True)

    homepage = HOME_PATH.read_text(encoding="utf-8")
    home_body = "\n".join(render_card(item, compact=True) for item in items[:3]) or render_empty("검토 승인된 새 소식이 준비되면 이곳에 표시됩니다.")
    homepage = replace_between(homepage, HOME_START, HOME_END, home_body)

    news_index = NEWS_INDEX_PATH.read_text(encoding="utf-8")
    index_body = "\n".join(render_card(item) for item in items) or render_empty("현재 검토 승인된 뉴스가 없습니다. XJTLU 공식 발표를 확인한 뒤 순차적으로 업데이트합니다.")
    news_index = replace_between(news_index, INDEX_START, INDEX_END, index_body)
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "XJTLU 한국어 뉴스",
        "itemListElement": [
            {"@type": "ListItem", "position": idx, "url": f"{SITE_URL}{item['url']}", "name": item["title"]}
            for idx, item in enumerate(items, start=1)
        ],
    }
    news_index = replace_between(
        news_index,
        JSON_START,
        JSON_END,
        '<script type="application/ld+json">' + json.dumps(item_list, ensure_ascii=False, separators=(",", ":")) + "</script>",
    )

    if check:
        if homepage != HOME_PATH.read_text(encoding="utf-8") or news_index != NEWS_INDEX_PATH.read_text(encoding="utf-8"):
            raise SystemExit("렌더링 결과가 저장소 파일과 다릅니다. python scripts/render_news.py를 실행하세요.")
        return 0

    HOME_PATH.write_text(homepage, encoding="utf-8")
    NEWS_INDEX_PATH.write_text(news_index, encoding="utf-8")
    for item in items:
        (ROOT / item["url"].lstrip("/")).write_text(render_article(item), encoding="utf-8")
    update_sitemap(items)
    print(f"Rendered {len(items)} approved/review-ready XJTLU Korea news item(s)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(check=args.check))
