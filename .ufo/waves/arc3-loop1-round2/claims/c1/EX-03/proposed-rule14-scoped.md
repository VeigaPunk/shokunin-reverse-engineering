# Proposed rule #14 text, scoped — PATCH TEXT (NOT APPLIED) — seat EX-03 (adversary-executor)

Wave arc3-loop1-round2, chain c1. Insert at the craft-section tail, before the
`## Config custody for live-probe rounds (SOP)` marker (the shape of EX-05's
harness `claims/c1/EX-05/insert-rule.py`). Nothing was applied; this seat wrote
only its report, `claims/c1/EX-03/attacks.md` + evidence, and this file.

Design deltas vs the frozen wording (each fixes a measured defect in
`attacks.md` §1–§4):

1. **Trigger names whose identity** — "self" is measured-empty (0/4,022 files);
   the origin incident is a *declared subject*. The text says "an artifact whose
   verification block declares the size/hash/line-count of itself **or of a file
   it produces**".
2. **Duty scoped to the author's handoff** — re-derivation is owed at the
   declaring artifact's last revision *before it is cited or landed*; a pin on
   another seat's artifact is scoped to the revision it names (fixes §1b
   third-party-pin overreach).
3. **Declared form** — the identity block names its subject; a checker can then
   bind claim→bytes (§2b/§2c).
4. **Honest citation disclosure** — the incident is cited at its wave paths
   (they are the evidence) *and* the principle-only corpus citation is labelled
   as exactly that, so the record does not present an adjacent citation as
   incident-recording (§4b).
5. **Metric caveat stated in the record, not in the rule** — command A counts
   blocks with resolving citations; it does not discriminate craft (measured:
   content-free control scores identically, §4a).

## Literal block text (insert as one rule block)

- **An artifact's identity declaration must be re-derived against the bytes it
  names, at the declaring seat's last handoff.** A verification block that
  states the size, hash, or line count of itself or of a file it produces holds
  only against that subject's current bytes: the declaring seat re-derives the
  identity after its last revision before citing or handing the artifact off,
  a stale declaration voids the verification block rather than the work, and
  the integrator records the fresh identity of the landed bytes in the round's
  records. A pin one seat records on *another* seat's artifact is scoped to the
  revision it names — later revisions by the owning seat do not restale the
  pin. Origin (arc3-loop1-round1): the EVM entry patch churned mid-wave and its
  recorded identity (8,316 B, `f95c5a05…`) stopped describing the file it
  produced — an independent re-apply read 8,598 B, `d8d85949…`
  (`.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`;
  VZ-1 debt D9), and the landed bytes were re-derived at landing (10,225 B,
  `dd986f56…`, `SCORECARD.md:1366`). The re-derivation discipline's recorded
  principle for evidence ids — an id held across a day and re-derives
  byte-exact — is `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`;
  that citation records the principle, not this incident (the incident lives in
  the wave paths above).

## Expected effect under command A (measured by me, `attacks.md` §6)

- rule blocks 13 → 14; the block above resolves via
  `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11` → 14/14, depth 10.0
  (the subject-adjacent citation is disclosed in the text, which is the point
  of delta 4 — the alternative, T1's incident-only form, measures 13/14, 9.29).
- prior 13 rule blocks byte-identical under a clean insertion (measured True).

## If the parent prefers the frozen wording verbatim

Land `claims/c1/EX-05/fallback-rule14-candidate.txt` as-is and record in the
round's SCORECARD/LOG text that (a) the rule's trigger as phrased matched zero
artifacts at the round-1 origin (my §1a), and (b) its `corpus/knowledge`
citation is subject-adjacent — not incident-recording (§4b). The record should
not describe 14/14 as discrimination of craft (T3 control, §4a).
