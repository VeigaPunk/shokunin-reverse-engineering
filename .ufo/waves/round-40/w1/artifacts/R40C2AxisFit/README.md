# R40C2AxisFit artifacts — DRAFT R40-C2 pre-freeze attack

Lane revision read: `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f` (SKILL.md, tools/round-39/, corpus/evidence/round-39/).
No REA or unblob run was made in this seat; every measurement is a read of committed bytes with the frozen round-39 interpreter.

| file | sha256 | what it shows |
|---|---|---|
| `clean-empty-probe.txt` | `8b52e7df75a69eeac983bae6c6e3960cc1a756fcb25a3f10da682ca9992b7a90` | R39-CL3 D2: a clean image with zero published files falls to `unclassified` under v1 (lab rewrite of H02) |
| `k2-two-tables-label.json` | `652b579cd0506ea4c1c4bfebffd170c82b450dbc06841c18851b9c6107cf86ee` | v1 label for K2 under the two-table SKILL (in-tree-symlink-metadata, row 7) |
| `k5-two-tables-label.json` | `e42f18c873eca98fc8a980047142eaf92860466a0b775e09393884ccd5b72876` | v1 label for K5 under the two-table SKILL (escaping-symlink-removed, row 6) — K5 is mixed |
| `min7-loadbearing.txt` | `48a7bd4885b63dd938b5f6eee1f119ec9b2d59967714fbf911f23680b98757be` | the 7 shortcut cells are all load-bearing on the 20 real envelopes |
| `min-table-sim.py` | `4498ffa402e608282d48d2fe49000b9880fd5775fa1c1feb332f28d50dd55182` | self-contained simulation of the draft's 13 classes vs a 15-cell first-match table |
| `min-table-sim.txt` | `6caa95231ef7f00a6ef10625640a08f12e402bcea9d80a70988adb0923ce3150` | 26/26 pairs, 15 non-* cells, 0 non-load-bearing cells, lower bound 10 |
| `min7-score.txt` | `2f88f9d823b3e9846c21476220390432158a91e4e677f9602bcace3bafcf880c` | executed: 7-non-* cell, 8-row table scores 20/20 on the frozen round-39 held-out set |
| `min7-table.md` | `74bb0d0de0294e7cc61d97bf2099a010e086b2719bce249b93513a4ad9f852d2` | the 7-cell table block (marker + header + 8 rows) |
| `mk-variants.py` | `1da9333b9e856c360eb691c7a231c8aca14a8f9c19e2c9081ff56dc65bed3c75` | rebuilds sk-min7.md, sk-two-tables.md, sk-single-table.md from the lane SKILL.md into --work |
| `ood-probe.txt` | `27cd37cdbce7e68850c39c4e4e9874e3f70e98a35dab58245b467426d9c2f2fc` | R39-CL1 reachable: envelopes with `operation` rewritten to `inspect` get no-squashfs-chunk / escaping-symlink-removed |
| `tableblock-score.txt` | `e4269869ccf8711316cbf6766c9f6f9da5b0b4ecac2235446699188ae8ae23a4` | the interpreter's embedded TABLE_BLOCK scores 18/20 on the same set; H03/H04 (clean-le) become unclassified |
| `two-tables.txt` | `4fd729061406f647a6ac84645bf0d9f033cd7f83b5ed6dc5c4026c1bd198b870` | two live tables: v1 interpreter exits 0 and still decides K5; single-table variant exits 2 (v1's own 'table missing' verdict) |
| `v1-baseline-and-cells.txt` | `221af65887697cf4c114cd2f095574eb1c371e06711853ee5e750304bdfada60` | v1 scores 20/20 on the frozen set; 9 distinct feature vectors; block 18 has 40 non-* decision cells |
| `v1-table-two-copies.txt` | `8053e88080f68224f6d94eee8b377e30f676816b4b3bd822b9605a316969ef95` | SKILL block 18 vs --print-table TABLE_BLOCK differ in 5 decision cells across 5 rows |

## Rebuild

```sh
S=$(mktemp -d); export TMPDIR=$S
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-40/w1/artifacts/R40C2AxisFit
python3 "$A/mk-variants.py" --root "$L" --work "$S/v"
# 7-cell shortcut table vs the frozen round-39 held-out set:
python3 "$L/tools/round-39/sqfs-triage.py" --skill "$S/v/sk-min7.md" --json "$L"/corpus/evidence/round-39/c2/heldout/H*/envelope.json
# two-table / single-table parser behaviour:
python3 "$L/tools/round-39/sqfs-triage.py" --skill "$S/v/sk-two-tables.md" --table-only; echo exit=$?
python3 "$L/tools/round-39/sqfs-triage.py" --skill "$S/v/sk-single-table.md" --table-only; echo exit=$?
# embedded TABLE_BLOCK vs SKILL block:
python3 "$L/tools/round-39/sqfs-triage.py" --print-table
# draft-class-list simulation (no carriers, no REA):
python3 "$A/min-table-sim.py"
```

## Limits

- The two `operation`-rewritten envelopes and the `files := []` envelope are lab rewrites of committed bytes, made to exercise the interpreter, which reads only `normalized_result` and never `operation`/`provider`. They are not real REA envelopes and are not offered as evidence about REA output.
- `min-table-sim.txt` is a decision-logic simulation over feature vectors derived from the draft's class list, not a score over real envelopes; it is marked [INFERENCE] in the report.
- No C2 held-out carrier was built and no C1 carrier was touched.
