# Interactive formats: what the wall can do that paper can't

A slide shown to a room is a page that one person turns. Everything in this file exists because
an HTML deck is not that: it can wait for a guess, take one from every student at once, let a
student walk up and move the idea with their hands, hold the answer back until the room has
committed, and explain itself the moment it is revealed. Those are the moves that teach, and they
are the moves a paper packet and a slideshow cannot make.

Read this with `deck.md` whenever a lesson has a moment where students should do something with
an idea rather than look at it, which is most moments. The game round and the sort are in
`deck.md`; the formats below sit beside them and share their routine.

**Contents**
1. [Why these, in any classroom](#1-why-these-in-any-classroom)
2. [Choosing the format](#2-choosing-the-format)
3. [The routine every format shares](#3-the-routine-every-format-shares)
4. [The formats](#4-the-formats)
5. [Patterns built from parts the deck already has](#5-patterns-built-from-parts-the-deck-already-has)
6. [Before you call it done](#6-before-you-call-it-done)
7. [Sources](#7-sources)

---

## 1. Why these, in any classroom

Each format carries one move that the research behind it found worth making. Each was chosen to
work for every student in the room, and above all for the students who read below grade level,
who lose the thread when working memory fills, who are new to English, or who stop raising their
hands after the first wrong answer in front of everyone. What the class profile says about the
room (reading levels, supports, home languages) still shapes the cards, the claims and the pace.

| The move | Why it works | Formats that make it |
|---|---|---|
| **Every student answers at once** | Active student responding: when every student responds on every question (response cards, a held-up letter), correct answers and time on task rise and disruption falls, including for students with disabilities. One hand up at a time means one student learns. | hinge question, true or false, game round |
| **The guess comes before the answer** | Predict, observe, explain: committing to a prediction makes the gap between intuition and result visible. Errors held with confidence are corrected *best* once the answer arrives, because the surprise buys attention. | estimate, what if, zoom-in, every reveal |
| **Hands move the idea** | Ordering mixed-up steps (Parsons problems) carries less cognitive load than producing them, and transfers. Placing numbers on a line builds the magnitude sense that later arithmetic stands on. Movement is also a regulation break for students who need one. | order it, number line, sort, match |
| **A wrong answer is something to study** | Studying an erroneous worked example beats solving the same problem cold, once the error is pointed at and explained. A mistake that belongs to "someone" is safe to pick apart. | find the mistake, hinge question |
| **Every answer can be right** | Which-one-doesn't-belong sets have a defensible reason for every tile, so the talk is about reasons, not about being right. The student who never volunteers can be right on the first try. | which one doesn't belong |
| **Push on a model** | An explorable explanation lets a student ask "what if?" and see the effect, instead of taking a sentence on faith. Cause and effect, felt in the hand. | what if |
| **Look before you name** | See, think, wonder: observation before vocabulary. A photo revealed a step at a time, or a graph revealed a piece at a time, keeps a whole room looking at the same detail. | zoom-in, label the photo, slow reveal (pattern) |
| **Low-stakes retrieval** | Short in-class retrieval helps students with lower working memory most, but only when it feels low-stakes: a test feeling erases the gain. So: no names, no points unless the teacher asks, the reveal explains, and a wrong answer is a turn in a game. | true or false, match, label the photo |

The one thing these formats must not become is a quiz projected on a wall. What separates a game
from a quiz here is that partners agree before anyone answers, everyone answers at once, and the
reveal teaches.

---

## 2. Choosing the format

Ask what students should do with the idea, and pick by the verb. Never pick by wanting variety: a
format that doesn't fit the idea teaches students to distrust the game.

| Students should... | Format | Class |
|---|---|---|
| Reason toward an answer they couldn't already know | Game round | `.game` (deck.md) |
| Show you, after teaching, whether they have it | **Hinge question** | `.hinge` |
| Recall several small facts fast | **True or false** | `.tf` |
| Put things into groups | Sort it | `.sort` (deck.md) |
| Put steps or events in order | **Order it** | `.order` |
| Place a quantity where it lives | **Number line** | `.line` |
| Estimate one quantity | **Estimate** | `.estimate` |
| Connect words to meanings or to the real thing | **Match** | `.match` |
| Argue for a choice with no single answer | **Which one doesn't belong** | `.wodb` |
| Find and fix an error | **Find the mistake** | `.mistake` |
| See what a change does to a result | **What if** | `.whatif` |
| Look closely before naming | **Zoom-in** | `.zoomin` |
| Recall the names of parts | **Label the photo** | `.pinned` with `data-quiz` |

Two to four of these in a period is plenty, usually one per phase of the lesson: an estimate or a
zoom-in to open, a sort or an order in the middle, a hinge question before independent work, a
true-or-false or a match to close. Each one is a slide, and each slide carries one of them: `V` and
`C` act on the first game on a slide, and two games on one slide is two ideas on one slide.

---

## 3. The routine every format shares

Every format is configured by `data-` attributes or plain child markup, built by the template when
the deck opens, and run by the same keys and the same routine. Nothing in the template is edited
per lesson.

**Talk first.** Put `data-timer` on the slide (60-120 seconds is usual) and an eyebrow that says
how students answer: *"Check · everyone shows a letter"*, *"Game · come up and put them in
order"*, *"True or false · show your card"*. Partners agree on the timer before anyone answers,
which is why a game slide with a timer counts as one of the lesson's talk moves.

**Everyone answers.** The format says what students hold up or do: a letter (A-D cards or
fingers), a True/False card, a pair walking to the board. Whiteboards work for estimates. The
plan names what students need on their desks.

**The reveal explains.** Every format carries a reason (`data-why`, or one per tile or claim; a
what-if's is its `data-caption`): one sentence a student could repeat to a partner, six words or
more for a game's, four or more for a tile's, five or more for a claim's. Marking an answer right
is not a reveal.

**Nothing jumps.** Reasons, fixes and answers reserve their space from the start, so the slide is
still when the answer lands. A student who reads slowly does not lose their place on the screen.

**Build steps and games.** On a slide with build steps, → brings every step in first (a "Talk
first" prompt, a "Say it" stem, a game held back until its question has been asked), and only then
reveals the game. A game inside a step waits for it, and `V` and `C` wait for it too: a game never
answers while it is still hidden.

**Fractions.** Any number you write in a game's attributes may be a fraction: `3/4` on a number
line's cards and ticks, an estimate's answer or range, a what-if slider's range, step and start, its
band. The deck and the checker read it the same way.

**Keys.** `V` reveals what was guessed (game round, hinge question, estimate, which one doesn't
belong, find the mistake, true or false, what if, label the photo). `C` checks what was arranged
(sort, order it, number line, match). Each format also has its own buttons for the mouse.

**A clicker runs the reveals.** A presentation clicker sends only → and ←. On a slide whose game
has something to reveal, → takes it forward before the deck moves on: it reveals the answer, steps
a zoom-in back, brings back the next label, moves to the next true-or-false claim. So the teacher can run
the game from the back of the room, and the answer never arrives before the prediction. Games
students arrange with their hands (sort, order it, number line, match) are checked with `C` or
their Check button, never by →: checking a half-built arrangement would only mark it wrong. Coming back to a staged
format with ← shows it finished; arriving with → starts it from the top; and ← on a staged format
steps it back one stage (the answer hidden again, the claim or the zoom before) before the deck goes
back a slide, so one press too many is undone with one press. Games with a single
reveal (game round, hinge question, estimate, which one doesn't belong, find the mistake, what if)
keep their state between visits, so a revealed answer stays revealed and points are never taken
back by navigating.

**At the board.** Anything that drags can also be tapped: tap a card, then tap where it goes. That
is how it works on a touch screen, from the laptop, and for a student whose fine-motor supports
make dragging hard. Targets are large on purpose.

**No teams, no points, no names.** Exactly as in `deck.md`: teams only when the teacher asks
(`--teams`), scored by hand with the footer's `+` on these formats, and never a student's name in
the file. A hinge question is never scored at all: it is the class telling the teacher what to
teach next.

**Language lines.** When the class has home languages, the headline is the question and carries
its line in each, as on every slide (`deck.md`, "Language access"). Card text, options and tiles
stay in the language of instruction and short. A true-or-false claim is a question on its own, so
each claim carries its own lines (below). With no home languages there are no lines. The examples
in this file carry Spanish lines.

---

## 4. The formats

### Hinge question

The check the teacher asks before moving on: one multiple-choice question where every wrong option is a
wrong idea students are known to hold, so the letters in the air say not only *how many* have it
but *what* the rest are thinking. Ask one at each point where the lesson hinges, typically before
independent work.

```html
<section class="slide" data-day="Wed 10/1" data-title="Check" data-timer="60" data-mins="3 min">
  <header class="head"><div class="eyebrow">Check · everyone shows a letter</div></header>
  <h2>A pump moves 2 litres a minute. How long to fill a 30-litre tank?</h2>
  <p class="es">La bomba mueve 2 litros por minuto. ¿Cuánto tarda en llenar 30 litros?</p>
  <div class="body">
    <div class="hinge" data-options="15 minutes|60 minutes|32 minutes|28 minutes" data-answer="1"
         data-traps="-|Multiplied 30 by 2 instead of dividing.|Added the 2 to the 30.|Took the 2 away from the 30."
         data-why="Each minute adds 2 litres, so 30 litres takes 30 ÷ 2 = 15 minutes."></div>
  </div>
</section>
```

- `data-options` two to six (A to F); `data-answer` counts from 1; `data-traps` has one entry per option,
  `-` for the right one. A trap names the thinking, kindly: *"Added the 2 to the 30."*
- **In class:** everyone holds up a letter at once. The teacher clicks an option card once per hand showing
  it (shift-click takes one away), then `V`. The wrong options show their traps, the right one
  goes green, and the tally line reads *"8 of 9 chose A · move on"* or *"4 of 9 chose A · reteach
  what B was thinking"*. `data-move-on` sets the share that counts as "move on" (default 80).
- **A good one** is answerable in under a minute, has one clearly right answer to someone who has
  it, and has distractors drawn from real errors (the packet's answer key and last year's papers
  are the source), never from random wrong numbers.

### True or false, quick-fire

Several short claims, one at a time, each answered by every student with a card. It is the
fastest retrieval the deck has: five claims in three minutes, every student answering every one.

```html
<div class="tf" data-labels="True|False">
  <div data-answer="False" data-why="Roots need water, air and nutrients. Soil only holds those.">Plants need soil to grow.
    <p class="es">Las plantas necesitan tierra.</p></div>
  <div data-answer="False" data-why="Water keeps the motor cool. Out of water, a pump burns out.">A pump can run without water around it.
    <p class="es">La bomba funciona sin agua.</p></div>
  <div data-answer="True" data-why="Lettuce needs the right light for enough hours. A lamp can give both.">A grow light can stand in for the sun.
    <p class="es">Una lámpara puede reemplazar el sol.</p></div>
</div>
```

- Each child is a claim: `data-answer` is one of `data-labels` (default `True|False`; `Fact|Myth`,
  `Agree|Disagree` and three labels such as `Pump|Light|Timer` all work), `data-why` explains.
  When the class has home languages, each claim carries its own line in each (`<p class="es">`,
  tagged with `lang` as in `deck.md`), and `A` reads the claim on screen with its lines.
- Two to eight claims, each under about sixteen words. The claims sit in one box sized to the
  longest, so nothing moves from claim to claim.
- **In class:** students hold up a card; → reveals; → again goes to the next claim. Asking *"how
  sure are you, one finger or three?"* before the reveal is worth the seconds: a confident wrong
  answer is the one most likely to be corrected for good.
- Phrase a claim as something a person says (*"Someone says: plants need soil"*) and set the labels
  to `Agree|Disagree`, and it becomes an argument about an idea rather than a test of a fact.

### Order it

The steps of a procedure, the links of a cause-and-effect chain, or events in time, shuffled;
students put them in order at the board. The build steps of a lab are the classic use: the order is
the understanding.

```html
<div class="order" data-ends="First|Last"
     data-why="The pump goes in the water before it gets power: a pump that runs dry burns out.">
  <div>Fill the reservoir with water</div>
  <div>Drop the pump into the water</div>
  <div>Push the tubing onto the pump</div>
  <div>Run the tubing up to the channel</div>
  <div>Plug in the pump</div>
</div>
```

- Write the children **in the right order**; the deck shuffles them so no card starts in its own
  place where it can help it. Three to six cards (the checker errors past eight), each a phrase. A
  card can be a photograph (a `<figure>` with `--focus`, its `<img>` and a one-word
  `<figcaption>`), shown as a thumbnail: the stages of a plant's life, the build in pictures.
- `data-ends` labels the top and bottom (`First|Last`, `Earliest|Latest`, `Cause|Effect`).
- **In class:** drag a card up or down, or tap one card and then another to swap them. `C` checks:
  cards in place go green with a ✓, the rest peach with a ✗, and the count appears. **Show the
  order** puts them right; **Start over** shuffles again.

### Number line

Cards students place where their values live: fractions, decimals and percents on 0 to 1,
measurements on a ruler's range, temperatures, pH. Where a number sits on a line is what it means;
this is the clothesline routine, on the wall.

```html
<div class="line" data-min="0" data-max="1" data-ticks="0|0.5|1"
     data-items="½=0.5|0.3=0.3|¾=0.75|90%=0.9|1/10=0.1"
     data-why="Half and 0.5 are the same spot. 90% is almost all the way to 1."></div>
```

- `data-items` reads `label=value`, three to eight cards, every value inside `data-min` to
  `data-max`; a value may be a fraction (`three quarters=3/4`). `data-ticks` sets the labelled
  ticks, value first (`value` or `value=label`: `1/4`, `0.5=½`), the reverse of the cards; leave it
  out for round-numbered ticks about a fifth of the range apart. `data-tolerance` is how close counts as right, in the line's
  own units (default 4% of the range).
- Fewer ticks is harder and better: `0|1` makes students reason about half; `0|0.25|0.5|0.75|1`
  does the reasoning for them.
- **In class:** drag a card onto the line, or tap a card and then the line. Cards close together
  stack in lanes, so two near values never hide each other. `C` checks: right cards go green, and a
  dashed copy of every wrong or unplaced card appears where it really lives.

### Estimate

One quantity the class estimates as a range before the real number lands: the seeds in a packet,
the litres in a tank, the minutes to fill it. Students set a *too low* (an answer nobody can get
wrong, which is how every student gets in), a *too high*, and a *just right*.

```html
<div class="talk">
  <figure class="talk-visual" style="--focus:50% 50%">
    <img src="…?width=1200" alt="An open paper packet of lettuce seeds spilled on a white table, with a ruler beside it.">
    <figcaption class="cap">Each seed is about the size of a grain of rice.
      <span class="cred">Wikimedia Commons · CC BY-SA 4.0</span></figcaption>
  </figure>
  <div class="talk-side">
    <div class="estimate" data-min="0" data-max="800" data-answer="263" data-unit=" seeds"
         data-why="We counted 263: about 26 rows of 10, and 3 left over."></div>
  </div>
</div>
```

- `data-answer` must be a real, counted or sourced number inside the range, and off its middle:
  the markers wait near each end and at the middle of the line, reading "?" until the class
  sets them, so a range centred on the answer parks *just right* on it (the checker warns).
  `data-unit` in words students own. `data-labels` renames the three markers; `data-snap` sets the step the markers move
  in (default about a hundredth of the range).
- Put the photograph of the thing being estimated beside it in the `.talk` layout, as above: an
  estimate of something nobody can see is a guess about a word.
- **In class:** partners agree, then a pair drags the three markers (or taps the line: the nearest
  marker jumps there); a marker shows its number once it is set. → reveals: the real number counts up to its place, and a line says whether it
  fell inside the range and how far *just right* was.

### Match

Words on the left, what they mean on the right, in a shuffled order; students draw a line from each
word to its meaning. Vocabulary is the obvious use; a word to its photograph is often the best one,
and an equation to its graph or a unit to a quantity work the same way.

```html
<div class="match" data-why="Each part has one job. Together they keep water moving past the roots.">
  <div><span>Reservoir</span><span>Holds the water</span></div>
  <div><span>Pump</span><span>Pushes the water up</span></div>
  <div><span>Net pot</span><span>Holds the plant above the water</span></div>
  <div><span>Timer</span><span>Turns the pump on and off</span></div>
</div>
```

- Each child is a pair of exactly two elements, left then right; three to six pairs. The right
  column is shuffled.
- **A photo on the right** is a `<figure>` with its `<img>` (with `--focus`) and a `<figcaption>`.
  The caption stays hidden until `C`, so it can name the thing without giving the match away, and
  it still satisfies the caption rule in `photographs.md`. The slide carries one credit line.
- **In class:** drag from a card to its partner, or tap one and then the other. Tapping a joined
  card frees it. `C` checks: right lines turn green, wrong ones dashed peach, and the count appears.

### Which one doesn't belong

Four tiles, and every one of them can be the odd one out for a reason. Students pick one and say
why, and since every answer can be right, the talk is about reasons: the routine for a room where
being wrong in front of others is the thing that stops a student talking.

```html
<div class="wodb">
  <div data-why="The only fraction with a 4 on the bottom.">¾</div>
  <div data-why="The only one written as a decimal.">0.75</div>
  <div data-why="The only one with a percent sign.">75%</div>
  <div data-why="The only one that is not the same amount as the others: it is 0.7.">7/10</div>
</div>
```

- Exactly four children, each with its own `data-why`. A tile is a number, a short word or
  expression, an inline SVG, or a photograph as a `<figure>` with `--focus` and a short
  `<figcaption>` label (one credit line for the slide). A bare `<img>` tile is wrapped for you, but
  a `<figure>` is what carries a label.
- **Design it so every tile has a reason.** Build the set from one property per tile: the only
  fraction, the only decimal, the only percent, the only one of a different value. If one tile has
  no honest reason, it is a quiz with one answer, and the checker errors.
- **In class:** think time, then talk (`data-phases="Think|60; Talk|120"` suits it). Click a tile to
  show one reason for it after a pair has argued for it; → or `V` shows all four.

### Find the mistake

Someone's worked solution, with one step gone wrong. Students point to the step, and the reveal
names it and fixes it. The work belongs to *someone*, never to a student in the room and never to a
name.

```html
<div class="mistake" data-why="To undo + 5 you take 5 away from both sides. Adding 5 made the problem bigger instead of undoing it.">
  <div>3x + 5 = 20</div>
  <div data-wrong data-fix="3x = 15">3x = 25</div>
  <div>x = 25 ÷ 3</div>
  <div>x = 8.3</div>
</div>
```

- Three to seven steps as children, in order; exactly one carries `data-wrong` and `data-fix`
  (what that step should have said). Every step after it inherits the error and is marked so.
  `data-label` replaces the default prompt above the steps.
- Use the error students actually make. The packet's predicted errors are the source; a made-up
  slip teaches nothing about the real one.
- **In class:** students hold up the step number; the teacher clicks the step the class picked (it is
  marked *we think*). `V` shows the wrong step, its fix under the steps, and whether the class found it.

### What if

A small model the class can push on: one to three sliders feed a formula, and the result shows as
a number and a bar against a target band. With *predict first* on (the default), the result goes
back under cover every time a slider moves, so each change is a prediction before it is a fact.

```html
<div class="whatif" data-inputs="Plants|1|24|1|12; Litres each plant drinks a day|0.1|0.5|0.05|0.25"
     data-formula="a * b * 7" data-output="Litres a week" data-unit=" L"
     data-band="0|40" data-band-label="fits in our tank"
     data-caption="Double the plants and the week's water doubles too."></div>
```

- `data-inputs`: one row per slider, `Label|min|max|step|start`, separated by `;`. One slider that
  matters teaches more than three that might.
- `data-formula` uses `a`, `b`, `c` for the sliders in order, numbers (`1e3` too), `+ - * / % ^ ( )`,
  and `round` (`round(x, 1)` keeps one decimal), `floor`, `ceil`, `min`, `max`, `abs`, `sqrt`, `pow`,
  `PI`. Write every `*` (`2*a`, not `2a`); `-a^2` means `-(a^2)`; no comments or other symbols. The deck parses the formula itself
  rather than running it as code, with the same rules the checker uses, and the checker works it
  out across each slider's whole range: it errors if the result goes below zero (bars start at
  zero), stops being a number (a division by zero) or the formula won't parse, and warns on a slider
  the formula never uses.
- `data-output` names the result in words students own; `data-band` and `data-band-label` draw the
  target (the shape of every engineering verdict, as in the gauge); `data-max` fixes the bar's end
  (otherwise it is fitted to the largest result anywhere in the sliders' ranges, so a formula that
  peaks in the middle, like a pen's area for a fixed fence, still reads); `data-decimals` fixes the rounding;
  `data-predict="off"` makes it live from the start.
- The numbers must be real: the formula is the lesson's own relationship, checked against the
  packet's answer key at the slider's starting values.
- **In class:** *"What happens to the week's water if we double the plants?"* Partners predict, a
  student moves the slider, `V` or → reveals. The status says *inside*, *above* or *below the band*
  in words, not by colour alone. It counts as one of the deck's interactive charts.

### Zoom-in

A photograph that opens close on one detail and steps back, → by →, to the whole. At each step the
room says what it sees and what it might be. It is the strongest opening a deck has: students look
at the thing before anyone names it.

```html
<div class="body media">
  <figure class="zoomin" style="--focus:30% 35%" data-zooms="6|3|1">
    <img src="…?width=1400" alt="White lettuce roots hang from a black net pot into clear water.">
    <figcaption class="cap">Roots, not soil: every one of them is drinking.
      <span class="cred">Wikimedia Commons · CC BY-SA 4.0</span></figcaption>
  </figure>
</div>
```

- `--focus` is required and is the detail students see first; read it off the contact sheet's grid
  exactly as for a crop (`photographs.md` §7). `data-zooms` steps down to 1 (default `5|2.5|1`).
- The caption appears only at the whole photo. Clicking the photo steps back too; the full-size
  view opens only once the zoom is over.
- Choose a photo whose detail is genuinely ambiguous up close and obvious far away: roots that look
  like hair, a leaf's veins, a pump's impeller. The photo still needs its brief, its frame test and
  its credit; it counts toward the deck's photographs.

### Label the photo

The labelled photograph from `photographs.md` §9, with the names held back: the numbered pins
show, and each name comes back on → (or a click on its pin), in number order. *"What is part 1?
Tell your partner."* Then →.

```html
<div class="body media">
  <div class="pinned" data-quiz>
    <img src="…?width=1400" alt="A hydroponic tray under grow lights with a pump and tubing visible.">
    <div class="pin" style="--x:22%;--y:30%"><div class="n">1</div><div class="lab">Grow light</div></div>
    <div class="pin" style="--x:60%;--y:66%"><div class="n">2</div><div class="lab">Water channel</div></div>
  </div>
  <p class="cap">Follow the water from 2 back to the tank. <span class="cred">Wikimedia Commons · CC BY 2.0</span></p>
</div>
```

- Add `data-quiz` to any `.pinned`. Two or more pins. `V` shows or hides every name at once.
- Use it the lesson after the parts were taught, not the first time: it is retrieval, and retrieval
  needs something to retrieve.

---

## 5. Patterns built from parts the deck already has

Some strong routines need no new format. Build them from what `deck.md` and `dataviz.md` already
carry.

- **Slow reveal graph.** Draw the chart as an inline SVG in a `.figure` and give its parts
  `data-step` numbers: the data first, then the axis labels, the title last. Each → reveals a piece,
  and the class says what it notices and wonders at each one. The title last is the point: students
  read the shape before they are told what it means.
- **Faded worked example.** A `.flow.stack` of the solution's steps with the last one or two held
  back by `data-step` and a `.blank` in their place on the packet: students do the faded step, then →
  shows it. Fade from the end first; next time, fade one more.
- **Notice and wonder.** A `.pgrid` of two photographs and a `.heard` board beside them; pairs report,
  the teacher types, credited to pair numbers.
- **Would you rather.** Two options with photographs and numbers in a `.pgrid`, then a `.vote` with
  two options: vote, talk with the numbers, vote again.
- **Brain dump.** A `.heard` board with a two-minute timer at the start of a lesson: everything the
  room remembers from last time, typed as it is said. Cheapest retrieval there is.

---

## 6. Before you call it done

`check_deck.py` checks each format's configuration: option and answer counts, traps, `label=value`
cards inside the range, exactly one wrong step with its fix, four tiles each with a reason, claims
whose answers are among their labels and which carry their language lines, pairs of two, a
what-if formula that runs and stays at or above zero, a zoom-in with its `--focus`, a reason on
every game that has an answer, a timer on every game but the what-if, zoom-in and label the photo,
one game per slide, and no more game slides than the period has room for. Get it clean. Then the questions only a
person can answer:

- *Is every answer in a game the same as the packet's answer key?* The hinge answer, the true-or-false
  answers, the order, the values on the line, the estimate, the what-if at its starting values.
- *Is every wrong option, trap and mistake a real student error?* Not a random wrong number.
- *Would a student who reads slowly be able to read every card from the back row in the time
  given?* A phrase per card; a claim under sixteen words.
- *Does every which-one-doesn't-belong tile have an honest reason?*
- *Does the eyebrow say how students answer?* A letter, a card, a pair at the board.
- *Click through it once with → alone*, the way a clicker would: every game with an answer reveals
  it before the deck moves on, the arranged games move on unchecked (they are `C`'s), and nothing is
  revealed before its prediction.

---

## 7. Sources

- Heward, W. L., et al. (1996). *Everyone participates in this class: Using response cards to increase
  active student response.* Teaching Exceptional Children.
  [ResearchGate](https://www.researchgate.net/publication/303637095_Everyone_Participates_in_This_Class_Using_Response_Cards_to_Increase_Active_Student_Response);
  Horn, C. (2010). *Response cards: An effective intervention for students with disabilities.*
  [SAGE](https://journals.sagepub.com/doi/abs/10.1177/215416471004500110)
- Wiliam, D., on hinge questions: [Designing great hinge questions, ASCD](https://www.ascd.org/el/articles/designing-great-hinge-questions)
- White, R. & Gunstone, R. (1992), predict-observe-explain:
  [science-education-research.com](https://science-education-research.com/teaching-science/constructivist-pedagogy/predict-observe-explain/)
- Butterfield, B. & Metcalfe, J., the hypercorrection effect:
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3079415/); in a classroom:
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/29781391/)
- Ericson, B., et al. (2017). *Solving Parsons problems versus fixing and writing code.*
  [ACM](https://dx.doi.org/10.1145/3141880.3141895)
- Siegler, R. & Ramani, G. (2008). *Playing linear numerical board games promotes low-income children's
  numerical development.* [Developmental Science](https://onlinelibrary.wiley.com/doi/10.1111/j.1467-7687.2008.00714.x);
  Shore, C., [Clothesline Math](https://clotheslinemath.com/)
- Stadel, A., Estimation 180 and the too-low / too-high routine:
  [Mount Holyoke](https://www.mtholyoke.edu/news/news-stories/how-number-talk-estimation-180)
- Danielson, C., *Which One Doesn't Belong?*:
  [Meaningful Math Moments](https://www.meaningfulmathmoments.com/which-one-doesnt-belong-wodb.html)
- Learning from erroneous examples, a systematic review:
  [Educational Psychology Review (2025)](https://link.springer.com/article/10.1007/s10648-025-10071-x);
  Alcala, L., My Favorite No: [Edutopia](https://www.edutopia.org/article/using-error-analysis-boost-engagement-student-talk-math/)
- Renkl, A. & Atkinson, R. (2004). *How fading worked solution steps works.*
  [Instructional Science](https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6)
- Explorable explanations: [overview](https://en.wikipedia.org/wiki/Explorable_explanation);
  Case, N., [Explorable Explanations](https://blog.ncase.me/explorable-explanations/)
- Project Zero, [See, Think, Wonder](https://pz.harvard.edu/resources/see-think-wonder); Laib, J.,
  [Slow Reveal Graphs](https://slowrevealgraphs.com/)
- Naylor, S. & Keogh, B., concept cartoons:
  [science-education-research.com](https://science-education-research.com/teaching-science/concept-cartoons/)
- Retrieval practice and special educational needs:
  [Chartered College of Teaching](https://my.chartered.college/impact_article/how-do-children-with-special-educational-needs-experience-retrieval-practice-2/);
  Roediger, H., Agarwal, P., et al. (2011). *Test-enhanced learning in the classroom.*
  [PDF](https://pdf.retrievalpractice.org/guide/Roediger_Agarwal_etal_2011_JEPA.pdf)
- Mayer, R., segmenting and signalling:
  [Cambridge Handbook of Multimedia Learning](https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/DD24C2F48B9B1277CE59F78276110258)
