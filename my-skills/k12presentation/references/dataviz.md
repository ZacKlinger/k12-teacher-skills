# Data visualization — the center of the deck

Read this with `deck.md` whenever a lesson touches a number, which is nearly always. Six chart
types of the kit's own, and two more from `references/interactives.md`, all click-driven, all
configured with `data-` attributes — no chart is ever hand-drawn.

**The kit is already in `assets/deck_template.html`.** There is nothing to paste and nothing to
copy: write the chart's markup into a slide (each chart's attributes are under "Choosing the chart"
below) and `build_deck.py` wraps the slides in the template. `assets/dataviz_kit.html` remains the
source of truth for the kit and holds a working demo of each type.

Every chart needs **both** classes — `class="dv dv-bars"`. `dv` carries the colour variables and
the base type; `dv-bars` picks the type. With only the type class the chart builds and renders
*invisible*: labels, no bars, because `--dv-a` and its siblings are undefined. `check_deck.py`
catches this, but it is worth knowing why.

**Every deck carries at least one interactive chart, and two to four when the lesson has numbers
in it.** A what-if model and an estimate (`references/interactives.md`) count: both carry a real
number through the same predict-then-reveal moment. This is enforced, not encouraged: a deck with none has pushed the whole lesson back into
prose, which is the one channel these students cannot use. Static `.bars` from the deck's component
catalog do not count — they are for a comparison you don't need to reveal, and they skip the
predict-then-reveal moment that makes a number stick.

## Why this carries the lesson

For a student reading below grade level, or reading English as a new language, a paragraph
explaining that a hydroponic system uses a twentieth of the water is a wall. The same fact as two bars is instant,
and it stays. So the chart is not an illustration hung next to the explanation — **the chart is
the explanation, and the words on the slide are its caption.**

That inverts the usual order of writing a slide. Decide what the picture shows first. Then write
the six words that name what a student is looking at.

## The routine that makes a chart teach

Every chart in the kit starts empty or unrevealed, because the sequence that makes data stick is
always the same:

1. **Ask before you show.** "How much water do you think a field lettuce needs compared to ours?"
2. **Take a public guess.** The guess chart holds a draggable line; the dot plot takes their real
   numbers; the bars let you ask "what does the next one look like?" before the click.
3. **Reveal.** One click, or → on a clicker, or `V` (bars come one per press, so the room can guess
   before each). The gap between the guess and the truth is the moment the lesson lives in.
4. **Read it together, out loud, with a stem.** Reading a chart is a skill these students are
   still building. Give them the sentence: *"The ______ bar is ______ times bigger than ______,
   which means ______."*
5. **Write it once.** Every chart that carries a lesson idea gets one matching question on the
   packet, with the same stem. A chart nobody writes about is a chart nobody remembers.

## Choosing the chart

| What you're showing | Chart | Class |
|---|---|---|
| A percent, a rate, a share of a group | Icon array — 100 countable dots | `dv-icons` |
| A number worth predicting first | Guess then reveal | `dv-guess` |
| The class's own measurements | Live dot plot, built by clicking | `dv-dots` |
| Two to four quantities compared | Bars revealed one at a time | `dv-bars` |
| One value against the range it should be in | Gauge with a target band | `dv-gauge` |
| Percent increase or decrease | Percent strip — the chunk drawn on the base | `dv-percent` |
| A cause and its effect the class can push on | What-if model: sliders, a formula, a target band | `whatif` (interactives.md) |
| One quantity the class estimates as a range | Too low, just right, too high, then the real number | `estimate` (interactives.md) |

Each chart is one element with both classes and its `data-` attributes; every one also takes
`data-caption` (the finding, shown once revealed) and `data-hint`:

- `dv-icons`: `data-fill` (how many dots fill), `data-total` (default 100), `data-cols` (default 20).
- `dv-guess`: `data-actual`, `data-max`, `data-unit`, `data-ask` (the question above the plot).
- `dv-dots`: `data-bins="0-4|5-9|10-14"`, `data-ask`.
- `dv-bars`: `data-rows="Label|value|colour|note; Label|value"` (colour and note optional),
  `data-unit`, `data-prefix` (`$`), `data-ratio` (a line shown after the last bar).
- `dv-gauge`: `data-value`, `data-min`, `data-max`, `data-lo` and `data-hi` (the target band),
  `data-band-label`, `data-unit`.
- `dv-percent`: `data-base`, `data-pct`, `data-dir="up"` or `"down"`, `data-unit`,
  `data-before-label`, `data-after-label`.

