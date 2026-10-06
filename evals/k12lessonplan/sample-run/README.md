# A sample run: four lessons against the rubrics

Four lesson requests, each run through `k12lessonplan` (and `k12presentation` where slides were
asked for), then judged row by row against the rubrics in this folder's parents. The point was
not a score. It was to find out which rows the skills fail, whether those failures belong to the
skills or to one unlucky lesson, and whether the fixes hold.

| Lesson | Request | Context the skill had | Files |
|---|---|---|---|
| [L1](L1-grade7-math/) | Grade 7 math, 7.RP.A.2a, proportional tables, with slides | A class profile (simulated): 50 minutes, Spanish and Vietnamese, four accommodations | packet, deck, plan |
| [L2](L2-grade4-science/) | Grade 4 science, 4-LS1-1, a bird-beak lab | Nothing: one clarifying round asked the period length and the learners | packet, plan |
| [L3](L3-sdc-science/) | Grades 9-10 special day class, an engineering build day, with slides | A real class profile, and the previous lesson read from Drive by its code | packet, deck, plan |
| [L4](L4-grade3-ela/) | Grade 3 ELA, RL.3.2, the moral of a fable | Nothing: one round; the teacher named Arabic and readers below grade level | packet, plan |

Each folder holds the transcript (the clarifying round, the talk-through, and the plan as
delivered in chat), `packet.json` and the rendered packet, and for L1 and L3 the slides and the
built deck. Every row's verdict and its reason is in [`scores.csv`](scores.csv), written by
[`build_scores.py`](build_scores.py).

## Results

Rows whose condition did not hold are skipped, as the rubric README says. The decks were scored
against `deck.csv` as it stood then; P-D5 to P-D7, O-D8 and M-D2 came after this run and are not
in these rates. Two rows could not be
tested here at all (below), so they are left out of the rates.

| | L1 | L2 | L3 | L4 | All |
|---|---|---|---|---|---|
| Run 1, as first generated | 49/59 | 45/48 | 55/60 | 44/47 | **193/214 (90%)** |
| Run 2, after fixing the skills | 58/59 | 47/48 | 59/60 | 46/47 | **210/214 (98%)** |

Sixteen run-2 passes are marked borderline in `scores.csv`: calls a stricter judge could flip,
each with the reason.

## What run 1 found

Twenty-one fails on twelve rows. The useful part is how they cluster: a row that fails in every
lesson is the skill's fault, not the lesson's.

| Row | Failed in | What happened | What changed |
|---|---|---|---|
| P3 Big Idea vs. SWBAT | all four | The Big Idea appeared in the talk-through but not in the plan as delivered | `SKILL.md`: the plan's first part carries the Big Idea and the "I can" as two lines |
| O13 Information density | all four | Look-fors written as running prose inside a block's paragraph | `SKILL.md`: look-fors as a numbered list, one line each (still failing, below) |
| O-C4 Essential questions only | L1, L2, L4 | The reflection prompt had no sentence stem, because `packet.md` said "two lines" and nothing more | `packet.md`: the reflection carries its stem |
| O-C3 Key words where they land | L1, L3 | A word voted on before its definition; a word defined but used in no task | `render_packet.py` now names any key word no task uses; `lesson_design.md`: define above the first task |
| O10, P-D1 Deck agrees with plan | L1 | Slide minutes summed to 61 in a 50-minute period; a 10-minute Discuss had a 6.5-minute timer | `check_deck.py` now sums the slides' minutes against the period |
| O-D4 Key words pictured | L1 | One key word had no word slide | `check_deck.py` now warns on it |
| O-M1 Work surface | L1 | Two "test every row and explain" tasks had ruled lines instead of room to work | `packet.md`: compute-then-explain gets a box with its stems above it |
| P-M4 Structural variety | L1 | The standard names tables and graphs; only tables had a task | `lesson_design.md`: every case the standard names gets a task |
| R3 Exit ticket, hardest case | L3 | The standard came from the profile's unit list, while the day's task met a different one | `standards.md`: match the standard to the day, not the unit |
| O-C1 Language lines | L3 | A context sentence got a Spanish line, which the skill says stays in English | Nothing new: the rule was already there |
| P-D3 Talk slides | L1 | A vote-and-revote and a partner compare had no reporter | `deck.csv` calibrated: a reporter is required when the move ends in a share |

Two bugs in `read_packet.py` turned up along the way, both in rebuilding a deck from a packet
file: a numbered list of directions was read as questions, and a plural key word ("flow rates")
was read as a second word. Both are fixed.

## What is still failing

**O13, in all four.** The look-fors are now a list, but the plan's block notes still run four to
eight sentences against the skill's own "two to four lines each." The rule is in the skill. The
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
  Both decks therefore fail the deck checker's photograph floor. That is the environment, not the
  deck, but it means the decks here have diagrams and charts where a classroom deck would also
  have photographs.
- **Four lessons is a small sample.** One grade band per subject; no social studies, no K-2, no
  multi-day lesson, no IEP-modified standards.

## Reproducing it

Install the two skills from `my-skills/` (`my-skills/tools/package_skill.sh k12lessonplan`, then
the same for `k12presentation`), connect the Learning Commons Knowledge Graph, and send each
transcript's first teacher message in a fresh chat. For L1 and L3, put the class profile in the
project's knowledge first. Judge with the prompt in [the rubric README](../../README.md), passing
`shared.csv`, the subject's CSV, `classroom.csv`, and `deck.csv` when there is a deck.
