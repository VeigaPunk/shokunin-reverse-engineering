# R26 wave 2 seat RerunC2Counter — C2 counting command re-run

Seat: KaidokuR26.RerunC2Counter. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin,
base a0639d8e61e486e2a716ff94cddd89a73200a02c, claims frozen at c27f445e70cedbaf5300b2fd0a53e821d9b659a9.
Scope: re-run the R26-C2 counting command at four revs, run --selftest, compare the
instrument sha256 with 3b0f6507e7f77fd1763fc26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e
at each commit after 81f63f36. Lane untouched: read-only git only, no checkout, no jj.

## Commit order (observed)

git -C <lane> log --oneline -15, run 2026-10-22T12:59:32Z, exit 0. Oldest to newest:
a0639d8e (base) -> c27f445e (claims freeze) -> 81f63f36 (instrument) -> ebe2cb4a ->
46ebfd2f (C2 repair) -> bd0c84bc -> c3277726 -> fe3eb4ed (HEAD). Observation.

## Runs of the counting command (observation; producing runs 2026-10-22T13:01:37Z, capture re-run 13:02:26Z, all exit codes as shown)

Command for each rev (cwd = lane, python 3.14.8):
`env TMPDIR=<seat>/tmp python3 -I -B tools/round-26/c2-calibration.py --root <lane> --rev <REV>`

- REV a0639d8e (base): output JSON, `"items": 6, "mismatches": 5`, EXIT=1.
  Mismatch items K1, K2, K4, K5, K6; K3 passes (measured 638fb211 gives 9/9, matching
  the stale 9/9 row). Matches the claims' before_expected wording exactly.
- REV c27f445e (freeze commit): `"items": 6, "mismatches": 5`, EXIT=1, same item set.
  Inference: identical to base because the freeze commit only adds claims/census bytes
  and does not touch SCORECARD, SHONEN, SKILL.md or PROVINCE.md.
- REV 46ebfd2f (C2 repair): `"items": 6, "mismatches": 0`, EXIT=0. K1 17/17 equals
  command A rule_blocks 17 == citation_resolved_rules 17; K2 finds SKILL.md:81-314;
  K3 measured ebe2cb4a... resolves to 17/17; K4 109/109 at REV and at measured
  ebe2cb4a...; K5 measured c265db9bd3c0883... prefixes result.json measured_revision;
  K6 line after the box line has contains_contested false and both PROVINCE pointers
  inside 303 lines.
- REV c3277726 (routed fixes): `"items": 6, "mismatches": 0`, EXIT=0, same values as
  46ebfd2f (no SCORECARD/SHONEN-relevant bytes changed by that commit).

Every run printed complete JSON and exited; no run hung, errored or wrote to the lane.

## Acceptance: does 5 to 0 of 6 hold

Holds (observation). Before repair (a0639d8e, c27f445e): 5 of 6, exit 1. After repair
(46ebfd2f, c3277726): 0 of 6, exit 0, exactly the claims target {items 6, mismatches 0,
exit 0}. The K3-only-pass prediction in the claims' before_expected is what the
instrument observed at both pre-repair revs.

## Selftest (observation; 2026-10-22T13:01:37-38Z)

`env TMPDIR=<seat>/tmp python3 -I -B tools/round-26/c2-calibration.py --selftest`:
`{"selftest": "c2-calibration", "cases": 18, "failures": 0, ...}`, EXIT=0, wall 1.0 s.
Detail: 1 green case, one red fixture per item K1-K6 plus k6-contested-red (all counted,
exit 1), decoy '| coverage |' row outside ## Owned axes not read (exit 0), duplicate-row
and mutated-rows cases counted, bad-revision case exits 2. Consistent with the claims'
fixtures rule including the decoy.

## Instrument byte pin (observation; commands run 2026-10-22T12:59-13:02Z)

- sha256sum of the working-tree tools/round-26/c2-calibration.py = 3b0f6507e7f77fd1763f
  c26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e — equals the pinned digest.
- git ls-tree at 81f63f36, ebe2cb4a, 46ebfd2f, bd0c84bc, c3277726 and HEAD fe3eb4ed all
  give blob 0e2b3043ab3bc0e7f5a9a9af5805b46f59422948; git cat-file blob of it hashes to
  the same 3b0f6507... digest. So the instrument is byte-identical at every commit after
  81f63f36, including HEAD, and the runs above judged every tree with the same bytes.
- At a0639d8e and c27f445e the script is ABSENT in the tree (ls-tree empty). Consistent
  with the freeze_kind INSTRUMENT_ABSENT disclosure; those revs were measured by the
  committed instrument reading Git objects at REV, per the claims counting_command.

## Residual risk and verification gaps

- The instrument's command A logic (SCORECARD recipes, README map walk, rule-block
  counting) is taken as the frozen definitions; this seat re-ran the counter, it did not
  independently re-derive command A from first principles (inference: covered by the
  instrument's own selftest red fixtures, but an outside reimplementation could still
  diverge on an edge case such as nested headings inside ## Measurement recipes).
- K4's 109/109 reflects the tree after C1's entry landed (coupling disclosed in claims);
  no independent recount of knowledge files was made here (unknown here, delegated by
  design to the frozen instrument).
- Capture files under <seat>/raw are byte re-runs at 13:02:26Z; the first observation
  batch ran at 13:01:37Z with identical exits and counts. Both are retained.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/w2/RerunC2Counter)

- raw/c2-a0639d8e.txt sha256 eb12dad66807626eb30d12b3b0477f77a82831ca9db7392b66a364a106c09beb
- raw/c2-c27f445e.txt sha256 ece2b7952974f05a55abad7fbdea7971ea5d7a4f661945f1b288f7d9599d5480
- raw/c2-46ebfd2f.txt sha256 1453b3a4fc22210aa40fab8d510d0e6a47c69b1f18c4438d31a734ef58670628
- raw/c2-c3277726.txt sha256 549f62e76b2507482ed833ae529598d54fb340ecc4f45c9cd8f3c5855312f153
- raw/selftest.txt sha256 67adbaacd3734c3b3b76d734bb15311f1b95a9dd2fa17e5d2f3c46694cfa27cf
- raw/blob-at-head.txt sha256 214001b7e9ab2ad61e3fc0c2046798cd0b4d747d2c4eac2ce73d4983eddf2a95
- raw/python-version.txt sha256 f615dc9512de8b165e2b595e5cdc608a3ba7927ae92f959c5b42ec3d58e2ffa8
- tmp/ used as TMPDIR for all runs; selftest scratch removed by the instrument itself.

## Tooling

No tool installed or upgraded; system python3 3.14.8 and git only (directive channel
order not exercised). No pacman, uv, npx or REA call was needed for this scope.
