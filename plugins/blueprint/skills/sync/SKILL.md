---
name: sync
description: Keep documents and code consistent after something changes. Finds which requirement, UX, design, test, and task documents are stale after a requirements change, shows the impact by requirement ID, and detects drift between the code and the design documents, then applies the updates the user agrees to. Use when requirements changed, when code was changed without updating the documents, when review or the gate reports a stale document, or when the user asks what a change affects.
argument-hint: "[docs | code | all] (default: all)"
---

# Sync

Documents rot the moment code or requirements move on without them. This skill finds out what is out of date, shows what a change touches, and brings the documents back in line, one decision at a time. It never edits application code and never resolves a conflict silently.

Arguments: $ARGUMENTS

## 1. See where things stand

1. Run the status script from the project root (try `python`, then `py`):

   `python '${CLAUDE_PLUGIN_ROOT}/scripts/check_approved.py' --all --json`

   It lists every document with its status, version, and any `STALE` or missing-upstream problems. If the script cannot run, read the document headers yourself and compare each `based_on` version with the current version of that document.
2. Documents written before version tracking existed have no `based_on` line. Treat them as unknown, compare their `updated` dates with their upstream documents, and add `based_on` when you update them.
3. Note whether the project is a git repository. Git history makes the next steps precise; without it, ask the user what changed and rely on the document comparison below.

Use the **docs** direction (section 2) when requirements or documents changed, the **code** direction (section 3) when code changed, or both for `all`.

## 2. Docs direction: a requirement or upstream document changed

1. **Find what changed upstream.** For each stale document, take the upstream document it was built on. With git: find the commit where the downstream document was last changed and diff the upstream document against it. Without git: compare the set of requirement IDs in the upstream document with the IDs cited in the downstream coverage tables, and ask the user to describe anything else that changed. List the changes by ID: added, changed, removed.
2. **Impact analysis.** For each changed ID, search all of `docs/` for that ID and list where it is cited: screens (S-), journeys (J-), modules (M-), APIs, tables, error codes, test cases (T-), and tasks (TASK-). Build one table: changed ID, change, and everything affected, in dependency order (UX, then design, then test plan, then tasks).
3. **Check for the unwritten.** Note requirements with no downstream coverage (new ones) and downstream items citing IDs that no longer exist (orphans).

## 3. Code direction: the code moved away from the documents

Compare what the code does with what the documents say, and report each difference:

- Routes and endpoints in the code against the API contracts in the LLD.
- Models, schemas, and migrations against the LLD data model.
- Error codes raised in the code against the error catalog.
- The folder structure and module boundaries against the HLD, and, if it exists, against `docs/codebase-map.md` (suggest `/blueprint:map --refresh` when the map is the thing that is stale).
- Configuration variables against the LLD configuration table.
- With git: changes to the code since the documents were last updated, to know where to look first.

For each difference, work out which side is probably wrong, but do not decide. A difference is either **doc drift** (the code is right and the document should change) or **code drift** (the document is right and the code is a bug or a shortcut).

## 4. Write the sync report

Create `docs/sync-report.md` with today's date and scope:

- A findings table: ID (SY-001, ...), type (doc-stale, doc-drift, code-drift, orphan, gap), location, what differs, and your proposed resolution.
- The impact table from section 2.
- A short list of decisions needed from the user.

## 5. Decide, then apply

1. Present the findings in batches by importance. For each one, ask the user to choose: **update the document**, **change the code** (becomes a task, not an edit), or **ignore** (recorded in the report as accepted drift).
2. **Never invent a requirement.** A change to the PRD happens only when the user states the new or changed behavior. If code drift suggests the product behavior has changed, ask whether that behavior is now intended before touching the PRD.
3. Apply the agreed updates in dependency order: PRD, UX (and prototype), HLD, LLD, test plan, tasks. For each document:
   - Make minimal edits. Keep IDs stable. Never reuse an ID; new items get new IDs, removed items are marked removed.
   - Bump `version`, set `updated`, and set `based_on` to the current versions of its inputs.
   - If it was `approved`, set it back to `in-review` and say so.
4. **Tasks** (`docs/tasks.md`): add tasks for new or changed requirements and for each "change the code" decision; mark obsolete tasks `cancelled`; add a rework task for a `done` task whose requirement changed. Do not flip a `done` task back to `todo`. Add a line to the change log.
5. If a managed block exists in `CLAUDE.md`, refresh only the version numbers inside the markers.

## 6. Hand-off

Tell the user in a few lines: how many documents were stale, what changed, which documents are now `in-review`, and any decision left open. Recommend `/blueprint:review` for the changed documents, then re-run `/blueprint:plan` if they want to confirm the gate passes. Remind them that code changes decided here are tasks, to be done under the usual rules.
