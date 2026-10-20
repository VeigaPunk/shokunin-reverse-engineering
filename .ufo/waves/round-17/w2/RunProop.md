# W2 falsify — retained run `runs/pro-op` (round 17)

Target: `.ufo/waves/round-17/runs/pro-op/` at lane rev `da64646adcb19c1ede7537b799b8c7d283fe43da`
(baseline `b563c799…`, predictions frozen at `271167473d87ef710f07ecdd98caf0ce12091686`).
All commands below are read-only. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier executed;
Python run with `-I -B`; scratch under `/tmp`. Nothing verified here was re-run to confirm a user report.
There is no runtime-routing/resume surface in this artifact set, so `resume_continuity_v1` and
same-identity rerouting checks are N/A.

---

## F1 — BLOCKER — `receipt-validate.py` cannot validate any receipt the producer writes

**Path:line.** `.ufo/waves/round-17/tools/receipt-validate.py:98` classifies a carrier receipt only when
`isinstance(receipt.get("steps"), list)`; `.ufo/waves/round-17/tools/carrier-run.py:309,349` builds
`steps` as a **dict** keyed by step name (`analyze`, `inspect-go-binary`). The validator's carrier
selftest fixture uses a list (`receipt-validate.py:470`), so the selftest is green while no real
receipt can pass.

**Command and output (target receipt):**

```
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py \
  .ufo/waves/round-17/runs/pro-op/receipt.json
```
exit 1:
```
"counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0}, "exit": 1
"checks_performed": 306, "kind": "unknown",
"findings": [{"code":"unrecognized_shape",
              "detail":"receipt matches neither retain nor carrier shape","where":"$"}]
```
The same exit 1 / `kind=unknown` / `unrecognized_shape` was returned for each of the eight
`runs/<label>/receipt.json` (calib-shfmt, calib-esbuild-0.25.12, pro-notesmd-cli, pro-aether,
pro-esbuild-0.21.5, pro-containerd-shim, pro-esbuild-0.27.7, pro-op).

**Depth probe — the shape is the only blocker.** Copy of the identical receipt with `steps` converted
`dict -> list` (values only), `/tmp/pro-op-steps-list.json`:

```
receipt-validate.py /tmp/pro-op-steps-list.json   -> exit 0, checks_performed 336, findings []
```
So every digest, pin entry and `pins.compare` re-run in the real receipt passes; only the container
type is rejected. Patching only `classify` in a `/tmp` copy to accept `(list, dict)` still exits 1 with
two `field_type` findings (`$.steps[0]`, `$.steps[1]`, "step is not an object") because
`receipt-validate.py:284` iterates `receipt.get("steps")`, i.e. the dict's **keys**.

**Smallest fix (two edits in the consumer, one canonical shape):**
1. `classify`: accept `(list, dict)`.
2. In `check_required`, normalise once: `steps = receipt.get("steps") or []`;
   `steps = list(steps.values()) if isinstance(steps, dict) else steps`, then enumerate.
3. Add one end-to-end selftest case that writes a receipt from `carrier-run.py`'s shape (`steps` dict,
   `"steps": {"analyze": {...}, "inspect-go-binary": {...}}`) rather than the list fixture at
   `:470`. No carrier re-run is needed to clear F1.

