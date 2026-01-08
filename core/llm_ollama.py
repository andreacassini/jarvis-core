cat > core/llm_ollama.py <<'PY'
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

SYSTEM = (
    "Sei Jarvis, assistente domestico. "
    "Parla sempre in italiano, tono naturale e conciso. "
    "Regola critica: NON inventare azioni o risultati. "
    "Se l'utente chiede di fare qualcosa sul PC/domotica, rispondi che devi usare un tool e chiedi conferma/dettagli. "
    "Non dire mai: 'ho aperto', 'ho fatto', 'tutto pronto' se non hai un risultato reale."
)

def chat(text: str) -> str:
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": text},
            ],
        },
        timeout=120,
    )
    r.raise_for_status()
    return (r.json().get("message", {}).get("content") or "").strip()
PY