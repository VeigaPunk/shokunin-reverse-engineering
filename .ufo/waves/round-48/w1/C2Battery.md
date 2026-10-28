# R48-C2 mutation probe (C2Battery)

Axes: calibration (primary), depth/coverage unaffected. Frozen claim: `plans/round-48-claims.md@dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`. Assignment is to attack the frozen C2 battery before landing; this seat is read-only on lane sources.

## Baseline detector

Command:

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C2Battery python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/record2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/C2Battery/receipt.json
```

At `2026-10-28T18:48:14Z`, exit 1; stdout SHA-256 `f0bf3d66c54b8d954b6f6e0bec2916d31b1afccde806da2ce20ae2260c1ab6be`. Raw stdout saved in scratch `stdout.txt`; JSON receipt saved at `C2Battery/receipt.json`. Genuine v3 failed three structural requirements: round-47 no seat atom/correction, no re-derived round-48 corrections line, and round-47 `exempted 2` quote unbacked (cited receipts are C1/C2 A7). Oracle itself was green (44 atoms; mismatches empty; met_target true), axis score cells passed. Battery metrics are absent: it explicitly skipped because genuine structural clauses failed. Consequently no battery mutant verdict can be inferred from this run.

## Frozen battery attack and precondition finding

Code inspection of frozen `record2.py` identifies a testability gap in the precondition: `evaluate()` calls `run_battery()` only if the genuine score is 0; on any nonzero code it returns `battery: {skipped: ...}`. This makes all mutation coverage conditional on a complete green landing card. It hides what the battery itself is supposed to detect whenever the genuine record has any missing clause, including the specific floor/quote corrections absent at freeze. This is an observed gating behavior, not an assertion that an unseen forged card survives.

The five mutation implementations are `gold-tautology`, `seats-moved`, `quote-off-by-one`, `axes-score-cell-off`, `axes-correction-forged`. The current frozen card is not genuine-green, so a meaningful execution of them through the prescribed evaluator is unavailable at this revision. Therefore requested determinations (no-op mutant at landing revision, failure for wrong clause, v3-green survivor) are **not run / inconclusive**; no landing revision was supplied and must not be fabricated. The assignment is expressly before landing, so this negative result is the correct bounded evidence rather than constructing an artificial green card.

Restoration: no mutation was made; no frozen or other lane source changed. Scratch is used for process temp/output only. No fixture repo or git mutation created. No tool installed. Disk guard checked before the pass (scratch volume 32% used, 548.7G free).