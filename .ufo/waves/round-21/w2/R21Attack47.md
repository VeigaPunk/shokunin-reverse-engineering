# R21Attack47 — R21-C2 retrospective compatibility

- **Axis:** depth (C2).
- **Scope:** retained R20 label `t1246-pprof` only; this is a retrospective comparison against its frozen prediction, not a fresh forecast or analysis.
- **Binding:** `.ufo/waves/round-20/runs/t1246-pprof/comparison-log-binding.json` names `.ufo/waves/round-20/runs/t1246-pprof/logs/rea-ghidra-hCPl3X/ghidra.log`, declares `verified: true`, and pins SHA-256 `4b7710fe2921fb5b433af61de28595c7a9e77561853e148b25f0a94d4b8e73c3`.
- **Digest verification:** `sha256sum .ufo/waves/round-20/runs/t1246-pprof/logs/rea-ghidra-hCPl3X/ghidra.log` → `4b7710fe2921fb5b433af61de28595c7a9e77561853e148b25f0a94d4b8e73c3  .ufo/waves/round-20/runs/t1246-pprof/logs/rea-ghidra-hCPl3X/ghidra.log`; computed digest matches the binding.

## Comparison record

- **ARGV:** `python3 -I -B .ufo/waves/round-21/tools/compare-first-failure.py --prediction .ufo/waves/round-20/predictions/swiss-misread-v2/t1246-pprof.json --log .ufo/waves/round-20/runs/t1246-pprof/logs/rea-ghidra-hCPl3X/ghidra.log --extractor .ufo/waves/round-20/tools/first-failure-extract.py`
- **STDOUT:** `{"finding": "failure_match", "last_line": 529, "match": true, "observed": {"index": 27091201, "kind": "invalid_index", "phase": "markup", "va": null}, "predicted": {"index": 27091201, "kind": "invalid_index", "phase": "markup_walk", "va": 10516608}}`
- **STDERR:** empty.
- **EXIT:** `0`.

The frozen prediction and observed bounded log agree on first-failure `kind=invalid_index` and `index=27091201` through log line 529. The comparator's contract is kind/index comparison: phase (`markup_walk` vs. `markup`) and VA (`10516608` vs. null) are not matching claims. This is a first-failure match only; unrelated analyzer errors do not establish successful analysis. No REA tool or native carrier was run, and no production files were changed.

Report: `.ufo/waves/round-21/w2/R21Attack47.md`
