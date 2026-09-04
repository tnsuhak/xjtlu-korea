from pathlib import Path

p = Path('xjtlu-sports-facilities.html')
s = p.read_text(encoding='utf-8')

old_css = ".video-section-wide{width:min(1440px,calc(100vw - 32px));margin-left:50%;transform:translateX(-50%);padding-left:0!important;padding-right:0!important}.video-frame{position:relative;padding-top:56.25%;overflow:hidden;background:#000;border-radius:6px;box-shadow:0 22px 50px rgba(14,26,46,.16)}.video-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}"
new_css = ".video-section-wide{width:min(1440px,calc(100vw - 32px));margin-left:50%;transform:translateX(-50%);padding-left:0!important;padding-right:0!important}.video-wrap{background:#0e1a2e;padding:0;margin-bottom:30px;border-radius:6px;overflow:hidden;box-shadow:0 22px 50px rgba(14,26,46,.18)}.video-copy{padding:28px 32px 20px}.video-wrap h3{color:#fff;margin:0 0 8px;font-size:22px}.video-wrap p{color:#cdd7e6;font-size:13px;margin:0}.video-frame{position:relative;padding-top:56.25%;overflow:hidden;background:#000;border-radius:0;box-shadow:none}.video-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}"
if old_css not in s:
    raise SystemExit('expected video CSS not found')
s = s.replace(old_css, new_css, 1)

old_mobile = ".video-section-wide{width:calc(100vw - 8px)}.video-frame{border-radius:4px}"
new_mobile = ".video-section-wide{width:calc(100vw - 8px)}.video-wrap{border-radius:4px;margin-bottom:18px}.video-copy{padding:20px 14px 14px}.video-wrap h3{font-size:20px}"
if old_mobile not in s:
    raise SystemExit('expected mobile video CSS not found')
s = s.replace(old_mobile, new_mobile, 1)

old_section = '<section class="section video-section-wide"><h2>영상으로 보는 XJTLU 스포츠 시설 (타이창)</h2><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/nVirGEvdcT8" title="XJTLU 타이창 스포츠 시설 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></section>'
new_section = '<section class="section video-section-wide"><div class="video-wrap"><div class="video-copy"><div class="eyebrow">XJTLU SPORT VIDEO</div><h3>영상으로 보는 XJTLU 스포츠 시설 (타이창)</h3><p>Taicang(XEC) 캠퍼스의 스포츠 시설과 실제 공간을 영상으로 확인해 보세요.</p></div><div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/nVirGEvdcT8" title="XJTLU 타이창 스포츠 시설 영상" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></div></section>'
if old_section not in s:
    raise SystemExit('expected video section not found')
s = s.replace(old_section, new_section, 1)

p.write_text(s, encoding='utf-8')
