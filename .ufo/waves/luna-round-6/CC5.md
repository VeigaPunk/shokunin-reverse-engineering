# CC5 — leg 5 cross-lane comparison (lane B seat)

## CLAIM
Leg 5 (`inspect_electron_fuses` on an Electron carrier) agrees across lanes at class and byte level: lane A's CLI receipt and lane B's BB5 MCP receipt both return RESULT, matching frozen L5; my independent replay reproduces lane B's stdout byte-for-byte and lane A's dossier content exactly.

## METHOD
Read-only hashing plus one disclosed non-blind replay (the compare assignment).
- Recomputed both receipts' embedded stdout blocks (+LF): lane A 3771 B → `afebe903…` = recorded (`receipts/leg-5.md:12`); lane B 9085 B → `14ef0f1c…` = recorded, line hashes 1037 B `5a4a91b6…` / 8048 B `83f9d564…` = recorded (`receipts-B/leg-5.md:24,44-45`). Receipt file hashes: lane A `52741f00…`; lane B `57ac0124…` = `BB5.md:2` claim.
- Carrier `/usr/lib/signal-desktop/signal-desktop` re-hashed on disk: `f7a9b441…`, 223,513,856 B = SC3.md:10 = both receipts' input.
- Replay: `/tmp/rea-cc5`, `npx -y rea-agents@6.5.0 --mcp`, NDJSON initialize (2024-11-05) + `tools/call` `{"path": …}`; raw stdout/stderr kept at `/tmp/rea-cc5/`; server rc 0 via stdin close; no driver leftovers.

## FINDINGS
- Class: both lanes RESULT (JSON-RPC `result`, no `error`, exit 0) = frozen L5 → MATCH (`receipts-B/leg-5.md:50`; `receipts/leg-5.md:11`).
- Byte reproducibility: my replay stdout = 9085 B `14ef0f1c…`, identical to lane B's measurement stdout including both per-line hashes. My inner dossier text (3770 B, `140be763…`) + LF = `afebe903…` = lane A's recorded stdout.
- Payload identity: canonical-JSON equality lane A = lane B `content[0].text` = `structuredContent`; same `evidence_id ev_36045c43…`, subject sha `f7a9b441…`, 9-fuse fingerprint (RunAsNode disabled … WasmTrapHandlers enabled, raw bytes 48/49), sentinel offset 35260752, `complete:true`.

## THREATS
Replay non-blind — both receipts were read as the compare assignment requires; byte equality evidences determinism, not blind prediction. Common-mode: one host, node v26.12.0, shared npx cache, same REA build — intra-host reproducibility only. Other seats' probes were visibly running concurrently (e.g. cc3-luna6); none touched my session. Config drift, Command A/token set, and host-write audits are other seats' scope, not verified here.

## VERDICT
CLEAN — leg 5 RESULT↔RESULT (both match frozen L5); all receipt hashes and the carrier hash recompute; my independent replay is byte-identical to lane B and content-identical to lane A.
