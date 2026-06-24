import httpx
import os
import sys
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b:free")

RESOLVED_MODEL = None

def chat(history: list[dict]) -> str:
    global RESOLVED_MODEL
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://adepttech.solutions", #optional
        "X-Title": "ATS Internship Chatbot", #optional
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
        data = response.json()
        RESOLVED_MODEL = data.get("model", MODEL)
        return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"[ERROR] HTTP {e.response.status_code}: {e.response.text}"
    except httpx.RequestError as e:
        return f"[ERROR] Network error: {e}"

def main():
    if not OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set in .env")
        sys.exit(1)

    print("=" * 50)
    print(f"  OpenRouter Chatbot — {MODEL}")
    print("  Type 'quit' to exit")
    print("=" * 50 + "\n")

    # conversation history- grows with each turn
    history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        reply = chat(history)
        if reply.startswith("[ERROR]"):
            history.pop()  # remove unanswered user message, keep context clean
            print(f"\nAssistant: {reply}\n")
            continue

        history.append({"role": "assistant", "content": reply})

        if len(history) == 3:  # first turn only
            print(f"  [model: {RESOLVED_MODEL}]")

        print(f"\nAssistant: {reply}\n")

if __name__ == "__main__":
    main()