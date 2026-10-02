#!/usr/bin/env python3
"""Build a deck from its slides alone, then check it.

Usage:
    python3 build_deck.py slides.html "Science 1.7 - Pump build - deck.html" \
        --title "Science 1.7 · Pump build" --minutes 65 --packet packet.json

--packet reads the key words and the languages from the packet's meta, and the checker
holds the deck to the packet: every question on a slide, in the packet's words. It takes
packet.json or the packet .docx itself (read through read_packet.py), so a deck built in a
later conversation is held to the page as printed. Without a packet, pass
--vocab "reservoir,pump,gallon" and --languages es.

--teams turns on team play, and only when Zac asks for teams: "--teams 3" for Team 1-3,
or names, "--teams Pumps,Roots,Lights". One scoreboard then sits in the footer of every
slide with the period's running total, and each game round gets a lock-in row per team.
Without it the games run as partner talk, with no points.

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
sys.path.insert(0, HERE)
from read_packet import load_packet  # noqa: E402  (packet.json, or the packet .docx itself)

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
    ap.add_argument("--packet", help="the lesson's packet.json or packet .docx: key words, "
                                     "languages, and the questions the deck has to carry")
    ap.add_argument("--teams", default="",
                    help="only when Zac asks for teams: a count (3) or names, comma-separated")
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
        try:
            meta = load_packet(args.packet, args.languages).get("meta", {})
        except (OSError, ValueError) as e:
            sys.exit(f"Could not read the packet {args.packet}: {e}")
        if not args.vocab and meta.get("vocab"):
            args.vocab = ",".join(meta["vocab"])
        if args.languages == "es" and meta.get("languages"):
            args.languages = ",".join(meta["languages"])
    words = [w.strip() for w in args.vocab.split(",") if w.strip()]
    teams = [t.strip() for t in args.teams.split(",") if t.strip()]
    if len(teams) == 1 and teams[0].isdigit():
        teams = [f"Team {i}" for i in range(1, int(teams[0]) + 1)]
    if len(teams) == 1 or len(teams) > 6:
        sys.exit(f"--teams needs two to six teams, not {len(teams)}.")
    body = {"data-vocab": words, "data-teams": teams}
    attrs = "".join(f' {k}="' + "|".join(v.replace("&", "&amp;").replace('"', "&quot;") for v in vals) + '"'
                    for k, vals in body.items() if vals)
    deck = deck.replace("<body>", f"<body{attrs}>", 1)
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
