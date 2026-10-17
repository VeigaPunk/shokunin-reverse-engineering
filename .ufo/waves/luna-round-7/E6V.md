## CLAIM
Leg-8 supports a RESULT-class observation for `inspect_with_objdump` on the pinned `/usr/bin/jq` carrier; it does not establish behavior for other objdump operations or carriers.

## METHOD
Read-only comparison of `receipts/leg-8.md`, `receipts-B/leg-8.md`, and `SC5.md`. No REA/MCP calls or live probes.

## FINDINGS
- Lane A records `npx -y rea-agents@6.5.0 --mcp` and `inspect_with_objdump` `{path:/usr/bin/jq, operation:file_headers}`; the receipt reports carrier SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` (`receipts/leg-8.md:3-13`). The captured `objdump -f` result is complete, exit 0, not truncated, and reports ELF x86-64, flags `0x150`, start `0x3cf0`, `artifact_changed:false` (`:12,19`). SC5 independently records `/usr/bin/jq` as ELF with the same hash (`SC5.md:9-10`).
- Lane B's primary run used a different carrier (`/home/vgpnk/.local/bin/jq`, SHA-256 `b1c22172…`); its distinct output is not evidence of drift for `/usr/bin/jq` (`receipts-B/leg-8.md:6-8,16-29`). Its later compare run explicitly used `/usr/bin/jq` and reports the same Evidence ID, subject digest, and raw objdump output as lane A; a repeat had the same captured stdout hash (`:41-55`).
- Limitations are explicit: executable version/support remain unknown; the header-only calls do not cover other operations (`receipts/leg-8.md:19`; `receipts-B/leg-8.md:34,47`).

## THREATS
This verifies the recorded receipts, not the historical execution independently. Lane B's primary carrier differs; only its compare run corroborates the pinned carrier. Recorded pre/post hashes cannot prove exact bytes consumed during execution (`receipts/leg-8.md:19`).

## VERDICT
CLEAN — the pinned-carrier receipt supports the leg-8 RESULT claim; carrier and operation scope remain bounded as stated.
