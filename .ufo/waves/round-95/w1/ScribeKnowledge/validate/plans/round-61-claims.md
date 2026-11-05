# kaidoku round 61 — claims (the routed edge-mislabel closes append-only, and the edge-numstat class becomes an instrument)

Round base `2d976fba2bfc3b85dcc0546f9ec8e149fa2185fe` (lane `main` tip at round
start, pushed = origin/main; the round-60 verifier spot-check commit, which
admitted r60 with no new routed defects and routed its status-neutral note 1
to this round). The carry-in landed at `319e5244f088fc01cca7b0b8259f0ce5085e7b48`
BEFORE this declaration (the r60 non-author closure recorded per QUALITY #34:
admitted true, spot-check path `corpus/lessons/round-60-verifier-spotcheck.md`;
note 1 accepted as the round's routed correction target D60-1; the two sibling
sites named in the same entry). This file is the round declaration; the
**freeze** is the single commit that first adds the round-61 wave artifacts
(census-start receipt, before-arms, demo and duty receipts, the S261 snapshot)
and the claims container `.ufo/waves/round-61/claims.json`, recorded in
`LOG.md` and `.ufo/waves/round-61/l1/FREEZE` before any claim data lands. One
new instrument is introduced: `tools/round-61/numstat-edge-audit.py` (the
D60-1 class as an instrument — the r59 D58-1 pattern), committed BEFORE this
claims file per QUALITY #33 and pinned in the container. L1-inline round: no
wave surface exists on this host (the kaidoku round-53 L0 question stays open
and unanswered; routed around, never treated as answered).

## Claims

- **R61-C1 — calibration (the routed D60-1 precision defect closes
  append-only).** The r60 closure's note 1: `.ufo/waves/round-60/l1/scores/c1-after.txt:10`
  says "SKILL delta landing→record exactly `1 0` by numstat"; the `1 0` is
  the freeze→landing edge (the landing `bbdb03ab…` added the registry row);
  landing→record re-derives `0 0`. The correction lands append-only: a
  correction block appended to the defective receipt (filed bytes stay as
  filed, additions only), the correction receipt
  `.ufo/waves/round-61/l1/scores/d601-correction.txt` with every edge
  re-derived by numstat, a new LOG correction entry (the r60 entries are
  never edited), and the SCORECARD round-61 section naming both sibling
  sites — the LOG round-60 close entry ("the SKILL delta landing→record
  exactly `1 0`") and the SCORECARD round-60 atom T7 ("the SKILL delta
  landing→tip exactly `1 0`"; landing→tip re-derives `0 0`, base→tip is
  `1 0`). Before: at the base the correction is absent (`cat-file -e` rc=128)
  and the mislabel stands as filed at all three sites (grep counts 1/1/1);
  after: the correction block is present (grep 0→1), the numstat edges are
  pasted (freeze→landing `1 0`; landing→record `0 0`; landing→tip `0 0`;
  base→record `1 0`), and the r60 wave paths show 0 deletions across the
  round (append-only). A do-nothing control cannot reach it: the correction
  block, the receipt, and the LOG/SCORECARD corrections do not exist at the
  base, and no re-read of the base produces them. Claims: this correction
  and its measuring are one claim (calibration — matching the record to the
  observed state, the D58-1 axis).