```html
<div class="dv dv-guess" data-ask="How many litres does a field lettuce drink?" data-actual="40"
     data-max="60" data-unit=" L" data-caption="Forty litres in a field; ours drank two."></div>
```

Two rules of thumb. **The percent strip is the fix for the most common percent error** — a student
who has seen 20% drawn *on* the $65 bar stops answering "$13" to "what's the new price." And
**the gauge is the shape of every engineering verdict**: a measured value, the range it needs to be
in, and the visible gap between them.

## Rules that keep a chart readable

- **One message per chart.** If you'd need two sentences to say what it shows, it's two charts.
- **The heading states the message, not the topic.** "Our system is short on light," not "Light
  data." A student who reads only the heading should still get the finding.
- **Label directly.** Every value sits on or beside its own bar, dot, or line. No legends, no
  "see the key" — a legend is a second reading task laid on top of the first.
- **Six categories, maximum.** Four is better. Sort biggest to smallest unless time or a real
  order says otherwise.
- **Color means one thing all deck long.** Lilac leads — it is the first color chosen, the series
  the lesson is about, the "before," the thing being singled out. Mint is the target, the healthy
  case, or a value that grew. Peach is the problem or a value that shrank. Blue is the comparison
  series, butter the third option.
  Each pastel has a `-deep` sibling — pastels fill shapes, deeps carry text, numbers, and thin
  lines, because a pastel at label size on white vanishes from the back row. Never let color be the
  only carrier: the label says it too, for the colorblind students and for the projector that
  washes everything out.
- **Bars start at zero.** Always. A truncated axis is a lie told in a room where nobody can check it.
- **Units in words they own.** Gallons, minutes, football fields, water bottles, days. Convert
  anything else before it reaches the slide.
- **Real numbers only.** Sourced, or generated by the class. If a number can't be verified, use the
  class's own measurement instead; it's better data for the class anyway.
- **Two to four charts per lesson.** Every phase with a chart is a phase without one somewhere else.

## The kit is primitives, not templates

Every chart in `dataviz_kit.html` ships with demo numbers — lettuce, gallons, a $65 pair of shoes.
Those are placeholders and none of them should ever reach a slide. Each chart is configured
entirely through its `data-` attributes, so building one means deciding what this lesson's data
actually is and writing that in: the real values, the real labels, the real units, the caption that
states this lesson's finding.

Pick by the shape of the data, never by wanting variety. If none of the eight fits what the lesson is
showing, don't force one — use a plain figure, a table, or an SVG diagram from the deck's component
catalog. A chart that doesn't fit its data teaches a student to distrust charts.

## What makes one magnetic

A chart that merely displays is forgettable; the ones that hold a room share a few moves, and the
kit builds them in — use them rather than working around them:

- **Numbers arrive by counting up.** A value that spins from zero and lands reads as an event. Set
  `data-unit` and `data-prefix` so the count carries its own units.
- **The chart is the hero.** It fills the slide. A chart tucked under three bullets is decoration;
  a chart with six words above it is the lesson. Bars are set tall on purpose — don't shrink them.
- **One annotation, on the mark it explains.** A bar row takes a fourth field — its note — which
  prints under the bar with a small leader line: `Our system|12|var(--dv-b)|this is the one in our room`.
  One note per chart. Two is a paragraph.
- **End on the ratio, not the values.** `data-ratio="11 times more food in the same space"` lands a
  chip after the last bar. The comparison is the finding; the numbers are how you got there.
- **Reveal in the order of the argument.** Bars come one click at a time so the class can predict
  the next one. The order you write them in is the order the story is told.
- **Restraint everywhere else.** Hairline rules, no chart junk, one accent per chart, generous
  white space around it. The motion is the only thing moving.

## Slow reveal

A published graph read all at once is read by the strongest reader in the room. Read slowly, it is
read by everyone: draw it as an inline SVG in a `.figure`, give the data, the axis labels and the
title their own `data-step` numbers in that order, and let each → add one piece while the class says
what it notices and wonders. The title comes last, so students read the shape before they are told
what it shows.

## Making the class the data source

The strongest version of any of these is the one built from their measurements: the dot plot filled
in as pairs report, the tally during four corners, the slope chart of each tray after six weeks.
The reading load drops to nearly zero because they already know what the numbers mean — they made
them. When a lesson has any chance of generating its own data, build the chart around that instead
of a published figure, and put the published figure next to it afterward as the comparison.

## In the packet

A chart on screen and nothing on paper wastes it. Pair each one with a task that asks students to
read it, in this order of difficulty: *read a value* → *compare two values* → *say what it means* →
*predict the next one*. The stem goes on the task that asks for the sentence.
