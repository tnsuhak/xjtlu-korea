from pathlib import Path

p = Path('xjtlu-sports-facilities.html')
html = p.read_text(encoding='utf-8')

repls = [
    (
        '<div class="wrap quick"><div><b>SIP</b><span>Central + South Campus</span></div><div><b>Taicang</b><span>XEC Sports Centre</span></div><div><b>Swimming Pool</b><span>Taicang 캠퍼스</span></div><div><b>36 Clubs · 10 Teams</b><span>공식 스포츠 조직</span></div></div>',
        '<div class="wrap quick"><div><b>SIP</b><span>Central + South Campus</span></div><div><b>Taicang</b><span>XEC Sports Centre</span></div><div><b>Swimming Pool</b><span>교내 수영장 · Taicang(XEC) only</span></div><div><b>36 Clubs · 10 Teams</b><span>공식 스포츠 조직</span></div></div>'
    ),
    (
        '<article class="facility-box sip"><h3>South Campus · 실내 Sports Centre</h3><div class="chips"><span class="chip">Fitness Centre / Gym</span><span class="chip">농구</span><span class="chip">배드민턴</span><span class="chip">탁구</span><span class="chip">실내 골프</span><span class="chip">스쿼시</span><span class="chip">당구</span><span class="chip">양궁</span><span class="chip">펜싱</span><span class="chip">요가</span><span class="chip">댄스</span><span class="chip">무도</span><span class="chip">클라이밍 월</span><span class="chip">실내 트랙</span><span class="chip">다목적 활동실</span><span class="chip">복싱룸</span></div></article>',
        '<article class="facility-box sip"><h3>South Campus · 실내 Sports Centre</h3><div class="chips"><span class="chip">Fitness Centre / Gym</span><span class="chip">농구</span><span class="chip">배드민턴</span><span class="chip">탁구</span><span class="chip">실내 골프</span><span class="chip">스쿼시</span><span class="chip">당구</span><span class="chip">양궁</span><span class="chip">펜싱</span><span class="chip">요가</span><span class="chip">댄스</span><span class="chip">무도</span><span class="chip">클라이밍 월</span><span class="chip">실내 트랙</span><span class="chip">다목적 활동실</span><span class="chip">복싱룸</span></div><p style="margin-top:18px">Fitness Centre(GM101)에는 <strong>근력운동 장비, 유산소 머신, 웨이트리프팅 플랫폼</strong> 등이 마련돼 있으며 공식 안내상 약 60명이 동시에 이용할 수 있습니다.</p></article>'
    ),
    (
        '<a href="https://www.xjtlu.edu.cn/en/it-services/sports-centre-eng" target="_blank" rel="noopener">XJTLU Sports Centre</a>',
        '<a href="https://www.xjtlu.edu.cn/en/it-services/gym-intro" target="_blank" rel="noopener">XJTLU Sports Centre</a>'
    ),
    (
        '<div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/nVirGEvdcT8" title="XJTLU 스포츠 시설 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></div></section>',
        '<div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/nVirGEvdcT8" title="XJTLU 스포츠 시설 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div><p style="margin:12px 0 0;font-size:12px"><a href="https://youtu.be/nVirGEvdcT8" target="_blank" rel="noopener" style="color:#e8d4a0;text-decoration:none;font-weight:700">YouTube에서 영상 보기 →</a></p></div></section>'
    )
]

for old, new in repls:
    if old not in html:
        raise SystemExit(f'Expected marker not found: {old[:80]}')
    html = html.replace(old, new, 1)

marker = '\n\n<section class="section" id="sip">'
comparison = '''\n\n<section class="section"><h2>SIP vs Taicang, 스포츠시설 한눈에 비교</h2><p class="lead">두 캠퍼스 모두 운동시설을 갖추고 있지만, 실제 구성은 다릅니다. 특히 <strong>교내 수영장은 Taicang(XEC)에만</strong> 있으며, SIP 학생은 캠퍼스 밖 Dushu Lake Gym의 50m 수영장도 이용할 수 있습니다.</p><div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table style="width:100%;min-width:680px;border-collapse:collapse;background:#fff;border:1px solid var(--rule);font-size:13px"><thead><tr style="background:var(--navy);color:#fff"><th style="padding:12px 14px;text-align:left">구분</th><th style="padding:12px 14px;text-align:left">SIP 캠퍼스</th><th style="padding:12px 14px;text-align:left">Taicang(XEC)</th></tr></thead><tbody><tr style="border-bottom:1px solid var(--rule)"><td style="padding:12px 14px;font-weight:700;color:var(--navy)">Fitness / GYM</td><td style="padding:12px 14px">South Campus Fitness Centre · Gym</td><td style="padding:12px 14px">Sports Centre Gymnasium / Fitness</td></tr><tr style="border-bottom:1px solid var(--rule);background:#fafafa"><td style="padding:12px 14px;font-weight:700;color:var(--navy)">교내 수영장</td><td style="padding:12px 14px"><strong>없음</strong> · Dushu Lake Gym 50m 수영장은 캠퍼스 밖</td><td style="padding:12px 14px"><strong>있음</strong> · XEC Sports Centre</td></tr><tr style="border-bottom:1px solid var(--rule)"><td style="padding:12px 14px;font-weight:700;color:var(--navy)">실내 주요시설</td><td style="padding:12px 14px">농구·배드민턴·탁구·골프·스쿼시·당구·양궁·펜싱·요가·댄스·무도·클라이밍·실내트랙</td><td style="padding:12px 14px">농구·배드민턴·스쿼시·탁구·당구·실내골프·무도·펜싱·Training Hall·다목적홀·댄스 스튜디오</td></tr><tr><td style="padding:12px 14px;font-weight:700;color:var(--navy)">야외시설</td><td style="padding:12px 14px">러닝트랙·축구장·농구장·배구장·테니스장 + SEID 주변 시설</td><td style="padding:12px 14px">공식 Campus Life 페이지는 XEC 실내 Sports Centre 시설을 중심으로 안내</td></tr></tbody></table></div></section>'''

if comparison.strip() not in html:
    if marker not in html:
        raise SystemExit('SIP section marker not found')
    html = html.replace(marker, comparison + marker, 1)

required = [
    'SIP vs Taicang, 스포츠시설 한눈에 비교',
    'Fitness Centre(GM101)',
    '교내 수영장 · Taicang(XEC) only',
    'https://www.xjtlu.edu.cn/en/it-services/gym-intro',
    'https://youtu.be/nVirGEvdcT8',
    'Dushu Lake Gym 50m 수영장'
]
for item in required:
    if item not in html:
        raise SystemExit(f'Validation failed: {item}')

if html.count('<h1>') != 1:
    raise SystemExit('H1 validation failed')

p.write_text(html, encoding='utf-8')
print('sports page refinement validated')
