#!/usr/bin/env python3
"""Check a finished deck against the rules in references/deck.md and
references/photographs.md.

    python3 scripts/check_deck.py <deck.html> --minutes 60

Why this exists: every rule in here was, at some point, a sentence in the skill
that a build quietly skipped -- decks shipped with zero photographs, with the
fallback script missing, with the same photo used twice, with template
placeholder text still in place. Prose asks; a script checks. Run it before the
deck goes anywhere near a classroom, fix what it reports, run it again.

Exit code 0 = clean (warnings allowed), 1 = at least one error.
"""

from __future__ import annotations

import argparse
import itertools
import math
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_packet import load_packet  # noqa: E402  (packet.json, or the packet .docx itself)

# --------------------------------------------------------------------------
# Placeholder strings that ship in assets/deck_template.html. If any survive
# into a real deck, that part of the template was never filled in.
# --------------------------------------------------------------------------
PLACEHOLDERS = [
    "REPLACE_FILE_NAME",
    "VIDEO_ID",
    "LESSON TITLE",
    "STANDARD CODE",
    "The question this lesson answers.",
    "The headline, six to twelve words",
    "One line naming the input.",
    "The do-now question, readable from the back row.",
    "The finding, stated as the headline.",
    "The words above it are its caption.",
    "One question, big enough to fill the screen.",
    "The claim this photograph proves",
    "A full sentence describing",
    "What to notice — not what the thing is.",
    "What to look for in this one",
    "What students meet in the first block",
    "La pregunta en español",
    "La instrucción en español",
    "La misma pregunta, en español.",
    "Adivina primero. Después miramos.",
]

FILENAMEISH = re.compile(r"^[\w\-. %]+\.(jpg|jpeg|png|gif|webp|tif|tiff|svg)$", re.I)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warns: list[str] = []
        self.notes: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


def slides(html: str) -> list[tuple[str, str]]:
    """Return (attributes, inner html) for each slide, in order."""
    pat = r'<section class="slide([^"]*)"([^>]*)>(.*?)</section>'
    return [
        (m.group(1) + " " + m.group(2), m.group(3))
        for m in re.finditer(pat, html, re.S)
    ]


def attr(blob: str, name: str) -> str | None:
    """An attribute's value, double- or single-quoted; data-x never matches the end of
    a longer name."""
    m = re.search(rf"(?<![\w-]){re.escape(name)}\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s\"'=<>`]+))", blob)
    if not m:
        return None
    return next(g for g in m.groups() if g is not None)


def imgs(html: str) -> list[str]:
    return re.findall(r"<img\b[^>]*>", html, re.I)


def is_poster(tag: str) -> bool:
    """A video's thumbnail is not a photograph.

    It has its own failure story (see the facade in the template), it does not
    count toward the photo floor, and asking it for a caption saying what to
    notice makes no sense -- the video says it.
    """
    return "img.youtube.com" in (attr(tag, "src") or "")


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------


def body_of(slide_html: str) -> str:
    """Inner HTML of a slide's .body, counting <div> nesting.

    A plain non-greedy regex stops at the first </div>, which for any slide with
    cards or a flow is the *inner* one -- that made every structured slide look
    empty. Count instead.
    """
    m = re.search(r'<div class="body[^"]*"[^>]*>', slide_html)
    if not m:
        return ""
    i = m.end()
    depth = 1
    for tag in re.finditer(r"<(/?)div\b[^>]*>", slide_html[i:]):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            return slide_html[i : i + tag.start()]
    return slide_html[i:]


def check_structure(html: str, sl: list, minutes: int, rep: Report) -> None:
    n = len(sl)
    if n == 0:
        rep.error("No slides found. Did the file get written from the template?")
        return

    # roughly one slide per 2-3 minutes
    lo, hi = int(minutes / 4.5), int(minutes / 3)
    if n < lo:
        rep.error(
            f"{n} slides for a {minutes}-minute period. Expected about {lo}-{hi}. "
            "Too few slides means each one is carrying more than a student who "
            "reads slowly can take in at once -- segment them."
        )
    elif n > hi:
        rep.warn(f"{n} slides for {minutes} minutes -- more than the usual {lo}-{hi}.")
    else:
        rep.note(f"{n} slides for a {minutes}-minute period (expected {lo}-{hi}).")

    for i, (a, body_html) in enumerate(sl, 1):
        title = attr(a, "data-title") or f"slide {i}"
        if not attr(a, "data-title"):
            rep.warn(f"Slide {i}: no data-title, so it has no entry in the jump menu.")
        if not attr(a, "data-day"):
            rep.warn(f"Slide {i} ({title}): no data-day.")

        inner = re.sub(r"<[^>]+>", "", body_of(body_html)).strip()
        is_dark = "dark" in a.split(">")[0]
        # charts and the talk kit draw themselves when the deck opens, so an
        # empty-looking div with one of these classes is content, not a hole
        has_media = bool(re.search(r'<img|<iframe|<svg|dv-', body_html)) or \
            has_class(body_html, ["vote", "picker", "heard"] + COMPONENTS)
        if not inner and not has_media and not is_dark:
            rep.error(
                f"Slide {i} ({title}): the body is empty. A headline alone is not a "
                "slide -- only the dark checkpoint is allowed to be bare."
            )


def check_minutes(sl: list, minutes: int, rep: Report) -> None:
    """The minutes on the slides are the plan's agenda seen from the front of the room. A
    cover that names the whole period doesn't count toward it."""
    total, counted = 0.0, 0
    for a, _ in sl:
        m = re.match(r"\s*(\d+(?:\.\d+)?)\s*min", attr(a, "data-mins") or "")
        if not m or float(m.group(1)) >= minutes:
            continue
        total += float(m.group(1))
        counted += 1
    if counted and abs(total - minutes) > max(2, minutes * 0.05):
        rep.warn(f"The slides' minutes add up to {total:g}; the period is {minutes}. "
                 "Make each slide's data-mins match the plan's agenda, so the clock on the "
                 "wall and the plan in hand tell the same story.")
    elif counted:
        rep.note(f"Slide minutes add up to {total:g} of {minutes}.")


