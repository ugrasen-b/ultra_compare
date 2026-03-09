from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


@dataclass(frozen=True)
class PageRange:
    start: int
    end: int

    def normalize(self, total_pages: int) -> "PageRange":
        if self.start < 1 or self.end < 1:
            raise ValueError("Page numbers must be 1-based and positive.")
        if self.end < self.start:
            raise ValueError("End page must be >= start page.")
        if self.start > total_pages:
            raise ValueError("Start page exceeds total pages.")
        return PageRange(self.start, min(self.end, total_pages))


def _iter_pages(reader: PdfReader, pages: PageRange | None) -> Iterable[str]:
    total_pages = len(reader.pages)
    if total_pages == 0:
        return []
    if pages is None:
        return (page.extract_text() or "" for page in reader.pages)

    normalized = pages.normalize(total_pages)
    # PdfReader pages are 0-based index
    page_slice = reader.pages[normalized.start - 1 : normalized.end]
    return (page.extract_text() or "" for page in page_slice)


def extract_text(path: str | Path, pages: PageRange | None = None) -> str:
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    reader = PdfReader(str(pdf_path))
    chunks = list(_iter_pages(reader, pages))
    return "\n".join(chunks).strip()


__all__ = ["PageRange", "extract_text"]
