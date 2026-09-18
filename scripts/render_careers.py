from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "xjtlu-career-outcomes.json"
SUMMARY_PATH = ROOT / "xjtlu-graduate-destinations-careers.html"
DETAIL_PATH = ROOT / "xjtlu-alumni-careers.html"

DETAIL_URL = "xjtlu-alumni-careers.html"
SUMMARY_URL = "xjtlu-graduate-destinations-careers.html"

# 요약 섹션(졸업 후 진로 페이지)과 상세 페이지의 데이터 블록은 모두 이 스크립트가 렌더링합니다.
BLOCKS = (
    "CAREER_SUMMARY",
    "CAREER_KPI",
    "CAREER_EMPLOYERS",
    "CAREER_INDUSTRY",
    "CAREER_REGION",
    "CAREER_PATTERNS",
    "CAREER_GRADUATE",
    "CAREER_METHOD",
)

SUMMARY_EMPLOYER_PREVIEW = 12
SUMMARY_INDUSTRY_PREVIEW = 5


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_data() -> dict:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for key in ("kpis", "employers_primary", "industry_stats", "region_stats", "copy"):
        if not data.get(key):
            raise SystemExit(f"공개 데이터에 필수 항목이 없습니다: {key}")
    return data


def replace_between(text: str, name: str, body: str) -> str:
    start, end = f"<!-- {name}_START -->", f"<!-- {name}_END -->"
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f"렌더링 마커가 없거나 중복되었습니다: {start} / {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{body}\n{end}{after}"


