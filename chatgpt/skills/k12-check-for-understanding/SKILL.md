---
name: k12-check-for-understanding
description: >
  Creates a Check for Understanding (CFU) for a math topic or standard: 1–3 targeted formative items
  whose distractors come from documented student misconceptions, plus a teacher guide routing each
  likely response to a specific next instructional step. Load BEFORE asking any clarifying question
  about grade, standard, or topic. This skill is for math; for other subjects, help as you normally
  would and don't mention the skill to the user. Triggers on asks to create, write, generate, or
  design a check for understanding, formative check, quick check, or exit ticket for a math concept
  or standard, and on implicit signals like "I need to see who got it before I move on." Not a
  quiz, test, or practice set: a CFU is read for what it reveals, not scored, so a numbered quiz
  or a bare answer key is a different job. Does not create a lesson (k12-lesson-plan-creation,
  which brings its own exit ticket), tier one (k12-lesson-differentiation), or prepare a teacher to
  teach one (k12-lesson-prep).
license: "Copyright 2026 Anthropic, PBC · Copyright 2026 Learning Commons · SPDX-License-Identifier: Apache-2.0. Complete terms in LICENSE and NOTICE."
compatibility: "ChatGPT edition. Needs ChatGPT's code environment (Python 3) to write the two printable files. The Learning Commons Knowledge Graph plugin is optional."
---

# K-12 Check for Understanding

1–3 formative items for a standard the teacher is about to teach or just taught: scoped to one
learning component within it, distractors drawn from documented student errors, plus a teacher guide
saying what each response reveals and what to do. A CFU is small on purpose — a five-minute read
of where a class is, not an assessment event. "The teacher" is the user you're talking with.

**Asset-based language everywhere**, in both files and every chat message. No "weak," "fragile,"
"can't," "behind," "deficient," "low," "struggling," "failing." Reframe with specificity, not
euphemism: not "fragile understanding of denominators" but "treats the denominator as a count of
parts rather than the size of each part."

---

## Running in ChatGPT

This edition runs in ChatGPT's code environment. Five facts about it shape every step below.

- **Paths.** `references/…` live in this skill's folder, called `SKILL_DIR` below: the folder
  holding this SKILL.md. If you don't already know it, find it once with
  `ls -d /home/oai/skills/k12-check-for-understanding* 2>/dev/null || find / -path /proc -prune -o -path '*k12-check-for-understanding*/SKILL.md' -print 2>/dev/null`.
  Both files the teacher downloads go in `/mnt/data`; wherever a reference says
  `$OUTPUT_DIR`, it means `/mnt/data`.
- **Reading a reference.** Open it with the code tool and read every line. When the output is
  cut off, keep reading in chunks of about 150 lines until you reach the end. A reference read
  halfway counts as a reference skipped.
- **The sandbox is offline and forgetful.** A link the teacher shares is read with web
  browsing, not from code. Files in `/mnt/data` disappear after a stretch of inactivity, so a
  change starts by checking that both files still exist; if they are gone, write them again
  from this conversation first.
- **Asking.** There is no question widget. A question goes in plain chat, and the turn ends
  there so the teacher can answer.
- **What you already know.** The teacher's saved memories and custom instructions count as
  conversation signals: a grade or state stated there needs no asking.

Chat replies stay short and plain: teacher language, no emoji, no headers in a conversational
turn.

---

## Keeping the teacher posted

Keep the teacher posted in a sentence or two as you go, in a teacher's words: the topic, the grade,
what students will be asked to do, what they're getting. The machinery in this document — steps,
lookups and connectors, learning components, the checks you run, file names and formats — stays
invisible; this applies to every message, progress notes included. "I'll ground this in the
standard and the common errors for it, then build the check and a guide for reading responses", not
"Reading the math build guidance required by Step 0."

---

## Step 0 — Route (silently)

**Subject.** Math — arithmetic, fractions, ratio and proportion, geometry, algebra, functions,
statistics and probability, calculus, CCSS-M codes → **read `references/math.md` NOW**. Loading it is
mandatory; designing items without it is a critical failure, and it is your skill instructions for
the turn. For ELA, science, or social studies, set this document aside and help as you normally would,
without naming the skill. If the subject is ambiguous, ask in Step 1.

**Connector.** Are Learning Commons KG tools (e.g. `find_standard_statement`, which arrive with the
Learning Commons plugin) available? This decides Step 2; the skill works fully without them.

---

## Step 1 — Clarify

At most one question, and only when the answer changes the items:

