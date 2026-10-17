## CLAIM
2nd opinion on the r9-02 tension (`:215-216` vs `:82-84`): is the "four statuses complete" claim real, and is Lane A's append-only erratum disposition correct?

## METHOD
Independent first pass on primary sources only (full `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md` at HEAD `cfc84c2` via `git show HEAD:` + worktree; `PROVINCE.md`, `SCORECARD.md:92-123`), then Lane A outputs (V5/F5/D5/R2/R3/C2/C7/X1/P0/P1; r4 V12b) compared and their pointers re-checked against HEAD. Ran command A at HEAD; ran X1's R9-02 census predicate on D5's extracted erratum text. `git status --porcelain`: only untracked `.ufo/` dirs; no tracked edits; no probes/MCP/network.

## FINDINGS
- Tension REAL. Schema union (:50-55) defines four variants; recorded runs demonstrate three: `verified` (:118-124, run 11 :306), `contradicted` (:106-124, run 10 :305), `unresolved` with both bases (:78-95, run 9 :304; :184-213, run 13 :308). `inferred` occurs only as `inferred:0` (:83); envelope `confidence:"inferred"` (:206, :244) is a different field. Claims at :7-8, :215-216, and :326 "four distinct typed statuses" overstate/miscount. Assigned pointers are exact at HEAD (no drift). Scope limit (matches R2/R3): the record cannot establish that no omitted run observed `inferred`.
- Lane A disposition is sound: V5's finding, F5's corroboration, D5's verbatim erratum draft; my draft-matched-before-comparison. Nothing landed: worktree == HEAD, EOF still :375; P1 item 5 Pending.
- Integration hazard 1 (C2, confirmed): append as new top-level `## Errata (luna-round-5, …)`; D5's `### Erratum` under `## Census note` (:352) would nest wrongly.
- Integration hazard 2 (new): D5's erratum verbatim FAILS X1's R9-02 census guard — predicate run: `four.status` True, negation regex False ("unobserved" ≠ `not.observed`). Add e.g. "this record does not establish that no run ever produced `inferred`" (matches `does.not.establish`; also tightens scoping).
- Residuals, parent-owned: `corpus/README.md:122` still says "all four statuses live … unsupported" (:53 already qualified); `LOG.md:286-289` stale ("observes all four statuses live"). Outside item 5's target file; flag for integration decision.
- Invariant held: command A at HEAD → mapped/knowledge_files 72/72, rules 9/9, coverage/depth 10.0, missing/dangling empty; token set 72.

## THREATS
Textual/lexical verification only; historical `/tmp` receipts absent, so `inferred` stays "not evidenced", never "unreachable". The guard mismatch depends on X1's exact regex; parent may widen the guard instead of the wording. Line pointers valid at `cfc84c2` only.

## VERDICT
FINDING: tension confirmed (3 of 4 status variants recorded); append the scoped V5/D5 erratum as a top-level EOF `## Errata` with a "does not establish" clause so X1's census guard passes.
