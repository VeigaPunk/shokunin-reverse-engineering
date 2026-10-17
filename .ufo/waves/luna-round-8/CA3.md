## CLAIM
Yes: a wrong or nonexistent tool name can produce a refusal indistinguishable by outcome class alone from the intended 6.5-only tool being rejected. The receipt must bind the refusal to the exact requested name.

## METHOD
Inspected `.ufo/waves/luna-round-8/receipts/leg-1.md:3-11` and listed `.ufo/waves/luna-round-8/receipts` (`ls -la` showed only `leg-1.md`). No MCP probes run.

## FINDINGS
The only receipt records the version command/output; it contains no `tools/call` request. L3–L8 receipts were absent in this snapshot, so their request names and matching responses cannot be checked. For each refusal, capture the byte-exact JSON-RPC request (including `method`, `params.name`, arguments, and `id`) and correlate its response ID/error. Compare `params.name` to the frozen verb for that leg; the refusal text or outcome label alone does not rule out a wrong-name call.

## THREATS
This is a filesystem snapshot, not evidence that an executor actually used a wrong name. The six refusals remain unverifiable until their receipts exist and include the request bytes.

## VERDICT
FINDING: outcome-only refusals are forgeable by wrong-name calls; this snapshot cannot distinguish them because L3–L8 request receipts are missing.
