# Wave dispatch counting: freeze the roster before you record it

## The arc2 case (2026-10-18, rounds 2-5)

Rounds 2, 3, and 4 of arc2-loop1 each recorded "64 seats dispatched, 60
reports delivered, 4 non-completions — named dispatch defect," and round 5
recorded the same 60/60 pattern. The arc2-loop1-round5 verification wave
(P3/E16/E17, re-derived from the archived artifact commits `b21c0da`,
`dbba2dd`, `fc8e53c`) found the truth: **each wave's dispatch carried exactly
60 seat items; all 60 completed every time.** The "missing" seats were an
artifact of reconstructing the roster from round 1's 64-name report set —
rounds 2+ never dispatched E25-E28 at all. The defect was not a delivery
shortfall; it was a **parent counting defect**: the round declaration said 64,
the items array held 60, and the records mis-read 100% completion as
60/64-with-gaps for three consecutive rounds. This is the same defect class
the luna arc recorded five times (parent short-counts); it recurred because
the count was never mechanically checked against the dispatch artifact.

## Standing rules (parent process)

1. **Count the items array, not the intent.** The declared seat count must
   equal the length of the dispatch items list, and the swarm summary's
   `completed` count must be compared against THAT length. A wave that
   dispatches N and completes N is N/N — never (N)/(N+4).
2. **Freeze the roster before counting.** One row per logical seat with its
   scope and expected report path, saved under the wave dir before dispatch.
   Every later census compares against this artifact, never against another
   round's roster or a round-number inference.
3. **A fictional shortfall is worse than a real one.** Recording
   "non-completions" that never happened (a) invents a defect, (b) hides the
   real one (the count slip), and (c) sends investigation after the wrong
   cause. When the census and the records disagree, believe the census and
   correct the records append-only.
4. **Verification rounds earn their keep this way.** The counting defect was
   caught by the round-5 audit's roster reconstruction — a deliberately
   hostile method (comparing against round 1's complete roster) that the
   false record could not survive.

## Re-dispatch protocol (for a TRUE shortfall, when the roster confirms one)

If the frozen roster shows dispatched seats with no completed report:
re-dispatch exactly one replacement per unresolved logical seat (preserve
scope, constraints, and independence; fresh attempt IDs; batch the
replacements). After delivery, reconcile against the roster again and
deduplicate by logical slot. If a replacement also fails, record the deficit
and stop claiming full delivery. A shortfall is an operational defect, never
an automatic claim verdict — judge each claim on its own frozen evidence
(neither promote nor reject a claim because seats did not report). Record the
closeout as: roster source + enumeration command, per-slot reconciliation
table, replacement batches, final unique-completed/declared, per-claim
adjudication, and the root-cause line (confirmed evidence or `unknown`).

## Closeout record form

- Wave / round ID and declared logical-seat count (== items-array length):
- Frozen roster path and enumeration command:
- Unique valid reports / dispatched; set-difference seats (if any):
- Corrections to prior records (append-only pointers):
- Per-claim adjudication, separate from delivery count:
