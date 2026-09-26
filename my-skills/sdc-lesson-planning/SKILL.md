---
name: "sdc-lesson-planning"
description: "Plans a class session for Zac's SDC (special day class) grades 9-10 science and math, then delivers a student packet as an editable Word document and an HTML slide deck with real photographs, timers, interactive charts, and embedded videos, with the lesson plan written straight into the chat. Load this skill BEFORE asking any clarifying question about the lesson. Use it whenever Zac is planning what to teach: explicit asks (\"plan tomorrow's lesson\", \"Science 1.7\", \"Day 4 of the hydroponics unit\") and implicit ones (\"I'm teaching surface area Thursday\", \"need something for period 3 tomorrow\"). Also use it for just a packet, just slides, or just an agenda, and for a viewing guide for a film or video, a multi-day packet, or a review game such as a Jeopardy board. Do NOT use it for grading, rubrics, IEP paperwork, parent emails, or standards lookups; answer those directly."
license: MIT
---

# SDC lesson planning (grades 9-10, science and math)

Builds one class session at a time for a self-contained special day class. Zac is the teacher —
"you" in these instructions, never a third party. Two files, plus the plan in chat:

| Deliverable | Format | Who holds it |
|---|---|---|
| Lesson plan | **Chat message, never a file** | Zac, read on screen |
| Student packet | Word document (uploads clean to Google Drive) | Students |
| Slide deck | Single HTML file: photographs, timers, charts, videos | Projected; students use it to navigate the packet |

The packet and the deck are the same lesson seen twice. Every slide that asks students to write
names the packet page it belongs to; every packet task appears on a slide; and every question and
direction carries the same short Spanish line in both places (see "Language access" below). Read
`references/lesson_design.md` before drafting anything — it carries the structure that never
changes.

**The steps below are the d.school's design modes, in order** — empathize (Step 0-1), define and
ideate (Step 2), prototype (Step 3), test (Step 4). That isn't decoration: each mode is here
because it prevents a specific way lesson-building goes wrong, and the steps name the moves they
ask for. `references/design_method.md` is the short version; read it once and the vocabulary in
the steps will make sense.

---

## Step 0 — Empathize: find the context before asking for it

Class length and where you are in the unit decide almost everything, so find them in this order
and only ask for what's still missing.

1. **Project profile.** In a claude.ai project it is already in the project knowledge; otherwise
   look in the connected folder for `project-profile.md`, `PROJECT.md`, `course-profile.md`, or
   anything under a `lesson-planning/` or `unit/` folder. It holds the course, the lesson-code
   format, the weekly schedule, the home languages, the accommodations checklist, the unit arc, and
   equipment on hand.
2. **The session length, from the schedule.** Turn the request's date ("tomorrow", "Thursday",
   "the 30th") into a weekday using today's date, and read that day's minutes and notes off the
   profile's schedule. A day listed under "days that break the pattern" wins. This is the answer to
   "how long is the session", so don't ask it when the schedule has it.
3. **The previous lesson.** Work out the code before this one (Science 1.7 follows Science 1.6)
   and find it: in the project's files or the conversation first; then, when Google Drive is
   connected, search Drive for the code in the title (`title contains 'Science 1.6'`, falling back
   to the unit name) and read the packet. It tells you what students already did, what vocabulary
   is live, and what the do-now can reach back to. One search and one read, not a survey of the
   folder. Mention in a line which lesson you built from, so a wrong match is caught early.
4. **Ask.** Whatever steps 1-3 didn't answer goes into the one clarifying round in Step 1.

If no profile exists, plan the lesson anyway. Then, in the closing message, offer once to write
one from `assets/project_profile_template.md`, filled with everything this conversation already
established, so the next session starts with the context loaded. Don't nag about it more than once
per conversation.

**Defaults when nothing says otherwise:** grade 9-10 SDC, science or math per the request, student
reading level 3rd-5th grade, Spanish as the one home language, class period 60 minutes on a normal
day and 90 on a block day, and a room with a projector, whiteboard, and student devices only if the
profile says so.

