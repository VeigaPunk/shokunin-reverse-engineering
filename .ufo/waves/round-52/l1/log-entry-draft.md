# LOG.md round-52 entry (draft; append-only, lands at the landing commit)

## 2026-10-30 — round 52 (KaidokuR52): the device-accounting law re-frozen and measured; triage v6 executability audit

Round base `c525de54a53eb3c4fee28ede2721da4527cf8ece`; claims draft
`ab0eafedc41402b43b41a4362084119578dfe7ce` (plans/round-52-claims.md, ports the round-51
declaration with its wave-1 amendments F1–F11 baked in); wave-1 dispatch
`1842addcef3458515859b928b92d9bbd0a46c5d5` (64 seats, v2 policy, one batched swarm through
the inline spawn handoff). Freeze commit: FREEZE-HASH-PLACEHOLDER. Landing commit:
LANDING-HASH-PLACEHOLDER.

- R52-C1 (coverage): law-derived gap rule (required.char-device=false, device kinds allowed=[]),
  counter v2 with law_shape_ok / census_rederived_ok / depth_gap_recorded / re_scored_pins,
  controls CTL-OLD 2/4 (reproducing the round-50 miss) and CTL-NEW 4/4, mutations M1–M4 red
  per the frozen battery; carrier re-fetch through the pinned vendor chain
  (/fast/scratch/hyaku/kaidoku-r52/carrier-cache/, vendor bytes never committed); REA data run
  per carrier; predicate carriers_matched == 4 → LE AVM members Frontier → Core.
  RESULT-PLACEHOLDER (receipt .ufo/waves/round-52/l1/scores/c1-after.json).
- R52-C2 (depth): triage table v6 as SKILL.md rule block 27 (legacy-body-unreadable /
  preserve-unresolved for FAILED bodies of no-reader families) + instrument
  tools/round-52/sqfs-triage-v6.py with the frozen executability audit; before 1 violation
  (dmg_Z3_v3ddwrt_inode_table) at the claims-draft base over the v5 table bytes, after 0;
  census_outside 0 both sides (census3 inherited). RESULT-PLACEHOLDER (receipts
  .ufo/waves/round-52/l1/scores/c2-before.json / c2-after.json).
- Frontier step: S252 opened (man7 mknod(2), EPERM/CAP_MKNOD ground, L1 + ScoutMknod
  second-read); census before exit 0 / 158 rows (sources-census-start.txt); assimilation
  RESULT-PLACEHOLDER; mistakes mined into corpus/lessons/round-52.md ## Mistakes.
- Routed-defect repairs this round: interpolation check (check-dispatch.py, M51-6), per-seat
  status.json + wave-accounting.py (r51 closure item 2), band-respecting round shape (64-seat
  v2 wave + falsify wave), fetcher guard selftests (defect 4), misroot-sweep helper (defect 5),
  census W04 duplicates RESULT-PLACEHOLDER (fixed subset or named debt), carried L0
  kaidoku | round-50 unchanged.
