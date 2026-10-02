#!/usr/bin/env python3
"""Find, judge, and test deck photographs from Wikimedia Commons, with no browser.

Usage:
    python3 find_photos.py search --slot roots "lettuce roots net pot bare" \
                                  --slot pump "submersible water pump aquarium" \
                                  [--out photo-candidates] [--n 12]
    python3 find_photos.py pick photo-candidates roots 3 --focus "30% 25%" --pattern pgrid \
                                  [--library photo-library.md --claim "..." --alt "..."]
    python3 find_photos.py probe "Science 1.7 - Pump build - deck.html"

search  One Commons query per slot (the frame test's nouns, not the topic's). Drops
        scans, PDFs, small files and panoramas, then writes one contact sheet per slot:
        every candidate numbered, shown whole (never cropped, so the subject's place in
        the frame is visible), with a faint grid at 25/50/75% to read --focus off. Look
        at each sheet once and judge it against the frame test. The numbered list on
        stdout carries size, license, author and the file's own description.
pick    Prints the slide-ready URL and credit line for candidate N, load-tests that exact
        URL, and draws the photo the way the slide pattern will crop it at --focus,
        at the narrowest and the widest shape that pattern takes on a projector, into
        one image. With --library it appends the row to the unit photo library.
probe   Load-tests every linked photograph in a finished deck and asks YouTube whether
        each video will play embedded, so nothing has to be opened in a browser to know
        the pictures and the video will appear.

This runs in Claude's own sandbox. It needs network access to commons.wikimedia.org and
upload.wikimedia.org; when the sandbox can't reach them it says so and exits 2, and
references/photographs.md has the fallback. Requires Pillow for the images (the lists
still print without it).
"""

import argparse
import concurrent.futures
import html
import io
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
FILEPATH = "https://commons.wikimedia.org/wiki/Special:FilePath/"
# Wikimedia asks every client for a descriptive User-Agent and blocks generic ones.
UA = ("k12presentation/1.0 (classroom slide builder; "
      "https://github.com/ZacKlinger/k12-teacher-skills) python-urllib")
THUMB_W = 330
PHOTO_MIME = ("image/jpeg", "image/png", "image/webp")

# The shapes each slide pattern crops to, measured in the deck template on 1024x768,
# 1280x720 and 1920x1080 screens. A subject that survives the narrowest and the widest
# survives every projector in between.
PATTERNS = {
    "photo":  {"width": 1400, "shapes": []},                 # letterboxed, never cropped
    "pinned": {"width": 1400, "shapes": []},
    "fill":   {"width": 1400, "shapes": [(2.0, "1024x768"), (3.0, "1280x720")]},
    "pgrid":  {"width": 900,  "shapes": [(1.05, "1024x768"), (1.6, "1280x720")]},
    "talk":   {"width": 1400, "shapes": [(1.2, "1024x768"), (1.8, "1280x720")]},
    "vocab":  {"width": 900,  "shapes": [(0.8, "narrow cell"), (1.3, "wide cell")]},
}

NETWORK_HELP = """\
Commons is not reachable from this sandbox ({err}).

To fix it once: in Claude's settings, under Capabilities, find code execution's network
access and allow commons.wikimedia.org and upload.wikimedia.org (or all domains).
Until then, use the fallback in references/photographs.md section 4: web search
restricted to commons.wikimedia.org, judged from each file page. Never open a
browser tab for photographs, and never ask Zac for them."""


class NetworkDown(Exception):
    pass


