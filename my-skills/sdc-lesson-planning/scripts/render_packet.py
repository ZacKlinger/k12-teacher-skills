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

Any block a student has to act on may carry an `"es"` string: one short Spanish line,
rendered under the English it supports. It is abbreviated support, not a translation --
see references/packet.md for what gets one and what deliberately does not. On a student
packet the renderer reports, on stderr, every question that has no Spanish line and every
Spanish line that ran longer than its English.

Requires python-docx. Install with: pip install python-docx --break-system-packages
"""

import json
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
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
    "margin": 0.7,
    "line_gap": 30,       # points between writing lines — sized for teen handwriting
    "space_after": 8,
}

TEACHER = {
    "font": "Calibri",
    "body": 11,
    "h1": 16,
    "h2": 12.5,
    "small": 9.5,
    "margin": 0.75,
    "line_gap": 24,
    "space_after": 6,
}

INK = RGBColor(0x1B, 0x1F, 0x24)
MUTED = RGBColor(0x69, 0x70, 0x79)
# The Spanish line is secondary to the English but it is not fine print: the students
# reading it are the ones with the least margin. Darker than MUTED, lighter than INK.
ES_INK = RGBColor(0x4A, 0x51, 0x59)
ACCENT = RGBColor(0x3E, 0x6D, 0xA8)
RULE = "E4E7EB"
FILL = "F3F6FA"
BOX_LINE = "9AA2AC"


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
    """Rows stay whole; the table does not break across pages where avoidable."""
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        el = OxmlElement("w:cantSplit")
        trPr.append(el)


def _row_height(row, inches):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:trHeight")
    el.set(qn("w:val"), str(int(inches * 1440)))
    el.set(qn("w:hRule"), "atLeast")
    trPr.append(el)


class Renderer:
    def __init__(self, data, out_path):
        self.data = data
        self.out = out_path
        self.audience = data.get("audience", "student")
        self.S = STUDENT if self.audience == "student" else TEACHER
        self.doc = Document()
        self._setup()
        # every paragraph the renderer emits is registered here so a task group can be
        # bound together after the fact
        self._group = None
        # Spanish coverage, reported on stderr once the document is written
        self._es = []
        self._missing_es = []
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
        bits = [b for b in (meta.get("course"), meta.get("day"), meta.get("title")) if b]
        run = foot.add_run("  ·  ".join(bits))
        run.font.size = Pt(self.S["small"] - 1)
        run.font.color.rgb = MUTED
        run.font.name = self.S["font"]
        foot.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ------------------------------------------------------------ text primitives
    def p(self, text="", size=None, bold=False, italic=False, color=None,
          space_after=None, space_before=None, indent=0, keep=False, align=None):
        par = self.doc.add_paragraph()
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

    def run(self, par, text, size=None, bold=False, italic=False, color=None):
        r = par.add_run(text)
        r.font.name = self.S["font"]
        r.font.size = Pt(size or self.S["body"])
        r.bold = bold
        r.italic = italic
        r.font.color.rgb = color or INK
        return r

    def es_line(self, text, indent=0, space_after=4):
        """The Spanish support line — one line, under the English it supports.

        Not italic. Italic costs a striving reader real speed, and this line is read
        by the students who have the least of it to spare; the separation from the
        English comes from size and colour instead.
        """
        if not text:
            return None
        self._es.append(str(text))
        par = self.p(space_after=space_after, space_before=0, indent=indent)
        self.rich(par, str(text), size=self.S["small"])
        for r in par.runs:
            r.font.color.rgb = ES_INK
        return par

    def es_in_cell(self, cell, text):
        """Same line, but inside a tinted box (a note, a word bank) so it stays in it."""
        if not text:
            return None
        self._es.append(str(text))
        par = cell.add_paragraph()
        par.paragraph_format.space_before = Pt(2)
        par.paragraph_format.space_after = Pt(0)
        self.rich(par, str(text), size=self.S["small"])
        for r in par.runs:
            r.font.color.rgb = ES_INK
        return par

    def rich(self, par, text, size=None):
        """Renders **bold** spans inside a plain string. Everything else is literal."""
        for i, chunk in enumerate(text.split("**")):
            if chunk:
                self.run(par, chunk, size=size, bold=(i % 2 == 1))

    # ------------------------------------------------------------ group binding
    def begin_group(self):
        self._group = []

    def end_group(self):
        """Bind everything emitted since begin_group so a page break can't split it."""
        if not self._group:
            self._group = None
            return
        for par in self._group[:-1]:
            par.paragraph_format.keep_with_next = True
        self._group = None

    # ------------------------------------------------------------ blocks
    def heading(self, text, minutes=None, es=None):
        par = self.p(space_before=14, space_after=4, keep=True)
        self.run(par, text.upper(), size=self.S["h2"], bold=True)
        if minutes:
            self.run(par, f"   {minutes} min", size=self.S["small"], color=ACCENT, bold=True)
        _para_border(par, "bottom", RULE, 8)
        if es:
            # the Spanish line belongs to the heading, so it has to hold onto what
            # follows too -- otherwise a break lands between it and the first task
            # and the page ends on a heading alone
            es_par = self.es_line(es, space_after=2)
            if es_par is not None:
                es_par.paragraph_format.keep_with_next = True
            par.paragraph_format.keep_with_next = True
        return par

    def title_block(self):
        meta = self.data.get("meta", {})
        eyebrow = "  ·  ".join(
            b for b in (meta.get("course"), meta.get("day"), meta.get("period")) if b
        )
        if eyebrow:
            par = self.p(space_after=2, keep=True)
            self.run(par, eyebrow.upper(), size=self.S["small"], color=MUTED, bold=True)
        par = self.p(space_after=6, keep=True)
        self.run(par, meta.get("title", ""), size=self.S["h1"], bold=True)

        if self.audience == "student" and meta.get("name_line", True):
            t = self.doc.add_table(rows=1, cols=2)
            t.autofit = True
            for cell, label in zip(t.rows[0].cells, ("Name:", "Date:")):
                cell.text = ""
                par = cell.paragraphs[0]
                self.run(par, label, size=self.S["small"], color=MUTED)
                par.paragraph_format.space_after = Pt(2)
                _cell_borders(cell, RULE, 6, sides=("bottom",))
            _no_split(t)
            self.p(space_after=4)

        obj = self.data.get("objective")
        if obj:
            self._banner("Objective", obj, self.data.get("standard"))
        # The agenda belongs on the board and in the deck, not on the student's page —
        # printing it there costs a third of page 1 and students read it off the screen
        # anyway. The lesson plan always prints it.
        agenda = self.data.get("agenda")
        if agenda and (self.audience == "teacher" or meta.get("show_agenda")):
            self.agenda(agenda)

    def _banner(self, label, text, sub=None):
        t = self.doc.add_table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _shade(cell, FILL)
        _cell_borders(cell, ACCENT_HEX, 12, sides=("left",))
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        self.run(par, label.upper() + "  ", size=self.S["small"], bold=True, color=ACCENT)
        self.run(par, text, size=self.S["body"])
        if sub:
            p2 = cell.add_paragraph()
            p2.paragraph_format.space_before = Pt(2)
            p2.paragraph_format.space_after = Pt(0)
            self.run(p2, sub, size=self.S["small"], color=MUTED, italic=True)
        _no_split(t)
        self.p(space_after=2)

    def agenda(self, items):
        par = self.p(space_before=8, space_after=3, keep=True)
        self.run(par, "TODAY", size=self.S["small"], bold=True, color=MUTED)
        rows = []
        for it in items:
            if isinstance(it, (list, tuple)):
                rows.append((str(it[0]), f"{it[1]} min" if len(it) > 1 else ""))
            else:
                rows.append((str(it), ""))
        t = self.doc.add_table(rows=len(rows), cols=2)
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
        self.p(space_after=4)

    def question(self, blk):
        self.begin_group()
        num = str(blk.get("number", "")).strip()
        par = self.p(space_before=12, space_after=4)
        if num:
            self.run(par, f"{num}. ", bold=True)
        self.rich(par, blk.get("prompt", ""))
        if blk.get("minutes"):
            self.run(par, f"   ({blk['minutes']} min)", size=self.S["small"], color=MUTED)

        if blk.get("es"):
            self.es_line(blk["es"])
            self._check_es_length(blk.get("prompt", ""), blk["es"], num)
        elif self.audience == "student":
            self._missing_es.append(num or blk.get("prompt", "")[:40])

        if blk.get("example"):
            self.tinted("Example", blk["example"])
        if blk.get("hint"):
            self.tinted("Hint", blk["hint"])
        for stem in blk.get("stems", []) or []:
            self.stem(stem)
        for sub in blk.get("parts", []) or []:
            par = self.p(space_after=3, indent=0.3)
            self.rich(par, sub)
        self.space(blk.get("space", {"kind": "lines", "count": 3}))
        self.end_group()

    def stem(self, text):
        t = self.doc.add_table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _shade(cell, FILL)
        _cell_borders(cell, RULE, 6, sides=("left",), style="single")
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

    def space(self, spec):
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
            t = self.doc.add_table(rows=count, cols=1)
            for row in t.rows:
                cell = row.cells[0]
                _cell_borders(cell, BOX_LINE, 6, sides=("bottom",))
                par = cell.paragraphs[0]
                par.paragraph_format.space_before = Pt(0)
                par.paragraph_format.space_after = Pt(0)
                _row_height(row, self.S["line_gap"] / 72.0)
            _no_split(t)
            self.p(space_after=6)
            return
        # box / work space
        height = float(spec.get("height_in", 2.0)) if isinstance(spec, dict) else 2.0
        label = spec.get("label") if isinstance(spec, dict) else None
        t = self.doc.add_table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _cell_borders(cell, BOX_LINE, 6)
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        if label:
            self.run(par, label, size=self.S["small"], color=MUTED)
        _row_height(t.rows[0], height)
        _no_split(t)
        self.p(space_after=4)

    def table(self, blk, fill_rows=0, row_height=None):
        headers = blk.get("headers") or []
        rows = [list(r) for r in (blk.get("rows") or [])]
        blanks = int(blk.get("blank_rows", fill_rows) or 0)
        ncols = len(headers) or (len(rows[0]) if rows else 2)
        total = len(rows) + blanks + (1 if headers else 0)
        if total == 0:
            return
        t = self.doc.add_table(rows=total, cols=ncols)
        t.style = "Table Grid"
        idx = 0
        if headers:
            for c, head in enumerate(headers):
                cell = t.rows[0].cells[c]
                _shade(cell, FILL)
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
        h = float(row_height or blk.get("row_height_in", 0.45))
        for r in range(len(rows) + (1 if headers else 0), total):
            _row_height(t.rows[r], h)
        _no_split(t)
        self.p(space_after=6)

    def note(self, blk):
        t = self.doc.add_table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _shade(cell, FILL)
        _cell_borders(cell, ACCENT_HEX, 12, sides=("left",))
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        label = blk.get("label")
        if label:
            self.run(par, label.upper() + "  ", size=self.S["small"], bold=True, color=ACCENT)
        self.rich(par, blk.get("text", ""))
        self.es_in_cell(cell, blk.get("es"))
        _no_split(t)
        self.p(space_after=4)

    def listing(self, blk):
        self.begin_group()
        if blk.get("label"):
            par = self.p(space_before=8, space_after=3)
            self.run(par, blk["label"], bold=True)
        self.es_line(blk.get("es"), space_after=5)
        ordered = blk.get("ordered", False)
        for i, item in enumerate(blk.get("items", []), 1):
            par = self.p(space_after=4, indent=0.25)
            marker = f"{i}. " if ordered else "•  "
            self.run(par, marker, bold=ordered)
            self.rich(par, str(item))
        self.end_group()

    def wordbank(self, blk):
        t = self.doc.add_table(rows=1, cols=1)
        cell = t.rows[0].cells[0]
        _shade(cell, FILL)
        _cell_borders(cell, BOX_LINE, 6)
        par = cell.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        self.run(par, (blk.get("label") or "Word bank").upper() + "  ",
                 size=self.S["small"], bold=True, color=ACCENT)
        self.run(par, "     ".join(str(i) for i in blk.get("items", [])))
        self.es_in_cell(cell, blk.get("es"))
        _no_split(t)
        self.p(space_after=4)

    # ------------------------------------------------------------ spanish coverage
    @staticmethod
    def _words(text):
        return len(re.sub(r"\*\*", "", str(text)).split())

    def _check_es_length(self, english, spanish, num):
        """Abbreviated means shorter. Spanish runs 15-20% longer than English for the
        same content, so only a real overshoot is worth reporting."""
        en, es = self._words(english), self._words(spanish)
        if en and es > en * 1.2:
            self._long_es.append(f"{num or '?'}: {es} Spanish words for {en} English")

    def report(self):
        if self.audience != "student":
            return
        if self._missing_es:
            print(
                "  note  no Spanish line on question(s): "
                + ", ".join(str(m) for m in self._missing_es)
                + "\n        Every question a student answers carries one. See packet.md.",
                file=sys.stderr,
            )
        for msg in self._long_es:
            print(
                f"  note  Spanish longer than the English it supports — {msg}. "
                "Cut it to the task itself.",
                file=sys.stderr,
            )

    # ------------------------------------------------------------ dispatch
    def render(self):
        self.title_block()
        for blk in self.data.get("sections", []):
            kind = blk.get("type")
            if kind == "heading":
                self.heading(blk.get("text", ""), blk.get("minutes"), blk.get("es"))
            elif kind == "phase":
                self.heading(blk.get("name", ""), blk.get("minutes"), blk.get("es"))
            elif kind == "question":
                self.question(blk)
            elif kind in ("text", "paragraph"):
                self.begin_group()
                par = self.p(space_after=6)
                self.rich(par, blk.get("text", ""))
                self.es_line(blk.get("es"), space_after=6)
                self.end_group()
            elif kind == "labeled":
                self.begin_group()
                par = self.p(space_after=6)
                self.run(par, blk.get("label", "") + "  ", bold=True)
                self.rich(par, blk.get("text", ""))
                self.es_line(blk.get("es"), space_after=6)
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
            elif kind == "space":
                self.space(blk)
            elif kind == "page_break":
                self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            elif kind == "spacer":
                self.p(space_after=int(blk.get("points", 12)))
            else:
                raise ValueError(f"unknown block type: {kind!r}")
        self.doc.save(self.out)
        self.report()


ACCENT_HEX = "3E6DA8"


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1]) as fh:
        data = json.load(fh)
    Renderer(data, sys.argv[2]).render()
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
