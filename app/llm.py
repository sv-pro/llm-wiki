"""LLM client — OpenAI-compatible API (Ollama, LiteLLM, or any compatible endpoint)."""
from __future__ import annotations

import json
import os
from typing import AsyncIterator

import httpx

LLM_BASE_URL: str = os.environ.get("LLM_BASE_URL", "").rstrip("/")
LLM_MODEL: str = os.environ.get("LLM_MODEL", "")
LLM_API_KEY: str = os.environ.get("LLM_API_KEY", "")


def is_configured() -> bool:
    return bool(LLM_BASE_URL and LLM_MODEL)


def provider_label() -> str:
    if not LLM_BASE_URL:
        return "none"
    if "ollama" in LLM_BASE_URL or "11434" in LLM_BASE_URL:
        return "Ollama"
    if "4000" in LLM_BASE_URL or "litellm" in LLM_BASE_URL.lower():
        return "LiteLLM"
    return "OpenAI-compatible"


def _headers() -> dict[str, str]:
    h: dict[str, str] = {"Content-Type": "application/json"}
    if LLM_API_KEY:
        h["Authorization"] = f"Bearer {LLM_API_KEY}"
    return h


async def stream_query(messages: list[dict]) -> AsyncIterator[str]:
    """Stream a chat completion response token by token."""
    url = f"{LLM_BASE_URL}/v1/chat/completions"
    payload = {"model": LLM_MODEL, "messages": messages, "stream": True}
    async with httpx.AsyncClient(timeout=300) as client:
        async with client.stream("POST", url, json=payload, headers=_headers()) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data = line[6:].strip()
                if data == "[DONE]":
                    return
                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue


async def health_check() -> tuple[bool, str]:
    """Probe the LLM endpoint with a minimal request."""
    if not is_configured():
        return False, "LLM not configured — set LLM_BASE_URL and LLM_MODEL"
    try:
        url = f"{LLM_BASE_URL}/v1/chat/completions"
        payload = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload, headers=_headers())
            resp.raise_for_status()
        return True, f"{provider_label()} / {LLM_MODEL}"
    except Exception as exc:
        return False, str(exc)
