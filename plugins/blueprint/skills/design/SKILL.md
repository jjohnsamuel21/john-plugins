---
name: design
description: Run an architecture discussion and then write the high-level design (docs/hld.md) and low-level design (docs/lld.md) - architecture decisions with trade-offs, code organization, data model, API contracts, sequence diagrams, error catalog, logging, and a "where to look when X breaks" playbook. Use after the PRD and UX design, when the user wants architecture, API or database design, or technical design before coding.
argument-hint: "[hld | lld | both] (default: both)"
---

# Design

Decide how the product will be built, with the user, before it is built. This is a conversation first and a document second: the user should end up understanding the system well enough to explain and debug it.

Arguments: $ARGUMENTS

## 1. Preconditions

1. Read `docs/prd.md`. If it is missing, tell the user to run `/blueprint:prd` first and stop. Read `docs/ux.md` and the prototype if they exist; if `docs/ux.md` is missing, ask whether to continue without it (design from the PRD alone) or to run `/blueprint:ux` first.
2. Check each document's `status`. If any is not `approved`, say which, and ask whether to continue. If yes, say so in the HLD summary so the dependency stays visible.
3. Read `docs/discovery.md` for constraints (stack, hosting, team, deadline).
4. If `docs/hld.md` or `docs/lld.md` exist, read them and update in place with stable IDs.
5. **Existing codebase:** read it before proposing anything. Use the Explore subagent for a broad sweep. Record what you found (entry points, main modules, data stores, how things are wired) and design as a **delta**: current state, target state, and the migration steps between them. Never design as if the code did not exist.
6. Read the templates `${CLAUDE_PLUGIN_ROOT}/templates/hld.md` and `${CLAUDE_PLUGIN_ROOT}/templates/lld.md`.

## 2. Architecture discussion (before any document)

Do not start writing yet. Take the key decisions one group at a time. For each decision, give **two or three options**, the trade-offs of each in a sentence or two, and your **recommendation with the reason**. Then let the user choose. Use AskUserQuestion for the choice when it is available.

Decision groups, in this order:

1. **System shape**: single deployable, modular monolith, or services. Match it to team size and how many people must understand the system. Prefer the fewest moving parts that meet the NFRs, and say so.
2. **Stack**: honor stated constraints and the existing codebase. Where the user has not decided, recommend and explain.
3. **Data**: store type, ownership, consistency, retention, and how data gets in and out.
4. **API style and auth**: how clients talk to the system, how users and services prove who they are.
5. **State, sync, offline**: where state lives, what happens with a bad connection.
6. **Integrations and background work**: external systems, queues, schedules, retries.
7. **Deployment and operations**: hosting, environments, configuration, secrets.
8. **Observability and debugging**: logs, correlation IDs, error reporting, health checks. This is a design decision, not an afterthought.
9. **Code organization** (see section 3).

Challenge choices that are heavier than the PRD needs. Ask what each component costs the owner to understand and operate. Record every decision as an ADR (ADR-001, ...) with the options considered and why.

## 3. Code organization (always decided, always written down)

Hard-to-navigate code is a design failure, so design for navigation:

- A **folder structure** with a one-line purpose for each top-level folder.
- **One feature, one place**: a rule for where the code for a feature lives, and which direction dependencies may point.
- A **feature map**: each FR-/UX- requirement mapped to the module and file paths that implement it. This is the table a new developer, or the owner in six months, reads first.
- **Naming and layering conventions** short enough to remember.

**Scope of the run:** with the argument `hld`, do sections 1 to 4 and stop. With `lld`, require an existing `docs/hld.md` (stop and say so if it is missing) and do sections 5 to 7. With `both` or no argument, do everything.

## 4. Write the HLD

`docs/hld.md`, from the template: context diagram, component diagram, data flow for the core journeys, ADRs, stack, deployment view, security, observability approach, how each NFR is met, risks, the code-organization section, and the feature map. Diagrams are Mermaid. Every element cites the requirement IDs it serves.

## 5. Write the LLD

`docs/lld.md`, from the template, for each module:

- **Data model**: entities, fields with types and constraints, indexes, relationships (Mermaid ER diagram), and migrations.
- **API contracts**: for each endpoint or message, method and path, auth, request and response shape, validation rules, every error it can return, and the requirement IDs it serves.
- **Sequence diagrams** for each core journey, from the user's action through the system and back.
- **State machines** for anything with a lifecycle.
- **Error catalog**: code, HTTP status or equivalent, user-facing message, cause, where it is logged, and what the user or operator should do.
- **Logging conventions**: levels, structured fields, a correlation ID on every request, and what must never be logged.
- **Configuration**: every setting and environment variable, default, and who sets it.
- **Debugging playbook**: a table of symptom, likely cause, where to look (file and log), and how to confirm. Write one row for every MUST journey step that can fail.
- **Delta and migration** (existing codebase): what changes, in what order, and how to roll back.

## 6. Self-check before showing it

1. Every MUST FR maps to a module, and to at least one endpoint or screen action.
2. Every endpoint and table cites at least one requirement; nothing exists "just in case".
3. Every screen in `docs/ux.md` has a data source in the API.
4. Every error code in the catalog is returned by at least one endpoint and appears in the playbook.
5. Every NFR is addressed by a stated mechanism, including debuggability and maintainability.
6. Diagrams and tables agree with each other.

## 7. Hand-off

Write both files with `status: in-review` and today's date. A new file is `version: 0.1` (bump it when updating one). Set `based_on` to the current versions of the documents each was written against: `prd` and `ux` for the HLD, and `prd`, `ux`, and `hld` for the LLD. Summarize in a few lines: the main decisions and what they cost, the riskiest part, and any open question. Recommend `/blueprint:testplan` next, then `/blueprint:review`. Never mark documents `approved`.
