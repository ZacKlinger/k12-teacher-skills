---
name: "k12presentation"
description: "Builds the interactive HTML slide deck a K-12 teacher projects to run a lesson: real photographs found on Wikimedia without a browser, phased talk timers, predict-then-reveal charts, game rounds, sorts, hinge questions, matching, ordering, number lines, what-if models and other whole-class games a clicker can run, key words marked, and a home-language line on every question when the class has home languages, all in one file that runs from the teacher's computer with no student devices. k12lessonplan calls it when slides are asked for with a lesson; use it directly whenever a teacher wants slides from something they already have, above all a student packet k12lessonplan made (the .docx, or its Google Doc downloaded as Word): \"make slides for this packet\", \"turn this lesson plan into a deck\", \"slides for the viewing guide\", \"add a game slide\", \"a Jeopardy review for unit 1\", \"a matching game for the vocab\", a Google Doc or PDF of a lesson. Do NOT use it to plan a lesson from scratch or to make the printed packet; that is k12lessonplan."
license: MIT
---

# k12presentation

Builds the deck a teacher teaches from: one HTML file, opened in a browser on the classroom
computer and projected, that runs the lesson. It carries real photographs, timers, talk slides
whose turns chime, interactive charts, game rounds and sorts, the lesson's key words marked, and,
when the class has home languages, one short line in each under every question and direction.
"The teacher" is the person you are talking with. Everything runs from their one computer: big
targets, keyboard keys, nothing that needs a student device, an account, or a student's name.

The deck does two jobs at once. It is what the teacher teaches from, and it is what a student looks
up at when they've lost the thread of the packet. So it is the packet seen on the wall: the same
questions in the same words, the packet page named on every slide that asks students to write.

---

## Where the lesson comes from

Take the first of these that applies, and build from it alone:

1. **k12lessonplan, in this conversation**, whether it called this skill at its build step or
   the teacher took up its offer of a deck afterwards. Build from what it left: `packet.json`
   (every task's exact wording, any language lines, the key words in `meta.vocab`, the lesson's
   name, the minutes, the languages) and the plan it wrote into the chat (the agenda, the talk moves, the
   photographs it promised by subject, the video). Every slide comes from those. Don't re-plan,
   don't reword a question, don't add a task the packet doesn't have.
2. **A packet k12lessonplan made, in a later conversation**: the packet `.docx`, or its
   Google Doc downloaded as Word (File › Download › Microsoft Word), usually with the plan pasted
   beside it. Read it first:

   ```bash
   python3 scripts/read_packet.py "<name> - packet.docx"
   ```

   It prints the lesson's name, the timed sections, every numbered question with its language
   lines, and the key words, read from the page as printed, so an edit the teacher made in Docs is
   the wording the deck carries. Then build exactly as in 1, passing the `.docx` itself to `--packet`.
   The minutes come from the packet's section headings; the talk moves, photographs and video
   from the pasted plan. With no plan, choose those yourself from the packet's tasks and name them
   in the three lines you say before building.
3. **Any other lesson the teacher has**: a Google Doc, a PDF, a pasted plan, a packet from last
   year. Read
   it once and pull out the objective, the agenda with minutes, every task in its own words, the key
   words, and the moments students talk. Say in three lines what you found and the deck you're
   about to build, then build. Ask only what the document and the profile can't answer, and never
   more than one round: usually just the period length, which the profile's schedule answers when
   there is a class profile (`project-profile.md` in the working folder, or the project's
   knowledge). The profile also says whether the class has home languages.
4. **Just slides**: pause slides for a viewing guide, a review game, one game slide to add to a
   deck. Build exactly that (the "Shapes" section below).

---

## Read before building

- `references/deck.md`: the slide skeleton, the component catalog, talk slides, games, key words,
  timers, video, and the checklist before you call it done.
- `references/slide_criteria.md`: what a good slide is made of, seen from the back row.
- `references/photographs.md`: the deck carries real photographs and they are not optional. The
  claim-first method lives there, and it is the difference between photographs that argue for the
  lesson and photographs that merely sit near it.
- `references/interactives.md`: the games beyond the game round and the sort, and why each one
  works for this room: hinge question, true or false, order it, number line, estimate, match, which
  one doesn't belong, find the mistake, what if, zoom-in, label the photo. Read it whenever a moment
  in the lesson asks students to *do* something with an idea, and pick the format by that verb.
- `references/dataviz.md`: the chart kit. Every deck carries at least one interactive chart, two to
  four whenever the lesson touches a number, which is nearly always. For any student for whom
  reading is the barrier, a chart they can interpret carries more of the lesson than any paragraph,
  and each one is predicted before it's revealed.

---

## Build

Write only the slides, the `<section class="slide">` elements in order, to `slides.html`, using the
components in `references/deck.md`. Don't open or copy `assets/deck_template.html`: `build_deck.py`
puts the slides inside it, and the template already carries the navigation, the per-slide timers,
the photo styles and zoom, the blocked-image fallback, click-to-play video, the chart kit, the
talk kit, the games and the key-word marks.

