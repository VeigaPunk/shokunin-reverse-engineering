# ZB1 — luna-round-6 final battery score (lane B synthesis)

## CLAIM
Round-6 operability battery: **10/10 outcome-class matches** (L1–L9 clean; L10 class-level only, predicted compare tool never reached), **10/10 cross-lane class agreement**, zero ERROR-UNEXPECTED, zero config drift at HEAD `f0e8cde`.

## METHOD
Read-only synthesis at HEAD `f0e8cde`: all 20 receipts (legs 1–10, `receipts/` + `receipts-B/`), tallies PS3/RE2, compares CC1–CC10, adjudications CB9/BB10, controls CB1/CB5/CB8. No probes run.

## FINDINGS
| Leg | A-class | B-class | Agreement | Match |
|---|---|---|---|---|
| L1 | RESULT | RESULT | byte `3eb8e06c…` | ✓ |
| L2 | RESULT | RESULT | byte `38d44bf8…`, count 207 | ✓ |
| L3 | RESULT | RESULT | byte `fb47bd53…` | ✓ |
| L4 | RESULT | RESULT | class only (A `.node` vs B `rg`) | ✓ |
| L5 | RESULT | RESULT | payload (dossier `afebe903…`; NDJSON `14ef0f1c…`, same evidence_id) | ✓ |
| L6 | RESULT | RESULT | class only (probe table vs `sc4-index.db`) | ✓ |
| L7 | RESULT | RESULT | byte `3492d27d…` | ✓ |
| L8 | RESULT | RESULT | Evidence id on equal carrier (CC8) | ✓ |
| L9 | TYPED-REFUSAL | TYPED-REFUSAL | byte frame `2b596b31…` | ✓ |
| L10 | TYPED-REFUSAL | TYPED-REFUSAL | byte `e4cf0833…` | ✓* |

10/10 class matches. L10* = `capability_unavailable` (WABT absent) at prerequisite `inspect_wasm_artifact`; `compare_wasm_interfaces` never sent — flagged by EX10/BB10/CC10/CB9; credit rests on that typed refusal counting as TYPED-REFUSAL. Agreement 10/10 (6 byte-identical, 2 payload/Evidence, L4/L6 class-only; cites e.g. CC1.md:10, CC3.md:9, CC5.md:15, CC9.md:11, CC10.md:10). Both receipt sets hold 10 legs (CC10.md:13). PS3's 7/10 snapshot superseded (its missing L3/L7/L10 all matched); RE2 stale. No ERROR-UNEXPECTED.

## THREATS
- receipts-B overwritten by compare seats: leg-3 = CC3 (19:07:53; BB3's `75b83edf…` original displaced), leg-7 CC7, leg-8 CC8, leg-9 BB9-over-CC9; displaced versions unrecoverable (untracked dir).
- CB1 forged a valid receipts-B entry from lane A stdout (no fraud found); BB2/BB7/BB10 and CC seats read lane A pre-run (CB8) → corroboration, not blind replication.
- Common mode: one host/node/npx cache; L10's predicted tool unobserved; L4/L6 carriers/scopes differ.
- Command A/token-set controls: other seats' scope (CB5 CLEAN); probe seats report no config edits.

## VERDICT
CLEAN — battery score: 10/10 outcome-class matches (L10 class-contingent, route flagged), 10/10 cross-lane agreement, 0 ERROR-UNEXPECTED, 0 config drift.
