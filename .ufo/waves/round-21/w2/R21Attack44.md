# R21Attack44 — C2 retrospective compatibility for t1246-nm

## Scope and axes

- **Calibration:** one retained R20 exact-artifact case only; this is not a fresh forecast or evidence that all nineteen retained cases match.
- **Depth:** compare the frozen h1 first-failure prediction against the bound retained Ghidra log through the original R20 extractor, using the R21 comparator.

Frozen claim: `.ufo/waves/round-21/claims.json:9` (C2). This assignment covers only label `t1246-nm`; no production files were edited, no REA/native carrier was run, and no other label was inspected or counted.

## Bound artifact and digest

The R20 binding at `.ufo/waves/round-20/runs/t1246-nm/comparison-log-binding.json` names:

- Log: `.ufo/waves/round-20/runs/t1246-nm/logs/rea-ghidra-xpz849/ghidra.log`
- Bound SHA-256: `b0752b438f053e445a95a320f58da493143f079f2a12e3c7f895481373388d53`
- Binding `verified`: `true`

Observed local `sha256sum` output:

```text
b0752b438f053e445a95a320f58da493143f079f2a12e3c7f895481373388d53  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-nm/logs/rea-ghidra-xpz849/ghidra.log
```

**Digest match: yes** — the observed digest exactly matches the digest recorded in the R20 binding.

## Exact comparison run

Working directory: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`

Actual argv:

```json
["python3", "-I", "-B", ".ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", ".ufo/waves/round-20/predictions/swiss-misread-v2/t1246-nm.json", "--log", ".ufo/waves/round-20/runs/t1246-nm/logs/rea-ghidra-xpz849/ghidra.log", "--extractor", ".ufo/waves/round-20/tools/first-failure-extract.py"]
```

Captured stdout:

```json
{"finding": "failure_match", "last_line": 248, "match": true, "observed": {"index": 22070273, "kind": "invalid_index", "phase": "markup", "va": null}, "predicted": {"index": 22070273, "kind": "invalid_index", "phase": "markup_walk", "va": 5308992}}
```

Captured stderr: `""` (empty)

Exit: `0`

## Finding and limits

**R21Attack44-F1 — exact retained case matches.** The frozen prediction's h1 failure and the observation extracted from the digest-matched bound log both have `kind: invalid_index` and `index: 22070273`. The comparator returns `failure_match`, bounded through `last_line: 248`, with exit 0. R21's comparator explicitly compares `(kind, index)`; `phase` (`markup_walk` vs `markup`) and `va` (`5308992` vs `null`) differ but are not part of this comparator's equality predicate. This is the requested single-artifact compatibility result, not a broader structural equivalence claim.

This outcome is a matched observed Go-analysis failure, not successful analysis. The original extractor documents unrelated analyzer errors separately in `other_errors`; those errors do not establish success, and the bounded first-failure match does not assert success beyond line 248. No evidence here establishes the other eighteen retained matches or the full C2 claim.

## Verification gaps and disposition

- Scope was limited to the assigned retained label and requested hash/comparison. No build, formatter, broad test suite, or unrelated verifier was run.
- The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”), so LSP references/definition/diagnostics were unavailable; no grep result is offered as semantic proof. No source callers were changed in this assignment.
- No tools were installed or updated; no package/service/boot mutation occurred.

No actionable defect was demonstrated for this one assigned retained case. No production patch is proposed.

Report: .ufo/waves/round-21/w2/R21Attack44.md
