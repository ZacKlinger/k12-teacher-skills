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
import re
import sys
from collections import Counter

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
    m = re.search(rf'{name}="([^"]*)"', blob)
    return m.group(1) if m else None


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
        has_media = bool(re.search(r'<img|<iframe|<svg|dv-|class="(?:vote|picker|heard)\b', body_html))
        if not inner and not has_media and not is_dark:
            rep.error(
                f"Slide {i} ({title}): the body is empty. A headline alone is not a "
                "slide -- only the dark checkpoint is allowed to be bare."
            )


def check_photos(html: str, sl: list, minutes: int, rep: Report) -> None:
    all_imgs = [t for t in imgs(html) if not is_poster(t)]
    floor = 5 if minutes <= 70 else 8
    ceil = 8 if minutes <= 70 else 12

    if len(all_imgs) < floor:
        rep.error(
            f"{len(all_imgs)} photographs; a {minutes}-minute period needs {floor}-{ceil}. "
            "A student who reads at a third-grade level and has never seen the thing "
            "cannot picture it from the word."
        )
    elif len(all_imgs) > ceil:
        rep.warn(f"{len(all_imgs)} photographs -- more than the usual {floor}-{ceil}.")
    else:
        rep.note(f"{len(all_imgs)} photographs (expected {floor}-{ceil}).")

    # base64 inlining: deck.md used to say "single file, no external assets",
    # which pushed builds into inlining every photo and producing 2 MB decks.
    # The one exception is the class's own photographs (the frame, the garden, a
    # build), which can't be linked and are worth more than any stock photo. Up to
    # three, each shrunk to about 1200px, keeps the deck quick to open.
    inlined = re.findall(r'src="data:image/[^"]+"', html)
    if len(inlined) > 3:
        rep.error(
            f"{len(inlined)} photographs are base64-inlined. Link public photos by URL, and "
            "inline only the class's own photos, three at most -- inlining everything "
            "produced a 1.9 MB deck that is slow to open in front of a class."
        )
    for blob in inlined:
        if len(blob) > 340_000:
            rep.error(
                f"An inlined photo is {len(blob) // 1000} KB. Shrink it to about 1200px wide "
                "at JPEG quality 70 (see references/photographs.md, 'Your own photos')."
            )

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
# text elements in document order, so a Spanish line can be measured against the
# English line immediately above it
TEXT_EL = re.compile(r'<(h1|h2|p|div)\b([^>]*)>(.*?)</\1>', re.S | re.I)


def text_of(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


UNSPACED = {"zh", "ja", "ko", "th", "my", "km", "lo"}


def check_language_access(html: str, sl: list, rep: Report, langs=("es",)) -> None:
    """Every question and every direction carries a Spanish line.

    Reading is the barrier in this room twice over for a newcomer, and a slide is
    the one surface a student cannot ask a neighbour to re-read for them. The line
    is abbreviated on purpose -- the task, not the framing -- so this checks that
    it is *there* and that it stayed short, and leaves whether it is good Spanish
    to a human.
    """
    total = len(ES_CLASS.findall(html))
    if total == 0:
        rep.error(
            "No Spanish anywhere in the deck. Every question and every direction "
            'carries a <p class="es"> line under the English it supports. See the '
            '"Language access" section of references/deck.md.'
        )
    else:
        rep.note(f"{total} Spanish support line(s).")

    # A room with more than one home language: each extra language rides the same
    # `.es` line style, marked with its code -- <p class="es" lang="zh">.
    for code in langs:
        if code == "es":
            continue
        tagged = re.compile(r'<[^>]*\bclass="[^"]*\bes\b[^"]*"[^>]*\blang="' + re.escape(code)
                            + r'(-[^"]*)?"|<[^>]*\blang="' + re.escape(code)
                            + r'(-[^"]*)?"[^>]*\bclass="[^"]*\bes\b')
        n = len(tagged.findall(html))
        if n == 0:
            rep.error(
                f"No '{code}' lines in the deck, but the room's languages include it. Each "
                f'one sits beside the Spanish as <p class="es" lang="{code}">. See the '
                '"Language access" section of references/deck.md.'
            )
        else:
            rep.note(f"{n} '{code}' support line(s).")

    for i, (a, body) in enumerate(sl, 1):
        title = attr(a, "data-title") or f"slide {i}"
        has_es = bool(ES_CLASS.search(body))

        headline = ""
        m = re.search(r"<(h1|h2)\b[^>]*>(.*?)</\1>", body, re.S | re.I)
        if m:
            headline = text_of(m.group(2))
        asks = headline.endswith("?") or bool(re.search(r'<p[^>]*class="[^"]*\binstruct\b', body))
        writes = bool(attr(a, "data-packet"))

        if not has_es and (asks or writes):
            why = "asks a question" if asks else "sends students to the packet"
            rep.warn(
                f"Slide {i} ({title}) {why} but carries no Spanish line. If the slide "
                "only points at a page, that is fine -- say so and move on."
            )

        # Abbreviated means shorter. Spanish runs 15-20% longer than English for the
        # same content, so only a real overshoot means the framing got translated too.
        prev = ""
        for el in TEXT_EL.finditer(body):
            classes = set((attr(el.group(2), "class") or "").split())
            body_text = text_of(el.group(3))
            if not body_text:
                continue
            if "es" in classes:
                code = (attr(el.group(2), "lang") or "es").split("-")[0]
                if code in UNSPACED:
                    continue
                if prev and len(body_text.split()) > len(prev.split()) * 1.2:
                    rep.warn(
                        f"Slide {i} ({title}): the Spanish line is longer than the English "
                        f"above it ({len(body_text.split())} words to {len(prev.split())}). "
                        "It carries the task, not the framing -- cut it back."
                    )
            elif el.group(1).lower() in ("h1", "h2") or "instruct" in classes:
                prev = body_text


def check_talk(sl: list, rep: Report) -> None:
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
        if not re.search(r"<img|<svg|dv-|data-yt|class=\"vote", body):
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
            "No talk slide. Every lesson runs at least one student-to-student talk move on "
            'screen: a slide with data-phases="Think|30; A talks|60; B talks|60; Share|60", '
            'the roles, and a "Say it" stem. See "Talk slides" in references/deck.md.'
        )
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
        writes = bool(re.search(r'class="frames|class="blank', body))
        if writes and not attr(a, "data-packet"):
            rep.warn(f"Slide {i} ({title}) asks students to write but has no data-packet.")

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
                    "Only a direction (.instruct) or its Spanish line (.es) may sit there -- "
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
    ap.add_argument("--languages", default="es",
                    help="home languages in the room, comma-separated codes (default es)")
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
    check_photos(html, sl, args.minutes, rep)
    check_template_wiring(raw, html, rep)
    check_teaching(raw, html, sl, rep)
    check_talk(sl, rep)
    langs = [c.strip() for c in args.languages.split(",") if c.strip()] or ["es"]
    check_language_access(html, sl, rep, langs)

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
