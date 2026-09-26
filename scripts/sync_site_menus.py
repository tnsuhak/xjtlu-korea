from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"

CAREER_MENU_LABEL = "한국학생 취업·진로 통계"
OLD_CAREER_MENU_LABELS = ("한국인 취업·진로 현황", "한국인 진로 사례")

DETAIL_MENU = """<div id="detailSiteMenu" class="detail-site-menu" aria-label="XJTLU Korea 전체 메뉴" aria-hidden="true">
  <div class="detail-site-menu-inner">
    <div class="detail-site-menu-head">
      <div class="detail-site-menu-headcopy"><span>XJTLU KOREA</span><h2>전체 메뉴</h2><p>메인 페이지의 주제와 관련 상세페이지를 함께 확인하세요.</p></div>
      <button type="button" class="detail-site-menu-close" onclick="closeDetailSiteMenu()" aria-label="전체 메뉴 닫기">✕</button>
    </div>
    <div class="detail-site-menu-grid">
      <section class="detail-site-menu-group"><h3><a href="/#information">학교소개 <small>메인에서 보기 →</small></a></h3><a href="/xjtlu-dual-degree-liverpool-2plus2.html">리버풀대학교 복수학위·2+2</a><a href="/xjtlu-exchange.html">XJTLU 교환학생</a><a href="/xjtlu-suzhou-china-life.html">XJTLU 쑤저우 소개</a></section>
      <section class="detail-site-menu-group"><h3><a href="/#admission">학부 입학 <small>메인에서 보기 →</small></a></h3><a href="/xjtlu-admission-requirements-korea-2027.html">2027 학부 입학조건·편입</a><a href="/xjtlu-tuition-scholarships-2027.html">2027 학부 학비·장학금</a><a href="/xjtlu-living-cost-2027.html">XJTLU 생활비 2027</a></section>
      <section class="detail-site-menu-group"><h3><a href="/xjtlu-undergraduate-programmes.html">학부 전공·진로 <small>전체 보기 →</small></a></h3><a href="/xjtlu-undergraduate-programmes.html">학부 전공 전체 보기</a><a href="/xjtlu-graduate-destinations-careers.html">졸업 후 진로·대학원 진학</a><a href="/xjtlu-alumni-careers.html">한국학생 취업·진로 통계</a></section>
      <section class="detail-site-menu-group"><h3><a href="/masters/">석사 <small>석사 홈 →</small></a></h3><a href="/masters/programmes.html">석사 전공 전체 보기</a><a href="/masters/admission-requirements-2027.html">2027 석사 입학조건</a><a href="/masters/tuition-scholarships-2027.html">2027 석사 학비·장학금</a></section>
      <section class="detail-site-menu-group"><h3><a href="/#campus-life">학생생활 <small>메인에서 보기 →</small></a></h3><a href="/xjtlu-accommodation-sip-taicang.html">SIP·Taicang 숙소·기숙사</a><a href="/xjtlu-suzhou-china-life.html">XJTLU 쑤저우 소개</a><a href="/xjtlu-sports-facilities.html">스포츠·헬스장 시설</a><a href="/xjtlu-clubs-student-organisations.html">동아리·학생단체</a><a href="/xjtlu-student-videos.html">XJTLU 학생 후기 영상</a></section>
      <section class="detail-site-menu-group"><h3><a href="/#news">뉴스 <small>메인에서 보기 →</small></a></h3><a href="/news/">XJTLU 최신 뉴스 전체 보기</a></section>
      <section class="detail-site-menu-group"><h3><a href="/#contact">상담 <small>메인에서 보기 →</small></a></h3><p>입학조건·학비·전공·숙소 상담은 TNS유학에서 안내합니다.</p><div class="detail-site-menu-cta"><a class="kakao" href="https://open.kakao.com/o/slehLvKi" target="_blank" rel="noopener">카카오톡 상담</a><a class="phone" href="tel:01051500105">전화상담</a></div></section>
    </div>
  </div>
</div>"""

EXPECTED_GROUPS = (
    "학교소개",
    "학부 입학",
    "학부 전공·진로",
    "석사",
    "학생생활",
    "뉴스",
    "상담",
)


def sync_home_menu() -> bool:
    text = HOME.read_text(encoding="utf-8")
    start = text.find('<div id="mobileNav">')
    end = text.find("<!-- ====== HERO ====== -->", start)
    if start < 0 or end < 0:
        raise SystemExit("index.html 메뉴 영역을 찾지 못했습니다")

    menu_region = text[start:end]
    for old in OLD_CAREER_MENU_LABELS:
        menu_region = menu_region.replace(old, CAREER_MENU_LABEL)

    updated = text[:start] + menu_region + text[end:]
    changed = updated != text
    if changed:
        HOME.write_text(updated, encoding="utf-8")
    return changed


def sync_detail_menu(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    start = text.find('<div id="detailSiteMenu"')
    if start < 0:
        raise SystemExit(f"상세 메뉴 시작점을 찾지 못했습니다: {path.name}")
    hero = text.find('<header class="hero"', start)
    if hero < 0:
        raise SystemExit(f"상세 메뉴 뒤 hero를 찾지 못했습니다: {path.name}")

    updated = text[:start] + DETAIL_MENU + "\n\n" + text[hero:]
    changed = updated != text
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def validate() -> None:
    home = HOME.read_text(encoding="utf-8")
    start = home.find('<div id="mobileNav">')
    end = home.find("<!-- ====== HERO ====== -->", start)
    region = home[start:end]
    if CAREER_MENU_LABEL not in region:
        raise SystemExit("메인 메뉴에 한국학생 취업·진로 통계가 없습니다")
    for old in OLD_CAREER_MENU_LABELS:
        if old in region:
            raise SystemExit(f"메인 메뉴에 구형 진로 라벨이 남아 있습니다: {old}")

    for path in sorted(ROOT.glob("xjtlu-*.html")):
        text = path.read_text(encoding="utf-8")
        start = text.find('<div id="detailSiteMenu"')
        hero = text.find('<header class="hero"', start)
        if start < 0 or hero < 0:
            raise SystemExit(f"상세 메뉴 검증 실패: {path.name}")
        menu = text[start:hero]
        positions = [menu.find(f">{label} <small>") for label in EXPECTED_GROUPS]
        if any(pos < 0 for pos in positions) or positions != sorted(positions):
            raise SystemExit(f"메뉴 그룹/순서 불일치: {path.name}")
        if CAREER_MENU_LABEL not in menu:
            raise SystemExit(f"진로 메뉴 라벨 불일치: {path.name}")
        for old in OLD_CAREER_MENU_LABELS:
            if old in menu:
                raise SystemExit(f"구형 진로 라벨이 남아 있습니다: {path.name}: {old}")


def main() -> int:
    sync_home_menu()
    for path in sorted(ROOT.glob("xjtlu-*.html")):
        sync_detail_menu(path)
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
