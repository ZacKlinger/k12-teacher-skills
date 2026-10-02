---
name: "sdc-lesson-planning"
description: "Plans a class session for Zac's SDC (special day class) grades 9-10 science and math, then delivers a student packet built to print from Google Docs, with the lesson plan written straight into the chat. The HTML slide deck is built from that packet by the sdc-slideshow skill: in the same turn when Zac asks for slides, offered otherwise. Load this skill BEFORE asking any clarifying question about the lesson. Use it whenever Zac is planning what to teach: explicit asks (\"plan tomorrow's lesson\", \"Science 1.7\", \"Day 4 of the hydroponics unit\") and implicit ones (\"I'm teaching surface area Thursday\", \"need something for period 3 tomorrow\"). Also use it for just a packet, just slides, or just an agenda, a viewing guide, a review game such as a Jeopardy board, or a multi-day lesson when he asks for more than one day. One session at a time unless asked. Do NOT use it for grading, rubrics, IEP paperwork, parent emails, or standards lookups; answer those directly."
license: MIT
---

# SDC lesson planning (grades 9-10, science and math)

Builds one class session at a time for a self-contained special day class, and more than one only
when Zac asks for more than one day. Zac is the teacher — "you" in these instructions, never a
third party. The plan in chat and the packet every time; the deck when he asks for it, offered
otherwise:

| Deliverable | Format | Who holds it |
|---|---|---|
| Lesson plan | **Chat message, never a file** | Zac, read on screen |
| Student packet | Word document that Zac adds to Google Drive, where it becomes the Google Doc he prints | Students, on paper |
| Slide deck | Single HTML file opened in Chrome, built by the `sdc-slideshow` skill from this packet, in this conversation or a later one | Projected; students use it to navigate the packet |

Both files travel through Google Drive, and the Google Doc is the page students actually get; see
"Google Drive" below for what that asks of every build.

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

1. **Project profile.** In Cowork, look in the working folder for `project-profile.md`,
   `PROJECT.md`, `course-profile.md`, or anything under a `lesson-planning/` or `unit/` folder; in a
   project, it may be in the project knowledge instead. It holds the course, the lesson-code
   format, the weekly schedule, the home languages, the accommodations and UDL checklists, the unit
   arc, and equipment on hand. Read the class notes beside it too, the file named exactly what the
   project is called (`SDC Science.md`; see "Class notes"): what works with this class, the words
   they own, the pairings that work.
2. **The session length, from the schedule.** Turn the request's date ("tomorrow", "Thursday",
   "the 30th") into a weekday using today's date, and read that day's minutes and notes off the
   profile's schedule. A day listed under "days that break the pattern" wins. This is the answer to
   "how long is the session", so don't ask it when the schedule has it.
3. **The previous lesson.** Work out the code before this one (Science 1.7 follows Science 1.6)
   and find it: in the working folder or the conversation first; then, when Google Drive is
   connected, search Drive for the code: `title contains 'Science 1.6'`, then
   `fullText contains 'Science 1.6'` (which finds a day inside a multi-day packet), then the unit
   name; read the packet. It tells you what students already did, what vocabulary
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

- `references/design_criteria.md` — what a good page is made of: the page budget, ink,
  readability, key words, organizers, whole tasks. Everything below serves it.
- `references/packet.md` — the student packet rules and the `packet.json` schema.

The deck has its own skill, `sdc-slideshow`, with its own references (the slide spec, the chart
kit, the photographs method, games); it reads them when you hand the deck over below.

Order of work: settle the plan and the packet content first, then build the deck from that same
content so the two cannot drift. Slide text is drawn from the packet's actual wording — a student
looking up at the screen should see the same question they're reading on the page, in English and
in Spanish both.

**Student packet (Word).** Write `packet.json`, then render:

```bash
python3 scripts/render_packet.py packet.json "$OUTPUT_DIR/<code> - <short title> - packet.docx"
```

Never write layout code by hand, and never edit the rendered document — every change goes back
into `packet.json` and re-renders instantly. The renderer prints every task whole, prompt and
answer space together, so no page break ever separates them. List the lesson's key words in
`meta.vocab` and each one prints highlighted the first time a section uses it; mark the questions the reduced
packet can drop with `"core": false`. The packet stays text and line art: photographs live on the
screen, where they are in color and the size of a wall.

The render prints how the page reads: a grade estimate against the profile's reading level, the
sentences over twenty words, and the long words that aren't key words. Fix each sentence and word
it names before you check pages (`references/packet.md`, "Reading level").

Then check it the way the copier will meet it:

```bash
python3 scripts/check_packet.py "$OUTPUT_DIR/<code> - <short title> - packet.docx" --max-pages 2 --sheet pages.png
```

