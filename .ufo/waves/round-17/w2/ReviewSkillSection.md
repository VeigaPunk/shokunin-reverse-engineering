# Review: SKILL.md 'Retained Go carrier diagnostics — round 17' + registry rows 448-449

Target: SKILL.md:509-541 (new section and its 10 registry rows) and SKILL.md:448-449
(in-place citation-drift / custody-pair rows), lane revision
`da64646adcb19c1ede7537b799b8c7d283fe43da` (baseline `b563c799…`). Read-only.
No installs were made. Every command below was run against Git objects or retained
round-17 files; no carrier or REA analyze/search was executed.

## Findings (severity order)

### F1 High — `receipt-validate` cannot recognise any round-17 carrier receipt; the row's "0 valid" state is unreachable
`SKILL.md:536` advertises `receipt-validate.py <RECEIPT>` with "0 valid". The tool's own
docstring says it is for `carrier-run.py` receipts (`tools/receipt-validate.py:1-25`), but
`classify()` only accepts a carrier receipt when `steps` is a **list**
(`tools/receipt-validate.py:98-101`), while the producer writes a **dict**
(`tools/carrier-run.py:317,349`). The selftest fixture uses a list
(`tools/receipt-validate.py:470`), so the green case never exercises the producer's shape.

```
$ jq -r '.steps|type' .ufo/waves/round-17/runs/pro-op/receipt.json
object
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/runs/pro-op/receipt.json
{ "counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0}, "exit": 1,
  "receipts": [{ "checks_performed": 306, "kind": "unknown", "status": "invalid",
    "findings": [{"code": "unrecognized_shape", "where": "$",
                  "detail": "receipt matches neither retain nor carrier shape"}]}] }
(selected fields; the tool also emits pins_available/pins_path and the full counts)
$ bash -c 'for f in .ufo/waves/round-17/runs/*/receipt.json; do python3 -I -B \
    .ufo/waves/round-17/tools/receipt-validate.py "$f" >/dev/null 2>&1; echo "$? $f"; done'
1 …/calib-esbuild-0.25.12/receipt.json   (same for all eight)
```
Impact: a healthy receipt is reported invalid; `runs/calib-shfmt` etc. never reach 0.
Digests are still recomputed (306 checks; no digest/pin findings), so the evidence bytes
are intact — the verdict is wrong. The r17 knowledge `recheck:` names this exact command
as the digest recheck (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`), so
the documented recheck exits 1 on healthy evidence.
Smallest fix: in `classify()` accept a dict `steps`, and in `check_required()` iterate
`steps.items()` (keys as `where`) so step fields are still checked; add one selftest case
built from a real `runs/<label>/receipt.json` shape.

### F2 Medium-high — both rows cite `.ufo/waves/round-17/verification.json`, which does not exist at the reviewed revision
`SKILL.md:449` asserts the custody-pair argv "exercised argv retained in
`.ufo/waves/round-17/verification.json`"; `SKILL.md:448` cites the same file alongside
round-16. At `da64646` the file is absent, and the probe says so:

```
$ git cat-file -e da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/verification.json
fatal: path '.ufo/waves/round-17/verification.json' does not exist in 'da64646…'
$ python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root $LANE --rev da64646…
  "counts": {"rows": 17, "exercised_match": 6, "unlabelled_variant": 11,
             "labelled_unexercised": 0, "receipt_files": 20, "argv_records": 74}
  line 449  custody-pair  class=unlabelled_variant  matched_receipt=null
(selected fields/rows; counts include argv_records and the excluded-glob tally)
```
The citation-drift half of 448 survives on round-16 evidence (below); the custody-pair
row has no live retention pointer, and the ten new rows (lines 532-541) plus custody-pair
(line 449) account for all 11 `unlabelled_variant` rows at this revision. The intended producer exists only as an untracked file: `verify.py:141-143`
runs `python3 -I …/custody-pair.py capture --out …/custody/custody-r17.v2.txt --label
round-17`, which matches the advertised template exactly. C1(b) ("matches an exercised
retained argv or is explicitly labelled") is therefore not yet met.
Smallest fix: land `verify.py` and its `verification.json` in the same commit as these
rows (then 449 becomes an exercised match), or drop the parenthetical and label the row
"exercised argv pending".

### F3 Medium — dead frozen-prediction commit `2716747` in the run script and the cited knowledge entry
`run-carriers.sh:2` (committed at da64646) and
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37` both say predictions were
frozen at `2716747`. That object does not exist; the frozen commit is `2711674`:

```
$ git cat-file -e 2716747^{commit}     → fatal: Not a valid object name
$ git cat-file -e 2711674^{commit}     → exists
$ git show -s --format='%h %ci' 2711674 → 2711674 2026-10-20 10:46:45 -0300
$ head -1 .ufo/waves/round-17/runs/run-log.txt → == calib-esbuild-0.25.12 start 2026-10-20T10:47:42-03:00
$ git diff --stat 2711674 da64646 -- .ufo/waves/round-17/predictions/   (empty)
```
The section's sentence "frozen in Git before the run" is true at `2711674` (57 s before
the first run, unchanged through da64646), but its cited script/entry name a nonexistent
commit. Smallest fix: replace `2716747` with `2711674` in both files.

