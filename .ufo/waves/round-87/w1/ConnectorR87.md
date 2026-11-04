# ConnectorR87 — round 87 connector report (R87-C1 cross-links)

Deliverable: `.ufo/waves/round-87/w1/ConnectorR87/links.md`. Read-only seat. No frozen file, production file, scratch or VCS state was touched.

## Evidence
- The R87 battery's population is the round-70 carrier table, copied rather than reused by reference:
  - the 4 sha256 pins are byte-identical (`tools/round-70/packed-elf.py:91-110` vs `tools/round-87/upx-tamper-battery.py:78-84`)
  - `DECLARED_ORIG` is identical (r70 l.116 = battery l.86)
  - the packing mode `upx --best` is the same (r70 l.85, battery l.227)
- The round-68 and round-69 index lines state the limit as "default packing".
- The repair's docstring (`upx-magic-repair.py:8-15`) relies on `packhead.cpp` for "the checksum excludes the magic". The frozen plan's source list names only `linux.h` and `p_unix.cpp`, and `packhead` appears in neither the plan nor `claims.json`.
- Sibling overlap: only `kaidoku-shokunin/PROVINCE.md` mentions UPX among all lanes' PROVINCE files.
  - revenger-shokunin holds packer bibliography (S348 SoK Deep Packer Inspection, S206/S244/S249/S280/S328) with no UPX or ELF measurement.
  - The single non-kaidoku `UPX` hit is a base64 false positive in chousa.
  - Kaidoku alone claims the ground.

## Affected axes
- coverage: the frontier supersession must be magic-only.
- calibration: the S-row for the checksum rule is missing, and the packing-mode limit differs from R68/R69.
- depth: R70 is the correct ancestor link.

## Proposed move (one)
- The R87 knowledge entry and registry row should cite **R70** (with S269 and S270) as the ancestor for population and packing mode, not R68.
- Add a third S-row for UPX v5.2.0 `src/packhead.cpp` (checksum = sum of bytes 4..30 mod 251, excluding the magic), or drop that claim from the entry.
- Supersede only the magic half of `corpus/README.md:324` and `PROVINCE.md:466/474/537`.
- The exact coverage-map row, index line, frontier note and two SKILL registry rows are in links.md section 3.

## Risks
- If the claim is not met, the map row must use the "measured, not promoted" variant.
- The repair row's selftest stamp is unverified: this seat did not run it.
- The slug `2026-11-04-r87-upx-magic-repair` is a proposal.

## Verification for the L1
- `python3 -I -B tools/round-68/registry-conformance.py --root . --rev <rev>` after adding the rows: expect no unregistered round-87 paths.
- `grep -c packhead corpus/SOURCES.md` must be ≥ 1 if the entry states the checksum rule.