It reports the page count against the budget and how full each page is, estimated for Google Docs,
because Zac prints from the Google Doc that "Add to Drive" makes, and Docs sets the same file about a
twentieth taller than Word. It writes every page into one image. Look at that image once, then fix what it reports in `packet.json` in the order
`references/design_criteria.md` gives (take off, merge, fill the gap, then cut) and re-render. Two
pages for a 60-minute lesson; a block aims for two and never passes four. A multi-day packet adds
`--days <n>` and is checked a day at a time, each day its own sheet.

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
   One line on UDL: the move this lesson makes for engagement, for representation, and for action
   and expression, one each (see "Universal Design").
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

**Slide deck: built when asked, offered otherwise.** The deck is its own skill, `sdc-slideshow`, so
it can be built now or in any later conversation from the packet alone. Build it in this turn when
the request asks for slides or a deck, or when the class notes' standing requests say every lesson
gets one: once the packet renders clean, load `sdc-slideshow` (it is installed beside this one) and
follow it, handing it `packet.json` and the plan you are about to deliver. The code, the minutes,
the languages and the key words ride in the packet's `meta`; the talk moves, the photographs you
promised by subject and the verified video come from the talk-through in Step 2. The deck is the
packet seen on the wall, so it is built from the packet's words and checked against them, never
reworded. Photographs are its job too: never ask Zac for one. Otherwise deliver the packet and the
plan, and make the deck the first of the next moves in Step 4. If `sdc-slideshow` isn't installed,
say so in one line and deliver the packet and the plan.

Then check the whole lesson the way it will be taught: list `$OUTPUT_DIR` and confirm every file
exists and is non-trivial in size; look at the packet's page image from `check_packet.py`; read the
slideshow skill's report when there is a deck. Work every calculation in the lesson — the answer
key, the worked example, the numbers on the slides, the game answers — they all have to agree.

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

`references/packet.md` carries the `"es"` field and the list of blocks that take one; the slideshow
skill puts the packet's own lines on the slides and checks them against the packet.
`render_packet.py` reports any question missing a line — it is the only thing checking the page, so
read what it prints.

## Accommodations

