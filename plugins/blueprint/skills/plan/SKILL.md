---
name: plan
description: The build gate. Checks that every requirement and design document is approved and current, then writes the ordered build plan (docs/tasks.md) with traceability to requirements and tests, and adds a managed index to CLAUDE.md so the coding agent builds from the documents. Use when the user is ready to start building, asks for a build plan, task breakdown, or implementation plan, or wants to know whether they may start coding.
argument-hint: "[docs/features/<name>.md for a lite feature]"
---

# Plan

Turn approved documents into an ordered plan the coding agent can follow, and refuse to do it if the documents are not ready. This skill does not write application code.

Arguments: $ARGUMENTS

## 1. The gate (always first)

1. From the project root, run the gate script. Try `python`, and if that is not found try `py`:

   `python '${CLAUDE_PLUGIN_ROOT}/scripts/check_approved.py'`

   For a lite feature (an argument naming a file in `docs/features/`), run it with `--file <that path>` instead. If the project keeps its documents in a folder other than `docs/`, add `--docs <folder>`.
2. If the script cannot run at all, perform the same check yourself: read the header of `docs/prd.md`, `ux.md`, `hld.md`, `lld.md`, and `testplan.md`, and require that each exists, has `status: approved`, and that every version listed in its `based_on` equals the current `version` of that document. **Never skip the gate because the script failed.**
3. **If the gate passes**, continue to section 2.
4. **If the gate fails**, show the table, then explain each problem in plain words with the next step. For example: a document that is `in-review` needs `/blueprint:review <path>` and the user's sign-off; a `STALE` document was written against an older version of its input and needs the owning skill to refresh it (or `/blueprint:sync`); a missing document needs its skill run. Then stop. Do not write the plan.
5. **Override.** Do not suggest bypassing the gate. If the user asks, or explicitly says to proceed anyway, require them to name what they are skipping, then continue. Record `gate: override` and the reason in the `tasks.md` header, and put the list of unapproved or stale documents in a visible "Build risk" box at the top of the plan. Tell them once that tasks built on unapproved documents may need rework.

When you show the user commands to run themselves, use Windows CMD syntax.

## 2. Read everything

Read `docs/prd.md`, `ux.md`, `hld.md`, `lld.md`, `testplan.md`, and the decision log in `docs/discovery.md`. If `docs/tasks.md` exists, read it and update in place: keep task IDs and statuses, add new tasks with new IDs, and mark obsolete ones `cancelled` rather than deleting them. Read the template `${CLAUDE_PLUGIN_ROOT}/templates/tasks.md`.

For a lite feature, read the feature file and write a short `docs/features/<name>-tasks.md` instead of the full plan, with the same header fields as the template (`doc: tasks`, `status: in-review`, `version`, `updated`) and the same task format, usually three to eight tasks. Skip the CLAUDE.md block if one already exists.

## 3. Build the plan

**Task format.** Each task has an ID (`TASK-001`), a title, `Covers` (FR-, UX-, NFR- IDs), `Implements` (S-, M-, API-, table, and error IDs from the design), `Paths` (where the code goes, from the HLD feature map), `Depends`, `Tests` (the T- IDs that must pass), a size, and a status.

**Sizes.** S is about half a day, M is about a day. Anything larger is split. A task a developer cannot finish and test in a day is not a task.

**Order.**
1. **Foundations.** Project setup, configuration, test runner, structured logging with correlation IDs, the error catalog skeleton, and a health check. Debuggability is built first, not added later.
2. **Walking skeleton.** The thinnest end-to-end slice of the most important journey, through UI, API, and data, with its happy-path test. Milestone M1 ends with this working.
3. **Vertical slices** per journey, MUST before SHOULD, each including its API, data, UI, error codes, tests, and a check that its debugging-playbook row works.
4. **Non-functional work** (performance, security, accessibility), scheduled where it can be tested.
5. **Hardening.** Negative and edge cases, regression tests, and updating documents to match what was built.
6. **Release.** The exit criteria from the test plan.

**Milestones.** Each milestone ends with something demonstrable. Write its demo script in one or two lines, and include measuring the real app against the UX budgets where a journey is complete.

**Existing codebase.** Take tasks from the LLD's delta and migration section, in its order, with the rollback step. Put behavior-preserving regression tests before any refactor.

**Rules.**
- Every MUST requirement is covered by at least one task, and every task cites at least one requirement. A task with none is an **enabler**: label it, and give the reason.
- Every task lists the tests that prove it. A task with no test is incomplete.
- Do not edit approved documents. If you find a defect in one while planning, record it under "Issues found while planning" and tell the user to fix it through the owning skill and `/blueprint:review`.

## 4. Traceability

Write a matrix in `tasks.md`, one row per FR, UX, and NFR requirement: tasks that implement it and tests that prove it. List requirements with no task as gaps and fix them before finishing. Do not change the PRD's own traceability table, because that would reopen an approved document.

## 5. The CLAUDE.md index

1. Read the template `${CLAUDE_PLUGIN_ROOT}/templates/claude-md-block.md` and fill in the document table with current versions.
2. If `CLAUDE.md` exists in the project root: replace the text between `<!-- blueprint:start -->` and `<!-- blueprint:end -->` if both markers are present, otherwise append the block at the end. Never change anything outside the markers. If there is no `CLAUDE.md`, create one containing the block.
3. Tell the user in one sentence what was added.

## 6. Hand-off

Write `docs/tasks.md` with `status: in-review`, `version: 0.1`, today's date, and `based_on` listing the five documents with their current versions. Summarize in a few lines: milestones, number of tasks by size, the first task, gaps, and any build risk. Tell the user how to begin, for example: "Ask me to implement TASK-001, following CLAUDE.md." When requirements or code change later, use `/blueprint:sync`.
