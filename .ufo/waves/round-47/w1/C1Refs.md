# C1Refs — R47-C1 clause 8: verified, satisfied by a candidate, and attacked

Seat `C1Refs`, round 47 wave 1, lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze = measured revision `5017e1f7299c3a812e87e7950148f54313dd279e` (re-derived with
`git log --format=%H -1 -- plans/round-47-claims.md tools/round-47/`). Read-only on the lane tree;
all candidates and attacks ran in fixture repos under `/fast/scratch/hyaku/kaidoku-r47/C1Refs`
(removed at yield). Receipts: `.ufo/waves/round-47/w1/C1Refs/` — `receipt.json`,
`count-freeze.out`, `runs.json` (18 probes), `landing.json` (end-to-end CLI + recipe A),
`selftest.out`, `rows.md`, `report.md`, and the three harnesses.

Clause 8 reads (`plans/round-47-claims.md:83-84`): "`refs >= 3`, every reference carries a line
selector and resolves at `--rev`, the path set is validated, and `corpus/lessons/round-46.md` is
cited; both sha256 pins match." It is computed by `check_refs` (`tools/round-47/exact.py:152-176`)
over `HARD_REF = ((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?` with
`ALLOW = corpus/lessons/, corpus/knowledge/, plans/, tools/round-47/` and `MUST_CITE =
corpus/lessons/round-46.md`.

## Verdict at the freeze (do-nothing)

Exit **1**, `failing ["marker_occurrences 0 != 1", "marker_block_count 0 != 1"]`,
`block_present 0`, `rule_blocks 23`, `marker_occurrences 0`, `frozen_path_changed []`,
`battery {"skipped": "artefact fails a structural clause first"}`; stdout sha256
`88fafc60…f28ba`, UTC `2026-10-28T17:54:40Z`. Clause 8 is therefore **not evaluated** at the
freeze — it is reachable only once a marked block exists, which is why the claim's target is a
landing measurement.

## Candidate: clause 8 satisfied, and the list empties to `[]`

`rows.md` holds the paste-ready block: four rows, trigger cells naming exactly one of
R46-CL2/CL3/CL4/CL6 each, arm cells exactly `symbol` / `once` / `digest` / `order`, exit cells all
`1`, `mutations_sha256:19a2166e…a112`, `interpreter_sha256:dcef54f1…412c`, seven citations that
resolve at the freeze (`corpus/lessons/round-46.md:57-66,21,60-62,63-64,65-70`,
`plans/round-47-claims.md:70-89,83-84`). Run end-to-end through the frozen CLI on a two-commit
fixture (freeze bytes → landing commit): exit **0**, `failing []`, `rule_blocks 24`, battery
`forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`, every forgery
`v2_exit 0, v3_exit 1`; `--profile v2` also exit 0. A variant with one extra row keeps clause 8
green and reports only `rows 5 != 4` and the routed-cardinality clause — the list shrinks to the
*other* clauses, not to a silent pass.

## Findings table

