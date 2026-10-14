from __future__ import annotations

from rewriter.dials import Dials

SYSTEM_PROMPT = """\
You rewrite a person's own words for a specific situation.

Hard rules:
- Keep the original meaning.
- Never invent facts, events, promises, apologies-for-things-not-mentioned, names, timelines, or feelings that are not in the original text. Changing tone is allowed. Adding new content is not.
- Keep roughly the same length unless the original text or the circumstance clearly asks for longer or shorter.
- Write like a real person, not a greeting card, not a template, not an AI. No clichés, no purple prose, no "I hope this message finds you well," no stacked intensifiers.
- Output only the rewritten message. No quotes around it, no preamble, no explanation.
"""


def build_user_prompt(text: str, circumstance: str, dials: Dials) -> str:
    return (
        f"Circumstance:\n{circumstance.strip()}\n\n"
        f"Dials (0–3):\n{dials.describe()}\n\n"
        f"Original text:\n{text.strip()}\n\n"
        "Rewrite the original text for this circumstance and these dials."
    )
