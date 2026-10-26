Draft for L1 integration (seat `R40W2Scorecard`, round 40 wave 2). This entry is appended to `LOG.md`
by the L1; nothing here is written into the lane by this seat. Claim numbers are the frozen counters'
at `42c10a58cb2cae3a4a0122af35a0cf95ac718043`; owned-axis counts are command A at
`4d62ee5a86b4692a13f682b29ed7975e8d7e5326` (`artifacts/R40W2Scorecard/cmdA.txt`).

---

## 2026-10-26 — round 40: genuine AVM-layout BE SquashFS v4 measured but not promoted (honest stop on a counter suffix false negative); a triage table with a scored action column at 26/26 on freeze-seeded held-out data

- Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`. Freeze `7fce308631a8b457d6b7c5a4b39a923c4e9a49de`:
  both claims, every round-40 tool, the four C1 carriers with their independent oracles and the gap
  rule, the SKILL triage v2 block 19 and its entry, S123 and the wave-1 evidence. Wave 1 ran 42 seats
  against the draft before the freeze (42 non-empty outputs; every change from the draft is named in
  `plans/round-40-claims.md` `## Changes from the draft`). Owned axes were tied at 10, so both are
  lowest: R40-C1 works coverage, R40-C2 depth.
- Controls `45e89864e967d7501110b529cb8517b26b92c7ef` land before any claim data: the C1 do-nothing
  receipt at the freeze (exit 1, `carriers_matched 0`, every documentation binding false), the C1,
  C1-extra and fetch-vendor selftest receipts (70 cases 5 green/65 red with `failures []`; 7/7; 8/8),
  and the C2 counter at the freeze (exit 2, `no_manifest_at_rev`). No control meets either target under
  its own rule: the C2 shortcuts top out at 24/26 (`CTL-C2-4`, `CTL-C2-5`, `CTL-C2-6`).
- R40-C2 data `2d1ac5bcd08f6828dbfdee9054bbeec0ea211b33`: `tools/round-40/heldout-gen-v2.py --seed
  7fce3086… --run` writes 26 carriers over 13 classes × 2 with per-carrier envelope and run records and
  a manifest whose `seed` is the freeze hash, first added after the freeze and no later than its
  envelopes. R40-C1 receipts `73c7bf9c73bd7b4891c4e46c93d1d29c287e4541`: four REA 6.5.0
  `extract-firmware --max-depth 1` receipts (V1, V2, L1, L2). Vendor bytes are never committed (the AVM
  licence); `tools/round-40/fetch-vendor.py` rebuilds them from the pinned chain into a cache and the
  counters read `--carrier-cache`.
- R40-C1 landing `42c10a58cb2cae3a4a0122af35a0cf95ac718043`, score
  `c17565bc772dd296deeaf1699fbe737c6afbea3c`, honest-stop record
  `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`: the frozen counter scores **3 of 4**, `met_target false`, exit 1. V1 publishes 697/697
  oracle regular files, V2 8/8, L1 7/7, L2 6/6; the AVM layout holds on all four (`sqsh` 4.0,
  `mkfs_time == bytes_used` at 5442392 / 26013550 / 230884 / 241390, little-endian metadata block
  lengths where decidable — V1 1380 vs 25605, V2 704 vs 16386, L2 identity, L1 plausibility 932 vs
  9347), compression ids 4/4/4/1 all covered, and every gap within the frozen rule (V1 264 = 263
  `unpublished-entry` + 1 `depth-limited` on 381 non-regular entries, the char device invisible; V2 86
  = 85 + 1 on 95; L1 3 = 2 + 1 on 13; L2 3 = 2 + 1 on 10). All documentation bindings are true and the
  supplementary gate `c1-extra.py` is met (exit 0).
