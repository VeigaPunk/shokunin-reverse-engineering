## CLAIM
At the latest visible snapshot, **1/10 predictions matched**; nine legs remain unscored and no mismatch is evidenced. This is a partial, not final, battery score.

## METHOD
Inventoried `.ufo/waves/luna-round-8` with `Glob("**/*")`; visible artifacts included only `receipts/leg-1.md` as a receipt. Compared its captured result with the frozen prediction. No probes run by this synthesis seat.

## FINDINGS
| Leg | Frozen prediction | Evidence / score |
|---|---|---|
| L1 | Exact version `6.4.0`, exit 0 | stdout `6.4.0`, exit 0 (`receipts/leg-1.md:3-11`); match (1) |
| L2 | Exactly 170 tools | No receipt; unscored |
| L3 | `inspect_go_binary`: TYPED-REFUSAL | No receipt; unscored |
| L4 | `inspect_rust_binary`: TYPED-REFUSAL | No receipt; unscored |
| L5 | `inspect_electron_fuses`: TYPED-REFUSAL | No receipt; unscored |
| L6 | `inspect_sqlite_database`: TYPED-REFUSAL | No receipt; unscored |
| L7 | `search_bytes`: TYPED-REFUSAL | No receipt; unscored |
| L8 | `inspect_with_objdump`: TYPED-REFUSAL | No receipt; unscored |
| L9 | Six 6.5-only names absent from 170-tool list | No receipt; unscored |
| L10 | `analyze` / `inspect-binary-layout` control: RESULT | No receipt; unscored |

**Current tally: 1 match / 10; 9 unscored; 0 evidenced mismatches.** Do not cite as the final score.

## THREATS
The lane is active and artifacts may appear after this snapshot. Recompute from all ten final receipts before reporting the round score.

## VERDICT
FINDING: L1 matches; final N/10 remains unestablished pending the other nine receipts.
