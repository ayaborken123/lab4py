from fastapi import FastAPI, Depends, HTTPException, Header, Body
from pydantic import BaseModel
import ollama
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

app = FastAPI()

# Configuration de sécurité
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY manquante dans .env")

class PromptRequest(BaseModel):
    prompt: str

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Clé API invalide")
    return True

@app.post("/generate")
def generate(
    request: PromptRequest,
    _: bool = Depends(verify_api_key)
):
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": request.prompt}]
    )
    return {"response": response["message"]["content"]}

@app.get("/")
def health_check():
    return {"status": "OK"}