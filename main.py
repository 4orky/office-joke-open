#!/usr/bin/env python3
"""Office Joke Open -- make.fun bounty
u-aldy998-make-the-ai-judge-laugh-the-office-joke-open-9920f232

The program writes a single one-line joke about office life
(1-200 characters) to /output/entry.txt.

Candidates were drafted against the judge's brief, in order of weight:
  1. about office life and works as a joke, not a complaint or remark
  2. the laugh is earned: a turn or misdirection that pays off in the
     last few words
  3. a specific office detail, not a generic grumble about work
  4. fresh: a familiar setup taken somewhere unexpected
  5. reads cleanly in one pass, tight enough that no word could be cut
Each candidate carries a hand-scored craft score (0-10 per criterion,
summed below); selection is deterministic: highest score wins, ties go
to the shorter text. The output is byte-identical on every run.
"""

import os

CANDIDATES = [
    # score: joke 10, laugh 9, specific 10, fresh 9, clean 10 = 48
    {
        "text": "I asked for a raise and my manager gave me a standing desk instead, so now I can worry about money on my feet.",
        "score": 48,
    },
    # score: joke 10, laugh 9, specific 10, fresh 8, clean 10 = 47
    {
        "text": "The fire drill went off during our all-hands, and for the first time ever the whole company agreed on something: leaving.",
        "score": 47,
    },
    # score: joke 10, laugh 9, specific 9, fresh 9, clean 9 = 46
    {
        "text": "Our team-building exercise was trust falls; I fell, nobody caught me, and HR called it a valuable lesson in self-reliance.",
        "score": 46,
    },
    # score: joke 10, laugh 8, specific 9, fresh 7, clean 9 = 43
    {
        "text": "I set my Slack status to 'in a meeting' and went for a walk; my boss replied, 'Great, can you take this call while you walk?'",
        "score": 43,
    },
    # score: joke 9, laugh 8, specific 9, fresh 8, clean 8 = 42
    {
        "text": "HR said our open-plan office encourages collaboration, which is why I now know Dave's divorce timeline better than my own deadlines.",
        "score": 42,
    },
]


def pick(cands):
    best = cands[0]
    for c in cands[1:]:
        if c["score"] > best["score"] or (
            c["score"] == best["score"] and len(c["text"]) < len(best["text"])
        ):
            best = c
    return best["text"]


JOKE = pick(CANDIDATES)

# The gate requires 1-200 characters of non-whitespace UTF-8 text in a
# single line. Validate before writing, then read the file back and
# confirm it holds exactly the chosen joke, byte for byte.
if len(JOKE) < 1 or len(JOKE) > 200:
    raise SystemExit(f"joke is {len(JOKE)} characters, gate requires 1-200")
if JOKE.strip() == "" or "\n" in JOKE:
    raise SystemExit("joke must be a single non-empty line")

os.makedirs("/output", exist_ok=True)
with open("/output/entry.txt", "w", encoding="utf-8") as f:
    f.write(JOKE)
with open("/output/entry.txt", "r", encoding="utf-8") as f:
    written = f.read()
if written != JOKE:
    raise SystemExit("entry.txt does not match the chosen joke")
print(f"wrote {len(written)} characters to /output/entry.txt")
