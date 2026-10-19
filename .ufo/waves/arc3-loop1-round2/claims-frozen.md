# arc3-loop1-round2 — frozen claims, 2026-10-19

Wave: 64 seats, `opencode-go-2/deepseek-v4.1-flash` (opencode-go key 2 of 7 — rotation
advanced after round 1). Roster frozen PRE-DISPATCH per the r9 wire-it amendment:
the dispatch items array must carry exactly the 64 seat names below; the parent
counts the items array before dispatch.

Freeze history: a first draft of this file was discarded pre-dispatch — its chain
sums were hand-arithmetized and wrong (parent-side catch, the r5 lesson applied to
our own freeze; no seats were dispatched against it). This freeze's roster is
enumerated mechanically: 12 + 30 + 18 + 4 = 64, every seat name appearing exactly
once.

Axis set: **depth (owned)**, **freshness (fleet)**, **operability (fleet)**.
Lowest-axis rule: all three owned proxies remain tied at 10.0 with none retired;
the owned claim is selected by the standing most-falsifiable-next-claim tie-break.
Claims are causally separable: SKILL.md craft text, the census instrument, and the
custody receipt instrument — no shared edit targets.

## C1 — depth (owned): queue-drain rule #14 — self-identity re-derivation discipline

Measured origin (arc3-loop1-round1): EX-12's entry patch was revised mid-wave and
its own "Verification performed" identity claim still described the superseded
revision — caught by critic CR-2 (F2) and the convergence seat (D9); the parent
recorded the fresh hash at landing. Rule: an artifact that records its own
byte-identity (size/hash/line-count) must re-derive that identity after every
revision; a stale self-identity voids the verification block, not the work; the
integrator records the fresh identity at landing.

Falsifiable before → after: queue-drain rules 13 → 14, 14/14 citation-resolved at
the work commit (command A), prior 13 rules byte-identical; citations in rule-#11
form (stanza key + receipt, no bare line numbers).

## C2 — freshness (fleet): census fail-closures — H1 absent-file guard + H3 blind-instrument floor

Named debt (arc3-loop1-round1 C3 verdict, items H1/H3; patch texts drafted):
- H1: an absent CURRENT-only scoped file reads silent PASS (`lines=0 loci=0`) —
  `claims/c3/RV-11/proposed-missing-file-guard.patch.md` (in the round-1 tree:
  `.ufo/waves/arc3-loop1-round1/claims/c3/RV-11/`).
- H3: needles neutered → `loci=0`, G2's second disjunct vacuous → blind PASS —
  `claims/c3/CR-5/proposed-g2-positive-floor.patch.md`
  (`.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/`).

Claim: after the round's commit, the census FAILs with a declared class when a
scoped file is absent, and FAILs when its positive-floor assertion finds zero
loci in a non-empty scope; every round-1 silent-PASS injection now reproduces as
a declared FAIL; ordinary runs at HEAD stay PASS 0/0/0/0; scope bounds otherwise
byte-stable (creep audit 0 flags); the H4 self-certification residual stays named —
the external diff audit (`scope-diff.py` form) is run on the v11 diff as the
chain's certificate.

## C3 — operability (fleet): custody receipt v2 — epoch times + inode/ctime pins + label fix

Measured origin (arc3-loop1-round1 cross seats): the canonical custody receipt
labels local (-03) mtimes as `MTIME_UTC` (reproduced from the epoch — digests
unaffected, label defect), and sha256-only custody is blind to a same-content
rewrite (attack 3, measured).

Claim: after the round's commit, `.ufo/gates/custody-pair/` exists as a committed
tool emitting a v2 receipt per path: sha256 + mtime epoch (UTC-rendered, correctly
labeled) + inode + ctime; the label defect is gone; a live same-content rewrite
of a custody path is detected (inode/ctime movement); v1 receipts remain
verifiable against the tool's sha256 fields; the round's own live pre/post pair
(exit 0, 5/5) is captured by the tool.

## Cross-cutting rules (frozen)

- Custody: the 5 paths stay READ-ONLY (hash/stat capture only) for every seat; the
  v2 tool's live pair is captured per C3.
- No installs this round. Scratch under `/var/tmp` or `/dev/shm` (`/tmp` is
  quota-exhausted, EDQUOT — standing round-1 record).
- Seat discipline: seats write ONLY their seat report at
  `.ufo/waves/arc3-loop1-round2/seats/<SEAT>.md` and artifacts under
  `.ufo/waves/arc3-loop1-round2/claims/{c1,c2,c3,cross}/<SEAT>/`; NO git
  mutations; no LOG/SCORECARD/SHONEN writes; corpus/SKILL/README edits as patch
  text only. Only the designated implementer writes its chain's real target:
  C2's EX-16 (`.ufo/gates/c1-census-v10.py`) and C3's EX-31 (new files under
  `.ufo/gates/custody-pair/` only). Census scope bounds and the probe's pointer
  table must not be widened (the r4 laundering precedent).
- Seat reports carry: work performed (evidence pointers), proposed changes (patch
  text paths or "none"), before→after measurement, attacks attempted, blockers.
- Round report: `.ufo/reports/arc3-loop1-round2/kaidoku.md` (parent-written).

## Roster (64 seats, enumerated)

C1 chain (12): PL-1, EX-01, EX-02, EX-03, EX-04, EX-05, EX-06, SC-1, RV-1, RV-2,
  CR-1, VZ-1
C2 chain (30): PL-2, EX-11, EX-12, EX-13, EX-14, EX-15, EX-16, EX-17, EX-18,
  EX-19, EX-20, EX-21, EX-22, EX-23, EX-24, EX-25, EX-26, SC-2, SC-3, RV-3, RV-4,
  RV-5, RV-6, RV-7, RV-8, RV-9, RV-10, CR-2, CR-3, VZ-2
C3 chain (18): PL-3, EX-31, EX-32, EX-33, EX-34, EX-35, EX-36, EX-37, EX-38,
  EX-39, EX-40, SC-4, RV-11, RV-12, RV-13, RV-14, CR-4, VZ-3
Cross (4): CN-1, CN-2, CU-1, VZ-4

Counts: C1 = 1+6+1+2+1+1 = 12. C2 = 1+16+2+8+2+1 = 30. C3 = 1+10+1+4+1+1 = 18.
Cross = 4. Total = 12+30+18+4 = 64.

Assertions at dispatch: len(items) == 64; every item name in this roster; no
duplicate names.
