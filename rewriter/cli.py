from __future__ import annotations

import argparse
import sys

from rewriter.dials import DIAL_MAX, DIAL_MIN, Dials
from rewriter.llm import ConfigError, LLMError, complete
from rewriter.prompt import SYSTEM_PROMPT, build_user_prompt


def _dial(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"must be an integer from {DIAL_MIN} to {DIAL_MAX}") from exc
    if not DIAL_MIN <= number <= DIAL_MAX:
        raise argparse.ArgumentTypeError(f"must be an integer from {DIAL_MIN} to {DIAL_MAX}")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rewriter",
        description=(
            "Rewrite a paragraph for a circumstance, using trust, flirt, and emotion dials (0-3)."
        ),
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="The paragraph to rewrite. If omitted, text is read from stdin.",
    )
    parser.add_argument(
        "-c",
        "--circumstance",
        required=True,
        help='Situation, e.g. "apologizing to my partner".',
    )
    parser.add_argument(
        "-t",
        "--trust",
        type=_dial,
        required=True,
        help=f"Trust dial ({DIAL_MIN}-{DIAL_MAX}).",
    )
    parser.add_argument(
        "-f",
        "--flirt",
        type=_dial,
        required=True,
        help=f"Flirt dial ({DIAL_MIN}-{DIAL_MAX}).",
    )
    parser.add_argument(
        "-e",
        "--emotion",
        type=_dial,
        required=True,
        help=f"Emotion dial ({DIAL_MIN}-{DIAL_MAX}).",
    )
    return parser


def read_text(argument: str | None) -> str:
    if argument is not None:
        text = argument.strip()
    elif sys.stdin.isatty():
        print("Paste the original paragraph. End with a blank line, then Ctrl+Z Enter (Windows) or Ctrl+D (Unix):", file=sys.stderr)
        lines: list[str] = []
        try:
            while True:
                line = input()
                if line == "" and lines:
                    break
                lines.append(line)
        except EOFError:
            pass
        text = "\n".join(lines).strip()
    else:
        text = sys.stdin.read().strip()

    if not text:
        raise SystemExit("No text to rewrite.")
    return text


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    text = read_text(args.text)
    dials = Dials(trust=args.trust, flirt=args.flirt, emotion=args.emotion)
    user_prompt = build_user_prompt(text, args.circumstance, dials)

    try:
        rewritten = complete(SYSTEM_PROMPT, user_prompt)
    except (ConfigError, LLMError) as exc:
        print(exc, file=sys.stderr)
        return 1

    print(rewritten)
    return 0
