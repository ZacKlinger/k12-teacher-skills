#!/usr/bin/env python3
"""The checker holds the line on every format: the two gallery decks build clean, and the
deck of deliberately broken configs raises every error it should.

    python3 checker_test.py <out-dir>      (the decks are built into out-dir)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def skill_dir():
    """The skill: classroom-plugin/skills/, plugin/skills/ or my-skills/ (as run_checks.py
    finds it), or wherever K12_SKILL points."""
    if os.environ.get("K12_SKILL"):
        return os.environ["K12_SKILL"]
    for base in ("classroom-plugin/skills", "plugin/skills", "my-skills"):
        d = os.path.join(ROOT, base, "k12presentation")
        if os.path.isdir(os.path.join(d, "scripts")):
            return d
    sys.exit("Can't find k12presentation under classroom-plugin/skills/, plugin/skills/ or my-skills/; set K12_SKILL.")


SKILL = skill_dir()
BUILD = os.path.join(SKILL, "scripts", "build_deck.py")
FIX = os.path.join(HERE, "fixtures")

CLEAN = [("existing_formats", "60"), ("interactive_formats", "60")]
EXPECTED = [
    "data-answer='4' isn't one of the 3 options",
    "a hinge question needs one data-traps entry per option",
    "order it takes three to eight steps",
    "card 'a=2' should read 'label=value'",
    "data-answer must be a number between 0 and 100",
    "which one doesn't belong takes exactly four tiles",
    "tile B has no real data-why",
    "mark exactly one step data-wrong",
    "claim 1's data-answer isn't one of",
    "every pair in a match holds exactly two elements",
    "doesn't work",
    "goes below zero",
    "data-band should read",
    "a zoom-in with no --focus",
    "data-zooms should step down to 1",
    "data-teams on a sort",
    "2 games on one slide",
    "takes six options at most",
    "Slide 14 (blank zooms): data-zooms should step down to 1",
    "tick '½=0.5'",
    "tick '2'",
    "Slide 16 (runaway formula): data-formula",
    "Slide 17 (divide by zero): data-formula '10 / (a - 5)' doesn't work",
    "Slide 20 (unquoted class): data-answer='9'",
    "Slide 21 (comment in formula): data-formula",
]
# configs that are fine and must not be flagged
NOT_EXPECTED = [
    "Slide 18 (maths in text)",
    "Slide 19 (fine in quotes)",
    "Slide 22 (wrapped formula)",
]


def build(name, minutes, out):
    deck = os.path.join(out, name + ".html")
    r = subprocess.run([sys.executable, BUILD, os.path.join(FIX, name + ".slides.html"), deck,
                        "--title", "Science 1.7 · " + name, "--minutes", minutes,
                        "--vocab", "reservoir,pump", "--languages", "es"], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    failed = 0
    for name, minutes in CLEAN:
        code, log = build(name, minutes, out)
        if code != 0:
            failed += 1
            print(f"FAIL {name} should build clean:\n" + "\n".join(l for l in log.splitlines() if "ERROR" in l))
        else:
            print(f"ok   {name} builds clean")
    code, log = build("broken_configs", "45", out)
    for want in EXPECTED:
        if want in log:
            print(f"ok   broken deck: {want}")
        else:
            failed += 1
            print(f"FAIL broken deck never said: {want}")
    for bad in NOT_EXPECTED:
        if bad in log:
            failed += 1
            print(f"FAIL broken deck flagged a config that is fine: {bad}")
        else:
            print(f"ok   broken deck leaves alone: {bad}")
    if "Traceback" in log:
        failed += 1
        print("FAIL the checker crashed:\n" + log)
    print(f"\n{'checker test passed' if not failed else str(failed) + ' failure(s)'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
