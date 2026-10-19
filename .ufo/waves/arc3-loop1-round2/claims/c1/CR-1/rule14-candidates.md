# CR-1 — candidate rule #14 texts, judged against command A's real parser

Command A (SCORECARD.md:104-122) counts a craft rule "citation-resolved" only if
the rule block contains at least one `corpus/knowledge/<name>.md[:start[-end]]`
reference whose line span exists inside that file. A rule text citing only
wave-tree paths scores **unresolved** — which, at 14 rules, drops
`depth_score` from 10.0 to `round(10*13/14, 2)` = **9.29**.

## T1 — incident-only citations (the honest form of the claim as frozen)

- **An artifact that records its own byte-identity must re-derive that identity after every revision; a stale self-identity voids the verification block, not the work.** The arc3-loop1-round1 entry patch churned mid-wave: its recorded identity (8,316 B, `f95c5a05…`) stopped describing the artifact it produced — an independent re-apply read 8,598 B, `d8d85949…` (`.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`; VZ-1 debt D9, `.ufo/waves/arc3-loop1-round1/claims/c1/VZ-1/verdict.md:149-166`), and the landed bytes were re-derived at landing (10,225 B, `dd986f56…`, `.ufo/waves/arc3-loop1-round1/claims/cross/wave-summary.md:50`). Re-derive before citing; the integrator records the fresh identity at landing.

Prediction under command A: refs = [] → `valid=False` → 13/14, depth 9.29.

## T2 — T1 plus one adjacent corpus/knowledge citation (laundering-risk form)

- (T1 text, plus:) The re-derivation discipline's analogue in the evidence-id family is recorded where an id held across a day and re-derives byte-exact (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`).

Prediction: 14/14 — but the cited file does not record the incident; the corpus
reference is *adjacent*, not the demonstrated incident. Passes the metric while
weakening the rule's actual citation integrity.

## T3 — decoration control (no incident, no discipline content)

- **Cite the source you measured, not the one you remember.** (`corpus/knowledge/2026-10-13-r3-evm-interface.md:23-25`)

Prediction: 14/14 — demonstrating that command A's rule count alone cannot
discriminate craft from decoration. The discriminating criterion must be the
second half of the survival test: a real failure mode caught.
