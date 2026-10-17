## CLAIM
Verifier for the outbound item routed by K1: "tsukuroi ADJ-06 | The l0-questions row exists" (`.ufo/waves/luna-round-10/K1.md:9,15`).

## METHOD
Read-only review: root `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (grep/awk); K1.md; tsukuroi worktree `PROVINCE.md:42,66-71`, `.ufo/reports/round-1/tsukuroi.md:72,89-95`, `.ufo/continuations/fleet-r1-interactive.json:77,85-92`, `LOG.md:329`; `git log`/`status`/`show` in fleet root (HEAD 0b1ac3b) and tsukuroi (HEAD f266220). No probes, network, sibling edits; only this note created.

## FINDINGS
- **Row exists, exactly once:** `grep -c "ADJ-06" .ufo/l0-questions.md` → `1`; line 42 = "tsukuroi | round-1 | … arbitrate the kaidoku/revenger shipped-artifact overlap before an ADJ-06 analysis is routed? Evidence: tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md sections 1-2 and its JSON source pins."
- **Durable at fleet root:** `git status --porcelain .ufo/l0-questions.md` → empty (tracked, clean; root HEAD `0b1ac3b`); row added by commit `79752af` ("fleet state: checkpoint WIP…", 2026-10-15 09:00:09 -0300).
- **Location precision:** `kaidoku-shokunin/.ufo/` contains no l0-questions.md, and tsukuroi's local `.ufo/l0-questions.md` holds only ROUTE-BINDING/RECEIPT-BINDING rows. K1's `.ufo/l0-questions.md:42` resolves root-relative only; K1 labels it "root L0 question", so the citation is consistent but not kaidoku-local.
- **Provenance:** tsukuroi states its asks stay lane-local (`LOG.md:329` "never a write to the shared side channel"; report `:89-91`; continuation JSON `:77` "integrator copies information to shared reports/ledgers"). The root row is integrator-side aggregation of tsukuroi's ask; content matches `PROVINCE.md:42` ("Request an ownership ruling before any RE work") and `:70` ("The integrator must arbitrate this shared scope").
- **Backing uncommitted on tsukuroi's side:** `adjacency-handoffs-fleet-r1.{md,json}` are untracked (`git status --porcelain corpus/knowledge/` → two `??` rows); the ADJ-06 table and Frontier note are 54 uncommitted worktree insertions (`HEAD:PROVINCE.md` = 19 lines vs 73 in worktree).

## THREATS
Existence is verified; durability of the cited backing is not — untracked sibling files could vanish without a commit. Row authorship (integrator-aggregated vs lane-written) is inferred from tsukuroi's stated local-only practice, not witnessed.

## VERDICT
CLEAN: the tsukuroi ADJ-06 l0-questions row exists (fleet-root `.ufo/l0-questions.md:42`, tracked and committed); the caveats concern provenance/location and uncommitted sibling backing, not existence.
