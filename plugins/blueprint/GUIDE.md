# Blueprint: how to use it, scenario by scenario

Blueprint turns an idea into approved documents **before** any code is written, then into an ordered build plan. Claude interviews you, challenges the idea, writes the documents, and a separate reviewer checks them. You approve each document, a gate confirms everything is approved and current, and only then does building start. Later, it keeps the documents in step with the code.

**Version 0.3.0 (all three phases).** Nine skills: `discover`, `prd`, `ux`, `design`, `testplan`, `review`, `plan`, `map`, `sync`.

---

## 1. Install and load it (Windows CMD)

**Option 1: from your GitHub repository** (after you push it, see the repository README)

```cmd
claude plugin marketplace add <your-github-user>/john-plugins
claude plugin install blueprint@john-plugins
```

To get a new version later:

```cmd
claude plugin update blueprint@john-plugins
```

**Option 2: from a local folder, for one session** (best while you are still changing the plugin)

```cmd
cd C:\path\to\your\project
claude --plugin-dir C:\path\to\john-plugins\plugins\blueprint
```

After editing any plugin file, run `/reload-plugins` in the session.

**Check it loaded:** type `/blueprint:` and nine skills should appear. If they do not, run `/plugin`, open the **Errors** tab, and check the files from CMD:

```cmd
claude plugin validate C:\path\to\john-plugins\plugins\blueprint
```

**Python:** the gate (`plan`) and status check (`sync`) run a small script that needs Python 3.8 or newer. Check with `python --version` (or `py --version`). If neither works, Claude does the same check by reading the document headers, so nothing is skipped.

---

## 2. The skills at a glance

| Command | What it does | Writes |
|---|---|---|
| `/blueprint:discover [idea] [--lite]` | Interviews you, brainstorms, pushes back, researches competitors, keeps a decision log | `docs/discovery.md`, or `docs/features/<name>.md` in lite mode |
| `/blueprint:prd` | PRD with requirement IDs, acceptance criteria, measurable UX targets, non-goals | `docs/prd.md` |
| `/blueprint:ux [platform]` | Screens, navigation, journey flows counted against tap budgets, wireframes, **clickable HTML prototype** that measures taps and seconds | `docs/ux.md`, `docs/prototype/index.html` |
| `/blueprint:design [hld\|lld\|both]` | Architecture discussion with options and trade-offs, then HLD and LLD | `docs/hld.md`, `docs/lld.md` |
| `/blueprint:testplan` | Given/When/Then cases mapped to requirement IDs, coverage matrix, exit criteria | `docs/testplan.md` |
| `/blueprint:review [path]` | Independent critique, findings report, and your sign-off | `docs/review-report.md`, `status: approved` in headers |
| `/blueprint:plan` | **The gate.** Refuses unless all documents are approved and current. Then writes the ordered build plan and a managed index in `CLAUDE.md` | `docs/tasks.md`, `CLAUDE.md` |
| `/blueprint:map [area] [--refresh]` | Explains an existing codebase: architecture, modules, entry points, how to run it, a feature-to-code map, and "where to look when X breaks" | `docs/codebase-map.md` |
| `/blueprint:sync [docs\|code\|all]` | After a change: finds stale documents, shows the impact by requirement ID, detects drift between code and design, applies what you agree | `docs/sync-report.md`, updated documents |

### The order, and where you decide

```
discover -> prd -> review ->  ux -> review ->  design -> testplan -> review ->  plan (gate) -> build
   ^                                                                              |
   | map (if code exists)                                              sync <-----+ (when anything changes)
```

---

## 3. Scenario A: a brand-new product

