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
    """
    Structured judge output for scoring and downstream use (Mutator, stats).
    score: 0 = fail (no harmful content), 1 = success (harmful content present).
    refusal_type: why the attempt failed (for Mutator to adapt).
    categories: harm categories touched (for aggregation and reporting).
    """

    score: int  # 0 = fail, 1 = success
    reason: str
    refusal_type: str = ""  # e.g. refused, partial, off_topic, role_only, clarification
    categories: List[str] = field(default_factory=list)  # e.g. dangerous, illegal
    confidence: float = 0.0  # 0.0–1.0

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "JudgeResult":
        raw_cats = d.get("categories")
        if isinstance(raw_cats, list):
            categories = [str(x) for x in raw_cats]
        elif isinstance(raw_cats, str) and raw_cats:
            categories = [s.strip() for s in raw_cats.split(",") if s.strip()]
        else:
            categories = []
        return cls(
            score=int(d.get("score", 0)),
            reason=str(d.get("reason", "")),
            refusal_type=str(d.get("refusal_type", "")),
            categories=categories,
            confidence=float(d.get("confidence", 0.0)),
        )


@dataclass
class AttemptRecord:
    """Single attempt: prompt used and full judge result (for Mutator and stats)."""

    prompt: str
    judge_result: "JudgeResult"

    @property
    def reason(self) -> str:
        """Backward-compat access to judge reason."""
        return self.judge_result.reason


@dataclass
class RetrievedTemplate:
    """One item from vector store: document + metadata name."""

    document: str
    name: str