This divergence was flagged as an unverified assumption in wave 1 —
`.ufo/waves/round-17/w1/ReceiptValidateTool.md:22` ("if CarrierRunTool diverges, validation yields
`missing_field` findings rather than exit 2") — and integration at `da64646` did not reconcile it.

## F2 — HIGH — the round's own admission gate and knowledge `recheck:` are red as produced

**Path:line.** `claims.json:22` ("capability rows 4 … -> +1 only if the capture runs and its receipt
validates"); `.ufo/waves/round-17/w1/ConnCapabilityHistory.md:70` ("each `receipt-validate.py` exit 0");
`w1/ReviewCapabilityTable.md:37` (D2); `w1/ConnFleetCorpusRules.md:52` (K19);
`w1/draft-scorecard.md:46` ("Entry condition: `receipt-validate.py` exit 0 … Otherwise no row is added").
The knowledge entry's own recheck command
(`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`) invokes exactly the failing command.

**Command and output.** The recheck command above returns exit 1 for `pro-op`. Consequence: on the
artifacts as landed, C2's capability row **must not** be entered and `validate_exit` must not be
filled with 0; the knowledge entry's `recheck:` line is currently self-falsifying.

**Smallest fix.** Fix F1, then re-run `receipt-validate.py` over the eight receipts (no carrier rerun;
their bytes already pass — 336 checks on the list-shaped copy) and record the exit. If L1 instead
elects not to change tools this round, drop the capability row and state the red gate verbatim in
LOG/SCORECARD. Do not record `receipt-validate.py` exit 0 without running it.

## F3 — MEDIUM — stale frozen-commit token `2716747` is not a revision

**Path:line.** `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37` ("committed at `2716747`")
and `.ufo/waves/round-17/run-carriers.sh:2` ("predictions frozen at lane commit 2716747").

**Commands and output:**
```
git rev-parse --verify 2716747
  fatal: Needed a single revision
git rev-parse --verify 2711674
  271167473d87ef710f07ecdd98caf0ce12091686
```
The correct full SHA is already in the same entry at line 2 and line 1. The evidence itself survives
(see “Verified”): prediction bytes are identical at `2711674`, at `da64646`, and in the working tree;
`git merge-base --is-ancestor 2711674 HEAD` = 0; commit time `2026-10-20T13:46:45Z` precedes pin-pre
`13:55:55.592Z` and analyze start `13:55:56.407Z`.

**Smallest fix.** Replace both tokens with `271167473d87ef710f07ecdd98caf0ce12091686` (append-only
correction in the knowledge entry). This is the R16 citation-drift class that C1(b) claims to
discharge; it is present in a committed artifact.

## F4 — MEDIUM — the documented repro deletes the retained evidence it tells you to compare

**Path:line.** `corpus/knowledge/…-go-carrier-diagnostics.md:3` says "rerun one carrier with
`bash …/run-carriers.sh <label>` and compare `observation.json` fields";
`run-carriers.sh:15` executes `rm -rf "$out"; mkdir -p "$out"` before the run, where
`out="${RUNS_DIR:-runs}/$label"` (`:14`). Running the documented command for `pro-op` destroys
`runs/pro-op/` (receipts, retained logs, observation, compare) first.

**Smallest fix.** Document the existing override:
`RUNS_DIR=/tmp/r17-recheck bash run-carriers.sh pro-op`, then compare `runs/pro-op/observation.json`
to `/tmp/r17-recheck/pro-op/observation.json` using `carrier.sha256_pre` as the equality guard. (Or make
`rm -rf` conditional on an explicit `--force`.)

## F5 — LOW — mid-run pin checks are not evidenced in the receipt

**Path:line.** `corpus/knowledge/…-go-carrier-diagnostics.md:26-29` claims 146 paths "were hashed before,
every 30 s during, and after each session … no mid-run check differed". The code does check every
`PIN_CHECK_S = 30.0` (`carrier-run.py:35,425`) but records **only on mismatch**
(`carrier-run.py:430`, `rec["pins_changed_during_run"]`). `runs/pro-op/receipt.json.steps.analyze` has
no `pins_changed_during_run`, and no pin-check count/timestamp field exists.

**Observation.** The sentence is supported by reading the producer, and is falsifiable only by
trusting that the branch executed; a receipt-only auditor cannot distinguish "checks ran, all equal"
from "checks never ran". The pre/post claim at `:28-29` is fully receipt-backed (146 entries, 0 error
entries, `pins_compare.equal=true`, `changed=[]`, `errors=[]`).

**Smallest fix.** Add `pin_checks` (int) and `last_pin_check_utc` to the polled-step record; then the
knowledge sentence is receipt-evidenced without changing any claim.

## F6 — LOW — `receipt-validate.py` does not recompute the log binding (self-asserted booleans)

**Path:line.** The validator has no reference to `binding`, `logfile_ok`, `log_file_line` or
`import_target` (`grep -n "import_target\|logfile_ok\|binding\|log_file_line\|evidence_id"
tools/receipt-validate.py` → no match). The receipt's
`retained_logs[0].binding = {logfile_ok: true, target_ok: true}` is trusted. This is the enforcement
recommended by `w1/SentinelPollRace.md:70` and not implemented.

**Observation for this run (manual, independent).** Binding holds:
`runs/pro-op/logs/rea-ghidra-yRmWqx/ghidra.log:2`
`Using log file: /tmp/kr17-rea-_qnkq6vy/rea-ghidra-yRmWqx/ghidra.log`; `:46`
`IMPORTING: file:///tmp/kr17-rea-_qnkq6vy/rea-ghidra-yRmWqx/target-f4ac474fd020.bin`; carrier
`sha256=f4ac474fd0202c73…` ⇒ prefix `f4ac474fd020` matches; `:103` `REPORT: Analysis succeeded for file:
file:///…/target-f4ac474fd020.bin`. `session_dir` in the receipt is exactly the directory named in both
lines, and the retained subdirectory is `logs/rea-ghidra-yRmWqx`. So no wrong-log finding — only a
checking-tool gap (a forged `binding: {true,true}` would not be caught).

**Smallest fix.** In `receipt-validate.py`, for every `retained_logs[]` entry, assert the log text
contains `Using log file: <session_dir>/ghidra.log` and
`IMPORTING: file://<session_dir>/target-<carrier.sha256_pre[:12]>.bin`; emit `binding_mismatch`
otherwise.

## F7 — LOW — retained batch console log omits the first of the eight runs

**Path:line.** `.ufo/waves/round-17/runs/run-log.txt:1` starts at `== calib-esbuild-0.25.12 start
2026-10-20T10:47:42-03:00`; the `calib-shfmt` pair is absent, although its receipt shows analyze
`13:47:06.688Z → 13:47:37.309Z` (10:47:06–10:47:37 local), immediately before. File is 14 lines /
872 bytes, and the committed blob equals the working file
(`git show da64646:…/runs/run-log.txt | sha256sum` = working sha
`0d2dd4c0e1aef0ae8a97a083f065bb093d4778354e2829bda0a0fcf36242dfcc`), so this is an original-shaped gap,
not later tampering. It is not cited by the knowledge entry; impact is bookkeeping only (a reader
counting runs from this file sees 7).

**Smallest fix.** Append the two reconstructed `calib-shfmt` lines with a note that they come from
`runs/calib-shfmt/receipt.json` timestamps, or title the file as covering 7/8 runs.

---

## Verified (bounded no-finding)

Checked with the exact commands named; every item below held.

| Check | Evidence |
|---|---|
| Prediction bytes == frozen blob | `git show 2711674:.ufo/waves/round-17/predictions/pro-op.prediction.json` sha256 `d13875e2…` == working file == blob at `da64646`; 2064 bytes |
| Freeze precedes run | commit `2026-10-20T13:46:45Z`; prediction pin mtime `13:46:29.550Z`; `pins_pre` `13:55:55.592Z`; analyze start `13:55:56.407Z`; ancestor checks exit 0 |
| Pins | 146 paths (143 Go-data files + carrier + r16 `selection.py` + prediction), 0 `error` entries, `pins_compare.equal=true`, `changed=[]`, post `14:00:05.292Z` brackets the step end `14:00:05.229Z` |
| Receipt digests | list-shaped copy of the same receipt → exit 0, 336 checks, 0 findings; carrier sha pre==post==current `/usr/bin/op` `f4ac474f…`; `analyze.json` sha `5d4d1eb6…`; `carrier-run.stdout` differs from `receipt.json` only by `receipt_path` |
| Log binding + completeness | `ghidra.log:2` and `:46` as quoted above; 115 lines, 10927 bytes, newline-terminated; last retained copy `14:00:04.728Z` (0.5 s before exit); all Go lines (`:68-75`) precede the bridge script (`:110-114`), so the “all Go lines captured” claim holds for this run |
| Observation reproduced | `log-extract.py --log runs/pro-op/logs/rea-ghidra-yRmWqx/ghidra.log` output is byte-identical to retained `observation.json` (sha `7729b215…` log; fields: untested `["1.26.8"]`, `snapshot_labels []`, `missing_bootstrap true`, `classification bootstrap_missing`, language `x86:LE:64:default:golang`, `bootstrap_attempts 2`) |
| Compare | `compare.py --prediction predictions/pro-op.prediction.json --observation <fresh>` exit 0, 5/5 fields match; re-compare against retained observation exit 0 (only the path strings in `prediction`/`observation` differ, from cwd-relative invocation) |
| Prediction is mechanical, not hand-written | `predict.py --go-version go1.26.8 --golang-root …/typeinfo/golang` output is **exactly equal** to the frozen file (all six keys incl. `basis`, `selection`, `expected`) |
| Knowledge row vs log | `knowledge:57` pro-op row: `go1.26.8`, `f4ac474fd0202c73`, “none, untested 1.26.8”, “no snapshot line; missing bootstrap ×2”, bootstrap missing — matches `ghidra.log:68-75`, which contains exactly two `Untested Go version [1.26.8]` and two `Missing Go bootstrap type info` and no `GoApiSnapshot`/`snapshot` line (`grep -in snapshot` → none) |
| Build-info column independent | `go version -m /usr/bin/op` → `go1.26.8`; `pacman -Qo /usr/bin/op` → `1password-cli 2.41.0-1`; `inspect-go.json` `go_version go1.26.8`, `header_offset 29405184`, inline |
| Run sequencing | eight analyze intervals 13:47:06→14:00:05Z, ~1 s gaps, no overlap; pro-op dominates at 4 m 09.8 s (polls 496, 494 log polls) |
| Every run bound once | all eight receipts: `bound_sessions` length 1, `unbound_sessions []`; leftovers recorded as `node-compile-cache` under each private `TMPDIR` |
| Exits | all eight: `carrier-run.exit=0`, `inspect-go-binary.exit=0`, `analyze.exit=0`, `observation.exit=0`, `compare.exit=0` |
| Pilot claim | `pilot/README.txt` + `pilot/SHA256SUMS`: only shfmt `58f76563…` and esbuild 0.25.12 `bab29b2c…` were pilot carriers; the six `pro-*` were unseen |
| Source-law anchors cited by prediction/knowledge | `GoRttiMapper.java:79` `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`; `:170-171` range check + `Untested Go version [%s]`; `:179-180` request echo; `:358-360` missing-bootstrap throw; `GoApiSnapshot.java:115` `EMPTY`, `:122-126` base-file null path, `:159-160` fallback WARN, `:163` INFO; `GoBuildInfo.java:488-489` strip `go`; `TransientProgramProperties.java:107-110` null supplier not cached |
| Producer pinning (bracket) | `git log` for both `carrier-run.py` and `receipt-validate.py` shows only `2711674`; `git diff 2711674 da64646 -- .ufo/waves/round-17/tools/` changes only `buildinfo-probe.py` and `temporal-sweep.py`, neither used by this run ⇒ the dict-shape producer read here is the one that made the receipt |
| All pro-op artifacts tracked | `git ls-tree -r da64646 …/runs/pro-op` 14 files == 14 files on disk; `git status` clean except wave-2 scratch |

## Residual risk / verification gaps

- **Tool package bytes are not pinned.** `npx -y rea-agents@6.5.0` resolved from
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (package.json version `6.5.0`,
  observed). The receipt pins the carrier, Go data and prediction but not the resolved npm package or
  the Ghidra install; the argv is a request, not a byte commitment. (`carrier-run.py` and
  `receipt-validate.py` themselves are bracketed by `2711674`→`da64646`, so their identity is safe.)
- **`pins.py` proves same-bytes-at-two-instants, not continuity**; a 30 s mid-run sampler cannot rule
  out change-and-restore. The knowledge entry says exactly this at `:29-31`.
- **Binding is manual for now** (F6): the fact is verified for `pro-op`, but the durable check lives
  only in `carrier-run.py`'s capture-time booleans.
- **No second independent log capture of this run exists** (REA deletes its root; the retained copy is
  the only one), so log completeness is bounded by the last poll + 0.5 s, as `log_capture_limit` states.
- No tools were installed or upgraded for this review; no host state changed.
