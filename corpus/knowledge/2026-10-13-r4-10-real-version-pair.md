<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/10-real-version-pair.md. -->

# 10 — Real cross-version binary compare: 1password-cli `op` 2.34.1 → 2.40.0 (41–43 MB Go ELF)

Lane: kaidoku-shokunin, round 4. Date: 2026-10-13. Host: Linux x86_64, node v24.21.0,
`npx -y rea-agents@6.4.0` (npx cache `dea9475797100b20`; domain modules imported from
`dist/domain/*` — the same code the MCP `compare_bundles` / `compare_functions` tools wrap).
Provider: Ghidra 12.1.4 headless (`-Xmx2G`). Scratch: `/tmp/rea-r4` (kept this round for
re-inspection; contains all raw evidence JSON).

Round 2 (`kaidoku-r2/08-version-diff.md`) proved the machinery on 31 KB `expac` /
84 KB `bwrap` and priced `op` at overview level only. This round ran the **substantial**
pair end-to-end including function-level dossiers.

## Targets — cached pacman pairs (`uniq -d` walk: 354 duplicated pkgbases)

| Pair | Member | Sizes (B) | sha256 | Type |
| ---- | ------ | --------- | ------ | ---- |
| `1password-cli` 2.34.1-1 → 2.40.0-2 | `usr/bin/op` | 41,210,040 → 43,475,106 | `d24dc5d4…` → `8d029d2c…` | ELF x86-64 static, stripped Go (**go1.25.7 → go1.26.8**) |
| `qpdf` 12.3.2-2 → 12.4.1-1 | `usr/bin/qpdf` | 14,528 → 14,600 | `2899dbfd…` → `dd26ac2d…` | ELF x86-64 PIE dyn, stripped C++ (control pair for `matched`/`symbol`) |

Extraction: `tar -xOf <pkg> usr/bin/<name>` — hashes reproduce round 2's `op` values.

## Run log (exact commands + wall-clock)

| # | Command | Wall | Result |
| - | ------- | ---- | ------ |
| 1 | `REA_GHIDRA_STARTUP_TIMEOUT_MS=800000 rea analyze op-2.34.1 --format json --snapshot snap-234.json` | 6m57.1s | `ev_c0cfbcce9695…`, 33,060 procs / 76,550 strings / 18 segs |
| 2 | same on `op-2.40.0` | 5m56.4s | `ev_0b3c8101fa5f…` — **identical evidence_id to round-2 run** (deterministic replay across sessions); 11,595 procs / 76,338 strings / 16 segs |
| 3 | `rea compare eb-234.json eb-240.json` (1-rec snapshot bundles) | 0.7s | `status:unknown`, `unresolved:2`, both `unresolved_branch` |
| 4 | `rea search op-2.34.1 "main.main" --kind procedures --mode regex --snapshot …` (default timeout) | 5m31.8s FAIL | `provider_timeout`, `operation=search_procedures`, `timeout_ms=330000`, retryable — **every verb pays the full import; the env bound must be raised on each call** |
| 5 | retry with `…=900000` | 6m57.9s | `ev_d41c9e66b99e…`, 1 hit: `main::main.main @ 0x1076920` |
| 6 | `rea search op-2.40.0 "main.main" …` (`…=900000`) | 5m49.9s | `ev_c657f980fe0e…`, **0 hits** — no `main.main` exists in this version's inventory |
| 7 | `rea search <op> ".*" --kind procedures` both | 6m45.3s / 5m40.9s | `ev_3a190f38183…` / `ev_48f0f11c5b0…`; 33,060 vs 11,595 rows |
| 8 | `rea function op-2.34.1 --procedure _rt0_amd64_linux` | 6m04.6s | `ev_0626e9ea1e76…`, 244,195 B dossier (ELF entry `0x485f40`) |
| 9 | `rea function op-2.40.0 --procedure entry` | 5m04.1s | `ev_5a94e8aa481b…`, 247,814 B dossier (ELF entry `0x491f20`) |
| 10 | `rea analyze qpdf-12.3.2 / 12.4.1 --snapshot …` | 6.1s / 6.1s | `ev_aedcac027285…` / `ev_97c58945a6eb…`, 62 procs each |
| 11 | `rea search qpdf-* "main"` and `".*"` | ~6s ea | `ev_4c283341fee8…` / `ev_ce0f61a53f75…`; shared non-EXTERNAL names: `entry`, `_DT_INIT`, `_DT_FINI`, `_INIT_0`, `_FINI_0`, `FUN_00101020` |
| 12 | `rea function qpdf-* --procedure entry` | 7.8s / 6.3s | `ev_775ddbb46770…` / `ev_d6d3c057ce54…`, 31,476 B each |
| 13 | `rea compare` on canonical 3-record bundles (domain-built via `createEvidenceBundle`) | <1s ea | both pairs `status:unknown`, `unresolved:6` — every record `unresolved_branch` |
| 14 | domain `compareBundles` + `record_pairs` (3 pairs each) | <1s ea | both `status:changed`, `records_changed:3`, `unresolved:0`, `observed_change` |
| 15 | domain `compareFunctions(qpdf entry, qpdf entry)` | <1s | `changed`, match `matched`/`symbol`; 7/8 dims unchanged, `assembly` +13/−13 (2 hunks) |
| 16 | domain `compareFunctions(_rt0_amd64_linux, entry)` — same ELF entry function | <1s | `changed`, match **`mismatched`/`explicit`**; 6/8 dims changed (below) |

