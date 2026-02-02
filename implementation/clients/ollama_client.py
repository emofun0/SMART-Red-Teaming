"""Ollama API client for target model (defender)."""

from typing import Optional

import requests

from implementation.config import AttackConfig


class OllamaTargetClient:
    """Client for local Ollama /generate endpoint."""

    def __init__(self, config: Optional[AttackConfig] = None):
        self._config = config or AttackConfig.from_env()
        self._url = self._config.ollama_generate_url
        self._model = self._config.target_model

    def generate(self, prompt: str, stream: bool = False) -> str:
        """Send prompt to target model and return response text."""
        try:
            resp = requests.post(
                self._url,
                json={
                    "model": self._model,
                    "prompt": prompt,
                    "stream": stream,
                },
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json().get("response", "")
        except requests.RequestException as e:
            return f"[Error] Ollama connection failed: {e}"
