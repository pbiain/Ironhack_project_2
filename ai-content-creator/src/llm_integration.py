"""LLM API integration module."""

import os


class LLMIntegration:
    """Wrapper for LLM provider API usage."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
