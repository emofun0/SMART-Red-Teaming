import pandas as pd
import chromadb
from datasets import load_dataset
from chromadb.utils import embedding_functions

print("Downloading rubend18/ChatGPT-Jailbreak-Prompts from HuggingFace...")
try:
    dataset = load_dataset("rubend18/ChatGPT-Jailbreak-Prompts", split="train")
    df = pd.DataFrame(dataset)
    print("Download success!")
except Exception as e:
    print(e)
    exit()

df = df.dropna(subset=['Prompt'])
prompts = df['Prompt'].tolist()
names = df['Name'].tolist()

print(f"In total {len(prompts)} valid attack templates.")

print("Initializing ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./jailbreak_memory_db")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

try:
    chroma_client.delete_collection("jailbreak_prompts")
except:
    pass

collection = chroma_client.create_collection(
    name="jailbreak_prompts",
    embedding_function=sentence_transformer_ef
)

print("Storing to DB (Embedding)...")

ids = [str(i) for i in range(len(prompts))]
metadatas = [{"source": "rubend18", "name": name} for name in names]

batch_size = 100
for i in range(0, len(prompts), batch_size):
    end = min(i + batch_size, len(prompts))
    collection.add(
        documents=prompts[i:end],
        metadatas=metadatas[i:end],
        ids=ids[i:end]
    )

print("DB build success!")

print("\n--- Retrieval Test (Memory Recall) ---")
test_query = "Developer Mode"
results = collection.query(
    query_texts=[test_query],
    n_results=1
)

print(f"Quering: {test_query}")
print(f"Matching template ({results['metadatas'][0][0]['name']}):")
print("-" * 50)
print(results['documents'][0][0]) 
print("-" * 50)
