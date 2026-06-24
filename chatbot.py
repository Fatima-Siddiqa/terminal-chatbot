import httpx
import os
import sys
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b:free")

def chat(history: list[dict]) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://adepttech.solutions",
        "X-Title": "ATS Internship Chatbot",
    }
    payload = {
        "model": MODEL,
        "messages": history,
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    try:
        response = httpx.post(BASE_URL, headers=headers, json=payload, timeout=60.0)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"[ERROR] HTTP {e.response.status_code}: {e.response.text}"
    except httpx.RequestError as e:
        return f"[ERROR] Network error: {e}"