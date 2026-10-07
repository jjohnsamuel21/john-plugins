---
name: review
description: Critically review the project's requirement and design documents in docs/ for gaps, contradictions, vague wording, and missing traceability, then record the user's sign-off by marking documents approved. Use after the PRD is written, before design or coding starts, or when the user asks to review any requirements or design document.
argument-hint: "[path to a document] (default: every document in docs/)"
---

# Review

Find what is wrong or missing in the documents before it becomes code, and give the user a clear approve or fix decision. The author of a document must not be its only reviewer, so the critique comes from a separate read-only reviewer.

Arguments: $ARGUMENTS

## 1. Choose what to review

- If a path is given, review that file. Otherwise list `docs/` and review every file that has a document header (`doc:` and `status:`): discovery, prd, and any others present, such as ux, hld, lld, or testplan.
- If nothing is found, say so and point the user to `/blueprint:discover`.

## 2. Get an independent critique

Delegate to the `reviewer` subagent (`blueprint:reviewer`) with the file paths and the checklist below. If the subagent is unavailable, run the checklist yourself and say that the review was not independent.

### Checklist

1. **Completeness**: every section of the document's template is filled in or deliberately marked not applicable.
2. **Vagueness**: words such as fast, easy, simple, intuitive, robust, scalable, flexible, user-friendly, seamless, or "etc." with no measure.
3. **Testability**: each functional requirement has a Given/When/Then acceptance criterion that someone could run.
4. **Contradictions**: requirements, scope, and non-goals that conflict with each other or with the discovery record.
5. **Scope discipline**: too many MUST items, items that appear in both scope and non-goals, features with no journey that needs them.
6. **Failure and edge cases**: empty states, errors, offline, permissions, first-time use, bad input.
7. **UX targets**: every UX requirement has a number, and the targets cover creating and navigating the core journeys.
8. **Debuggability and maintainability**: NFRs exist and are checkable.
9. **Traceability**: every requirement cites a source, every ID referenced exists, no ID is reused. In later documents: every design element, test, and task cites at least one requirement, and every MUST requirement is covered.
10. **Assumptions and open questions**: each assumption is marked and has someone or something that would confirm it, and no open question blocks a MUST requirement.
11. **Over-engineering**: anything the PRD does not require.
12. **UX document**: every journey has a counted step total within its budget; every screen serves a requirement and every MUST FR has a screen; every screen lists its states; prototype measurements are recorded and meet the targets.
13. **Design documents**: every MUST FR maps to a module and to an API or screen action; every endpoint and table cites a requirement; every error code in the catalog is returned somewhere and appears in the debugging playbook; a code-organization section with a feature map exists; each architecture decision records the options considered; the design is no heavier than the NFRs and team size justify.
14. **Test plan**: every MUST has an acceptance case and a negative case; every UX and NFR requirement has a measuring case; every error code has an API case; every Then is observable; exit criteria are stated.
15. **Staleness**: a document whose `based_on` lists an upstream version that no longer matches that document's current `version` is stale. For older documents with no `based_on`, compare `updated` dates. The gate script (`${CLAUDE_PLUGIN_ROOT}/scripts/check_approved.py`) reports this too. Flag it, say what to re-check, and recommend `/blueprint:sync`.
16. **Build plan** (`docs/tasks.md`): every MUST requirement is covered by a task, every task cites a requirement or is labeled an enabler with a reason, every task lists tests, no task is larger than a day, foundations and the walking skeleton come first, and the milestones are demonstrable.

## 3. Write the report

Create `docs/review-report.md` with:

- A one-paragraph verdict: ready to approve, approve after fixes, or needs rework.
- A findings table: ID (RV-001, ...), severity (**blocker**, **major**, **minor**), document, location, issue, suggested fix.
- A requirement coverage table: requirement ID against the screens (UX), modules and APIs (design), and test cases that cover it. Columns for documents that do not exist yet are marked "not yet written".

## 4. Walk the user through it

1. Present the blockers and majors first, with your suggested fix for each.
2. Ask which fixes to apply. Apply the agreed ones to the documents, keep IDs stable, and bump `version`.
3. If any substantive change was made, review the changed parts again.

## 5. Sign-off

Documents are approved in dependency order: PRD, then UX, then HLD and LLD, then test plan. If the user asks to approve a document whose upstream document is not approved, say so and recommend approving the upstream one first.

Only when the user clearly says they approve a specific document (not before, and never on your own initiative):

1. Set `status: approved`, `approved_by: <the user's name>`, `approved_on: <today>` in that document's header.
2. Record the requirement coverage in `docs/review-report.md`. Fill in the PRD's own Traceability table only when approving the PRD itself, and never edit an already-approved document just to update coverage.
3. Tell the user which documents are approved and which are not, and what the next step is.

If an approved document is changed later by anyone, set it back to `status: in-review` and say so. Approval always refers to a specific version.
