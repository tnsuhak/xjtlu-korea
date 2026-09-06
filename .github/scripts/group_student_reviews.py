from pathlib import Path

p = Path('xjtlu-student-videos.html')
s = p.read_text(encoding='utf-8')

replacements = {
    'XJTLU 학생 후기 영상 모음 | 한국·외국인 학생 인터뷰 | TNS유학': 'XJTLU 학생 후기 영상 모음 | 한국인 재학생·졸업생·외국인 재학생 | TNS유학',
    '시안교통리버풀대학교(XJTLU) 재학생 후기 영상 모음. 한인 학생회장 인터뷰, 한국 재학생 후기, 외국인 재학생 인터뷰와 전공·진로 선택 후기를 한 페이지에서 확인하세요.': '시안교통리버풀대학교(XJTLU) 학생 후기 영상 모음. 한국인 재학생 후기, 한국인 졸업생 후기, 외국인 재학생 후기를 한 페이지에서 확인하세요.',
    'XJTLU 한국 학생과 외국인 재학생 인터뷰, 전공·진로 선택 후기 영상 모음.': 'XJTLU 한국인 재학생·졸업생과 외국인 재학생 인터뷰 영상 모음.',
    'XJTLU 한국 학생과 외국인 재학생 인터뷰 및 전공·진로 선택 후기 영상 모음': 'XJTLU 한국인 재학생·졸업생과 외국인 재학생 인터뷰 영상 모음',
    '한국 학생과 외국인 재학생이 직접 전하는 XJTLU 대학생활, 인터뷰와 전공·진로 선택 이야기를 한곳에서 확인할 수 있습니다.': '한국인 재학생과 졸업생, 외국인 재학생이 직접 전하는 XJTLU 학업·캠퍼스 생활·졸업 이후의 이야기를 한곳에서 확인할 수 있습니다.',
    '<section class="intro"><h2>재학생의 이야기를 영상으로 확인하세요</h2><p>메인 페이지에는 대표 영상 1개만 보여주고, 다양한 재학생 인터뷰 영상은 이 페이지에 모았습니다. 관심 있는 영상을 선택해 확인해 보세요.</p></section>': '<section class="intro"><h2>재학생부터 졸업생까지, 실제 경험을 확인하세요</h2><p>후기를 한국인 재학생, 한국인 졸업생, 외국인 재학생으로 나눠 정리했습니다. 메인 페이지에는 대표 영상 1개만 보여주고 전체 영상은 이 페이지에서 확인할 수 있습니다.</p></section>',
}
for old, new in replacements.items():
    s = s.replace(old, new)

s = s.replace('.video-card:first-child{grid-column:1/-1}', '.video-card.featured{grid-column:1/-1}')
s = s.replace('.video-card:first-child{grid-column:auto}', '.video-card.featured{grid-column:auto}')

start = s.find('<section class="video-grid" aria-label="XJTLU 학생 후기 영상">')
end = s.find('</section>', start)
if start == -1 or end == -1:
    raise SystemExit('video grid not found')
end += len('</section>')

