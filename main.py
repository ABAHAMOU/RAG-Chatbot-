from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_service import generer_reponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    history: list[dict] = []  

@app.post("/chat")
async def chat(payload: ChatRequest):
    reponse = generer_reponse(payload.question, payload.history)
    return {"answer": reponse}
