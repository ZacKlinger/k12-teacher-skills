# The HTML decks: what they communicate, what they teach, and what they could do

*Revised Sep 26: the blank-screen key is gone. Students need something to look at and talk about,
so every talk slide now carries its visual, and photos open larger instead. The output criteria for
slides and worksheets are in `sdc-lesson-planning/references/design_criteria.md`.*

September 26, 2026

## What was read

Your lesson decks aren't in Drive or among your artifacts, so they likely live on your computer, and
only one full lesson deck was reachable: **Garden Field Guide** (Sep 8, published as an artifact), built on the skill's
template. Every skill-built deck starts from `assets/deck_template.html`, so the template was read as
the common ancestor of all of them. Your three game pages (Hydro Jeopardy, Readiness Jeopardy, Who in
the Room) show what you build when you design interaction yourself. To review more decks, drop the
`.html` files into `my-skills/decks/` or a Drive folder and point a session at them.

## What the decks already do well

Keep these; they are the reason the decks work.

- **Headlines are claims, not topics.** *"In our tank, we choose everything these roots touch"* says
  what the photograph proves. A student who reads only the headline still leaves with the idea.
- **The picture comes before the word.** Garden Field Guide shows roots with no soil, then the tank
  beside the garden, and only then names *limiting factor*. Concrete first, then the abstraction.
- **Predict, then reveal.** The chart kit won't show a bar until someone guesses. A prediction that
  turns out wrong is the moment the brain decides to remember.
- **One idea per slide, and room around it.** Most slides carry under fifteen words.
- **The packet chip on every writing slide.** *"Packet p. 1"* in the corner ends the "which page?"
  hunt, which costs a slow reader the first minute of every task.
- **The language line is short.** *"¿Quién controla el agua aquí?"* carries the task and nothing more.

## Where Garden Field Guide loses the student

1. **Template text reached the projector.** After the chart reveal, students saw the caption
   *"The bar is the finding. The words above it are its caption."* That sentence was the template's
   instruction to the builder, not a caption. The checker now catches it, and the template's example
   carries a real caption instead.
2. **The chart teaches a misconception.** *"Our tank: 4 things controlled. The garden: 0. Weather
   decides everything here."* But gardeners water, space, weed, and amend soil. In a lesson about
   limiting factors, a zero bar tells students outdoor growing is beyond anyone's control, which is
   the misconception the lesson should be taking apart. A four-against-zero comparison also doesn't
   need a chart. The stronger chart is the one the class makes at the garden: which limiting factor
   each pair found, dotted onto the live dot plot when they come back in.
3. **The same finding appears twice, once to nobody.** The 4-and-0 returns as big numbers on the
   "Head Back" slide, which is on screen while the class walks out the door.
