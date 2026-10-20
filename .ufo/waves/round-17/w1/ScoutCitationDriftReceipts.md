# Citation-drift probe — retained execution receipts (r17 W1 scout)

**Question.** Every retained execution of `.ufo/gates/citation-drift/citation-drift-probe.py`
under `.ufo`; exact argv, revision, exit; newest exercised **strict** invocation so the
`SKILL.md` row can be aligned to it.

**Method (read-only).** JSON-aware walk of every `.ufo/**/*.json` for objects whose `argv`
array contains `citation-drift-probe.py`, plus a raw-string census for
`CITATION_DRIFT_VERDICT` / `CITATION_DRIFT_REVISION`. Coverage: 2,468 `.ufo/**/*.json`
opened; 39 are unparseable (envelopes/truncated fixtures) and none of those 39 contains the
probe string, so the walk is exhaustive for parseable JSON. 470 `.ufo` files mention the
probe by name; only **4** retain an argv. Git-object byte checks and `git log` were
read-only. No carrier binary executed; no analysis tool run; no installs.

## 1. Observation — the four argv-bearing receipts

All four are wave-level `verification` records; all use `--strict`.

| # | File:lines | Label | Revision | Exit | Verdict / finding | Isolation |
|---|---|---|---|---|---|---|
| 1 | `.ufo/waves/round-14/verification.json:106-121` (revision key :2) | `citation-strict` | `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22` | **0** | `clean findings=0` | absolute script/root/table/expected, **no `-I`**, no `cwd` |
| 2 | `.ufo/waves/round-15/verification.json:127-142` (revision key :2) | `citation-strict` | `7ad23fe1735cd868ec203d93deb13bb2c42889ad` | **1** | `failed findings=1`; `citation_dead entry=sc-arc3r2-cites-shonen SCORECARD.md:1435 cites SHONEN.md:6-6` | absolute paths, **no `-I`**, no `cwd` |
| 3 | `.ufo/waves/round-15/final-recheck.json:17-32` (revision key :2) | `citation-final` | `ba3b2195d080d3083d339a67c35359855ad164a5` | **0** | `clean findings=0` | absolute paths, **no `-I`**, no `cwd` |
| 4 | `.ufo/waves/round-16/verification.json:317-334` (source revision :2, `executed_at_utc` :4) | `citation-strict` | `27b8fc13156230981312c44380cddab1f2bd318d` | **0** | `clean findings=0`, `executed_at_utc 2026-10-20T08:36:33Z` | **`python3 -I`**, absolute paths, `cwd` retained at :332 |

Exact argv, record 4 (the other three differ only by lacking `-I`; all argv elements are
identical otherwise):

```
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 27b8fc13156230981312c44380cddab1f2bd318d \
  --table /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json \
  --expected /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/expected.json \
  --strict
```

`cwd=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, exit 0.

## 2. Observation — newest exercised strict invocation

Record **#4 (r16)** is newest. Commit dates (observed): `3e99fbd` 2026-10-20 02:32:55 -0300;
`7ad23fe` 04:16:10; `ba3b2195` 04:17:51; `27b8fc13` 05:35:55. Its receipt carries the only
retained run timestamp (`2026-10-20T08:36:33Z`) and the only `-I` + `cwd` pair. This matches
`corpus/lessons/round-16.md:140` ("Existing own strict citation probe: clean, 0 findings,
exit 0, measured source revision above").

Byte identity (observed, read-only): probe `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`,
table `7994eec7e764e8c3195dd79efb850b63d437aa610e6a9d96ed24484bb53789d1`, expected
`05c251fb06d2c1537ee39231602bb7e8d73ea16a9caf7614f3104cc276aac52c` — identical as
worktree files, as Git blobs at `27b8fc13`, and as Git blobs at `HEAD b563c79`. `git diff
27b8fc13..HEAD -- .ufo/gates/citation-drift SKILL.md` is empty; r16's producer pins
(`verification.json:415-417`) still match. So the r16 argv remains reproducible now with
`--rev` set to the baseline `b563c799d97774aae4351276fe43cb897311e349`.

## 3. Alignment target for `SKILL.md:448`

Current row's first backticked command is the **relative, non-isolated** variant:
`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table ... --expected ...`
— no `-I`, no `--strict`, relative `--root .`. The r16 exercised argv is isolated, absolute
and strict. `corpus/lessons/round-16-verifier-spotcheck.md:184` flags exactly this row
("still advertises `python3 ... --root .` without `-I`, whereas r16's exercised strict argv
is isolated and absolute"), and `.ufo/waves/round-17/claims.json:12` (C1(b)) requires the
row be re-exercised with its isolated absolute argv and the receipt retained.

Recommended alignment: advertise the r16 shape with `--rev <REV>` (or the r17 re-exercise's
revision when retained), keeping `-I`, absolute script/root/table/expected, and `--strict`
in the runnable command. Do not silently keep the relative variant as if exercised; either
replace it or label it explicitly unexercised. Note `expected.json:4-6` records a distinct
`frozen_run.revision 679af5d7…` — running over another revision is a different measurement,
so no frozen-run claim follows from these four receipts.

## 4. Observation — output-only records without argv (bounded census)

These executed the probe (or a copied probe) but retain no command line, so they cannot
anchor a SKILL row:

- `.ufo/waves/arc3-loop1-round1/claims/c2/EX-23/harness/census-results.json` — 22 scenarios ×
  4 guard keys = **88** verdict strings. Exits: `guardA/probe` 0×15, 2×7; `guardA/strict`
  1×13, 0×2, 2×7; `guardB/probe` 2×20, 0×2; `guardB/strict` 2×20, 0×2. Runs a copied
  `head-citation-drift-probe.py` (`census.py:28`), not the gate path; no revision/argv in JSON.
- `.ufo/waves/arc3-loop1-round3/claims/c1/RV-4/measurements.json` — `probe_rehearsal` at
  `2dded2eb827b…`, `8c1f2ce867d1…`, `39e2b5484bd8…` (default + strict, all rc 0) and
  `probe_rehearsal_v2_current_table`; no argv.
- `.ufo/waves/arc3-loop1-round3/claims/c3/RV-12/evidence/landed-scenarios.json` (**106**
  verdict strings) and `base2-scenarios.json` (**65**) — per-scenario short 10-char revisions;
  no argv.
- `.ufo/waves/arc3-loop1-round3/claims/c3/PL-3/census-v2.json:1509` — invocation **template**
  only (relative, `--rev <REV>`, no `--strict`); not an execution.

## 5. Inference and remaining unknowns

- [INFERENCE] Ordering "newest" rests on r16's single top-level `executed_at_utc` plus commit
  dates; there is no per-command timestamp, so the probe's exact wall-clock position inside
  the r16 run is not retained.
- [OBSERVATION] No round-17 execution is retained: `.ufo/waves/round-17/w1/` held only
  `swarm-registry.json` plus sibling scout drafts; `round-17/pilot/*.json` are esbuild/shfmt
  tool receipts, not citation-drift runs. The r17 re-exercise required by C1(b) has not
  happened at this baseline.
- [OBSERVATION] r14/r15 receipts omit `cwd`; their relative-path behavior is unproven, though
  their argv are absolute.
- No tool installed or updated.
