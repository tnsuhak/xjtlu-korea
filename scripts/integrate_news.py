from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
DATA = ROOT / "news" / "news-data.json"
NEWS_INDEX = ROOT / "news" / "index.html"
NEWS_DIR = ROOT / "news"

HOME_START = "<!-- NEWS_ITEMS_START -->"
HOME_END = "<!-- NEWS_ITEMS_END -->"

NEW_ITEM = {
    "id": "xjtlu-aiat-aolns-restructured-academies-2026",
    "title": "XJTLU, AI·첨단기술과 생명·자연과학 분야 학부 체계 개편",
    "summary": "XJTLU가 2026년 9월 AI·컴퓨터·전자전기·통신 분야를 아우르는 AIAT와 생명과학·약학·바이오·디지털헬스 등을 아우르는 AoLNS를 새롭게 출범했습니다. 2027학년도 관련 전공을 검토하는 학생이라면 달라진 학문 조직과 전공 구성을 확인할 필요가 있습니다.",
    "date": "2026-09-14",
    "source_date": "2026-09-01",
    "source_url": "https://www.xjtlu.edu.cn/en/news/2026/09/two-restructured-academies-to-launch-in-september",
    "category": "전공·학부 개편",
    "priority": 40,
    "status": "preview_ready",
    "content_type": "official_update",
    "personal_story": False,
    "reviewed_at": "2026-09-14",
    "sections": [
        {
            "heading": "AIAT: AI부터 전자전기·통신까지",
            "paragraphs": [
                "Academy of AI and Advanced Technology(AIAT)는 기존 School of Advanced Technology와 School of AI and Advanced Computing을 바탕으로 구성됐습니다. 인공지능, 컴퓨터과학, 전기·전자공학, 통신공학 분야를 한 조직 안에서 연결합니다.",
                "XJTLU 공식 발표 기준 AIAT는 학부 9개, 석사 10개, 박사 3개 프로그램을 운영하며 AI·알고리즘·데이터과학뿐 아니라 컴퓨터 시스템, 소프트웨어공학, 통신, 전기공학, 메카트로닉스 등을 폭넓게 다룹니다."
            ]
        },
        {
            "heading": "AoLNS: 생명과학·약학·바이오·디지털헬스 통합",
            "paragraphs": [
                "Academy of Life and Natural Sciences(AoLNS)는 기존 School of Science와 Wisdom Lake Academy of Pharmacy를 통합해 출범했습니다. 생물·의생명과학, 화학·재료과학, 약학·바이오의약공학, AI·통계·바이오인포매틱스, 디지털헬스, 환경·One Health 등을 연결하는 구조입니다.",
                "공식 발표 기준 AoLNS는 학부 10개, 석사 9개, 박사 5개 프로그램을 운영합니다. 약학이나 생명과학을 전통적인 단일 전공으로만 보기보다 AI·데이터·바이오의약·헬스 분야와 결합하려는 방향이 뚜렷합니다."
            ]
        },
        {
            "heading": "2027학년도 전공 선택에서 확인할 점",
            "paragraphs": [
                "2027학년도 XJTLU 진학을 검토한다면 이번 변화는 대학 조직도 이상의 의미가 있습니다. AI·컴퓨터·전자전기 계열과 생명·약학 계열 모두 인접 분야를 연결하는 교육·연구 구조가 강화되고 있습니다.",
                "다만 조직 개편이 개별 전공의 입학조건이나 학위명 변경을 자동으로 의미하는 것은 아닙니다. 실제 지원 시에는 희망 전공의 최신 커리큘럼, 학위명, 2+2 가능 여부와 입학요건을 각각 확인해야 합니다."
            ]
        }
    ]
}

NEWS_CSS = r'''
/* TNS NEWS SECTION START */
#news .news-head-row{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:28px}
#news .news-all{display:inline-flex;align-items:center;gap:8px;color:var(--navy);font-size:13px;font-weight:800;text-decoration:none;white-space:nowrap;border-bottom:1px solid #cfd5df;padding-bottom:4px}
#news .news-all:hover{color:#8b6a1f;border-color:var(--gold)}
#news .home-news-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
#news .news-card{background:#fff;border:1px solid #e4e7ec;padding:22px 20px;display:flex;flex-direction:column;min-height:250px;box-shadow:0 5px 16px rgba(20,33,61,.04)}
#news .news-meta{font-family:'DM Mono',monospace;font-size:9.5px;line-height:1.5;color:#9a7827;margin-bottom:10px}
#news .news-card h3{font-size:16px;line-height:1.5;margin:0 0 10px}
#news .news-card h3 a{color:var(--navy);text-decoration:none}
#news .news-card h3 a:hover{color:#8b6a1f}
#news .news-card p{font-size:12.5px;line-height:1.65;color:#667085;margin:0 0 16px}
#news .news-more{margin-top:auto;color:var(--navy);font-size:12px;font-weight:800;text-decoration:none}
#news .news-empty{grid-column:1/-1;background:#fff;border:1px dashed #cbd5e1;padding:32px;text-align:center;color:#667085;font-size:13px}
@media(max-width:980px){#news .home-news-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:620px){#news .news-head-row{align-items:flex-start;flex-direction:column;gap:10px;margin-bottom:20px}#news .home-news-grid{grid-template-columns:1fr}#news .news-card{min-height:0;padding:19px 17px}}
/* TNS NEWS SECTION END */
'''

