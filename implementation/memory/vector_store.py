"""ChromaDB-backed vector store for jailbreak templates."""

from typing import List, Optional

import chromadb
from chromadb.errors import NotFoundError

from implementation.config import AttackConfig
from implementation.memory.db_builder import build_jailbreak_db
from implementation.models import RetrievedTemplate


class JailbreakVectorStore:
    """Persistent ChromaDB collection for jailbreak prompt templates."""

    def __init__(self, config: Optional[AttackConfig] = None, auto_build: bool = True):
        self._config = config or AttackConfig.from_env()
        self._client = chromadb.PersistentClient(path=self._config.db_path)
        self._collection = self._get_or_build_collection(auto_build)

    def _get_or_build_collection(self, auto_build: bool):
        """Get collection; if missing and auto_build, build DB then retry."""
        try:
            return self._client.get_collection(self._config.collection_name)
        except NotFoundError:
            if not auto_build:
                raise
            print(
                f"Collection [{self._config.collection_name}] not found. "
                "Building jailbreak DB (first run or DB missing)..."
            )
            build_jailbreak_db(self._config, verbose=True)
            return self._client.get_collection(self._config.collection_name)

    def search(self, query: str, top_k: Optional[int] = None) -> List[RetrievedTemplate]:
        """Semantic search; returns list of RetrievedTemplate."""
        k = top_k or self._config.retrieval_top_k
        results = self._collection.query(
            query_texts=[query],
            n_results=k,
        )
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        return [
            RetrievedTemplate(document=doc, name=meta.get("name", "unknown"))
            for doc, meta in zip(documents, metadatas)
        ]
