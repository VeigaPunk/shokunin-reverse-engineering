# RunProesbuild0277 — attack on `runs/pro-esbuild-0.27.7` (wave 2, falsify)

Lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`; baseline
`b563c799d97774aae4351276fe43cb897311e349`; predictions frozen at
`271167473d87ef710f07ecdd98caf0ce12091686`.
Read-only: no REA `analyze`/`search`/`decompile`, no Ghidra/`analyzeHeadless`,
no carrier execution, no lane file edited but this report; scratch only under
`/tmp`; no installs or updates.

Observation: the worktree diverged during this review — `run-carriers.sh` is
`M` (uncommitted `RUNS_DIR` indirection) and `verify.py` is untracked. Every
anchor below is the committed blob at `da64646` (checked with `git show`);
where the worktree differs I say so.

## Findings

### F1 — HIGH (calibration / capability gate): the receipt gate is red on the target and on all eight retained carrier receipts

Exact target command (per assignment):

```sh
$ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py \
    /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/pro-esbuild-0.27.7/receipt.json
{
  "counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0},
  "exit": 1,
  "receipts": [{
    "checks_performed": 306,
    "findings": [{"code": "unrecognized_shape",
                  "detail": "receipt matches neither retain nor carrier shape",
                  "where": "$"}],
    "kind": "unknown", "status": "invalid", "valid": false
  }]
}
EXIT=1
```

(Excerpt: the shown values are verbatim; the full result also carries `tool`,
`pins_available`, `pins_path`, and each receipt's input path.)

Cause (observation, from source):

- The producer writes `steps` as a **mapping**: `tools/carrier-run.py:275`
  (`"steps": {}`), `:317`, `:349` (`receipt["steps"] = steps`), and its own
  selftest reads it as a mapping (`carrier-run.py:555-558`,
  `receipt["steps"]["analyze"]`).
- The validator accepts only an **array**: `tools/receipt-validate.py:98`
  (`isinstance(receipt.get("steps"), list)`), iterates with
  `enumerate(...)` at `:284`, and its carrier fixture is array-shaped at `:470`.
  With `kind == "unknown"` it appends `unrecognized_shape` and sets
  `required = []` (`:242-250`), so no required-field check runs.
- Both selftests are green because neither crosses the producer/validator
  boundary; `contract.md:43` names the fields but not the container type.

Bounded counterfactual (scratch copy, no lane edit): copying the receipt to
`/tmp/receipt-list-steps.json` and converting only `steps` dict→list gives
`kind: "carrier"`, `checks_performed: 336`, `findings: []`, `EXIT=0`. Every
digest, size and pin check therefore passes; the sole blocker is the container
type.

Scope (observation): the eight real receipts all fail the same way —

```sh
$ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py \
    /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/{calib-esbuild-0.25.12,calib-shfmt,pro-aether,pro-containerd-shim,pro-esbuild-0.21.5,pro-esbuild-0.27.7,pro-notesmd-cli,pro-op}/receipt.json
