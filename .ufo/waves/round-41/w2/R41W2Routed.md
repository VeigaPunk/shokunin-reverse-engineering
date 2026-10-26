DEFECTS FOUND — attacked the Round-41 landing and routed-defect disposition at dispatch tip `7a24ff74736e84b1903db7ba01891c406a6e32a2`, focusing on coverage, depth and calibration.

## Evidence and verdicts

### R41-C1 — coverage: the bounded landing is supported; provenance remains open

The frozen score at `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4` records `carriers_matched: 4`, `met_target: true`, `exit_code: 0`, `frozen_path_changed: []`; the supplementary `c1-extra` receipt records `met: true`, exit 0. Its frozen C1 paths did not change between freeze `d764389e9cbe61b9d1b07538ff3bff02d50bb34f` and measured revision (the only diff in the claim’s listed frozen paths is none; the displayed diff for `plans/round-41-claims.md`, C1 tools/spec, and C1 carrier tables was empty). The four-carrier score is consistent with the independent oracle challenge: `R41W2C1Oracle.md` reports rebuilt carrier/oracle tables, AVM-vs-auto equality, and direct `sasquatch-v4be` results with zero mismatches on V3, V4, L3 and L4.

**R40-CL1: fixed for this claim’s specified exact-path surface.** The frozen claim names a derivation-rooted, whole-segment path rule; the C1 counter compares paths against the resolved root rather than relying on the old suffix matcher. L3/L4 hold the two collision directions. The independent oracle review corroborated all four specified table/carrier pairs. Do not generalize this to arbitrary REA path shapes or carriers.

**R40-CL2: open, explicitly disclosed.** C1’s own limits state that the rerun cannot prove which process wrote the committed receipt. `c1-counter.py:768–775` also implements `provenance_ok` as a substring test (`PROV_SEGMENT in output_directory`) plus a `..` exclusion; this accepts a containing path, not necessarily a path rooted at the intended scratch segment. Thus the evidence supports the bounded extraction/projection claim and the declared limitation, not receipt provenance. The score field `run_provenance_ok: true` must not be presented as proof of authorship.

### R41-C2 — depth: honest NOT MET; a counter lookup defect, not a table disagreement

The committed score `c2-at-e9a24d07.json` records 52/52 pair matches and 13 distinct decisions, but `exit_code: 1`, `met_target: false`, and `bindings_false: ["observed_features_match_declared"]`. The missing declared tuples are precisely `C01`–`C12`; all named classes are reported `match`.

The frozen manifest’s `declared_schema.location` says the binding tuple lives at `carriers[].declared`; `heldout-gen-v3.py` writes that key for every carrier, including combos (`:1464`), and documents it at the manifest schema (`:1820–1822`). The frozen counter’s lookup at `c2-counter.py:1495–1506` instead searches `class_expected.features`, `features`, `declared_features`, or a per-class map, never `declared`. Consequently it reports C01–C12 as `declared-tuple-incomplete` and fails the binding. This is a frozen scorer/schema mismatch, not evidence that combo envelopes failed to reach their declared tuples.

Independent evidence supports that distinction: `R41W2C2IndepEval.md` reports a third evaluator written from the frozen precedence text, 56/56 agreement with both recorded evaluator/interpreter pairs (52 held-out plus four round-40 receipts), and observed=declared on all 52, including all 12 combos. Its comparator reads the official score receipt for the frozen tools’ pairs, so this is corroboration, not a substitute official score. The claim remains **NOT MET** under the frozen counter receipt; do not convert a diagnostic correction into a retroactive pass.

### Routed items and landing consequences

