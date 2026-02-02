"""Gemini LLM client for strategist, assembler, judge, and mutator agents."""

import json
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from implementation.config import get_google_api_key


class GeminiLLMClient:
    """Wrapper around Google Gemini API with safety settings for red teaming."""

    DEFAULT_SAFETY_SETTINGS: List[Dict[str, str]] = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        safety_settings: Optional[List[Dict[str, str]]] = None,
    ):
        key = api_key or get_google_api_key()
        genai.configure(api_key=key)
        self._model_name = model_name
        self._safety = safety_settings or self.DEFAULT_SAFETY_SETTINGS
        self._model = genai.GenerativeModel(model_name, safety_settings=self._safety)

    def generate(self, prompt: str) -> str:
        """Generate text from prompt. Raises on API error."""
        response = self._model.generate_content(prompt)
        if not response.text:
            raise ValueError("Empty response from Gemini")
        return response.text.strip()

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """Generate and parse JSON from prompt. Cleans markdown code blocks."""
        raw = self.generate(prompt)
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
