---
name: testplan
description: Write the test plan (docs/testplan.md) as Given/When/Then test cases mapped to requirement IDs - acceptance, negative, API contract, UI and usability, and non-functional cases including debuggability - with a coverage matrix and exit criteria. Use after the PRD and designs, before coding, or when the user asks for test cases.
argument-hint: "[feature or area to focus on]"
---

# Test plan

Define how every requirement will be proven, before the code exists. The result is a list of test cases a developer can implement and a reviewer can check against the requirements. This skill writes cases, not test code.

Arguments: $ARGUMENTS

## 1. Preconditions

1. Read `docs/prd.md`. If it is missing, tell the user to run `/blueprint:prd` first and stop.
2. Read `docs/ux.md`, `docs/hld.md`, and `docs/lld.md` when they exist. The more of them exist, the more specific the cases can be. If the LLD is missing, write the cases at requirement level and mark API-level cases as "pending LLD".
3. Note each document's `status`. If any is not `approved`, say so, ask whether to continue, and note the dependency in the test plan's approach section.
4. If `docs/testplan.md` exists, read it and update in place. Test IDs stay stable.
5. Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/testplan.md`.

## 2. Case types to write

For every requirement, write the cases that would convince a skeptical reviewer.

- **Acceptance (A)**: one or more cases per functional requirement, taken from its acceptance criterion and extended to the happy path with realistic data.
- **Negative and edge (N)**: invalid input, missing data, duplicates, permission problems, interrupted operations, empty and first-time states, limits. Every MUST FR gets at least one.
- **API contract (C)**: for each endpoint in the LLD, a success case and one case for every error code it can return. Check status, response shape, and validation rules.
- **UI and usability (U)**: for each UX requirement, a case that measures it with a number: taps, steps, seconds, or screens, using the prototype's counter or the real app. State the pass threshold from the PRD.
- **Non-functional (X)**: performance and load against the stated targets, security checks, reliability (restart, retry, offline), accessibility.
- **Debuggability (D)**: for the main failure points, a case that injects the failure and checks that the user sees the right message and that the log carries the error code, correlation ID, and module named in the LLD's debugging playbook. This keeps the system understandable when it breaks.
- **Regression (R)** (existing codebase): the existing behavior the redesign must not break, identified from discovery's "must not break" list.

## 3. Writing rules

- Format: `T-001`, with **Covers** (requirement IDs, plus API, screen, or error IDs), **Type**, **Priority**, **Given / When / Then**, and **Test data**.
- One behavior per case. Concrete values, not "valid input".
- Every Then is observable: a screen, a response, a database state, or a log line.
- Cases for MUST requirements are priority P1, SHOULD are P2, COULD are P3.
- If a requirement cannot be tested as written, do not invent a test. Raise it as an issue against the PRD and list it under open questions.

## 4. Coverage matrix and exit criteria

1. Build a matrix with one row per requirement ID (FR, UX, NFR) and the test IDs that cover it. Every MUST requirement must show at least one acceptance case and one negative case. Every UX and NFR requirement must show a measuring case.
2. List requirements with no cases as **gaps**, and fix them before finishing.
3. Define the **exit criteria** for release: all P1 cases pass, no open blocker defect, UX measures within target, and so on.
4. Add a short section on test data, environments, and the order cases should be built in (the happy path of the core journey first).

## 5. Hand-off

Write `docs/testplan.md` with `status: in-review` and today's date. A new file is `version: 0.1` (bump it when updating one). Set `based_on` to the current versions of `prd`, `ux`, `hld`, and `lld` (only those that exist). Summarize in a few lines: number of cases by type, coverage of MUST requirements, any gaps or untestable requirements. Recommend `/blueprint:review` next. Never set `status: approved`.
