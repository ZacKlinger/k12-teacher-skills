#!/usr/bin/env bash
# Build the two branches offered to anthropics/k12-teacher-skills, from upstream main and this
# fork's working branch. Pushes nothing.
#
#   my-skills/tools/build_upstream_branches.sh [source-branch]
#
#   contrib/evals-calibration  upstream main + the rubric changes to the official skills' evals
#   contrib/classroom-skills   that + the opt-in k12-classroom plugin, its rubrics, the deck's browser
#                              checks (evals/k12presentation/harness) and the sample run
#
# Commits are authored by whoever runs it (git config user.name / user.email), which is what the
# CLA bot matches against. Re-running resets both branches. Then, when ready:
#   git push -u origin contrib/evals-calibration contrib/classroom-skills
set -euo pipefail

repo="$(git rev-parse --show-toplevel)"
src="${1:-$(git -C "$repo" rev-parse --abbrev-ref HEAD)}"
git -C "$repo" rev-parse --verify -q "$src" >/dev/null || { echo "no branch $src" >&2; exit 1; }
git -C "$repo" remote get-url upstream >/dev/null 2>&1 ||
  git -C "$repo" remote add upstream https://github.com/anthropics/k12-teacher-skills.git
git -C "$repo" fetch -q upstream main

wt="$(mktemp -d)"
cleanup() { git -C "$repo" worktree remove --force "$wt" >/dev/null 2>&1 || true; }
trap cleanup EXIT
git -C "$repo" worktree add -q -B contrib/evals-calibration "$wt" upstream/main
cd "$wt"

# ---------------------------------------------------------------- 1. the evals
git checkout -q "$src" -- \
  evals/k12-lesson-plan-creation/rubrics/shared.csv \
  evals/k12-lesson-plan-creation/rubrics/math.csv \
  evals/k12-lesson-plan-creation/rubrics/science.csv \
  evals/k12-lesson-differentiation/rubrics/differentiation.csv \
  evals/README.md
python3 - <<'PY'
# the README rows and conditions that only the classroom rubrics use wait for the second branch
p = "evals/README.md"; s = open(p).read()
for prefix in ("| k12lessonplan/rubrics/ |", "| k12presentation/rubrics/ |", "| `home-languages` |",
               "| `plan-in-chat` |", "| `class-context-available` |", "| `game-present` |"):
    lines = [l for l in s.splitlines(keepends=True) if l.startswith(prefix)]
    assert len(lines) == 1, prefix
    s = s.replace(lines[0], "", 1)
open(p, "w").write(s)
PY
git add -A
git commit -q -F - <<'MSG'
Evals: judge content where the teacher receives it, and let criteria bend

- Grading rules: student-facing criteria are judged against the student
  materials; teacher-facing criteria against wherever the teacher received
  the content, a document or the chat when the teacher asked for it there.
- O3 and O3b apply when an observation template was delivered.
- O5 asks for one Universal Design move per principle, not any two
  representation features.
- O16 (new): student directions readable at the class's stated level.
- M6 (new): learner needs shape the first draft.
- A row whose ID ends in -MC replaces its base row when its condition
  holds: P-M3-MC, R-M1-MC and P-S3-MC bend for classes working from
  modified standards without lowering the bar for anyone else.
- P-M3's floor scales for periods shorter than 50 minutes; P-S3 says
  pre-teaching a procedure, tool or word is not explanation.
- Run each judge at least twice per output.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG

# ---------------------------------------------------------------- 2. the plugin
git checkout -q -B contrib/classroom-skills
mkdir -p classroom-plugin/.claude-plugin classroom-plugin/skills
git archive "$src" my-skills/k12lessonplan my-skills/k12presentation | tar -x
mv my-skills/k12lessonplan my-skills/k12presentation classroom-plugin/skills/
rm -rf my-skills
for s in k12lessonplan k12presentation; do
  git show upstream/main:plugin/skills/k12-lesson-prep/LICENSE > "classroom-plugin/skills/$s/LICENSE"
  sed -i 's/^license: .*/license: "SPDX-License-Identifier: Apache-2.0. Complete terms in LICENSE."/' \
    "classroom-plugin/skills/$s/SKILL.md"
done
sed -i 's|https://github.com/ZacKlinger/k12-teacher-skills|https://github.com/anthropics/k12-teacher-skills|' \
  classroom-plugin/skills/k12presentation/scripts/find_photos.py
cat > classroom-plugin/.claude-plugin/plugin.json <<'JSON'
{
  "name": "k12-classroom",
  "version": "0.1.0",
  "description": "Two skills that plan from a class profile: a lesson planner that delivers a printable student packet and the lesson plan in chat, and an interactive HTML slide deck built from that packet, with talk timers, predict-then-reveal charts, games, and a short line in each home language.",
  "author": {
    "name": "ZacKlinger"
  }
}
JSON

