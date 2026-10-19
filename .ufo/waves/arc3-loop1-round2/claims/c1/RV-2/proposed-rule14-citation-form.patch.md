# PATCH PROPOSAL (not applied) — rule #14 citation form: SCORECARD line range → section key

Seat RV-2 (reviewer, chain c1), 2026-10-19 wave `arc3-loop1-round2`.
Target: the rule #14 payload of `claims/c1/EX-01/rule14.patch.md` (the rock the
integrator will land), one sentence. Reviewer seat writes no repo target.

## Why

Rule #11 (`SKILL.md:196-206`) requires citations into an operator-mutable file
to anchor by content key + receipt, "never by bare line number"; the escape
clause admits a line number only "inside an append-only record that names its
capture stamp". The payload's `SCORECARD.md:1366-1368` is a bare line range into
a file whose head is rewritten every round (measured: line-neutral today — the
range resolves at HEAD and its content matches the claim — but the form does not
guarantee that; see `evidence/scorcard-cadence.txt`). `LOG.md:1411-1412` needs no
change: LOG.md is append-only history (probe `exempt` entry, `pointer-table.json`).

## Proposed change (one citation, same meaning, no new tokens)

```diff
--- a/claims/c1/EX-01/rule14.patch.md   (payload, lines 9-10)
+++ b/claims/c1/EX-01/rule14.patch.md   (payload, lines 9-10)
@@
-  landing (10,225 B / `dd986f56…` — `SCORECARD.md:1366-1368`;
-  `LOG.md:1411-1412`) — never a revert, never a carried-over number.
+  landing (10,225 B / `dd986f56…` — `SCORECARD.md`'s `arc3-loop1-round1`
+  section, the "fresh identity recorded" line; `LOG.md:1411-1412`) — never a
+  revert, never a carried-over number.
```

Equivalent one-line variant (keeps the range, adds key + stamp):

```diff
-  landing (10,225 B / `dd986f56…` — `SCORECARD.md:1366-1368`;
+  landing (10,225 B / `dd986f56…` — `SCORECARD.md`, `arc3-loop1-round1` section
+  (the range at the 2026-10-19 landing record); `SCORECARD.md:1366-1368`;
```

## Verification performed on the proposal (scratch only)

- Both variants keep the payload's citation count and the command-A outcome:
  rule blocks 14, resolved 14 (the counted citation is the corpus/knowledge one).
- The anchor `arc3-loop1-round1` is unique in SCORECARD.md at HEAD and the
  content anchor `10,225 B` + `dd986f56…` sits inside the target lines
  (`evidence/content-match.txt`).
- No token class changes: the payload remains census/needle-clean
  (`evidence/needle-scan.txt`: 0 hits, exit 0).

## If the integrator prefers to keep the bare range

Then the landing record must carry the adjudication explicitly: line ranges into
`SCORECARD.md`'s appended round sections are treated as conforming because (a)
the citing sentence carries the identity value, (b) the target's measured
write-cadence is tail-append with line-neutral head rewrites, and (c) the same
class already exists in rule #12 (`SCORECARD.md:544-545`, stable at 544 across
every recorded revision). Naming the ruling is what keeps the claim's "rule-#11
form" line honest; silence leaves a strict reading standing.
