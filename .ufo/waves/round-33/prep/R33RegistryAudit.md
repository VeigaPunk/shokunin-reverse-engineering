# R33RegistryAudit — SKILL round-31/32 registry vs cited source files (read-only)

- **Seat:** `KaidokuR33.R33RegistryAudit` (UFO-FSD reviewer)
- **Base:** `428315a8f5674b952def862910af6e07a6c2224b` (lane HEAD throughout; `git status` shows only the untracked `.ufo/waves/round-33/` prep tree)
- **Contract:** `.ufo/waves/round-33/prep-contract.txt`
- **Scope:** SKILL.md round-31 measurement registry (lines 1040–1048) and round-32 instrument registry + witness paragraphs (lines 1064–1084), checked read-only against every cited script and claims file. Held item U064N008Hf47eb933 not inspected. No tools run, no probes executed, no installs.
- **Method:** source read of all nine `tools/round-3{1,2}` instruments, `independent-pe/pe_indep.py` + `compare.py` + `secondary_evidence.py`, `final-c1-witness/pe_own_compare.py`, `source-reopen/verify_quotes.py`, and all four claims files. Selftest case counts re-derived by counting case tuples (reported count = `len(cases)` + printed extras).
- **Execution UTC:** file reads and `git log`/`ls`/`head` only, 2026-10-23T08:05–08:20Z. No gate, counter, selftest, or build was run (read-only audit; the contract forbids unassigned runs).

## 1. Findings by severity

### HIGH — none that break the registry's core statements

The freeze-selectable gate, independent-PE compare, final-C1 witness, and quote-replay entries are substantively accurate (evidence in §3). The defects below are mismatches of degree, not false registrations.

### MEDIUM — mismatches where the registered text diverges from the bytes

**M1. Exit map claims uncaught errors are "could-not-evaluate"; the code exits 1 on any uncaught exception.**
`SKILL.md:1068` (ARM64X positive counter, verdict map): *"uncaught errors are could-not-evaluate, not a predicate result."* In `tools/round-32/c1-arm64x-positive.py` an uncaught exception (corrupt `PKG_JSON`, missing envelope blob, OracleError) propagates through `measure()` → `main()` → Python's default exception exit **1**. Exit 1 is registered as "failed". Nothing prints a `PIN`/`ERROR` marker for crashes, so a crash is indistinguishable from a measured predicate failure by exit code alone. The sentence describes intent, not the exit map. (Round-30's own registry row already documents the crash class: "a missing REA `package.json` crashes with exit 1".)

**M2. Round-31 counters: write mode still prints the receipt-shaped target line and exits 0/1 — the "never a receipt" norm is aspirational for this tool.**
`SKILL.md:1044` says "`--write-evidence` … is never a receipt". Source: `tools/round-31/c1-sqlite-positive.py:187-201` — write mode skips `committed_check` (line 180 `if verdict == LABEL and not write`) but still prints `carriers=12 pass=12 target=12 entry_ok=… province_ok=…` and returns `0 if passed == TARGET and e_ok and p_ok`. Same shape in `c2-sqlite-refusals.py:342,354-363` (`requests=… matches=… target=23 …`, exits 0/1). Only the per-carrier `runs.tsv` column distinguishes write mode (`verdict_without_committed_clause` in r32; r31 writes plain `verdict`). The exit-3 "not a receipt" separation exists only in the round-32 counter (`c1-arm64x-positive.py:211-218`, defect M31-3 fix). A reader copying the r31 row could mistake a write-mode exit-0 line for a measure receipt.

**M3. Replay prerequisites omitted for the final-C1 witness.**
`SKILL.md:1083` (residual witness table): "committed sibling envelope/readobj/TSV captures reproduce the recorded layout." Verified: `final-c1-witness/` holds `carriers.tsv`, `predictions.tsv`, `env/k01…k12.json`, `ro-k01…k12.txt` — but `pe_own_compare.py:118` calls `own_parse(f"{CAR}/{cid}.dll")`, i.e. **live carrier bytes** from `/fast/scratch/hyaku/kaidoku-r32/carriers/` (TSV `path` column), which are not committed anywhere. After scratch loss a replay needs a fresh `build-arm64x-carriers.sh` output dir verified against the frozen TSV sha256 column. The row also omits that `<SCRATCH>` must contain copies of the two TSVs (`{SCR}/carriers.tsv`, `{SCR}/predictions.tsv` read at lines 114-115) and receives `compare-own.json` (line 143). Exit-code conflation as M1 also applies: any exception → 1 = failed.

