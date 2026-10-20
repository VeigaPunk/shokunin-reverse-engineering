# RunProaether — attack on `runs/pro-aether/` (W2, falsify)

**Target.** Retained run `.ufo/waves/round-17/runs/pro-aether/` (carrier `/usr/bin/aether`, aether
4.32.0-2, sha256 `06c91f55df4117e5…`) at lane rev `da64646adcb19c1ede7537b799b8c7d283fe43da`,
predictions frozen at `271167473d87ef710f07ecdd98caf0ce12091686`. Read-only: no REA `analyze`, no
carrier execution, no Ghidra. All commands below were run exactly as shown; outputs are quoted, not
paraphrased. No tools installed or upgraded.

## Verdict

The **provenance chain itself holds** — log binding, frozen-prediction bytes, freeze time, fresh
re-extract, fresh compare, and the knowledge row all check out (bounded no-finding in §3). The
**receiving gate does not**: the round's own `receipt-validate.py` rejects all eight retained receipts,
including this one, and the knowledge entry's `recheck:` line prescribes exactly that failing command.
Calibration is harmed; depth is largely supported.

| Assigned check | Result |
|---|---|
| `receipt-validate.py runs/pro-aether/receipt.json` | **FAIL — exit 1, `unrecognized_shape`** (F1) |
| log contains `Using log file: <session>/ghidra.log` | PASS — `ghidra.log:2` |
| log contains `IMPORTING: file://<session>/target-<sha[:12]>.bin` | PASS — `ghidra.log:46`, `06c91f55df41` |
| prediction bytes == `git show 2711674:…/pro-aether.prediction.json` | PASS — both `f11749b3…` |
| freeze commit time < receipt analyze `started_at_utc` | PASS — `13:46:45Z` < `13:50:04.056Z` |
| fresh `log-extract.py` vs retained `observation.json` | PASS — identical modulo `log_path`/`log_file_line` |
| fresh `compare.py` | PASS — exit 0, 5/5 fields match |
| knowledge row `pro-aether` matches log | PASS — row 54 vs log `:92/:93/:95` |

---

## 1. Findings

### F1 — HIGH (calibration): the retained receipts fail the round's own validator, so C2's entry condition is red

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py \
    .ufo/waves/round-17/runs/pro-aether/receipt.json
… "findings": [{ "code": "unrecognized_shape",
                 "detail": "receipt matches neither retain nor carrier shape" }],
  "status": "invalid", "valid": false, "exit": 1        # counts: valid 0 / invalid 1
