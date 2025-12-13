import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNK_FILE = "C:/Ro1/Test/loan-product-assistant/data/processed/chunks.txt"
VECTOR_STORE = "C:/Ro1/Test/loan-product-assistant/data/processed/vector_store.index"

# Load best free embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def get_embedding(text: str):
    """Return embedding using free MiniLM model"""
    return model.encode(text, convert_to_numpy=True)


def build_vector_store():
    print("🔧 Building FAISS vector store...")

    # Load chunks
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = [c.strip() for c in f.read().split("---chunk---") if c.strip()]

    # Create embeddings
    embeddings = np.array([get_embedding(chunk) for chunk in chunks]).astype("float32")

    # Create FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index
    faiss.write_index(index, VECTOR_STORE)

    print("✅ Vector store saved at:", VECTOR_STORE)


if __name__ == "__main__":
    build_vector_store()