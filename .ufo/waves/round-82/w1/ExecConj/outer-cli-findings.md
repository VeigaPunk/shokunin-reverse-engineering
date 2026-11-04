# R82-C1-SUMMARY-DOMAIN-001 — outer CLI reproduction

Follow-up requested by KaidokuR82; source revision `eb227c4694e16cb8fae74df0eea2f07643b46124`.

Correction to the initial coordination reply: the follow-up was reachable and has now been executed. This supplement supplies actual outer `--battery` evidence, superseding the helper-only limitation for the summary-domain finding.

The gate remains SHA-256 `6155a1ffa7564acffc755caeafbe450f5b080d00526edf4bef247444ad04e1af`, identical to the original freeze.

## Observed exit assertions

| Isolated fixture | Required exit | Actual exit | Result |
|---|---:|---:|---|
| Genuine baseline | 0 | 0 | green control satisfied |
| Landing binder replaced with 64 zeroes | 1 | 1 | red control satisfied |
| Landing pristine.summary=[1,0], 11 original case rows retained | 1 | 0 | false green |
| Landing pristine.summary=[true,0] | 1 | 0 | false green |
| Landing pristine.summary=[11,false] | 1 | 0 | false green |

Stable finding-id: **R82-C1-SUMMARY-DOMAIN-001**. Population is derived only from case-list length; summary[0] is not bounded or reconciled. Python isinstance(value,int) also accepts bool, while false compares equal to zero. Therefore malformed boolean summaries and below-floor emitted summary population pass the complete outer battery, not merely a helper call. These demonstrations mutate the stored parsed summary; they do not replace the recorded stdout string, so they also expose the absence of reconciliation with that string. No claim is made that a live producer emitted these malformed values.

## Evidence and containment

`outer-cli-fixtures.py` is the isolated candidate driver. It extracts only six relevant files at the source revision into a private git fixture, verifies the absolute toplevel before every commit, and invokes the real script with `--battery --root <fixture> --rev <fixture commit> --json-out <own evidence>`. Fixture commit hashes, exact argv, expected/actual exits and gate digests are retained in `outer-cli-evidence.json`. Each fixture additionally retains `outer-<case>.json`, `.stdout.txt`, and `.stderr.txt`.

Only private scratch git state was changed. The sole scratch path was `/fast/scratch/hyaku/kaidoku-r82/ExecConj/`; TMPDIR was explicitly set beneath it for all fixture operations and child executions. Scratch was removed in finally after retaining evidence, confirmed by `scratch_removed=true`. No production edits, repository sweeps, tool installs, or promotion decisions. This is candidate evidence for L1 integration.
