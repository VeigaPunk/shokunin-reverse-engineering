# kaidoku round 53 — claims (attempt 1, fresh-start round)

Round base `6697518f0ad8e8399567ae4c9cd0207fc7c04d8b` (lane `main` tip at round start, pushed,
`jj-lane.sh state` `ahead=0 behind=0 tracked=0 untracked=0`). This file is the round
declaration; the **freeze** is the single later commit that adds the round-53 instruments,
frozen inputs, fixtures and this file's amended text, recorded in `LOG.md` and
`.ufo/waves/round-53/l1/FREEZE` before any counting run over the scored corpus. Amendments
after wave-1 attacks land in the freeze commit and are listed in `## Wave-1 amendment record`
(empty until then); a counter bug found after the freeze is a miss, never a patch.

## Fresh-start compliance (operator rule, run-13)

The last three kaidoku closures are all `rejected-honest-stop` (`MANIFEST.json rounds[]`:
r50 @`d5db4a21`, r51 @`619e95da`, r52 @`00d0bfd0`). Their spot-checks and reports were read
first (`corpus/lessons/round-50-verifier-spotcheck.md`, `round-51-verifier-spotcheck.md`,
`round-52-verifier-spotcheck.md`, `.ufo/reports/round-{50,51,52}/kaidoku.md`). What they
teach, applied before declaring:

- r50–r52 each died re-attempting the AVM four-carrier C1 and the v6 audit as twin claims
  without landing either. The lesson (fleet §9): size to what one round lands and verifies.
  **r53 does not attempt the AVM C1 at all**; its routed findings stay routed (below). The two
  declared claims are offline over committed bytes: no REA run, no vendor fetch, no network.
- r52 routed: (1) the results handoff lacks per-seat id/status → this round's dispatch shape
  carries `status.json` per seat and the orchestrator's `r53-w1-results.json` carries
  name/agent/id/status per row; the record oracle atom T3 counts them; (2) the 19 W04
  duplicate-URL warnings stand as named debt unless a census-safe correction set lands (below);
  (3) the inherited `.ufo/waves/round-50/w3/ScribeEntryC1.md` modification was committed by the
  run-12 wrap-up commit `6697518f` — resolved, named here; (4) SHONEN boxes 1–2 cite pointers a
  non-author could verify — they stay `[~]`: a subagent this lane dispatches is still the lane.
- Each declared claim is measured against a do-nothing control the cheapest work-skipping path
  cannot pass (control receipts committed before any data commit; §9).

**Lowest-axis rule.** Owned axes coverage/depth/calibration sit tied at 10.0 (`SCORECARD.md`
`## Owned axes`; none retired): every owned axis is a lowest axis, so both claims satisfy the
rule. **Stagnation nudge:** saturation line 10.0, window N=10, last capability round 49 — r53
is round 4 of the window, so the nudge has not fired; the round is not obliged to be a
frontier/capability move and declares none.

## R53-C1 — depth: triage table v6, the fixture-level reader census, and the executability audit

Surface moved: `SKILL.md` `## Queue-drain craft` — rule block 26 (triage table v5) gains block
27 (table v6) plus the frozen executability audit. The one ddwrt FAILED no-pad body
`dmg_Z3_v3ddwrt_inode_table` is routed `legacy-body-failure`/`cross-read-legacy` by the v5
family-cell narrowing, but the frozen reader evidence says **no independent reader executes
that cross-read on those bytes**: the family census is fixture-level, `squashfs_v3_ddwrt` is
6/7 NO-READER, and the same no-reader refusal marks seven `clean`-labelled ddwrt envelopes
whose extraction only sasquatch performed. A prescribed action the frozen census says cannot
run is a depth defect; seven `clean` labels that a no-reader family sibling (`clean-unverified`,
block 26) would refuse are the same defect mirrored. Resolved findings, each with its landing:
CritTriV6 F1 (drop the `census_outside` clause — census3 stays its own gate), F2 (move the
seven no-reader `clean` envelopes to `clean-unverified`; 8 pair changes total, scope declared
here before data), F3 (freeze the fixture→reader table with lineage and explicit audit scope),
F4 (first-match precedence stated; the new row precedes `legacy-body-failure` and duplicates
`no-reader-failure`'s action under a narrower trigger — declared, not accidental), F5 (label
`legacy-body-refused`, not `unreadable` — the measured fact is reader refusal, never damage),
F6 (kill-control swap uses `cross-read-legacy`, the non-vacuous pair), F7 (census rows carry
command/exit/UTC lineage where committed evidence provides it; rows without it are marked
declared-not-recaptured, never silently recaptured); MutTriV6 F1 (the before-arm is a frozen
witness script, not the v5 instrument's `--table` flag — `tools/round-50-c3/` holds no table
file and its `--freeze` gate refuses a base-descending freeze), F2 (the v6 row keys on the
**fixture census**, never the bare family: a synthetic reader-backed ddwrt FAILED body must
still route `cross-read-legacy`; family-key mutants are red on that witness), F3 (the
census-clause arithmetic is dropped with the clause), F4 (carryover counts +1: v5 corpus is
126 envelopes, the v6 battery is scored over the same 126); CritClaims F2 (before-arm witness
at the base) and F3 (separability — no census coupling in either predicate).

