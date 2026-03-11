"""PDF loader using pypdf (no LangChain)."""

import os

from rag.core.types import Document


class PDFLoader:
    def load(self, source: str) -> list[Document]:
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ImportError("pypdf is required: uv add pypdf")

        reader = PdfReader(source)
        docs: list[Document] = []
        for i, page in enumerate(reader.pages):
            text = (page.extract_text() or "").strip()
            if not text:
                continue
            docs.append(
                Document(
                    text=text,
                    metadata={
                        "source": source,
                        "filename": os.path.basename(source),
                        "page": i + 1,
                        "total_pages": len(reader.pages),
                        "source_type": "pdf",
                    },
                )
            )
        return docs
