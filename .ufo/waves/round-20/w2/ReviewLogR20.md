PARTIAL — `LOG.md` is append-only at S, but the C1/D5 census closure is not substantiated in the S tree.

## Findings (by severity)

**Medium — D5 closure lacks its required final evidence.** Observation: the new entry says the census declares the two round-17 blocks DATED and says the D5 record-shape check was fixed (`LOG.md:2299,2310-2312`). The S contract requires `W20/verify/final-census.json` (`.ufo/waves/round-20/contract.md:55`), but that object is absent: `git show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/verify/final-census.json >/dev/null` — exit 128; `git ls-tree -r --name-only 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20 | grep -E 'final-census\.(json|stdout)$'` — exit 1. The only retained census run is explicitly `census-start`: its metadata records c1-census exit 1 at revision `d1d981d2...` (`evidence/census-start/meta.txt:1-4`), and its stdout reports two UNDECLARED blocks and `VERDICT: FAIL` (`evidence/census-start/c1-census.stdout:10-14,115`). These are pre-fix observations, not proof that the final source fails; however they cannot substantiate the claimed post-fix, delivered-tip PASS. The canonical claim asserts PASS at the delivered tip (`claims.json:15-18`), so D5 remains unverifiable from S.

**Low — some LOG assertions lack direct evidence pointers.** The cited baseline tool is named at `LOG.md:2298-2299`, but the actual `open_count=11, named_open=11, substance_open=11` output is in `.ufo/waves/round-20/w1/RoutedR19Tool.md:18-39` (commands/exits at `:49-51`), not linked from the LOG entry. The attempt/quota/recovery narrative at `LOG.md:2308-2312` likewise has no evidence path in the entry; `wave1-result-attempt1.txt` is empty at S, while `wave1-dispatch-attempts.json:3-10` records dispatch attempts, not the stated 18:45/quota event.

## Holds and supersession check

- **Append-only: HOLDS.** `git diff --numstat 14f0260ad319ecc26994381b2415d5a999003375 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- LOG.md` — exit 0; output `25 0 LOG.md`. The unified diff is one insertion at `LOG.md:2288-2312`, with no B-era lines changed.
- C2’s cited S040-S046 rows exist (`corpus/SOURCES.md:46-52`) and retained C2 evidence exists under the cited directory. C3’s knowledge entry cites rerun comparison records and receipt validation (`corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md:45-47,58`); `evidence/compare-rerun/summary.txt:1-19` records exit 0 for all 19 labels. Thus the final `19/19` statement (`LOG.md:2304-2307`) follows the later rerun, not the earlier `compare=2` run log; no superseded C3 outcome remains standing.
- The round-20 entry itself is one appended block (`LOG.md:2289-2312`). No install/update was made.

Report: .ufo/waves/round-20/w2/ReviewLogR20.md
