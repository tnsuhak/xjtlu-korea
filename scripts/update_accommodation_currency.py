from pathlib import Path

RATE_NOTE = "2026년 9월 17일 기준 1위안 ≈ 204원"


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise SystemExit(f"Expected text not found in {path}: {old[:80]}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Homepage summary cards and tuition/accommodation summary.
replace_once(
    "index.html",
    '<p class="adm-p"><b>기숙사비:</b> 월 약 1,700위안 (약 38만원)</p>',
    '<p class="adm-p"><b>기숙사비:</b> 월 약 1,700위안 (약 35만원)</p>',
)
replace_once(
    "index.html",
    '국제학생 아파트 기준, 주요 객실 유형은 월 약 1,700위안(약 38만원)부터입니다.',
    '국제학생 아파트 기준, 주요 객실 유형은 월 약 1,700위안(약 35만원)부터입니다.',
)
replace_once(
    "index.html",
    '2인실 연 6,000위안, 1인실 연 14,000위안 수준입니다.',
    '2인실 연 6,000위안(약 122만원), 1인실 연 14,000위안(약 285만원) 수준입니다.',
)

# Accommodation detail page: show KRW equivalents consistently.
replace_once(
    "xjtlu-accommodation-sip-taicang.html",
    '<td>약 1,710 RMB</td>',
    '<td>약 1,710 RMB (약 35만원)</td>',
)
replace_once(
    "xjtlu-accommodation-sip-taicang.html",
    '<td>2,400-2,700 RMB</td>',
    '<td>2,400-2,700 RMB (약 49만-55만원)</td>',
)
replace_once(
    "xjtlu-accommodation-sip-taicang.html",
    '<td>1인실 1,860 RMB<br>2인 공유 시 1인 부담액 절반</td>',
    '<td>1인실 1,860 RMB (약 38만원)<br>2인 공유 시 1인 부담액 절반</td>',
)
replace_once(
    "xjtlu-accommodation-sip-taicang.html",
    '<td>장기 거주 기준 약 1,500-1,620 RMB<br>30-90일은 2,220-2,340 RMB</td>',
    '<td>장기 거주 기준 약 1,500-1,620 RMB (약 31만-33만원)<br>30-90일은 2,220-2,340 RMB (약 45만-48만원)</td>',
)
replace_once(
    "xjtlu-accommodation-sip-taicang.html",
    '<td>Studio 약 2,550-2,700 RMB<br>1 Bedroom 약 3,060 RMB</td>',
    '<td>Studio 약 2,550-2,700 RMB (약 52만-55만원)<br>1 Bedroom 약 3,060 RMB (약 62만원)</td>',
)
replace_once(
    "xjtlu-accommodation-sip-taicang.html",
    '</tbody></table></div></section>',
    f'</tbody></table></div><p class="notice" style="margin-top:18px">원화 환산은 {RATE_NOTE} 기준으로 반올림한 참고 금액입니다.</p></section>',
)
replace_once(
    "xjtlu-accommodation-sip-taicang.html",
    '<strong>6,000 RMB / 1인 / 학년</strong>',
    '<strong>6,000 RMB / 1인 / 학년 (약 122만원)</strong>',
)
replace_once(
    "xjtlu-accommodation-sip-taicang.html",
    '<strong>14,000 RMB / 객실 / 학년</strong>',
    '<strong>14,000 RMB / 객실 / 학년 (약 285만원)</strong>',
)

print("Accommodation CNY/KRW conversions updated")
