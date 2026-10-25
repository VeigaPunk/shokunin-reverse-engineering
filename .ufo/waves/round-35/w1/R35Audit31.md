# R35Audit31 — C2 D-1 first-change time order (review)

Scope: advisory evidence only; read-only git queries plus one run of the frozen counter
(`tools/round-35/c2-calibration-counter.py`). No lane files written except this seat report.

## Axis of review
D-1: the round-35 census-start receipt is committed before the first `corpus/SOURCES.md`
change of the round, and carries the base count (106 rows, exit 0, 9 W04 warnings).

## Evidence (commands / output)

| Check | Command | Result |
|---|---|---|
| Census-start receipt added | `git log --diff-filter=A -- .ufo/waves/round-35/assimilation/census-start.txt` | only `d2729cba` (2026-10-25T16:05:46-03:00) |
| Census-start receipt changed since | `git log aa04633a..HEAD -- .ufo/waves/round-35/assimilation/census-start.txt` | only `d2729cba` — never modified after add |
| Receipt commit parent | `git rev-parse d2729cba^` | `aa04633a686d49756763b1feed4be6830d5bb479` = base → receipt lands in the FIRST post-base commit |
| SOURCES.md changes since base | `git log aa04633a..HEAD -- corpus/SOURCES.md` | empty; blob `dc7a3ccc…` identical at base and HEAD |
| Receipt content | `git show d2729cba:.ufo/waves/round-35/assimilation/census-start.txt` | `rows=106`, `EXIT=0`, exactly 9 W04 lines (S033/S047/S054/S062/S069/S083/S090/S092/S102) |
| Receipt hash vs frozen pin | `sha256sum` of receipt at d2729cba | `b6ce2b1773c60af4e3f5b14b7a63ba9743cae1eeec121b1ada50178a3d7af10a` = `frozen_inputs` pin in claims-canonical.json |
| Frozen counter at HEAD | `python3 -I -B tools/round-35/c2-calibration-counter.py --root <lane> --base aa04633a… --rev 3ecf4298… --freeze 2323d197` | `C2_FAIL: D1_no_sources_change_after_base; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry`; exit=1 |
| Predicate gate | counter read claims at freeze rev 2323d197 | passed (exit 1, not 2 — predicate byte-identical) |
| Instrument identity at HEAD | `git show 3ecf4298:tools/round-35/c2-calibration-counter.py \| sha256sum` | `576c14dd…` = canonical instrument pin (a85ca674 intermediate `3a23f3eb…` is the recorded supersession) |

## Findings
1. Ordering logic (`first_change_time`): oldest `%cI` in `base..rev` for the path — correct
   orientation (oldest = first change). Comparison `ct > fc` is strict; ties pass.
2. If vacuous-fail edge: with no post-base SOURCES.md change, `first_change_time` returns
   `None` and D-1 fails (`D1_no_sources_change_after_base`) even though the receipt is
   already in the first post-base commit — the semantic "committed before the first change"
   holds trivially. The predicate wording does not require a change to exist; the counter
   does. (At the final measured revision, C1 data will add S125/S129 rows — a post-base
   change strictly after 16:05:46 — so ordering would then pass; today's failure is the
   pre-data state.)
3. Content check is substring-based: `rows=106`, `EXIT=0`, `W04` presence only; the exact
   "9 W04 warnings" count is not asserted by the counter (file has exactly 9 today).

## Limits
- Measured revision used: `3ecf4298` (HEAD at review time), pre-data; D-2/D-3/D-4 failures
  in the same run are out of scope for this review.
- No `find`/`du`, no network, no writes outside this seat report.
