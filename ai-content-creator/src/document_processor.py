"""Markdown document ingestion and processing."""


class DocumentProcessor:
    """Handles loading and preprocessing markdown documents."""

    def ingest(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


# This function reads a markdown file and returns its full text as a string.
def load_markdown(file_path):
    # Open the file in read mode with UTF-8 encoding
    with open(file_path, "r", encoding="utf-8") as f:
        # Read all file content
        return f.read()


# This function extracts a section of text between two markers.
# Example:
# extract_section(content, "## 1. Brand Voice", "## 2.")
def extract_section(content, start_marker, end_marker=None):
    try:
        # Split content at the start marker
        section = content.split(start_marker)[1]

        # If an end marker is provided, stop at that marker
        if end_marker:
            section = section.split(end_marker)[0]

        # Remove extra spaces and return clean text
        return section.strip()

    except IndexError:
        # If markers are not found, return empty string
        return ""
