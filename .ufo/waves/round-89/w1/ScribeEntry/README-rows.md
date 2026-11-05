# README row drafts — round 89 (ScribeEntry)

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; draft for the L1 to integrate into
`corpus/README.md`. Every number below is stated by a committed receipt (named in the row or in
`.ufo/waves/round-89/w1/ScribeEntry/report.md`).

## Shape note (read before integrating)

The two tables have declared headers:

- `## Coverage map` — `| section | entries | state |` (3 columns); every coverage row in the file has
  3 cells.
- `## Knowledge` — `| entry | topic | source | verified-at |` (4 columns); 126 of the index rows have
  4 cells.

The **round-88 index row (README.md:269) has only 2 cells** (no `source`, no `verified-at`) and the
**round-89 index row already landed at README.md:270 has 3 cells** (no `source`), while the
**round-89 coverage row at README.md:130 has 4 cells** (one more than the coverage table's 3
columns). The drafts below use the *table's declared* shape, not the round-88 row's literal shape,
because copying the round-88 row's shape reproduces its missing-column defect. Two other index rows
have the same defect (README.md:140 and :141, both 2 cells) and one has 5 (README.md:139).

## Coverage-map row draft (append after the round-88 row, README.md:129)

```markdown
| Packed-ELF `b_info` value classes (round 89) | `2026-11-04-r89-binfo-field-value-class` | **Core** — a wrong-but-in-range first-block `sz_cpr` passes every bound the packer applies to the field and fails only at the payload stage (`compressed data violation`); `tools/round-89/upx-field-value-repair.py` derives the value stored-value blind and reports `intact` / `chain-geometry` / `field-value`, re-validating the corrected bytes through the round-87 anchor path; `tools/round-89/upx-field-battery.py` scores `recovered 4 of 4` on the four pinned carriers with refuse-plain / corrupt-payload / intact-idempotent / isolation controls and the round-87 8/8 and round-88 4/4 regression arms, where the unchanged round-88 repair scores `0 of 4` (`.ufo/waves/round-89/pre/c1-base-r88-repair.json`) |
```

## Knowledge-index row draft (append after the round-87 row, README.md:268)

```markdown
| `2026-11-04-r89-binfo-field-value-class` | a wrong-value `sz_cpr` is the same redundancy as a zeroed one: the stored value is not an input to the derivation, only the `intact`/`corrected` decision; nine field classes measured on two carriers show `sz_unc` has no redundancy, `sz_cpr = sz_unc + 1` answers `header corrupted` (the shared object answers `corrupt b_info` for the same class, so the class — not the message — is the key), and a tampered `l_info.version` is tolerated by `upx -t` yet breaks the locator; limits: block 0 only, no decompression, the round-89 repair's own cost curve unmeasured | S311, S312, S306, S309, S310; `tools/round-89/upx-field-value-repair.py`, `tools/round-89/upx-field-battery.py`; receipts `.ufo/waves/round-89/pre/`, `.ufo/waves/round-89/l1/scores/` | 2026-11-04 |
```

## Frontier-note paragraph draft (the file's `## Frontier` prose, after the round-88 note)

```markdown
Round-89 frontier note, 2026-11-04: **packed-ELF `b_info` value classes** are Core for the four pinned carriers (`jq`, `xxd`, `libz.so.1.3.2`, `docker-init`) under UPX 5.2.0 `--best`, little-endian ELF x86-64, a *wrong but in-range* first-block `sz_cpr` (`2026-11-04-r89-binfo-field-value-class`; S311, S312, S306, S309, S310; `tools/round-89/upx-field-value-repair.py`, counter `tools/round-89/upx-field-battery.py`, recovered 4 of 4 with the round-87 8/8 and round-88 4/4 regression arms). Still Frontier: later-block `sz_cpr` values, `p_filesize`/`p_blocksize`/adler repairs, entry-altered stubs, big-endian/PE/32-bit UPX carriers, and an overlay carrier whose chain does not account for `u_len`.
```

## Numbers used, with the receipt behind each

| number | receipt |
|---|---|
| `recovered 4 of 4`, `met_target true`, exit 0, four controls true, round-88 regression `recovered 4 of 4` rc 0 | `.ufo/waves/round-89/pre/c1-candidate-at-declaration.json` |
| tamper jq 252→244, xxd 249→241, libz 201→193, dinit 226→218; every repaired file equals its packed pin | same (`cases[].tamper`, `cases[].repaired_equals_packed`) |
| REA counts jq 167/30/190, xxd 99/29/103, libz 184/29/199, dinit 1268/29/1111 | same (`cases[].rea.counts`) |
| unchanged round-88 repair `recovered 0 of 4`, exit 1, all controls true | `.ufo/waves/round-89/pre/c1-base-r88-repair.json` |
| `identity` and `naive-global` `recovered 0 of 4`, exit 1 | `.ufo/waves/round-89/pre/c1-control-identity.json`, `…/c1-control-naive.json` |
| round-87 class regression `recovered 8 of 8`; round-88 class regression `recovered 4 of 4` | `.ufo/waves/round-89/l1/scores/c1-r87class-regression.json`, `…/c1-r88class-regression.json` |
| nine field classes × two carriers = 18 cells, 14 rc 1 and 4 rc 0, verbatim `upx -t` texts | `.ufo/waves/round-89/l1/scores/block29-cells.json` |
| `compressed data violation` on all four tampered carriers | `.ufo/waves/round-89/pre/c1-base-r88-repair.json` (`cases[].precondition.tail`) |
| docker-init candidates 136 / 226 / 440 accounting 123,942,159 / 851,288 / 850,696 against `u_len` 851,288 | `.ufo/waves/round-88/w1/ExecGeomCross/evidence/docker-init.derive.json` |
| repair selftest 16 cases, failures 0 | `tools/round-89/upx-field-value-repair.py --selftest` (this seat, exit 0; receipt `.ufo/waves/round-89/w1/ScribeEntry/receipts/selftest.txt`) |
| the repair's refusal set and exit codes (2 / 1 / 2) | this seat's `receipts/refusals.json` |
