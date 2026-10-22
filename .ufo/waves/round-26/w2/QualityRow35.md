# QualityRow35 — wave-2 attack on QUALITY row 35 (reversed source decisions)

Seat KaidokuR26.QualityRow35 (critic, leaf). Judged committed bytes at HEAD fe3eb4edf410244eff46151a148c8f754be1ce80 (row added in c3277726). Lane read-only; this report is the only lane write. 2026-10-22, 12:58 to 13:01 UTC. No REA run, no install, no git write, no jj, no web source opened.

## Verdict

**Fails, on two of the three axes.** Grounded: partly holds. Checkable: fails. Satisfied for the round-24 capinfos case: could not be evaluated, because two reasonable readings of the row give opposite answers, and the one the drafter intended fails.

| Axis | Verdict | Counterexample |
|---|---|---|
| Grounded | holds, with two defects | G1, G2 |
| Checkable | fails | K1, K2, K3, K4 |
| Satisfied (capinfos, after round 26) | could not be evaluated; fails under the drafter's reading | S1, S2 |

## Grounded

- observation: every lesson citation resolves at c3277726 and at fe3eb4ed. `round-24-verifier-spotcheck.md:44` contains the quoted "Preserve the historical mistaken rejection and corrective S071 rather than relabel it as always correct" (grep -oF, exit 0). `:61` contains "initial rejection was wrong". `round-24.md:23` holds the rejection and "Flip: a claim that depends on capinfos semantics directly". `round-25-verifier-spotcheck.md:196-197` is routed defect 5. (e1, 12:58:52Z, exit 0.)
- G1, false provenance (observation): the criterion cell says "round 24 never searched `PcapProvider.js:330`" and cites `.ufo/waves/round-26/w1/CapinfosFacts.md`. That report says at line 81: "Unknown: whether the L1 read pcapAnalysis.js or PcapProvider.js before 69e82c48." Its line 24 ("It did not search REA's consumer code") contradicts its own line 81. S066 at 69e82c48 hashed `pcapAnalysis.js` (7651b4c5…), and line 59 of that file reads "File format as capinfos reports it (pcap vs pcapng)." (e3 12:59:39Z, e4 13:00:16Z, exit 0.) So the row turns an unknown into a fact.
- G2, unresolved citation at the row's own commit (observation): `git cat-file -e c3277726:.ufo/waves/round-26/w1/CapinfosFacts.md` printed "fatal: path … exists on disk, but not in 'c3277726'", exit 128. It does resolve at fe3eb4ed (exit 0). The search clause also cites a wave seat report rather than a lesson. `corpus/lessons/round-26.md` has no capinfos, QUALITY or row-35 line (e3: its only hits are line 37 "Rejected: none." and the M26-1 row). QUALITY.md:3-4 says "every criterion cites the lesson that produced it".
- Minor (observation): the why cell cites `round-24.md:85-87` as the fired flip. The evidence that fired the flip ("`PcapProvider.js:330` reads") is on line 84.

## Checkable

- K1, the scope sentence excludes the trigger case (observation, with the reading as inference). The row covers decisions that "a later round or an outside review reverses". Capinfos was reversed inside round 24, by in-round residual seat ResHonesty-2 in commit 5c88c05b (2026-10-21T15:18:48-03:00). That seat's file is under `.ufo/waves/round-24/residual/`, and its header calls it a "Round-24 residual seat". The outside spot-check (18e7eb6d, 18:33:04-03:00) came later and agreed with the flip; it did not reverse anything. On a literal reading, the first sentence does not govern capinfos. (e4, exit 0.)
- K2, the first fail clause is ambiguous in a way that matters (observation). The row fails "when the rejected decision survives only as prose in a lesson table with no registry row and no flip clause". For capinfos: registry rows naming the rejection = 0, and the lesson flip clause is present = 1 (e4).
  - Conjunctive reading: the clause requires both to be missing, so capinfos passes.
  - Disjunctive reading: either missing fails, so capinfos fails.
  - The w1 drafter meant the disjunctive reading ("a lane holding the capinfos rejection only at `round-24.md:23` fails", QualityRow.md §3). The positive clause ("stays locatable with its stated reason and its flip condition") asks for no registry row at all, which supports the conjunctive reading.
