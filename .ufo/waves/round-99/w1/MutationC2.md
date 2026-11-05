# MutationC2: mutation test of the R99-C2 battery against upx-pe-repair.py at L

Seat: MutationC2 (mutation-tester). Lane: kaidoku, round 99, attempt 1.
Repair under test: `tools/round-99/upx-pe-repair.py` at L = 01c4b79cc1cf8e6172b507edebb6a4d3125c5c6f.
Counter: `tools/round-99/pe-upx-trunc-battery.py` (identical at F = 8fb5ac4 and L; `git diff --stat` empty). Counter not modified.
Tools: upx 5.2.0 (/usr/bin/upx, pre-existing); system python3 3.14. Nothing installed or upgraded. No pacman.

## Method
- Clone per mutant: `git clone --shared <lane> $S/m/<id>`; `git -C $S/m/<id> checkout --detach 01c4b79...`; `rev-parse --show-toplevel` asserted equal to clone dir before each write.
- Mutant = L source with one decision changed (exact-substring replace, asserted count == 1). Copied to `$S/m/<id>/tools/round-99/upx-pe-repair.py`.
- Frozen command, worktree mode, clone-local:
  `python3 -I -B $S/m/<id>/tools/round-99/pe-upx-trunc-battery.py --root $S/m/<id> --repair tools/round-99/upx-pe-repair.py --rev worktree --work $S/work/<id> --json-out $S/rcpt/<id>.json`
- Verdict: exit 1 or label != TARGET = KILLED; exit 0 with met True = SURVIVED.
- Baseline (M00, unmutated L): exit 0, `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79`, met True. Also run once by hand: `python3 -I -B .../pe-upx-trunc-battery.py --root $S/m/base ... --rev worktree` exit 0, 10.7 s.
- Mutant runner: `python3 -I -B $S/run_mut.py` (exit 0, log `run.log`); edge probes: `python3 -I -B probe_edges.py` (exit 0) and `python3 -I -B probe2.py` (exit 0). Scripts copied to the wave dir.
- Repair-candidate sha256 per mutant is in the receipts: 26 receipts, 25 distinct mutant hashes, and M00 (control, unmutated L) hashes to L's `ac97598a94c0`. All mutants compiled with `ast.parse`.

## Kill table (25 mutants + control)
| id | single decision changed | battery exit | verdict / failing arms |
|---|---|---|---|
| M01 | truncation end without ALIGN_UP | 0 | SURVIVED |
| M02 | truncation test `<` -> `<=` | 1 | KILLED: recovered 3/30, decoy 0/9, intact 1/10 |
| M03 | last header = section 0 | 1 | KILLED: truncated 0/40 |
| M04 | last header = max raw end | 0 | SURVIVED |
| M05 | drop FileAlignment==0 refusal | 0 | SURVIVED |
| M06 | FileAlignment read at SectionAlignment offset | 1 | KILLED: recovered 9/30, decoy 2/9, intact 3/10, overlay 12/20 |
| M07 | drop output-is-directory refusal | 0 | SURVIVED |
| M08 | fixed temp name instead of mkstemp | 0 | SURVIVED |
| M09 | drop PackHeader uniqueness (min of set) | 0 | SURVIVED |
| M10 | drop PackHeader checksum check | 0 | SURVIVED |
| M11 | gate window start rptr-63 | 0 | SURVIVED |
| M12 | scan window ends one byte early (+1023) | 0 | SURVIVED |
| M13 | too-few-sections bound n<3 -> n<2 | 0 | SURVIVED |
| M14 | drop chmod 0644 on output | 0 | SURVIVED |
| M15 | drop fsync of output | 0 | SURVIVED |
| M16 | drop PackHeader magic rewrite | 1 | KILLED: recovered 10/30, decoy 0/9, overlay 10/20 |
| M17 | section 2 always UPX2 (no .rsrc branch) | 0 | SURVIVED |
| M18 | resource dir offset 96 for PE32+ | 0 | SURVIVED |
| M19 | drop c_len <= file size check | 0 | SURVIVED |
| M20 | drop truncation refusal | 1 | KILLED: truncated 0/40 |
| M21 | version bound 14 -> 15 | 0 | SURVIVED |
| M22 | drop PackHeader bounds check | 1 | KILLED: recovered 24/30, decoy 7/9, intact 8/10 (IndexError past EOF in second window of UPX2 carriers fastlist64, gle64dll) |
| M23 | c_len < u_len -> <= | 0 | SURVIVED |
| M24 | skip UPX-name repair of sections 0/1 | 1 | KILLED: recovered 10/30, overlay 10/20 |
| M25 | skip section-2 rename | 0 | SURVIVED |

