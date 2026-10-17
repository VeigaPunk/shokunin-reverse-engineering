# DB2 — r4u-01 erratum draft (2nd opinion, from VB2.md)

## CLAIM

Append-only errata block correcting the two misconverted `.fwimage` decimal byte counts at `corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md:41`, drafted from `VB2.md`; spot-checks confirm the hex literals are correct and both decimals wrong.

## METHOD

Read `VB2.md` (appeared 16:39) as the designated source only. Spot-checked its load-bearing claims against primaries, no full re-pass: `git show HEAD:corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md` (:10-13, :41, :49, :114-119); `sha256sum` of all four subject blobs under `/usr/lib/firmware/nvidia/610.57.04/`; `readelf -S` (GNU Binutils 2.47) on both GSP blobs; `printf '%d' 0x1c01dc8 0x505b000`. Read-only; no REA probes, MCP, or network; no tracked-file writes.

## FINDINGS

- Recheck: `0x1c01dc8` = 29,367,752; `0x505b000` = 84,258,816 (matches VB2). :41 records 29,358,536 / 84,242,432; deltas +9,216 / +16,384.
- `readelf -S` ground truth: `.fwimage` size fields `0000000001c01dc8` / `000000000505b000` — the hex at :41 stands; all four blob `sha256sum`s match :10-13.
- Pointer fix: VB2 cites ":47" for the `≈29,367,752 B` extent statement — `grep -n` places it at **:49**; VB2's ":41↔:47 tension" should read :41↔:49.
- Append boundary: file is 119 lines / 19,470 B, ending :119 "…remain true as written." New errata appends after it. The census `add()` check wants the appended tail to carry `0x1c01dc8`, `29,367,752`, `0x505b000`, `84,258,816` — the block below carries all four.

Draft append (integration text):

```markdown
## Errata (luna-round-5, 2026-10-16, append-only)

- The `.fwimage` decimal byte counts in the GSP-wrapper candidate above are
  misconverted; the hex literals are correct. `0x1c01dc8` = **29,367,752 B**
  (gsp_tu10x, not 29,358,536 B) and `0x505b000` = **84,258,816 B**
  (gsp_ga10x, not 84,242,432 B); these values supersede the earlier decimals.
  Ground truth: `readelf -S` (GNU Binutils 2.47) on the `sha256sum`-matched
  subjects recorded at the top of this file. The tu10x extent stated later
  (`29,365,384` + 37 × 64 = `29,367,752 B`) is consistent. All other recorded
  numbers stand.
```

## THREATS

VB2 ran the live-blob pass; I confirmed blob identity via sha256 and re-read only `.fwimage` rows. Heading wording is the integrator's choice; the testable parts are the four tokens plus append-only. Disclosure: orientation reads before VB2.md existed had shown me Lane A V2/D2; numbers agree, but this draft rests on VB2.md plus my checks.

## VERDICT

FINDING: erratum ready for integration; correct VB2's :47 pointer to :49.
