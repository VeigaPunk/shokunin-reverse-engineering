# R21Attack35 — R21-C2 retrospective compatibility, retained label t1246-buildid

Axes: **calibration** (exact retained digests/argv/stdout/stderr/exit, zero invented results) and **depth** (actual tool execution on the bound log+prediction, saturation and corroboration checks).

Scope: retrospective compatibility only — R21 `compare-first-failure.py` driving the ORIGINAL R20 `first-failure-extract.py` against the bound R20 log and frozen R20 prediction. Not a fresh forecast. No REA producers, no native-carrier execution (the carrier is quoted statically from the prediction only), no production edits, no lane git/index mutation. No installs attempted (all pacman transactions paused; none needed). Only writes: this report.

## 1. Input integrity (digest match: YES)

Binding `.ufo/waves/round-20/runs/t1246-buildid/comparison-log-binding.json`:

- `log_path`: `.ufo/waves/round-20/runs/t1246-buildid/logs/rea-ghidra-qGQ7Im/ghidra.log`
- `log_sha256`: `c3c0af191d694f48e3d039d0d7d254733493ef602f79f6dbc60d60719df4d864`, `verified: true`

Recomputed:

```
$ sha256sum .ufo/waves/round-20/runs/t1246-buildid/logs/rea-ghidra-qGQ7Im/ghidra.log
c3c0af191d694f48e3d039d0d7d254733493ef602f79f6dbc60d60719df4d864  .ufo/waves/round-20/runs/t1246-buildid/logs/rea-ghidra-qGQ7Im/ghidra.log
```

Exact match. The log evaluated is byte-identical to the bound retained log. Size 16446 bytes, 167 newlines (`wc -l -c`).

## 2. Frozen prediction

`.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-buildid.json` (label `t1246-buildid`, go1.24.6 linux/amd64, snapshot_status `exact_diff`):

- `first_failure`: `{"h0": null, "h1": null}`
- `predicted_failure_h1`: false, `predicted_failure_kind_h1`: "none"
- `predicted_eof_reads_h1`: [], `predicted_invalid_index_reads_h1`: []

So the frozen R20 forecast for this label is: no qualifying Go-analysis I/O failure at h1, i.e. predicted `null`.

## 3. Assigned verification run (retained argv/stdout/stderr/exit)

cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`:

```
$ python3 .ufo/waves/round-21/tools/compare-first-failure.py \
    --prediction .ufo/waves/round-20/predictions/swiss-misread-v2/t1246-buildid.json \
    --log .ufo/waves/round-20/runs/t1246-buildid/logs/rea-ghidra-qGQ7Im/ghidra.log \
    --extractor .ufo/waves/round-20/tools/first-failure-extract.py
{"finding": "failure_match", "last_line": 167, "match": true, "observed": null, "predicted": null}
EXIT=0
```

stdout verbatim as above; stderr: empty; exit: 0.

Tool mechanics (read from source before running, inert): it validates the prediction requires a present `first_failure.h1`, then runs the extractor as `subprocess.run([sys.executable, '-I', '-B', extractor, log], timeout=120)`, requires extractor exit 0, requires an envelope JSON with `first_failure` and integer `last_line`, and compares `(kind, index)` pairs only. Exit codes: 0 match, 1 mismatch, 2 comparison_unevaluable. It never executes the analyzed carrier.

## 4. Independent direct extractor run (depth cross-check)

Same envelope path the comparator uses, run directly (temporary subshell; nothing persisted):

```
$ python3 -I -B .ufo/waves/round-20/tools/first-failure-extract.py \
    .ufo/waves/round-20/runs/t1246-buildid/logs/rea-ghidra-qGQ7Im/ghidra.log
{
  "cause_line": null,
  "first_failure": null,
  "first_failure_line": null,
  "last_line": 167,
  "log_path": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-buildid/logs/rea-ghidra-qGQ7Im/ghidra.log",
  "other_errors": []
}
EXIT=0
```

stderr: empty; exit: 0. Matches the comparator's internal observation exactly.

## 5. Result

- **`failure_match`, `match: true`, exit 0** — predicted `null` (h1) equals observed `null` through `last_line` 167.
- Digest match: **yes** (Section 1).
- R20 original extractor is compatible with the R21 comparator for this retained label, and the frozen R20 prediction is reproduced against the byte-identical bound log.

Saturation: the extractor's `last_line` 167 equals the log's full line count (167 newlines), so the null observation is bounded by EOF, not by a truncated window — absence covers the whole log.

Acceptance caveat addressed: unrelated analyzer errors would surface in `other_errors`; it is empty here, and a literal fallback cross-check (no LSP server for these standalone Python scripts; plain text grep per fallback policy) for `ERROR|Invalid index|past EOF|EOFException|IOException|Go analysis failure` found zero matches in the log. Success therefore rests on the exact match plus digest identity, not on absence being masked by other errors — indeed none exist even in the non-qualifying bucket.

## 6. Residual risk / gaps

- Comparison semantics are kind/index only; `phase`/`va`/`line` are validated but not compared (tool docstring states this by design). Adequate for the assigned envelope; a phase-varying mismatch between h1 forecast and observation would not be caught by this tool.
- The extractor is caller-owned code executed as a subprocess by design (documented in the comparator docstring, not a sandbox); I read both sources before running: log regex-parse to JSON stdout only, no network, no filesystem writes outside selftest tempdirs.
- Retrospective only; no fresh R21 forecast is claimed, and no live Ghidra/REA session was involved.