4. **The Do Now asks the hardest question first.** *"What is one constraint that hydroponics removes
   compared to traditional soil agriculture?"* comes before the photograph and the word that would
   make it answerable, and it's twelve words with two abstractions for readers at a third-to-fifth
   grade level. A do-now should reach back to something students already hold (last week's frame),
   not forward to what the lesson hasn't taught yet.
5. **The longest headline sits on the emptiest slide.** The objective is a nineteen-word headline in
   the deck's largest type. On screen the "I can" works best at a dozen words; the full sentence
   lives on the packet.
6. **Talk is nearly absent.** One minute of *"Notice and wonder · with your partner"*, with no roles,
   no speaking stem, no turn structure, against more than twenty minutes of individual writing and
   walking. Under the old skill, movement was the non-negotiable and the walk satisfied it. Talk was
   incidental, and it shows.

## Principles worth designing to

For readers two to six years below grade level, the research on multimedia learning points the same
way your instincts already do.

- **Coherence:** every word on a slide earns its place; decoration and repeated findings cost
  attention a struggling reader doesn't have.
- **Signaling:** the headline says what to notice; the photograph's crop and pins point at it.
- **Segmenting:** one idea at a time, and within a slide, one piece at a time. Build steps
  (`data-step`) now do that.
- **Contiguity:** the question, the stem, and the packet page sit together on one screen, never across
  a click.
- **Redundancy, used carefully:** reading a slide aloud while students read it is redundant for a
  fluent reader but a lifeline for a newcomer. The read-aloud key makes that a choice, not a habit.
- **Retrieval and prediction:** every lesson opens by pulling something back and asks for a guess
  before every reveal.
- **UDL:** several ways in (photo, chart, voice, language line), several ways to respond (say it,
  write it, vote).

## What changes when talk replaces movement

A movement deck is traffic signs: where to stand, which corner, how long to walk. A talk deck is a
script for a conversation, and the slide becomes the facilitator so you can listen instead of run
the clock.

| | Movement-first deck | Talk-first deck |
|---|---|---|
| The talk slide carries | The question, maybe a stem | The question, each partner's job, a "Say it" stem, turns timed in phases, who reports |
| Stems | Writing frames ("Start here") | Speaking frames ("Say it"), short enough for one breath |
| The listener | Waits | Has a job: "Say it back: You said…" |
| Timing | One countdown for the block | Think, A talks, B talks, share; chimes at each switch, the speaker's card lights up |
| Who shares | Volunteers | A pair picked at random, after they've rehearsed |
| Checkpoints | One question, answered alone | Vote, talk, revote; the shift between bars is what the talk did |
| Student ideas | Said once, gone | Typed onto a "What we heard" board, credited to pairs, reused in the closing |
| Logistics slides | Walk there, head back, corner signs | Few; movement survives as talk that moves (four corners, defend) |
| Rhythm | Input, then activity | Every input (photo, clip, chart) followed by a two-to-three-minute turn |

Garden Field Guide, talk-first: after the photo comparison, a turn-and-talk ("Which would you rather
be, a plant in our tank or in the garden? Why?"). At the garden, partners split the field notes: one
observes, one records, switch at the chime. Back inside: a vote on which limiting factor was
strongest, a talk, a revote, the pair picker for two reporters, their ideas on the board, and a
closing CER that cites one of them.

## Using what only HTML can do

**Built into the template now:**

| Feature | What it does in the room |
|---|---|
| Phased talk timer (`data-phases`) | One press runs think, A, B, share; chimes at each switch; lights up whose turn it is |
| Vote, talk, revote (`.vote`) | Count hands before and after talk; both bars on screen |
| Pair picker (`.picker`, key P) | Calls a numbered pair at random, no repeats; no names in the file |
| What we heard (`.heard`) | A board you type student ideas into; kept through a reload on that computer |
| Build steps (`data-step`) | → reveals the next piece before the next slide: answers after predictions, worked-example lines one at a time |
| Read aloud (key A) | Reads the headline, then each language line in its own voice, then the direction |
| Look closer (click a photo) | Opens it at wall size with the slide's question under it; the screen is never blanked |
| Talk layout (`.talk`) | The visual students discuss on the left, the turns and the starter on the right |

**Already there:** per-slide timers, six predict-then-reveal chart types, a live dot plot for class
data, click-to-play video with a fallback, photo fallback cards, a jump menu.

**One design constraint worth keeping:** the syllabus bans phones in class, so every interaction runs
from your one computer: big targets, keyboard keys, nothing that needs a student device.

**Next, not built yet:**
- *Math manipulatives in SVG*: a draggable number line, an area model you can resize, a scale that
  tips. HTML can show a relationship changing as you drag, which no printed page can.
- *Faded worked examples*: the build steps make these possible now. The math reference could require
  one: a full example, a half-filled one, then the students' turn.
- *Carrying the board forward*: export "What we heard" as a line for the profile's Day map, so the next
  do-now can quote a pair's idea from yesterday.
- *A phone view for outdoor blocks*: the field notes slide was on a wall nobody could see from the
  garden.

The checker now errors on a deck with no talk slide, on talk phases that don't add up to the slide's
timer, and on the leaked template caption.
