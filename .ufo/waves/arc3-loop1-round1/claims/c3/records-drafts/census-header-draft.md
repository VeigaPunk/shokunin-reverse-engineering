# Census-header change text — C3 records draft (SC-7, arc3-loop1-round1)

Seat SC-7 · chain c3 · role scribe · 2026-10-19. **Draft for the PARENT; NOT
applied.** SC-7 did not write `.ufo/gates/c1-census-v10.py` (EX-28 owns the real
target; not landed at the last poll, 10:07Z). This is the C3 records draft for
the instrument-header change text; the disposition record and row-level history
stanza were drafted same-chain by SC-6
(`claims/c3/SC-6/e22-disposition.draft.md`, sha256 `ed5cf1f7…`, §6 P1) and EX-26
(`claims/c3/EX-26/proposed-census-header-disposition.patch.md`, sha256
`f467814d…`). This draft adopts **SC-6's P1 as the base** and adds the one
sentence SC-6's file does not carry — the records-commit verification measured
by SC-7.

## 1. The change

Target: `.ufo/gates/c1-census-v10.py`, lines 1-2. The line-1 provenance
docstring extends into a multi-line stanza stating the E22 disposition (the C3
claim requires the disposition "stated in the instrument's own header"); the
shebang line stays directly after the closing `"""` (the r4 re-key precedent).
Instrument sha256 at HEAD:
`36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`.

No SCOPE-table edit: at HEAD no scope row is undeclared or stale (measured
below), so the claim's re-key branch is not taken and no row is retired.

## 2. Applyable text (assembled: SC-6 P1 + SC-7 addendum)

SC-7 addendum sentence, inserted immediately before the closing `"""`:

    Records-commit check (arc3-loop1-round1): the round's SCORECARD records
    append is locus-free in this unit — records-tree census pre-verified PASS
    0/0/0/0, exit 0 (SC-7 simulation of the drafted records text); re-run at
    the records commit.

Full assembled stanza (copy-paste; if this text and SC-6's file ever diverge,
SC-6's file is authoritative for the history sentences):

```python
"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d.

E22 DISPOSITION (arc3-loop1-round1; measured 2026-10-19 at HEAD e845c2b,
instrument sha256 36e96cd5…): the arc2-loop1-round3 carried debt "census
scope-table drift (FAIL undeclared=2 at 766-line HEAD vs PASS at 701-line
b21c0da — re-key or retire)" is DISCHARGED BY RE-KEY, none retired. Rows added
at 265e1aa (round-2 :702-767, round-3 :768-854, fixed-bound at the then-EOF;
RECEIPT widened) and shifted +1 at 6bc4c29 (r1 :636-702, r2 :703-768,
r3 :769-855) for the capability-row insertion at :622. At HEAD: PASS 0/0/0/0
(scope-errors [], g11 []); the declared SCORECARD bound :855 vs file EOF :1336
is the deliberate fixed-bound posture — the uncovered tail :856-1336 holds zero
loci in this unit at HEAD, and an injected tail locus reads UNDECLARED (FAIL,
exit 1). Records appends must stay locus-free in this unit or re-key the bound
in the same commit. Records-commit check (arc3-loop1-round1): the round's
SCORECARD records append is locus-free in this unit — records-tree census
pre-verified PASS 0/0/0/0, exit 0 (SC-7 simulation of the drafted records
text); re-run at the records commit."""
#!/usr/bin/env python3
```

## 3. Evidence (all SC-7-verified at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`)

- Census at HEAD: `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0
  unresolved=0)`, exit 0; full-output capture sha `3b677b8e…` — four
  independent captures, one digest (EX-26 / SC-6 / EX-30 / RV-11 files,
  sha256sum-verified by SC-7).
- E22 finding as recorded: `SCORECARD.md:850-852` ("E22 census scope-table
  drift (FAIL undeclared=2 at 766-line HEAD vs PASS at 701-line `b21c0da` —
  re-key or retire next calibration round)"). Prior disposition records:
  `SCORECARD.md:908`, `:990`, `:1096`; row-level history: SC-6 draft §3.
- Records-tree simulation (SC-7, `/var/tmp/sc7` scratch): the three census
  files at HEAD + this round's SCORECARD section (literal text in
  `scorecard-section-draft.md`) → census `PASS 0/0/0/0`, exit 0. Same tree +
  planted tail pin literal → `FAIL undeclared=1`, exit 1 (detector live; same
  class as SC-6 fixture A1). Commands and verbatim output in `seats/SC-7.md`
  §3.

## 4. Parent application notes

1. Land R9 (this stanza) at a work commit or the records commit — either is
   consistent; the census re-run at the records commit is required regardless
   (C3's claim closes there). The addendum's "pre-verified" clause is true for
   the drafted records text; if the merged records differ from the drafts,
   re-run and adjust before sealing.
2. If EX-28 landed its own stanza, prefer the landed bytes and treat this
   draft as superseded (note it in the round report).
3. Keep the shebang line directly after the closing `"""`.
4. Peer variants to reconcile before sealing (same-chain, all patch-text):
   PL-3 plan §6 recommends extending the stanza with the v9@HEAD flip and the
   r8-necessity explicitly; CR-5 A2/A4 require the causal chain (766-tree
   reproduction → r8 re-key necessary → PASS at `e845c2b`) in the header and
   the records-side disposition sentence (present in
   `scorecard-section-draft.md`); RV-11's `SCORECARD.md:908` wording patch is
   a separate proposal. The assembled stanza above already carries the re-key
   history and the fail-closed control; merge the fuller form if preferred
   before sealing.
