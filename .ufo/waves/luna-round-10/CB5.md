## CLAIM
Adversary check of X4's assembled round-10 closeout draft (X4.md:8-26) for claims exceeding evidence, against primary records at true HEAD `c343939`.

## METHOD
Read X4 plus every cited seat (R8/F1/F2/C1/C3/C4/W2-W4/W7/W9/D1-D5/Y1-Y4/S4/S5/N2/A1/X2/P0/P1/W10) and fleet `MANIFEST.json:2747-2867`. Re-ran the `SCORECARD.md:93-123` Command A recipe; `git rev-parse HEAD`, reflog, `git diff --numstat` per records commit; counted the nine reports' `## Verdicts` tokens; `ls` round-9 wave count. Read-only; sole write this file.

## FINDINGS
1. **Stale HEAD.** `git rev-parse HEAD` → `c343939` ("protocol conformance…operator amendment rollout", reflog HEAD@{0}, 22:42:01), `+28/-0` EOF appends to LOG.md/SCORECARD.md (Capabilities/Saturation scaffolds), one commit past the briefed `6e83a20`. X4 (synthesized 22:36) names only `6e83a20` and omits the obligation its added `## Saturation` text creates: the lane's next round — round 10 — must declare saturation line + window N (`AXES.md:65-83`). I re-ran Command A at `c343939`: 79/79, 9/9, 10.0/10.0, missing/dangling `[]` — C1's numbers replicate; the text is stale vs final HEAD.
2. **Mandated disclosure omitted — and under-scoped.** `R8.md:10` requires disclosing SCORECARD rewrites (it lists rounds 2,3,4,7); `X4.md:19` omits it. Numstat over all nine records commits: SCORECARD deletions in FIVE — `a4bd355` (40/4: rewrote coverage row + Open-gap), `a9580eb` (60/8), `0772d54` (55/7), `cfc84c2` (46/1), `6e2ee8f` (32/1); other four pure appends; LOG 0 deletions. True scope = rounds 1,2,3,4,7 (adds r1 to PB2:26's five-commit finding).
3. **Mis-citation.** `X4.md:13` "…with lane identity (…`Y3.md:5-12`)" — `Y3.md:11` explicitly disclaims lane identity; the supporting seats are `Y4.md:8-18`/`N2.md:9` (uncited). I reproduced 19 arc commits, all `kaidoku-shokunin <kaidoku@shokunin.local>`. Also `X4.md:15` cites W9:7-19 for "does not prove seven missing" (line is W9:26), and `X4.md:19` cites round-10 `R6.md:8-15` for landed scope — actual sources `P0.md:8`/`P1.md:10`/`W10.md:13`.
4. **Claims that replicate exactly:** 9 improved/27 unchanged/0 harmed/0 unprovable = 36 axis verdicts counted from the nine `## Verdicts` sections (e.g. r1:85-91); six MANIFEST prose values across five rows = `MANIFEST.json:2791,2805,2819,2846-2847,2860`; round 6 = 127 (`:2824`); R9 = 121 files (reproduced); 896/895 = records arithmetic over MANIFEST self-declarations (R8/R9 128-unrostered; draft's R9 caveat bounds it); SHONEN 4×`[~]` (S4/S5).

## THREATS
`c343939` landed after X4 and most lane-A files; lane-B seats NB1/NB2/PB2/TB1 independently caught it — I confirm from primary. Wave files still mutating (236 untracked). No sibling/receipt re-runs; no live probes/network.

## VERDICT
FINDING: X4's numbers replicate, but the assembled text omits the required five-commit SCORECARD-rewrite disclosure and the `c343939` saturation obligation, and mis-cites lane identity to a source that disclaims it.
