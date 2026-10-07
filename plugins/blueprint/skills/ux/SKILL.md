---
name: ux
description: Design the user experience from an approved PRD - screen inventory, navigation map, user flows measured against tap and time budgets, wireframes with all states, and a clickable HTML prototype with a built-in tap counter. Use after the PRD is written, when the user wants UI/UX design, screens, flows, wireframes, or a prototype before coding.
argument-hint: "[platform: web | mobile | desktop] [journey to focus on]"
---

# UX

Design how the product feels to use, and prove it against the PRD's usability targets before any code exists. The output is a design document and a prototype the user can click through, with a counter that measures taps and seconds per journey.

Arguments: $ARGUMENTS

## 1. Preconditions

1. Read `docs/prd.md`. If it is missing, tell the user to run `/blueprint:prd` first and stop.
2. Check its header. If `status` is not `approved`, say so and ask whether to continue; if yes, note it in the UX document so the dependency is visible. Never silently build on an unreviewed PRD.
3. Read the PRD's journeys (J-), UX requirements (UX-), and the MUST functional requirements. Read `docs/discovery.md` for the user's own words about what felt heavy.
4. If `docs/ux.md` exists, read it and update in place. Keep screen IDs stable.
5. Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/ux.md`.

## 2. Agree the ground rules (short conversation)

Ask in one batch, with your recommendation for each:

1. **Platform**: web, mobile, desktop, or a mix. Which is primary?
2. **Navigation style** you want to start from (bottom tabs, sidebar, single flow, command palette) and any product the user likes or dislikes.
3. **Visual direction** in a few words, only as far as it affects layout. Colors and polish are not the goal here.
4. **Which journey matters most.** Design that one first and hardest.

If the user says "default", recommend and record the choice.

## 3. Design in this order

1. **Screen inventory.** List every screen with an ID (S-001, ...), its purpose, the requirement IDs it serves, how the user gets there, and its states (populated, empty, loading, error, first-time). Challenge any screen that serves no requirement, and any MUST requirement with no screen.
2. **Navigation map.** A Mermaid diagram of how screens connect. State the rules: how many top-level destinations, maximum depth from home to any screen, where the primary action lives, and how the user always gets back.
3. **Journey flows.** For each PRD journey, draw the flow (Mermaid) and **count the steps**: every tap, selection, and required typed field is one step. Compare the count with the journey's budget and with the UX-xxx targets. If it is over budget, redesign it, not the budget. Typical fixes: remove a confirmation, default a field, merge two screens, move the action to where the user already is, make optional things optional. Record the final count and what you cut.
4. **Wireframes.** One ASCII wireframe per screen, in a code block, with the content that matters and every state noted. Wireframes show layout and hierarchy, not styling.
5. **Interaction and content rules.** Validation behavior, empty-state copy, error messages (what happened, what to do), destructive actions, undo, keyboard and accessibility basics, and any rule the developers need so they do not have to guess.
6. **Prototype.** See section 4.
7. **Coverage.** Fill the table that maps each UX-xxx and each MUST FR-xxx to the screens that satisfy it.

Keep the design as light as the targets require. Every extra screen, setting, and option is a cost for the user and something the owner must later understand and debug. Say so when you cut something.

## 4. Build the prototype

1. Copy `${CLAUDE_PLUGIN_ROOT}/templates/prototype.html` to `docs/prototype/index.html`. It is self-contained (no installs, no network) and has a device frame, state switcher, journey launcher, and a counter that records taps and seconds against each journey's budget.
2. Edit only the marked section: fill in `JOURNEYS` (id, name, tap budget from the PRD, start screen, end screen) and `SCREENS` (one entry per screen in the inventory, with all of its states). Use plain HTML and the provided classes. Elements the user can tap carry `data-go="<screen-id>"` to navigate or `data-tap` to count a tap without navigating. Use mock data only.
3. Build the core journey screens first and make them work end to end. Other screens can be simple placeholders marked as such.
4. Tell the user how to open it on Windows: `start docs\prototype\index.html` in CMD. Walk them through running the core journey with the counter: choose the journey, press Start, perform it as a first-time user would, and read the result.
5. Ask them to try the journey, and to switch the state selector through empty, loading, and error. Record their reaction and the measured taps and seconds in the UX document. If a journey fails its budget or feels heavy, change the design and the prototype, and measure again.

## 5. Write the document

Write `docs/ux.md` from the template with `status: in-review`, today's date, and `based_on: [prd@<current PRD version>]`. A new document is `version: 0.1`; when updating one, bump the version. Include the measured prototype results. Never set `status: approved`; that is the review skill's job after the user signs off.

Finish with a short summary: screens count, journeys against budget (passes and any that fail), what you cut and why, open questions. Recommend `/blueprint:design` next, or `/blueprint:review docs/ux.md` first.
