# john-plugins

A Claude Code plugin marketplace. It currently lists one plugin.

| Plugin | What it does |
|---|---|
| [`blueprint`](plugins/blueprint) | From idea to build plan before any code is written: interview-driven discovery, PRD, UX design with a clickable prototype, HLD and LLD, test plan, independent review, an approval gate into an ordered build plan, codebase mapping, and document sync. |

## Install

Run these in your terminal (Windows CMD works):

```cmd
claude plugin marketplace add jjohnsamuel21/john-plugins
claude plugin install blueprint@john-plugins
```

Then start `claude` in any project and type `/blueprint:` to see the skills. Full usage, by scenario, is in [plugins/blueprint/GUIDE.md](plugins/blueprint/GUIDE.md).

Update to the latest release:

```cmd
claude plugin update blueprint@john-plugins
```

Requirement: Python 3.8 or newer for the approval-gate script (Claude falls back to reading document headers if Python is missing).

## Develop locally

Load the plugin from your checkout without installing it:

```cmd
cd C:\path\to\your\project
claude --plugin-dir C:\path\to\john-plugins\plugins\blueprint
```

After editing a plugin file, run `/reload-plugins` in the session. Validate before every commit:

```cmd
claude plugin validate .\plugins\blueprint --strict
claude plugin validate . --strict
```

## Repository layout

```
john-plugins\
├── .claude-plugin\marketplace.json    the catalog: lists each plugin and where it lives
├── plugins\
│   └── blueprint\
│       ├── .claude-plugin\plugin.json the plugin manifest (name, version)
│       ├── skills\                    discover, prd, ux, design, testplan, review, plan, map, sync
│       ├── agents\                    researcher and reviewer subagents
│       ├── templates\                 document templates, the prototype starter, the CLAUDE.md block
│       ├── scripts\check_approved.py  approval gate and document status report
│       └── GUIDE.md                   how to use it, scenario by scenario
└── README.md
```

## Releasing a new version

1. Change the plugin.
2. Bump `version` in `plugins/blueprint/.claude-plugin/plugin.json`. If you do not bump it, installed users will not receive the update.
3. Validate (see above), commit, and push.
4. Users run `claude plugin update blueprint@john-plugins`.

Do not rename a published plugin or the marketplace: installs are recorded under those names.

## License

MIT. See [LICENSE](LICENSE).

## Adding another plugin

Create `plugins/<new-name>/` with its own `.claude-plugin/plugin.json`, then add an entry to `.claude-plugin/marketplace.json` whose `name` is identical to the manifest `name`.
