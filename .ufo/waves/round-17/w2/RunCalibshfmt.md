# RunCalibshfmt — attack on `runs/calib-shfmt/` (wave 2, falsify)

Seat: `KaidokuR17.RunCalibshfmt` (leaf; no subagents). Target:
`.ufo/waves/round-17/runs/calib-shfmt/` at lane revision
`da64646adcb19c1ede7537b799b8c7d283fe43da` (baseline `b563c79`).
Read-only: no REA `analyze`/`search`/`decompile`, no Ghidra, no carrier
execution, no edits outside this report. Tool installs: none.

## Verdict

One blocking defect, and it is cross-cutting: `receipt-validate.py` rejects
this receipt — and all eight retained carrier receipts — on **shape**
(`unrecognized_shape`), not on bytes. The calib-shfmt evidence chain otherwise
passes every assigned check: the log binds to the session and carrier, the
prediction bytes are exactly the frozen commit, the prediction is
byte-reproducible from `predict.py`, the freeze precedes the run, and the
knowledge row matches the log. The row is a **post-pilot replication**, not a
blind prediction; the entry discloses that in prose but not in the table.

## F1 — HIGH (calibration, blocks the round's own gate): the validator rejects every real carrier receipt

Exact command and output:

```
$ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py \
    /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/calib-shfmt/receipt.json
{
  "counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0},
  "exit": 1,
  "receipts": [{
    "checks_performed": 306,
    "findings": [{"code": "unrecognized_shape",
                  "detail": "receipt matches neither retain nor carrier shape",
                  "where": "$"}],
    "kind": "unknown", "status": "invalid", "valid": false
  }],
  "tool": "receipt-validate.py"
}
# process exit 1
```

All eight:

```
$ cd .../.ufo/waves/round-17 && bash -c 'python3 -I -B tools/receipt-validate.py runs/*/receipt.json'
{"invalid": 8, "receipts": 8, "unreadable": 0, "valid": 0, "exit": 1}   # process exit 1
```

Cause (observation):

- `tools/receipt-validate.py:98` classifies a carrier receipt only when
  `isinstance(receipt.get("steps"), list)`; `:284` then iterates
  `enumerate(receipt.get("steps") or [])`.
- `tools/carrier-run.py:275,309,317,349` writes `receipt["steps"]` as a **dict
  keyed by step name** (`analyze`, `inspect-go-binary`, `search:NAME`), and its
  own selftest asserts that keyed shape (`:555-558`).
- `tools/receipt-validate.py:470` builds its "carrier" selftest fixture with a
  **list**, so `--selftest` is green (`SELFTEST: CLEAN cases=5`) and cannot see
  the disagreement. `w1/ReceiptValidateTool.md` predicted that a producer
  divergence would surface as `missing_field`; the observed outcome is
  `unrecognized_shape`.

This is a shape defect, not tampering — controlled experiment (only the `steps`
container was changed, in `/tmp`, adding `name` to each step object):

```
$ python3 -I -B -c '... r["steps"] = [dict(v, name=k) for k,v in r["steps"].items()] ...'  # /tmp/rc-list-*.json
$ bash -c 'python3 -I -B tools/receipt-validate.py /tmp/rc-list-calib-esbuild-0.25.12.json /tmp/rc-list-calib-shfmt.json /tmp/rc-list-pro-aether.json /tmp/rc-list-pro-containerd-shim.json /tmp/rc-list-pro-esbuild-0.21.5.json /tmp/rc-list-pro-esbuild-0.27.7.json /tmp/rc-list-pro-notesmd-cli.json /tmp/rc-list-pro-op.json'
{"invalid": 0, "receipts": 8, "unreadable": 0, "valid": 8, "exit": 0}   # process exit 0
# every receipt: checks_performed 336, findings []
```

The real receipt's 306 checks already re-hashed every recorded path and
re-ran `pins.compare` with **zero** digest/pin findings; the 30-check delta is
the carrier required-field set, the only checks the shape change adds. So the
receipt's content is valid; only the classifier is wrong.

Impact (observation):

- The knowledge entry makes this exact command its `recheck:` at
  `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`; it exits 1.
- `claims.json` C2 admits the capability row "only if the capture runs and its
  receipt validates"; `w1/ConnCapabilityHistory.md:70` and
  `w1/draft-scorecard.md:46` make "`receipt-validate.py` exit 0" the entry
  condition. The SCORECARD capability row is absent at `da64646` (observation:
  `SCORECARD.md` has no "retained REA Ghidra-session log" row); under the
  stated gate the exit 1 is sufficient to keep it absent (inference).
- The SKILL.md round-17 `receipt-validate` row (`SKILL.md:536`) says
  `0 valid, 1 digest/pin/field finding, 2 unreadable`; on this round's own
  receipts it is red.

