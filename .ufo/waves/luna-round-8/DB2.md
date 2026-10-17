# DB2 — content derivability for legs 6-10

## CLAIM
Every leg 6-10 claim the pending consolidated 6.4.0 symmetry entry needs is derivable from round-8 receipts at HEAD `6e2ee8f`: L6-L8 TYPED-REFUSAL per verb/carrier, L9 six exact-name absences, L10 RESULT, stdout digests reproducing. PR1's L6-L10 rows are stale; MANIFEST/CA6 leg-10 file-hash citations are stale-by-append and need parent refresh.

## METHOD
Read-only: recomputed sha256 of every `text` block in leg-6/7/8.md, their RV3 replays, and leg-10.md (+LF/no-LF); file hashes vs `MANIFEST.txt` and `census-pre.txt`; brute-forced leg-10.md line prefixes against c89eea7a; re-ran leg-9's six `grep -nFw` checks plus exact `analyze`/`inspect_binary_layout` membership on the 170-line leg-2-tools.txt; hashed /tmp survivors (`luna-round-8-leg-6.sqlite`, `kaidoku-luna-round-8-leg10*.stdout`, `luna-round-8-ex7-run/*`). No probes, no tracked-file edits.

## FINDINGS
- L6-L8 + replays fully derivable: all six stdout digests recompute +LF (5bc135e0, c7997ada, 866f8b58, 7481ffaf, 65d740cf ×2); each call returns `-32602` `Tool <name> not found` (`leg-6.md:9-11`; `leg-7.md:9-13`, open_binary success first; `leg-8.md:8-10`); leg-8's 626-byte count checks; carriers match claims (fixture 03c5ec9e hashed now = :4; true 8bc9a73a; jq e8156675; index.db 3701a7e3).
- L7 has raw corroboration: `/tmp/luna-round-8-ex7-run/mcp.stdout` (1075 B) = 866f8b58 exactly; mcp.stderr = 6fbf7ed6 = displayed stderr +LF.
- L9 reproduced independently: 170 lines; six names exit 1, empty stdout (e3b0c442); exact `analyze` also absent (rc=1); `inspect_binary_layout` present (:85) — L10's fallback verb is forced/derivable.
- L10 RESULT derivable: `leg-10.md:7-25` summary view (ev_9befd8a5, jq e8156675); 61450b92 recomputes and equals `/tmp/kaidoku-luna-round-8-leg10-summary.stdout`; 6abdf805 recomputes (analyze→refusal, binary_overview RESULT); :26 tools/list 23e94d0b = `...leg10.stdout` (2,127,950 B).
- leg-10.md file hash: current 6cd389e9 (40,401 B); MANIFEST c89eea7a = exact first-59-lines+LF prefix (brute-forced) → append-only fallback section (:61-84; mtime 21:14:02 > MANIFEST 21:02:41). `MANIFEST.txt:10` and `CA6.md:10` cite pre-append bytes.
- census-pre.txt stale for leg-3 (d641e3d3/1430 B) and leg-4 (8f04ac26/1233 B), omits leg-10; its leg-6-9 rows agree everywhere. FB2.md:16's b2012fcf = sha256(leg-10.md:75 + "\n```\n") — boundary artifact, not block content (9e2726cb); block self-labels non-authoritative.
- Stale lane-A L6-L10 rows (superseded, cf. VB6.md:12): `PR1.md:15-19` Pending; PS2:14; PS3:15-19; RE2:12-14; RE3:11; RE5:11; RE6:25; XG1:11-13; CA2:15; CA7:14; CA8:14; CA10:13; RV8:5.

## THREATS
Legs 6/8/replays are display↔claim self-consistency only (no raw survivor; exits/process sweeps unverifiable now); leg-9 is derived output (6.4.0 via leg-2). EX receipts say `--mcp` where P0's method says `mcp`; class invariance across forms is indirect. census/MANIFEST mtime ordering unresolvable read-only.

## VERDICT
FINDING: legs 6-10 fully receipt-derivable; PR1 L6-L10 rows stale; MANIFEST/CA6 leg-10 hash citations stale-by-append (parent refresh).
