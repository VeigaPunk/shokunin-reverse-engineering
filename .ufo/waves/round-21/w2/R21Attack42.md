# R21Attack42 — t1246-go retrospective C2 compatibility

**Axis:** C2 / depth. **Scope:** only the retained R20 `t1246-go` artifact; retrospective compatibility, not a fresh forecast.

## Artifact identity

The binding `.ufo/waves/round-20/runs/t1246-go/comparison-log-binding.json` names `.ufo/waves/round-20/runs/t1246-go/logs/rea-ghidra-2PFXTv/ghidra.log` and records SHA-256 `5eeac729f78f5bcc774172e10b9ce26045ef2d96707f759a3cbf6ea9c0a3df2a` (`verified: true`). The independently computed digest matched that bound digest exactly.

Frozen prediction: `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-go.json`, label `t1246-go`; `first_failure.h1` predicts `invalid_index`, index `35082496`, phase `markup_walk`, VA `10925280`; `h0` is null.

## Verification record

Hash command:

```text
argv: sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-go/logs/rea-ghidra-2PFXTv/ghidra.log
stdout: 5eeac729f78f5bcc774172e10b9ce26045ef2d96707f759a3cbf6ea9c0a3df2a  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-go/logs/rea-ghidra-2PFXTv/ghidra.log
stderr: (empty)
exit: 0
```

Assigned comparator invocation (using the original R20 extractor):

```text
argv: python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-go.json --log /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-go/logs/rea-ghidra-2PFXTv/ghidra.log --extractor /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py
stdout: {"finding": "failure_match", "last_line": 646, "match": true, "observed": {"index": 35082496, "kind": "invalid_index", "phase": "markup", "va": null}, "predicted": {"index": 35082496, "kind": "invalid_index", "phase": "markup_walk", "va": 10925280}}
stderr: (empty)
exit: 0
```

## Result and limits

This retained artifact is a match under the comparator's declared kind/index comparison: observed and predicted `kind` are `invalid_index`, and indices are both `35082496`. The observation is bounded through log line 646. It is **not** a full failure-record equality: observed phase is `markup` rather than predicted `markup_walk`, and observed VA is null rather than `10925280`; the comparator's match predicate intentionally does not compare those fields. This is one exact-artifact retrospective match, not evidence that analysis completed successfully or that unrelated analyzer errors are success. The original extractor documents those other-analyzer errors as separate from the Go first failure; they cannot establish success.

No production files were edited. No REA tool or native carrier was run. No build, test suite, formatter, or outside verifier was run. The comparator result does not separately report the extractor's unrelated-error inventory, so this review makes no claim about its contents.