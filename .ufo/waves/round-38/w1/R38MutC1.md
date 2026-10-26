# R38MutC1 — mutation test of the frozen c1-counter (round 38, wave 1)

Seat: mutation tester (leaf; no subagents). Judged on coverage, calibration.
Frozen instrument: `tools/round-38/c1-counter.py` at freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`
(== HEAD `cb4326b2aa4c2024af0651fe6115b82d0c4de3df` bytes), sha256
`a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8`. The frozen counter was
never modified; all mutants were exact single-occurrence string replacements in scratch copies
(`/fast/scratch/hyaku/kaidoku-r38/R38MutC1`, removed at end; manifest with old/new strings,
per-mutant sha256 and unified diffs archived).

Method: for each mutant, run the unchanged selftest
`python3 -I -B <mutant copy> --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
with `HYAKU_SCRATCH` pointed into my own scratch (isolates the counter's shared
`mint.wrapped.json` scratch file from sibling seats). Baseline (pristine frozen bytes +
committed selftest fixtures): 15 cases, green_ok=1, red_ok=14, failures=[], exit 0 — rerun
green after all mutants. Each mutant copy also carried the committed `selftest/` fixtures and
`tools/round-27/xpin-attribute.mjs` (verified clean in `git status`).

## Result table (27 mutants: 8 killed, 19 survive)

| mutant | class | selftest | killed? |
|---|---|---|---|
| M01 unanchored suffix (`fp.endswith(rel)`, drops `fp == rel` and `/` anchor) | oracle hit counting | green | SURVIVED |
| M02 hit condition → `if True` (hits ≡ len(oracle)) | oracle hit counting | green | **SURVIVED** |
| M03 `after_handler_ok` → `True` | handler check | green | **SURVIVED** |
| M04 handler exact membership → substring match | handler check | green | SURVIVED |
| M05 `after_gaps_empty` → `True` | gap check | green | **SURVIVED** |
| M06 `gaps(env) == []` → `len(gaps) <= 1` | gap check | green | **SURVIVED** |
| M07 evidence-id recomputed==stored dropped | evidence-id check | green | **SURVIVED** |
| M08 `startswith('ev_')` dropped | evidence-id check | green | SURVIVED |
| M09 `key in ev` guard dropped | evidence-id check | crash (`KeyError: 'K1/after'`, exit 1) | KILLED (crash, not a clean red) |
| M10 `province_core_section` → `True` | binding | green | SURVIVED (redundant with row binding) |
| M11 row regex word-boundaries dropped | binding province_core_row | green | SURVIVED |
| M12 row→entry citation (`ENTRY in r`) dropped | binding province_core_row | green | SURVIVED |
| M13 frontier-note `'big-endian'` conjunct dropped | binding frontier_note | green | SURVIVED |
| M14 `entry_present` → `True` | binding | green | SURVIVED (redundant with `sourced`) |
| M15 `opened == 2026-10-26` dropped | binding sourced | red (`source row opened earlier` flips) | KILLED |
| M16 `ENTRY in used` dropped | binding sourced | red (`used-by lacks entry` flips) | KILLED |
| M17 coverage-map table-row filter dropped | binding coverage_map_row | green | SURVIVED |
| M18 `carriers_unchanged` → `cur is not None` | carriers_unchanged | red (`carriers changed` flips) | KILLED |
| M19 byte equality → parsed-JSON equality | carriers_unchanged | green | SURVIVED |
| M20 `== TARGET` → `>= TARGET` | target comparison | green | SURVIVED |
| M21 `bind_ok` drops `'sourced'` | bind_ok tuple | red (3 cases flip) | KILLED |
| M22 `after_subject_ok` → `True` | subject-digest binding | green | **SURVIVED** |
| M23 `after_operation_ok` → `True` | operation/provider binding | green | **SURVIVED** |
| M24 `oracle_frozen` equality dropped | oracle_frozen | red (`oracle changed` flips) | KILLED |
| M25 `oracle_files > 0` guard dropped | guard | green | SURVIVED |
| M26 `TARGET = 4` → `3` | target comparison | red (green + 4 red cases flip) | KILLED |
| M27 `HANDLER` constant → `squashfs_v4_le` | handler check | red (`wrong chunk handler` flips) | KILLED |

Full machine-readable log: `.ufo/waves/round-38/w1/artifacts/R38MutC1/selftest-results.tsv`
(exit code + selftest JSON per mutant); exact mutations: `mutants-manifest.json`.

## Findings