def check_photos(html: str, sl: list, minutes: int, rep: Report) -> None:
    all_imgs = [t for t in imgs(html) if not is_poster(t)]
    floor = 5 if minutes <= 70 else 8
    ceil = 8 if minutes <= 70 else 12

    if len(all_imgs) < floor:
        rep.error(
            f"{len(all_imgs)} photographs; a {minutes}-minute period needs {floor}-{ceil}. "
            "A student who reads slowly, or has never seen the thing, "
            "cannot picture it from the word."
        )
    elif len(all_imgs) > ceil:
        rep.warn(f"{len(all_imgs)} photographs -- more than the usual {floor}-{ceil}.")
    else:
        rep.note(f"{len(all_imgs)} photographs (expected {floor}-{ceil}).")

    # base64 inlining: deck.md used to say "single file, no external assets",
    # which pushed builds into inlining every photo and producing 2 MB decks.
    if "data:image" in html:
        rep.error(
            "Photographs are base64-inlined. Link them by URL instead -- inlining "
            "produced a 1.9 MB deck that is slow to open in front of a class."
        )

    local = [attr(t, "src") or "" for t in all_imgs
             if not re.match(r"(https?:)?//", attr(t, "src") or "") and not (attr(t, "src") or "").startswith("data:")]
    if local:
        rep.warn(f"{len(local)} photograph(s) point at a local file ({local[0][:50]}). The deck is opened "
                 "on another computer, where that file is not; link each photo by its URL.")

    for t in all_imgs:
        src = attr(t, "src") or ""
        alt = attr(t, "alt")
        short = (src[:70] + "...") if len(src) > 70 else src

        if alt is None or not alt.strip():
            rep.error(f"<img> with no alt text: {short}")
        elif FILENAMEISH.match(alt.strip()):
            rep.error(f"alt text is a filename, not a sentence: {alt!r}")
        elif len(alt.split()) < 5:
            rep.warn(
                f"alt text is only {len(alt.split())} words: {alt!r}. It becomes the "
                "visible text when an image is blocked -- write a real sentence."
            )

        if "upload.wikimedia.org" in src and "/thumb/" in src:
            rep.error(
                f"Hand-assembled Wikimedia thumb URL (contains an unguessable hash, "
                f"404s every time): {short}. Use Special:FilePath instead."
            )
        if "commons.wikimedia.org" in src and "Special:FilePath" not in src:
            rep.warn(f"Commons URL that is not a Special:FilePath redirect: {short}")

        for bad in ("google.com/imgres", "gstatic.com", "pinterest.", "shutterstock",
                    "gettyimages", "istockphoto", "alamy"):
            if bad in src:
                rep.error(f"Photo from a blocked/unstable source ({bad}): {short}")

    # duplicates -- the same photo twice means it was picked for the topic, not
    # for the specific claim the slide is making.
    # Count each photo once per slide. The same file twice on ONE slide is a
    # deliberate comparison -- the crop demonstration, before-and-after, the same
    # scene under two conditions. The failure this catches is the same photo
    # reappearing on a DIFFERENT slide, which means a brief was just "show the
    # topic" and any picture of the topic would have done.
    per_slide = Counter()
    for a, body in sl:
        for src in {attr(t, "src") or "" for t in imgs(body) if not is_poster(t)}:
            if src:
                per_slide[src] += 1
    dupes = {s_: c for s_, c in per_slide.items() if c > 1}
    if dupes:
        rep.error(
            f"{len(dupes)} photograph(s) reused across different slides. Each photo "
            "should prove a different claim -- a repeat means at least one brief was "
            "just 'show the topic'. First: " + list(dupes)[0][:60]
        )

    # crop aiming
    for block, label in ((r'<div class="pgrid".*?</div>\s*</div>', "pgrid"),
                         (r'<div class="vc shot".*?</div>', "vocab shot")):
        for m in re.finditer(block, html, re.S):
            chunk = m.group(0)
            for fig in re.finditer(r"<figure[^>]*>.*?</figure>|<div class=\"vc shot\"[^>]*>.*?</div>",
                                   chunk, re.S):
                if "<img" in fig.group(0) and "--focus" not in fig.group(0):
                    rep.warn(
                        f"A cropped {label} photo has no --focus set, so it centre-crops "
                        "at 50%/50% -- which is what cuts subjects in half."
                    )

    # Captions and credits, checked without assuming a markup shape. A real build
    # invented <div class="photo"><img><div class="credit"> and shipped ten
    # photographs with zero captions, so looking only inside <figure> misses it.
    for m in re.finditer(r"<img\b[^>]*>", html, re.I):
        if is_poster(m.group(0)):
            continue
        window = html[m.start() : m.start() + 900]
        window = window[: window.find("</section>") if "</section>" in window else len(window)]
        has_caption = bool(re.search(r"<figcaption|class=\"cap\b", window))
        src = (attr(m.group(0), "src") or "")[:60]
        if not has_caption:
            rep.error(
                "A photograph has no caption. The caption says what to notice -- "
                f"without it the photo is decoration: {src}"
            )

    # Credit is checked per slide, not per photo: one line covering a grid of
    # four is adequate attribution and far less noisy than four stacked credits.
    for i, (a, body) in enumerate(sl, 1):
        body_photos = [t for t in imgs(body) if not is_poster(t)]
        if body_photos and not re.search(r'class="cred\b|class="credit\b', body):
            rep.warn(
                f"Slide {i} ({attr(a, 'data-title') or i}) has photographs but no "
                "credit line. Commons images need attribution."
            )


ES_CLASS = re.compile(r'class="[^"]*\bes\b[^"]*"')
# text elements in document order, so a language line can be measured against the
# English line immediately above it
TEXT_EL = re.compile(r'<(h1|h2|p|div)\b([^>]*)>(.*?)</\1>', re.S | re.I)


