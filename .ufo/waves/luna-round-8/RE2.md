## CLAIM
At this filesystem snapshot, raw receipts confirm 1/10 frozen predictions matched; nine legs are unscored, not mismatches. This is not a final battery score.

## METHOD
Read the current receipt inventory and scored each available raw receipt against the dispatch's frozen predictions. `ls -la .ufo/waves/luna-round-8/receipts` listed only `leg-1.md`. Compared with `.ufo/waves/luna-round-8/PS3.md`; no probes run.

## FINDINGS
| Leg | Frozen prediction | Raw receipt evidence | Score |
|---|---|---|---|
| L1 | Exact version `6.4.0`, exit 0 | `receipts/leg-1.md:3-11`: stdout `6.4.0`, stderr empty, exit 0 | Match |
| L2 | Exactly 170 tools | No receipt | Unscored |
| L3-L8 | Six specified 6.5-only verbs each TYPED-REFUSAL | No receipts | Unscored |
| L9 | Six 6.5-only names absent from 170-tool list | No receipt | Unscored |
| L10 | `analyze` / `inspect-binary-layout` control RESULT | No receipt | Unscored |

My tally: **1 confirmed match / 10 slots; 9 unscored; 0 evidenced mismatches**. PS3 reports 0 scored / 10 unscored based on its earlier no-receipt snapshot (`PS3.md:2-5,21`). Difference: +1 verified match now available (L1); no disagreement on an observed outcome.

## THREATS
This is a point-in-time inventory; further receipts may arrive. Recompute against all ten final raw receipts before treating this as the completed score.

## VERDICT
FINDING: 1/10 confirmed matched; nine unscored; PS3's zero-scored snapshot is superseded for L1 only.