git checkout -q "$src" -- evals/k12lessonplan evals/k12presentation evals/README.md
git show "$src":my-skills/profiles/sdc-science-profile.md \
  > evals/k12lessonplan/sample-run/L3-sdc-science/profile.md

python3 - <<'PY'
import json

def edit(path, old, new):
    s = open(path).read()
    assert old in s, (path, old[:60])
    open(path, "w").write(s.replace(old, new, 1))

p = ".claude-plugin/marketplace.json"
d = json.load(open(p))
d["plugins"].append({
    "name": "k12-classroom", "displayName": "K-12 Classroom",
    "description": "A lesson planner that reads the class profile before the first draft and delivers a printable student packet with the plan in chat, and a slide deck built from that packet to run the lesson from one computer. Install it instead of k12-education's lesson planner, not beside it.",
    "version": "0.1.0", "category": "education", "source": "./classroom-plugin"})
with open(p, "w") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write("\n")

edit("evals/k12presentation/README.md",
     "(`classroom-plugin/skills/k12presentation`, or\n`my-skills/k12presentation` in a fork that keeps its skills apart)",
     "(`classroom-plugin/skills/k12presentation`)")

edit("evals/k12lessonplan/sample-run/L3-sdc-science/transcript.md",
     "(my-skills/profiles/sdc-science-profile.md in this repository)", "(profile.md in this folder)")

p = "evals/k12lessonplan/sample-run/README.md"
s = open(p).read()
s = s[:s.index("## Reproducing it")] + """## Reproducing it

Install the `k12-classroom` plugin from this repository's marketplace (or upload each folder in
`classroom-plugin/skills/` as a skill in claude.ai), connect the Learning Commons Knowledge
Graph, and send each transcript's first teacher message in a fresh chat. For L1 and L3, put the
folder's `profile.md` in the project's knowledge first. Judge with the prompt in
[the rubric README](../../README.md), passing `shared.csv`, the subject's CSV, `classroom.csv`,
and `deck.csv` when there is a deck. `run_checks.py` in the folder above runs the skills' own
checkers over a lesson folder and writes the report the judge reads beside it.
"""
open(p, "w").write(s)
edit(p, "A real class profile, and the previous lesson read from Drive by its code",
     "A real class profile (`profile.md`), and the previous lesson read from Drive by its code")

edit("README.md", """## Layout

- `plugin/` - Main skill content bundled as a plugin; also includes teacher-focused 3rd party MCP servers that are available for users to enable""",
"""### K-12 Classroom (opt-in)

A second plugin in this marketplace, `k12-classroom`, plans from what a teacher has already said about the room: a class profile with the schedule, home languages, accommodations and Universal Design choices, and the previous lesson. It has two skills:
- `k12lessonplan`: Plans one session and delivers a printable student packet (Word, built to survive a Google Docs conversion) with the lesson plan in chat
- `k12presentation`: Builds the interactive HTML slide deck that runs the lesson from one classroom computer, from that packet, in the same chat or a later one

It is an alternative to `k12-lesson-plan-creation`, not an addition to it: install one planner or the other, so two skills don't compete for the same request.

```
claude plugin install k12-classroom@k12-teacher-skills
```

## Layout

- `plugin/` - Main skill content bundled as a plugin; also includes teacher-focused 3rd party MCP servers that are available for users to enable
- `classroom-plugin/` - The opt-in `k12-classroom` plugin""")
PY

git add -A
git commit -q -F - <<'MSG'
Offer an opt-in k12-classroom plugin: a profile-first planner and a deck

A second plugin in the marketplace, beside k12-education rather than in
it, so the official plugin and its lesson planner are unchanged:

- k12lessonplan plans one session from a class profile (schedule, home
  languages, accommodations, Universal Design choices, the previous
  lesson), asks at most one round of questions, talks the arc through
  before building, and delivers a Word packet built to survive Google
  Docs, with the plan in chat.
- k12presentation builds the HTML deck that runs the lesson from one
  computer: phased talk timers, predict-then-reveal charts, games,
  marked key words and language lines, checked against the packet.

Rubrics: evals/k12lessonplan/rubrics/classroom.csv (11 rows) and
evals/k12presentation/rubrics/deck.csv (17 rows), layered on shared.csv,
with four conditions documented in evals/README.md.

Browser checks: evals/k12presentation/harness builds fixture decks and
drives them in Chromium (layout at six screen sizes, every game format
by pointer, keyboard and clicker). It needs node and Playwright; run.sh
runs it all.

Sample run: four lessons (Grade 7 math, Grade 4 science, a grades 9-10
special day class build day, Grade 3 ELA) scored row by row: 193 of 214
before the skill fixes it found, 210 of 214 after, with the limits of a
self-judged run written down.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG

cd "$repo"
echo "built from $src:"
git log --format='  %h %an | %s' -2 contrib/classroom-skills
git diff --stat upstream/main contrib/classroom-skills | tail -1
echo "nothing pushed. When ready: git push -u origin contrib/evals-calibration contrib/classroom-skills"
