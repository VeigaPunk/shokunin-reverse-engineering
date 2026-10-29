# ExecRegistryRow — receipts

All commands run offline in a scratch clone (`git clone --shared` of the lane, detached at
`6f4aba63`). No REA run, no `--data-run`, no lane write. Scratch:
`/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow` (removed after receipts were copied here).

Exit-code semantics: 0 met/clean, 1 not met/violation, 2 could-not-evaluate.

---

## R1 — baseline: frozen C2 counter at the lane HEAD

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
export TMPDIR=/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow
python3 -I -B tools/round-50/c2-record.py --root . --rev HEAD \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 \
  --work "$TMPDIR/work" --json-out "$TMPDIR/c2-head.json"
```
- exit code: **0**
- stdout sha256: `6b2275bcebe292393e16651998e764c13656db9746a20245b47005926145ffab`
  (identical to the `--json-out` receipt, which is the printed JSON plus a trailing newline)
- UTC: 2026-10-29T17:40Z (scratch mtime)
- result: `exit_code 0`, `mismatches 0`, `atoms_total 11`, all eleven atoms green (B1–B11),
  `reason` null. **B9 green at HEAD.**
- receipt artifact sha256: `receipt-c2-head.json` =
  `6b2275bcebe292393e16651998e764c13656db9746a20245b47005926145ffab`

## R2 — B9 coupling simulation (three arms, frozen derivations)

```
python3 -I -B $S/sim-b9.py $S/clone   # uses c2-record.py's own b9()/registry_region()/census_paths()
```
- exit code: **0**
- artifact: `receipt-sim-b9.json`
  sha256 `ba2176052a9bd990d87fe5f23379669892f4044bb1979977d3c9a5e32d067972`
- arms and verdicts:
  - **A** file in-tree, no registry row → `b9_problems: ["tools/round-50/sqfs-triage-v5.py: no registry row"]` → **red (1)**
  - **B** file in-tree + candidate row → `b9_problems: []`, `b9_ok: true` → **green (0)**
  - **C** row only (no file) → `b9_problems: ["tools/round-50/sqfs-triage-v5.py: 2 registry rows, want 1"]` → **red (1)**
  - census in every arm: 12 `tools/round-49/**` + `tools/round-50/**` paths (+ the new one in arms A/B)

## R3 — path-rule measurement (the decisive one)

```
python3 -I -B $S/sim-paths.py $S/clone   # uses c1-counter.frozen_drift() and c2-record.freeze_check()
```
- exit code: **0**
- artifact: `receipt-sim-paths.json`
  sha256 `f6a0327632fd380297214e886be82d3b36f68308926585a3cd45e7ffe1150c42`
- results:

| landing path | C1 `frozen_drift` (freeze `435d41fd`) | C2 `freeze_check` | B9 |
|---|---|---|---|
| `tools/round-50/sqfs-triage-v5.py` | `['tools/round-50/sqfs-triage-v5.py']` → **C1 would exit 2** | `('frozen path touched in FREEZE..REV: … A tools/round-50/sqfs-triage-v5.py', 'frozen_path_changed')` → **C2 would exit 2** | green with the row |
| `tools/round-50-c3/sqfs-triage-v5.py` | `[]` → **no drift** | `(None, None)` → **no drift** | green; census unchanged at 12 |

- `instrument_visible_to_census_prefix`: `true` (in-tree) / `false` (out-of-tree).
- `git ls-tree -r --name-only HEAD -- tools/round-50` returns **0** hits for `round-50-c3`
  (pathspec matches the `tools/round-50` directory only).

## R4 — frozen C2 counter at the simulated C3 landing (out-of-tree path + row)

```
cd $S/clone   # rev 80cd92b4361deb22d7c984a72c0f924db7190388 = instrument + registry row
python3 -I -B tools/round-50/c2-record.py --root . --rev HEAD \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 \
  --work "$S/w4" --json-out "$S/c2-outtree.json"
```
- exit code: **0**
- artifact: `receipt-c2-c3landing.json`
  sha256 `952de06c856ff88d4d7c29762532dc5c0375f70c2959d0c24a3f5ac56753219a`
- result: `exit_code 0`, `mismatches 0`, `atoms_total 11`, all eleven atoms green including B9,
  `reason` null. **The C2 coupling stays green at the C3 landing.**

## R5 — frozen C2 counter at the same landing with the in-tree path (the failure it would cause)

```
python3 -I -B tools/round-50/c2-record.py --root . --rev <in-tree landing rev> \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --work "$S/work2" --json-out "$S/c2-sim.json"
```
- exit code: **2** (could-not-evaluate)
- artifact: `receipt-c2-oldfreeze-intree.json`
  sha256 `fe932ae1170362c91468126368f5bbc4389087ff04d4fa27d01547090ccef0df`
- result: `reason: "frozen_path_changed"`,
  `detail: "frozen path touched in FREEZE..REV: 549dfded A tools/round-50/sqfs-triage-v5.py"`

## R6 — row validation against every frozen rule

```
python3 -I -B $S/validate-row.py $S/clone $S/row-final.txt
```
- exit code: **0**
- artifact: `receipt-validate-row.json`
  sha256 `3477a457ad5329ca2a83c99b01aa31efc7bb88975a98df9f14ba86969aeed0d6`
- the row bytes validated: `row-final.txt`
  sha256 `3cce072798d598511393f3b84c6c19b99eeecda317e43a09e6c147cc5f88f64e`
- checks, all true:
  - `cells` = 7; `cell0_matches_path` true; `no_raw_pipe_in_cells` true
  - `kind_gate_or_probe` true (cell 1 opens `gate`)
  - `entry_command_naming_path` true; `entry_command_text` =
    `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py`
  - `meaning_c2record_port` = `null` (no error) — the frozen round-48 rule ported into
    `c2-record.py`
  - `meaning_round48_rule` = `{"0": "success", "1": "not-met", "2": "unevaluable"}` — the
    original `tools/round-48/meanings.py` rule
  - `selftest_cell_ok` true; `selftest_cell_text` =
    `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest — …`
  - `pinned_cell_ok` true; `pinned_paths_exist` = true for the manifest
  - `rows_in_region_before` = 54, `duplicate_cell0_paths` = `[]`,
    `target_row_already_present` = false, `rows_naming_round50_c3` = `[]`
  - `all_rows_7_cells` true; `rows_with_bad_meaning` = `[]` (all 54 existing rows still
    parse under the round-48 meaning rule)

## R7 — effect on the other registry gates (measured at HEAD and at the C3 landing rev)

| command | exit | result |
|---|---|---|
| `python3 -I -B tools/round-46/registry.py --root . --freeze HEAD --rev HEAD --json-out r46.json` | 0 | `met_target true`, `failing []` — green at HEAD **and** at the C3 landing rev |
| `python3 -I -B tools/round-45/c2-counter.py --root . --rev HEAD --freeze HEAD --json-out r45.json` | 0 | `met_target true`, `failing []`, `scope_size 6`, `unregistered []` — green (scope is rounds 44-45 only) |
| `python3 -I -B tools/round-48/meanings.py --root . --rev HEAD --freeze HEAD --json-out r48-head.json` | 1 | **already red at HEAD**: `failing: ["registry rows outside the census: [ …12 rows… ]"]`. At the C3 landing rev the list is the same 12 **plus** `tools/round-50-c3/sqfs-triage-v5.py` = 13. Pre-existing and disclosed (`plans/round-50-claims.md:34-38`); not a new defect |
| `python3 -I -B tools/round-49/c2-mismatch.py --root . --rev HEAD --freeze HEAD --json-out r49.json` | 1 | A8 red at HEAD and at the C3 landing rev with **identical** numbers (`rows 146 -> 149, derived 146 -> 152`) — A8 counts `corpus/SOURCES.md` rows, not registry rows; the new row does not move it |

## R8 — pinned-value path existence and hash

```
sha256sum .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/manifest.json
```
- `1acd4ca21435477b5a7141f0edfef081212526ffb0280810dca4c0e72a20bbb9`
- git-tracked: yes (`git ls-files --error-unmatch` exits 0)
- corpus census (read-only): manifest `entries` = 135, `envelopes/` dirs = 126, nine entries are
  manifest-only per `REBUILD.md`.
- the four `squashfs_v2_nonstandard *_ddefault` rows the claim names are present in the
  manifest, all `a1_label clean` / `a1_action none`, and all four have envelope directories:
  `squashfs_v2_nonstandard_squashfs_v2.0_be_ddefault`,
  `…_squashfs_v2.0_le_ddefault`, `…_squashfs_v2.1_be_ddefault`, `…_squashfs_v2.1_le_ddefault`.
- wider than the claim names: `squashfs_v3_broadcom` carries 7 `clean`/`none` `_ddefault` rows
  and `squashfs_v3_nonstandard` carries 8.

## R9 — source hashes at the measured lane revision

```
sha256sum tools/round-50/c2-record.py tools/round-50/c1-counter.py SKILL.md
```
- `4749bcd86c8f61bfb6994baeab3bd990b61ea0c369b87197351d0a4618e71285  tools/round-50/c2-record.py`
- `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813  tools/round-50/c1-counter.py`
- `19046cf204ce999e5dccb1ebe86eebe9921e84ded8443dd87abc5a693fd8c974  SKILL.md`
- registry region at HEAD: **54** rows.

## R10 — host guard

```
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
```
- exit code **0**; `kaidoku-r50` 5.3 G, `idle=0`. No heavy pass was run; the guard was
  consulted before the clone work and the load was low.

---

## R11 — the lane's C3 instrument path holds a 49-byte STUB (do-nothing green)

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
ls -la tools/round-50-c3/ ; sha256sum tools/round-50-c3/sqfs-triage-v5.py
cat tools/round-50-c3/sqfs-triage-v5.py
```
- exit code: **0**
- 49 bytes, sha256 `af1b22ba25b36e2340c5cadb6b9d1078988b75697edbf52c925e41d32f587218`
- content: `#!/usr/bin/env python3` / `# simulated C3 instrument`
- git status in the lane: `?? tools/round-50-c3/` — **untracked, not committed**
- the real instrument: `.ufo/waves/round-50/w3/ExecTriageV5/tools/round-50-c3/sqfs-triage-v5.py`,
  90,837 bytes, sha256 `c444f7ee918234bfa0b286afd37739a3b9fa1e7b2cdd4455fd4b25862f66367f`

## R12 — the stub fake-greens

```
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest --work $S/w
```
- exit code: **0**; stdout **0 bytes** (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
  = the sha256 of the empty string)

```
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root . --rev HEAD --freeze HEAD \
  --envelopes <R42C2ReconLegacy/envelopes> --work $S/w8 --json-out $S/stub-pred2.json
```
- exit code: **0**; **the `--json-out` receipt is NOT written** (`stub-pred2.json` absent)
- cause: a 2-line file with no `main()` simply runs and exits 0; only the receipt's presence
  distinguishes it. **A scoring step must require the receipt to exist and parse, not just a
  zero exit.**

## R13 — the real instrument at the same path (the bytes that must be frozen)

```
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest --work $S/w3
```
- exit code: **0**; stdout 1,230 bytes, sha256
  `52c6fd3c3ca0f1547c90fbe8a9c8f53f50cf5a2ed23a1f726b9258f28a526bd1`
- last line: `selftest: 13 cases, pass 13, fail 0`

```
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root . --rev HEAD --freeze HEAD \
  --envelopes <R42C2ReconLegacy/envelopes> --work $S/w9 --json-out $S/real-pred.json
```
- exit code: **1**; the receipt IS written — `receipt-real-instrument-before.json`,
  sha256 `6f917393054397f929a11eb0718dc87399840c65d9a2f678a16148c3aecc5fce`
- `pair_mismatches` = **19**, `evaluator_missing` = `[]`, and **all four**
  `squashfs_v2_nonstandard *_ddefault` rows are among the mismatches — the claim's before-state
  (exit 1, ≥4 mismatches incl. the four v2ns rows) reproduces on the real bytes only.

## R14 — the competing sibling row vs mine, against B9's frozen self-test rule

```
python3 -I -B  # c2-record.py's own cells() and the frozen b9() regexes, both rows
```
- exit code: **0**
- `ExecTriageV5`'s landing-draft row (`…/ExecTriageV5/receipts/landing-draft.md` line 84):
  - `cells` = 7; `kind` ok **True**; `entry names path` **True**; `pinned cell ok` **True**
  - `selftest cell ok` **False** — cell 3 is
    `` `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest` (13 cases, pass 13, fail 0, exit 0 at the freeze) ``
    which opens with a backtick, so `re.match` against B9's
    `<interpreter> <path> … --selftest` fails and the `none — <reason>` alternative also fails
  - round-48 meaning map: `{0: success, 1: not-met, 2: unevaluable}` — valid
- my row (`row-final.txt`): `cells` = 7; `kind` ok **True**; `entry names path` **True**;
  `pinned cell ok` **True**; `selftest cell ok` **True**; round-48 meaning map valid.
- The difference is the self-test cell alone.

## R15 — attribution of the fleet misroot

```
grep -rn "simulated C3 instrument" /fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2/*.py
```
- exit code: **0**
- one hit: `/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2/final-landing.py:64`
  → `fh.write('#!/usr/bin/env python3\n# simulated C3 instrument\n')`
- that scratch dir belongs to a **second instance of my seat** (`ExecRegistryRow-2`); its
  scripts (`validate-peer-row.py`, `registry-couplings.py`, `drift-extension.py`) are written
  from a *peer* seat's perspective ("the peer seat's registry row"), and `final-landing.py`
  writes the stub into a fixture clone at a path that was resolved relative to the lane root.
- the fleet tree is clean again: `git status --porcelain` in `/home/vgpnk/Projects/shokunin`
  shows only the pre-existing `M .scratch/goal-20261029-hyaku-run12.md` and
  `M .ufo/l0-questions.md` — **no `?? tools/`**.

## R16 — C2 at the landing with the REAL instrument + my row

```
# fixture clone: real instrument copied byte-identical to tools/round-50-c3/, my row pasted
git -C clone commit -m 'sim: real instrument at round-50-c3 + ExecRegistryRow row'   # rev e7b0a89a
python3 -I -B tools/round-50/c2-record.py --root . --rev HEAD \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --work $S/w4 --json-out $S/c2-real.json
```
- exit code: **0**
- receipt: `receipt-c2-realinstrument-landing.json`, sha256
  `1545d354989c49ff1308ef38c15d3c6c1e1d62fb266b4a3ae091c0a5e4ea29bc`
- `exit_code 0`, `mismatches 0`, `atoms_total 11`, **all eleven atoms green including B9**,
  `reason` null. The C2 coupling stays green with the real instrument and my row.

## Not run (stated, not claimed)

- No REA of any kind (`npx rea-agents`, `rea`, the `rea-agents` package): not invoked.
- No `--data-run` on any tool.
- `tools/round-50/c1-counter.py` was **not** run end-to-end (it needs REA and the vendor
  carriers); its frozen `frozen_drift()` derivation was exercised directly instead, which is
  the arm that decides the path question.
- The v5 instrument was not built (not this seat's assignment) and its selftest was not run;
  cell 3 of the row therefore states the spelling, not a case count.
- `tools/round-42/sqfs-triage-v4.py --selftest` was not run (not this seat's assignment).
- The v5 instrument's `--controls` arm was not run by this seat (the sibling owns it); this
  seat ran only its `--selftest` and its predicate command against the committed envelope
  corpus, plus the frozen C2 counter, all read-only against the lane.

## Tooling

No tool was installed or upgraded by this seat; nothing to record for the operator's
tooling channel.
