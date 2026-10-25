# R35Audit32 — C2 census count parser review (wave-1, milestone: evidence + first falsifications)

Seat: R35Audit32 (scribe review; read-only lane, probes in private /tmp).
Scope: `tools/round-35/c2-calibration-counter.py` D-1 census-count parsing vs frozen claims
(`plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`).

## 1. Claims read (frozen)
- C2 predicate (P35-c2, byte-identical in plan/claims/counter): D-1 = census-start receipt
  `carries the base count (106 rows, exit 0, 9 W04 warnings)` and is committed before the
  first `corpus/SOURCES.md` change after base.
- `claims-canonical.json`: instruments pinned (c2 counter sha256 `576c14dd…`), base
  `aa04633a`, instrument revision `d2729cba`, supersession `a85ca674` (finalized freeze-read path).
- `.ufo/waves/round-35/assimilation/census-start.txt` at lane HEAD: `rows=106`,
  `EXIT=0`, exactly 9 `W04` lines (S033/S047/S054/S062/S069/S083/S090/S092/S102), plus
  `malformed=0`, `tiers A=100 B=5 C=1`, `status mined=102 rejected=4`, `duplicate_ids=0`.

## 2. Commands / outputs
- Read: `plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`,
  `tools/round-35/c2-calibration-counter.py` (lines 1–275), census-start receipt. Read-only.
- HEAD (lane): `3ecf42981a0b63414de90ade643040d609dbb8a5` — "round-35: commit failing
  do-nothing controls before claim data (C1/C2 exit 1)".
- Counter at HEAD:
  `python3 -I -B tools/round-35/c2-calibration-counter.py --root . --base aa04633a… --freeze 2323d197456f1328459d9420aff025cffbcb3e27 --rev HEAD`
  → exit 1: `D1_no_sources_change_after_base; D2_lesson_missing; D3_source_missing;
  D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106;
  D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4;
  D4_section_missing:### Round-34 run-6 instrument registry` (expected pre-data do-nothing).
  Note: D-1 content checks pass at HEAD — census exists, `rows=106`/`EXIT=0`/`W04` substrings
  present; D-1 fails only on ordering (`no_sources_change_after_base`).
- Freeze resolution: `claims-canonical.json` exists at `2323d197` (canonicalize commit), absent
  at `f1ea3a6d`/`a85ca674` (those hold `claims-frozen.json`); counter exits 2 if freeze lacks it.
- Counter selftest: not run on lane; fixtures inspected — green fixture census line is
  `rows=106 EXIT=0 W04 warnings` (single W04 token), red fixture only corrupts lesson seat counts.

## 3. Findings — falsification candidates (probes in private /tmp, repo mirrors green fixture)
| # | Finding | Probe | Result |
|---|---------|-------|--------|
| F1 | **W04 count not enforced.** P35-c2 requires exactly `9 W04 warnings`; parser checks only `"W04" in census` (token presence). Any 1..N W04 mentions pass; the tool's own green selftest fixture (one W04 token) codifies this. | A: census `rows=106 EXIT=0 W04 warnings` (1 W04) | exit 0 `C2_CLEAN` (false-accept) |
| F2 | **Substring accept of `rows=106`** — `"rows=106" in census` matches `rows=1060`/`rows=1067`; value is never parsed (no regex, no equality). | B: census `rows=1060 EXIT=0 W04 warnings` | exit 0 `C2_CLEAN` (false-accept) |
| F3 | Control symmetry: with no W04 token the check fails as intended (`D1_census_content_missing`), confirming enforcement is presence-only, never counting. | C: census `rows=106 EXIT=0` | exit 1 `D1_census_content_missing` |
| F4 | Same substring style for `EXIT=0` (matches `EXIT=00`, or any line containing it) — same family as F2, lower severity. | (inspection) | — |

Limits/notes:
- D-1 ordering is implemented as committer-date comparison (`parse_iso(ct) > parse_iso(fc)`) via
  `git log -1 %cI` vs oldest `base..rev` SOURCES change; equivalent to commit order only modulo
  clock skew/amend/rebase (not ancestry). No false-accept found in this harness.
- `"rows=106"` etc. also match anywhere in the receipt body (e.g. inside a warning line), not
  anchored to the manual-census block — same root cause as F2.
- Do-nothing at base and at HEAD fail as designed (D-1 content passes trivially because the
  committed receipt already carries the tokens; only ordering blocks it pre-data).

## 4. Advisory (for main agent / judging)
- C2 D-1 frozen check under-verifies the frozen predicate: the "9 W04 warnings" figure and the
  exact `rows=106` value are not enforced at score time. A junk receipt with 1 W04 line or
  `rows=1060` would score clean — the stated kill rule ("any frozen check failing") cannot fire
  on these.
- Fix direction (if approved by main; not applied — read-only seat): parse the manual-census
  block with anchored regex (`^rows=106$`-style equality, count `^kaidoku W04 ` lines == 9,
  `^EXIT=0$`), and extend the red selftest fixture with a single-W04 / wrong-rows census to
  guard the regression. Do not alter the frozen predicate string.
- No lane files were written/read by this seat; all probes in `/tmp` temp repos; no VCS mutation.
