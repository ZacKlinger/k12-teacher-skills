# Grounding the lesson in real standards

Read this at Step 1.5, before the talk-through. The point is that the objective on the board comes
from the actual standard statement, not from a paraphrase of a paraphrase — and that the
misconceptions the lesson plans for are the documented ones, not the ones that came to mind.

## Use the Learning Commons Knowledge Graph whenever it's connected

Check whether these tools exist in the conversation: `find_standard_statement`,
`find_standards_progression_from_standard`, `find_learning_components_from_standard`,
`find_misconceptions_for_standard`, `find_curriculum_lessons`, `find_materials_for_lesson`. They
may be listed under a connector name rather than plainly — search the available tools for
"standard" before concluding they're absent.

If they exist, call them **before** presenting the talk-through. If a call fails because the
connector isn't authorized, say so once in plain language ("the standards connector needs
authorizing in your connector settings — I'll plan from best knowledge for now") and continue.
Never fabricate a standard code, a statement, or a UUID.

### Resolving the standard

- **A code is known** (from the request or the class profile):
  `find_standard_statement(code=<code>, academicSubject=<subject>)`. Code search is a prefix match,
  so `7.RP` returns the family and `7.RP.A.3` returns the leaf.
- **No code**: `find_standard_statement(keywords=["percent increase", "percent change"],
  academicSubject=<subject>)` — a standard matches if any keyword appears in its description. Pick
  the best fit for the grade, then use its `code` to pull relatives if useful.

`academicSubject` is `"Mathematics"`, `"English Language Arts"`, `"Science"`, or
`"Social Studies"`. Pass `jurisdiction` with the state whenever the profile or the request names
one, so the lesson quotes the state's adopted wording; social studies standards exist only under a
state, so for social studies ask for the state in Step 1 if nothing names it. Cap at three search
attempts; results from the wrong grade band count as a miss, so change the keywords rather than
giving up early. From the chosen standard keep: the verbatim statement, the `code`, and the
`caseIdentifierUUID`; every later call needs the UUID.

**Match the standard to the day, not the unit.** A profile's "standards in play" lists the
unit's standards; today's task may meet a different one. Before settling, say what students will
actually do (build and test a part against criteria, compare two tables, trace a moral through
details) and pick the standard whose verb that is. A test-against-criteria day in a unit filed
under "break the problem down" is the evaluate-against-criteria standard, and the plan should say
so.

### Math — after the standard resolves

Issue these together, then read the results:

1. `find_standards_progression_from_standard(caseIdentifierUUID, direction="backward")` → the one
   primary prerequisite standard. This is what "what students already know coming in" should be
   built on, and it is often the real reason a class is struggling.
2. `find_learning_components_from_standard(caseIdentifierUUID)` → up to five sub-skills. These
   become the lesson's success criteria and the things you watch for while circulating.
3. `find_misconceptions_for_standard(caseIdentifierUUID, subject="Mathematics")` → keep the three
   most relevant. Rewrite each in your own words as a specific wrong answer a student in this class
   would produce, why they produce it, and the move that addresses it. These go in the lesson plan's predicted errors,
   and at least one of them should be what the error-analysis task on the packet is built from.

### Science — after the standard resolves

`find_learning_components_from_standard` and `find_standards_progression_from_standard` return
nothing for science standards; don't call them. Instead:

1. `find_curriculum_lessons(caseIdentifierUUID=<uuid>, author="OpenSciEd")` → pick the closest
   grade-and-topic match.
2. `find_materials_for_lesson(lessonIdentifier, materialSource=["activity"])` → take the anchoring
   phenomenon, the driving question, where this sits in the storyline, which science and
   engineering practices are foregrounded, and which crosscutting concept the lesson leans on.
   These become the three targets and the phenomenon in `references/lesson_design.md`
   ("Science days"). Also name what students must already know coming in, as a specific skill
   ("can read a bar graph with a scale of 5"), so the plan has a prerequisite to check.

### ELA and social studies — after the standard resolves

The graph has no misconceptions or progressions for these subjects; don't call those tools. For
K-2 ELA, `find_learning_components_from_standard(caseIdentifierUUID)` returns sub-skills; use them
as the look-fors. Otherwise the standard statement is the anchor: name the text (ELA) or the
sources (social studies) the lesson turns on, and the specific prior skill students need coming in
("can find a key detail and say which sentence shows it"), so the plan has a prerequisite to check.
Predicted errors come from your knowledge of the standard and the text; say they reflect general
best practice.

**Never reproduce curriculum student-facing text.** Investigation prompts, discussion questions,
and activity narratives inform your design; the words on the packet are always original. Unless
the teacher has said they use OpenSciEd or Illustrative Mathematics, don't name those curricula
anywhere, in the documents or in chat.

## What lands where

- The lesson plan quotes the standard statement verbatim, once, with its code.
- The objective is that standard translated into one "I can…" sentence a student can read.
- The prerequisite standard (math) or the storyline position plus the specific prior skill
  (science) appears in the plan's "what students already know" line.
- The talk-through's opening line names the code plus a ten-word gist, enough for the teacher to
  catch a mismatch immediately.
- Misconceptions become predicted errors in the plan and, where they fit, the error-analysis task
  in the packet.

## When the connector isn't there

Plan from best knowledge, pick the standard you're confident in, and put one line at the bottom of
the lesson plan: *"Planned without the standards connector. Standard alignment and misconceptions
reflect general best practice."* Say the same thing in one sentence in chat so it isn't a surprise.
