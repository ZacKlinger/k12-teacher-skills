# ChatGPT editions

The four K-12 skills, prepared for ChatGPT. ChatGPT reads the same open
[Agent Skills](https://github.com/agentskills/agentskills) format as Claude: a folder holding a
`SKILL.md`, its references, and its scripts. So the teaching does not change here. The subject
guides, the output contracts, the worked examples, and the Word-document renderer are the same
files, and the rubrics in [`evals/`](../evals) score both editions alike.

What changes is the runtime around them: where files land, how the teacher is asked a question,
what the sandbox can reach. Those differences run through every `SKILL.md`, which is why the
ChatGPT editions live in their own folder rather than as edits to the Claude ones.

## What's here

```
chatgpt/
├── build.py                    assembles upload-ready skills into chatgpt/dist/
└── skills/<skill-name>/
    ├── SKILL.md                the ChatGPT edition of the skill's instructions
    └── agents/openai.yaml      name, blurb, and starter prompt for ChatGPT's skill picker
```

Those two files per skill are the only ChatGPT-specific ones. At build time, `references/`,
`scripts/`, `LICENSE`, and `NOTICE` come straight from `plugin/skills/<skill-name>/`, so a change
to the pedagogy lands in both editions at once.

## Build and install

1. Build the skills. Python 3 is all it needs:

   ```
   python3 chatgpt/build.py
   ```

   This validates each skill against the Agent Skills specification, then writes
   `chatgpt/dist/<skill-name>/` and `chatgpt/dist/<skill-name>.zip`. Use `--check` to validate
   without writing anything.

2. In ChatGPT, open **Skills**, choose **Create**, then **Upload from your computer**, and upload
   each zip. ChatGPT scans every upload and may mark one Needs Review before it can be used.

3. Optional but recommended: add the **Learning Commons** plugin from ChatGPT's plugin library.
   It gives the skills the Knowledge Graph's standards, progressions, learning components, and
   documented misconceptions. Without it, every skill still works and marks its documents as
   drafted from general best practice.

Availability depends on the account. OpenAI lists
[Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) for Business,
Enterprise, Healthcare, and Edu workspaces, subject to admin settings, and Learning Commons
offers its plugin through
[ChatGPT for Teachers and ChatGPT Edu](https://learningcommons.org/blog/chatgpt-for-teachers/).
Check under **Skills** in your own account before relying on either.

## What differs from the Claude edition

| | Claude edition | ChatGPT edition |
|---|---|---|
| Where documents land | `$OUTPUT_DIR`, attached to the chat | `/mnt/data`, delivered as download links |
| Finding bundled files | relative to the skill | `SKILL_DIR`, located once, since ChatGPT mounts skills outside the working folder |
| Asking the teacher | a structured-question tool when present | one plain chat message, numbered, and the turn ends there |
| Showing progress | a task list when present | one or two sentences in chat |
| Making Word documents | the bundled renderer | the bundled renderer, named explicitly over ChatGPT's own Word skill |
| The sandbox | can install packages | offline: uses the preinstalled python-docx, reads shared links with web browsing |
| Revisions | working files persist | working files can expire, so the skill rebuilds them from the conversation |
| Reading references | read in full | read in full, in chunks when the code tool cuts output short |
| Delivery order | main document attached last, so it lands on top | main document linked first |
| What the teacher has said | the conversation | the conversation, plus ChatGPT memory and custom instructions |
| Lesson prep | tool use left to the model | names the Knowledge Graph calls and the rubric's guardrails (no preamble, no menus, no restructuring) |

Each ChatGPT `SKILL.md` opens with a **Running in ChatGPT** section that carries most of these,
so the steps beneath it can stay close to the Claude wording.

## Keeping the editions in step

When a `SKILL.md` under `plugin/skills/` changes, carry the same change into
`chatgpt/skills/<skill-name>/SKILL.md`. The two files walk the same steps in the same order, so a
side-by-side diff shows only the rows in the table above:

```
git diff --no-index plugin/skills/k12-lesson-plan-creation/SKILL.md chatgpt/skills/k12-lesson-plan-creation/SKILL.md
```

Then run `python3 chatgpt/build.py --check`. It fails when a ChatGPT `SKILL.md` names a reference
or script that no longer exists, carries a Claude-only instruction (a question tool, a task
list, `"$OUTPUT_DIR"`), or breaks the spec's limits, such as the 1024-character description. A
skill added under `plugin/skills/` without a ChatGPT edition is reported too.

Changes to `references/` and `scripts/` need no porting. Rebuild and re-upload.
