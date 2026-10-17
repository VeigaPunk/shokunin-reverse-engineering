## CLAIM
Independent Lane-B read of item 5 (`corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:215-216` vs `:82-84`), drafted from primary sources before reading Lane A, then diffed against Lane A's item-5 seats (V5, D5, G5, F5, R8, R3, C5, C1, C2, C4, P1/P2, K1): I confirm the overclaim; Lane A converges on substance. Integration-relevant divergences remain in the append's heading and the census gate's required strings.

## METHOD
Full read of the 375-line entry at HEAD `cfc84c2`; greps for `inferred|decorated`; `git status --porcelain` and `git diff HEAD` empty (nothing landed; worktree == HEAD, 375 lines). Recipe A run at HEAD → `{"mapped":72,"knowledge_files":72,"missing":[],"dangling":[],"citation_resolved_rules":9,"rule_blocks":9,"coverage_score":10.0,"depth_score":10.0,"revision":"cfc84c22"}`. Then read Lane A outputs. No REA/MCP/network; no tracked-file writes.

## FINDINGS
Converged: the union's four statuses (`:50-55`) are not all evidenced by recorded runs — verified (`:118-124`), unresolved/no-native-candidate (`:82-84`), unresolved/unsupported-native-evidence (`:192-197`), contradicted (`:112-113`); `inferred`/decorated-name-candidate is schema-only (`:53`), count `inferred:0` (`:83`); `confidence:"inferred"` (`:206,:244,:345`) is envelope metadata, not a status. Overclaim sites: `:7-8`, `:215-216`, `:326-334` (origin: round-4 V12b). Remedy: EOF append-only erratum with the omitted-run caveat; V5/D5's draft (`D5.md:12`) matches my independent draft on substance.

Divergences:
1. Heading: D5 drafts `### Erratum …` (would nest under `## Census note`, `:352-375`); C2 wants top-level `## Errata (luna-round-5, …)`; C4's census gate (`C4.md:13,17`) requires literal `## Errata (round 5 freshness` plus tail strings ('single queued-pairing', 'across separate runs', '0 verified', '0 inferred', '39 unresolved', '0 contradicted') that appear in no draft (grep: only C4.md). House convention across 49 corpus headings: `## Errata (…)`.
2. D5's text omits G5's confidence-metadata clause (`G5.md:10`) and carries the omission caveat only implicitly ("in this record").
3. `corpus/README.md:122` still claims "all four statuses live … unsupported" (same overclaim; outside every item-5 scope; F5:10). `:53` is already qualified.

## THREATS
Corpus-textual only; unrecorded runs could have produced `inferred` (no reachability claim); `/tmp` scratch uninspected. C4's gate is untested against a real integrated append; heading reconciliation is the parent's call.

## VERDICT
FINDING: overclaim confirmed by two independent reads; append the scoped erratum as a top-level `## Errata (…)` block at EOF, reconciling heading/gate strings before the census; README:122 remains a flagged residual.
