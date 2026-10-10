#!/usr/bin/env python3
"""Summarize how a skill gets used, from a claude.ai data export.

claude.ai: Settings > Privacy > Export data. Unzip it, then:

    python3 my-skills/tools/usage_report.py path/to/conversations.json > usage.md

By default it keeps conversations that mention the lesson-planning skill or a lesson code
("Science 1.6", "Math 1.5"); pass --match to use your own pattern (a regular expression
tested against the conversation title and every message). For each conversation it counts
your turns, the turns after the first request (revisions), what the revisions were about,
and what files came back; then it rolls those up across all of them.

The export format isn't documented and has changed before, so the reader is deliberately
forgiving: it looks for message text in `text` and in `content[].text`, and for the sender
in `sender` or `role`. If a field it needs is missing, it says so instead of guessing.
"""

import argparse
import json
import re
import statistics
import sys
from collections import Counter

DEFAULT_MATCH = r"k12lessonplan|sdc-lesson-planning|\b(science|math)\s+\d+\.\d+\b|student packet|slide deck"

# What a follow-up turn is asking to change. A turn can land in more than one bucket.
THEMES = {
    "length and timing": r"\b(minutes?|block|period|time|too long|cut)\b",
    "language lines": r"\b(spanish|espa|translat|bilingual|language)\w*",
    "photos": r"\b(photo|image|picture|pic)s?\b",
    "video": r"\b(video|youtube|clip|timestamp)s?\b",
    "slides and deck": r"\b(slide|deck|timer|chart|html)s?\b",
    "packet layout": r"\b(packet|page|worksheet|docx|word doc|font|print)s?\b",
    "question count and difficulty": r"\b(question|harder|easier|simpler|rigor|reading level)s?\b",
    "standards": r"\b(standard|ngss|ccss|hs-\w+)s?\b",
    "games and activities": r"\b(game|jeopardy|vote|corners|station|talk|partner)s?\b",
    "accommodations": r"\b(iep|504|accommodat|support|scaffold)\w*",
    "context from earlier lessons": r"\b(yesterday|last (class|lesson|time)|previous|day \d|\d\.\d)\b",
}


def text_of(msg):
    parts = [msg.get("text") or ""]
    for c in msg.get("content") or []:
        if isinstance(c, dict) and c.get("type") == "text" and c.get("text"):
            parts.append(c["text"])
    return "\n".join(p for p in parts if p)


def sender_of(msg):
    s = (msg.get("sender") or msg.get("role") or "").lower()
    return "human" if s in ("human", "user") else "assistant" if s else "?"


def files_back(msg):
    names = set()
    for key in ("files", "attachments"):
        for f in msg.get(key) or []:
            if isinstance(f, dict) and f.get("file_name"):
                names.add(f["file_name"])
    # file names can hold spaces, so count the extensions rather than parse the names
    for i, ext in enumerate(re.findall(r"\.(docx|html|pdf|pptx)\b", text_of(msg))):
        names.add(f"{ext}#{i}")
    return names


def summarize(conv, pattern):
    msgs = conv.get("chat_messages") or conv.get("messages") or []
    title = conv.get("name") or conv.get("title") or "(untitled)"
    blob = title + "\n" + "\n".join(text_of(m) for m in msgs)
    if not pattern.search(blob):
        return None
    human = [m for m in msgs if sender_of(m) == "human"]
    later = human[1:]
    themes = Counter()
    for m in later:
        t = text_of(m).lower()
        for name, rx in THEMES.items():
            if re.search(rx, t):
                themes[name] += 1
    delivered = set()
    for m in msgs:
        if sender_of(m) == "assistant":
            delivered |= files_back(m)
    first = re.sub(r"\s+", " ", text_of(human[0]))[:160] if human else ""
    return {
        "title": title,
        "date": (conv.get("created_at") or "")[:10],
        "project": (conv.get("project") or {}).get("name") if isinstance(conv.get("project"), dict)
                   else conv.get("project_name") or "",
        "turns": len(human),
        "revisions": len(later),
        "words_per_turn": round(statistics.mean(len(text_of(m).split()) for m in human)) if human else 0,
        "themes": themes,
        "files": sorted(delivered),
        "first": first,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", help="conversations.json from a claude.ai data export")
    ap.add_argument("--match", default=DEFAULT_MATCH, help="regex a conversation must match")
    args = ap.parse_args()

    data = json.load(open(args.export, encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("conversations") or data.get("data") or []
    if not isinstance(data, list) or not data:
        sys.exit("No conversations found. Is this the conversations.json from the export?")
    if not any("chat_messages" in c or "messages" in c for c in data[:20]):
        sys.exit("Conversations have no 'chat_messages' or 'messages' field; the export format "
                 "has changed. Open the file and adjust text_of()/sender_of().")

    pattern = re.compile(args.match, re.I)
    rows = sorted(filter(None, (summarize(c, pattern) for c in data)), key=lambda r: r["date"])
    if not rows:
        sys.exit(f"No conversation matched {args.match!r}.")

    themes = Counter()
    for r in rows:
        themes.update(r["themes"])
    revs = [r["revisions"] for r in rows]
    weeks = Counter(r["date"][:7] for r in rows)

    out = [f"# Skill usage: {len(rows)} conversations", ""]
    out.append(f"- Dates: {rows[0]['date']} to {rows[-1]['date']}")
    out.append(f"- Follow-up turns after the first request: median {statistics.median(revs)}, "
               f"max {max(revs)}, total {sum(revs)}")
    out.append(f"- One-shot conversations (no follow-up): {sum(1 for v in revs if v == 0)}")
    out.append("- By month: " + ", ".join(f"{k} {v}" for k, v in sorted(weeks.items())))
    out += ["", "## What the follow-ups asked for", "", "| Theme | Turns |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in themes.most_common()]
    out += ["", "## Every conversation", "",
            "| Date | Title | Project | Turns | Follow-ups | Top theme | Files back | First ask |",
            "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        top = r["themes"].most_common(1)[0][0] if r["themes"] else ""
        first = r["first"].replace("|", "/")
        out.append(f"| {r['date']} | {r['title'][:50]} | {r['project']} | {r['turns']} | "
                   f"{r['revisions']} | {top} | {len(r['files'])} | {first} |")
    print("\n".join(out))


if __name__ == "__main__":
    main()
