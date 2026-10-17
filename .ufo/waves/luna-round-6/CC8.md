# CC8 — compare seat: leg 8 (L8 inspect_with_objdump on jq), lane B

## CLAIM
Lane-B independent re-run reproduces L8's pre-registered RESULT class on both jq carriers. Cross-lane agreement is stronger than class-level: mirroring lane A's exact carrier (/usr/bin/jq) reproduces its Evidence byte-identically — same evidence_id ev_aa75cc2e36b149a82b41e763b92697efc1e2c432571d14c003e3a7bff0219c2f, same raw objdump stdout, subject digest e8156675…, exit 0, completion_status complete.

## METHOD
From /tmp/rea-cc8, stdio MCP sessions `npx -y rea-agents@6.5.0 mcp` (initialize → notifications/initialized → tools/call), stdin held open 6s so responses flush, `timeout 240`, each server exited 0 on EOF. Discovery pass before any lane-A reading: server rea 6.5.0, tools/list = 207. Primary run used PATH jq (/home/vgpnk/.local/bin/jq, static, sha256 b1c22172…); compare run used RV3's carrier (/usr/bin/jq, PIE, sha256 e8156675…) only after my run and stdout hash were recorded. Receipt: receipts-B/leg-8.md (embedded stdout hash-verified byte-exact against capture files).

## FINDINGS
- Primary (B carrier, jq-1.8.2 static, 2,267,912 bytes): evidence ev_d1ea68b7…, objdump -f output, exit_code 0, artifact_changed false → RESULT, MATCH; stdout sha256 86f5497f….
- Compare (A carrier): evidence_id and raw stdout identical to RV3's receipt (.ufo/waves/luna-round-6/receipts/leg-8.md); reproduced across two independent process runs (stdout sha256 9c47f056… twice) → evidence_id is deterministic over subject+operation+provider output.
- Carrier divergence is the only substantive difference: PATH jq is the 2.27 MB static build; RV3 used the 30.8 KB PIE /usr/bin/jq. The frozen prediction pins only "on jq"; both satisfy RESULT.
- Invocation forms differ (RV3: `--mcp` flag, protocol 2025-03-26; mine: `mcp` subcommand, 2025-06-18) yet the same server and the same Evidence result; stdout-envelope hashes differ only for that reason.
- Driver note: closing stdin immediately raced teardown (id:2 response dropped; server stderr logged status:error, 6.05 ms) — a driver artifact, not a REA behavior; the held-open-stdin form is authoritative.

## THREATS
- Concurrent lane-B seats ran their own REA servers during my probes (foreign PIDs observed in pgrep); my sessions all exited 0 and were verified gone before I finished.
- RV3's original stdout artifact was not retained by lane A; byte comparison rests on evidence_id equality (deterministic over content, confirmed by repetition) plus their embedded receipt copy.
- Only operation file_headers was exercised; other objdump operations unobserved. npx cache is shared and warm (common-mode with lane A).

## VERDICT
CLEAN — leg 8 RESULT class matched in both lanes; Evidence byte-identical given equal carrier; receipts-B/leg-8.md filed.
