#!/usr/bin/env python3
"""Read a student packet back into what the deck is built and checked from.

Usage:
    python3 read_packet.py "Science 1.7 - Pump build - packet.docx"
    python3 read_packet.py packet.docx --languages es,zh -o packet.json

The deck is the packet seen on the wall, so it builds from the packet. In the conversation
that planned the lesson that is packet.json. Any other time it is the packet itself: the
Word file k12lessonplan made, or the same packet downloaded from its Google Doc as a
.docx, with whatever the teacher changed there. This reads that file and returns the shape
packet.json has: the lesson code and title, the timed sections, every numbered question in
the page's own words with its language lines, the key words, and the languages.

build_deck.py and check_deck.py take the .docx for --packet directly and read it through
here, so the deck is held to the page as printed. Run this first on its own: it prints
what it found, and a question it missed is cheaper to catch before the slides exist.

Standard library only: a .docx is a zip of XML, and the slideshow skill needs nothing the
planner installs.
"""

import argparse
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
LANG_INK = "3A3F45"          # the renderer's colour for a language line (ES_INK)
QUESTION = re.compile(r"^\s*(\d+[a-z]?)[.)]\s+(\S.*)$")
HEADING = re.compile(r"^([^\t·]+?)(?:\s+·\s+[^\t]+?)?(?:\t+\s*(\d+)\s*min)?$")
CODE = re.compile(r"^[A-Za-z][A-Za-z ]*\d+(?:\.\d+)+$")


def _on(el, tag):
    """A toggle property (w:b, w:i) is on when present unless its val says otherwise."""
    x = el.find(W + tag) if el is not None else None
    return x is not None and x.get(W + "val", "true").lower() not in ("false", "0", "off")


def _runs(p):
    """Each run's text and the properties that carry meaning in a packet."""
    out = []
    for r in p.iter(W + "r"):
        text = ""
        for node in r:
            if node.tag == W + "t":
                text += node.text or ""
            elif node.tag == W + "tab":
                text += "\t"
            elif node.tag in (W + "br", W + "cr"):
                text += " "
        if not text:
            continue
        rpr = r.find(W + "rPr")
        color = rpr.find(W + "color") if rpr is not None else None
        hl = rpr.find(W + "highlight") if rpr is not None else None
        shd = rpr.find(W + "shd") if rpr is not None else None
        lang = rpr.find(W + "lang") if rpr is not None else None
        sz = rpr.find(W + "sz") if rpr is not None else None
        fill = (shd.get(W + "fill") or "").upper() if shd is not None else ""
        out.append({
            "text": text,
            "bold": _on(rpr, "b"),
            "color": (color.get(W + "val") or "").upper() if color is not None else "",
            # Word writes a highlight; Google Docs exports the same mark as shading
            "marked": (hl is not None and hl.get(W + "val", "none") != "none")
                      or fill not in ("", "AUTO", "FFFFFF"),
            "lang": lang.get(W + "val") if lang is not None else None,
            "size": int(sz.get(W + "val")) / 2 if sz is not None and sz.get(W + "val", "").isdigit()
                    else None,
        })
    return out


def _indented(p):
    """A numbered step in a directions list sits indented; a question sits at the margin.
    Both open with a bold "1.", so the indent is what tells them apart."""
    ppr = p.find(W + "pPr")
    ind = ppr.find(W + "ind") if ppr is not None else None
    if ind is None:
        return False
    left = ind.get(W + "left") or ind.get(W + "start") or "0"
    return left.lstrip("-").isdigit() and int(left) > 0


def _guess_lang(text):
    """Only for a packet whose language lines carry no language tag and no --languages
    was given: tell the scripts apart, and the Latin-script lines by their marks."""
    for code, pat in (("zh", r"[一-鿿]"), ("ja", r"[぀-ヿ]"),
                      ("ko", r"[가-힯]"), ("ar", r"[؀-ۿ]"),
                      ("ru", r"[Ѐ-ӿ]"), ("vi", r"[ơưđăƠƯĐĂạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]"),
                      ("tl", r"\b(ang|mga|ng|sa)\b")):
        if re.search(pat, text):
            return code
    return "es"


