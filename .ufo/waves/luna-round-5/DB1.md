## CLAIM
Draft deliverable for item 1: the exact append-only erratum block for `corpus/knowledge/2026-10-13-asar-surface.md:14-16`, sourced from `VB1.md` (2nd opinion; it landed 16:40 mid-run), plus its house-style reference. My independent primary-source draft, made before VB1.md appeared, reached the same disposition — the two converge.

## METHOD
Read-only: `VB1.md`; primary files `asar-surface.md:14-19,80-91`; `2026-10-13-r2-asar-deep-obsidian.md:23-29`; `2026-10-13-r3-renderer-asar.md:31-37,79-85,107`; house-style survey of errata headers/blocks. Boundary bytes re-measured: 91 lines, final byte `0a`. Invariant receipt read: `.ufo/waves/luna-round-5/receipts/census-pre.out` — command A unchanged (72/72, 9/9, cfc84c2). No probes/MCP/network; no tracked file touched.

## FINDINGS
Exact block — append after the final LF at `:91`; leave `:80-84` and `:85-91` byte-intact:

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

Edits vs VB1.md's verbatim proposal (format only, disclosed): `knowledge/` prefix added to two citations; `r3:107` shorthand expanded; "above" added at the :14-15 anchor. House-style reference: `corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md:114-119` (dated append-only errata; framing corrected while "historical run observations … remain true") + same-file header precedent `asar-surface.md:85`. Lane A convergence: `D1.md:11-13`, `V1.md:12-15`, `G1.md:33-44` propose the same correction; G1's header matches.

## THREATS
Textual only; counts are as recorded in r2/r3 (no live reprobe). VB1 logged incidental Lane A fragment exposure; I did too (localization greps) — both blocks stay anchored on r2/r3 citations. Header label "(luna-round-5, …)" must match the parent's final round title.

## VERDICT
CLEAN — exact erratum block + house-style reference delivered; converges with VB1 and Lane A item-1 seats; no tracked files touched.
