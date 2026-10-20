# CarrierRunTool — round-17 wave-1 report

Seat: `KaidokuR17.CarrierRunTool-3`. Scope: implement
`.ufo/waves/round-17/tools/carrier-run.py` per contract.md §"W/tools/carrier-run.py"
(contract.md:31-49). One new file written; no other file touched.

## Files changed
- `.ufo/waves/round-17/tools/carrier-run.py` (new, 547 lines, stdlib-only,
  `python3 -I` clean, `SELFTEST: CLEAN cases=2`, exit 0).

## Contract conformance (observed)
- CLI shape matches contract.md:32-33: `--carrier/--label/--out-dir` required;
  `--rea-version` (default 6.5.0), `--timeout` (1800), `--poll` (0.5),
  repeatable `--search` (carrier-run.py:517-541).
- Pin set = `[carrier, R16_SELECTION]`; Go typeinfo dir deliberately not pinned
  (carrier-run.py:287, R16_SELECTION at :37; r16 `selection.py` confirmed to
  exist on disk).
- Step argv recorded as run: `npx -y rea-agents@<V> inspect-go-binary|analyze|
  search <carrier> ... --format json`; search uses `--pattern NAME --kind
  procedures --format json` matching `rea search --help` (carrier-run.py:274,
  :280-287). stdout→`<step>.json`, stderr→`<step>.stderr` under `--out-dir`.
- Poller: baseline set of `/tmp/rea-ghidra-*` dirs recorded once before analyze
  (carrier-run.py:262-264); only *new* dirs are tracked; `ghidra.log`/`script.log`
  copied via `*.tmp` + `os.replace` into `logs/<dirname>/` (carrier-run.py:143-197);
  per-dir `polls`, `last_copy_utc`, per-file `{path, sha256, bytes}` retained;
  receipt carries `session_dir_baseline`, `retained_logs`, `log_capture_limit`
  (carrier-run.py:40-43, :295-296).
- Final `poller.scan()` after process exit is a best-effort catch of late lines
  before REA deletes its runtime root (carrier-run.py:353; pilot README.txt:4-6
  documents REA deleting the root at close).
- `analyze` `evidence_id` parsed from stdout JSON when present
  (carrier-run.py:201-207, :274-275); receipt schema per contract.md:43-47
  including `python`, `orig_argv`, `pins_pre/post/compare`.
- Exits (carrier-run.py:300-309): 0 all steps ran & pins equal & analyze==0;
  1 pins differ; 2 could-not-evaluate (bad input, step spawn/timeout, receipt
  write failure) or analyze exit != 0 (recorded, not hidden — contract.md:48).
- Depth beyond minimum: mid-run re-snapshot of pins every `PIN_CHECK_S`=30 s
  records `pins_changed_during_run` in the step record (carrier-run.py:35,
  :343-354) — throttled so hashing a large carrier doesn't dominate I/O.
- `--selftest` never invokes REA (carrier-run.py:372-514): fake commands are
  injected through the `runner` callable parameter plus a `session_glob`
  override; a `sys.executable` fake child creates `<tmp>/rea-ghidra-FAKE01/`,
  writes `ghidra.log`+`script.log`, prints JSON, then `shutil.rmtree`s the dir —
  proving the poller retained the log *before* deletion. A pre-existing
  `rea-ghidra-AAAAAA` dir proves baseline dirs are never copied. Case 2 forces
  analyze exit 3 → run returns 2 with `steps.analyze.exit == 3` recorded.

## Observations vs inference
- Observed: `SELFTEST: CLEAN cases=2`, exit 0; missing-arg path errors via
  argparse exit 2. Observed from `search --help`: flags used are exactly
  `--pattern`, `--kind procedures`, `--format json`.
- Inference: contract.md:48 is read as "exit 2 iff analyze exit != 0"; other
  REA step nonzero exits are recorded in the receipt without forcing nonzero
  (matches "REA nonzero exits are recorded, not hidden"). Flag for L1 if the
  intent was "any step".
- Inference: `inspect-go-binary` runs unpolluted by the session baseline
  because the baseline is taken after it returns (contract step order 2→3);
  any session dir it creates would be pre-counted, not retained.
- Limitation (stated in receipt + --help): polling copy can miss lines written
  after the final poll; pins prove "same bytes at two instants" only
  (carrier-run.py:15-21, :40-43).

## Risks / blockers
- `pins.py` is a sibling seat file (PinsTool); `carrier-run.py` loads it by
  absolute path at runtime — a missing/renamed pins.py yields exit 2
  ("pins module unavailable"), selftest unaffected (injects a fake pins).
- No installs performed; no REA/Ghidra analysis commands executed.
