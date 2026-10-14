# Rewriter

A Python CLI tool that rewrites a paragraph for a specific circumstance, using three "dials" — **trust**, **flirt**, and **emotion** (each 0–3) — to control the tone. Powered by Groq (or any OpenAI-compatible LLM API).

## Install

```bash
pip install -e .
```

This installs the `rewriter` command and pulls in `python-dotenv`.

## Setup

Put your Groq API key in `rewriter/.env`:

```
GROQ_API_KEY=gsk_your-key-here
OPENAI_MODEL=llama-3.3-70b-versatile
```

Or set it as an environment variable:

```powershell
$env:GROQ_API_KEY = "gsk_..."
```

See `.env.example` for all supported variables.

## Usage

```bash
rewriter "I wanted to let you know that the deadline needs to move to next Friday." \
  -c "telling my boss about a delay" \
  -t 1 -f 0 -e 1
```

Or use `python -m rewriter` instead of `rewriter`.

You can also pipe text via stdin:

```bash
echo "Some paragraph" | python -m rewriter -c "apologizing to a friend" -t 2 -f 0 -e 2
```

### Arguments

| Argument | Flag | Description |
|---|---|---|
| `text` | (positional) | Paragraph to rewrite. Read from stdin if omitted. |
| `--circumstance` | `-c` | Situation context (required) |
| `--trust` | `-t` | Trust dial, 0–3 (required) |
| `--flirt` | `-f` | Flirt dial, 0–3 (required) |
| `--emotion` | `-e` | Emotion dial, 0–3 (required) |

### What the dials mean

| Dial | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Trust** | Distant, guarded | Polite, civil | Warm, natural | Direct, unguarded |
| **Flirt** | Zero romantic charge | Light warmth | Clearly flirty | Strong, charged |
| **Emotion** | Matter-of-fact | Restrained feeling | Visibly emotional | Honest intensity |

## Project Files

```
rewriter/
├── pyproject.toml        # Package metadata, dependencies, CLI entry point
├── .env.example          # Template showing all env vars the tool accepts
├── .gitignore            # Keeps .env, __pycache__, build artifacts out of git
├── README.md             # This file
└── rewriter/
    ├── __init__.py       # Package marker + version string
    ├── __main__.py       # Enables `python -m rewriter`
    ├── cli.py            # Argument parsing & main() entry point
    ├── dials.py          # Dials dataclass + human-readable level descriptions
    ├── llm.py            # Loads API config from env, sends chat completion request
    ├── prompt.py         # System prompt (hard rules) + user prompt builder
    └── .env              # Your API key (git-ignored, never committed)
```

### File-by-file

- **`__init__.py`** — Marks the directory as a Python package. Contains the version string.
- **`__main__.py`** — Allows running via `python -m rewriter`. Just calls `main()` from `cli.py`.
- **`cli.py`** — Parses command-line arguments (text, circumstance, three dials). Reads text from stdin if not given as an argument. Calls the LLM and prints the result.
- **`dials.py`** — Defines the `Dials` dataclass with validation (0–3 range). Contains human-readable descriptions for each level of trust, flirt, and emotion that get injected into the prompt.
- **`llm.py`** — Loads `.env` via `python-dotenv`, reads the API key/model/base-URL from environment variables (checks `GROQ_API_KEY` first, falls back to `OPENAI_API_KEY`), and sends a chat completion request using only the standard library (`urllib`). Defaults to Groq's API. No SDK dependency.
- **`prompt.py`** — Contains the system prompt (hard rules: keep meaning, no invented facts, write like a real person) and builds the user prompt by combining the circumstance, dials, and original text.
