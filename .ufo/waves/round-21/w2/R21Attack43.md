# R21Attack43 — t1246-gofmt retrospective C2 compatibility

**Axes:** C1 / calibration; C2 / depth. **Scope:** only retained R20 label `t1246-gofmt`; retrospective compatibility, not a fresh forecast.

## Artifact identity

The binding `.ufo/waves/round-20/runs/t1246-gofmt/comparison-log-binding.json` names `.ufo/waves/round-20/runs/t1246-gofmt/logs/rea-ghidra-jjj6WB/ghidra.log`, records SHA-256 `019e11e750a1764dc1ba4b4c2adfe1e588b7f224a34c162f04aa6622f16d3462`, and has `verified: true`. The independently computed digest matches exactly (182 lines; 19,101 bytes).

Frozen prediction: `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-gofmt.json`, label `t1246-gofmt`; `first_failure.h1` and `first_failure.h0` are both null.

## Verification record

Hash invocation:

```text
argv: sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-gofmt/logs/rea-ghidra-jjj6WB/ghidra.log
stdout: 019e11e750a1764dc1ba4b4c2adfe1e588b7f224a34c162f04aa6622f16d3462  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-gofmt/logs/rea-ghidra-jjj6WB/ghidra.log
stderr: (empty)
exit: 0
```

Assigned comparator invocation, using the original R20 extractor:

```text
argv: python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-gofmt.json --log /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-gofmt/logs/rea-ghidra-jjj6WB/ghidra.log --extractor /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py
stdout: {"finding": "failure_match", "last_line": 182, "match": true, "observed": null, "predicted": null}
stderr: (empty)
exit: 0
```

## Result and limits

For this exact retained artifact, the comparator returns `failure_match`: predicted and observed first failures are both null. The negative observation is bounded through log line 182. This is a match under the comparator's contract, not proof of analysis success or a fresh forecast. Unrelated analyzer errors do not establish success; the comparator output does not include the extractor's separate `other_errors` inventory, so this review makes no claim about that inventory or use it as a success signal.

No production files were edited. No REA tool or native carrier was run; no installs, builds, formatters, broad test suites, or outside verifier were run. Verification is limited to this single bound log/prediction pair and the assigned comparator invocation; it makes no claim about other labels or general forecast calibration.