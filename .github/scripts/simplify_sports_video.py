from pathlib import Path

p = Path('xjtlu-sports-facilities.html')
s = p.read_text(encoding='utf-8')

old_h1 = '<h1>XJTLU 스포츠·헬스장 시설<br>SIP와 Taicang 캠퍼스 비교</h1>'
new_h1 = '<h1>XJTLU 스포츠·헬스장 시설</h1>'
if old_h1 not in s:
    raise SystemExit('Expected sports page H1 not found')
s = s.replace(old_h1, new_h1, 1)

old_video = '''<section class="section"><div class="video"><div class="video-head"><span>XJTLU SPORTS VIDEO</span><h2>영상으로 보는 XJTLU 스포츠 시설</h2><p>XJTLU 스포츠 환경을 영상으로 함께 확인해 보세요.</p></div><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/nVirGEvdcT8" title="XJTLU 스포츠 시설 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></div><p style="margin:10px 0 0;font-size:12px"><a href="https://youtu.be/nVirGEvdcT8" target="_blank" rel="noopener" style="color:var(--navy);font-weight:700">YouTube에서 영상 보기 →</a></p></section>'''

# Handle older variant without the direct YouTube text link as well.
old_video_2 = '''<section class="section"><div class="video"><div class="video-head"><span>XJTLU SPORTS VIDEO</span><h2>영상으로 보는 XJTLU 스포츠 시설</h2><p>XJTLU 스포츠 환경을 영상으로 함께 확인해 보세요.</p></div><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/nVirGEvdcT8" title="XJTLU 스포츠 시설 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></div></section>'''

new_video = '''<section class="section"><h2>영상으로 보는 XJTLU 스포츠 시설 (타이창)</h2><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/nVirGEvdcT8" title="XJTLU 타이창 스포츠 시설 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></section>'''

if old_video in s:
    s = s.replace(old_video, new_video, 1)
elif old_video_2 in s:
    s = s.replace(old_video_2, new_video, 1)
else:
    raise SystemExit('Expected sports video block not found')

p.write_text(s, encoding='utf-8')
