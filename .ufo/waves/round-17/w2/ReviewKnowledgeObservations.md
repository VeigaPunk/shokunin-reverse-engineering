# ReviewKnowledgeObservations — retained-run verification of the round-17 Go-carrier entry

Seat: `KaidokuR17.ReviewKnowledgeObservations` (author-side advisory, leaf). Revision
`da64646adcb19c1ede7537b799b8c7d283fe43da`. Read-only: no REA `analyze`/`search`/`decompile`, no
Ghidra/`analyzeHeadless`, no carrier execution, no installs; scratch files under `/tmp`. Commands
below run from `kaidoku-shokunin/` unless a path says otherwise.

**Verdict.** Every cell of the Observations table (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:49-58`)
and every one of the five OBSERVATION bullets (`:68-96`) reproduces from the retained receipts,
`inspect-go.json`, `analyze.json`, `observation.json`, `compare.json` and the retained
`ghidra.log`s. The defects are in the surrounding provenance claims: at `da64646` the
documented recheck cannot return success, its rerun deletes the comparand, the freeze hash is
unresolvable, the `inspect-go-binary` Evidence ID is not in the receipt, and the mid-run pin
claim has no positive record. No measured table value is false.

## Findings

### F1 — HIGH (calibration/provenance) — the documented recheck is INVALID on all eight receipts

Target: `knowledge …r17….md:3` (the `recheck:` line).

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py \
    .ufo/waves/round-17/runs/calib-shfmt/receipt.json; echo exit=$?
{
  "counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0},
  "exit": 1,
  ...
  "receipts": [{
    "checks_performed": 306,
    "findings": [{"code": "unrecognized_shape",
                  "detail": "receipt matches neither retain nor carrier shape",
                  "where": "$"}],
    "kind": "unknown", "receipt": "runs/calib-shfmt/receipt.json",
    "status": "invalid", "valid": false}],
  "tool": "receipt-validate.py"
}
exit=1
```

All eight labels produce the same `unrecognized_shape`, 306 checks, exit 1
(`calib-shfmt`, `calib-esbuild-0.25.12`, `pro-notesmd-cli`, `pro-aether`,
`pro-esbuild-0.21.5`, `pro-containerd-shim`, `pro-esbuild-0.27.7`, `pro-op`).

Cause (observation): `tools/receipt-validate.py:98-101` classifies a carrier receipt only when
`receipt["steps"]` is a **list**; `tools/carrier-run.py:309` initialises `steps = {}` and
`:312`/`:331` write keyed entries (`inspect-go-binary`, `analyze`). `receipt-validate.py:284`
then iterates `steps` as a list. The validator's selftest fixture is a list
(`receipt-validate.py:470`), so the producer's actual shape is never exercised.

The generic walk still verifies the receipt's digest/size fields (`receipt-validate.py:369`,
306 checks) and reports **no** `sha256_mismatch`; the data is digest-consistent. The only finding
is the shape classification, but the tool's exit 1/`invalid` is what a reader of `:3` will see.
`verify.py:93` (untracked at `da64646`, present in the working tree) expects exit 0, so the integration verifier would record eight failures; the
capability condition in `claims.json` C2 ("+1 only if … its receipt validates") is blocked.

Smallest fix: in `receipt-validate.classify`, accept `steps` as a dict and iterate
`steps.items()` (keyed `where`) in `check_required`; or write a list from `carrier-run.py` and
update its consumers. Re-run the eight receipts and retain the passing outputs.

Revision note (observation): the command/output above are at the target revision `da64646`.
While this review ran, the working tree gained an uncommitted fix to `receipt-validate.py`
(`git status` shows `M`; `classify` accepts dict and `_iter_steps` handles both shapes). With
that working-tree version, all eight receipts now return `valid: 1`, exit 0, and
`--selftest` prints `SELFTEST: CLEAN cases=7`. If the change is committed, F1 is resolved; the
finding stands for the revision named in the assignment.

### F2 — HIGH (provenance) — the recheck's second step deletes the comparand

