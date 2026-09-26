# The slide deck

Start from `assets/deck_template.html`: copy it, keep the `<head>` and the closing `<script>`
exactly as they are, and replace the sample slides. The chrome — navigation, countdown, day tag,
packet chip, progress bar, jump menu — already works. Don't rewrite it, and don't position anything
by hand.

The deck does two jobs at once. It's what Zac teaches from, and it's what a student looks up at
when they've lost the thread of the packet.

---

## The skeleton every slide uses

```html
<section class="slide" data-day="Day 2" data-title="Do Now"
         data-packet="p. 1" data-timer="300" data-mins="5 min">
  <header class="head"><div class="eyebrow">Do Now · silent · on your own</div></header>
  <h2>The headline, six to twelve words.</h2>
  <div class="body"> …cards, a flow, a chart, stems, vocabulary, video… </div>
</section>
```

Three parts, in this order, on every slide:

1. **Head** — `.eyebrow` on the left says where we are in the period. The right side fills itself:
   the live countdown when the slide has `data-timer`, otherwise the plain `data-mins`. The packet
   chip is injected from `data-packet`. **Never place the time or the packet chip by hand** — hand
   placement is what used to collide with the eyebrow.
2. **Headline** (`h1`/`h2`) — the serif, regular weight, sentence case, six to twelve words. It
   states the point, not the topic: "Same lettuce, one twelfth of the water," not "Water usage."
3. **Body** (`.body`) — where the content actually lives, and it fills the middle band. **Cards and
   flows are the default**: parallel things go in cards, anything with a sequence or a cause goes in
   a flow, numbers go in a chart. Reach for a container before reaching for another sentence.

**Nothing goes under the body.** No summary line, no closing thought, no "here's why that
matters." If the cards, the flow, or the chart didn't land the point, another sentence won't fix
it — rebuild the body. A line of commentary at the bottom of every slide reads as filler, and after
three slides students stop looking at that part of the screen.

The two exceptions are `.es` and `.instruct`. `.es` is the Spanish line (below); `.instruct` is a
plain direction students can't get from the body itself —
*"One person per corner says why"*, *"Hand it to me at the door"*, *"Words you can use: water,
nutrients, soil."* A direction, never a conclusion. Most slides don't need one.

`.stand` — a quiet sans line under the headline — exists for the rare case where the body needs
setup it can't carry, like the source of a number. Use it sparingly and never alongside an
instruction.

**A headline alone is not a slide, and neither is a headline over a paragraph.** A student looking
at any single slide should learn something without hearing you say a word — and the way they learn
it is by looking at structure: three cards, four steps with arrows between them, two bars, a word
next to its non-example. The dark checkpoint is the one exception, one question meant to hang in
the air, and a lesson gets two of those at most.

The test for junk: if a line could be deleted and nothing on the slide would be harder to
understand, delete it. Labels that repeat a heading, a caption restating the chart it
sits under, a sentence summarizing the cards above it — all junk. Structure, not prose, carries a
slide.
---

## Spare is not the same as thin

Everything above this line tells you what to take away, and a deck built from subtraction alone
converges on sixteen slides of headline-over-nothing. Two of the three decks this skill has built
shipped with zero photographs; one had no charts either. Nothing in the rules was violated. That is
the failure this section exists to prevent.

**Spare** is a visual property: white ground, hairline rules, one pastel, no furniture. Keep it.
**Thin** is a content property: a student looks at the slide and there is nothing there to think
about. The house style is spare *so that* what remains can be dense — restraint is what buys the
attention, and then something has to be worth spending it on.

So every body owes the room a payload. Before a slide is done, name what a student gets from
looking at it for ten seconds without hearing your voice. If the honest answer is "the topic," it
isn't finished. The payload is one of:

