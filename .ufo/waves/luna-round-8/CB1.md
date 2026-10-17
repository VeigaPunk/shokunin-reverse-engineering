## CLAIM
Independent forgery screen on the final receipt set: do the receipts' hash claims and cited artifacts reproduce offline, or is any receipt fabricated?

## METHOD
Read-only; no probe, no tracked-file write. Recomputed sha256 of leg-1..10.md vs MANIFEST.txt; hashed every displayed stdout block (block text + trailing LF) against its in-file claim; hashed surviving /tmp artifacts; recomputed census-pre.txt's self-hash and 13 fingerprints. Re-ran leg-9's six greps; re-derived the leg-2 tool list from `leg-2.md` and from the raw /tmp 6.4.0 session; stat+sha256sum on carriers `/usr/bin/jq`, `/usr/bin/true`, `/usr/lib/signal-desktop/signal-desktop`; read-only schema/row query of the leg-6 fixture.

## FINDINGS
- MANIFEST: legs 1–9 recompute byte-exact. `leg-10.md` = `6cd389e9…` ≠ claimed `c89eea7a…`; `head -n 59` (27,655 B) hashes to `c89eea7a` exactly → 21:14 append after MANIFEST's 21:02, not a false hash.
- All 14 display-layer stdout claims recompute under one convention: L1 `37543669`; L2 `0bbe6bc7` (1,955,257 B); L3 `5c682099`; L4 `0fbd3bd0`; L5 `adfb7370`; L6 `5bc135e0`; L7 `866f8b58`; L8 `65d740cf` (its declared 626 B matches); L10 `61450b92` and `6abdf805`; L9's `e3b0c44` is the empty-output constant.
- leg-3 "KNOWN DEFECT" REFUTED: its displayed block hashes to the claimed `5c682099`, identical to `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B). Hashing without the trailing LF (622 B → `225d67cc`) explains the earlier claim; no display corruption needs repair. Its "incomplete transcription" copy at `leg-10.md:73-75` is correctly labelled (11,588 B, no match).
- /tmp corroboration: `leg10.stdout` `23e94d0b` (cited `leg-10.md:26`) holds a 6.4.0 `tools/list` of exactly 170 names, order-identical to `leg-2-tools.txt`, plus `inspect_binary_layout` evidence; `leg10-summary.stdout` `61450b92`.
- Carriers verify: jq 30,800 B `e8156675`; true 43,320 B `8bc9a73a`; signal-desktop 223,513,856 B `f7a9b441`; fixture 8,192 B `03c5ec9e` with the stated schema and row.
- Predictions corroborated: 6.4.0 in all nine session receipts; 170 unique names from two independent sessions; six refusals exactly once each (`-32602`), none present in the raw artifact or 6.4.0 CLI help; L10 RESULT bound to jq.
- Census drift: `128006b1` recomputes and 11/13 fingerprints match, but `leg-3.md` (1430→1448 B) and `leg-4.md` (1233→1200 B) were rewritten after the ~20:57 census. MANIFEST also omits the three `-RV3-replay.md` files and census-pre.txt.

## THREATS
Hashes prove content identity, not execution, and no pre-round digest exists, so manufacture before freeze cannot be excluded. L4–L7 have no surviving raw artifact, resting on display-layer hashes alone. Leg-3/leg-4 pre-edit text is unrecoverable.

## VERDICT
FINDING: no fabricated receipt detected; residual defects are staleness only — MANIFEST stale for leg-10, census-pre stale for leg-3/leg-4, and the leg-3 display-corruption claim refuted.