The profile's accommodations checklist is part of the lesson from the first draft, not a revision
after it. Build every ticked item in by default: stems, word banks, large print
(`meta.large_print`), chunked directions, the reduced-item marking, response choices. In the plan's
Differentiation line, name each ticked accommodation and where it landed ("large print: whole
packet; word bank: above 3 and 5"). If the profile has no checklist, use the stems and word banks the
packet rules already call for and ask nothing.

**The reduced packet** is the same lesson for the students on modified assignments: the questions
marked `"core": false` left out, part (a) only, large print, and one word bank on the front page
and nowhere else, with the same question numbers so it matches the slides. Build it when Zac asks
(`render_packet.py ... --reduced`, `references/packet.md`), and when the profile ticks reduced item
count, offer it as one of the three next moves.

## Universal Design

The profile's UDL checklist is design for the whole room, where the accommodations are supports
for particular students. Every lesson carries at least one move from each of the three groups,
engagement, representation, and action and expression, taken from what the profile ticks, and
the plan's Differentiation line names the three. Two strategies are not enough: a lesson that only
adds stems and a word bank has given every student the same single way in. With no profile, pick
one per group yourself; the key words, the talk moves and the organizer already cover most of it.

## Class notes

The class notes are one file beside the profile in the working folder, **named exactly what the
project is called**: the SDC Science project keeps `SDC Science.md`, the SDC Math project
`SDC Math.md`. Take the name as Zac wrote it, spaces and capitals included, from the project's own
name in Cowork (the working folder's name when that is all you can see), so the file is the one
he recognizes in the folder and in Drive. The skill keeps it, so Zac never has to: start it from
`assets/class_notes_template.md` the first time there is something to put in it. Read it in
Step 0. Update it at the end of every lesson and whenever he says how one went:

- A pattern that held twice goes under *What works* or *What doesn't* ("votes at the board settle a
  fight faster than discussion"); a one-off stays out.
- A key word students used correctly on their own goes under *Words they own*, with the lesson
  code, only when he says so or their work shows it; never assume it.
- Pairings and roles that worked, by role, never by name.
- Anything he says once that should hold every time goes under *Teacher's standing requests*, and
  from then on it holds.

Keep it under about sixty lines by merging and trimming, never by deleting his edits. Describe
students by need or role, never by name. Where there is no folder to write to (a claude.ai project
without a working folder), skip the file and carry what you learned into the next lesson's point
of view instead.

## Lesson codes and file names

Name every session by the teacher's code from the profile, and name files by it:
`Science 1.7 - Pump build - packet.docx`, `Science 1.7 - Pump build - deck.html`. Put the code in
the packet's `meta.code` so it leads the header and footer, and in the deck's day tag. A file that
arrives already named needs no renaming in Drive, and the next lesson can find it by its code. Use a
plain hyphen in file names, never a dash or a slash.

**One session at a time is the default.** Build more than one day only when Zac asks for more than
one ("Day 1 and 2", "this week", "Monday through Wednesday"); then use the multi-day shape in
`references/formats.md`: one packet with a section per day, every day on its own sheet under its
own code, and one deck per day. Viewing guides and review games are in the same file.

## Google Drive

Everything Zac keeps lives in Google Drive, so every file is built for the trip there and for what
students meet at the other end.

**The path.** The packet arrives as a lesson-coded `.docx`. Zac adds it to Drive, it becomes a
Google Doc with the same name, and he prints from that Doc; the Doc is the student's page, not the
Word file. The deck is one HTML file he opens with **Open in Chrome**. A copy kept in Drive is for
keeping: Drive previews an HTML file as its code, so presenting from Drive means downloading the
file and opening it in Chrome.

**The packet survives Docs because the renderer builds for Docs.** Docs ignores Word's
keep-together settings and splits tables between rows, but never splits a single row, so every task
prints as one row and moves whole or not at all. Docs sets text about a twentieth taller, so
`check_packet.py` budgets for Docs, not Word. Verdana, black text, hairline rules, and no fills all
come through the conversion and the copier unchanged. So never hand-edit the `.docx` or reach for
what Docs drops or moves: text boxes, floating images, columns, shapes, a second page size. Every
change goes back through `packet.json`.

**Real text, for the student on a screen too.** Every question, direction and language line is
text, never a picture of text, so a student who opens the Doc on a device can have it read aloud,
zoom it, or search it, and the lesson code in the header and footer is what Step 0 searches for
next time.

**The deck works from anywhere it lands.** The slideshow skill builds it as one file: timers,
charts, talk kit and games inside it, photographs and the video linked by URL, so it works opened
from the working folder, from a Drive download, or from a USB stick on the classroom computer.

**What the skill does in Drive itself.** It reads: the previous lesson, by its code (Step 0). It
doesn't upload the packet; the lesson-coded file name already makes adding it one step with
nothing to rename.

## Step 4 — Test: hand it over

The deck is a prototype until it has been in front of students, however clean it checks. So the
handover is set up for the test that hasn't happened yet, not presented as a finished thing.

Present the files by their lesson-coded names, packet first, so each is one step into Drive. Then
write the lesson plan into the chat as described in Step 3. In the same message:

- **What to watch for.** Name the one moment the lesson is most likely to fail and the observable
  that would tell him it did — the point of view from Step 2 says where that is. *"If they can't
  say which faces are hidden, the box model didn't land; that shows up at question 3, not
  question 1."* This is the difference between handing over a lesson and handing over a test.
- Say what the talk moves need (partner assignments, corner signs, cards) if they need anything,
  and offer to make the printable if so.
- When there is a deck, pass on anything the slideshow skill reported that he should know, in a
  line each: photographs
  it couldn't load-test (and the setting that fixes it), a video that won't play embedded.
- **Ask for reaction in the I like / I wish / What if form** — "tell me an *I like*, an *I wish*,
  and a *what if*." It reads as an invitation rather than a request for approval, and "I wish"
  gets an honest complaint out of a busy person faster than "any changes?" does. Run it on your own
  draft first: if you can't name your own *I wish*, you haven't looked hard enough.
- Offer 3 specific next moves drawn from this lesson — not "let me know if you want changes." For
  example: *"Want me to (1) build the Day 5 lab that follows this, (2) cut the packet to five
  questions for a shortened period, or (3) add a second-tier version of question 4 for the students
  who finish early?"* When no deck was built this turn, the deck is the first of the three, and
  the offer says it works later too: *"(1) build the slide deck from this packet: now, or in any
  later chat, from the packet file or its Google Doc downloaded as Word, with this plan pasted
  beside it."*

- **Keep the Day map current yourself.** In Cowork, append this lesson's row to the profile's Day
  map in the working folder (`| Science 1.7 | Tue 9/29 | Pump build: criteria and constraints | |`,
  the last cell for how it went), and create the profile from `assets/project_profile_template.md`
  if there isn't one. Only where there is no folder to write to, hand the row over to paste.
- **Update the class notes** (see "Class notes") without mentioning it unless something changed
  that he should know about.

If he comes back after teaching it, that is the only real test data this lesson will ever produce.
Fold it into the next lesson's point of view, fill the "how it went" cell of the Day map row
yourself, and update the class notes.

Keep the machinery invisible. Say "student packet" and "slide deck," never "JSON" or "renderer";
the only file names he sees are the lesson-coded ones he will keep.

---

## What good looks like here

This is a self-contained class of students who are two to six years below grade level in reading
and often carry attention and processing supports. The lesson that works has short blocks, one
instruction at a time, a reason to talk to a partner, something to look at that isn't text, and writing
tasks small enough that finishing is realistic. Rigor lives in the thinking a question demands,
never in the volume of writing it requires. A packet with six good questions and room to answer
them beats one with twenty.

