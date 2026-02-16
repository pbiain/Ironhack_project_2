"""Primary and secondary knowledge base management."""

from pathlib import Path


class KnowledgeBase:
    """Simple knowledge base loader."""

    def __init__(self, primary_path: Path, secondary_path: Path):
        self.primary_path = primary_path
        self.secondary_path = secondary_path
