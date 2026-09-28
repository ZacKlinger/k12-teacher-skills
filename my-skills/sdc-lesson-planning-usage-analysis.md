# How `/sdc-lesson-planning` is actually used, and what changed because of it

September 26, 2026

A tool reveals its shape in what gets made with it. Six weeks of packets, games, and guides in
Drive tell a clearer story about this skill than its own instructions do: it was written for one
kind of day, and it has been asked to carry four.

## What this analysis could and could not see

**Could not see: the chats themselves.** Conversations in the claude.ai projects *SDC Math* and
*SDC Science* are not reachable from a Claude Code session; there is no connector for chat history.
Everything below is read from what those chats produced and from what you wrote about them.
The last section explains how to get the per-conversation analysis you asked for.

**Could see:**

| Source | What it holds |
|---|---|
| Drive, `Lesson Plans` folder and My Drive root | About two dozen skill-era packets and guides (some duplicated), Aug 10 to Sep 23 |
| claude.ai artifacts | Hydro Jeopardy (9/18), Readiness Jeopardy (9/21), Garden Field Guide (9/8), SCRAP SF Field Trip Checklist (9/22) |
| The skill as installed in claude.ai | Last updated Aug 28 |
| Draft PR #1 in this repo | Your Sep 25 revision: student talk replaces movement, science practices |
| *Claude for Teachers feedback* doc | Your own account of what works and what doesn't (Sep 25) |
| *Klinger SDC_Science_Syllabus* | Course structure, accommodations, routines |

## How you use it

**1. Four shapes of work, and the skill was built for one.** The skill plans "one class session at
a time." What it has been asked for:

| Shape | Examples in Drive and artifacts | Covered before this PR? |
|---|---|---|
| Single lesson, packet + deck | Science 1.5, Science 1.6, Hydroponics Day 2, flight packet | Yes |
| Multi-day packet | Math 1.5, *Field trip prep, Day 1 & 2, 60 min each* | No |
| Viewing guide | Top Gun: Maverick (v3, 16 questions, multi-day), tubing video (timestamped), Pursuit of Happyness (EN and ES), Fruitvale Station | No |
| Review game | Hydro Jeopardy, Readiness Jeopardy | No |

The uncovered shapes are a third of the output, and the third version of the Top Gun guide
suggests they cost the most revision.

**2. You number lessons your own way, and rename every file to match.** Packets arrive titled
`student_packet_bilingual`, `Session_1_Student_Worksheet`, `student_materials_day1`; you rename
them `Science 1.5`, `Science 1.6`, `Math 1.5`. Inside, the headers still say *Intro Day* and *Day 2*,
so the page a student holds and the file you keep disagree about what day it is. Three copies of
`Session_1_Student_Worksheet` and two of `student_packet_bilingual` sit side by side.

**3. You carry yesterday into today by hand.** On Sep 1, four earlier packets were uploaded to Drive
within two minutes of each other. Your feedback doc names the reason: *"when I want to reference an
artifact or lesson from the previous day, Claude struggles; it forces me to manually add an
artifact to the project context."* The skill's Step 0 looked for "a connected folder," which a
claude.ai project doesn't have, so it never found the previous lesson on its own.

**4. You tell it the period length almost every time.** Science runs 90 minutes and opens with
breakfast and a do-now; math runs 60. The skill asks "60 or 90?" whenever no profile answers,
and I found no profile in Drive or in this repo. Your feedback asks for exactly this: *"not having to guide a lesson plan
into how long it should be."*

**5. Language access found its form, then drifted.** On Aug 24 the Pursuit of Happyness guide was
two separate documents, English and Spanish. From Aug 28 on, one packet carries one short Spanish
line per task, and it works: Science 1.5 and 1.6 keep the lines to the task. Math 1.5 drifts,
translating whole context sentences (*"El equipo de Jordan hizo esta lista..."*), which is the
doubling the rule exists to prevent. Your feedback also asks for more than one home language on the
same page, which the skill had no way to do.

**6. The rules stop at the skill's edge.** Readiness Jeopardy was built for Science 1.6, the same
day, and it is good: fair-guess questions, reveals that explain rather than just answer. But it has
no Spanish lines and no lesson code, because games were never inside the skill.

**7. Accommodations live in the syllabus, not the skill.** The syllabus promises extended time,
modified assignments, visual supports, preferential seating, sensory breaks, and behavior supports.
The skill had nowhere to hold them, so they arrived, if at all, as revisions. Your feedback:
*"IEP / 504's are an afterthought... a checklist"* would be better than an open question.

**8. The installed skill is a month behind your thinking.** claude.ai still runs the Aug 28 version.
Your Sep 25 revision (student talk as the non-negotiable, science practices) is sitting in a draft
PR and hasn't reached a single lesson yet.

## What changed in the skill

This PR builds on PR #1, so it carries your talk and science-practice revisions forward.

