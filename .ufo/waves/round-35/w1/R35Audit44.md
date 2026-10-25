# R35Audit44 — predicate text identity audit

Seat: `R35Audit44`; item: compare predicate text identities. Read-only review; only lane write is this report. No scoring, VCS mutation, installs, delegation, or source-tree access.

## Evidence

Compared decoded JSON predicate strings with Python `==` (Unicode string equality; no whitespace normalization) and counter `PREDICATE` constants parsed from the counter source. Both predicates are byte-identical between:

- `.ufo/waves/round-35/claims-canonical.json` at HEAD and at `2323d197456f1328459d9420aff025cffbcb3e27`;
- each corresponding counter constant at HEAD;
- each corresponding committed do-nothing receipt (`controls/c1-do-nothing.json`, `controls/c2-do-nothing.json`);
- the historical `claims-frozen.json` predicates at HEAD.

Observed `True` for all eight canonical-vs-counter/receipt comparisons and both canonical-at-HEAD vs canonical-at-2323d197 comparisons. Both controls name `freeze=2323d197456f1328459d9420aff025cffbcb3e27`. Predicate lengths: C1 478 characters, C2 684.

Commands/logic used:

```text
read plans/round-35-claims.md; .ufo/waves/round-35/claims-canonical.json; both counter sources; controls/*.json; freeze-status.md
Python: parse JSON; ast.parse counter modules and ast.literal_eval PREDICATE; compare strings with ==
git show <revision>:<path>; SHA-256 each counter blob at selected revisions
```

## Caveats / first falsification

1. **Plan identity assertion is not literally met.** The plan's claim-discipline bullet says the predicate sentence is byte-identical “in this plan,” but the plan gives after-state bullets and does not contain the literal `P35-c1:` or `P35-c2:` sentence (confirmed by reading it and byte-searching). Current identity is established across canonical claims, counter constants, and receipts—not plan. This is documentation/evidence-contract mismatch, not a mismatch among the machine-scored predicate copies.
2. **A different freeze-gate debt remains.** `freeze-status.md` records the round-34 `freeze-integrity.py` failure: its discovery selected the earlier first-added `claims-frozen.json` at `13d7a815`, pinned to earlier counter hashes. Read-only `git show` hash checks confirmed those earlier hashes differ from final counter bytes; canonical file `claims-canonical.json` is absent at that early revision and present at `2323d197`. At `2323d197`, final counter hashes match canonical instrument pins (C1 `e28792c7…`, C2 `576c14dd…`). Thus predicate text identity does not cure the recorded `INSTRUMENT_REVISED` / setup-order debt; do not describe it as a clean freeze-integrity pass.
3. `claims-canonical.json` has `instrument_revision=d2729cba…`; that prep revision predates the claim file and carries earlier counter bytes. The snapshot's explicit `instrument_supersessions` mentions `a85ca674…`, whose counters also do not match final pins. This is consistent with the disclosed setup-order history, not a predicate text difference.

The plan/claim wording also differs in detail (e.g. plan says “no later than the first commit” and “8 cells (NF=9)”; predicate uses “committed before the first” and “exactly eight cells”). The frozen counter checks are governed by the canonical predicate and its own implementation; this report does not reinterpret or alter the frozen scope.

## Smallest safe correction / disposition

Do not edit the frozen predicates or counters. Correct the plan's identity assertion in a future un-frozen documentation revision to name the actual identity set (canonical JSON, counter constant, receipts), or preserve a literal predicate copy at a future freeze if plan-level byte identity is required. Keep the existing setup-order failure disclosed; no retroactive re-freeze or claim that text identity resolves it.

Limits: no counter execution or synthetic mutation; identity comparison is static. No code or claim changes proposed.

Report: `.ufo/waves/round-35/w1/R35Audit44.md`
