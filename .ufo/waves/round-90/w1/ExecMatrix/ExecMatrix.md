# Tamper matrix — R90-C1 class T5-chain-szcpr-wrong-later (ExecMatrix-5)

Round-90 wave-1 executor seat build of the frozen matrix: four pinned
carriers × interior first-segment `b_info` block indices (1..n-2) × in-range
sampled directions (stored − 7 on every interior index, stored ± 7 on every
sampled index; every tamper delta that leaves 0 < value ≤ sz_unc), plus the
two out-of-class shapes (last block before the stop × both directions; libz
interior), with full recovery arms per cell and every refusal kept verbatim.

## Ground rules re-derived

- Carrier sources (pins verified, sha256): jq `e8156675…7806`, xxd
  `7b1e5d0c…e65`, libz `6c78c5e5…ca9`, dinit `0bd49c8d…115`; UPX pin
  `cf2f6e7c…969` verified before every matrix pass (`upx --version` → `upx
  5.2.0`, same binary hash as the claims.json pin).
- B_info layout per carrier (block offset, sz_unc, sz_cpr):
  - `jq:` `[[576, 904, 252], [840, 5408, 1651], [2503, 9561, 4758], [7273, 5528, 2626], [9911, 1184, 174]]` — l_info `556`, b0 `576`,
    ph_off `14000`, u_len `30800`.
  - `libz:` `[[9304, 680, 201], [9517, 63157, 33574], [43103, 23584, 17012]]` — l_info `9284`, b0 `9304`,
    ph_off `65544`, u_len `108560`.
  - `xxd:` `[[576, 904, 249], [837, 2856, 950], [1799, 21717, 11492], [13303, 4528, 2140], [15455, 784, 163]]` — l_info `556`, b0 `576`,
    ph_off `19524`, u_len `38928`.
  - `dinit:` `[[576, 736, 226], [814, 592, 202], [1028, 575549, 265172], [266212, 230752, 82125], [348349, 27304, 4313]]` — l_info `556`, b0 `576`,
    ph_off `357748`, u_len `851288`.

## Matrix — 20 in-class cells, 18 recovered, 2 leave-alone, 0 refused

All cells are `upx -t` → `Exception: compressed data violation` (rc 1)
before repair (verbatim `upx:` line held in each cell receipt).

| carrier | index | delta | stored | value | r89 rc/chg | r90 path | verdict |
|---|---|---|---|---|---|---|---|
| jq | 1 | -7 | 1651 | 1644 | 0/False | back-point d=+7 | recovered=True |
| jq | 1 | +7 | 1651 | 1658 | 0/False | back-point d=-7 | recovered=True |
| jq | 2 | -7 | 4758 | 4751 | 0/False | back-point d=+7 | recovered=True |
| jq | 2 | +7 | 4758 | 4765 | 0/False | back-point d=-7 | recovered=True |
| jq | 3 | -7 | 2626 | 2619 | 0/False | back-point d=+7 | recovered=True |
| jq | 3 | +7 | 2626 | 2633 | 0/False | back-point d=-7 | recovered=True |
| xxd | 1 | -7 | 950 | 943 | 0/False | back-point d=+7 | recovered=True |
| xxd | 1 | +7 | 950 | 957 | 0/False | back-point d=-7 | recovered=True |
| xxd | 2 | -7 | 11492 | 11485 | 0/False | back-point d=+7 | recovered=True |
| xxd | 2 | +7 | 11492 | 11499 | 0/False | back-point d=-7 | recovered=True |
| xxd | 3 | -7 | 2140 | 2133 | 0/False | back-point d=+7 | recovered=True |
| xxd | 3 | +7 | 2140 | 2147 | 0/False | back-point d=-7 | recovered=True |
| dinit | 1 | -7 | 202 | 195 | 0/True | back-point d=+7 | recovered=True |
| dinit | 1 | +7 | 202 | 209 | 0/True | back-point d=-7 | recovered=True |
| dinit | 2 | -7 | 265172 | 265165 | 0/False | back-point d=+7 | recovered=True |
| dinit | 2 | +7 | 265172 | 265179 | 0/False | back-point d=-7 | recovered=True |
| dinit | 3 | -7 | 82125 | 82118 | 0/False | back-point d=+7 | recovered=True |
| dinit | 3 | +7 | 82125 | 82132 | 0/False | back-point d=-7 | recovered=True |

R90-derived for every signature cell took the single candidate its successor
hypothesis allowed: `derived = successor position − 12 − block offset`,
`candidates=1` on every row, and the stored chain account was strictly
smaller (`stored_accounted < uncompressed_accounted` everywhere).

## Two red leaves: full-arms out-of-class

| carrier | shape | delta | stored | value | rc | bytes vs intact | record |
|---|---|---|---|---|---|---|---|
| libz | interior | -7 | 33574 | 33567 | 0 | equal=False, test=False, unpack=False |
| libz | interior | +7 | 33574 | 33581 | 0 | equal=False, test=False, unpack=False |

## libz interior cells (out of class, leave-alone)

