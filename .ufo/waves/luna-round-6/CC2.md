# CC2 — compare leg 2 (lane A vs lane B)

## CLAIM
Byte-compare `receipts/leg-2.md` (lane A) vs `receipts-B/leg-2.md` (lane B) for L2: count and first-5 names identical? stdout identical? classes identical? Report PASS/DIVERGE.

## METHOD
Both receipts present by 19:01 (`receipts-B/leg-2.md` filed by BB2); read-only compare, no probe re-run (CC1 precedent). From each receipt's bytes I extracted the embedded raw stdout (after the `FULL STDOUT (raw REA MCP server stdout):` marker, through the separating newline before `STDERR`); recomputed sha256 — both `38d44bf8…` = each receipt's claimed `STDOUT SHA-256`; parsed the two JSON-RPC records (id 1 initialize, id 2 `tools/list`); extracted count, first-5, last tool name from the parsed payloads; `cmp` on the two extracted payload files; `sha256sum` of receipt files (`receipts/leg-2.md` → `df232a1d…c7e4`; `receipts-B/leg-2.md` → `96777c3f…ffd4`); cross-checked B's scratch `/tmp/rea-bb2/stdout.raw`.

## FINDINGS
- **count identical: 207 = 207** (`receipts/leg-2.md:6`, `receipts-B/leg-2.md:7`; independently re-parsed from both payloads).
- **first-5 names identical:** `annotate_native_function`, `inspect_native_load_image`, `inspect_native_data_type`, `inspect_native_instruction`, `resolve_native_call_targets`; last tool `inspect_address_context` both.
- **stdout byte-identical:** both payloads 3,089,024 bytes, sha256 `38d44bf8ee0944315a1d50d3e3acec1401be50efe7090ac22ec8498e853d4129`; `cmp A_payload.bin B_payload.bin` → identical; equals `stdout.raw` scratch hash. Server `rea` 6.5.0, protocol `2025-03-26` both; exit 0 both.
- **classes identical: YES (derived).** Neither receipt declares a class label; observed 207 = frozen L2 prediction → RESULT for both.
- **Token set unchanged:** `npx -y rea-agents@6.5.0 mcp` both; both cwds under /tmp; caches differ (`…round-6-…` vs `…round-6B-…`); clientInfo labels differ (EX2/BB2 probe names) — no effect on measured bytes.
- stderr differs by environment: A carries npm cold-cache notices, B is empty after prewarm.

## THREATS
Same host/node/npx and same registry pin across lanes — byte-identity proves listing determinism, not package provenance. Leg-2 receipts are not in `receipts/MANIFEST.txt` (only leg-1 listed), so receipt-file hashes are externally unanchored. A's COUNT summary adds `"nextCursor":null`, B omits it; the raw payload carries no such field — semantic only (absent ≡ null). No re-run by CC2; my re-extraction from raw bytes mitigates trusting the compose scripts, but both could share an extraction idiom.

## VERDICT
CLEAN — PASS: L2 count 207, first-5 names, and full 3,089,024-byte stdout (sha256 `38d44bf8…`) identical across lanes; RESULT class identical.
