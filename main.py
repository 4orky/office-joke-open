"""Single-line office joke for the make.fun Office Joke Open.

Bounty: u-aldy998-make-the-ai-judge-laugh-the-office-joke-open-9920f232.
The brief wants one joke about office life, at most two hundred
characters, funny enough to make a judge laugh out loud.

This script drafts a dozen original one-liners, grades every draft on
five craft axes, and writes the best-graded line to the entry file.
The five axes, each graded from zero to ten:

  setup -- the opening scene clicks at once for anyone who has ever
      worked in an office;
  twist -- the ending swerves somewhere the reader did not see coming;
  detail -- a concrete office object or ritual carries the joke, not a
      vague complaint about work in general;
  novelty -- the punchline is not the first obvious one for its setup;
  economy -- no word can be cut without losing something.

The twist counts double, because the laugh lives or dies on the turn.
The winner is the highest weighted total; ties go to the shorter line,
then to the draft listed first. The run is deterministic: the entry
file comes out byte-identical every single time."""

import hashlib
from pathlib import Path

ENTRY_PATH = Path("/output/entry.txt")
LIMIT = 200


class Draft:
    """A candidate joke with one grade per craft axis."""

    def __init__(self, line, setup, twist, detail, novelty, economy):
        self.line = line
        self.setup = setup
        self.twist = twist
        self.detail = detail
        self.novelty = novelty
        self.economy = economy

    def weighted(self):
        return self.setup + self.twist * 2 + self.detail + self.novelty + self.economy


DRAFTS = [
    Draft("I asked for a raise and my manager gave me a standing desk instead, so now I can worry about money on my feet.", 9, 10, 10, 9, 10),
    Draft("We held a meeting to plan fewer meetings; it ran an hour over and ended with a follow-up meeting.", 8, 7, 9, 7, 8),
    Draft("IT gave me a passphrase instead of a password, so now I forget a whole sentence instead of a single word.", 8, 8, 8, 8, 8),
    Draft("The CEO called us a family, then invoiced us for the birthday cake.", 8, 9, 8, 8, 9),
    Draft("My out-of-office reply says I am unreachable, which is the most honest thing I have written all year.", 8, 7, 8, 7, 9),
    Draft("Our printer has been warming up since March; HR now lists patience as a core competency.", 8, 8, 9, 7, 8),
    Draft("I asked IT for a second monitor and got a second manager instead; both of them watch me work now.", 8, 8, 8, 8, 7),
    Draft("The lift has been broken for a month, so our startup's elevator pitch is just us taking the stairs.", 7, 7, 8, 7, 7),
    Draft("Facilities replaced the broken coffee machine with a suggestion box, so now we queue to complain about having nothing to queue for.", 8, 8, 9, 8, 7),
    Draft("My performance review says I am a self-starter, which is HR for 'nobody showed you how anything works'.", 8, 8, 8, 8, 8),
    Draft("The team offsite was a trust exercise in the car park; I now trust exactly one colleague, and it is the one who stayed in the car.", 8, 7, 8, 7, 7),
    Draft("I wear headphones to signal do-not-disturb, and my manager reads them as an invitation to tap my shoulder.", 9, 8, 9, 7, 8)]


def choose_best(drafts):
    """Return the draft with the best weighted total, ties broken short."""
    best = None
    best_key = None
    for position, draft in enumerate(drafts):
        key = (draft.weighted(), -len(draft.line), -position)
        if best_key is None or key > best_key:
            best_key = key
            best = draft
    return best


def confirm_entry(text):
    """Reject anything that breaks the bounty gate, with reasons listed."""
    problems = []
    if text.strip() == "":
        problems.append("entry is blank")
    if text != text.strip():
        problems.append("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        problems.append("entry runs over more than one line")
    if len(text) > LIMIT:
        problems.append("entry is %d characters, over the %d limit" % (len(text), LIMIT))
    if problems:
        raise SystemExit("entry rejected: " + "; ".join(problems))


for draft in DRAFTS:
    if len(draft.line) > LIMIT:
        raise SystemExit("draft over the limit: " + draft.line)

chosen = choose_best(DRAFTS)
confirm_entry(chosen.line)
ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
ENTRY_PATH.write_text(chosen.line, encoding="utf-8")
roundtrip = ENTRY_PATH.read_text(encoding="utf-8")
if roundtrip != chosen.line:
    raise SystemExit("entry file came back different from the chosen joke")
digest = hashlib.sha256(roundtrip.encode("utf-8")).hexdigest()
print("entry ready: %d characters, sha256 %s" % (len(roundtrip), digest))
