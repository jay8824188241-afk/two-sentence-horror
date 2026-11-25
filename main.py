#!/usr/bin/env python3
"""Two-Sentence Horror — make.fun bounty entry.

Writes one original two-sentence horror story to /output/entry.txt.
Deterministic, standard library only, no network, no randomness.
"""

import hashlib
import os
import re

STORY = (
    "I set up a camera to find out why my dog barked at the empty hallway "
    "every night at 2 AM. "
    "The footage showed him barking at me \u2014 standing in the hallway, "
    "smiling, while I was asleep in bed."
)

OUTPUT_PATH = "/output/entry.txt"


def count_sentences(text):
    """Count sentences by terminal punctuation followed by whitespace/end."""
    stripped = text.strip()
    if not stripped:
        return 0
    parts = re.split(r"(?<=[.!?])\s+", stripped)
    return len([p for p in parts if p.strip()])


def self_check(story):
    """Gate checks mirroring the bounty rule: 1-400 chars, exactly 2 sentences."""
    assert story == story.strip(), "story must not start/end with whitespace"
    assert 1 <= len(story) <= 400, f"story must be 1-400 chars, got {len(story)}"
    assert count_sentences(story) == 2, (
        f"story must be exactly two sentences, got {count_sentences(story)}"
    )
    # No hidden extra sentence-enders (e.g. abbreviations like "a.m.").
    enders = re.findall(r"[.!?]", story)
    assert len(enders) == 2, f"expected exactly 2 sentence-enders, got {len(enders)}"
    return True


def main():
    story = STORY.strip()
    assert story, "story must not be blank"
    self_check(story)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(story)

    # Read back and verify the file holds exactly what was intended.
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        written = f.read()
    assert written == story, "entry.txt content differs from the story"
    self_check(written)

    digest = hashlib.sha256(story.encode("utf-8")).hexdigest()
    print(f"Wrote {len(story)} characters to {OUTPUT_PATH}")
    print(f"Sentences: {count_sentences(story)}")
    print(f"SHA-256: {digest}")
    print(story)


if __name__ == "__main__":
    main()
