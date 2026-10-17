# VB1 — receipt verifier 1–2

## CLAIM
Recomputed: (a) sha256 of every stdout block in receipts/leg-1.md + leg-2.md; (b) L1 `--version` stdout = `6.4.0` exact; (c) L2 tools count = 170.

## METHOD
Read-only, no live probes. Extracted each ```text stdout block from leg-1.md (L6–L8) and leg-2.md (L11–L14) via python3 hashlib, re-hashed; compared byte-level to surviving raw captures /tmp/kaidoku-luna-round8-rv1/leg{1,2}.stdout; re-parsed leg2.stdout JSON-RPC lines, recounted tools, diffed names vs leg-2-tools.txt; recomputed MANIFEST self-hashes for both md files.

## FINDINGS
- leg-1.md block = 6 B `6.4.0\n`, sha256 `3754366908…bcafd` = claimed (L11); byte-identical to raw leg1.stdout. L1 = `6.4.0` exact, single line. leg-1.md contains exactly one 64-hex string (the claim).
- leg-2.md block = 1,955,257 B, sha256 `0bbe6bc7…0279` = claimed (L17); byte-identical to raw leg2.stdout. Hash covers the trailing newline (no-NL variant `3ed152ac…` ≠ claim — consistent with whole-file capture hashing). L17 is the only hash claim line; the 189 other 64-hex strings sit inside captured tool-schema JSON (dummy examples).
- L2 from raw stdout: 2 JSONL responses; initialize serverInfo `{rea, 6.4.0}`; tools/list id=2 → exactly 170 tools, 170 unique names; first5 matches leg-2.md L9 verbatim; protocol `2025-03-26` matches. leg-2-tools.txt: 170 lines, order- AND set-identical to raw names.
- MANIFEST self-hashes recompute: leg-1.md `af959f64…`, leg-2.md `f298e8f1…`.
- Non-blocking discrepancy (outside assigned checks): leg-1.md L9 claims stderr empty, but /tmp/kaidoku-luna-round8-rv1/leg1.stderr = 209 B npm notice ("npm notice New major version of npm available! 11.20.0 -> 12.2.0"). Environmental noise; stdout hash/L1/L2 unaffected. leg2.stderr = 0 B, matching its empty-stderr claim.

## THREATS
- Provenance ordering: leg-1.md mtime 20:52:40 predates leg1.stdout 20:53:06, so the surviving /tmp capture cannot independently attest the receipt — only content identity is verified (which holds exactly). leg-2 ordering is consistent (capture 20:53:37, md 20:55:02).
- Exit codes 0 for legs 1–2 are not recomputable (no .exit files in the rv1 dir); only consistency-checked (both responses complete, stderr empty/notice-only).
- Same-minute mtimes could mask a same-second rewrite of /tmp artifacts; content equality is the strongest available evidence absent an authorized live re-run.

## VERDICT
CLEAN — both stdout hashes recompute exactly (bytes == raw captures == claims), L1=6.4.0 exact, L2 count=170; one cosmetic stderr-claim discrepancy in leg-1.md reported above.
