## CLAIM
Score legs 1–5 against the parent-frozen predictions using receipt evidence only.

## METHOD
Read `.ufo/waves/luna-round-6/receipts/leg-1.md:3-11`. Inventory command `ls -la --time-style=long-iso .ufo/waves/luna-round-6/receipts/` showed `leg-1.md` only (271 bytes); no probes were run.

## FINDINGS
- L1 — PREDICTED: exact `6.5.0`; OBSERVED: stdout `6.5.0`, exit 0, stderr empty; match: YES (receipt SHA-256 recorded at `leg-1.md:11`).
- L2 — PREDICTED: exactly 207 tools; OBSERVED: no receipt available; match: UNSCORED.
- L3 — PREDICTED: RESULT class; OBSERVED: no receipt available; match: UNSCORED.
- L4 — PREDICTED: RESULT class; OBSERVED: no receipt available; match: UNSCORED.
- L5 — PREDICTED: RESULT class; OBSERVED: no receipt available; match: UNSCORED.

Scoreable: 1/5; matching among scoreable: 1/1. Missing evidence is not classified as ERROR-UNEXPECTED.

## THREATS
Legs 2–5 may have run without receipts yet; no observation supports assigning their outcome classes. This score is limited to the receipt inventory at scoring time.

## VERDICT
FINDING: L2–L5 remain unscored because their receipts were absent.