| Evidence | Change | Where |
|---|---|---|
| Files renamed by hand to lesson codes | Every session is named by its code. `meta.code` leads the packet header and footer; files arrive as `Science 1.7 - Pump build - packet.docx` | `SKILL.md` "Lesson codes and file names", `render_packet.py` |
| Previous lesson re-uploaded by hand | Step 0 works out the previous code and, when Drive is connected, finds and reads that packet: one search, one read | `SKILL.md` Step 0 |
| Period length asked every time | The profile holds a weekly schedule; the skill reads minutes off the date and only asks when the schedule can't answer | `SKILL.md` Steps 0 and 1, profile template |
| No test data loop in claude.ai | One optional line in the clarifying round (*"How did 1.6 go?"*) and a ready-to-paste Day map row at the end of every lesson | `SKILL.md` Steps 1 and 4 |
| Accommodations arrive as revisions | Accommodations checklist in the profile; every ticked item is built in from the first draft and reported in the plan | profile template, `SKILL.md` "Accommodations", `render_packet.py` (`large_print`) |
| One language only | `meta.languages` lists the home languages; each gets one abbreviated line; right-to-left scripts print right to left; the renderer and the deck checker report gaps per language | `render_packet.py`, `check_deck.py --languages`, `deck_template.html`, `packet.md`, `deck.md` |
| Viewing guides, multi-day packets, games built outside the rules | A reference for each shape, drawn from your best examples (Top Gun v3, tubing worksheet, Math 1.5) | `references/formats.md` |
| Two Jeopardy boards built from scratch in a week | A review-game template generalized from your Readiness Jeopardy, with language lines per clue; fill one data object, nothing else | `assets/review_game_template.html` |
| Description too narrow to trigger on these asks | Description names lesson codes, viewing guides, multi-day packets, and review games (kept under the 1024-character limit) | `SKILL.md` front matter |

Two draft profiles, one per project, are pre-filled from the Drive evidence in
`my-skills/profiles/`. Lines marked **confirm** are inferences.

## What changes in your workflow

The aim is a first message that needs no answer before the plan starts.

1. **Merge PR #1, then this one, and upload the new version.** Run
   `my-skills/tools/package_skill.sh sdc-lesson-planning`, then in claude.ai go to Settings >
   Capabilities > Skills and replace `sdc-lesson-planning` with `my-skills/dist/sdc-lesson-planning.zip`.
2. **Put a profile in each project's knowledge, once.** Open `my-skills/profiles/`, fill the
   schedule table, tick the accommodations that fit this year's roster, and paste each file into
   the matching project. Five minutes, and every lesson after it skips the questions.
3. **Open with the code and the day.** *"Science 1.7 tomorrow: build the reservoir."* The skill finds
   1.6, reads the minutes off Tuesday, and goes straight to the point of view and the arc.
4. **One chat per lesson, titled by its code.** Long chats that run across lessons are where
   context gets muddy and where the skill loses track of which day it is.
5. **Close the loop in one line.** Paste the Day map row the skill hands you, and after teaching add
   how it went, or answer the optional question at the start of the next lesson. That line is the
   only real test data a lesson produces.
6. **Let the file names do the filing.** With *Convert uploads* on in Drive settings, a coded `.docx`
   becomes a Google Doc with the right title and no renaming. Keep one folder per course; Science
   1.6 and the tubing worksheet are currently in My Drive's root, where Step 0's search still finds
   them but you might not.
7. **Edit the skill here, not in claude.ai.** Changes made in a chat vanish; changes made here keep
   their history, and the packaging script turns them into an upload in one command.

## What was left out, on purpose

- **Uploading packets to Drive automatically.** The Drive connector can create a file, but only if
  the whole `.docx` passes through the conversation as base64, about 50 KB per packet, on every
  lesson. That is slow and expensive for a step the coded file name already makes a single drag.
  Worth revisiting if the connector learns to upload from a file path.
- **The eval-rubric points from your feedback doc** (SDC and modified-curriculum conditions for
  R-M1, P-S3, P-M3; credit for a plan written in chat). They belong in `evals/`, not in this skill,
  and you said you'd open a GitHub discussion on them.
- **A live vote tally on the deck.** The dataviz kit can already be filled from the room's own
  numbers; a dedicated tally slide is a natural next step if the vote in Science 1.6 proves a
  pattern.

## Getting the analysis of every conversation

The per-chat view you asked for needs the chats. To get it:

1. claude.ai > Settings > Privacy > **Export data**. The export arrives by email as a zip.
2. Unzip it and run:
   `python3 my-skills/tools/usage_report.py path/to/conversations.json > usage.md`
3. The report lists every lesson-planning conversation with its turns, how many follow-ups it
   needed, what those follow-ups asked for (timing, Spanish, photos, video, deck, packet layout,
   question count, games, accommodations, earlier lessons), and a roll-up across all of them.
   Share `usage.md` (not the raw export) in a new session for a second pass that tests these
   findings against every conversation.

The export format isn't documented, so the script reads it forgivingly and says plainly when a
field it needs is missing.
