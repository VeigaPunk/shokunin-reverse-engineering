# MutationC1 — mutation test of `tools/round-99/self-assessment-audit.py` (R99-C1 counter)

Seat: MutationC1 (lane kaidoku, round 99, wave w1). Godspeed axes: (a) kill power across the four
detector channels (selftest / B0 label / Bk label / exit code), (b) coverage of untested decision
points (survivors = findings), (c) byte-exact restoration, (d) cost (whole campaign: ~5 s).

## Method
- Pristine counter bytes: sha256 `e732465bde4d7c125b45fc60ead9343ee6d1c73378830e42e028ac2d0334eec0`
  (git blob `ee3b7fda` identical at F `8fb5ac4` and Bk `c19d57c`; equals `counter_sha256` in every
  committed receipt, incl. the B0 control `pre/c1-do-nothing-at-base.json` — the counter does not
  exist at B0 `de098f5`, it is copied into the clone at `tools/round-99/self-assessment-audit.py`,
  exactly as the committed B0 control was produced).
- 12 single-decision mutants, each one verified-unique string replacement (diffs in
  `.ufo/waves/round-99/w1/MutationC1/mutants/*.diff`, hashes in `mutants.json`).
- Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone`,
  `git -C $S/clone checkout --detach <rev>`; toplevel asserted before every git mutation.
- Per rev (B0, Bk), per mutant: `--selftest`, then the frozen command run from the clone cwd:
  `python3 -I -B tools/round-99/self-assessment-audit.py --root $S/clone --rev <rev> --json-out <receipt>`
  (TMPDIR pointed into scratch; 28 receipts in `MutationC1/receipts/`, full per-run table in `summary.tsv`).
- Kill rule: selftest rc != 0 OR (label|mismatches|exit) differs from the committed anchor at that
  rev. Anchors: B0 `pre/c1-do-nothing-at-base.json`, Bk `l1/scores/c1-at-c19d57c….json`.

## Calibration and restoration (pristine bytes)
| run | rev | label | exit | verdict |
|---|---|---|---|---|
| CALIB | B0 | `mismatches 17; head-score mismatch; head-fraction mismatch; map-rows 176 of 182; registry 0 of 9` | 1 | CALIB-OK (== anchor) |
| CALIB | Bk | `mismatches 0; head-score ok; head-fraction ok; map-rows 183 of 183; registry 14 of 14` | 0 | CALIB-OK (== anchor) |
| RESTORE | B0 | same as B0 anchor | 1 | RESTORED-OK (sha256 re-verified `e732465b…`) |
| RESTORE | Bk | same as Bk anchor | 0 | RESTORED-OK (sha256 re-verified `e732465b…`) |
Pristine selftest: `SELFTEST cases=9 failures=0`, rc 0 — matches committed `pre/c1-selftest.txt`.

## Kill table (K = killed channel; "same" = label/exit equal to that rev's anchor)
| mutant (single decision) | sha256 (mutant) | selftest | B0 | Bk | verdict |
|---|---|---|---|---|---|
| m01 drop sha-membership check | `7c86a815eb13560e7f7aefe3bbe7b41cb822c4e5af52837b7b0e3caf98b89896` | rc1 f1 (F5) | same | same | KILLED |
| m2 registry body = whole SKILL.md (rows before heading) | `ed463f26a7cf384c73ad31cb8052e37ed110eaddc7e41fc79594efa163c4ec6b` | rc1 f1 (F7) | same | same | KILLED |
| m03 exit-map regex: drop `(?<![\w.])` lookbehinds | `2bc5f9eb2e63177250065ff30d9429dbee9764d6a95f5ebe244a012a96176e19` | ok | same | same | SURVIVED |
| m04 drop KIND_RE kind-gate | `8807bf8b556e4d6925ea9bc3bcd54976a8e46845ea7cad17c531152a21948515` | ok | same | same | SURVIVED |
| m05 registry row floor 5 -> 4 cells | `ba56421e4b5eaad85128be6d108940df3bfe7660c77334ea4562511ec75bba8b` | ok | same | same | SURVIVED |
| m06 invert a1 (`!=` -> `==` head score) | `d503a5865f04890d5adc84738ea1bb5a38f15e7b2ef1bc607ad4186d16c9d480` | rc1 f9 | `mismatches 16; head-score ok…` exit 1 | `mismatches 1; head-score mismatch…` exit 1 | KILLED |
| m07 invert a2 (`!=` -> `==` head fraction) | `382cbf458a2d247ab41a15524791b3ae1a7092f2872d16fefac85daeae631adb` | rc1 f9 | `mismatches 16; head-fraction ok…` exit 1 | `mismatches 1; head-fraction mismatch…` exit 1 | KILLED |
| m08 TOOL_DIRS drop round-99 | `b8f9e05fe1d23c2a03d6dfa3eda8ebd2e44ff95e615ba361a7657327740ab2b7` | ok | same | `registry 9 of 9` exit 0 | KILLED |
| m09 drop REG_HEAD-absent fallback | `332159994564f45d66dbf643e33491c4fa014f97fa2ff049a4caac6e451ba07f` | ok | same | same | SURVIVED |
| m10 A3: accept any non-blank section line (prose) | `f38d57da4b4a44c1474de1090aa133e946ba69e7ada615d31738a6dad808c863` | ok | same | same | SURVIVED |
| m11 drop 20-char floor (`< 20` -> `< 0`) | `fbf988ba6be4795e8d7d0a0a380ebc5a2b8744d426313c218254f34033207262` | rc1 f1 (F2) | same | same | KILLED |
| m12 exit always 0 | `4b68b31ccf946eea484064ad75851f01fc361c3363b8a875222549a1d53e77d3` | ok | label same but **exit 0 != 1** | same | KILLED |

Totals: 12 mutants — 7 killed, 5 survived, 0 inconclusive. Baselines green at both revs.

## Survivors — coverage findings (defects the current envelope cannot see)
1. **m03** exit-map lookbehinds unexercised: F6 deletes the whole cell; no fixture carries a decoy
   like `10=`/`x0=` that only the `(?<![\w.])` guard rejects. Both revs + selftest green.
2. **m04** kind-gate unexercised in isolation: F4's path-only row is already rejected by the
   exit-map/sha cells, so KIND_RE could vanish without any detector noticing.
3. **m05** 5-cell floor unexercised: no valid-looking 4-cell registry-row fixture exists.
4. **m09** REG_HEAD-absent fallback unexercised: the heading already exists at B0 and Bk, and every
   selftest skill string includes it. Without the fallback an absent heading would crash
   (uncaught IndexError, exit 1, no receipt) — outside the tested envelope, worth a fixture.
5. **m10** A3 table-row gate redundant on all tested inputs: accepting prose lines changes nothing —
   the 20-char floor still rejects F1's prose line (`mentionedinprose` = 16 chars), and the B0/Bk
   coverage-map sections contain no >= 20-char prose stem mentions. Gate + floor jointly tested;
   the gate alone is not.

## Notes
- m12: the label string alone does not see it; only the receipt `exit` field (part of the frozen
  predicate) does — the committed-receipt comparison must keep pinning exit, not just the label.
- `counter_sha256` is the counter hashing its own runtime bytes, so every mutant receipt carries a
  different value (e.g. m12 `4b68b31c…`); expected, not a kill signal.
- m06/m07 die on every channel — selftest fails all 9 cases (green included) and both revs diverge.
- m11 dies only via selftest F2 (stem-only row) — both real-rev labels stay clean; the selftest is
  the sole guard for the 20-char floor at these revs.
- No tools installed (python3 + git sufficient); no pacman transactions, no sysctl/host changes.
- Lane untouched except this wave dir; L1 receipts only read/copied; scratch
  `/fast/scratch/hyaku/kaidoku-r99/MutationC1` deleted on exit (trap + explicit rm).
