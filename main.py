from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import ollama
import os
from dotenv import load_dotenv
from typing import Dict

app = FastAPI()
load_dotenv()

# Configuration initiale
API_KEYS: Dict[str, int] = {
    os.getenv("API_KEY"): 5  # 5 crédits initiaux pour la clé principale
}

class PromptRequest(BaseModel):
    prompt: str

def verify_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    if x_api_key not in API_KEYS or API_KEYS[x_api_key] <= 0:
        raise HTTPException(
            status_code=402,
            detail="Clé API invalide ou crédits épuisés"
        )
    return x_api_key

@app.post("/generate")
def generate(
    request: PromptRequest,
    api_key: str = Depends(verify_api_key)
):
    try:
        # Déduction du crédit avant traitement
        API_KEYS[api_key] -= 1
        
        # Appel à l'API Ollama
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": request.prompt}]
        )
        
        return {
            "response": response["message"]["content"],
            "remaining_credits": API_KEYS[api_key]
        }
        
    except Exception as e:
        API_KEYS[api_key] += 1  # Rollback en cas d'erreur
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/credits")
def check_credits(api_key: str = Depends(verify_api_key)):
    return {"remaining_credits": API_KEYS[api_key]}