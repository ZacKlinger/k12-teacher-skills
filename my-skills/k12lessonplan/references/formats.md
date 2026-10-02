# Session shapes beyond the single lesson

Most requests are one class session: one packet, one deck, one plan in chat. That is the default,
always. Three other shapes come up often enough to have their own rules. Each keeps the parts that never change (lesson code,
objective and standard, the language lines, the accommodations from the profile, the plan in chat
with an answer key) and changes only what the shape needs.

| Shape | Asked for as | Files |
|---|---|---|
| Multi-day lesson | "Day 1 and 2 of field trip prep", "one packet for the whole week", "plan Monday through Wednesday" | One packet with a section per day; one deck per day |
| Viewing guide | "a viewing guide for Top Gun", "worksheet for this tubing video" | Packet only, unless slides are asked for |
| Review game | "make a Jeopardy for this", "a game to review the six parts" | One HTML game board, built by the `k12presentation` skill |

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

## Multi-day lesson

Only when the request names more than one session: "Day 1 and 2", "this week", "Monday through
Wednesday", "a two-day lab". Never stretch a single request into several days on your own, and
never fold tomorrow's lesson into a week because the unit has more to cover; offer the next day
as one of the three next moves instead. "Tomorrow" is one lesson.

The work runs across days (a budget planned on Day 1 and checked on Day 2, a build over a week), so
the packet does too, and every day still stands on its own:

- **Every day keeps its own code and its own minutes.** Science 1.7 and Science 1.8, each with its
  minutes read off the schedule for its own weekday (Monday's block and Wednesday's period are not
  the same length), and each day's blocks summing to that day's period.
- **One packet, one `day` block per day.** The `day` block (`references/packet.md`) opens each day
  with its code, its minutes, its title, and its own "I can". Every day after the first starts on a
  fresh page with its own name line, so a day can be handed out, collected, or reprinted from the
  Google Doc by itself. Leave the top-level `objective` out; each day carries its own.
- **Each day is one sheet, both sides.** Two pages per day, which also means every day starts on
  the front of a sheet when the stack is copied double-sided. A block day aims for two and never
  passes four, and always an even number. Check it with
  `check_packet.py ... --days <n>`: it finds each day and errors on a day that would start on the
  back of a sheet or spill in Google Docs.
- **The header says the range**: `meta.code` is `"Science 1.7-1.8"` (plain hyphen), `meta.title`
  is the shared title, `meta.day` reads `"2 days"`. The file is
  `Science 1.7-1.8 - Field trip prep - packet.docx`.
- Day 2's do-now reaches back to a Day 1 answer by name: *"What was your near-miss category from
  yesterday?"* It is the cheapest retrieval in the packet and it tells you in five minutes who
  kept Day 1.
- A take-along page (the checklist that goes to Scrap SF, the data sheet that goes to the garden)
  sits last, on its own page, under a `note` banner saying where it goes.
- **One deck per day**, each named by its own code (`Science 1.8 - Check it - deck.html`), so the
  deck on the projector always matches the day on the page. A single deck with a divider slide per
  day only if Zac asks for it.
- **The talk-through in Step 2 covers the whole arc first**: one point of view for the run, then
  each day's objective, agenda and spine in order, so a wrong turn on Day 1 is caught before Day 3
  is built on it. The plan in chat then covers every day in order, each with its own agenda, look
  fors, predicted errors and answer key. A Day map row for each day.

---

## Review game

A Jeopardy-style board on the projector is a slide shape, so the slideshow skill builds it: load
`k12presentation` and ask it for "a review game board", handing it the packet. In the plan, say the
game runs as talk: partners agree on a guess before a team answers.
