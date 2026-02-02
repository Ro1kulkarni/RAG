# 🏦 Loan Product Assistant – Bank of Maharashtra  
A complete **Lightweight RAG (Retrieval-Augmented Generation)** system that helps users get accurate answers about **Bank of Maharashtra loan products** using scraped data, embeddings, vector search, and a local LLM (Ollama).

This is built as part of the **Generative AI Developer Technical Assessment**.

---

# 📌 Project Overview  
The goal of this project is to develop an AI assistant that can answer questions like:

- “What are the interest rates for a Bank of Maharashtra home loan?”
- “What is the tenure for personal loans?”
- “Tell me about the Maha Super Flexi Housing Loan.”
- “What are the processing fees for women applicants?”

To solve this, I built a **full RAG pipeline**:

1. **Scrape** public loan information from Bank of Maharashtra’s official website  
2. **Clean and preprocess** the scraped data  
3. **Chunk the text** and convert into vector embeddings  
4. **Store embeddings** inside a FAISS vector database  
5. **Retrieve relevant chunks** for each question  
6. **Use a local LLM** (Ollama + Llama2/Llama3) to generate final answers

This project demonstrates **end-to-end RAG architecture**, data handling, scraping, vector search, and LLM integration.

---

# 🧠 Features  
✔ Scrapes loan information (Home, Personal, Vehicle, Gold, Education loans)  
✔ Cleans unwanted HTML, ads, and navigation  
✔ Generates embeddings using Sentence Transformers  
✔ Stores all chunks in FAISS vector store  
✔ Queries the vector store to fetch the BEST matching chunks  
✔ Uses **Ollama** (totally FREE) for LLM answers  
✔ Command-line chatbot included  
✔ Fully modular folder structure  
✔ Easy to extend and deploy  

--- 