- **A real number**, with its unit and its comparison. Not "uses less water" — *250 L versus 20 L*.
- **A photograph of the actual thing**, carrying a claim (`references/photographs.md`).
- **A structure with parts**: three cards that differ, four steps with arrows, two sides compared.
  Parallel boxes that all say roughly the same thing are one card wearing three hats.
- **A named specific**: this farm, this town, this plant, this year. Named things are rememberable
  in a way that categories are not.
- **A question with a hard edge** — one where a student could be wrong, and the wrongness would show.

### The test every slide has to pass

`references/design_method.md` carries the method behind the whole skill; two of its mindsets do
their work here, on each slide, and they are the fastest way to tell a finished slide from an
unfinished one.

**Show, don't tell.** The strongest version of any slide is the one where the evidence is on screen
and the sentence is unnecessary. Before writing a sentence, ask what could be shown instead — the
photograph, the two bars, the four steps. A sentence explaining a chart usually means the chart is
doing too little, not that the sentence is needed. Applied as a test: *cover the prose on this
slide. Does it still teach?* If yes, cut the prose. If nothing is left, the body was never there.

**Beginner's mind.** You know what a greenhouse looks like; the student does not. Every place the
slide assumes a picture the student doesn't have is a place a photograph goes. This assumption is
invisible from inside expertise — which is why it is a rule in `references/photographs.md` rather
than a judgement call.

**Focus on human values.** In this room that means the person in the photograph, the town the
number comes from, the worker whose job the machine changed. Abstractions are where students who
read slowly lose the thread; a person doing something is where they find it again.

---

## Language access

**Every slide that asks a question or gives a direction carries a Spanish line.** It goes directly
under the thing it supports — under the headline when the headline is the question, under the
`.instruct` when the direction is the instruction:

```html
<h2>How many football fields is that?</h2>
<p class="es">¿Cuántas canchas de fútbol americano son?</p>
…
<p class="instruct">Work with your partner. One paper between two.</p>
<p class="es">Trabajen en pareja. Una hoja para dos.</p>
```

A new word gets its Spanish inside the word cell, where the word is:

```html
<div class="vc word"><div class="k">Word</div><div class="w">Yield</div>
  <div class="say">say it: YEELD</div>
  <div class="es">rendimiento</div></div>
```

The line carries **the task, and nothing else**. Headlines that state a finding, card bodies,
captions, chart labels, stats, the standfirst — all stay English. A translated slide is two slides
of text where there was one, and text is the channel this room cannot use; a four-word Spanish line
under the question is what actually gets a newcomer into the work.

**Shorter than the English, always.** The checker warns when a Spanish line runs more than about a
fifth longer than the line above it, which is nearly always the framing having been translated
along with the task.

**It matches the packet, word for word.** The Spanish on a slide is the same Spanish that is on that
question in the packet. The whole deck-and-packet parity rule applies here too — a student looking
up from the page has to see the sentence they were just reading.

Plain everyday Spanish, `tú`-form imperatives. `check_deck.py` errors on a deck with no Spanish at
all, and warns on any slide that asks a question or sends students to the packet without it — that
warning is a judgement call when the slide only names a page number.

---


**A second home language** sits right under the Spanish, same class, marked with its code:
`<p class="es" lang="zh">写下你的答案。</p>`. Add `dir="rtl"` for Arabic, Farsi, Urdu, or Hebrew and
the rule flips to the right side. Run the checker with the room's languages,
`--languages es,zh`, and it errors on a language with no lines at all.
## What the type is doing

The look is spare on purpose: white ground, square corners, hairline rules, one pastel doing the
work on any given slide. Dark surfaces — the checkpoint slide, the vocabulary word cell, the
jump menu — use `--caviar`, a warm near-black. Don't reach for `--ink` there: it is a cool
grey tuned for body text on white, and at full-slide size on a projector it reads as navy. Nothing is boxed, shadowed, or rounded. Restraint is the house style —
the density lives in *what is said*, not in how much furniture surrounds it.

- Headlines, card titles, vocabulary words, numbers on charts: the **serif**, regular weight. It
  carries the things worth reading slowly.
