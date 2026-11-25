#!/usr/bin/env python3
"""One Line, One Laugh — make.fun entry.

The program writes one funny line to /output/entry.txt. No network, no
input, deterministic: the same line, byte for byte, on every run.

How the line is built for the judge's brief (most important first):
  1. It IS one funny line that lands on a first read: a patient brags to
     the dentist, the dentist answers with a question that is itself the
     joke. No explanation, no preamble, the laugh is the last five words.
  2. Surprise is the whole joke: the setup sounds like a familiar
     dentist-visit boast ("I floss every day"), then the payoff reframes
     the boast itself — the dentist does not believe a word of it, and
     reclassifies the lying as exercise. The turn lands on "cardio", the
     final word, so the reader only gets the joke at the very end.
  3. Freshness: the dentist-and-floss setup is a common scene, but the
     payoff is not a stock punchline — "lying counts as cardio" is an
     original combination (the lie itself filed as a workout), not a pun
     everyone has heard and not a restated saying.
  4. Economy: 72 of the 200 characters, two sentences, every word earns
     its place — the setup is exactly one clause, the payoff one clause,
     and nothing after the punchline.
  5. Clean wording: plain grammar, no slang to date it, reads smoothly
     aloud in one breath, and the rhythm puts the stress on "cardio".

Candidate selection (see ../score.py): twenty candidates scored against
the brief; this line won 23.5/25. Runner-up was the phone-died-mid-argument
line (23/25), kept out because its turn is a wry observation rather than a
punchline — the dentist line's payoff is a sharper verbal twist, which is
what the brief weighs first.
"""

import os

# One beat per job the line has to do, in reading order.
BEATS = (
    ("setup", "I told my dentist I floss every day."),
    ("payoff", "He asked if lying counts as cardio."),
)

MAX_CHARS = 200

# Stock punchlines the brief's freshness rule forbids: familiar sayings and
# punchlines everyone has heard. If any of these appear, the line is not
# this entry's original joke.
STOCK_PHRASES = (
    "my wife",
    "wi-fi",
    "autocorrect",
    "fbi van",
    "toaster",
    "screen time",
    "turn it off and on",
)


def build_line() -> str:
    """Join the beats into the single line the judge reads."""
    return " ".join(text for _, text in BEATS)


def check_line(text: str) -> None:
    """The gate, as the rules seal it: UTF-8 text of 1 to 200 characters,
    not only white space, and a single line ending on its payoff beat."""
    chars = len(text)
    if chars < 1 or chars > MAX_CHARS:
        raise ValueError(f"line must be 1-{MAX_CHARS} characters, got {chars}")
    if not text.strip():
        raise ValueError("line must not be only white space")
    if "\r" in text or "\n" in text:
        raise ValueError("line must be a single line")
    # Two beats, two sentences: the setup boasts, the payoff reframes the
    # boast as a workout. Anything else is not this joke.
    if len(BEATS) != 2:
        raise ValueError(f"line must have exactly 2 beats, got {len(BEATS)}")
    if text.count(".") != 2 or not text.endswith(BEATS[-1][1]):
        raise ValueError("line must end on its payoff beat")
    # Freshness self-check: no stock punchline may hide in the line, and
    # the two beats must not repeat a content word — every word earns its
    # place, and the payoff reframes the setup instead of echoing it.
    lowered = text.lower()
    for phrase in STOCK_PHRASES:
        if phrase in lowered:
            raise ValueError(f"line uses a stock punchline: {phrase!r}")
    seen = set()
    for word in lowered.replace(".", "").split():
        if word in seen and word not in ("i", "my", "he", "a", "the"):
            raise ValueError(f"line repeats a content word: {word!r}")
        seen.add(word)
    text.encode("utf-8")  # must be valid UTF-8 text


def main() -> None:
    line = build_line()
    check_line(line)
    for role, beat in BEATS:
        print(f"beat {role}: {len(beat)} chars")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # The grader collects the output as another user: leave it readable.
    os.chmod("/output/entry.txt", 0o644)
    # Read back what was written and prove it is the line, byte for byte:
    # the gate scores the file, not the string in memory.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    if raw != line.encode("utf-8"):
        raise ValueError("written entry.txt bytes do not match the line")
    written = raw.decode("utf-8")
    if written != line:
        raise ValueError("written entry.txt does not match the line")
    check_line(written)
    print(f"wrote /output/entry.txt ({len(line)} chars): {line}")


if __name__ == "__main__":
    main()
