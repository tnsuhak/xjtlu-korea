#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "xjtlu-masters-2027.json"

EXPECTED_TOTAL = 54
EXPECTED_DEGREES = {"MSc": 32, "MRes": 13, "MA": 7, "MArch": 1, "MDes": 1}

def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    programmes = data["programmes"]

    assert len(programmes) == EXPECTED_TOTAL, (len(programmes), EXPECTED_TOTAL)
    assert data["meta"]["scope"]["public_catalogue_mode"] == "full_time_only"
    assert data["meta"]["scope"]["part_time_programmes_excluded"] is True
    assert all(p["attendance"] == "full_time" for p in programmes)
    assert not any("part time" in p["name_en"].lower() or "part-time" in p["name_en"].lower() for p in programmes)
    assert not any(p["name_en"] == "International MBA" for p in programmes)

    counts = Counter(p["degree_type"] for p in programmes)
    assert dict(counts) == EXPECTED_DEGREES, counts

    ids = [p["id"] for p in programmes]
    names = [p["name_en"] for p in programmes]
    assert len(ids) == len(set(ids)), "Duplicate programme id"
    assert len(names) == len(set(names)), "Duplicate programme name"

    required = [
        "id", "name_en", "degree_type", "school", "attendance", "campus",
        "full_time_duration_months", "tuition_2026_rmb_total",
        "tuition_2027_status", "intake_2027_status", "ielts_academic",
        "undergraduate_background_ko", "mres_full_tuition_scholarship_eligible"
    ]
    for p in programmes:
        missing = [k for k in required if k not in p]
        assert not missing, f"{p.get('name_en')}: missing {missing}"
        assert p["full_time_duration_months"] in {18, 24}, p["name_en"]
        assert p["tuition_2026_rmb_total"] in {150000, 180000, 200000}, p["name_en"]
        assert p["ielts_academic"]["overall"] in {6.0, 6.5, 7.0}, p["name_en"]
        assert p["ielts_academic"]["minimum_each"] in {5.5, 6.0}, p["name_en"]
        assert p["mres_full_tuition_scholarship_eligible"] == (p["degree_type"] == "MRes"), p["name_en"]

    print(f"OK: {len(programmes)} full-time XJTLU masters programmes validated")
    print("Degree counts:", dict(counts))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
