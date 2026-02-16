"""Markdown document ingestion and processing."""


class DocumentProcessor:
    """Handles loading and preprocessing markdown documents."""

    def ingest(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
