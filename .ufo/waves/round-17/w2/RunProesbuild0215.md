# RunProesbuild0215 — attack on `runs/pro-esbuild-0.21.5` (wave 2, falsify)

Lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`; baseline
`b563c799d97774aae4351276fe43cb897311e349`; predictions frozen at
`271167473d87ef710f07ecdd98caf0ce12091686`.
Path convention: anchors are relative to the lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; `W` = `.ufo/waves/round-17`.
Read-only: no REA `analyze`/`search`/`decompile`, no Ghidra/`analyzeHeadless`,
no carrier execution; scratch only under `/tmp`; no lane file edited but this
report. No installs.

## Findings

### F1 — HIGH (calibration): the receipt gate is red on every retained carrier receipt — producer writes `steps` as an object, validator requires an array

- Anchors: `tools/receipt-validate.py:98` (`isinstance(receipt.get("steps"), list)`),
  `:284` (iterates a list), selftest fixture `:470` (`"steps": [{ … }]`);
  producer `tools/carrier-run.py:275` (`"steps": {}`) and `:349`
  (`receipt["steps"] = steps`), whose own selftest asserts object access
  (`carrier-run.py:555-558`). The gate's advertised semantics are
  `SKILL.md:536` ("0 valid, 1 …, 2 unreadable"), the recheck command is
  `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`, and the C2
  capability gate is `claims.json:22` ("only if the capture runs and its receipt
  validates"); w1 already specified that gate as exit 0 (`W/w1/ReviewCapabilityTable.md:37`, D2).
- Exact command (target):
  `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/pro-esbuild-0.21.5/receipt.json`
- Output: `exit 1`; `{"counts":{"invalid":1,"receipts":1,"unreadable":0,"valid":0}, … "kind":"unknown","findings":[{"code":"unrecognized_shape","detail":"receipt matches neither retain nor carrier shape","where":"$"}]}` with `checks_performed: 306`.
- Scope: every retained carrier receipt fails the same way:
  `for f in runs/*/receipt.json; do python3 -I -B tools/receipt-validate.py "$f" >/dev/null; echo "$f EXIT=$?"; done`
  → `calib-esbuild-0.25.12`, `calib-shfmt`, `pro-aether`, `pro-containerd-shim`,
  `pro-esbuild-0.21.5`, `pro-esbuild-0.27.7`, `pro-notesmd-cli`, `pro-op` all
  `EXIT=1`. `receipt-validate.py --selftest` → `SELFTEST: CLEAN cases=5`, exit 0,
  because its carrier fixture is array-shaped (`:470`) and never exercises the
  producer's shape.
- Bounded counterfactual (scratch copy, no lane edit): copying the target
  receipt to `/tmp/rpe_probe/receipt.json` with only `steps` converted
  dict→list yields `kind:"carrier"`, `checks_performed: 336`, no findings,
  `exit 0`. So no digest/size/pin check fails; the sole blocker is the container
  type. The run's evidence is intact; the gate's success branch is simply
  unreachable for the lane's own receipts, and `knowledge:3` currently returns 1.
- Smallest fix: in `classify`, accept both (`isinstance(receipt.get("steps"), (list, dict))`),
  and in the carrier branch iterate `receipt["steps"].values()` (stable `where`
  such as `$.steps.<name>`) when it is a dict; replace the array fixture with one
  mirroring `carrier-run.py`'s dict receipt while keeping the tampered-digest red
  case. `contract.md:43-47` should name the container type.

### F2 — MEDIUM (provenance/calibration): the pre-registration commit is cited as an object that does not exist

- Anchors: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37` and
  `.ufo/waves/round-17/run-carriers.sh:2` both say `2716747`.
- Exact command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse --verify 2716747^{commit}`
  → `fatal: Needed a single revision` (exit 128); `git rev-parse --disambiguate=2716747` → empty.
- The correct object is `271167473d87ef710f07ecdd98caf0ce12091686` (full form at
  `knowledge:1`, and in the committed round-17 `LOG.md` entry);
  `git show -s --format=%H 2711674` → `271167473d87ef710f07ecdd98caf0ce12091686`.
- Smallest fix: replace both occurrences with `2711674` (or the full hash).

### F3 — MEDIUM-LOW (calibration): the knowledge entry says both REA Evidence IDs are in `receipt.json`; the inspect-go ID is not

- Anchor: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:60-61`
  ("REA `inspect-go-binary` and `analyze` Evidence IDs … are in each `runs/<label>/receipt.json`").
- Observation: the target receipt's inspect step keys are exactly
  `['argv','cwd','ended_at_utc','exit','started_at_utc','stderr_path','stderr_sha256','stdout_path','stdout_sha256']`
  (no `evidence_id`); `carrier-run.py:333` attaches `evidence_id` only to the
  analyze step. The inspect-go ID lives in `runs/pro-esbuild-0.21.5/inspect-go.json`
  (`ev_5c06eceff96ee9f44596daacb182839e8ab629d1b1b8926f187cfafaddae43f7`).
- Smallest fix: "… are in each `runs/<label>/receipt.json` (analyze) and
  `runs/<label>/inspect-go.json` (inspect-go-binary)".

### F4 — MEDIUM (depth): the gate does not re-derive the log↔run binding it is cited to check

- The knowledge entry makes content binding the admission criterion
  (`knowledge:22-25`); the receipt records `binding: {logfile_ok, target_ok}`
  (`runs/pro-esbuild-0.21.5/receipt.json:1800-1803`), but `receipt-validate.py`
  contains no reference to `Using log file`, `IMPORTING`, or `binding`.
- Bounded test (scratch, list-shaped copy so F1 does not mask it): set both flags
  to `false`, leave every digest/pin intact →
  `python3 -I -B tools/receipt-validate.py /tmp/rpe_probe/receipt_bindfalse.json`
  → `exit 0`, `valid: true`, `findings: []`. The recorded booleans are trusted,
  so a receipt can bind an unrelated log and still validate.
- The log itself carries a stronger, unused full-content binding:
  `ghidra.log:54` = `Loading file:///tmp/kr17-rea-5l3r8v9k/rea-ghidra-lI5mW3/target-b567f467fdac.bin?MD5=d8460492d5dd2218e9788366cf117e37…`,
  and `md5sum <carrier>` = `d8460492d5dd2218e9788366cf117e37` (full MD5, not only the 12-hex prefix).
- Smallest fix: in the carrier branch, require `session_dir`, read the retained
  `ghidra.log`, assert both literal binding strings against
  `carrier.sha256[:12]`, compare the logged `MD5=` with md5 of the pinned carrier,
  and compare with the recorded booleans; add a red case with a mismatched MD5.

### F5 — LOW (operability/recheck): the documented recheck deletes the evidence it tells you to compare

- Anchor: `knowledge:3` says rerun with `bash …/run-carriers.sh <label>`; at rev,
  `run-carriers.sh:14-15` are `out="runs/$label"` then `rm -rf "$out"; mkdir -p "$out"`.
  Following that sentence removes `runs/<label>/receipt.json`, `observation.json`,
  `compare.json` and `logs/` before producing replacements. The worktree has an
  uncommitted `RUNS_DIR` indirection (`git diff -- run-carriers.sh`), but it is not
  at `da64646`.
- Smallest fix: commit the `RUNS_DIR` indirection and document
  `RUNS_DIR=runs-recheck bash run-carriers.sh <label>`, or say to copy
  `runs/<label>/` before the rerun.

### F6 — LOW (provenance): `runs/run-log.txt` omits the first scripted leg (`calib-shfmt`)

- `runs/run-log.txt` starts at `== calib-esbuild-0.25.12 start 2026-10-20T10:47:42-03:00`;
  it has no `calib-shfmt` lines. But `runs/calib-shfmt/receipt.json` shows
  `steps.analyze` `13:47:06.688621Z`–`13:47:37.309101Z`, `orig_argv` from
  `tools/carrier-run.py`, and it carries the same script-style
  `carrier-run.stdout` redirect; `predictions/carriers.tsv` lists `calib-shfmt`
  first, and `knowledge:2` claims eight sessions starting 13:47Z.
- Smallest fix: append the two missing `== calib-shfmt start/end` lines marked
  "appended from receipt timestamps" (append-only), or state that run-log capture
  began at the second leg.

### F7 — LOW (calibration): "no mid-run check differed" is not receipt-evidenced

- Anchor: `knowledge:28-29`. `carrier-run.py:420-433` records
  `pins_changed_during_run` only on inequality; there is no check count, and the
  target `steps.analyze` keys (above) contain no mid-run field. A reader cannot
  distinguish "checked, equal" from "never checked".
- Smallest fix: record `pins_checks_during_run: N` (and `pins_mid_equal: true`)
  even when equal. The adjacent caveat "identical bytes at those instants, not
  continuity" is correct and should remain.

## Target checks that pass (bounded no-finding — what I checked)

1. **Fresh extraction.** `python3 -I -B tools/log-extract.py --log runs/pro-esbuild-0.21.5/logs/rea-ghidra-lI5mW3/ghidra.log`
   → exit 0; sha256 of stdout `211b48f64e467b13ef95b83dfd048c4caf5348e382b4e6a241df61dc39abc210`
   equals `sha256sum runs/pro-esbuild-0.21.5/observation.json`. Byte-identical.
2. **Fresh compare.** `python3 -I -B tools/compare.py --prediction predictions/pro-esbuild-0.21.5.prediction.json --observation /tmp/rpe_obs.json`
   → exit 0, `all_match: true`, 5/5 fields (`untested_version`, `snapshot_label`,
   `missing_bootstrap`, `snapshot_route`, `fallback_to`). The recorded
   `runs/pro-esbuild-0.21.5/compare.json` equals this output modulo the
   `observation` path.
3. **Log binding.** `ghidra.log:2` = `Using log file: /tmp/kr17-rea-5l3r8v9k/rea-ghidra-lI5mW3/ghidra.log`;
   `:46` = `IMPORTING: file:///tmp/kr17-rea-5l3r8v9k/rea-ghidra-lI5mW3/target-b567f467fdac.bin`.
   Carrier sha `b567f467fdac92c606717c86ea5cd1d6c30145c616776c0f2ff5429ad48586ba`
   → sha[:12] `b567f467fdac`, exactly the target stem. `receipt.bound_sessions`
   is exactly `["/tmp/kr17-rea-5l3r8v9k/rea-ghidra-lI5mW3"]`,
   `unbound_sessions: []`, `session_dir_baseline: []`. Stronger still, `:54`'s
   `MD5=d8460492d5dd2218e9788366cf117e37` equals `md5sum` of the pinned carrier.
4. **Prediction provenance.** `sha256sum predictions/pro-esbuild-0.21.5.prediction.json`
   = `8585d342b203c8bb523d095dadbab2eaa6032d73ca2900a0a7f6d48fd677cbfc`
   = `git show 271167473d87ef710f07ecdd98caf0ce12091686:.ufo/waves/round-17/predictions/pro-esbuild-0.21.5.prediction.json | sha256sum`
   = line 11 of `predictions/SHA256SUMS`. Commit time `2026-10-20T10:46:45-03:00`
   (= `13:46:45Z`) precedes `steps.analyze.started_at_utc`
   `2026-10-20T13:51:13.639911+00:00` by 4 m 28 s; `git merge-base --is-ancestor 2711674… da64646…` → exit 0.
   Re-derivation: `python3 -I -B tools/predict.py --go-version go1.20.12 --golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`
   → exit 0, JSON-equal to the committed prediction; its `selection.base`
   (`go1.20.0.json`, `6def3499…`) and `selected_diff`
   (`patchverdiffs/go1.20.12.json.diff`, `148352d3…`) match the installed files'
   sha256.
5. **Knowledge row** (`knowledge:55`). pnpm path matches `carriers.tsv` and
   `receipt.carrier.path`; `sha256[:16]` `b567f467fdac92c6` matches; `go1.20.12`
   matches `inspect-go.json.normalized_result.build_info.go_version` and the
   independent `tools/buildinfo-probe.py` (`go_version: go1.20.12`,
   `header_offset: 9388032`, same as REA's); route `info` matches `ghidra.log:62`
   `INFO (GoApiSnapshot) Using Go API snapshot for 1.20.12`;
   `loaded; 4411 types` matches `:65` `INFO (GoTypeManager) Found 4411 Go types`;
   `x86:LE:64:default:golang` matches `:48`.
6. **Pins.** 146 entries = 143 files under `typeinfo/golang` (`find … -type f | wc -l` = 143)
   + carrier + round-16 `selection.py` + frozen prediction; `pins_compare`
   `equal: true`, `changed/missing/errors` empty; the pinned prediction sha is
   `8585d342…` (the committed value).
7. **Receipt internals.** Despite F1's shape verdict, the validator's 306
   recomputations yield no `sha256_mismatch`, `missing_file`, or size finding;
   `script.log` sha `2db60bf882262828bdd51350b6b1bee901a16e946b30542d4f96e28add14446b`
   matches the receipt. Negative route markers are genuinely absent from the
   log (`grep -E "Untested Go version|Missing Go bootstrap|Falling back|Invalid Go version"`
   → no match, exit 1).

## Residual risk / gaps

- **Capture tail.** Last `ghidra.log` line is `10:52:44 … ANALYZING changes made by post scripts`
  while `steps.analyze.ended_at_utc` is `10:52:45.420916Z` (= `10:52:45.42-03:00`);
  the final ~1 s is absent as `log_capture_limit` discloses. All Go diagnostics
  (through `10:52:42`) are present, so no compared field is affected. [observation]
- **Non-discriminating field.** `snapshot_label` is the request echo; the
  discriminating fields for this carrier are `snapshot_route` (`info`),
  `fallback_to` (empty) and `untested_version` (empty). The entry and
  `compare.json` rules disclose this. [observation]
- **Chronology unit.** The carrier receipt has no top-level `started_at_utc`;
  the chronology check uses `steps.analyze.started_at_utc`. The contract's
  carrier shape (`contract.md:43-47`) does not require a top-level field, so this
  is a contract-shape inference, not a run defect. [inference]
- My eight-receipt sweep passed `runs/*/receipt.json`; `runs/run-log.txt` is a
  file, not a receipt (that one path exits 2 as unreadable, correctly).
