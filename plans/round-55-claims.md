# kaidoku round 55 — claims (carry-in repair round: the four routed round-54 closure defects)

Round base `79421b757f36b2ddb776631ecfd57d42dc2f33e2` (lane `main` tip at round start,
pushed; the round-54 verifier spot-check commit, whose section 5 routed four
status-neutral defects to this round). This file is the round declaration; the
**freeze** is the single commit that adds the round-55 wave artifacts (census-start
receipt, before-arm receipts, the round-55 instrument receipts) and the claims
container `.ufo/waves/round-55/claims.json`, recorded in `LOG.md` and
`.ufo/waves/round-55/l1/FREEZE` before any repair data lands. The freeze pins two
new instruments committed with the declaration, `tools/round-55/corrections-pin.py`
(sha256 `f71e6b2135ccd9b3a71bb7d9f78ff1a6a063b0ce4a4208edc9841a48aec9d40a`) and
`tools/round-55/v6-block-digest.py` (sha256
`22785c1e47b61cc807f99f1ef3fecc5aa5203e90b8e4ba5bee7eedcc2a8f741c`); both bytes are
frozen from the declaration commit onward and are named in the container's frozen
atoms so the R29 gate audits them. L1-inline round: no wave surface exists on this
host (the kaidoku round-53 L0 question stays open and unanswered; routed around,
never treated as answered).

## Fresh-start compliance (operator rule)

The last three kaidoku closures are `rejected-honest-stop` (r50 @`d5db4a21`,
r51 @`619e95da`, r52 @`00d0bfd0`; dispatch digests quoted in the rendered round
prompt section 7). Their lessons (`corpus/lessons/round-50.md`,
`round-51.md`, `round-52.md`), the r53 and r54 spot-checks, and the r54 plans'
fresh-start section were read before declaring. Ruled out this round, with reasons:

1. **AVM LE-SquashFS Frontier→Core (the r50/r51/r52 twin claim).** REA 6.5.0,
   sasquatch/sasquatch-v4be, unblob and vendor fetches are measurably absent on this
   host (PROVINCE `## Host migration — 2026-10-31`); three consecutive rounds died
   re-attempting it; the routed findings stay routed, untouched.
2. **A second declared claim beyond the carry-in pair.** r51/r52 both failed on a
   second declared claim that could not land; this round declares exactly the two
   claims the carry-in work already grounds, both offline over committed bytes.
