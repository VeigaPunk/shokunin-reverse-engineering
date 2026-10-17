## CLAIM
2nd-opinion r9-02 erratum draft from VB5.md, as assigned. VB5's disposition holds: the `:215-216` vs `:82-84` tension is real; the draft below (top-level `## Errata`, census-guard clause included) is the minimal fix.

## METHOD
Independent primary pass first (before VB5.md existed): r9-02 file at HEAD `cfc84c2`, README r9-02 rows, round-4 debt record — substance matched VB5's before reading it. VB5.md then consumed as the designated input; its pointers re-checked at HEAD: EOF `:375`, `:7-8`/`:83`/`:215-216`/`:326` exact, LOG.md:286-287 spot-verified ("…observes all four statuses live"), no tracked edits (`git status --porcelain`). No probes/MCP/network; no Lane A output read. X1-guard regex left unverified (X1.md excluded by "From VB5.md only").

## FINDINGS
Tension confirmed: schema pins four variants (:46-55); runs demonstrate three — `unresolved` both bases (runs 9, 13), `contradicted` (run 10), `verified` (runs 8/11) — plus the typed refusal (run 7); `inferred` occurs only as `inferred:0` (:83); envelope `confidence:"inferred"` (:206, :244, :345) is a different field. Draft for EOF append as a new top-level section (not nested under `## Census note`):

```
## Errata (luna-round-5, 2026-10-16, append-only)

- **Status-taxonomy qualifier (axes :7-8; candidate-5 closing :215-216;
  Summary :326):** "all four verification statuses observed live" / "the
  four statuses … complete row 13's observable behavior surface" overstate
  this record. The schema union (:46-55) pins four variants; recorded runs
  demonstrate three — `unresolved` with both bases (`no-native-candidate`
  run 9; `unsupported-native-evidence` run 13), `contradicted` (run 10),
  `verified` (runs 8/11) — plus the typed refusal (run 7); :326's "four
  distinct typed statuses" counts four (status, basis) outcomes, two
  `unresolved`. `inferred` (`decorated-name-candidate`) is not observed in
  any recorded run here (sole count `inferred:0`, :82-84); envelope
  `confidence:"inferred"` labels (:206, :244, :345) are the workflow
  epistemic grade, a different field. Read the claim as three of four
  variants recorded; this record does not establish that no run ever
  produced `inferred` — a decorated-name probe remains an open residual.
  Historical observations above remain true as written.
```

Parent-owned residues outside this file's scope: `corpus/README.md:122` (`:53` already qualified in round 4) and `LOG.md:286-289`.

## THREATS
Guard clause used verbatim per VB5; if X1's regex differs, parent may widen the guard. `inferred` stays "not evidenced", never "unreachable". Pointers valid at `cfc84c2` only; the load-bearing text for any guard variant is "does not establish".

## VERDICT
FINDING: erratum draft finalized for parent append — top-level EOF `## Errata`, cites `:7-8`/`:215-216`/`:326`, 3-of-4 qualification with the "does not establish" clause; README:122 + LOG.md residues flagged parent-owned.
