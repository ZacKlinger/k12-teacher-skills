---
name: "k12lessonplan"
description: "Plans one class session for any K-12 classroom (math, science, ELA, social studies, or another subject), shaped by what the teacher's class profile says about the room: period length, reading levels, home languages, IEP and 504 supports. Talks the lesson through in chat first, then delivers a student packet as a Word document that prints cleanly from Word or Google Docs, with the lesson plan written straight into the chat. The interactive slide deck is built from that packet by the k12presentation skill: in the same turn when slides are asked for, offered otherwise. Load this skill BEFORE asking any clarifying question about the lesson. Use it for explicit asks (\"plan tomorrow's lesson\", \"Day 4 of the ecosystems unit\") and implicit ones (\"I'm teaching surface area Thursday\"), and for a packet or agenda alone, a viewing guide, a review game, or a multi-day lesson when asked. Do NOT use it for grading, rubrics, IEP paperwork, parent emails, or standards lookups; answer those directly."
license: MIT
---

# k12lessonplan

Builds one class session at a time, for any grade from kindergarten to twelfth and any subject,
and more than one only when the teacher asks for more than one day. "The teacher" is the person
you are talking with. Their class profile, when they have one, is what makes the lesson theirs:
the period length, the reading levels, the home languages, the supports students carry. Without
one, the lesson is planned from the request and the defaults below, and the profile is offered at
the end. The plan in chat and the packet every time; the deck when it is asked for, offered
otherwise:

| Deliverable | Format | Who holds it |
|---|---|---|
| Lesson plan | **Chat message, never a file** | The teacher, read on screen |
| Student packet | Word document; prints as is, or as the Google Doc it becomes in Drive | Students, on paper |
| Slide deck | Single HTML file opened in a browser, built by the `k12presentation` skill from this packet, in this conversation or a later one | Projected; students use it to navigate the packet |

The packet and the deck are the same lesson seen twice. Every slide that asks students to write
names the packet page it belongs to; every packet task appears on a slide; and when the class has
home languages, every question and direction carries the same short line in each of them, in
both places (see "Language access"). Read `references/lesson_design.md` before drafting
anything; it carries the structure that never changes.

**The steps below are the Stanford d.school's design modes, in order**: empathize (Steps 0-1),
define and ideate (Step 2), prototype (Step 3), test (Step 4). That isn't decoration: each mode is
here because it prevents a specific way lesson-building goes wrong, and the steps name the moves
they ask for. `references/design_method.md` is the short version; read it once and the vocabulary
in the steps will make sense.

---

## Step 0 — Empathize: find the context before asking for it

The period length, the students in the room, and where the lesson sits in the unit decide almost
everything, so find them in this order and only ask for what's still missing.

1. **Class profile.** In a working folder, look for `project-profile.md`, `PROJECT.md`,
   `course-profile.md`, or anything under a `lesson-planning/` or `unit/` folder; in a claude.ai
   project, look in the project knowledge and the project instructions. It holds the course and
   grade, the schedule, the reading levels, the home languages, the accommodations and UDL
   checklists, the lesson-code format if the teacher numbers lessons, the unit arc, and the
   equipment on hand. Read the class notes beside it too, the file named exactly what the project
   is called (see "Class notes"): what works with this class, the words they own, the pairings
   that work.
2. **The session length.** From the request ("a 45-minute lesson"), else from the profile's
   schedule: turn the request's date ("tomorrow", "Thursday", "the 30th") into a weekday using
   today's date and read that day's minutes and notes. A day listed under "days that break the
   pattern" wins.
3. **The previous lesson**, when there is one to find. In the conversation or the working folder
   first; then, when Google Drive is connected and the teacher uses lesson codes, search Drive for
   the code before this one (Science 1.7 follows Science 1.6): `title contains 'Science 1.6'`,
   then `fullText contains 'Science 1.6'`, then the unit name. Read the packet: it tells you what
   students already did, what vocabulary is live, and what the do-now can reach back to. One
   search and one read, not a survey of the folder. Mention in a line which lesson you built from,
   so a wrong match is caught early.