---

## Step 1 — Empathize: one clarifying round, at most three questions

Ask together, in a single structured-question round, only what you couldn't find:

- **Which lesson is this?** The lesson code (Science 1.7) or the date — this sets what students
  already know and what comes next. Ask this every time it isn't already established.
- **How long is the session?** Only when the schedule couldn't answer it: 60 minutes or 90-minute
  block. Never guess; the whole agenda scales off it.
- **What's the focus?** The topic, standard, or skill — only if the request didn't say.

When Step 0 found the previous lesson, add one optional line to the same round: *"How did 1.6 go?
One line is plenty, or skip it."* It is the only test data a lesson ever produces, and it is
cheapest to collect here. Never hold the plan for it.

Anything else (reading level, supports, format) comes from the profile or the defaults above,
silently. If the profile and the schedule answered everything, skip straight to Step 2 and say what
you're about to do in one sentence: the code, the minutes, and the lesson you're building from.

---

## Step 1.5 — Ground it in the standard

Read `references/standards.md` and follow it before the talk-through. If the Learning Commons
Knowledge Graph tools are connected, calling them is not optional: the standard statement, the
prerequisite standard, the sub-skills, and the documented misconceptions all come from there, and a
lesson planned without them is a lesson resting on a paraphrase. If they aren't connected, plan
from best knowledge and say so once.

---

## Step 2 — Define, then ideate: talk it through in chat before building anything

This is the part Zac actually wants, and it is where the two modes that decide a lesson's quality
happen. Nothing gets rendered until he's had a chance to steer.

**Define first, in two lines, before any activity exists** (`references/design_method.md`):

- **Point of view** — *[this student] needs [this] because [the insight]*. The last clause is the
  one that does work: it names what is actually hard about the idea for a student who reads three
  to six years below grade level. Take the misconception from the Learning Commons graph when
  Step 1.5 gave you one, so the insight is documented rather than assumed. A point of view that
  would fit any class on any day is not one.
- **How might we** — the point of view turned into a design question narrow enough to rule things
  out and wide enough that the first answer isn't the only one. *"How might we make surface area
  something a student can hold?"*

Show both to Zac. They take two lines and they are the cheapest place to catch a lesson aimed at
the wrong difficulty — a mismatch here is visible in a sentence, and invisible once it's a deck.

**Then present the arc** in chat as compact text — not a document, not a file:

1. **Objective** — one student-facing "I can…" sentence, plus the standard code and a ten-word
   gist, so a mismatch is catchable in the first line. Above it, one line of **Big Idea**: what
   should still be true in a student's understanding a month from now. The "I can" is what they do
   today; the Big Idea is why today matters. On a science day, add the three targets from
   `references/lesson_design.md` ("Science days"): Practice, Core idea, Crosscutting concept.
2. **Agenda with minutes** — every block named, minutes summing exactly to the period, do-now
   first and closing last.
3. **The spine** — one line per block saying what happens, including each named talk move and
   the question students talk about, the media moment, and **what students will be looking at** — name the photographs by subject
   ("a real NFT channel with roots visible", "an actual 40-foot shipping-container farm").
4. **What students write** — the essential questions only, listed, each with the Spanish line it
   will carry so he can see the wording before it renders. If the packet would have more than about
   eight tasks for a 60-minute period, cut before showing it.
5. **Two or three real choices** — this is the ideation, made reviewable. Offer genuine forks:
   two candidate videos (with verified links, see below), two talk moves for the Discuss block, two
   contexts for the math problem, two photo sets for the notice-and-wonder. Say which you'd pick
   and why, in one line.

   Generate them by flaring first and judging second — options built while you are also judging
   them come out as one idea and two strawmen, and Zac can tell. Offering him one option is a
   decision already made and a talk-through not worth having.

Close with an open invitation to change anything, then build when he says go. Apply changes in
chat and re-present — revisions are nearly free at this stage and expensive after rendering.

