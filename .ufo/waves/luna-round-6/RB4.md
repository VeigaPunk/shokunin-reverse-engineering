## CLAIM
Read-only review of RV1–RV8 + XA at f0e8cde: replay coverage is outcome-class-adequate (10/10 legs) but receipt-faithful for only 5/10 digest-anchored legs; the MANIFEST-only-L1 defect is moderate bookkeeping damage, not outcome corruption.

## METHOD
Read RV1–RV8, XA, EX6/EX7/EX8/EX10, CA6, all ten `receipts/leg-*.md`, `MANIFEST.txt`, `census-pre.txt`. Recomputed read-only: receipt file hashes; the MANIFEST entry (matches `leg-1.md`); L1 stdout `3eb8e06c…`; L9 target frame `2b596b31…`; per-receipt field audit (command/stderr/exit/≥1 hash, 10/10). `ps` check for RV1's flagged EX8 server. No probes started.

## FINDINGS
- Class coverage: every leg replayed (RV1.md:8-9 L1–L2; RV2.md:8-10 L3–L5; RV3.md:8-10 L6–L8; RV4.md:9-10 L9–L10), plus RV7.md:5 reruns.
- Receipt-level reproduction is thinner: L1/L2 byte-compared (RV1.md:8-9), L7 (EX7.md:8), L8 and L9 digests (RV7.md:5), L5 key fields only (RV2.md:10). Unreproduced: L3 (replay `af23888b…` vs receipt `fb47bd53…`, leg-3.md:221), L4 (replay carrier `/usr/bin/rg` vs Signal `.node`, RV2.md:9 / leg-4.md:18), L10 (replay was Harmony `invalid_input`; canonical leg-10.md:16 is WABT `capability_unavailable`).
- L6's executor transcript is lost: leg-6.md:1 is RV3's replay, displacing EX6 (EX6.md:15); EX6's `/tmp` capture no longer exists.
- `MANIFEST.txt` (mtime 18:18:38) has one line, `leg-1.md`, hash correct; legs 2–10 landed 18:19–18:28, never added; format is `file hash`, so `sha256sum -c` fails (CC1.md:17). RV5.md:11 flagged regeneration; nothing owned it.
- RV5/RV6/RV8 audited the pre-receipt state (18:17–18:18), so their verdicts are stale; no RV seat re-audited the final 10-file set — XA did, but XA.md:12 misattributes the L10 Harmony route to "RV2.md:6,10" (it is RV4.md:6,10). RV1.md:13's leaked EX8 MCP process (PID 5403) is gone.

## THREATS
Chronology is inferred from mtimes, not a signed log; lane-B probes are still running (`ps`: cc6-leg6 MCP), so lane-A files may change. Treating `capability_unavailable` as TYPED-REFUSAL is EX10's classification, unadjudicated here.

## VERDICT
FINDING: coverage suffices for class scoring (10/10), not receipt fidelity (L3/L4/L10 unreproduced, L6 transcript lost); MANIFEST-only-L1 is moderate — the delivered 10-file set is unanchored and not `sha256sum`-checkable — but no leg outcome is corrupted (recheckable stdout digests recompute).
