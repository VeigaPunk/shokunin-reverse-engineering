# R45W1RegR44C1Counter — registry row for `tools/round-44/c1-counter.py`

Seat `R45W1RegR44C1Counter`, round 45 wave 1, lane `kaidoku`. Freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec`. Read-only on the lane tree; every artifact is
under `.ufo/waves/round-45/w1/R45W1RegR44C1Counter/`.

## Deliverable

One paste-ready registry row, seven columns, first cell exactly
`` `tools/round-44/c1-counter.py` ``:

- `.ufo/waves/round-45/w1/R45W1RegR44C1Counter/row.txt` — the single line, no trailing
  newline, 1529 bytes, sha256 `2f2ea910c9c6cb86ea5b5ea389dd2cfa571821d21299a91cbcc6997efed0a931`.
- `.ufo/waves/round-45/w1/R45W1RegR44C1Counter/row.md` — same line plus per-column
  provenance, the landing constraints measured against the frozen R45-C2 counter, and the
  caveat that exit 1 is overloaded.
- `.ufo/waves/round-45/w1/R45W1RegR44C1Counter/receipt.md` — 16 exit-path probes, six
  identity checks, three R45-C2 landing simulations, each with argv, exit, stdout sha256 and
  UTC.

```text
| `tools/round-44/c1-counter.py` | gate — R44-C1 coverage: re-derives the four frozen unblob SquashFS v1/v2 carriers (layout, carve, oracle census, gap rule) and re-runs REA `extract-firmware` to compare the plus-extractor projection; `--dev-arm` is the positive control on captured or freshly run envelopes; `--verify-receipt` re-checks a receipt's own identity | `0` met — every carrier clause and binding true (`failing == []`, `bindings_false == []`); `1` not met — a named false clause or binding, a red selftest case, or a receipt whose `counter_sha256` does not describe its `counter`; `2` could-not-evaluate — unusable or absent `--root`/`--rev`/`--freeze`/`--pkg65`, `rerun_disabled` under `--no-rerun`, `rerun_env_error`, `frozen_path_changed`, unreadable receipt, or a failed self-stamp. Caveat: the selftest's start-up refusals (missing `xpin-attribute.mjs`, undiscoverable `--pkg65` or node, xpin mint failure) and any uncaught exception exit 1 with no JSON receipt, so a broken harness reads as "not met" | `python3 -I -B tools/round-44/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root>` — exit 0, `cases` 47, `failures` [] (2026-10-28) | `tools/round-44/carriers.json` (ids, paths, handler and sha256 pins for the four carriers, whose bytes live under `corpus/evidence/round-42/c2/fixtures/`) and `corpus/evidence/round-44/c1/` at the freeze; `FROZEN_PATHS`/`FROZEN_PREFIXES` in the counter | `--json-out` and `--work` only; selftest fixtures under `$HYAKU_SCRATCH/kaidoku-r44/counter` | kaidoku |
```

## Instrument identity

- blob at freeze and at HEAD: `9695d586b3b1a792f1ad15e8dc4b4f54b8fe1569` (identical; last
  commit touching the path is `c48f8a4b`, so the frozen bytes are what these probes ran).
- bytes: sha256 `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`.
- `EXPECTED_IDS = ('v1le','v1be','v2le','v2be')`; `carriers.json` maps them to
  `corpus/evidence/round-42/c2/fixtures/{v1-le,v1-be,v2-le,v2-be}--squashfs_v*.bin` with
  handlers `squashfs_v1`/`squashfs_v2`; `CLAUSES` has 22 entries, `BINDINGS` 12.

## Verification performed (all in `receipt.md`)

| claim in the row | evidence | exit |
|---|---|---|
| `--selftest` green, 47 cases, `failures []` | `--selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, stdout sha `fbe23fef…`; reproduced byte-identically on a second run | 0 |
| `0` means met | selftest `green` case + clean fixture | 0 |
| `1` means not met / red | 46 red selftest cases; thin and wrong-path mutations | 1 |
| `2` means could-not-evaluate | no-args, `--bogus`, `--no-rerun`, malformed `carriers.json`, unreadable receipt | 2 |
| `--verify-receipt` probe maps 0/1/2 | crafted receipt / wrong digest / missing file | 0, 1, 2 |
| row lands under the frozen R45-C2 counter | fixture `SKILL.md`, `--rev == --freeze` | 0 |

