---
name: "sdc-slideshow"
description: "Builds the interactive HTML slide deck for Zac's SDC (special day class) grades 9-10 science and math: real photographs found on Wikimedia without a browser, phased talk timers, interactive charts, game rounds and sorting games, key words marked, a language line on every question, all in one file he opens in Chrome. sdc-lesson-planning calls it at its build step with the packet and plan; use it directly whenever Zac wants slides from something he already has: \"make slides for this packet\", \"turn this lesson plan into a deck\", \"slides for the viewing guide\", \"add a game slide\", \"a Jeopardy review for unit 1\", a Google Doc or PDF of a lesson. Do NOT use it to plan a lesson from scratch or to make the printed packet; that is sdc-lesson-planning."
license: MIT
---

# SDC slideshow (grades 9-10, science and math)

Builds the deck Zac teaches from: one HTML file, opened with **Open in Chrome** and projected, that
runs the lesson. It carries real photographs, timers, talk slides whose turns chime, interactive
charts, game rounds and sorts, the lesson's key words marked, and one short language line under
every question and direction. Zac is the teacher, "you" in these instructions.

The deck does two jobs at once. It is what Zac teaches from, and it is what a student looks up at
when they've lost the thread of the packet. So it is the packet seen on the wall: the same
questions in the same words, the packet page named on every slide that asks students to write.

---

## Where the lesson comes from

Take the first of these that applies, and build from it alone:

1. **sdc-lesson-planning, in this conversation.** It hands over at its build step: `packet.json`
   (every task's exact wording, the language lines, the key words in `meta.vocab`, the lesson code,
   the minutes, the languages) and the plan it wrote into the chat (the agenda, the talk moves, the
   photographs it promised by subject, the video). Every slide comes from those. Don't re-plan,
   don't reword a question, don't add a task the packet doesn't have.
2. **A lesson Zac already has**: a Google Doc, a PDF, a pasted plan, a packet from last year. Read
   it once and pull out the objective, the agenda with minutes, every task in its own words, the key
   words, and the moments students talk. Say in three lines what you found and the deck you're
   about to build, then build. Ask only what the document and the profile can't answer, and never
   more than one round: usually just the period length, which the profile's schedule answers when
   there is a profile (`project-profile.md` in the working folder).
3. **Just slides**: pause slides for a viewing guide, a review game, one game slide to add to a
   deck. Build exactly that (the "Shapes" section below).

---

## Read before building

- `references/deck.md`: the slide skeleton, the component catalog, talk slides, games, key words,
  timers, video, and the checklist before you call it done.
- `references/slide_criteria.md`: what a good slide is made of, from the back row of this room.
- `references/photographs.md`: the deck carries real photographs and they are not optional. The
  claim-first method lives there, and it is the difference between photographs that argue for the
  lesson and photographs that merely sit near it.
- `references/dataviz.md`: the chart kit. Every deck carries at least one interactive chart, two to
  four whenever the lesson touches a number, which is nearly always. Reading is the barrier in
  this room; a chart a student can interpret carries more of the lesson than any paragraph, and
  each one is predicted before it's revealed.

---

## Build

Write only the slides, the `<section class="slide">` elements in order, to `slides.html`, using the
components in `references/deck.md`. Don't open or copy `assets/deck_template.html`: `build_deck.py`
puts the slides inside it, and the template already carries the navigation, the per-slide timers,
the photo styles and zoom, the blocked-image fallback, click-to-play video, the chart kit, the
talk kit, the games and the key-word marks.

```bash
python3 scripts/build_deck.py slides.html "$OUTPUT_DIR/<code> - <short title> - deck.html" \
  --title "<code> · <short title>" --minutes <period length> --packet packet.json
```

`--packet` reads the key words and the languages from the packet's `meta` and checks the deck
against the packet: every question is on a slide in the packet's own words. Without a
`packet.json`, pass `--vocab "reservoir,pump"` and `--languages es` instead. Add `--teams 3` (or
team names) only when Zac asks for teams; see "Games" below.

It writes the deck and runs the checker in one step. Zac opens the deck as a local file in Chrome,
not in the chat's preview, so everything in it works from a file, which the template does.

**Every talk move gets its slide.** Every lesson runs at least two student-talk moves, and each one
in the plan gets a talk slide built the way `references/deck.md` "Talk slides" describes, with the
thing students talk about on it. A game run as talk (partners agree on the timer before anyone
answers) counts as one.