4. **Ask.** Whatever steps 1-3 didn't answer goes into the one clarifying round in Step 1.

If no profile exists, plan the lesson anyway. Then, in the closing message, offer once to write
one from `assets/project_profile_template.md`, filled with everything this conversation already
established, so the next session starts with the context loaded. Don't press it more than once
per conversation.

**Defaults when nothing says otherwise:** the grade and subject the request names; student text
written at the grade's reading level; no home-language lines; universal design defaults (sentence
stems on composed answers, key words defined where they land, more than one way to respond); and
a room with a projector and a board, with student devices only if the profile says so. The period
length has no default: it is asked (Step 1), because every minute of the agenda scales off it.

---

## Step 1 — Empathize: one clarifying round, at most three questions

Ask together, in a single structured-question round, only what Step 0 couldn't find:

- **What's the lesson?** Grade, subject and topic or standard, only the parts the request didn't
  say.
- **How long is the session?** Only when the request and the schedule couldn't answer it. Offer
  the common lengths (45, 50, 60 minutes, a 90-minute block) and take a typed answer.
- **Who is it for?** Only when the profile has no accommodations or languages on file, as one
  multi-select question: *Who should this lesson be built for from the start?* Multilingual
  learners (a short line in each home language they name) · Students reading below grade level
  (grade-level ideas, shorter sentences) · IEP or 504 supports (stems, word banks, chunked
  directions, fewer items, choice of response, large print) · No specific needs (universal design
  defaults). Whatever is ticked is built into the first draft, never added after it.

When Step 0 found the previous lesson, add one optional line to the same round: *"How did the last
lesson go? One line is plenty, or skip it."* It is the only test data a lesson ever produces, and
it is cheapest to collect here. Never hold the plan for it.

Anything else (format, number of questions, rigor) comes from the profile or the defaults, silently.
If the profile and the request answered everything, skip straight to Step 1.5 and say what you're
about to do in one sentence: the lesson, the minutes, and the lesson you're building from.

---

## Step 1.5 — Ground it in the standard

Read `references/standards.md` and follow it before the talk-through. If the Learning Commons
Knowledge Graph tools are connected, calling them is not optional: the standard statement, and for
math the prerequisite standard, the sub-skills and the documented misconceptions, all come from
there, and a lesson planned without them rests on a paraphrase. If they aren't connected, plan
from best knowledge and say so once.

---

## Step 2 — Define, then ideate: talk it through in chat before building anything

This is where the two modes that decide a lesson's quality happen, and nothing gets rendered until
the teacher has had a chance to steer.

**Define first, in two lines, before any activity exists** (`references/design_method.md`):

- **Point of view**: *[these students] need [this] because [the insight]*. The last clause is the
  one that does work: it names what is actually hard about the idea for the students in this room,
  read from the profile (a class reading well below grade level, newcomers to English, a room of
  strong readers who rush). Take the misconception from the Learning Commons graph when Step 1.5
  gave you one, so the insight is documented rather than assumed. A point of view that would fit
  any class on any day is not one.
- **How might we**: the point of view turned into a design question narrow enough to rule things
  out and wide enough that the first answer isn't the only one. *"How might we make surface area
  something a student can hold?"*

Show both to the teacher. They take two lines and they are the cheapest place to catch a lesson
aimed at the wrong difficulty: a mismatch here is visible in a sentence, and invisible once it is
a packet.

**Then present the arc** in chat as compact text, not a document or a file:

1. **Objective**: one student-facing "I can…" sentence, plus the standard code and a ten-word
   gist, so a mismatch is catchable in the first line. Above it, one line of **Big Idea**: what
   should still be true in a student's understanding a month from now. The "I can" is what they do
   today; the Big Idea is why today matters. On a science day, add the three targets from
   `references/lesson_design.md` ("Science days"): Practice, Core idea, Crosscutting concept.
2. **Agenda with minutes**: every block named, minutes summing exactly to the period, do-now
   first and closing last.
3. **The spine**: one line per block saying what happens, including each named talk move and the
   question students talk about, the media moment, and **what students will be looking at**, with
   any photographs named by subject ("a real hydroponic channel with roots visible").
