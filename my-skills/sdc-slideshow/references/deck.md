# The slide deck

Write only the slides, the `<section class="slide">` elements, into `slides.html`, and build with
`scripts/build_deck.py`, which puts them inside `assets/deck_template.html` and runs the checker.
The chrome (navigation, countdown, day tag, packet chip, progress bar, jump menu, photo zoom)
already works. Don't open the template's stylesheet or scripts, don't rewrite them, and don't
position anything by hand. `references/slide_criteria.md` sets the type sizes and contrast the
template is built to.

The deck does two jobs at once. It's what Zac teaches from, and it's what a student looks up at
when they've lost the thread of the packet.

---

## The skeleton every slide uses

```html
<section class="slide" data-day="Day 2" data-title="Do Now"
         data-packet="p. 1" data-timer="300" data-mins="5 min">
  <header class="head"><div class="eyebrow">Do Now · silent · on your own</div></header>
  <h2>The headline, six to twelve words.</h2>
  <div class="body"> …cards, a flow, a chart, stems, vocabulary, video… </div>
</section>
```

Three parts, in this order, on every slide:

1. **Head** — `.eyebrow` on the left says where we are in the period. The right side fills itself:
   the live countdown when the slide has `data-timer`, otherwise the plain `data-mins`. The packet
   chip is injected from `data-packet`. **Never place the time or the packet chip by hand** — hand
   placement is what used to collide with the eyebrow.
2. **Headline** (`h1`/`h2`) — the serif, regular weight, sentence case, six to twelve words. It
   states the point, not the topic: "Same lettuce, one twelfth of the water," not "Water usage."
3. **Body** (`.body`) — where the content actually lives, and it fills the middle band. **Cards and
   flows are the default**: parallel things go in cards, anything with a sequence or a cause goes in
   a flow, numbers go in a chart. Reach for a container before reaching for another sentence.

**Nothing goes under the body.** No summary line, no closing thought, no "here's why that
matters." If the cards, the flow, or the chart didn't land the point, another sentence won't fix
it — rebuild the body. A line of commentary at the bottom of every slide reads as filler, and after
three slides students stop looking at that part of the screen.

The two exceptions are `.es` and `.instruct`. `.es` is the Spanish line (below); `.instruct` is a
plain direction students can't get from the body itself —
*"One person per corner says why"*, *"Hand it to me at the door"*, *"Words you can use: water,
nutrients, soil."* A direction, never a conclusion. Most slides don't need one.

`.stand` — a quiet sans line under the headline — exists for the rare case where the body needs
setup it can't carry, like the source of a number. Use it sparingly and never alongside an
instruction.

**A headline alone is not a slide, and neither is a headline over a paragraph.** A student looking
at any single slide should learn something without hearing you say a word — and the way they learn
it is by looking at structure: three cards, four steps with arrows between them, two bars, a word
next to its non-example. The dark checkpoint is the one exception, one question meant to hang in
the air, and a lesson gets two of those at most.

The test for junk: if a line could be deleted and nothing on the slide would be harder to
understand, delete it. Labels that repeat a heading, a caption restating the chart it
sits under, a sentence summarizing the cards above it — all junk. Structure, not prose, carries a
slide.
---

## Spare is not the same as thin

Everything above this line tells you what to take away, and a deck built from subtraction alone
converges on sixteen slides of headline-over-nothing. Two of the three decks this skill has built
shipped with zero photographs; one had no charts either. Nothing in the rules was violated. That is
the failure this section exists to prevent.

**Spare** is a visual property: white ground, hairline rules, one pastel, no furniture. Keep it.
**Thin** is a content property: a student looks at the slide and there is nothing there to think
about. The house style is spare *so that* what remains can be dense — restraint is what buys the
attention, and then something has to be worth spending it on.

So every body owes the room a payload. Before a slide is done, name what a student gets from
looking at it for ten seconds without hearing your voice. If the honest answer is "the topic," it
isn't finished. The payload is one of:

- **A real number**, with its unit and its comparison. Not "uses less water" — *250 L versus 20 L*.
- **A photograph of the actual thing**, carrying a claim (`references/photographs.md`).
- **A structure with parts**: three cards that differ, four steps with arrows, two sides compared.
  Parallel boxes that all say roughly the same thing are one card wearing three hats.
- **A named specific**: this farm, this town, this plant, this year. Named things are rememberable
  in a way that categories are not.
- **A question with a hard edge** — one where a student could be wrong, and the wrongness would show.

### The test every slide has to pass

Two mindsets from the design method behind these lessons do their work here, on each slide, and
they are the fastest way to tell a finished slide from an unfinished one.

