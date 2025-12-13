import os
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter

INPUT_FILE = "C:/Ro1/Test/loan-product-assistant/data/processed/knowledge_base.txt"
CHUNK_OUTPUT = "C:/Ro1/Test/loan-product-assistant/data/processed/chunks.txt"

# Recommended RAG chunking configuration
CHUNK_SIZE = 500        # Target size
CHUNK_OVERLAP =200     # Overlap for context retention


def chunk_text():
    print("✂️ Creating high-quality recursive chunks...")

    # Load cleaned knowledge base text
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Recursive Character Text Splitter (BEST FOR RAG)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",   # Split by paragraphs first
            "\n",     # Then by lines
            ". ",     # Then by sentences
            " ",      # Then by spaces
            ""        # Finally at character level
        ]
    )

    chunks = splitter.split_text(full_text)

    # Save chunks
    with open(CHUNK_OUTPUT, "w", encoding="utf-8") as f:
        for ch in chunks:
            f.write(ch.strip() + "\n\n---chunk---\n\n")

    print(f"✅ Created {len(chunks)} high-quality chunks using recursive splitting!")


if __name__ == "__main__":
    chunk_text()