def text_of(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


UNSPACED = {"zh", "ja", "ko", "th", "my", "km", "lo"}
# a space between syllables, not words: measured in characters, not words
SYLLABIC = {"vi"}


def check_language_access(html: str, sl: list, rep: Report, langs=()) -> None:
    """When the class has home languages, every question and every direction carries a
    line in each of them.

    Reading is the barrier twice over for a newcomer, and a slide is the one surface a
    student cannot ask a neighbour to re-read for them. The line is abbreviated on
    purpose -- the task, not the framing -- so this checks that it is *there* and that
    it stayed short, and leaves whether it is good Spanish, Vietnamese or Arabic to a
    human. A line is `<p class="es" lang="vi">`: the class marks a language line (its
    name is historical), the lang names the language, and a line with no lang is
    Spanish. With no languages listed there is nothing to check.
    """
    total = len(ES_CLASS.findall(html))
    if not langs:
        if total:
            rep.warn(f"{total} language line(s) in the deck, but no home languages were given. "
                     "Pass --languages (or a packet that lists them) so they are checked.")
        else:
            rep.note("No home languages listed for this class; no language lines expected.")
        return
    rep.note(f"{total} language support line(s).")

    for code in langs:
        tagged = re.compile(r'<[^>]*\bclass="[^"]*\bes\b[^"]*"[^>]*\blang="' + re.escape(code)
                            + r'(-[^"]*)?"|<[^>]*\blang="' + re.escape(code)
                            + r'(-[^"]*)?"[^>]*\bclass="[^"]*\bes\b')
        n = len(tagged.findall(html))
        if code == "es":
            # a line with no lang attribute is Spanish
            n += len(re.findall(r'<[^>]*\bclass="[^"]*\bes\b[^"]*"(?![^>]*\blang=)[^>]*>', html))
        if n == 0:
            rep.error(
                f"No '{code}' lines in the deck, but the class's languages include it. Each "
                f'question and direction carries one as <p class="es" lang="{code}">. See the '
                '"Language access" section of references/deck.md.'
            )
        else:
            rep.note(f"{n} '{code}' support line(s).")

    es_next = re.compile(r'\s*<(p|div)\b[^>]*\bclass="[^"]*\bes\b', re.I)
    for i, (a, body) in enumerate(sl, 1):
        title = attr(a, "data-title") or f"slide {i}"
        has_es = bool(ES_CLASS.search(body))
        game = any(set(classes(t)) & set(COMPONENTS) or ("pinned" in classes(t) and re.search(r"\sdata-quiz\b", t))
                   for _, t, _ in tags(body))

        # each question and each direction has its own line straight under it: the
        # headline when it asks something or runs a game, every .instruct, every word cell
        missing = []
        m = re.search(r"<(h1|h2)\b[^>]*>(.*?)</\1>", body, re.S | re.I)
        if m and ("?" in text_of(m.group(2)) or game) and not es_next.match(body, m.end()):
            missing.append("the headline")
        for im in re.finditer(r'<p\b[^>]*class="[^"]*\binstruct\b[^"]*"[^>]*>.*?</p>', body, re.S | re.I):
            if not es_next.match(body, im.end()):
                missing.append(f"the direction \"{text_of(im.group(0))[:40]}\"")
        for _, t, start in tags(body):
            c = classes(t)
            if "vc" in c and "word" in c and not ES_CLASS.search(block(body, start)):
                missing.append("the word cell")
        if missing:
            rep.warn(f"Slide {i} ({title}): no language line under {', '.join(dict.fromkeys(missing))}. "
                     "Each question and direction carries its own, straight under it.")
        elif not has_es and attr(a, "data-packet"):
            rep.warn(
                f"Slide {i} ({title}) sends students to the packet but carries no language line. "
                "If the slide only points at a page, that is fine -- say so and move on."
            )

        # Abbreviated means shorter. Most languages run 15-20% longer than English for
        # the same content, so only a real overshoot means the framing got translated too.
        prev = ""
        for el in TEXT_EL.finditer(body):
            cls = set((attr(el.group(2), "class") or "").split())
            body_text = text_of(el.group(3))
            if not body_text:
                continue
            if "es" in cls:
                code = (attr(el.group(2), "lang") or "es").split("-")[0]
                if code in UNSPACED:
                    continue
                if code in SYLLABIC:
                    if prev and len(body_text) > len(prev) * 1.2:
                        rep.warn(
                            f"Slide {i} ({title}): the '{code}' line is longer than the English "
                            f"above it ({len(body_text)} characters to {len(prev)}). It carries the "
                            "task, not the framing -- cut it back."
                        )
                    continue
                if prev and len(body_text.split()) > len(prev.split()) * 1.2:
                    rep.warn(
                        f"Slide {i} ({title}): the language line is longer than the English "
                        f"above it ({len(body_text.split())} words to {len(prev.split())}). "
                        "It carries the task, not the framing -- cut it back."
                    )
            elif el.group(1).lower() in ("h1", "h2") or "instruct" in cls:
                prev = body_text


# Every game and interactive the template builds. A slide carrying one has content
# even when its markup looks empty, and one of them on a timed slide is run as talk.
GAMES = ["game", "sort", "hinge", "order", "line", "estimate", "wodb", "mistake", "tf", "match", "whatif"]
COMPONENTS = GAMES + ["zoomin"]
NAMES = {"game": "a game round", "sort": "a sort", "hinge": "a hinge question", "order": "an order-it",
         "line": "a number line", "estimate": "an estimate", "wodb": "a which-one-doesn't-belong",
         "mistake": "a find-the-mistake", "tf": "a true-or-false", "match": "a match", "whatif": "a what-if",
         "zoomin": "a zoom-in", "quiz": "a label-the-photo"}
LETTERS = "ABCDEF"
VOID = {"img", "br", "hr", "input", "source", "wbr", "meta", "link"}
# An opening tag, read the way a browser reads it: a ">" or quotes inside a quoted
# attribute value ("x > 3") do not end the tag.
ATTRS = r"""(?:\s+[^\s=>/"']+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>"']+))?)*"""
TAG = re.compile(r"<([A-Za-z][\w-]*)(" + ATTRS + r")\s*/?>")


def tags(html: str):
    """Every opening tag in html, with its name (lower case), the whole tag, and where it starts."""
    for m in TAG.finditer(html):
        yield m.group(1).lower(), m.group(0), m.start()


def classes(tag: str) -> list[str]:
    return (attr(tag, "class") or "").split()


def has_class(html: str, names) -> bool:
    names = set(names)
    return any(names & set(classes(t)) for _, t, _ in tags(html))


def has_line(html: str, code: str) -> bool:
    """Whether html carries a language line in `code` (a bare .es line is Spanish)."""
    for _, t, _ in tags(html):
        if "es" in classes(t) and (attr(t, "lang") or "es").split("-")[0] == code:
            return True
    return False


def block(html: str, start: int) -> str:
    """The whole element that opens at `start`, counting nesting of its own tag, so a
    component's children come with it however deep they go."""
    m = TAG.match(html, start)
    if not m:
        return ""
    name = m.group(1)
    if name.lower() in VOID or m.group(0).endswith("/>"):
        return m.group(0)
    depth = 0
    for t in re.finditer(rf"<{name}\b{ATTRS}\s*/?>|</{name}\s*>", html[start:], re.I):
        depth += -1 if t.group(0).startswith("</") else 1
        if depth == 0:
            return html[start : start + t.end()]
    return html[start:]


def head(el: str) -> str:
    """An element's own opening tag."""
    m = TAG.match(el)
    return m.group(0) if m else ""


def children(el: str) -> list[str]:
    """The direct child elements of an element's html, in order. Text between them,
    including a '<' that is only maths ("0.25<0.3"), is skipped."""
    h = head(el)
    if not h or not el.rstrip().endswith(">") or h == el:
        return []
    inner = el[len(h) : el.rindex("</")] if "</" in el else ""
    out, i = [], 0
    while True:
        m = TAG.search(inner, i)
        if not m:
            return out
        c = block(inner, m.start())
        if c:
            out.append(c)
        i = m.start() + max(len(c), len(m.group(0)))


def words(html: str) -> int:
    return len(text_of(re.sub(r'<p\b[^>]*class="es[^"]*"[^>]*>.*?</p>', " ", html, flags=re.S)).split())


def value(s) -> float:
    """A number as an author writes it on a card or a tick: 0.75, 75, or 3/4."""
    s = str(s).strip()
    m = re.fullmatch(r"(-?\d*\.?\d+)\s*/\s*(\d*\.?\d+)", s)
    return float(m.group(1)) / float(m.group(2)) if m else float(s)


def numbers(*vals) -> bool:
    try:
        [value(v) for v in vals]
        return True
    except (TypeError, ValueError, ZeroDivisionError):
        return False


def js_round(x: float, d: float = 0) -> float:
    k = 10 ** d
    return math.floor(x * k + 0.5) / k


FORMULA_TOKEN = re.compile(r"\d*\.?\d+(?:[eE][+-]?\d+)?|\*\*|[A-Za-z_]+|\S")
FORMULA_FN = {"round": js_round, "floor": math.floor, "ceil": math.ceil,
              "min": lambda *x: min(x), "max": lambda *x: max(x),
              "abs": abs, "sqrt": math.sqrt, "pow": math.pow}


def compile_formula(src: str):
    """The what-if formula, parsed exactly the way the deck parses it: the same tokens,
    the same grammar, the same functions (compile() in assets/deck_template.html). So a
    formula this passes is one the slide runs, and one it refuses is one the slide would
    show as "This model needs fixing". Returns a function of [a, b, c]."""
    toks, pos = FORMULA_TOKEN.findall(src or ""), [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        t = peek()
        pos[0] += 1
        return t

    def need(t):
        if peek() != t:
            raise ValueError(f'it needs "{t}" near "{peek() or "the end"}"')
        pos[0] += 1

    def binop(f, op, g):
        return {"+": lambda v: f(v) + g(v), "-": lambda v: f(v) - g(v), "*": lambda v: f(v) * g(v),
                "/": lambda v: f(v) / g(v), "%": lambda v: math.fmod(f(v), g(v)),
                "^": lambda v: math.pow(f(v), g(v))}[op]

    def total():
        f = product()
        while peek() in ("+", "-"):
            op = take()
            f = binop(f, op, product())
        return f

    def product():
        f = unary()
        while peek() in ("*", "/", "%"):
            op = take()
            f = binop(f, op, unary())
        return f

    def unary():
        if peek() == "-":
            take()
            g = unary()
            return lambda v: -g(v)
        if peek() == "+":
            take()
            return unary()
        return power()

    def power():                                  # right to left, and tighter than a minus sign
        f = atom()
        if peek() in ("^", "**"):
            take()
            return binop(f, "^", unary())
        return f

    def atom():
        t = take()
        if t is None:
            raise ValueError("it ends too soon")
        if re.match(r"\d|\.\d", t):
            n = float(t)
            return lambda v: n
        if t == "(":
            f = total()
            need(")")
            return f
        if t in ("a", "b", "c"):
            k = "abc".index(t)
            return lambda v: v[k]
        if t == "PI":
            return lambda v: math.pi
        if t in FORMULA_FN:
            need("(")
            args = [total()]
            while peek() == ",":
                take()
                args.append(total())
            need(")")
            fn = FORMULA_FN[t]
            return lambda v: float(fn(*[g(v) for g in args]))
        raise ValueError(f'it uses "{t}"')

    f = total()
    if pos[0] < len(toks):
        raise ValueError(f'it has something extra at "{toks[pos[0]]}"')
    return f


def evaluate(formula: str, a: float, b: float, c: float) -> float:
    return float(compile_formula(formula)([a, b, c]))


def samples(lo: float, hi: float, step: float, n: int) -> list[float]:
    """A slider's values across its whole range, not only its ends: a formula that peaks or
    dips in the middle (an area with a fixed fence) shows up."""
    k = max(1, min(n - 1, int((hi - lo) / step + 1e-9) if step > 0 else n - 1))
    return [lo + (hi - lo) * j / k for j in range(k + 1)]


def check_whatif(i: int, title: str, blob: str, rep: Report) -> None:
    rows = [[x.strip() for x in r.split("|")] for r in (attr(blob, "data-inputs") or "").split(";") if r.strip()]
    if not 1 <= len(rows) <= 3:
        rep.error(f"Slide {i} ({title}): a what-if takes one to three sliders in data-inputs, "
                  '"Label|min|max|step|start", separated by semicolons.')
        return
    if len(rows) == 3:
        rep.warn(f"Slide {i} ({title}): three sliders is a lot to hold at once. One that matters "
                 "usually teaches more than three that might.")
    grids = []
    for r in rows:
        r += [""] * (5 - len(r))
        if not numbers(r[1], r[2], *[x for x in r[3:5] if x]) or value(r[1]) >= value(r[2]):
            rep.error(f"Slide {i} ({title}): slider {r[0]!r} should read 'Label|min|max|step|start' "
                      "with min below max.")
            return
        lo, hi = value(r[1]), value(r[2])
        step = value(r[3]) if r[3] and value(r[3]) > 0 else (hi - lo) / 20
        grids.append(samples(lo, hi, step, 21 if len(rows) > 2 else 41))
    formula = attr(blob, "data-formula") or ""
    if not formula.strip():
        rep.error(f"Slide {i} ({title}): a what-if needs data-formula, written in a, b, c for "
                  "the sliders in order, e.g. \"a * b * 7\".")
        return
    letters = set(re.findall(r"(?<![\w.])([a-c])(?![\w])", formula))
    unused = [chr(97 + k) for k in range(len(rows)) if chr(97 + k) not in letters]
    if unused:
        rep.warn(f"Slide {i} ({title}): the formula never uses {', '.join(unused)}, so moving that "
                 "slider changes nothing. A slider that does nothing teaches that sliders lie.")
    outs = []
    try:
        f = compile_formula(formula)
        for vals in itertools.product(*grids):
            outs.append(float(f(list(vals) + [0.0] * (3 - len(vals)))))
    except (ValueError, ZeroDivisionError, OverflowError, TypeError) as e:
        rep.error(f"Slide {i} ({title}): data-formula {formula!r} doesn't work: {e}. It may use "
                  "a, b, c, numbers, + - * / % ^ ( ) and round, floor, ceil, min, max, abs, sqrt, pow, PI, "
                  "with * written out (2*a, not 2a).")
        return
    if not all(math.isfinite(o) for o in outs):
        rep.error(f"Slide {i} ({title}): somewhere in its sliders' range the formula's result is not "
                  "a number (a division by zero, a root of a negative). The slide would show '–' there.")
        return
    if min(outs) < 0:
        rep.error(f"Slide {i} ({title}): the what-if goes below zero ({min(outs):g}) somewhere in "
                  "its sliders' range. Its bar starts at zero, like every bar in the deck.")
    top = attr(blob, "data-max")
    if top and numbers(top) and max(outs) > value(top) * 1.001:
        rep.warn(f"Slide {i} ({title}): the output reaches {max(outs):g} but data-max is {top}, "
                 "so the bar runs off its track. Raise data-max or leave it out.")
    band = [b for b in (attr(blob, "data-band") or "").split("|") if b.strip()]
    if band and (len(band) != 2 or not numbers(*band) or value(band[0]) >= value(band[1])):
        rep.error(f"Slide {i} ({title}): data-band should read 'low|high', e.g. \"0|40\".")
    if not attr(blob, "data-output"):
        rep.warn(f"Slide {i} ({title}): a what-if with no data-output says 'Result'. Name what "
                 "the number is, in words students own: 'Litres a week'.")


def check_ticks(i: int, title: str, kind: str, blob: str, lo: float, hi: float, rep: Report) -> None:
    for t in [t for t in (attr(blob, "data-ticks") or "").split("|") if t.strip()]:
        v = t.split("=", 1)[0]
        if not numbers(v) or not lo - 1e-9 <= value(v) <= hi + 1e-9:
            rep.error(f"Slide {i} ({title}): tick {t.strip()!r} on {NAMES[kind]} should read 'value' or "
                      f"'value=label' (e.g. 0.5=½ or 1/4), with the value between {lo:g} and {hi:g}. "
                      "Ticks put the value first; cards put the label first.")


def check_games(sl: list, rep: Report, langs=()) -> int:
    """Games and interactives are configured in data- attributes and child markup, and a
    typo there is a game that breaks in front of the class. Each one on a slide with a
    timer is run as talk (partners agree first), so it counts toward the lesson's talk
    moves. Returns how many slides do."""
    as_talk = 0
    for i, (a, body) in enumerate(sl, 1):
        title = attr(a, "data-title") or f"slide {i}"
        found = []
        for _, blob, start in tags(body):
            kinds = [c for c in classes(blob) if c in COMPONENTS]
            if not kinds:
                continue
            kind, el = kinds[0], block(body, start)
            why = (attr(blob, "data-why") or "").strip()
            found.append(kind)
            if attr(blob, "data-teams") is not None:
                rep.error(f"Slide {i} ({title}): data-teams on {NAMES[kind]}. Teams are set once for "
                          "the whole deck, and only when the teacher asks for them: build with --teams.")
            kids = children(el) if kind in ("order", "wodb", "mistake", "tf", "match") else []
            needs_why = kind not in ("wodb", "tf", "whatif", "zoomin")

            if kind in ("game", "hinge"):
                opts = [o for o in (attr(blob, "data-options") or "").split("|") if o.strip()]
                ans = (attr(blob, "data-answer") or "").strip()
                if len(opts) < 2:
                    rep.error(f"Slide {i} ({title}): {NAMES[kind]} needs at least two "
                              'data-options, "A|B|C".')
                if len(opts) > 6:
                    rep.error(f"Slide {i} ({title}): {NAMES[kind]} takes six options at most (A to F); "
                              f"it has {len(opts)}, and the deck would drop the rest.")
                if not ans.isdigit() or not 1 <= int(ans) <= max(1, min(6, len(opts))):
                    rep.error(f"Slide {i} ({title}): data-answer={ans!r} isn't one of the "
                              f"{min(6, len(opts))} options. It counts from 1.")
                if kind == "hinge":
                    traps = (attr(blob, "data-traps") or "").split("|")
                    if len(traps) != len(opts):
                        rep.error(f"Slide {i} ({title}): a hinge question needs one data-traps entry "
                                  f"per option ({len(opts)}), '-' for the right one. Each wrong "
                                  "answer is a known wrong idea, and the trap names it.")
                    else:
                        for k, t in enumerate(traps[:6]):
                            if str(k + 1) != ans and len(t.split()) < 3:
                                rep.error(f"Slide {i} ({title}): option {LETTERS[k]} has no trap. "
                                          "Say the wrong thinking that leads there, in a few words; "
                                          "that is what tells you what to reteach.")
            elif kind == "sort":
                bins = [b for b in (attr(blob, "data-bins") or "").split("|") if b.strip()]
                items = [x for x in (attr(blob, "data-items") or "").split("|") if x.strip()]
                if len(bins) < 2 or len(items) < 3:
                    rep.error(f"Slide {i} ({title}): a sort needs two or more data-bins and "
                              'three or more data-items, "Card=1|Card=2".')
                elif len(bins) > 3 or len(items) > 8:
                    rep.warn(f"Slide {i} ({title}): a sort of {len(items)} cards into {len(bins)} bins. "
                             "Two or three bins and three to eight cards fit a wall and a period; "
                             "split a bigger sort in two.")
                for x in items:
                    k = x.rsplit("=", 1)
                    if len(k) != 2 or not k[1].strip().isdigit() or \
                            not 1 <= int(k[1]) <= max(1, len(bins)):
                        rep.error(f"Slide {i} ({title}): sort card {x.strip()!r} should read "
                                  f"'Card=bin', with the bin a number from 1 to {len(bins)}.")
            elif kind == "order":
                if not 3 <= len(kids) <= 8:
                    rep.error(f"Slide {i} ({title}): order it takes three to eight steps as child "
                              f"elements, in the right order; it has {len(kids)}.")
                elif len(kids) > 6:
                    rep.warn(f"Slide {i} ({title}): {len(kids)} steps to order. Past six, the "
                             "game is mostly reading; split the procedure in two.")
            elif kind in ("line", "estimate"):
                lo, hi = attr(blob, "data-min") or "0", attr(blob, "data-max")
                if hi is None or not numbers(lo, hi) or value(lo) >= value(hi):
                    rep.error(f"Slide {i} ({title}): {NAMES[kind]} needs data-min below data-max.")
                    continue
                lo, hi = value(lo), value(hi)
                check_ticks(i, title, kind, blob, lo, hi, rep)
                if kind == "line":
                    items = [x for x in (attr(blob, "data-items") or "").split("|") if x.strip()]
                    if not 3 <= len(items) <= 8:
                        rep.error(f"Slide {i} ({title}): a number line takes three to eight cards in "
                                  'data-items, "label=value".')
                    for x in items:
                        k = x.rsplit("=", 1)
                        if len(k) != 2 or not numbers(k[1]) or not lo <= value(k[1]) <= hi:
                            rep.error(f"Slide {i} ({title}): card {x.strip()!r} should read "
                                      f"'label=value' with the value between {lo:g} and {hi:g}.")
                else:
                    ans = attr(blob, "data-answer")
                    if ans is None or not numbers(ans) or not lo <= value(ans) <= hi:
                        rep.error(f"Slide {i} ({title}): data-answer must be a number between "
                                  f"{lo:g} and {hi:g}.")
                    elif abs(value(ans) - (lo + hi) / 2) < 0.1 * (hi - lo):
                        rep.warn(f"Slide {i} ({title}): the answer {value(ans):g} sits near the middle "
                                 f"of {lo:g} to {hi:g}, where the Just right marker waits. Set the "
                                 "range so the answer is off-centre, or the line hints at it.")
                    if not attr(blob, "data-unit"):
                        rep.warn(f"Slide {i} ({title}): an estimate with no data-unit. '263' is a "
                                 "number; '263 seeds' is a thing a student can picture.")
            elif kind == "wodb":
                if len(kids) != 4:
                    rep.error(f"Slide {i} ({title}): which one doesn't belong takes exactly four "
                              f"tiles; it has {len(kids)}.")
                for k, t in enumerate(kids):
                    if len((attr(head(t), "data-why") or "").split()) < 4:
                        rep.error(f"Slide {i} ({title}): tile {LETTERS[k] if k < 6 else k + 1} has no "
                                  "real data-why. Every tile needs a reason it could be the odd one; "
                                  "a tile with none means one answer is right and it is a quiz.")
                    if "<img" in t and "--focus" not in t:
                        rep.warn(f"Slide {i} ({title}): a photo tile has no --focus, so it centre-crops.")
            elif kind == "mistake":
                wrong = [k for k in kids if re.search(r"\sdata-wrong\b", head(k))]
                if not 3 <= len(kids) <= 7:
                    rep.error(f"Slide {i} ({title}): find the mistake takes three to seven steps; "
                              f"it has {len(kids)}.")
                if len(wrong) != 1:
                    rep.error(f"Slide {i} ({title}): mark exactly one step data-wrong (it has "
                              f"{len(wrong)}). One mistake is a hunt; two is a mess.")
                elif not (attr(head(wrong[0]), "data-fix") or "").strip():
                    rep.error(f"Slide {i} ({title}): the wrong step needs data-fix, what it "
                              "should have said.")
            elif kind == "tf":
                labels = [x.strip().lower() for x in (attr(blob, "data-labels") or "True|False").split("|") if x.strip()]
                if not 2 <= len(kids) <= 8:
                    rep.error(f"Slide {i} ({title}): true or false takes two to eight claims; "
                              f"it has {len(kids)}.")
                for k, c in enumerate(kids, 1):
                    h = head(c)
                    if (attr(h, "data-answer") or "").strip().lower() not in labels:
                        rep.error(f"Slide {i} ({title}): claim {k}'s data-answer isn't one of "
                                  f"{', '.join(labels)}.")
                    if len((attr(h, "data-why") or "").split()) < 5:
                        rep.error(f"Slide {i} ({title}): claim {k} has no real data-why. The reveal "
                                  "says why, in a sentence a student could repeat.")
                    for code in langs:
                        if not has_line(c, code):
                            rep.warn(f"Slide {i} ({title}): claim {k} has no '{code}' line. Each claim "
                                     "is a question on its own; it carries its line like a headline.")
                    if words(c) > 16:
                        rep.warn(f"Slide {i} ({title}): claim {k} runs {words(c)} words. A claim is "
                                 "read from the back row in a few seconds; cut it to one idea.")
            elif kind == "match":
                bad = [k for k in kids if len(children(k)) != 2]
                if not 3 <= len(kids) <= 6:
                    rep.error(f"Slide {i} ({title}): match takes three to six pairs; it has {len(kids)}.")
                if bad:
                    rep.error(f"Slide {i} ({title}): every pair in a match holds exactly two "
                              "elements, the left and the right.")
            elif kind == "whatif":
                check_whatif(i, title, blob, rep)
            elif kind == "zoomin":
                if "--focus" not in el:
                    rep.error(f"Slide {i} ({title}): a zoom-in with no --focus zooms into the middle "
                              "of the photo. --focus is the detail students see first.")
                zooms = [z for z in (attr(blob, "data-zooms") or "5|2.5|1").split("|") if z.strip()]
                if not zooms or not numbers(*zooms) or value(zooms[0]) <= 1:
                    rep.error(f"Slide {i} ({title}): data-zooms should step down to 1, e.g. \"6|3|1\".")
            for k in kids if kind in ("order", "match") else []:
                if words(k) > 14:
                    rep.warn(f"Slide {i} ({title}): a card in {NAMES[kind]} runs {words(k)} words. Cards are "
                             "read from across the room; keep each to a phrase.")
            if needs_why and len(why.split()) < 6:
                rep.error(f"Slide {i} ({title}): {NAMES[kind]} has no real data-why"
                          + (f" (it is {len(why.split())} words; write a sentence of six or more)" if why else "")
                          + ". The reveal explains the answer in a sentence a student could repeat; "
                          "it never just marks it right.")
        games = [k for k in found if k in GAMES]
        quizzes = sum(1 for _, t, _ in tags(body) if "pinned" in classes(t) and re.search(r"\sdata-quiz\b", t))
        on_slide = [k for k in found if k in GAMES or k == "zoomin"] + ["quiz"] * quizzes
        if len(on_slide) > 1:
            rep.warn(f"Slide {i} ({title}): {len(on_slide)} games on one slide ({', '.join(NAMES[g] for g in on_slide)}). "
                     "V and C act on the first; one game per slide.")
        if games:
            if attr(a, "data-timer"):
                # a slide with data-phases is a talk slide already, and check_talk counts it
                if not attr(a, "data-phases"):
                    as_talk += 1
            elif "whatif" not in games:
                rep.warn(f"Slide {i} ({title}): {NAMES[games[0]]} with no data-timer. Give partners "
                         "a timed minute to agree before anyone answers; that is what makes "
                         "it talk and not a quiz.")
        for _, t, start in tags(body):
            if "pinned" in classes(t) and re.search(r"\sdata-quiz\b", t):
                if len([1 for _, p, _ in tags(block(body, start)) if "pin" in classes(p)]) < 2:
                    rep.warn(f"Slide {i} ({title}): a label-the-photo quiz with fewer than two pins.")
    if as_talk:
        rep.note(f"{as_talk} game slide(s) run as talk.")
    return as_talk


def check_density(sl: list, minutes: int, rep: Report) -> None:
    """The caps the docs set on a whole deck: games earn their place (two to four in an
    hour, one per slide), and the dark checkpoint is rare enough to stop the room."""
    def has_game(body):
        return any(set(classes(t)) & set(COMPONENTS) or ("pinned" in classes(t) and re.search(r"\sdata-quiz\b", t))
                   for _, t, _ in tags(body))
    n = sum(1 for _, body in sl if has_game(body))
    cap = max(4, round(4 * minutes / 60))
    if n > cap:
        rep.warn(f"{n} game slides for a {minutes}-minute period. A game earns its place where the "
                 f"lesson's verb calls for one: two to four an hour, about {cap} at most here.")
    dark = sum(1 for a, _ in sl if "dark" in classes(a))
    if dark > 2:
        rep.warn(f"{dark} dark slides. The dark checkpoint stops the room because it is rare: "
                 "two in a period at most.")


def check_vocab(html: str, words: list, rep: Report) -> None:
    """The packet's key words are marked on the slides too, by the template, from the
    body's data-vocab. A key word that never appears on a slide isn't being taught
    on the wall."""
    if not words:
        return
    text = text_of(re.sub(r'<p class="es[^"]*"[^>]*>.*?</p>', " ", html, flags=re.S)).lower()
    missing = [w for w in words
               if not re.search(r"(?<![\w-])" + r"\s+".join(map(re.escape, w.lower().split()))
                                + r"(?:s|es|ed|ing)?(?![\w-])", text)]
    if missing:
        rep.warn("Key word(s) never on a slide: " + ", ".join(missing)
                 + ". Each one gets a word slide and appears where it is used.")
    else:
        rep.note(f"{len(words)} key word(s), each on a slide and marked.")
    shown = {" ".join(text_of(w).lower().split())
             for w in re.findall(r'<div class="w">(.*?)</div>', html, flags=re.S)}
    unslid = [w for w in words if w not in missing
              and not any(t in (w.lower(), w.lower() + "s", w.lower() + "es") or w.lower() in
                          (t, t + "s", t + "es") for t in shown)]
    if unslid:
        rep.warn("Key word(s) with no word slide: " + ", ".join(unslid)
                 + ". Each key word gets one: the word, how to say it, what it means, and a "
                 "picture or a non-example.")


def norm(text: str) -> str:
    """Words only, lowercase: punctuation, bold marks and blanks don't count as a difference."""
    text = re.sub(r"\*\*|_{2,}", " ", str(text)).replace("\u2019", "'").lower()
    return " ".join(re.findall(r"[\w']+", text))


def check_against_packet(html: str, packet: dict, rep: Report) -> None:
    """The deck is the packet on the wall. Every question a student answers on paper is on
    a slide in the packet's own words, with the packet's language lines, so a student who
    looks up recognizes the task without reading it twice."""
    def questions(blocks):
        for b in blocks:
            if b.get("type") == "question":
                yield b
    meta = packet.get("meta", {})
    langs = meta.get("languages")
    if langs is None:  # a packet written before languages were opt-in
        langs = ["es"] if any(q.get("es") for q in questions(packet.get("sections", []))) else []
    wall = norm(text_of(html))
    missing, lines = [], []
    for q in questions(packet.get("sections", [])):
        prompt = norm(q.get("prompt", ""))
        # the first sentence carries the task; context before it may be cut on a slide
        first = norm(re.split(r"(?<=[.?!])\s+", str(q.get("prompt", "")).strip())[-1])
        num = q.get("number", "?")
        if prompt not in wall and (len(first.split()) < 4 or first not in wall):
            missing.append(str(num))
        for code in langs:
            if q.get(code) and norm(q[code]) not in wall:
                lines.append(f"{num} ({code})")
    if missing:
        rep.warn("Packet question(s) not on any slide in the packet's words: "
                 + ", ".join(missing) + ". Every task a student writes appears on a slide, "
                 "worded the same, with its packet page named.")
    else:
        rep.note("Every packet question is on a slide in the packet's words.")
    if lines:
        rep.warn("A slide's language line differs from the packet's, or is missing, for: "
                 + ", ".join(lines) + ". Use the packet's line word for word.")


def check_talk(sl: list, rep: Report, games: int = 0) -> None:
    """Student talk is the non-negotiable, and the deck is what runs it.

    A talk slide carries data-phases (think, A talks, B talks, share), and its
    data-timer is their sum -- the timer runs the phases, and the period math
    runs on data-timer, so the two have to agree or one of them is lying.
    """
    talk = 0
    for i, (a, body) in enumerate(sl, 1):
        title = attr(a, "data-title") or f"slide {i}"
        spec = attr(a, "data-phases")
        if not spec:
            continue
        talk += 1
        phases = []
        for part in spec.split(";"):
            bits = part.split("|")
            if len(bits) != 2 or not bits[1].strip().isdigit():
                rep.error(f"Slide {i} ({title}): data-phases entry {part.strip()!r} should read "
                          "'Name|seconds', e.g. 'A talks|60'.")
                continue
            phases.append((bits[0].strip(), int(bits[1])))
        timer = attr(a, "data-timer")
        total = sum(sec for _, sec in phases)
        if not timer:
            rep.error(f"Slide {i} ({title}) has data-phases but no data-timer. Add "
                      f'data-timer="{total}", the sum of the phases.')
        elif timer.isdigit() and int(timer) != total:
            rep.error(f"Slide {i} ({title}): the phases add up to {total}s but data-timer "
                      f"is {timer}s. Make them agree.")
        if not (re.search(r'<img|<svg|dv-|data-yt', body) or has_class(body, ["vote"] + COMPONENTS)):
            rep.error(f"Slide {i} ({title}) is a talk slide with nothing to look at. Students "
                      "talk best about something in front of them: put the photograph, chart, "
                      "or diagram they are discussing in the .talk layout's visual.")
        names = {n for n, _ in phases}
        for want in re.findall(r'data-phase="([^"]*)"', body):
            if want not in names:
                rep.warn(f"Slide {i} ({title}): an element waits for phase {want!r}, which "
                         f"isn't one of {sorted(names)}. It will never light up.")
    if talk == 0:
        rep.error(
            "No talk slide. Every lesson runs at least two student-to-student talk moves on "
            'screen, one of them a talk slide: data-phases="Think|30; A talks|60; B talks|60; '
            'Share|60", the roles, and a "Say it" stem. See "Talk slides" in references/deck.md.'
        )
    elif talk + games == 1:
        rep.warn("One talk move on screen. Every lesson runs at least two; give the second its "
                 "talk slide, or run a game round as talk.")
    else:
        rep.note(f"{talk} talk slide(s) with phased timers.")


def check_template_wiring(raw: str, html: str, rep: Report) -> None:
    """`raw` is the untouched file -- the wiring lives in <style> and <script>,
    which the markup passes deliberately strip. `html` is the stripped markup,
    used only for leftover placeholder text."""
    if "imgmiss" not in raw:
        rep.error(
            "The photo fallback is missing. A blocked image will show a broken icon "
            "on the projector. Copy assets/deck_template.html rather than rebuilding "
            "the file by hand."
        )
    if ".pgrid" not in raw and "<img" in html:
        rep.error("Photo styles are missing -- the deck was not built from the template.")
    if "timer-time" not in raw:
        rep.error("Deck chrome (timer/nav) is missing -- start from the template.")

    for p in PLACEHOLDERS:
        if p in html:
            rep.error(f"Template placeholder text survived into the deck: {p!r}")


def check_teaching(raw: str, html: str, sl: list, rep: Report) -> None:
    # Interactive charts are not optional. In a room where reading is the barrier
    # the chart is the explanation and the words are its caption -- a deck with
    # none has pushed all its meaning back into prose, which is the one channel
    # these students cannot use. Static .bars do not count: the teaching happens
    # in the predict-then-reveal click, not in the picture.
    kinds = ["dv-icons", "dv-guess", "dv-dots", "dv-bars", "dv-gauge", "dv-percent"]
    charts = sum(len(re.findall(r'class="[^"]*\b' + k + r'\b', html)) for k in kinds)
    # a what-if model and an estimate carry a real number through the same
    # predict-then-reveal moment, so they count; a static .bars never does
    charts += sum(1 for _, t, _ in tags(html) if {"whatif", "estimate"} & set(classes(t)))
    if charts == 0:
        rep.error(
            "No interactive chart. Every deck carries at least one, and two to four "
            "when the lesson touches numbers -- the chart is the explanation, and a "
            "deck without one has put the whole lesson back into prose. The kit is "
            "already in the template; see references/dataviz.md."
        )
    elif charts == 1:
        rep.warn(
            "Only one interactive chart. Two to four is the usual range for a lesson "
            "with numbers in it."
        )
    else:
        rep.note(f"{charts} interactive charts.")

    for k in kinds:
        for m4 in re.finditer(r'class="([^"]*\b' + k + r'\b[^"]*)"', html):
            if not re.search(r"\bdv\b", m4.group(1)):
                rep.error(
                    f'A {k} chart is missing the `dv` base class (class="{m4.group(1)}"). '
                    "`dv` carries the colour variables -- without it the chart builds but "
                    'renders invisible: labels and no bars. Use class="dv ' + k + '".'
                )

    if re.search(r'class="bars"', html) and charts == 0:
        rep.warn(
            "The deck uses static .bars but no interactive chart. Static bars are for "
            "a comparison you don't need to reveal; they skip the predict-then-reveal "
            "moment that makes the number stick."
        )

    for i, (a, body) in enumerate(sl, 1):
        title = attr(a, "data-title") or f"slide {i}"
        # a talk slide's "Say it" stem is spoken, not written; a frame anywhere else is a
        # sentence students write down
        writes = bool(re.search(r'class="frames|class="blank', body)) and not attr(a, "data-phases")
        if writes and not attr(a, "data-packet"):
            rep.warn(f"Slide {i} ({title}) asks students to write but has no data-packet.")
        for _, t, start in tags(body):
            if "frames" in classes(t) and not any("frame" in classes(x) for _, x, _ in tags(block(body, start))):
                rep.warn(f'Slide {i} ({title}): a .frames with no .frame inside. Each stem is '
                         '<div class="frame">I think <span class="blank"></span> because…</div>, '
                         'under <div class="frames-label">Say it</div>.')

        timer = attr(a, "data-timer")
        if timer and timer.isdigit() and int(timer) > 1800:
            rep.warn(f"Slide {i} ({title}): timer is {int(timer)//60} minutes.")

        # A summary line under the body reads as filler. Only <p> that follows the
        # *closed* body counts -- .vlink sits inside .body.media and is correct,
        # which an "any </div> then <p>" test flags wrongly.
        b = body_of(body)
        after = body[body.find(b) + len(b) :] if b else ""
        # `es` joins `instruct` here by name, not by loosening the test: a summary
        # line under the body is still the thing this check exists to catch.
        for m2 in re.finditer(r'<p[^>]*class="([^"]*)"', after):
            if m2.group(1).split() and not set(m2.group(1).split()) <= {"instruct", "es"}:
                rep.warn(
                    f"Slide {i} ({title}): a <p class=\"{m2.group(1)}\"> follows the body. "
                    "Only a direction (.instruct) or its language line (.es) may sit there -- "
                    "a summary line reads as filler."
                )

    # --- video -----------------------------------------------------------
    facades = re.findall(r'<div class="video-wrap"[^>]*data-yt="([^"]*)"', html)
    bare = re.findall(r'<div class="video-wrap"(?![^>]*data-yt)', html)
    n_video = len(facades) + len(bare)

    if n_video == 0:
        rep.warn(
            "No video. Every lesson normally gets one -- it is the reliable attention "
            "reset in a period where reading is expensive."
        )
    if bare:
        rep.error(
            f"{len(bare)} video(s) use a bare iframe instead of the click-to-play facade. "
            "A blocked embed renders a black rectangle with no way forward; the facade "
            "degrades to a poster, then to a labelled card, and always keeps the link."
        )
    for vid in facades:
        if not vid or not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
            rep.error(
                f"data-yt is not a valid YouTube id: {vid!r}. Ids are 11 characters -- "
                "a placeholder here is a dead video in front of the class."
            )
    if n_video and 'class="vlink"' not in html:
        rep.error(
            "A video has no plain link underneath. School networks block embeds often "
            "enough that the fallback is not optional."
        )
    markup_only = re.sub(r"<script\b.*?</script>", "", html, flags=re.S | re.I)
    if re.search(r"autoplay=1", markup_only):
        rep.error(
            "autoplay=1 is in the markup. The template's script adds it after a click; "
            "a deck that plays on slide change talks over you."
        )
    for m3 in re.finditer(r'<button class="vfacade".*?</button>', html, re.S):
        if "<img" not in m3.group(0):
            rep.error("A video facade has no poster image, so a blocked embed shows nothing.")

    # --- dark surfaces ----------------------------------------------------
    for bad, why in ((r"\.slide\.dark\{background:var\(--ink\)", "the checkpoint slide"),
                     (r"\.vc\.word\{background:var\(--ink\)", "the vocabulary word cell")):
        if re.search(bad, raw):
            rep.warn(
                f"A dark surface ({why}) still uses --ink, which reads as navy at full "
                "size on a projector. Dark surfaces use --caviar."
            )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck")
    ap.add_argument("--minutes", type=int, default=60,
                    help="length of the class period (default 60)")
    ap.add_argument("--languages", default="",
                    help="the class's home languages, comma-separated codes (default: none, or "
                         "the packet's)")
    ap.add_argument("--vocab", default="",
                    help="the packet's key words, comma-separated; each should be on a slide")
    ap.add_argument("--packet", help="the lesson's packet.json, or the packet .docx itself; the deck "
                                     "is checked against it")
    args = ap.parse_args()

    try:
        html = open(args.deck, encoding="utf-8").read()
    except OSError as e:
        print(f"cannot read {args.deck}: {e}", file=sys.stderr)
        return 1

    # Strip HTML comments before any parsing. The template documents the slide
    # skeleton inside a comment, and counting that as a real slide inflates the
    # count by one and hunts for placeholders that are only ever documentation.
    raw = html
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    # Style and script bodies are not markup. A CSS comment mentioning a tag, or
    # a script that builds one, is not a slide element -- reading them as markup
    # invents elements that do not exist on any slide.
    html = re.sub(r"<style\b.*?</style>", "<style></style>", html, flags=re.S | re.I)
    html = re.sub(r"<script\b.*?</script>", "<script></script>", html, flags=re.S | re.I)

    rep = Report()
    sl = slides(html) or []
    check_structure(html, sl, args.minutes, rep)
    check_minutes(sl, args.minutes, rep)
    check_photos(html, sl, args.minutes, rep)
    check_template_wiring(raw, html, rep)
    check_teaching(raw, html, sl, rep)
    packet = None
    if args.packet:
        try:
            packet = load_packet(args.packet, args.languages)
        except (OSError, ValueError) as e:
            rep.warn(f"Could not read {args.packet}: {e}")
        if packet:
            meta = packet.get("meta", {})
            if not args.vocab and meta.get("vocab"):
                args.vocab = ",".join(meta["vocab"])
            if not args.languages and meta.get("languages"):
                args.languages = ",".join(meta["languages"])
            check_against_packet(html, packet, rep)
    # home languages are opt-in: none named, none required
    langs = [c.strip() for c in args.languages.split(",") if c.strip()]
    games = check_games(sl, rep, langs)
    body = re.search(r"<body\b[^>]*>", raw)
    teams = attr(body.group(0), "data-teams") if body else None
    if teams:
        rep.note(f"Team play on: {teams.replace('|', ', ')}, one running score in every slide's "
                 "footer. Teams only when the teacher asked for them.")
    check_talk(sl, rep, games)
    check_vocab(html, [w.strip() for w in args.vocab.split(",") if w.strip()], rep)
    check_language_access(html, sl, rep, langs)
    check_density(sl, args.minutes, rep)

    size_mb = len(html.encode()) / 1e6
    if size_mb > 1.0:
        rep.warn(f"Deck is {size_mb:.1f} MB -- large enough to be slow to open.")

    for m in rep.notes:
        print(f"  ok    {m}")
    for m in rep.warns:
        print(f"  warn  {m}")
    for m in rep.errors:
        print(f"  ERROR {m}")

    print()
    if rep.errors:
        print(f"{len(rep.errors)} error(s), {len(rep.warns)} warning(s) — fix the errors, then re-run.")
        return 1
    print(f"clean — 0 errors, {len(rep.warns)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