- **R40-CL3:** the round-41 C2 counter specifies whole-subtree/tool/writer and SKILL-block drift checks, including mutate-then-restore protection. This is addressed in the counter’s design, independently of the failed C2 feature binding.
- **R40-CL4:** the C2 generator documents the damaged block’s compressed-length pinning. No contrary finding emerged in the reviewed score/evaluator artifacts.
- **R40-CL5:** the v3 interpreter has no embedded table copy, and the v3 entry documents the revised prose. Wave-1 review reports the repairs; this routing review did not re-audit every prose clause.
- **R40-CL6:** the C1 entry and frozen fetch chain name image → member → nested file/carrier digest checks; the scored C1 and supplementary gate passed. The independent oracle seat did not re-run the fetch chain.
- **R40-CL7 and D2:** still operator-owned: the round-40 lesson asks for an operator ruling on AVM terms/history; no ruling was in the reviewed landing evidence. Derived-metadata-only handling remains the stated restriction, not a ruling.
- **D1:** the round-41 S126 durability item is reported fixed by the wave-1 ledger through an in-lane digest-matched copy and local-source gate. The round-41 entry’s new S127/S128 citations are URL-based identity sources, not S126.
- **D3:** the expected pairs are no longer taken from the generator’s class map: the score names the frozen independent evaluator as expected source, and the separate third-evaluator report corroborates the pairs. The counter’s declared-feature lookup failure remains distinct.
- **R36-CL5:** remains open/unbound per the wave-1 routed ledger. In particular, the claims do not name `claim_row` source-row ids and the counters report their predicate constants rather than reading the predicate sentence from the claims file; QUALITY 39’s per-call REA package digest requirement is also not bound by the reviewed predicate/score. No Round-41 claim should be described as closing this carryover.
- **S118/S121 anchors:** remain partial per the routed ledger: S118 still omits the recursive-link-loop source site (lines 58–65); S121’s row still lacks the URL/hash for the second `debian/rules` file. The Round-41 entries cite S118 but do not complete those registry anchors.
- **R39-CL6 recurrence:** the scored receipts include exit codes, but the cross-domain line and complete wave-status fill are closure duties; this review does not assert their completion from the score files.
- **Round-39 erratum:** `tools/round-39/heldout-gen.py` is frozen history; the routed item requires recording its still-open status in the Round-41 lesson. That lesson was not among the reviewed evidence here.

## Axes and proposed move

- **Coverage:** no observed harm on the measured proxy. The C1 score and independent oracle evidence support only the four named carriers and retain the explicit provenance limit.
- **Depth:** the evaluator/interpreter decision pairs agree, but the frozen C2 counter exits 1. The depth claim is not a successful landing under its own target.
- **Calibration:** measured proxy unchanged in `R41W2Harm.md`; reporting C2 as met would contradict the official receipt.

**One bounded move:** correct the C2 counter’s declared-feature lookup to read the manifest’s documented per-carrier `declared` tuple, compare all required fields for every carrier including combos, and retain red selftests for absent, malformed and wrong tuples. Any rescore must be a diagnostic in a sandbox against unchanged frozen inputs and be reported separately; the original frozen exit-1 result remains the claim verdict. Keep R40-CL2 disclosed and open.

Risks: touching a frozen counter cannot retroactively repair the frozen verdict; independent comparator results depend on the score receipt for frozen tool outputs; a passing tuple repair would not establish the precedence as the best triage or close the other routed/operator-owned items.

## Verification

Evidence commands/results actually used by this review:

- Read `plans/round-41-claims.md` first, including `## Changes from the draft`.
- Read-only Git revision checks: `git -C <lane> cat-file -t` on base/freeze/controls/data/landing/tip revisions → each `commit`; `git -C <lane> merge-base --is-ancestor <freeze> <e9a24d07>` and `<e9a24d07> <tip>` → both true.
- `git -C <lane> log --format='%h %s' <freeze>..<tip>` → listed controls, held-out, C1 receipt/data, docs, score, and wave-1 evidence commits; no commit in the interval changed the reviewed C1/C2 frozen tools or claims file.
- Read official score JSONs: C1 `4/4`, exit 0; C1 extra met, exit 0; C2 `52/52`, 13 decisions, binding false, exit 1.
- Read `R41W2C1Oracle.md` and `R41W2C2IndepEval.md`; latter reports 56/56 agreement and 52/52 observed=declared. No fresh extractor or counter run was performed by this seat.
- Read `R41ConnRouted.md`, `corpus/lessons/round-40.md` routed rows, `R40W2ConnRouted.md`, `round-39-verifier-spotcheck.md` §5, and current S118/S121 rows to classify carried items.

No build/tests/linters run; no tools installed; no VCS mutation. No scratch artifacts were needed. This report is the only file written by this seat.

Report: .ufo/waves/round-41/w2/R41W2Routed.md
