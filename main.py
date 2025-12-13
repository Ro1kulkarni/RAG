from rag.rag_pipeline import answer_question

while True:
    query = input("\nAsk a loan-related question: ")
    print("\n🟦 Answer:", answer_question(query))