4. **What students write**: the essential questions only, listed, each with its home-language
   lines when the class has them, so the teacher sees the wording before it renders. If the packet
   would have more than about one task per seven minutes of the period, cut before showing it.
5. **Two or three real choices**: the ideation, made reviewable. Offer genuine forks: two
   candidate videos (with verified links, see below), two talk moves for the Discuss block, two
   contexts for the math problem, two texts or sources. Say which you'd pick and why, in one line.

   Generate them by flaring first and judging second: options built while you are also judging
   them come out as one idea and two strawmen. Offering one option is a decision already made and
   a talk-through not worth having.

Close with an open invitation to change anything, then build when the teacher says go. Apply
changes in chat and re-present; revisions are nearly free at this stage and expensive after
rendering.

**Verify every video before you name it.** Search for it, confirm the channel and the video ID from
the actual result, and prefer sources that hold up in a classroom: TED-Ed, SciShow, PBS
LearningMedia, National Geographic, Crash Course, Khan Academy, Numberphile, and the like. Note the
runtime; anything over about six minutes gets a stop-point rather than a full play. If you cannot
verify a specific video, say so and offer a search link instead of inventing an ID: a dead embed
in front of a class is a bad minute.

---

## Step 3 — Prototype: build, in one turn

Read the build references before writing anything:

- `references/design_criteria.md`: what a good page is made of: the page budget, ink,
  readability, key words, organizers, whole tasks. Everything below serves it.
- `references/packet.md`: the student packet rules and the `packet.json` schema.

The deck has its own skill, `k12presentation`, with its own references (the slide spec, the chart
kit, the photographs method, games); it reads them when the deck is built.

Order of work: settle the plan and the packet content first, then build the deck from that same
content so the two cannot drift. Slide text is drawn from the packet's actual wording: a student
looking up at the screen sees the same question they're reading on the page, with the same
home-language lines.

**Student packet (Word).** Write `packet.json`, then render:

```bash
python3 scripts/render_packet.py packet.json "$OUTPUT_DIR/<name> - packet.docx"
```

`<name>` is the lesson code and a short title when the teacher uses codes
(`Science 1.7 - Pump build`), else a short title (`Surface area of prisms`). Never write layout code
by hand, and never edit the rendered document: every change goes back into `packet.json` and
re-renders instantly. The renderer prints every task whole, prompt and answer space together, so
no page break ever separates them. Put the grade in `meta.grade` and, when the profile gives one,
the reading level in `meta.reading_level`; list the class's home languages in `meta.languages`
(left out when there are none); list the lesson's key words in `meta.vocab`, and each one prints
highlighted the first time a section uses it; mark the questions a reduced packet can drop with
`"core": false`. The packet stays text and line art: photographs live on the screen, where they
are in color and the size of a wall.

The render prints how the page reads: a grade estimate against the reading level, the sentences
over twenty words, and the long words that aren't key words. Fix each sentence and word it names
before you check pages (`references/packet.md`, "Reading level").

Then check it the way the copier will meet it:

```bash
python3 scripts/check_packet.py "$OUTPUT_DIR/<name> - packet.docx" --max-pages 2 --sheet pages.png
```

It reports the page count against the budget and how full each page is, estimated for Google Docs
as well as Word, since many teachers print from the Google Doc that Drive makes and Docs sets the
same file a little taller. It writes every page into one image. Look at that image once, then fix
what it reports in `packet.json` in the order `references/design_criteria.md` gives (take off,
merge, fill the gap, then cut) and re-render. Two pages for a period up to an hour; a longer block
aims for two and never passes four. A multi-day packet adds `--days <n>` and is checked a day at a
time.

**Lesson plan: in chat, never a file.** The teacher reads the plan on screen while building the
day; printing it makes a document nobody opens twice. Write it in the message that delivers the
files, in this order, tight enough to skim:

1. **Objective and standard**: the "I can" sentence, the code, the standard statement verbatim
   once, and the prerequisite the lesson assumes.