**Show, don't tell.** The strongest version of any slide is the one where the evidence is on screen
and the sentence is unnecessary. Before writing a sentence, ask what could be shown instead — the
photograph, the two bars, the four steps. A sentence explaining a chart usually means the chart is
doing too little, not that the sentence is needed. Applied as a test: *cover the prose on this
slide. Does it still teach?* If yes, cut the prose. If nothing is left, the body was never there.

**Beginner's mind.** You know what a greenhouse looks like; the student does not. Every place the
slide assumes a picture the student doesn't have is a place a photograph goes. This assumption is
invisible from inside expertise — which is why it is a rule in `references/photographs.md` rather
than a judgement call.

**Focus on human values.** In this room that means the person in the photograph, the town the
number comes from, the worker whose job the machine changed. Abstractions are where students who
read slowly lose the thread; a person doing something is where they find it again.

---

## Language access

**Every slide that asks a question or gives a direction carries a Spanish line.** It goes directly
under the thing it supports — under the headline when the headline is the question, under the
`.instruct` when the direction is the instruction:

```html
<h2>How many football fields is that?</h2>
<p class="es">¿Cuántas canchas de fútbol americano son?</p>
…
<p class="instruct">Work with your partner. One paper between two.</p>
<p class="es">Trabajen en pareja. Una hoja para dos.</p>
```

A new word gets its Spanish inside the word cell, where the word is:

```html
<div class="vc word"><div class="k">Word</div><div class="w">Yield</div>
  <div class="say">say it: YEELD</div>
  <div class="es">rendimiento</div></div>
```

The line carries **the task, and nothing else**. Headlines that state a finding, card bodies,
captions, chart labels, stats, the standfirst — all stay English. A translated slide is two slides
of text where there was one, and text is the channel this room cannot use; a four-word Spanish line
under the question is what actually gets a newcomer into the work.

**Shorter than the English, always.** The checker warns when a Spanish line runs more than about a
fifth longer than the line above it, which is nearly always the framing having been translated
along with the task.

**It matches the packet, word for word.** The Spanish on a slide is the same Spanish that is on that
question in the packet. The whole deck-and-packet parity rule applies here too — a student looking
up from the page has to see the sentence they were just reading.

Plain everyday Spanish, `tú`-form imperatives. `check_deck.py` errors on a deck with no Spanish at
all, and warns on any slide that asks a question or sends students to the packet without it — that
warning is a judgement call when the slide only names a page number.

---


**A second home language** sits right under the Spanish, same class, marked with its code:
`<p class="es" lang="zh">写下你的答案。</p>`. Add `dir="rtl"` for Arabic, Farsi, Urdu, or Hebrew and
the rule flips to the right side. Run the checker with the room's languages,
`--languages es,zh`, and it errors on a language with no lines at all.
## What the type is doing

The look is spare on purpose: white ground, square corners, hairline rules, one pastel doing the
work on any given slide. Dark surfaces — the checkpoint slide, the vocabulary word cell, the
jump menu — use `--caviar`, a warm near-black. Don't reach for `--ink` there: it is a cool
grey tuned for body text on white, and at full-slide size on a projector it reads as navy. Nothing is boxed, shadowed, or rounded. Restraint is the house style —
the density lives in *what is said*, not in how much furniture surrounds it.

- Headlines, card titles, vocabulary words, numbers on charts: the **serif**, regular weight. It
  carries the things worth reading slowly.
- Standfirsts, card bodies, instructions, labels: the **sans**, quiet grey. It carries the things
  read at a glance.
- Eyebrows, section labels, the packet marker: small caps sans, letter-spaced, muted — orientation
  only, never emphasis.

When a slide looks wrong it is usually serif where the sans belongs, or a container that should
have been a hairline.

---

## Segmentation: one idea per slide

A slide carrying three moves at once loses a student who reads slowly. Break it:

- Directions with three steps → three cards on one slide, or three slides if each needs explaining.
- A question plus its sentence stems → one slide; the stems are that question's scaffold.
- A question plus a new word plus a data table → three slides.
- Anything you'd say "and then, also" about → the "also" is the next slide.

Roughly one slide per two to three minutes: a 60-minute period lands around 14-20 slides, a
90-minute block around 20-28.

---

## Components

