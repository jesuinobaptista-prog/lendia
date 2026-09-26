import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Configuração da API do Gemini
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
APP_PIN = os.getenv("APP_PIN", "1234")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    message: str
    pin: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    if req.pin != APP_PIN:
        raise HTTPException(status_code=401, detail="PIN de acesso incorreto.")
    
    try:
        response = model.generate_content(req.message)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
