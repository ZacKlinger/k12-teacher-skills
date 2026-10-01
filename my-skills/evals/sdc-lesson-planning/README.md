# Evals for `sdc-lesson-planning`

A rubric for scoring what this skill makes, built from Anthropic and Learning Commons'
lesson-plan rubric (`evals/k12-lesson-plan-creation/rubrics/`) and changed where a special day
class needs it. Each criterion still passes or fails on its own, so a failing `SDC-R1` says the
page reads too hard, not that the lesson is bad.

## What changed from the upstream rubric

| | Criteria | Why |
|---|---|---|
| Kept as written | 36 shared, math and science criteria | They describe good teaching in any room |
| Kept, reworded | `O4`, `P9` | The plan is read in the chat; timing is judged at this room's pace |
| Bent with an SDC condition | `R1`, `R-M1`, `P-S3`, `O15` | Friendly numbers first, short explicit instruction before an investigation, and a plan in the chat are sound here; the condition keeps the criterion instead of dropping it |
| Replaced | `P-M3` by `SDC-T1`, `O5` by `SDC-U1` | Two talk moves of any length instead of a ten-minute Discuss block; one UDL move per principle instead of any two strategies |
| Dropped | `O3`, `O3b` | They required an observation template. A teacher who chose a lighter format failed them for the choice, not the teaching |
| New | `SDC-R1`, `SDC-R2`, `SDC-P1`, `SDC-L1`, `SDC-A1`, `SDC-D1`, `SDC-G1`, `SDC-M1`, `SDC-M2` | Readability, key words, print integrity through Google Docs, language lines, accommodations from the first draft, a deck that matches the packet, fair games, the whole plan in chat, continuity from the last lesson |

`rubric.csv` keeps the upstream columns and adds two: **Judged by** (the LLM judge, one of the
skill's scripts, or both) and **Source** (which upstream criterion it came from, or `new`).
Conditionals: `Math`, `Science`, `Game present`, and `SDC`, which every lesson from this skill
meets.

## Running it

1. **Make the lesson.** Run the skill on a real request ("Science 1.7 tomorrow: build the
   reservoir") and keep its outputs together in one folder: the packet `.docx`, the deck `.html`,
   the `packet.json` if you have it, and the final chat message saved as `plan.md`.
2. **Run the scripts.** They are the judge for anything that can be measured:

   ```bash
   python3 my-skills/evals/sdc-lesson-planning/run_checks.py path/to/lesson-folder
   ```

   This writes `checks.txt` with the render report (key words, reading level, language lines),
   the packet check (pages, fill, every task whole) and the deck check.
3. **Run the LLM judge** with the system prompt below. Give it `plan.md`, the packet's text (or
   its PDF), the deck's HTML, `checks.txt`, and `rubric.csv`.
4. **Track pass rates per criterion** across a handful of real requests (a math day, a science
   day, a block day, a multi-day request, a viewing guide), rather than one total score.

### Judge prompt

```
You are a careful evaluator of classroom materials for a grades 9-10 special day class (SDC):
students reading two to six years below grade level, many with attention or processing supports,
some learning English. Judge whether the lesson meets each rubric criterion.

You will receive:
  1. plan.md: the lesson plan, which this skill writes into the chat on purpose.
  2. The student packet (text or PDF) and the slide deck (HTML).
  3. checks.txt: what the skill's own checkers measured.
  4. The rubric.

Grading rules:
  - The lesson plan is plan.md. Judge every criterion about the plan against it; never fail a
    criterion because the plan is not a separate document.
  - Judge student-facing criteria against the packet and the deck: the content must be there,
    not only promised in the plan.
  - For a criterion whose "Judged by" names a script, read checks.txt first: an ERROR there fails
    the criterion; a clean report passes the measured part, and you judge the rest.
  - Skip a criterion whose Conditional doesn't apply (no game in the deck: skip SDC-G1). Every
    lesson here meets the SDC condition.
  - Pass means clearly and fully met. Fail means absent, incomplete, or only partly met.

Respond ONLY with a valid JSON array. Each element:
{"id": "...", "pass": true|false|null, "explanation": "one sentence"}  (null = skipped)
```

## Calibrating

When a result looks wrong, first decide whether the lesson or the criterion is wrong. If it's the
criterion, change its **What pass requires** here and note why in **Notes**. The SDC conditions
here are also the ones worth proposing upstream: the rubric already has a Conditional column for
`K-2-phonics` and `Gr8+-argument-writing`, and `SDC` or `modified-curriculum` would let these
criteria bend to the room without being dropped.
