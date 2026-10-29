# kaidoku round 50, attempt 2 — claims (re-dispatch after the run-11 wrap-up release)

Base `8ccc05e6b073d4218223571d0b390f6e93789d94` (lane `main`, attempt-1 tip, pushed). Attempt 1
froze R50-C1/R50-C2 at `435d41fd4ad9211d1579fc447936fb33d2b74467` and landed C2 (met at
`11ccdb7211bf9f632a1d6bc4a9a44106d5c42b42`); C1 was left unmeasured (REA `provider_timeout` at
host load 95–176) and the operator wrap-up released the round without a closure, so the driver
re-dispatched round 50. This attempt runs the SAME round number and resumes C1 under the SAME
frozen bytes: **no new C1 freeze, no amendment** — the predicate, counter, kill rule, carriers,
oracle and control fixtures are exactly the committed freeze bytes, verified unchanged at this
attempt's start (`git diff --stat 435d41fd 8ccc05e6 -- tools/round-50/ plans/round-50-claims.md
tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` is empty; receipt
`.ufo/waves/round-50/l1/frozen-unchanged-attempt2.txt`). M50-6's fix is applied as process, not
as an instrument change: the REA-dependent controls are scored and the data run is executed in
the quietest window this attempt can find, with each REA step's load and attempts recorded.

Owned axes coverage / depth / calibration sit tied at 10 (none retired): every owned axis is a
lowest axis. **R50-C1 works coverage (resumed); R50-C3 works depth (new this attempt).** They
are causally separable: C1 reads the four chain-pinned vendor carriers (never committed), the
frozen oracle/gap tables and controls under `tools/round-50/`, its REA receipts under
`corpus/evidence/round-50/c1/`, and the documentation bindings (entry, `PROVINCE.md` round-50
section, `corpus/README.md` coverage map, SOURCES rows S243/S244/S245/S249, SCORECARD capability
row). C3 reads `SKILL.md`, the round-42 recon envelope corpus, and its own new instrument; its
only landing surfaces are `SKILL.md` (new rule block 26), the new instrument file, its registry
row, and the SCORECARD/LOG record. The two claims share no write surface except `SCORECARD.md`
and `LOG.md` record sections (separate sections, landing order C3 then C1) — each is verifiable
without the other having landed.

## R50-C1 — coverage (resumed, predicate unchanged)

The rule is the frozen text: `plans/round-50-claims.md` section "R50-C1" (byte-identical to the
counter docstrings; `mkplan.py --check` re-verifies at scoring time). Restated pointer only:

- Target: `carriers_matched == 4`, every binding true, `frozen_path_changed []`, exit 0, at a
  REV that descends from the freeze and first-adds the after-receipts after it.
- Before (this attempt's re-measurement): the frozen counter at `--rev 435d41fd… --freeze
  435d41fd…` exits 1 with `carriers_matched 0` (fresh receipt alongside the attempt-1 one).
- Controls scored BEFORE any data run (frozen order): CTL-C1-0..C1-4 and POS via
  `tools/round-50/c1-controls.py gen` + `score`; receipts under
  `.ufo/waves/round-50/controls-attempt2/`. Kill rule unchanged: CTL-C1-0/1/2/4 meeting the
  target, or the do-nothing tree scoring any carrier clause green, stops C1 before data.
- Data: `tools/round-50/c1-run.sh after --id <id> --carrier <CACHE>/<pin>.bin --data-run` per
  carrier, L1 only; carriers materialised by `tools/round-50/fetch-vendor.py` into
  `/fast/scratch/hyaku/kaidoku-r50/carrier-cache/` against the frozen chain pins.

## R50-C3 — depth: triage table v5, the no-independent-reader rule the v4 table lacks

Surface moved: `SKILL.md` rule block 21 (table v4) mis-routes the three SquashFS handler
families that have **no independent second reader** — `squashfs_v2_nonstandard`,
`squashfs_v3_broadcom`, `squashfs_v3_nonstandard` (round-49 w2 `W2Skill.md` findings F1 and F2,
routed and unfixed at this base; the round-49 landing fixed F3/F4/F5 only):

- F1: the `legacy-body-failure` row's `failing handler` glob `squashfs_v[123]*` matches the
  no-reader families, and its cross-read rule ("if the independent readers fail where sasquatch
  failed the body is damaged") condemns a **healthy** no-reader body, for which reader failure
  is guaranteed by definition, not evidence of damage.
- F2: the `clean` row gives a no-reader run the oracle-backed action `none` ("match files to the
  oracle") where no oracle can exist; the four committed v2ns `_ddefault` recon envelopes label
  `clean`/`none` today, contradicting the Frontier status those families hold in
  `PROVINCE.md`/the round-49 entry.

Claim: land **triage table v5** as `SKILL.md` rule block 26 (the next free craft-block number;
blocks 22-25 are the freeze-integrity/meaning blocks; dated supersession of block 21's
routing/action columns for the no-reader families; block 21 stays as history) plus the scoring
instrument `tools/round-50-c3/sqfs-triage-v5.py`, such that:

- **Path rule (measured, not assumed):** both frozen round-50 counters freeze the WHOLE
  `tools/round-50/` tree — seat-measured on a fixture clone (wave-3 `ExecFetchDry`:
  `c1-counter.py` `frozen_drift = ['tools/round-50/sqfs-triage-v5.py']` → C1 exit 2;
  `c2-record.py` `freeze_check = frozen_path_changed`) — so the C3 instrument lands at
  `tools/round-50-c3/` (outside every frozen walk; B9's census covers `tools/round-49/**` +
  `tools/round-50/**` only, so the outside path needs no row for B9, and the lane registry
  still gets one as a gate-registration duty).

- **Predicate** (the same sentence in the counter docstring, this file, and the receipt label):
  at the measured revision REV, with FREEZE an ancestor of REV, frozen paths untouched, running
  `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <LANE> --rev <REV> --freeze <FREEZE>
  --envelopes <DIR> --json-out <OUT>` exits 0 with `pair_mismatches 0`, `evaluator_missing 0`,
  `table_labels == evaluator_labels` on every envelope of the frozen held-out dir, `selftest`
  green (every committed mutation flips ≥1 pair, none a no-op or cross-flip, do-nothing red);
  and at the base REV the same command exits 1 with the no-reader `*_ddefault` rows among the
  mismatches.
- **Frozen rule details (wave-3 attack amendments, folded BEFORE the C3 freeze; CritC3Design
  C3-1/4/5/6, RevTriageV4 H1/H2, ExecRegistryRow 5b):**
  - before-run `--rev` is the exact declared base `f890bbea…` (SKILL, the v4 evaluator and the
    held-out envelopes are byte-identical to `8ccc05e6…` — seat-measured empty diff — but the
    declared base is what the receipt names).
  - the `legacy-body-failure` `failing handler` cell becomes the comma-separated alternation
    `squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt`, matched as ANY-of-exact-alternatives
    (per-alternative `fnmatch`, so plain names are exact): positive matcher tests for all four,
    negative for `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`
    (H2: no single glob expresses this set; a silent `squashfs_v[123]` swap is the mutation to
    catch).
  - the no-reader set is handler-level and frozen: {`squashfs_v2_nonstandard`,
    `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`} — worded "no validated complete
    independent oracle" (broadcom has a partial 7-Zip listing; a no-reader FAILURE label never
    suppresses a successful partial cross-read). `squashfs_v3_ddwrt` stays reader-backed (R42
    Core, backhand-cli oracle); its two no-pad `_ddefault` envelopes keep `clean` under table AND
    evaluator (v5 changes nothing for ddwrt) — their known v4 residue (reader-refused no-pad
    bodies) is unchanged by this claim and needs a body-variant discriminator that does not
    exist in the scored features; disclosed, not fixed, here.
  - expected before-state: the seat-measured **19** no-reader `clean/none` `_ddefault` rows
    (4 v2ns + 7 v3_broadcom + 8 v3_nonstandard; ExecRegistryRow 5b), not just the four v2ns.
  - v5 implements the duplicate-handler-glob table refusal its docstring claims (H1: v4's
    docstring over-claims it; v4:455-459 refuses only duplicate labels), with a selftest case.
  - controls are SEMANTIC reds: the junk table stays syntactically valid (unique labels, a
    catch-all clean pair) and must exit 1 with `pair_mismatches > 0`, never exit 2; the guard row
    named by the guard-deleted control is `clean-unverified`; the corpus has ZERO no-reader
    extractor-failure envelopes (38 no-reader rows = 19 clean + 19 depth-limited), so the
    `no-reader-failure` row/action is witnessed by a committed SYNTHETIC zero-file
    extractor-failure envelope in the selftest fixtures, and deleting or swapping that exact
    row/action flips its synthetic pair.
- **Evaluator**: ported from `tools/round-42/sqfs-triage-v4.py` (the lane's scored evaluator
  pattern, R41-C2/R42-C2/R43-C1), written from this claim's precedence text: (1) a handler
  family with no independent reader (v2ns, v3_broadcom, v3_nonstandard per the round-49 entry's
  reader census) takes the new labels `clean-unverified` (run completed, gaps `none`, >0 files →
  action `record-unverified`: uncorroborated, never `clean`) and `no-reader-failure` (sasquatch
  failed, 0 files → action `preserve-unresolved`: the failure stands unresolved — reader absence
  forbids both the damaged-body verdict and the broken-extractor verdict); (2) the reader-backed
  v1/v2/v3/v3_ddwrt/v4 families keep the v4 rows exactly, with `legacy-body-failure`'s
  `failing handler` cell replaced by the frozen comma-list alternation above (the reader-backed
  v1/v2/v3/v3_ddwrt families).
- **Held-out dir**: the round-42 recon envelope corpus
  `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/` (126 envelopes, committed since
  round 42). **Disclosed limit:** these are not fresh data — v4 scored 78 of them at R43-C1 and
  W2Skill re-read the four v2ns rows. The claim is depth (the rule the table adds), not held-out
  generalization; the before-state is measured, not assumed.
- **Counting command**: the predicate's command, run twice — before at the declared base
  `--rev f890bbea…` (exit 1 with the seat-measured **19** no-reader `clean/none` `_ddefault`
  rows mismatched: 4 v2ns, 7 v3_broadcom, 8 v3_nonstandard) and after at the
  landing REV (exit 0). Receipts under `.ufo/waves/round-50/l1/scores/c3-{before,after}.json`
  → `.ufo/waves/round-50/c3/{c3-before,c3-after}.json`.
- **C3 freeze (before any C3 data)**: one commit adding this file's C3 section (already),
  `tools/round-50-c3/sqfs-triage-v5.py` (instrument + evaluator + selftest + committed mutation
  battery) and its `instrument-registry v2` row. Controls scored with the frozen instrument
  BEFORE the table lands, receipts committed: do-nothing (v4 table at base → red), junk table
  (every row `clean` → red), guard-row-deleted mutant → red, swapped-action mutant → red. If the
  do-nothing control is green, the instrument is broken — re-design before data, never after.
- **Kill rule**: do-nothing green at the freeze, a committed mutation leaving its pair green or
  flipping the wrong pair, or a no-op mutation, stops C3 and is reported as a miss.
- **Registry (B9 coupling)**: the new `.py` file gets exactly one `instrument-registry v2` row
  (gate|probe kind, verdict map 0/1/2, selftest spelling, pinned-value path), so the frozen C2
  atom B9 stays green at the new REV; no other `.py`/`.sh` lands under `tools/round-50/`.

## Landing order and shared-file rules

1. C3 freeze (instrument + registry row), C3 controls + before-run receipts.
2. C3 table (rule block 26) lands in `SKILL.md`; C3 after-run.
3. C1: controls-attempt2 receipts, data run, entry `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`
   (the stem the FROZEN counter pins — `tools/round-50/c1-counter.py` constants `entry`/`stem`
   `2026-10-28-r50-avm-le-squashfs-core`, `core_heading` `## Round-50 additions to Core`, `frontier_mark`
   `Round-50 frontier note`, `opened` `2026-10-28`, `prov_base` `/fast/scratch/hyaku/kaidoku-r50`; this file's
   first draft wrongly named a `2026-10-29-r50-le-avm-hsqs-core` stem and is corrected by this commit before any
   data — the counter, not this file, is the rule), `PROVINCE.md` `## Round-50 additions to Core` + frontier note,
   `corpus/README.md` coverage-map row, SOURCES rows S243/S244/S245/S249 (opened 2026-10-28,
   re-opened 2026-10-29 this attempt) listing the entry in `used-by`, SCORECARD capability row +
   Owned-axes coverage head `140/140` (B1 stays green), attempt-2 SCORECARD/LOG/lesson sections.
4. C2 consistency at the final REV: `tools/round-50/c2-record.py --rev <final> --freeze
   435d41fd…` exits 0 (`atoms_total 11`, `mismatches 0`) — the record stays green at the new tip;
   B1's head is updated in the same commit as the entry.

## Frontier step (inside the claim cap)

- Sourced claim: C1's entry cites S243 (Freetz AVM_LE/AVM_BE patch), S244 (AVM download index),
  S245 (unblob 26.6.4 LE handler), S249 (AVM licence) — all opened 2026-10-28 (attempt-1
  receipts under `.ufo/waves/round-50/w1/C1Src*/`), re-opened 2026-10-29 with fresh receipts at
  `.ufo/waves/round-50/l1/srcs-attempt2/` and copies under `corpus/evidence/round-50/c1/index/`.
- Mistakes mined this attempt append to `corpus/lessons/round-50.md` `## Mistakes` (M50-7+).
- Assimilation: theme AVM LE (attempt-1 Gate reaffirmed; staged S206 re-grounded as S243; the
  two refused staged entries stay refused with their reasons restated); `considerthese/` does
  not exist in this lane (one report line).

## Round shape

Two v1 waves (policy `ufo-wave-policy.json`, band 32–64 each), round total 64–128: **w3 build**
(~40 seats: source re-opens, entry/rows drafts, C3 instrument build + attacks pre-freeze,
binding drafts) and **w4 falsify** (dispatched after w3 settles and the landing, ~36 seats:
re-run each counting command, attack each claim and new row, mutation-test the v5 instrument,
re-open the new SOURCES rows). Attack roles ≥25% round-wide; a few connector seats per wave;
the §3 planner seat is the L1 (validator rejects `planner`). Waves are dispatched through the
inline spawn handoff (`<wave>.ready`), never by the L1 calling `task`.
