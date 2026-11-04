# Round 72 — checker children and a survivor bound to a failing case

- Author: L1 KaidokuR72; drafting seat: ScribeLesson.
- Round: 72, wave r72-w1.
- Base: `56241b1c8baff95862730c008f1ae5132b03388e`.
- Declaration: `6316c1053f927a1a1cdc3e0960b70acab5f56381`.
- Operative freeze: `34fe7aa70b627d92e2d27dbce308d9f5bebda63d` (assignment's freeze pointer; this drafting seat did not rerun the freeze gate).
- Claims container: `.ufo/waves/round-72/claims.json` is present and was read; its `frozen_atoms.A0` records the four pre-freeze fixes `17d8b5f785a449aed76f42e697071007ae9e226f`, `306cbb3fb11661fba6f364f73ad0b1eeb24a959f`, `25ecc71116bad0673416ebfc128be5a16e03b7e2`, and `1563ea353ab32acc2141c82b89299580cb73f4c8`.
- Report: `.ufo/waves/round-72/w1/ScribeLesson.md`.
- Draft: `.ufo/waves/round-72/w1/ScribeLesson/round-72.md`; intended landing: `corpus/lessons/round-72.md` (L1-owned).

Axes: coverage (which process boundary is observed), calibration (a known mutant has a named kill), operability (retained receipts distinguish observation from summaries). These are the frozen R72-C1/C2/C3 axes, not new predicates.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M72-1 | observation-scope / checker-child gap | `tools/round-71/packed-elf.py:52–57` says “every child of the route” and that the route records each child's observed environment. The round-71 lesson's Outcome records 46 route children (upx 21, node 16, readelf 8, git 1), but explicitly admits checker-mode git/readelf inherit the caller environment. The checker uses bare `subprocess.run` at lines 514–516 and `run(["readelf", ...])` without env/capture at line 702. Corroboration: `.ufo/waves/round-72/l1/pre/c1-at-base.json`, arm `A11_checker_env`, has `checker_child_env {}`, both shim canaries present, `keys_exact false`, and `ok false`, even though checker `rc 0`. Every route child being recorded was not evidence that checker-mode children were recorded. | none for checker-mode coverage in round 71: its route-only A8 observation did not exercise this boundary. The qualified docstring must not be silently generalized to all modes. | R72-C1's falsifiable `A11_checker_env` (`tools/round-72/seam-probe.py`) requires both git/readelf shim environments to have exactly HOME/LANG/PATH/TMPDIR, no canary, descendant HOME/TMPDIR, and the checker's own log to contain at least two records with git and readelf in its census. `tools/round-72/packed-elf.py:615–624,850` builds the checker env and emits `checker_child_env`. The retained before receipt fails A11 (9/11 overall); the L1 must bind the after result to the measured revision, not this implementation description. |
| M72-2 | survivor-without-regression-binding | `.ufo/waves/round-71/w1/MutReaders/mutants.md:27,39,57` reports survivor **i**, `probe:471`, `binding_ok=True`: built-in selftest exit 0 and added detector not-killed. The report explicitly says the complete A10 arm stayed false because the genuine checker rejected the broken binding; survival is not evidence of A10 false acceptance. The round-72 before receipt `.ufo/waves/round-72/l1/pre/c2-at-base.json` preserves `A10_binding_force_true` surviving, seven pristine cases, `expect_case null`, and no failed cases. | none binding survivor i to a committed failing selftest case in round 71; recording a survivor in a report was not a regression gate. | R72-C2 binds `A10_binding_force_true` to `a10-binding-from-checker`: `tools/round-72/mutation-check.py:88–98` declares the before/after patch sets, and `tools/round-72/seam-probe.py:761–767` tests true, false, missing clauses, and missing binding. `.ufo/waves/round-72/l1/pre/c2-mutant-test.json` records the mutant killed with exactly that failed case, pristine ten cases green, wrong-case kills empty, and target pin matched at `306cbb3fb11661fba6f364f73ad0b1eeb24a959f`. This is a retained pre-freeze result, not a landing verification by this seat. |

## Gate

SOURCES candidate: S275, the Linux proc(5) `/proc/pid/environ` paragraph identified by the claims container's `frontier.sources`. This draft does not admit a source from the container alone. URL, access date, located quote (at most 25 words), snapshot digest, and admission decision must come from ScoutSource's retained live-fetch evidence.

| SOURCES row | URL | access date | located quote (≤25 words) | snapshot sha256 / evidence / decision |
|---|---|---|---|---|
| S275 | [L1 — filled by the non-author closure.] | [L1 — filled by the non-author closure.] | [L1 — filled by the non-author closure.] | [L1 — filled by the non-author closure.] |

ScoutSource had not published its final output when consulted by this drafting seat. The source gate remains unclaimed here.

## What the wave found

- [L1 — filled from executor receipts: measured revisions, commands, exit codes, and each frozen claim's observations.]
- [L1 — filled from reviewer, critic, and mutation-tester findings: named attacks, survivors, fixes, and limits without upgrading fixture evidence to full execution.]
- [L1 — filled from sentinel, scout, connector, and scribe reports: scope/security findings, source disposition, sibling scan, and knowledge/lesson disposition.]
- [L1 — filled from closure: controls, non-author judgment, settlement, and any unresolved findings.]
