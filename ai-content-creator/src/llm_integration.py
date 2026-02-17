"""LLM API integration module."""
import os
from openai import OpenAI


class LLMIntegration:
    """Wrapper for LLM provider API usage."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")

"""
Handles communication with the LLM.
"""

def generate_content(prompt: str) -> str:
    """
    Sends a prompt to the LLM and returns the generated text.
    """

    # Create client using API key from environment
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Safe + affordable
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content