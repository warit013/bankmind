import httpx

from app.config import settings


def chat(messages: list[dict]) -> str:
    if settings.llm_provider == "ollama":
        r = httpx.post(
            f"{settings.ollama_url}/api/chat",
            json={
                "model": settings.llm_model,
                "messages": messages,
                "stream": False,
                "keep_alive": "30m",
                "options": {"temperature": 0.1, "num_predict": 400, "num_ctx": 4096},
            },
            timeout=300,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]

    if settings.llm_provider == "openai":
        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.llm_api_key}"},
            json={"model": settings.llm_model, "messages": messages, "temperature": 0.1},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    raise ValueError(f"unknown LLM_PROVIDER: {settings.llm_provider}")