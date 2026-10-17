# HB1 — hex→decimal recompute of r4u-01 (independent)

## CLAIM
Recompute every hex→decimal conversion in `corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md`; adjudicate debt item 2 (0x1c01dc8 / 0x505b000 size decimals).

## METHOD
Regex-extracted every `0x…` literal in the file; exact integer conversion (`int(x,16)`). Ground truth for paired decimals: local read-only `readelf -S`/`-h` on `/usr/lib/firmware/nvidia/610.57.04/*.bin` (sha256 of all four blobs match r4u-01 :10–13 — identical artifacts), plus re-running the file's own carve (`dd skip=64 count=766595`) and reading ELF header fields from raw bytes. No REA probes, no MCP, no network, no tracked-file writes; drafted from primary sources only (no Lane A outputs read).

## FINDINGS
Full hex census: 0x0=0; 0x40=64 ✓ (skip=64); 0x1000=4096 ✓; 0x3c0000=3,932,160 (no decimal claimed); 0x400000=4,194,304; 0x4009000=67,145,728 (entry, no decimal claimed); 0xbc0000=12,320,768; 0x1c01dc8=29,367,752; 0x505b000=84,258,816.

Debt item 2 CONFIRMED — both :41 decimals are wrong:
- 0x1c01dc8 = **29,367,752** B; file says 29,358,536. `readelf -S` on gsp_tu10x.bin (sha256 d157e3b7… matches :12) shows `.fwimage` size field `0000000001c01dc8`. Internal corroboration: :49 gives "true extent ≈29,367,752 B" — verified exactly (e_shoff 29,365,384 + 37×64 = 29,367,752) — so :41 is the erratum.
- 0x505b000 = **84,258,816** B; file says 84,242,432. `readelf -S` on gsp_ga10x.bin (sha256 c0156954… matches :13) shows size field `000000000505b000`. Delta 16,384 = 0x4000 (consistent with hex 'b' misread as '7': 0x5057000 = 84,242,432).
- :103 restates both hex values with no decimals — no second copy of the error.

0x400000–0xbc0000 span = 8,126,464 B = 7.75 MiB; "~8 MiB" (:71, :73) is a round-up — imprecise, not wrong.

Suggested append-only erratum: ":41 .fwimage decimals corrected: 0x1c01dc8 = 29,367,752 B (not 29,358,536); 0x505b000 = 84,258,816 B (not 84,242,432). All other values stand."

## THREATS
- Ground truth used local readelf on the shipped blob (read-only, non-REA). If judged out of bounds, the arithmetic alone yields the same two corrections, with :49 as internal corroboration.
- Decimal-only claims (450,624; 19,669,056; 155,648; 759,230; 766,595; 16,945,176) have no hex counterpart — outside recompute scope; carve size 766,595 reproduced exactly.
- Adjacent, not a conversion: :25 "24 nonzero bytes" / ga10x "(range scan [(0,256)]…)" — both ucodes actually hold 19 nonzero bytes, all within offsets 0–23 (24 is the header length). Wording imprecision only.

## VERDICT
FINDING: r4u-01 :41 decimals are misconverted as alleged — correct 0x1c01dc8 = 29,367,752 B, 0x505b000 = 84,258,816 B (blob-verified); every other hex→decimal pair in r4u-01 recomputes clean.
