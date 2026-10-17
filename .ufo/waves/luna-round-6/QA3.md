# QA3 — receipt-format audit (5 required fields)

## CLAIM
Every battery receipt (10 lane A `receipts/leg-1..10.md` + 10 lane B `receipts-B/leg-1..10.md`) must carry the 5 required fields: command, full stdout, stderr, exit, stdout sha256. This audit answers whether they do and lists gaps.

## METHOD
Read-only audit, snapshot 2026-10-16T22:02:25Z (lane-B receipts were still landing during it). For each existing receipt: line-anchored label greps plus reading of label/structure lines; small receipts read in full; the two 3 MB receipts (A/leg-2, A/leg-3) inspected via per-line lengths and head/tail slices, never dumped. MANIFEST hash re-checked with `sha256sum`. No receipt modified; my only write is this file.

## FINDINGS
Existing at snapshot: 16/20 receipts — 10 lane A, 6 lane B (legs 1,2,7,8,9,10).
- All 16 carry all 5 fields; 0 missing-field receipts. Lane A evidence: leg-1:1-11, leg-2:1/7/8/11/18, leg-3:3/203/212/219/221, leg-4 (##Command/##Full stdout/##Stderr/Exit code/SHA-256 of complete stdout file), leg-5, leg-6, leg-7:3/12/14/15/17/24, leg-8:3/13/14/16/22, leg-9:1/2/6/10/11, leg-10 (COMMAND/FULL SERVER STDOUT/STDERR/PROCESS EXIT CODE/SERVER STDOUT SHA-256). Lane B: leg-1:6/15/23/29/35, leg-2:1/8/9/12/13, leg-7:7/27/35/43/50, leg-8:6/32/39/47/53, leg-9:6/10/17/23/29/35, leg-10:6/29/37/45/54.
Gaps:
1. MISSING FILES: `receipts-B/leg-3,4,5,6.md` absent at snapshot (concurrent seats). Refreshed 22:02:54Z: leg-4 landed too (17/20); legs 3,5,6 still absent.
2. MANIFEST: `receipts/MANIFEST.txt:1` hashes only leg-1 (verified matching `24bfd90f…`); legs 2-10 have no file-hash manifest, receipts-B none at all.
3. SCOPE NUANCE: A/leg-9's stdout field is the target response frame (`receipts/leg-9.md:2`); whole-process stdout is hashed (`leg-9.md:12`, `1ff84c06…`) but not printed. B/leg-9:10 prints both (1696 B = init 1037 + target 659), so cross-lane comparison is still possible.
4. COSMETIC: label/fence conventions vary ("Full stdout" / "FULL STDOUT" / "Server stdout"; A/leg-2 stdout unfenced; sha256 sometimes listed before stdout). A/leg-6/7/8 and B/leg-7 print two adjacent SHA-256 labels (carrier hash vs stdout hash) — distinguishable by label, conflation risk if quoted alone.

## THREATS
- Live wave: lane-B receipts appeared mid-audit (leg-2, leg-7, leg-8, leg-9, leg-10), so gap 1 may shrink after this snapshot; re-check receipt count before citing it.
- I verified field presence/labels, not byte-completeness of every stdout blob; that would need per-leg re-runs, and lane-A receipts must not seed re-runs.
- Adjacent carrier/stdout hashes could be conflated by a downstream reader.
- Line citations are rounded to label lines; commands above reproduce them.

## VERDICT
FINDING: 16/16 existing receipts carry all 5 fields; gaps are 4 lane-B receipts (legs 3,4,5,6) absent at snapshot, no hash manifest beyond leg-1, and A/leg-9's stdout field not showing whole-process stdout.
