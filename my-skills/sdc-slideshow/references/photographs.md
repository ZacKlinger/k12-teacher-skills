# Photographs in the deck

A student who reads at a third-grade level and has never seen a greenhouse cannot picture a
greenhouse from the word. Photographs are where most of this lesson's meaning actually lands, which
is why they carry as many rules as the charts do.

**Contents**
1. [The brief comes before the search](#1-the-brief-comes-before-the-search)
2. [Where a photograph is required](#2-where-a-photograph-is-required)
3. [Sources](#3-sources)
4. [Finding candidates](#4-finding-candidates)
5. [Building the URL](#5-building-the-url)
6. [Judging what came back](#6-judging-what-came-back)
7. [Aiming the crop with `--focus`](#7-aiming-the-crop-with---focus)
8. [Caption, credit, alt text](#8-caption-credit-alt-text)
9. [The four patterns](#9-the-four-patterns)

---

## 1. The brief comes before the search

This is the step that decides whether the photographs feel welded to the lesson or dropped on top
of it. **Do not search for the topic. Search for the evidence.**

A search for "hydroponics" returns pictures of hydroponics, all of them equally true and none of
them arguing for anything. The deck then reads as a topic with pictures near it. What you want is
the photograph that makes one specific sentence undeniable.

So before you search, write the slot down — three lines, in this order:

| Line | What it is | Example |
|---|---|---|
| **Claim** | The one sentence this photo has to make land. Usually the slide's headline. | Lettuce roots can grow with no soil at all. |
| **Frame test** | What must be *visible in the frame* for the claim to land. This is your accept/reject rule, written before you have anything to be lenient about. | Bare white roots hanging in air or water, clearly not in dirt, close enough to see individual roots. |
| **Caption** | What you'll tell students to notice. | Roots sit in a thin film of water, not soil. |

The frame test is the whole trick. Written first, it is a specification. Written after you've found
a nice-looking picture, it becomes a justification for the picture you already like — which is how
a wide, pretty, generic greenhouse shot ends up on a slide about roots.

This is the *focus* half of flare and focus (generate wide, then judge hard): §4 pulls 8-12
candidates precisely so that §6 has something to reject, and the frame test is the criterion that
makes rejecting possible. Converging on the first plausible photo is the single most
common way a deck ends up with pictures near the topic instead of pictures arguing for the lesson.

Then search using the *frame test's* nouns, not the topic's: `lettuce roots net pot bare` beats
`hydroponics`.

**Every photo in the deck gets its own brief, and no two slots get the same photograph.** If the
same image would serve two slots, at least one of those briefs is too vague to be doing any work —
go back and sharpen the claim. (A real build shipped ten photos of which only eight were distinct;
the repeats were both on slides whose briefs, reconstructed afterwards, were just "show
hydroponics.")

---

## 2. Where a photograph is required

Five to eight in a 60-minute period, eight to twelve on a block. Required at:

- **The opening.** The first content slide shows the real thing the day is about, before any
  definition of it. Students should see it before they are told what it is called.
- **Every new vocabulary word.** The word appears beside a photograph of the actual object or
  process — a real nutrient-film channel, not a cartoon of one.
- **Every number with a physical referent.** Acres, gallons, kilowatts, tons: put the real place or
  object on the slide next to the figure. This is what makes scale land.
- **Any procedure students will run.** Show the equipment as it will look on their table, in the
  arrangement they'll see, so the photo doubles as the setup instruction.

Beyond those, use one wherever the point is easier to see than to say — a comparison, a
notice-and-wonder pair, the moment something goes wrong in a system.

---

## 3. Sources, cheapest and best first

Most of what a deck costs to build is spent finding photographs, and nearly all of that is spent
looking: one real build took 121 screenshots. So take photographs from the first of these that has
one, and only search when none does.

1. **The unit photo library, kept by the skill.** A semester unit comes back to the same subjects
   every week (the frame, roots, a pump, a channel). Every photo that passes §6 goes into
   `photo-library.md` in the working folder, which the skill writes and reads itself: claim, file
   name, `--focus`, credit, alt text, one row each (`find_photos.py pick --library` writes the row).
   The next lesson reads the table before it searches. Zero searching for a subject already found,
   and the class sees the same pump on Friday that it saw on Monday, which is a feature:
   recognition is cheap for a reader.
2. **Wikimedia Commons**, searched by `scripts/find_photos.py` (§4). Free to use with a credit
   line, doesn't block hotlinking, and holds real photography for nearly every science and
   applied-math topic, including most of what NASA, USDA, NOAA, USGS and NIH have released into
   the public domain, so one search reaches those collections too.

**Photographs never depend on Zac.** Never ask him for one, never wait on an upload, and never
build a slot around a picture of the class: sourcing them is the skill's job, every time. A deck
that needs a photograph from him is a deck that isn't ready on the morning he opens it.

**Never open a browser tab to find, judge, or test a photograph.** Not Claude in Chrome, not a
built-in browser. The script does all three from the sandbox, and it costs one image per slot
instead of a screenshot per candidate.

**Never** pull an image from a Google Images result page, a stock site, a news article, a blog, a
Pinterest pin, or a district website. Those URLs are licensed, unstable, or hotlink-blocked, and
they are the reason a deck shows a broken icon in front of a class. Stock libraries (Unsplash,
Pexels) are beautiful and wrong for this: they show the idea of hydroponics, not the root that
proves the claim.

**Link photographs by URL.** An earlier build inlined all ten and produced a 1.9 MB file that was
slow to open in front of a class. A linked photograph also survives the trip through Drive: the
deck is one file that looks the same on any computer with a connection.

---

## 4. Finding candidates: one command, one image per slot

Write every slot's brief first (§1), then search them all at once with the frame test's nouns:

```bash
python3 scripts/find_photos.py search --out photo-candidates \
  --slot roots "lettuce roots net pot bare" \
  --slot pump  "submersible water pump bucket" \
  --slot scale "shipping container farm interior"
```

For each slot it runs one Commons query, drops scans, PDFs, files under 1000px and panoramas, and
writes `photo-candidates/<slot>.png`: up to twelve candidates, numbered, each shown **whole**, never
cropped, so you see where the subject sits in the frame. A faint grid at 25, 50 and 75 percent lets
you read `--focus` straight off the tile. The list it prints carries each file's size, license,
author, and its own description, which often settles what a thumbnail can't.

Look at each sheet once and judge it against the frame test (§6). Then take the winner:

```bash
python3 scripts/find_photos.py pick photo-candidates roots 3 --focus "30% 25%" --pattern pgrid \
  --library photo-library.md --claim "Lettuce roots can grow with no soil." \
  --alt "White lettuce roots hang from a black net pot into clear water."
```

`--pattern` is the slide pattern the photo goes into (`photo`, `fill`, `pgrid`, `talk`, `vocab`,
`pinned`; §9). `pick` prints the `src`, the `--focus`, and the credit line to paste, load-tests that
exact URL, and, for a pattern that crops, writes `photo-candidates/<slot>-pick.png`: the whole photo
with the focus marked, beside the crop the slide will make on the narrowest and the widest screen
it meets. Look at it once. If the subject loses its head in either crop, move `--focus` and pick
again; if no focus saves it, take the next candidate.

If a whole sheet fails the frame test, change the nouns and search that one slot again; the new
search replaces only that slot's candidates. That is two images, not twenty screenshots.

### When the sandbox can't reach Commons

The script says so and exits 2. It needs network access to `commons.wikimedia.org` and
`upload.wikimedia.org`, which is a setting on Claude's side (Settings, Capabilities, code
execution's network access), not something to work around. Mention that setting once in the
handover so it gets switched on, and build this deck the slower way:

Search the web restricted to `commons.wikimedia.org` with the frame test's nouns. The results come
back as real `File:` page URLs; the file name is everything after `File:`, percent-decoded. Read
the file page of the three or four likeliest: the description, the size, and the categories
usually say whether a shot is a close-up or a wide establishing view, and files in
`Category:Quality images` are reliably single-subject and sharp. Prefer file names that describe a
single subject over ones that describe a place. You can't see these photographs, so say once in the
handover that they are unverified, and note that the deck degrades a blocked photo to a labeled
card rather than a broken icon. Still no browser tab, and still nothing asked of Zac.

---

## 5. Building the URL

```
https://commons.wikimedia.org/wiki/Special:FilePath/<encodeURIComponent(file name)>?width=1400
```

`width=1400` for a full-slide photo, `width=900` for a grid cell. This redirect resolves any valid
Commons file name, including names with spaces, parentheses, and accents.

**Never hand-assemble an `upload.wikimedia.org/.../thumb/a/ab/...` path.** Those contain a content
hash you cannot guess, and a guessed one 404s every time. Special:FilePath exists precisely so you
don't have to know the hash.

---

## 6. Judging what came back

The load probe below tells you the bytes arrived. It does not tell you the photograph is any good,
and shipping on a green load probe is how misframed photos reach a classroom — one real build took
121 screenshots while building and still shipped subjects cut in half, because nothing in the
process ever asked *is this the right picture, framed the right way.* Loading is the floor. Judging
is the gate.

**Look at every candidate and hold it against its frame test.** Reject on any of these:

- The frame test's subject isn't clearly visible, or you have to hunt for it.
- The subject is small in the frame — a wide establishing shot where the thing that matters is a
  few percent of the pixels. From twelve feet this is a picture of nothing.
- Cluttered background competing with the subject.
- Text, watermark, logo, or a collage baked into the image.
- It's a diagram, a render, or an illustration. A diagram is a `.figure` in SVG, not a photograph.
- The subject sits well off-centre *and* the slot crops (`.pgrid`, `.vc.shot`, `.photo.fill`) —
  either aim `--focus` at it (§7) or take a different photo.
- Under about 800px wide; it will look soft on a projector.

Prefer: one subject filling the frame, recognizable from the back row at twelve feet, people
working over empty equipment. If the point is scale, something familiar has to be in the frame — a
hand, a person, a car, a door.

**Reject and go back to the candidate list.** Rejecting is the normal case, not a failure — that's
why you pulled 8-12. A measured example: six candidates pulled for a hydroponics slide yielded two
usable photographs. One was a portrait of a person in an orchard whose *file name* matched the
query and whose *content* had nothing to do with it; one 404'd; one was a panorama so wide it
rendered as a stripe. Nothing about that is unusual, and none of it is visible from the file name
alone — which is the argument for looking at every candidate. If the whole list fails the frame test, the search terms were the topic's and
not the frame test's; re-read the brief and search again. Only after two honest attempts should you
loosen the claim, and say so in the handover if you do.

Then confirm they load. `pick` already load-tested each photograph's exact URL; once the deck is
built, test them all together, along with the video:

```bash
python3 scripts/find_photos.py probe "<code> - <short title> - deck.html"
```

Anything that isn't `ok` gets replaced with another candidate — not shipped and not explained away.
For the video, `probe` asks YouTube whether it will play inside the deck and prints its title, so a
video whose owner turned embedding off is caught here instead of in front of the class.

The crop preview from `pick` is the look at the photo as a slide. A photo that was fine as a
thumbnail can be badly cropped inside `.pgrid`; that is what `--focus` is for, and the preview is
where you see it.

---

## 7. Aiming the crop with `--focus`

`.pgrid`, `.vc.shot`, and `.photo.fill` crop with `object-fit: cover`, which defaults to a centre
crop at 50% 50%. A subject that isn't dead centre gets cut — this is the stylesheet generating the
misframing, not the photo being bad.

Set `--focus` on the `<figure>` (or the cropping element) as `x% y%`, naming the point that must
survive the crop. Read it off the contact sheet's grid: a subject centred a third of the way across
and a quarter of the way down is `30% 25%`.

```html
<figure style="--focus:30% 25%">   <!-- subject sits upper-left -->
```

Set it on every cropped photo. A centre-framed subject still gets `--focus:50% 50%` written out, so
that "no `--focus`" reliably means "nobody looked."

Uncropped patterns (`.photo`, `.pinned`) letterbox rather than crop, so `--focus` doesn't apply —
but a wide photo will render short inside a tall band. If it looks lost, either use `.photo.fill`
with a `--focus`, or find a photo whose shape suits the slot.

---

## 8. Caption, credit, alt text

All three, on every photograph. A real build shipped ten photos with credits and **zero** captions;
without the caption the photo is decoration and the class looks at it without knowing what for.

- **Caption — what to notice, not what it is.** "Roots sit in a thin film of water, not soil," never
  "A hydroponic system." One line, sentence case, the house sans. It is the third line of the brief
  you already wrote in §1.
- **Credit** — a quiet second line: *Wikimedia Commons · CC BY-SA 4.0*, or *USDA*. One credit per
  slide covers a grid.
- **Alt text** — a real sentence describing the photo, because it becomes the *visible* text if the
  image is ever blocked. Write it so a student could picture the photo from the words alone. A
  filename or a three-word fragment is not alt text.

---

## 9. The four patterns

`assets/deck_template.html` ships working examples of the first two; copy from the file rather than
retyping from here. All the CSS is already in the template — there is nothing to paste in.

**One photograph, full slide** — the opening, the real thing, the scale anchor. The body must carry
`media`; that is what sizes it by height. Add `fill` to crop to the band instead of letterboxing.

```html
<div class="body media">
  <figure class="photo" style="--focus:50% 40%">
    <img src="…?width=1400" alt="Lettuce growing in long white channels inside a greenhouse.">
    <figcaption class="cap">Roots sit in a thin film of water, not soil.
      <span class="cred">Wikimedia Commons · CC BY-SA 4.0</span></figcaption>
  </figure>
</div>
```

**Two to four photographs, compared** — notice-and-wonder, two methods, before and after. The bold
line is the label; the line under it is what to look for.

```html
<div class="body">
  <div class="pgrid">
    <figure style="--focus:50% 45%"><img src="…?width=900" alt="…">
      <figcaption><b>Water</b>Roots in nutrient water</figcaption></figure>
    <figure style="--focus:40% 60%"><img src="…?width=900" alt="…">
      <figcaption><b>Soil</b>Roots in an open field</figcaption></figure>
  </div>
  <p class="cap"><span class="cred">Both photographs: Wikimedia Commons · CC BY-SA 4.0</span></p>
</div>
```

**A word beside the real thing** — the vocabulary slide, with the photo as the middle cell.

```html
<div class="body">
  <div class="vocab">
    <div class="vc word"><div class="k">Word</div><div class="w">nutrient</div>
      <div class="say">NOO-tree-ent</div></div>
    <div class="vc shot" style="--focus:50% 50%">
      <img src="…?width=900" alt="Green water running through a growing channel."></div>
    <div class="vc"><div class="k">Means</div><div class="d">Food a plant needs, mixed into the water.</div></div>
  </div>
</div>
```

**A labeled photograph** — naming the parts of a real system. Pin positions are percentages of the
image box; place them by eye against the actual photo and keep labels off faces and off the
subject.

```html
<div class="body media">
  <div class="pinned">
    <img src="…?width=1400" alt="A hydroponic tray under grow lights.">
    <div class="pin" style="--x:22%;--y:30%"><div class="n">1</div><div class="lab">Light</div></div>
    <div class="pin" style="--x:60%;--y:66%"><div class="n">2</div><div class="lab">Water channel</div></div>
  </div>
</div>
```
