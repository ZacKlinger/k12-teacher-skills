#!/usr/bin/env bash
# Build the fixture decks and run every check: the static checker, the layout audit at six
# classroom screen sizes, the pointer-and-key interaction tests, and the review board.
#   evals/k12presentation/harness/run.sh [out-dir]
# Needs python3, node and Playwright with Chromium (npm i -g playwright; CHROMIUM_PATH=...
# points it at a Chromium it can't find on its own).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
SKILL="${K12_SKILL:-}"
for base in classroom-plugin/skills plugin/skills my-skills; do
  [ -z "$SKILL" ] && [ -d "$ROOT/$base/k12presentation/scripts" ] && SKILL="$ROOT/$base/k12presentation"
done
[ -n "$SKILL" ] || { echo "can't find k12presentation; set K12_SKILL" >&2; exit 1; }
export K12_SKILL="$SKILL"
OUT="${1:-$(mktemp -d)}"
mkdir -p "$OUT" && cp -r "$HERE/fixtures/img" "$OUT/"
status=0
echo "== checker";      python3 "$HERE/checker_test.py" "$OUT" || status=1
echo; echo "== layout: existing formats";    node "$HERE/layout_audit.js" "$OUT/existing_formats.html" || status=1
echo; echo "== layout: interactive formats"; node "$HERE/layout_audit.js" "$OUT/interactive_formats.html" || status=1
echo; echo "== interactions";                node "$HERE/interactions.js" "$OUT/interactive_formats.html" || status=1
# its deck has lesson-level errors on purpose, so the build's exit code is not the test; a
# build that never wrote the deck must still fail, not test an old one
rm -f "$OUT/edge_cases.html"
python3 "$SKILL/scripts/build_deck.py" "$HERE/fixtures/edge_cases.slides.html" "$OUT/edge_cases.html" \
  --title "Science 1.7 · edge cases" --minutes 30 --vocab "reservoir,pump" --languages es > /dev/null 2>&1
echo; echo "== edge cases";                  node "$HERE/edge_cases.js" "$OUT/edge_cases.html" || status=1
echo; echo "== review board";                node "$HERE/review_board.js" "$SKILL/assets/review_game_template.html" || status=1
echo; [ $status -eq 0 ] && echo "all checks passed (decks in $OUT)" || echo "checks failed (decks in $OUT)"
exit $status