- Standfirsts, card bodies, instructions, labels: the **sans**, quiet grey. It carries the things
  read at a glance.
- Eyebrows, section labels, the packet marker: small caps sans, letter-spaced, muted — orientation
  only, never emphasis.

When a slide looks wrong it is usually serif where the sans belongs, or a container that should
have been a hairline.

---

## Segmentation: one idea per slide

A slide carrying three moves at once loses a student who reads slowly. Break it:

- Directions with three steps → three cards on one slide, or three slides if each needs explaining.
- A question plus its sentence stems → one slide; the stems are that question's scaffold.
- A question plus a new word plus a data table → three slides.
- Anything you'd say "and then, also" about → the "also" is the next slide.

Roughly one slide per two to three minutes: a 60-minute period lands around 14-20 slides, a
90-minute block around 20-28.

---

## Components

| Component | Class | What it's for |
|---|---|---|
| **Cards** | `.cards` / `.card` | 2-4 parallel things: options, criteria, the shape of the period. Title plus one or two lines each. `.n` takes a small label (First / Then / Last, or 01 / 02 / 03) |
| **Flow** | `.flow` / `.step` / `.arrow` | Anything with a sequence or a cause: how a system works, the steps of a procedure, a chain from input to result. `.step.end` colors the outcome mint, `.step.problem` colors it peach. `.flow.stack` runs it vertically |
| Panel | `.panel` | A hairline, a label, and a source note above or under a chart. Use it only when the source genuinely needs saying — a chart with a caption usually stands alone |
| Vocabulary | `.vocab` | A new word: the word with how to say it, its meaning, and a non-example |
| Sentence stems | `.frames` | The frames from the packet, shown while students write |
| Big stats | `.stats` | 2-4 numbers that carry the point themselves |
| Static bars | `.bars` | A comparison you don't need to reveal interactively |
| Scale anchor | `.scale` | An abstract quantity as a count of something known — football fields, classrooms, bus rides, phone charges |
| Side by side | `.compare` | Two methods, two claims, before and after |
| Four corners | `.corners` | The four claims with where in the room each one lives |
| Talk slide | `.cards` + `.frames` | A talk move: the move's name, the question, who is Partner A, the stem, and the listener's job. Give it a timer |
| Figure | `.figure` + inline `<svg>` | A diagram drawn in SVG: flows, cross-sections, labeled parts |
| Video | `.body.media` + `.video-wrap` | An embedded, verified video. The body must carry `media` — that is what sizes the frame by height so it cannot overflow onto the text below it |
| Agenda | `.agenda` | The period at a glance, current block marked with `.now` |
| Checkpoint | `.slide.dark` | One question, nothing else |
| Spanish line | `.es` | The question or the direction in Spanish, abbreviated — see "Language access" |

**Photographs have their own reference** — `references/photographs.md` covers where one is
required, how to pick it so it argues for the slide's claim rather than merely matching the
topic, how to aim the crop, and the four patterns. Every deck carries five to eight in a
60-minute period. The CSS and the blocked-image fallback are already in the template; there is
nothing to paste in.

**Interactive charts are already in the template** — see `references/dataviz.md`. Every deck
carries at least one; `check_deck.py` treats a deck with none as an error. Any lesson touching a number gets two to four of them, usually inside a
`.panel`. That is the part of the deck doing the heaviest teaching in a room where reading is the
barrier.

**The scale anchor is the move worth reaching for.** "2.67 acres" means nothing to a 15-year-old;
"twelve football fields" means something immediately. Do the arithmetic first and state the
conversion on the slide.

---

## Timers

`data-timer` is seconds; `data-mins` is the label shown when there's no countdown. Timers never
start by themselves — Zac starts them with S or a click when the work actually begins, because a
countdown that starts while students are still finding their pencils is a countdown that lies.

