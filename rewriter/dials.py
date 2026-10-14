from __future__ import annotations

from dataclasses import dataclass

DIAL_MIN = 0
DIAL_MAX = 3

TRUST_LEVELS = {
    0: (
        "Low trust. Keep distance. Do not assume closeness, shared history, "
        "or that the other person will give you the benefit of the doubt."
    ),
    1: (
        "Polite, civil trust. Respectful and clear. Not cold, not intimate."
    ),
    2: (
        "Established trust. Warm and natural. Contractions are fine. "
        "Speak as if goodwill already exists."
    ),
    3: (
        "High trust. Direct and unguarded, like talking to someone who "
        "already knows you. Still do not invent private details."
    ),
}

FLIRT_LEVELS = {
    0: (
        "No flirt. Zero romantic or teasing charge. Do not add compliments "
        "or innuendo that were not already in the original."
    ),
    1: (
        "Light warmth only. A little playfulness is allowed if the original "
        "already leans that way. Never overt."
    ),
    2: (
        "Clearly flirty. Show interest through wording and rhythm, not "
        "pickup lines. Stay grounded in the original meaning."
    ),
    3: (
        "Strong flirt. Charged and personal, still a real person—not cheesy, "
        "not a greeting card. Do not invent attraction or history."
    ),
}

EMOTION_LEVELS = {
    0: (
        "Matter-of-fact. Feelings only if they are already in the original, "
        "and then stated plainly."
    ),
    1: (
        "A little feeling in the word choice. Restrained."
    ),
    2: (
        "Emotion is visible. The reader should feel it without drama for "
        "drama's sake."
    ),
    3: (
        "High emotion. Honest intensity, not theatrical, not poetic padding."
    ),
}


@dataclass(frozen=True)
class Dials:
    trust: int
    flirt: int
    emotion: int

    def __post_init__(self) -> None:
        for name, value in (
            ("trust", self.trust),
            ("flirt", self.flirt),
            ("emotion", self.emotion),
        ):
            if not DIAL_MIN <= value <= DIAL_MAX:
                raise ValueError(
                    f"{name} must be an integer from {DIAL_MIN} to {DIAL_MAX}, got {value}"
                )

    def describe(self) -> str:
        return (
            f"trust={self.trust}: {TRUST_LEVELS[self.trust]}\n"
            f"flirt={self.flirt}: {FLIRT_LEVELS[self.flirt]}\n"
            f"emotion={self.emotion}: {EMOTION_LEVELS[self.emotion]}"
        )
