# RunCalibesbuild02512 — falsify: retained run `calib-esbuild-0.25.12`

Target: `.ufo/waves/round-17/runs/calib-esbuild-0.25.12/` at lane revision
`da64646adcb19c1ede7537b799b8c7d283fe43da`. Committed state is what is cited; a peer's
uncommitted `RUNS_DIR` edit to `run-carriers.sh:14` and the untracked `verify.py` (both
appearing mid-wave) are called out where used and touch no other cited line.
Axes: calibration, depth. Read-only: no carrier executed, no REA analyze/search/decompile,
no Ghidra; scratch under `/tmp`; no tools installed or upgraded.

## Findings (severity order)

### F1 — HIGH (calibration): `receipt-validate.py` cannot validate **any** carrier-run receipt; the round's pending gate is guaranteed to fail

`receipt-validate.py:98-100` classifies a carrier receipt only when `steps` is a **list**;
`carrier-run.py:275,309,349` always emits `steps` as a **dict** keyed by step name
(`steps["analyze"]`, `steps["inspect-go-binary"]`, `steps["search:*"]`). The two tools' own
selftests encode the contradictory shapes and both pass:
`receipt-validate.py:470` builds `"steps": [{...}]` (`SELFTEST: CLEAN cases=5`),
`carrier-run.py:555-558` reads `receipt["steps"]["analyze"]` (`SELFTEST: CLEAN cases=2`).

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py \
    .ufo/waves/round-17/runs/calib-esbuild-0.25.12/receipt.json
  "counts": { "invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0 },
  "exit": 1,
  "receipts": [ { "code": "unrecognized_shape",
                  "detail": "receipt matches neither retain nor carrier shape",
                  "kind": "unknown", "status": "invalid", "valid": false } ]
EXIT=1
```

All eight retained runs behave identically (per-receipt loop, exit 1 each,
`status=invalid kind=unknown ['unrecognized_shape']`): `calib-esbuild-0.25.12`, `calib-shfmt`,
`pro-aether`, `pro-containerd-shim`, `pro-esbuild-0.21.5`, `pro-esbuild-0.27.7`,
`pro-notesmd-cli`, `pro-op`.

Consequences, all direct:
- The L1's pending-pass script `verify.py` (present in the worktree, **untracked at
  `da64646`**, mtime 11:09:48 -03:00) runs `receipt-validate.py <run>/receipt.json` with
  **expected exit 0** for all eight labels (`verify.py:93`) and returns 1 when
  `unexpected_exits` is non-empty (`verify.py:178`). The "single post-integration execution
  pass" the LOG defers measured values to (`LOG.md:2066-2067`) therefore exits 1 on its first
  eight receipt checks, and `verification.json` is written with eight unexpected exits.
- The knowledge entry's own `recheck:` (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`)
  names this tool, so the documented recheck exits 1.
- The capability gate (`claims.json:22`; `corpus/lessons/round-17.md:17,26`) requires the
  receipt to validate; under this tool no carrier receipt can, so the gate is unsatisfiable.

Not an artifact-integrity problem: with the shape unrecognized, the validator still performed
306 checks (pins-compare rerun, pin entries, recursive digest walk) with **zero** digest/pin
findings — the only finding is the shape.

Smallest fix (two spots in `receipt-validate.py`, proven): accept a dict in `classify`
(line 98) and iterate step values in `check_required` (line 284), because iterating a dict
yields keys and would otherwise emit `field_type` findings:

```python
if isinstance(receipt.get("steps"), (list, dict)) and isinstance(receipt.get("carrier"), dict):
...
_steps = receipt.get("steps") or []
if isinstance(_steps, dict):
    _steps = list(_steps.values())
for index, step in enumerate(_steps):
```

I applied exactly this to a `/tmp` copy with a sibling `pins.py` and re-ran all eight receipts:

```
calib-esbuild-0.25.12 exit=0 valid carrier checks=336 []
calib-shfmt          exit=0 valid carrier checks=336 []
pro-aether ... pro-op (all eight) exit=0 valid carrier checks=336 []
```

(336 = 306 pre-existing checks + 30 required-field checks; no findings.) Add one selftest case
built from the real producer shape (or from `carrier-run.run()` with its fake runner) so the
two fixtures cannot drift again. Changing the producer to a list instead is the alternative
fix; it requires `carrier-run.py:275,309,349` plus its selftest assertions at `:555-558`.

### F2 — MEDIUM (calibration): the frozen-prediction commit is cited with an unresolvable abbreviation

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37` and
`.ufo/waves/round-17/run-carriers.sh:2` both say `2716747`. That object does not exist; the
real commit is `271167473d87ef710f07ecdd98caf0ce12091686` (prefix `2711674`).

```
$ git rev-parse --verify --quiet 2716747^{commit}; echo $?
1                      # no output, unresolvable
$ git rev-parse --verify 2711674^{commit}
271167473d87ef710f07ecdd98caf0ce12091686
```

The same file's front matter (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:1`)
and `corpus/lessons/round-17.md:26` carry the full correct hash, so this is a digit
transposition, not a provenance disagreement. Smallest fix:
replace `2716747` with `2711674` (or the full hash) at both sites. This is exactly the
citation-drift class the round's C1 claims to discharge, so it should not survive integration.