# summary of the emitted JSON (values verbatim):
{"counts": {"invalid": 8, "receipts": 8, "unreadable": 0, "valid": 0}, "exit": 1}
# kinds {'unknown'}, statuses {'invalid'}
```

Impact: C2's admission test is explicit — "capability rows 4 … -> +1 only if
the capture runs and its receipt validates" (`claims.json:22`), echoed by
`SKILL.md:536` and `w1/ReviewCapabilityTable.md:37`. The gate fails on the
lane's own receipts. The capability row is correctly **not** in `SCORECARD.md`
(verified absent), so this is not an overclaim; it is a blocked step plus a
broken recheck: the knowledge entry's `recheck:` command
(`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`) returns exit 1
today. Same defect independently found by `w2/RunProesbuild0215.md` F1.

Smallest fix: make one container canonical. Either accept mappings in
`classify`/`check_required`/iteration (`isinstance(..., (list, dict))`, iterate
`.values()` with stable `where` such as `$.steps.analyze`) and change the
validator's carrier fixture to `carrier-run.py`'s shape, or emit a list from
`carrier-run.py` and migrate the eight receipts. Add the cross-tool receipt to
at least one selftest so the two shapes cannot drift again, and name the
container in `contract.md:43`.

### F2 — MEDIUM (depth): the retained comparison for this carrier cannot fail on the hand prediction's distinguishing expectations

Observation: this is the only hand-written prediction, and its `expected` is
all absence — `untested_version: null`, `snapshot_label: null`,
`missing_bootstrap: false`, `snapshot_route: "none"`, `fallback_to: null`
(`predictions/pro-esbuild-0.27.7.prediction.json`). `compare.py`'s five rules
(`compare.py:45-51`) make every one of those match any observation that merely
lacks the signal. The four **positive** expectations the author wrote to
discriminate this route — `language_compiler`,
`invalid_version_strings`, `bootstrap_attempts_at_least`,
`analyzer_errors_contain` — are read by no tool:

```sh
$ grep -rn "extra_expectations" .ufo/waves/round-17/tools/*.py
# no output
```

(`predict.py` does not emit that key; normal predictions carry `expected` with
only the five compared fields.)

Bounded falsification of the comparator (three invocations, all against the
retained prediction):

```sh
# cwd = /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# 1. fresh extract of the retained log
$ python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log .ufo/waves/round-17/runs/pro-esbuild-0.27.7/logs/rea-ghidra-DjvEp2/ghidra.log > /tmp/fresh-extract.json
EXIT=0   # classification "other", bootstrap_attempts 2, two analyzer errors, snapshot_route "none"

# 2. variant A: no Go analysis at all
#    go_lines=[], analyzer_errors=[], bootstrap_attempts=0, classification="no_go_analysis"
$ python3 -I -B .ufo/waves/round-17/tools/compare.py --prediction .ufo/waves/round-17/predictions/pro-esbuild-0.27.7.prediction.json --observation /tmp/variant-no-go.json
all_match: true   EXIT=0

# 3. variant B: violates three extra_expectations
#    language_compiler="x86:LE:64:default", bootstrap_attempts=0, analyzer_errors=["something else"]
$ python3 -I -B .ufo/waves/round-17/tools/compare.py --prediction .ufo/waves/round-17/predictions/pro-esbuild-0.27.7.prediction.json --observation /tmp/variant-extra-false.json
all_match: true   EXIT=0
```

So the retained `compare.json` would also have been green if the binary had
produced no Go analysis at all, or an inconsistent compiler/attempt/error set.
The run's conclusion itself is **not** falsified: I checked the four extra
expectations by hand and they hold (see N4). What fails is the inference that
the retained comparison supports "The hand prediction matched"
(`knowledge:83`); it supports only the absence fields. The prose at
`LOG.md:2047` ("8/8 compare exit 0") inherits the same weakness for this
carrier.

Smallest fix: have `compare.py` evaluate `extra_expectations` when present
(equality for `language_compiler`, both-empty/contains for
`invalid_version_strings`, `>=` for `bootstrap_attempts_at_least`, substring for
`analyzer_errors_contain`), re-run it against the retained `observation.json`,
and keep the result in `compare.json`; alternatively, state in `knowledge:78-83`
and `LOG.md:2047` that this carrier's comparison is absence-only and the
positive checks were manual.

### F3 — MEDIUM (provenance): the pre-registration commit is cited as an object that does not exist

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37` and
`.ufo/waves/round-17/run-carriers.sh:2` both say `2716747`.

```sh
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -t 2716747
fatal: Not a valid object name 2716747
EXIT=128
```

The correct object is `271167473d87ef710f07ecdd98caf0ce12091686`
(`knowledge:1`; `git show -s --format=%H 2711674` resolves to it). The frozen
prediction itself is correctly committed there (N1). Smallest fix: replace
both `2716747` occurrences with `2711674` or the full hash. Same defect
independently found by `w2/RunProesbuild0215.md` F2.

### F4 — MEDIUM-LOW (calibration): "no mid-run check differed" has no retained record

`knowledge:26-29` says the 146 paths "were hashed before, every 30 s during,
and after each session … and no mid-run check differed."

Observation: `carrier-run.py:422-433` snapshots mid-run, but writes
`pins_changed_during_run` **only on inequality**. The target's
`steps.analyze` keys are
`['argv','cwd','ended_at_utc','evidence_id','exit','polls','retained_logs','started_at_utc','stderr_path','stderr_sha256','stdout_path','stdout_sha256']`
— there is no check count and no mid-run timestamp. The analyze step ran
134.4 s (`13:53:40.959991Z`–`13:55:55.366587Z`), so roughly four 30-s checks
should have run; the receipt cannot distinguish "checked, equal" from "never
checked". This is the exact shape `corpus/QUALITY.md:29` (row 19) rules out
("a `pins_unchanged_during_run: true`-style boolean is not a measurement").

Smallest fix: record `pins_checks_during_run: N` and `last_pin_check_utc` in
the step record even when equal (two lines after `carrier-run.py:425`), or
delete the mid-run sentence and keep only the pre/post instants. Same defect
independently found by `w2/RunProesbuild0215.md` F7.

### F5 — MEDIUM-LOW (gate completeness): the validator trusts the recorded log↔run binding instead of re-deriving it

`knowledge:22-25` makes content binding the admission criterion, and the
receipt records `binding: {logfile_ok: true, target_ok: true}`
(`runs/pro-esbuild-0.27.7/receipt.json:1800`). But the gate never reads it:

```sh
$ grep -n "binding\|import_target\|Using log file\|IMPORTING" .ufo/waves/round-17/tools/receipt-validate.py
# no output, EXIT=1
```

For this target the binding is genuinely true (N2), so this is a gate gap, not
a false artifact: a doctored receipt could attach an unrelated `ghidra.log`,
update its digest, and still validate. `w1/SentinelPollRace.md:70` specified
the post-hoc content gate; it was not integrated.

Smallest fix: in the carrier branch, read `retained_logs[].files["ghidra.log"]`
and assert `Using log file: <session_dir>/ghidra.log`, `IMPORTING:
file://<session_dir>/target-<carrier.sha256[:12]>.bin`, and (stronger, already
present in this log) the full `?MD5=<md5(carrier)>`; compare with the recorded
booleans and add a mismatched-MD5 red case.

### F6 — LOW (provenance): the knowledge entry says the inspect-go Evidence ID is in `receipt.json`; it is not

`knowledge:60-61`: "Full SHA-256, REA `inspect-go-binary` and `analyze` Evidence
IDs, step argv, exit codes, timestamps and log digests are in each
`runs/<label>/receipt.json`."

Observation for this run: the analyze ID is present
(`receipt.json:1839`, `ev_987ae889…`), and matches `analyze.json`. The
inspect step has no `evidence_id` key (keys listed in F4); its ID
`ev_a1e7ac95032d7b36ea1c7c1429d7c6f8a8e252c153267bfa9f5e5228fe302ea1` exists
only in `runs/pro-esbuild-0.27.7/inspect-go.json`. Smallest fix: "… in
`runs/<label>/receipt.json` (analyze) and `runs/<label>/inspect-go.json`
(inspect-go-binary)". Same defect independently found by
`w2/RunProesbuild0215.md` F3.

### F7 — LOW (operability): the documented recheck deletes the evidence it says to compare

`knowledge:3` says to rerun with `bash …/run-carriers.sh <label>` and "compare
the receipt's `carrier.sha256_pre` first". At the reviewed revision,
`run-carriers.sh:14-15` is `out="runs/$label"` then `rm -rf "$out"; mkdir -p
"$out"` — the command removes `receipt.json`, `observation.json`,
`compare.json` and `logs/` before producing replacements, so the comparison it
asks for is impossible after the command starts. The worktree's uncommitted
`${RUNS_DIR:-runs}` indirection would allow a safe rerun, but it is not at
`da64646` and the published sentence does not use it. Smallest fix: publish the
recheck as `RUNS_DIR=/tmp/r17-recheck bash run-carriers.sh <label>` after
committing that indirection, or copy `runs/<label>/` aside first. Same defect
independently found by `w2/RunProesbuild0215.md` F5.

## Verified, bounded no-findings

- **N1 — prediction pre-registration.** `git show
  271167473d87ef710f07ecdd98caf0ce12091686:.ufo/waves/round-17/predictions/pro-esbuild-0.27.7.prediction.json`
  is byte-identical to the working file (`cmp` clean; both
  `sha256 7dc311b6fc6e2eb72117baefe3c908ce41ec859e99abce36587015e141efed6e`);
  `git log --follow` shows only `2711674` touched it, and
  `git diff --name-only 2711674 da64646 -- .ufo/waves/round-17/predictions/` is
  empty. Commit time `2026-10-20T13:46:45Z` precedes the receipt's analyze
  `started_at_utc 2026-10-20T13:53:40.959991Z` by 6 m 55 s.
- **N2 — the bound log binds this carrier.** `ghidra.log:2` =
  `Using log file: /tmp/kr17-rea-g39lajwh/rea-ghidra-DjvEp2/ghidra.log`;
  `:46` = `IMPORTING: file:///tmp/kr17-rea-g39lajwh/rea-ghidra-DjvEp2/target-c638273fcf95.bin`;
  `:56` =
  `Loading file:///tmp/kr17-rea-g39lajwh/rea-ghidra-DjvEp2/target-c638273fcf95.bin?MD5=90ac17944eb91ae50b5abfc1da37fcc1...`
  and `md5sum` of the carrier is exactly `90ac17944eb91ae50b5abfc1da37fcc1`.
  Session path equals `retained_logs[0].session_dir`; `c638273fcf95` is
  `carrier.sha256_pre[:12]`. Last copy `13:55:54.866060Z` precedes process end
  `13:55:55.366587Z`, and the receipt declares the polling tail limit.
- **N3 — extraction and comparison reproduce.** Fresh
  `log-extract.py --log <retained ghidra.log>` exit 0 and `diff` against
  `runs/pro-esbuild-0.27.7/observation.json` is empty. Fresh
  `compare.py --prediction … --observation /tmp/fresh-extract.json` gives
  `all_match: true`, exit 0, identical per-field verdicts to the retained
  `compare.json` (only the recorded input-path strings differ).
- **N4 — the knowledge table row matches the log.** Row `knowledge:58`: two
  `Reading Go binary info` lines (log 63, 68), two
  `unable to get GoRttiMapper` errors (64, 69), no
  snapshot/untested/invalid/missing-bootstrap line; language
  `x86:LE:64:default:golang` (log 48); carrier prefix `c638273fcf95573c`
  matches. `build_info: null` is independently confirmed:
  `python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py
  /home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.27.7/node_modules/@esbuild/linux-x64/bin/esbuild`
  → `found: false`, `magic_file_offsets: []`, sha `c638273f…`; `readelf -S`
  shows `.gopclntab`/`.gosymtab` but no `.go.buildinfo`. The hand prediction's
  falsifier ("if a fallback Go version is set the run would show a version
  route") did not occur, so the predicted absent-build-info route is the
  observed one. The four `extra_expectations` hold (language compiler,
  `invalid_version_strings: []`, `bootstrap_attempts: 2`, both errors contain
  `unable to get GoRttiMapper`) — but see F2 for how that is *not* what the
  retained comparator measured.
- **N5 — cited source anchors exist and say what is claimed** (extracted from
  `Base-src.zip`): `GoRttiMapper.java:79` is
  `GoVerRange.parse("1.15-1.25")`; `:106` is the unconditional
  `Msg.info(..., "Reading Go binary info: ")`; `:150-163` is `getGoBinary`
  with `buildInfo == null → return null` before any version message; `:179-180`
  is the request-echo `Using Go API snapshot for version %s`; `:201-210` is
  `hasGolangSections` (gopclntab/Mach-O/PE section names);
  `GolangSymbolAnalyzer.java:135` and `GolangStringAnalyzer.java:105` are the
  exact `unable to get GoRttiMapper` messages; `ElfLoader.java:188-200` selects
  the golang cspec from section names.
- **N6 — pin and session integrity.** 146 pinned paths = carrier + r16
  `selection.py` + frozen prediction + all 143 files under the installed Go
  data dir (`find … -type f | wc -l` = 143; zero unpinned); pre/post maps equal
  in all eight receipts; every run has exactly one bound session and zero
  unbound; analyze intervals are strictly sequential,
  `13:47:06.688621Z`–`14:00:05.228761Z`, matching the entry's
  "13:47–14:00 UTC".
- **N7 — no capability overclaim.** `SCORECARD.md` was not touched by
  `da64646` and contains no r17 capability row; `LOG.md:2045-2047` claims only
  the capture and `8/8 compare exit 0`, and `LOG.md:2063-2066` defers measured
  values. Honest withholding given F1.

## Residual risk / gaps

- The hand prediction's positive discriminators are true by manual reading,
  not by the retained comparator; F2's fix should re-run `compare.py` and
  replace `compare.json` rather than leave the manual result as the only
  support.
- Mid-run pin equality is unrecorded (F4); the claim may well be true, but it
  is not auditable from the retained receipt.
- Depth note (inference): the carrier carries `.go.fipsinfo` (Go ≥ 1.24 module
  data) yet no `.go.buildinfo`; the entry establishes the *absence* of the
  record (two readers agree) but does not examine *why* it is absent
  (stripping vs. link mode). This does not change the observed route; it does
  limit how far "absent build info" can be generalized as a carrier property.
- One run per carrier; the entry already lists determinism under
  "Not examined". The worktree is live (F7's uncommitted change), so the
  recheck text and `run-carriers.sh` may move after this report.