**Smallest fix (do not rewrite the receipts).** In `tools/receipt-validate.py`
normalize the container once, in `classify` and before the `:284` loop:

```python
steps = receipt.get("steps")
steps = list(steps.values()) if isinstance(steps, dict) else steps
```

and add one selftest fixture built from a real keyed `carrier-run.py` receipt.
Changing `carrier-run.py` to emit a list instead would invalidate all eight
retained receipts, which cannot be re-derived without eight REA analyze runs.

## F2 — LOW (calibration): the calib-shfmt table row is a post-pilot replication, unmarked

Exact commands and outputs:

```
$ cmp pilot/shfmt.json runs/calib-shfmt/analyze.json; echo $?
0
$ diff <(grep -E '\((Go|Golang)' pilot/shfmt-log/ghidra.log | sed -E 's/^[0-9-]+ [0-9:]+ //') \
       <(grep -E '\((Go|Golang)' runs/calib-shfmt/logs/rea-ghidra-j5AXOZ/ghidra.log | sed -E 's/^[0-9-]+ [0-9:]+ //')
# empty
```

- `predictions/carriers.tsv:1` labels the carrier
  `calibration (pilot-seen)`; `pilot/README.txt:1` dates the pilot
  10:17–10:19 -03; the freeze is 10:46:45 -03
  (`271167473d87ef710f07ecdd98caf0ce12091686`, author = committer).
- The retained `analyze.json` is byte-identical to `pilot/shfmt.json` (same
  evidence ID `ev_2b29a1dd…`), and the Go lines are identical after stripping
  timestamps. The prediction file's mtime is 13:46:25Z — after the pilot,
  before the 13:47:06.688621Z run.
- The entry discloses this at
  `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37-38`
  ("The two `calib-*` carriers had been seen in the pilot"), and both
  `predictions/carriers.tsv:1` ("calibration (pilot-seen)") and `LOG.md:2047`
  ("two calibration, six prospective") already carry the distinction. F2 is
  therefore a labeling gap, not a concealment; the separate false "before any
  run" phrase at `:1` is covered by peers. But the eight-row table (`:49-58`,
  calib-shfmt at `:51`) is the one artifact that presents the row without the
  marker; a reader of the table alone sees eight uniform predictions.

**Smallest fix:** add a `blind?` column (or `(pilot-seen)` after `calib-shfmt`
at `:51`). The 8/8 count already distinguishes "two calibration, six
prospective" at `LOG.md:2047`, so no count change is needed. The separate
"before any run" wording at `:1` and `run-carriers.sh:2` is already covered by
`w2/CriticPreregistration.md:79-84`; not repeated here.

## Assigned checks — bounded no-findings

1. **Fresh extract equals the stored observation.**
   `python3 -I -B tools/log-extract.py --log runs/calib-shfmt/logs/rea-ghidra-j5AXOZ/ghidra.log > /tmp/rc-shfmt-extract.json`
   → exit 0; `cmp /tmp/rc-shfmt-extract.json runs/calib-shfmt/observation.json`
   → exit 0 (byte-identical). Values: `log_sha256`
   `13b8fbbe…` (`ghidra.log` sha256 confirmed by `sha256sum`), `log_bytes`
   11440, `classification: bootstrap_missing`, `missing_bootstrap: true`,
   `untested_versions: ["1.27.0"]`, `snapshot_route: "none"`,
   `snapshot_labels: []` (`observation.json:76-81`).
2. **Fresh compare passes.**
   `python3 -I -B tools/compare.py --prediction predictions/calib-shfmt.prediction.json --observation /tmp/rc-shfmt-extract.json`
   → exit 0, `all_match: true`; all five fields match
   (`untested_version` 1.27.0, `snapshot_label` []/null, `missing_bootstrap`
   true/true, `snapshot_route` none/none, `fallback_to` []/null). Stored
   `compare.json:2` is the same except the `observation` path.
3. **The bound log is genuinely this session and this carrier.**
   `ghidra.log:2` contains exactly
   `Using log file: /tmp/kr17-rea-y138m4zi/rea-ghidra-j5AXOZ/ghidra.log`;
   `ghidra.log:46` contains exactly
   `IMPORTING: file:///tmp/kr17-rea-y138m4zi/rea-ghidra-j5AXOZ/target-58f765638eed.bin`.
   The carrier pre-sha is `58f765638eed5309…` (`receipt.json:8`), so
   `sha256[:12] = 58f765638eed`; the receipt's `session_dir` is the same
   directory and `binding` is `{logfile_ok: true, target_ok: true}`
   (`receipt.json:1800-1803`).