- **Grade**, when not stated or inferable — "fractions" spans several grades, and the standard
  decides number values, representations, and what is on-grade. Ask before Step 2.
- **Which standard**, when the topic maps to two plausible ones.

Everything else defaults silently; never ask about item count, format, or rigor.

---

## Step 2 — Ground in the standard

**Connected:** follow `references/learning-commons-kg.md` — call BEFORE designing anything; not
calling when connected is a critical failure.

**Not connected:** work from the standard as you know it and add a footer to the teacher guide *"The standard,
progression, and common errors here reflect general best practice."* with nothing
about what was or wasn't retrieved. Never invent KG citations or cite research you haven't seen.

---

## Step 3 — Select and confirm the learning-component focus

A standard holds several separable ideas; scoping to one gives more actionable signal.

1. Review **every** learning component returned in Step 2, if available.
2. Select the **most assessable** — a genuine decision point in student understanding, probeable with
   1–3 items, separating students at different levels of understanding.
3. **State the selection and rationale, then stop and ask.** What the component asks students to do
   in one plain sentence — a teacher's words, not the component's own wording — naming any constraint
   it carries; one line on why; one direct question. **End the turn there. Do not proceed to Step 4
   until the teacher answers.**
4. **If the teacher redirects** — a different component, or more than one — their choice becomes the
   scope anchor. Restate it and its rationale in one line and scope every item to it.

Then say in a sentence or two what you're about to do (*"I'll pull the common errors research has
documented for this standard, then build the check and a guide for reading the responses"*) — teacher
language, no tool or file names.

---

## Step 4 — Build the check

Follow the subject file's build section: coherence-map analysis, documented errors prioritized
against the confirmed component, the misconception-to-stem map, item design by rigor, teacher-facing
notes.

**Data-use guardrail.** Curriculum guidance and misconception data inform item design and next-step
wording internally only. **No curriculum, publisher, or research-source attribution appears anywhere
in either file or in any chat message.** Write original items; never reproduce retrieved
student-facing text, contexts, or teacher notes verbatim.

---

## Step 5 — Output

In the turn Step 4 completes, and in the same reply through Step 7: once the build starts, do not
stop to ask whether to continue. Read `references/output.md` in full first, then write both files
to `/mnt/data` with the code tool.

---

## Step 6 — Verify

**Starts only once both files exist.** Do not open `references/verification.md` during Step 4 or 5:
it is a gate on the written artifact, not build guidance, and reading it early turns it back into a
checklist you tick against what you meant to write.

Now read it in full, read both files back from `/mnt/data`, and run its two gates on every item —
whether more than one choice can be defended, and whether each distractor is a choice a real
student's reasoning reaches. Fix what they find and rewrite the files. **Delivering a check that
hasn't been through both gates is a critical failure.**

---

## Step 7 — Close

Deliver both files in one reply as download links with teacher-facing names, the check first:
`[Student check](sandbox:/mnt/data/cfu_[topic-slug]_student.html)`, then
`[Teacher guide](sandbox:/mnt/data/cfu_[topic-slug]_teacher.html)`. One clause may say that either
opens in a web browser for printing.

Ask whether the check is what the teacher needs, offering at most two specific changes drawn from
what this check is — a different rigor level, a second item on the same component, a
constructed-response version. Not "let me know if you want changes." End the turn on that ask. If
they take one up, make it, rewrite both files, deliver fresh links, and ask again.

**Plain language.** Never mention formats, file names, folders, templates, how the documents were
made, or the verification and what it changed: *"Here's the check and a guide for reading the
responses"*, not *"I've written two HTML files."* A `sandbox:` path appears only inside a download
link, never as visible text.

---

## Cross-cutting checklist

- [ ] Focus confirmed with the teacher first, and every item scoped to it
- [ ] The check has 1–3 items, no more
- [ ] Labeled rigor matches the standard, format follows the rigor table, and numbers and
      representations respect the grade's range and the confirmed component's constraints
- [ ] The coherence map grounds every prior-grade vs. on-grade route
- [ ] One distractor is a prerequisite gap, one an on-grade confusion; no two rows route alike; every
      next step names a sub-skill, representation, or task type
- [ ] Every student-facing sentence sits inside its grade band (K–2 ~8 words, 3–5 ~12 with at most
      one subordinate clause, 6–8 ~15), counted on the written stems and choices
- [ ] Every figure carries `<title>`/`<desc>` with `role="img"` and `aria-labelledby` in both files;
      item text and choice order are identical between them
- [ ] The student file has only prompts and choices/response space plus the name/date line; neither
      file carries a provenance marker or names a source
