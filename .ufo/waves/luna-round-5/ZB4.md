## CLAIM
Item-4 convergence diff (Z protocol, `PB0.md:19`): Lane A and Lane B converge on targets and staleness facts; two real divergences remain — the `:163` remedy shape, and a gate-vs-draft wording mismatch; one unilateral (`:160` scope).

## METHOD
Primaries only, git-object reads at HEAD cfc84c2 plus 6645585/c265db9/2abd30f/6a71cd5 for the drift timeline. Swept all wave reports (two full-text greps) and read every item-4-touching seat (P0,V4,D4,F4,G4,R4,C2,C3,C4,C6,C7,C1,P1,P2,X1,X2,S2,K1; PB0,CB3,CB5,FB). Simulated `X1.md:34` and `C4.md:24` gates in Python on the V4:9/D4:18 text. No probes; no tracked edits.

## FINDINGS
CONVERGENT (adjudicated from primaries):
- Current targets `:131`/`:163`; inherited `:128`/`:160` now hold the r12-02 ledger row / sasquatch bullet. Timeline: 6645585 `:128`/`:157` → 2abd30f `:130`/`:162` → 6a71cd5 `:131`/`:163`; `SCORECARD.md:68-70`'s “:157→:160 correction” matched no revision.
- `:163` items exercised: map `:47`/`:53`/`:56`; knowledge `:116`/`:122`/`:125`; detail r5-02:181-186, r9-02:323-332, r11-01:335+. Nit cell overstated; `LOG.md:389-394,395-401` ⇒ 1 self-corrected pre-landing / 2 fixed at integration / 1 accepted. D4's `:131` row is byte-identical to HEAD:131 except that cell; its delete-text equals HEAD:163 byte-exact.

DIVERGENT:
- Remedy shape: delete (V4:8, D4:8-12, R4:9, CB3:10, P2:14) vs in-place replace (C2:11 alone; G4:8/PB0:12 “retire/restate”). Adjudication: deletion breaks no tracked current-surface citation — `corpus/lessons/2026-10-15-round-1.md:37` (:164) is baseline-pinned by that file's `:3,:7` declarations; `LOG.md:685` (:169) is a historical append; `SCORECARD.md:68-70` lies below :163. Only future HEAD-relative numbering shifts.
- Gate vs draft: `X1.md:34` and `C4.md:24` both require “2 fixes applied at integration”; C4 also spelled `four nits`/`one accepted`. V4:9/D4:18 say “4 nits… 2 fixed at integration… 1 accepted” → both gates evaluate False on the drafted text (simulated); a spelled variant (“four nits: one self-corrected pre-landing, 2 fixes applied at integration, one accepted”) passes both.

UNILATERAL: F4:9-15 `:160` “7z fallback covers today” qualification — no draft, no gate; C7:10/G4:10 ask to settle scope; Lane B silent. UNPROVABLE: current sasquatch/7z host state (no probes).

Residual flagged by both lanes, outside item 4: README `:122` “all four statuses live” (F5:10, C7:11, CB5:11) — item-5 class.

## THREATS
Gates simulated on strings; final parent wording unknown; drift timeline read from five revisions only. FB:15's “:131 = r14-02 lessons row” label is loose (it is the round-13-distillation row) but its quoted texts are exact.

## VERDICT
FINDING: targets and staleness fully converged; resolve `:163` delete-vs-in-place and pick wording satisfying X1:34+C4:24 — current drafts fail both.
