# RunProcontainerdshim — round-17 wave-2 falsification (pro-containerd-shim)

Seat: author-side advisory (leaf, no dispatch). Target: the retained run at
`runs/pro-containerd-shim/` and its producing/inspecting tools, at lane revision
`da64646adcb19c1ede7537b799b8c7d283fe43da`. Receipt bytes are identical committed
vs worktree (`sha256 c29907302d4e429b7d46e663ef06a8db3c31f66aa65102413d610063ceef2313`
for both). The only tracked worktree change under `.ufo/waves/round-17` is
`run-carriers.sh` (uncommitted `RUNS_DIR` patch, see F3); the rest is untracked
wave-2 dispatch metadata.

Method: ran only the round-17 tools against retained bytes, `git` (read-only),
`pacman -Qo`, and `zipfile` reads of the installed `Base-src.zip`. No REA
`analyze`/`search`/`decompile`, no Ghidra, no carrier execution. Python always
`-B`; scratch only under `/tmp`. No installs or updates.

---

## F1 HIGH — `receipt-validate.py` rejects every retained carrier receipt (`unrecognized_shape`); C2's admission gate fails as the artifacts stand

Command (single target, exact):

```
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py \
  .ufo/waves/round-17/runs/pro-containerd-shim/receipt.json
```

Output (abridged; full JSON on stdout), exit **1**:

```
"counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0},
"exit": 1,
"receipts": [{"checks_performed": 306,
  "findings": [{"code": "unrecognized_shape", "detail":
    "receipt matches neither retain nor carrier shape", "where": "$"}],
  "kind": "unknown", "status": "invalid", "valid": false}]
```

All eight receipts, same command with both globs, exit **1**:
`{"invalid": 8, "receipts": 8, "unreadable": 0, "valid": 0}`, codes
`["unrecognized_shape"]`, `checks_performed` 306 for each.

Cause — a container-type interface mismatch between two wave-1 tools, both
committed at `271167473d87…` and unchanged by `da64646`:

- Emitter `tools/carrier-run.py:309` builds `steps = {}`, `:317`/`:349` assign
  `receipt["steps"] = steps` — a **mapping** keyed `inspect-go-binary`/`analyze`
  (`runs/pro-containerd-shim/receipt.json:1826` is `"steps": {`). Its own
  selftest indexes it as a dict (`carrier-run.py:555-558`).
- Validator `tools/receipt-validate.py:98` classifies carrier shape only when
  `isinstance(receipt.get("steps"), list)`; `:284` iterates `enumerate(...)`, so a
  mapping cannot be walked. Its selftest fixture is a list
  (`receipt-validate.py:470`), which is why `--selftest` still prints
  `SELFTEST: CLEAN cases=5`, exit 0.
- `contract.md`'s carrier receipt line says only "every step {argv, cwd,
  started/ended utc, …}" and does not pin list vs mapping — the ambiguity was
  never closed.

The receipt content itself is sound: converting only the container to a list in
`/tmp` (`/tmp/rpcs-receipt-list.json`, no other byte changed) yields
`{"invalid": 0, "valid": 1}`, `checks_performed: 336`, `findings: []`, exit **0**.
So the blocker is the container type alone, not any digest, pin, or field.

Why it matters (all exact anchors):

- `claims.json:22` (C2 falsifiable_before_after): "capability rows … +1 only if
  the capture runs and its receipt validates." On these receipts it does not;
  the row cannot enter on the current validation route (a validator fix, or an
  explicitly different validation command, is required first).
- Wave-1 gate statements that assume exit 0: `w1/ConnCapabilityHistory.md:70`,
  `w1/draft-scorecard.md:46`, `w1/draft-log-entry.md:45`,
  `w1/ReviewCapabilityTable.md:37`, `w1/ConnFleetCorpusRules.md:52`.
- The knowledge entry's documented recheck (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`)
  invokes exactly this command; a rechecker gets exit 1 and no validity signal.
- The run driver never calls it: committed `run-carriers.sh` runs only
  `carrier-run.py`, `log-extract.py`, `compare.py` (lines 19-27). `measure.py:12-13`
  states receipts are counted as blobs and "nothing about its validity is
  measured" (`measure.py:54,147,162`). So the gate is unmechanized *and* the one
  manual validator fails — both halves are needed in the fix.
- Observation from `w2/measure-head.json`: `C2_scorecard_capability_row: 0`, so
  the row is not yet committed; adding it before this is fixed (or reporting
  "receipt validates") would falsify C2's own gate.

