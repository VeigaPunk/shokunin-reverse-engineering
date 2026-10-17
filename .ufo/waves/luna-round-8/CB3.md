## CLAIM
Every leg-3..8 receipt's request names the exact frozen tool from `P0.md:11` — no wrong-name artifact (hyphen form, misspelling, wrong-verb substitution). Seat CB3, substitution 2.

## METHOD
Extracted each `tools/call` `"name"` and each `Tool <x> not found` echo (`grep -o | uniq -c`) from `receipts/leg-3..8.md` and the RV3 replays; compared against `P0.md:11`. Recomputed SHA-256 of surviving raw stdout (`/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`, `/tmp/luna-round-8-ex7-run/mcp.stdout`) and byte-diffed `leg-3.md:21-22` against raw. Checked hyphen variants and the six names against `receipts/leg-2-tools.txt` (170 names).

## FINDINGS
- L3 `inspect_go_binary` (leg-3.md:5,22); L4 `inspect_rust_binary` (:5,13); L5 `inspect_electron_fuses` (:3,9); L6 `inspect_sqlite_database` (:9,11,18); L7 `search_bytes` (:10,13,21); L8 `inspect_with_objdump` (:8,10,18). Request = echo = prediction, exact, all six.
- Raw L3 stdout hashes `5c682099…a569` = claimed; displayed block leg-3.md:21-22 is byte-identical to raw (623 B, diff IDENTICAL) — the known display defect is absent from the current revision. Raw L7 stdout hashes `866f8b…bb6b` = claimed, echoing `Tool search_bytes not found`; its `open_binary` pre-call is in the 170-name list.
- All six names: 0 matches in leg-2-tools.txt; no hyphenated variants in any of the six receipts. RV3 replays independently name L6/L7/L8 verbs (leg-{6,7,8}-RV3-replay.md:9,10,9).
- Anomaly: `census-pre.txt:97` records leg-3.md 1430 B / `d641e3d3…` and leg-4.md 1233 B / `8f04ac26…`; `MANIFEST.txt:3-4`, `CA6.md:10` and current files all show 1448 B / `1be7e4f9…` and 1200 B / `aa4aa7a3…`. Leg-3/4 mtimes (20:59:03 / 20:58:39) precede census-pre.txt's mtime (21:06:07), so that inventory is not a live 21:06 read; the consistent capture window is (20:57:41, 20:58:39] — the pre-repair epoch. Mechanism unproven; mismatch verified by recomputation.

## THREATS
No leg preserves request-side stdin bytes; raw stdout survives only for L3/L7, so L4–L6/L8 rest on receipt transcription plus the server echo (REA's refusal echoes the requested name). A wrong-name request whose name is also absent still yields TYPED-REFUSAL, so the echo — not the class — is the discriminator; all six echoes equal the predictions. Out of seat: MANIFEST is stale for leg-10 (MANIFEST.txt:10 `c89eea7a…` vs current `6cd389e9…`, mtime 21:14).

## VERDICT
CLEAN — all six request names exact, no wrong-name artifact; annex anomaly: census-pre.txt's L3/L4 inventory is a stale pre-repair snapshot, not the delivered bytes.
