---
doc: testplan
product: <product name>
status: draft            # draft | in-review | approved
version: 0.1
updated: <YYYY-MM-DD>
approved_by:
approved_on:
based_on: [prd@0.0, ux@0.0, hld@0.0, lld@0.0]      # upstream documents and the versions this was written against
---

# Test Plan: <product name>

## 1. Approach
Levels (unit, API, UI, end to end), how usability is measured, and what is out of scope.

## 2. Environments and test data
| Environment | Purpose | Data |
|---|---|---|

## 3. Test cases
Type: A acceptance, N negative or edge, C API contract, U usability, X non-functional, D debuggability, R regression.

| ID | Covers | Type | Pri | Given | When | Then | Data |
|---|---|---|---|---|---|---|---|
| T-001 | FR-001 | A | P1 | | | | |
| T-002 | FR-001 | N | P1 | | | | |
| T-003 | UX-001 | U | P1 | the prototype or app on a fresh account | the user creates a routine from the home screen | it takes at most 4 taps and 30 seconds | |
| T-004 | API-001, E-001 | C | P1 | | | | |
| T-005 | NFR-004 | D | P1 | a forced failure in module M-001 | the user triggers journey step 2 | the user sees message E-001 and the log shows E-001 with the correlation ID and module | |

## 4. Coverage matrix
| Requirement | Priority | Cases | Gap? |
|---|---|---|---|
| FR-001 | MUST | T-001, T-002 | no |
| UX-001 | MUST | T-003 | no |

Rule: every MUST has an acceptance case and a negative case. Every UX and NFR requirement has a measuring case.

## 5. Build order
The cases to implement first (the happy path of the core journey), then the rest by priority.

## 6. Exit criteria
- All P1 cases pass.
- No open blocker or major defect.
- Every UX measure is within target.
- Every gap in the coverage matrix is closed or accepted in writing.

## 7. Open questions and untestable requirements