### F3 — LOW (calibration): the knowledge entry mispoints where the `inspect-go-binary` Evidence ID lives

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:60-61` claims
"REA `inspect-go-binary` and `analyze` Evidence IDs ... are in each
`runs/<label>/receipt.json`." Only the analyze ID is there.

```
$ python3 -B -c 'import json;r=json.load(open(".../runs/calib-esbuild-0.25.12/receipt.json"));
  print(list(r["steps"]["inspect-go-binary"]))'
['argv','cwd','ended_at_utc','exit','started_at_utc','stderr_path','stderr_sha256','stdout_path','stdout_sha256']
$ python3 -B -c '... inspect-go.json ...["evidence_id"]'
ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626
```

Smallest fix: "…`inspect-go.json` and `analyze.json` (the analyze ID is also in
`receipt.json`)" — or record `evidence_id` for the inspect step in `carrier-run.py`.

### F4 — MEDIUM (calibration, headroom): registry citations name a file that does not exist at HEAD, and C1(b)'s target count is currently unmet

`SKILL.md:448-449` state the exercised argv is "retained in `.ufo/waves/round-17/verification.json`";
that path is absent at the cited lane revision, and the lane's own audit reports the rows as
unlabelled:

```
$ git cat-file -e da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/verification.json
fatal: path ... does not exist     (EXIT=128)
$ python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root . --rev da64646a
counts {"rows":17,"exercised_match":6,"labelled_unexercised":0,"unlabelled_variant":11,...}
# baseline b563c79: {"rows":7,"exercised_match":5,"labelled_unexercised":0,"unlabelled_variant":2}
```

C1(b) (`claims.json:12`, falsifiable form at `claims.json:22`) states
"unlabelled-variant registry rows M -> 0"; at HEAD the
count is 2 -> 11, including `receipt-validate` (`SKILL.md:536`), `go-carrier-run`,
`go-log-extract`, `go-route-predict`, `go-route-compare`, `pins`, `temporal-sweep`,
`invocation-audit`, `go-buildinfo-probe`, `round17-structural-controls`, and `custody-pair`.
`LOG.md:2065-2066` already asserts "SKILL rows citation-drift/custody-pair aligned in place",
which the audit contradicts for custody-pair at this revision.

This is *partly* declared-pending: the pending pass records those argv and the audit would
then reach 0 (it matches argv presence, not exit status — see residual risk 3). But the
citations are unresolvable now, and with F1 the pass that creates the file exits 1. Smallest
fix, in order: fix F1; run the pass; confirm `unlabelled_variant == 0` and a green
`verification.json`; only then keep the past-tense alignment wording and the citations. Note
that `verify.py` itself and the `RUNS_DIR` line in `run-carriers.sh:14` are uncommitted worktree
edits made during this wave; only the committed state (no `verify.py`, `2716747` at
`run-carriers.sh:2`, `echo` as the loop's last command) is what `da64646` attests.

## Bounded no-finding — what I checked and found sound

1. **Log binding holds by the log's own bytes.** On the fresh extract
   (`log-extract.py --log .../logs/rea-ghidra-B5tAvn/ghidra.log` → exit 0,
   `classification: snapshot_loaded`, `log_sha256 e2b678fe…`, `log_bytes 11330`):
   line 2 `Using log file: /tmp/kr17-rea-1cqz92us/rea-ghidra-B5tAvn/ghidra.log`;
   line 46 `IMPORTING: file:///tmp/kr17-rea-1cqz92us/rea-ghidra-B5tAvn/target-bab29b2ca7a9.bin`.
   Session path equals the receipt's `retained_logs[0].session_dir`, and `bab29b2ca7a9` is
   `carrier.sha256_pre[:12]`. It is not a copied pilot log: the pilot's file is a different
   artifact (`sha256 f6b61152…`, session `/tmp/rea-ghidra-r9xmGu`, 10:18:19).
2. **Prediction provenance is genuine.** The prediction file's bytes equal the frozen commit:
   `git show 2711674:.ufo/.../calib-esbuild-0.25.12.prediction.json | sha256sum` and
   `sha256sum` of the worktree file both give `a551fa61e4785f8e011bc84bb7fa8e3158f05db2f1a84dfe4d6585fdbb90eb39`.
   Commit `%cI` 2026-10-20T10:46:45-03:00 = 13:46:45Z precedes
   `steps.analyze.started_at_utc` 2026-10-20T13:47:43.330377+00:00 by 58.33 s. The prediction
   is also inside the receipt's pre/post pin set and unchanged in both maps.
