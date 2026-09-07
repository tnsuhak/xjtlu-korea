from pathlib import Path
import re

p = Path("index.html")
s = p.read_text(encoding="utf-8")

footer = """<footer>
  <div style="max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr auto;gap:42px;align-items:start;color:rgba(255,255,255,.35);font-size:11px;line-height:1.9;">
    <div>
      <strong style="display:block;color:rgba(255,255,255,.78);font-size:13px;margin-bottom:6px;">서울 본사</strong>
      <div>서울 강남구 테헤란로 5길 7 KG타워 B1</div>
      <div>Tel. <a href="tel:0232881733" style="color:rgba(255,255,255,.55);text-decoration:none;">02-3288-1733~5</a></div>
      <div>Email. <a href="mailto:tns@tnsuhak.com" style="color:rgba(255,255,255,.55);text-decoration:none;">tns@tnsuhak.com</a></div>
    </div>
    <div>
      <strong style="display:block;color:rgba(255,255,255,.78);font-size:13px;margin-bottom:6px;">부산 지사</strong>
      <div>부산 부산진구 중앙대로 694 쥬디스태화 9층 37호</div>
      <div style="margin-top:4px;">연락처 <a href="tel:01050241733" style="color:#c9a84c;text-decoration:none;font-weight:800;">010-5024-1733</a></div>
    </div>
    <div style="text-align:right;white-space:nowrap;align-self:end;">
      <div style="color:rgba(255,255,255,.48);font-weight:700;">TNS유학 · ㈜티앤에스월드와이드</div>
      <div>대표: 신윤옥 · 사업자등록번호: 220-87-54964</div>
      <div style="margin-top:8px;">© 2026 TNS Worldwide Co., Ltd.</div>
    </div>
  </div>
  <style>
    @media(max-width:760px){
      footer>div{grid-template-columns:1fr!important;gap:22px!important}
      footer>div>div:last-child{text-align:left!important;white-space:normal!important}
    }
  </style>
</footer>"""

s2, n = re.subn(r"<footer>.*?</footer>", footer, s, count=1, flags=re.S)
assert n == 1, f"footer replacement count={n}"
assert "QUICK MENU" not in s2
assert ">COMMUNITY<" not in s2
assert "tel:01050241733" in s2
assert "© 2026 TNS Worldwide Co., Ltd." in s2
p.write_text(s2, encoding="utf-8")