| id | finding | measurement | severity for the landing |
|---|---|---|---|
| F1 | clause 8 accepts a content-free citation set: three repeats of one lesson line | `refs 6` over two distinct paths, `unresolved []`, exit 0, battery green (`runs.json` case `D`) | clause 8 states a floor, not a relevance binding; the L1's prose must supply the relevance |
| F2 | `refs >= 3` counts occurrences, and `SELF` needs no selector, so the claim's "at least three citations carry a line selector" is stronger than the code | case `P2`: `refs 5`, exactly **two** selected non-SELF citations, exit 0 | the floor can be met by citing the interpreter three times |
| F3 | a **directory** resolves as a citation at rev (`git show <rev>:plans/` is a tree listing) | case `E`: `plans/:1`, `tools/round-47/:1-2` → exit 0 at rev | "the path set is validated" is a string prefix, not a file test |
| F4 | clause 8 and clause 9 partition the citation universe; the battery's `_fixture_files` carries only six paths, so any `corpus/knowledge/` cite scores the artefact **1 inside the battery** | case `C` and `landing.json`: clause 8 exit 0 (`refs 11`, `unresolved []`) but full counter exit 1 `battery v2_green 0 != 4`, `battery genuine_green 0 != 1` | block 24 must cite lessons/plans only — a knowledge citation cannot land |
| F5 | F4 collides with `corpus/QUALITY.md` Row 77(a) (recipe A counts only `corpus/knowledge/` citations per craft block); the depth claim therefore lowers its own proxy | recipe A on the two landings: no knowledge cite → `citation_resolved_rules 23/24`, `depth_score 9.58`, `uncited_rules [24]`; with the knowledge cite → `24/24`, `10.0` but clause 9 red | the L1 must choose: land 23/24 and record the harm, or land 24/24 and report clause 9 unmet. M46-4 recurring by construction |
| F6 | `--selftest` is not runnable as written (argparse demands `--root/--freeze/--rev` first) | bare form exit **2** usage error; runnable form `EXACT_SELFTEST: cases=16 failures=0`, exit 0, sha `0249b80f…8aaa` | a report quoting the bare form records a could-not-evaluate (R46-CL8 class) |
| F7 | two of clause 8's bindings have no selftest red case: `refs < 3` and the missing must-cite | selftest case list has `red-ref-no-selector`, `red-ref-outside-allowlist`, `red-pin-mismatch` only; probes `R` (`refs 2 < 3`) and `J2` (`does not cite corpus/lessons/round-46.md`) are both red | the instrument's own discrimination under-covers its clause 8 |

Negative (the clause holds): `corpus/lessons/../../SCORECARD.md:1` does not resolve — git refuses
`..`, so it lands as `absent at rev`; the guard is git's, not the counter's. Out-of-set paths
(`tools/round-46/gate.py:99`) and out-of-range selectors (`:0-66`, `:57-103` on a 102-line file),
a zeroed pin, and a dropped selector each fail clause 8 **alone**, with every other clause green.

## Lane state after the freeze (context)

While I measured, the lane amended the claim six times: `9018c53b` (A1), `62e33f7d` (A2),
`2e4ae434` (A3), `1e2c3102` (A4), `07d2894e` (A5), `f54b3b6d` (A6) all touched `tools/round-47/`
and/or `plans/round-47-claims.md`. Measured consequences:

- `--freeze 5017e1f7… --rev a631bba0` exits **2** `frozen_path_changed`
  (`blob_changed ["plans/round-47-claims.md", "tools/round-47/"]`); `--freeze 62e33f7d` also exits
  2. The counter only evaluates from `--freeze 07d2894e` onwards.
- At `a631bba0` under `--freeze 07d2894e` the counter exits **1** with exactly
  `["battery v2_green 0 != 4", "battery genuine_green 0 != 1"]`, `refs 9`, the `corpus/knowledge/`
  citation cited — F4 on the real lane, not just in my fixture.
- A6 changed `tools/round-47/exact.py` (`_fixture_files` now adds every citation the marked block
  names) so the interpreter sha is `01a4bca7…` instead of the frozen `dcef54f1…`; block 24's pin
  follows it (match verified). Under A6 and `--freeze f54b3b6d --rev 31b092d1` the counter exits
  **0** with the battery `4 / 4 / 0 / 1 / 0`.
- So the freeze is a seven-commit series and the interpreter I verified clause 8 against is no
  longer the scoring bytes; the claim's freeze sentence is false for the current bytes (M46-3
  class).

## Notes for the L1

- The uncommitted working-tree block 24 also measures exit 0 with the battery green on the same
  harness — but it changed under me between two reads (arm cells went from
  `` `symbol` (the equality) `` to bare `` `symbol` ``), so a sibling is editing `SKILL.md` and
  `rows.md` is the stable reference.
- Block 24 must not write `tools/round-46/gate.py` anywhere: it is outside `ALLOW`. Describe "the
  gate's argv literal" instead (clause 7 is about the file, not about citing it).
- On the frozen bytes, do not add a `corpus/knowledge/` citation without deciding F5 — the two
  cannot both hold. A6 (`f54b3b6d`) later lifted this by widening the battery fixture, which is
  itself the evidence that F4 was the right defect to name.
- Nothing was installed (no tool, no package) and no lane file, frozen byte, or fleet file was
  written; `git` was used read-only except inside fixture repos whose `--show-toplevel` was
  asserted equal to the fixture before the first commit.
