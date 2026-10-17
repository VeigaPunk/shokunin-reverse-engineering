## CLAIM
Lane B 2nd opinion: independently adjudicate the r1-asar framing debt (`corpus/knowledge/2026-10-13-asar-surface.md:14-16`) against r2-asar-deep-obsidian / r3-renderer-asar / r3-typora-signal; propose the append-only erratum.

## METHOD
Read-only, corpus-textual. Sources: `asar-surface.md:14-19,80-91`; `r2-asar-deep-obsidian.md:23-29`; `r3-renderer-asar.md:31-37,79-85,107`; `r3-typora-signal.md:7-13,83-87`; debt record `.ufo/waves/luna-round-4/B1.md:9`; map row `corpus/README.md:23`. No live REA/MCP/network. Command A at HEAD (SCORECARD.md:92-123, `git show` only): `mapped 72, missing [], dangling [], coverage 10.0, depth 10.0, 9/9`. Lane A `V1.md`/`D1.md` not opened before drafting.

## FINDINGS
- **Debt confirmed, narrow.** r1:14-15 calls `obsidian.asar` a sibling holding "the renderer payload". r3:31-37 counts 45 literal `ipcMain` ops in its `main.js` (44 `on` + 1 `handle("register-cli")`) — "the 'renderer asar' label understates it" (:37) — plus renderer code (`app.js` 64 `ipcRenderer` refs). r2:23-29: outer `app.asar` registers zero Obsidian IPC, only `@electron/remote` internals. r3:79-85: `main: index.js` absent → payload, not launchable package (r3:107: `app.asar` "only its launcher").
- **Main-process half stands.** `app.asar` remains the Electron main-process entry (`/usr/bin/obsidian` execs electron against it; package `main: main.js`); the correction is functional, not a negation. Preserve history + attribution (B1:9).
- **r3-typora-signal:** no contradiction; corroborates the loader-vs-payload pattern (1,383 B loader; 99.38% opaque `.jsc`); its census errata (:83-87) already reflected in summary :78; nothing further owed.
- **Map aligned:** `corpus/README.md:23` reads "app.asar (launcher) + obsidian.asar (real app: 45 ipcMain ops)"; B1's WONTFIX stands.
- **Proposed append:**
```
## Errata (luna-round-5, 2026-10-16, append-only)

- **Role clarification — obsidian.asar is not renderer-only; app.asar is its
  launcher.** The :14-15 observation stands (`/usr/bin/obsidian` execs electron
  against `app.asar`, the main-process entry; `obsidian.asar` its sibling
  resource). But "the renderer payload" understates `obsidian.asar`: the outer
  `app.asar` is functionally a thin launcher — statically it registers no
  Obsidian IPC, only `@electron/remote` internals (2 literal + 13 dynamic
  operations; `2026-10-13-r2-asar-deep-obsidian.md:23-29`) — while the 25 MB
  `obsidian.asar` is the real application: its `main.js` holds 45 literal
  `ipcMain` operations (44 `on` + 1 `handle("register-cli")`) alongside the
  renderer code (`app.js` 64 `ipcRenderer` refs, 3 HTML entrypoints;
  `2026-10-13-r3-renderer-asar.md:31-37`). Not separately launchable:
  `main: index.js` is absent, so the launcher loads it by path — "a payload,
  not a launchable package" (`r3-renderer-asar.md:79-85`); r3:107: `app.asar`
  is "only its launcher".
```

## THREATS
Corpus-textual only; no artifact re-probed, counts as recorded in r2/r3. A registry grep incidentally surfaced Lane A V1/D1 fragments; neither was deliberately read. Erratum is a proposal; the integrator owns the append.

## VERDICT
FINDING: framing debt real and narrow — append the role clarification (obsidian.asar is not renderer-only: 45 ipcMain ops, r3:31-37), keeping the launcher/main-entry observation.
