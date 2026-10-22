# MutC2Depth — R26-C2 items K1, K2, K3 attacked on the repaired depth row

Seat: KaidokuR26.MutC2Depth (mutation-tester, leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Tips judged: `fe3eb4edf410244eff46151a148c8f754be1ce80`, `003de8cc38a86a914c0348ded674091d47d71fc1` and
`0375717e72dac9ba3e964a83cbc889dd94f3f55d` (the L1 landed two further commits during my window, one of them touching
`corpus/README.md` and two knowledge files, which the detector does read); the whole suite ran at all three with
identical results. Detector: frozen `tools/round-26/c2-calibration.py`, sha256
`3b0f6507e7f77fd1763fc26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e` (unchanged since 81f63f36). Scratch:
`/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC2Depth/`. UTC 2026-10-22T13:00:00Z to 13:11:30Z. No REA call, no web
source, no tool installed.

## Method

Sandbox clones of the lane at each tip (`clone/`, `clone2/`, `clone3/`). Each mutant edits only `SCORECARD.md` in the clone, is committed there, and is measured with the same
bounded detector on pristine, mutated and restored bytes: `python3 -I -B clone/tools/round-26/c2-calibration.py --root <CLONE> --rev <MUTANT_REV>`. All mutation and Git writes
happened in the clones. The lane was read-only: no add, commit, checkout or reset in the lane, and no jj command. Lane `SCORECARD.md` sha256
`10ae7acf0b46392ab9b194f4a21c08688b539ff71ca5db747ad9e8a1e83ec74b` is unchanged across all three tips. The lane working tree and HEAD moved during my window because of sibling
seats and the two L1 commits; neither was my write. `SKILL.md`'s craft heading is still at line 81 and its last non-blank line at 314 at every tip, so K2's span never moved. Baseline at all three tips, same detector: `items 6, mismatches 0`, exit 0. K1 pass (row 17/17, command A
17/17); K2 pass (craft span SKILL.md:81-314 in the evidence cell); K3 pass (measured `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb` resolves, command A there 17/17 equals the K1 N
of 17). Green baseline, so every red below is a killed mutant. Detector notes, verbatim: M1 "depth row N/M != command A rule_blocks/citation_resolved_rules"; M2 "the depth
evidence cell does not contain SKILL.md:81-314 (craft span at REV is 81-314)"; M3 and M1b "command A at the measured revision does not give the K1 N"; M5 and M7 "2 '| depth |'
rows inside ## Owned axes; the row is not unique"; M6 "revision does not resolve to a commit". For M4 and M4b the JSON is identical to the baseline run after removing `rev`,
`root` and the per-item `stated` and `observed` echoes; K1 stays `row_nm [17, 17]`, so the decoy's `3/3` is not read.

## Mutant table

| # | Mutation (depth row only) | Expected | Observed | Verdict |
|---|---|---|---|---|
| M1 | observable first N/M `17/17` to `17/18` | K1 mismatch | exit 1, 1 mismatch, K1 only, `row_nm [17, 18]` | killed |
| M1b | observable first N/M `17/17` to `16/17` | K1 and K3 mismatch | exit 1, 2 mismatches, `row_nm [16, 17]`, K3 `k1_n 16` | killed |
| M2 | evidence craft span `SKILL.md:81-314` to `SKILL.md:81-318` | K2 mismatch | exit 1, 1 mismatch, K2 only, `in_evidence_cell false` | killed |
| M3 | evidence measured hash to `638fb211` | K3 mismatch | exit 1, 1 mismatch, K3 only, command A there 9/9 against N 17 | killed |
| M4 | decoy depth row `3/3` **before** the `## Owned axes` heading | no change (row scope) | exit 0, 0 mismatches, identical to baseline | survived |
| M4b | decoy depth row `3/3` **after** the section, in `## Reconciled current state` | no change (row scope) | exit 0, 0 mismatches, identical to baseline | survived |
| M5 | second depth row inside `## Owned axes`, right after the real one | K1 K2 K3 mismatch | exit 1, 3 mismatches, "row is not unique" | killed |
| M6 | evidence measured hash to `deadbee` (unresolvable) | K3 mismatch | exit 1, 1 mismatch, "revision does not resolve to a commit" | killed |
| M7 | decoy depth row `3/3` at the **end of the `## Owned axes` body** | K1 K2 K3 mismatch | exit 1, 3 mismatches, "row is not unique" | killed |

Killed: M1, M1b, M2, M3, M5, M6, M7. Survived: M4, M4b.

## Observations

1. **K1 discriminates the denominator.** M1 (`17/18`, N unchanged) is killed by K1 alone; K3 still passes because K3 compares command A at the measured
   revision against the K1 N of 17, which did not move. M1b (`16/17`) also trips K3, since the K1 N moved to 16. K1 alone therefore does not certify the
   denominator.
2. **K2 is pinned to the exact span string.** M2 is caught with `in_evidence_cell false`; the span observed at the tip is SKILL.md:81-314. M2 reproduces a
   historical defect verbatim: at base `a0639d8e` the depth evidence cell read "craft section `SKILL.md:81-318` at `08c7a729`" — the round-25 stale span
   re-inserted.
3. **K3 is pinned to a revision that agrees with the row's N.** M3 re-inserts `638fb211`, the base-era measured hash (`git show a0639d8e:SCORECARD.md`, depth
   evidence cell: "baseline `a79945c4`, measured `638fb211`"). It resolves, but command A there gives 9/9 against the repaired N of 17, so K3 fails. The row's
   number and its measured revision are coupled; the old hash cannot be reinstated alone. M6 shows K3's second branch, an unresolvable hash, is live.
