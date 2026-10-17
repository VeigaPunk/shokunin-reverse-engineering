## CLAIM
Parent-ready convergence diff for item 1 (r1-asar framing, `corpus/knowledge/2026-10-13-asar-surface.md:14-16`): clause-by-clause comparison of Lane A V1/D1 with Lane B VB1/DB1, plus one recommended append-only erratum text.

## METHOD
Primary sources read first (`asar-surface.md`; `r2-asar-deep-obsidian.md:23-29`; `r3-renderer-asar.md:31-37,79-85,107`; r4 `B1.md`/`V01a.md`); independent draft before reading V1/D1 and VB1/DB1. Read-only, no probes. Boundary at HEAD `cfc84c2`: 91 lines / 11,100 B, clean, trailing LF.

## FINDINGS
- **Agree — clauses 1/3/4/6:** append after :91, retain :14-16 and :80-91 byte-intact, no README map edit (V01a WONTFIX); :14-15 launcher observation stands, corrected only for "renderer payload" understating `obsidian.asar` (45 literal `ipcMain` ops = 44 `on` + 1 `handle("register-cli")`; renderer code; absent `index.js` → payload, not launchable). Facts re-verified against r2 :23-29 and r3 :31-37,79-85,107.
- **Disagree — clause 2 (heading):** V1 "round 5" and D1 "round 5, 2026-10-16" collide with six existing 2026-10-13 "round 5 audit" errata (e.g. `2026-10-13-r4u-04-dnfile-il.md:177`); adopt VB1/DB1's (and G1's collision-free) `luna-round-5, 2026-10-16, append-only`.
- **Minor — clause 5 (citations):** only VB1/DB1 keep the P0-named r3 :107; nit — "3 HTML entrypoints" sits at r3 :81, outside :31-37. Clause 7: keep map/README talk out of the erratum (D1 has it in-text); record "no README row changed" in the round record.
- X1 census tokens (`app, asar, obsidian, main, js, renderer, 45, ipc`) and pure-prefix append both hold for the text below.

**Recommended final text** (= DB1.md:11-28, verbatim):

```markdown
## Errata (luna-round-5, 2026-10-16, append-only)

- **Role clarification — obsidian.asar is not renderer-only; app.asar is
  its launcher.** The :14-15 observation above stands (`/usr/bin/obsidian`
  execs electron against `app.asar`, the main-process entry; `obsidian.asar`
  is its sibling resource). But "the renderer payload" understates
  `obsidian.asar`: the outer `app.asar` is functionally a thin launcher —
  statically it registers no Obsidian IPC, only `@electron/remote` internals
  (2 literal + 13 dynamic operations;
  `knowledge/2026-10-13-r2-asar-deep-obsidian.md:23-29`) — while the 25 MB
  `obsidian.asar` is the real application: its `main.js` holds 45 literal
  `ipcMain` operations (44 `on` + 1 `handle("register-cli")`) alongside the
  renderer code (`app.js` 64 `ipcRenderer` refs, 3 HTML entrypoints;
  `knowledge/2026-10-13-r3-renderer-asar.md:31-37`). Not separately
  launchable: `main: index.js` is absent, so the launcher loads it by path —
  "a payload, not a launchable package"
  (`knowledge/2026-10-13-r3-renderer-asar.md:79-85`); its summary (`:107`):
  `app.asar` is "only its launcher".
```

## THREATS
Textual only; counts as recorded in r2/r3, not live-reprobed. Heading must match the parent's final round title (DB1's caveat); a renumber changes only the heading, not the body.

## VERDICT
FINDING: adopt the Lane B block above with the `luna-round-5` heading — Lane A's "round 5" numbering collision is the only material divergence.
