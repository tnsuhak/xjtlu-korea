from pathlib import Path

p = Path('index.html')
html = p.read_text(encoding='utf-8')

replacements = {
    '>복수학위·2+2<span class="arr">→</span></a>': '>복수학위·리버풀대학교 2+2<span class="arr">→</span></a>',
    '>전공·진로<span class="arr">→</span></a>': '>전공·대학원 진학·졸업 후 진로<span class="arr">→</span></a>',
    '>2027 학비·장학금<span class="arr">→</span></a>': '>2027 학비·장학금·연간 비용 자세히<span class="arr">→</span></a>',
    '>숙소 상세<span class="arr">→</span></a>': '>SIP·Taicang 숙소·기숙사 자세히<span class="arr">→</span></a>',
    '>스포츠 시설<span class="arr">→</span></a>': '>스포츠 시설·이용 안내<span class="arr">→</span></a>',
    '>동아리 215개<span class="arr">→</span></a>': '>215개 동아리·학생단체 전체 보기<span class="arr">→</span></a>',
    '>2027 입학조건·편입<span class="arr">→</span></a>': '>2027 한국학생 입학조건·편입 안내<span class="arr">→</span></a>',
}

for old, new in replacements.items():
    count = html.count(old)
    if count != 1:
        raise SystemExit(f'Expected exactly one match for {old!r}, found {count}')
    html = html.replace(old, new, 1)

for old in replacements:
    if old in html:
        raise SystemExit(f'Old short label remains: {old}')

p.write_text(html, encoding='utf-8')
print('Expanded contextual link labels to UNNC-like detail level')