- **R61-C2 — depth, capability acquisition (the edge-numstat class as an
  instrument).** `tools/round-61/numstat-edge-audit.py`: a receipt's
  committed bytes are scanned for rev-name bindings (a lowercase name +
  optional `commit`/`rev` word + 40-hex; first occurrence wins; 64-hex
  sha256 run-ons rejected by lookahead; `rev=` forms do not bind) and for
  edge claims of the strict grammar `(SKILL|LOG|SCORECARD|PROVINCE) delta
  <a>→<b> exactly `<x> <y>`` (U+2192 arrow; the ASCII `->` and dot forms
  are out of scope, not findings); every claim is re-derived by
  `git diff --numstat --no-color --no-renames X Y -- path` (no shell, no
  worktree bytes), absent rows counting `0 0`, binary edges (`- -`, per the
  git-diff docs) fail closed as NUMSTAT_BINARY, unresolvable names fail
  closed as NUMSTAT_NAME_UNRESOLVED, and a claimed pair that disagrees with
  its re-derived edge is NUMSTAT_EDGE_MISMATCH. Verdicts: 0 = at least one
  claim, every one re-derives; 1 = any finding, each named; 2 = zero claims
  in the grammar, receipt absent at REV, unknown revision, or failed git —
  never vacuously clean (the QUALITY #66 boundary). Demonstrated on the
  committed bytes at the base: selftest 25 cases 0 failures (in-memory,
  injected runner); RED on the routed defect itself — the r60
  `scores/c1-after.txt` at the base: exit 1, NUMSTAT_EDGE_MISMATCH@10,
  claims `1 0`, re-derives `0 0`, internal header bindings only (the first
  mechanical naming of D60-1); RED on the SCORECARD T7 sibling (with
  disclosed caller-supplied `--name` overrides — the section prints
  abbreviated hashes — 2 claims found, T7 fires, the r59 T8 `freeze→fixup
  `1 0`` atom re-derives green on the same run); RED on the LOG r60-close
  sibling (same shape: the close entry fires, the r59 entry's true claim
  stays green); fail-closed arm — the same SCORECARD run with no overrides
  exits 1 on 2× NUMSTAT_NAME_UNRESOLVED; zero-claims arm — the r59
  `d581-correction.txt` exits 2 (unevaluable, never clean). Registration:
  SKILL registry row (seven cells, pipe-free, anchored on the registry
  marker — the M60-1 rule), SCORECARD capability row, census3 drift census
  re-run (the M58-2 rule). A do-nothing control cannot reach it: the
  instrument, its registry and capability rows, and every demo receipt are
  absent at the base (`scores/c2-before.txt`). The GREEN demo on the
  correction receipt and the PERSISTENT arm (the defect still fires at the
  close tip — a correction does not clear filed bytes) land with the close
  commit, the disclosed r59/r60 ordering (the receipts they measure do not
  exist before the landing).

Causal separability: C1's correction is verifiable without C2 (grep counts,
numstat pastes, append-only numstat); C2's instrument and demos are
verifiable without C1 (every red demo runs at the base against bytes C1
never touches). Distinct axes: calibration vs depth. Lowest-axis rule: all
three owned axes sit tied at 10.0, so both claims are lowest-axis claims.
Stagnation nudge not fired (window N=10, last capability r60; r61 = 1/10).
Sourced claim: S261 (the git-diff documentation, opened this round) grounds
C2's design — `--numstat` shows added/deleted line counts in decimal
notation for the named paths, and binary files print two `-` instead of
saying `0 0`, so an edge-labeled `A B` claim is a function of the
(X, Y, path) triple alone and a binary edge is not a count.

## Fresh-start compliance (operator rule)

The rendered prompt §7 binds this round as a fresh-start round and lists the
last three rejected closures: r50, r51, r52 (all `rejected-honest-stop`). All
three were re-read and spot-checked against the lane record before declaring
(probes and outputs pasted in the freeze receipt `scores/freshstart-spotcheck.txt`):

1. r50: the honest-stop report exists at the fleet root (`.ufo/reports/round-50/kaidoku.md`,
   attempt-2 filing naming the run-11 wrap-up stop of attempt 1); the
   attempt-2 C1 miss is as filed. The rejections were operator/provider
   boundaries, not fabricated claims.
2. r51: `.ufo/waves/round-51/l1/wave-accounting.json` at the base carries
   `floor64_met: false` with the 36-seat wave — the below-band stop as
   recorded, never waived into admission.
3. r52: the SCORECARD round-52 section names both declared claims
   unprovable (2 matches); the pre-freeze honest stop stands.
4. The 19 standing W04 duplicate-url warnings both closures name are still
   standing at this round's census-start (19; named debt, never waived).

Ruled out by this spot-check: none of the three rejections was for an
inflated or unverifiable claim, so the bar this round must clear is the
do-nothing control test — each declared claim's before-arm is red at the
base (correction absent rc=128; instrument absent rc=128, 0 rows) and the
do-nothing control cannot produce the correction, the gate, the demos, or
the registrations.

## Duty (the orphaned-evidence duty, run to dispositions)

- receipt-audit (the frozen r56 gate, pin `897df532…`) over the EIGHT
  host-era containers r53–r60 at the base; the r58 container's quoted bare
  name is standing disclosed named debt (the r59 non-author closure ruled
  the flip condition does not fire; no copy planted — the third refusal).
- record-audit (the frozen r57 gate, pin `3a5fff9a…`) over the r60 record
  section at the base (named N, missing 0 expected).
- the two-direction orphan census at the base (quotepath off).
- the standing halfway sweep re-run (the r60 planned field): the frozen r60
  sweep (`annotation-sweep.py`, pin `38614088…`, composing the frozen r59
  gate `ba9ccbb9…` via `--expect-sha256`) re-run at the r61 tip after the
  round's receipts land, dispositions extended append-only if new findings
  are named.
- the registry-drift census re-runs after the new SKILL row lands (the
  M58-2 rule): census3 `--generate` at the landing rev, `--check` at the
  record rev.
