# The student packet

Read before writing `packet.json`. The renderer handles layout; these are the content rules.

## What earns a spot on the page

A packet holds the **essential questions only** — the ones that make a student think about the
objective. Everything else is busywork, and busywork is expensive here: it eats the minutes a
struggling reader needs for the questions that matter, and it teaches students that the packet is
something to survive rather than something to use.

Cut anything that is:

- a definition they can copy without understanding it,
- the same skill practiced a fifth time when three showed mastery,
- a "warm-up" that isn't the do-now,
- a question whose answer is already printed above it,
- a graphic organizer nobody will look at again.

**Length caps.** 60-minute period: 5 to 8 tasks, 2-3 pages. 90-minute block: 8 to 12 tasks,
3-4 pages. If the content won't fit, the lesson is too big for the period — say so during the
talk-through rather than shrinking the write space.

The Spanish lines (below) cost about a line each — roughly a third of a page on a full 8-task
packet. The caps do not move to make room for them. When a packet is running over, the space comes
from cutting a task, never from shrinking the write space or dropping the Spanish.

## Room to write

Undersized answer space tells a student their thinking doesn't fit. Size the space to the answer
you actually want:

| Answer | Space |
|---|---|
| A number, a word, a circle | `{"kind": "lines", "count": 1}` |
| One sentence | `{"kind": "lines", "count": 2}` |
| Two to three sentences | `{"kind": "lines", "count": 4}` |
| Math work | `{"kind": "box", "height_in": 1.6, "label": "Show your work"}` |
| A drawing, a diagram, a model | `{"kind": "box", "height_in": 2.6, "label": "Draw it"}` |
| Answered in a table or on the board | `{"kind": "none"}` |

Writing lines are set at 30-point pitch — big-handwriting friendly. Don't shrink them.

**Sentence starters sit on the writing line.** A question's `stems` print on its first lines, with
gaps on the rule where the words go and a trailing blank left as the rest of the line, so the
student starts writing where the sentence starts. `count` is the total number of lines, the
starters' own lines included: one starter and one sentence of answer is `count: 2`.

**Circle one** is `"choices": ["not yet", "almost", "ready to go"]` on the question, not a list
inside the prompt. The options print on their own line, spaced wide enough to circle.

**Graphic organizers** are an `organizer` block, chosen by the thinking the task asks for
(`references/design_criteria.md` has the table):

```json
{"type": "organizer", "kind": "tchart", "label": "Tank vs. garden", "columns": ["Our tank", "The garden"], "rows": 4, "es": "Compara."}
{"type": "organizer", "kind": "notice_wonder", "label": "Look at the frame", "rows": 3}
{"type": "organizer", "kind": "flow", "label": "Where the water goes", "steps": ["Tote", "", "", "Channels"]}
{"type": "organizer", "kind": "cer", "stems": {"claim": "The top gets ______ water."}}
{"type": "organizer", "kind": "frayer", "word": "impeller"}
```

**Page budget.** Two pages for a 60-minute lesson, even page counts, every page three-quarters
full. `scripts/check_packet.py` measures it; the order for fixing it is in
`references/design_criteria.md`.

## Every packet also carries

- **One reflection prompt**, usually under the closing: "Which part was hardest? What made it
  hard?" with two lines. It is the one place a student writes about their own thinking.
- **On a science day:** a "Draw it" box for the first model before the investigation, a second
  "Draw it again. Show how, not only what." box beside or below it for the revised model, and a
  closing claim-evidence-reasoning with three stems (claim, evidence from today's investigation,
  reasoning using the crosscutting concept). See `references/lesson_design.md`, "Science days".
- **Talk prompts** where a talk move happens during work on the page: the question and the stem
  the pair uses, with one line to write what they decided. Talk that leaves no trace on paper is
  easy to skip.

## Hints, examples, stems

Every question that could stall a student carries **one** support, chosen for what's actually hard
about it:

- `"example"` — a worked first item. Use when the format is the obstacle ("2.67 × 6 = 16.02").
- `"hint"` — the move, not the answer ("Multiply the acres for one person by 6").
- `"stems"` — for composed sentences, always, on that task.

A question with all three is over-supported and the page starts to look like a wall. Pick the one
that unlocks it.

## The Spanish line

Every question a student answers and every direction they have to follow carries **one short
Spanish line**, in an `"es"` field on the block, rendered directly under the English.

It is support, not translation. The line carries **the task and nothing else** — what to do, what
is being asked, the numbers involved. The framing, the context sentence, the worked example, the
scaffold: all of that stays in English, where the student is already getting it from the slide, the
photograph, and you.

```json
{
  "type": "question",
  "number": "3",
  "prompt": "Your diet has to feed **6 people for one year**. How many acres does that take?",
  "es": "Tu dieta alimenta a 6 personas por un año. ¿Cuántos acres necesitas?",
  "hint": "Multiply the acres for one person by 6.",
  "space": { "kind": "box", "height_in": 1.6, "label": "Show your work" }
}
```

**What takes an `"es"`:** `question` (the prompt), `text`, `labeled`, `note`, `list` / `steps` (one
line summarizing the direction, never one per item), `heading`, `wordbank`.

**What deliberately does not:** `hint`, `example`, `stems`, `parts`, and table headers. Those are
the exclusions that keep this abbreviated, and they are load-bearing — translating the hints and the
stems doubles the page, and a page that has doubled is a page a struggling reader stops reading. A
student who needs the Spanish needs it to know *what is being asked*; the support around the
question is already the shortest thing on the page.

