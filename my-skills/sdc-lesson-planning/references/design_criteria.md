# What a good page and a good slide are made of

These are the output criteria for every packet and deck. They come from one room: students who read
two to six years below grade level, several with attention, processing, or fine-motor supports,
some reading English as a new language, and a copier that prints in grey. Each criterion says what
it protects. The two checkers enforce what can be measured; the rest is judgment, and this is what
the judgment is for.

## The worksheet

**Printed from Google Docs.** Zac prints from the Google Doc that "Add to Drive" makes, so that is
the page that counts. Docs ignores Word's keep-together settings and splits tables anywhere; the one
thing it never splits is a single table row. So the renderer carries every task, with its heading,
its lines, and the table or organizer that answers it, in one borderless row, and Docs moves it
whole or not at all. Docs also sets text about a twentieth taller than Word; `check_packet.py`
estimates the Docs fill of every page and budgets against that, and checks a PDF exported from the
Google Doc directly when there is one.

**One sheet, both sides.** A 60-minute lesson fits on two pages; a 90-minute block aims for two and
never takes more than four. Every page is at least three-quarters full, and the page count is even,
so nothing prints with a blank back. `check_packet.py` measures this; run it every time.
*Protects:* paper, copier time, and a student's sense that the task is finishable.

**How to get there, in order.**
1. Take off the page anything a student doesn't act on. A section where students listen belongs on
   the slides; the packet holds the tasks.
2. Merge tasks that share rows. A vote and a report-out about the same six parts are one table
   with two columns, filled at two moments.
3. Merge questions that share a setup. Two questions about the same build are one question with
   two sentence starters.
4. Let a short block fill the gap a tall one leaves: a note, a word bank, or a one-line question
   placed after the table instead of before it.
5. Only then cut a question.

**No ink on structure.** Hairlines and rules draw the page; nothing is filled grey. A fill costs
toner on every copy, prints as mud on a tired copier, and lowers the contrast of the text on it.
The renderer draws this way; don't ask it for shading.

**Readable at a struggling reader's pace.**
- Verdana 12, left-aligned, never justified. No italics anywhere: italic costs a striving reader
  speed, and the students reading the language line have the least to spare.
- The language line is 11 point in a dark grey, directly under its English. It is support, not
  fine print.
- One task per numbered item. A prompt says what to do in one sentence; context, if any, is one
  sentence before it.
- Capitals only for short labels (section names, "I CAN", "WORD BANK"), never for sentences.

**Writing space sized to the answer.** Writing lines are 30 points apart, wide enough for a student
whose plan covers fine-motor needs. A sentence starter is printed on the first writing line itself,
with gaps on the rule where the words go, so the student starts writing where the sentence starts.
Count lines by the answer: a word or a number, one line; a sentence, two; an explanation, three.
A box is for drawing or showing work, never for a sentence.

**Graphic organizers match the thinking.** Pick the organizer from what the task asks the mind to
do, and use the same one for the same kind of thinking all year, so its shape becomes a cue:

| Thinking | Organizer |
|---|---|
| Compare two things | `tchart` |
| Look closely | `notice_wonder` |
| Order, process, cause and effect | `flow` |
| Argue from evidence | `cer` |
| Own a new word | `frayer` |
| Record class data | `fill_table` |
| Choose | `choices` on the question (circle one) |

An organizer, its question, and its heading stay on one page; the renderer keeps them together.

**Headings are one line.** Section name, its gloss in the room's language, the minutes flush right.
*Protects:* about a third of a page across a packet.

## The slide

**Something to look at, always.** Every content slide carries a photograph, a chart, or a diagram,
and so does every talk slide: students talk best about a thing in front of them. The talk layout
puts the visual on the left at the size of a wall and the turns on the right. The screen is never
blanked. Click any photograph and it opens at full size with the slide's question under it, for
close looking.

**Readable from the back row.** Headlines are the largest text; everything a student reads (card
text, directions, sentence starters, the language line) is at least about 1.6% of the screen width,
roughly 20 pixels on a 1280-wide projector, and in ink, not grey. Grey is for chrome only:
the eyebrow, the credit, the slide counter. Projectors wash contrast out; the template's colours are
chosen to survive it.

**One idea per slide, and nothing summarized under it.** A slide says one thing, in a headline that
is a claim. The only line under the body is a direction students physically follow.

**The same words on the wall and the page.** The question on a slide is the packet's wording, the
sentence starter is the packet's, the packet page is named on the slide. A student looking up should
recognize the task without re-reading it.

**Predictable routines.** The same move looks the same every day: a talk slide always has the
turns on the right and the starter at the bottom, the timer always sits top right, the packet page
always sits in the eyebrow. Predictability is an accommodation: it frees working memory for the
content.

**Time you can see, talk you can hear.** Anything with a fixed length has a timer; every talk move
runs on phases that chime, so the teacher can listen instead of watch the clock.

**Read aloud on demand.** A reads the slide: headline, each language line in its own voice, the
direction. For a student who can't yet read the question off the wall, the wall reads it to them.

## Cost

The deck and packet are built from their content alone. The model writes the slides
(`build_deck.py` supplies the template around them) and the packet's JSON (`render_packet.py`
draws it), so no build reads or rewrites the 60 KB template. Pages and slides are checked as one
image each (`check_packet.py --sheet`; one screenshot per photo slot on a contact sheet), not one
screenshot at a time.
