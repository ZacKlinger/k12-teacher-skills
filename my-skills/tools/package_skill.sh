#!/usr/bin/env bash
# Zip a skill in my-skills/ for upload to claude.ai (Settings > Capabilities > Skills).
#   my-skills/tools/package_skill.sh k12lessonplan
# Writes my-skills/dist/<skill>.zip with the skill folder at the root of the archive.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
skill="${1:?usage: package_skill.sh <skill-folder-name>}"
[ -f "$here/$skill/SKILL.md" ] || { echo "no SKILL.md in $here/$skill" >&2; exit 1; }
mkdir -p "$here/dist"
out="$here/dist/$skill.zip"
rm -f "$out"
(cd "$here" && zip -qr "$out" "$skill" -x '*/__pycache__/*' '*.pyc' '*/.DS_Store')
echo "wrote $out ($(du -h "$out" | cut -f1))"