4. **The row-scope guard is active, and the decoys are not vacuous.** M4 and M4b stayed green because rows outside `## Owned axes` are never read, which is the frozen rule and the round-25
   first-row false accept. The decoy content is detectable once in scope: M7 places the identical `3/3` decoy at the end of the `## Owned axes` body, far below the three axis rows, and the
   detector reports that the row is not unique. So M4 and M4b surviving is the scope guard firing, not an inert fixture, and the guard is positional rather than adjacency-based: the section
   ends at the next line starting with `## `, not at the end of the table. [INFERENCE] — supported by M7 counting the same decoy text as a row, and by `owned_axes_rows` scanning to the next
   line starting with `## `.
5. **The instrument's own selftest agrees.** `python3 -I -B clone/tools/round-26/c2-calibration.py --selftest` gives exit 0, `cases 18, failures 0`, including
   `decoy-outside-owned-axes` at exit 0 and `k4-duplicate-row-inside-owned-axes` at exit 1. My lane-level results reproduce both behaviours.

## Limits

- The mutants attack the C2 instrument's reading of the depth row only; they say nothing about the truth of the 17/17 count itself, which is command A's
  arithmetic over `corpus/knowledge` and `SKILL.md`.
- K1, K2 and K3 as frozen do not check the depth row's prose, its last-change column, the historical claims inside the observable cell, or the coverage and
  calibration rows. A wrong denominator is caught; a wrong history string is not.
- Verdicts cover the three tips named above. A later commit that moves the craft span or the depth row re-pins K1 and K2.

## Verdict

**Holds.** Six of eight depth-row mutants are killed by the exact item they target, with no collateral items failing: M1, M1b, M2, M3 and M6 each fail only
their own item set, and M1b fails K1 and K3 as expected because it moves the N. The two survivors, M4 and M4b, are the specified row-scope guard working as
frozen, and their decoy content is demonstrably detectable once inside the section, as M7 shows. No mutant produced a false mismatch on an unmodified depth row,
and the pristine baseline is green at all three tips.

## Artifacts (under `/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC2Depth/`)

