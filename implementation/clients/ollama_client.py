"""Ollama API client for target model (defender)."""

from typing import Optional

import requests

from implementation.config import AttackConfig


class OllamaConnectionError(Exception):
    """Raised when Ollama is unreachable or target model is not available."""

    pass


class OllamaTargetClient:
    """Client for local Ollama /generate endpoint."""

    def __init__(self, config: Optional[AttackConfig] = None):
        self._config = config or AttackConfig.from_env()
        self._base_url = self._config.ollama_base_url.rstrip("/")
        self._url = self._config.ollama_generate_url
        self._model = self._config.target_model

    def check_connection(self) -> None:
        """
        Verify Ollama is reachable and the configured target model exists.
        Raises OllamaConnectionError if the service is down or model is missing.
        """
        try:
            resp = requests.get(
                f"{self._base_url}/api/tags",
                timeout=10,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise OllamaConnectionError(
                f"Ollama is not reachable at {self._base_url}. "
                f"Ensure Ollama is running (e.g. ollama serve). Error: {e}"
            ) from e

        data = resp.json()
        models = data.get("models") or []
        available = [m.get("name", "") for m in models]
        if not any(
            name == self._model or name.startswith(self._model + ":") or self._model.startswith(name)
            for name in available
        ):
            raise OllamaConnectionError(
                f"Target model '{self._model}' is not available. "
                f"Pull it with: ollama pull {self._model}"
            )

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