Score: 7 killed, 18 survived, of 25. Control M00 passes. Receipts: `.ufo/waves/round-99/w1/MutationC2/receipts/M00..M25.json`; mutants: `.../mutants/`; `summary.json`.

## Survivors: classification
Population facts from the 10 packed carriers (`probes/probe_pop.py`): PackHeader at window offset 32 (9 carriers) or 69 (sevenzip64dll); every carrier's last section raw end is already FileAlignment-aligned; every packed file length equals its aligned end except sevenzip64dll (overlay 2228471); no carrier has FileAlignment 0, two sections, two valid headers, a checksum-valid header with bad lengths, version 15, or c_len == u_len.

Blind spots, confirmed by a targeted probe (crafted from the t32 pack; base L vs mutant):
- M05 FileAlignment 0: base rc 2 `refused: filealign-zero`; mutant rc 1 `ZeroDivisionError` traceback.
- M09 duplicate valid header at window start: base rc 2 `packheader-candidates:2`; mutant rc 0 with output.
- M13 NumberOfSections 2: base rc 2 `refused: sections`; mutant rc 1 `IndexError` traceback.
- M12 only header at window offset 1023: base rc 0; mutant rc 2. Base output fails `upx -t` (rc 1), so the window edge is accepted without evidence either way.
- M11 only header at window start 960: base rc 0; mutant rc 2.
- M10 checksum-invalid look-alike at 960 with nonzero lengths: base rc 0; mutant rc 2 `packheader-candidates:2`. The frozen decoy arm is rejected by its zero lengths (`c_len > 0` fails), so it never isolates the checksum.
- M19 c_len beyond file size, valid checksum: base rc 2; mutant rc 0, output fails `upx -t`.
- M21 version 15, valid checksum: base rc 2; mutant rc 0.
- M23 c_len == u_len, valid checksum: base rc 2; mutant rc 0.
- M01 last raw end 100 bytes below its aligned end (file cut at the raw end): base rc 2 `truncated`; mutant rc 0, output fails `upx -t`. The frozen truncation cuts are at aligned_end-1 and mid-UPX1 only, so no cut lands between raw end and aligned end.
- M08 pre-existing `<out>.tmp`: base leaves the sentinel intact; mutant overwrites and renames it away.
- M14 output mode: base 0o644; mutant 0o600.
- M25 section-2 name left as `.rdata` on gle64dll tampered-both input: base output `UPX2`, mutant `.rdata`; both `upx -t` rc 0 and the frozen unpack sha agree. The frozen oracle cannot see the section-2 name.
- M17, M18 (unprobed, [INFERENCE]): the `.rsrc` branch and the PE32+ resource-directory offset only change output when the resource RVA lies inside a UPX2 section. No carrier does this, so the branches are never exercised. Blind spot, not equivalence.
- M04 (unprobed, [INFERENCE]): max raw end equals the last header on every UPX layout (increasing rptr); it differs only for out-of-order section tables. Equivalent on UPX layouts; blind spot for crafted tables.
- M07 is equivalent under the frozen predicate: rc 2, no Traceback, nothing created in both. Only stderr text differs (`output-write-failed: Is a directory` instead of `output-is-directory`), and the cli arm never checks text.
- M15 is an equivalent mutant for every observable output. Only durability is lost, and no test can see it.

Summary: equivalent = M04 (on UPX layouts), M07 (predicate), M15. Blind spots = the other 15 (M01, M05, M08, M09, M10, M11, M12, M13, M14, M17, M18, M19, M21, M23, M25).

## Observations on L (base, not mutants)
- L returns rc 0 for crafted inputs whose output fails `upx -t` (base rows of the M10, M11, M12 probes, `upx_t_rc 1`). The intact path trusts the header rule and never tests the pack. These inputs are outside the frozen population. Recorded as scope, not a counted failure.
- The frozen counter's "effective 79 of 79" and "truncated 40 of 40" are not affected by these survivors. Every survivor leaves the frozen label at TARGET, so the calibrated predicate does not measure the guard surface.

## Hand-off (for the main agent, not applied here)
Adding single fixtures for each blind spot above (FileAlignment 0, two sections, duplicate and edge-positioned headers, c_len beyond file, version 15, c_len == u_len, unaligned raw-end cut, pre-existing `<out>.tmp`, output mode, section-2 name assertion) would kill most survivors. The counter is frozen (R99-C2); this seat did not re-freeze or re-score anything.

Receipts and probes in `.ufo/waves/round-99/w1/MutationC2/`: `receipts/`, `mutants/`, `summary.json`, `probes/probe2.json`, `probes/probe_edges.json`, `probes/probe_pop.py`, `run_mut.py`, `run.log`, `probe2.log`.