## Per-dimension function diffs (8 dims: identity, pseudocode, assembly, comments, calls, references, strings_names, cfg)

**`op` ELF-entry pair** (`_rt0_amd64_linux@0x485f40` ↔ `entry@0x491f20`, verdict `mismatched`):

| dim | left | right | delta |
| --- | ---- | ----- | ----- |
| identity | — | — | changed (name + signature projection differ) |
| pseudocode | 2,581 ln | 2,262 ln | +41/−41 in 25 hunks |
| assembly | 24 | 24 | +1/−1 in 2 hunks |
| comments | 1 | 0 | changed |
| calls | 0 | 0 | unchanged |
| references | 4 | 2 | changed |
| strings_names | 1 | 1 | changed |
| cfg | 1 blk | 1 blk | unchanged |

**`qpdf` `entry`↔`entry`** (verdict `matched`/`symbol`, control case): 7/8 unchanged;
`assembly` 294→294 lines +13/−13 in 2 hunks — pure relocation text, limitation
"Assembly is opaque provider text; relocation normalization is unavailable." attached.

## Go toolchain naming collapse — why no shared-named function exists in the `op` pair

- `op-2.34.1` (`go1.25.7`): Go analyzer fully recovered pclntab names — 33,060
  procedures, ~32,933 carrying `namespace::pkg.name` symbols (`main::main.main`,
  `runtime::runtime.mstart0`, `_rt0_amd64_linux`, protobuf type stubs).
- `op-2.40.0` (`go1.26.8`): only 11,595 procedures recovered, 11,588 of them
  `FUN_*`/`thunk_FUN_*` auto-names; the sole real name is `entry`. Ghidra 12.1.4's Go
  analyzer cannot parse the Go 1.26 moduledata/pclntab layout (transient
  `Missing Go bootstrap type info, unable to extract Go RTTI info` seen in its
  `ghidra.log` during the session — dir since deleted, so this is observed-not-cited).
- Consequence: `search "main.main"` is positive on 2.34.1, empty on 2.40.0; the
  *same* ELF entry stub is `_rt0_amd64_linux` in one version and `entry` in the other.
  `compare_functions` reports `function_match.status=mismatched` even though the two
  dossiers describe the same function — symbol-keyed pairing fails across Go
  toolchain bumps, and an operator must pair by ELF role/address, not by name.
- Both entry dossiers decompile the *resolved* rt0 flow (~2.3–2.6k pseudocode lines
  for a 1-instruction `JMP` thunk: Ghidra follows the jump into `_rt0_amd64`/`rt0_go`),
  so the pseudocode dim carries real codegen drift (Go 1.25→1.26 runtime startup).

