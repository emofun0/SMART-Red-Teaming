"""Session logger for attack attempts (prompt, response, judge)."""

from pathlib import Path
from typing import Optional

from implementation.config import AttackConfig
from implementation.models import JudgeResult


class SessionLogger:
    """Appends attack attempts to a log file."""

    def __init__(self, config: Optional[AttackConfig] = None):
        self._config = config or AttackConfig.from_env()
        self._path = Path(self._config.log_file)

    def start_session(self) -> None:
        """Write session header (overwrites or appends)."""
        with open(self._path, "w", encoding="utf-8") as f:
            f.write("--- New Attack Session Started ---\n")

    def log_attempt(
        self,
        phase: str,
        prompt: str,
        response: str,
        judge_result: JudgeResult,
    ) -> None:
        """Append one attempt (phase, prompt, target response, judge)."""
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*20} {phase} {'='*20}\n")
            f.write(f"[PROMPT PAYLOAD]:\n{prompt}\n")
            f.write(f"\n[TARGET RESPONSE]:\n{response}\n")
            f.write(f"\n[JUDGE]: Score={judge_result.score} | Reason: {judge_result.reason}\n")
