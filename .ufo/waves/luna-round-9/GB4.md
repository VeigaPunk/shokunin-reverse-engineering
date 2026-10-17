# GB4 — P0/PB0 review: plans consistent?

## CLAIM
Seat GB4 (lane B): P0's integration plan (lane A) and PB0's verification brief (lane B) are consistent on all four items' targets, dispositions, and post-integration invariants; two integration rulings remain open. Read-only; only this file written.

## METHOD
- Read P0, P1, P2, PB0, PB2, X4, G4, H, E2, R5, B2, B3, T1, CB4, C2, S1.
- Re-ran command A verbatim (`SCORECARD.md:92-123`, `REV=a280e07133f52f719b0805fc73c0b997e77b5062`): `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07133f52f719b0805fc73c0b997e77b5062", "rule_blocks": 9}`; `git diff --quiet HEAD --` exit 0.
- First-hand anchors: r4-16 `:751-752` two-site text (EOF `:925`); r12-01 errata headers `:97`,`:110`, bullets `:99-104`,`:112-121`, "7 values" `:117`; `PROVINCE.md:114-116` verbatim refusal; jq "benign" `:217`,`:236-237`, "not binary compromise" `:219`, EOF `:242`; stale `:107-109` cites at `SCORECARD.md:79` and `corpus/lessons/2026-10-15-round-1.md:152`; baseline sha256 r4-16 `622e3661…`, jq `541f3499…`.
- No probes, network, `/tmp` access, deletions, or tracked edits.

## FINDINGS
- **Consistent:** item 1 pointer-only to r4-16 EOF, no supersession claim (A3/H/PB0); item 2 home = SCORECARD (X4) with B3's no-waiver guard; item 3 no deletion, operator-owned, audit scope caveat (C1/Q3/R5/PB0); item 4 append-only qualification, PROVINCE untouched; invariants 79/79, 9/9, 10.0 and non-target byte identity (G4/P0/PB0/PB2).
- **Open ruling 1 (item 2 mechanics):** B2 drafts a mid-file "insertion" near the recipes (`B2.md:10-13`; T1 simulates adjacency), while G4 asserts each target's final blob *starts with* its BASE — a mid-file insertion satisfies T1's parser test but breaks G4's prefix check; R5/CB4/PB0 already flag the mechanics ruling.
- **Open ruling 2 (item 4 policy):** P0/P1/P2 keep a scoped "benign"; D3/PB2/Z5 prefer explicit disavowal/retraction and loci breadth (r2 `:12`,`:219`; r3 `:60`,`:136` separate) — PB0 lists it as a parent call.
- **Minor:** P0's r12-01 range `:97-114` ends mid-bullet (`:115-121` continues); P1/P2/PB0 ranges all resolve — anchor variance only. TB1's 63-hex defect concerns G3's recorded hash, not the plan.

## THREATS
Snapshot at `a280e07`; lane-B peers still landing. No post-landing byte check exists. "7 values" not re-derived; `/tmp` not inspected. Ruling 1 is judged from drafts, not landed bytes.

## VERDICT
FINDING: plans consistent on targets/dispositions/invariants (command A 79/79, 9/9, 10.0 re-verified); two integration rulings remain — item-2 note placement vs G4's blob-prefix assertion, item-4 qualifier-vs-disavowal/loci.
