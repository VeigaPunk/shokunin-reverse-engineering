# CritTriV6 — r52-w1 report (R52-C2 pre-freeze attack)

Verdict: the v6 design is **not freeze-ready**. The one-pair envelope change is real; the claim's
premise, its audit inputs, and its census coupling are not. Full text, evidence and the ordered
fix list: `.ufo/waves/round-52/w1/CritTriV6/findings.md`.

Findings (severity):
1. **HIGH — census clause couples C2 to C1.** At `ab0eafed` census3 exits 0. Adding the seven
   required round-52 registry rows with the census unchanged gives census_outside = 7, exit 1.
   "census_outside 0 after" needs an unnamed census regeneration, and C2 then fails when C1 lands
   alone, breaching the claims' separability sentence. Drop the clause; keep census3 as its own gate.
2. **HIGH — "their readers succeeded" is false; residue is 7, not 2.** Seven ddwrt-family `clean`
   envelopes sit on NO-READER bytes (three nopad: `be.nopad_ddefault`, `le.nopad_ddefault`,
   `dep_A2`). The round-50 census and the round-49 `v3-readers.out` both show both readers refusing
   the nopad bytes. Only sasquatch succeeded. Also inconsistent: Z3 is downgraded for reader refusal
   while the healthy bytes on the same refusal stay `clean`. Choose: keep seven as disclosed residue
   (one pair), or move seven to `clean-unverified` (eight pairs, scope amendment).
3. **HIGH — before=1 is reproducible only under an unfrozen mapping.** No damaged subject digest has
   a census row; v1 and v2 have no family row; the 6/7 table is not in the round-49 entry the claim
   cites. Only a majority-family rule gives 1→0, and it contradicts the v5 evaluator's reader-backed
   ddwrt. Freeze a family→reader table with lineage and an explicit audit scope.
4. **MEDIUM — new row duplicates `no-reader-failure`; precedence unspecified.** Same action and
   cause, two labels for one condition. The one-pair result needs first-match precedence or a
   narrowed legacy cell, and the claims state neither.
5. **MEDIUM — `legacy-body-unreadable` implies damage.** The measured fact is reader refusal. The
   claim's "cannot be executed" is wrong: the cross-read runs and returns refusal. The defect is an
   unsupported inference, not a non-executable action. Rename to a refusal label.
6. **MEDIUM — the swap-action kill control is vacuous.** New-row action = `no-reader-failure` action
   (`preserve-unresolved`), so swapping flips zero pairs and the "none a no-op" rule cannot be
   satisfied. Swap with `cross-read-legacy` instead.
7. **MEDIUM — reader matrix not honestly captured.** `reader-census.txt` has no per-row command,
   exit or UTC. Recapture at landing with per-row capture under a frozen path.
8. **LOW — embedded v5 draft and landed SKILL block differ in prose**; scoring unaffected; derive
   the v6 baseline from landed bytes.
9. **LOW — circularity.** The rule, evaluator and audit all read the same 126 envelopes; the claim
   discloses it.

Verified, not contested: the one-pair set `{dmg_Z3_v3ddwrt_inode_table}` (P1); base census exit 0;
nine FAILED envelopes and their v5 labels; the nopad reader refusals agree across the two receipts.

Answers to the four questions: (1) label/action overstated, envelope change exactly one pair;
(2) yes, red-before can come from the mapping, not ddwrt (F3); (3) scope creep and a separability
breach, keep out of v6 (F1); (4) `clean` on the nopad envelopes is not on valid grounds (F2).

Receipts: `.ufo/waves/round-52/w1/CritTriV6/receipts/` — `probe_v6_attack.json` and
`probe_v6_attack.receipt.txt` (exit 0), `census-coupling.receipt.txt`. Probe script:
`.ufo/waves/round-52/w1/CritTriV6/probe_v6_attack.py`.

Exercised: read-only inspection of the claims, v5 instrument, round-50 c3 receipt, round-42
envelope corpus, round-49/50 reader receipts, round-51 census3; offline probes; registry-row
simulation in a scratch clone of the lane at the claims base. Not run: v6 implementation, its
controls, the canonical judge, REA, downloads, or any commit/stage/push in the lane.

Tools installed: none.
