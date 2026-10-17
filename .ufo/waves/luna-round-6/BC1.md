## CLAIM
Independent recount of the lane-B score from `receipts-B/leg-1..10.md` against the frozen register (L1 6.5.0 exact, L2 207 exact, L3–L8 RESULT class, L9–L10 TYPED-REFUSAL class): my N = **10/10 matches**, 0 ERROR-UNEXPECTED. Reproduces ZB1's headline.

## METHOD
Read-only at HEAD `f0e8cde`; no probes, no tracked-file edits. Read all ten receipts-B plus `MANIFEST.txt`; ran `sha256sum -c` over a reformatted manifest; re-parsed leg-2's embedded 3,087,986-byte `tools/list` frame and counted tools in-process; recomputed declared digests from embedded fenced/marker-delimited blocks; hashed the literal `6.5.0\n`; grepped lane-A receipts for the digests ZB1 cites; read `ZB1.md` only after fixing my own table.

## FINDINGS
- L1 exact: stdout `6.5.0`, exit 0; declared `3eb8e06c…` = sha256 of `6.5.0\n` — ✓
- L2 exact: my parse of the embedded frame gives exactly 207 tools, 207 unique names, no duplicates; the reconstructed init+list bytes hash to the declared `38d44bf8…` — ✓
- L3–L8 RESULT: typed Evidence payloads, no `error` key, exit 0 each (L7 hit at `file_offset` 0, complete; L8's frozen `/usr/bin/jq` run byte-identical to lane A) — ✓
- L9–L10 TYPED-REFUSAL: structured refusals (`invalid_request`/`invalid_format`; `capability_unavailable`, WABT absent) — ✓
- Manifest: all ten receipt files verify (`sha256sum -c` rc=0), incl. leg-3 = `9785585…` → CC3's 19:07:53 overwrite was byte-restored, so ZB1's "displaced versions unrecoverable" is contradicted.
Diff vs ZB1: same 10/10, same per-leg classes, same L10 contingency. Precision diffs: ZB1's "6 byte-identical" borrows CC3/CC9 `/tmp` re-runs for L3/L9 — receipt-to-receipt byte identity holds only for L1, L2, L7, L10; leg-9's B digest `2a20c456` covers a 772-byte pretty-printed transcript (lane A frame `2b596b31`), so B's L9 evidence is class-level.

## THREATS
Compare-seat overwrites left legs 3, 7, 8, 9 authored by CC3/CC7/CC8/BB9: leg coverage and internal hashes verify, but original BB7/BB8 receipts are absent (BB3's was restored). L10's frozen tool was never reached. `CB1.md` shows copying lane-A stdout yields hash-consistent receipts-B, so hash agreement ≠ execution. Single host/node/npx cache is common mode; MANIFEST is self-authored (19:06) and my only file-level anchor. Exact-value checks rest on my own parsing, not seats' assertions.

## VERDICT
CLEAN — lane-B recount 10/10; ZB1's score reproduced; its leg-3 "unrecoverable" threat is stale.
