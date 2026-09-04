from pathlib import Path

p = Path('xjtlu-sports-facilities.html')
s = p.read_text(encoding='utf-8')

css_anchor = ".video-frame{position:relative;padding-top:56.25%;overflow:hidden;background:#000}.video-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}"
css_new = ".video-section-wide{width:min(1440px,calc(100vw - 32px));margin-left:50%;transform:translateX(-50%);padding-left:0!important;padding-right:0!important}.video-frame{position:relative;padding-top:56.25%;overflow:hidden;background:#000;border-radius:6px;box-shadow:0 22px 50px rgba(14,26,46,.16)}.video-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}"
if css_anchor not in s:
    raise SystemExit('video css anchor not found')
s = s.replace(css_anchor, css_new, 1)

mobile_anchor = "@media(max-width:800px){.navlinks{display:none}.hero{min-height:440px}.quick{grid-template-columns:1fr 1fr}.quick div:nth-child(2){border-right:0}.campus-switch,.grid2,.grid3,.next{grid-template-columns:1fr}.hero h1{font-size:35px}.cta{padding:36px 20px}.video{padding:22px 16px}}"
mobile_new = "@media(max-width:800px){.navlinks{display:none}.hero{min-height:440px}.quick{grid-template-columns:1fr 1fr}.quick div:nth-child(2){border-right:0}.campus-switch,.grid2,.grid3,.next{grid-template-columns:1fr}.hero h1{font-size:35px}.cta{padding:36px 20px}.video{padding:22px 16px}.video-section-wide{width:calc(100vw - 8px)}.video-frame{border-radius:4px}}"
if mobile_anchor not in s:
    raise SystemExit('mobile css anchor not found')
s = s.replace(mobile_anchor, mobile_new, 1)

section_old = '<section class="section"><h2>영상으로 보는 XJTLU 스포츠 시설 (타이창)</h2><div class="video-frame">'
section_new = '<section class="section video-section-wide"><h2>영상으로 보는 XJTLU 스포츠 시설 (타이창)</h2><div class="video-frame">'
if section_old not in s:
    raise SystemExit('video section anchor not found')
s = s.replace(section_old, section_new, 1)

s = s.replace('"dateModified":"2026-09-04"', '"dateModified":"2026-09-05"', 1)

p.write_text(s, encoding='utf-8')