| Component | Class | What it's for |
|---|---|---|
| **Cards** | `.cards` / `.card` | 2-4 parallel things: options, criteria, the shape of the period. Title plus one or two lines each. `.n` takes a small label (First / Then / Last, or 01 / 02 / 03) |
| **Flow** | `.flow` / `.step` / `.arrow` | Anything with a sequence or a cause: how a system works, the steps of a procedure, a chain from input to result. `.step.end` colors the outcome mint, `.step.problem` colors it peach. `.flow.stack` runs it vertically |
| Panel | `.panel` | A hairline, a label, and a source note above or under a chart. Use it only when the source genuinely needs saying — a chart with a caption usually stands alone |
| Vocabulary | `.vocab` | A new word: the word with how to say it, its meaning, and a non-example |
| Sentence stems | `.frames` | The frames from the packet, shown while students write |
| Big stats | `.stats` | 2-4 numbers that carry the point themselves |
| Static bars | `.bars` | A comparison you don't need to reveal interactively |
| Scale anchor | `.scale` | An abstract quantity as a count of something known — football fields, classrooms, bus rides, phone charges |
| Side by side | `.compare` | Two methods, two claims, before and after |
| Four corners | `.corners` | The four claims with where in the room each one lives |
| Talk slide | `.roles` + `.frames` + `data-phases` | A talk move, run by the slide: the question, each partner's job, the "Say it" stem, and a phased timer. See "Talk slides" below |
| Vote, talk, revote | `.vote` | Hands counted before and after partners talk; the shift between the two bars is what the talk did |
| Game round | `.game` | A fair-guess question with lettered answers: partners agree on the timer and show a letter, V reveals and explains. See "Games" below |
| Sort it | `.sort` | Cards students come up and drag into bins; C checks every card and shows the reason. See "Games" below |
| Pair picker | `.picker` | Calls a pair by number, never by name, after they've rehearsed. P picks |
| What we heard | `.heard` | A board you type students' ideas into during a share-out, credited to pairs |
| Build steps | `data-step` on any element | Holds an element back until → , so the prediction comes before the answer |
| Figure | `.figure` + inline `<svg>` | A diagram drawn in SVG: flows, cross-sections, labeled parts |
| Video | `.body.media` + `.video-wrap` | An embedded, verified video. The body must carry `media` — that is what sizes the frame by height so it cannot overflow onto the text below it |
| Agenda | `.agenda` | The period at a glance, current block marked with `.now` |
| Checkpoint | `.slide.dark` | One question, nothing else |
| Spanish line | `.es` | The question or the direction in Spanish, abbreviated — see "Language access" |

**Photographs have their own reference** — `references/photographs.md` covers where one is
required, how to pick it so it argues for the slide's claim rather than merely matching the
topic, how to aim the crop, and the four patterns. Every deck carries five to eight in a
60-minute period. The CSS and the blocked-image fallback are already in the template; there is
nothing to paste in.

**Interactive charts are already in the template** — see `references/dataviz.md`. Every deck
carries at least one; `check_deck.py` treats a deck with none as an error. Any lesson touching a number gets two to four of them, usually inside a
`.panel`. That is the part of the deck doing the heaviest teaching in a room where reading is the
barrier.

**The scale anchor is the move worth reaching for.** "2.67 acres" means nothing to a 15-year-old;
"twelve football fields" means something immediately. Do the arithmetic first and state the
conversion on the slide.

---

## Talk slides

Student talk is the non-negotiable in every lesson, at least two moves a period, and the deck is
what runs it, so a talk slide does more than post a question. It carries six things. The checker
errors on a deck with no talk slide and warns on a deck with only one:

1. **The question** as the headline, with its language line under it.
2. **The thing to talk about** — a photograph, chart, or diagram, in the `.talk` layout: the visual
   in `.talk-visual` on the left, the turns and the starter in `.talk-side` on the right. Students
   talk best about something in front of them, and the checker errors on a talk slide without one.
3. **The roles** — `.roles` with one `.role` per turn: who speaks, and what the listener does while
   they wait ("Say it back: *You said…*"). A listener with no job is a student waiting for a turn.
4. **The stem** — `.frames` labeled **Say it**, not **Start here**. It is a speaking frame, so it is
   short enough to say out loud in one breath.
5. **The turns, timed** — `data-phases="Think|30; A talks|60; B talks|60; Share|60"`, with
   `data-timer` set to their sum. One press of S runs every phase and chimes at each switch, and
   the matching `.role` lights up (`data-phase="A talks"`), so you can walk the room instead of
   watching the clock, and a student can see whose turn it is from across it.
6. **Who reports** — the `.picker` on the share slide, after rehearsal. Pairs are numbered, never
   named; the file never holds a student's name.

