## CLAIM
All six 6.5-only verbs were refused identically at the schema/catalog layer: a top-level JSON-RPC `error` object with code `-32602` and message `Tool <name> not found`. None is a result-level (`isError`) or provider/capability-level refusal. XG1's "unclassifiable" verdict is superseded by now-present receipt bytes.

## METHOD
Read `.ufo/waves/luna-round-8/receipts/leg-{3,4,5,6,7,8}.md` from disk (landed 20:52–21:14). Grepped `"error"`, `isError`, `"tool":`; extracted each displayed ```text stdout block and recomputed its SHA-256 against the in-file claim; extracted `protocolVersion` per leg; listed `/tmp/kaidoku-luna-round-8-leg-*`. No probes run; no tracked file touched.

## FINDINGS
Every leg carries one `tools/call` refusal, all with the identical code and message template:
- `leg-3.md:22` — `-32602` `Tool inspect_go_binary not found`; block 623 B, recomputes to claimed `5c6820…d5a569`
- `leg-4.md:13` — `-32602` `Tool inspect_rust_binary not found`; 625 B → `0fbd3b…f7030d5f`
- `leg-5.md:9` — `-32602` `Tool inspect_electron_fuses not found`; 628 B → `adfb73…1f927b115`
- `leg-6.md:18` — `-32602` `Tool inspect_sqlite_database not found`; 629 B → `5bc135…537637349`
- `leg-7.md:21` — `-32602` `Tool search_bytes not found` (id 3; id 2 `open_binary` succeeded); 1075 B → `866f8b…4e6cb21bb6b`
- `leg-8.md:18` — `-32602` `Tool inspect_with_objdump not found`; 626 B → `65d740…100306241d`

All six blocks hash exactly to their claimed value. `isError` occurs 0 times in all six files; no other JSON-RPC error code appears. Class is invariant across negotiated protocol version (2024-11-05 in legs 3/4/5/8; 2025-03-26 in legs 6/7) and the uniform `Tool <name> not found` template marks a registry lookup rejection before dispatch. Positive dispatch evidence: `leg-7.md:26` stderr holds exactly one execution log line, for `open_binary`; no line exists for `search_bytes`. Verb names match the six round-7 entries `corpus/knowledge/2026-10-16-l7-01..06`.

KNOWN-DEFECT note: `leg-3.md`'s displayed block now recomputes to the claimed `5c6820…`, and `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B) hashes identically — display corruption is not observable in present bytes.

## THREATS
Hashes are self-consistent, not independently attested: only leg-3 has a surviving raw `/tmp` stdout; legs 4–8 raw files are absent, so their display integrity rests on the in-file claim. `-32602` is JSON-RPC "Invalid params" repurposed by the server as unknown-tool — a spec-code nuance, not a separate class. A mistyped tool name could mimic this message, but the names match the six knowledge entries. No probe re-run (not assigned).

## VERDICT
CLEAN: all six refusals are `-32602` `Tool <name> not found` — schema-level unknown tool, uniform across the six legs.