```
tip fe3eb4ed (clone/), tip 003de8cc (clone2/), tip 0375717e (clone3/)
mutate.py            bdf8299e36c7dbdb0789fa2c0f001778bd58bec3cf2f18735eb32dcbd871086f   mutants.json         fae5b9ac4a078ca91ae3dace8f19c4ed9326c9ef52bdd34a181f8f169818361c   runs/summary.txt     25b06c0a7bb9d7cbb3174c545e5af9617f5b003b6700acfeb52f824b71527c57
runs/baseline.json   d35fa2be920c11e3f369efeb45ee8b82e7e3bba4528a4d42f691b76b305ce014   runs/M1.json         1404ca14879b52ff16ea52ef95ce63f54d4ac8a83ff224e6c50a3fe981f7ceb2   runs/M1b.json        ed40292ff8ae1e9516ee13837a54958f64687dbc004294757d15b0a7c4c03d97
runs/M2.json         2123c5e14fddfa4584aab6795dd6a85d6723ec3b0f51341d102adef9beefb8a6   runs/M3.json         bf5296db620a43ec7c1037dcd5250adcaae6f22e8c7b2b7ba4d7f3e4fec73684   runs/M4.json         290c45b02f802da446175d1fbb41f97a6e962e19e30f813088e0e03bc5898f96
runs/M4b.json        f96d3833e5551c4c8dd57d18ef7e729181293d654678af2f8092a26ba4e3a8fd   runs/M5.json         ae4342d70dad697b7cb356568c974c30e5f0c186eccfa187c692b1a57b359001   runs/M6.json         a832c3c3abc743408260271b418e64e44bbb416c8fbab8b81709439da0b04c9b
runs/M7.json         682f39ac6c05ef12eb3a7546e123110a9fb53fd751b1453d63f0f02a6abdd724   mutate2.py           aef96697e675a71961ca6042ac909f8f81bca0ccf07dbb2af785abcfd73ff672   mutants2.json        c5d55626b6d7e34cf4e60e4b77eaee6acd9ef9574d5cd19d6475bb402537fb59
runs2/summary.txt    6bd368ff1b1d2c44c11eed3a4dd9e05b231530043fd65551c522cb1da24e70b5   runs2/baseline.json  6e060c447979116c2bcc986990de677217b96f750885d86f1a26c2f3a2a1c23c   runs2/M1.json        4026bfcfcbd64f23a2f57f2fd68179ab442ee8309b31e36d639c1547c1b1bc4d
runs2/M1b.json       1413c3b8b26e944ff20a782f67f0a5abe2d71d5853125c87f1fd08352bdc866b   runs2/M2.json        05ff815f47789cb4f48daf665686c26b244fca5f90a9d98c39f0ed7fbf98aebf   runs2/M3.json        55cf2e89948aca39a7841588ce4947a676245a5b3e2a6d7702e61fa0e4a9ad7b
runs2/M4.json        3540ff1a10e89c5328bf2b29b99cb99d7fcd51caf96ead7f67c0b80c6bab8402   runs2/M4b.json       2d8ff43fbbeb8aa778fde4f0db799f92eb2485e4588005076e74d73d4b461858   runs2/M5.json        c588b9da6cb313b68021a15ea8bba62908214b925b80d90500de32d5720a2721
runs2/M6.json        7a47ebddece2948b6214f53856467fcde3c19faf131b8c06f145e000c9fc2568   runs2/M7.json        96545c058fadfc57581b410a240aef207f2a7e46ee62fc84975b87147d1ea587   mutate3.py           fddb274569790fed8940f4ecdb858760fba05ae7d8d85a11a9da23fe46c2f21f
mutants3.json        abcbf6d11a39e3bcf5ae62c59eaa3d7d05f7f2f7fa36fc9f2141cd3a1065a120   runs3/summary.txt    c58b3da5f81eef08b81700160bdd53be273266ffc60ef5b06efef790a565cd84   runs3/baseline.json  32b3868a95eaa9026e9c5f5e89b1ede3505ce779c2e5ae87127fbdacf17618be
runs3/M1.json        295d6f0401cd1c99bc0cf10d6fbbce085c6175881ecaf67352b9290f577ec7fa   runs3/M1b.json       7c93ab10f26dbd090a354e25870e029219eaa58d948ab19ef867abbf0e06ca9b   runs3/M2.json        3e02689d3cf31ce2944696fb2e0a37bb1f0e5af544b5e4f24d63d0d6100397a7
runs3/M3.json        d143c5fe706d58b13b4d65e8081faeac35f35db6f3b95ae6887a0b899f5f9557   runs3/M4.json        7c8148b2cc3af520f536a9cdc6a344efc06da1cdc7ba586a437dc099ca533871   runs3/M4b.json       5f622106b8808c5e6a63cbe87c6f3865867f02e1abaa8d73f738ef10f054a76d
runs3/M5.json        ead82d80a578d57b341003d48e86fc4a3c51925f9ecb21ef62508ba4942bde1f   runs3/M6.json        3f3d81a83a37a585ff99e740a5da78d0ad05cf85d550847c7b305361e6184315   runs3/M7.json        174a73483f20aa83d0c295bfd75c719962d1e9a393e6399bcfefff5edde8aab2
```

All three clones end with an empty `git status --porcelain`. Restoration evidence: after every mutant the harness restored
`SCORECARD.md` and asserted byte equality with the pristine file; the recorded restored sha256 is `10ae7acf0b46392ab9b194f4a21c08688b539ff71ca5db747ad9e8a1e83ec74b` for all twenty-seven runs.

Report: `.ufo/waves/round-26/w2/MutC2Depth.md`
