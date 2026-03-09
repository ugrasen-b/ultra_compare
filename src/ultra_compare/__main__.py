from __future__ import annotations

import argparse
from pathlib import Path

from .pdf_extract import PageRange, extract_text


def _parse_page_range(raw: str | None) -> PageRange | None:
    if raw is None:
        return None
    if "-" not in raw:
        page = int(raw)
        return PageRange(page, page)
    start_raw, end_raw = raw.split("-", 1)
    return PageRange(int(start_raw), int(end_raw))


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from a PDF.")
    parser.add_argument("pdf", type=Path, help="Path to PDF file")
    parser.add_argument(
        "--pages",
        type=str,
        default=None,
        help="Page range (1-based), e.g. 1-3 or 2",
    )
    args = parser.parse_args()

    pages = _parse_page_range(args.pages)
    text = extract_text(args.pdf, pages)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