The row's first cell, cell count (7) and `exits_ok` tokens were checked by calling the
frozen counter's own `parse_rows`/`exits_ok`/`ROW_TOOL` on the line, not by eye.

## Findings

1. **No exit code outside `{0,1,2}`.** Across 16 probes (help, usage, unknown option, every
   mode, every guard) the observed set is exactly `{0,1,2}`. Signals are not modelled;
   `SIGINT` → 130 by CPython default was **not exercised**.
2. **Exit 1 is overloaded.** Four start-up refusals exit 1 with a bare stderr message, empty
   stdout and no JSON receipt, indistinguishable from "target not met": xpin missing (only
   from a relocated copy), `--pkg65` undiscoverable, xpin mint failure, and any uncaught
   exception (`--work /proc/self/nope` → `FileNotFoundError` traceback, measured). The module
   docstring promises `2 unevaluable (bad args, git/node failure, ...)` for that class, so the
   document and the code disagree. Scoring mode does honour the map, so the damage is confined
   to `--selftest`/`--dev-arm` harness failures. The row states the caveat in cells[2].
3. **First match wins.** `parse_rows` + `by_tool.setdefault` keep the first row per path;
   measured `dup_rows_for_path: 2`, `first_match_is_existing: True` on the live `SKILL.md`.
   **Land the row as a replacement of `SKILL.md:1636`, not as an addition** — an appended
   duplicate is dead data.
4. **R45-C2 already scores at HEAD.** `tools/round-45/c2-counter.py --root . --freeze f762b72`
   exits 1 at the freeze (`unregistered` = the six paths, sha `d6e202aa…`) and exits 0 at HEAD
   (`unregistered []`, `thin []`, `registry_rows 45`, sha `398b6dc6…`, UTC 2026-10-28T15:45:00Z),
   because `e715263c` landed the six rows. So this row is an **accuracy upgrade** of the
   incumbent, not a prerequisite for the predicate; landing it keeps exit 0 (fixture-proven).
   Its additions over the incumbent: named `rerun_disabled`/`rerun_env_error`/self-stamp/
   unreadable-receipt exit-2 causes, the exit-1 overloading caveat, and the fact that the
   carrier bytes are pinned by sha under `corpus/evidence/round-42/c2/fixtures/` rather than by
   a frozen path. Its "47 cases" claim is confirmed exactly.
5. **Carrier drift is a score failure, not an integrity refusal.** The four carrier `.bin`
   files are outside `FROZEN_PATHS` and `FROZEN_PREFIXES` (`tools/round-44/`,
   `corpus/evidence/round-44/oracle/`); they are bound only by the sha256 pins inside the
   frozen `carriers.json` (`carrier_pin_ok`, source line 2035, documented line 119). A commit
   that rewrites them therefore reads as exit 1 `carrier_pin_ok`, not exit 2
   `frozen_path_changed`. Source-derived, not executed end-to-end. Routing candidate for the
   freeze-integrity rule.
6. **The selftest is 46 negative controls and 1 positive.** `green_ok 1`, `red_ok 46`. A
   counter that always exited 1 would pass 46/47 — which is why `--dev-arm` exists. Calibration
   note: register the positive-control rate, not just `failures == []`.
7. **`--pkg65` auto-discovers.** From the repo root, `--selftest` with no `--pkg65` finds
   `rea-agents@6.5.0` in the npx cache and produces byte-identical stdout. The row still passes
   `--pkg65` explicitly so the command is reproducible without the cache layout.

## Files written

- `.ufo/waves/round-45/w1/R45W1RegR44C1Counter/row.txt` (paste line)
- `.ufo/waves/round-45/w1/R45W1RegR44C1Counter/row.md`
- `.ufo/waves/round-45/w1/R45W1RegR44C1Counter/receipt.md`
- `.ufo/waves/round-45/w1/R45W1RegR44C1Counter.md` (this report)

No lane-tree file was modified; `git status --porcelain` shows only untracked `.ufo/` wave
artifacts. No commit, stage, stash or jj command was run. No install or upgrade was made.

## Risks and blockers

- No blocker. The one row claim not exercised end-to-end is exit 2 `receipt_identity_failed`
  (requires a receipt that writes but re-reads as mismatched); it is source-only
  (`main()` after `write_receipt`) and is named as such.
- If the L1 lands this row *in addition to* the incumbent, the incumbent stays in force and
  the upgrade is invisible to the counter (finding 3).
