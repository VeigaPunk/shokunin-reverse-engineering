# arc3-loop1-round6 — frozen claims, 2026-10-19

Wave: 48 seats (within the scheduled 32–64 band), scheduled provider
`xai-oauth/grok-4.7-fast`. **Lane substitution at dispatch:** the xai lane
returned 403 out-of-credits on all 48 seats (zero delivered, ~30 s). Per the
operator directive the full roster re-dispatched on
`zai-coding-plan/glm-5.3-flash-low` (the zai glm-5.3-flash pin at MAX effort).
Recorded with cause, not a lane signal.

**Second substitution (same round):** the zai wave was interrupted by the
operator after 3 seats delivered complete, verified artifacts (PL-4's census
patch, EX-7's viaIR corpus draft, SC-3's rule-15 draft — all landed in the
wave tree). Per the operator directive the remaining 45 seats re-dispatched
on `antigravity/gemini-3.8-flash` (the antigravity/Cursor lane). That dispatch
was interrupted by the operator before any seat finished (0 delivered); a third
dispatch on `cursor/grok-4.7-xhigh-fast` was likewise interrupted at dispatch
(0 delivered). Per the operator directive the remaining 45 seats re-dispatched
a fourth time on `opencode-go-7/deepseek-v4.1-flash` (opencode-go key 7). The
three completed seats stand as delivered; the wave's effective roster is
3 zai + 45 opencode-go-7.
Roster frozen PRE-DISPATCH; the items array carries exactly the 48 names below.
Roster enumerated mechanically: 12 + 12 + 12 + 12 = 48.

Axis set: **operability (fleet; the census instrument's Frontier blind spot,
the R1 residual carried from rounds 4–5)**, **coverage (owned; a named
Unknown or a corpus completeness move)**, **depth (owned; a queue-drain rule
or a SKILL.md craft improvement)**. Claims are causally separable: the census
gate code (`.ufo/gates/`), corpus/knowledge, SKILL.md.

## C1 — operability (fleet): close the census Frontier blind spot (R1 residual)

Named debt (rounds 4–5 R1): `c1-census-v10.py`'s SCOPE table covers PROVINCE
only at lines 8-13, 15-26, 40-43, 44, 45-62, 64-71, 119-131. The `## Frontier`
section (73-93) and the post-unlock frontier (133-162) are UNDECLARED — so the
instrument reads PASS identically whether or not those bullets are stale. The
R4/R5 PROVINCE repairs were clause-audited by hand, not instrument-graded.

Claim: extend the census instrument so the Frontier-region staleness claims
become gradable — either by declaring the region in SCOPE (with a marker
scheme suited to bullets that carry no pin/version/path loci), or by adding a
declared secondary classification for locus-free bullets (a frontier-claim
register each bullet is checked against). The extended instrument must:
(a) still read PASS on the current tree; (b) FAIL (or flag a named disposition)
when a declared-stale literal is reintroduced into a Frontier bullet —
demonstrated by a seeded-fault arm in its selftest or a scratch-tree
measurement; (c) keep every existing SCOPE row and every current counter
intact. The instrument lives at `.ufo/gates/c1-census-v10.py`; a v11 or an
in-place extension is the lane's choice — record which and why.

Falsifiable before → after: the Frontier region is UNDECLARED at HEAD
(measured: `grep` the SCOPE table for any row covering 73-93 or 133-162 →
none); after, a seeded reintroduction of a stale literal (e.g. "real
solc/vyper-compiled bytecode untested" back into :91-93) is caught by the
instrument on a scratch tree, while the clean tree still reads PASS.

## C2 — coverage (owned): close one named corpus Unknown

The lane's corpus carries named Unknowns the rounds keep deferring. Pick ONE
that is provable on this host this round without an operator gate: candidates
include (a) the `viaIR` solc pipeline's dispatch shape (r3/r4 Unknowns name
it — compile a solc carrier with `via_ir` and characterize the dispatch), (b)
a Vyper `--no-optimize` / `-O codesize` dispatcher form (r4 Unknown — CR-1's
variants were probed K/K but never byte-characterized), or (c) another named
Unknown a seat can close with evidence. The chosen Unknown lands as a corpus
knowledge entry + map token; command A re-measures 84 → 85.

Falsifiable before → after: command A at the work commit — knowledge_files
84 → 85, mapped 85, missing [], dangling []; the entry's K/K or typed-refusal
evidence is cited inside it.

## C3 — depth (owned): queue-drain craft rule #15 or a craft-table improvement

The lane's `SKILL.md` Queue-drain craft section holds 14 rules (command A's
`rule_blocks=14`). Land rule #15 — a craft rule the arc has earned — OR a
material improvement to an existing rule's decision table. Candidate content
the arc has proven: (a) the "census-checked vs instrument-graded" distinction
(the R1 lesson — a substring census can read PASS on ungraded scope; the
clause-level audit is the real check), (b) the coupled-landing discipline
(the PROVINCE↔corpus and F5b↔C1 couplings — a repair whose truth depends on
a sibling landing must declare the dependency and land same-commit), (c) the
parsed-and-empty ≠ byte-absence distinction (the sweep's biggest catch).
Whatever lands must cite the corpus entries that earned it (rule #14).

Falsifiable before → after: `rule_blocks` 14 → 15 with the new rule's
citations resolving under command A's pattern; or a named rule's decision
table extended with a measured row.

## Seat roster (48, one AgentSwarm items array)

c1 chain (the census instrument, 12): PL-1..PL-4, EX-1..EX-4, RV-1..RV-4
c2 chain (the corpus Unknown, 12): EX-5..EX-12, CR-1..CR-4
c3 chain (the depth rule, 12): EX-13..EX-16, SC-1..SC-4, RV-5..RV-8
verdicts/convergence (12): VZ-1..VZ-4, CN-1..CN-4, CR-5..CR-8
