## CLAIM
RB1 reviewing WB1-6: verify the SCORECARD rewrite diffs (round 2/3/4/7 records commits) and the dispositions left in the WB1/WB2/WB3/WB5/WB6 re-audit seats.

## METHOD
Read-only git objects. `git diff --numstat`/`-U0` and byte-prefix tests (`git cat-file blob`) for all nine records commits plus `c343939`; Command A (`SCORECARD.md:92-123`) replays from immutable objects; `git blame`; MANIFEST/seat-count spot checks; read of the WB seats on disk at my cut. No probes, network, or deletions; only this file written.

## FINDINGS
Six sites verified byte-exact: `a9580eb^:25` calibration row; r2 `:56-62` version-drift; `0772d54^:24` depth row; r3 `:61-66` authority-contradiction; `cfc84c2^:68` pointer `:157`→`:160`; `6e2ee8f^:23` coverage row 72/72@`2abd30f5`→78/78@`3395b6d`.

Arc census: five of nine records commits rewrite SCORECARD, head-only, 21 deleted lines (r1 `a4bd355^` `:23`+`:53-55`, 4; r2 8; r3 7; r4 1; r7 1). LOG prefix-identical in all nine (0 deletions); work commits touch neither file; r5/r6/r8/r9 and `c343939` are pure appends. Command A reproduces every cited measured value; at HEAD it returns 79/79 while `SCORECARD.md:23` still reads 78/78@`3395b6d` — WB2's stale-row finding confirmed (map now ends `corpus/README.md:68`, row says `:11-67`).

WB review: WB1/WB2/WB3 diffs and counts match my independent census; nit — WB3's r1 old lines `:20`/`:52-54` do not reproduce (actual `:23`/`:53-55`; substance unaffected). Disposition split: WB1/WB3 read strict (undisclosed rewrites → adjudication); WB2 reads lenient (living-row update, not a breach), grounded in `PROTOCOL.md:420` (row = score → pointer → last-change round) and `:447` (append-only line names LOG). WB1's r1-disclosure quote reproduces (`SCORECARD.md:267-268`). WB5's six decorated values (`MANIFEST.json:2791,2805,2819,2846,2847,2860`) and WB6's counts (64/64/126/127/127; r7 128 artifacts incl. `receipts/census-final-B.txt`) spot-check clean. WB4 (landed mid-review) also reproduces: the r4 pointer fix is disclosed (`SCORECARD.md:71-72`; `LOG.md:748`; report:53) but mispoints — at `cfc84c2`, `corpus/README.md:160` is the sasquatch row and the described content is `:163`; `:128` is stale; at HEAD it moved to `:177`.

## THREATS
Goal text not in-repo (WB2, WB3, WB5 agree). Round-1's rewrite was unflagged by lane A's W1 but disclosed in-row; strict readings make it a fifth deviating commit. Brief said HEAD `6e83a20`; actual HEAD is `c343939` (additive: 16+/0 LOG, 12+/0 SCORECARD). Seats may still land after my cut.

## VERDICT
FINDING: six sites and the rewrite census verified; WB1/WB2/WB3/WB4/WB5/WB6 reproduce (nits: WB3's r1 lines, WB4's disclosure-is-wrong-value); disposition split (strict vs living-row) needs parent adjudication — under the strict criterion include round 1.
