# k12presentation evals

Two kinds of check for the slide-deck skill (`classroom-plugin/skills/k12presentation`, or
`my-skills/k12presentation` in a fork that keeps its skills apart).

## `rubrics/deck.csv`

The LLM-as-judge rubric for a delivered deck, in the same format as the other rubrics in this
folder's parent; [the rubric README](../README.md) says how to run it. `O-D8`, whether every slide
fits a classroom screen, is deterministic: `harness/layout_audit.js` on the delivered deck fails any
slide that runs under the footer, spills off the side, or scrolls at 1024x768 or larger, and any
FAIL line fails the row. `evals/k12lessonplan/run_checks.py` runs it beside the deck checker when
node and Playwright are installed, so the judge gets both reports.

## `harness/`: does it fit, and does it play

A rubric can't see whether a slide runs under the footer on a laptop presenting in a browser
window, or whether a card dragged to the bottom of a list actually lands there. The harness builds
four fixture decks and drives them in Chromium:

| Check | What it proves |
|---|---|
| `checker_test.py` | The two gallery decks (every pre-existing slide type; every interactive format) build clean, and the deck of broken configs raises every error it should, without the checker crashing. |
| `layout_audit.js` | At 800x600, 1024x768, 1280x720, 1280x800, 1366x657 and 1920x1080, every slide, opened and played (charts revealed, games answered, cards placed), stays off the footer, inside the screen, and inside its body, and from 1024x768 up never falls back to scrolling. The gallery includes a full talk move (the packet's long question, a language line, four turns, a stem, a picker) that must fit. |
| `interactions.js` | Real mouse drags, taps, keys and a clicker's → and ← on every interactive format, and the keyboard alone (Tab, Enter, Space, arrows) on the drag games: hand counts and the hinge tally, drag-to-reorder, placing on a number line with lanes, the estimate's markers and reveal, which-one-doesn't-belong reasons, find the mistake, the true-or-false run with → alone and read-aloud, drawing and checking match lines, the what-if's predict-first cover, the zoom-in's steps, label-the-photo, a dark slide. |
| `edge_cases.js` | The cases a review found, pinned: charts revealed by a clicker one stage at a time, key words never marking a game option, a scrolling slide keeping its clock, a game on the first or last slide survives a double press, a game held back by a build step waits for it, a clicked button gives the keyboard back, fraction ticks and fraction card values land at their value, a what-if that peaks mid-range still scales its bar, bare photo tiles in which-one-doesn't-belong, dragging from a photo card in a match. (Its deck only exercises edge cases; the lesson-level checker errors it gets are expected.) |
| `review_board.js` | The Jeopardy board fills one screen at every size with no scrolling, and → reveals then closes a clue. |

Run everything:

```bash
evals/k12presentation/harness/run.sh            # builds into a temp folder
evals/k12presentation/harness/run.sh evals/k12presentation/harness/out/   # or into harness/out/
```

It needs `python3`, `node` and Playwright with Chromium (`npm i -g playwright && npx playwright
install chromium`; set `CHROMIUM_PATH` to use a Chromium already on the machine, and `K12_SKILL`
to test a copy of the skill somewhere else). The fixtures use local SVG stand-ins for photographs
so the checks run offline, and carry Spanish lines, so they are built with `--languages es`; the
gallery slide files in `harness/fixtures/` double as a catalogue of every format's markup.

Run it after any change to `assets/deck_template.html`, `assets/review_game_template.html` or
`scripts/check_deck.py`, and add a fixture slide and an interaction test with any new format.