def _get(url, timeout=25):
    """Fetch a URL; return (bytes, content type, final url). Network-level failures
    (no route, proxy refusal, DNS) raise NetworkDown; HTTP errors raise HTTPError."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.headers.get("Content-Type", ""), r.geturl()
    except urllib.error.HTTPError:
        raise
    except (urllib.error.URLError, OSError) as e:
        raise NetworkDown(str(getattr(e, "reason", e)))


def plain(s, limit=None):
    """Commons metadata is HTML; reduce it to one line of text."""
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    if limit and len(s) > limit:
        s = s[: limit - 1].rstrip() + "…"
    return s


def file_url(name, width):
    return FILEPATH + urllib.parse.quote(name.replace(" ", "_"), safe="") + f"?width={width}"


def credit_line(c):
    lic = c["license"] or "see file page"
    if lic.lower() in ("public domain", "pd", "cc0"):
        lic = "Public domain" if lic.lower() != "cc0" else "CC0"
    who = c["artist"]
    if who and len(who) <= 40 and lic not in ("Public domain", "CC0"):
        return f"Photo: {who} · Wikimedia Commons · {lic}"
    return f"Wikimedia Commons · {lic}"


# ------------------------------------------------------------------ search

def query_commons(q, n):
    if "filetype:" not in q:
        # Commons indexes scanned books and PDFs in the file namespace; this keeps
        # the results to photographs.
        q += " filetype:bitmap"
    params = {
        "action": "query", "format": "json", "formatversion": "2",
        "generator": "search", "gsrnamespace": "6", "gsrsearch": q,
        "gsrlimit": str(min(50, n * 3)),
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": str(THUMB_W),
        "iiextmetadatafilter": "LicenseShortName|Artist|ImageDescription|Credit",
    }
    body, _, _ = _get(API + "?" + urllib.parse.urlencode(params))
    pages = (json.loads(body).get("query") or {}).get("pages") or []
    pages.sort(key=lambda p: p.get("index", 0))
    out = []
    for p in pages:
        info = (p.get("imageinfo") or [{}])[0]
        w, h = info.get("width", 0), info.get("height", 0)
        if info.get("mime") not in PHOTO_MIME or w < 1000 or not h:
            continue
        if not 0.45 <= w / h <= 3.2:      # panoramas render as a stripe, slivers as a post
            continue
        meta = info.get("extmetadata") or {}
        name = p["title"].split(":", 1)[1]
        out.append({
            "file": name,
            "width": w, "height": h,
            "license": plain((meta.get("LicenseShortName") or {}).get("value")),
            "artist": plain((meta.get("Artist") or {}).get("value"), 60),
            "description": plain((meta.get("ImageDescription") or {}).get("value"), 160),
            "page": info.get("descriptionurl", ""),
            "thumb": info.get("thumburl", ""),
        })
        if len(out) == n:
            break
    for i, c in enumerate(out, 1):
        c["n"] = i
    return out


def _font(size):
    try:
        from PIL import ImageFont
    except ImportError:
        return None
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
                 "/Library/Fonts/Arial Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _grid(draw, x0, y0, w, h, font):
    """Faint lines at 25/50/75% of the photo, labeled, so --focus can be read off."""
    for f in (0.25, 0.5, 0.75):
        x, y = x0 + int(w * f), y0 + int(h * f)
        for xy in (((x, y0), (x, y0 + h)), ((x0, y), (x0 + w, y))):
            draw.line(xy, fill=(0, 0, 0, 90), width=3)
            draw.line(xy, fill=(255, 255, 255, 150), width=1)
        lab = str(int(f * 100))
        draw.text((x + 3, y0 + 2), lab, fill=(255, 255, 255, 230), font=font,
                  stroke_width=2, stroke_fill=(0, 0, 0, 200))
        draw.text((x0 + 3, y + 2), lab, fill=(255, 255, 255, 230), font=font,
                  stroke_width=2, stroke_fill=(0, 0, 0, 200))


def contact_sheet(slot, query, cands, thumbs, path):
    from PIL import Image, ImageDraw
    cols, tw, th, cap = 4, 340, 255, 30
    rows = max(1, (len(cands) + cols - 1) // cols)
    head = 44
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, head + rows * (th + cap + 8) + 8),
                      (34, 34, 34))
    d = ImageDraw.Draw(sheet, "RGBA")
    big, mid, small = _font(26), _font(15), _font(12)
    d.text((10, 10), f"{slot}  ·  {query}", fill=(255, 255, 255), font=mid)
    for i, c in enumerate(cands):
        x = 8 + (i % cols) * (tw + 8)
        y = head + (i // cols) * (th + cap + 8)
        d.rectangle((x, y, x + tw - 1, y + th - 1), fill=(60, 60, 60))
        im = thumbs.get(c["n"])
        if im is None:
            d.text((x + 12, y + th // 2 - 8), "did not load: reject", fill=(255, 120, 120), font=mid)
        else:
            im = im.convert("RGB")
            im.thumbnail((tw, th))
            ox, oy = x + (tw - im.width) // 2, y + (th - im.height) // 2
            sheet.paste(im, (ox, oy))
            _grid(d, ox, oy, im.width, im.height, small)
        d.rectangle((x, y, x + 44, y + 36), fill=(0, 0, 0, 200))
        d.text((x + 6, y + 3), f"{c['n']}", fill=(255, 214, 0), font=big)
        d.rectangle((x, y + th, x + tw - 1, y + th + cap - 1), fill=(255, 255, 255))
        d.text((x + 6, y + th + 7),
               f"#{c['n']}  {c['width']}×{c['height']}  {c['license'] or '?'}",
               fill=(20, 20, 20), font=mid)
    sheet.save(path)


def cmd_search(args):
    os.makedirs(args.out, exist_ok=True)
    store_path = os.path.join(args.out, "candidates.json")
    store = json.load(open(store_path)) if os.path.exists(store_path) else {}
    try:
        import PIL  # noqa: F401
        have_pil = True
    except ImportError:
        have_pil = False
        print("note  Pillow is missing (pip install pillow), so no contact sheets; "
              "judge from the descriptions and file pages.")
    for slot, query in args.slot:
        try:
            cands = query_commons(query, args.n)
        except NetworkDown as e:
            print(NETWORK_HELP.format(err=e), file=sys.stderr)
            return 2
        except urllib.error.HTTPError as e:
            print(f"Commons answered {e.code} for slot '{slot}'. Try again in a minute.",
                  file=sys.stderr)
            return 2
        store[slot] = {"query": query, "candidates": cands}
        print(f"\n[{slot}] {query}: {len(cands)} candidate(s)")
        if not cands:
            print("  none passed the filters. Change the nouns (the frame test's, not the "
                  "topic's) and search again.")
            continue
        thumbs = {}
        if have_pil:
            from PIL import Image

            def load(c):
                try:
                    im = Image.open(io.BytesIO(_get(c["thumb"])[0]))
                    im.load()
                    return c["n"], im
                except Exception:          # a tile that won't load is a rejected tile
                    return c["n"], None
            with concurrent.futures.ThreadPoolExecutor(4) as pool:
                thumbs = dict(pool.map(load, cands))
            sheet = os.path.join(args.out, f"{slot}.png")
            contact_sheet(slot, query, cands, thumbs, sheet)
            print(f"  sheet: {sheet}")
        for c in cands:
            flag = "" if not have_pil or thumbs.get(c["n"]) is not None else "  [thumbnail failed]"
            who = f" · {c['artist']}" if c["artist"] else ""
            print(f"  #{c['n']:<2} {c['file']} · {c['width']}×{c['height']} · "
                  f"{c['license'] or '?'}{who}{flag}")
            if c["description"]:
                print(f"       {c['description']}")
    with open(store_path, "w") as fh:
        json.dump(store, fh, indent=1)
    print(f"\nLook at each sheet once; pick with: find_photos.py pick {args.out} <slot> <number> "
          "--focus \"x% y%\" --pattern <photo|fill|pgrid|talk|vocab|pinned>")
    return 0


# ------------------------------------------------------------------ pick

def parse_focus(s):
    m = re.fullmatch(r"\s*(\d{1,3})%\s+(\d{1,3})%\s*", s or "")
    if not m:
        raise SystemExit(f"--focus takes two percentages, like \"30% 25%\", not {s!r}")
    return int(m.group(1)) / 100, int(m.group(2)) / 100


def crop_like_css(im, ratio, fx, fy):
    """object-fit: cover with object-position: fx fy -- the point fx across the image
    lines up with the point fx across the box, and likewise down."""
    w, h = im.size
    if w / h > ratio:                      # too wide: crop the sides
        cw, ch = int(h * ratio), h
    else:                                  # too tall: crop top and bottom
        cw, ch = w, int(w / ratio)
    x = int((w - cw) * fx)
    y = int((h - ch) * fy)
    return im.crop((x, y, x + cw, y + ch))


def crop_preview(im, pattern, fx, fy, path):
    from PIL import Image, ImageDraw
    shapes = PATTERNS[pattern]["shapes"]
    mid = _font(15)
    panels = [("whole photo, --focus marked", im.copy())]
    for ratio, where in shapes:
        panels.append((f"as the slide crops it ({where})", crop_like_css(im, ratio, fx, fy)))
    hgt = 300
    scaled = []
    for label, p in panels:
        p = p.convert("RGB")
        p = p.resize((max(1, int(p.width * hgt / p.height)), hgt))
        scaled.append((label, p))
    W = sum(p.width for _, p in scaled) + 12 * (len(scaled) + 1)
    sheet = Image.new("RGB", (W, hgt + 46), (34, 34, 34))
    d = ImageDraw.Draw(sheet, "RGBA")
    x = 12
    for i, (label, p) in enumerate(scaled):
        sheet.paste(p, (x, 34))
        if i == 0:                         # mark the focus point on the whole photo
            cx, cy = x + int(p.width * fx), 34 + int(p.height * fy)
            d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), outline=(255, 214, 0), width=3)
            d.line((cx - 15, cy, cx + 15, cy), fill=(255, 214, 0), width=2)
            d.line((cx, cy - 15, cx, cy + 15), fill=(255, 214, 0), width=2)
        d.text((x, 10), label, fill=(255, 255, 255), font=mid)
        x += p.width + 12
    sheet.save(path)


def probe_url(url):
    """Load the exact URL the slide will use. Returns (ok, detail, image or None)."""
    try:
        body, ctype, _ = _get(url, timeout=30)
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}", None
    if not ctype.startswith("image/"):
        return False, f"not an image ({ctype or 'no type'})", None
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(body))
        im.load()
        return True, f"{im.width}x{im.height}, {len(body) // 1000} KB", im
    except ImportError:
        return True, f"{len(body) // 1000} KB", None
    except Exception:
        return False, "bytes arrived but are not a readable image", None


def cmd_pick(args):
    store_path = os.path.join(args.dir, "candidates.json")
    if not os.path.exists(store_path):
        print(f"No {store_path}; run search first.", file=sys.stderr)
        return 1
    slot = json.load(open(store_path)).get(args.slot)
    if not slot:
        print(f"No slot '{args.slot}' in {store_path}.", file=sys.stderr)
        return 1
    c = next((c for c in slot["candidates"] if c["n"] == args.number), None)
    if not c:
        print(f"No #{args.number} in slot '{args.slot}'.", file=sys.stderr)
        return 1
    fx, fy = parse_focus(args.focus)
    width = args.width or PATTERNS[args.pattern]["width"]
    url = file_url(c["file"], width)
    try:
        ok, detail, im = probe_url(url)
    except NetworkDown as e:
        print(NETWORK_HELP.format(err=e), file=sys.stderr)
        return 2
    credit = credit_line(c)
    print(f"src     {url}")
    print(f"focus   --focus:{args.focus.strip()}")
    print(f"credit  {credit}")
    print(f"file    {c['page'] or c['file']}")
    print(f"load    {'ok' if ok else 'FAIL'}  {detail}")
    if not ok:
        print("        Do not ship it: pick another candidate.")
        return 1
    if im is not None and PATTERNS[args.pattern]["shapes"]:
        out = os.path.join(args.dir, f"{args.slot}-pick.png")
        crop_preview(im, args.pattern, fx, fy, out)
        print(f"crops   {out}  (look once: the frame test's subject must survive every crop)")
    if args.library:
        if not (args.claim and args.alt):
            print("library skipped: --claim and --alt are both needed for a row.", file=sys.stderr)
        else:
            new = not os.path.exists(args.library)
            with open(args.library, "a", encoding="utf-8") as fh:
                if new:
                    fh.write("# Unit photo library\n\nEvery photograph that passed its frame test. "
                             "Read this before searching.\n\n"
                             "| Claim | File | Focus | Credit | Alt text |\n|---|---|---|---|---|\n")
                cell = lambda s: s.replace("|", "/").strip()
                fh.write(f"| {cell(args.claim)} | {cell(c['file'])} | {args.focus.strip()} | "
                         f"{cell(credit)} | {cell(args.alt)} |\n")
            print(f"library row added to {args.library}")
    return 0


# ------------------------------------------------------------------ probe

def probe_video(vid):
    """Ask YouTube's oEmbed endpoint about a video: it answers 200 with the title for a
    video that will play inside the deck, 401 or 403 when embedding is off or the video is
    private, 404 when there is no such video."""
    url = ("https://www.youtube.com/oembed?format=json&url="
           + urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}", safe=""))
    try:
        body, _, _ = _get(url, timeout=20)
    except urllib.error.HTTPError as e:
        why = {401: "embedding is off or the video is private",
               403: "embedding is off or the video is private",
               404: "no such video", 400: "no such video"}.get(e.code, f"HTTP {e.code}")
        return False, why
    try:
        meta = json.loads(body)
        return True, f"plays in the deck: \"{meta.get('title', '?')}\" ({meta.get('author_name', '?')})"
    except ValueError:
        return False, "YouTube answered with something that is not oEmbed"


def cmd_probe(args):
    try:
        page = open(args.deck, encoding="utf-8").read()
    except OSError as e:
        print(f"cannot read {args.deck}: {e}", file=sys.stderr)
        return 1
    urls = []
    for src in re.findall(r"<img\b[^>]*?\bsrc=\"(https?://[^\"]+)\"", page):
        src = html.unescape(src)
        if src not in urls and "img.youtube.com" not in src:
            urls.append(src)
    videos = [v for v in dict.fromkeys(re.findall(r'data-yt="([A-Za-z0-9_-]{11})"', page))
              if v != "VIDEO_ID"]
    if not urls and not videos:
        print("No linked photographs or videos in the deck.")
        return 1

    def one(u):
        try:
            ok, detail, _ = probe_url(u)
        except NetworkDown as e:
            return u, None, str(e)
        except Exception as e:             # one bad URL fails itself, not the whole probe
            return u, False, f"error: {e}"
        return u, ok, detail
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        results = list(pool.map(one, urls))
    if results and all(ok is None for _, ok, _ in results):
        print(NETWORK_HELP.format(err=results[0][2]), file=sys.stderr)
        return 2
    bad = 0
    for u, ok, detail in results:
        name = urllib.parse.unquote(u.rsplit("/", 1)[-1])
        print(f"  {'ok  ' if ok else 'FAIL'}  {name[:70]}  {detail}")
        bad += not ok
    if urls:
        print(f"{len(urls) - bad} of {len(urls)} photographs load."
              + ("" if not bad else " Replace every FAIL with another candidate."))
    for vid in videos:
        try:
            ok, detail = probe_video(vid)
        except NetworkDown:
            print(f"  note  video {vid}: YouTube is not reachable from this sandbox; "
                  "say in the handover that the video wasn't play-tested.")
            continue
        print(f"  {'ok  ' if ok else 'FAIL'}  video {vid}  {detail}")
        bad += not ok
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="one query per slot, one contact sheet per slot")
    s.add_argument("--slot", nargs=2, action="append", required=True, metavar=("NAME", "QUERY"))
    s.add_argument("--out", default="photo-candidates")
    s.add_argument("--n", type=int, default=12)
    p = sub.add_parser("pick", help="URL, credit, load test and crop preview for one candidate")
    p.add_argument("dir")
    p.add_argument("slot")
    p.add_argument("number", type=int)
    p.add_argument("--focus", default="50% 50%")
    p.add_argument("--pattern", choices=sorted(PATTERNS), default="photo")
    p.add_argument("--width", type=int)
    p.add_argument("--library")
    p.add_argument("--claim")
    p.add_argument("--alt")
    r = sub.add_parser("probe", help="load-test every photograph and video in a deck")
    r.add_argument("deck")
    args = ap.parse_args()
    return {"search": cmd_search, "pick": cmd_pick, "probe": cmd_probe}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
