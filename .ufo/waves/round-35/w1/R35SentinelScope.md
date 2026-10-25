# R35 Sentinel — scope/source execution boundary audit (wave 1)

Seat: R35SentinelScope. Surface: round-35 frozen claims C1 (coverage, .jsc→source mapping via S125/S129) and C2 (calibration, D-1..D-4 closure); counters `tools/round-35/c1-coverage-counter.py`, `c2-calibration-counter.py`. Method: read-only git-object inspection and independent counter runs (no `--json-out`, no worktree/source mutation).

## 1. Baseline verification (evidence)

- Base `aa04633a…`, instrument/freeze commits below. HEAD = `3ecf4298` ("round-35: commit failing do-nothing controls before claim data (C1/C2 exit 1)").
- Instrument pins in `claims-canonical.json` match **HEAD** and **2323d197**: C1 `e28792c7…`, C2 `576c14dd…`, plan `45b644a4…` (sha256 over `git show` blobs). At the declared `instrument_revision` `d2729cba89` the same blobs hash `cd4ab7e7…` / `39fe39c5…` — **not** the pinned bytes, and `claims-canonical.json` does not exist at that revision.
- `frozen_inputs.census-start.txt` hash `b6ce2b17…` matches at freeze rev, 2323d197 and HEAD.
- Predicates byte-equal between counter constants and claims JSON: `c1_const == c1_claims` True, `c2_const == c2_claims` True. Plan file does **not** contain the full predicate sentences (plan uses its own phrasing) — the claim-discipline "byte-identical in this plan" clause does not hold verbatim, though counters never compare against the plan.
- Controls committed at HEAD were reproduced independently (identical outputs, see §4).

## 2. Findings

### F1 — `instrument_revision` is unusable as `--freeze` (MEDIUM, operational trap)
- Exploit/use path: a scorer following the canonical file uses `--freeze d2729cba89` (the declared `instrument_revision`).
- Evidence: `python3 -I -B tools/round-35/c1-coverage-counter.py --root <LANE> --rev HEAD --freeze d2729cba895b8664f3ccb27196091494f3cda83b` → `C1: claims file absent at freeze revision`, exit 2; same for C2. The revision also predates the final counter bytes (F1 pins mismatch).
- Impact: documented freeze revision yields unevaluable (exit 2) rather than a score; a run that silently substituted a later revision would still be correct but undocumented.
- Smallest remediation: in `claims-canonical.json`, rename/annotate the field (e.g., add `"freeze_revision": "2323d197…"`, keep `instrument_revision` as historical snapshot tag); state in freeze-status/note that scoring freeze = 2323d197 (first commit adding `claims-canonical.json`; unchanged through HEAD).

### F2 — Plan cites `merge/kaidoku/PROVINCE.md`, which does not exist (LOW, provenance wording)
- Evidence: `git ls-tree -r --name-only HEAD | grep merge/` → empty; no `merge/` path in the lane. The frontier bullet exists in **root** `PROVINCE.md` (line 147–148, "`.jsc` → source mapping", r4 frontier) at base and HEAD.
- Impact: none on scoring (C1 counter reads root `PROVINCE.md`), but the plan's theme-path description is not reproducible in-repo.
- Smallest remediation: plan text should cite root `PROVINCE.md` r4 frontier bullet.

### F3 — D-4 scan boundary is textual, catches an unrelated table (MEDIUM for build)
- Evidence: `c2` at base and HEAD fails `D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4` and `D4_section_missing:### Round-34 run-6 instrument registry`. Line 1081 is the *Residual witness registry* 4-cell table below the Round-32 registry; the counter scans from `### Round-32 instrument registry` until the next `##`/`###` heading, so that unrelated table is inside the checked span.
- Impact: fixing the two registry sections alone does not green D-4; the residual-witness table must move under its own heading (or be reformatted to 8 cells / non-table).
- Smallest remediation: relocate `### Residual witness registry` to its own heading, or change scan to stop at the next `###`-level heading that begins a new table (would require instrument change => not allowed post-freeze; therefore build must satisfy the frozen byte semantics).

### F4 — Predicate binding is substring containment, not equality (LOW, latent)
- Evidence: `if PREDICATE not in json.dumps(claims_obj)` in both counters. Currently exact byte-equal (verified), so no live failure; a future claims edit that embeds the predicate anywhere (comment/other field) while altering the canonical `predicate` values would still pass.
- Impact: weakens "refuses on mismatch" claim; no mutation/score risk under current frozen snapshot.

### F5 — `--json-out` write scope is caller-unbounded (LOW)
- Evidence: `open(args.json_out, "w")` with no containment check in either counter; default invocation writes nothing. No lane write is performed by the counters otherwise (only `git show`/`ls-tree`/`log`, stdout, stderr).

### F6 — D-1 ordering uses committer timestamps (LOW, integrity note)
- Evidence: `git log --format=%cI` comparisons (census commit time vs first SOURCES.md change). Committer dates are author-controllable (env/grafts/rewrites); the counter only guarantees the check reads immutable objects, not that the recorded times are honest. Fail-closed behavior verified (missing census → `D1_census_start_missing`).

## 3. Zero-mutation / `resume_continuity_v1`

- No resume surface exists in this artifact set: `w1-dispatch.json` `counts.resume=0`; both counters are stateless one-shot CLI reads; round-35 wave-1 seats are fresh spawns.
- Canonical contract (`run-logic.md` §2.1, referenced in-lane transcripts) requires explicit stable native-session selection before any resume mutation, and zero mutation on failed preflight. With no resume path to reject, the zero-mutation property is vacuously satisfied; same N/A conclusion as round-17 w2 / round-19 w2 sentinel reports.

## 4. Executed evidence (read-only)

- `C1 @ base` (`--rev aa04633a… --freeze 2323d197…`) → `C1_FAIL: entry_missing:…mapper-contract.md; entry_missing:…release-inventory.md; registry_row_missing:S125; registry_row_missing:S129; province_missing:…mapper-contract; province_missing:…release-inventory; readme_missing:…mapper-contract.md; readme_missing:…release-inventory.md`, exit 1. Matches committed `controls/c1-do-nothing.json` exactly.
- `C2 @ base` → `C2_FAIL: D1_census_start_missing; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry`, exit 1. Matches `controls/c2-do-nothing.json` exactly.
- `C1 @ HEAD` → same 8 failures, exit 1 (entries/rows/PROVINCE/README not yet landed).
- `C2 @ HEAD` → `D1_no_sources_change_after_base` (SOURCES.md untouched since base) + D2/D3/D4 failures, exit 1.
- `C1/C2 @ HEAD --freeze d2729cba89` → exit 2 (claims absent at freeze revision) — F1.
- Source-execution boundary (C1): counter body uses only `subprocess.run(["git","-C",root,…])` with `show`/`ls-tree`/`log`; no `shell=True`, no network, no REA, no worktree reads. Prep captures `.ufo/waves/round-35/prep/jsc-sources/` (`jsc2js-readme.md`, `releases-page1.json`, `releases-page7.json`) are committed; S125/S129 URLs correspond to the captured xqy2006/jsc2js README/Releases.
- `considerthese/` absent in lane (plan line "considerthese/ does not exist" holds).

## 5. Limits

- No network fetch, no REA/other runtime invoked; counters run without `--json-out`; no track, source, or VCS mutation. Git committer-date honesty (F6) is outside what the counters can prove.