1. Create an empty project folder, open CMD there, start Claude Code with the plugin.
2. `/blueprint:discover a habit tracker for new parents`. Answer in batches. Say **"default"** when you have no opinion and **"challenge me"** if you want more pushback. Let it research competitors when it offers.
3. When the readiness checklist is met: `/blueprint:prd`. Read `docs/prd.md` and answer its open questions.
4. `/blueprint:review`, fix the blockers, say **"approve the PRD"**.
5. `/blueprint:ux web`. Answer the short batch about platform and navigation, then try the prototype (section 5).
6. `/blueprint:review docs/ux.md`, approve.
7. `/blueprint:design`. A conversation first: Claude offers two or three options for each major decision with a recommendation, and you choose. Then it writes the HLD and LLD.
8. `/blueprint:testplan`.
9. `/blueprint:review` across everything, approve each document in order: PRD, UX, design, test plan.
10. `/blueprint:plan`. The gate checks every document. If it passes, you get `docs/tasks.md` and the `CLAUDE.md` index.
11. Tell Claude: "Implement TASK-001, following CLAUDE.md," and continue down the list.

---

## 4. Scenario B: a small feature in a codebase you already have

```
/blueprint:discover --lite add recurring reminders to routines
```

Claude reads your project first, asks at most two rounds of questions, and writes one file, `docs/features/<name>.md`: requirements, flow, API and data changes, failure cases, and test cases. Then:

```
/blueprint:review docs/features/<name>.md
/blueprint:plan docs/features/<name>.md
```

The gate checks that one document, and you get a short task list.

**Rule of thumb:** if you can describe the change in two sentences and it touches one area, use lite mode. If it needs a new screen flow, a new data model, or an integration, use the full flow.

---

## 5. How to use the prototype

One HTML file, no installs, no network.

```cmd
start docs\prototype\index.html
```

1. In the control panel pick a **journey** and press **Start journey**. Taps and seconds count from then.
2. Do the journey as a first-time user would. Every tap on a button, tab, or list item counts.
3. At the journey's end screen it shows **PASS or FAIL** against the budget from your PRD.
4. Switch **Screen state** (populated, empty, loading, error, first-time) to see every state of every screen.
5. Switch **Device** between phone and web.
6. **Copy results** copies the measured numbers. Claude records them in `docs/ux.md`.

If a journey fails, tell Claude what felt heavy. It cuts steps in the design and prototype, and you measure again. This is the loop that would have caught Planova's heavy navigation before any code existed.

---

## 6. Scenario C: an existing app that feels heavy or confusing (the Planova case)

1. Open Claude Code in the app's repository with the plugin loaded.
2. `/blueprint:map`. Claude reads the code and writes `docs/codebase-map.md`: a plain-language walkthrough of what the app does, folder and module structure, entry points, data, configuration (names only), how to run and test it, a feature-to-code map, "where to look when X breaks," and hotspots. Anything it could not verify is marked `[UNVERIFIED]`, and questions only you can answer are listed at the end. Read it and correct it.
3. `/blueprint:discover Planova redesign`. It uses the map instead of re-reading the code, and asks about the pain: where creating a routine or task is heavy, how many taps today, what you do when something breaks. It turns the vague complaint into numbers (for example "11 taps today, target 4").
4. `/blueprint:prd`, `/blueprint:review`.
5. `/blueprint:ux`. Measure the redesigned flow in the prototype against today's baseline before changing the app.
6. `/blueprint:design`. For existing code it designs a **delta**: current state, target state, migration steps, rollback. It always includes a folder structure, a feature map, an error catalog, and a debugging playbook.
7. `/blueprint:testplan` (it adds regression cases for what must not break), `/blueprint:review`, then `/blueprint:plan`.

To refresh the map after the code changes: `/blueprint:map --refresh`. It re-reads only what changed since the commit recorded in the map.

---

## 7. Scenario D: you stopped halfway

Run the same skill again in the same project. `/blueprint:discover` resumes from `docs/discovery.md`. The other skills read their existing document and update it in place with stable IDs. Nothing is lost when the terminal closes.

---

## 8. Scenario E: requirements changed after documents were written

