#!/usr/bin/env python3
"""Build a deck from its slides alone, then check it.

Usage:
    python3 build_deck.py slides.html "Science 1.7 - Pump build - deck.html" \
        --title "Science 1.7 · Pump build" --minutes 65 --packet packet.json

--packet reads the key words and the languages from the packet's meta, and the checker
holds the deck to the packet: every question on a slide, in the packet's words. Without a
packet, pass --vocab "reservoir,pump,gallon" and --languages es.

`slides.html` holds only the <section class="slide"> elements, in order. Everything
else -- the stylesheet, navigation, timers, the talk kit, the chart kit, the photo
fallback -- comes from assets/deck_template.html, untouched. So a build never reads or
rewrites 60 KB of template to change a dozen slides, and never breaks the wiring by
editing around it.

The checker runs as the last step and its exit code is this script's, so one command
builds and checks.
"""

import argparse
import json
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
    ap.add_argument("--vocab", default="",
                    help="the packet's key words (meta.vocab), comma-separated; marked on every slide")
    ap.add_argument("--packet", help="the lesson's packet.json: key words, languages, and the "
                                     "questions the deck has to carry")
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
    meta = {}
    if args.packet:
        meta = json.load(open(args.packet, encoding="utf-8")).get("meta", {})
        if not args.vocab and meta.get("vocab"):
            args.vocab = ",".join(meta["vocab"])
        if args.languages == "es" and meta.get("languages"):
            args.languages = ",".join(meta["languages"])
    words = [w.strip() for w in args.vocab.split(",") if w.strip()]
    if words:
        attr = "|".join(w.replace("&", "&amp;").replace('"', "&quot;") for w in words)
        deck = deck.replace("<body>", f'<body data-vocab="{attr}">', 1)
    # the builder's notes in the template's head comment are for the builder, not the deck
    deck = re.sub(r"<!--\s*DECK TEMPLATE.*?-->\n?", "", deck, count=1, flags=re.S)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(deck)
    n = deck.count('<section class="slide')
    print(f"wrote {args.out} ({len(deck.encode()) // 1000} KB, {n} slides)")

    check = os.path.join(HERE, "check_deck.py")
    r = subprocess.run([sys.executable, check, args.out, "--minutes", str(args.minutes),
                        "--languages", args.languages] + (["--vocab", args.vocab] if words else [])
                       + (["--packet", args.packet] if args.packet else []))
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