### F4 Medium — the advertised `bash run-carriers.sh <LABEL>` entry always exits 0 and deletes `runs/<LABEL>` before rerunning
`SKILL.md:532` advertises the shell entry. The committed script's last command in the loop
is `echo` (`run-carriers.sh:30`), so the script's exit status is 0 regardless of per-label
outcomes, and line 15 `rm -rf "$out"` removes the previous run before line 19 starts:

```
$ bash .ufo/waves/round-17/run-carriers.sh __no_such_label__; echo rc=$?
rc=0
```
Per-label failure is only discoverable from `runs/<LABEL>/carrier-run.exit`. Worse, the
knowledge `recheck:` (knowledge:3) says to rerun a label with this script "and compare
`observation.json` fields": at the reviewed revision the rerun deletes that observation
(and `compare.json`) before the new run. The working tree adds `${RUNS_DIR:-runs}`
(uncommitted; `git diff` shows the single-line change), which is the only non-destructive
path and is what the untracked `verify.py` relies on (`env={"RUNS_DIR": "verify/replicate"}`).
Smallest fix: track and return the worst child status, and document/parameterise the
output directory in the committed script; amend the recheck to copy the run first.

### F5 Low — mid-run pin drift is recorded but does not gate the exit
`SKILL.md:532` says "pinned pre, every 30 s, and post" with "1 pin drift". Only the
pre/post comparison maps to 1 (`tools/carrier-run.py:376`); the 30 s check records
`pins_changed_during_run` on the step record (`:430`) and never changes the return code.
All eight receipts show `pins_changed_during_run` absent (no observed contradiction).
Smallest fix: word it "1 pre/post pin drift; mid-run drift is recorded per step, not
gated", or make mid-run drift return 1.

### F6 Low — `go-buildinfo-probe` exit map omits 2
`SKILL.md:540` gives only "0 emitted (`found:false` when no magic)". The tool returns 2 for
an unreadable/malformed path (`tools/buildinfo-probe.py:625-634`):

```
$ python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py /nope/bin; echo rc=$?
{ "path": "/nope/bin", "error": "unreadable: …" }
rc=2
```
Smallest fix: append "2 unreadable/malformed".

### F7 Low — `go-route-predict` exit map omits unreadable-root / selection-failure 2
`SKILL.md:534` says "2 unparseable/empty version (no guess)". `run()` returns 2 for any
`ValueError` or other exception, including an unreadable `--golang-root` and selection
load failure (`tools/predict.py:248-265`; module docstring lists them). Smallest fix:
widen to "2 unparseable/empty version or unreadable root/selection failure".

### F8 Low — the private `TMPDIR` parent survives; the write-scope cell does not say so
`SKILL.md:532` says writes go only to `runs/<LABEL>/` and a private `/tmp/kr17-rea-*`
parent. That is literally true, but all eight receipts record
`"session_parent_leftovers": ["node-compile-cache"]` and eight `/tmp/kr17-rea-*`
directories are still present, so the parent is not removed (the `os.rmdir` at
`tools/carrier-run.py:365-367` only fires when empty). Smallest fix: add "; parent
persists when npx writes `node-compile-cache`" to the cell, or clean it.

## Bounded no-findings (what I checked and found sound)

1. **citation-drift row (SKILL.md:448).** "frozen-run preflight" is present (exactly one
   occurrence in SKILL.md) and the pointer-table anchor
   `skill-registry-citation-drift-row` (`must_match: frozen-run preflight`) still fires.
   The advertised argv is token-for-token the exercised strict argv: round-16
   `verification.json` label `citation-strict` = `python3 -I <abs>/citation-drift-probe.py
   --root <abs> --rev 27b8fc… --table <abs>/pointer-table.json --expected
   <abs>/expected.json --strict`, exit 0. The untracked w2 head probe is the same flags
   with `--rev da64646…` but adds `-B` (`python3 -I -B …`), so it is a variant, not the
   advertised form; it exits 0 with `CITATION_DRIFT_VERDICT: clean findings=0`.
   No non-strict argv exists in any retained `verification.json` (round-14/15/16 all
   strict), so "unexercised variant" is accurate. Probe semantics 0/2 and the strict
   0/1/2 map match `citation-drift-probe.py:474-499`; the three preflight findings
   (`pointer_table_tampered`/`_unreadable`/`_unpinned`) match `run_check` at
   `:288-316`; `pointer-table.json` sha256 `7994eec7…` matches the `expected.json` pin
   (frozen-run guard live); the selftest table is exactly 13 cases and cases 11/12/13
   are `rev_unresolvable`/`table_tampered`/`table_absent` as the row states.
