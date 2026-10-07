---
name: map
description: Reverse-engineer an existing codebase into a navigable map (docs/codebase-map.md) - architecture, modules, entry points, data stores, APIs, configuration, how to run and test it, a feature-to-code map, and a "where to look when X breaks" guide. Use when the user cannot navigate or understand their own code, is taking over a codebase, wants to document what exists, or before redesigning an existing app.
argument-hint: "[folder or area to map] [--refresh]"
---

# Map

Explain an existing codebase to its owner, accurately and in layers, so they can navigate it and debug it. Every statement in the map must come from reading the code, and every claim cites a path. This skill does not change the code.

Arguments: $ARGUMENTS

## 1. Scope and set-up

1. Find the project root. If the arguments name a folder or area, map only that; otherwise map the whole repository. For a large repository, say how big it looks and propose a scope (for example "backend first"), then confirm with the user in one question.
2. If `docs/codebase-map.md` exists, read it. With `--refresh`, or when its recorded `commit` differs from the current git HEAD, update only the parts that changed: use `git diff --stat <recorded commit>` and `git log` to find them, and leave the rest untouched. Otherwise ask whether to refresh or rebuild.
3. Read the template `${CLAUDE_PLUGIN_ROOT}/templates/codebase-map.md`.
4. Skip dependency and build folders (`node_modules`, `dist`, `build`, `.venv`, `__pycache__`, `.git`, and similar). **Never read or copy secret values.** For `.env` files and configuration, record variable names only.

## 2. Investigate in layers

Work from the outside in. Delegate broad sweeps to the Explore subagent, and read the important files yourself rather than trusting a summary.

1. **Inventory.** Languages, frameworks, package manifests, scripts, and how to install, run, build, and test. Take the commands from `package.json`, `Makefile`, `pyproject.toml`, `README`, CI files, and similar.
2. **Entry points.** Where execution starts: server start, CLI, routes, UI root, scheduled jobs, message consumers.
3. **Structure.** The folder tree with the purpose of each top-level folder, and the modules inside.
4. **Dependencies between modules.** Which module calls which. Look for circular dependencies and for modules everything depends on.
5. **Data.** Databases, collections or tables, schemas (from models, migrations, or queries), and caches or files.
6. **Interfaces.** Routes and API endpoints, events, and external services the code calls, with the files that handle them.
7. **Configuration.** Environment variables and settings (names, purpose, default), never values.
8. **Cross-cutting behavior as it actually is.** How errors are handled, how and where logging happens, authentication, validation, retries.
9. **Tests.** What exists, how to run it, and what is not covered.
10. **Hotspots.** Very large files, duplicated logic, dead code candidates, circular dependencies, a high count of TODO or FIXME comments, and anything that looks fragile. Report evidence, not opinions.
11. **Main features.** Pick the five or so most important features or journeys, and trace each through the code from the user's action to the data, naming the files and functions on the path.

## 3. Rules for accuracy

- Cite a path for every claim. Use `path/to/file.ext:line` for specific functions when helpful.
- If you could not verify something, mark it `[UNVERIFIED]` and say what would confirm it. Do not guess how code behaves.
- Separate **what the code does** from **what it seems intended to do**. If they differ, say so.
- Put questions only the owner can answer in the "Questions for the owner" section.
- Keep it as short as the repository allows. A map nobody reads is worthless.

## 4. Write the map

Write `docs/codebase-map.md` from the template as you go (structure first, then modules, then the deep dives), so progress is saved if the session ends. It must contain:

- A **plain-language walkthrough**: what the application does and how a request travels through it, in a page or less, written for someone who has forgotten the code.
- The architecture and module diagrams (Mermaid).
- The **feature-to-code map** and the **"where to look when X breaks"** table, built from the traced journeys and the real error handling and logging.
- How to run, test, and debug it, with commands in **Windows CMD** syntax where the project runs on Windows, and the commands the project's own scripts define.
- The hotspots and the unverified items.

Set the header `status: draft`, `version`, today's date, `commit` (the current git HEAD short hash, or `none`), and `scope`.

## 5. Hand-off

Tell the user in a few lines: what the application turned out to be, the three things most worth knowing before changing it, the biggest hotspots, and the questions only they can answer. Then suggest the next step: `/blueprint:discover` for a redesign or new feature (it reads the map first), or `/blueprint:design` to design a change as a delta. Map does not require approval, but if the user wants the map to be a trusted reference, suggest they read it and run `/blueprint:review docs/codebase-map.md`.
