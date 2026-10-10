# A sample run: three lessons against the rubrics

Three lesson requests, each run through `k12lessonplan` (and `k12presentation` where slides were
asked for), then judged row by row against the rubrics in this folder's parents. The point was
not a score. It was to find out which rows the skills fail, whether those failures belong to the
skills or to one unlucky lesson, and whether the fixes hold.

| Lesson | Request | Context the skill had | Files |
|---|---|---|---|
| [L1](L1-grade7-math/) | Grade 7 math, 7.RP.A.2a, proportional tables, with slides | A class profile (simulated): 50 minutes, Spanish and Vietnamese, four accommodations | packet, deck, plan |
| [L2](L2-grade4-science/) | Grade 4 science, 4-LS1-1, a bird-beak lab | Nothing: one clarifying round asked the period length and the learners | packet, plan |
| [L4](L4-grade3-ela/) | Grade 3 ELA, RL.3.2, the moral of a fable | Nothing: one round; the teacher named Arabic and readers below grade level | packet, plan |

The IDs skip L3: that lesson was run on a real class, and it was withdrawn so the sample uses no
real classroom. The one rule it changed (match the standard to the day, not the unit) stays in
`standards.md`.

Each folder holds the transcript (the clarifying round, the talk-through, and the plan as
delivered in chat), `packet.json` and the rendered packet, and for L1 the slides and the built
deck. Every row's verdict and its reason is in [`scores.csv`](scores.csv), written by
[`build_scores.py`](build_scores.py).

## Results

Rows whose condition did not hold are skipped, as the rubric README says. The deck was scored
against `deck.csv` as it stood then; P-D5 to P-D7, O-D8 and M-D2 came after this run and are not
in these rates, and P-D2, P-D4, O-D5 and O-D6 have been widened since, with no change to these
verdicts (neither deck has a game). The committed decks are builds of the template as it was
then, and the layout audit fails both on O-D8 as shipped. Rebuilt from `slides.html` with the
current template, L3 fits every screen from 1024x768 up, and L1 fails O-D8 on one slide: its
agree-or-disagree talk slide scrolls at 1366x657, carrying more than a laptop screen holds. Two rows could not be
tested here at all (below), so they are left out of the rates.

| | L1 | L2 | L4 | All |
|---|---|---|---|---|
| Run 1, as first generated | 49/59 | 45/48 | 44/47 | **138/154 (90%)** |
| Run 2, after fixing the skills | 58/59 | 47/48 | 46/47 | **151/154 (98%)** |

Fourteen run-2 passes are marked borderline in `scores.csv`: calls a stricter judge could flip,
each with the reason.

## What run 1 found

Sixteen fails on ten rows. The useful part is how they cluster: a row that fails in every
lesson is the skill's fault, not the lesson's.

| Row | Failed in | What happened | What changed |
|---|---|---|---|
| P3 Big Idea vs. SWBAT | all three | The Big Idea appeared in the talk-through but not in the plan as delivered | `SKILL.md`: the plan's first part carries the Big Idea and the "I can" as two lines |
| O13 Information density | all three | Look-fors written as running prose inside a block's paragraph | `SKILL.md`: look-fors as a numbered list, one line each (still failing, below) |
| O-C4 Essential questions only | L1, L2, L4 | The reflection prompt had no sentence stem, because `packet.md` said "two lines" and nothing more | `packet.md`: the reflection carries its stem |
| O-C3 Key words where they land | L1 | A word voted on before its definition, and a word defined but used in no task | `render_packet.py` now names any key word no task uses; `lesson_design.md`: define above the first task |
| O10, P-D1 Deck agrees with plan | L1 | Slide minutes summed to 61 in a 50-minute period; a 10-minute Discuss had a 6.5-minute timer | `check_deck.py` now sums the slides' minutes against the period |
| O-D4 Key words pictured | L1 | One key word had no word slide | `check_deck.py` now warns on it |
| O-M1 Work surface | L1 | Two "test every row and explain" tasks had ruled lines instead of room to work | `packet.md`: compute-then-explain gets a box with its stems above it |
| P-M4 Structural variety | L1 | The standard names tables and graphs; only tables had a task | `lesson_design.md`: every case the standard names gets a task |
| P-D3 Talk slides | L1 | A vote-and-revote and a partner compare had no reporter | `deck.csv` calibrated: a reporter is required when the move ends in a share |

Two bugs in `read_packet.py` turned up along the way, both in rebuilding a deck from a packet
file: a numbered list of directions was read as questions, and a plural key word was read as a second
word. Both are fixed.

## What is still failing

**O13, in all three.** The look-fors are now a list, but the plan's block notes still run four to
six sentences against the skill's own "two to four lines each." The rule is in the skill. The
model doesn't keep it. A firmer rule (three sentences a block, anything more as a sub-list) is
the likely fix, and it is untested.

## How far to trust these numbers

- **The same model generated and judged.** A judge grading its own work is generous in ways it
  can't see. Read the borderline calls in `scores.csv` with that in mind.
- **Run 2 was made knowing what failed.** It shows the fixes can be built, not that a fresh model
  would build them. The real test is the updated skills in a fresh chat, judged by a separate
  model, twice per output, as the rubric README recommends.
- **One row was calibrated after it failed.** P-D3's reporter requirement now applies only to a
  move that ends in a share. The reasoning is in the row's note; it is still a change made after
  seeing the result.
- **Two rows could not be tested here.** O-C2 (every task prints whole) needs `check_packet.py`,
  which needs LibreOffice, and LibreOffice cannot open files in this sandbox. O-D6 (photographs
  argue for the claim) needs Wikimedia Commons, which this environment's network policy blocks.
  The deck therefore fails the deck checker's photograph floor. That is the environment, not the
  deck, but it means the deck here has diagrams and charts where a classroom deck would also
  have photographs.
- **Three lessons is a small sample.** One grade band per subject; no high school, no social
  studies, no K-2, no multi-day lesson, no special education class, no IEP-modified standards.

## Reproducing it

Install the two skills from `my-skills/` (`my-skills/tools/package_skill.sh k12lessonplan`, then
the same for `k12presentation`), connect the Learning Commons Knowledge Graph, and send each
transcript's first teacher message in a fresh chat. For L1, put the class profile in the
project's knowledge first. Judge with the prompt in [the rubric README](../../README.md), passing
`shared.csv`, the subject's CSV, `classroom.csv`, and `deck.csv` when there is a deck.