def read_docx(path, languages=None):
    """The packet at `path` as the dict packet.json would be, plus meta.source."""
    with zipfile.ZipFile(path) as z:
        body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
        feet = [ET.fromstring(z.read(n)) for n in z.namelist()
                if re.match(r"word/(footer|header)\d*\.xml$", n)]

    meta = {"source": path}
    sections, vocab, seen_langs = [], [], []
    last_q = None          # the question the next language lines belong to
    tagged = False
    for p in body.iter(W + "p"):
        runs = _runs(p)
        text = "".join(r["text"] for r in runs).strip()
        if not text:
            continue
        for r in runs:
            if r["marked"]:
                w = r["text"].strip(" .,;:!?").lower()
                if w and w not in vocab:
                    vocab.append(w)
        visible = [r for r in runs if r["text"].strip()]
        is_line = visible and all(r["color"] == LANG_INK for r in visible)
        if is_line:
            code = next((r["lang"] for r in visible if r["lang"]), None)
            if code:
                tagged = True
                code = code.split("-")[0].lower()
            if last_q is not None:
                last_q.setdefault("_lines", []).append((code, text))
            continue
        lead = visible[0] if visible else None
        m = QUESTION.match(text)
        if m and lead and lead["bold"] and not _indented(p):
            last_q = {"type": "question", "number": m.group(1), "prompt": m.group(2).strip()}
            sections.append(last_q)
            continue
        last_q = None
        h = HEADING.match(text)
        if h and lead and lead["bold"] and lead["text"].strip().isupper() and (lead["size"] or 0) >= 13:
            blk = {"type": "heading", "text": h.group(1).strip().capitalize()}
            if h.group(2):
                blk["minutes"] = int(h.group(2))
            sections.append(blk)
        elif "title" not in meta and lead and lead["bold"] and (lead.get("size") or 0) >= 16:
            meta["title"] = text

    # the language lines under each question, keyed by language: by the tag the renderer
    # writes, else by the order --languages gives, else by the script they're written in
    langs = [c.strip() for c in (languages or "").split(",") if c.strip()]
    for q in sections:
        for i, (code, line) in enumerate(q.pop("_lines", [])):
            if not code:
                code = langs[i] if i < len(langs) else _guess_lang(line)
            q.setdefault(code, line)
            if code not in seen_langs:
                seen_langs.append(code)
    meta["languages"] = langs or seen_langs
    # the renderer marks a key word however the sentence inflects it ("flow rates"), so a
    # plural whose singular is also marked is the same word
    vocab = [w for w in vocab
             if not any(w in (v + "s", v + "es") for v in vocab if v != w)]
    if vocab:
        meta["vocab"] = vocab

    for root in feet:
        for p in root.iter(W + "p"):
            bits = [b.strip() for b in "".join(t.text or "" for t in p.iter(W + "t")).split("·")]
            if bits and CODE.match(bits[0]):
                meta["code"] = bits[0]
                break
        if "code" in meta:
            break
    meta["_tagged"] = tagged
    return {"meta": meta, "sections": sections}


def load_packet(path, languages=None):
    """packet.json as written, or a packet .docx read back into the same shape. A file that
    exists but can't be read as either raises ValueError, so callers catch one thing."""
    if str(path).lower().endswith(".docx"):
        try:
            return read_docx(path, languages)
        except (KeyError, zipfile.BadZipFile, ET.ParseError) as e:
            raise ValueError(f"not a readable Word packet ({e})") from e
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("packet", help="the packet .docx (or a packet.json, read as is)")
    ap.add_argument("--languages", default="",
                    help="home languages in print order, e.g. es,zh; only needed when the "
                         "packet's language lines carry no language tag")
    ap.add_argument("-o", "--out", help="also write what was read as JSON here")
    args = ap.parse_args()
    try:
        data = load_packet(args.packet, args.languages)
    except (OSError, ValueError) as e:
        print(f"cannot read {args.packet}: {e}", file=sys.stderr)
        return 1
    meta = data.get("meta", {})
    qs = [b for b in data.get("sections", []) if b.get("type") == "question"]
    langs = meta.get("languages") or []
    print(f"  lesson     {meta.get('code', '(no code in the footer)')}  ·  {meta.get('title', '(no title)')}")
    timed = [b for b in data.get("sections", []) if b.get("type") == "heading"]
    if timed:
        print("  sections   " + "  ·  ".join(
            b["text"] + (f" {b['minutes']} min" if b.get("minutes") else "") for b in timed))
    print(f"  languages  {', '.join(langs) or '(none)'}"
          + ("" if meta.get("_tagged") or not qs else "  (untagged lines: from --languages or the script)"))
    print(f"  key words  {', '.join(meta.get('vocab', [])) or '(none marked)'}")
    print(f"  questions  {len(qs)}")
    for q in qs:
        missing = [c for c in langs if not q.get(c)]
        print(f"    {q['number']:>3}. {q['prompt'][:80]}"
              + (f"   (no {', '.join(missing)} line)" if missing else ""))
    if not qs:
        print("  No numbered questions found. If this packet was not made by k12lessonplan, "
              "build from its text with --vocab and --languages instead of --packet.")
    if args.out:
        meta.pop("_tagged", None)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
