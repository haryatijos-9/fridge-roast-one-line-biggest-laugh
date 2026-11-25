#!/usr/bin/env python3
"""Fridge Roast: One Line, Biggest Laugh.

Scores six original smart-fridge roast lines against the judge's five
criteria (most important first) and writes the winning line to
/output/entry.txt. Python 3.13, standard library only.
"""

import os
import sys

# Judge criteria, most important first (weights 5..1).
CRITERIA = [
    ("on_subject", 5),   # a roast of a smart fridge, aimed at the fridge itself
    ("punchline", 4),    # builds to a turn or surprise that lands on first read
    ("specific", 3),     # specific to smart fridges, not any generic gadget gag
    ("tight", 2),        # every word earns its place inside 200 chars
    ("fresh", 1),        # dodges the obvious cracks (ordering groceries, watching you)
]

# Candidate lines: (text, scores per criterion, 0-10).
CANDIDATES = [
    (
        "My fridge's ice maker has one job and a union rep "
        "- it goes on strike every time I actually need ice.",
        {"on_subject": 9, "punchline": 9, "specific": 10, "tight": 9, "fresh": 9},
    ),
    (
        "My fridge texted me that the milk expired three days "
        "after I drank it. Thanks for the autopsy, detective.",
        {"on_subject": 8, "punchline": 8, "specific": 8, "tight": 8, "fresh": 8},
    ),
    (
        "My fridge locks the ice cream drawer and emails me a "
        "salad recipe. I bought an appliance, I got a nutritionist "
        "with a grudge.",
        {"on_subject": 8, "punchline": 8, "specific": 7, "tight": 7, "fresh": 8},
    ),
    (
        "My fridge shows ads on its touchscreen now. I paid two "
        "grand to stand in my kitchen watching commercials for butter.",
        {"on_subject": 8, "punchline": 7, "specific": 8, "tight": 8, "fresh": 9},
    ),
    (
        "I asked my fridge for a recipe. It said, 'Have you tried "
        "closing the door and thinking about your life choices?'",
        {"on_subject": 8, "punchline": 8, "specific": 6, "tight": 8, "fresh": 7},
    ),
    (
        "My smart fridge dispenses water slower than a DMV line "
        "- and still asks me to rate the experience afterwards.",
        {"on_subject": 7, "punchline": 7, "specific": 7, "tight": 8, "fresh": 7},
    ),
]


def score(candidate):
    text, marks = candidate
    total = sum(marks[name] * weight for name, weight in CRITERIA)
    return total


def ranked_candidates():
    # Highest score first; ties go to the shorter line (tighter wording),
    # then to the earlier candidate, so the result is fully deterministic.
    return sorted(
        CANDIDATES,
        key=lambda c: (-score(c), len(c[0]), CANDIDATES.index(c)),
    )


def main():
    ranked = ranked_candidates()
    for text, marks in ranked:
        print(f"{score((text, marks)):3d}  {text}", file=sys.stderr)
    winner, _ = ranked[0]
    assert 1 <= len(winner) <= 200, "winning line must be 1-200 characters"
    assert winner.strip(), "winning line must not be only whitespace"
    path = "/output/entry.txt"
    try:
        os.makedirs("/output", exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(winner)
    except OSError:
        # Local run without a writable /output: write beside the script.
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(winner)
    print(winner)


if __name__ == "__main__":
    main()
