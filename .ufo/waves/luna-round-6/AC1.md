## CLAIM
Lane A matches the assignment's frozen battery predictions on all ten legs: 10/10.

## METHOD
Compared each `receipts/leg-N.md` with the frozen expectations specified in this assignment. Scored the current raw receipts; earlier report snapshots are not treated as current receipt inventory. No probes run.

## FINDINGS
| Leg | Frozen prediction | Observed class/value | Match? |
|---|---|---|---|
| L1 | Exact `6.5.0` | `6.5.0`, exit 0 | Yes |
| L2 | Exactly 207 tools | `tools/list`: 207 | Yes |
| L3 | RESULT | Structured `inspect_go_binary` result | Yes |
| L4 | RESULT | Structured `inspect_rust_binary` result | Yes |
| L5 | RESULT | Structured Electron-fuses result | Yes |
| L6 | RESULT | Structured SQLite inspection result | Yes |
| L7 | RESULT | Structured `open_binary` / `search_bytes` results | Yes |
| L8 | RESULT | Structured objdump result, exit 0 | Yes |
| L9 | TYPED-REFUSAL | `invalid_request` / `invalid_input` | Yes |
| L10 | TYPED-REFUSAL | `capability_unavailable` / `unsupported_provider` | Yes |

Score: **10/10**, zero mismatches, zero unscored legs.

## THREATS
PS1–PS3, RE2, CB9, and XG2 contain earlier receipt-availability snapshots. PS4 separately states a conditional L10 prediction (`RESULT` if carriers exist), unlike the frozen L9–L10 TYPED-REFUSAL classes supplied in this assignment. If PS4's conditional is the authoritative freeze, L10 mismatches and the score is 9/10; this table follows the supplied assignment freeze.

## VERDICT
FINDING: 10/10 under the assignment's frozen classes; reconcile PS4's conflicting L10 wording before claiming zero drift.
