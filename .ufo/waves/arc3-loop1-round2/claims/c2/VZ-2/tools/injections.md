# VZ-2 (C2 convergence) — injection fixtures, exact recipes

Before-state instrument: `.ufo/gates/c1-census-v10.py` at HEAD `14b1682`,
blob `8fee9422…`, sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`
(copy preserved at `../before/c1-census-v10.py`). Root tree: `../before/` outputs,
`/var/tmp/vz2/roots/<t>/` construction, re-runnable via `tools/battery.sh <instrument.py> <tag>`.

All roots are byte copies of the three scoped files at HEAD (`worktree == HEAD blob`
verified: PROVINCE `d075a3c6…`, SKILL `483b0eba…`, SCORECARD `a7c72950…`).
Custody paths are only READ (anchor re-derivation); nothing under `~` was written.

Provenance of the output directories: `before/` = instrument `6f1d19ff…`;
`after/` = `82fb807e…` for t0–t10 and `df9ffdf9…` for t11/t12 (each `.out`
carries its instrument path in the header line); `final/` = **canonical, all
12 roots + records sim + scope-diff at the final landed revision `d0772ce8…`**.
Use `final/` for any re-check; it also holds the landed instrument copy.

| t | injection (recipe) | before-state | target |
|---|---|---|---|
| t0 | pristine copies | PASS 0/0/0/0 | control |
| t1 | SKILL.md omitted from root (H1 = RV-11 A5) | **PASS exit 0** `lines=0 loci=0` | FAIL declared |
| t2 | SKILL.md present but 0 bytes | **PASS exit 0** | (variant of H1) |
| t3 | PROVINCE.md omitted | FAIL exit 1 (scope-errors) | stays FAIL |
| t4 | all three files gate-token-free/empty | FAIL exit 1 (scope-errors) | stays FAIL |
| t5 | instrument with `PIN`/`VER`/`PTR` set never-matching (`tools/blind.py`) | **PASS exit 0** `loci=0` G2 ok (H3 = CR-5) | FAIL declared |
| t6 | PROVINCE.md:17 `rea-agents@6.5.0`→`9.9.9` + ` (historical)` same physical line (H2 = VZ-3 A3/A3b) | PASS (`historical (inline marker)`) | named residual, outside the two patch texts |
| t7 | PROVINCE.md EOF += `The build shipped 6.7.0 last week.` (H5 = RV-11 A2) | PASS (no gate token → not a locus) | named residual, unit boundary |
| t8 | SCORECARD.md:651 inserted `planted rea-agents@6.3.0 …` inside DATED 636-702 (CR-5 t5) | PASS (`historical (dated scope)`) | documented refusal class (fail-open to widen) |

Exact fixture edits:

- t5 blind: `python3 tools/blind.py <instrument> <copy>` — replaces the three
  `^(PIN|VER|PTR) = re\.compile\(.*\)$` assignment lines with `(?!x)x`.
- t6: line 17 (1-based) of PROVINCE.md, index 16.
- t7: append one line, no `rea|kimi|omp|npx|config.toml|mcp.json|mcp_servers|devin` token.
- t8: insert at 1-based line 651 (inside declared DATED range 636-702).
