# What a good slide is made of

These are the output criteria for every deck. They come from one room: students who read two to
six years below grade level, several with attention, processing, or fine-motor supports, some
reading English as a new language, and a projector that washes out contrast. Each criterion says
what it protects. `check_deck.py` enforces what can be measured; the rest is judgment, and this is
what the judgment is for.

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

**Key words look the same on the wall and the page.** Each key word is marked once on a slide,
where it first appears, bold with a yellow stroke like the packet's, so recognition carries across
from screen to paper. Once, because yellow everywhere marks nothing.

**Every guess counts.** A game round, a sort, a hinge question or any format in
`references/interactives.md` puts every student's thinking in play at once and gets students out
of their seats to the board; partners agree first, so it is talk, not a quiz. Points and teams only
when the teacher asks for them, and a hinge question never.

**The prediction comes first.** Every reveal waits for a guess, and a clicker's → reveals a game's
answer before it turns the slide, so the answer can never arrive ahead of the thinking.

**Nothing jumps.** Answers and reasons hold their space before they appear. A student who reads
slowly keeps their place on the screen when the answer lands.

**Fits the screen it lands on.** Type scales to the screen's shorter side, a slide that still runs
long shrinks a step at a time, and as a last resort it scrolls; text never runs under the footer.
A 16:9 projector, a 4:3 projector and a laptop presenting in a browser window all read the same.

**Hands, not only eyes.** Anything that drags can be tapped instead (tap the card, tap where it
goes), for a touch board and for students whose fine-motor supports make dragging hard.

## Cost

The deck is built from its content alone: the model writes the slides and `build_deck.py` supplies
the template around them, so no build reads or rewrites the template. Photographs are judged on
one contact sheet per slot (`find_photos.py search`) and load-tested from the sandbox
(`find_photos.py pick` and `probe`), never one screenshot at a time and never in a browser tab.