4. **Prediction bytes equal the frozen commit.**
   `git show 2711674…:.ufo/waves/round-17/predictions/calib-shfmt.prediction.json > /tmp/rc-shfmt-frozen.json && cmp /tmp/rc-shfmt-frozen.json predictions/calib-shfmt.prediction.json`
   → exit 0; both sha256 `c4c534cf87127e8959418ec292acd41ca4df313e95ea28a2fc5b31f97fffa220`
   (also `predictions/SHA256SUMS:4` OK). No post-freeze commit touches
   `predictions/` (`git log 2711674..HEAD -- predictions/` empty; diff empty).
   `predict.py --go-version go1.27.0-X:nodwarf5 --golang-root …/typeinfo/golang`
   output is byte-identical to the file (`cmp` exit 0), with `predict.py` and
   `round-16/selection.py` unchanged between freeze and HEAD.
5. **Freeze precedes the analyze step.**
   `git show -s --format='%aI %cI' 2711674` →
   `2026-10-20T10:46:45-03:00` both = `13:46:45Z`;
   `receipt.json:1861` analyze `started_at_utc`
   `2026-10-20T13:47:06.688621+00:00`. Prediction mtime 13:46:25.32Z;
   `pins_pre` 13:47:05.97Z. Gap to analyze start: 21.7 s.
6. **The calib-shfmt knowledge row matches the log.** Row
   `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:51`: sha[:16]
   `58f765638eed5309` = `carrier.sha256_pre`; package `shfmt 3.14.1-1`
   (`pacman -Q shfmt`); build Go `go1.27.0-X:nodwarf5` from `inspect-go.json`,
   independently confirmed by `go version -m /usr/bin/shfmt` and
   `buildinfo-probe.py` (header_offset 3515584, sha `58f76563…`);
   `Untested Go version [1.27.0]` ×2 (`ghidra.log:83,87`),
   `Missing Go bootstrap type info` ×2 (`:84,88`), zero
   `Using Go API snapshot` lines; evidence ID `ev_2b29a1dd…` matches
   `analyze.json` and `receipt.json:1839`.
7. **Pins.** 146 entries = 143 files in the installed Go data dir
   (`find …/typeinfo/golang -type f | wc -l` = 143) + `/usr/bin/shfmt` +
   `round-16/selection.py` + the frozen prediction; `pins_pre` and `pins_post`
   carry the same 146; `pins_compare` `{equal: true, changed: [], errors: []}`;
   `bound_sessions` 1, `unbound_sessions` 0.
8. **Receipt digests.** `sha256sum` of the retained `ghidra.log` and
   `script.log` equal `retained_logs[0].files.*.sha256`
   (`13b8fbbe…`, `15b696af…`); the validator's 306 checks found no digest
   mismatch even before the shape fix.

## Residual risk / overlaps

- F1 is already visible to peers (`w2/RunProaether.md` F1,
  `w2/DraftLessonEvidence.md` F1, `w2/ReviewInPlaceEdits.md` F1,
  `w2/ConnScorecardCapability.md`). This report's addition is the controlled
  eight-receipt list-shaped run: 336 checks each, zero findings — the receipts
  are content-valid, and shape is the sole blocker.
- Mid-run pins: `carrier-run.py:422-433` records `pins_changed_during_run` only
  on mismatch; `steps.analyze` retains neither a count nor a timestamp, so
  "no mid-run check differed" (`knowledge:29`) is a code inference, not a
  retained observation (peers `RunProaether.md` F2, `RunProesbuild0215.md` F7,
  `ConnScorecardCapability.md` F5).
- Recheck destroys evidence: at HEAD, `run-carriers.sh:14-15` is
  `out="runs/$label"` then `rm -rf "$out"; mkdir -p "$out"`, and the knowledge
  `recheck:` at `:3` runs exactly that for `<label>`. The worktree has an
  uncommitted `RUNS_DIR` mitigation; HEAD does not.
- `runs/run-log.txt:1` starts with `calib-esbuild-0.25.12`; there are no
  calib-shfmt lines (peers `CriticPreregistration.md:73`,
  `SentinelSessionResidue.md:56`). Receipt timestamps still place calib-shfmt
  first (13:47:06–13:47:37Z).
- Eight `/tmp/kr17-rea-*` parents remain (2.6 MB each, `node-compile-cache`
  only); each receipt records this in `session_parent_leftovers`. Benign.

## Not run

No REA `analyze`/`search`/`decompile`, no Ghidra/`analyzeHeadless`, no carrier
execution. Commands used: the three round-17 tools on retained files,
`predict.py`, `buildinfo-probe.py`, `go version -m` (file read only), `git`
object reads, `sha256sum`, `cmp`, `diff`, `pacman -Q`, `find`.
