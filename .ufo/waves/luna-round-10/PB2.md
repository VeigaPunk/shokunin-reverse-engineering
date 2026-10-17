## CLAIM
Independent round-10 LOG/SCORECARD drafts from read-only evidence at HEAD `c343939`, diffed against lane-A seat P2's draft (`.ufo/waves/luna-round-10/P2.md`). Drafts are provisional: no round-10 report or MANIFEST row exists yet.

## METHOD
`git diff --numstat <c>^ <c> -- LOG.md SCORECARD.md` for the nine records commits plus `c343939`; command A recipe (`SCORECARD.md:92-123`) run at `6e83a20` and `c343939`; Python census of kaidoku rows in `/home/vgpnk/Projects/shokunin/MANIFEST.json`; grep over nine round reports, `SHONEN.md`, `K1.md`; read-only sibling spot-checks. Only this file written.

## FINDINGS
Command A, both revisions: `{"citation_resolved_rules":9,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":79,"mapped":79,"missing":[],"rule_blocks":9}`.

Append-only: LOG 0 deletions in all nine records commits. SCORECARD deletions in five — `a4bd355`:4, `a9580eb`:8, `0772d54`:7, `cfc84c2`:1, `6e2ee8f`:1 — every deletion hunk above the parent's first `## luna-round-` header (living Owned-axes/Open-gaps rows only); r5/r6/r8/r9 and `c343939` pure-append. P2 omits this; lane A lists 2/3/4/7, missing `a4bd355` (round 1, the first instance).

MANIFEST: six rows carry enum+prose verdict values (`:1509,:2791,:2805,:2819,:2846,:2847,:2860`); three carry non-enum `verified (…)` (`:1522,:1535,:1548`); three carry non-`train` types. Parent-owned ledger; not rewritten.

Dispatch: r2/r4/r5/r6 reports name short-count occurrences 1–4; r7 repaired by 5-seat backfill (`luna-round-7/kaidoku.md:4`); r6 census 127 distinct (`luna-round-6/kaidoku.md:47-51`). SHONEN 4×[~] (`SHONEN.md:6-12`). Outbound verified: Tameshi `verification-patterns-fleet.md:35,73,102`; tsukuroi `PROVINCE.md:42,70-71`.

Drafts (integrator-editable):
> LOG: "luna-round-10 — arc closeout: census, debt ledger, SHONEN. Command A at `6e83a20`/`c343939`: 79/79, 9/9, 10.0/10.0. Append-only audit: LOG clean; SCORECARD living-row edits in rounds 1–4,7 confined to the current-state block. Five dispatch short-counts (r2,4,5,6,7; r6=127 distinct). MANIFEST enum-prose rows named. Carried and outbound items routed, not resolved here."
> SCORECARD: "## luna-round-10 — arc closeout: measure at the integrated HEAD; record only review-derived debt statuses and enum verdicts; declare the required saturation line + window N (`AXES.md:65-83`, `c343939`); Capabilities row only with a running demonstration; SHONEN 4×[~] retained; records-only round claims no improved axis."

Diff vs P2: mine adds the five-commit append-only census (incl. r1), the `c343939` saturation/Capabilities obligation, the `c343939` re-measure, and the outbound items; P2's counts (short-counts, 127, 4×[~], 79/79 at `6e83a20`) reproduce; no factual conflict.

## THREATS
Living-row sanction is an operator call — no protocol text authorizes rewriting SCORECARD's top block (`PROTOCOL.md:447` covers LOG only). No round-10 report/row exists, so final verdicts, admission and debt disposition stay unasserted. P2's file may be revised after my 22:37 read. Sibling checks read-only.

## VERDICT
FINDING: drafts delivered; append-only deviation spans five records commits (lane A/P2 list four, missing `a4bd355`); saturation declaration and MANIFEST prose rows remain open gates.
