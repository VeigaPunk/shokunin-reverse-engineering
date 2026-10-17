## CLAIM
Audit the ten expected `receipts/leg-1.md` through `leg-10.md` for command, full stdout, stderr, exit code, and stdout SHA-256 fields.

## METHOD
Read the available canonical leg receipts and checked each field's presence. The bounded existence poll (`test -f .ufo/waves/luna-round-8/receipts/leg-$i.md`, legs 1–10, repeated 12 times) reported 9/10 present in every check; the final `Glob` likewise listed legs 1–9 but not leg 10. Evidence: leg-1.md:3-11; leg-2.md:1-17; leg-3.md:4-23; leg-4.md:4-14; leg-5.md:4-14; leg-6.md:3-24; leg-7.md:3-32; leg-8.md:3-21; leg-9.md:16-24.

## FINDINGS
Each of the nine available canonical receipts contains all five fields. Empty stderr/stdout values are explicitly identified where applicable. Leg 10 was absent at the final check, so its fields cannot be assessed.

## THREATS
This is a point-in-time artifact audit, not proof that a missing probe did or did not run. The check verifies field presence only, not the correctness of each recorded hash or completeness of the captured output bytes.

## VERDICT
FINDING: legs 1–9 carry all five required fields; leg 10 is missing, so 10/10 completeness is not established.
