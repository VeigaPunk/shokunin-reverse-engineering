# ScoutMergeThemes — round 52, wave r52-w1 (second-reader assimilation scan)

Verdict: **scan complete. One theme (AVM LE/BE marker provenance). Two candidates admitted narrowly, one rejected. No device-node, padding or ddwrt ground exists in the package.**

Full scan: `.ufo/waves/round-52/w1/ScoutMergeThemes/scan.md`. Status: `.ufo/waves/round-52/w1/ScoutMergeThemes/status.json` (settled). Receipts: `.ufo/waves/round-52/w1/ScoutMergeThemes/receipts/` (15 commands; `receipts.jsonl` holds command, exit, stdout/stderr sha256, UTC start/end).

## Findings

1. **`avm-le-image-genuine-marker` (S212–S214): admit, narrowed.** Not held in the lane. It shows a genuine AVM_LE marker from a clean `-DTARGET_FORMAT=AVM_LE` build and that the round-12 "unreachable" result was a stale-build artefact. It bears on the r50 line-60 claim that the marker is "re-stampable" with "no stock-mksquashfs invocation". Re-measure S212/S213 in lane scratch; re-open S214 at commit `86c23d96`. Renumber S212→S252, S213→S253, S214→S254.
2. **`avm-firmware-image-unblob` (S218, S219, S220, S223): admit only the 1970 stock-reader fingerprint and the NMI/TI negative.** Reject the restated "both formats / ordinary handlers" claims (held in r41 and r50), S216/S217 (lane S125 same directory), and the 9 877-file tally (no held ground to attach it to). S220 is on an unpinned `master` branch and must be re-cited at a commit. Renumber S218→S255, S223→S256.
3. **`unblob-format-matrix` (S122): reject.** Same document as lane S116, already held as `2026-10-26-unblob-format-matrix`.

## Lane facts for the L1 (receipts R1, R10, R13–R15)

- Package: 132 rows S106..S237; 77 knowledge entries (matches `MERGE-REPORT.md`).
- Lane: 158 rows, max S251, next free **S252**.
- **44 of 132 package ids collide numerically** with lane S106..S149 (different documents). 88 are numerically free (S150..S237). Renumber by document.
- `considerthese/` does not exist in the lane.

## Gaps and limits

- No candidate for C1 (device-node law) or C2 (ddwrt FAILED body, padding). Receipts R2–R4 show zero device-node ground and no padding or ddwrt ground beyond held matrix references.
- The admitted rows rest on shokuknow own-work tsv files. Adoption must re-measure them in lane scratch; this scan copied no measurements.
- No cited URL was fetched (per the scan contract).

## Tooling

No tool was installed or updated. Only the lane's disk-guard status was read (read-only). No REA run, no `--data-run`, no corpus/evidence write, no git mutation. Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScoutMergeThemes` was copied into `receipts/` and removed.
