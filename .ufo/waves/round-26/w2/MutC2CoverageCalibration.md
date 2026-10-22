# MutC2CoverageCalibration — R26-C2 items K4 and K5 attacked on the repaired rows

Seat: KaidokuR26.MutC2CoverageCalibration (mutation-tester, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Detector: frozen lane instrument `tools/round-26/c2-calibration.py`, sha256 `3b0f6507e7f77fd1763fc26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e` (unchanged since 81f63f36).
Scratch: `/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC2CoverageCalibration/`. UTC 2026-10-22T13:11:54Z–13:30Z.
No REA call, no web source, no tool installed or upgraded.

## Method

Two sandbox clones of the lane (`clone/` rooted at the C2 after-receipt commit `46ebfd2f`, `clone2/` rooted at the
then-current lane tip `16307c47`). Every mutant edits one file in the clone, is committed there, and is measured with
the same bounded detector on pristine, mutated and restored bytes:
`python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-26/c2-calibration.py --root <CLONE> --rev <MUTANT_REV>`.
All mutation and all Git writes happened in the clones; the lane was read-only (`git show`, `git log`, `git status`,
`git rev-parse`, `git diff` only; no add, commit, checkout, reset, stash or push, and no `jj` command). The lane index
sha256 read `43f95c68e5dac7cbb3c94d45a75d82bdb78d97d30660c33e1b14ef5e8a38a117` while the lane HEAD was `fe3eb4ed` and
`58b09bb67c8bede6a97df43d6279ba607c6c50b2a39df796b86bf912fb95a21a` after the L1's commits `003de8cc`, `0375717e` and
`16307c47` landed during my window (observation: the index moved only together with the lane HEAD moving under L1
commits, and it is byte-stable across repeated `git status` calls of mine).
Baseline (pristine bytes, same detector): `items 6, mismatches 0`, exit 0 at `46ebfd2f`, `fe3eb4ed`, `16307c47` and in
the lane working tree (`out/lane-pristine-16307c47.json`). K4 pass (row 109/109; command A mapped 109, knowledge_files
109; measured `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb` resolving to 109/109 there); K5 pass (measured
`c265db9bd3c0883fbaf4487f839559c85a736826`, a prefix of `result.json` `measured_revision`). Green baseline, so every
red below is a killed mutant. The instrument's selftest also passes: `--selftest` → exit 0, `cases 18, failures 0`.

## Mutant table

Base `46ebfd2f`; UTC from `out/mutation-results.json` (13:21:42Z–13:21:45Z), re-verified at tip `16307c47`
(`out/mutation-results-tip16307c47.json`, 13:29:52Z–13:29:55Z) with identical verdicts.

| # | Mutation | Expected | Observed | Verdict |
|---|---|---|---|---|
| M1 | coverage observable first N/M `109/109` → `108/108` (the base-era count) | K4 mismatch | exit 1, 1 mismatch, K4 only, `row_nm [108, 108]`, `headline_ok false`, note "coverage row N/M does not match command A at REV and at the measured revision" | killed |
| M2 | coverage evidence cell measured revision → `3395b6d` (the base-era hash) | K4 mismatch | exit 1, 1 mismatch, K4 only, `hex_after_measured 3395b6d`, command A there `mapped 78 / knowledge_files 78` against the row's 109/109 | killed |
| M3 | README `## Coverage map` row for `2026-10-22-r26-native-reader-evidence-id-identity` removed | K4 mismatch | exit 1, 1 mismatch, K4 only, command A at the mutant `mapped 108 / knowledge_files 109`, `missing ["2026-10-22-r26-native-reader-evidence-id-identity"]` | killed |
| M4 | calibration evidence cell measured revision → `75af886a` (the base-era hash) | K5 mismatch | exit 1, 1 mismatch, K5 only, `prefix_ok false`, note "the measured revision in the calibration row is not a prefix of measured_revision" | killed |
| M5a | the word `measured` removed from the calibration evidence cell | K5 mismatch | exit 1, 1 mismatch, K5 only, `hex_after_measured null`, note "no 7-40 hex revision after 'measured' in the calibration evidence cell" | killed |
| M5b | the word `measured` removed from the coverage evidence cell | K4 mismatch | exit 1, 1 mismatch, K4 only, `hex_after_measured null`, note "no 7-40 hex revision after 'measured'" | killed |
| M6 | extra README `## Coverage map` row naming a stem with no knowledge file (dangling map entry) | K4 mismatch | exit 0, 0 mismatches; command A reports `dangling ["2026-10-22-r26-nonexistent-entry"]` but `mapped 109 / knowledge_files 109` | **survived** |
| M7 | second `\| coverage \|` row inside `## Owned axes` | K4 mismatch | exit 1, 1 mismatch, K4, note "2 '\| coverage \|' rows inside ## Owned axes; the row is not unique" | killed |

Killed: M1, M2, M3, M4, M5a, M5b, M7. Survived: M6.

## Observations

1. **Every assigned mutant is killed by exactly its target item, with no collateral item failing.** M1, M2, M3 and M5b
   fail K4 only; M4 and M5a fail K5 only. Each exits 1 with `mismatches 1`. [observation]
2. **K4 pins the coverage count from two independent sides.** M1 breaks only the headline (the row's N/M no longer
   equals command A at REV) and M2 breaks only the measured-revision side (command A at `3395b6d` gives 78/78), so
   either half alone turns K4 red; M3 breaks it from the data side by unmapping one knowledge file from the README
   map. The round-25 stale values `108/108` and `3395b6d` cannot be reinstated. [observation]
3. **K5 pins the calibration row to `result.json`.** Reinstating the base-era `75af886a` is caught by the prefix
   comparison against `measured_revision` `c265db9b…`; removing the word `measured` is caught by the null-hex branch.
   The word `measured_revision` in the same cell does not satisfy the rule: `\bmeasured\b` does not match
   `measured_revision` (underscore is a word character), so M5a finds no hex at all. [observation]
4. **Row uniqueness is live on the coverage row too.** M7 (a second `| coverage |` row inside `## Owned axes`) is
   rejected as undecidable, matching the instrument's own `k4-duplicate-row-inside-owned-axes` selftest case.
   [observation]
5. **Coverage finding (M6 survived): K4 as frozen compares counts only, not map membership.** A README
   `## Coverage map` row naming a knowledge file that does not exist leaves `mapped == knowledge_files == 109`, so
   K4 stays green while the map holds a false row. The frozen rule is "N == M == command A mapped == knowledge_files";
   command A does compute `dangling`, but K4 does not read it. A coverage limit of the frozen rule, disclosed rather
   than fixed here. [observation; that a false map row is a corpus defect rather than a counter defect is my inference.]

## Limits

- The mutants attack the C2 instrument's reading of the coverage and calibration rows only; they say nothing about
  whether 109/109 is the right count, nor about the prose, the score column, the last-change column or the history
  strings inside those cells. K4's two halves are checked against command A at two revisions, so a defect keeping row
  and tree self-consistent at one wrong revision is outside the rule. Verdicts cover `46ebfd2f`, `fe3eb4ed` and
  `16307c47`; the `## Owned axes` coverage and calibration rows are byte-identical across those tips (section diff),
  so a later edit to either row re-pins K4 and K5. M6's survival is a coverage finding; the contract of K4 and K5 is
  untouched.

## Artifacts (under `/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC2CoverageCalibration/`)

```
run_mutations.py  ed3ce34fe66e1bd31fbb7523563db89bbfabc2db80e066b6e4899d5377b2bd3d   out/mutation-results.json  667f283b04d0fec5944404bbb616d77c6d3577e3bb9c21350771167ae8166273
out/mutation-results-tip16307c47.json  a2541c4d4ebdc6990811bdb9fb0f7bb3f04a8ba48f7f57fac822153df36b4e24   out/M6-tip.json  4f49fbbdcd647a518ae463ac043b31b7a99b197bc99be4c214f3777031e5249d
out/M7-tip.json  4ce6040e595a958f972e7121f3ebdd726580408cb11a23f858cb563ca19c7cf5   out/selftest.json  272b0c9ef3377dffe5324b9885938e4c88adcd2fb280005519f8fbcceb5840bd
out/lane-pristine-16307c47.json  eec2edf865403c9a093ee4d8ed6741439c3c63f321419004689551af68d58ba0   out/lane-pristine-head.json  369c5272f3b7fc2c3f63f755f630c0496f81a332c9ef028c7ed94f2efb2de4a4
fixtures/M1-coverage-NM-stale-108.patch  83447fde8fa23e0c042de1c0aee3c7635bbdfff65eb0ddaa26f2f3f75f5875aa   fixtures/M2-coverage-measured-hash-stale-3395b6d.patch  c93eae60516d94be8bc4b035778951c4dc1de11ef9cf6ed88846425e4df24bb8
fixtures/M3-readme-coverage-map-row-removed.patch  a7efe28c72d40ee900f8569ad8727073b8d96ee9755eac70fd9c7497abd35b14   fixtures/M4-calibration-measured-hash-stale-75af886a.patch  b560de02c58459f800de56c5dd12333866ea14122b7d060540db946261c1fcd2
fixtures/M5a-calibration-word-measured-removed.patch  c8625af556ecd225ad0f46d8c254a383a3e49960c8fe90c744069a6fe5187a3e   fixtures/M5b-coverage-word-measured-removed.patch  6a5e44888c0f58115db9f5a49896b01c1275b17b757c482c1d422038bb825aa6
fixtures/M6-dangling-readme-map-row.patch  6c2e83f88dfc037396792b574f7bf1a047a6e29a7a3dbc8893d6a00a2694563e
```

`clone/` and `clone2/` hold branches `mut/M1…mut/M7`; both end restored on their base rev with an empty `git status`.
After every mutant the harness restored the touched file and asserted byte equality with the pristine file:
`clone/` `SCORECARD.md` `d0798fa66f5b974f2aec7dc6e59ac2674f5e726dc4cc7b9387d40e4c64329907`, `corpus/README.md`
`ff5fc422db7f100fc98c6920f758ed06e263fa539fe00e7d42c8863039fecc00`, tree `4e8e3785d0419c95c3b37751ef258633b24743cd`;
`clone2/` `SCORECARD.md` `fbd7691cdc6d58473d6e354b50f7bb0ee320ca36bb0bde66616de9c028ea4e9d`, `corpus/README.md`
`d6723012393c3bcd15f1bf4c7b3d307acac0cc289e13f3006e9540dc5d87acec`, tree `4884d4214d946fb58d3ad0eea5958c8081cbe731`.
The detector re-run on restored bytes after each mutant: exit 0, `mismatches 0`. The seven patches re-apply cleanly
with `git am` onto `46ebfd2f` in an independent clone and reproduce the same verdicts.

## Verdict

**Holds.** The five assigned mutation points on K4 and K5 — the coverage row's first N/M token, the coverage row's
measured hash, the README map row, the calibration row's measured hash and the word `measured` itself — are all
detected by the frozen instrument, each by exactly its target item and with a green pristine baseline. One extra probe
survives: K4 as frozen does not read command A's `dangling` set, so a README map row naming a nonexistent knowledge
file is not caught. That is a coverage finding, disclosed and not repaired.

Report: `.ufo/waves/round-26/w2/MutC2CoverageCalibration.md`