**Verify every video before you name it.** Search for it, confirm the channel and the video ID
from the actual result, and prefer sources that hold up in a classroom: TED-Ed, SciShow,
Veritasium, PBS Learning Media, National Geographic, Crash Course, Khan Academy, MIT K12, Steve
Spangler, Numberphile. Note the runtime; anything over about six minutes gets a stop-point rather
than a full play. If you cannot verify a specific video, say so and offer a search link instead of
inventing an ID — a dead embed in front of a class is a bad minute.

---

## Step 3 — Prototype: build, in one turn

Read the build references before writing anything:

- `references/packet.md` — the student packet rules and the `packet.json` schema.
- `references/deck.md` — the slide deck spec and the component catalog.
- `references/dataviz.md` — the chart kit and how to use it. Not optional: every deck carries at
  least one interactive chart, and two to four whenever the lesson touches a number, which is
  nearly always in science and always in math. Reading is the barrier in this room; a chart a
  student can interpret carries more of the lesson than any paragraph, and each one is predicted
  before it's revealed.
- `references/photographs.md` — the deck carries real photographs and they are not optional. This
  reference is where the claim-first selection method lives, and it is the difference between
  photographs that argue for the lesson and photographs that merely sit near it.

Order of work: settle the plan and the packet content first, then build the deck from that same
content so the two cannot drift. Slide text is drawn from the packet's actual wording — a student
looking up at the screen should see the same question they're reading on the page, in English and
in Spanish both.

**Student packet (Word).** Write `packet.json`, then render:

```bash
python3 scripts/render_packet.py packet.json "$OUTPUT_DIR/<code> - <short title> - packet.docx"
```

Never write layout code by hand, and never edit the rendered document — every change goes back
into `packet.json` and re-renders instantly. The renderer handles keep-together grouping so a page
break can't land between a question and its answer space. The packet stays text and line art:
photographs live on the screen, where they are in color and the size of a wall.

**Lesson plan — in chat, never a file.** Zac reads the plan on screen while he builds the day;
printing it makes a document nobody opens twice. Write it in the message that delivers the files,
in this order, tight enough to skim:

1. **Objective and standard** — the "I can" sentence, the code, a ten-word gist.
2. **Agenda** — one line per block with minutes, summing to the period.
3. **The blocks** — for each: what you say (real say-aloud lines for the moves that matter), what
   students do, what to watch for. Two to four lines each, not a script for every minute. For the
   main work block, name **three look-fors**: something you could see a student do, why it
   matters, and your move when you see it. Take them from the learning components when Step 1.5
   returned them. Where a task has more than one correct answer, say so, so a right answer that
   doesn't match the key isn't marked down.
4. **Student talk** — each talk move by name, the question, the stem, who is Partner A, and what
   the listener does. For the Discuss block, how it opens, the one idea it has to reach, and how
   it ends.
5. **Media** — the video (title, channel, runtime, purpose stated before it plays) and one line
   naming what each photograph is there to do.
6. **Differentiation** — by need: the support and where it lands. One line on language access:
   which questions and directions carry Spanish, so he knows what is on the page he is handing out.
7. **Predicted errors** — at least three, each with three parts: the specific wrong answer a
   student in this room would give (in math, the wrong expression or equation beside the right
   one), *why* a student lands there, and your move. "Writes 6 + s² instead of 6s², because they
   read the formula as two separate things. Point to one face, then all six: how many of these?"
   The why is what lets you recognize a version of the error you didn't predict.
8. **Answer key** — every packet question. English only; the plan is his, not a student's.
9. **Closing check** — what a correct exit answer looks like, and what to do tomorrow if half the
   class misses it. The closing targets the difficulty the point of view named, the standard's
   hardest case, not its easiest version.
10. **If you have to cut** — one or two lines naming what must survive a shortened period (the
   hardest case, the Discuss block, the closing) and why, so a lost twenty minutes costs the right
   twenty minutes.

Prose and short lists, no headers-within-headers. If it runs past what fits on a screen or two,
it's too long: cut the parts a teacher already knows how to do.