The libz cells leave the file byte-identical (r90 rc 0, class `,intact`),
- i=1 d=-7: r89 rc 0 no change; r90 rc 0 output byte-identical,
  upx -t rc False (still `violation`), unpack_pin False — exactly the
  declared `u_len`-gap leave-alone (stored chain accounts 98,592 of 108,560;
  exact-total rule rejects every candidate).
- i=1 d=+7: r89 rc 0 no change; r90 rc 0 output byte-identical,
  upx -t rc False (still `violation`), unpack_pin False — exactly the
  declared `u_len`-gap leave-alone (stored chain accounts 98,592 of 108,560;
  exact-total rule rejects every candidate).

## Out-of-class: last-block-before-stop (all 4 carriers, both directions)

| carrier | d | stored | value | rc | output vs tampered | class stdout |
|---|---|---|---|---|---|---|
| jq | -7 | 174 | 167 | 0 | **5 bytes CHANGED (anchor repair, see below)** | `{"break_index": null, "class": "anchor", "delta": 0, "derived_sz_cpr": 252, "stored_accoun…` |
| jq | +7 | 174 | 181 | 0 | unchanged | `{"break_index": null, "class": "intact", "delta": 0, "derived_sz_cpr": 252, "stored_accoun…` |
| xxd | -7 | 163 | 156 | 0 | unchanged | `{"break_index": null, "class": "intact", "delta": 0, "derived_sz_cpr": 249, "stored_accoun…` |
| xxd | +7 | 163 | 170 | 0 | unchanged | `{"break_index": null, "class": "intact", "delta": 0, "derived_sz_cpr": 249, "stored_accoun…` |
| libz | -7 | 17012 | 17005 | 0 | **5 bytes CHANGED (anchor repair, see below)** | `{"break_index": null, "class": "anchor", "delta": 0, "derived_sz_cpr": 201, "stored_accoun…` |
| libz | +7 | 17012 | 17019 | 0 | unchanged | `{"break_index": null, "class": "intact", "delta": 0, "derived_sz_cpr": 201, "stored_accoun…` |
| dinit | -7 | 4313 | 4306 | 0 | unchanged | `{"break_index": null, "class": "intact", "delta": 0, "derived_sz_cpr": 226, "stored_accoun…` |
| dinit | +7 | 4313 | 4320 | 0 | unchanged | `{"break_index": null, "class": "intact", "delta": 0, "derived_sz_cpr": 226, "stored_accoun…` |

Verbatim `upx -t` on a red leave-alone cell (jq last d=−7, val 167):
`upx: …: Exception: compressed data violation` rc 1 (same line for all red
cells; full text in the receipts).

### Measured: 2 red last-block cells the repair does NOT leave byte-identical

- `jq` last d=−7 (val 167) and `libz` last d=−7 (val 17005): the round-90
  tool `upx-break-repair.py` reclassifies these as `anchor` (class `anchor`,
  `restored` bytes) and treats the whole file like the round-87 magic class,
  rewriting the header anchor — 5 bytes total at file offsets `[9915,
  10094..10097]` (jq) / `[43107, 60124..60127]` (libz).  All four
  `upx-break-repair.py` recovery arms fail on these (equal=False,
  test=False, unpack=False, `upx -t` rc 1).  The `+` directions on the same
  last block (jq val 181, libz val 17019, xxd ±, dinit ±) ARE left
  byte-identical (`class intact`, `uncompressed_accounted` = u_len).
  The pattern: the −7 direction drops the *chain stop itself* into a
  NEW block that the sentinel walk then self-resumes through (measured:
  `format upx -t violation`, `first_n=5, TOTAL=22585, resume_at=None`
  vs the + direction's `first_n=5, TOTAL=30800, resume_at=13228`),
  so the successor-derived candidate can equal the stored chain's own
  accounting — the acceptance predicate is not met, the tamper falls
  through to the anchor class, and the round-87 header repair fires
  instead — the chain law is not the class that owns these bytes.

## Verbatim upx -t verdicts

- All red (tampered) cells: `upx: /…/in: Exception: compressed data
  violation` (rc 1, `Tested 1 file: 0 ok, 1 error.`)
- All repaired cells: `testing /…/repaired [OK]` then `Tested 1 file.`
  (rc 0, `0 ok, 1 error` never appears).

## Cell receipts

Every cell carries a JSON receipt under `receipts/`: `cell-NNN-<car>-i<idx><d>.json`
(in-class + red OOC leaves), `ooc-NNN-<car>-last<d>.json` (last-block rows).
28 receipts total, one per row; the consolidated matrix plus per-carrier
layout/sentinel/resume provenance lives in `tamper-matrix.json`.

## Reproduction commands

```
python3 -I -B .ufo/waves/round-90/w1/ExecMatrix/matrix.py --run
                                   # 4 carriers x interior x directions
python3 -I -B /fast/scratch/…/probe.py   # red-cell full-arms probes
python3 - # sentinel/resume per-cell walk (inline, see sa-check/side*.log)
```

Run window: 2026-11-05T00:03–00:13 UTC (packed carriers rebuilt per pass with
the pinned `/usr/bin/upx 5.2.0`; integrity re-verified by `[OK]` on every
intact packed and `Exception: compressed data violation` on every tamper).