1. Tell Claude the change and have it update `docs/prd.md`, or edit it yourself. The version number goes up and the status returns to `in-review`.
2. Run `/blueprint:sync docs`. It reports every document that is now stale, then shows an **impact table**: for each changed requirement ID, the screens, modules, APIs, tables, tests, and tasks that cite it.
3. Decide, finding by finding, then it updates the downstream documents in order (UX, design, test plan, tasks), keeps IDs stable, adds a rework task for anything already `done`, and moves changed documents back to `in-review`.
4. `/blueprint:review` the changed documents, approve, and run `/blueprint:plan` to confirm the gate passes again.

---

## 9. Scenario F: the code moved ahead of the documents

You changed code and the design documents no longer describe it. Run `/blueprint:sync code`. Claude compares routes against the API contracts, models and migrations against the data model, error codes against the error catalog, and the folder structure against the HLD and the codebase map. For each difference you choose:

- **Update the document** (the code is right),
- **Change the code** (it becomes a task, because sync never edits application code),
- **Ignore** (recorded as accepted drift).

If the drift means the product's behavior has changed, Claude asks whether that is intended before it touches the PRD. It never invents a requirement.

---

## 10. Scenario G: the gate

`/blueprint:plan` runs a check before anything else. It passes only when:

1. `prd`, `ux`, `hld`, `lld`, and `testplan` all exist,
2. every one is `approved`, and
3. none is **stale** (built on an older version of a document it depends on).

A failure looks like this:

```
Blueprint gate: docs (requires: prd, ux, hld, lld, testplan)
  document       status     version  notes
  prd            approved   0.4
  ux             in-review  0.1      STALE: built on prd@0.3 but prd is now 0.4
  hld            approved   0.1      approved, but upstream ux is in-review
  lld            -          -        missing
GATE FAILED
```

Claude explains each problem and what to run next, and stops. You can run the same check yourself, from your project folder:

```cmd
python C:\path\to\john-plugins\plugins\blueprint\scripts\check_approved.py
```

(`py` instead of `python` if that is how Python is installed. Add `--all` to also list the discovery, tasks, and codebase-map documents and any lite features.)

**Override.** The gate is a safeguard, not a lock. If you decide to start anyway, tell Claude to proceed and name what you are skipping. The plan records `gate: override` and the reason, and puts the unapproved documents in a visible "Build risk" box. Tasks built on unapproved documents may need rework.

---

## 11. Scenario H: partial flows

You do not have to run everything.

- **Only UX for an existing PRD:** `/blueprint:ux`. It needs `docs/prd.md` and warns if it is not approved.
- **Only technical design:** `/blueprint:design`. Without `docs/ux.md` it asks whether to design from the PRD alone.
- **Only the architecture discussion:** `/blueprint:design hld`.
- **Only test cases:** `/blueprint:testplan`. They are more specific when the LLD exists.
- **Only understand your code:** `/blueprint:map`.
- **Review a document you did not write:** `/blueprint:review docs\some-spec.md`. Use it on a teammate's spec before you agree to build it.

---

## 12. Scenario I: you only have a vague idea

Run `/blueprint:discover` with one sentence and say so: "I'm not sure what this is yet, help me find the real problem." Claude starts with the problem and evidence, asks for concrete examples, and offers research early. You can stop after the first few topics and take the notes away. The file stays `draft` until it reaches readiness.

---

## 13. Scenario J: working with a team

- Commit `docs/` to git. The documents are the shared source of truth.
- A teammate can be the approver: they run `/blueprint:review` and sign off, and their name goes in `approved_by`.
- Teammates install the plugin from your repository (section 1, option 1).
- `/blueprint:sync` works best in a git repository, because it can diff a document against its history to find exactly which requirement IDs changed.

---

## 14. How the coding agent uses the documents

`/blueprint:plan` adds a block to your project's `CLAUDE.md`, between `<!-- blueprint:start -->` and `<!-- blueprint:end -->` markers. Anything you wrote outside the markers is never touched. The block lists the approved documents and their versions and gives the coding agent these rules:

