from core.llm_ollama import chat as ollama_chat

@app.post("/v1/chat", response_model=QueryOut)
def chat(q: UserQuery):
    try:
        reply = ollama_chat(q.text)
        return QueryOut(
            ok=True,
            speech=reply,
            plan=None,
            result=None,
            used_ai=True
        )
    except Exception as e:
        return QueryOut(
            ok=False,
            speech=f"Errore AI locale (Ollama): {e}",
            plan=None,
            result=None,
            used_ai=True
        )