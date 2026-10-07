<!-- blueprint:start -->
## Requirements, design, and build plan (managed by Blueprint)

The approved documents in `docs/` are the source of truth for what to build.

| Document | Path | Version |
|---|---|---|
| Product requirements | docs/prd.md | <version> |
| UX design and prototype | docs/ux.md, docs/prototype/index.html | <version> |
| High-level design | docs/hld.md | <version> |
| Low-level design | docs/lld.md | <version> |
| Test plan | docs/testplan.md | <version> |
| Build plan | docs/tasks.md | <version> |

### How to work
1. Take the next task in `docs/tasks.md` whose dependencies are done. Work on one task at a time.
2. Read the requirements it covers (`FR-`, `UX-`, `NFR-` in docs/prd.md) and the matching sections of docs/ux.md, docs/hld.md, and docs/lld.md.
3. Write the test cases listed for the task (docs/testplan.md) before or together with the code.
4. Follow the folder structure, naming, and layering rules in docs/hld.md. Use its feature map to decide where code goes.
5. Use the error codes and logging conventions in docs/lld.md. Every failure path logs its error code and correlation ID.
6. Cite requirement and task IDs in commit messages, and in code comments where a requirement drives the code.
7. Do not build anything that no requirement covers and do not expand scope. If something is missing, ambiguous, or wrong in the documents, stop and ask. Do not guess.
8. If a change alters behavior described in docs/, update the document in the same change, or run `/blueprint:sync`.
9. When a task is done, tick it in docs/tasks.md.
<!-- blueprint:end -->
