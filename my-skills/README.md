# Classroom skills: `k12lessonplan` and `k12presentation`

Two Claude skills that plan a K-12 lesson from what a teacher has said about the class, then
build the materials to teach it. They sit beside Anthropic and Learning Commons' K-12 skills in
this repository and are judged against the same rubrics.

| Skill | What it does | What it delivers |
|---|---|---|
| [`k12lessonplan`](k12lessonplan/SKILL.md) | Plans one class session from the class profile (period length, reading levels, home languages, IEP and 504 supports), talks the arc through in chat, then builds | The lesson plan, in chat, and a student packet as a Word document that prints cleanly from Word or Google Docs |
| [`k12presentation`](k12presentation/SKILL.md) | Builds the deck that runs the lesson from one classroom computer, from the packet, in the same chat or a later one | One HTML file: photographs, phased talk timers, predict-then-reveal charts, games a clicker can run, key words marked, and, when the class has home languages, a line in each under every question |

## How they fit together

The packet is the contract between the two. The deck asks the packet's questions in the packet's
words, and every slide that asks students to write names the packet page. `read_packet.py` reads a
packet `.docx`, including one exported from Google Docs, back into structured form. That way a deck
built in a later conversation is held to the page as printed, and a question reworded in Docs is
the wording the deck is checked against.

Each skill ships checkers that enforce what its instructions only state: reading level, key words
that no task uses, slide minutes against the period, every packet question present on a slide.

## Layout

```
my-skills/
  k12lessonplan/        SKILL.md, references/, assets/ (class profile template),
                        scripts/ (render_packet.py, check_packet.py)
  k12presentation/      SKILL.md, references/, assets/ (deck and game templates),
                        scripts/ (build_deck.py, check_deck.py, find_photos.py, read_packet.py)
  tools/                package_skill.sh, build_upstream_branches.sh, usage_report.py
evals/k12lessonplan/    rubrics/classroom.csv, run_checks.py, and a scored sample run
evals/k12presentation/  rubrics/deck.csv and a browser harness for layout and interaction
```

## Install

**claude.ai:** package each skill, then upload both zips under Settings › Capabilities › Skills.

```bash
my-skills/tools/package_skill.sh k12lessonplan
my-skills/tools/package_skill.sh k12presentation    # zips land in my-skills/dist/
```

**Claude Code:** copy `k12lessonplan/` and `k12presentation/` into `~/.claude/skills/`.

Then give each class a profile: fill in
[`project_profile_template.md`](k12lessonplan/assets/project_profile_template.md) once and add
it to the project's knowledge. Without one, the planner asks what it needs in a single round.

## Requirements

- Python 3 with `python-docx` and Pillow: `pip install -r my-skills/requirements.txt`
- Optional: LibreOffice and poppler (`pdftoppm`). `check_packet.py` uses them to measure how the
  packet prints and skips that check, saying so, when they are missing.
- For the deck harness in `evals/k12presentation/harness/`: Node and Playwright with Chromium.

## Evaluating

- **Checkers:** `python3 evals/k12lessonplan/run_checks.py <lesson-folder>` runs both skills'
  checkers over one lesson and writes the report an LLM judge reads beside it.
- **Rubrics:** `shared.csv` plus the subject's rubric, then `classroom.csv`, and `deck.csv` when
  there is a deck. [`evals/README.md`](../evals/README.md) gives the judge prompt and the rules.
- **Sample run:** three lessons scored row by row, 138 of 154 rows passing before the fixes the run
  prompted and 151 of 154 after. The [run's README](../evals/k12lessonplan/sample-run/README.md)
  says how far to trust those numbers.

## Offering them upstream

`tools/build_upstream_branches.sh` builds two branches from Anthropic's `main`: one with the
rubric calibrations, one adding these skills as an opt-in `k12-classroom` plugin. It pushes
nothing. Run it yourself so the commits carry your name, which is what the contributor license
check matches.

## License

The two skills are released under the [MIT License](LICENSE). The rubrics and evals in
[`evals/`](../evals/) adapt Anthropic and Learning Commons' Apache-2.0 rubrics and remain under
the repository's [LICENSE](../LICENSE) and [NOTICE](../NOTICE).