**M4. `independent-pe/secondary_evidence.py` exists, is committed, but is unregistered.**
The committed sibling `.ufo/waves/round-32/independent-pe/secondary_evidence.py` (sha256 `9aed4a5d…d83d7`, `A2PEIndependent.md:166`) reads `indep.json` + carrier bytes and produces `secondary-evidence.json` — the evidence for the "secondary directory starts at primary bloc end, no data-directory entry" findings (`A2PEIndependent.md:141`). SKILL.md:1077's retained-witness paragraph names only `pe_indep.py` and `compare.py`. A verifier reading the registry cannot know the placement/reference evidence has its own script. Hard-codes the same scratch `BASE` (`secondary_evidence.py:16`).

**M5. Round-31 replay prerequisites omitted: mutant/carrier tree lives under `/fast/scratch/hyaku/kaidoku-r31/`.**
`c2-sqlite-refusals.py:75` hard-codes `base_of()` → `/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite`, and `corpus/evidence/round-31/c2/predictions.tsv` names all request paths under `/fast/scratch/hyaku/kaidoku-r31/`. Measure exits 2 (PIN) when the tree is absent/altered; the row (SKILL.md:1045) registers `--build` as "mutant builder" but never says a measure run presupposes the scratch tree rebuilt by `--build`. Round-30's registry discloses the equivalent scratch coupling; the r31 row dropped it.

### LOW — conformance-limit / completeness disclosures, no false statement

**L1. Freeze-selectable gate kind vs. §Gate self-test standard (routed defect 3, already known — disclosure adequate, cite the open defect).**
`SKILL.md:1073` keeps kind `gate` with "no self-invocation mode; inherited gate-conformance limitation, not selftest credit". Source confirms: `tools/round-32/freeze-integrity.py` has no selftest path (argparse: `--root --round [--claims] [--rev]`), exit 2 only for absent freeze commit; argparse usage errors also exit 2 (unregistered-but-accurate). Spot-check defect #3 (`corpus/lessons/round-32-verifier-spotcheck.md:115`) demands a fixture selftest or probe re-registration and is open. The row should cross-reference that defect so the `gate` kind is visibly contested rather than silently non-conformant. Do **not** relabel it probe in the registry — the historical gate purpose (detect post-freeze edits to pinned inputs; exits 1 on tamper, demonstrated on the amended-predictions clone) is real; disclosure, not demotion, is the fix while the routed defect is pending.

**L2. `cited-runs-gate` selftest write scope undisclosed.**
`tools/round-31/cited-runs-gate.py:344` builds its throw-away git repo under `tempfile.mkdtemp(dir=os.path.dirname(SCRIPT))` — i.e., inside `tools/round-31/` in the lane checkout — removed by `shutil.rmtree` (line 607) unless `--keep-selftest` (line 250, unregistered flag). The registry's convention elsewhere annotates in-lane selftest writes ("creates and removes only its isolated fixture directory under .ufo/rounds/interactive-r1/"); this row's write-scope cell is silent.

**L3. `verify_quotes.py` absolute-path pins and assertion exit-1 not fully disclosed.**
`SKILL.md:1084` correctly says restore `reopen/` captures to the script's absolute `RE` (`/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSourceReopen/reopen`, line 8) and that `census.json` writes to `RE.parent` (line 231). Two undisclosed limits: `SNAP`/`C1IN` are absolute lane paths (lines 6-7) so replay is lane-checkout-fixed; and the line-158 `assert run26 is not None` raises → exit 1, indistinguishable from a check failure (same class as M1).

