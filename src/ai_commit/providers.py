"""LLM provider abstraction (OpenAI / Anthropic / Ollama)."""

import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass


@dataclass
class ProviderConfig:
    name: str
    model: str
    api_key: str | None = None
    base_url: str = ""


def call(system: str, user: str, cfg: ProviderConfig, timeout: int = 30) -> str:
    if cfg.name == "openai":
        return _call_openai(system, user, cfg, timeout)
    if cfg.name == "anthropic":
        return _call_anthropic(system, user, cfg, timeout)
    if cfg.name == "ollama":
        return _call_ollama(system, user, cfg, timeout)
    raise ValueError(f"Unknown provider: {cfg.name}")


def detect_provider(model: str) -> str:
    if model.startswith(("gpt-", "o1", "o3")):
        return "openai"
    if model.startswith("claude"):
        return "anthropic"
    return "ollama"


def _post_json(url: str, headers: dict, payload: dict, timeout: int) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} from {url}: {body}") from e


def _call_openai(system: str, user: str, cfg: ProviderConfig, timeout: int) -> str:
    if not cfg.api_key:
        cfg.api_key = os.environ.get("OPENAI_API_KEY", "")
    if not cfg.api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    base = cfg.base_url or "https://api.openai.com/v1"
    body = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
        "max_tokens": 400,
    }
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }
    resp = _post_json(f"{base}/chat/completions", headers, body, timeout)
    return resp["choices"][0]["message"]["content"].strip()


def _call_anthropic(system: str, user: str, cfg: ProviderConfig, timeout: int) -> str:
    if not cfg.api_key:
        cfg.api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not cfg.api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    base = cfg.base_url or "https://api.anthropic.com/v1"
    body = {
        "model": cfg.model,
        "max_tokens": 400,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    headers = {
        "x-api-key": cfg.api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    resp = _post_json(f"{base}/messages", headers, body, timeout)
    return resp["content"][0]["text"].strip()


def _call_ollama(system: str, user: str, cfg: ProviderConfig, timeout: int) -> str:
    base = cfg.base_url or "http://localhost:11434"
    body = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 400},
    }
    resp = _post_json(f"{base}/api/chat", {"Content-Type": "application/json"}, body, timeout)
    return resp["message"]["content"].strip()
