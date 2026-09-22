from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DETAIL_PAGES = sorted(ROOT.glob("xjtlu-*.html"))

SOURCE_SECTION_BY_ATTR = re.compile(
    r"\n?<section\b[^>]*(?:"
    r"class\s*=\s*[\"'][^\"']*\b(?:sources?|references)\b[^\"']*[\"']"
    r"|id\s*=\s*[\"'](?:sources?|references)[\"'])[^>]*>.*?</section>\s*",
    re.IGNORECASE | re.DOTALL,
)

SOURCE_SECTION_BY_LABEL = re.compile(
    r"\n?<section\b[^>]*>.*?(?:"
    r"자료\s*출처"
    r"|<h[1-6][^>]*>\s*(?:출처|Sources?|References?)\s*</h[1-6]>"
    r").*?</section>\s*",
    re.IGNORECASE | re.DOTALL,
)

VISIBLE_SOURCE_LABEL = re.compile(
    r"자료\s*출처|<h[1-6][^>]*>\s*(?:출처|Sources?|References?)\s*</h[1-6]>",
    re.IGNORECASE,
)


def cleaned(text: str) -> str:
    previous = None
    while text != previous:
        previous = text
        text = SOURCE_SECTION_BY_ATTR.sub("\n", text)
        text = SOURCE_SECTION_BY_LABEL.sub("\n", text)
    return text


def main(check: bool = False) -> int:
    changed: list[str] = []
    remaining: list[str] = []

    for path in DETAIL_PAGES:
        original = path.read_text(encoding="utf-8")
        updated = cleaned(original)
        if updated != original:
            changed.append(path.name)
            if not check:
                path.write_text(updated, encoding="utf-8")
        if VISIBLE_SOURCE_LABEL.search(updated):
            remaining.append(path.name)

    if remaining:
        raise SystemExit(
            "Visible source labels remain in non-news detail pages: " + ", ".join(remaining)
        )

    if check and changed:
        raise SystemExit(
            "Source cleanup is not rendered yet for: " + ", ".join(changed)
        )

    if changed and not check:
        print("Removed visible source sections from: " + ", ".join(changed))
    else:
        print("No visible source sections remain in non-news detail pages")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(check=args.check))