Smallest fix (one file, two call sites): in `receipt-validate.py`, accept
`isinstance(steps, (list, dict))` in `classify` (`:95-103`) and normalize
`steps = list(steps.values())` when a mapping before the `:284` loop; add one
mapping-shaped carrier fixture to `--selftest` so the emitter's real shape is
exercised. Also pin the container type in `contract.md`. The alternative
(change `carrier-run.py` to emit a list) also requires editing its selftest
assertions at `:555-558` **and regenerating all eight retained receipts**,
which rewrites the evidence under review — strictly larger and destructive.

[OBSERVATION] exit code, finding codes, and counts above are direct output.
[INFERENCE] no other consumer currently requires the dict shape (I found none in
`tools/`, `measure.py`, `controls.py`).

## F2 MEDIUM — pre-registration commit cited as `2716747`, which is not a Git object

```
git cat-file -t 2716747   → fatal: Not a valid object name 2716747   (exit 128)
```

Two committed occurrences: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37`
("all eight carriers were committed at `2716747` before the first run") and
`run-carriers.sh:2` ("predictions frozen at lane commit 2716747"). The header of
the same knowledge entry (`:1`) and `claims.json` use the correct
`271167473d87ef710f07ecdd98caf0ce12091686`; only the shorthand introduced in the
observation paragraph/driver comment is wrong.

Substance is unaffected: the frozen blob for this carrier is byte-equal
(`cmp` silent; `sha256 847cfc536e6db833a6d5d7af84a931935e1e90636d4f8a0bc0ff4be8c9d3c055`
both from `git show 271167473d87…:…/pro-containerd-shim.prediction.json` and the
working file), and the commit precedes the run:
`git log -1 --format=%ct 271167473d87…` → `1792504005` →
`date -u -d @1792504005` → `2026-10-20T13:46:45Z`, versus
`receipt.steps.analyze.started_at_utc = 2026-10-20T13:52:46.325583+00:00`
(6 min 1 s later). The prediction files also verify against
`predictions/SHA256SUMS` (17/17 `OK`).

Smallest fix: replace both occurrences with the full sha (or `2711674`).
Related coverage note: `w2/citation-drift-head.json` reports
`CITATION_DRIFT_VERDICT: clean findings=0` because that gate checks a fixed
pointer table; it does not scan committed shorthand strings, so this drift is
invisible to it. [OBSERVATION]

## F3 MEDIUM — the documented recheck reruns into `runs/<label>` and deletes the evidence it just validated

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3` says: validate the
receipt, "then rerun one carrier with `bash …/run-carriers.sh <label>` and
compare `observation.json` fields". The committed driver does
`out="runs/$label"; rm -rf "$out"; mkdir -p "$out"` (`run-carriers.sh:14-15`).
Following the documented order therefore replaces the validated
`receipt.json`/`observation.json`/`logs/` with a fresh run before any
comparison, so the retained bytes on disk are no longer the ones validated
(occasionally recoverable from git at `da64646`, but the working-tree evidence
is mutated). The instruction's ordering is ambiguous ("compare the receipt's
`carrier.sha256_pre` first" can be read as before the rerun), but as written the
rerun and deletion precede the `observation.json` comparison.

