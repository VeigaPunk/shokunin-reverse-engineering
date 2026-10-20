# C1 census scope review

Axes: **calibration** (declared versus undeclared claims), **freshness** (line-range stability), and **depth** (what file edits actually reach the census).

## Findings

- **Medium — SCORECARD appends do not shift old ranges, but relevant appended claims are unscoped.** **Observation:** `SCOPE` is a fixed, 1-based inclusive line table: PROVINCE rows at `c1-census-v10.py:255-261`, SCORECARD rows ending at `:276` (line 2122); `scope_of()` only matches `s <= line <= e` (`:400-404`). The census constructs its file set from `SCOPE`, then reads/classifies every line of those files (`:633-657`); a non-historical hit with no matching row becomes `UNDECLARED` (`:601-602`). The current run read SCORECARD through line 2471. It reports `SCORECARD.md:2380-2382 [scope None]` as UNDECLARED; these lines mention REA 6.5.0/6.7.0 (`SCORECARD.md:2380-2382`). **Inference:** an EOF append in SCORECARD leaves existing absolute line numbers intact, but a new appended REA/version/path/pin locus past line 2122 can itself trigger UNDECLARED unless an exact scope row covers it. The current unscoped hit demonstrates this is not hypothetical.

- **Low — line-count-changing PROVINCE rewrites can stale both census coordinate tables.** **Observation:** PROVINCE `SCOPE` entries are also fixed line ranges (`c1-census-v10.py:255-261`); the separate `FRONTIER` register has fixed PROVINCE spans through lines 162 (`:292-307`). **Inference:** same-line replacements do not shift them. Inserting/deleting physical lines before later ranges does not move the table automatically: content may be classified under the wrong row or outside all rows, where a relevant locus can become UNDECLARED. This can also misalign `FRONTIER` rows.

- **LOG appends are outside this census.** **Observation:** no `LOG.md` row appears in `SCOPE` (`c1-census-v10.py:254-277`), and the input file set is derived only from those rows (`:633-643`). **Inference:** appending to LOG neither shifts the existing coordinates nor changes this tool's result.

## Safe edit plan

1. Rewrite the stale PROVINCE statements in place, preserving physical line count; keep edits within their current `CURRENT` rows. Do not widen existing `DATED` spans. If line-count changes are unavoidable, re-key every affected `SCOPE` endpoint/marker and `FRONTIER` range in the same change, retaining each row's intended content and boundaries.
2. Append SCORECARD and LOG records at EOF to avoid shifting existing coordinates. Before expecting a clean census, give each new census-relevant SCORECARD assertion its own narrow, truthful `CURRENT` or `DATED` scope row (with an in-row marker for a DATED row), rather than extending an older DATED span. LOG needs no row unless the instrument is deliberately changed to read it.
3. The observed current FAIL also has an unscoped SKILL hit at `SKILL.md:512` (block `512-519`), in addition to SCORECARD `2380-2382`; account for both existing undeclared blocks with narrow, truth-preserving coverage if the goal is PASS. Do not conceal fresh claims with historical wording.

## Evidence and verification

**Observed current-tree run:** live pins were 6.7.0 for Devin/OMP/Kimi; the census reported `VERDICT: FAIL (stale=4 ambiguous=0 undeclared=2 unresolved=0)`, with stale PROVINCE loci at lines 9, 16, 17, and 44 and undeclared blocks at SCORECARD 2380-2382 and SKILL 512-519. Scope marker and frontier-register errors were empty. No candidate edit was made or checked.

Commands run (cwd: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`):

- `git diff --no-ext-diff 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 -- .ufo/gates/c1-census-v10.py` — exit 0; no output (target has no diff from the declared baseline).
- `python3 -I -B .ufo/gates/c1-census-v10.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --quiet` — exit 1.
- `python3 -I -B .ufo/gates/c1-census-v10.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` — exit 1; detailed block locations above.

**Verification gap:** no `lsp` device is mounted (the `xd://lsp` docs request returned “No such tool”); therefore LSP status/references/definition/diagnostics were unavailable. No grep was used as semantic evidence. The census runs describe only the present tree, not a hypothetical round-19 edit.

Report: `.ufo/waves/round-19/w1/ReviewC1CensusScope.md`
