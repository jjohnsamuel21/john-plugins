---
doc: prd
product: <product name>
status: draft            # draft | in-review | approved
version: 0.1
updated: <YYYY-MM-DD>
approved_by:
approved_on:
based_on: [discovery@0.0]      # upstream documents and the versions this was written against
---

# PRD: <product name>

## 1. Overview
One paragraph: the problem, who has it, and what this product does about it.

## 2. Background and evidence
Why this is worth building. Reference discovery decisions as (D-xxx).

## 3. Users
| Persona | Goal | Context | Key frustration today |
|---|---|---|---|

## 4. Goals and success metrics
| ID | Goal | Metric | Baseline | Target | How measured |
|---|---|---|---|---|---|
| G-001 | | | | | |

## 5. Non-goals
Things this product will deliberately not do, each with a reason.

## 6. Scope
- **MVP:**
- **Later:**

## 7. User journeys
### J-1 <name>
Trigger, numbered steps, outcome, step or time budget. Each journey lists the requirement IDs it depends on.

## 8. Functional requirements
| ID | Requirement (one testable statement) | Priority | Acceptance criterion | Source |
|---|---|---|---|---|
| FR-001 | The system shall ... | MUST | Given ... when ... then ... | D-001 |

Priority: MUST (v1 fails without it), SHOULD (important, can slip), COULD (nice to have).

## 9. UX requirements
Every line carries a number.
| ID | Requirement | Measure | Target |
|---|---|---|---|
| UX-001 | Create a routine | taps / seconds from home screen | <= 4 taps, <= 30 s |

## 10. Non-functional requirements
| ID | Category | Requirement | Target |
|---|---|---|---|
| NFR-001 | Performance | | |
| NFR-002 | Security and privacy | | |
| NFR-003 | Reliability | | |
| NFR-004 | Debuggability | Every failure is traceable from user-visible symptom to log line | |
| NFR-005 | Maintainability | A new developer can locate the code for any feature from the docs | |
| NFR-006 | Accessibility | | |

## 11. Constraints and dependencies
Stack, hosting, integrations, deadlines, team.

## 12. Assumptions
Each marked `[ASSUMPTION]` with the person or event that would confirm it.

## 13. Risks and mitigations
| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|

## 14. Open questions
Anything unresolved. Nothing here may block a MUST requirement.

## 15. Glossary

## 16. Traceability
Filled in by the review skill. Maps each requirement to the design, test, and task that cover it.
| Requirement | Design | Test | Task |
|---|---|---|---|
