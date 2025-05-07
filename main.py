from fastapi import FastAPI
from pydantic import BaseModel  # <-- Ajouter cette ligne
import ollama

app = FastAPI()

class PromptRequest(BaseModel):  # <-- Définir le modèle de données
    prompt: str

@app.post("/generate")
def generate(request: PromptRequest):  # <-- Utiliser le modèle comme paramètre
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": request.prompt}]  # <-- Accéder au prompt via request
    )
    return {"response": response["message"]["content"]}