NEWS_SECTION = r'''
<!-- ====== 최신 뉴스 ====== -->
<div class="sec-alt" id="news">
  <div class="sec fi">
    <div class="news-head-row">
      <div>
        <p class="label">XJTLU NEWS</p>
        <h2 class="sec-h">XJTLU 최신 소식</h2>
        <p class="sec-p">XJTLU 공식 발표 중 한국 학생과 학부모에게 필요한 입학·전공·진로·한국 협력 소식을 선별해 정리합니다.</p>
      </div>
      <a class="news-all" href="/news/">뉴스 전체 보기 →</a>
    </div>
    <div class="home-news-grid">
<!-- NEWS_ITEMS_START -->
<div class="news-empty">검토 승인된 최신 소식을 불러오는 중입니다.</div>
<!-- NEWS_ITEMS_END -->
    </div>
  </div>
</div>
'''

def load_data() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))

def write_data(data: dict) -> None:
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def add_latest_item() -> None:
    data = load_data()
    items = data.setdefault("items", [])
    ids = {item.get("id") or item.get("slug") for item in items}
    if NEW_ITEM["id"] not in ids:
        items.append(NEW_ITEM)
        data["updated_at"] = "2026-09-17"
        write_data(data)

def ensure_home_scaffold() -> None:
    text = HOME.read_text(encoding="utf-8")

    if "/* TNS NEWS SECTION START */" not in text:
        if "</style>" not in text:
            raise ValueError("index.html 기본 style 종료 태그를 찾지 못했습니다")
        text = text.replace("</style>", NEWS_CSS + "\n</style>", 1)

    desktop_anchor = '    <li><a href="#reviews">학생후기</a></li>\n    <li><button type="button" class="nav-menu-btn"'
    if 'href="#news">뉴스</a></li>' not in text:
        if desktop_anchor not in text:
            raise ValueError("데스크톱 뉴스 메뉴 삽입 위치를 찾지 못했습니다")
        text = text.replace(
            desktop_anchor,
            '    <li><a href="#reviews">학생후기</a></li>\n'
            '    <li><a href="#news">뉴스</a></li>\n'
            '    <li><button type="button" class="nav-menu-btn"',
            1,
        )

    mobile_anchor = '<a href="#campus-life">학생생활</a><a href="#reviews">학생후기</a>'
    if '<a href="#reviews">학생후기</a><a href="#news">뉴스</a>' not in text:
        if mobile_anchor not in text:
            raise ValueError("모바일 뉴스 메뉴 삽입 위치를 찾지 못했습니다")
        text = text.replace(
            mobile_anchor,
            mobile_anchor + '<a href="#news">뉴스</a>',
            1,
        )

    site_menu_news = '<section class="site-menu-group"><h3><a href="#news">뉴스 <small>메인에서 보기 →</small></a></h3><a href="/news/">XJTLU 최신 뉴스 전체 보기</a></section>'
    if site_menu_news not in text:
        contact_anchor = '      <section class="site-menu-group"><h3><a href="#contact">입학문의'
        if contact_anchor not in text:
            raise ValueError("전체 메뉴 뉴스 삽입 위치를 찾지 못했습니다")
        text = text.replace(contact_anchor, "      " + site_menu_news + "\n" + contact_anchor, 1)

    if HOME_START not in text or HOME_END not in text:
        cta_anchor = "\n<!-- CTA -->"
        if cta_anchor not in text:
            raise ValueError("홈페이지 뉴스 섹션 삽입 위치를 찾지 못했습니다")
        text = text.replace(cta_anchor, "\n" + NEWS_SECTION.strip() + "\n" + cta_anchor, 1)

    text = text.replace('<a class="related-link" href="xjtlu-suzhou-china-life.html">쑤저우 생활 자세히 보기<span class="arr">→</span></a>', '')
    text = text.replace('<a class="related-link" href="xjtlu-living-cost-2027.html">생활비 2027<span class="arr">→</span></a>', '')

    HOME.write_text(text, encoding="utf-8")

