import os
import datetime
import zoneinfo

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.schemas import ChatRequest, ChatResponse

load_dotenv()

app = FastAPI()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")


def is_peak_hour() -> bool:
    now = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Shanghai"))
    if now.weekday() >= 5:
        return False
    return (9 <= now.hour < 12) or (14 <= now.hour < 18)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY not set")

    peak = is_peak_hour()

    if peak:
        input_price = float(os.getenv("DEEPSEEK_PEAK_INPUT_MISS", "2"))
        output_price = float(os.getenv("DEEPSEEK_PEAK_OUTPUT", "8"))
    else:
        input_price = float(os.getenv("DEEPSEEK_OFFPEAK_INPUT_MISS", "1"))
        output_price = float(os.getenv("DEEPSEEK_OFFPEAK_OUTPUT", "4"))

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": req.prompt}],
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=60, trust_env=False) as client:
        resp = await client.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=resp.text)

    data = resp.json()
    answer = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})

    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)

    cost_cny = (
        prompt_tokens / 1_000_000 * input_price
        + completion_tokens / 1_000_000 * output_price
    )

    return ChatResponse(
        answer=answer,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost_cny=round(cost_cny, 6),
    )