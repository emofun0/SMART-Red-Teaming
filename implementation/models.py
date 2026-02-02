"""Data models for agent inputs/outputs and workflow state."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StrategyOutput:
    """Strategist agent output: thought + search keywords for vector DB."""

    thought: str
    search_keywords: str  # can be space-separated or single phrase

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StrategyOutput":
        return cls(
            thought=d.get("thought", ""),
            search_keywords=d.get("search_keywords", ""),
        )


@dataclass
class JudgeResult:
    """Judge agent output: score (0/1) and reason."""

    score: int  # 0 = fail, 1 = success
    reason: str

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "JudgeResult":
        return cls(
            score=int(d.get("score", 0)),
            reason=str(d.get("reason", "")),
        )


@dataclass
class AttemptRecord:
    """Single attempt: prompt used and judge feedback (for mutator history)."""

    prompt: str
    reason: str


@dataclass
class RetrievedTemplate:
    """One item from vector store: document + metadata name."""

    document: str
    name: str
