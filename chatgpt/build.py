#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""Assemble the ChatGPT editions of the K-12 skills into upload-ready folders and zips.

A ChatGPT skill is its Claude counterpart in plugin/skills/<name>/ (references, scripts,
LICENSE, NOTICE) with the files in chatgpt/skills/<name>/ laid over it (SKILL.md and
agents/openai.yaml). The pedagogy lives in one place; only the runtime instructions differ.

Usage:
    python3 chatgpt/build.py           # validate, then write chatgpt/dist/<name>/ and <name>.zip
    python3 chatgpt/build.py --check   # validate only, write nothing

Validation follows the Agent Skills specification (agentskills.io/specification) and the field
rules for agents/openai.yaml, confirms every references/ or scripts/ path a SKILL.md names
exists in the assembled skill, and flags Claude-only instructions left in a ChatGPT edition.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLAUDE_SKILLS = HERE.parent / "plugin" / "skills"
OVERLAYS = HERE / "skills"
DIST = HERE / "dist"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# A bundled path named in SKILL.md prose, e.g. `references/math.md` or `scripts/render_all.sh`.
BUNDLED_PATH_RE = re.compile(r"\b((?:references|scripts)/[A-Za-z0-9_./-]*[A-Za-z0-9_])")
# Instructions that only make sense in Claude's runtime; a ChatGPT SKILL.md must not carry them.
# Phrases are matched across line wraps, so "structured question\ntool" still counts.
CLAUDE_ONLY = [
    ("structured question tool", "ChatGPT has no question widget; ask in plain chat"),
    ("task-list or to-do tool", "ChatGPT has no task list"),
    ("newest-first", "ChatGPT lists links in reading order; deliver the main document first"),
    ('"$OUTPUT_DIR"', "write to /mnt/data, ChatGPT's folder for downloadable files"),
]
SKIP = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)  # fixed timestamp so a rebuilt zip is byte-identical


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse the flat YAML subset SKILL.md frontmatter uses: plain, quoted, and folded scalars."""
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must open with a --- frontmatter block")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is never closed with ---")
    lines = text[4:end].splitlines()
    fields: dict[str, str] = {}
    i = 0
    while i < len(lines):
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", lines[i])
        i += 1
        if not match:
            continue  # entries nested under a map key (e.g. metadata:) are not validated here
        key, value = match.group(1), match.group(2).strip()
        if value in (">", ">-", "|", "|-"):
            block = []
            while i < len(lines) and (lines[i][:1] in (" ", "\t") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            value = (" " if value.startswith(">") else "\n").join(b for b in block if b)
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = value
    return fields, text[end + 4:]


def parse_openai_yaml(text: str) -> dict[str, str]:
    """Read the quoted `key: "value"` pairs under `interface:` in agents/openai.yaml."""
    fields: dict[str, str] = {}
    in_interface = False
    for line in text.splitlines():
        if re.match(r"^\S", line):
            in_interface = line.strip() == "interface:"
        elif in_interface:
            match = re.match(r'^\s+(\w+):\s*"(.*)"\s*$', line)
            if match:
                fields[match.group(1)] = match.group(2)
    return fields


def validate(name: str, skill: Path) -> list[str]:
    """Return every problem found in one assembled skill folder."""
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    try:
        meta, body = parse_frontmatter(text)
    except ValueError as err:
        return [f"{name}: {err}"]

    errors = []
    if meta.get("name") != name:
        errors.append(f"{name}: frontmatter name is {meta.get('name')!r}; it must match the folder")
    if len(name) > 64 or not NAME_RE.match(name):
        errors.append(f"{name}: name must be 1-64 lowercase letters, digits, and single hyphens")
    description = meta.get("description", "")
    if not 1 <= len(description) <= 1024:
        errors.append(f"{name}: description is {len(description)} characters; 1-1024 allowed")
    if "compatibility" in meta and not 1 <= len(meta["compatibility"]) <= 500:
        errors.append(f"{name}: compatibility is {len(meta['compatibility'])} characters; 1-500 allowed")
    if len(text.splitlines()) > 500:
        errors.append(f"{name}: SKILL.md runs {len(text.splitlines())} lines; keep it under 500")

    for path in sorted(set(BUNDLED_PATH_RE.findall(body))):
        if not (skill / path).exists():
            errors.append(f"{name}: SKILL.md names {path}, which the assembled skill does not contain")
    for phrase, why in CLAUDE_ONLY:
        pattern = r"[\s-]+".join(re.escape(word) for word in re.split(r"[\s-]+", phrase))
        if re.search(pattern, body, re.IGNORECASE):
            errors.append(f"{name}: SKILL.md still says {phrase!r} ({why})")

    yaml_path = skill / "agents" / "openai.yaml"
    if not yaml_path.exists():
        errors.append(f"{name}: agents/openai.yaml is missing")
        return errors
    ui = parse_openai_yaml(yaml_path.read_text(encoding="utf-8"))
    for field in ("display_name", "short_description", "default_prompt"):
        if not ui.get(field):
            errors.append(f"{name}: agents/openai.yaml needs a quoted interface.{field}")
    blurb = ui.get("short_description", "")
    if blurb and not 25 <= len(blurb) <= 64:
        errors.append(f"{name}: interface.short_description is {len(blurb)} characters; 25-64 allowed")
    if ui.get("default_prompt") and f"${name}" not in ui["default_prompt"]:
        errors.append(f"{name}: interface.default_prompt must mention the skill as ${name}")
    return errors


def assemble(name: str, dest: Path) -> None:
    """Copy the Claude skill folder to dest, then lay the ChatGPT overlay files over it."""
    shutil.copytree(CLAUDE_SKILLS / name, dest, ignore=SKIP)
    overlay = OVERLAYS / name
    for src in sorted(overlay.rglob("*")):
        if src.is_file() and src.name != ".DS_Store":
            target = dest / src.relative_to(overlay)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)


def write_zip(skill: Path, zip_path: Path) -> None:
    """Zip a skill folder with the folder itself at the archive root, as skill uploads expect."""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for src in sorted(p for p in skill.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo((Path(skill.name) / src.relative_to(skill)).as_posix(), ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (src.stat().st_mode & 0o777) << 16
            archive.writestr(info, src.read_bytes())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = ap.parse_args()

    names = sorted(p.name for p in OVERLAYS.iterdir() if p.is_dir())
    unported = sorted(p.name for p in CLAUDE_SKILLS.iterdir()
                      if p.is_dir() and p.name not in names)
    for name in unported:
        print(f"note: plugin/skills/{name} has no ChatGPT edition in chatgpt/skills/", file=sys.stderr)

    errors = [f"{name}: no matching plugin/skills/{name} to build from"
              for name in names if not (CLAUDE_SKILLS / name).is_dir()]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp)
        for name in names:
            assemble(name, staging / name)
            errors += validate(name, staging / name)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        if args.check:
            print(f"ok: {len(names)} ChatGPT skills validate ({', '.join(names)})")
            return 0

        DIST.mkdir(exist_ok=True)
        for name in names:
            dest = DIST / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(staging / name, dest)
            write_zip(dest, DIST / f"{name}.zip")
            print(f"built {dest.relative_to(HERE.parent)}/ and {name}.zip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