1. **No selftest case is decided by the envelope-content checks (headline).** M02, M03, M05,
   M06, M22, M23 all survive: the oracle-hit comparison (`after_oracle_hits == oracle_files`),
   handler check, gap check, subject-digest check and operation/provider check are each
   individually removable while the selftest stays 15/15 green. Every red case is instead
   decided by structural absence (missing receipt / oracle or carrier change), the
   PROVINCE/SOURCES/README text checks, or the evidence-id recomputation mismatch (the
   wrong-handler and gap fixtures are caught because their tampered envelope no longer
   recomputes to the stored id — not by the semantic checks named in the case titles).
   Consequence: a future counter edit that silently drops any of these checks still passes
   its own selftest — the selftest overstates what the counter enforces.
2. **Probe A — R36-CL3 reproduces on the round-38 instrument.** A receipt whose
   `normalized_result.files` were copied from the frozen oracle TSV (correct sha256s, BE
   handler, no gaps) and re-minted with `xpin-attribute.mjs` — no REA run anywhere — makes
   the **frozen** counter exit 0 with `carriers_matched == 4`, `met_target = true`
   (probe-results.json, probe A). The counter cannot distinguish a fabricated-but-consistent
   receipt from a real run; this is the disclosed R36-CL3 blind spot, now falsified against
   P38-C1's instrument.
3. **Probes C/D — surviving mutants correspond to concrete acceptance.** A re-minted
   LE-handler receipt: frozen counter red, M03-counter (handler check removed, selftest
   green) **met_target=true**. A receipt publishing `unrelated.bin` (zero oracle files):
   frozen counter red, M02-counter **met_target=true**. So the selftest cannot protect the
   predicate's "publishes every regular file of the frozen independent oracle" and "names the
   squashfs_v4_be handler" sentences against counter regressions.
4. **Counter itself holds on those dimensions** (probe B): a re-minted receipt with LE
   handler + extraction gap + a missing oracle file is rejected by the frozen counter
   (`met_target=false`) — the surviving mutants are selftest coverage gaps, not live holes
   for those fields. The live hole is probe A (fabrication), which no per-field check can
   close without run attestation.
5. **Killed set (what the selftest does protect):** `sourced` opened/used-by conjuncts
   (M15/M16), `carriers_unchanged` byte equality (M18), `oracle_frozen` equality (M24),
   `bind_ok` consuming `sourced` (M21), the TARGET constant (M26), the HANDLER constant via
   the province row (M27), and evidence-id presence (M09 — but by unhandled `KeyError`, i.e.
   the selftest would crash rather than report a clean red if that guard regressed).
6. **Redundant bindings:** `province_core_section` (M10) and `entry_present` (M14) are not
   independently load-bearing — their failure modes are covered by `province_core_row` and
   `sourced` respectively. Harmless, but the selftest cannot kill them.
7. **Untested boundary details (minor survivors):** word-boundary regex in the province row
   (M11), row→entry citation (M12), frontier-note `big-endian` conjunct (M13), coverage-map
   table-row restriction (M17), carriers byte-vs-parsed equality (M19), `>=` vs `==` target
   (M20), empty-oracle guard (M25), evidence-id `ev_` prefix and recomputation equality
   (M07/M08 — no case mints a tampered or non-`ev_` id).

## Lane-state observations (not mine to repair)

- The working tree carries an **uncommitted rewrite of the frozen counter** (` M
  tools/round-38/c1-counter.py`) that re-introduces a sasquatch-v4be before-arm premise the
  freeze explicitly corrected ("the round-37 missing-extractor-dependency before-arm does not
  reproduce … corrected premise" — plans/round-38-claims.md). 93-line diff archived:
  `artifacts/R38MutC1/uncommitted-counter-diff-vs-HEAD.diff`.
- That working-tree file changed **again during this run** (sha256 `f27f982b…` →
  `733be016…`); a sibling is actively editing it. Second snapshot:
  `uncommitted-counter-diff-snapshot2.diff` (111 lines). Committed bytes at HEAD/freeze
  remained `a7a62b09…` throughout — my mutation base and all probes used those bytes.
- I wrote only: this report, `artifacts/R38MutC1/*`, and scratch (removed). No VCS mutation;
  no writes to corpus/, PROVINCE.md, SCORECARD.md, SHONEN.md, or the fleet repo.

## Restoration evidence

- Frozen counter sha256 before == after: `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8`
  (working tree + `git show HEAD:` both re-verified at end of run).
- All 27 mutants lived only under scratch
  `/fast/scratch/hyaku/kaidoku-r38/R38MutC1` — removed (`test ! -e` passed). Every mutant is
  reproducible from `mutants-manifest.json` (exact old/new strings, per-mutant sha256, diffs).
- Baseline selftest green before and after the mutant series (control against drift).

Tooling: nothing installed or upgraded (node v24.21.0, rea-agents 6.5.0 package root and
preinstalled sasquatch-v4be were sufficient; no pacman transactions).
