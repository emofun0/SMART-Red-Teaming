"""Build jailbreak template vector DB from HuggingFace dataset. Reusable for auto-init."""

from typing import Optional

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions
from datasets import load_dataset

from implementation.config import AttackConfig

BATCH_SIZE = 100
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DATASET_NAME = "rubend18/ChatGPT-Jailbreak-Prompts"


def build_jailbreak_db(config: Optional[AttackConfig] = None, verbose: bool = True) -> None:
    """
    Download dataset, create ChromaDB collection, and populate with embeddings.
    Idempotent: recreates the collection if it exists (same as prebuilt script).
    """
    cfg = config or AttackConfig.from_env()
    if verbose:
        print("Downloading rubend18/ChatGPT-Jailbreak-Prompts from HuggingFace...")
    try:
        dataset = load_dataset(DATASET_NAME, split="train")
        df = pd.DataFrame(dataset)
        if verbose:
            print("Download success!")
    except Exception as e:
        raise RuntimeError(f"Failed to load dataset {DATASET_NAME}: {e}") from e

    df = df.dropna(subset=["Prompt"])
    prompts = df["Prompt"].tolist()
    names = df["Name"].tolist()
    if verbose:
        print(f"In total {len(prompts)} valid attack templates.")

    if verbose:
        print("Initializing ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=cfg.db_path)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    try:
        chroma_client.delete_collection(cfg.collection_name)
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name=cfg.collection_name,
        embedding_function=sentence_transformer_ef,
    )

    if verbose:
        print("Storing to DB (Embedding)...")
    ids = [str(i) for i in range(len(prompts))]
    metadatas = [{"source": "rubend18", "name": name} for name in names]

    for i in range(0, len(prompts), BATCH_SIZE):
        end = min(i + BATCH_SIZE, len(prompts))
        collection.add(
            documents=prompts[i:end],
            metadatas=metadatas[i:end],
            ids=ids[i:end],
        )

    if verbose:
        print("DB build success!")
