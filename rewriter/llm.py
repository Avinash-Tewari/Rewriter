from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.error
import urllib.request

from dotenv import load_dotenv

# Load .env from the package directory (where the user stores their key),
# then fall back to whichever directory the tool is run from.
_pkg_env = Path(__file__).resolve().parent / ".env"
load_dotenv(_pkg_env)
load_dotenv()  # also check CWD/.env

DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_BASE_URL = "https://api.groq.com/openai/v1"


class ConfigError(RuntimeError):
    """Missing or invalid environment configuration."""


class LLMError(RuntimeError):
    """The API call failed or returned an unusable response."""


def _env(*names: str, default: str | None = None) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def load_api_key() -> str:
    key = _env("REWRITER_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY")
    if not key:
        raise ConfigError(
            "No API key found. Set REWRITER_API_KEY or GROQ_API_KEY in the environment."
        )
    return key


def load_model() -> str:
    return _env("REWRITER_MODEL", "GROQ_MODEL", "OPENAI_MODEL", default=DEFAULT_MODEL) or DEFAULT_MODEL


def load_base_url() -> str:
    url = _env("REWRITER_BASE_URL", "GROQ_BASE_URL", "OPENAI_BASE_URL", default=DEFAULT_BASE_URL)
    return (url or DEFAULT_BASE_URL).rstrip("/")


def complete(system: str, user: str) -> str:
    key = load_api_key()
    model = load_model()
    url = f"{load_base_url()}/chat/completions"

    payload = {
        "model": model,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise LLMError(f"API request failed ({exc.code}): {detail}") from exc
    except urllib.error.URLError as exc:
        raise LLMError(f"Could not reach the API: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise LLMError("API returned invalid JSON.") from exc

    try:
        text = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError("API response was missing the rewritten text.") from exc

    rewritten = (text or "").strip()
    if not rewritten:
        raise LLMError("API returned an empty rewrite.")
    return rewritten
