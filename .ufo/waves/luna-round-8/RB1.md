# RB1 — independent final scorer (raw receipts, 6e2ee8f)

## CLAIM
Independent scoring of all 10 legs of the frozen 6.4.0 battery from raw receipts at HEAD 6e2ee8f; N/10 and diff vs CA6's 10/10.

## METHOD
Read `P0.md` predictions first, then receipts `leg-1..10.md`, `leg-2-tools.txt`, `MANIFEST.txt`, `census-pre.txt`. Recomputed every claimed stdout SHA-256 from displayed blocks (own Python), parsed `leg-2.md:12` raw tools/list JSON, ran my own `grep -nFw` for the six names, and cross-checked every surviving /tmp original (RV1 leg1/leg2, leg-3-mcp, ex7 mcp, leg10 + summary, sqlite carrier) and carriers (`/usr/bin/true`, `/usr/bin/jq`, Signal size). No probes, no writes.

## FINDINGS
- L1 MATCH: stdout `6.4.0\n` → claimed `3754366908ac`; /tmp original byte-identical; exit 0 (`leg-1.md:7`).
- L2 MATCH: raw parse = 170 tools, 170 unique; order identical to `leg-2-tools.txt`; full stdout recomputes to `0bbe6bc7`; /tmp original identical.
- L3–L8 MATCH: each call = `-32602` `Tool <name> not found` (TYPED-REFUSAL) for inspect_go_binary, inspect_rust_binary, inspect_electron_fuses, inspect_sqlite_database, search_bytes, inspect_with_objdump; every displayed stdout block recomputes to its claim (`5c682099`, `0fbd3bd0`, `adfb7370`, `5bc135e0`, `866f8b58`, `65d740cf`); /tmp originals for L3 (623B) and L7 (1075B/384B) match.
- L9 MATCH: my grep rc=1/empty ×6; six names also absent in the parsed raw array.
- L10 MATCH: `inspect_binary_layout`(jq) → RESULT (coverage 202/202; evidence digest = actual jq sha `e8156675`); block hash `61450b92` recomputes; /tmp summary and 2.1MB full-run (`23e94d0b`) originals match.
- **Score: RB1 10/10.** Diff vs CA6 (10/10): score identical; drifts CA6 missed — `leg-10.md` was rewritten after MANIFEST/CA6 (`c89eea7a` → `6cd389e9`, mtime 21:14 > CA6 21:07), so MANIFEST's leg-10 hash is stale (content still verifies); `leg-3.md` display defect is repaired now (block hashes to claim) while census-pre retains pre-repair leg-3 `d641e3d3` / leg-4 `8f04ac26` snapshots; the other 9 receipt hashes match MANIFEST.

## THREATS
Receipts prove stored bytes, not re-execution; /tmp mtimes + logger lines are process-level support only. Stderr displays for L1 ("empty") and L3 (npm-notice `527d12b4`) do not match their runs' /tmp captures (209B notice vs 0B) — display-only; stdout chains intact. Protocol mix (L3–L5, L8 = 2024-11-05 vs P0's 2025-03-26) — predictions unaffected. L10's fallback block is an "incomplete transcription; not raw"; byte-identity is asserted, though L10 verifies via primary + EX10 hashes. MANIFEST drift means receipt hash-immutability is scoped to current state.

## VERDICT
FINDING: 10/10 confirmed independently — score agrees with CA6, but MANIFEST/CA6's leg-10 hash is stale (file rewritten post-CA6; content still verifies) and leg-3/leg-4 receipts changed after the census snapshot.
