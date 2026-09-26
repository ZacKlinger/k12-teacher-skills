#!/usr/bin/env python3
"""Check a rendered student packet the way a copier and a student will meet it.

Usage:
    python3 check_packet.py packet.docx [--max-pages 2] [--sheet pages.png]

Converts the packet to PDF with LibreOffice, then measures every page: how far down
the ink reaches, and so how much of the page is paper nobody writes on. It reports
the page count against the budget, any page that ends early because a block too tall
to fit was pushed to the next one, and a last page that is mostly empty. With
--sheet it also writes every page side by side into one image, so the whole packet
can be looked at once instead of page by page.

Needs LibreOffice (soffice), poppler (pdftoppm), and Pillow. If any is missing it says
so and exits 0: the check is worth having, not worth blocking a lesson on.
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

# The renderer's margins are 0.7 in, and the footer sits just above the bottom edge of
# the body, so the measurement stops short of it.
MARGIN_IN = 0.7
FOOTER_IN = 1.0
DPI = 40


def ink_bottom(img, top_px, bottom_px):
    """Lowest row with ink between the margins, as a fraction of the writable height."""
    g = img.convert("L")
    w, _ = g.size
    px = g.load()
    for y in range(bottom_px - 1, top_px, -1):
        dark = 0
        for x in range(0, w, 2):
            if px[x, y] < 200:
                dark += 1
                if dark > 2:
                    return (y - top_px) / float(bottom_px - top_px)
    return 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--max-pages", type=int, default=2,
                    help="page budget: 2 (one sheet, both sides) for a 60-minute lesson")
    ap.add_argument("--sheet", help="write all pages side by side into this PNG")
    args = ap.parse_args()

    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice or not shutil.which("pdftoppm"):
        print("  skip  LibreOffice or pdftoppm is not installed; look at the pages by hand.")
        return 0
    try:
        from PIL import Image
    except ImportError:
        print("  skip  Pillow is not installed; look at the pages by hand.")
        return 0

    work = tempfile.mkdtemp()
    env = dict(os.environ, HOME=os.environ.get("HOME") or work)
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", work,
                    os.path.abspath(args.docx)], capture_output=True, env=env, timeout=180)
    pdfs = glob.glob(os.path.join(work, "*.pdf"))
    if not pdfs:
        print("  skip  LibreOffice could not convert the packet; look at the pages by hand.")
        return 0
    subprocess.run(["pdftoppm", "-r", str(DPI), "-png", pdfs[0], os.path.join(work, "p")],
                   capture_output=True, timeout=120)
    pages = [Image.open(f) for f in sorted(glob.glob(os.path.join(work, "p-*.png")))]
    n = len(pages)

    errors, warns = [], []
    fills = []
    for img in pages:
        top = int(MARGIN_IN * DPI)
        bottom = img.size[1] - int(FOOTER_IN * DPI)
        fills.append(ink_bottom(img, top, bottom))

    print(f"  ok    {n} page(s): " + ", ".join(f"p{i + 1} {f:.0%}" for i, f in enumerate(fills)))
    if n > args.max_pages:
        spare = sum(1 - f for f in fills[:-1]) + (1 - fills[-1])
        errors.append(
            f"{n} pages against a budget of {args.max_pages}. The pages hold about "
            f"{spare:.1f} pages of unused paper between them; recover that first (below), "
            "then cut: a section with no student task, a table that repeats another's rows, "
            "a second writing line nobody will fill.")
    for i, f in enumerate(fills[:-1]):
        if f < 0.75:
            warns.append(
                f"Page {i + 1} ends at {f:.0%}: the next block was too tall to fit and moved "
                "whole. Move a short block (a note, a word bank, a one-line question) after "
                "it so the gap fills, or shorten the tall block.")
    if n > 1 and fills[-1] < 0.4:
        warns.append(
            f"The last page is {fills[-1]:.0%} full. That is a sheet of paper for a few "
            "lines: pull them back onto the page before, or cut.")
    if n % 2 == 1 and n > 1:
        warns.append(f"{n} pages prints with a blank back. An even count uses both sides.")

    if args.sheet:
        w = sum(p.size[0] for p in pages) + 10 * (n - 1)
        h = max(p.size[1] for p in pages)
        sheet = Image.new("RGB", (w, h), "#808080")
        x = 0
        for p in pages:
            sheet.paste(p, (x, 0))
            x += p.size[0] + 10
        sheet.save(args.sheet)
        print(f"  ok    all pages in one image: {args.sheet}")

    for m in warns:
        print(f"  warn  {m}")
    for m in errors:
        print(f"  ERROR {m}")
    shutil.rmtree(work, ignore_errors=True)
    print()
    if errors:
        print(f"{len(errors)} error(s), {len(warns)} warning(s).")
        return 1
    print(f"clean — 0 errors, {len(warns)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
