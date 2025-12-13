import requests
import faiss
import numpy as np
from rag.embedder import get_embedding
import json

VECTOR_STORE = "C:/Ro1/Test/loan-product-assistant/data/processed/vector_store.index"
CHUNK_FILE = "C:/Ro1/Test/loan-product-assistant/data/processed/chunks.txt"

# Load chunks
with open(CHUNK_FILE, "r", encoding="utf-8") as f:
    CHUNKS = [c.strip() for c in f.read().split("---chunk---")]

# Load FAISS index
index = faiss.read_index(VECTOR_STORE)

# Function to call Ollama locally
def call_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt},
        stream=True
    )

    final_text = ""

    for line in response.iter_lines():
        if not line:
            continue

        try:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                final_text += data["response"]
        except:
            continue

    return final_text

# Main RAG function
def answer_question(question: str):
    # Embed question
    q_emb = np.array([get_embedding(question)]).astype("float32")

    # Search top 3 chunks
    _, I = index.search(q_emb, 3)

    retrieved_chunks = "\n\n".join(
        [CHUNKS[i] for i in I[0] if i < len(CHUNKS)]
    )

    # Final prompt for the model
    prompt = f"""
You are a Bank of Maharashtra Loan Assistant AI.
Use ONLY the context below to answer the question accurately.

Context:
{retrieved_chunks}

Question: {question}

Answer:
"""

    # Generate answer using Ollama
    return call_ollama(prompt)