- K3, the second fail clause satisfies itself (observation). It fires only when the disagreement "appears in no lane artifact other than the reviewer's own file". Row 35 itself quotes `round-24-verifier-spotcheck.md:44`, so once the row exists that clause can never fire. At c3277726, SCORECARD had 0 capinfos lines, yet the clause was already unfalsifiable (e3: c3277726 SCORECARD count `0`).
- K4, the search clause leaves no record a reader can test (observation). "Before a source is rejected as not needed, the consuming code is searched for it" requires no recorded command, tree or hits. A future rejection row "Not needed: X already records Y" with no search record passes. The competing w1 draft (CapinfosFacts.md §7) required "a recorded search … (command, tree, hits as file:line)"; row 35 dropped that.
- Also (inference): "beside the round-level verdict they already carry" is undefined. The round-24 verdict is at SCORECARD.md:3048 and LOG.md:2954. The new record is at SCORECARD.md:3077 (a different section, 29 lines away) and LOG.md:2969.

## Satisfied for capinfos after round 26 (at fe3eb4ed)

| Clause | Result | Evidence (e2 12:59:07Z, e3, e4; all exit 0) |
|---|---|---|
| Rejected decision stays locatable with reason and flip condition | holds | `round-24.md:23` unchanged; `git log -L 23,23` shows only 69e82c48 |
| Admitting row names the decision it reverses | weak pass | S071: "the earlier rejection is reversed"; no path or line; `grep -c 'round-24.md:23' SOURCES.md` = 0 |
| Admitting row names the evidence that fired the flip | weak pass | S071 names "residual review ResHonesty-2 finding 7"; S071 does not cite PcapProvider.js (count 0; S070 does) |
| SCORECARD records the disagreement with path and line | holds since fe3eb4ed | SCORECARD.md:3077 "`corpus/lessons/round-24-verifier-spotcheck.md:44`, `:61`" |
| LOG records it | holds since fe3eb4ed | LOG.md:2969, same citations |
| Registry row for the rejection (disjunctive reading of K2) | fails | `status rejected` rows = S022 and S028 only; 0 rows name capinfos as rejected |
| Consuming code searched before rejection | unknown | G1; this was a round-24 act and cannot be repaired now |

- S1 (observation): the commit that added row 35 (c3277726) did not satisfy the row's own SCORECARD leg; SCORECARD capinfos count was `0` there. The leg was met one commit later, at fe3eb4ed.
- S2 (inference): S071 still says the flip condition "fired". CapinfosFacts R2 argues the condition was already met when the rejection was written. If that holds, "fired" presents an original error as a later trigger, which is close to the laundering the row forbids.

## Smallest safe correction

QUALITY rows are never rewritten (QUALITY.md:4), so append row 36 "supersedes 35" that:
1. Scopes the rule to any reversal: in-round residual review, a later round, or an outside review.
2. Fails the lane when the rejection has no SOURCES row with status rejected and a flip clause, OR when the admitting row lacks a path:line pointer to the rejected decision.
3. Requires the rejection row to record its consumer-code search (command, tree, revision, hits or "no hit").
4. Says "beside" means the same round's SCORECARD section and LOG entry, and drops the self-satisfying "no lane artifact" fail clause.
5. Restates the round-24 search as unknown, and cites a lesson rather than a seat report (add the case to `corpus/lessons/round-26.md` Mistakes).

On the lane side, append one SOURCES row for the capinfos rejection: status rejected, superseded by S071, pointing at `round-24.md:23`. Do not edit S071 or `round-24.md:23`. Impacted axes: calibration (QUALITY as the admission bar) and honesty or provenance (G1).

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/w2/QualityRow35/)

| File | sha256 |
|---|---|
| e1-citations.txt | 61ba55727a74ecee27e9c52c7853188fa3b3581ed4b25d511e53327e93b21ceb |
| e2-satisfaction.txt | 4310c2d39819146b3bb73001248ad3600c375e194d2a07ee5770836d86144b87 |
| e3-scorecard-lesson.txt | 2e04d062e69348d6426d5f93c07b7156a532b55bacdaa3972c7cfe0693042abd |
| e4-scope-provenance.txt | 9e27b98e4ffe1350d120f294097bc2d02a2b979b25c9a6fcc275697770eec538 |

Each artifact is the captured output of a bash block of read-only `git show`, `grep`, `awk` and `sha256sum` commands over committed bytes, with its UTC time at the top. Lane file digests at fe3eb4ed: QUALITY.md c04b8e793c20c386b06ec86cc5d9fa1997719bdc3a348f227c5b2ef0de401636; SOURCES.md 945900936762151ad8544c8a0f66179d5c119aefe562e82a067b1085f6ae4657. REA 6.5.0 `dist/domain/pcap/pcapAnalysis.js` 7651b4c5582b62513196146b7aa08043fab93d0848ce7f8680523d867597c641, line 59 read locally on 2026-10-22. Installs: none.
