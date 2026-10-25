# R35Audit14 — C2 census ordering mutant

**Scope:** Read-only inspection of the frozen C2 claim/counter and immutable lane history; mutation experiments were confined to `/tmp/r35-audit14-w1` and `/tmp/r35-audit14-order`. No lane production files, counters, claims, corpus, plans, receipts, or VCS state were changed. The only lane write is this assigned report.

## Frozen target and implementation

- `plans/round-35-claims.md` lines 34–46 and `.ufo/waves/round-35/claims-canonical.json` claim C2 closure of D-1..D-4. D-1 specifies a committed census receipt before the first post-base `corpus/SOURCES.md` change and base count (106 rows, exit 0, 9 W04 warnings).
- `tools/round-35/c2-calibration-counter.py` lines 63–77 retrieves census and commit time at the measured revision; rejects missing required substrings; compares receipt commit time against `first_change_time`, computed as oldest `git log --format=%cI BASE..REV -- corpus/SOURCES.md` timestamp. It does not parse or count the nine W04 warning lines; it only tests for substring `W04`.
- Census receipt at lane HEAD `3ecf4298` contains nine warning lines, `EXIT=0`, and `rows=106` (read directly from `assimilation/census-start.txt`). The receipt entered history in `d2729cba` at `2026-10-25T16:05:46-03:00`. In history after declared base `aa04633a…`, `git log ... -- corpus/SOURCES.md` has 0 commits at the observed tip, so the counter's D-1 branch would fail with `D1_no_sources_change_after_base` at this tip; no D-1 pass can currently be established from this evidence.

## Mutation/falsification evidence

Commands were run with the frozen counter at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-35/c2-calibration-counter.py`; counter invocations were read-only and the supplied `--root` pointed at temporary repositories.

1. **Observed current tip:** `python3 -I -B <counter> --root /tmp/r35-audit14-w1 --base aa04633a686d49756763b1feed4be6830d5bb479 --freeze 2323d197456f1328459d9420aff025cffbcb3e27 --rev 3ecf4298` → exit 1, `C2_FAIL: D1_no_sources_change_after_base; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry`. The receipt exists at this tip, but no post-base SOURCES change exists; other listed failures are independent extant C2 failures.
2. **Ordering mutant:** built `/tmp/r35-audit14-order` with a base commit, then a `corpus/SOURCES.md` change timestamped `2026-10-25T16:19:30-03:00`, then a census receipt commit timestamped `2026-10-25T16:20:00-03:00`; added canonical predicate text at the synthetic freeze. Ran `python3 -I -B <counter> --root /tmp/r35-audit14-order --base "$BASE" --freeze "$REV" --rev "$REV"` → exit 1, `C2_FAIL: D2_lesson_missing; D3_entry_missing; D4_skill_missing`; notably **no D1 failure**. Thus the D-1 predicate (receipt later than first SOURCES change) was falsified, but the counter accepted the ordering because the first-change path uses `git log` commit timestamps and the counter checked no D1 failure. The temporary fixture omitted D2/D3/D4 surfaces, hence the unrelated named failures.
3. **Earlier fixture attempt / limitation:** a first chronology experiment used the full lane clone and got `D1_no_sources_change_after_base` because the synthetic empty commits did not actually modify `corpus/SOURCES.md`; that run was not treated as evidence about ordering sensitivity. The focused fixture above has an actual SOURCES diff and isolates the false acceptance of D-1.

## Advisory finding

The frozen counter's D-1 ordering test is bypassable by a valid history where a SOURCES-changing commit precedes the census commit. It compares `%cI` timestamps rather than commit ancestry/order, and the first-change helper returns the oldest timestamp-sorted log line. The synthetic counter result demonstrates absence of D-1 failure in the deliberately late-census case. This is a falsification only; claim predicates/instrument scope were not changed.

**Limits:** Synthetic experiment proves counter behavior on the explicit constructed history, not a scored lane measurement. No test/build/lint/formatter was run. No LSP session was available or used. All source trees were treated read-only.
