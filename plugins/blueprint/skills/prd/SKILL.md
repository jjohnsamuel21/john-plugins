---
name: prd
description: Write a complete Product Requirements Document (docs/prd.md) from a finished discovery, with requirement IDs, acceptance criteria, measurable UX targets, and non-goals. Use after the discover skill is done, or when the user asks to write or regenerate the PRD.
argument-hint: "[product name]"
---

# PRD

Turn the discovery record into a PRD that a designer, a developer, and a coding agent can all build from without guessing.

Arguments: $ARGUMENTS

## 1. Preconditions

1. Read `docs/discovery.md`. If it is missing, tell the user to run `/blueprint:discover` first and stop.
2. If its header says `status: draft` (not `ready`), list the unmet readiness items and ask whether to continue anyway. If they say yes, carry those gaps into the PRD as `[ASSUMPTION]` items and open questions. Never hide them.
3. Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/prd.md`. If `docs/prd.md` already exists, read it, keep the requirement IDs unchanged, and update in place instead of renumbering.

## 2. Writing rules

- **Source everything.** Each requirement's Source column cites the discovery decision (D-xxx) or the user statement it comes from. If you cannot cite a source, it is an assumption: mark it `[ASSUMPTION]`.
- **IDs are permanent.** Use `G-` for goals, `FR-` for functional, `UX-` for UX, `NFR-` for non-functional, `R-` for risks, `J-` for journeys, three digits each. Never reuse or renumber an ID after it has been written.
- **One testable statement per requirement.** "The system shall ..." and a Given/When/Then acceptance criterion. If it cannot be tested, rewrite it or move it to open questions.
- **No vague words without a number.** Replace "fast", "easy", "intuitive", "robust", "scalable", "simple" with a measure and a target, or ask the user for one.
- **Describe what, not how.** No architecture, library, or table design in the PRD, except constraints the user stated as hard. Design belongs to later documents.
- **Every journey has a budget** (steps, taps, or seconds) and cites the requirements it depends on.
- **UX requirements are all measurable.** Include the user's usability targets from discovery verbatim in number.
- **Always include** NFRs for debuggability and maintainability, and a non-goals section that is not empty.
- **Prioritize honestly.** MUST means v1 fails without it. If more than about 60 percent of the requirements are MUST, challenge the scope with the user.
- Keep prose short. Use the template's tables.

## 3. Self-check before showing it

Check your own draft and fix what you find:

1. Every FR has an acceptance criterion and a source.
2. Every UX and NFR line has a number.
3. No two requirements contradict each other, and none duplicates another.
4. Every MUST maps to at least one journey or goal, and every journey step is supported by a requirement.
5. Every non-goal and risk from discovery appears in the PRD.
6. Open questions do not block any MUST requirement.

## 4. Hand-off

1. Write `docs/prd.md` with `status: in-review`, today's date, and `based_on: [discovery@<current discovery version>]`. A new PRD is `version: 0.1`; when updating an existing one, bump the version.
2. Tell the user in a few lines: how many requirements by type, the three biggest risks, anything marked as an assumption, and any open question that needs their answer.
3. Recommend `/blueprint:review` next, then `/blueprint:ux` for the screens, flows, and clickable prototype. **Never set `status: approved` yourself.** Only the review skill does that, after the user signs off.