3. **Fresh compare reproduces the retained verdict.** `compare.py --prediction … --observation
   /tmp/r17cal-extract.json` → exit 0, `all_match: true`, 5/5 fields: `untested_version []`,
   `snapshot_label ["1.23.12"]`, `missing_bootstrap false`, `snapshot_route "info"`,
   `fallback_to []`. The retained `observation.json` has the same log digest and the same
   field values, so the retained compare was not curated relative to fresh extraction.
4. **The route field is a real discriminator, and the entry says so correctly.** In
   `GoApiSnapshot.java:148-166` (Base-src.zip), `getPatchVerDiffFile` logs
   `Msg.info("Using Go API snapshot for %s")` only when the requested patch diff was found
   (or patch is 0) and `Msg.warn("Falling back from …")` otherwise; no base JSON ⇒ `EMPTY`
   and no line. The log shows the INFO line from `GoApiSnapshot` (line 63) and the pinned
   `patchverdiffs/go1.23.12.json.diff` exists, so `info` is a genuine prediction of diff
   resolution, not an echo. The `GoRttiMapper` echo (line 64) is correctly labelled
   non-discriminating at `knowledge:41-45`, and `compare.py` marks `snapshot_label`
   non-discriminating in its own `rules`.
5. **The knowledge row matches the log** (`knowledge:52`): `bab29b2ca7a9e89b` = sha[:16];
   build-info `go1.23.12` = `inspect-go.json` `build_info.go_version` (log `Go version 1.23.12`,
   line 67); route `info`; `loaded; 4881 types` = `Found 4881 Go types` (line 66);
   `Using Go API snapshot for 1.23.12` (INFO) = line 63. Analyze Evidence ID
   `ev_391dbfe6…` matches `analyze.json` and `steps.analyze.evidence_id`.
6. **Receipt internals are consistent and honestly bounded.** 146 pins = 143 installed Go data
   files + carrier + r16 `selection.py` + frozen prediction (SKILL.md:532's "143" is exact);
   no pin errors; `pins_pre == pins_post` path sets; `pins_compare.equal true`; the mid-run
   divergence key (`pins_changed_during_run`, written only on mismatch at
   `carrier-run.py:427-433`) is absent in all eight receipts; `session_parent_leftovers`
   honestly records `["node-compile-cache"]` rather than claiming a clean `/tmp` (the parent
   directory still exists with only that entry).
7. **Log completeness for this run.** The retained log has 124 lines and includes
   `REPORT: Analysis succeeded for file: …target-bab29b2ca7a9.bin` (line 118) and the
   post-script lines (119-124, through `ReaGhidraBridge.java`). `knowledge:132-133` states the
   tail limit and confines absence claims to the last retained line; for this run the statement
   is satisfied.

## Residual risk / verification gaps (no artifact change requested)

1. **No completeness gate in the extractor/comparator.** `log-extract.py` and `compare.py`
   contain no `Analysis succeeded`/failure check, although w1 `draft-lesson-gate.md` S8 made a
   completeness check an admission condition. A future log truncated after the Go lines would
   still compare-pass while the analysis result is unknown. This run is not affected (item 7).
   Smallest follow-up: emit `analysis_succeeded` from `log-extract.py` and require it where the
   claim depends on absence, without turning the documented tail limit into a false failure.
2. **`run-carriers.sh` cannot fail.** Its loop ends with `echo` (`run-carriers.sh:30`), so the
   script exits 0 even when `carrier-run.py` records 1/2 in `carrier-run.exit`. Consequently
   `verify.py`'s `go-carrier-run-replicate` step (expect 0) is vacuous, and the SKILL row at
   `SKILL.md:532` advertises an exit map the wrapper does not propagate. Adjacent to the
   calib-shfmt seat; flagged here only because it weakens the same pending pass.
3. **`invocation-audit.py` classifies argv presence, not success.** A row matches even when the
   recorded command exited nonzero, so C1(b)'s "exercised" can be met by a failing run (F1's
   eight `receipt-validate-*` argv will match while exiting 1). This is a definitional limit of
   C1(b), worth stating wherever the audit count is presented as proof.
4. **`snapshot_label` cannot falsify** (request echo, disclosed). For this run the discriminating
   content is `snapshot_route`/`missing_bootstrap`; no overclaim was found, but the 5/5 "all
   fields match" headline is weaker than 5 independent confirmations.

## Environment

No installs or upgrades. Commands used: `python3 -I -B` on round-17 tools (`receipt-validate`,
`log-extract`, `compare`, `invocation-audit`, and `carrier-run --selftest`), `git`
(`rev-parse`/`show`/`cat-file`/`ls-tree`), `sha256sum`, `grep`/`sed`, and a `/tmp` copy of
`receipt-validate.py` for the fix proof. No carrier was executed, no REA analyze/search/decompile,
no Ghidra.
