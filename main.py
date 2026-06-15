import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from prompt import PROMPT
from fastapi.responses import FileResponse

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = FastAPI()

# Lets a webpage call this server (browsers block that by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# The incoming request: ticket text, 1–5000 characters (a size check)
class Ticket(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/analyze")
def analyze_ticket(ticket: Ticket):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=PROMPT,
        messages=[{"role": "user", "content": ticket.text}],
    )
    reply = message.content[0].text
    start = reply.find("{")
    end = reply.rfind("}")
    # Claude should return clean JSON; if it ever doesn't, fail clearly instead of crashing
    try:
        return json.loads(reply[start:end + 1])
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(
            status_code=502,
            detail="The analyzer returned an unexpected response. Please try again.",
        )