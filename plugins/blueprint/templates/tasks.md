---
doc: tasks
product: <product name>
status: draft            # draft | in-review | approved
version: 0.1
updated: <YYYY-MM-DD>
approved_by:
approved_on:
based_on: [prd@0.0, ux@0.0, hld@0.0, lld@0.0, testplan@0.0]
gate: pass               # pass | override
gate_override_reason:
---

# Build Plan: <product name>

> **Build risk** (only when the gate was overridden): list the unapproved or stale documents here.

## 1. How to use this plan
Work top to bottom. Take the next task whose dependencies are done. Each task is finished when its tests pass, it cites its requirement IDs, and any document it changes is updated. Tick the status as you go.

Sizes: S about half a day, M about a day. Nothing larger.

## 2. Milestones
| ID | Milestone | Ends with | Demo |
|---|---|---|---|
| M1 | Walking skeleton | The core journey works end to end on the happy path | |
| M2 | | | |

## 3. Tasks
Status: `todo`, `doing`, `done`, `cancelled`.

### M0 Foundations
| ID | Task | Covers | Implements | Paths | Depends | Tests | Size | Status |
|---|---|---|---|---|---|---|---|---|
| TASK-001 | Project setup, config, test runner | enabler | M-001 | | | | S | todo |
| TASK-002 | Structured logging with correlation ID, error catalog skeleton, health check | NFR-004 | M-001 | | TASK-001 | | M | todo |

### M1 Walking skeleton
| ID | Task | Covers | Implements | Paths | Depends | Tests | Size | Status |
|---|---|---|---|---|---|---|---|---|

### M2 ...
| ID | Task | Covers | Implements | Paths | Depends | Tests | Size | Status |
|---|---|---|---|---|---|---|---|---|

## 4. Definition of done (every task)
- The tests listed for the task pass.
- Requirement or task IDs are cited in the commit message and in code comments where they drive the code.
- Failure paths log their error code and correlation ID.
- Any document whose described behavior changed is updated in the same change.
- The task is ticked here.

## 5. Traceability
| Requirement | Priority | Tasks | Tests | Gap? |
|---|---|---|---|---|
| FR-001 | MUST | | | |

Enablers (tasks that serve no single requirement) and why:

## 6. Issues found while planning
Defects or ambiguities found in approved documents. Fix through the owning skill, then `/blueprint:review`.

## 7. Change log
| Date | Change | Source |
|---|---|---|