```bash
python3 scripts/build_deck.py slides.html "$OUTPUT_DIR/<name> - deck.html" \
  --title "<name>" --minutes <period length> --packet packet.json
```

`--packet` reads the key words and the languages from the packet's `meta` and checks the deck
against the packet: every question is on a slide in the packet's own words. It takes
`packet.json` or the packet `.docx` itself. With neither, pass `--vocab "reservoir,pump"` and,
when the class has home languages, `--languages es,vi`. Add `--teams 3` (or team names) only when
the teacher asks for teams; see "Games" below.

It writes the deck and runs the checker in one step. The teacher opens the deck as a local file in
a browser, not in the chat's preview, so everything in it works from a file, which the template
does.

**Every talk move gets its slide.** Every lesson runs at least two student-talk moves, and each one
in the plan gets a talk slide built the way `references/deck.md` "Talk slides" describes, with the
thing students talk about on it. A game run as talk (partners agree on the timer before anyone
answers) counts as one.

**Use a game where it earns its place**, chosen by what students should do with the idea: a game
round for a fair guess, a hinge question before independent work, a sort to classify, order it for
a procedure, a number line or an estimate for a quantity, a match for vocabulary, which one doesn't
belong for an argument, find the mistake for the error the class always makes, a what-if for cause
and effect, a zoom-in to open (`references/deck.md`, "Games", and `references/interactives.md`).
HTML can do what paper can't: let every guess in the room count, hold the answer until the room has
committed, and let a student walk to the board and move the idea. Two to four in a period, one per
slide.

**Games have no teams and no points unless the teacher asks for them.** When they do, `--teams`
puts one scoreboard in the footer of every slide, carrying the period's running total from game to
game.

**Every deck carries at least one interactive chart**, two to four when the lesson has numbers in
it. Where reading is the barrier, the chart is the explanation and the words are its caption.

Pass the real period length. The slide count and the photograph floor both scale off it, so a
90-minute deck checked at 60 gets told it has too many slides, and a checker that is wrong once is
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

Two rules that hold on every build. **Photographs never depend on the teacher**: never ask them for
one and never wait on an upload. **No browser tab, ever, for photographs**: `scripts/find_photos.py`
searches Commons from the sandbox, lays every slot's candidates out as one numbered image,
load-tests the pick, and previews its crop, so a deck's photographs cost one search and one look
per slot.

---

## Language access

**When the class has home languages, every question and every direction on a slide carries one
short line in each**, under the English, as `<p class="es" lang="vi">` (the class marks a language
line; the `lang` names the language, in the profile's order). Not a translated deck: a single line
that says what to do and what is being asked. Slide headlines that aren't questions, captions,
chart labels and stems stay in the language of instruction. When the deck comes from a packet, the
line on a slide is the packet's line for the same question, word for word, and the languages come
from the packet. With no home languages, there are no lines. `check_deck.py` errors when a listed
language has no lines; read the lines end to end yourself, since the checker knows they exist and
are short but not that they say the task.

---

## Shapes

- **A lesson deck**: everything above.
- **Viewing guide**: one pause slide per stop, carrying that stop's question, its language line and
  a timer, and nothing that competes with the footage. Timestamps come from the verified video's
  transcript or chapters, never from memory.
- **A review game board**: a Jeopardy-style board from `assets/review_game_template.html`; see
  `references/deck.md`, "A whole review game". Name it by the lesson's name,
  `Science 1.6 - Review game.html`.
- **One slide to add**: build it with the same components and hand it over as the
  `<section>` to paste, or rebuild the deck with it in place when you have the deck's `slides.html`.

---

## Before you hand it over

`scripts/check_deck.py` runs inside the build and enforces the mechanical rules: photo count,
duplicates, alt text, captions, credits, aimed crops, the fallback script, leftover placeholder
text, base64 bloat, empty bodies, talk moves, game data, key words, the packet's questions. Get it
clean, then decide about every warning. Then:

```bash
python3 scripts/find_photos.py probe "$OUTPUT_DIR/<name> - deck.html"
```

so every photograph is known to load and YouTube confirms the video will play inside the deck.

The questions nothing automated asks for you: *does every photograph argue for the claim on its
slide*; *would a student looking at any single slide for ten seconds, hearing nothing, come away
with something*; and *do the numbers on the slides, the game answers and the sort bins agree with
the answer key*. The closing checklists in `references/deck.md` and `references/photographs.md`
cover the rest.

## Hand it back

Name the file and say to open it in a browser (it is built in and used from Chrome). When the
deck has games, add one line: a presentation clicker runs it, since → reveals each game's answer
before it moves on. If the
photographs could not be load-tested this session, say so in one line and name the fix: network
access to `commons.wikimedia.org` and `upload.wikimedia.org` for Claude's sandbox. A copy kept in
Drive is for keeping: Drive previews an HTML file as its code, so presenting from Drive means
downloading the file and opening it in a browser. Everything a slide needs is inside the file or linked by URL, so it works from the working
folder, a Drive download, or a USB stick; never point a slide at a local file.

When k12lessonplan called this skill, hand back to it quietly: it delivers the files and the
plan together. Keep the machinery invisible either way. Say "slide deck", never "template" or
"checker".
