"""Groq LLM call over plain HTTP (no function calling). Tries GROQ_MODEL first, then the fallback model."""
import re

import requests

import config

URL = "https://api.groq.com/openai/v1/chat/completions"


def chat(system, user, temperature=0.2):
    if not config.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing (check .env or Streamlit secrets)")
    last_err = "unknown error"
    for model in (config.GROQ_MODEL, config.GROQ_FALLBACK_MODEL):
        try:
            r = requests.post(
                URL,
                headers={"Authorization": f"Bearer {config.GROQ_API_KEY}"},
                json={"model": model, "temperature": temperature,
                      "max_completion_tokens": 2500,
                      "messages": [{"role": "system", "content": system},
                                   {"role": "user", "content": user}]},
                timeout=90,
            )
            if r.status_code != 200:
                last_err = f"{model}: HTTP {r.status_code} {r.text[:250]}"
                continue
            content = r.json()["choices"][0]["message"].get("content") or ""
            content = re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()
            if content:
                return content
            last_err = f"{model}: empty answer"
        except Exception as e:
            last_err = f"{model}: {e}"
    raise RuntimeError(f"Groq call failed. {last_err}")