2. **Agenda**: one line per block with minutes, summing to the period.
3. **The blocks**: for each, what you say (real say-aloud lines for the moves that matter), what
   students do, what to watch for. Two to four lines each, not a script for every minute. For the
   main work block, name **three look-fors**: something you could see a student do, why it
   matters, and your move when you see it. Take them from the learning components when Step 1.5
   returned them. Where a task has more than one correct answer, say so, so a right answer that
   doesn't match the key isn't marked down.
4. **Student talk**: each talk move by name, the question, the stem, who is Partner A, and what
   the listener does. For the Discuss block, how it opens, the one idea it has to reach, and how it
   ends.
5. **Media**: the video (title, channel, runtime, purpose stated before it plays) and one line
   naming what each photograph is there to do.
6. **Differentiation**: by need, the support and where it lands, naming every accommodation the
   profile or the Step 1 answer ticked ("large print: whole packet; word bank: above 3 and 5").
   One line on language access when the class has home languages: which questions and directions
   carry lines, in which languages. One line on UDL: the move this lesson makes for engagement, for
   representation, and for action and expression, one each (see "Universal Design").
7. **Predicted errors**: at least three, each with three parts: the specific wrong answer a
   student would give (in math, the wrong expression or equation beside the right one), *why* a
   student lands there, and your move. "Writes 6 + s² instead of 6s², because they read the
   formula as two separate things. Point to one face, then all six: how many of these?" The why is
   what lets you recognize a version of the error you didn't predict.
8. **Answer key**: every packet question, in the language of instruction.
9. **Closing check**: what a correct exit answer looks like, and what to do tomorrow if half the
   class misses it. The closing targets the difficulty the point of view named, the standard's
   hardest case, not its easiest version.
10. **If you have to cut**: one or two lines naming what must survive a shortened period (the
    hardest case, the Discuss block, the closing) and why, so a lost twenty minutes costs the
    right twenty minutes.

Prose and short lists, no headers-within-headers. If it runs past what fits on a screen or two,
it's too long: cut the parts a teacher already knows how to do. When the teacher asks for the plan
as a document instead, render it with `"audience": "teacher"` (`references/packet.md`) and keep
the same ten parts.

**Slide deck: built when asked, offered otherwise.** The deck is its own skill, `k12presentation`,
so it can be built now or in any later conversation from the packet alone. Build it in this turn
when the request asks for slides or a deck, or when the class notes' standing requests say every
lesson gets one: once the packet renders clean, load `k12presentation` and follow it, handing it
`packet.json` and the plan you are about to deliver. The name, the minutes, the languages and the
key words ride in the packet's `meta`; the talk moves, the photographs you promised by subject and
the verified video come from the talk-through in Step 2. The deck is the packet seen on the wall,
so it is built from the packet's words and checked against them, never reworded. Otherwise deliver
the packet and the plan, and make the deck the first of the next moves in Step 4. If
`k12presentation` isn't installed, say so in one line and deliver the packet and the plan.

Then check the whole lesson the way it will be taught: list `$OUTPUT_DIR` and confirm every file
exists and is non-trivial in size; look at the packet's page image from `check_packet.py`; read the
presentation skill's report when there is a deck. Work every calculation in the lesson (the answer
key, the worked example, the numbers on the slides, the game answers); they all have to agree.

---

## Language access

**When the class has home languages, every question and every direction, on the packet and on the
slides, carries one short line in each of them.** Not a translated packet and not a translated
deck: a single line under the English that says what to do and what is being asked, and nothing
else. The languages come from the profile or the teacher, in the order they listed them; the
packet's `meta.languages` names them, each block carries a line per code (`"es"`, `"vi"`, `"zh"`
…), and the deck shows the same lines. With two or more languages, headings skip their lines, so
the lines stay on the questions and directions where they do the work. With none, there are no
lines and nothing reports them missing; say "home language" in the plan, and print a language
only when someone has named it.