Give a timer to anything with a fixed length: do-now, turn-and-talk, stations, independent work,
the closing. Don't put one on a discussion you might want to let run. Match the packet: 15 minutes
of partner math on the page is `data-timer="900"` on the slide.

---

## Videos

Every lesson gets one. It is the reliable attention reset in a period where reading is expensive,
and a deck without one is usually a deck that ran out of time rather than one that didn't need it.

Put the video in `<div class="body media">` — always. That class sizes the frame from the available
height rather than the width, which keeps it from spilling over whatever sits underneath. Nothing
else goes on a video slide except the link line.

**The template ships a click-to-play facade, not a bare iframe.** The markup carries the verified id
in `data-yt`, shows the YouTube poster image, and swaps in the real player when Zac clicks:

```html
<div class="body media">
  <div class="video-wrap" data-yt="dQw4w9WgXcQ">
    <button class="vfacade" type="button">
      <img src="https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
           alt="Title card showing a greenhouse interior with rows of lettuce under lights.">
      <span class="vbtn"></span>
      <span class="vhint">click to play · TED-Ed · 4 min</span>
    </button>
  </div>
  <p class="vlink">TED-Ed · 4 min ·
    <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" target="_blank" rel="noopener">open on YouTube</a>
    — use this link if the embed is blocked at school</p>
</div>
```

The reason is failure behaviour, and it is worth understanding rather than copying. A bare iframe
renders a **black rectangle** whenever the embed can't load — a filtered school network, a
sandboxed viewer, a room with no internet. Black tells you nothing and offers no way forward. The
facade degrades in stages instead: if the player is blocked you still have a poster and a link; if
the poster is blocked too it falls through to the same labelled card every other photo uses, and
the link is still there. It also means nothing loads from YouTube until someone asks it to, which
is faster and quieter on privacy.

`autoplay=1` is added by the script, after a click. Never put it in the markup — a deck that starts
playing on slide change is a deck that talks over you.

**Verify the id against a real search result, every time.** An id that doesn't resolve looks
identical in the file to one that does; the difference only shows up in front of the class. The
plain link under the frame is not optional for the same reason.

**Print the runtime.** Anything over about six minutes gets a stop-point rather than a full play,
and the eyebrow states the purpose before it plays — *"count what they say they don't need."*

## Before you call it done

Run the checker first — it catches the things that have actually gone wrong before
(no photographs, duplicate photographs, missing captions, the fallback script absent,
template placeholder text left in, base64 bloat, un-aimed crops):

```bash
python3 scripts/check_deck.py "$OUTPUT_DIR/<topic>_deck.html" --minutes <60 or 90>
```

`--minutes` must be the real period length: the slide bounds (14-20 / 20-28) and the photograph
floor (5-8 / 8-12) are both derived from it.

Fix every error and re-run until it exits clean. Then read the warnings and decide about each
one — they are judgement calls, not noise. The checker cannot see whether a photograph is the
*right* photograph, so the eyes-on checks below still matter:

- Click through every slide: no slide is a bare headline, nothing overlaps the head, and no slide
  carries a summary line under its body.
- Every writing slide has `data-packet`; every packet question appears on some slide.
- Every question and every direction has its Spanish line, and it says the same thing as the
  Spanish on that question in the packet.
- The video is a facade with a real 11-character `data-yt`, a poster with real alt text, and the
  plain link under it. Click it once and confirm the player actually appears.
- Dark surfaces are `--caviar`, not `--ink`.
- Timer seconds match the packet's minutes, and the phases sum to the period.
- Every interactive chart works: starts empty, each click does what it should, the caption lands
  at the end, and the numbers match the packet answer key.
- New words appear as `.vocab` slides at the moment they're first used, and the packet repeats the
  same wording.
- The deck is a single HTML file with no sidecar folder. Photographs and the video are
  linked by URL — that is expected, and inlining them as base64 is not (it once produced a
  1.9 MB deck). See `references/photographs.md`.