- The one miss is a counter false positive on a path suffix, visible inside the frozen evidence rather
  than argued: L2's receipt records two `unpublished-entry` gaps, at `firmware.bin_extract/bin/busy`
  and `firmware.bin_extract/usr/bin/ls` (both symlinks), while the same counter's
  `nonregular_published` lists `firmware.bin_extract/usr/bin/busy` — the regular file `usr/bin/busy` of
  `oracle.tsv`, whose path ends with the symlink path `bin/busy` (`same_rel` is equality or
  `endswith('/' + rel)`, `tools/round-40/c1-counter.py:606-607`). No symlink path was published. Verdict
  **NOT MET**, honest stop: the round-39 AVM sentence stands, the Core row was demoted at `4d62ee5a` to
  `## Round-40 measured, not promoted (R40-C1 honest stop)`, and the round-40 frontier note says
  measured-not-promoted.
- R40-C2 score at `42c10a58`: **26/26**, `bindings_false []`, `frozen_paths_changed []`,
  `met_target_consistent true`, exit 0; 13 classes × 2, 12 distinct (label, action) pairs, the
  out-of-domain envelope labelled `unclassified` with action `none`, v1 table 3086 B and v2 table
  6603 B byte-identical at the freeze and at the measured revision, and the interpreter exits 2 on the
  base `SKILL.md` (v2 marker absent). **MET.**
- Freeze integrity: both scores report no frozen-path change between the freeze and `42c10a58`, and
  every score receipt records the scorer's exit code through `tools/round-40/score-receipt.sh` (routed
  R39-CL6). The C2 instruments' selftest case counts (c2-counter 42, sqfs-triage-v2 45, heldout-gen-v2
  6) are declared in `plans/round-40-claims.md` and the round-40 registry; the 42-case run is recorded
  in wave-1 build evidence (`w1/R40C2Counter.md` §E1, `cases 42 pass 42 fail 0`), not as a controls
  receipt, so no C2 selftest receipt is claimed beyond that pointer.
- Surfaces: two knowledge entries — `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` (landed
  `42c10a58`) and `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` (landed at the freeze) — both
  mapped in `corpus/README.md` (coverage map `:95-96`, knowledge map `:207-208`, frontier bullet
  `:250`); S123 at the freeze and S124–S126 at the landing (registry 122 → 126 rows, appends only);
  `PROVINCE.md` carries the measured-not-promoted record, the round-40 frontier note and the demotion.
  Command A at `4d62ee5a`: coverage 128/128 → **130/130** (`missing []`, `dangling []`), depth
  18/18 → **19/19** (`citation_resolved_rules 19`, craft section `SKILL.md:81-375`, v2 marker `:361`).
- Owned scores: coverage 10 → 10, depth 10 → 10, calibration 10 → 10 (no calibration claim this round;
  the r1 rubric value 9/9 stands). Both improved proxies are perfect finite counts, so no axis retires
  and no score moves. Capabilities: one row entered — SquashFS `extract-firmware` outcome triage v2
  (label + action, 11-token action column, out-of-set `unclassified`, 26/26). **No AVM-BE capability
  row**: C1 stopped, and a measured-not-promoted record is not a capability.
- Disclosed limits carried from the claims: the C1 rerun shows the carrier extracts through the pinned
  toolchain at scoring time and cannot prove which process wrote the committed receipt; REA records no
  extractor argv on success, so the absence of `-be` is shown by the AVM handler branch and direct
  `unblob -v` logs, not by the receipt. C2: a table with one load-bearing cell per label can also score
  a closed class set, the `cause` column is prose and unscored, and operation and provider change
  together in the out-of-domain class, so the provider cell is not tested alone.
- Wave 2 (38 seats, dispatched `0b15c8b2`) is falsifying the landing. At draft time of this entry no
  wave-2 finding is adjudicated; the L1 completes the scorecard's wave-2 record after the wave settles.
  Two observations are already recorded from committed bytes: the 3/4 figure is bound to `42c10a58`,
  because the demotion renames the heading and `c1-extra.py`'s `frontier_content` also goes false at
  `4d62ee5a` (the carrier, oracle and receipt blobs are byte-identical across the two revisions), and
  the worktree at `0b15c8b2` carries an uncommitted `SKILL.md` `+19`-line `### Round-40 instrument
  registry` section that L1 must commit or drop.
- Tool installs: none in this round's commits and none by this seat; the pinned toolchain stays as
  recorded in the round-36/38 entries (`sasquatch`/`sasquatch-v4be` 4.5.1, unblob 26.6.4, rea-agents
  6.5.0).
