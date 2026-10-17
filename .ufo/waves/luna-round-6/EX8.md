## CLAIM

L8 matched its preregistered `RESULT` prediction: REA 6.5.0 returned typed Evidence for `inspect_with_objdump` on `/usr/bin/jq`.

## METHOD

From `/tmp`, started `npx -y rea-agents@6.5.0 --mcp`, initialized REA 6.5.0, confirmed `tools/list` returned 207 tools, and called `inspect_with_objdump` with `path=/usr/bin/jq`, `operation=file_headers`. The MCP server exited 0 after stdin close. Full provider stdout, stderr, exit code, and stdout SHA-256 are in `receipts/leg-8.md`.

## FINDINGS

Evidence `ev_aa75cc2e36b149a82b41e763b92697efc1e2c432571d14c003e3a7bff0219c2f` records provider command `objdump -f /usr/bin/jq`, exit code 0, complete output and empty stderr. The output identifies `elf64-x86-64`, architecture `i386:x86-64`, and start address `0x0000000000003cf0`. REA reports `output_truncated=false` and `artifact_changed=false`; stdout SHA-256 is `22205280f95a0151fec83144666eab3e5a0ccb2300d0d3cb688b3edd00e6570f`.

## THREATS

The Evidence labels format and objdump version unknown; this was header-only inspection. `artifact_changed=false` establishes no detected change to `/usr/bin/jq`, not host-wide immutability. No operator configuration was edited. A preliminary MCP framing attempt stalled before any tool call and was terminated; the successful JSON-lines MCP run above completed normally.

## VERDICT

CLEAN — L8 produced the predicted `RESULT` class.