def safe_text(value: object) -> str:
    return html.escape(str(value or ""), quote=True)

def render_home_card(item: dict) -> str:
    summary = safe_text(item["summary"])
    if len(summary) > 130:
        summary = summary[:127].rstrip() + "…"
    url = f'/news/{item["id"]}.html'
    return (
        '<article class="news-card">'
        f'<div class="news-meta">{safe_text(item["source_date"])} · {safe_text(item["category"])}</div>'
        f'<h3><a href="{url}">{safe_text(item["title"])}</a></h3>'
        f'<p>{summary}</p>'
        f'<a class="news-more" href="{url}">기사 자세히 보기 →</a>'
        "</article>"
    )

def replace_between(text: str, start: str, end: str, body: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"렌더링 마커 오류: {start} / {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{body}\n{end}{after}"

def patch_home_latest_four() -> None:
    data = load_data()
    visible = {"preview_ready", "approved", "published"}
    items = [item for item in data.get("items", []) if item.get("status") in visible]
    items.sort(key=lambda item: (item.get("source_date", ""), int(item.get("priority", 0)), item.get("id", "")), reverse=True)
    body = "\n".join(render_home_card(item) for item in items[:4])
    text = HOME.read_text(encoding="utf-8")
    text = replace_between(text, HOME_START, HOME_END, body)
    HOME.write_text(text, encoding="utf-8")

def modernize_news_pages() -> None:
    old_programme_link = '<a href="/xjtlu-programmes-careers-graduate-destinations.html">전공·진로</a>'
    new_programme_links = (
        '<a href="/xjtlu-undergraduate-programmes.html">학부 전공</a>'
        '<a href="/xjtlu-graduate-destinations-careers.html">졸업 후 진로·대학원</a>'
    )
    for path in sorted(NEWS_DIR.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if '<link rel="icon" href="/favicon.svg" type="image/svg+xml">' not in text:
            text = text.replace("<head>\n", '<head>\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n', 1)
        text = text.replace("XJTLU 한국어 입학 안내 · TNS유학", "XJTLU 한국 공식 대표 · TNS Worldwide")
        text = text.replace(old_programme_link, new_programme_links)
        path.write_text(text, encoding="utf-8")

def prepare() -> None:
    add_latest_item()
    ensure_home_scaffold()

def finalize() -> None:
    patch_home_latest_four()
    modernize_news_pages()

def check() -> None:
    data = load_data()
    ids = {item.get("id") for item in data.get("items", [])}
    if NEW_ITEM["id"] not in ids:
        raise SystemExit("최신 AIAT/AoLNS 뉴스가 news-data.json에 없습니다")

    home = HOME.read_text(encoding="utf-8")
    if home.count(HOME_START) != 1 or home.count(HOME_END) != 1:
        raise SystemExit("홈페이지 뉴스 마커가 올바르지 않습니다")
    if 'href="#news">뉴스</a>' not in home:
        raise SystemExit("홈페이지 뉴스 메뉴가 없습니다")
    between = home.split(HOME_START, 1)[1].split(HOME_END, 1)[0]
    if between.count('<article class="news-card">') != 4:
        raise SystemExit("홈페이지 최신 뉴스는 4건이어야 합니다")
    if '>쑤저우 생활 자세히 보기<' in home or '>생활비 2027<' in home:
        raise SystemExit("캠퍼스 생활 섹션에 제거 대상 링크가 남아 있습니다")

    news_index = NEWS_INDEX.read_text(encoding="utf-8")
    if "XJTLU 한국 공식 대표 · TNS Worldwide" not in news_index:
        raise SystemExit("뉴스 인덱스 대표자 표기가 최신 상태가 아닙니다")

    for path in NEWS_DIR.glob("*.html"):
        text = path.read_text(encoding="utf-8")
        if "xjtlu-programmes-careers-graduate-destinations.html" in text:
            raise SystemExit(f"삭제된 전공/진로 통합 URL이 남아 있습니다: {path}")
        if '<link rel="icon" href="/favicon.svg" type="image/svg+xml">' not in text:
            raise SystemExit(f"favicon이 없습니다: {path}")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.prepare:
        prepare()
    if args.finalize:
        finalize()
    if args.check:
        check()
    if not (args.prepare or args.finalize or args.check):
        prepare()
        finalize()
        check()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())