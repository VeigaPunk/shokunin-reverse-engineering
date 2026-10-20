HOLDS — both runner selftests pass at REV b2aad08ceeee8dd125ce0d316056d8bd766c7f94 and each demonstrably reports failure (exit 1, `SELFTEST: FAILED …`) when product code is mutated.

# Scope

Re-run `.ufo/waves/round-17/tools/carrier-run.py --selftest` and `bash .ufo/waves/round-18/run-carriers.sh --selftest`; verify the selftest can fail (forced red on a /tmp copy). Lane HEAD verified = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (`git rev-parse HEAD`).

# Commands and exit codes (OBSERVED)

Byte-identity to REV first:

    $ git show b2aad08:.ufo/waves/round-17/tools/carrier-run.py | sha256sum
    6665dc7a59bda891a8dc72608da552cbc327cd81ef6ea9dd588c711f707d412c  -
    $ sha256sum .ufo/waves/round-17/tools/carrier-run.py
    6665dc7a59bda891a8dc72608da552cbc327cd81ef6ea9dd588c711f707d412c  (identical)
    $ git show b2aad08:.ufo/waves/round-18/run-carriers.sh | sha256sum
    9034e243a735dc2db9be941849eaa96a17382f79c37728794b8012634fb0706b  -
    $ sha256sum .ufo/waves/round-18/run-carriers.sh
    9034e243a735dc2db9be941849eaa96a17382f79c37728794b8012634fb0706b  (identical)

Green runs (OBSERVED):

    $ python3 -I -B .ufo/waves/round-17/tools/carrier-run.py --selftest
    SELFTEST: CLEAN cases=3
    EXIT=0

    $ bash .ufo/waves/round-18/run-carriers.sh --selftest
    SELFTEST: CLEAN cases=21
    EXIT=0

Forced red on /tmp copies — product code mutated, selftest assertions untouched (OBSERVED):

**MutA** — `carrier-run-mutA.py` line 421: `receipt["mid_run_drift_steps"] = mid_drift` → `= []` (drift recorded but not attributed to steps; run() still exits 1):

    $ sed -i '421s/mid_drift/[]/' carrier-run-mutA.py
    $ python3 -I -B carrier-run-mutA.py --selftest
    SELFTEST: FAILED case3 mid-run drift map: code=1
    EXIT=1

**MutB** — `carrier-run-mutB.py` line 434 (nonzero-analyze/timeout path): `return receipt, 2` → `return receipt, 0`:

    $ sed -i '434s/return receipt, 2/return receipt, 0/' carrier-run-mutB.py
    $ python3 -I -B carrier-run-mutB.py --selftest
    SELFTEST: FAILED case2 nonzero analyze: code=0
    EXIT=1

**MutC** — `run-carriers-mutC.sh` line 207 (label selector): `[ -n "$only" ] && [ "$only" != "$label" ] && continue` → unconditional `continue` (processes no rows):

    $ sed -i '207s/.*/  continue  # MUTATION: selector broken/' run-carriers-mutC.sh
    $ bash run-carriers-mutC.sh --selftest
    SELFTEST: FAILED selector-run compare.json present (expected 0, got 1)
    SELFTEST: FAILED selector-run producer.json present (expected 0, got 1)
    SELFTEST: FAILED producer.json has branch_tip (expected 1, got )
    SELFTEST: FAILED producer.json has tool_sha256 (expected 1, got )
    SELFTEST: FAILED producer.json parses (expected 0, got 1)
    SELFTEST: FAILED producer.json records all 7 tools (expected 7, got )
    SELFTEST: FAILED mixed-run exit (expected 1, got 0)
    SELFTEST: FAILED fakeA carrier-run exit (expected 0, got )
    SELFTEST: FAILED fakeA compare exit (expected 0, got )
    SELFTEST: FAILED fakeBad compare exit (expected 1, got )
    SELFTEST: FAILED fakeNoPred carrier-run exit (expected 2, got )
    SELFTEST: FAILED fakeBadSha carrier-run exit (expected 2, got )
    SELFTEST: FAILED fakeBad producer.json present (expected 0, got 1)
    SELFTEST: FAILED rm-guard exit (expected 1, got 0)
    SELFTEST: FAILED cases=21 fails=14
    EXIT=1

    (Interesting byproduct: skipping every row leaves `overall=0`, so an all-skip returns
    green — the "mixed-run exit (expected 1, got 0)" line. The selftest catches it via the
    missing-artifact chks, not via exit code alone.)