**Length.** Shorter than the English, or the framing got translated too. This is also why the
exclusions matter to the page and not only to the reader: one line per task is a third of a page,
and translating the hints and stems as well would be a page and a half. The renderer reports any
line that ran more than about 20% over — Spanish naturally runs a little longer, so only a real
overshoot is worth reporting, and when it does, cut back to the task.

**Register.** Plain everyday Spanish, `tú`-form imperatives — *escribe*, *mira*, *explica*. Not
academic register, not `usted`. Keep the technical term in English with the Spanish beside it when
the cognate isn't obvious (*yield (rendimiento)*), because the term on the board, in the word bank,
and on the slide is the English one and a student has to be able to match them.

The renderer prints a note on any student packet question that has no Spanish line. Read those
notes; they are the only thing that checks this.

## Page breaks

The renderer binds each question to its hint, stems, and answer space, so a break can't split
them. What it can't decide for you is where a *section* should start fresh. Insert
`{"type": "page_break"}` when a new phase begins and the previous one ended near the bottom, or
when students will be working on one page while looking at a slide about another. Keep a table and
the question that feeds it on the same page — put the break before the pair, never between them.

A tall group — a question with an example, a hint, and a 2-inch work box — moves to the next page
whole rather than splitting, which can leave the bottom of a page open. That trade is correct, but
you can usually fill it: put the phase's short directions, its word bank, or a reference table
*after* the break instead of before it, so the short blocks land in the gap.

Render the packet before delivering, convert it to PDF, and look at the pages: no page should end
with a heading alone, no answer space should open a page without its question above it, and the
packet should not run a page longer than the caps above.

## Tiering on one page

Everyone gets the same packet. Push and support inside the task:

- `"parts"` splits a question into (a) everyone and (b) go further. Word part (b) as a real
  extension ("Now find how many fields the whole class would need"), never as "challenge for fast
  finishers."
- A `wordbank` block sits directly above the question that needs it.
- A `note` block carries a reminder in the student's language ("Acres are a way to measure land.
  One acre is about one football field minus the end zones.").

## `packet.json` schema

```
{
  "audience": "student" | "teacher",
  "meta":   {"code", "title", "course", "day", "period", "name_line": true,
             "languages": ["es"], "large_print": false},
  "objective": "I can …",
  "standard":  "CODE — ten-word gist",
  "agenda":  [["Do Now", 5], ["Model", 12], …],      // prints on the lesson plan only
  "sections": [ blocks ]
}
```

Blocks:

| Block | Fields | Use for |
|---|---|---|
| `heading` | `text`, `minutes?` | A phase title on the student page |
| `phase` | `name`, `minutes` | Same thing on the lesson plan |
| `question` | `number`, `prompt`, `es?`, `hint?`, `example?`, `stems[]?`, `parts[]?`, `choices[]?`, `space`, `minutes?` | Any task a student does |
| `text` | `text` | A sentence of directions or context |
| `labeled` | `label`, `text` | A short lead-in plus its line |
| `list` / `steps` | `label?`, `items[]`, `ordered?` | Directions, procedures, materials |
| `table` | `headers[]?`, `rows[][]` | Reference data students read |
| `fill_table` | `headers[]`, `rows[][]?`, `blank_rows?`, `row_height_in?` | An organizer students write into |
| `note` | `label?`, `text` | A boxed reminder, a watch-for, a teacher note |
| `wordbank` | `label?`, `items[]` | Vocabulary or numbers a task needs |
| `organizer` | `kind` (`tchart`, `notice_wonder`, `flow`, `cer`, `frayer`), `label?`, `es?`, and per kind `columns[]`/`rows`, `steps[]`, `stems{}`, `word`, `height_in?` | A graphic organizer matched to the thinking |
| `stem` | `text` | A standalone sentence frame |
| `space` | `kind`, `count`/`height_in`/`label` | Write space not attached to a question |
| `page_break` | — | Force a new page |
| `day` | `code`, `day`, `period`, `title`, `es?`, `objective?`, `standard?` | Opens one day of a multi-day packet (`references/formats.md`); every day after the first starts a new page with its own name line |

`heading`, `text`, `labeled`, `note`, `list` / `steps` and `wordbank` each take an optional `es`
as well — one short Spanish line, rendered under the block. See "The Spanish line" above.

**`meta` fields worth knowing.** `code` is the lesson code from the profile ("Science 1.7"); it
leads the header and the footer, so `course` can usually be left out and `day` can carry the unit
name ("Hydroponics"). `languages` lists the home languages in print order (default `["es"]`); each
block then takes one line per code, `"es"` and `"zh"` side by side, and the renderer reports any
question missing any of them. Right-to-left languages (`ar`, `fa`, `ur`, `he`) print right-aligned
on their own. `large_print: true` sets the whole packet about a quarter larger, for the students
whose plans call for it; it adds pages, so cut a question before it adds more than one.

`**bold**` works inside any text field. Nothing else marks up — no markdown headings, no pipes,
no emoji.

## There is no lesson-plan document

The renderer builds one file: the student packet. The lesson plan is written into the chat (see
SKILL.md Step 3), and the answer key goes there with it — not on a page that has to be printed,
hidden from students, and found again tomorrow.

`"audience": "teacher"` still exists in the renderer for the rare case where Zac asks for something
printed for himself — a station card, an observation grid, a set of corner signs. It is never used
for the plan.
