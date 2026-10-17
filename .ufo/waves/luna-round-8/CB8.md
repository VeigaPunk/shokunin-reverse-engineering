## CLAIM
CA10's strict RESULT criteria (CA10.md:5-7) applied to the now-present leg-10 receipt: PASS/FAIL per criterion; L10 = RESULT only if every conjunct holds.

## METHOD
Read CA10.md, receipts/leg-10.md, RV4.md, P0.md (:5,:13). Read-only verification: sed-extracted displayed stdout blocks, sha256sum/cmp against surviving /tmp captures; parsed the full-run stdout frames; recomputed `sha256sum /usr/bin/jq`; checked both tool-name lists. No server runs; no writes except this file.

## FINDINGS
1. Pinned server from /tmp ≤240s — PASS. `npx -y rea-agents@6.4.0 mcp`, cwd=/tmp (leg-10.md:3,30,63; P0.md:5); /tmp captures prove live runs (mtimes 20:53/20:57), call durations <5s, no timeout.
2. initialize = rea 6.4.0 — PASS. leg-10.md:14; independently frame id=1 of /tmp/kaidoku-luna-round-8-leg10.stdout (2,127,950 B, SHA-256 `23e94d0b…`).
3. Control verb advertised + exact tools/call — PASS via inspect-binary-layout: in the 170-name list (leg-2-tools.txt:85; same-session tools/list frame count 170); exact request leg-10.md:9. Bare `analyze` is absent from both the 6.4.0 list and round-6's 6.5.0 list, so EX10's `-32602` (leg-10.md:45) is correct behavior, not a gate failure.
4. Matching response id clean — PASS. Block-a id=2 carries a result with no JSON-RPC error/isError (re-verified in the artifact).
5. Success schema, nonempty, IDs, carrier digest — PASS. `ev_9befd8a5…`, provider rea-analysis-view, subject sha256 `e8156675…` equals my recomputed `sha256sum /usr/bin/jq`. Nuance: the compact capture is a view projection (operation inspect_analysis_view, parent_operation inspect_binary_layout); direct full layout Evidence `ev_294a…` is inside the verified 2.1 MB artifact.
6. Full capture — PASS for the control of record: displayed stdout byte-identical to /tmp/kaidoku-luna-round-8-leg10-summary.stdout (14,250 B), hashing to claimed `61450b…`; stderr byte-matches; exit 0 recorded (no per-leg .exit file in /tmp); EX10 display self-hashes to its claimed `6abdf805…`.
7. Normal exit — PASS. Exit 0 recorded each block; stdout LF-complete; final stderr status ok.
Extras: the fallback copy is truncated exactly as its label says (11,589 vs 14,250 B), raw claim assertion-only; EX10 workflow frames lack /tmp artifacts.

## THREATS
cwd=/tmp, the 240s cap, and exit 0 are receipt assertions — corroborated, not artifact-proven. Fallback byte-identity to block A is unproven. A deterministic server could imitate the schema (CA10's residual). The compact RESULT is derivative; direct Evidence exists only in the large artifact.

## VERDICT
CLEAN: all seven CA10 criteria PASS on artifact-verifiable evidence for the inspect_binary_layout control; L10 = RESULT holds.
