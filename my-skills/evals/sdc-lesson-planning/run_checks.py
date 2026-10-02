#!/usr/bin/env python3
"""Run the skill's own checkers over one lesson and write what they report.

Usage:
    python3 run_checks.py path/to/lesson-folder [--out checks.txt]

The folder holds what one lesson produced: the packet (`* - packet.docx`), the deck
(`* - deck.html`), and, when there is one, the `packet.json` it was rendered from. Without
it, the deck is checked against the packet .docx itself, as a deck built in a later
conversation would be. The report is the evidence for the rubric's script-judged criteria
(SDC-P1, SDC-R1, SDC-R2, SDC-L1, SDC-D1, SDC-G1, O14) and is handed to the LLM judge beside
the lesson itself.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "..", "sdc-lesson-planning", "scripts")
# the deck's checker lives with the slideshow skill once the deck is its own skill
DECK_SCRIPTS = next((d for d in (os.path.join(HERE, "..", "..", "sdc-slideshow", "scripts"), SCRIPTS)
                     if os.path.exists(os.path.join(d, "check_deck.py"))), SCRIPTS)


def run(cmd):
    r = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, timeout=600)
    return (r.stdout + r.stderr).strip("\n"), r.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--out", default=None, help="default: checks.txt in the folder")
    args = ap.parse_args()
    folder = os.path.abspath(args.folder)
    out = []

    data = {}
    js = glob.glob(os.path.join(folder, "*packet*.json")) + glob.glob(os.path.join(folder, "packet.json"))
    if js:
        data = json.load(open(js[0]))
        with tempfile.TemporaryDirectory() as tmp:
            text, _ = run([os.path.join(SCRIPTS, "render_packet.py"), js[0],
                           os.path.join(tmp, "packet.docx")])
        out.append("== Packet text (render report: key words, reading level, language lines)\n" + text)
    meta = data.get("meta", {})
    days = sum(1 for b in data.get("sections", []) if b.get("type") == "day") or 1

    for docx in sorted(glob.glob(os.path.join(folder, "*packet*.docx"))):
        cmd = [os.path.join(SCRIPTS, "check_packet.py"), docx]
        if days > 1:
            cmd += ["--days", str(days)]
        if "(reduced)" in docx:
            cmd += ["--max-pages", "4"]
        text, code = run(cmd)
        out.append(f"== Packet pages: {os.path.basename(docx)} (exit {code})\n" + text)

    minutes = re.search(r"\d+", str(meta.get("period", "")))
    for deck in sorted(glob.glob(os.path.join(folder, "*deck*.html"))):
        cmd = [os.path.join(DECK_SCRIPTS, "check_deck.py"), deck,
               "--minutes", minutes.group(0) if minutes else "60",
               "--languages", ",".join(meta.get("languages") or ["es"])]
        if meta.get("vocab"):
            cmd += ["--vocab", ",".join(meta["vocab"])]
        # the deck is held to the packet: its source when there is one, else the packet itself
        printed = [d for d in sorted(glob.glob(os.path.join(folder, "*packet*.docx")))
                   if "(reduced)" not in d]
        if js:
            cmd += ["--packet", js[0]]
        elif printed:
            cmd += ["--packet", printed[0]]
        text, code = run(cmd)
        out.append(f"== Deck: {os.path.basename(deck)} (exit {code})\n" + text)

    if not out:
        print(f"Nothing to check in {folder}: no packet.json, packet .docx, or deck .html.")
        return 1
    report = "\n\n".join(out) + "\n"
    path = args.out or os.path.join(folder, "checks.txt")
    with open(path, "w") as fh:
        fh.write(report)
    print(report)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