$ python3 -I -B …/receipt-validate.py <the 8 runs/*/receipt.json>
  {'invalid': 8, 'receipts': 8, 'unreadable': 0, 'valid': 0}   # tool "exit": 1
```

* Cause is a **cross-tool shape disagreement**, not a corrupt receipt:
  `tools/receipt-validate.py:98-101` requires `isinstance(receipt["steps"], list)`, and
  `:284` then iterates `enumerate(receipt["steps"])`. `tools/carrier-run.py:317,349` writes
  `receipt["steps"]` as a **dict keyed by step name**, and its own selftest asserts that keyed shape
  (`:555-558`: `receipt["steps"]["analyze"]["evidence_id"]`, `["search:main.main"]`). Wave-1's tool
  spec agrees with the keyed shape: `w1/CarrierRunTool.md:46` writes `steps.analyze.exit == 3`.
* **Selftest green, product red:** `receipt-validate.py --selftest` → `SELFTEST: CLEAN cases=5`, exit 0.
  Its fixture (`_carrier_receipt`, `:459-475`) builds a **list**, so the disagreement can never surface
  in selftest.
* Consequence for the claim, not just the tool: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`
  makes this exact command the entry's `recheck:`; `w1/ConnCapabilityHistory.md:70` and `:91` make
  "each `receipt-validate.py` exit 0" the capability-row gate; `w1/draft-scorecard.md:46` repeats it as
  the entry condition. `claims.json` C2 admits the row "only if the capture runs and its receipt
  validates". Today `measure.py da64646` reports `receipts 8` while
  `scorecard_capability_rows_matching 0` — and `measure.py:12-13` explicitly says a receipt is "only a
  blob … nothing about its validity is measured", so nothing else would ever catch this.
* **Smallest fix** (no re-runs, no receipt regeneration): normalize in the validator —
  `steps = receipt.get("steps"); steps = list(steps.values()) if isinstance(steps, dict) else steps`
  — in `classify` and before the `:284` loop, plus one selftest case built with the **keyed** shape so
  the two tools cannot drift again. Editing `carrier-run.py` to emit a list instead would invalidate
  all eight receipts (they were produced by the current tool) and cannot be re-derived without eight
  REA analyze runs — strictly worse.

### F2 — MEDIUM (depth): "hashed every 30 s during … no mid-run check differed" has no retained evidence

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:26-30` asserts 146 paths were hashed
"before, every 30 s during, and after each session" and that "no mid-run check differed". The receipt
retains only `pins_pre`, `pins_post`, `pins_compare` (pre/post, `taken_at_utc` 13:50:03.34Z /
13:51:12.83Z). `tools/carrier-run.py:422-433` performs the throttled mid-run snapshot
(`PIN_CHECK_S = 30.0`, `:35`) but records it **only on inequality**
(`rec["pins_changed_during_run"]`). For pro-aether the analyze step has no `pin_checks`/timestamps, so
a reader cannot distinguish "checks ran and agreed" from "no check ever fired" without reading tool
source. That is the R16-PROVENANCE failure mode (temporal stability asserted without evidence) inside
the entry written to close it; `:29-30` hedges *continuity*, not *occurrence*.

**Smallest fix:** always persist `pin_checks: {count, first_utc, last_utc}` in each step record (the
code already has the loop and `monotonic()`); or, without re-running, amend `:27-29` to "checked at
30 s intervals; a mismatch is recorded as `pins_changed_during_run` (`carrier-run.py:422-433`), absent
here".

### F3 — MEDIUM-LOW (calibration): the freeze commit is cited by an unresolvable hash `2716747`

```
$ git rev-parse --verify 2716747^{commit}
fatal: Needed a single revision                                   # exit 128
$ git rev-parse --verify 2711674^{commit}
271167473d87ef710f07ecdd98caf0ce12091686                          # exit 0
```

Sites: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37` and
`.ufo/waves/round-17/run-carriers.sh:2`. The entry's own head (`:1`) carries the full correct hash, so
body and head disagree, and the run script's provenance comment cannot be resolved. This is precisely
the citation-drift class C1(b)/R16-INVOCATION claims to discharge, reproduced in the round's headline
artifacts (two independent files, so not a one-off typo).

**Smallest fix:** replace `2716747` with `2711674` (or the full 40-hex hash) in both files.

### F4 — LOW (calibration): the recheck's second command destroys the evidence it is meant to recheck

`knowledge:3` says: `bash .ufo/waves/round-17/run-carriers.sh <label>` and compare `observation.json`.
That script does `out="${RUNS_DIR:-runs}/$label"` (`run-carriers.sh:14`) then `rm -rf "$out"`
(`:15`) — so following the recheck as written deletes and replaces the retained run (and repeats a
full REA analyze) before any comparison. A recheck that is not read-only cannot validate custody.

**Smallest fix:** keep the read-only chain first (`receipt-validate.py` → `log-extract.py` →
`compare.py` over the retained files), and for the re-run use the supported override:
`RUNS_DIR=/tmp/r17-recheck bash .ufo/waves/round-17/run-carriers.sh <label>`.

---

## 2. Axis effects

- **calibration — harmed** by F1 (the shipped gate is red on 100% of retained receipts and green only
  on its own fixture), F3 (two unresolvable hash citations), F4 (destructive recheck).
- **depth — supported, with one gap**: the prediction-vs-observation chain is source-grounded and
  reproducible (§3); F2 is the only place where a stability claim outruns its retained evidence.

## 3. Bounded no-finding — what was checked and passed

All items below are [OBSERVATION] from the quoted bytes; nothing is repeated from the entry on trust.

1. **Log binding is real and self-identifying.** `ghidra.log:2`
   `Using log file: /tmp/kr17-rea-0o3ukbw2/rea-ghidra-JpGezV/ghidra.log`; `:46`
   `IMPORTING: file:///tmp/kr17-rea-0o3ukbw2/rea-ghidra-JpGezV/target-06c91f55df41.bin`. The target
   suffix equals `carrier.sha256_pre[:12]` = `06c91f55df41` (`receipt.carrier.sha256_*` =
   `06c91f55df4117e5…`), the same session dir appears in `bound_sessions`, and `/usr/bin/aether`
   still has that sha today. `receipt.retained_logs[0].binding = {logfile_ok: true, target_ok: true}`
   is produced by `carrier-run.py:128-137`, which recomputes both substrings from the copied bytes.
2. **Prediction is genuinely pre-registered.**
   `git show 271167473d87ef…:.ufo/waves/round-17/predictions/pro-aether.prediction.json | sha256sum`
   and `sha256sum predictions/pro-aether.prediction.json` both → `f11749b30fe5cf08…`; commit time
   `2026-10-20T10:46:45-03:00` = `13:46:45Z` precedes analyze start `13:50:04.056Z`. The frozen
   `pro-aether.inspect-go.json` in the same commit equals the run's (`go1.25.14`,
   `header_offset 20068336`, evidence `ev_01b04ce9…`). `predictions/SHA256SUMS` verifies: 17× OK,
   exit 0 (checked from the round root, where its `predictions/…` paths resolve).
3. **Prediction is reproducible from source, not fitted.** Re-running
   `predict.py --go-version go1.25.14 --golang-root …/typeinfo/golang` reproduces the frozen
   prediction exactly (`diff` empty). Its cited anchors are line-exact in `Base-src.zip`:
   `GoRttiMapper.java:79` (`GoVerRange.parse("1.15-1.25")`), `:170-181` (range log at 170-172,
   `Using Go API snapshot for version %s` at 179-180); `GoApiSnapshot.java:111`, `:122-126`
   (`withPatch(0)`, null base → `EMPTY`), `:148-166` (WARN `:158-161`, INFO `:162-164`);
   `GoVer.java:62-81` (`[^.0-9].*$` truncation), `:105-107`, `:143-159`;
   `GoVerRange.java:42-57`, `:83-87`; `GoBuildInfo.java:237-238`, `:488-489`. The installed data dir
   contains `go1.25.0.json` only for the 1.25 line (sha256 `54d10162…`, matching the prediction's
   `selection.base.sha256`), so `fallback → 1.25.0` is structurally forced, not post-hoc.
4. **Fresh extraction and compare agree with the retained ones.**
   `log-extract.py --log …/ghidra.log` → exit 0; its output is byte-identical to
   `runs/pro-aether/observation.json` after dropping the two path fields. `compare.py` → exit 0,
   `all_match: true` on all five fields, including the discriminating
   `snapshot_route=fallback` and `fallback_to=1.25.0`; `snapshot_label` is correctly self-labelled
   "non-discriminating: request echo", matching `GoRttiMapper.java:179-180`.
5. **Knowledge row 54 matches the log.** `loaded; 6115 types` = `ghidra.log:95`
   (`Found 6115 Go types`); `Falling back from 1.25.14 to 1.25.0… (WARN)` = `:92`; `…for version
   1.25.14` = `:93`; package identity `aether 4.32.0-2` confirmed by `pacman -Q aether` /
   `pacman -Qo /usr/bin/aether`.
6. **The EOF cause citation is faithful, including "interface-type markup".**
   `ghidra.log:177` `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854`
   — the exact numbers at `knowledge:88`; `:124` and `:138` show
   `GoInterfaceType.additionalMarkup(GoInterfaceType.java:77)` in the same chain, and the cited
   range `:97-177` spans ERROR line to cause.
7. **Run-level claims hold.** Analyze windows across all eight runs are strictly sequential
   (`13:47:06→13:47:37`, `13:47:43→13:49:24`, … `13:55:56→14:00:05Z`), matching `knowledge:2`.
   All eight receipts: `pins_compare.equal true`, exactly 1 bound / 0 unbound sessions,
   `carrier-run.exit 0`, `compare.exit 0`. `146` pinned paths decompose exactly as 143 Go-data files +
  `selection.py` + prediction + carrier.
8. **Custody is in Git and the producing tools are fixed.** 113 blobs under
   `.ufo/waves/round-17/runs/` exist at `da64646`, worktree clean; `carrier-run.py`, `log-extract.py`,
   `compare.py`, `predict.py` are byte-identical between `2711674` and `da64646` (only
   `buildinfo-probe.py` and `temporal-sweep.py` changed), so tool identity is recoverable from the rev.
9. **Completeness claim is bounded correctly.** Last Go line is `ghidra.log:207`
   (`Go strings found: 7200`, 13:50:39Z); `:238` `REPORT: Analysis succeeded` and the bridge-script
   `REPORT/SCRIPT` pairs at `:239-240` and `:242-243` follow it, so "every Go line precedes the bridge
   script" holds, and
   `log_capture_limit` is recorded verbatim.

## 4. Residual risk / verification gaps

- **Not re-derived:** I did not run REA `analyze` or the carrier, so I cannot prove the receipt's
  hashed outputs were produced by that REA session rather than substituted. Every recorded sha256 was
  independently recomputed and matched (`BAD 0` across step stdout/stderr and both logs), and the
  in-log session/target binding plus the unchanged tool bytes make substitution unlikely — but the log
  is outside REA Evidence (already flagged at `w1/CriticCapabilityPreclaim.md:97`, item iii), so this
  is integrity-plus-consistency, not cryptographic custody.
- **Not exercised:** `carrier-run.py --selftest` (shape read from code and its assertions rather than
  run); `predict.py` for the other carriers; only pro-aether was re-extracted/re-compared end to end.
- **Consequence if unfixed:** entering the capability row before F1 is resolved would make C2's
  "only if … its receipt validates" clause false at the moment of entry, and would leave
  `knowledge:3`'s recheck failing for every future reader.
