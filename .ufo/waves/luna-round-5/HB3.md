## CLAIM
Independent HB3 unit audit: verify r4u-01's disputed `.fwimage` hex→decimal sizes against ground truth, and audit MB (10^6) vs MiB (2^20) usage in `2026-10-13-r4u-01-firmware-deep.md`, `2026-10-13-r4-12-godot-arm64-scale.md`, `2026-10-13-r4-14-libsignal.md`.

## METHOD
Read-only; all three paths == HEAD `cfc84c2` (`git diff HEAD --stat` on them → empty). Recomputed every cited size with python3. Ground truth beyond arithmetic: the four nvidia blobs are on host and `sha256sum` matches r4u-01:10-13 byte-exactly, so ran stock `readelf -SW` (non-REA fallback reader, PROVINCE.md:13) on both GSP blobs. No REA/MCP/network; no tracked-file writes.

## FINDINGS
- **r4u-01:41 wrong — confirmed on the shipped artifacts, not just arithmetic.** readelf: `.fwimage` size `1c01dc8` on tu10x (10 sections, 3 `.fwsignature_*`) and `505b000` on ga10x (19 sections, 12 sigs) → correct **29,367,752 B / 84,258,816 B**. Recorded 29,358,536 / 84,242,432 are wrong (diffs 9,216 / 16,384; the wrong values equal 0x1bff9c8 / 0x5057000). Cross-checks: :49 `e_shoff`+37×64 = 29,367,752; file totals 29,381,504 / 84,310,168 = final section end + section-header table exactly (0x1c05100+640; 0x50673d8+19×64).
- **MB/MiB convention clean in all three files**; MB=10^6, MiB=2^20, never mixed. r4-12 is the explicit exemplar: 91,662,336 B = 91.6 MB (truncation; round 91.7) = 87.4 MiB (:8/:19); 69,538,816 B = 69.5 MB = ~66.3 MiB (:26/:123); raw section sizes 91,661,312 + 1,024 B PE headers = 91,662,336 exactly; "~17.4 M insns" = /4 ✓.
- r4u-01 "~29.37 MB" (:47,:49) = 29.368 decimal MB ✓; "~8 MiB" (:71-73) = 7.75 MiB start-span / 8.00 MiB covered through 0xc00000 — fair either way. r4-14 "25 MB"/"24.9 MB" (:5,:7,:41,:47) = 24,944,200 B decimal ✓ (:9); 1.7× ratio = 1.7154 ✓ (:57); exact anchors 741×24 = 0x4578 ✓ (:17,:74), 0x230 = 560 < 600 ✓ (:25,:29).
- Concordant with Lane A H1/H2/H4/V2 (read post-draft); this pass adds the artifact-level evidence R2:8 flagged missing.

## THREATS
r4-12/r4-14 targets absent from host (no Godot exe, `/usr/lib/signal-desktop` gone) → those conversions verified arithmetically + internally, not re-measured. Entropy/gzip/offset claims not re-run. GB/GiB tokens ("2.36 GB", "6–8 G") lack byte counts — unverifiable. "HB3" has no corpus referent (seat ID). Errata unapplied by this seat.

## VERDICT
FINDING: r4u-01:41 decimals confirmed wrong against sha256-identical shipped blobs — correct 29,367,752/84,258,816 B; MB/MiB labeling clean across all three files.