**L4. `compare.py` host dependency and argv-insensitivity undisclosed.**
`independent-pe/compare.py:212` shells `llvm-readobj --version` for the payload's `readobj_tool` field (unbounded PATH lookup); and the script takes **no** argv — `main()` ignores `sys.argv`, so "entry" is bare `python3 -I -B compare.py` with everything (TSV at line 19, BASE at line 20) hard-coded. The SKILL.md:1077 paragraph's "inputs are sibling decode/oracle/readobj captures and frozen carriers.tsv" is accurate but a reader could reasonably expect inputs to be passed in.

**L5. `--fleet` default and `PKG_JSON`-crash note dropped in r31/r32 counter rows.**
All three c2-calibration counters accept `--fleet` (default `/home/vgpnk/Projects/shokunin`) and resolve `MANIFEST.json` at fleet pin `cef00867…`; registered command shows only `--root --rev`. Also every r31/r32 counter reads `PKG_JSON` by `json.load(open(...))` — a missing package.json crashes exit 1 (r30 row disclosed this; r31/r32 rows dropped the parenthetical).

**L6. `pe_indep.py --json` registered as required; it is optional.**
`.ufo/waves/round-32/independent-pe/pe_indep.py:437-439`: `--json` is optional (payload always prints to stdout); only `--tsv`/`--file` is required. Registered entry `--tsv <carriers.tsv> --json <NEW-JSON>` matches the exercised argv, so label it "exercised argv", not the only form.

### Consistency checks that PASSED (no change needed)

- Selftest counts: c1-sqlite 14 (7+7), c2-sqlite 12 (9+3), cited-runs 17 (14+3), c1-arm64x 18 (11+7), c2-calib-v3 18 (16+2) — all match.
- Exit maps: freeze-integrity 0/1/2 verified at `tools/round-32/freeze-integrity.py:43,62,64`; `--claims` works for claims-v2/v3 (freeze = earliest `--diff-filter=A` commit; claims-v3 first-add is `f382e3b7`, claims.json `9a73680a` per docstrings/`git log`).
- `compare.py` verdict 0/1 (`:234`), 372 checks = 12 carriers × 31 checks matches `compare.stdout.txt`; `pe_own_compare.py` 12 checks/carrier → recorded "144/144" in `FinalC1Measure.md`/`counter.stdout.txt`.
- `verify_quotes.py` positive+negative quote controls, ≤25-word rule, `EXPECT`/`LIVE_EXPECT` pins match committed `verify-out.txt`/`census.json`; TSV column indices (`tsv[2]` sha, `tsv[4]` native, `tsv[5]` ec; `pred[1]` procs, `pred[2]` segs) match `final-c1-witness/*.tsv`.
- v1/v2 counters' "0 clean under superseded predicate; 1; 2" maps verified at `c2-capability-calibration{,-v2}.py` exits; both accept `--selftest` (10 and 14 cases respectively; registry claims no count).
- `arm64x_oracle.py`/`sqlite_oracle.py` CLI entries, claims-file `instruments`/`frozen_inputs` digests, `MutOracle.md` 8/12 killed, `A2BuildRecheck.md` independent rebuild — all consistent.

## 2. Proposed surgical prose edits to SKILL.md

All edits are single-cell or sentence-level; no table structure changes, no kind relabels. Exact replacement text (quote → replace).

**E1 — SKILL.md:1068, ARM64X positive counter verdict map.** Replace
`2 could-not-evaluate (pins); 3 could-not-evaluate (write mode, never a receipt); uncaught errors are could-not-evaluate, not a predicate result`
with
`2 could-not-evaluate (pins); 3 could-not-evaluate (write mode, never a receipt); a missing REA package.json crashes with exit 1 (uncaught errors exit 1, indistinguishable from failed — a crash is not a predicate result but cannot be told apart by exit code alone)`

**E2 — SKILL.md:1044, c1-sqlite-positive exit-codes cell.** Replace
``--write-evidence` skips the committed-record clause and is never a receipt`
with
``--write-evidence` skips the committed-record clause and is never a receipt; unlike the round-32 counter it still prints the target line and exits 0/1 (pre-M31-3), so write-mode output is receipt-shaped and only `runs.tsv`'s verdict column marks it`

