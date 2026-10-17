# HB2 — hex→decimal recompute: r2-firmware-probe, r5-01

## CLAIM
Every hex→decimal conversion in the two assigned entries recomputes correctly. Recomputation of the round's item-2 pair shows the misconversion is on r4u-01's decimal side: 0x1c01dc8 = 29,367,752 and 0x505b000 = 84,258,816 are the genuine `.fwimage` sizes (readelf-verified); r4u-01:41's "(29,358,536 B)" / "(84,242,432 B)" are wrong.

## METHOD
- Strict sweeps `grep -nE '0x[0-9a-fA-F]'` and `grep -oE '0x[0-9a-fA-F]+'|sort|uniq -c` on both files (both git-clean vs HEAD cfc84c2).
- python3 recompute of every literal; little-endian byte-order checks.
- Non-REA live ground truth: `stat`, `readelf -h/-S/-x`, `od -j 18 -N 2`, `head -c 8` on `/usr/lib/firmware/nvidia/610.57.04/*.bin`.
- Cross-read r4u-01:41,49,103 for item 2. No Lane-A outputs read; no REA, no network.

## FINDINGS
1. r2-firmware-probe.md: **zero hex literals** (strict grep rc=1; all `0x` substrings live in `tu10x`/`ga10x` filenames). Its decimals are exact live sizes: 12032=0x2F00, 31744=0x7C00, 29381504=0x1C05380, 84310168=0x5067898 (`stat` verbatim). `NVUCODES`@0 re-confirmed.
2. r5-01-riscv-bypass.md: all literal conversions check out —
   - 0x8000 = 32768 ✓ (":32,768 B", :43; csreg range :26,43);
   - `f3 00`→`b7 00` = LE 243→183 ✓ (:25,43); live `od`@18 on both gsp files: `f3 00` (EM_RISCV=243); b7=183;
   - 0xff00 = 65280 (:76,78,94; no decimal stated; "no ELF can ride it" consistent);
   - disasm :30,64 — 0x1=1, 0x31=49, 0xc=12, 0x14=20, 0x600=1536; reconstructed read address ((1<<49)+1)<<12−0x600 = 0x2000000000000A00 (coherent, as claimed); `ram:04bfa000` = 79,667,200 (no decimal stated).
3. Item-2 reconciliation: readelf shows `.fwimage` size `0000000001c01dc8` (tu10x; next section @0x1c01e08 = 0x40+size exactly — equals r5-01:12's carve length 29,367,752) and `000000000505b000` (ga10x). Correct decimals 29,367,752 and 84,258,816; r4u-01's stated decimals are low by 9,216 (0x2400) and 16,384 (0x4000). Hex side: correct.

## THREATS
- /tmp scratch (patched copies, envelopes) is gone: patch-byte claims verified indirectly (original bytes + arithmetic), not on the patched files themselves.
- sha256 digests not re-hashed (not conversions); firmware mtimes Aug 3, sizes match.
- r2:103 "12 KiB" for 12,032 B is rounded wording (11.75 KiB, 12.03 KB), non-hex.

## VERDICT
CLEAN — assigned files, all conversions correct. Boundary FINDING (item 2): r4u-01:41 decimals misconverted → 29,367,752 / 84,258,816; hex verified.
