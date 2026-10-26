# CTL-C2-1 — catch-all table (pre-freeze shortcut control for P39-C2)

Rule set with a single `*` row. It labels every envelope `clean`, so it cannot fail
loudly and cannot separate any class. This is the do-nothing baseline the draft's kill
rule names first: if this table ever scores `matched == N`, P39-C2 is dead.

## Queue-drain craft

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| clean | * | * | * | * | * | * | anything -> nothing to triage | CTL-C2-1 catch-all |

Prediction (7-class, 2 per class, N = 14): every envelope -> `clean`; only the two
`clean` carriers are right, so 2/14. No class-specific cause is ever distinguished.
