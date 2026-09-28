#!/usr/bin/env python3
"""Build a deck from its slides alone, then check it.

Usage:
    python3 build_deck.py slides.html "Science 1.7 - Pump build - deck.html" \
        --title "Science 1.7 · Pump build" --minutes 65 --languages es

`slides.html` holds only the <section class="slide"> elements, in order. Everything
else -- the stylesheet, navigation, timers, the talk kit, the chart kit, the photo
fallback -- comes from assets/deck_template.html, untouched. So a build never reads or
rewrites 60 KB of template to change a dozen slides, and never breaks the wiring by
editing around it.

The checker runs as the last step and its exit code is this script's, so one command
builds and checks.
"""

import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "deck_template.html")
STAGE_OPEN = '<div class="stage" id="stage">'
STAGE_CLOSE = '\n</div>\n\n<div class="footer">'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slides", help="file holding only the <section class=\"slide\"> elements")
    ap.add_argument("out", help="the deck to write")
    ap.add_argument("--title", required=True, help="browser tab title, e.g. 'Science 1.7 · Pump build'")
    ap.add_argument("--minutes", type=int, default=60)
    ap.add_argument("--languages", default="es")
    args = ap.parse_args()

    template = open(TEMPLATE, encoding="utf-8").read()
    slides = open(args.slides, encoding="utf-8").read().strip()
    if '<section class="slide' not in slides:
        sys.exit("No <section class=\"slide\"> elements in " + args.slides)
    if "<html" in slides.lower() or "<style" in slides.lower():
        sys.exit(args.slides + " should hold only the slides, not a whole page. "
                 "The template supplies everything else.")

    a = template.index(STAGE_OPEN) + len(STAGE_OPEN)
    b = template.index(STAGE_CLOSE, a)
    deck = template[:a] + "\n\n" + slides + "\n" + template[b:]
    deck = re.sub(r"<title>.*?</title>", "<title>" + args.title.replace("<", "&lt;") + "</title>",
                  deck, count=1, flags=re.S)
    # the builder's notes in the template's head comment are for the builder, not the deck
    deck = re.sub(r"<!--\s*DECK TEMPLATE.*?-->\n?", "", deck, count=1, flags=re.S)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(deck)
    n = deck.count('<section class="slide')
    print(f"wrote {args.out} ({len(deck.encode()) // 1000} KB, {n} slides)")

    check = os.path.join(HERE, "check_deck.py")
    r = subprocess.run([sys.executable, check, args.out, "--minutes", str(args.minutes),
                        "--languages", args.languages])
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