## Candidate: the full cross-version pipeline now works at 41–43 MB scale, function level included

- claim: `analyze → search → function → compare` runs end-to-end on two 41–43 MB
  stripped Go ELFs: every verb needs `REA_GHIDRA_STARTUP_TIMEOUT_MS` raised (~5–7 min
  per call, each a fresh Ghidra import — `--snapshot` accumulates *records* but does
  not keep the program resident across CLI invocations). `record_pairs` via the domain
  call (MCP `compare_bundles` input) turns the CLI's `unknown`/6-`unresolved_branch`
  verdict into `changed`/`observed_change`/`unresolved:0`; `compare_functions` then
  diffs paired dossiers across 8 dimensions with honest `mismatched` naming status.
- source: run log rows 1–16; `dist/domain/bundleComparison.js:64-92` (pair logic),
  `functionComparison.js:9-38`, `functionComparisonNormalization.js:10-27` (match rule).
- verify: re-run rows 8+9, then `node domain-compare.mjs functions fn-234-entry.json
  fn-240-entry.json`; and `compareBundles(eb-234-full, eb-240-full, pairs-full)`.
- verified-at: 2026-10-13
- suggested: admit — first function-level cross-version diff on a >40 MB binary;
  pairs with round-2's HELD machinery claim and closes its "untested at this scale" gap.

## Candidate: across a Go toolchain bump, per-function symbol-keyed matching collapses — pair by ELF role/address, not name

- claim: Ghidra 12.1.4 recovers namespaced Go symbols for a go1.25.7 build but falls
  back to `FUN_*` auto-names (11,588/11,595) on a go1.26.8 build of the same project.
  Zero shared procedure names exist across the pair (`search "main.main"`: hit vs
  empty; `.*` inventories intersect only at nothing — 2.40.0's only real name is
  `entry`). The *same* function (ELF entry: `0x485f40` vs `0x491f20`) compares as
  `function_match:mismatched`, so a name-keyed diff misses real correspondences; the
  8 dims still diff correctly when the pair is fed explicitly (cfg unchanged,
  pseudocode +41/−41/25 hunks).
- source: run log rows 5–9, 16; `readelf -h` entry addresses; `go version` on both
  binaries (`go1.25.7` vs `go1.26`, `go1.26.8` strings); `s234-all.json` /
  `s240-all.json` inventories in `/tmp/rea-r4`.
- verify: `rea search op-2.40.0 ".*" --kind procedures` → count non-`FUN_` names (1:
  `entry`); compare `function_match` on the ELF-entry dossier pair.
