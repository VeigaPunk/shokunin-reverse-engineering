# RB3 — claim-shape review 2 (exact claim text vs evidence; leg-10 fallback route)

## CLAIM
Exact claim sentences on record — the frozen L1–L10 predictions, EX10's L10 write-up, and leg-10.md's fallback-route section — match recomputable evidence, or their divergence is disclosed.

## METHOD
Read-only at HEAD `6e2ee8f`; no probes. Read receipts leg-1..10, leg-2-tools.txt, MANIFEST.txt, census-pre.txt and reports EX10/RV4/CA6/CE1; recomputed SHA-256 of every displayed fence and every surviving `/tmp` raw; byte-compared fences to raws; `grep -cFx` on the six frozen names plus `analyze`; `head -59 receipts/leg-10.md | sha256sum`. Only this file written.

## FINDINGS
1. **Fallback route.** leg-10.md `:13-16` recomputes `61450b92…` and is byte-equal to the surviving raw `/tmp/kaidoku-luna-round-8-leg10-summary.stdout`. The fallback re-copy `:73-76` is fenced "(incomplete transcription; not raw)", hashes `9e2726cb…`, and diverges from the raw at byte 11415 (omits the `unknowns` array) — disclosed, not silent. No raw survives for the fallback run itself (stderr 21:07:17; nothing in `/tmp`) nor for EX10's workflow block `6abdf805…`. Byte-identity stays inference: `ev_294a449…`, the summary replay's `parent_evidence_id`, also occurs in the preserved first-session raw `leg10.stdout`, so evidence IDs are session-stable and identical calls plausibly yield identical bytes. The `61450b92…` claim is honest but only transitively verifiable.
2. **Spot checks recompute.** L1 `3754366908…` = sha256("6.4.0\n"); L2 = 170 lines / 170 unique, first five names in leg-2.md:9 order; six frozen names + `analyze` = 0 `grep -cFx` matches; L3–L8 each `-32602` `Tool <name> not found`; L10 RESULT via both routes.
3. **Stale exact text.** MANIFEST.txt:10 and CA6.md:10 cite leg-10.md `c89eea7a…`; current bytes `6cd389e9…`, with `head -59` = `c89eea7a…` (27,655 B), mtime 21:14:02 after both. census-pre.txt:97 cites leg-3.md `d641e3d3…`/1430 B and leg-4.md `8f04ac26…`/1233 B vs current `1be7e4f9…`/1448 B and `aa4aa7a3…`/1200 B — neither recomputes.
4. The round-context "known defect" does not reproduce: leg-3.md `:21-22`+LF is byte-identical to `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B, `5c682099…` = claim).

## THREATS
`/tmp` is shared and mutable; raws survive only for L1–L3 and L10. L4–L9 hashes self-refer to displays. Fallback byte-identity is inference, not measurement. No live probes were run.

## VERDICT
FINDING: fallback-route claim is shape-honest but only transitively verifiable (no raw); MANIFEST.txt:10 and CA6.md:10 carry a stale leg-10 hash; leg-3 display defect does not reproduce at the current revision.