3. **A registry-drift census (r53's sized-out census3 item).** Stays planned; it
   needs its own sizing pass and would repeat the r51/r52 over-declaration shape.
4. **Any wave dispatch.** No dispatch surface on this host (L0 open); L1-inline.

Section 9 sizing: both declared claims close artifacts and instruments that do not
exist at the base (a tip-run receipt, correction rows, a reproducible-digest
instrument and receipt, a convention row, a mechanical pin with registry and
capability rows) — a do-nothing control cannot reach them; the before-arm receipts
at the base prove the open state.

**Lowest-axis rule.** Owned axes coverage/depth/calibration sit tied at 10.0
(`SCORECARD.md` `## Owned axes`; none retired): every owned axis is a lowest axis,
so C1 (calibration) satisfies the rule. **Stagnation nudge:** saturation line 10.0,
window N=10, last capability round 49 — r55 is round 6 of the window, so the nudge
has not fired; the round is not obliged to be a frontier/capability move (C2 is one
anyway, by claim type).

claim_row: S255

## R55-C1 — calibration: the four routed round-54 closure defects close with committed, content-checked artifacts

Surface moved: the round-54 record's receipted completeness against its own filed
claims — the record must match reality (fleet `AXES.md` calibration definition).
The r54 closure's section 5 routed four status-neutral defects; each closes with an
artifact that exists and verifies at the measured revision, never by prose alone:

- **(a) tip gate run (spot-check 5.1)** — the freeze gate is executed at the r54
  close tip `90f3a9b9…` and the receipt lands:
  `.ufo/waves/round-54/l1/scores/freeze-gate-tip-90f3a9b9.json` (wrapper: command,
  exit, gate stdout verbatim; expected exit 0, disclosures exact 29 of 29, no stray,
  the round-54 gate row CLEAN). The byte-identity argument the closure used remains
  true and is now redundant: the receipt exists.
- **(b) "only executed instrument" wording (spot-check 5.2)** — correction rows:
  `corpus/lessons/round-54.md` gains an appended `## Corrections (round 55)` block
  naming BOTH executed instruments as frozen (`tools/round-53/r53-record.py`, three
  record receipts; `tools/round-53/sqfs-triage-v6.py`, the landing re-score,
  `c1-v6-at-landing.json`); the LOG declaration entry of this round carries the
  appended correction pointing at the superseded text; the filed r54 report is
  fleet-owned and stays as filed — the correcting round's report carries the
  correction, per the protocol's correction rule.
- **(c) v6-table digest not reproducible (spot-check 5.3)** —
  `tools/round-55/v6-block-digest.py` defines THE extraction (marker line through
  the last consecutive `|`-leading line, LF-joined with one trailing LF) and
  `.ufo/waves/round-55/l1/records/v6-digest-repro.txt` carries the command and its
  outputs at the round-53 base, the r54 landing, the r54 close tip and the r55
  base: full digest `946e535947ba6d17da9f4b1ca7993af285e66103547a5c2107b253e5dd204bcc`
  (23 lines, 8961 bytes) at all four revisions. The receipt DISCLOSES that the r54
  receipt's 16-hex prefix `b340ed2b48facca7` was NOT reproduced — neither by this
  extraction nor by the r54 closure's three independent boundaries nor by an
  extraction battery of ~100 boundaries run this round (probe script retained in
  the round scratch, sweep transcribed in the receipt) — so the unpinned value is
  superseded by a reproducible command with its full digest, and a correction
  inside the receipt names the superseded text. The claim under test (byte-identity
  base→landing) stands under the pinned command.
- **(d) D1 anchoring + mechanical pin (spot-check 5.4 / section 3 observations)** —
  two parts, both landed: (i) `corpus/QUALITY.md` gains an appended row 101 stating
  the anchoring convention for provenance fields that land inside a correction
  block (list items naming their field, receipts checking them grep unanchored and
  say so); (ii) the mechanical pin itself is claim C2 below.

**Predicate (before → after), measured by counting commands:**
- Before (receipt `.ufo/waves/round-55/l1/scores/c1-before.txt`, committed at the
  freeze): at the base each of the four closures is absent — 0/4 present (the tip
  receipt path absent by `git cat-file -e`; no `## Corrections (round 55)` block in
  the r54 lesson; no `tools/round-55/v6-block-digest.py` and no extraction command
  line in the r54 c2-after receipt; no anchoring row in QUALITY and no
  `tools/round-55/corrections-pin.py`).
- After (receipt `.../c1-after.txt`, committed with the record): 4/4 present and
  content-checked at the measured revision (the receipt parses with exit 0 and the
  CLEAN verdict; the correction block names both instruments; the digest receipt
  names the command and the four identical full digests and the disclosure; row 101
  present; the pin's selftest and both demonstrations green/red as declared).
- Kill rule: any artifact present but failing its content check at the measured
  revision is a miss, reported, never waived.

**Do-nothing control:** the before-arm receipt (0/4 at the base) — the closures
cannot exist without this round's work. **Separability:** C1 reads no C2 surface
(the pin's registry/capability rows are C2's); C2 verifies without any C1 artifact.

## R55-C2 — depth, capability acquisition: a mechanical pin for append-only TSV ledgers

Surface moved: the corrections-ledger governance gap the r54 closure observed
(section 3, observation a: "convention-governed only — no mechanical pin refuses an
in-place edit of a corrections row"). The new instrument
`tools/round-55/corrections-pin.py` is a gate that reads an append-only TSV ledger
at two revisions from git objects (S255 grounds the revision-pinned blob read) and
returns 0 only when the bytes at `--rev` are the bytes at `--base` plus appended
lines; every other difflib opcode is a named finding (`row_edited`, `row_deleted`,
`row_inserted`, `header_changed`). Exit map 0/1/2 (clean / failed /
could-not-evaluate). Self-test: `--selftest`, 11 in-memory fixture cases asserting
exit class and finding id per case.

**Predicate (before → after):**
- Before (receipt `.../scores/c2-before.txt`, committed at the freeze): at the
  base the pin does not exist (`git cat-file -e` fails), no SKILL registry row and
  no SCORECARD capability row names `corrections-pin` (grep counts 0).
- After (at the measured revision): the gate exists, its `--selftest` passes 11
  cases with 0 failures; its SKILL instrument-registry row exists (gate, verdict
  map, self-test spelling, pinned-value path, write scope, owner); its SCORECARD
  capabilities row enters this round; and two committed demonstrations run:
  (green) the corrections ledger `c753b24f…→<measured rev>` — clean, rows 2,
  appended 0; (red) the historical round-53 in-place verdict edit on
  `corpus/claim-freezes-v2.tsv` `fe8fab8d→f78fc766` — exit 1 naming line 29
  `round-53`, which is precisely the event QUALITY row 100 governs and the event
  the closure said no mechanical pin refused.
- Kill rule: a selftest failure, a red demonstration that fails to go red, or a
  green demonstration that goes red at the measured revision is a miss.

**Do-nothing control:** the before receipt — the pin, its rows and its
demonstrations cannot exist without this round's work.

## Frontier step (inside the claim cap)

- **Sourced claim:** C2 rests on the round's new SOURCES row **S255** (git-show
  documentation, git-scm.com, opened this round; snapshot bytes and sha256
  `.ufo/waves/round-55/l1/s255/`): "For plain blobs, it shows the plain contents"
  (DESCRIPTION) is the named ground for reading a ledger's bytes from a revision
  rather than a worktree — a verdict names the revision it was measured against.
- **Census:** round-start receipt `.ufo/waves/round-55/l1/census-start.txt` (the
  host-adapted census command; exit 0, 19 standing W04); the same command at the
  filing tip is the end receipt, exit 0 required.
- **Mistakes mined** into `corpus/lessons/round-55.md` `## Mistakes` (lead item:
  the r54 digest-without-command receipt authoring class).
- **W04 duplicates:** the 19 warnings stand as named debt (no census-safe
  supersedes set this round); one report line carries the debt.
- **Assimilation:** `considerthese/` does not exist in this lane (measured at
  round start); the shokuknow register is unreachable from this host; the report
  carries `Assimilation: none — shokuknow unreachable`.

## Wave shape

No wave: no dispatch surface on this host (kaidoku round-53 L0 question open and
unanswered; routed around). All work L1-inline; the measurements are the two new
frozen instruments plus plain shell/git counting commands over committed bytes.
