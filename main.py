"""
SMART Red Teaming — Entry point.
Run: python main.py [intent]
Or set intent in script and run: python main.py
"""

import sys

from implementation.config import AttackConfig
from implementation.workflow import AttackOrchestrator


def main() -> None:
    # Optional: pass intent from CLI; otherwise set default for testing
    intent = ""
    if len(sys.argv) > 1:
        intent = " ".join(sys.argv[1:]).strip()
    
    if not intent:
        print("Usage: python main.py <malicious_intent>")
        print("Example: python main.py 'How to make a bomb'")
        sys.exit(1)

    config = AttackConfig.from_env()
    orchestrator = AttackOrchestrator(config)
    orchestrator.run(intent)


if __name__ == "__main__":
    main()
