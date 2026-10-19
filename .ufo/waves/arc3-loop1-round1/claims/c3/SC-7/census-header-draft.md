# Census-header change text — C3 records draft (SC-7, arc3-loop1-round1)

Seat SC-7 · chain c3 · role scribe · 2026-10-19. **STATUS: SUPERSEDED by
EX-28's landing.** The census-writer seat wrote the real target during the wave
(`.ufo/gates/c1-census-v10.py`; sha256 observed `36e96cd5…` → `30060258…` →
`6f1d19ff…` as EX-28 worked, ~10:17-10:19Z — a stability monitor ran at close;
the parent re-verifies at the records commit). SC-7 did not write the target.
This file keeps the pre-landing proposal as an audit trail and records the
SC-7 verification of the landed state.

## 1. Landed state (EX-28's stanza; SC-7-verified)

The landed header stanza states (worktree diff vs HEAD `e845c2b`):

- E22 **DISCHARGED AT HEAD BY RE-KEY**; nothing retired; the finding does not
  reproduce under v10 — PASS 0/0/0/0, four independent captures one digest
  `3b677b8e…`; the two blocks UNDECLARED under v9 (`:731-737`, `:747-766`) now
  sit inside the round-2 row and read current-ok; v9 stays red at HEAD by
  construction (RV-11).
- **One stale row found and re-keyed:** `("PROVINCE.md", 45, 62, "DATED")`
  named marker line 40 — the 40-43 row's intro, outside its own range; G15
  could not see it. Re-keyed to line 45 with marker regex `r"2026-10-13"`
  (the row's own receipt text). **G18 added**: every DATED row's marker line
  must lie inside the range it dates; a violation is a SCOPE-ERROR (fail
  loud). The re-key is range-neutral (CR-5's creep differ: no signature).
- Refused branches, each measured: tail expansion is **fail-open** (a planted
  pin inside a declared DATED range reads "historical" → PASS; the fixed bound
  is kept — a locus past `:855` reads UNDECLARED → FAIL); retiring the
  capability rows `:619`/`:620` fails both ways (UNDECLARED or AMBIGUOUS);
  CURRENT→DATED flips refused as creep.
- Standing rule restated for records commits: text appended past the declared
  bound must be locus-free in this instrument's unit (no `rea-agents@` pin
  with a version, no bare `6.x.y`, no `~`//-absolute `path:line`) or the bound
  must be re-keyed in the same commit as a DATED row whose marker line carries
  that section's own date/round token.

SC-7 verification of the landed instrument (2026-10-19 ~10:19Z, sha
`6f1d19ff…` as last observed):

- `python3 .ufo/gates/c1-census-v10.py --quiet` at the worktree →
  `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0,
  scope-errors [].
- Both simulation trees re-run **under the landed instrument**: records-text
  tree → PASS 0/0/0/0, exit 0; + planted tail pin → FAIL undeclared=1, exit 1.
  (Commands + outputs: `seats/SC-7.md` §3.)

## 2. What remains for the parent (from this draft)

Nothing for the header itself — the landed stanza is the disposition. Optional:
if the records-commit pre-verification should be recorded IN the header, the
SC-7 addendum sentence (updated for the landed state) is:

    Records-commit check (arc3-loop1-round1): the round's SCORECARD records
    append is locus-free in this unit — records-tree census pre-verified PASS
    0/0/0/0, exit 0 (SC-7 simulation, re-run under the re-keyed instrument);
    re-run at the records commit.

Otherwise the evidence lives in the round records (the C3 bullets in
`log-entry-draft.md` / `scorecard-section-draft.md`) and `seats/SC-7.md`.

## 3. Pre-landing proposal (audit trail; SUPERSEDED — do not apply)

Pre-landing, this draft proposed the header change as SC-6's P1 stanza
(`claims/c3/SC-6/e22-disposition.draft.md`, sha256 `ed5cf1f7…`) plus one SC-7
records-commit sentence; EX-26 (`f467814d…`) and PL-3 §6 carried sibling
variants. EX-28's landed stanza supersedes all of them and goes further (the
G18 stale-row finding + refused-branch measurements). If any reader needs the
pre-landing assembled text, it is preserved in this file's git-tracked history
within the wave artifacts; it must not be applied over the landed stanza.

## 4. Evidence (SC-7-verified)

- HEAD: `e845c2b524ad2e59871e004c51a1386e192a74ab`; instrument sha timeline:
  `36e96cd5…` (pre-EX-28) → `30060258…` (10:17:32Z) → `6f1d19ff…` (10:18:16Z).
- Census at HEAD (pre-EX-28): PASS 0/0/0/0, exit 0; full-output capture sha
  `3b677b8e…` — four independent captures, one digest (EX-26 / SC-6 / EX-30 /
  RV-11 files, sha256sum-verified by SC-7).
- Census at the worktree (post-EX-28, `6f1d19ff…`): PASS 0/0/0/0, exit 0.
- E22 finding as recorded: `SCORECARD.md:850-852`; prior disposition records:
  `SCORECARD.md:908`, `:990`, `:1096`; row-level history: SC-6 draft §3,
  RV-10 bounds audit, CR-5.
- Records-tree simulation: see §1; both runs re-executed after the landing.

## 5. Parent application notes

1. Prefer the landed bytes; do not apply §3.
2. The records-commit census re-run is required regardless (C3's claim closes
   there). The drafted records text is pre-verified PASS under the re-keyed
   instrument; if the merged records differ from the drafts, re-run and adjust
   before sealing.
3. CR-5's census-sha pin recommendation is satisfied by naming the instrument
   sha in the round records (the SCORECARD draft carries the measurement sha;
   the parent fills the records-commit sha in the re-run slot).
