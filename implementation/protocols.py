"""Protocols (interfaces) for Target and Judge. Enables swapping implementations."""

from typing import Protocol, runtime_checkable

from implementation.models import JudgeResult


@runtime_checkable
class TargetProtocol(Protocol):
    """Interface for the model under attack (e.g. Ollama, OpenAI, Anthropic)."""

    def generate(self, prompt: str, stream: bool = False) -> str:
        """Send prompt to the target model and return response text."""
        ...

    def check_connection(self) -> None:
        """Verify the target is reachable and the configured model is available. Raise on failure."""
        ...


@runtime_checkable
class JudgeProtocol(Protocol):
    """Interface for the evaluator that scores (prompt, response) for harmful content."""

    def run(self, attack_prompt: str, target_response: str) -> JudgeResult:
        """Return structured JudgeResult (score, reason, refusal_type, categories, etc.)."""
        ...
