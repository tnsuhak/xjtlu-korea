from pathlib import Path
import re

p = Path('index.html')
html = p.read_text(encoding='utf-8')

old_css = re.compile(r'/\* Campus life guide links \*/.*?@media\(max-width:700px\)\{\.campus-life-grid\{grid-template-columns:1fr\}\}\n', re.S)
new_css = """/* Compact contextual detail links — aligned with UNNC Korea */
.related-links{margin-top:22px;display:flex;align-items:center;justify-content:flex-end;gap:8px;flex-wrap:wrap}
.related-label{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.12em;color:#98a2b3;margin-right:2px}
.related-link{display:inline-flex;align-items:center;gap:7px;padding:8px 11px;border:1px solid #d9dee7;border-radius:3px;background:rgba(255,255,255,.72);color:var(--navy);font-size:12px;font-weight:700;line-height:1.4;text-decoration:none;transition:.2s}
.related-link:hover{border-color:var(--gold);color:#8b6a1f;transform:translateY(-1px)}
.related-link .arr{color:var(--gold)}
#campus-life .related-links{justify-content:flex-start;margin-top:24px}
@media(max-width:560px){.related-links{justify-content:flex-start;margin-top:18px}.related-label{width:100%;margin-bottom:1px}.related-link{font-size:12px;padding:8px 10px}}
"""
html, css_count = old_css.subn(new_css, html, count=1)
if css_count != 1:
    raise SystemExit(f'Campus-life CSS replacement count: {css_count}')

replacements = [
    (
        '<div class="source-note"><a href="xjtlu-dual-degree-liverpool-2plus2.html"><strong>복수학위·리버풀대학교 2+2 상세 가이드 →</strong></a><br><span style="display:inline-block;margin-top:7px;font-size:12px;color:var(--mid);line-height:1.7;">XJTLU에서 4년을 공부하는 경로와 영국 리버풀대학교로 이동하는 2+2의 차이, 취득 학위와 비용 구조를 정리했습니다.</span></div>',
        '<div class="related-links" aria-label="이 내용과 관련된 상세 가이드"><span class="related-label">관련 글</span><a class="related-link" href="xjtlu-dual-degree-liverpool-2plus2.html">복수학위·2+2<span class="arr">→</span></a></div>'
    ),
    (
        '<div class="source-note"><a href="xjtlu-programmes-careers-graduate-destinations.html"><strong>전공·대학원 진학·졸업 후 진로 상세 가이드 →</strong></a><br>전공 분야별 학업 방향과 2025년 졸업생 진학 결과, 취업·인턴십 지원을 함께 정리했습니다.</div>',
        '<div class="related-links" aria-label="이 내용과 관련된 상세 가이드"><span class="related-label">관련 글</span><a class="related-link" href="xjtlu-programmes-careers-graduate-destinations.html">전공·진로<span class="arr">→</span></a></div>'
    ),
    (
        '<div class="source-note"><a href="xjtlu-tuition-scholarships-2027.html"><strong>2027 학비·장학금 상세 가이드 →</strong></a><br>학비, 장학금, 지원 일정은 변경될 수 있습니다. 최신 기준과 지원 가능 여부는 상세 가이드와 TNS유학 상담을 통해 확인해 주세요.</div>',
        '<div class="related-links" aria-label="이 내용과 관련된 상세 가이드"><span class="related-label">관련 글</span><a class="related-link" href="xjtlu-tuition-scholarships-2027.html">2027 학비·장학금<span class="arr">→</span></a></div>'
    ),
    (
        '<div class="source-note" style="margin-top:22px;"><a href="xjtlu-accommodation-sip-taicang.html"><strong>XJTLU 숙소 상세 가이드 →</strong></a><br><span style="display:inline-block;margin-top:7px;font-size:12px;color:var(--mid);line-height:1.7;">SIP·Taicang 숙소별 비용, 거리, 주방·욕실, 예약 시 확인할 내용을 자세히 정리했습니다.</span></div>',
        '<div class="related-links" aria-label="이 내용과 관련된 상세 가이드"><span class="related-label">관련 글</span><a class="related-link" href="xjtlu-accommodation-sip-taicang.html">숙소 상세<span class="arr">→</span></a></div>'
    ),
    (
        '<div class="source-note"><a href="xjtlu-admission-requirements-korea-2027.html"><strong>2027 입학조건·편입 상세 가이드 →</strong></a><br><span style="display:inline-block;margin-top:7px;font-size:12px;color:var(--mid);line-height:1.7;">한국 고교 내신·IELTS·해외고 2학년 진학·한국 대학 편입 기준을 정리했습니다.</span></div>',
        '<div class="related-links" aria-label="이 내용과 관련된 상세 가이드"><span class="related-label">관련 글</span><a class="related-link" href="xjtlu-admission-requirements-korea-2027.html">2027 입학조건·편입<span class="arr">→</span></a></div>'
    )
]
for old, new in replacements:
    if old not in html:
        raise SystemExit('Expected long detail-guide block not found')
    html = html.replace(old, new, 1)

campus_pattern = re.compile(
    r'<div class="campus-life-grid">\s*'
    r'<a class="campus-life-card" href="xjtlu-sports-facilities\.html">.*?</a>\s*'
    r'<a class="campus-life-card" href="xjtlu-clubs-student-organisations\.html">.*?</a>\s*'
    r'</div>',
    re.S
)
new_campus = '<div class="related-links" aria-label="캠퍼스 생활 상세 가이드"><span class="related-label">관련 글</span><a class="related-link" href="xjtlu-sports-facilities.html">스포츠 시설<span class="arr">→</span></a><a class="related-link" href="xjtlu-clubs-student-organisations.html">동아리 215개<span class="arr">→</span></a></div>'
html, campus_count = campus_pattern.subn(new_campus, html, count=1)
if campus_count != 1:
    raise SystemExit(f'Campus-life card replacement count: {campus_count}')

if html.count('class="related-links"') != 6:
    raise SystemExit('Expected six compact related-link groups')
if 'campus-life-card' in html or 'campus-life-grid' in html:
    raise SystemExit('Old campus-life card markup/style remains')
for phrase in [
    '비용 구조를 정리했습니다.',
    '취업·인턴십 지원을 함께 정리했습니다.',
    '최신 기준과 지원 가능 여부는 상세 가이드',
    '예약 시 확인할 내용을 자세히 정리했습니다.',
    '한국 대학 편입 기준을 정리했습니다.'
]:
    if phrase in html:
        raise SystemExit(f'Long guide description remains: {phrase}')

p.write_text(html, encoding='utf-8')
print('Compact contextual links validated')
