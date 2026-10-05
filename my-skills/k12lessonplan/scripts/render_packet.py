#!/usr/bin/env python3
"""Render a lesson JSON into an editable Word document.

Usage:
    python3 render_packet.py packet.json out.docx

One renderer serves both audiences. `"audience": "student"` produces the student packet
(large type, generous write space, hints, stems). `"audience": "teacher"` produces the
lesson plan (tighter type, phase headers with minutes, notes and tables).

The renderer's main job beyond typesetting is keeping a task whole: a question, its hint,
its stems, and its answer space are bound together so a page break can never land inside
them. Nothing in the JSON needs to say that — it happens for every task block.

A room whose students read in other home languages lists them in `meta.languages`
(["es"], ["es", "vi"], ...), and any block a student has to act on carries one short line
per language under a key named by its code: `"es": "...", "vi": "..."`, rendered under the
English it supports. It is abbreviated support, not a translation -- see
references/packet.md for what gets one and what deliberately does not. On a student packet
the renderer reports, on stderr, every question missing a line in a listed language and
every line that ran longer than its English. With no `meta.languages` there are no language
lines (an older packet that carries "es" lines without the key is read as ["es"]).

`meta.code` is the teacher's own name for the session ("Science 1.7") and leads the header
and footer. `meta.large_print: true` sets the whole packet in larger type for the students
whose plans call for it.

`meta.vocab` lists the lesson's key words. In a student packet each one is printed bold on
a yellow highlight the first time it appears in each section (`meta.vocab_style: "bold"`
drops the highlight for a copier that turns it to mud). Once per section, not every time:
a page where every third word is yellow marks nothing, and highlights on neighbouring lines
run into each other. Word banks list the words in plain bold. On stderr the renderer reports
how the student text reads against `meta.reading_level` (default: the grade in
`meta.grade` or `meta.course`): the sentences
that run long and the long words that aren't key vocab.

    python3 render_packet.py packet.json out.docx --reduced

builds the reduced packet from the same JSON: questions marked "core": false are left out,
each question keeps only its first part, the type is large, and the packet's word banks
become one, on the front page under the "I can".

Requires python-docx. Install with: pip install python-docx --break-system-packages
"""

import argparse
import copy
import json
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import (WD_ALIGN_PARAGRAPH, WD_BREAK, WD_COLOR_INDEX, WD_LINE_SPACING,
                             WD_TAB_ALIGNMENT)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

# ---------------------------------------------------------------- style constants

STUDENT = {
    "font": "Verdana",
    "body": 12,
    "h1": 17,
    "h2": 13.5,
    "small": 10,
    "es": 11,             # the language line is read by the students with the least margin
    "margin": 0.7,
    "line_gap": 30,       # points between writing lines — room for large handwriting
    "space_after": 8,
}

TEACHER = {
    "font": "Calibri",
    "body": 11,
    "h1": 16,
    "h2": 12.5,
    "small": 9.5,
    "es": 10,
    "margin": 0.75,
    "line_gap": 24,
    "space_after": 6,
}

INK = RGBColor(0x1B, 0x1F, 0x24)
MUTED = RGBColor(0x69, 0x70, 0x79)
# A language line is secondary to the English but it is not fine print: the students
# reading it are the ones with the least margin. Darker than MUTED, lighter than INK.
ES_INK = RGBColor(0x3A, 0x3F, 0x45)
ACCENT = RGBColor(0x3E, 0x6D, 0xA8)
RULE = "E4E7EB"
FILL = "F3F6FA"
BOX_LINE = "9AA2AC"
# Structure is drawn in hairlines, never in fills: a grey fill costs toner on every copy,
# prints as mud on a tired copier, and lowers the contrast of whatever sits on it.
GRID = "8A9099"


# ---------------------------------------------------------------- low-level helpers

def _shade(cell, hexfill):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hexfill)
    cell._tc.get_or_add_tcPr().append(el)