**Claim:** land **triage table v6** as `SKILL.md` rule block 27 (dated supersession of block
26's ddwrt routing; block 26 stays as history) plus the scoring instrument
`tools/round-53/sqfs-triage-v6.py` (ports `tools/round-50-c3/sqfs-triage-v5.py`), the frozen
fixture-level reader census `tools/round-53/reader-census.json`, and the before-arm witness
`tools/round-53/v5-baseline-witness.py`, such that:

- **Predicate** (the same sentence in this file, the instrument docstring, and the receipt
  label): at a REV descending from the R53 freeze, with every frozen path unchanged, running
  `python3 -I -B tools/round-53/sqfs-triage-v6.py --root <LANE> --rev <REV> --freeze <FREEZE>
  --envelopes <DIR> --json-out <OUT>` exits **0** with `pair_mismatches 0`,
  `evaluator_missing 0`, `executability_violations 0`, `clean_residue 0`, and a green
  selftest; and at the declared base the frozen witness command
  `python3 -I -B tools/round-53/v5-baseline-witness.py --root <LANE> --rev 6697518f0ad8e8399567ae4c9cd0207fc7c04d8b
  --freeze <FREEZE> --envelopes <DIR> --json-out <OUT2>` exits **1** with
  `executability_violations 1` naming `dmg_Z3_v3ddwrt_inode_table` and `clean_residue 7`
  naming the seven no-reader `clean` envelopes. `<DIR>` is the committed corpus
  `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes` (126 envelopes; same
  disclosed limit as R50-C3 — depth over the scored corpus, not held-out generalization).
- **The v6 changes (all before any data):** (1) new row `legacy-body-refused` → action
  `preserve-unresolved`, trigger = FAILED body (`extractor-failure+`, 0 published) of a
  fixture the frozen census marks NO-READER, placed before `legacy-body-failure`; (2) the
  `legacy-body-failure` row narrowed to reader-backed fixtures (census condition), cause text
  stating the census condition; (3) the seven no-reader ddwrt `clean` envelopes route
  `clean-unverified`/`record-unverified` (the census condition on the `clean` row, mirroring
  block 26's no-reader-family rule); (4) first-match precedence: census-conditioned rows
  decide before family rows; the evaluator implements the identical precedence as an
  independent code path over the same frozen census; (5) the **executability audit**: for
  every FAILED-body envelope whose prescribed action prescribes a cross-read, the audit
  checks the frozen census and counts a violation when no reader backs those bytes;
  `clean_residue` counts `clean`-labelled envelopes whose census rows are NO-READER.
- **Frozen census:** `tools/round-53/reader-census.json` — one row per ddwrt fixture (15
  envelopes) plus the no-reader families' fixtures, each row: fixture id, reader outcomes
  (reader name, command, exit, UTC) **or** `lineage:` pointers to the committed evidence
  (`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, the round-50 census tables, S250/
  S251 ground) with `recaptured: false`. Fresh recapture is attempted only where a committed
  mksquashfs recipe exists; a recapture that contradicts the lineage is a kill rule: stop
  before the freeze, report the contradiction. No new reader is claimed validated.
- **Controls (scored with the frozen instruments BEFORE the data, receipts committed):**
  do-nothing (the witness at base → red, the receipt below); junk table (syntactically valid,
  wrong labels → `pair_mismatches > 0`, exit 1); audit-guard-deleted mutant → red;
  family-key mutant (v6 rows keyed on the bare family) → **red on the synthetic
  reader-backed ddwrt FAILED-body witness** (fixture scope; corpus-vacuous by design and
  declared); swapped-action mutant (`preserve-unresolved` ↔ `cross-read-legacy`) → red;
  `clean-unverified`-suppressed mutant → red. Kill rule: any green-that-should-be-red at the
  freeze → stop before data, report as a miss.
- **Before (measured, already committed):** the v5 table at the base routes
  `dmg_Z3_v3ddwrt_inode_table` `legacy-body-failure`/`cross-read-legacy` (SKILL.md block 26
  at `6697518f`, marker `<!-- sqfs-triage-table v5 -->`), and the seven no-reader `clean`
  envelopes keep `clean` — the witness receipt is the before-arm receipt.
- **After:** the v6 counters at the landing REV; receipts
  `.ufo/waves/round-53/l1/scores/c1-{before,after}.json` (before = witness at base; after =
  v6 instrument at the landing).
- **Registry:** exactly one `instrument-registry v2` row each for `sqfs-triage-v6.py` and
  `v5-baseline-witness.py`; the census JSON is a frozen input pinned by sha256 in the
  `instruments` map, not a registry row; no other code files land under `tools/round-53/`.
- **Score binding:** depth row's rule-block citation proxy 26/26 → 27/27 at the landing
  (command A's craft-section rule, re-run and recorded in the round record).

## R53-C2 — calibration: the round-53 record oracle over committed bytes

Surface moved: the round's own record (SCORECARD round-53 section, LOG entry, wave
accounting, receipts, SOURCES/census receipts) re-derives from committed bytes with a frozen
counter — the r49/r50 calibration shape (`tools/round-50/c2-record.py`), ported to ten atoms
`T1..T10`. Calibration here is measured exactly as fleet `AXES.md` defines it: mismatches
between the lane's self-assessment and observed repo state, counted by a counter any reader
can re-run.

**Claim:** land `tools/round-53/r53-record.py` such that:

- **Predicate** (the same sentence in this file, the instrument docstring, and the receipt
  label): at a REV descending from the R53 freeze, running `python3 -I -B
  tools/round-53/r53-record.py --root <LANE> --rev <REV> --freeze <FREEZE> --base
  6697518f0ad8e8399567ae4c9cd0207fc7c04d8b --json-out <OUT>` exits **0** with `mismatches 0`
  over atoms T1–T10; and at the freeze itself the same command exits **1** with exactly
  `mismatches 8` — T3, T4, T5, T6, T7, T8, T9, T10 red (landing-only atoms), T1 and T2 green.
- **Atoms** (each names its SCORECARD line; the counter parses the declared value from the
  committed record text and checks it against observed state — record-vs-reality, not
  record-vs-target, so C2 verifies the record's honesty independently of C1's success):
  - **T1** the claims file exists at REV and its `instruments` map pins, by sha256, every
    file the freeze added under `tools/round-53/`, and the pins re-derive at REV.
  - **T2** LOG.md carries the round-53 declaration entry at REV citing this file's commit;
    `git diff --name-status <base> <REV> -- LOG.md` shows no deletion.
  - **T3** the wave line: one v1 wave `r53-w1`, the declared seat count; countable as: that
    many seat dirs under `.ufo/waves/round-53/w1/`, each with parseable `status.json`
    (`seat`,`role`,`status`,`summary`,`artifacts`), settled+blocked+failed equal to the
    section's numbers, and `r53-w1-results.json` rows each carrying `name`,`agent`,`id`,
    `status` with `id` nonempty.
  - **T4** every receipt path named in the record section exists at REV, parses (JSON), and
    its revision/`rev` field equals the landing hash the section names; declared exit codes
    match.
  - **T5** the census receipts: the census-start receipt exists at the recorded path with the
    recorded exit code; the census-end receipt exists with exit 0 and the W04 warning count
    the section states.
  - **T6** SOURCES: the section's before→after row counts equal the census grep counts at
    base vs REV; every new row id named exists at REV with the named tier; each new row's
    `used-by` paths exist.
  - **T7** the record section exists in SCORECARD.md at REV and its declared atom-value
    lines re-derive (the section's `T1..T10` table itself — the oracle's self-anchor).
  - **T8** no-harm: the three Owned-axes rows are byte-equal (rstrip-normalized) base→REV;
    PROVINCE.md byte-equal base→REV; `corpus/README.md`, SKILL.md, tools/ diffs only where
    the record declares them, each declared path checked, each undeclared production path
    red.
  - **T9** the freeze ledger: the round's freeze row present in `corpus/claim-freezes-v2.tsv`
    and the committed freeze-gate receipt (`tools/round-29/freeze-gate.py --disclosures` at
    REV) exists with exit 0.
  - **T10** the misroot-sweep receipt exists and its finding list matches the record
    section's misroot line.
- **Before:** at the freeze, `mismatches 8` (the eight landing atoms red; T1/T2 green) — the
  do-nothing control receipt is this run, committed before any data commit.
- **Controls (pre-data, receipts committed):** junk record (a forged section with wrong
  numbers → `mismatches > 0`, exit 1); forged receipt (declared receipt whose `rev` differs →
  red); falsified-wave line (seat count wrong vs the seat dirs → red); battery: ≥10
  committed mutations, each flipping exactly its own atom or failing the run, none a no-op.
- **Counting command:** the predicate command, run at the freeze (before receipt) and at the
  landing REV (after receipt): `.ufo/waves/round-53/l1/scores/c2-{before,after}.json`.
- **Registry:** exactly one `instrument-registry v2` row for `r53-record.py`.

**Separability:** C1 is verifiable without C2 (its counters read SKILL/tools/census/envelopes
only) and C2 without C1 (its atoms cross-check the record's statements against whatever
landed; a C1 honest failure recorded honestly keeps T4/T7 green). The claims share no write
surface except the record sections in SCORECARD.md/LOG.md (separate sections).

## Routed, not attempted this round

The AVM LE-SquashFS C1 (coverage) stays unattempted; its durable pre-freeze findings stay
routed to the round that declares that re-freeze: CritRuleDerive F-1/F-3 (`removed.kinds`
channel; decidable kill rule), CritRetry F1–F6 (retry policy inadmissible as written;
exhausted-ENOENT exit semantics), CritFetchChain F1–F3 (stale-carrier fail-closed; guard
selftests on the named file), CritCounterV2 F1/F2/F3 (rule sha in receipt; receipt mutation;
retry evidence erasure), CritClaims F1/F4/F5 (closure/live command split; retry control;
the false "readers succeeded" rationale — C1's census resolution F2 supersedes that
rationale for the v6 scope only). Named in the round report and lesson; nothing here
narrows or amends the r50/r51/r52 frozen targets.

## Frontier step (inside the claim cap)

- **Sourced claim:** C1's landing entry cites the round's new SOURCES row **S253** (the
  sasquatch project README/usage — reader-refusal ground for legacy SquashFS variants),
  opened this round by the L1 and a scout; per QUALITY 45 the claims file names `claim_row:
  S253` and the v6 counter accepts only that row for the entry's new-source citation.
- **Census:** before = `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  kaidoku` receipt at round start; end = the same command at the filing tip, exit 0 required.
- **Mistakes mined** into `corpus/lessons/round-53.md` `## Mistakes`: (1) the r52 claims file
  quoted r51's retry disposition with an invented qualifier (class `reference-drift`;
  captured-by none — a claims-file citation is not a Gate quote; fix: claims citations quote
  prior dispositions verbatim with file:line; QUALITY row lands only if shown able to fail);
  (2) the r51/r52 handoffs omitted per-seat id/status (class `attribution`; captured-by
  QUALITY 22; fix: per-seat `status.json` + id/status results rows, demonstrated by atom T3).
- **W04 duplicates:** the 19 warnings stay debt unless a row-by-row audit lands a
  census-safe correction set under CORPUS.md rule 2 (supersedes rows); any landed correction
  is logged old→new in the lesson; otherwise one report line carries the debt.
- **Assimilation:** the scout scans `/home/vgpnk/Projects/shokuknow/merge/kaidoku/`
  (read-only); the round adopts ONE theme + 1–3 entries only if the id-collision scratch
  check and the scratch mirror pass `sources-census.sh validate --file` exit 0 before any
  append; else the report says `Assimilation: none` with the scan receipt. `considerthese/`
  does not exist in this lane; one report line says so.

## Wave shape (run-13: 16–32 seats)

**One v1 wave, `r53-w1` = 25 seats** under `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`
(band 16–32): executor 7 (V6 port, witness, census, record oracle, controls, misroot-sweep
helper, census3 regen), scribe 3 (sources/W04 audit, lesson scaffold, knowledge entry draft),
scout 3 (S253 opening, census verification, merge-package scan), reviewer 3 (v6 port, record
oracle, claims/freeze-chain), critic 3 (v6 design, record atoms, round shape), mutation-tester
2 (v6 battery, record battery), connector 2 (sibling overlap, cross-source), sentinel 1,
revenger 1 (v5 gate ancestry semantics). Attack roles reviewer+critic+mutation-tester+
sentinel+revenger = **10/25 = 40 %** (strict reviewer/critic/mutation-tester = 8/25 = 32 %).
The §3 planner seat is the L1 (the validator rejects `planner`). Dispatch through the inline
spawn handoff (`r53-w1.ready`), never a direct `task` call; no residual wave — the wave
carries build and attack together. Per-seat `status.json` before yield; results rows carry
id/status; dead seats stay dead in the evidence. The L1 alone runs the counting commands
after the wave (freeze → controls → before-arms → landing → after-arms).

## Wave-1 amendment record

(empty until wave-1 attacks land; amendments land in the freeze commit)