Smallest fix: commit the `RUNS_DIR` redirection already present uncommitted in
the worktree (`out="${RUNS_DIR:-runs}/$label"`) and change the knowledge recheck
to `RUNS_DIR=/tmp/r17-recheck bash …/run-carriers.sh <label>`; or drop the rerun
clause and keep the receipt/observation digests as the recheck. [OBSERVATION of
committed script + instruction; INFERENCE that the rerun replaces the compared
observation, which is the script's literal behaviour]

## F4 LOW — log/session binding is capture-time only; the validator never re-derives it

`carrier-run.py:126-137` computes `{logfile_ok, target_ok}` and `:353` stamps
`binding` into `retained_logs[]`; the receipt records
`binding: {logfile_ok: true, target_ok: true}`. `receipt-validate.py` contains no
binding logic at all (no `binding`/`Using log file`/`IMPORTING` occurrence) — it
only hashes the retained log. `log-extract.py` does re-derive the same facts into
`log_file_line` and `import_target` (`log-extract.py:85-86`), but no tool
compares them to the receipt's `session_dir`/`carrier`, and `compare.py` ignores
both fields.

Wave 1 had already recommended enforcement here
(`w1/SentinelPollRace.md:70`: "Add this to `log-extract.py` output and enforce it
in `receipt-validate.py`"); the first half landed, the second did not.

I verified binding by hand and it holds for this run (see "verified" item 1), so
this is a missing defensive check, not a failed one. Smallest fix: in
`receipt-validate.py`'s carrier branch, read each retained `ghidra.log`, require
`Using log file: <session_dir>/ghidra.log` and
`IMPORTING: file://<session_dir>/target-<carrier sha256[:12]>.bin`, and emit a
`log_binding_mismatch` finding otherwise.

## F5 LOW (calibration) — the knowledge method asserts a mid-run pin cadence/result the receipt cannot reproduce

`corpus/knowledge/…-go-carrier-diagnostics.md:26-30` says pins "were hashed
before, every 30 s during, and after each session … and no mid-run check
differed". The code does re-snapshot every `PIN_CHECK_S = 30.0`
(`carrier-run.py:35,421-433`), but it records **only failures**
(`pins_changed_during_run`); the key is absent in all eight receipts and no
count or timestamp of mid-run checks is retained. So "no mid-run check differed"
is supported only by absence of a failure record, and "every 30 s during" is a
code-reading claim, not a retained measurement — precisely the distinction the
entry itself gets right two sentences later (`:29`, "identical bytes at those
instants, not continuity between them").

Smallest fix: add `mid_checks: N` (plus the last mid `taken_at_utc`) to each
polled step record, or reword to "re-snapshotted every 30 s during; disagreements
would be recorded (none were)". [OBSERVATION of code + receipts; INFERENCE on
how many checks ran for this carrier — analyze spanned 53.6 s, so at least two
fires, but that count is not in the artifact]

## F6 LOW (calibration) — the "field by field" 5/5 is two independent facts, not five

For this carrier the prediction's five fields are not independent:
`snapshot_label` is matched by a rule the tool itself labels
`"non-discriminating (request echo)"` (`compare.json` `rules`); `snapshot_route:
"none"` and `fallback_to: null` follow from the same no-base precondition as
`missing_bootstrap` (no base JSON → `GoApiSnapshot.EMPTY` → no
`GoApiSnapshot` line → `Missing Go bootstrap type info`). The knowledge entry
states the echo caveat for the `GoRttiMapper` label (`:31-36`) but still presents
the comparison as five checks.

The genuinely discriminating observations are (a) `untested_version 1.27.2`,
which tests `predict.py`'s replication of `GoVer.parse` against Ghidra's own
parse, and (b) `missing_bootstrap: true`, the central runtime fact. That is still
a real pre-registered prediction; the note is about not overreading "5/5". Fix is
wording only (one sentence in the entry/LOG): say two independent facts and name
them. [OBSERVATION of compare rules + prediction `expected`; INFERENCE of
coupling from `GoApiSnapshot.java:111,122-126,148-166`, which the prediction
already cites]

---

## Verified, no finding (bounded)

1. **Log/session binding holds.** Retained
   `logs/rea-ghidra-cxp30X/ghidra.log:2` reads
   `Using log file: /tmp/kr17-rea-l9k4m3ex/rea-ghidra-cxp30X/ghidra.log` and
   `:46` reads
   `IMPORTING: file:///tmp/kr17-rea-l9k4m3ex/rea-ghidra-cxp30X/target-d3aa80d720b8.bin`.
   Receipt `retained_logs[0].session_dir` is the same directory;
   carrier `sha256 = d3aa80d720b80f70721a3e66997fcfc72fdfc4d5ef304094e0173e829dbf370d`,
   whose `[:12]` is `d3aa80d720b8`; `analyze.json` `subject.digest.sha256` and
   the live `/usr/bin/containerd-shim-runc-v2` hash agree; `analyze.json`
   `evidence_id` equals `receipt.steps.analyze.evidence_id`
   (`ev_8a6f88c9927db2ec1b87526cdaf3baf2dd59b3cf574ab84026a7774e731dfe54`).
2. **Fresh extraction reproduces the retained observation byte-for-byte.**
   `log-extract.py --log …/ghidra.log` exit 0; `cmp observation.json /tmp/fresh…`
   silent (`OBS_IDENTICAL`). Output: `classification: bootstrap_missing`,
   `untested_versions: ["1.27.2"]`, `missing_bootstrap: true`,
   `snapshot_labels: []`, `analyzer_errors` = the two `unable to get
   GoRttiMapper` messages, `language_compiler: x86:LE:64:default:golang`,
   `log_sha256: 43c4e92b91241b5959be01e3844c1d0bedadf0368f19871c05cf3cc4c79175c3`
   (matches receipt).
3. **Fresh compare matches, exit 0.** `compare.py --prediction
   predictions/pro-containerd-shim.prediction.json --observation /tmp/fresh…`
   → `all_match: true` for all five fields
   (`untested_version 1.27.2`; `snapshot_label []/null`; `missing_bootstrap
   true/true`; `snapshot_route none/none`; `fallback_to []/null`), exit 0.
   (Contract exit 2 also observed correctly on a nonexistent observation path.)
4. **Prediction is pre-registered and unchanged.** Byte-equal to the blob at
   the frozen commit (per F2), `SHA256SUMS` OK, commit time precedes analyze by
   6 min, and the prediction-time `inspect-go.json` is byte-identical to the
   run-time one (`INSPECT_IDENTICAL`; go_version `go1.27.2-X:nodwarf5`).
5. **Knowledge row for pro-containerd-shim matches the log.**
   `…-go-carrier-diagnostics.md:56`: path and package
   (`pacman -Qo` → `owned by containerd 2.4.2-1`), `sha256[:16]
   d3aa80d720b80f70`, `go1.27.2-X:nodwarf5`, route `none, untested 1.27.2`,
   `Untested Go version [1.27.2]` (log:241,245), no `GoApiSnapshot` line
   (component count in the log: `GoRttiMapper 6`, `GolangSymbolAnalyzer 1`,
   `GolangStringAnalyzer 1`, no `GoApiSnapshot`), `missing bootstrap ×2`
   (log:242,246). All match.
6. **Pins are complete and stable at their instants.** 146 entries =
   143 files under `…/typeinfo/golang` (`find -type f | wc -l`) + carrier +
   r16 `selection.py` + the frozen prediction; all eight receipts
   `pins_pre == pins_post` (`equal: true`), no `missing`/`errors`; `pins_pre`
   completed 26 µs before `inspect-go-binary` started and 0.715 s before
   `analyze` (a re-measured snapshot of the same 146 paths takes 0.047 s, and
   `pins.py` stamps `taken_at_utc` after hashing, so the instant is credible).
7. **Extraction completeness on this log.** All 8 Go-component lines in
   `ghidra.log` are in `go_lines` (independent component count 6+1+1 = 8; no
   Go/Golang mention outside a component). Log is newline-terminated; last
   retained line is 10:53:39 (`ANALYZING changes made by post scripts`), last
   Go line 10:53:18, last copy 13:53:39.481Z, analyze end 13:53:39.982Z — the
   documented `log_capture_limit` and the entry's `:132-133` bound hold; no
   truncated final line.
8. **Prediction source anchors are accurate** (checked in the installed
   `Base-src.zip`): `GoRttiMapper.java:79` `GoVerRange.parse("1.15-1.25")`,
   `:171` `Untested Go version`, `:180` snapshot label;
   `GoVer.java:62,65` parse/truncation; `GoBuildInfo.java:237,488` getGoVer and
   `startsWith("go")`; `GoApiSnapshot.java:111,122-126,148-166` EMPTY return,
   patch-0 base, WARN/INFO route. The prediction's `basis` line numbers resolve
   to those statements.
9. **Run steps and exits.** `carrier-run.exit=0`, `compare.exit=0`,
   `observation.exit=0`; step argv are exactly
   `npx -y rea-agents@6.5.0 inspect-go-binary|analyze <carrier> --format json`;
   `cwd` is the round-17 dir; all eight runs report `all_match: true` with no
   hidden mismatch (checked every `compare.json`).

## Residual risk / verification gaps

- I did not re-run `carrier-run.py`: it launches REA `analyze` (forbidden to
  this seat), so the emitter's runtime behaviour is code-reading plus its
  selftest, not a fresh execution. Its receipt bytes are, however, fully
  digest-verified by the validator (306 checks each, zero digest findings).
- Session directories under `/tmp/kr17-rea-*` are deleted by REA, so I could
  not confirm the original path existed; binding is established from the
  retained log's own bytes and the receipt, as required.
- F1 is a gate/bookkeeping failure, not fabricated evidence: the underlying
  observation and comparison reproduce exactly (items 2-5).
