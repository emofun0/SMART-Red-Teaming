"""
Build jailbreak template vector DB from HuggingFace dataset.
Run once: python prebuilt_jailbreak_db.py
Uses implementation.config for DB path and collection name.
Same logic is used automatically by main.py if the DB is missing.
"""

from implementation.memory.db_builder import build_jailbreak_db


def main() -> None:
    build_jailbreak_db(verbose=True)


if __name__ == "__main__":
    main()
