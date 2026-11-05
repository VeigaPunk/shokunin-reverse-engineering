# ExecGeomIndep — scoped findings (round 89, kaidoku; claim R89-C1 derivation)

Full evidence: `.ufo/waves/round-89/w1/ExecGeomIndep/report.md` (commands with exit codes, tables, mechanism).
Receipts: `.ufo/waves/round-89/w1/ExecGeomIndep/receipts/`.

- **Independent derivation** (`derive_szcpr.py`, stdlib only, no import of round-87/88/89 tools): derived block-0
  `sz_cpr` = jq 252, xxd 249, libz.so.1.3.2 201, docker-init 226 — the round-88 record values.
- **Four inputs agree** (intact, `sz_cpr := 0`, `:= true-8`, `:= 0xFFFFFFF0`) on all four carriers: 4 of 4 carriers,
  16 of 16 cells equal.
- **Repo comparison**: `tools/round-89/upx-field-value-repair.py --info` reports the same `derived_sz_cpr` in 16 of 16
  cells (exit 0 each). Only label difference: `0xFFFFFFF0` is `field-value` in the repo tool, `field-value-outofrange`
  in mine.
- **Ablation**: the stored word is never read by any walk or gate (it is overwritten at `b0+4` before walking). A
  55-value sweep per carrier gives one derived value each. A scratch mutant that leaves the stored word in place
  refuses zero and 0xFFFFFFF0 on all carriers and returns the wrong candidate (136) on docker-init — the stored
  value would change the result if it were read.
- **Limits**: one field, four carriers, one packer version. Uniqueness beyond the measured docker-init survivor set
  (three candidates, one fitting `u_len`) is not established. Round-89 C2 was not examined.
- **Own defect, fixed and disclosed**: first locator read the version/format bytes at the wrong offset; corrected
  before any result was recorded (report §8).
- **Installs**: none. Scratch deleted after receipts were copied.
