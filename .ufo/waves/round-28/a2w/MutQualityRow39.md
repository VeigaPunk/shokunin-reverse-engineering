# MutQualityRow39 — mutation test of QUALITY row 39

Seat: KaidokuR28a2.MutQualityRow39. Date: 2026-10-22. Lane: read-only, tip at
dispatch 9db24c9e10287d44d9f780d782ab608f3c84ff5a. Sandbox:
`git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin` into
`/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow39/clone`.

## Target

QUALITY row 39: every REA call record (the `runs.tsv` row) names the resolved
package version and the sha256 of the resolved package's own `package.json`,
per call; the counting instrument rejects a run whose recorded version or
`package.json` sha256 differs from the pin.

Enforcement lives in `tools/round-28/c1-heldout-naming.py`:

- `RUNS_HEADER` (line 60) requires columns `pkg_version` and `pkg_json_sha256`;
  `tsv` (lines 127-132) returns None when the file header differs, so a runs.tsv
  missing a pkg column is rejected as "runs.tsv absent or header differs".
- `check_runs` line 174:
  `if r["pkg_version"] != PKG_VERSION or r["pkg_json_sha256"] != PKG_JSON_SHA:`
  with `PKG_VERSION = "6.5.0"`, `PKG_JSON_SHA = "a5003023..."` (lines 57-58).
- Selftest red cases `red-pkg-sha` (sets `pkg_json_sha256` to "0"*64) and
  `red-pkg-version` (sets `pkg_version` to "6.7.0"), lines 532-533.

`c2-filtered-flag.py` has no REA calls (openchain HTTP fetch only), so row 39's
check has no counterpart there — observation, not a defect of this counter.

## Detector and baselines (observed)

Command: `python3 tools/round-28/c1-heldout-naming.py --selftest`, run in the
clone. Pristine file sha256 `29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c`
(identical in lane and clone — observed via sha256sum on both).

- 18:24:26Z baseline, pristine bytes: 21 cases, `failures=0`, exit 0.
- Post-M5 restore, 18:33:09Z: sha256 back to `29c2b571…`, `git status` clean.
  The lane file was never touched (all edits in the clone only).

## Mutations (each applied, selftest run, then `git restore` in the clone)

Mutant diffs and per-mutant file hashes: `mutants.diff` (sha256 below).

- M1, drop the `pkg_json_sha256` comparison.
  18:29:06Z, mutant sha256 `f7c879f3…`. Selftest output excerpt:
  `FAIL red-pkg-sha exit=0 want=1`, `selftest cases=21 failures=1`, exit 1.
  Verdict: KILLED by `red-pkg-sha`.
- M2, drop the `pkg_version` comparison.
  18:30:07Z, mutant sha256 `74ad88e4…`. Excerpt:
  `FAIL red-pkg-version exit=0 want=1`, `failures=1`, exit 1.
  Verdict: KILLED by `red-pkg-version`.
- M3, equality weakened to prefix match (`startswith(PKG_VERSION)` /
  `startswith(PKG_JSON_SHA)`).
  18:31:06Z, mutant sha256 `4e0081a2…`. Excerpt: every case `ok`,
  `selftest cases=21 failures=0`, exit 0.
  Verdict: SURVIVED. A forged `pkg_version` or `pkg_json_sha256` that merely
  shares the pin's prefix would be accepted; the selftest's red values
  ("6.7.0", "0"*64) do not share the prefix, so no case detects this
  weakening. Coverage finding (observation).
- M4, check scoped to the first carrier only
  (`name == carriers[0]["carrier"] and (...)`).
  18:32:06Z, mutant sha256 `c4044371…`. Excerpt:
  `FAIL red-pkg-version exit=0 want=1`, `failures=1`, exit 1.
  Verdict: KILLED by `red-pkg-version` (the second fixture carrier is left
  unchecked; the selftest covers both rows).
- M5, digest comparison case-folded (`r["pkg_json_sha256"].lower()`).
  18:33:09Z, mutant sha256 `0e06c2ba…`. Excerpt: every case `ok`,
  `failures=0`, exit 0.
  Verdict: SURVIVED. An uppercase rendering of the pinned digest is accepted;
  no red fixture exercises a case-variant. Coverage finding (observation).

## Result

The row-39 check exists and the selftest kills mutants that remove either
comparison or narrow the check's per-carrier scope: 3 killed, 2 survived
(M3 prefix, M5 case-fold). The survivors show the selftest never proves strict
byte equality — it has no red case that differs from the pin only in case or
only after a matching prefix. Coverage findings, not a change to the contract
(this seat does not judge or ship).

Separately observed (observation, `sha256sum`, 18:33Z):
`PKG_JSON_SHA` equals the sha256 of
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`
(`a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`, package
name+version `rea-agents 6.5.0`), so the pin is the resolved package's own
`package.json` digest. The h01 envelope carries provider version
`evmole@0.9.3` but no pkg-version/package.json-sha members — the per-call pin
travels only in the runs.tsv row (observation; row 39's fail clauses target
the call record's columns, which are present and read).

## Artifacts (scratch, sha256)

- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow39/mutants.diff`
  — see sha256 printed beside this report's write.
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow39/clone/` — sandbox
  clone used for every mutant run; counter restored to `29c2b571…`.

No tools installed this seat; no installs needed.