Target: `knowledge …r17….md:3` ("rerun one carrier with `bash …/run-carriers.sh <label>` and
compare `observation.json` fields").

```
$ git show da64646:.ufo/waves/round-17/run-carriers.sh | nl -ba | sed -n '14,15p'
    14  out="runs/$label"
    15  rm -rf "$out"; mkdir -p "$out"
```

Following `:3` literally removes `runs/<label>` — receipt, retained logs, `observation.json` —
before the new run; the "compare" then has no original. At `da64646` there is no output-dir
override; the working tree's uncommitted `RUNS_DIR` addition is not in the revision. The run is
committed, so git can restore it, but the documented sequence silently destroys the comparand.

Smallest fix: recheck via a copy (`cp -a runs/<label> /tmp/kr17-recheck-<label>`; compare
`/tmp/.../observation.json` to the committed `runs/<label>/observation.json`), or add
`RUNS_DIR`/`--out-dir` at the revision and document `RUNS_DIR=/tmp/...`; alternatively make the
script refuse a non-empty output directory. (The working tree already carries the `RUNS_DIR`
hunk; commit it and use `RUNS_DIR=/tmp/...`, or use the copy-first recheck.)

### F3 — MEDIUM (provenance) — the freeze commit is cited by an unresolvable hash

Target: `knowledge …r17….md:37`; same string in `run-carriers.sh:2` (committed at `da64646`).

```
$ git rev-parse --verify 2716747^{commit}
fatal: Needed a single revision          # exit 128
$ git rev-parse --verify 2711674^{commit}
271167473d87ef710f07ecdd98caf0ce12091686
$ git show -s --format='%ci %H' 2711674
2026-10-20 10:46:45 -0300 271167473d87ef710f07ecdd98caf0ce12091686
```

`knowledge …:1` already carries the full correct hash; `:37` contradicts it. Fix: replace
`2716747` with `2711674` (or the full 40-hex) in both sites.

### F4 — MEDIUM (calibration) — 0.27.7's "hand prediction matched" is vacuous under `compare.py`

Target: `knowledge …r17….md:83` ("The hand prediction matched") and `:47` ("compare exit 0").

```
$ head -n 62 runs/pro-esbuild-0.27.7/logs/rea-ghidra-DjvEp2/ghidra.log > /tmp/kr17-0277-trunc.log
$ python3 -I -B tools/log-extract.py --log /tmp/kr17-0277-trunc.log > /tmp/kr17-0277-trunc.obs.json
$ python3 -I -B tools/compare.py --prediction predictions/pro-esbuild-0.27.7.prediction.json \
    --observation /tmp/kr17-0277-trunc.obs.json; echo exit=$?
# extract exit 0; observation: go_lines 0, classification no_go_analysis,
# bootstrap_attempts 0, analyzer_errors [], snapshot_route none
# compare exit 0; all_match True; untested_version/snapshot_label/
# missing_bootstrap/snapshot_route/fallback_to all True
```

`compare.py:39,43` compares only the five fields. The hand prediction's discriminating
expectations are in `predictions/pro-esbuild-0.27.7.prediction.json` `extra_expectations`
(`bootstrap_attempts_at_least: 1`, `analyzer_errors_contain: "unable to get GoRttiMapper"`,
`language_compiler`, `invalid_version_strings`) and are not checked. Observation: the **real**
log does satisfy them (log lines 63/64 and 68/69; `observation.json` `bootstrap_attempts: 2`,
two analyzer errors), so the claim is true by inspection, but the retained automated check
cannot fail on a log with no Go analysis. The table's 0.27.7 cells are correct; the
"matched" claim overstates the tool evidence. Fix: have `compare.py` evaluate the extras (or
at least `classification != no_go_analysis` and `bootstrap_attempts >= 1`), or qualify `:83`
as "matched by inspection; the five compare fields are all-absent for this route".

### F5 — MEDIUM-LOW (calibration) — "before any run" is false for the pilot

Targets: `knowledge …r17….md:1` ("predictions frozen … before any run") and `:37` ("before the
first run").

```
$ git show -s --format='%ci' 2711674
2026-10-20 10:46:45 -0300
$ sed -n '1p' .ufo/waves/round-17/pilot/README.txt
Round-17 L1 pilot (2026-10-20 ~10:17-10:19 -03), NOT the final measured runs.
$ head -2 .ufo/waves/round-17/pilot/shfmt-log/ghidra.log | tail -1
2026-10-20 10:17:28 INFO  (LoggingInitialization) Using log file: /tmp/rea-ghidra-LuPZRm/ghidra.log
```

The two calib carriers were `analyze`d in the pilot at ~10:17–10:19 -03, ~28–29 minutes before
the prediction commit; the pilot's `analyze` JSONs are byte-identical to the final runs
(`sha256sum`: `271ced90…` for shfmt, `1904619c…` for 0.25.12) and supply the quoted IDs. The
predictions are prospective for the eight measured runs, not for "any run". The entry discloses
the pilot at `:38`, so the six `pro-*` prospective claim stands; the absolute wording does not.
Fix: "before the eight measured runs" and "before the first measured run".

### F6 — LOW-MEDIUM (provenance) — `inspect-go-binary` Evidence IDs are not in `receipt.json`

Target: `knowledge …r17….md:60-61` ("REA `inspect-go-binary` and `analyze` Evidence IDs … are in
each `runs/<label>/receipt.json`").

```
$ python3 -I -B -c "import json; r=json.load(open('.ufo/waves/round-17/runs/calib-shfmt/receipt.json')); \
  print('inspect', 'evidence_id' in r['steps']['inspect-go-binary'], \
        'analyze', 'evidence_id' in r['steps']['analyze'])"
inspect False analyze True
```

All eight receipts: inspect `False`, analyze `True`. The inspect ID is in
`runs/<label>/inspect-go.json` (`ev_f8ef12a8…` for shfmt) and in
`predictions/<label>.inspect-go.json`; `carrier-run.py:333` parses only the analyze stdout.
Smallest fix: reword to "the `analyze` Evidence ID (the `inspect-go-binary` ID is in the
referenced `inspect-go.json`)", or record the inspect ID in the receipt's inspect step.

### F7 — LOW (calibration) — "no mid-run check differed" has no positive record

Target: `knowledge …r17….md:26-30`.

```
$ grep -rn 'pins_changed_during_run' .ufo/waves/round-17/runs; echo exit=$?
exit=1            # 0 matching lines
$ nl -ba .ufo/waves/round-17/tools/carrier-run.py | sed -n '412,433p'
  412  last_pin_check = 0.0
  425  if now - last_pin_check >= PIN_CHECK_S:
  427      mid = pins.snapshot(pin_paths)
  428      cmp_mid = pins.compare(pins_pre, mid)
  429      if not cmp_mid["equal"]:
  430          rec["pins_changed_during_run"] = { … }
```

The 30 s checks run (the first fires at loop entry), but a receipt records only a mismatch. The
number and timestamps of the checks are never retained, so "no mid-run check differed" is an
absent-key inference, not a recorded positive. This is the kind of temporal claim QUALITY #19 is
about. Fix: record `mid_checks: {count, last_taken_at_utc, last_equal}` (or at least the count)
in the polled step, or reword `:28-29` to "mid-run checks record only differences; none was
recorded". (The working-tree validator now checks `pin_checks` when present, but
`carrier-run.py` writes none; the positive record is still absent.)

### F8 — LOW (provenance) — the only sequential runner log covers 7/8 runs

Target: `knowledge …r17….md:2` ("run sequentially by the round-17 L1").

```
$ git show da64646:.ufo/waves/round-17/runs/run-log.txt | head -1
== calib-esbuild-0.25.12 start 2026-10-20T10:47:42-03:00
$ python3 -I -B -c "import json; r=json.load(open('.ufo/waves/round-17/runs/calib-shfmt/receipt.json')); \
  print(r['pins_pre']['taken_at_utc'], r['steps']['analyze']['started_at_utc'], r['steps']['analyze']['ended_at_utc'])"
2026-10-20T13:47:05.973725+00:00 2026-10-20T13:47:06.688621+00:00 2026-10-20T13:47:37.309101+00:00
```

The shfmt run (13:47:06–13:47:37Z) precedes the log's first entry (13:47:42Z) but is absent from
`run-log.txt`. The receipt and `.exit` files prove it; the claim "sequentially" is supported by
the receipt timestamps, not by the runner log. Fix: add the shfmt lines or a note that the
receipt is authoritative for the first run.

## Bounded no-findings (every table cell and observation checked)

I checked all 8 rows × 6 columns against `receipt.json`, `inspect-go.json`, `observation.json`,
`compare.json`, `analyze.json`, `pacman -Qo/-Q`, `go version -m`, and the retained
`ghidra.log`. No cell differs.

| label | sha256[:16] / package | build-info Go | predicted | observed log anchors | bootstrap / counts |
|---|---|---|---|---|---|
| calib-shfmt | `58f765638eed5309`, shfmt 3.14.1-1 | `go1.27.0-X:nodwarf5` | none, 1.27.0 | 82-89 | missing ×2 |
| calib-esbuild-0.25.12 | `bab29b2ca7a9e89b`, pnpm 0.25.12 | `go1.23.12` | info | 62-66, 83 | 4881 types; 6264 strings |
| pro-notesmd-cli | `412dc532d278b9e4`, no owner | `go1.25.8` | fallback → 1.25.0 | 67-71, 85 | 2302 types; 3229 strings |
| pro-aether | `06c91f55df4117e5`, aether 4.32.0-2 | `go1.25.14` | fallback → 1.25.0 | 91-97, 177, 207 | 6115 types; 7200 strings |
| pro-esbuild-0.21.5 | `b567f467fdac92c6`, pnpm 0.21.5 | `go1.20.12` | info | 61-65, 82 | 4411 types; 6010 strings |
| pro-containerd-shim | `d3aa80d720b80f70`, containerd 2.4.2-1 | `go1.27.2-X:nodwarf5` | none, 1.27.2 | 240-247 | missing ×2 |
| pro-op | `f4ac474fd0202c73`, 1password-cli 2.41.0-1 | `go1.26.8` | none, 1.26.8 | 68-75 | missing ×2 |
| pro-esbuild-0.27.7 | `c638273fcf95573c`, pnpm 0.27.7 | `build_info: null` | hand none | 63-69 | no mapper; 2 Reading, 2 analyzer errors |

Specific checks that held:

- **Carrier/package:** `pacman -Qo` returns `shfmt 3.14.1-1`, `aether 4.32.0-2`,
  `containerd 2.4.2-1`, `1password-cli 2.41.0-1`; notesmd has no owner; the esbuild paths are
  the kimi-code pnpm trees. `go version -m` on all 8 returns the table's build-info versions
  (`go1.27.0-X:nodwarf5`, `go1.23.12`, `go1.25.8`, `go1.25.14`, `go1.20.12`,
  `go1.27.2-X:nodwarf5`, `go1.26.8`; 0.27.7: "not a Go executable").
- **Build-info / route:** `inspect-go.json` `normalized_result.build_info.go_version` matches;
  0.27.7 `build_info` is `null`. `predictions/*.prediction.json` `expected.snapshot_route`
  matches the table; `selection.status` is `exact_diff` (0.25.12, 0.21.5), `base_only`
  (notesmd, aether), `missing_base` (shfmt, containerd, op), `null` (0.27.7).
- **Observed lines:** shfmt 82-89 (Reading, Untested ×2, Missing ×2, two analyzer errors);
  0.25.12 62-66, 83 (`GoApiSnapshot` INFO 1.23.12, echo, 4881, strings 6264); notesmd 67-71, 85
  (fallback WARN 1.25.8 → 1.25.0, echo, 2302, strings 3229); aether 91-97, 207 (fallback
  1.25.14 → 1.25.0, echo, 6115, failure, strings 7200); containerd 240-247; 0.21.5 61-65, 82
  (INFO 1.20.12, 4411, strings 6010); op 68-75; 0.27.7 63-69 (two Reading, two
  `unable to get GoRttiMapper`, no version/untested/invalid/bootstrap).
- **Nit, not a finding:** the three out-of-range rows quote `Untested Go version [X]` once, but
  the logs contain it twice (82-89, 240-247, 68-75); the `×2` is only on the `Missing` line. The
  `bootstrap_attempts = 2` bullet makes the repetition clear; adding `×2` to `Untested` would be
  exact.
- **Aether failure:** log 97 `Go analysis failure java.io.IOException:
  java.lang.reflect.InvocationTargetException`; 124 `GoInterfaceType.additionalMarkup`; 177
  `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854`; 207
  `Go strings found: 7200`. The cited `:97-177` covers the failure line, the interface frame and
  the cause line (the EOF stack continues to 198, but both quoted anchors are in range).
- **Compare:** all eight `compare.json` have `all_match: true`; `observation.json`
  `language_compiler` is `x86:LE:64:default:golang` for all 8; `snapshot_route` matches the
  table for all 8.
- **Evidence IDs:** the quoted analyze IDs match `analyze.json` (`ev_2b29…` shfmt, `ev_4fd3…`
  notesmd); the pilot `pilot/shfmt.json`/`pilot/esb.json` IDs equal the final runs, and the
  analyze JSON files are byte-identical (sha above).
- **Pins:** all 8 receipts have 146 `pins_pre` entries = carrier + r16 `selection.py` +
  `<label>.prediction.json` + all 143 files under the installed
  `Ghidra/Features/Base/data/typeinfo/golang` (no unpinned file; no `error` entries); all 8
  `pins_compare.equal` true, no changed/missing/errors; windows 13:47:05–14:00:05Z.
- **Binding:** for all 8, the retained `ghidra.log` line 2 names its own
  `<session>/ghidra.log`, and `IMPORTING:` names `<session>/target-<carrier sha[:12]>.bin`;
  one bound session, zero unbound.
- **Provider:** `analyze.json` `analysis_profile.parameters.upstream_analysis_profile.provider`
  is `ghidra 12.1.4`; argv is `npx -y rea-agents@6.5.0 analyze …`; every analyze step exit 0;
  every `carrier-run.exit` and `compare.exit` is 0.
- **Source anchors re-read from `Base-src.zip`:** `GoRttiMapper.java:79` (`1.15-1.25`),
  `:102-128` (shared property + Reading), `:170-172` (only logs), `:179-180` (request echo),
  `:351-361` (constructor throws `Missing Go bootstrap type info`); `GoApiSnapshot.java:111`,
  `:122-126` (no base), `:148-166` (WARN fallback / INFO exact); `GoBuildInfo.java:488-489`
  (strip `go`); `GoVer.java:62-81` (parse); `TransientProgramProperties.java:107-110` (null not
  cached); `ElfLoader.java:188-200` (section-name → golang cspec);
  `GolangSymbolAnalyzer.java:135` / `GolangStringAnalyzer.java:105` (null mapper error).
- **Hand prediction / probe:** `predict.py --go-version ''` exits 2 with
  `{"error": "unparseable Go version '' (post-strip ''): GoVer.INVALID", "input": ""}`;
  `buildinfo-probe.py` on 0.27.7 exits 0 with `found:false`, `go_version:null`,
  `magic_file_offsets: []`, and on shfmt reports `go1.27.0-X:nodwarf5` at 3515584. The
  "absent build info" observation is source-consistent (`readelf -S` shows `.gopclntab`,
  `.gosymtab`, `.go.fipsinfo` and no `.go.buildinfo`).
- **Historical claims:** no `ghidra.log` exists anywhere in the lane outside
  `.ufo/waves/round-17/`, so "no analyzer log had ever been retained" holds for the repo;
  r4-10's "observed-not-cited" wording is at
  `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:72-73`.

## Residual risk / verification gaps

- **Sample:** one run per carrier; the analyze-ID repeat is one content-identical pair
  (pilot/final analyze JSON byte-identical), not a determinism proof. The entry says this.
- **Route coverage:** the decision-table row `:103` says "a lower patch (or the base)"; the
  runs observe only the base fallback (1.25.8/1.25.14 → 1.25.0). No `fallback_diff`/lower-patch
  observation exists, and the installed data has no 1.25 patch diffs. The "lower patch" half is
  source-only; the "Not examined" section should say so.
- **Discrimination:** sibling `w2/CriticC2Depth.md` F3 computes 36 of 40 field matches from a
  naive version-string-plus-range model; the only non-trivial route test is the two 1.25.x
  base fallbacks. The entry's "prediction before observation" is honest, but the 8/8 tally
  overstates independent tests.
- **Aether EOF:** cause remains UNKNOWN; the same 1.25.0 fallback on `pro-notesmd-cli` did not
  fail (`observation.json` `analyzer_errors: []`; log 68, 77-78, 82), so the fallback data is
  not sufficient. The entry hedges correctly; adding that control would tighten it.
- **Mid-run / run-log:** F7 and F8 above; the pre/post pins are the only fully retained pin
  records.
- **Validator:** F1 means the retained receipts are not validator-clean at `da64646`; the
  digest checks I relied on are the validator's 306 generic checks plus the actual log bytes.
  No evidence changed as a result, but the capability/C2 condition is not met until the
  working-tree fix is committed and the recheck is re-run.

## Commands (read-only; representative)

`receipt-validate.py` on all 8 receipts; `log-extract.py` on all 8 retained `ghidra.log`s;
`compare.py` on all 8 predictions/observations; `buildinfo-probe.py` on 0.27.7 and shfmt;
`predict.py --go-version ''`; `sha256sum -c predictions/SHA256SUMS`; `git rev-parse/show` for
`2711674`/`2716747`; `pacman -Qo/-Q`; `go version -m` on all 8 carriers; `readelf -S` on 0.27.7;
`unzip -p Base-src.zip` for the Java anchors; `grep -rn pins_changed_during_run`; and `git show
da64646:…` for the committed script/receipt anchors. No REA analyze/search/decompile, no Ghidra,
no carrier execution, no network, no installs.