2. **custody-pair row (SKILL.md:449) semantics.** Parser and commands match: `capture
   --out … [--label …]`, `verify A [B] --live [--require-paths N]`, `paths`, `selftest`
   (`custody-pair.py:1308-1336`). Exit map 0/10/11/12/13/14/2/3, precedence
   `CONTENT-DRIFT > UNEVALUABLE > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH`,
   capture 0 at 5/5 / 14 on any unevaluable / else 13 with the receipt written, the
   both-cleanly-absent MATCH ruling, `--require-paths` on distinct resolved paths, the
   v1 sums/stanza/pipe parse paths, the write guard over measured paths + custody paths
   + sidecar neighbours by path and inode, scratch order `$CUSTODY_PAIR_SCRATCH` →
   `/dev/shm` → `/var/tmp`, v2 self-pinned instrument sha, and 28 selftest cases
   (`EXIT_SELFTEST_FAIL=3`) all match source (case count checked statically; the gate
   selftest was not executed in this lane). The
   only gap is the dead receipt (F2); the advertised argv itself matches the parser and
   the intended capture run.
3. **Signal table (SKILL.md:519-525).** Checked against the retained logs and the installed
   Ghidra 12.1.4 source (`Base-src.zip`): INFO is emitted only when
   `patchVer.getPatch() == goVer.getPatch()` after the base exists
   (`GoApiSnapshot.java` `getPatchVerDiffFile`); WARN fallback then the mapper line echoing
   the requested version (`GoRttiMapper.java` `apiSnapshot.getVer()`), observed in aether
   (`Falling back from 1.25.14 to 1.25.0`, next line `…for version 1.25.14`) and notesmd-cli;
   out-of-range runs log `Untested …` then no snapshot line and `Missing Go bootstrap type
   info` twice (shfmt 1.27.0, containerd 1.27.2, op 1.26.8 — counts 2/2/2), and the
   installed bases stop at `go1.25.0.json`; esbuild 0.27.7 has `build_info: null`
   (`inspect-go.json`) and only `Reading Go binary info` ×2 plus `unable to get
   GoRttiMapper` ×2; aether bootstraps (fallback) then logs `Go analysis failure …`.
   One calibration nuance, not a defect: the `pro-esbuild-0.27.7` route was hand-derived
   from installed source, not emitted by `predict.py` (author field in
   `predictions/pro-esbuild-0.27.7.prediction.json`; knowledge:36-37); the section's
   "predicted from installed source and frozen in Git before the run" still holds, but
   the machine-vs-hand distinction lives only in the knowledge entry and the
   `go-route-predict` row's "no guess" exit.
4. **Section counts and pins.** 8 retained runs, all `carrier-run.exit=0`,
   `compare.exit=0`, `observation.exit=0`, `bound_sessions=1`, `unbound_sessions=0`,
   `pins_compare.equal=true`, `n_pins=146` = carrier + r16 `selection.py` + frozen
   prediction + 143 files under the installed golang dir (matches `find … | wc -l` = 143);
   the 6 `pro-*` rows are labelled prospective in `predictions/carriers.tsv`; every run's
   `analyze.argv` is `npx -y rea-agents@6.5.0`; `session_parent` is `/tmp/kr17-rea-*`;
   the retained log carries exactly one `Using log file:` and the
   `IMPORTING: file://…target-<sha[:12]>.bin` line; `LOG_NAMES` is only
   `ghidra.log`/`script.log`, so `session.json` is never copied.
5. **New registry rows' CLIs/selftests.** All ten advertised `--selftest` forms exit 0
   (pins 7 cases, log-extract 8, predict 17, compare 10, receipt-validate 5 incl. the
   tampered-file red case, buildinfo-probe 11, controls 11, temporal-sweep 6,
   invocation-audit 6, carrier-run 2 incl. the deleted-session-dir assertion). Main exit
   maps 0/1/2 match the rows for log-extract (missing log → 2), predict (empty version →
   2), compare (invalid JSON → 2), pins (`compare` missing file → 2; differ names paths),
   temporal-sweep (no args → 2), invocation-audit (no args → 2), controls (`fail()` →
   2); `log-extract` route comes from the `GoApiSnapshot` component only; `compare`
   compares route fields only when `snapshot_route` is predicted and marks
   `snapshot_label` non-discriminating; `temporal-sweep`'s correction rule is one line
   carrying `R16-PROVENANCE` + exact `file:line` + the required phrase;
   `invocation-audit` strips only `python*` interpreter tokens and relativises in-lane
   absolute paths; `buildinfo-probe` imports no subprocess; `controls.py` reads Git
   objects only.

## Residual risk / verification gaps

- I did not run `verify.py` (it spawns `bash run-carriers.sh`, i.e. a REA analyze run,
  which the lane contract forbids). Consequences of F2 (missing `verification.json`) and
  F4 (destructive rerun, uncommitted `RUNS_DIR`) are therefore reasoned from the source,
  not observed end-to-end.
- I did not execute the custody capture (it reads the five operator paths and writes a
  receipt); its semantics are verified from source and selftest only.
- F2 is discharged if the L1 lands `verification.json` produced by `verify.py` in the
  same landing; the advertised argv templates already match that producer exactly.