def _cell_borders(cell, color=BOX_LINE, sz=6, sides=("top", "left", "bottom", "right"),
                  style="single"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = tcPr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tcPr.append(borders)
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        if side in sides:
            el.set(qn("w:val"), style)
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:color"), color)
        else:
            el.set(qn("w:val"), "nil")
        borders.append(el)


def _para_border(par, side="bottom", color=BOX_LINE, sz=6):
    pPr = par._p.get_or_add_pPr()
    bdr = pPr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        pPr.append(bdr)
    el = OxmlElement(f"w:{side}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), "1")
    el.set(qn("w:color"), color)
    bdr.append(el)


def _no_split(table):
    """Rows stay whole, and the table stays on one page: every paragraph in every row
    but the last is kept with the next, so a break can only land before or after it.
    A vote tally split across two pages is two half-organizers."""
    rows = list(table.rows)
    for i, row in enumerate(rows):
        trPr = row._tr.get_or_add_trPr()
        el = OxmlElement("w:cantSplit")
        trPr.append(el)
        if i < len(rows) - 1:
            for cell in row.cells:
                for par in cell.paragraphs:
                    par.paragraph_format.keep_with_next = True


def _grid(table, color=GRID, sz=4, header=False):
    """Hairline grid on every cell; a firmer rule under the header row."""
    for r, row in enumerate(table.rows):
        for cell in row.cells:
            _cell_borders(cell, color, sz)
            if header and r == 0:
                tcb = cell._tc.get_or_add_tcPr().find(qn("w:tcBorders"))
                bottom = tcb.find(qn("w:bottom"))
                bottom.set(qn("w:sz"), "10")
                bottom.set(qn("w:color"), "1B1F24")


def _widths(table, inches):
    """Fix column widths. Word ignores a cell width unless autofit is off and every
    cell in the column agrees."""
    table.autofit = False
    for i, w in enumerate(inches):
        table.columns[i].width = Inches(w)
        for cell in table.columns[i].cells:
            cell.width = Inches(w)


def _valign_bottom(cell):
    el = OxmlElement("w:vAlign")
    el.set(qn("w:val"), "bottom")
    cell._tc.get_or_add_tcPr().append(el)


BLANK = re.compile(r"_{2,}")
# a gap wide enough to write a word or two in by hand
GAP = "\u00a0" * 18


def _row_height(row, inches):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:trHeight")
    el.set(qn("w:val"), str(int(inches * 1440)))
    el.set(qn("w:hRule"), "atLeast")
    trPr.append(el)


# languages written without spaces between words: the word-count length check skips them
UNSPACED = {"zh", "ja", "ko", "th", "my", "km", "lo"}
# languages that put a space between syllables, not words: a word count runs far past the
# English for the same content, so their lines are measured in characters instead
SYLLABIC = {"vi"}
# languages written right to left: their line is right-aligned and marked bidi
RTL = {"ar", "fa", "ur", "he", "ps", "prs"}


def _rtl(par, lang):
    if str(lang).split("-")[0] not in RTL:
        return
    par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    ppr = par._p.get_or_add_pPr()
    # schema order: bidi sits ahead of spacing, indentation and justification
    ppr.insert_element_before(
        OxmlElement("w:bidi"), "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
        "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
        "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
        "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")
    for r in par.runs:
        r._r.get_or_add_rPr().append(OxmlElement("w:rtl"))


EAST_ASIAN = {"zh", "ja", "ko"}


def _lang_tag(par, lang):
    """Mark a language line with its language. Read-aloud on a student's device then speaks
    it in the right voice instead of an English one, and the slideshow skill, reading the
    packet back, knows which line is which language. Runs after _rtl: w:lang follows w:rtl
    in a run's properties."""
    code = str(lang or "").strip()
    if not code:
        return
    base = code.split("-")[0]
    for r in par.runs:
        el = OxmlElement("w:lang")
        el.set(qn("w:val"), code)
        if base in EAST_ASIAN:
            el.set(qn("w:eastAsia"), code)
        if base in RTL:
            el.set(qn("w:bidi"), code)
        r._r.get_or_add_rPr().append(el)


# ---------------------------------------------------------------- readability

def syllables(word):
    """A plain vowel-group count: good to a syllable on everyday English, which is all a
    reading-level estimate needs."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|[^laeiouy]ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def readability(items, vocab, target):
    """Report lines for the student's English: an overall grade estimate (key words count
    as one syllable, because they are being taught, not assumed), every sentence over 20
    words, and the long words that are not key vocabulary."""
    taught = {w.lower() for v in vocab for w in v.split()}
    words = sents = syl = 0
    long_sents, hard = [], {}
    for label, text in items:
        text = re.sub(r"\*\*|_{2,}", " ", str(text))
        for sent in re.split(r"(?<=[.?!])\s+", text.strip()):
            ws = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", sent)]
            if not ws:
                continue
            sents += 1
            words += len(ws)
            for w in ws:
                base = re.sub(r"(?:'s|s|es|ed|ing)$", "", w.lower())
                n = 1 if (w.lower() in taught or base in taught) else syllables(w)
                syl += n
                if n >= 4 or (len(w) >= 12 and w.lower() not in taught and base not in taught):
                    hard.setdefault(label, []).append(w)
            if len(ws) > 20:
                long_sents.append(f"{label}: one sentence of {len(ws)} words")
    if not words:
        return []
    grade = 0.39 * words / sents + 11.8 * syl / words - 15.59
    if target is None:
        out = [f"  note  reads at about grade {max(grade, 1):.1f}, {words / sents:.0f} words a "
               "sentence (no target: set meta.grade, or meta.reading_level from the profile)"]
    else:
        out = [f"  {'ok  ' if grade <= max(target, 1) + 0.5 else 'note'}  reads at about grade "
               f"{max(grade, 1):.1f} (target {max(target, 1):g}), {words / sents:.0f} words a sentence"]
    for line in long_sents[:6]:
        out.append(f"  note  {line}. Break it in two.")
    for label, ws in list(hard.items())[:6]:
        uniq = list(dict.fromkeys(ws))
        out.append(f"  note  {label}: " + ", ".join(f"'{w}'" for w in uniq)
                   + (" is a long word" if len(uniq) == 1 else " are long words")
                   + " outside the key vocab. Say it shorter, or add it to meta.vocab if it "
                   "is being taught.")
    return out


def packet_languages(data):
    """The home languages that get a line, in print order. An explicit `meta.languages`
    wins, an empty list included. Without the key, a packet that already carries "es"
    lines (written before languages were opt-in) is read as Spanish; anything else has
    no language lines."""
    meta = data.get("meta", {})
    if "languages" in meta:
        return [str(c) for c in (meta.get("languages") or [])]
    if any(isinstance(b, dict) and b.get("es") for b in data.get("sections", [])):
        return ["es"]
    return []


def reading_target(meta):
    """The grade the student's English should read at: `meta.reading_level` when the
    class profile gives one, else the class's own grade (`meta.grade`, or the grade named
    in `meta.course`, K as 0). None when nothing says."""
    if meta.get("reading_level") not in (None, ""):
        return float(meta["reading_level"])
    for v in (meta.get("grade"), meta.get("course")):
        if v in (None, ""):
            continue
        t = str(v).strip().lower()
        if re.match(r"^(k|kindergarten)\b", t) or re.search(r"\bgrade k\b", t):
            return 0.0
        m = re.search(r"(\d{1,2})", t)
        if m and 0 < int(m.group(1)) <= 12:
            return float(m.group(1))
    return None


class Renderer:
    def __init__(self, data, out_path):
        self.data = data
        self.out = out_path
        self.audience = data.get("audience", "student")
        self.S = dict(STUDENT if self.audience == "student" else TEACHER)
        meta = data.get("meta", {})
        if meta.get("large_print"):
            for k in ("body", "h1", "h2", "small", "es"):
                self.S[k] = round(self.S[k] * 1.25 * 2) / 2
            self.S["line_gap"] = round(self.S["line_gap"] * 1.2)
        # the home languages in the room; each carries one short line under the English
        self.langs = packet_languages(data)
        self.days_seen = 0      # `day` blocks so far; every one after the first starts a page
        self.vocab = []
        self._vocab_re = None
        self._vocab_hits = {}
        self._vocab_seen = set()    # key words already highlighted in this section
        self.add_vocab(meta.get("vocab") or [])
        self.vocab_style = meta.get("vocab_style", "highlight")
        self.reading_level = reading_target(meta)
        self._read = []         # (label, English text) for every prompt and direction
        self.doc = Document()
        self._setup()
        # every paragraph the renderer emits is registered here so a task group can be
        # bound together after the fact
        self._group = None
        self._last_group = []
        # where paragraphs and tables go: the document, or the cell of an open unit
        self.target = self.doc
        self._fresh = None
        # language-line coverage, reported on stderr once the document is written
        self._es = []
        self._missing_es = {c: [] for c in self.langs}
        self._long_es = []

    # ------------------------------------------------------------ document setup
    def _setup(self):
        sec = self.doc.sections[0]
        m = Inches(self.S["margin"])
        sec.top_margin = sec.bottom_margin = m
        sec.left_margin = sec.right_margin = m
        normal = self.doc.styles["Normal"]
        normal.font.name = self.S["font"]
        normal.font.size = Pt(self.S["body"])
        normal.font.color.rgb = INK
        rpr = normal.element.get_or_add_rPr()
        rfonts = rpr.get_or_add_rFonts()
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rfonts.set(qn(attr), self.S["font"])
        pf = normal.paragraph_format
        pf.space_after = Pt(self.S["space_after"])
        pf.space_before = Pt(0)
        pf.line_spacing = 1.15
        self._footer()

    def _footer(self):
        meta = self.data.get("meta", {})
        foot = self.doc.sections[0].footer.paragraphs[0]
        bits = [b for b in (meta.get("code"), meta.get("course"), meta.get("day"),
                            meta.get("title")) if b]
        run = foot.add_run("  ·  ".join(bits))
        run.font.size = Pt(self.S["small"] - 1)
        run.font.color.rgb = MUTED
        run.font.name = self.S["font"]
        foot.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ------------------------------------------------------------ text primitives
    def _par(self):
        """A new paragraph in the current target. A fresh unit cell already holds one
        empty paragraph; the first paragraph written there reuses it, so a unit never
        opens with a blank line."""
        if self._fresh is not None:
            par, self._fresh = self._fresh, None
            return par
        return self.target.add_paragraph()

    def _table(self, rows, cols):
        self._fresh = None
        t = self.target.add_table(rows=rows, cols=cols)
        if self.target is not self.doc:
            # python-docx follows a table in a cell with an empty, full-height
            # paragraph; hand it to whatever is written next instead of leaving a
            # blank line after every table in every unit
            self._fresh = self.target.paragraphs[-1]
        return t

    def p(self, text="", size=None, bold=False, italic=False, color=None,
          space_after=None, space_before=None, indent=0, keep=False, align=None):
        par = self._par()
        if indent:
            par.paragraph_format.left_indent = Inches(indent)
        if space_after is not None:
            par.paragraph_format.space_after = Pt(space_after)
        if space_before is not None:
            par.paragraph_format.space_before = Pt(space_before)
        if align is not None:
            par.alignment = align
        if keep:
            par.paragraph_format.keep_with_next = True
        if text:
            self.run(par, text, size=size, bold=bold, italic=italic, color=color)
        if self._group is not None:
            self._group.append(par)
        return par

    def gap(self, pts=6):
        """The paragraph Word needs after every table, held to a few points. At full
        line height it is a wasted line after every table, and when a table fills a
        page it is the reason a blank page prints."""
        par = self._par()
        pf = par.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(max(1, int(pts)))
        if self._group is not None:
            self._group.append(par)
        return par

    def run(self, par, text, size=None, bold=False, italic=False, color=None):
        r = par.add_run(text)
        r.font.name = self.S["font"]
        r.font.size = Pt(size or self.S["body"])
        r.bold = bold
        r.italic = italic
        r.font.color.rgb = color or INK
        return r

    def es_line(self, text, indent=0, space_after=4, lang="es"):
        """A home-language support line — one line, under the English it supports.

        Not italic. Italic costs a striving reader real speed, and this line is read
        by the students who have the least of it to spare; the separation from the
        English comes from size and colour instead.
        """
        if not text:
            return None
        self._es.append(str(text))
        par = self.p(space_after=space_after, space_before=0, indent=indent)
        self.rich(par, str(text), size=self.S["es"], vocab=False)
        for r in par.runs:
            r.font.color.rgb = ES_INK
        _rtl(par, lang)
        _lang_tag(par, lang)
        return par

    def es_in_cell(self, cell, text, lang="es"):
        """Same line, but inside a tinted box (a note, a word bank) so it stays in it."""
        if not text:
            return None
        self._es.append(str(text))
        par = cell.add_paragraph()
        par.paragraph_format.space_before = Pt(2)
        par.paragraph_format.space_after = Pt(0)
        self.rich(par, str(text), size=self.S["es"], vocab=False)
        for r in par.runs:
            r.font.color.rgb = ES_INK
        _rtl(par, lang)
        _lang_tag(par, lang)
        return par

    def lang_lines(self, blk, indent=0, space_after=4):
        """One line per home language, in the order meta.languages lists them."""
        pars = []
        for code in self.langs:
            par = self.es_line(blk.get(code), indent=indent, space_after=space_after, lang=code)
            if par is not None:
                pars.append(par)
        return pars

    def lang_in_cell(self, cell, blk):
        for code in self.langs:
            self.es_in_cell(cell, blk.get(code), lang=code)

    def rich(self, par, text, size=None, vocab=True):
        """Renders **bold** spans inside a plain string, and on a student packet marks each
        key word (meta.vocab) the first time it falls in a section. Everything else is
        literal."""
        for i, chunk in enumerate(text.split("**")):
            if not chunk:
                continue
            pieces = [(chunk, False)]
            if vocab and self._vocab_re is not None and self.audience == "student":
                pieces, last = [], 0
                for m in self._vocab_re.finditer(chunk):
                    key = " ".join(m.group(1).lower().split())
                    self._vocab_hits[key] = self._vocab_hits.get(key, 0) + 1
                    if key in self._vocab_seen:
                        continue
                    self._vocab_seen.add(key)
                    pieces.append((chunk[last:m.start()], False))
                    pieces.append((m.group(0), True))
                    last = m.end()
                pieces.append((chunk[last:], False))
            for piece, key in pieces:
                if not piece:
                    continue
                r = self.run(par, piece, size=size, bold=(i % 2 == 1) or key)
                if key:
                    self.mark_vocab(r)

    def mark_vocab(self, r):
        r.bold = True
        if self.vocab_style == "bold":
            r.font.underline = True
        else:
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW

    def add_vocab(self, words):
        """Key words for this packet (and a day's own words in a multi-day packet). A word
        matches with an ordinary ending (-s, -es, -ed, -ing) so 'pump' marks 'pumps'."""
        for w in words:
            w = " ".join(str(w).split())
            if w and w.lower() not in (v.lower() for v in self.vocab):
                self.vocab.append(w)
        if self.vocab:
            alts = "|".join(r"\s+".join(map(re.escape, w.split()))
                            for w in sorted(self.vocab, key=len, reverse=True))
            self._vocab_re = re.compile(r"(?<![\w-])(" + alts + r")(?:s|es|ed|ing)?(?![\w-])",
                                        re.IGNORECASE)

    def _in_a_task(self, word):
        """Whether a key word turns up in something a student answers (a question's prompt,
        parts, stems or choices, or an organizer's stems), not only in a note or a text."""
        pat = re.compile(r"(?<![\w-])" + r"\s+".join(map(re.escape, word.split()))
                         + r"(?:s|es|ed|ing)?(?![\w-])", re.IGNORECASE)

        def walk(blocks):
            for b in blocks or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "question":
                    yield b.get("prompt", "")
                    for k in ("parts", "stems", "choices"):
                        yield from (str(x) for x in (b.get(k) or []))
                elif b.get("type") == "organizer":
                    if b.get("kind") == "cer":
                        yield "Claim Evidence Reasoning"   # the organizer's own row names
                    stems = b.get("stems") or {}
                    yield from (str(v) for v in (stems.values() if isinstance(stems, dict) else stems))
                    yield from (str(c) for c in (b.get("columns") or []) + (b.get("steps") or []))
                yield from walk(b.get("sections"))

        return any(pat.search(t) for t in walk(self.data.get("sections")))

    # ------------------------------------------------------------ group binding
    def begin_group(self):
        self._group = []

    def end_group(self):
        """Bind everything emitted since begin_group so a page break can't split it."""
        self._last_group = list(self._group or [])
        if not self._group:
            self._group = None
            return
        for par in self._group[:-1]:
            par.paragraph_format.keep_with_next = True
        self._group = None

    # ------------------------------------------------------------ blocks
    def heading(self, text, minutes=None, es=None, blk=None):
        """One line per section: the name, its gloss in the room's language, and the
        minutes flush right. Three lines of heading per section is a page of headings
        across a packet."""
        self._vocab_seen = set()    # a new section highlights its key words afresh
        par = self.p(space_before=10, space_after=4, keep=True)
        self.run(par, text.upper(), size=self.S["h2"], bold=True)
        lines = blk if blk is not None else {"es": es}
        # with one home language the gloss rides on the heading line; with two or
        # more, headings go without, and the lines stay on the tasks (SKILL.md)
        if len(self.langs) == 1 and lines.get(self.langs[0]):
            gloss = self.run(par, "  ·  " + str(lines[self.langs[0]]), size=self.S["es"])
            gloss.font.color.rgb = ES_INK
        if minutes:
            width = 8.5 - 2 * self.S["margin"]
            par.paragraph_format.tab_stops.add_tab_stop(Inches(width), WD_TAB_ALIGNMENT.RIGHT)
            self.run(par, f"\t{minutes} min", size=self.S["small"], color=MUTED, bold=True)
        _para_border(par, "bottom", GRID, 6)
        par.paragraph_format.keep_with_next = True
        return par

    def title_block(self):
        meta = self.data.get("meta", {})
        eyebrow = "  ·  ".join(
            b for b in (meta.get("code"), meta.get("course"), meta.get("day"), meta.get("period"))
            if b
        )
        if eyebrow:
            par = self.p(space_after=2, keep=True)
            self.run(par, eyebrow.upper(), size=self.S["small"], color=MUTED, bold=True)
        par = self.p(space_after=6, keep=True)
        self.run(par, meta.get("title", ""), size=self.S["h1"], bold=True)

        if self.audience == "student" and meta.get("name_line", True):
            self.name_line()

        obj = self.data.get("objective")
        if obj:
            self._banner("Objective", obj, self.data.get("standard"))
        # The agenda belongs on the board and in the deck, not on the student's page —
        # printing it there costs a third of page 1 and students read it off the screen
        # anyway. The lesson plan always prints it.
        agenda = self.data.get("agenda")
        if agenda and (self.audience == "teacher" or meta.get("show_agenda")):
            self.agenda(agenda)

    def name_line(self):
        t = self._table(rows=1, cols=2)
        t.autofit = True
        for cell, label in zip(t.rows[0].cells, ("Name:", "Date:")):
            cell.text = ""
            par = cell.paragraphs[0]
            self.run(par, label, size=self.S["small"], color=MUTED)
            par.paragraph_format.space_after = Pt(2)
            _cell_borders(cell, RULE, 6, sides=("bottom",))
        _no_split(t)
        self.gap(4)

    def day(self, blk):
        """Opens one day of a multi-day packet. Every day after the first starts on a fresh
        page with its own name line, so a day can be handed out, collected, or reprinted from
        the Google Doc on its own; each day carries its own "I can"."""
        later = self.days_seen > 0
        self.days_seen += 1
        self.add_vocab(blk.get("vocab") or [])
        self._vocab_seen = set()
        if later:
            self.page_break()
        eyebrow = "  ·  ".join(str(b) for b in (blk.get("code"), blk.get("day"), blk.get("period"))
                               if b)
        if eyebrow:
            par = self.p(space_before=0 if later else 6, space_after=2, keep=True)
            self.run(par, eyebrow.upper(), size=self.S["small"], color=MUTED, bold=True)
        if blk.get("title"):
            par = self.p(space_after=4, keep=True)
            self.run(par, blk["title"], size=self.S["h2"] + 1.5, bold=True)
            line = blk.get(self.langs[0]) if len(self.langs) == 1 else None
            if line:
                gloss = self.run(par, "  ·  " + str(line), size=self.S["es"])
                gloss.font.color.rgb = ES_INK
        meta = self.data.get("meta", {})
        if later and self.audience == "student" and meta.get("name_line", True):
            self.name_line()
        if blk.get("objective"):
            self._banner("Objective", blk["objective"], blk.get("standard"))

    def page_break(self):
        # The break's own paragraph mark lands at the top of the new page, so it is made
        # 1 pt tall instead of a blank line.
        par = self._par()
        par.add_run().add_break(WD_BREAK.PAGE)
        pf = par.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(1)
        pf.space_before = pf.space_after = Pt(0)

    def _banner(self, label, text, sub=None):
        t = self._table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _cell_borders(cell, "1B1F24", 12, sides=("left",))
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        self.run(par, ("I can" if label.lower() == "objective" else label).upper() + "  ",
                 size=self.S["small"], bold=True)
        body = text[6:] if label.lower() == "objective" and text.lower().startswith("i can ") else text
        self.run(par, body, size=self.S["body"])
        if sub:
            p2 = cell.add_paragraph()
            p2.paragraph_format.space_before = Pt(2)
            p2.paragraph_format.space_after = Pt(0)
            self.run(p2, sub, size=self.S["small"], color=MUTED)
        _no_split(t)
        self.gap(2)

    def agenda(self, items):
        par = self.p(space_before=8, space_after=3, keep=True)
        self.run(par, "TODAY", size=self.S["small"], bold=True, color=MUTED)
        rows = []
        for it in items:
            if isinstance(it, (list, tuple)):
                rows.append((str(it[0]), f"{it[1]} min" if len(it) > 1 else ""))
            else:
                rows.append((str(it), ""))
        t = self._table(rows=len(rows), cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        for (name, mins), row in zip(rows, t.rows):
            row.cells[0].width = Inches(4.6)
            row.cells[1].width = Inches(1.1)
            p1 = row.cells[0].paragraphs[0]
            p1.paragraph_format.space_after = Pt(1)
            self.run(p1, name, size=self.S["body"])
            p2 = row.cells[1].paragraphs[0]
            p2.paragraph_format.space_after = Pt(1)
            p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            self.run(p2, mins, size=self.S["small"], color=MUTED)
            for c in row.cells:
                _cell_borders(c, RULE, 4, sides=("bottom",))
        _no_split(t)
        self.gap(4)

    def question(self, blk):
        self.begin_group()
        num = str(blk.get("number", "")).strip()
        par = self.p(space_before=9, space_after=3)
        if num:
            self.run(par, f"{num}. ", bold=True)
        self.rich(par, blk.get("prompt", ""))
        self._read.append((f"question {num}" if num else "a question",
                           " ".join([blk.get("prompt", "")] + list(blk.get("parts") or []))))
        if blk.get("minutes"):
            self.run(par, f"   ({blk['minutes']} min)", size=self.S["small"], color=MUTED)

        for code in self.langs:
            line = blk.get(code)
            if line:
                self.es_line(line, lang=code)
                self._check_es_length(blk.get("prompt", ""), line, num, code)
            elif self.audience == "student":
                self._missing_es[code].append(num or blk.get("prompt", "")[:40])

        if blk.get("example"):
            self.tinted("Example", blk["example"])
        if blk.get("hint"):
            self.tinted("Hint", blk["hint"])
        for sub in blk.get("parts", []) or []:
            par = self.p(space_after=3, indent=0.3)
            self.rich(par, sub)
        choices = blk.get("choices") or []
        if choices:
            # options to circle get a line of their own, spaced wide enough to
            # circle one without touching the next
            par = self.p(space_before=4, space_after=4, indent=0.3)
            for i, c in enumerate(choices):
                if i:
                    self.run(par, "\u00a0" * 10)
                self.run(par, str(c), bold=True)
        stems = blk.get("stems", []) or []
        spec = blk.get("space", {"kind": "lines", "count": 3})
        if stems and isinstance(spec, dict) and spec.get("kind", "lines") == "lines":
            # the stem is the first writing line, not a box above the lines: the
            # student starts writing where the sentence starts
            self.space(dict(spec, count=max(int(spec.get("count", 2)), len(stems))), stems)
        else:
            for stem in stems:
                self.stem(stem)
            self.space(spec)
        if spec == {"kind": "none"} or (isinstance(spec, dict) and spec.get("kind") == "none"):
            # a question whose answer space is the table or organizer after it
            # stays on the same page as that table
            for par in self._group or []:
                par.paragraph_format.keep_with_next = True
        self.end_group()

    def stem(self, text):
        t = self._table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _cell_borders(cell, GRID, 8, sides=("left",), style="single")
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        par.paragraph_format.space_before = Pt(1)
        self.rich(par, text)
        _no_split(t)
        p = self.p(space_after=2)
        return t

    def tinted(self, label, text):
        par = self.p(space_after=4, indent=0.15)
        self.run(par, f"{label}: ", size=self.S["small"], bold=True, color=ACCENT)
        self.rich(par, text, size=self.S["small"])
        return par

    def stem_on_line(self, cell, text):
        """A sentence frame printed on its writing line: blanks become gaps on the
        rule, and a trailing blank becomes the rest of the line."""
        text = BLANK.sub("___", str(text)).strip()
        text = re.sub(r"\s*___\s*[.?!]?$", "", text)   # a trailing blank is the rest of the line
        par = cell.paragraphs[0]
        for i, chunk in enumerate(text.split("___")):
            if i:
                gap = self.run(par, GAP)
                gap.font.underline = True
            if chunk:
                self.rich(par, chunk)
        _valign_bottom(cell)

    def space(self, spec, stems=None):
        if not spec:
            return
        kind = spec.get("kind", "lines") if isinstance(spec, dict) else str(spec)
        if kind == "none":
            return
        if kind == "lines":
            # Writing lines are a borderless table with a rule under each row. Bordered
            # empty paragraphs look right in isolation but Word merges consecutive
            # identical borders into one box, so three lines print as one.
            count = int(spec.get("count", 3)) if isinstance(spec, dict) else 3
            t = self._table(rows=count, cols=1)
            for i, row in enumerate(t.rows):
                cell = row.cells[0]
                _cell_borders(cell, BOX_LINE, 6, sides=("bottom",))
                par = cell.paragraphs[0]
                par.paragraph_format.space_before = Pt(0)
                par.paragraph_format.space_after = Pt(1)
                if stems and i < len(stems):
                    self.stem_on_line(cell, stems[i])
                _row_height(row, self.S["line_gap"] / 72.0)
            _no_split(t)
            self.gap(6)
            return
        # box / work space
        height = float(spec.get("height_in", 2.0)) if isinstance(spec, dict) else 2.0
        label = spec.get("label") if isinstance(spec, dict) else None
        t = self._table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _cell_borders(cell, BOX_LINE, 6)
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        if label:
            self.run(par, label, size=self.S["small"], color=MUTED)
        _row_height(t.rows[0], height)
        _no_split(t)
        self.gap(4)

    def table(self, blk, fill_rows=0, row_height=None):
        headers = blk.get("headers") or []
        rows = [list(r) for r in (blk.get("rows") or [])]
        blanks = int(blk.get("blank_rows", fill_rows) or 0)
        ncols = len(headers) or (len(rows[0]) if rows else 2)
        total = len(rows) + blanks + (1 if headers else 0)
        if total == 0:
            return
        t = self._table(rows=total, cols=ncols)
        _grid(t, header=bool(headers))
        idx = 0
        if headers:
            for c, head in enumerate(headers):
                cell = t.rows[0].cells[c]
                par = cell.paragraphs[0]
                par.paragraph_format.space_after = Pt(2)
                self.run(par, str(head), size=self.S["small"], bold=True)
            idx = 1
        for r, data_row in enumerate(rows):
            for c in range(ncols):
                cell = t.rows[idx + r].cells[c]
                par = cell.paragraphs[0]
                par.paragraph_format.space_after = Pt(2)
                val = data_row[c] if c < len(data_row) else ""
                self.rich(par, str(val))
        # every row a student writes in is tall enough to write in, filled or not
        h = float(row_height or blk.get("row_height_in", 0.36))
        for r in range(1 if headers else 0, total):
            _row_height(t.rows[r], h)
            for cell in t.rows[r].cells:
                cell.paragraphs[0].paragraph_format.space_before = Pt(3)
        _no_split(t)
        self.gap(6)

    def note(self, blk):
        t = self._table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _cell_borders(cell, BOX_LINE, 12, sides=("left",))
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        label = blk.get("label")
        if label:
            self.run(par, label.upper() + "  ", size=self.S["small"], bold=True)
        self.rich(par, blk.get("text", ""))
        self._read.append((f"the {label.lower()} note" if label else "a note", blk.get("text", "")))
        self.lang_in_cell(cell, blk)
        _no_split(t)
        self.gap(4)

    def listing(self, blk):
        self.begin_group()
        if blk.get("label"):
            par = self.p(space_before=8, space_after=3)
            self.run(par, blk["label"], bold=True)
        self.lang_lines(blk, space_after=5)
        ordered = blk.get("ordered", False)
        for i, item in enumerate(blk.get("items", []), 1):
            par = self.p(space_after=4, indent=0.25)
            marker = f"{i}. " if ordered else "•  "
            self.run(par, marker, bold=ordered)
            self.rich(par, str(item))
            self._read.append((blk.get("label") or "a list item", str(item)))
        self.end_group()

    def wordbank(self, blk):
        t = self._table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _cell_borders(cell, GRID, 4)
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        self.run(par, (blk.get("label") or "Word bank").upper() + "  ",
                 size=self.S["small"], bold=True)
        # plain bold: the bank is the list of key words, so a highlight on each one says
        # nothing, and the section's first use of a word still gets its highlight
        for k, item in enumerate(blk.get("items", [])):
            if k:
                self.run(par, "     ")
            self.run(par, str(item).replace("**", ""), bold=True)
        self.lang_in_cell(cell, blk)
        _no_split(t)
        self.gap(4)


    # ------------------------------------------------------------ graphic organizers
    def organizer(self, blk):
        """A graphic organizer matched to the thinking the task asks for: compare
        (tchart), notice and wonder, sequence (flow), argue (cer), a new word (frayer).
        Drawn in hairlines like everything else, and kept on one page."""
        kind = blk.get("kind", "tchart")
        label = blk.get("label") or (f"New word: {blk['word']}" if blk.get("word") else None)
        if label:
            par = self.p(space_before=8, space_after=2, keep=True)
            self.rich(par, "**" + str(label) + "**")
        for es_par in self.lang_lines(blk, space_after=3):
            es_par.paragraph_format.keep_with_next = True
        if kind in ("tchart", "notice_wonder"):
            cols = blk.get("columns") or (["I notice", "I wonder"] if kind == "notice_wonder"
                                         else ["", ""])
            nrows = int(blk.get("rows", 4))
            t = self._table(rows=nrows + 1, cols=len(cols))
            for c, head in enumerate(cols):
                cell = t.rows[0].cells[c]
                _cell_borders(cell, "1B1F24", 10, sides=("bottom",)
                              + (("right",) if c < len(cols) - 1 else ()))
                self.rich(cell.paragraphs[0], "**" + str(head) + "**")
            for r in range(1, nrows + 1):
                _row_height(t.rows[r], self.S["line_gap"] / 72.0)
                for c in range(len(cols)):
                    _cell_borders(t.rows[r].cells[c], BOX_LINE, 6, sides=("bottom",)
                                  + (("right",) if c < len(cols) - 1 else ()))
        elif kind == "flow":
            steps = blk.get("steps") or ["", "", ""]
            t = self._table(rows=1, cols=len(steps) * 2 - 1)
            arrow_w = 0.32
            box_w = (8.5 - 2 * self.S["margin"] - arrow_w * (len(steps) - 1)) / len(steps)
            _widths(t, [box_w if c % 2 == 0 else arrow_w for c in range(len(steps) * 2 - 1)])
            for i, step in enumerate(steps):
                cell = t.rows[0].cells[i * 2]
                _cell_borders(cell, GRID, 4)
                if step:
                    self.run(cell.paragraphs[0], str(step), size=self.S["small"], bold=True)
                if i < len(steps) - 1:
                    arrow = t.rows[0].cells[i * 2 + 1]
                    _cell_borders(arrow, GRID, 4, sides=())
                    ap = arrow.paragraphs[0]
                    ap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    self.run(ap, "\u2192", size=self.S["h2"], color=MUTED)
                    el = OxmlElement("w:vAlign"); el.set(qn("w:val"), "center")
                    arrow._tc.get_or_add_tcPr().append(el)
            _row_height(t.rows[0], float(blk.get("height_in", 1.1)))
        elif kind == "cer":
            parts = [("Claim", "What I think"), ("Evidence", "What I saw or measured"),
                     ("Reasoning", "Why the evidence proves it")]
            stems = blk.get("stems") or {}
            t = self._table(rows=3, cols=2)
            _grid(t)
            _widths(t, [1.45, 8.5 - 2 * self.S["margin"] - 1.45])
            for r, (name, gloss) in enumerate(parts):
                head, body = t.rows[r].cells
                self.run(head.paragraphs[0], name, bold=True)
                gp = head.add_paragraph()
                self.run(gp, gloss, size=self.S["small"], color=MUTED)
                if stems.get(name.lower()):
                    self.stem_on_line(body, stems[name.lower()])
                _row_height(t.rows[r], float(blk.get("height_in", 0.85)))
        elif kind == "frayer":
            word = blk.get("word", "")
            cells = blk.get("cells") or ["What it means", "Draw it", "An example", "Not an example"]
            t = self._table(rows=2, cols=2)
            _grid(t)
            for i, name in enumerate(cells[:4]):
                cell = t.rows[i // 2].cells[i % 2]
                self.run(cell.paragraphs[0], str(name), size=self.S["small"], bold=True, color=MUTED)
            for row in t.rows:
                _row_height(row, float(blk.get("height_in", 1.25)))
            if word:
                # the word sits above the square, where the eye starts
                pass
        else:
            raise ValueError(f"unknown organizer kind: {kind!r}")
        _no_split(t)
        self.gap(6)

    # ------------------------------------------------------------ spanish coverage
    @staticmethod
    def _words(text):
        return len(re.sub(r"\*\*", "", str(text)).split())

    def _check_es_length(self, english, spanish, num, code="es"):
        """Abbreviated means shorter. Most languages run 15-20% longer than English for the
        same content, so only a real overshoot is worth reporting. Languages written
        without spaces between words can't be counted this way and are left to a human."""
        base = code.split("-")[0]
        if base in UNSPACED:
            return
        name = "Spanish" if code == "es" else f"'{code}'"
        if base in SYLLABIC:
            en = len(re.sub(r"\*\*", "", str(english)))
            es = len(re.sub(r"\*\*", "", str(spanish)))
            if en and es > en * 1.2:
                self._long_es.append(f"{num or '?'}: {es} {name} characters for {en} English")
            return
        en, es = self._words(english), self._words(spanish)
        if en and es > en * 1.2:
            self._long_es.append(f"{num or '?'}: {es} {name} words for {en} English")

    def report(self):
        if self.audience != "student":
            return
        for code, missing in self._missing_es.items():
            if not missing:
                continue
            name = "Spanish" if code == "es" else f"'{code}'"
            print(
                f"  note  no {name} line on question(s): "
                + ", ".join(str(m) for m in missing)
                + "\n        Every question a student answers carries one. See packet.md.",
                file=sys.stderr,
            )
        for msg in self._long_es:
            print(
                f"  note  language line longer than the English it supports — {msg}. "
                "Cut it to the task itself.",
                file=sys.stderr,
            )
        missing = [w for w in self.vocab if not self._vocab_hits.get(" ".join(w.lower().split()))]
        if self.vocab:
            print(f"  ok    key words used (each highlighted once per section): " + ", ".join(
                f"{w} ×{self._vocab_hits.get(' '.join(w.lower().split()), 0)}" for w in self.vocab),
                file=sys.stderr)
        if missing:
            print("  note  key word(s) never used on the page: " + ", ".join(missing)
                  + ". Use each one in a task, or take it off meta.vocab.", file=sys.stderr)
        idle = [w for w in self.vocab if w not in missing and not self._in_a_task(w)]
        if idle:
            print("  note  key word(s) defined but in no task: " + ", ".join(idle)
                  + ". A word students never use is a word they don't keep: put it in a "
                  "question, a stem, or a choice.", file=sys.stderr)
        for line in readability(self._read, self.vocab, self.reading_level):
            print(line, file=sys.stderr)


    # ------------------------------------------------------------ units
    # Google Docs, which is how these packets are printed, ignores "keep with next"
    # and lets a table break anywhere -- tested: a question and its writing lines,
    # built as a paragraph plus a table, split across pages in Docs every time. The
    # one thing Docs will not split is a single table row. So every task travels in
    # its own borderless one-row table: heading, question, language line, starter,
    # lines, and the table or organizer that answers it, as one piece.
    def begin_unit(self):
        t = self.doc.add_table(rows=1, cols=1)
        _widths(t, [8.5 - 2 * self.S["margin"]])
        cell = t.rows[0].cells[0]
        _cell_borders(cell, "FFFFFF", 0, sides=())
        tcPr = cell._tc.get_or_add_tcPr()
        mar = OxmlElement("w:tcMar")
        for side in ("top", "left", "bottom", "right"):
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:w"), "0")
            el.set(qn("w:type"), "dxa")
            mar.append(el)
        tcPr.append(mar)
        trPr = t.rows[0]._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        self.target = cell
        self._fresh = cell.paragraphs[0]
        return t

    def end_unit(self):
        # a cell must end in a paragraph; if the last thing in it is a table, the
        # trailing one is held to a point so it adds no line
        cell = self.target
        last = cell.paragraphs[-1]
        if not last.text.strip():
            pf = last.paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.line_spacing = Pt(1)
        self.target = self.doc
        self._fresh = None
        self.gap(4)

    @staticmethod
    def units(sections):
        """Group blocks into units that print as one piece: a heading, any lead-ins
        after it (a direction, a note, a word bank, the table a question reads from),
        the task they lead into, and everything the task is answered in (its lines,
        a starter after it, a box, a table or organizer). A question and its answer
        space are never two units, so no page break can ever fall between them."""
        lead = ("heading", "phase", "text", "paragraph", "labeled", "note", "callout",
                "wordbank", "list", "steps", "stem")
        answer = ("space", "fill_table", "organizer", "stem")
        out, unit = [], []
        i = 0
        while i < len(sections):
            b = sections[i]
            kind = b.get("type")
            if kind in ("page_break", "day"):
                if unit:
                    out.append(unit)
                    unit = []
                out.append([b])
                i += 1
                continue
            if kind in ("heading", "phase") and unit and \
                    any(u.get("type") not in ("heading", "phase") for u in unit):
                out.append(unit)   # a new section closes a unit still waiting for its task
                unit = []
            unit.append(b)
            i += 1
            nxt = sections[i].get("type") if i < len(sections) else None
            if kind in lead and nxt is not None:
                continue           # a lead-in waits for the task it introduces
            if kind == "table" and nxt == "question":
                continue           # the data a question reads stays above that question
            if kind == "question":
                spec = b.get("space")
                if isinstance(spec, dict) and spec.get("kind") == "none" and nxt == "table":
                    unit.append(sections[i])   # the table it is answered in
                    i += 1
                while i < len(sections) and sections[i].get("type") in answer:
                    unit.append(sections[i])   # lines, a starter, a box, an organizer
                    i += 1
            out.append(unit)
            unit = []
        if unit:
            out.append(unit)
        return out

    # ------------------------------------------------------------ dispatch
    def render(self):
        self.title_block()
        for unit in self.units(self.data.get("sections", [])):
            wrap = self.audience == "student" and any(
                b.get("type") in ("question", "table", "fill_table", "organizer", "heading",
                                  "phase", "space")
                for b in unit)
            if wrap:
                self.begin_unit()
            for blk in unit:
                self.block(blk)
            if wrap:
                self.end_unit()
        last = self.doc.paragraphs[-1] if self.doc.paragraphs else None
        if last is not None and not last.text.strip():
            last.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            last.paragraph_format.line_spacing = Pt(1)
            last.paragraph_format.space_after = Pt(0)
            last.paragraph_format.keep_with_next = False
        self.doc.save(self.out)
        self.report()

    def block(self, blk):
        kind = blk.get("type")
        if kind == "heading":
            self.heading(blk.get("text", ""), blk.get("minutes"), blk=blk)
        elif kind == "phase":
            self.heading(blk.get("name", ""), blk.get("minutes"), blk=blk)
        elif kind == "question":
            self.question(blk)
        elif kind in ("text", "paragraph"):
            self.begin_group()
            par = self.p(space_after=6)
            self.rich(par, blk.get("text", ""))
            self._read.append(("a direction", blk.get("text", "")))
            self.lang_lines(blk, space_after=6)
            self.end_group()
        elif kind == "labeled":
            self.begin_group()
            par = self.p(space_after=6)
            self.run(par, blk.get("label", "") + "  ", bold=True)
            self.rich(par, blk.get("text", ""))
            self._read.append((blk.get("label") or "a direction", blk.get("text", "")))
            self.lang_lines(blk, space_after=6)
            self.end_group()
        elif kind in ("list", "steps"):
            blk = dict(blk)
            if kind == "steps":
                blk["ordered"] = True
            self.listing(blk)
        elif kind == "table":
            self.table(blk)
        elif kind == "fill_table":
            self.table(blk)
        elif kind in ("note", "callout"):
            self.note(blk)
        elif kind == "stem":
            self.stem(blk.get("text", ""))
        elif kind == "wordbank":
            self.wordbank(blk)
        elif kind == "organizer":
            self.organizer(blk)
        elif kind == "space":
            self.space(blk)
        elif kind == "page_break":
            self.page_break()
        elif kind == "day":
            self.day(blk)
        elif kind == "spacer":
            self.p(space_after=int(blk.get("points", 12)))
        else:
            raise ValueError(f"unknown block type: {kind!r}")


ACCENT_HEX = "3E6DA8"


LEAD_INS = ("wordbank", "note", "callout", "text", "paragraph", "labeled", "stem", "table",
            "list", "steps")
ANSWERS = ("space", "fill_table", "organizer", "stem")


def reduce_packet(data):
    """The reduced packet, from the same lesson: the questions marked "core": false come
    out with their lead-ins and answer space, every question keeps only its first part,
    the type is large, and there is one word bank, on the front page under the "I can":
    the key words and every word the full packet banked, gathered in one place. A bank
    beside every question is a bank a student stops reading. In a multi-day packet each
    day is its own handout, so each day opens with its own.
    Question numbers stay as they are, so both packets match the slides."""
    d = copy.deepcopy(data)
    meta = d.setdefault("meta", {})
    meta["large_print"] = True
    langs = packet_languages(d)
    secs = d.get("sections", [])
    keep = [True] * len(secs)
    for i, b in enumerate(secs):
        if b.get("type") != "question" or b.get("core", True) is not False:
            continue
        keep[i] = False
        j = i + 1
        while j < len(secs) and secs[j].get("type") in ANSWERS:
            keep[j] = False
            j += 1
        j = i - 1
        while j >= 0 and secs[j].get("type") in LEAD_INS:
            keep[j] = False
            j -= 1

    def bank(words, banks):
        """One bank from the key words and the full packet's banks, words in order, no
        repeats; each language line joins the lines those banks carried."""
        items, seen = [], set()
        for w in list(words) + [x for bk in banks for x in bk.get("items", [])]:
            w = str(w).strip()
            if w and w.lower() not in seen:
                seen.add(w.lower())
                items.append(w)
        if not items:
            return None
        blk = {"type": "wordbank", "items": items[:10]}
        for code in langs:
            parts = []
            for bk in banks:
                for x in str(bk.get(code) or "").split(","):
                    if x.strip() and x.strip() not in parts:
                        parts.append(x.strip())
            if parts:
                blk[code] = ", ".join(parts)
        return blk

    # one bank per handout: the whole packet, or each day of a multi-day one (anything
    # before the first day rides with it)
    days = [i for i, b in enumerate(secs) if b.get("type") == "day"]
    starts = days or [0]
    ends = starts[1:] + [len(secs)]
    out = []
    for n, (start, end) in enumerate(zip(starts, ends)):
        lo = 0 if n == 0 else start
        stretch = list(zip(secs[lo:end], keep[lo:end]))
        words = [str(v) for v in (meta.get("vocab") or [])]
        if days:
            words += [str(v) for v in (secs[start].get("vocab") or [])]
        blk = bank(words, [b for b, _ in stretch if b.get("type") == "wordbank"])
        for b, k in stretch:
            if not k or b.get("type") == "wordbank":
                continue
            b = dict(b)
            if b.get("type") == "question" and b.get("parts"):
                b["parts"] = b["parts"][:1]
            if blk is not None and (not days or b.get("type") != "day"):
                out.append(blk)        # under the "I can", or under the day's own heading
                blk = None
            out.append(b)
        if blk is not None:
            out.append(blk)
    # a section whose every task came out loses its heading too
    d["sections"] = [b for i, b in enumerate(out)
                     if b.get("type") not in ("heading", "phase")
                     or (i + 1 < len(out) and out[i + 1].get("type") not in ("heading", "phase",
                                                                               "day", "page_break"))]
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("packet")
    ap.add_argument("out")
    ap.add_argument("--reduced", action="store_true",
                    help="core questions only, first parts only, large print, one word bank up front")
    args = ap.parse_args()
    with open(args.packet) as fh:
        data = json.load(fh)
    if args.reduced:
        data = reduce_packet(data)
    Renderer(data, args.out).render()
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
