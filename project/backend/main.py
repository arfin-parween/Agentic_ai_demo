from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import traceback

from ai_agent import run_agent

app = FastAPI(title="SafeSpace AI Therapist", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(query: Query):
    try:
        tool_called, response, demo_mode = run_agent(query.message)
        return {
            "response": response,
            "tool_called": tool_called,
            "demo_mode": demo_mode,
        }
    except Exception as e:
        print("🔥 /ask crashed:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))