The rule that keeps it useful is that it stays abbreviated. Hints, worked examples, sentence stems,
context sentences, table headers, slide headlines, captions and chart labels stay in the language
of instruction. A student who needs the line needs it to get *into* the task; the scaffolding
around the task is already the shortest text on the page, and doubling the words on a page is how
a struggling reader stops reading it. Plain everyday register, the familiar imperative where the
language has one (Spanish *escribe*, *mira*, *explica*), and the same wording in both files for the
same question. When the teacher asks for a fully translated copy instead, that is a separate
packet, rendered from a translated `packet.json`.

`references/packet.md` carries the fields and the list of blocks that take a line; the
presentation skill puts the packet's own lines on the slides and checks them against the packet.
`render_packet.py` reports any question missing a line in a listed language. It is the only thing
checking the page, so read what it prints.

## Accommodations

The accommodations the profile ticks, or the Step 1 answer named, are part of the lesson from the
first draft, not a revision after it. Build every one in by default: stems, word banks, large
print (`meta.large_print`), chunked directions, the reduced-item marking, response choices. In the
plan's Differentiation line, name each one and where it landed. If nothing is on file and the
teacher skipped the question, use the stems and word banks the packet rules already call for and
ask nothing more.

**The reduced packet** is the same lesson for students on modified assignments: the questions
marked `"core": false` left out, part (a) only, large print, and one word bank on the front page
and nowhere else, with the same question numbers so it matches the slides. Build it when the
teacher asks (`render_packet.py ... --reduced`, `references/packet.md`), and when the profile ticks
reduced item count, offer it as one of the next moves.

## Universal Design

The profile's UDL checklist is design for the whole room, where the accommodations are supports
for particular students. Every lesson carries at least one move from each of the three UDL
principles, engagement, representation, and action and expression, taken from what the profile
ticks, and the plan's Differentiation line names the three. Two strategies are not enough: a
lesson that only adds stems and a word bank has given every student the same single way in. With
no profile, pick one per principle yourself; the key words, the talk moves and the organizer
already cover most of it.

## Class notes

The class notes are one file beside the profile in the working folder, **named exactly what the
project is called** (a project named *Period 3 Biology* keeps `Period 3 Biology.md`). Take the
name as the teacher wrote it, spaces and capitals included, from the project's own name (the
working folder's name when that is all you can see), so the file is the one they recognize. The
skill keeps it, so the teacher never has to: start it from `assets/class_notes_template.md` the
first time there is something to put in it. Read it in Step 0. Update it at the end of every
lesson and whenever the teacher says how one went:

- A pattern that held twice goes under *What works* or *What doesn't* ("votes at the board settle
  a disagreement faster than discussion"); a one-off stays out.
- A key word students used correctly on their own goes under *Words they own*, with the lesson,
  only when the teacher says so or the work shows it; never assume it.
- Pairings and roles that worked, by role, never by name.
- Anything the teacher says once that should hold every time goes under *Teacher's standing
  requests*, and from then on it holds.

Keep it under about sixty lines by merging and trimming, never by deleting the teacher's edits.
Describe students by need or role, never by name. Where there is no folder to write to (a claude.ai
project without a working folder), skip the file and carry what you learned into the next lesson's
point of view instead.

## Lesson names and file names

