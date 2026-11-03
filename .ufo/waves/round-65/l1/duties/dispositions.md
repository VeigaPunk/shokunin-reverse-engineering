# round-65 duty findings — dispositions (before the landing)

Annotation sweep (r60 gate over the receipt corpus at the freeze `922ed89f`):
exit 0, 278 receipts, 5 findings, all 5 covered by the standing r60 disposition TSV
(`.ufo/waves/round-60/l1/records/sweep-dispositions.tsv`, pinned `ba9ccbb9…`). Names:
the r58 `c1-after.txt` annotation mismatches (2), `OUTPUT_MISSING`, `COMMAND_UNREEXECUTABLE`
and the r59 `COMMAND_UNREEXECUTABLE` row — unchanged from rounds 61–64; no disposition is
rewritten and no copy is planted.

Claims-container receipt audit (r56 gate, one run per container r53–r65 at `922ed89f`):

| container | exit | receipts_checked | findings | disposition |
|---|---|---|---|---|
| round-53 | 0 | 0 | — | clean |
| round-54 | 0 | 9 | — | clean |
| round-55 | 0 | 4 | — | clean |
| round-56 | 0 | 10 | — | clean |
| round-57 | 0 | 7 | — | clean |
| round-58 | 1 | 10 | `RECEIPT_ABSENT freeze-gate-tip-90f3a9b9.json` | standing named debt since round 58; the file is a genuine tip copy never present at the claimed revision; the flip condition is ruled not-firing; no copy planted (the sixth refusal stands) |
| round-59 | 0 | 13 | — | clean |
| round-60 | 1 | 14 | `RECEIPT_ABSENT freeze-gate-tip-90f3a9b9.json` | same standing class as round-58; named debt |
| round-61 | 0 | 15 | — | clean |
| round-62 | 0 | 2 | — | clean |
| round-63 | 0 | 0 | — | clean (lane-relative receipt pointers: the gate's full-path extractor sees none — the same style r63 and this round use) |
| round-64 | 1 | 2 | `RECEIPT_ABSENT receipt.json` | **false positive of the bare-name extractor**: the token is the placeholder `<receipt.json>` inside the frozen command template in `.ufo/waves/round-64/claims.json` (`--out <receipt.json>`), not a claimed receipt; the round's real receipt `.ufo/waves/round-64/w1/ExecMatrixRun/matrix-run.json` is present at its own revision. Filed bytes stay; the class is recorded in `corpus/lessons/round-65.md` Gate |
| round-65 | 0 | 0 | — | clean (same lane-relative pointer style; its `l1/` receipts exist at the freeze and are named in `frozen_atoms`) |

Record-receipt audit (r57 gate) over `SCORECARD.md` heading `## Round 64` at `922ed89f`:
exit 0, clean, named 21, missing 0 (`.ufo/waves/round-65/l1/duties/record-audit-r64.txt`).

Registry-drift census (r51 census3): generated at the freeze (`registry-census.json`, 69
paths) — the r64 census at `a35e5141` listed 68 because the `tools/round-64/jsc-route-matrix.py`
registry row landed after that revision; the single added path is that row. `--check` re-runs
at the record revision after the two round-65 registry rows land.

No duty above is reported as clean where its exit was non-zero; the three non-zero exits are
dispositioned, not waived.