How each talk move (the lesson skill's talk catalog, or whatever the plan names) lands on screen:

| Move | The slide carries |
|---|---|
| Turn-and-talk | Roles for A and B, "Say it" stem, `Think\|30; A talks\|60; B talks\|60` |
| Think-pair-share | `Think\|60; Pair\|120; Share\|120`, the picker on the share |
| Say it back | Partner B's role reads "Say it back: You said…", then `Switch\|60` |
| Agree / disagree / add on | The claim as the headline, the three stems as three frames |
| Vote, talk, revote | `.vote`: count round 1, run a turn-and-talk, count round 2 |
| Four corners, defend | `.corners`, then `Talk\|120; Defend\|180` and the picker per corner |
| Stations in pairs | One slide per rotation with its own phases, or one `Station\|480` phase each |
| Game round, sort it | `.game` or `.sort` with `data-timer` on the slide: partners agree first, then answer |

Keep the slide still while students talk, and keep the visual on it: the screen is never blanked.
Clicking a photograph opens it at full size with the slide's question under it, for close looking
before or during the talk. **A** reads the headline and its language lines aloud in their own
voices, for the student who can't yet read the question off the wall.

## Games

HTML can do what paper can't: let every guess in the room count, and let a student walk up and
move the idea with their hands. Two game slides do that, and both are talk first: partners agree
on the slide's timer before anyone answers, so a game round counts as one of the lesson's talk
moves.

**No teams and no points unless Zac asks for them.** The game is the guess, the talk and the
reveal; points are an extra he turns on for a class that wants them. When he asks for teams, build
with `--teams 3` (or names, `--teams "Pumps,Roots,Lights"`, two to six). Then one scoreboard sits
in the footer of **every** slide, not only the game slides, and keeps the period's running total
across every game in it: it survives a reload, starts fresh on a new day or after two hours with
no points, and **New period** (click twice) clears it between back-to-back classes. **+** and
**−** score anything by hand, a sort or a good answer in the share-out. Never put `data-teams` on
a slide; the checker errors on it.

**Game round** — a fair-guess question. Every option should be a fair guess, something a student
could reason toward without already knowing the answer; a round where only the student who
memorized it can play is a quiz.

```html
<section class="slide" data-day="Wed 10/1" data-title="Game round" data-timer="60" data-mins="4 min">
  <header class="head"><div class="eyebrow">Game · agree with your partner, then show your letter</div></header>
  <h2>Where should the pump sit?</h2>
  <p class="es">¿Dónde debe ir la bomba?</p>
  <div class="body">
    <div class="game" data-options="Inside the reservoir|Next to the reservoir|Up on the frame"
         data-answer="1" data-points="100"
         data-why="A pump has to sit in the water it moves. Out of the water it runs dry and burns out."></div>
  </div>
</section>
```

Pairs hold up a letter. **V** reveals: the right card turns green and the reason appears. V again
hides it, for a round you want to rerun. `data-answer` counts from 1. In a deck built with teams,
each team's row of letters appears under the options and you click the letter a team holds up to
lock it in (the eyebrow then says "then lock in"); the reveal gives `data-points` to every team
that locked the right one, and hiding it takes them back.

**Sort it** — cards into bins. Students come to the board and drag a card into its bin, or tap a
card and then a bin (or another card already in that bin) on a touch screen or from the laptop.
**C** checks: right cards go green, wrong ones go red, the count appears, and so does the reason.
Start over puts every card back, shuffled.

```html
<div class="sort" data-bins="Needs electricity|No electricity"
     data-items="Pump=1|Grow light=1|Reservoir=2|Net pot=2|Timer=1|Tubing=2"
     data-why="Anything that moves water or makes light runs on electricity. The rest just holds things."></div>
```

Each card reads `Card=bin`, with bins counted from 1; three to eight cards, two or three bins.
With teams on, score a sort by hand with the footer's **+**.

Both need a real `data-why`: the reveal explains in a sentence a student could repeat to a
partner, and never just marks an answer right. The checker reports an error for a game without one, for an answer
or a bin number out of range, and warns on a game slide with no timer.

### A whole review game

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
  the plan or the handover; it turns a game into a talk move.
- Name it by the lesson code, `Science 1.6 - Readiness game.html`. In claude.ai, also show it as an
  artifact so it opens straight from the chat.

Before handing it over: every category has one clue per value, every clue has its language lines,
and every reveal explains rather than only answers.

## Key words

`build_deck.py --packet packet.json` (or `--vocab "reservoir,pump,gallon"`) takes the packet's
`meta.vocab` and the deck marks each of those words **once per slide**, where it first appears,
bold with a yellow highlighter stroke, so the word a student is learning looks like the packet's.
Once is the signal; a word marked every time it appears is noise, and a slide full of yellow
hides the one word that's new. The stroke stays inside its own line, so marks on two lines of a
headline never paint over each other, and on a dark slide the word turns yellow instead. Language
lines, credits, eyebrows and the word cell of a word slide are left plain. Put `data-no-kw` on an
element to leave it plain too. The checker warns about a key word that never appears on any
slide: every key word gets its word slide and shows up where it is used.

## Timers

`data-timer` is seconds; `data-mins` is the label shown when there's no countdown. Timers never
start by themselves — Zac starts them with S or a click when the work actually begins, because a
countdown that starts while students are still finding their pencils is a countdown that lies.

Give a timer to anything with a fixed length: do-now, turn-and-talk, stations, independent work,
the closing. Don't put one on a discussion you might want to let run. Match the packet: 15 minutes
of partner math on the page is `data-timer="900"` on the slide.

---

## Videos

Every lesson gets one. It is the reliable attention reset in a period where reading is expensive,
and a deck without one is usually a deck that ran out of time rather than one that didn't need it.

Put the video in `<div class="body media">` — always. That class sizes the frame from the available
height rather than the width, which keeps it from spilling over whatever sits underneath. Nothing
else goes on a video slide except the link line.

**The template ships a click-to-play facade, not a bare iframe.** The markup carries the verified id
in `data-yt`, shows the YouTube poster image, and swaps in the real player when Zac clicks:

```html
<div class="body media">
  <div class="video-wrap" data-yt="dQw4w9WgXcQ">
    <button class="vfacade" type="button">
      <img src="https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
           alt="Title card showing a greenhouse interior with rows of lettuce under lights.">
      <span class="vbtn"></span>
      <span class="vhint">click to play · TED-Ed · 4 min</span>
    </button>
  </div>
  <p class="vlink">TED-Ed · 4 min ·
    <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" target="_blank" rel="noopener">open on YouTube</a>
    — use this link if the embed is blocked at school</p>
</div>
```

The reason is failure behaviour, and it is worth understanding rather than copying. A bare iframe
renders a **black rectangle** whenever the embed can't load — a filtered school network, a
sandboxed viewer, a room with no internet. Black tells you nothing and offers no way forward. The
facade degrades in stages instead: if the player is blocked you still have a poster and a link; if
the poster is blocked too it falls through to the same labelled card every other photo uses, and
the link is still there. It also means nothing loads from YouTube until someone asks it to, which
is faster and quieter on privacy.

`autoplay=1` is added by the script, after a click. Never put it in the markup — a deck that starts
playing on slide change is a deck that talks over you.

**Verify the id against a real search result, every time.** An id that doesn't resolve looks
identical in the file to one that does; the difference only shows up in front of the class. The
plain link under the frame is not optional for the same reason.

**Print the runtime.** Anything over about six minutes gets a stop-point rather than a full play,
and the eyebrow states the purpose before it plays — *"count what they say they don't need."*

## Before you call it done

Run the checker first — it catches the things that have actually gone wrong before
(no photographs, duplicate photographs, missing captions, the fallback script absent,
template placeholder text left in, base64 bloat, un-aimed crops):

```bash
python3 scripts/check_deck.py "$OUTPUT_DIR/<code> - <short title> - deck.html" --minutes <period> --packet packet.json
```

`--minutes` must be the real period length: the slide bounds (14-20 / 20-28) and the photograph
floor (5-8 / 8-12) are both derived from it.

Fix every error and re-run until it exits clean. Then read the warnings and decide about each
one — they are judgement calls, not noise. The checker cannot see whether a photograph is the
*right* photograph, so the eyes-on checks below still matter:

- Click through every slide: no slide is a bare headline, nothing overlaps the head, and no slide
  carries a summary line under its body.
- Every writing slide has `data-packet`; every packet question appears on some slide.
- Every question and every direction has its Spanish line, and it says the same thing as the
  Spanish on that question in the packet.
- The video is a facade with a real 11-character `data-yt`, a poster with real alt text, and the
  plain link under it. `scripts/find_photos.py probe` on the deck confirms it plays embedded
  and prints its title; check the title is the video you chose.
- Dark surfaces are `--caviar`, not `--ink`.
- Timer seconds match the packet's minutes, and the phases sum to the period.
- Every interactive chart works: starts empty, each click does what it should, the caption lands
  at the end, and the numbers match the packet answer key.
- Every game round's answer and every sort card's bin agree with the packet's answer key.
- New words appear as `.vocab` slides at the moment they're first used, and the packet repeats the
  same wording.
- The deck is a single HTML file with no sidecar folder. Photographs and the video are
  linked by URL — that is expected, and inlining them as base64 is not (it once produced a
  1.9 MB deck). See `references/photographs.md`.
