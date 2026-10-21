# PrimaryRizin — Rizin book debugger intro, dynamic-debugger boundary (round 22, w2)

Seat: `KaidokuR22R.PrimaryRizin-6` (scout, leaf). Author-side evidence only; not outside admission.
Scope: bounded primary-source support for the dynamic debugger boundary relative to
`PROVINCE.md` and `.ufo/waves/round-22/claims.json` (baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`).
Accessed 2026-10-21 ~13:02–13:05 UTC. No installs, no target execution, no debug attach,
no account/config inspection. Machine-readable twin: `PrimaryRizin.json`.

## Verdict

- **Assigned URL inaccessible.** `https://book.rizin.re/debugger/intro.html` → HTTP **404**
  (GitHub Pages "Page not found", 9379 bytes, sha256 `b6205073…0fb0368`).
  Per the contract, **no registry row is drafted** for this source.
- **Relocated page exists** (observation, not a substitute admission):
  `https://book.rizin.re/src/debugger/intro.html` → HTTP 200, linked from the book root as
  `./src/debugger/intro.html`. Its text matches upstream `rizinorg/book` `src/debugger/intro.md`
  at master = `c87ed6599b86ccfb8e1de5f39eb3dcec2c407b8b`. Whether to re-target a row to this URL
  is L1's decision; this seat does not draft one.

## Passage (from the relocated page; ≤25 words, contiguous, 19 words)

> "Debuggers are implemented as IO plugins. Therefore, rizin can handle different URI types for spawning, attaching and controlling processes."

- Heading: rendered `63 Debugger` (Quarto chapter numbering); source heading `# Debugger`
  (`src/debugger/intro.md:1`); passage at source lines 3–4 (reflowed across two lines).
- Dates: page carries no on-page date. HTTP `Last-Modified: Sun, 19 Jul 2026 02:46:32 GMT`
  (site deploy). Latest commit on the file: `c87ed65` 2026-06-19T06:31:21Z ("Update Remote access
  codes and help manual"), which changed only the `R! help` block, not this passage. Commit
  `5398cf7` 2024-12-04T03:50:25Z reflowed the passage with identical wording; the original
  authoring date of the wording is earlier and is not pinned.
- Identities: page sha256 `54da021a9af57ab637f88c6e8908f1e03cc0ca3ba572e831cbf614ff0ead33e4`
  (91140 bytes, ETag `"6a5c3a88-16404"`); source md sha256
  `c9c94b39b6ba5a6d07e2dea6234c89d9ef639cd61a926b608892417f6149a5a1` (3588 bytes; master == c87ed65, `cmp` equal).

## What the passage supports (bounded)

1. **Observed:** Rizin's debugger is an IO-plugin layer for *spawning, attaching and controlling
   processes*. The same page shows `rizin -d /bin/ls` and the `debug` plugin `dbg:///bin/ls, dbg://1388`.
   So in Rizin's own documentation, debugger use is process-creating/attaching (dynamic) ground.
   That is distinct from the static `execute-rizin-command` surface PROVINCE holds
   (`rizin -N -q -c <cmd> <path>`, Round-20 Core row).
2. **Relative to claims.json:** this supports keeping R22-C1's T1 verb `debug-with-rizin` unclaimed
   absent a separate demonstration. It also supports `not_claimed: "dynamic-analysis ownership (kaidoku/revenger overlap stays open)"`,
   and it fits PROVINCE `Adjacent → Non-REA dynamic analysis` and the closing sentence that "the
   remaining T1 debugger/signal verbs stay unclaimed unless separately demonstrated". Exercising
   the verb would mean spawning or attaching to a process, which the wave contract forbids
   ("No target execution/debug attach").

## Corroborating local source (own read, not the book)

REA `rea-agents@6.5.0` installed source,
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rizin/RizinDebugSessionManager.js:207-219`:
the debug session argv is `-N -0 -d -R stdout=<tty> -R stderr=<tty> -e dbg.exitkills=false [-D <backend>] <resolvedPath>`,
spawned via `#spawnProcess`. `cliCommandNames.js:58,178` maps `debug-with-rizin` → `rizin_debug_command`.
Read by text grep only. No LSP server answers the bundled `dist/*.js`, so this is literal, not semantic, proof.
The source was read, not executed.

## Unsupported inferences (explicitly NOT established)

- The book says nothing about REA, its argv, `-N`, `-0`, `dbg.exitkills`, or `-R` TTY redirection.
  The link between the passage and REA's `debug-with-rizin` comes from the REA source read above, not from the book.
- "Spawning" does not, by itself, say that every `-d` open *executes target code before the first command*.
  Rizin's exact spawn/stop-at-entry semantics are not stated on this page.
- The page states no security property. "Dynamic = unsafe" or "static info commands are safe" is
  lane policy, not book content.
- Host `rizin 0.8.2 @ linux-x86-64` (`rizin -v`, exit 0). The book is unversioned master, so nothing
  ties the page's behavior or help output to 0.8.2.
- The page does not establish province ownership, revenger overlap, or whether a debugger verb is
  "frontier" vs "adjacent". Those placements remain L1 judgments.
- Nothing here counts toward R22-C1 `t1_exercised_count` (no executed, retained REA Evidence) or
  R22-C2 (debugger verbs are not in the T2 list).

## Commands and observed exits

| # | argv (abridged) | exit | observed |
|---|---|---|---|
| 1 | `curl -sS -L -o rizin_dbg_intro.html -D … https://book.rizin.re/debugger/intro.html` | 0 | HTTP 404, GitHub Pages, 9379 B, `date: Wed, 21 Oct 2026 13:02:55 GMT` |
| 2 | `curl … -w http_code` on `/`, `/debugger/`, `/src/debugger/intro.html`, `/debugger/intro.md`, `/print.html` | 0 each | 200, 404, 200, 404, 404 |
| 3 | `curl -sS -L -o rizin_src_dbg_intro.html -D … https://book.rizin.re/src/debugger/intro.html` | 0 | HTTP 200, 91140 B, Last-Modified 2026-07-19T02:46:32Z |
| 4 | `curl https://book.rizin.re/` + grep `debugger/intro` | 0 | `href="./src/debugger/intro.html"` |
| 5 | `curl 'https://api.github.com/repos/rizinorg/book/commits?path=src/debugger/intro.md&per_page=3'` | 0 | HTTP 200; c87ed65 2026-06-19, 5398cf7 2024-12-04, 087722b 2021-09-30 |
| 6 | `curl https://raw.githubusercontent.com/rizinorg/book/c87ed65…/src/debugger/intro.md`; same at `master`; `cmp` | 0 | 200/200, files identical, 3588 B |
| 7 | `curl https://api.github.com/repos/rizinorg/book/commits/{c87ed65,5398cf7}` (patch filter) | 0 | c87ed65 touched only the `R! help` block; 5398cf7 reflowed the passage, wording unchanged |
| 8 | `rizin -v` | 0 | `rizin 0.8.2 @ linux-x86-64` |
| 9 | Grep/Read of REA 6.5.0 `dist/rizin/RizinDebugSessionManager.js`, `dist/cliCommandNames.js` | n/a | argv quoted above |

stderr was empty for all curl calls. Fetched bytes stayed in `/tmp` (not retained in the lane).
Only their sha256 values are recorded here.

## Blockers / remaining unknowns

- **Blocker for the assigned task:** the assigned URL returns 404, so no registry row is drafted.
- Unknown: when `/debugger/intro.html` stopped resolving. The site moved to a Quarto `src/` layout;
  the move date is not pinned, and no archive service was queried.
- Unknown: the original authoring date of the quoted wording (it predates 2024-12-04).
- Tooling: no install or update was performed. No pacman transaction. `RULES.md` was not read
  because no install was attempted.
