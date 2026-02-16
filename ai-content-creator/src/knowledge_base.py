"""Primary and secondary knowledge base management."""

from pathlib import Path


class KnowledgeBase:
    """Simple knowledge base loader."""

    def __init__(self, primary_path: Path, secondary_path: Path):
        self.primary_path = primary_path
        self.secondary_path = secondary_path

# src/knowledge_base.py

# Import helper functions from document_processor
from document_processor import load_markdown, extract_section


# This function builds a structured knowledge dictionary
# from the brand_guidelines markdown file.
def build_brand_knowledge(file_path):

    # Load the full markdown content
    content = load_markdown(file_path)

    # Extract different sections of the document
    brand_voice = extract_section(content, "## 1. Brand Voice", "## 2.")
    tone_guidelines = extract_section(content, "## 2. Tone Guidelines", "## 3.")
    messaging = extract_section(content, "## 3. Key Messaging Framework", "## 4.")
    audience = extract_section(content, "## 4. Target Audience Personas", "## 5.")

    # Return a dictionary (this will later become JSON)
    return {
        "brand_voice": brand_voice,
        "tone_guidelines": tone_guidelines,
        "messaging_framework": messaging,
        "target_audience": audience
    }
