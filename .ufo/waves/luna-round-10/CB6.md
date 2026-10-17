## CLAIM
Adversary re-run of the lane-A scope sweep in English plus content check of N1: N1's artifact is English, not Russian; its scope verdict holds, but it omits two of four records-commit SCORECARD rewrites and mis-points peer citations.

## METHOD
Read N1.md, its cited peers (R1/R3/R7/W3/W6/W7/S4/S5/K1), and the post-N1 arrivals; re-ran `git diff --numstat <records>^ <records> -- LOG.md SCORECARD.md` for a9580eb/0772d54/cfc84c2/6e2ee8f; re-ran N1's scope commands at actual HEAD `c343939` (brief's `6e83a20` stale: `git diff --numstat 6e83a20 c343939` → `16 0 LOG.md; 12 0 SCORECARD.md`); proposal-vocabulary grep over all 99 notes (22:47:41 -03); sibling-side spot check of K1. No probes, network, or deletions; only write is this file.

## FINDINGS
- Premise fails: `file` N1.md → "Unicode text, UTF-8 text"; first bytes ASCII `## CLAIM`. Kaidoku-wide plus four siblings' `.ufo` Cyrillic scans (`grep -rlP '[\x{0400}-\x{04FF}]'`) → zero hits.
- Miss: rounds 2 and 4 records commits also rewrite SCORECARD (numstat ins/del: a9580eb 60/8; cfc84c2 46/1); N1 names only rounds 3/7 (0772d54 55/7; 6e2ee8f 32/1 — reproduced). LOG has 0 deletions in all four. `R8.md:10` names all four rounds.
- Mis-cites: `R3.md:10` is a short-count bullet (support: `W3.md:10`); `R7.md:10-11` is CB3/round-9 text (support: `W7.md:10`, same coverage-row claim); `W6.md:9-13` covers enum prose/127-seat/census/SHONEN, not arbitration. Cited facts verified true via git.
- Count reconciles with birth+mtime: 52 files ≤ N1's cut, plus P2 (born 22:33:09, rewritten 22:37:46) = N1's "53 files (52 peers)"; P2's final text postdates N1 by 39 s, so that peer review is cut-bound.
- Re-sweep clean at `c343939`: corpus/PROVINCE diff exit 0 (worktree and staged, `HEAD`), untracked check empty, `git status --porcelain -uno` → 0 lines. No note among 99 proposes corpus/PROVINCE edits; peer YB3 independently CLEAN at 89 (`YB3.md:2,17`). K1's outbound items resolve (tsukuroi `PROVINCE.md:42,70-71`, `adjacency-handoffs-fleet-r1.md:54`; Tameshi per `YB1.md:8-14`).

## THREATS
Point-in-time: 53→99 notes during this run, lane B still landing; N1's integration re-check stands. Pattern scan, not full reads of all 99. Untracked scratch lacks history (P2's pre-rewrite content unrecoverable).

## VERDICT
FINDING: Scope cleanliness re-confirmed in English at c343939; N1 omits the round-2/4 SCORECARD rewrites and mis-points three peer citations (R3→W3, R7→W7, W6 unsupported).