**Use a game where it earns its place**: a game round for a fair-guess question, a sort for anything
students can classify with their hands (`references/deck.md`, "Games"). HTML can do what paper
can't: let every guess in the room count, and let a student walk to the board and move the idea.

**Games have no teams and no points unless Zac asks for them.** When he does, `--teams` puts one
scoreboard in the footer of every slide, carrying the period's running total from game to game.

**Every deck carries at least one interactive chart**, two to four when the lesson has numbers in
it. In a room where reading is the barrier, the chart is the explanation and the words are its
caption.

Pass the real period length. The slide count and the photograph floor both scale off it, so a
block-day deck checked at 60 gets told it has too many slides, and a checker that is wrong once is
a checker that gets ignored after that.

---

## Photographs

`references/photographs.md` governs them end to end: where one is required, how to choose it so it
argues for the slide's claim instead of merely matching the topic, how to aim the crop, how to
judge what came back, and the four patterns.

The two things worth carrying in your head: **write the claim and the frame test before you
search**, because a search for the topic returns pictures of the topic and none of them argue for
anything; and **the load probe is not the quality gate**, because bytes arriving says nothing about
whether the subject is in frame.

Two rules that hold on every build. **Photographs never depend on Zac**: never ask him for one and
never wait on an upload. **No browser tab, ever, for photographs**: `scripts/find_photos.py`
searches Commons from the sandbox, lays every slot's candidates out as one numbered image,
load-tests the pick, and previews its crop, so a deck's photographs cost one search and one look
per slot.

---

## Language access

**Every question and every direction on a slide carries one short line in each home language**,
under the English, as `<p class="es">` (with `lang="zh"` and so on for the others, in the profile's
order). Not a translated deck: a single line that says what to do and what is being asked. Slide
headlines that aren't questions, captions, chart labels and stems stay English. When the deck comes
from a packet, the line on a slide is the packet's line for the same question, word for word.
`check_deck.py` errors on a deck with no language lines; read the lines end to end yourself, since
the checker knows they exist and are short but not that they say the task.

---

## Shapes

- **A lesson deck**: everything above.
- **Viewing guide**: one pause slide per stop, carrying that stop's question, its language line and
  a timer, and nothing that competes with the footage. Timestamps come from the verified video's
  transcript or chapters, never from memory.
- **A review game board**: a Jeopardy-style board from `assets/review_game_template.html`; see
  `references/deck.md`, "A whole review game". Name it by the lesson code,
  `Science 1.6 - Readiness game.html`.
- **One slide to add**: build it with the same components and hand it over as the
  `<section>` to paste, or rebuild the deck with it in place when you have the deck's `slides.html`.

---

## Before you hand it over

`scripts/check_deck.py` runs inside the build and enforces the mechanical rules: photo count,
duplicates, alt text, captions, credits, aimed crops, the fallback script, leftover placeholder
text, base64 bloat, empty bodies, talk moves, game data, key words, the packet's questions. Get it
clean, then decide about every warning. Then:

```bash
python3 scripts/find_photos.py probe "$OUTPUT_DIR/<code> - <short title> - deck.html"
```

so every photograph is known to load and YouTube confirms the video will play inside the deck.

The questions nothing automated asks for you: *does every photograph argue for the claim on its
slide*; *would a student looking at any single slide for ten seconds, hearing nothing, come away
with something*; and *do the numbers on the slides, the game answers and the sort bins agree with
the answer key*. The closing checklists in `references/deck.md` and `references/photographs.md`
cover the rest.

## Hand it back

Name the file and say "Open in Chrome". If the photographs could not be load-tested this session,
say so in one line and name the fix: network access to `commons.wikimedia.org` and
`upload.wikimedia.org` for Claude's sandbox. A copy kept in Drive is for keeping: Drive previews an
HTML file as its code, so presenting from Drive means downloading the file and opening it in
Chrome. Everything a slide needs is inside the file or linked by URL, so it works from the working
folder, a Drive download, or a USB stick; never point a slide at a local file.

When sdc-lesson-planning called this skill, hand back to it quietly: it delivers the files and the
plan together. Keep the machinery invisible either way. Say "slide deck", never "template" or
"checker".
