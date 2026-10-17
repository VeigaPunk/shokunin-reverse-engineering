## CLAIM
XG2's finding stands on re-verification: current `/usr/bin/docker` and `/usr/bin/jq` bytes match the round-6 SC SHA-256 pins; `/usr/bin/rg` matches SC2's pin, but round-6 lane-A primary L4 exercised Signal's `.node`, not rg.

## METHOD
Read round-6 `SC1.md`/`SC2.md`/`SC6.md`, `receipts/leg-3,4,8.md`, `receipts-B/leg-4.md`, and round-8 `receipts/leg-3,4,8.md`. Ran read-only `sha256sum /usr/bin/docker /usr/bin/rg /usr/bin/jq` and `stat -Lc`. No REA/MCP calls; no tracked file touched; only write is this report.

## FINDINGS
- Fresh hashes (this session): docker `70f68a77…5f45c9`, 29,327,600 B = SC1.md:11; jq `e8156675…4f7806`, 30,800 B = SC6.md:8; rg `d006acfe…4ecae42`, 4,377,936 B = SC2.md:10. All exact; sizes match XG2's values.
- Round-6 primary carriers: docker L3 target + call `receipts/leg-3.md:5,17`; jq L8 carrier + digest `receipts/leg-8.md:10-11`. XG2's citations check out.
- rg asymmetry confirmed: lane-A L4 called `inspect_rust_binary` on the Signal `.node` fallback — args `receipts/leg-4.md:12`; reason :15 ("SC2 carrier attribution could not be found… no SC2 carrier record was available"); digest `1b44ed53…` :21; ":43 The SC2-carrier identity itself remains unverified". Lane-B L4 used `/usr/bin/rg`, "matches SC2's discovered carrier hash exactly" (`receipts-B/leg-4.md:14-18`). `grep -l 'usr/bin/rg'` over all round-6 lane-A `receipts/leg-*.md`: no matches.
- Round-8 (6.4.0) lane-A legs target the same carriers: docker `receipts/leg-3.md:5`, rg `receipts/leg-4.md:5`, jq `receipts/leg-8.md:8` — so rg was exercised by lane A this round, unlike round-6.

## THREATS
Matching hashes identify bytes, not which bytes a process consumed; receipt text is static and the round-8 refusal legs did not read the artifact. "Primary" is my reading of lane-A execution legs. No 6.4.0/6.5.0 server was run by this seat.

## VERDICT
CLEAN — XG2's finding stands: docker/jq pins re-verified on current bytes; the rg pin's round-6 lane-A primary was the Signal `.node`, with rg carried by lane-B (round 6) and lane-A (round-8 refusal leg).