**Slide deck (HTML).** Copy `assets/deck_template.html` and fill it with the lesson's slides. The
template ships the navigation, the per-slide countdown timers, the day tag, the photo styles, the
blocked-image fallback, the click-to-play video, the interactive chart kit, and the talk kit (phased
talk timers, vote-talk-revote, a pair picker, build steps, read-aloud) — all of it already wired.
Every talk move in the plan gets a talk slide built the way `references/deck.md` "Talk slides"
describes. There is nothing to paste in and nothing to rebuild by hand; copying the template is the
whole setup. Save as `$OUTPUT_DIR/<code> - <short title> - deck.html`.

Every deck carries **at least one interactive chart**, two to four when the lesson has numbers in
it. In a room where reading is the barrier, the chart is the explanation and the words are its
caption — a deck with no chart has put the lesson back into prose.

Then check the work before handing it over. Run the deck checker first — it is faster and more
reliable than reading the file, and every rule in it is one that a previous build silently broke:

```bash
python3 scripts/check_deck.py "$OUTPUT_DIR/<code> - <short title> - deck.html" --minutes <period length> --languages es
```

Pass the period length you settled in Step 1 — 60 or 90. The slide count and the photograph floor
both scale off it, so a block-day deck checked at 60 gets told it has too many slides, and a
checker that is wrong once is a checker that gets ignored after that.

Fix every error and re-run until it exits clean; then read the warnings and make a decision about
each one rather than ignoring them. What the checker cannot judge, you still have to: whether each
photograph is the *right* photograph for its claim, whether the slides look right at projection
size, and whether the arithmetic holds. So also list `$OUTPUT_DIR` and confirm both files exist and
are non-trivial in size; convert the packet to PDF (`soffice --headless --convert-to pdf`, when
available) and look at the page breaks; open the deck and click through it. Work every calculation
in the lesson — the answer key, the worked example, and the numbers on the slides all have to
agree.

---

## Language access

**Every question and every direction, on the packet and on the slides, carries one short line in
Spanish.** Not a translated packet and not a translated deck — a single line under the English that
says what to do and what is being asked, and nothing else.

**More than one home language.** When the profile lists more than Spanish, every language gets the
same one line, in the order the profile lists them: the packet's `meta.languages` names them and
each block carries a line per code (`"es"`, `"zh"`, `"vi"` …); the deck adds
`<p class="es" lang="zh">` beside the Spanish; the game carries them per clue. Pass the same list to
the checker (`--languages es,zh`). With two or more languages, headings skip their lines, so the
lines stay on the questions and directions where they do the work.

The rule that keeps it useful is that it stays abbreviated. Hints, worked examples, sentence stems,
context sentences, table headers, slide headlines, captions and chart labels stay English. A student
who needs the Spanish needs it to get *into* the task; the scaffolding around the task is already
the shortest text on the page, and doubling the words on a page is how a struggling reader stops
reading it. Plain everyday Spanish, `tú`-form imperatives, and the same wording in both files for
the same question.

`references/packet.md` carries the `"es"` field and the list of blocks that take one;
`references/deck.md` carries `.es` and where it sits on a slide. `check_deck.py` errors on a deck
with no Spanish and `render_packet.py` reports any question missing it — both are the only thing
checking this, so read what they print.

## Accommodations

