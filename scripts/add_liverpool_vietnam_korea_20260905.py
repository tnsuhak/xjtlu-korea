from pathlib import Path

ROOT = Path('.')
INDEX = ROOT / 'index.html'
DUAL = ROOT / 'xjtlu-dual-degree-liverpool-2plus2.html'
SITEMAP = ROOT / 'sitemap.xml'
PAGE = ROOT / 'university-of-liverpool-vietnam.html'

PAGE_HTML = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>리버풀대학교와 베트남 협력 | 교육·AI·의료 네트워크 | XJTLU Korea</title>
<meta name="description" content="영국 리버풀과 베트남의 City2City 협력, 리버풀대학교-호치민시 의약대 협력, 의료·문화 교류까지 2025~2026 주요 사례를 한국어로 정리했습니다.">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="https://xjtlu-korea.netlify.app/university-of-liverpool-vietnam.html">
<meta property="og:type" content="article">
<meta property="og:site_name" content="XJTLU Korea | TNS유학">
<meta property="og:title" content="리버풀대학교와 베트남 협력 | 교육·AI·의료 네트워크">
<meta property="og:description" content="리버풀과 베트남의 교육·의료·AI·문화 협력 사례 5가지를 정리했습니다.">
<meta property="og:url" content="https://xjtlu-korea.netlify.app/university-of-liverpool-vietnam.html">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"리버풀대학교와 베트남: 교육·AI·의료 네트워크","description":"2025~2026 리버풀과 베트남의 교육·의료·AI·문화 협력 사례","dateModified":"2026-09-05","inLanguage":"ko-KR","mainEntityOfPage":"https://xjtlu-korea.netlify.app/university-of-liverpool-vietnam.html","publisher":{"@type":"Organization","name":"TNS유학 ㈜티앤에스월드와이드"},"about":[{"@type":"CollegeOrUniversity","name":"University of Liverpool"},{"@type":"CollegeOrUniversity","name":"Xi'an Jiaotong-Liverpool University","alternateName":"XJTLU"}]}
</script>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--navy:#14213d;--deep:#0b1630;--gold:#c9a84c;--cream:#faf8f4;--paper:#fff;--ink:#171b26;--muted:#667085;--line:#e3e6ec;--jade:#1f6f78}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--cream);color:var(--ink);font-family:'Noto Sans KR',sans-serif;line-height:1.72;word-break:keep-all}.top{background:var(--deep);color:#cdd4e1;font-size:12px;padding:8px 5vw}.nav{height:68px;background:#fff;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 5vw;position:sticky;top:0;z-index:20}.brand{font-size:20px;font-weight:900;color:var(--navy);text-decoration:none}.brand span{color:var(--gold)}.navlinks{display:flex;gap:20px}.navlinks a{color:var(--navy);font-size:13px;text-decoration:none;font-weight:700}.wrap{width:min(1040px,90vw);margin:auto}.hero{background:radial-gradient(900px 500px at 82% 16%,#294d86 0,transparent 62%),linear-gradient(135deg,var(--deep),#172b4d);color:#fff;padding:72px 0 84px}.eyebrow{font-family:'DM Mono',monospace;color:var(--gold);font-size:11px;font-weight:700;letter-spacing:.15em}.hero h1{font-size:clamp(36px,6vw,58px);line-height:1.16;margin:12px 0 16px;max-width:850px}.hero p{margin:0;color:#d8deeb;font-size:16px;max-width:800px}.updated{margin-top:16px;color:#aeb8ca;font-size:12px}.answer{margin-top:-38px;background:#fff;border:1px solid var(--line);box-shadow:0 20px 55px rgba(20,33,61,.12);padding:25px 28px;position:relative}.answer small{display:block;color:var(--jade);font-size:11px;font-weight:800;letter-spacing:.08em}.answer h2{color:var(--navy);font-size:24px;line-height:1.35;margin:7px 0 9px}.answer p{margin:0;color:#4b5565;font-size:14px}.main{padding:60px 0 78px}.section{margin-bottom:56px}.section h2{color:var(--navy);font-size:30px;line-height:1.35;margin:0 0 12px}.lead{color:#4b5565;max-width:860px;margin:0 0 22px}.timeline{display:grid;gap:14px}.event{background:#fff;border:1px solid var(--line);padding:24px}.date{display:inline-block;background:#f3ead0;color:#7b6220;border-radius:999px;padding:5px 9px;font-family:'DM Mono',monospace;font-size:11px;font-weight:700}.event h3{color:var(--navy);font-size:20px;margin:11px 0 4px}.tag{color:#8a6d22;font-size:12px;font-weight:800}.event p{color:#4b5565;font-size:14px;margin:10px 0 0}.src{display:inline-block;margin-top:11px;color:var(--jade);font-size:12px;font-weight:800;text-decoration:none}.src:hover{text-decoration:underline}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#fff;border:1px solid var(--line);padding:22px}.card h3{color:var(--navy);font-size:17px;margin:0 0 8px}.card p{font-size:13.5px;color:#4b5565;margin:0}.note{background:#fff7df;border-left:4px solid var(--gold);padding:19px 21px;color:#596273;font-size:14px}.related{display:grid;grid-template-columns:1fr 1fr;gap:12px}.related a{background:#fff;border:1px solid var(--line);padding:18px;color:var(--navy);text-decoration:none;font-weight:800}.related span{display:block;color:var(--muted);font-size:12px;font-weight:400;margin-top:5px}.sources{border-top:1px solid var(--line);padding-top:16px;color:#8a92a2;font-size:12px;line-height:1.9}.sources a{color:#667085}.cta{background:var(--navy);color:#fff;padding:34px 28px;text-align:center}.cta h2{color:#fff;margin:0 0 8px}.cta p{margin:0;color:#d7ddea}.btn{display:inline-block;margin-top:14px;background:#fee500;color:#161000;text-decoration:none;padding:12px 20px;font-weight:800}.btn.alt{background:#fff;color:var(--navy);margin-left:6px}footer{padding:34px 5vw;background:#0a0d18;color:#9ca3af;font-size:12px}
@media(max-width:760px){.navlinks{display:none}.hero{padding:54px 0 70px}.hero p{font-size:15px}.answer{padding:20px}.main{padding:50px 0 64px}.section{margin-bottom:46px}.section h2{font-size:26px}.grid,.related{grid-template-columns:1fr}.event{padding:19px}.event h3{font-size:18px}.btn,.btn.alt{display:block;margin:10px auto 0;max-width:280px}}
</style>
</head>
<body>
<div class="top">XJTLU 한국어 입학 안내 · TNS유학</div>
<nav class="nav"><a class="brand" href="/">XJTLU <span>Korea</span></a><div class="navlinks"><a href="/">학교소개</a><a href="xjtlu-dual-degree-liverpool-2plus2.html">복수학위·2+2</a><a href="#contact">상담</a></div></nav>
<header class="hero"><div class="wrap"><div class="eyebrow">LIVERPOOL × VIETNAM</div><h1>리버풀대학교와 베트남,<br>연결이 빠르게 넓어지고 있습니다</h1><p>리버풀과 베트남의 연결은 대학 한 곳의 협력에 그치지 않고 도시·의료·교육·AI·문화 영역으로 확장되고 있습니다. XJTLU를 공동 설립한 University of Liverpool의 아시아 네트워크를 이해하는 데 도움이 되는 사례들입니다.</p><div class="updated">업데이트: 2026-09-05</div></div></header>
<div class="wrap"><section class="answer"><small>핵심 요약</small><h2>리버풀의 베트남 네트워크는 도시·대학·의료기관으로 이어지고 있습니다</h2><p>아래 사례는 영국-베트남 관계, 리버풀-호치민시 협력, University of Liverpool과 현지 대학·기관의 협력을 함께 보여줍니다. XJTLU와 University of Liverpool의 연결을 보다 넓은 아시아 네트워크 속에서 볼 수 있는 배경입니다.</p></section></div>
<main class="main"><div class="wrap">
<section class="section"><h2>주요 협력 사례 5가지</h2><p class="lead">2025년부터 2026년 사이 공식 기관들이 발표한 사례 중 성격이 겹치지 않고, 교육·연구·국제 네트워크를 이해하는 데 도움이 되는 내용을 골랐습니다.</p><div class="timeline">
<article class="event"><span class="date">03/2025</span><h3>리버풀 Alder Hey Children’s Hospital × 호치민시 어린이병원</h3><div class="tag">소아의료 · 임상서비스 · 연구 · 의료혁신</div><p>리버풀의 Alder Hey Children’s Hospital과 호치민시 Children’s Hospital 1이 임상서비스, 연구, 소아 의료혁신센터 개발을 포함한 협력 협약을 체결했습니다.</p><a class="src" href="https://www.alderhey.nhs.uk/alder-hey-sign-ground-breaking-agreement-with-childrens-hospital-in-vietnam/" target="_blank" rel="noopener">자료 출처: Alder Hey Children’s Hospital ↗</a></article>
<article class="event"><span class="date">29/10/2025</span><h3>영국 × 베트남</h3><div class="tag">포괄적 전략적 동반자 관계</div><p>영국과 베트남이 관계를 포괄적 전략적 동반자 관계로 격상했습니다. 교육, 과학기술, 무역 등 다양한 분야의 협력 확대가 포함됐습니다.</p><a class="src" href="https://www.gov.uk/government/news/joint-declaration-on-the-elevation-of-uk-viet-nam-relations-to-comprehensive-strategic-partnership" target="_blank" rel="noopener">자료 출처: 영국 정부 ↗</a></article>
<article class="event"><span class="date">30/10/2025</span><h3>리버풀 × 호치민시</h3><div class="tag">City2City · 교육 · 의료 · 과학기술</div><p>호치민시와 Liverpool City Region이 교육·훈련, 의료, 과학기술을 포함한 분야에서 협력하는 양해각서를 체결했습니다.</p><a class="src" href="https://mofahcm.gov.vn/tin-tuc/hoat-dong-doi-ngoai-tai-tphcm/thanh-pho-ho-chi-minh-ky-ket-ban-ghi-nho-hop-tac-voi-vung-do-thi-liverpool-vuong-quoc-anh" target="_blank" rel="noopener">자료 출처: 호치민시 외무국 ↗</a></article>
<article class="event"><span class="date">29/01/2026</span><h3>Liverpool Culture Festival in Ho Chi Minh City</h3><div class="tag">City2City · 문화 · 지역 교류</div><p>리버풀과 호치민시의 장기 City2City 협력의 일환으로 Liverpool Culture Festival이 호치민시에서 열렸습니다. Liverpool City Council, 영국 총영사관, British Council 등이 참여했습니다.</p><a class="src" href="https://cultureliverpool.co.uk/2026/liverpool-and-ho-chi-minh-city-mark-twinning-partnership-with-cultural-festival/" target="_blank" rel="noopener">자료 출처: Culture Liverpool ↗</a></article>
<article class="event"><span class="date">30/01/2026</span><h3>University of Liverpool × 호치민시 의약대학교(UMP)</h3><div class="tag">AI · Data Science · Digital Health · 공동연구</div><p>University of Liverpool과 University of Medicine and Pharmacy at Ho Chi Minh City가 장기 협력을 위한 MoU를 체결했습니다. 공중보건, 디지털헬스, 바이오메디컬 인포매틱스, AI·데이터 기반 의료혁신, 공동연구와 인적교류가 포함됩니다.</p><a class="src" href="https://news.liverpool.ac.uk/2026/01/30/liverpool-partners-with-university-of-medicine-and-pharmacy-at-ho-chi-minh-city/" target="_blank" rel="noopener">자료 출처: University of Liverpool ↗</a></article>
</div></section>
<section class="section"><h2>XJTLU를 볼 때 왜 의미가 있나요?</h2><div class="grid"><div class="card"><h3>리버풀대학교 네트워크</h3><p>XJTLU는 University of Liverpool과 Xi'an Jiaotong University가 공동 설립했습니다. 리버풀대학교의 국제 협력 범위를 함께 보면 XJTLU의 영국 연결성을 보다 넓게 이해할 수 있습니다.</p></div><div class="card"><h3>아시아에서 확장되는 접점</h3><p>베트남 사례는 리버풀의 아시아 접점이 학위·학생 이동뿐 아니라 도시, 의료, 연구, 문화 교류까지 넓어지고 있음을 보여줍니다.</p></div><div class="card"><h3>AI·데이터·의료의 실제 협력</h3><p>특히 UMP 협력은 AI, 데이터사이언스, 디지털헬스가 실제 공동연구 의제로 연결되고 있다는 점에서 공학·데이터·생명과학 관심 학생에게도 참고할 만합니다.</p></div></div></section>
<section class="section"><div class="note"><strong>XJTLU와의 연결을 이해하는 방법:</strong> XJTLU의 학위와 2+2 구조는 University of Liverpool과 직접 연결되어 있습니다. 이 페이지의 베트남 사례는 그 리버풀 네트워크가 아시아에서 어떻게 확장되고 있는지를 보여주는 추가 배경으로 보면 됩니다.</div></section>
<section class="section"><h2>관련 XJTLU 가이드</h2><div class="related"><a href="xjtlu-dual-degree-liverpool-2plus2.html">XJTLU 복수학위·리버풀대학교 2+2<span>중국 4년과 2+2, 타이창 2+1+1의 차이를 확인합니다.</span></a><a href="xjtlu-programmes-careers-graduate-destinations.html">XJTLU 전공·진로·대학원 진학<span>전공별 진로와 졸업 후 진학 방향을 확인합니다.</span></a></div></section>
<section class="section sources"><strong>자료 출처</strong><br>영국 정부, 호치민시 외무국, Alder Hey Children’s Hospital, Culture Liverpool, University of Liverpool의 공식 발표를 기준으로 정리했습니다. 외부 링크는 각 사례 카드에서 확인할 수 있습니다.</section>
<section class="cta" id="contact"><h2>XJTLU 입학과 리버풀대학교 학위 경로 상담</h2><p>희망 전공과 현재 학력을 알려주시면 XJTLU 입학, 복수학위, 2+2 가능 여부를 함께 확인해 드립니다.</p><a class="btn" href="https://open.kakao.com/o/slehLvKi" target="_blank" rel="noopener">카카오톡 무료 상담</a><a class="btn alt" href="tel:02-3288-1733">전화 02-3288-1733</a></section>
</div></main>
<footer>© 2026 TNS Worldwide Co., Ltd. · XJTLU 한국어 입학 안내</footer>
</body>
</html>'''


def patch_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f'Anchor not found: {old[:80]}')
    return text.replace(old, new, 1)


# Write/update the detail page.
PAGE.write_text(PAGE_HTML, encoding='utf-8')

# Homepage: keep this subtle. Add one related link and menu entries, not a new large section.
index = INDEX.read_text(encoding='utf-8')
if 'university-of-liverpool-vietnam.html' not in index:
    old = '<div class="related-links" aria-label="이 내용과 관련된 상세 가이드"><span class="related-label">관련 글</span><a class="related-link" href="xjtlu-dual-degree-liverpool-2plus2.html">복수학위·리버풀대학교 2+2<span class="arr">→</span></a></div>'
    new = '<div class="related-links" aria-label="이 내용과 관련된 상세 가이드"><span class="related-label">관련 글</span><a class="related-link" href="xjtlu-dual-degree-liverpool-2plus2.html">복수학위·리버풀대학교 2+2<span class="arr">→</span></a><a class="related-link" href="university-of-liverpool-vietnam.html">리버풀대학교의 베트남·아시아 네트워크<span class="arr">→</span></a></div>'
    index = patch_once(index, old, new)
    old = '<a class="mob-detail" href="xjtlu-dual-degree-liverpool-2plus2.html">리버풀대학교 복수학위·2+2</a>'
    new = old + '\n  <a class="mob-detail" href="university-of-liverpool-vietnam.html">리버풀대학교 베트남·아시아 네트워크</a>'
    index = patch_once(index, old, new)
    old = '<section class="site-menu-group"><h3><a href="#information">학교소개 <small>메인에서 보기 →</small></a></h3><a href="xjtlu-dual-degree-liverpool-2plus2.html">리버풀대학교 복수학위·2+2</a></section>'
    new = '<section class="site-menu-group"><h3><a href="#information">학교소개 <small>메인에서 보기 →</small></a></h3><a href="xjtlu-dual-degree-liverpool-2plus2.html">리버풀대학교 복수학위·2+2</a><a href="university-of-liverpool-vietnam.html">리버풀대학교 베트남·아시아 네트워크</a></section>'
    index = patch_once(index, old, new)
    INDEX.write_text(index, encoding='utf-8')

# 2+2 guide: add a compact bridge before FAQ.
dual = DUAL.read_text(encoding='utf-8')
if '리버풀대학교의 아시아 네트워크' not in dual:
    anchor = '<section class="section faq"><h2>자주 묻는 질문</h2>'
    section = '''<section class="section"><span class="tag">LIVERPOOL GLOBAL NETWORK</span><h2>리버풀대학교의 아시아 네트워크</h2><p class="lead">University of Liverpool은 베트남에서도 교육·의료·AI·도시 협력을 넓히고 있습니다. XJTLU의 복수학위와 2+2를 이해할 때, 리버풀대학교가 아시아에서 구축하는 실제 네트워크를 함께 보면 학교의 국제 연결성을 보다 입체적으로 볼 수 있습니다.</p><div class="notice"><strong>2025~2026 주요 사례:</strong> 리버풀-호치민 City2City 협력, University of Liverpool-호치민시 의약대 AI·데이터·디지털헬스 협력, Alder Hey-호치민 어린이병원 의료혁신 협력, Liverpool Culture Festival 등이 확인됩니다.</div><p style="margin:18px 0 0;"><a href="university-of-liverpool-vietnam.html" style="color:var(--navy);font-weight:700;text-decoration:none;">리버풀대학교 × 베트남 협력 사례 5개 자세히 보기 →</a></p></section>\n\n'''
    dual = patch_once(dual, anchor, section + anchor)
    DUAL.write_text(dual, encoding='utf-8')

# Sitemap
sitemap = SITEMAP.read_text(encoding='utf-8')
url = 'https://xjtlu-korea.netlify.app/university-of-liverpool-vietnam.html'
if url not in sitemap:
    entry = '  <url>\n    <loc>' + url + '</loc>\n    <lastmod>2026-09-05</lastmod>\n  </url>\n'
    sitemap = sitemap.replace('</urlset>', entry + '</urlset>')
    SITEMAP.write_text(sitemap, encoding='utf-8')

print('Added Korean Liverpool-Vietnam network guide, internal links and sitemap entry.')
