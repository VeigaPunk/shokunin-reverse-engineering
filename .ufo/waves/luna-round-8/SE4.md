## CLAIM
The sentinel expectation is that only `.ufo/waves/luna-round-8` appears as untracked in `git status`.

## METHOD
Ran `git status --short --untracked-files=all` from the repository root (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`).

## FINDINGS
Expectation not met. The output includes untracked paths outside round 8, including:
- `?? .ufo/interactive-sessions/20261015T050057Z/2026-10-15T05-04-02-264Z_01a13df2-26d8-70e2-8904-b7b57b6735e2.jsonl`
- `?? .ufo/waves/luna-round-1/C1.md`
- `?? .ufo/waves/luna-round-7/BB2.md`

The output also lists `.ufo/waves/luna-round-8/EX1.md` and `receipts/leg-1.md`. All reported entries were `??` (untracked); no modified or staged tracked paths appeared.

## THREATS
This is a point-in-time working-tree status; concurrent or later changes are not covered. Existing untracked paths' ownership and origin are unverifiable from this command.

## VERDICT
FINDING: untracked paths exist outside `.ufo/waves/luna-round-8`.
