# proposed patch TEXT — the four SKILL.md craft-section line pins (RV-11, c3)

Target: `.ufo/gates/citation-drift/pointer-table.json` (EX-41's landed pair).
Status: **proposal only — NOT applied.** Reviewer artifact; the parent adjudicates.
Rule-#11 conformance is satisfied either way; this is a noise-vs-cost choice, not a violation.

## What is measured

The four new entries `skill-rule14-cr2-identity` (:246), `skill-rule14-verdict-identities`
(:248), `skill-rule14-entry-recheck` (:252), `skill-rule14-log-fresh-identity` (:254)
pin a **citing line inside SKILL.md's craft section** (the queue-drain rule-#14 block,
`:240-255`). `extracted` grades the citing line by number; when the craft section gains
one line above `:246`, all four rows report `citation_dead` even though the citations
only moved. Measured on a scratch clone (`/var/tmp/rv11-arc3r3/attack-clone`):

```
fixture A rev a0b3787 (one line inserted before SKILL.md:246), landed table:
  citation_dead entry=skill-rule14-verdict-identities SKILL.md:248 states no resolvable pointer
  citation_dead entry=skill-rule14-entry-recheck       SKILL.md:252 states no resolvable pointer
  citation_dead entry=skill-rule14-cr2-identity        SKILL.md:246 states no resolvable pointer
  citation_dead entry=skill-rule14-log-fresh-identity  SKILL.md:254 states no resolvable pointer
  CITATION_DRIFT_VERDICT: failed findings=4 exit=1
control A-control (baseline 31-entry table, same fixture): clean findings=0 exit=0
control B (landed table, one bullet appended AFTER the block): clean findings=0 exit=0
```

Precedents: the r4 measurement (landing rule #11 inserted above the rule list
invalidated 9 of 11 SKILL.md pins, `SCORECARD.md` arc2-loop1-round4 section) and this
round's own live instance — the arc3-r1 round report's `SKILL.md:371` now holds
`## Refuses` (round 2 inserted rule #14 above the registry table; verified at HEAD and
recorded in the table's `exempt` ledger).

## Proposal A (recommended if the false-red surface is worth removing): anchor siblings

Add four `anchor`-class siblings with `pin_line`, which report `citation_moved` (true)
instead of `citation_dead` (wrong class) when the line shifts. Paste-ready objects
(insert alongside their `extracted` siblings; existing rows unchanged):

```json
{"id": "skill-rule14-cr2-identity-anchor", "kind": "anchor", "file": "SKILL.md",
 "must_match": "CR-2\\.md:86-89", "pin_line": 246,
 "note": "moved-line companion to skill-rule14-cr2-identity: the #14 incident citation must exist somewhere in the craft section; an insert above the block is a move, not a death."}
{"id": "skill-rule14-verdict-identities-anchor", "kind": "anchor", "file": "SKILL.md",
 "must_match": "claims/c1/verdict\\.md:149-153", "pin_line": 248,
 "note": "moved-line companion to skill-rule14-verdict-identities (same rationale)."}
{"id": "skill-rule14-entry-recheck-anchor", "kind": "anchor", "file": "SKILL.md",
 "must_match": "2026-10-19-arc3-r1-evm-real-solc\\.md:7", "pin_line": 252,
 "note": "moved-line companion to skill-rule14-entry-recheck (same rationale)."}
{"id": "skill-rule14-log-fresh-identity-anchor", "kind": "anchor", "file": "SKILL.md",
 "must_match": "LOG\\.md:1411-1412", "pin_line": 254,
 "note": "moved-line companion to skill-rule14-log-fresh-identity (same rationale)."}
```

Cost: entries 57 → 61; the table digest changes → the `expected.json` pin must be
re-derived in the same commit (the F3 coupling; the probe's own preflight enforces it).
`pin_line` is the line the anchor's content sat at when landed (the probe's
`anchor` branch: content found off `pin_line` → `citation_moved`).

## Proposal B (cheaper): records sentence only

Land the residual in the round's SCORECARD/LOG section, verbatim or equivalent:

> The four SKILL.md rule-#14 pins are line-pinned into the craft section; measured on a
> scratch insert fixture, a one-line insert above `:246` reads `citation_dead` for all
> four (a misclassified move, not a dead citation) while the append-after control stays
> clean and the pre-round 31-entry table is immune to the same fixture. The class is
> the r4 line-pin fragility; the pins are accepted with the false-red surface named.

## Why this is not a rule-#11 defect

None of the four entries touches an operator-mutable path and none carries a bare
`config.toml:N` token (audit rows: `claims/c3/RV-11/runs/landed-audit.json`, all
CONFORM). The finding is about the *false-failure class* the r4 precedent names, not
about forbidden pins.