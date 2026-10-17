## CLAIM
The two `.fwimage` decimals at `corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md:41` are misconverted; the hex literals are correct. Erratum is warranted; correct decimals are **29,367,752 B** and **84,258,816 B**.

## METHOD
Primary-source pass, Lane A unread until after this draft: (a) located the actual subject blobs at `/usr/lib/firmware/nvidia/610.57.04/`; `sha256sum` on all four matches the doc's recorded sums (:10–13) exactly, so these are the same bytes; (b) `readelf -S` on both GSP wrappers; (c) python `struct` parse of the embedded ELF header at offset 64; (d) python recompute of every hex pair.

## FINDINGS
- Ground truth: `readelf -S gsp_tu10x.bin` → `.fwimage PROGBITS 0000000000000000 00000040 0000000001c01dc8`; `gsp_ga10x.bin` → `000000000505b000`. Hex at :41 verbatim correct; decimals wrong (29,358,536 vs true 29,367,752, Δ+9,216; 84,242,432 vs true 84,258,816, Δ+16,384).
- The file self-contradicts: :47 already states extent ≈29,367,752 B, which I confirmed = e_shoff (29,365,384) + e_shnum (37) × e_shentsize (64) = 0x1c01dc8. Erratum resolves the :41↔:47 tension.
- Every other pair checks: 0x1000 = 4,096 B; 0x400000–0xbc0000 = 8,126,464 B = 7.75 MiB (matches "~8 MiB"); 29.37 MB ✓; inner ELF e_type=2 EXEC, e_machine=243 (RISC-V), entry 0x4009000 ✓; 3/12 `.fwsignature_*` sections ✓; `.fwversion` = 610.57.04 ✓; ucode last-nonzero offset 23 both files ✓; outer 10/19 sections ✓.
- Erratum content adjudication: correct only the two decimals; hex stands. Both Lane A drafts (V2, D2) flag a "conversion-only, source not re-read" threat — that threat is now closed: the erratum should cite the sha256-matched ground-truth `readelf -S` receipt. D2's append-only block is sound; my numbers match V2/D2/H1 exactly.

## THREATS
Assumes on-disk blobs are byte-stable; the sha256 match against :10–13 makes this strong. readelf version on this host was not cross-recorded; section sizes are format-trivial, low risk. "~8 MiB" for 7.75 MiB is loosely rounded but tilde-approximate — not erratum-worthy.

## VERDICT
FINDING: erratum needed — append-only correction to :41 decimals (29,367,752 B / 84,258,816 B); hex correct and now byte-verified against sha256-matched originals; Lane A V2/D2/H1 converged.