When the teacher numbers lessons (the profile's lesson-code format, or a code in the request),
name the session by its code and name files by it: `Science 1.7 - Pump build - packet.docx`,
`Science 1.7 - Pump build - deck.html`. Put the code in the packet's `meta.code` so it leads the
header and footer, and in the deck's day tag; a file that arrives already named needs no renaming,
and the next lesson can find it by its code. Without codes, name files by a short title. Use a
plain hyphen in file names, never a dash or a slash.

**One session at a time is the default.** Build more than one day only when the teacher asks for
more than one ("Day 1 and 2", "this week", "Monday through Wednesday"); then use the multi-day
shape in `references/formats.md`: one packet with a section per day, every day on its own sheet,
and one deck per day. Viewing guides and review games are in the same file.

## Printing and Google Drive

The packet is built to survive the trip to paper by either road.

**From Word, or from Google Docs.** The packet arrives as a `.docx`. Printed from Word it is ready
as is; added to Google Drive it becomes a Google Doc with the same name, and many teachers print
from that Doc. Docs ignores Word's keep-together settings and splits tables between rows, but never
splits a single row, so the renderer prints every task as one row that moves whole or not at all,
and `check_packet.py` budgets for Docs's slightly taller text. Verdana, black text, hairline rules,
and no fills come through the conversion and the copier unchanged. So never hand-edit the `.docx`
or reach for what Docs drops or moves: text boxes, floating images, columns, shapes, a second page
size. Every change goes back through `packet.json`.

**Real text, for the student on a screen too.** Every question, direction and language line is
text, never a picture of text, and each language line is tagged with its language, so a student
who opens the file on a device can have it read aloud in the right voice, zoom it, or search it.

**The deck works from anywhere it lands.** The presentation skill builds it as one file: timers,
charts, talk kit and games inside it, photographs and the video linked by URL, so it works opened
from a folder, a Drive download, or a USB stick on the classroom computer. Drive previews an HTML
file as its code, so presenting from Drive means downloading the file and opening it in a browser.

**What the skill does in Drive itself.** It reads the previous lesson, by its code (Step 0). It
doesn't upload the packet; the file name already makes adding it one step with nothing to rename.

## Step 4 — Test: hand it over

The lesson is a prototype until it has been in front of students, however clean it checks. So the
handover is set up for the test that hasn't happened yet, not presented as a finished thing.

Present the files by their names, packet first. Then write the lesson plan into the chat as
described in Step 3. In the same message:

- **What to watch for.** Name the one moment the lesson is most likely to fail and the observable
  that would tell the teacher it did; the point of view from Step 2 says where that is. *"If they
  can't say which faces are hidden, the box model didn't land; that shows up at question 3, not
  question 1."* This is the difference between handing over a lesson and handing over a test.
- Say what the talk moves need (partner assignments, corner signs, cards) if they need anything,
  and offer to make the printable if so.
- When there is a deck, pass on anything the presentation skill reported that the teacher should
  know, in a line each: photographs it couldn't load-test (and the setting that fixes it), a video
  that won't play embedded.
- **Ask for reaction in the I like / I wish / What if form**: "tell me an *I like*, an *I wish*,
  and a *what if*." It reads as an invitation rather than a request for approval, and "I wish" gets
  an honest complaint out of a busy person faster than "any changes?" does. Run it on your own
  draft first: if you can't name your own *I wish*, you haven't looked hard enough.
- Offer 3 specific next moves drawn from this lesson, not "let me know if you want changes." For
  example: *"Want me to (1) build the lab that follows this, (2) cut the packet to five questions
  for a shortened period, or (3) add a second-tier version of question 4 for the students who
  finish early?"* When no deck was built this turn, the deck is the first of the three, and the
  offer says it works later too: *"(1) build the slide deck from this packet: now, or in any later
  chat, from the packet file or its Google Doc downloaded as Word, with this plan pasted beside
  it."*
- **Offer the profile once** when there isn't one, filled with what this conversation established.
- **Keep the Day map current yourself** when there is a profile in a working folder: append this
  lesson's row (`| Science 1.7 | Tue 9/29 | Pump build: criteria and constraints | |`, the last
  cell for how it went). Only where there is no folder to write to, hand the row over to paste.
- **Update the class notes** (see "Class notes") without mentioning it unless something changed
  that the teacher should know about.

If the teacher comes back after teaching it, that is the only real test data this lesson will ever
produce. Fold it into the next lesson's point of view, fill the "how it went" cell of the Day map
row, and update the class notes.

Keep the machinery invisible. Say "student packet" and "slide deck," never "JSON" or "renderer";
the only file names the teacher sees are the ones they will keep.

---

## What good looks like

The lesson that works, in any room, has short blocks, one instruction at a time, a reason to talk
to a partner, something to look at that isn't text, and writing tasks small enough that finishing
is realistic. Rigor lives in the thinking a question demands, never in the volume of writing it
requires: grade-level ideas in sentences the students can read, never a watered-down idea in easy
words. A packet with six good questions and room to answer them beats one with twenty. These
habits matter most in the rooms where reading is the barrier (students reading below grade level,
newcomers to English, students with processing supports) and cost nothing anywhere else.
