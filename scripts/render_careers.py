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
    for key in ("kpis", "employers", "industry_stats", "graduate_destinations", "copy"):
        if not data.get(key):
            raise SystemExit(f"공개 데이터에 필수 항목이 없습니다: {key}")
    employers = data["employers"]
    for key in ("tier1", "tier2", "tier3", "group_only_labels"):
        if key not in employers:
            raise SystemExit(f"employers에 필수 항목이 없습니다: {key}")
    display_names = employers["tier1"] + employers["tier2"] + employers["tier3"]
    duplicates = sorted({name for name in display_names if display_names.count(name) > 1})
    if duplicates:
        raise SystemExit("기업 display name이 단계 간 중복되었습니다: " + ", ".join(duplicates))
    return data


def replace_between(text: str, name: str, body: str) -> str:
    start, end = f"<!-- {name}_START -->", f"<!-- {name}_END -->"
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f"렌더링 마커가 없거나 중복되었습니다: {start} / {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{body}\n{end}{after}"


def round_down(value: int, step: int) -> int:
    return (int(value) // step) * step


def headline_total(data: dict) -> int:
    """정확한 합계 대신 내림한 라운드 숫자만 노출합니다."""
    step = int(data["meta"]["display_rules"]["headline_round_down_to"])
    return round_down(data["kpis"]["core_career_academic_outcomes"], step)


def employer_count_display(data: dict) -> str:
    """정확한 기업 수 대신 내림한 라운드 숫자만 노출합니다."""
    step = int(data["meta"]["display_rules"]["employer_count_round_down_to"])
    return f"{round_down(data['kpis']['unique_employer_organizations'], step)}곳+"


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


def render_headline_kpis(data: dict, compact: bool = False) -> str:
    k = data["kpis"]
    cells = [
        (f'{k["career_outcomes"]}건', "확인된 취업·경력 사례"),
        (f'{k["graduate_study_outcomes"]}건', "확인된 대학원 진학"),
        (f'{k["further_study_transfer_exchange_outcomes"]}건', "편입·후속학업·교환"),
    ]
    if not compact:
        cells.append((employer_count_display(data), "확인된 기업·기관"))
    items = "".join(f"<div class=\"co-kpi\"><b>{esc(v)}</b><span>{esc(label)}</span></div>" for v, label in cells)
    wide = "" if compact else " co-kpis-4"
    return (
        f'<p class="co-headline">{headline_total(data)}건+의 취업·대학원·후속학업 경로를 확인했습니다.</p>'
        f'<div class="co-kpis{wide}">{items}</div>'
    )


def render_summary(data: dict) -> str:
    copy = data["copy"]
    industries = [(row["sector"], int(row["outcomes"])) for row in data["industry_stats"]]
    industries.sort(key=lambda row: row[1], reverse=True)
    preview = data["employers"]["tier1"][:SUMMARY_EMPLOYER_PREVIEW]
    return (
        f'<section class="section alt" id="alumni-careers" aria-labelledby="alumni-careers-title">'
        f'<h2 id="alumni-careers-title">{esc(copy["section_title"])}</h2>'
        f'<p class="lead">{esc(copy["intro"])}</p>'
        f"{render_headline_kpis(data, compact=True)}"
        f'<p class="co-sub">확인된 주요 취업·경력 기업</p>'
        f"{render_chips(preview)}"
        f'<p class="co-note">{esc(copy["employer_caveat"])}</p>'
        f'<p class="co-sub">확인된 진출 분야</p>'
        f"{render_bars(industries[:SUMMARY_INDUSTRY_PREVIEW])}"
        f'<a class="co-more" href="{DETAIL_URL}">XJTLU 한국인 진로 사례 자세히 보기 →</a>'
        f"</section>"
    )


def render_employers(data: dict) -> str:
    copy = data["copy"]
    emp = data["employers"]
    tier2 = render_chips(emp["tier2"])
    tier3 = "".join(f"<li>{esc(name)}</li>" for name in emp["tier3"])
    group_chips = render_chips(emp["group_only_labels"])
    fold_body = (
        '<p class="co-sub">글로벌·전문기업</p>'
        + tier2
        + '<p class="co-sub">그 외 확인된 기업·기관</p>'
        + f'<ul class="co-textlist">{tier3}</ul>'
        + '<p class="co-sub">이름 대신 분야로만 표시하는 소규모·특수 기관</p>'
        + group_chips
    )
    return (
        f"{render_chips(emp['tier1'])}"
        f'<details class="co-fold"><summary>그 외 주요 기업 보기</summary><div class="co-fold-body">{fold_body}</div></details>'
        f'<p class="co-note">{esc(copy["employer_caveat"])}</p>'
    )


def render_industry(data: dict) -> str:
    industries = [(row["sector"], int(row["outcomes"])) for row in data["industry_stats"]]
    industries.sort(key=lambda row: row[1], reverse=True)
    return f"{render_bars(industries)}"


def render_patterns(data: dict) -> str:
    cards = "".join(
        '<article class="co-pattern">'
        f'<span>{esc(row["title"])}</span>'
        f'<strong>{esc(row["copy"])}</strong>'
        "</article>"
        for row in data["safe_marketing_highlights"]
    )
    return f'<div class="co-patterns">{cards}</div>'


def render_graduate(data: dict) -> str:
    copy = data["copy"]
    further = "".join(
        '<div class="co-region">'
        f'<strong>{esc(row["category"])}</strong>'
        f"{render_chips(row['institutions'])}"
        "</div>"
        for row in data["further_academic_pathways"]
    )
    return (
        f"{render_chips(data['graduate_destinations'])}"
        f'<p class="co-note">{esc(copy["graduate_caveat"])}</p>'
        f'<p class="co-sub">Further Academic Pathways — 편입·후속학업·교환</p>'
        f'<div class="co-regions co-regions-further">{further}</div>'
        f'<p class="co-note">{esc(copy["further_caveat"])}</p>'
    )


def format_month_ko(iso_date: str) -> str:
    year, month, _ = iso_date.split("-")
    return f"{year}년 {int(month)}월"


def render_method(data: dict) -> str:
    copy = data["copy"]
    return (
        f'<div class="notice"><p style="margin:0 0 12px">{esc(copy["methodology"])}</p>'
        f'<p style="margin:0">{esc(copy["privacy"])}</p></div>'
        f'<p class="co-note">인턴십 {data["kpis"]["internship_outcomes_separate"]}건은 위 취업·경력 사례와 별도로 확인되었으며 취업 KPI에는 합산하지 않았습니다.</p>'
        f'<p class="co-note">자료 기준일 · {esc(format_month_ko(data["meta"]["as_of"]))}</p>'
    )


def build(data: dict) -> dict[str, dict[str, str]]:
    return {
        SUMMARY_URL: {"CAREER_SUMMARY": render_summary(data)},
        DETAIL_URL: {
            "CAREER_KPI": render_headline_kpis(data),
            "CAREER_EMPLOYERS": render_employers(data),
            "CAREER_INDUSTRY": render_industry(data),
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