grid = '''<section class="video-grid" aria-label="XJTLU 학생 후기 영상">
<div class="video-group-title"><span>KOREAN STUDENTS</span>한국인 재학생 후기</div>
<article class="video-card featured"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/c2h3t771rVk?rel=0" title="XJTLU 한인 학생회장 인터뷰" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">01 · KOREAN STUDENT · FEATURED</span><h2>XJTLU 한인 학생회장 인터뷰</h2><p>한국 재학생이 직접 전하는 XJTLU 대학생활과 캠퍼스 경험을 확인해 보세요.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/6eHbOLJ4ERg?rel=0" title="XJTLU 한국인 재학생 인터뷰" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">02 · KOREAN STUDENT</span><h2>한국인 재학생 인터뷰</h2><p>재학생이 직접 전하는 XJTLU 학업과 대학생활 경험을 영상으로 확인합니다.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/9iGRC82D3G0?rel=0" title="XJTLU 한국인 재학생 전공 및 진로 선택 후기" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">03 · KOREAN STUDENT</span><h2>전공·진로 선택 후기</h2><p>한국 재학생의 전공 선택과 진로에 관한 이야기를 영상으로 들어봅니다.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/ayDexdVyIpk?rel=0" title="XJTLU 한국인 재학생 후기 영상 4" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">04 · KOREAN STUDENT</span><h2>한국인 재학생 후기 ④</h2><p>XJTLU 재학생의 추가 인터뷰와 대학생활 경험을 확인해 보세요.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/_71HV9YKV2E?rel=0" title="XJTLU 한국인 재학생 후기 영상 5" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">05 · KOREAN STUDENT</span><h2>한국인 재학생 후기 ⑤</h2><p>같은 학생의 XJTLU 생활과 경험을 담은 추가 후기 영상입니다.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/h0t65P789sw?rel=0" title="XJTLU 한국인 재학생 후기 영상 6" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">06 · KOREAN STUDENT</span><h2>한국인 재학생 후기 ⑥</h2><p>한국 재학생이 직접 전하는 XJTLU 학업과 캠퍼스 생활 경험을 확인해 보세요.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/vXv_1GtqFdE?rel=0" title="XJTLU 한국인 재학생 후기 영상 7" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">07 · KOREAN STUDENT</span><h2>한국인 재학생 후기 ⑦</h2><p>한국 학생의 시각에서 본 XJTLU 수업과 대학생활 이야기를 확인할 수 있습니다.</p></div></article>

<div class="video-group-title"><span>KOREAN ALUMNI</span>한국인 졸업생 후기</div>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/lbgWNru8uPo?rel=0" title="XJTLU 한국인 졸업생 후기 1" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">01 · KOREAN ALUMNI</span><h2>한국인 졸업생 후기 ①</h2><p>XJTLU를 졸업한 한국 학생의 경험과 졸업 이후 이야기를 확인해 보세요.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/XbLR0oa0yEQ?rel=0" title="XJTLU 한국인 졸업생 후기 2" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">02 · KOREAN ALUMNI</span><h2>한국인 졸업생 후기 ②</h2><p>한국인 졸업생이 돌아보는 XJTLU 학업과 대학생활을 영상으로 확인합니다.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/iCgu_N-pjCQ?rel=0" title="XJTLU 한국인 졸업생 후기 3" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">03 · KOREAN ALUMNI</span><h2>한국인 졸업생 후기 ③</h2><p>XJTLU 졸업생의 실제 경험과 학교생활에 대한 이야기를 들어보세요.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/NuTLpUVReb4?rel=0" title="XJTLU 한국인 졸업생 후기 4" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">04 · KOREAN ALUMNI</span><h2>한국인 졸업생 후기 ④</h2><p>졸업생의 시각에서 본 XJTLU의 학업과 캠퍼스 경험을 확인해 보세요.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/f1M3erLwUTc?rel=0" title="XJTLU 한국인 졸업생 후기 5" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">05 · KOREAN ALUMNI</span><h2>한국인 졸업생 후기 ⑤</h2><p>한국인 졸업생이 전하는 XJTLU에서의 경험과 이후의 이야기를 확인합니다.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/41faYzujVao?rel=0" title="XJTLU 한국인 졸업생 후기 6" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">06 · KOREAN ALUMNI</span><h2>한국인 졸업생 후기 ⑥</h2><p>XJTLU를 경험한 한국인 졸업생의 이야기를 영상으로 만나보세요.</p></div></article>

<div class="video-group-title"><span>INTERNATIONAL STUDENTS</span>외국인 재학생 후기</div>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/KcDux0u1pkc?rel=0" title="XJTLU 외국인 재학생 후기 영상 1" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">01 · INTERNATIONAL STUDENT</span><h2>외국인 재학생 후기 ①</h2><p>외국인 재학생이 직접 전하는 XJTLU에서의 학업과 대학생활 이야기를 확인해 보세요.</p></div></article>
<article class="video-card"><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/tssEXewEU1I?rel=0" title="XJTLU 외국인 재학생 후기 영상 2" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><div class="video-copy"><span class="video-num">02 · INTERNATIONAL STUDENT</span><h2>외국인 재학생 후기 ②</h2><p>다른 국적의 재학생 시각에서 본 XJTLU 수업과 캠퍼스 경험을 영상으로 확인합니다.</p></div></article>
</section>'''

s = s[:start] + grid + s[end:]
p.write_text(s, encoding='utf-8')
print('Grouped reviews into Korean students, Korean alumni, and international students')
