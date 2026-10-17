## CLAIM
OPERABILITY (unowned proxy): replay legs 9–10 on REA 6.5.0; each should return the frozen outcome class.

## METHOD
- Invoked `npx -y rea-agents@6.5.0 mcp` from `/tmp`; 240-second deadline, closed stdin and waited for each MCP server to exit. Package inventory anchor: `.ufo/waves/luna-round-2/L7.md:2-8` and `receipts/L15-tools-6.5.0.txt:1-9` (207 tools; pinned package).
- L9 used `/usr/bin/jq` (ELF x86-64, SHA-256 `e8156675…f7806`). L10: no Wasm/Harmony carrier suffixes were found in the repo corpus or accessible `/tmp`; used a temporary plain ZIP and same-session `open_binary` + `inspect_artifact` Evidence. Fixture SHA-256 `a936c304…a5cc9437`; removed after probe.

## FINDINGS
- L9: `identify_flutter_build` returned structured `invalid_input` / malformed ZIP refusal → TYPED-REFUSAL; matches.
- L10: `project_harmony_application_graph` returned structured `invalid_input`, “requires HAP, HSP, or App Pack … (got zip)” → TYPED-REFUSAL; matches.
- Assigned legs: 2/2 predicted classes. Receipts: `receipts/leg-9.md`, `receipts/leg-10.md`.

## THREATS
One preparatory L10 call used `inspect_binary_layout` Evidence and was rejected because the graph requires `inspect_artifact` Evidence; it was not counted as the leg. Corrected run used the required Evidence type. Carrier absence is bounded to repo corpus and accessible `/tmp`, not a host-wide search. No config-edit command was issued; operator-config drift and host-wide mutation outside `/tmp` were not independently hashed (npx may use its cache). Both MCP subprocesses exited 0.

## VERDICT
FINDING: L10 required one non-counted wrong-Evidence setup call; final valid-Evidence replay matched the predicted TYPED-REFUSAL class.
