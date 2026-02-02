"""Configuration and environment settings."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class AttackConfig:
    """Immutable attack session configuration."""

    target_model: str = "phi4-reasoning:14b"
    ollama_base_url: str = "http://localhost:11434"
    max_rounds: int = 30
    db_path: str = "./jailbreak_memory_db"
    collection_name: str = "jailbreak_prompts"
    log_file: str = "attack_session.log"
    retrieval_top_k: int = 3

    @property
    def ollama_generate_url(self) -> str:
        return f"{self.ollama_base_url.rstrip('/')}/api/generate"

    @classmethod
    def from_env(cls, **overrides) -> "AttackConfig":
        """Build config from environment with optional overrides."""
        return cls(
            target_model=overrides.get("target_model", os.getenv("TARGET_MODEL", "llama3.1:8b")),
            ollama_base_url=overrides.get("ollama_base_url", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")),
            max_rounds=int(overrides.get("max_rounds", os.getenv("MAX_ROUNDS", "30"))),
            db_path=overrides.get("db_path", os.getenv("DB_PATH", "./jailbreak_memory_db")),
            collection_name=overrides.get("collection_name", os.getenv("COLLECTION_NAME", "jailbreak_prompts")),
            log_file=overrides.get("log_file", os.getenv("LOG_FILE", "attack_session.log")),
            retrieval_top_k=int(overrides.get("retrieval_top_k", os.getenv("RETRIEVAL_TOP_K", "3"))),
        )


def get_google_api_key() -> str:
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY not set in environment or .env")
    return key
