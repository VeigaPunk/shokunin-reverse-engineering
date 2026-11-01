# kaidoku round 54 — claims (repair round: the ten routed round-53 record defects)

Round base `45c6878634c16caa8e3e63472b30e439581b3a0d` (lane `main` tip at round start,
pushed; the round-53 verifier spot-check commit). This file is the round declaration;
the **freeze** is the single later commit that adds the round-54 wave artifacts
(census-start receipt, before-arm transcripts, the record receipts, the S254 snapshot)
and the claims container `.ufo/waves/round-54/claims.json`, recorded in `LOG.md` and
`.ufo/waves/round-54/l1/FREEZE` before any repair data lands. The freeze pins one
instrument, the frozen `tools/round-53/r53-record.py` (bytes unchanged since round 53;
pin re-derived in the container), which this round executes for two receipts; no new
counting instrument is introduced — every claim is measured by plain counting commands
(`git show`/`git cat-file`/`grep`/`wc`/`python -X utf8 -I -c` over committed bytes)
pasted in the report and SCORECARD record. L1-inline round: no wave surface exists on
this host (the kaidoku round-53 L0 question stays open and unanswered; routed around,
never treated as answered).

## Fresh-start compliance (operator rule; last three closures r50-r52 rejected-honest-stop)

The last three kaidoku closures are `rejected-honest-stop` (r50 @`d5db4a21`,
r51 @`619e95da`, r52 @`00d0bfd0`; dispatch digests quoted in the rendered round prompt
§7). Their lessons, the r53 spot-check (`corpus/lessons/round-53-verifier-spotcheck.md`,
this base) and the r53 plans' fresh-start section were read before declaring. Ruled
out this round, with reasons:

1. **AVM LE-SquashFS Frontier→Core (the r50/r51/r52 twin claim).** REA 6.5.0,
   sasquatch/sasquatch-v4be, unblob and vendor fetches are measurably absent on this
   host (PROVINCE `## Host migration — 2026-10-31`); three consecutive rounds died
   re-attempting it; the routed findings (CritRuleDerive, CritRetry, CritFetchChain,
   CritCounterV2, CritClaims) stay routed, untouched. A do-nothing control cannot
   reach it — but neither can this host.
