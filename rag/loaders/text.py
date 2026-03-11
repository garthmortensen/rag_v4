"""Plain-text loader for .txt, .md, .rst, .html, .htm, .csv files."""

import os

from rag.core.types import Document

TEXT_EXTENSIONS: frozenset[str] = frozenset(
    {".txt", ".md", ".rst", ".html", ".htm", ".csv"}
)


class TextLoader:
    def __init__(self, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def load(self, source: str) -> list[Document]:
        with open(source, encoding=self.encoding, errors="replace") as f:
            text = f.read().strip()
        if not text:
            return []
        return [
            Document(
                text=text,
                metadata={
                    "source": source,
                    "filename": os.path.basename(source),
                    "source_type": os.path.splitext(source)[1].lstrip("."),
                },
            )
        ]
