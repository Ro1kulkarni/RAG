from fastapi import FastAPI
from rag.rag_pipeline import answer_question

app = FastAPI()

@app.get("/ask")
def ask(q: str):
    return {"answer": answer_question(q)}