2. **The registry-drift census `census3` outside-13 (r53's planned second item).**
   Stays routed: this round's first-priority obligation is the ten routed record
   defects; declaring the census on top would repeat the r51/r52 failure shape
   (a second declared claim that does not land).
3. **A portability pass over the frozen instruments (r53's planned third item).**
   The frozen instruments' bytes are pinned by the r53 container (T1 re-derives the
   pins at any descendant rev); a "pass" that patches them in place would break the
   committed record, and a ported copy is a new instrument needing its own freeze,
   battery and registry rows. Sized out; stays planned, never a silent patch.
4. **Any wave dispatch.** No dispatch surface on this host (L0 open); L1-inline.

§9 sizing: both declared claims close artifacts and conventions that do not exist at
the base (receipts, a corrections ledger, a convention row, committed retention
artifacts) — a do-nothing control cannot reach them; the before-arm receipts at the
base prove the open state.

**Lowest-axis rule.** Owned axes coverage/depth/calibration sit tied at 10.0
(`SCORECARD.md` `## Owned axes`; none retired): every owned axis is a lowest axis, so
C1 (calibration) satisfies the rule. **Stagnation nudge:** saturation line 10.0,
window N=10, last capability round 49 — r54 is round 5 of the window, so the nudge
has not fired; the round is not obliged to be a frontier/capability move.

claim_row: S254

## R54-C1 — calibration: the nine routed-record defects close with committed receipts

Surface moved: the round-53 record's receipted completeness — the record must match
reality (fleet `AXES.md` calibration definition), and the non-author closure routed
ten status-neutral defects; nine of them are closable in lane-owned surfaces (the
tenth, the block-27 prose, is C2). Each closes with an artifact that exists and
verifies at the measured revision, never by prose alone:

- **D1 (provenance trio)** — `corpus/knowledge/2026-10-31-r53-triage-v6-reader-census.md`
  gains an appended `## Corrections (round 54)` block carrying `verified-at:` and
  `recheck:` (CORPUS provenance-trio rule); the landed header stays byte-identical.
- **D2 (dangling pointer)** — the same correction block re-points the control digest
  to `.ufo/waves/round-53/l1/s253/digests.txt` and names its value
  (`89ff4a11…4c4`); the absent `control-sha256.txt` path is never created.
- **D4 (receipts)** — the asserted-but-unreceipted C2 artifacts land:
  `c2-selftest-receipt.json` (the frozen oracle's `--selftest`, 32 cases) and
  `c2-control-battery.txt` (junk-record / forged-receipt / falsified-wave arms driven
  over the frozen oracle in a scratch fixture; the ≥10-mutation arm is the selftest).
- **D5 (correction convention)** — `corpus/QUALITY.md` gains row 97 (a landed
  freeze-ledger verdict row is never edited in place; a correction is an appended row
  in the new companion ledger `corpus/claim-freezes-corrections.tsv`), and that
  companion ledger lands with `round-53/correction-1` recording the r53 in-place
  verdict correction event (predicted verdict landed, corrected in place at
  `fe8fab8d`/`f78fc766`, disclosed in LOG and M53-6).
- **D6 (390-hit retention pointer)** — the over-broad sweep's listing is committed
  as `.ufo/waves/round-54/l1/misroot/r53-broad-sweep-retained.txt` (regenerated
  2026-11-01; count drift vs 390 disclosed inside), and correction entries in LOG and
  the SCORECARD record section re-target the pointer that `misroot-sweep.json` and
  the round-53 SCORECARD section point at the filed report.
- **D7 (35-vs-31)** — a dated erratum entry states the two counts with their counting
  commands: the round-50 receipt table carries 35 rows; the pinned
  `tools/round-53/reader-census.json` carries 31 fixture rows + 1 derived lineage +
  4 family totals (the JSON is authoritative).
- **D8 (lesson Gate)** — `corpus/lessons/round-53.md` gains an appended dated Gate
  correction with explicit rejected-candidate rows (LEARNING.md Gate format), and the
  round-54 lesson's own `## Gate` carries candidates/admitted/rejected/spot-check.
- **D9 (tip reproduction)** — `c2-after-tip-7c0630ce.json` receipts the r53 report's
  unreceipted reproduction claim: the frozen oracle at rev `7c0630ce…`, freeze
  `6ead6f1b…`, exits 0 with `mismatches 0`.
- **D10 (E11 revision)** — `census-e11-repro.txt` reproduces the M53-4 census E11
  failure from committed bytes (SOURCES@94efae0d + the S253 row verbatim + the entry
  present + the lesson absent on disk → exit 1, `E11 S253 missing used-by
  corpus/lessons/round-53.md`).

**Predicate (before → after), measured by counting commands:**
- Before (receipt `.ufo/waves/round-54/l1/scores/c1-before.txt`, committed at the
  freeze): at the base each of the nine closures is absent — 0/9 present and correct.
- After (receipt `.../c1-after.txt`, committed with the record): at the measured
  revision 9/9 present and correct, each content-checked (the selftest receipt reads
  `cases 32, fail 0`; the battery reads all arms red; the E11 line present with exit 1;
  the digest in the correction equals the `digests.txt` line; corrections-ledger row
  count = 1; erratum counts 35 vs 31+1+4 pasted; lesson Gate reject rows ≥ 3; the
  broad listing exists with its count line).
- Kill rule: any artifact present but failing its content check at the measured
  revision is a miss, reported, never waived.

**Do-nothing control:** the before-arm receipt (0/9 at the base) — the closures
cannot exist without this round's work. **Separability:** C1 reads no C2 surface
(SKILL.md is not in any C1 atom); C2 verifies without any C1 artifact.

## R54-C2 — depth: SKILL rule-block 27 prose and its scored table agree

Surface moved: `SKILL.md` `## Queue-drain craft` rule block 27's prose bullet. The
landed table's `clean` row carries census cell `*` under the two census-conditioned
guard rows (the A10 correction), while the prose still attributes
`partial,readable` to the clean row — a prose/table drift inside the landed block
(routed defect 3).

**Predicate (before → after):**
- Before (receipt `.../c2-before.txt`, committed at the freeze): at the base,
  `git show <base>:SKILL.md | grep -c 'row itself narrows its census cell to
  \`partial,readable\`'` = 1 (the drifted clause), and the v6 table's `clean` row in
  the marker block carries `*`.
- After (at the measured revision): the drifted clause count is 0; the prose states
  the `legacy-body-failure` narrowing (whose cell IS `partial,readable`) and the clean
  row's `*` under the guard rows; the table bytes between the `<!-- sqfs-triage-table
  v6 -->` marker and its table end are byte-identical base → measured revision
  (`git diff` word-empty); the frozen `tools/round-53/sqfs-triage-v6.py` re-run at the
  measured revision over the round-42 corpus exits 0 with `pair_mismatches 0`,
  `evaluator_missing 0`, `executability_violations 0`, `clean_residue 0` (receipt
  `.../scores/c1-v6-at-landing.json`); and command A's map/citation proxies hold
  (142/142 mapped, `citation_resolved_rules 27`) — no axis harmed.
- Kill rule: any table-byte drift or a v6 red run at the measured revision is a miss.

**Do-nothing control:** the before receipt — the drift cannot fix itself.

## Frontier step (inside the claim cap)

- **Sourced claim:** C1's D5 rests on the round's new SOURCES row **S254** (RFC 6962,
  Certificate Transparency, rfc-editor plain text, opened this round; snapshot bytes
  and sha256 `.ufo/waves/round-54/l1/s254/`): the append-only log model — a log
  misbehaves by "violating its append-only property by presenting two different,
  conflicting views" (§7.3) — is the named ground for the correction-entry convention:
  a ledger is corrected by appended entries that name what they correct, never by
  editing filed rows into a conflicting view. The convention's craft value is the
  lane's own freeze-ledger history (the r53 in-place event); S254 grounds the
  append-only form, not the lane rule.
- **Census:** round-start receipt `.ufo/waves/round-54/l1/census-start.txt`
  (`scripts/sources-census.sh validate --root <fleet> <explicit lane dir>` — the
  host-adapted form; exit 0, 19 standing W04); the same command at the filing tip is
  the end receipt, exit 0 required.
- **Mistakes mined** into `corpus/lessons/round-54.md` `## Mistakes`.
- **W04 duplicates:** the 19 warnings stand as named debt (no census-safe supersedes
  set this round); one report line carries the debt.
- **Assimilation:** `considerthese/` does not exist in this lane (measured at round
  start); the shokuknow register is unreachable from this host; the report carries
  `Assimilation: none — shokuknow unreachable`.

## Wave shape

No wave: no dispatch surface on this host (kaidoku round-53 L0 question open and
unanswered; routed around). All work L1-inline; the record receipts are produced by
the frozen round-53 instrument plus plain shell/python counting commands.