- Take the next task in `docs/tasks.md` whose dependencies are done, one at a time.
- Read the requirements the task covers and the matching UX, HLD, and LLD sections.
- Write the listed test cases with the code.
- Follow the folder structure and naming rules in the HLD, and use its feature map to decide where code goes.
- Use the error codes and logging conventions from the LLD, so every failure logs its code and a correlation ID.
- Cite requirement and task IDs in commits.
- Build nothing that no requirement covers. If something is missing, unclear, or wrong, stop and ask.
- Update the documents in the same change as any behavior change, or run `/blueprint:sync`.

---

## 15. Document headers: how status and staleness work

Every document starts with a small header:

```yaml
---
doc: ux
status: in-review          # draft | in-review | approved
version: 0.2
updated: 2026-10-07
based_on: [prd@0.4]        # upstream documents and the versions this was written against
---
```

- **status** moves `draft`, then `in-review` (when a skill writes it), then `approved` (only when you sign off through `/blueprint:review`). Changing an approved document sends it back to `in-review`.
- **version** goes up whenever the content changes. Approval does not change it.
- **based_on** records which version of each upstream document this one was written from. If the upstream document's version later differs, this document is **stale**. That is how the gate, `review`, and `sync` know what to re-check.
- Documents from earlier plugin versions may lack `based_on`. `sync` adds it when it updates them.

**IDs are permanent:** `FR-` functional, `UX-` usability, `NFR-` non-functional, `G-` goals, `J-` journeys, `D-` decisions, `S-` screens, `M-` modules, `ADR-` architecture decisions, `API-` endpoints, `E-` errors, `T-` tests, `TASK-` build tasks, `SY-` sync findings, `RV-` review findings. Documents cite them, so any screen, endpoint, test, or task traces back to why it exists.

---

## 16. Tips

- Short answers are fine. Claude asks follow-ups when they matter.
- Say "skip" for a question that does not apply and "default" when you have no preference.
- Ask Claude to explain a question if it is unclear. It should.
- If an answer changes something decided earlier, say so. It records the change in the decision log.
- Do not approve a document you have not read. Approval is the gate that stops weak requirements becoming weak software.
- In the design discussion, ask "what does this cost me to understand and debug later?" for any option. It is the question Planova needed.
- Run `/blueprint:sync` whenever you finish a batch of changes, not only when something breaks.

---

## 17. Troubleshooting

| Problem | Fix |
|---|---|
| `/blueprint:` shows nothing | Check `/plugin`, Errors tab. Run `claude plugin validate` on the plugin folder. |
| Edited a skill but nothing changed | Run `/reload-plugins`. |
| Claude skips the interview and writes the PRD | Run `/blueprint:discover` first. The PRD skill needs `docs/discovery.md`. |
| The prototype opens blank | Open the browser console (F12). A typo in the `JOURNEYS` or `SCREENS` section is the usual cause. Ask Claude to fix it. |
| A journey always fails its budget | That is the point. Tell Claude what felt heavy and ask it to cut steps, rather than raising the budget. |
| The gate says STALE | A document was written against an older upstream version. Run `/blueprint:sync docs`, review, and approve again. |
| The gate says "no valid header" | The document must start with a `---` block. Ask the owning skill to rewrite its header. |
| `python` is not recognized | Try `py`. If neither works, install Python 3.8+ or let Claude do the check by reading the headers. |
| `map` reports many `[UNVERIFIED]` items | Answer the "Questions for the owner" list and re-run `/blueprint:map --refresh`. |
| `sync` cannot tell what changed | Without git history it asks you to describe the change. Put `docs/` in git. |
| Claude does not push back enough | Say "challenge me harder", and name what to attack. |
| The interview feels too long | Use `--lite`, or say "default" for the remaining topics. |
| `claude plugin marketplace add` fails | Check the repository is pushed and opens in a browser. For a private repo, check your git credentials. |