def headline_total(data: dict) -> int:
    """정확한 합계 대신 내림한 라운드 숫자만 노출합니다."""
    step = int(data["meta"]["display_rules"]["headline_round_down_to"])
    return (int(data["kpis"]["core_outcomes_total"]) // step) * step


def split_industries(data: dict) -> tuple[list[tuple[str, int]], int]:
    """표시 최소 건수 미만 산업은 하나의 '기타' 묶음으로 합칩니다(재식별 방지)."""
    rules = data["meta"]["display_rules"]
    floor = int(rules["industry_min_display_outcomes"])
    named = [(row["industry"], int(row["outcomes"])) for row in data["industry_stats"] if int(row["outcomes"]) >= floor]
    other = sum(int(row["outcomes"]) for row in data["industry_stats"] if int(row["outcomes"]) < floor)
    named.sort(key=lambda row: row[1], reverse=True)
    if other:
        named.append((rules["industry_other_label"], other))
    return named, floor


def render_kpis(data: dict, compact: bool = False) -> str:
    k = data["kpis"]
    cells = [
        (f'{k["employment_outcomes"]}건', "확인된 취업·경력 사례"),
        (f'{k["graduate_study_outcomes"]}건', "확인된 대학원 진학 사례"),
        (f'{k["undergraduate_progression_outcomes"]}건', "2+2·학부 연계 학업 경로"),
    ]
    if not compact:
        cells.append((f'{k["employment_countries"]}개국', "취업·경력이 확인된 국가"))
    items = "".join(f"<div class=\"co-kpi\"><b>{esc(v)}</b><span>{esc(label)}</span></div>" for v, label in cells)
    wide = "" if compact else " co-kpis-4"
    return f'<div class="co-kpis{wide}">{items}</div>'


def render_headline_kpis(data: dict) -> str:
    return (
        f'<p class="co-headline">{headline_total(data)}건+의 취업·진학·학업 경로를 확인했습니다.</p>'
        f"{render_kpis(data)}"
    )


def render_chips(names: list[str]) -> str:
    chips = "".join(f'<span class="co-chip">{esc(name)}</span>' for name in names)
    return f'<div class="co-chips">{chips}</div>'


def render_bars(rows: list[tuple[str, int]]) -> str:
    top = max(value for _, value in rows)
    bars = []
    for label, value in rows:
        width = round(value / top * 100, 1)
        bars.append(
            '<div class="co-bar">'
            f'<span class="co-bar-label">{esc(label)}</span>'
            f'<span class="co-bar-track"><span class="co-bar-fill" style="width:{width}%"></span></span>'
            f'<span class="co-bar-val">{value}건</span>'
            "</div>"
        )
    return '<div class="co-bars">' + "".join(bars) + "</div>"


def render_summary(data: dict) -> str:
    copy = data["copy"]
    industries, _ = split_industries(data)
    preview = data.get("employers_featured") or data["employers_primary"][:SUMMARY_EMPLOYER_PREVIEW]
    unknown = [name for name in preview if name not in data["employers_primary"]]
    if unknown:
        raise SystemExit("employers_featured는 employers_primary의 부분집합이어야 합니다: " + ", ".join(unknown))
    return (
        f'<section class="section alt" id="alumni-careers" aria-labelledby="alumni-careers-title">'
        f'<h2 id="alumni-careers-title">{esc(copy["section_title"])}</h2>'
        f'<p class="lead">{esc(copy["intro"])} 아래는 XJTLU가 발표하는 공식 통계와는 별개로, TNS가 개별적으로 확인한 동문 사례를 집계한 결과입니다.</p>'
        f'<p class="co-headline">{headline_total(data)}건+의 취업·진학·학업 경로를 확인했습니다.</p>'
        f"{render_kpis(data, compact=True)}"
        f'<p class="co-sub">확인된 주요 취업·경력 기업</p>'
        f"{render_chips(preview)}"
        f'<p class="co-note">재직 중인 경력과 과거 경력이 함께 포함되어 있습니다. 그 외 확인된 기업과 기업별 분포는 상세 페이지에서 확인할 수 있습니다.</p>'
        f'<p class="co-sub">많이 확인된 진출 산업</p>'
        f"{render_bars(industries[:SUMMARY_INDUSTRY_PREVIEW])}"
        f'<a class="co-more" href="{DETAIL_URL}">XJTLU 동문 취업 현황 자세히 보기 →</a>'
        f"</section>"
    )


def render_employers(data: dict) -> str:
    copy = data["copy"]
    secondary = "".join(f"<li>{esc(name)}</li>" for name in data["employers_secondary"])
    return (
        f"{render_chips(data['employers_primary'])}"
        f'<p class="co-sub">그 외 확인된 기업·기관</p>'
        f'<ul class="co-textlist">{secondary}</ul>'
        f'<p class="co-note">{esc(copy["employer_caveat"])}</p>'
    )


def render_industry(data: dict) -> str:
    industries, floor = split_industries(data)
    return (
        f"{render_bars(industries)}"
        f'<p class="co-note">각 막대는 확인된 취업·경력 사례 건수입니다. 사례가 {floor}건 미만인 분야는 개인 식별 가능성을 줄이기 위해 '
        f'{esc(data["meta"]["display_rules"]["industry_other_label"])}로 묶어 표시했습니다.</p>'
    )


def render_region(data: dict) -> str:
    cells = []
    for row in data["region_stats"]:
        count = row["display_count"]
        value = f'{count}건' if count else "소수 사례"
        note = "확인된 사례" if count else "숫자 비공개"
        cells.append(
            f'<div class="co-region"><strong>{esc(row["region"])}</strong>'
            f"<b>{esc(value)}</b><span>{esc(note)}</span></div>"
        )
    countries = "".join(f'<span class="co-chip">{esc(name)}</span>' for name in data["countries_observed"])
    return (
        f'<div class="co-regions">{"".join(cells)}</div>'
        f'<p class="co-sub">취업·경력이 확인된 국가</p>'
        f'<div class="co-chips">{countries}</div>'
        f'<p class="co-note">{esc(data["copy"]["region_caveat"])}</p>'
    )


def render_patterns(data: dict) -> str:
    cards = "".join(
        '<article class="co-pattern">'
        f'<span>PATTERN {index:02d}</span>'
        f'<strong>{esc(row["major_group"])} → {esc(row["destination_field"])}</strong>'
        "</article>"
        for index, row in enumerate(data["career_patterns"], start=1)
    )
    return (
        f'<div class="co-patterns">{cards}</div>'
        f'<p class="co-note">{esc(data["copy"]["pattern_caveat"])}</p>'
    )


def render_graduate(data: dict) -> str:
    pathways = "".join(
        f'<div class="co-region"><strong>{esc(row["label"])}</strong>'
        f'<b>{int(row["outcomes"])}건</b><span>확인된 사례</span></div>'
        for row in data.get("academic_pathways", [])
    )
    block = (
        f"{render_chips(data['graduate_destinations'])}"
        f'<p class="co-note">대학별 진학 인원수는 공개하지 않으며, 위 대학 목록은 앞의 취업·경력 집계와는 연결되지 않은 별도의 집계입니다.</p>'
    )
    if pathways:
        block += f'<p class="co-sub">학부 단계 학업 연계 경로</p><div class="co-regions">{pathways}</div>'
    return block


def render_method(data: dict) -> str:
    copy = data["copy"]
    return (
        f'<div class="notice"><p style="margin:0 0 12px">{esc(copy["methodology"])}</p>'
        f'<p style="margin:0">{esc(copy["privacy"])}</p></div>'
        f'<p class="co-note">기준일 {esc(data["meta"]["as_of"])} · 집계 주체 {esc(data["meta"]["publisher"])}</p>'
    )


def build(data: dict) -> dict[str, dict[str, str]]:
    return {
        SUMMARY_URL: {"CAREER_SUMMARY": render_summary(data)},
        DETAIL_URL: {
            "CAREER_KPI": render_headline_kpis(data),
            "CAREER_EMPLOYERS": render_employers(data),
            "CAREER_INDUSTRY": render_industry(data),
            "CAREER_REGION": render_region(data),
            "CAREER_PATTERNS": render_patterns(data),
            "CAREER_GRADUATE": render_graduate(data),
            "CAREER_METHOD": render_method(data),
        },
    }


def main(check: bool = False) -> int:
    data = load_data()
    rendered = 0
    for filename, blocks in build(data).items():
        path = ROOT / filename
        original = path.read_text(encoding="utf-8")
        updated = original
        for name, body in blocks.items():
            updated = replace_between(updated, name, body)
        if check:
            if updated != original:
                raise SystemExit(
                    f"{filename}의 취업 데이터 블록이 최신이 아닙니다. python scripts/render_careers.py를 실행하세요."
                )
        elif updated != original:
            path.write_text(updated, encoding="utf-8")
        rendered += len(blocks)
    print(f"{'Checked' if check else 'Rendered'} {rendered} XJTLU alumni career data block(s)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(check=args.check))
