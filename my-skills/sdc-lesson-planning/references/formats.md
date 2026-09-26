# Session shapes beyond the single lesson

Most requests are one class session: one packet, one deck, one plan in chat. Three other shapes
come up often enough to have their own rules. Each keeps the parts that never change (lesson code,
objective and standard, the language lines, the accommodations from the profile, the plan in chat
with an answer key) and changes only what the shape needs.

| Shape | Asked for as | Files |
|---|---|---|
| Viewing guide | "a viewing guide for Top Gun", "worksheet for this tubing video" | Packet only, unless slides are asked for |
| Multi-day packet | "Day 1 and 2 of field trip prep", "one packet for the whole week" | One packet; one deck per day, or one deck with a day divider |
| Review game | "make a Jeopardy for this", "a game to review the six parts" | One HTML game from `assets/review_game_template.html` |

When the request doesn't name a shape, it's a lesson. When it names one of these, skip the parts of
Steps 2-3 that don't apply (a viewing guide has no movement or chart requirement) and say in one
line which shape you're building.

---

## Viewing guide

A guide students fill in while a film or a video plays. The footage is the lesson; the page is what
keeps attention on the part of the footage that matters.

**Segments are the structure.** One `heading` per stop, named for what happens and marked with where
it is: `"Running the lines — 5:16"`. The minutes on the heading are the footage between stops.

- **Online video:** get the timestamps from the transcript or the chapter markers of the verified
  video, never from memory. If you can't see either, name the segments without times and say so in
  one line; a wrong timestamp sends the class scrubbing through footage in front of everyone.
- **Feature film:** name scenes, not times ("the canyon run", "the final dogfight"). Classroom copies
  and streaming cuts drift by minutes.

**What goes on the page, in order:**

1. A before-you-watch prediction, one question, with a stem.
2. The words to watch for, as a `table`: *Word · What it means · the word in each home language*.
   This is the one table whose last column carries the home languages, because the word itself is
   the task.
3. The segment questions. Most are answerable in the moment: a word or number from the footage in a
   stem (`He uses ______ mm tubing`), or circle-one (`MORE lift or LESS lift`). A question that needs
   a composed sentence goes at a pause, not while footage runs. The prompt may carry one sentence of
   context before the question (the Mach 10 fact before the "why so long to shape it" question); the
   language line still carries only the question.
4. A closing transfer question that ties the footage to the class project: *one thing to copy on our
   system, and one thing you'd do differently*, or *which force matters most for your glider*.

**How many questions.** About one per two to three minutes of a short video. For a feature film, four
to six per viewing day, placed at the scenes that carry the physics, not spread evenly. Across a
multi-day film the total can pass the usual eight; the per-day count is what has to be finishable.

**The plan in chat** gives the stop points, the answer key with where in the footage each answer
appears, and the one scene to pause on if time runs short. No deck unless one is asked for; if it is,
one pause slide per stop, carrying that stop's question and a timer.

---

## Multi-day packet

One packet that runs across two or more sessions, because the work does (a budget planned on Day 1
and checked on Day 2, a build over a week).

- The header says so: `meta.day` reads `"Field trip prep — Day 1 & 2"` and `meta.period` reads
  `"60 min each day"`.
- Each day opens with a `heading` naming the day and its question (`"Day 2: Check it and finalize
  it"`), and each day's blocks sum to that day's period on its own.
- **A page break before every day after the first**, so a day can be handed in or kept on its own.
- Day 2's do-now reaches back to a Day 1 answer by name: *"What was your near-miss category from
  yesterday?"* It is the cheapest retrieval in the packet and it tells you in five minutes who
  kept Day 1.
- A take-along page (the checklist that goes to Scrap SF, the data sheet that goes to the garden)
  sits last, on its own page, under a `note` banner saying where it goes.
- The plan in chat covers every day in order, each with its own agenda summing to the period.
  Offer one deck per day by default; a single deck with a divider slide per day only if asked.

---

## Review game

A Jeopardy-style board on the projector, built from `assets/review_game_template.html`. Copy the
template and fill the `GAME` object at the bottom — title, categories, clues. The board, scoring,
keyboard controls, and dark and light themes are already wired; change nothing else.

- **Categories** are the lesson's parts or the unit's ideas (the six parts of the system, the four
  forces). Two to six of them.
- **Values are rungs, not random.** 100 is a fact a student can guess from everyday life, 200 applies
  it to our build, 300 asks why. Every question should be a *fair guess*: nobody needs to already
  know the answer, which is what keeps the whole room in it.
- **Each clue carries** `q` (the question), a line for each language in `GAME.languages` under its
  code (`es`, `zh` …, the same abbreviated line as the packet), and `a`, the reveal: one or two
  sentences of explanation a student could repeat to a partner, not a bare answer.
- **Run it as talk.** Partners get think time and agree on a guess before a team answers. Say so in
  the plan; it turns a game into a talk move.
- Name it by the lesson code, `Science 1.6 - Readiness game.html`. In claude.ai, also show it as an
  artifact so it opens straight from the chat.

Before handing it over: every category has one clue per value, every clue has its language lines,
and every reveal explains rather than only answers.