**E3 — SKILL.md:1073, freeze-integrity selftest cell.** Replace
`no self-invocation mode; inherited gate-conformance limitation, not selftest credit`
with
`no self-invocation mode; gate-conformance limitation (round-32 routed defect 3, open: add a fixture selftest or re-register as probe), not selftest credit; able-to-fail shown on the wave-1 amended-predictions clone; usage errors also exit 2`

**E4 — SKILL.md:1083, final-c1-witness row, pins/write-scope cell.** Replace
`frozen C1 carrier/prediction hashes and capture hashes in .ufo/waves/round-32/a2residual/FinalC1Measure.md; caller scratch output only; kaidoku`
with
`frozen C1 carrier/prediction hashes and capture hashes in .ufo/waves/round-32/a2residual/FinalC1Measure.md; <CARRIER-DIR> is the live pinned carrier set (scratch, uncommitted; rebuild via the carrier builder and verify against carriers.tsv), <SCRATCH> holds copies of carriers.tsv/predictions.tsv and receives compare-own.json; uncaught exceptions exit 1 = failed; kaidoku`

**E5 — SKILL.md:1077, retained-witness paragraph.** Append after `...not a frozen claim counter or a semantic/runtime capability.`:
` Committed sibling secondary_evidence.py (same BASE; reads indep.json plus the carrier bytes) produced the secondary-directory placement/reference evidence in A2PEIndependent.md:141; it is an evidence producer with no verdict or self-invocation. compare.py also shells llvm-readobj --version for its payload field and takes no argv (all inputs hard-coded at lines 19-20).`

**E6 — SKILL.md:1084, quote-replay row, verdict cell.** Append:
`; replay is fixed to the script's absolute SNAP/C1IN lane paths; an internal assert failure exits 1 (indistinguishable from check failure)`

**E7 — SKILL.md:1045, c2-sqlite-refusals exit-codes cell.** Append:
`; measure presupposes the built mutant tree under /fast/scratch/hyaku/kaidoku-r31/ (predictions.tsv path column, base_of() literal) — absent/altered mutants or siblings exit 2`

**E8 — SKILL.md:1048, cited-runs-gate selftest cell.** Replace
``--selftest` 17 cases; round-30 report exit 1`
with
``--selftest` 17 cases (builds and removes a throw-away git repo under tools/round-31/, kept with --keep-selftest); round-30 report exit 1`

**E9 — SKILL.md:1069/1070, c2 calibration rows, entry command.** Append to both commands:
` [--fleet <FLEET>] (defaults to the workspace parent; reads MANIFEST.json at fleet pin cef00867)`

**E10 — SKILL.md:1071, arm64x_oracle entry.** Replace `exceptions/nonzero could-not-evaluate` with `exceptions exit 1 (could-not-evaluate; no failure predicate is defined for a probe)`.

## 3. Residual risk and verification gaps

- No command was executed (read-only audit per contract); all claims rest on source reads at `428315a8`, not exercised runs. Exit-code behavior for uncaught exceptions (M1/E1) is inferred from unhandled exception paths in `measure()`/`main()` — no try/except wrapper exists — `[INFERENCE]` on the exact traceback text only, not on exit 1 itself.
- Replay of all three archived witnesses currently still works (scratch dirs exist as of 2026-10-23), but none of that is durable evidence; the registry's "restore captures" instructions assume scratch persistence that prep contracts do not guarantee.
- `pe_own_compare.py` and `compare.py` hard-code 12-carrier id lists/TSV shapes — replay on a different carrier set silently checks nothing new (bounded to frozen labels).
- The round-31 table's 5-column schema lacks a write-scope column; several of the surgical edits compensate inside cells. A future schema lift (add pinned-value/write-scope columns) would make E2/E7/E8 redundant.
- Frozen claims files remain the only admission authority: `claims.json` pins c1 counter/oracle/builder/carriers; `claims-v3.json` pins the v3 counter and freeze-integrity itself. Registry prose must never be used as a predicate substitute — consistent with "never reuse C2v3 for admission".

Trailer: `.ufo/waves/round-33/prep/R33RegistryAudit.md`
