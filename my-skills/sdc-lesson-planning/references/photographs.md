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

This is the *focus* half of the flare-and-focus move in `references/design_method.md`: §4 tells you
to pull 8-12 candidates precisely so that §6 has something to reject, and the frame test is the
criterion that makes rejecting possible. Converging on the first plausible photo is the single most
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

1. **The unit photo library.** A semester unit comes back to the same subjects every week (the
   frame, roots, a pump, a channel). Every photo that passes §6 goes into a short table in the
   project knowledge, `photo-library.md`: claim, file name, `--focus`, credit, alt text. The next
   lesson reads the table instead of searching. Zero screenshots, and the class sees the same
   pump on Friday that it saw on Monday, which is a feature: recognition is cheap for a reader.
2. **The class's own photographs.** The frame in the corner, the garden bed, a student build (no
   faces, no names). Nothing argues for "our system" like a picture of it, and it costs nothing to
   find. When Zac uploads one, shrink it to about 1200px wide at JPEG quality 70 and inline it as
   a data URI (it can't be linked); three per deck at most, and the checker holds that line.
3. **Wikimedia Commons**, searched once per slot and judged on a contact sheet (§4). Free to use
   with a credit line, doesn't block hotlinking, and holds real photography for nearly every
   science and applied-math topic. Federal public-domain collections are the next stop: NASA
   (`images-assets.nasa.gov`), USDA, NOAA, USGS, NIH.

**Never** pull an image from a Google Images result page, a stock site, a news article, a blog, a
Pinterest pin, or a district website. Those URLs are licensed, unstable, or hotlink-blocked, and
they are the reason a deck shows a broken icon in front of a class. Stock libraries (Unsplash,
Pexels) are beautiful and wrong for this: they show the idea of hydroponics, not the root that
proves the claim.

**Link public photographs by URL.** An earlier build inlined all ten and produced a 1.9 MB file
that was slow to open in front of a class. Only the class's own photographs are inlined.

---

## 4. Finding candidates: one search, one contact sheet

### Chrome connected (preferred)

For each slot, run one script from any open page. It queries Commons, drops scans and small files,
and lays the candidates out as a numbered grid, so **one screenshot judges all of them** (and every
tile that shows a photo has also passed the load probe):

```js
const q = 'lettuce roots net pot bare filetype:bitmap';   // the frame test's nouns
const api = 'https://commons.wikimedia.org/w/api.php?action=query&format=json&origin=*'
  + '&generator=search&gsrnamespace=6&gsrlimit=16&prop=imageinfo&iiprop=size|extmetadata'
  + '&gsrsearch=' + encodeURIComponent(q);
const pages = Object.values((await fetch(api).then(r => r.json())).query.pages)
  .filter(p => /\.(jpe?g|png|webp)$/i.test(p.title) && p.imageinfo[0].width >= 1000)
  .slice(0, 12);
document.body.innerHTML = '<div id="cs" style="display:grid;grid-template-columns:repeat(4,1fr);'
  + 'gap:6px;background:#222;padding:6px"></div>';
pages.forEach((p, i) => {
  const f = p.title.replace('File:', ''), m = p.imageinfo[0].extmetadata;
  const src = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + encodeURIComponent(f) + '?width=400';
  cs.insertAdjacentHTML('beforeend', '<figure style="margin:0;background:#fff">'
    + '<img src="' + src + '" style="width:100%;height:170px;object-fit:cover">'
    + '<figcaption style="font:13px sans-serif;padding:3px 5px">#' + (i + 1) + ' · '
    + (m.LicenseShortName ? m.LicenseShortName.value : '?') + ' · ' + p.imageinfo[0].width
    + 'px</figcaption></figure>');
});
pages.map((p, i) => '#' + (i + 1) + ' ' + p.title.replace('File:', '')).join('\n');
```

Wait two seconds, take **one** screenshot, and judge the grid against the frame test (§6). The
script returns the numbered file names, so the pick goes straight into §5. If nothing passes,
change the search nouns and run it again; that is still two screenshots, not twenty.

Keep `filetype:bitmap` in the query: Commons indexes scanned books and PDFs in the same namespace,
and without it a real search for `classroom projector screen students` came back with seven PDFs
and one photograph. Return file names only, never the API's `thumburl`: the tool blocks output
containing query strings and you lose the whole result.

**A crop still needs its own look.** The contact sheet shows candidates center-cropped; a photo in
`.pgrid`, `.vc.shot`, `.photo.fill` or `.talk-visual` is cropped again by the slide. Check those
slides once at projection size (§6, last paragraph), not every candidate.

### Chrome not connected

Use `WebSearch` with `allowed_domains: ["commons.wikimedia.org"]` and the frame test's nouns. The
results come back as real `File:` page URLs; the file name is everything after `File:`,
percent-decoded.

You cannot render the image on this path, so you cannot run §6 as written. Lean harder on what you
*can* read: the file name and the file description page usually say whether a shot is a close-up or
a wide establishing view, and Commons categories (`Category:Hydroponics`) are curated better than
search results. Prefer file names that describe a single subject over ones that describe a place.
Then say once in the handover that the photographs are unverified, and note that the deck degrades
a blocked photo to a labeled card rather than a broken icon.

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

Then confirm they load:

```js
const test = u => new Promise(res => {
  const i = new Image();
  const t = setTimeout(() => res('timeout'), 12000);
  i.onload  = () => { clearTimeout(t); res('ok ' + i.naturalWidth + 'x' + i.naturalHeight); };
  i.onerror = () => { clearTimeout(t); res('FAIL'); };
  i.src = u;
});
```

Anything that isn't `ok` gets replaced with another candidate — not shipped and not explained away.

Last, open the finished deck and **look at the photo slides as slides**, at the size they'll be
projected. A photo that was fine as a thumbnail can be badly cropped inside `.pgrid`; that is what
`--focus` is for, and you can only see it here.

---

## 7. Aiming the crop with `--focus`

`.pgrid`, `.vc.shot`, and `.photo.fill` crop with `object-fit: cover`, which defaults to a centre
crop at 50% 50%. A subject that isn't dead centre gets cut — this is the stylesheet generating the
misframing, not the photo being bad.

Set `--focus` on the `<figure>` (or the cropping element) as `x% y%`, naming the point that must
survive the crop:

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
