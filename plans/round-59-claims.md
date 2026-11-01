# kaidoku round 59 — claims (the D58-1 annotation contradiction closes append-only, and the annotation-consistency gate becomes an instrument)

Round base `df62b6f986fb460847037482e0199cdf1541e393` (lane `main` tip at round
start, pushed = origin/main; the round-58 verifier spot-check commit, which
admitted r58 and routed one status-neutral item to this round: **D58-1** — the
after-receipt `.ufo/waves/round-58/l1/scores/c1-after.txt`'s R1 annotation
reads "(base: 0 -> record: 1 ...)" while its own pasted output is `0`, the
cited grep pattern `'27 distinct filesystem paths'` cannot match the
correction note's actual wording ("distinct filesystem paths number 27"), and
the round report's before→after repeats the unreachable value ("the marker
probe → 1"). Substance independently verified true by the r58 closure §3 R1.)
This file is the round declaration; the **freeze** is the single commit that
first adds the round-59 wave artifacts (census-start receipt, before-arm
receipts, duty receipts, the S259 snapshot) and the claims container
`.ufo/waves/round-59/claims.json`, recorded in `LOG.md` and
`.ufo/waves/round-59/l1/FREEZE` before any repair data lands. One new
instrument is introduced: `tools/round-59/annotation-audit.py` (the M57-1 /
D58-1 class as an instrument), committed BEFORE this claims file per QUALITY
#33 and pinned in the container. L1-inline round: no wave surface exists on
this host (the kaidoku round-53 L0 question stays open and unanswered; routed
around, never treated as answered).

## Claims

- **R59-C1 — calibration.** D58-1 closes: the r58 c1-after.txt's R1
  annotation contradiction is repaired append-only (filed bytes stay as
  filed), the marker grep pattern is replaced by patterns that actually match
  what they claim to count, and the corrected counts are proved from
  committed bytes: the note's wording probe is 0 at the round-58 base → 2 at
  the record rev (the declaration entry + the landing entry's R1 bullet), and
  the note-of-record bullet probe is 0 → 1. The same claim executes the
  round's orphaned-evidence duty with the frozen instruments (receipt-audit
  over the six host-era containers, record-audit over the r58 record section,
  the two-direction orphan census) and dispositions what they name. A
  do-nothing control cannot reach it: the correction does not exist at the
  base (`c1-before.txt`), and the duty's finding (below) exists at the base.
- **R59-C2 — depth, capability acquisition.** `tools/round-59/annotation-audit.py`:
  a receipt's `base: N -> record: M` annotations must agree with the bound
  command's pasted output and with a re-derivation from git objects at the
  revision named inside the command; annotated commands outside the two
  supported grammars fail closed. Demonstrated: selftest 23/0; red on the
  D58-1 defect itself (the uncorrected r58 receipt at the base → exit 1,
  `ANNOTATION_OUTPUT_MISMATCH@6` + `ANNOTATION_REDERIVATION_MISMATCH@6`); green
  on this round's correction receipt; the persistent original finding on the
  appended r58 receipt is disclosed (a correction does not clear filed
  bytes). Registry row in SKILL (instrument-registry v2 grammar, seven
  cells), capability row in SCORECARD, pinned in the container. A do-nothing
  control cannot reach it: the instrument, its registry row and its
  demonstrations are absent at the base (`c2-before.txt`).

Claims are causally separable: C1's correction and duty receipts verify
without the instrument (plain pasted probes), and C2's demonstrations verify
without the correction landing (the red demo reads base bytes). Lowest-axis
rule: coverage/depth/calibration tied at 10.0, so each claim is a lowest-axis
claim; C1 is calibration, C2 is depth. Stagnation nudge not fired (window
N=10; last capability r58 — none entered, r57 was the last row — r59 = 2/10).

## Fresh-start compliance (operator rule)

The rendered prompt §7 binds this round as a fresh-start round and lists the
last three rejected closures: r50, r51, r52 (all `rejected-honest-stop`). All
three fleet reports were re-read before declaring, and spot-checked against
the lane record (probes run this round, outputs pasted in the round report):

1. r50: `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` at HEAD
   carries `carriers_matched 2`, `target 4`, `met_target false`, `exit 1` —
   the attempt-2 C1 miss as filed.
2. r51: `python -X utf8 -I -B tools/round-51/census3.py --root . --rev
   f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab --historical` → exit 1, registry
   55 / census 42 / outside 13 — exactly the r51 report's diagnostic numbers.
3. r52: `00d0bfd00b2778c3e0b22b7d0f6ade11abcb07a2` is an ancestor of
   `refs/heads/main` (merge-base rc=0) and carries
   `plans/round-52-claims.md` (cat-file rc=0).

Ruled out this round, with reasons:

1. **AVM LE-SquashFS Frontier→Core (the r50/r51/r52 twin claim).** REA 6.5.0,
   sasquatch/sasquatch-v4be and vendor fetches remain measurably absent on
   this host (PROVINCE `## Host migration — 2026-10-31`); three consecutive
   rounds died on it; the routed findings stay routed, untouched.
2. **New wave-based claims of any kind.** No dispatch surface on this host
   (the r53 L0 question stays open and unanswered); r51/r52's wave accounting
   was itself a rejection ground.
3. **Resuming the r51/r52 triage-v6 executability drafts.** Twice rejected as
   incomplete-instrument claims; the drafts stay wave evidence, not
   production instruments.
4. **Adding receipt claims to the r53 container (the r58 planned item "the
   receipts_checked-0 vacuous-clean shape").** The r53 container is frozen;
   amending a historical container is the amendment class every freeze
   forbids, and its FLAGGED INSTRUMENT_NONE finding is disclosed verbatim
   rather than shaped away (the r53 ruling). The honest form of that
   follow-up is a NEW audit receipt, not a container edit — and the r53
   container already audits clean on its full-path receipts at the base
   (this round's sweep, `records/receipt-audit-sweep.txt`).

## Sourced claim

**S259** (GNU Grep manual, https://www.gnu.org/software/grep/manual/grep.html,
opened this round, snapshot bytes + sha256 at `.ufo/waves/round-59/l1/s259/`)
grounds R59-C2's design: `grep -c` prints "a count of matching lines for each
input file" and exits 1 when no lines are selected, so a pasted `grep -c`
output is a function of the pattern AND the bytes probed — a pattern/wording
mismatch (D58-1's exact class) is detectable by re-deriving the count from
the same bytes, which is what the instrument does. The row lands with the
record commit, used-by targets in the same commit (the M53-4 rule).

## The duty's finding, named before any disposition lands

The receipt-audit sweep over the SIX host-era containers (r53–r58) at the
base names exactly one live finding: the r58 container's frozen atom T4
quotes the r58 sweep's finding name `freeze-gate-tip-90f3a9b9.json` as a bare
name, and the round-56 bare-name grammar (M56-2's rule: a bare name is a
claim about the container's OWN round scope) resolves it to zero paths under
`.ufo/waves/round-58/**` — `RECEIPT_ABSENT`, exit 1
(`records/receipt-audit-sweep.txt`). The bytes exist under round-55 (the r58
R2 repair landing) and round-54 (the original); nothing is missing
repo-wide. The disposition (recorded in
`records/w58-sweep-finding-disposition.txt` BEFORE the landing commit):
disclosed named debt, no copy planted — T4's sentence is a quotation of the
sweep's finding (its scope is named inline: "in round-55 scope"), not a
commitment that round-58 committed the file; planting a third byte-identical
copy in round-58 scope solely to flip the grammar green is the r53
"disclosed verbatim rather than shaped away" class, and r58 reject 1 rules
against in-tree receipts no record claims. Flip condition recorded: if a
non-author reviewer rules the T4 name IS a round-58 commitment, the repair is
the byte-identical landing at `.ufo/waves/round-58/l1/records/` with the
provenance sha256, exactly the r58 R2 pattern. The red audit persists at the
tip by design (filed bytes stay as filed) and is receipted as the expected
persistent state.

## §9 sizing (do-nothing controls)

Both before-arms are committed at the freeze: `scores/c1-before.txt` (the
D58-1 defect open at the base: no correction block, the defective annotation
as filed, the cited probe returning 0 where its annotation claims 1) and
`scores/c2-before.txt` (instrument absent rc=128, 0 registry rows, 0
capability rows). A round that did nothing would leave both arms exactly as
measured.

## Commit order (the r56/r57/r58 shape)

1. declaration: plans (this file) + `tools/round-59/annotation-audit.py`
   (the instrument, before the claims file) + LOG declaration entry.
2. freeze: claims container + FREEZE + before-arms + census-start + duty
   receipts (sweep, record-audit, orphan census, sweep-finding disposition,
   red demo, selftest) + s259/ + LOG freeze entry.
3. landing: the D58-1 correction append to the r58 c1-after.txt + the SKILL
   registry row + the SCORECARD capability row + the correction receipt
   `scores/d581-correction.txt` + LOG landing entry.
4. record: SCORECARD round-59 section + lesson + SOURCES S259 + ledger row +
   gate pre-flight receipt (run at the freeze) + LOG record entry.
5. close: after-arms + green/persistent-finding demo receipts + gate landing
   receipt (at the record rev) + census3 generate/check receipts +
   census-end + LOG close entry.

No amendments after the freeze. Every helper call passes repo-relative
forward-slash paths (M58-1's rule), and every commit is diff-tree verified
against its intended path list immediately after landing (the M55-4 rule).