- verified-at: 2026-10-13
- suggested: admit — measured, not inferred; the toolchain-version link is
  corroborated by embedded `go1.26.8`/`go1.25.7` strings and a transient Ghidra
  Go-bootstrap log line (session dir since GC'd — flagged honestly).

## Candidate: `rea compare` membership-only ceiling reproduces at 3-record scale; `record_pairs` remains the decisive channel (MCP/domain only)

- claim: on canonical bundles carrying 3 records per side (overview, search,
  analyze_function), CLI `rea compare` returns `status:unknown`, `unresolved:6`
  (all `unresolved_branch`); the same bundles plus a 3-pair `record_pairs` array
  return `status:changed`, `records_changed:3`, `unresolved:0`. Identical result on
  the op pair and the qpdf control pair.
- source: run log rows 13–14; `cmp-full-cli.json` / `qcmp-cli.json` vs
  `cmp-full-pairs.json` / `qcmp-pairs.json` in `/tmp/rea-r4`;
  `bundleComparison.js:94-156`.
- verify: `rea compare eb-234-full.json eb-240-full.json` then domain
  `compareBundles` with the pairs listed in `/tmp/rea-r4/pairs-full.json`.
- verified-at: 2026-10-13
- suggested: admit — extends round-2's finding from hand-wrapped/1-record bundles to
  canonical `createEvidenceBundle` outputs with mixed operation types.

## Candidate: evidence_ids are deterministic across rounds — `op-2.40.0` overview replayed `ev_0b3c8101…` identically to round 2

- claim: the `binary_overview` record for `op-2.40.0` (`8d029d2c…`) hashed to
  `ev_0b3c8101fa5fe860a42b7373658f9d8521df24f77edfc38ac8b843b340bf1ff5` — the same id
  round 2 reported. Extraction (`tar -xOf`), analysis, and id minting are all
  replay-deterministic across sessions/days. (`op-2.34.1` minted `ev_c0cfbcce…`
  here vs `ev_8e20ac5d…` in round 2 — round 2's run used default TOON/330 s-bound
  parameters, so the parameter fold, not the subject, differs.)
- source: `an-234.json`/`an-240.json` vs `kaidoku-r2/08-version-diff.md` row 14.
- verify: `rea analyze` the same extracted file with identical flags; compare
  `evidence_id`.
- verified-at: 2026-10-13
- suggested: admit — same-input-same-id confirmed on the right side; left-side
  variance is parameter-driven, not nondeterminism (worth one clean rerun if the
  distinction matters downstream).

## Candidate: at >40 MB every verb re-imports — `--snapshot` saves records, not runtime; budget ~6 min per call per version

- claim: each `rea` CLI call spins a fresh headless Ghidra (`/tmp/rea-ghidra-*`),
  imports the whole binary, analyzes, and deletes the project. `analyze`, `search`,
  and `function` each cost 5–7 min on the op binaries under fleet load (16+ parallel
  Ghidra jobs); a default-timeout `search` dies at exactly 330 s with
  `provider_timeout`/`search_procedures`. `--snapshot` only appends the returned
  record into the session file — useful for building compare-able bundles, useless
  as a runtime shortcut. Whole-pair function-level compare ≈ 6 calls ≈ 36 min.
- source: run log rows 1–9 (wall-clock), row 4 (typed timeout), `ps`/`/tmp/rea-ghidra-*`
  observation of fresh projects per call; `s234-main.json` timeout record.
- verify: `time rea search <41MB> "x" --kind procedures --mode regex` with and
  without `REA_GHIDRA_STARTUP_TIMEOUT_MS`.
- verified-at: 2026-10-13
- suggested: admit — priced on two binaries, three verb types, four timeout
  observations (incl. round 2's). Mitigation for the lane: raise the env bound on
  *every* call, batch all queries per binary into one snapshot file.

## Error taxonomy observed this round

| code | category | retryable | trigger |
| ---- | -------- | --------- | ------- |
| `provider_timeout` | `timeout` | true | `search_procedures` at 330 s default on 41 MB stripped Go (row 4) |

## Summary

**Substantial-pair compare HELD end-to-end: binary→records→membership+semantic diff,
with one real hazard surfaced.** The 1password-cli pair (41→43 MB, go1.25.7→go1.26.8)
went through the full loop: overviews (33,060 vs 11,595 procs, 18→16 segs,
76.5k→76.3k strings — real drift), full-procedure inventories, per-function dossiers,
CLI membership compare (`unknown`/6 `unresolved_branch`), domain `record_pairs`
compare (`changed`/0 unresolved, `observed_change`), and `compare_functions` on the
ELF-entry pair (6/8 dims changed, real pseudocode/reference/comment drift, cfg
unchanged). The qpdf control pair exercised the `matched`/`symbol` path (`entry`↔
`entry`, only relocation assembly churn). The decisive new finding: **a Go toolchain
bump silently collapses provider symbol recovery** — 99.94% of 2.40.0 procedures are
`FUN_*`, so the same function is `entry` vs `_rt0_amd64_linux` and `function_match`
reads `mismatched`; symbol-keyed cross-version pairing is unsafe across Go versions —
pair by ELF role/address (or explicit dossier ids) instead. Cost model is now priced:
~6 min per verb per version at this scale, every call a fresh import, raise
`REA_GHIDRA_STARTUP_TIMEOUT_MS` on all of them. Replay is deterministic
(`ev_0b3c8101…` reproduced from round 2). All artifacts in `/tmp/rea-r4`; one report
file written, nothing committed.
