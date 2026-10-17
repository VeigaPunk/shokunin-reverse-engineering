## CLAIM
CB1 necessity adversary 2, independent of H1: round 9 must NOT be rejected for smallness. The fleet protocol sets no size floor, and all four carried items are recorded, still-open debts — but admission stays conditional on per-item post-integration verification.

## METHOD
Read-only at HEAD `a280e07`: AXES.md admission rules; SCORECARD planned-next row, debt lines, and round-4/5/8 records; the four source loci checked first-hand via `grep -n`/`sed` (exact lines below). Command A not re-run by me (G2's lane-A run cited, not adopted). No probes, network, edits, or `/tmp` access.

## FINDINGS
1. No size floor exists: AXES.md:25-31 fixes 1–3 claims per round and admits a round iff "every claim verifies and no axis is harmed" — magnitude is never a criterion. Rejecting for smallness would be an unsanctioned rule and would incentivize round inflation.
2. Precedent: freshness rounds 4 and 5 were admitted via debt disposition (SCORECARD.md:374-415, 417-465), and round 8 landed a single entry (SCORECARD.md:542). This scale is the norm, and SCORECARD.md:556-558 registers this queue as round 9's planned move.
3. Necessity, verified first-hand: r4-16:751-752 still carries the two-site L197 account inside its r12-01 errata section (:728); r12-01:99-104 corrects it to four sites ("7 values" attributed, receipts gone). The jq "benign" at r2-jq:217,219,236-237 conflicts with `PROVINCE.md:114-116` (grep-verified: refusal bullet is exactly :114-116), and SCORECARD.md:77-80 already labels it correction debt. SCORECARD.md:459-460 records both census checks "for the instrument's owning round"; LOG.md:808-809 leaves the ~1.2GB `/tmp` litter explicitly "left". All four are open, not filler.
4. Divergence from H1: H1 rejects "on the evidence available" — proposals, not measured before→after. That objection concerns timing/measurement, not size, and applies to every pre-integration round; it does not answer this seat's question yes.

## THREATS
Smallness still limits claimable content: one aggregate "freshness improved" line is weaker than four itemized before→after (AXES.md:30-31), and item 2 partly re-records limits already narrated at SCORECARD.md:459-460 — the landed delta must show the adjudicated home, not new evidence. Adjacent drift outside my remit: SCORECARD.md:79 still points at `PROVINCE.md:107-109`; the actual refusal is :114-116 (same stale-pointer class as the wave steer); whether item 4 corrects it is the parent's call.

## VERDICT
CLEAN — reject-for-smallness fails: the four items are recorded open debts at the registered planned move; admit conditional on post-integration per-item evidence plus command A 79/79, 9/9 and non-target byte-identity.
