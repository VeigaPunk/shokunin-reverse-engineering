# ReviewKnowledgeLimits — r17 knowledge entry: provenance trio + Not examined

- **Seat**: KaidokuR17.ReviewKnowledgeLimits (advisory, author-side; leaf).
- **Revision**: `da64646adcb19c1ede7537b799b8c7d283fe43da` (baseline `b563c799…`, freeze `271167473d87ef710f07ecdd98caf0ce12091686`).
- **Target**: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (lines cited below; `nl -ba` numbering).
- **Scope**: the `source:`/`verified-at:`/`recheck:` trio, the `Not examined` section, and QUALITY #4–#9.
- **Method**: read-only. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier execution. Scratch only under `/tmp`; repository tools were copied, never edited. No installs.
- **Working-tree state at review (moving)**: `git status --porcelain` currently shows `M` on `run-carriers.sh`, `receipt-validate.py`, `carrier-run.py`, `compare.py`, `predict.py`, `temporal-sweep.py` — not my edits; an integration pass is landing H1/H2/M1 fixes concurrently. The committed revision `da64646` still has the defects reported below. I ran the working-tree validator on the eight receipts: exit 0, 8/8 valid, 340 checks each; the working-tree script now honors `RUNS_DIR`. The knowledge entry itself is unchanged. Tool line numbers below are the committed revision.

## Direct answers

1. **Is the recheck runnable as written?** At the assigned revision `da64646`: the first half runs but **fails on every retained receipt**: exit `1`, `unrecognized_shape` (all eight). The receipts themselves are byte-intact — a `/tmp` copy with only the shape mismatch fixed returns 8/8 `valid` (336 checks each, exit 0), and the current **working-tree** validator (another seat's uncommitted fix) returns 8/8 `valid`, 340 checks each, exit 0. The second half (`run-carriers.sh <label>`) is destructive and underspecified; see H2.
2. **Does `verified-at` overstate?** No on its checkable clauses: eight sessions, `rea-agents@6.5.0` argv, Ghidra `12.1.4` provider field, `13:47:06.688–14:00:05.228 UTC`, non-overlapping intervals, "author-side" qualifier. The overstatements sit in the Method (mid-run pins) and the recheck, not in `verified-at`. The `source:` line's "before any run" is false for the pilot (L6).
3. **QUALITY #4–#9**: #4 partial (four rows lack absolute paths); #5 partial (two causal clauses unlabelled inside OBSERVATION bullets); #6 partial (`inspect-go-binary` IDs are not in `receipt.json`; the buildinfo-probe check is unretained); #7 partial (the integrated entry dropped its own draft's live limitations and does not name the retained evidence's detail level); #8 partial (provider/Ghidra pinned, but the live claim source is unnamed and the JDK/launch-flags item was dropped); #9 clean (no target-runtime claims; one ambiguous "at runtime" phrase).
4. **Bottom line**: the observations are reproducible; the provenance wrapper is not. Fix H1 before the eight per-run wave-2 seats (`wave2-spec.json:14,19,24,29,34,39,44,49`) repeat the same failure, and before any capability row can pass the `receipt-validate.py` exit-0 gate (`w1/draft-scorecard.md:46`).

## High

### H1 — the recheck command exits 1 on all eight receipts (`receipt-validate.py` classifies the producer's shape as `unknown`)

- **Where**: doc `:3`; `tools/receipt-validate.py:98-101` (classify), `:284` (step iteration), `:459-500` (selftest fixture); `tools/carrier-run.py:275,309,349` (producer).
- **Observation** — exact command from doc `:3` (substituted label) and output:
  ```
  $ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py \
      /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/pro-aether/receipt.json
  {"counts":{"invalid":1,"receipts":1,"unreadable":0,"valid":0},
   "exit":1, "pins_available":true,
   "receipts":[{"checks_performed":306,
     "findings":[{"code":"unrecognized_shape",
                  "detail":"receipt matches neither retain nor carrier shape",
                  "where":"$"}],
     "kind":"unknown","status":"invalid","valid":false}],
   "tool":"receipt-validate.py"}
  EXIT=1
  ```
  Same result for all eight (loop over `runs/*/receipt.json`): `kind=unknown`, `unrecognized_shape`, exit 1.
- **Cause** (observation from source): `classify()` requires `isinstance(receipt["steps"], list)`, but `carrier-run.py` writes `"steps": {}` and fills it by name (`steps["inspect-go-binary"]`, `steps["analyze"]`, `steps["search:…"]`). The selftest fixture at `receipt-validate.py:470` uses a **list** (`"steps": [{…}]`), so `--selftest` is green (`SELFTEST: CLEAN cases=5`, exit 0) while no real receipt can pass. `W1/ReceiptValidateTool.md:11,22` recorded the assumption and predicted `missing_field` on divergence; the actual result is `unrecognized_shape`. The only finding was `unrecognized_shape`; no digest finding was emitted (`checks_performed=306`), so the failure is classification-only.
- **Fix verification** — copied validator + `pins.py` to `/tmp`, two minimal changes (`isinstance(..., (list, dict))`; `steps = list(steps.values())` when dict), then:
  ```
  $ python3 -I -B /tmp/rv2.py <the eight explicit receipt paths>
  {"counts":{"invalid":0,"receipts":8,"unreadable":0,"valid":8},"exit":0}
  each: kind="carrier", checks_performed=336, findings=[]
  ```
  The working tree now contains an equivalent fix plus a `check_binding` block (another seat's edit); the working-tree tool on the same eight paths gives `8/8 valid`, `340` checks each, exit 0. My run of it is at `/tmp/rv-wt.json`.
- **Severity**: high at `da64646` (the only stated recheck fails; C2's receipt-validates gate is unreachable). The working-tree fix, once committed, clears this.
- **Smallest fix**: at `receipt-validate.py:98` accept `(list, dict)`; at `:284` iterate `steps.values()` when `steps` is a dict; keep a dict-shaped selftest fixture (the working-tree fixture is now a dict — do not regress it to a list). Commit the working-tree fix. Do not change `carrier-run.py` to a list — that would invalidate the eight retained receipts.

### H2 — the second half of the recheck destroys the retained run and names fields that must differ

- **Where**: doc `:3`; `run-carriers.sh:14-15`; `runs/pro-aether/observation.json` keys.
- **Observation**:
  ```
  $ git show da64646:.ufo/waves/round-17/run-carriers.sh | nl -ba | sed -n '14,15p'
  14  out="runs/$label"
  15  rm -rf "$out"; mkdir -p "$out"
  ```
  (The working tree now changes `:14` to `out="${RUNS_DIR:-runs}/$label"`; the `rm -rf` remains.) Following the doc's `bash …/run-carriers.sh <label>` deletes `runs/<label>/` — `receipt.json`, `inspect-go.json`, `analyze.json`, and the retained `logs/<session>/ghidra.log|script.log` — **before** the rerun. The old run is committed at `da64646` (113 tracked paths under `runs/`), but the doc never says so, and the doc's `:3` text does not use `RUNS_DIR`.
  `observation.json` contains run-specific fields: `log_path=/home/…/runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log`, `log_sha256=f39c3293…`, `log_bytes=22462`, `log_file_line=/tmp/kr17-rea-0o3ukbw2/rea-ghidra-JpGezV/ghidra.log`, `import_target=/tmp/kr17-rea-0o3ukbw2/rea-ghidra-JpGezV/target-06c91f55df41.bin`, and `go_lines[].line`. A rerun necessarily changes the `/tmp` paths, the log digest and byte count, and may change line numbers; a naive JSON diff always fails.
- **Severity**: high for recheck reproducibility (the instruction, if followed, deletes the evidence it then asks you to compare; the first command's exit 1 is a de-facto guard only for a careful reader).
- **Smallest fix**: `RUNS_DIR=/tmp/rr-<label> bash /home/…/run-carriers.sh <label>`; compare `carrier.sha256_pre` **before** rerunning; compare only `untested_versions`, `snapshot_labels`, `missing_bootstrap`, `snapshot_route`, `snapshot_fallbacks`, `analyzer_errors`, `bootstrap_attempts`, `classification`, `language_compiler`; state that `log_path`, `log_sha256`, `log_bytes`, `log_file_line`, `import_target`, `go_lines[].line` are run-specific and must differ.

## Medium

### M1 — "no mid-run check differed" has no retained instants (QUALITY #19)

- **Where**: doc `:26-30`; `carrier-run.py:35` (`PIN_CHECK_S = 30.0`), `:422-432` (mid-check records only failures).
- **Observation**: every receipt has `pins_pre`/`pins_post` with `taken_at_utc` and `pins_compare.equal:true`; none has `pins_changed_during_run` and none has a `pin_checks`/mid-check timestamp list. The mid-check loop re-snapshots all 146 paths every ~30 s and writes a record **only when `cmp_mid["equal"]` is false**. The doc's "hashed before, every 30 s during, and after each session (`tools/pins.py`)" attributes the loop to `pins.py`; the loop is `carrier-run.py:420-432`, and the instants are not retained. The working-tree validator now looks for `step.pin_checks` in its new `check_binding` block, but `carrier-run.py` is unmodified and emits only `pins_changed_during_run` on failure — so that branch is dead for the current receipts and the gap survives the validator fix.
- **Severity**: medium (the pre/post maps satisfy #19; the mid-run sentence is an unrecorded measurement presented as retained evidence).
- **Smallest fix**: either record `pins_checks: [{taken_at_utc, equal}]` (count plus first/last instant is enough) in `receipt.json`, or reword to "no failure was recorded (`pins_changed_during_run` absent in all eight); mid-check instants are not retained", and cite `carrier-run.py:420-432`.

### M2 — `Not examined` dropped its own draft's live limitations (QUALITY #7; also #5/#8)

- **Where**: integrated `:122-133`; draft `w1/draft-knowledge-r17.md:128-143`.
- **Observation**: the integrated section keeps only patched-content, other providers/versions/OS, determinism, procedure inventories and log completeness. The draft's higher-value items are absent:
  - `:131` "Any target execution. Carriers are never run (contract)." — the integrated entry never says the targets were not executed.
  - `:137` "Ghidra class identity. The S003 source archive is not authenticated against the classes the installed provider loads (r14 limitation, unchanged)."
  - `:140` "Python source model fidelity. `selection.py` models file selection, not Java/Gson parsing; base-file parse and record usability were not checked." The integrated Method (`:31-40`) says predict.py "applies `GoVer.parse`" and "calls r16 `select_snapshot`", which reads as source-exact; `predict.py`'s own docstring says the selection module *models* `getApiSnapshotJsonFile`/`getPatchVerDiffFile`/`read`.
  - `:136` bundle sufficiency (range alone vs snapshot alone not tested); `:141` `GoRttiMapper.getSharedGoBinary` caching and the second analyzer pass; `:142` `ReaGhidraNoReturnFix` effect (the script actually ran: `script.log` shows `cleared=2 sites=3274 refit=952` for shfmt); `:143` JDK version and Ghidra launch flags.
  - **Detail level**: all eight `analyze.json` have `operation: binary_overview` and `relationship_coverage: null`; the entry nowhere says the retained REA evidence is an overview (no function/xref/decompile view), which #7 names explicitly.
- **Severity**: medium-high (this is the entry's central inference surface: "the source model predicted the route" is a Python-model prediction, not the provider's Java/Gson code).
- **Smallest fix**: add the three highest-value bullets — target execution, Python-model vs Java/Gson fidelity, S003 archive vs loaded classes — plus one sentence that the analyze evidence is `binary_overview` with `relationship_coverage: null`; optionally restore bundle sufficiency, the no-return script, and JDK/launch flags.

### M3 — four table rows lack the absolute path QUALITY #4 requires

- **Where**: doc `:52,53,55,58`; `predictions/carriers.tsv:2,3,5,8`.
- **Observation**:
  - `:52` `kimi-code pnpm @esbuild/linux-x64@0.25.12` — no absolute path; exact path is `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild` (`carriers.tsv:2`, `receipt.carrier.path`).
  - `:53` `~/.local/bin/notesmd-cli` — `~` is not absolute; exact `/home/vgpnk/.local/bin/notesmd-cli` (`carriers.tsv:3`).
  - `:55` `pnpm @esbuild/linux-x64@0.21.5` — no path; `carriers.tsv:5`.
  - `:58` `pnpm @esbuild/linux-x64@0.27.7` — no path; `carriers.tsv:8`.
  QUALITY #4 (`corpus/QUALITY.md:14`) requires "absolute path plus a stable identity". The `sha256[:16]` prefixes all match the receipts; full digests are only in the receipts (`:60`).
- **Severity**: medium (the entry alone does not locate four artifacts; the information exists one directory away).
- **Smallest fix**: replace the four cells with the absolute paths already in `predictions/carriers.tsv`, keeping the package descriptors as a parenthetical.

### M4 — the sentence "inspect-go-binary and analyze Evidence IDs … are in each receipt.json" is false for `inspect-go-binary`

- **Where**: doc `:60-61`; `runs/*/receipt.json` `steps["inspect-go-binary"]`; `runs/*/inspect-go.json`.
- **Observation**: all eight `steps["inspect-go-binary"]` records have `argv, cwd, started_at_utc, ended_at_utc, exit, stdout_path, stdout_sha256, stderr_path, stderr_sha256` (and no `evidence_id`). The inspect ID is only in the output file, e.g. `runs/calib-shfmt/inspect-go.json` `evidence_id = ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`. The analyze IDs are parsed into the receipt (`carrier-run.py:333-334`) and match the two examples at doc `:62-65`.
- **Severity**: medium-low (QUALITY #6 reproducibility; a verifier looking in the receipt for the inspect ID finds nothing).
- **Smallest fix**: either change the sentence to "analyze Evidence IDs … in `receipt.json`; `inspect-go-binary` IDs in `inspect-go.json`", or parse the inspect output in `carrier-run.py:312-314` as is already done for analyze.

### M5 — the historical `op` inference is under-informed by its own cited source

- **Where**: doc `:117-120`; `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:69`.
- **Observation**: the entry says the r4-10 `op` 2.40.0 collapse "belongs to the same missing-base class **only if** that build was go1.26.x", and "That package is no longer installed, so its cause stays UNKNOWN." r4-10 already records `op-2.40.0` as `(go1.26.8)` (`:69`), and this round's `pro-op` 2.41.0 is also go1.26.8 and routes `none` / `bootstrap_missing` (`observation.json`). The version condition is known; what is unknown is whether 2.40.0's run took the missing-base path rather than a layout path (its binary and log are gone).
- **Severity**: medium-low (calibration: the sentence implies a version uncertainty that the cited source resolves).
- **Smallest fix**: "r4-10 records `op-2.40.0` as go1.26.8; the current 2.41.0 (also go1.26.8) routed missing-base, so the class is demonstrated for this minor on this installation; whether 2.40.0's collapse used this path remains UNKNOWN because its binary and log are gone."

## Low (precision and citation depth)

- **L1 — unresolvable commit abbreviation `2716747`** (doc `:37`; also `run-carriers.sh:2`). `git rev-parse --verify 2716747^{commit}` → `fatal: Needed a single revision`; `2711674` → `271167473d87ef710f07ecdd98caf0ce12091686` (freeze time `2026-10-20 13:46:45 UTC`, first analyze `13:47:06.688 UTC`). Fix: `2711674` or the full hash in both places.
- **L2 — `TransientProgramProperties.java` is not in the `source:` header's S003 member list** (doc `:1` vs `:77`). The file is in the same archive: `unzip -l …/Base-src.zip | grep TransientProgramProperties` → `ghidra/app/plugin/core/analysis/TransientProgramProperties.java`. Fix: add the member to the S003 parenthetical.
- **L3 — two unlabelled causal clauses inside OBSERVATION bullets** (doc `:77`, `:81`). `:77` "because a null mapper is not cached (`TransientProgramProperties.java:107-110`)" is a source inference; `:81` "which comes from section names, not build info" is an inference whose basis is `predictions/pro-esbuild-0.27.7.prediction.json` (`ElfLoader.java:188-200`, `GoRttiMapper.hasGolangSections :201-210`), not the log. Fix: label both INFERENCE or split them into the labelled section with those anchors.
- **L4 — "at runtime" reads as target runtime** (doc `:71-72`). The entry means the analyzer session; the entry makes no target-execution claim (and `claims.json` non-claims say carriers are never run). Fix: "in the analyze session".
- **L5 — `run-log.txt` omits `calib-shfmt`** (`runs/run-log.txt`, 14 lines; first line `== calib-esbuild-0.25.12 start 2026-10-20T10:47:42-03:00`). `predictions/carriers.tsv:1` is `calib-shfmt`; its receipt's analyze starts `13:47:06.688` (earliest), and its `orig_argv` carries the script's 144 `--pin` shape. So the log is not the unedited stdout of the committed script (or is truncated). Fix: append the missing two lines with a named correction, or delete the log and cite the receipts; do not silently edit.
- **L6 — "before any run" is false for the pilot** (doc `:1`, `:37`). Pilot runs were `10:17–10:19 -03` = `13:17–13:19 UTC` (`pilot/README.txt:1`, `pilot/*/ghidra.log` first lines); the freeze is `13:46:45 UTC`. The next sentence discloses the pilot. Fix: "before the first measured (non-pilot) run".
- **L7 — timezone not stated** (doc `:2`). The `verified-at` window is UTC (`13:47–14:00`), while the retained logs carry host-local `10:47–11:00` (`ghidra.log:82` etc.). Fix: add "(log timestamps are host-local, -03; receipts are UTC)".
- **L8 — "zero unbound sessions" is narrower than written** (doc `:25`). `receipt.unbound_sessions` is the set of *retained* logs that failed the two binding lines; a session the poller never saw would not appear. Fix: "zero retained unbound sessions" (or "no missed session is evidenced").
- **L9 — provider version's live claim source is unnamed** (doc `:2`, `:98`). All eight `analyze.json` `analysis_profile.parameters.upstream_analysis_profile.provider` = `{id: ghidra, name: Ghidra, version: 12.1.4}`; #8 asks for the claim source. Fix: cite that field (and note the JDK/launch flags under M2).
- **L10 — decision-table row includes an untested disjunct** (doc `:106`: "No build-info record (or no fallback version)"). Only the first disjunct is observed (0.27.7 has `build_info: null`); the 0.27.7 prediction's `uncertainty` says the `fromFallbackInfo` default was not opened. Fix: split the row or mark the second disjunct "(source-inference, untested)".
- **L11 — `GoRttiMapper.java:179-180` is one hop short of "requested"** (doc `:42-43`). Those lines format `apiSnapshot.getVer()`; the request-echo is established by `GoApiSnapshot.get` `:111` (`read(is, archSearchOrder, goVer)`) and `read` `:239` (`new GoApiSnapshot(ver, results)`). Fix: cite `GoApiSnapshot.java:111,239` alongside.
- **L12 — the buildinfo-probe check is unretained** (doc `:79-80`). The claim is true — I ran `python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.27.7/node_modules/@esbuild/linux-x64/bin/esbuild` → `{"found": false, "go_version": null, "header_offset": null, "magic_file_offsets": [], "sha256": "c638273fcf95573ca74af586677800b4dd874c55f8f945adb54316d6902ba14b"}`, exit 0 — but the entry gives no command, no full target digest, and no retained output (`w2/.st-buildinfo-probe.py.out` is a selftest, not the carrier run). Fix: add the command and `found:false`/`sha256`, or retain `probe.json` under `runs/pro-esbuild-0.27.7/`; cite S024.
- **L13 — "REA deletes its Ghidra runtime root" is uncited** (doc `:11-12`). It is supported by `runs/*/analyze.json` limitations ("The imported Program and temporary project are ephemeral and deleted on close") and `w1/RevReaLifecycle.md:30,53,135-154`; the entry cites only r4-10 for the old log. Fix: add one of those anchors.

## Bounded no-findings (checked; held)

- **Log binding**: all eight `ghidra.log` contain `Using log file: <bound session>/ghidra.log` and `IMPORTING: file://<bound session>/target-<carrier sha256[:12]>.bin`, and `bound_sessions`/`unbound_sessions` are `1/0`; enforced at `carrier-run.py:126-137,357-358`. The doc's rule is accurate.
- **Pins**: every receipt pins exactly 146 paths = 143 files in `…/typeinfo/golang` + carrier + r16 `selection.py` + the frozen prediction; `pins_compare.equal:true` in all eight; the patched validator re-ran `pins.compare` with no mismatch. The "146" claim is exact.
- **Exit codes**: `carrier-run.exit`, `observation.exit`, `compare.exit` are 0 for all eight; both steps (`inspect-go-binary`, `analyze`) exit 0.
- **Sequentiality**: analyze intervals are non-overlapping (min start `13:47:06.688`, max end `14:00:05.228` UTC); the two `calib-*` are the pilot-seen carriers, the six `pro-*` have no pilot JSON.
- **Table values**: all eight `sha256[:16]` prefixes, build-info versions (`go1.27.0-X:nodwarf5`, `go1.23.12`, `go1.25.8`, `go1.25.14`, `go1.20.12`, `go1.27.2-X:nodwarf5`, `go1.26.8`, `null`), routes, labels, type counts (`4881/2302/6115/4411` from `Found N Go types`), `Go strings found: 7200`, `Missing Go bootstrap type info` ×2, `bootstrap_attempts` 2 for the out-of-range/mapper-null carriers and 1 for the bootstrapped ones, and `language_compiler = x86:LE:64:default:golang` all match the logs/observations. `0.27.7`'s log has only two `Reading Go binary info` plus two `unable to get GoRttiMapper`.
- **Evidence IDs**: `calib-shfmt` `ev_2b29a1dd…` and `pro-notesmd-cli` `ev_4fd342dd…` match the receipts; the pilot `shfmt.json`/`esb.json` IDs are the same `ev_2b29…`/`ev_391…`, with pilot log times `10:17:30`/`10:18:20` vs run `10:47:06`/`10:47:43` (~29.5 min), so "about 30 minutes apart" holds. `analyze.json`'s `operation` is `binary_overview` in all eight.
- **Predictions**: commit `2711674` contains all eight prediction files; `git diff 2711674 -- predictions/` is empty; `predict.py --go-version ''` exits 2 with `unparseable Go version '' (post-strip ''): GoVer.INVALID` (so the "refuses an empty version" statement is true); `compare.exit` is 0 for all eight (the tool exits 0 only when every field matches), and the inspected `runs/pro-aether/compare.json` shows the five fields (`untested_version`, `snapshot_label`, `missing_bootstrap`, `snapshot_route`, `fallback_to`) with `all_match:true`.
- **Provider/versions**: all eight `analyze.json` `upstream_analysis_profile.provider.version = 12.1.4`; all eight `steps.analyze.argv` contain `rea-agents@6.5.0`. `pacman -Q` gives `shfmt 3.14.1-1`, `aether 4.32.0-2`, `containerd 2.4.2-1`, `1password-cli 2.41.0-1`, matching the table.
- **Source anchors**: `GoBuildInfo.java:488-489`, `GoVer.java:62-81`, `GoRttiMapper.java:79`, `:170-172`, `GoApiSnapshot.java:122-126`, `:158-161`, `:162-164`, `TransientProgramProperties.java:107-110` all match the installed `Base-src.zip` (the `:179-180` caveat is L11). The aether citation `:97-177` covers the error line (`:97`), the `GoInterfaceType.additionalMarkup` frames (`:124,138`) and the `EOFException` (`:177`), so "during interface-type markup" is log-supported.
- **Not-examined claims**: no `search` step in any receipt; no patch/arch log line; all eight carriers are `amd64 elf`; the retained log's tail includes the bridge script and `ANALYZING changes made by post scripts`, so "every Go line precedes the bridge script" holds and the absence caveat is correctly bounded.
- **QUALITY #9**: no target-behavior claim anywhere; the aether cause is explicitly UNKNOWN and the entry says the run does not show the fallback data caused it. Only the L4 wording is imprecise.

## Residual risk and verification gaps

- I did not run `carrier-run.py`/`run-carriers.sh` (forbidden REA `analyze`); the rerun half of the recheck is inspected, not exercised. The `/tmp` patched validator is mine; I did not edit the repository tools. The working-tree `receipt-validate.py`/`run-carriers.sh` changes are another seat's (see header).
- The mid-run pin check was not exercised; its behavior is read from source, and the receipts cannot falsify a missed check (that is M1).
- The `run-log.txt` discrepancy (L5) could not be resolved from the retained files; I did not infer who removed the two lines.
- The working-tree edits to `run-carriers.sh`/`receipt-validate.py` are another seat's; I verified the validator's 8-receipt result (exit 0, 340 checks) but did not review the rest of that diff (e.g., `check_binding`'s path handling). This report is anchored to `da64646`; re-run the doc's recheck after the L1 integrates the working tree.
- The eight wave-2 per-run tasks (`wave2-spec.json:14-49`) run the same command; at `da64646` they all fail (H1), but the working-tree fix would clear them. Confirm the committed tool before relying on their reports.
- No tool installs or upgrades were needed or made.
