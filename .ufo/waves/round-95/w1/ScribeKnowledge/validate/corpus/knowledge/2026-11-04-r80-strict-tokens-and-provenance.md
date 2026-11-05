# Strict tokens, duplicate cells, and receipt provenance — round 80

**Date:** 2026-11-04 · **Round:** 80 · **Axes:** calibration (R80-C1), freshness (R80-C2),
depth (R80-C3) · **Base:** `16dfa009bf143080dfcdfc5f9ec34bd359536d90`.

Three instrument rules became checkable this round. Each is stated as the decision it encodes,
the signature that shows it firing, the command that re-derives it, and the receipt that holds the
measurement. None of the three is a claim about a reverse-engineering target; all three are rules
the lane's own evidence apparatus now enforces.

## 1. A declared token binds only as a whole token (S298)

| question | rule |
|---|---|
| When does a pointer's declared token bind the pointed line? | When at least one occurrence is **delimited**: the character before and the character after are missing (slice edge) or outside `[A-Za-z0-9._-]`. |
| What does a bare substring test accept? | `rea-agents@6.7.0` inside `rea-agents@6.7.05` and inside `rea-agents@6.7.00` — both a longer pin than declared. |
| What does the strict rule refuse, and how does it say so? | `reason = "token '…' occurs on line N only inside a longer token (`…`)"`; the old message `token '…' is not on line N` is kept when the token is absent altogether. |
| What would a binder that refuses everything look like? | It fails the two green controls: an exact quoted pin line and a two-line range whose token is on the second line must both bind. |

Measurement: `python3 -I -B tools/round-80/strictness-battery.py --root . --impl
tools/round-80/pointer-bind.py --control-impl tools/round-79/pointer-bind.py --work <scratch>
--json-out <receipt>` → `cases 4`, `green_cases 2`, `candidate_false_greens 0`,
`control_false_greens 4`, both green-refusal counts 0 (receipt
`.ufo/waves/round-80/l1/scores/c1-at-landing.json`). The round-79 control binder accepts all four
red fixtures; an independently written binder (`w1/ExecBinder/pointer-bind.py`) scored
`candidate_false_greens 0` against the same fixtures, so the rule is not an artefact of one
implementation.

## 2. A record that declares one cell twice is a defect, not a last-wins collapse (S297)

| question | rule |
|---|---|
| What did the round-79 parser do with a second `OMP` cell? | `{name: (pin, pointer)}` kept the last occurrence and reported five cells with no duplicate signal — the first cell vanished silently. |
| What does the strict parser do? | Counts every declared cell (`checks_total 6` for the duplicate fixture) and lists the repeated client in `duplicates: ["omp-pin"]`; the second cell keeps a distinct id (`omp-pin#2`). |
| Why is refusal the right default? | RFC 8259 §4 recommends unique names (`SHOULD`, S049), so a repeated cell is at best ambiguous; the lane's own record is a machine-read surface and ambiguity must be reported. |

Measurement: same battery, red cases `rb03`/`rb04` (duplicate `OMP` and duplicate `Devin`); the
round-79 control reports `checks_total 5, matched 5, duplicates` absent, the strict binder reports
`checks_total 6` and the duplicate id. Limit: ECMA-404's grammar does **not** require unique names,
so this is an interoperability rule for this lane's record, not a JSON validity claim.

## 3. A receipt's instrument digest must name a committed blob (R80-C2)

| question | rule |
|---|---|
| When is a receipt's provenance bound? | When its `instrument.sha256` equals a committed blob of its `instrument.path`: at the lane tip, at the receipt's own 40-hex `rev`, or at any committed revision of that path. |
| What is **not** bound? | A digest matching only the working tree; a receipt whose `rev` is symbolic (`@HEAD@`, `main`); a path that escapes the lane (`..`, absolute). |
| Which receipt is the declared negative control? | `.ufo/waves/round-69/l1/scores/prov-forged-instrument.json` — round 69's forged-instrument fixture must stay flagged, so "flagged 0" is never the target. |

Measurement: `python3 -I -B tools/round-80/receipt-provenance.py --root . --rev <40-hex>
--from-round 60 --to-round 79 --json-out <receipt>`. Base `16dfa009`: `receipts 34`, `flagged 2`,
`expected_control_flags 1`, `unexpected 1` naming
`.ufo/waves/round-79/l1/scores/c2-at-landing.json`. After the receipt was re-taken with committed
instrument bytes and a full 40-hex rev: `flagged 1`, `unexpected 0` (receipt
`.ufo/waves/round-80/l1/scores/c2-at-landing.json`).

## 4. Every refusal clause owns one table row and one isolating case (R80-C3)

| question | rule |
|---|---|
| What is bound? | Each `defects.append(...)` clause inside `validate_receipt()`, in source order `G01`–`G09`, to exactly one row of the round-80 SKILL table and one declared selftest case. |
| How is binding tested? | The row's declared fragment must occur in the clause's literal text and identify exactly one clause; the case name must appear in the gate's own `--selftest` source. |
| How is isolation proven? | Delete the clause in a copy (`defects.append(...)` → `pass`), run the copy's `--selftest`, and require the declared case to be present and failing. An absent declared case is a **survivor**; a copy with no `SELFTEST` summary is inconclusive. |

Measurement: `python3 -I -B tools/round-80/guard-battery.py --root . --rev <40-hex>
--expect-sha256 <gate digest> --work <scratch> --json-out <receipt>`. Base `16dfa009`: `guards 9`,
`rows 0`, `bound 0`, `survivors 9`, pristine 29 cases. After the gate revision: `guards 9`,
`rows 9`, `bound 9`, `survivors 0`, pristine 37 cases, pin matched (receipt
`.ufo/waves/round-80/l1/scores/c3-at-landing.json`). Every one of the nine mutants fails exactly its
own declared case and no other (`w1/ExecGate/mutants.json`, `isolating true` on all nine); an
independent enumeration and deletion tally (`w1/ReviewerC3/deletion-receipt.json`) reproduced the
base shape 8 survivors / 1 killed, the one being `: refused without a reason`.

## Limits

- The battery's `--validate` is internal consistency, not authenticity: a hand-authored receipt
  consistent with itself passes, exactly as round 78 recorded for its own readers.
- The guard table's binding test reads the clause's **literal** text; a clause whose message is
  computed at call time would bind by fragment but could not be checked for wording.
- The strict-token rule is a delimiter rule, not a version comparator: `6.7.0` and `6.7.00` are
  different tokens and both bind only where they stand whole.
- Coverage is unchanged by this round: these are the lane's instrument-layer rules, not a new
  carrier class (see the coverage map row).

## Sources

S049 (RFC 8259 §4, re-opened this round: 8-word quote at line 322; the row is held from round 21 and its used-by now names this entry), S298 (Python `re` §`\b`, 14-word quote at line 747);
both snapshots sha256-pinned in `.ufo/waves/round-80/l1/sources/`. The reject side is recorded in
`corpus/lessons/round-80.md` `## Gate`: the Wikipedia `JSON` article (tertiary, and it quotes
ECMA-404 saying uniqueness is not required) and a Cloudflare-blocked Stack Overflow page
(unreachable, not fabrication).
