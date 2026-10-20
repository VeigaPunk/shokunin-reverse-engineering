# Verify18Harness — W18 verify.py (post-integration pass)

## Files changed
- `.ufo/waves/round-18/verify.py` (new, 299 lines). Modelled on
  `.ufo/waves/round-17/verify.py` with the round-18 contract deltas applied.

## Source pin (jj-safe, contract `revpin.py` + `verify.py` bullets)
- `main()` resolves `base` (`argv[1]^{commit}`) then calls
  `revpin.resolve_source(LANE)` loaded via `spec_from_file_location` from
  `W18/tools/revpin.py` (verify.py:92-99). On `revpin.RevPinError` it prints a
  `{"refused": true, "revpin_finding": ...}` JSON and returns 2 **before any
  command runs** — satisfies "refuse before running anything on a finding".
- `HEAD` is never used as a revision; the record carries `source_branch`,
  `source_remote`, `source_pushed`, `head_revision`, `head_equals_source`
  (verify.py:275-280) so the pass output shows the jj-safe pin evidence.
- Tracked-only dirt is recorded (`git status --porcelain --untracked-files=no`,
  verify.py:101) not refused — `source` is a Git-object revision, untracked
  verify outputs don't move it. Observation; the r17 model recorded full
  porcelain output (r17 verify.py:60). [INFERENCE: restricting to tracked files
  matches the r18 contract bullet applied to r17/verify.py.]

## Commands (argv lists + expected exits), in pass order
  1. `pins-snapshot-pre` — `r17 tools/pins.py snapshot --out verify/tools-pre.json <W18/tools/*.py>` expect 0 (verify.py:148-152).
  2. `--selftest` (expect 0) for every `W18/tools/*.py` (dynamic glob: routed-defects, revpin, head-rev-lint, jj-red-before, swiss-misread — verify.py:157-159); edited/invoked W17 tools carrier-run, compare, invocation-audit, log-extract, pins, receipt-validate, temporal-sweep (verify.py:160-162); gates `citation-drift-probe.py --selftest` (verify.py:163-164); `custody-pair.py selftest --scratch <pre-created dir>` (subcommand form per custody-pair.py:1329-1333; scratch must pre-exist per custody-pair.py:1330-1332, created at verify.py:165-168); `measure.py --selftest`, `controls.py --selftest` (verify.py:169-170).
  3. `routed-defects.py --root LANE --rev <base>` and `--rev <source>` expect 0; `... --rev <source> --strict` expect 0 (verify.py:174-179). Baseline strict intentionally absent (open_count=6 there by design; the plain run retains the JSON).
  4. `head-rev-lint.py --root LANE --rev <base> --strict` expect 1; `--rev <source> --strict` expect 0 (verify.py:183-186).
  5. `jj-red-before.py --out verify/jj-red-before-receipt.json` expect 0 (verify.py:190-191).
  6. Per W18 run label (verify.py:196-230): `receipt-validate.py <run>/receipt.json` expect 0; `compare.py --prediction predictions/<lab>.prediction.json --observation <obs>` expect 0, where `<obs>` is the retained `<run>/observation.json`, else a fresh `log-extract.py --log <run>/logs/<bound>/ghidra.log` (bound session read from receipt.json `bound_sessions[0]`, mirroring r17 verify.py:94-96). Labels come from `predictions/carriers.tsv` column 1, else sorted `runs/` dirs (run_labels, verify.py:64-82).
  7. `measure.py <base>` / `measure.py <source>` expect 0; `controls.py <base> <source>` expect 0 (verify.py:234-236).
  8. `citation-drift-probe.py --root LANE --rev <source> --table …/pointer-table.json --expected …/expected.json --strict` expect 0 (verify.py:238-243).
  9. `temporal-sweep.py --root LANE --rev <source> --sites-rev <base>` expect 0 (`--sites-rev` keeps baseline site lines counted per temporal-sweep.py:417-419; verify.py:245-246); `invocation-audit.py --root LANE --rev <source>` expect 0 (verify.py:247-248).
  10. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` expect 0 (verify.py:250-252).
  11. `custody-pair.py capture --out W18/custody/custody-r18.v2.txt --label round-18`, expect unasserted (matches r17 verify.py:144-146 — capture legitimately exits nonzero when a custody path is absent per custody-pair.py:688-693; verify.py:255-258).
  12. `pins-snapshot-post` + `pins-compare tools-pre.json tools-post.json` expect 0 (verify.py:263-266).

## Depth choices beyond the r17 model
- **skip() record** (verify.py:131-146): missing receipt/prediction/observation
  produces an explicit recorded command with `exit: 2`, `skipped_reason`, and
  `exit_as_expected: false` — the pass never crashes on an incomplete runs/
  tree (r17 would `IndexError` at r17 verify.py:94) and the hole surfaces in
  `unexpected_exits`.
- **observation reuse**: prefers the run's retained `observation.json` (what
  `run-carriers.sh` wrote under `compare.json` provenance) over re-extraction;
  re-extracts only when absent.
- **pin_paths widened** (verify.py:105-114): all of `W18/tools`, all of
  `W17/tools` (edited in place this round), both edited gate tools,
  `run-carriers.sh`, `measure.py`, `controls.py`, `__file__`, every file under
  `predictions/`. Module-level `pins.snapshot` pre/post + `pins.compare`
  recorded; CLI snapshot/compare exercises the r17 pins CLI end-to-end.
- **pycache sweep** retained verbatim (find over `.ufo`, verify.py:269-270).

## Deliberate deviations
- No `go-carrier-run-replicate`: contract says the L1 runs every carrier
  analysis once, sequentially, after predictions freeze (contract.md:14-15) —
  a replicate would be a second Ghidra analysis; the task's command list does
  not include it.
- No `predict-*`/`buildinfo-probe-*`/`go-version-m-*`/quote-fidelity runs: not
  in the assigned command list.
- `routed-defects-source-strict` added (expect 0): C1's falsifier says
  open_count 0 at delivered revision; strict enforces it as an exit code.
  [INFERENCE: cheap depth move, harms no axis.]

## Commands run (all exits observed)
- `python3 -I -B -c 'import ast,sys;ast.parse(open(sys.argv[1]).read())' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/verify.py` → exit 0, last line of output: (no output — `ast.parse` prints nothing on success).
- Read-only inspection commands only: `grep -n …` on custody-pair.py / citation-drift-probe.py / compare.py / receipt-validate.py / temporal-sweep.py / invocation-audit.py / log-extract.py (exit 0), `ls` on r17 runs/predictions/tools and W18 dirs (exit 0), `git -C LANE status --porcelain` and `git -C LANE rev-parse refs/heads/main HEAD` (exit 0; both = 9011581d84527ba34c675f9cf912e54d2e72d470).
- No `--selftest` of my own file exists to run (verify.py is a harness, not a
  tool with fixtures; per assignment only the AST check applies). No tools
  installed.

## Risks / blockers
- `W18/tools/` and `W18/predictions/` do not exist yet at write time (siblings
  in flight). verify.py enumerates both at runtime — correct post-integration.
  If `tools/` were empty at runtime, `os.listdir` would raise; post-integration
  guarantees make that unreachable.
- `custody-pair selftest` gains the new off-branch red case via
  CustodyPairBranchTip's in-place edit; the harness already invokes the
  `selftest --scratch` subcommand form the tool documents.
- `pin["remote"]`/`pin["pushed"]`/`pin["head_equals_source"]` keys rely on the
  contract-specified `resolve_source` return shape (contract.md:52-56);
  `.get()` used so a shape drift degrades to nulls, not a crash.
