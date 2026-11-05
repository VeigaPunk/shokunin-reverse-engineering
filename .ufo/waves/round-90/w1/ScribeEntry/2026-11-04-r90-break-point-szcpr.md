# Packed-ELF `b_info` break point: a wrong later-block `sz_cpr` derived from its successor (round 90, R90-C1)

source: S311 — UPX v5.2.0 `src/p_lx_elf.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp — registry row S311, opened 2026-11-04, HTTP 200, 373743 bytes, sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc`; `PackLinuxElf64::un_shlib_1` line 7011 and the `b_info` header read with the short-peek refusal `corrupt b_info`; the block walk the break-point law steps along.
source: S312 — UPX v5.2.0 `src/p_unix.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.h — registry row S312, opened 2026-11-04, HTTP 200, 6651 bytes, sha256 `73bd992ec0fb46022e299ec4b2cd696545412453a654573e6246034cf4881a88`; the `packed_struct(b_info)` and `packed_struct(l_info)` trailers the walk steps by, in the copy the carriers use.
source: S306 (existing, round 87) — UPX v5.2.0 `src/stub/src/include/linux.h` — `struct b_info` line 570 with `uint32_t sz_cpr;` line 572: the 12-byte header the walk advances by `12 + sz_cpr`.
source: S309 (existing, round 88) — UPX v5.2.0 `src/packhead.h` — `unsigned u_len;` line 55: the declared uncompressed total the accounting bound is an exact-equality filter on.
source: S310 (existing, round 88) — UPX v5.2.0 `src/packer.cpp` — lines 544-546: the `PackHeader` arithmetic gate that answers `header corrupted` before any checksum.
source: pack-side row — none cited. The round-90 scout's report `.ufo/waves/round-90/w1/ScoutUpxPack/ScoutUpxPack.md` and any new `corpus/SOURCES.md` row were absent at the measured checkout (`ls` returned `No such file or directory`; `corpus/SOURCES.md` ends at S315). Add that row before this entry cites it.
verified-at: 2026-11-05 (round 90; measured at revision `18b21f092`; receipts `.ufo/waves/round-90/w1/ScribeEntry/receipts/`; no SCORECARD round-90 section existed at draft time, so the receipt path is the anchor)
recheck: 180d — `python3 -I -B tools/round-90/upx-break-repair.py --selftest` (17 cases, failures 0) and the counting command below.

## Status

[observation] The frozen counter's first run returns `P1 6 of 6; P2 3 of 4; P3 4 of 4`, exit 1, `met_target` false (`receipts/c1-battery.json`, `receipts/c1-battery.rc` = 1). The frozen expectation is `P1 6 of 6; P2 4 of 4; P3 4 of 4`.
[observation] The one short cell is the round-89 block-0 class on docker-init. In that run the repair exits 0, `upx -d` restores the carrier pin, `upx -t` answers rc 0, and REA 6.5.0 reports `procedure_count` 1267 where the original reports 1268 (`receipts/rea/`, the only non-1268 docker-init count among the battery's candidate runs). The same bytes (sha256 `0bd49c8d4da5…`, 851,288 bytes) were reported 1268 by three other REA runs in the battery, by the original's own run, and by two reruns on a copy at a different path (`receipts/rea-dinit-p2-rerun1.json`, `receipts/rea-dinit-p2-rerun2.json`, both `procedure_count` 1268, rc 0).
[observation] The first run's label is recorded as measured. This entry does not record the claim as met, and a rerun of the counter is a new receipt, not a replacement for the first.

## The class

[observation] Replacing one interior block's `sz_cpr` with a different in-range value (`0 < value <= sz_unc`), in either direction (stored − 7 and stored + 7), is refused by `upx -t` as `Exception: compressed data violation`, rc 1. Measured in 36 of 36 cells: block 0, each interior block, and the last block of the first segment, on jq (10 cells), xxd (10), libz (6) and docker-init (10) (`receipts/upx-t-tamper-messages.txt`). This is the message round 89 measured for a block-0 value, so the message alone does not say which block is wrong.
[observation] The round-87 anchor path reports the tampered files intact (every `UPX!` word is in place). The round-89 block-0 law scores 0 of 6 on the six P1 cells, each with rc 0 and `recovered` false (`receipts/c1-battery.json` `controls.no_work`).
[inference] The redundancy that fixes the value is the one round 88 used: `sz_cpr` is the distance to the next block. A wrong interior value still moves the walk, into the middle of the next block, where the walk's own checks fail. The walk therefore stops after the tampered block, and the stop identifies it.
[unknown] Whether the same class is repairable on a 32-bit ELF, or on a shared object with a different `cto` or filter layout. Neither was measured here.

## The rule

The repair is `tools/round-90/upx-break-repair.py` (sha256 `aaf3536ea2226ac8ec498603d50b7b1b4a57c5572c7edef4fcf0e2a91d35590b`). Its code, in order:

1. **Walk.** For each `l_info` candidate (round 88's `l_info_candidates`), walk the first segment by stored values. A block is accepted while `sz_unc != 0`, `sz_cpr != 0`, `sz_cpr <= sz_unc`, the payload fits before the PackHeader, and the method byte matches the block-0 method or the PackHeader method. The longest accepted prefix is kept.
2. **Route.** A prefix of one block or none is the round-89 block-0 class: the round-89 law runs, through the round-87 anchor path. A prefix of two or more blocks is this round's class.
3. **Break block.** The break block `p` is the last accepted block of the prefix. Its stored `sz_cpr` is not an input to the derivation.
4. **Successor scan.** For every offset `s` in `p + 13 .. ph_off − 12` whose 12-byte header is a plausible `b_info` (`0 < sz_cpr <= sz_unc`, payload inside the file, method matches), the candidate value is `derived = s − (p + 12)`. It is accepted only when `0 < derived <= sz_unc(p)` and `derived != stored(p)`.
5. **Sentinel.** With the candidate written, the chain from block 0 must reach the end-of-chain sentinel, directly or through the loader-resume step (round 87's `find_sentinel`).
6. **Exact total.** The uncompressed bytes the chain accounts for (the stored walk plus any resumed segment) must equal the PackHeader `u_len` exactly. This is a filter: `total != u_len` rejects the candidate. It is not a rank key (QUALITY 171).
7. **Strictly more.** When the stored chain reaches a sentinel, the candidate's total must be strictly greater than the stored chain's total. Survivors are ordered by (total, −derived). Two survivors with the same total set `ambiguous` in the receipt, and the smaller derived value wins.
8. **Re-validation.** The written bytes go through the round-87 anchor path; a result the anchor path refuses is refused.

[observation] Measured on the four carriers, interior block 1 (the first interior block; offsets 840 / 837 / 814 on jq / xxd / docker-init): both directions give the same derived value, and the accounted total equals `u_len` (`receipts/indep-info-summary.json`).

| carrier | block 1 offset | stored (−7 / +7) | derived | accounted | `u_len` | stored chain accounts |
|---|---|---|---|---|---|---|
| jq | 840 | 1644 / 1658 | 1651 | 30,800 | 30,800 | 14,527 |
| xxd | 837 | 943 / 957 | 950 | 38,928 | 38,928 | 11,899 |
| docker-init | 814 | 195 / 209 | 202 | 851,288 | 851,288 | 17,683 |

[inference] The derived values are the true values: each tamper was stored ±7 around the true value, and the derivation returns the midpoint in both directions (the measured midpoints are the values above).
[observation] The stored chain under-accounts `u_len` in all 18 interior cells on jq, xxd and docker-init (jq blocks 1–3: 14,527 / 24,088 / 29,616 of 30,800; docker-init blocks 1–3: 17,683 / 593,232 / 823,984 of 851,288). That is the strictly-more arm of step 7 working as designed.

Three outcomes, as the code reaches them:

| condition | output | receipt class |
|---|---|---|
| prefix of two or more blocks, stored chain intact, one survivor | one four-byte write at `p + 4`, inside the window | `break-point` |
| prefix of two or more blocks, stored chain not intact, no survivor | refused, rc 2: `later-block break: no successor accounts for exactly the declared u_len` | refused |
| prefix of two or more blocks, stored chain intact, no survivor | handed to the round-89 law; the output is whatever that law writes | `anchor` / `intact` / `field-value` |

[observation] The third row is not the "left unchanged" outcome the module docstring states. The code calls `_block0` on that branch, and the round-89 law's anchor path can write outside the window (Limits 1). The docstring and the code disagree on this branch; the code is the one measured.

## Composition with rounds 87, 88 and 89

| round | class | repaired by | place in this repair |
|---|---|---|---|
| 87 | UPX magic word tampered | round-87 anchor path | last step of every branch, on the repaired bytes |
| 88 | block-0 `sz_cpr` zeroed | chain geometry (`tools/round-88/upx-chain-repair.py`) | reached through the round-89 law |
| 89 | block-0 `sz_cpr` wrong, in range | block-0 law (`tools/round-89/upx-field-value-repair.py`) | the one-block-prefix route, and the fall-through |
| 90 | interior later-block `sz_cpr` wrong, in range | break-point derivation | first, when the prefix is two or more blocks |

[observation] Composition is measured, not assumed. The round-88 class (P3, zeroed block 0) is 4 of 4. The round-89 class (P2, block 0 at stored − 7) is 3 of 4, the failure being the docker-init REA count in Status. The independent block-0 cells recover on all four carriers (`receipts/indep-matrix-summary.txt`).

## Measured (R90-C1 battery, rev `18b21f092`)

`receipts/c1-battery.json`, exit 1, `label` "P1 6 of 6; P2 3 of 4; P3 4 of 4":

| population | cells | recovered | arms in each recovered cell |
|---|---|---|---|
| P1 later-block, block 1, stored ±7 (jq, xxd, docker-init) | 6 | 6 | repair rc 0, field-only, identity, `upx -t` rc 0, `upx -d` pin, REA counts |
| P2 block 0, stored − 7 (round-89 class; jq, xxd, libz, docker-init) | 4 | 3 | jq, xxd, libz all arms; docker-init `rea_recover` false, others true |
| P3 block 0, stored 0 (round-88 class) | 4 | 4 | all |

| control | observed |
|---|---|
| N1 plain ELF refused | 4 of 4, rc 2 |
| N2 flipped payload byte never recovered | 4 of 4 not recovered (`packer_clean` false) |
| N3 intact carrier byte-identical | 4 of 4 |
| isolation (listing after the child exits) | 12 of 12 invocations; `["in"]` or `["in", "out"]` |
| carrier_blind (bwrap, decoy carrier paths, tmpfs run root) | 6 of 6 blind cells re-scored; the probe saw the decoy sha on every pinned path (`probe.rc` 0) |
| no_work (round-89 repair, P1) | 0 of 6 |
| cheat_repack | unblinded: reproduces the intact packed bytes; blinded: killed |

[observation] Independent matrix (`receipts/indep-cells.json`, `receipts/indep-matrix-summary.txt`; 36 cells, 4 carriers, block index 0 to last, stored ±7): 26 recovered, 8 unchanged, 2 out-of-window writes. Interior non-last cells recover in 18 of 20; the two failures are libz block 1. Every recovered cell passes the window, `upx -t` rc 0 and `upx -d` pin arms.
[observation] Repair self-test: `python3 -I -B tools/round-90/upx-break-repair.py --selftest` → `SELFTEST cases=17 failures=0`, rc 0 (`receipts/repair-selftest.stdout`).

## Limits (measured)

1. **Last block before the chain stop.** The derivation has no survivor on the last block of the first segment, so the break-point law does not repair it. In the +7 direction on all four carriers, and in the −7 direction on xxd and docker-init, the output is unchanged with rc 0 and `upx -t` rc 1. In the −7 direction on jq and libz, the stored walk reaches a sentinel at a wrong offset (jq 10,090; libz 60,120, per the info record), the derivation has no survivor, and the walk falls through to the round-89 law. That law writes the four-byte `UPX!` word at the sentinel's value field (jq 10,094; libz 60,124), outside the tampered window, with rc 0, while `upx -t` stays rc 1 (`receipts/indep-cells.json` cells `jq-b4--7`, `libz-b2--7`, both class `anchor`). The frozen counter does not score a last-block cell, so it cannot see this.
2. **Labels.** Eight cells return rc 0, change no bytes, fail `upx -t` with rc 1, and carry the label `intact`: xxd and docker-init last block (both directions, 4 cells), jq last block +7, libz block 1 (both directions) and libz last block +7 (`receipts/indep-info-summary.json`). The label says the file is intact; `upx -t` says it is not. The exit code and the label mean "I changed nothing I own", as round 89 recorded (QUALITY 167).
3. **libz under-accounting shows as a declared class exclusion.** The shared object's stored chain accounts 98,592 of 108,560 `u_len` (`receipts/indep-layout.json`, `stored_accounted_total`). Every libz interior tamper (stored ±7 on block 1) is returned unchanged, rc 0, `upx -t` rc 1, labelled `intact` (2 of 2 cells). The shared object's block-0 class still composes (P2 and P3 libz recovered). The exact-total rule cannot decide that carrier, and it does not guess.
4. **Scan cost.** In-process `repair()` on an interior tamper, five runs per carrier, median and minimum (`receipts/scan-timing.txt`): jq 13,135 offsets in the scan range, 10.3 ms median (9.1 ms minimum); xxd 18,662 offsets, 11.0 ms (8.2 ms); libz 56,002 offsets, 43.1 ms (40.3 ms); docker-init 356,909 offsets, 139.5 ms (132.5 ms). The minimum per offset is 0.69, 0.44, 0.72 and 0.37 µs respectively. Four points on four different chain shapes do not establish a curve, so no linear bound is claimed.
5. **The last block is under-determined.** Any value that still leaves a stop before the resume offset accounts for the same total. The repair refuses that choice rather than picking one; Limits 1 records the branch where the refusal does not happen.
6. **REA counts are not perfectly stable at the single-count level.** On byte-identical docker-init output (sha256 `0bd49c8d4da5…`), one battery run reported 1267 procedures, and the other six runs (three battery candidates, the original, and two reruns) reported 1268 (`receipts/rea/`, `receipts/rea-dinit-p2-rerun1.json`, `receipts/rea-dinit-p2-rerun2.json`). The cause is not measured. The REA procedure count is therefore a corroborating arm of the counter, not an identity proof: byte equality with the pin (`upx -d` sha256) is the identity arm, and a single REA count can be off by one.
7. **Mechanism, not capability.** A packer-validated search over `1..sz_unc` would also repair these cells. The counter does not force the chain walk, so what is measured is the capability, not the mechanism.
8. **Unmeasured.** 32-bit ELF, LZMA-filtered shared objects, multi-member overlays, and any carrier outside the four pinned. All `[unknown]`.

## Counting command

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-90/upx-later-block-battery.py --root . --rev 18b21f092 \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r90/recheck --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" \
  --json-out /fast/scratch/hyaku/kaidoku-r90/recheck.json
```