The profile's accommodations checklist is part of the lesson from the first draft, not a revision
after it. Build every ticked item in by default: stems, word banks, large print
(`meta.large_print`), chunked directions, the reduced-item marking, response choices. In the plan's
Differentiation line, name each ticked accommodation and where it landed ("large print: whole
packet; word bank: above 3 and 5"). If the profile has no checklist, use the stems and word banks the
packet rules already call for and ask nothing.

## Lesson codes and file names

Name every session by the teacher's code from the profile, and name files by it:
`Science 1.7 - Pump build - packet.docx`, `Science 1.7 - Pump build - deck.html`. Put the code in
the packet's `meta.code` so it leads the header and footer, and in the deck's day tag. A file that
arrives already named needs no renaming in Drive, and the next lesson can find it by its code. Use a
plain hyphen in file names, never a dash or a slash.

For viewing guides, multi-day packets, and review games, read `references/formats.md`.

## Photographs

`references/photographs.md` governs them end to end — where one is required, how to choose it so it
argues for the slide's claim instead of merely matching the topic, how to aim the crop, how to
judge what came back, and the four patterns. Read it whenever you build a deck.

The two things worth carrying in your head before you get there: **write the claim and the frame
test before you search**, because a search for the topic returns pictures of the topic and none of
them argue for anything; and **the load probe is not the quality gate** — bytes arriving says
nothing about whether the subject is in frame.

## Step 4 — Test: hand it over

The deck is a prototype until it has been in front of students, however clean it checks. So the
handover is set up for the test that hasn't happened yet, not presented as a finished thing.

Present both files, then write the lesson plan into the chat as described in Step 3. In the same
message:

- **What to watch for.** Name the one moment the lesson is most likely to fail and the observable
  that would tell him it did — the point of view from Step 2 says where that is. *"If they can't
  say which faces are hidden, the box model didn't land; that shows up at question 3, not
  question 1."* This is the difference between handing over a lesson and handing over a test.
- Say what the talk moves need (partner assignments, corner signs, cards) if they need anything,
  and offer to make the printable if so.
- If the photographs could not be load-tested this session, say so in one line.
- **Ask for reaction in the I like / I wish / What if form** — "tell me an *I like*, an *I wish*,
  and a *what if*." It reads as an invitation rather than a request for approval, and "I wish"
  gets an honest complaint out of a busy person faster than "any changes?" does. Run it on your own
  draft first: if you can't name your own *I wish*, you haven't looked hard enough.
- Offer 3 specific next moves drawn from this lesson — not "let me know if you want changes." For
  example: *"Want me to (1) build the Day 5 lab that follows this, (2) cut the packet to five
  questions for a shortened period, or (3) add a second-tier version of question 4 for the students
  who finish early?"*

- **End with the Day map row**, ready to paste into the profile's project knowledge:
  `| Science 1.7 | Tue 9/29 | Pump build: criteria and constraints | |` — the last cell empty for
  how it went. In a claude.ai project the skill can't edit project knowledge itself, so this line
  is how the unit arc stays current without anyone retyping it.

If he comes back after teaching it, that is the only real test data this lesson will ever produce.
Fold it into the next lesson's point of view, and give him the finished Day map row with the "how it
went" cell filled.

Keep the machinery invisible. Say "student packet" and "slide deck," never "JSON" or "renderer";
the only file names he sees are the lesson-coded ones he will keep.

---

## Before you call the deck done

`scripts/check_deck.py` enforces the mechanical rules — photo count, duplicates, alt text,
captions, credits, aimed crops, the fallback script, leftover placeholder text, base64 bloat, empty
bodies. Run it and get it clean; the closing checklists in `references/deck.md` and
`references/photographs.md` cover the judgement calls it can't make.

Click the video once before you hand it over — the checker can tell you the id is well-formed and
the poster is there, but only a click tells you the player actually appears.

The two questions worth asking yourself once the checker is quiet, because nothing automated will
ask them for you: *does every photograph argue for the claim on its slide*, and *would a student
looking at any single slide for ten seconds, hearing nothing, come away with something.*

A third, which the checker can only half-ask: read the Spanish lines end to end. The checker knows
they exist and that they are short; it cannot tell you that they say the task, that they use the
same numbers and terms as the English, or that a slide's line matches the packet's.

---

## What good looks like here

This is a self-contained class of students who are two to six years below grade level in reading
and often carry attention and processing supports. The lesson that works has short blocks, one
instruction at a time, a reason to talk to a partner, something to look at that isn't text, and writing
tasks small enough that finishing is realistic. Rigor lives in the thinking a question demands,
never in the volume of writing it requires. A packet with six good questions and room to answer
them beats one with twenty.