**MutD** — `run-carriers-mutD.sh` line 239 (sha256-mismatch skip): `if [ "$actual" != "$expected" ]` → `if false`:

    $ sed -i '239s/.*/    if false; then  # MUTATION: sha-mismatch skip disabled/' run-carriers-mutD.sh
    $ bash run-carriers-mutD.sh --selftest
    SELFTEST: FAILED fakeBadSha carrier-run exit (expected 2, got 0)
    SELFTEST: FAILED fakeBadSha has no compare.exit (expected 1, got 0)
    SELFTEST: FAILED cases=21 fails=2
    EXIT=1

/tmp mutation copies removed after use; `carrier-run.py`'s selftest already removes its own `carrier-run-selftest-*` root and `run-carriers.sh` its `r18-run-carriers-selftest.*` root (OBSERVED: no residue under /tmp).

# Path:line anchors (REV b2aad08)

- `carrier-run.py` `_selftest()` at `.ufo/waves/round-17/tools/carrier-run.py:539-722`: 3 cases — happy path (632-659, asserts log retention after session-dir deletion, evidence_id capture, pin equality, pin-check map files, baseline-dir exclusion), nonzero analyze → code 2 (663-678), mid-run carrier drift → code 1 + `mid_run_drift_steps == ["analyze"]` + retained pin maps (683-715). Failure reporting: `SELFTEST: FAILED …` + `return 1` at 718-720; `SELFTEST: CLEAN cases=%d` at 721.
- `_selftest` never spawns REA/npx: docstring 540-544; fake children run under `sys.executable` (619-622, 665-668, 689-692); `_DoneProc` stubs at 81-94.
- `run-carriers.sh` `selftest()` at `.ufo/waves/round-18/run-carriers.sh:32-165`: stub tools written to a mktemp root (46-84), `chk` accumulator at 40-41, `SELFTEST: FAILED cases=$cases fails=$fails` + `return 1` at 159-162, `SELFTEST: CLEAN cases=$cases` at 163-164. Dispatch at 167-170.
- Mutated product lines: `carrier-run.py:421` (`mid_run_drift_steps`), `carrier-run.py:434` (drift/nonzero-analyze exit split at 430-441), `run-carriers.sh:207` (selector guard), `run-carriers.sh:239-242` (sha-mismatch skip).
- Selftest isolation claims hold at REV: `run-carriers.sh` header comment 14-18 ("never touches LANE beyond reading the Go data dir listing and a read-only `git rev-parse`, and never invokes REA"); the mutated-line list above shows all env overrides (`TOOLS_DIR`, `PREDICTIONS_DIR`, `SWISS_MISREAD`, `SELECTION_PY`, `SUMS`, `RUNS_DIR`) are honored at 24-28 and 112-114.

# Verdict basis

- OBSERVED: both selftests exit 0 on REV-identical bytes; all four product-code mutations produce `SELFTEST: FAILED` with exit 1. The check suite is falsifiable — it detects behavioral regressions in `run()` exit codes, drift attribution, the label selector, and the sha-mismatch skip, and it detects missing output artifacts (`carrier-run.exit`, `compare.exit`, `producer.json`) rather than relying on exit codes alone.
- OBSERVED (minor, worth noting not blocking): in MutC the skip-all path exits 0 because `overall` stays 0 — a run that silently processes nothing is green by exit code; the selftest still catches it via artifact checks (14 fails). Whether a zero-processed-row run *should* be red is a design question the tsv-shape checks (exit 2 on zero rows) partially address only for empty files, not for selector misses. [INFERENCE: a selector matching zero labels silently skips; the script writes no diagnostic for "selector matched nothing".]
- INFERENCE: `carrier-run.py` selftest coverage is behavioral, not exhaustive — e.g. `_stop_group` SIGKILL escalation, `PIN_CHECK_S` interval checks inside a long step, and `LogPoller` copy-backpressure paths are not directly exercised; a mutation confined to those could escape. No such latent break observed.
- Blockers: none. No tools installed (all needed binaries already present; pacman untouched).
