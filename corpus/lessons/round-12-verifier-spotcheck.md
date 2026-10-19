# round-12 — non-author verification and spot-check (orchestrator, kaika)

Written by the integrator, not the lane (CORPUS.md: corrections and outside reviews are new
files; the lane owns `round-12.md`). Verifiers were fresh agents dispatched by the orchestrator
after the round landed at `2a0d6c1`; full reports are committed in the fleet repo at
`.ufo/waves/kaika-w3/kaidoku-review.md` and `kaidoku-critic.md`.

## Spot-check (LEARNING.md — at least one admit and one reject)

| decision | sample | verifier | result |
|---|---|---|---|
| admit | C1 entry `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` — independent `inspect-go-binary` recheck reproduced the repeat ID and path-dependent copy IDs | W3ReviewKaidoku | agree |
| reject | PL-4 substring-form pointer rows (17/24 mutants killed) rejected by the lane in favour of rows killing 20/20 — five further independent mutants all killed | W3ReviewKaidoku | agree |

## Adjudication

ADMITTED on per-axis verdicts: coverage improved, depth improved, operability improved (outside the lane's owned axes — debt: record the axis add or withdraw it next round), calibration/freshness/adjacency unchanged; trends expansion improved, quality unchanged, discernment improved. Debts carried to round 13: create `corpus/SOURCES.md`; give the C1 entry an `S###` source row; disclose the unpaired custody legs in the entry.
