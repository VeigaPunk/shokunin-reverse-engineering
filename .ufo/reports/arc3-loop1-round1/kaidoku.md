# arc3-loop1-round1 — kaidoku round report

Date: 2026-10-19. Wave: 64 seats on `opencode-go/deepseek-v4.1-flash` (opencode-go
key 1 of 7; roster frozen pre-dispatch, items array asserted = 64). Harness
interrupted the wave's tail: 54/64 seat reports delivered; the deficit is
recorded per the counting lesson, not backfilled. Seat reports
`.ufo/waves/arc3-loop1-round1/seats/`; claim artifacts
`.ufo/waves/arc3-loop1-round1/claims/`; frozen claims
`.ufo/waves/arc3-loop1-round1/claims-frozen.md`.

## Work performed

- C1 (coverage, owned): EVM real-bytecode leg — the r3-07 frontier. Isolated
  npm solc install (receipt `claims/c1/EX-02/install-receipt.txt`), four
  ERC-20-shaped on-host compiles, probe runs on both pins in raw+hex forms,
  3-way selector reconciliation (`claims/c1/EX-07/reconciliation-run.txt` — ALL
  SOURCES AGREE), creation-code controls, rerun id-stability, custody pre/post
  pairs, independent keccak/disassembler recon (`claims/c1/RV-1/`,
  `claims/c1/EX-07/`), quality grade (`claims/c1/RV-3/`).
- C2 (operability, fleet): citation-drift frozen-run guard — implementation +
  13-case selftest (`claims/c2/EX-16/`), tampered/absent/unpinned injections
  (`EX-17`/`EX-18`/`EX-24`), frozen-run byte-stability (`EX-19`), mutation test
  (`RV-5`), consumer sweep (`RV-8`), merged registry row (planner's v3,
  `claims/c2/PL-2/frozen-run-guard.patch.md`).
- C3 (freshness, fleet): census E22 disposition — v9 byte-exact recovery +
  historical-tree reproduction (`RV-11`, `CR-5`), scope audit (`EX-29`,
  `RV-10`), instrument header disposition + marker re-key + G18 (`EX-28`),
  interplay check with the probe (`EX-31`, `CR-4`).
- Cross: custody seat (`CU-1`) + four corroborations; consistency sweep
  (`CN-1` — projections proving the C1/C2/C3 edit surfaces leave both
  instruments green); records reconciliation (`CN-2`); wave integrator
  first-hand re-verification of both landed real-target edits (`VZ-4`).

## Landed changes

- `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` — new entry (LOG entry
  above; work commit).
- `corpus/README.md:38` — map token + state-cell refresh, one physical line
  (190 → 190).
- `SKILL.md:371` — citation-drift registry row, guard semantics + 13-case
  self-invocation cell (one merged row replacing two rival patch texts).
- `.ufo/gates/citation-drift/{citation-drift-probe.py,expected.json}` — frozen-run
  guard + pinned table digest (probe `e2665074…`, expected `ff47bfd6…`).
- `.ufo/gates/c1-census-v10.py` — E22 disposition header, marker-line re-key,
  G18 assertion (`6f1d19ff…`).
- Wave tree `.ufo/waves/arc3-loop1-round1/` committed (solc node_modules and
  `__pycache__` excluded via the wave `.gitignore`; the install receipt pins
  the compiler bytes).

## Before → after measurements

- C1: command A (recipe in SCORECARD.md) — before 81/81, missing [], dangling
  [], 13/13 at `e845c2b`; after 82/82, missing [], dangling [], 13/13 rules at
  the work commit; prior-81 byte-identical (one file added, one README line
  reworded). Selector recovery K/K with zero extras on 5/5, 6/6, 9/9, 11/11
  legs; creation legs 0 functions (`bytecode.kind:"unknown"`).
- C2: probe selftest 11 → 13 cases, exit 0 both sides; tampered/absent/unpinned
  baselines: silent `findings=0 exit=0` before → declared preflight exit-2
  classes after (parent re-run: `pointer_table_tampered`,
  `pointer_table_unreadable`, `pointer_table_unpinned`); probe findings = 0 at
  HEAD, both modes, after.
- C3: census verdict at HEAD PASS 0/0/0/0 both sides (honest PASS→PASS
  disposition — the FAIL class reproduces only on historical trees: v9 at the
  766-line tree FAIL undeclared=2, measured from byte-exact recovery); one
  latent marker defect (committed row's marker outside its own range) re-keyed;
  G18 fired on its own intermediate state (parent-verified non-vacuity); creep
  audit 0 flags.
- Custody: 5-path sha256 pre-pair (09:57:18Z) = post-pair (integration
  capture), zero drift.

## SHONEN

- [~] SKILL.md real decision tables — 13/13 queue-drain rules with resolvable
  citations at the work commit (command A); verifier: none non-author.
- [~] End-to-end domain task executed and logged — the real-solc probe chain
  (install → compile → probe → reconcile) end-to-end, LOG entry above;
  verifier: none non-author.
- [~] Executable without oral context — the entry's recheck line runs verbatim
  given a disk-backed TMPDIR (measured); verifier: none non-author.
- [~] No cross-domain bleed — RESULT-class entry, no Core promotion, safety
  verdicts untouched (PROVINCE Adjacent intact); verifier: none non-author.

## Notes for the next round

- opencode-go key rotation advances to key 2 (round 2).
- Named debt queue: census latent holes (four patch texts in
  `claims/c3/`); EX-03's seat gap; creation-code scope; the pre-existing dirty
  `arc2-loop1-round10/C3.md`; host `/tmp` quota (recipes must carry
  disk-backed scratch).
