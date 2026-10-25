# R35Audit43 — immutable-read critic findings

**Scope:** advisory review of frozen C1/C2 predicates and immutable-Git counter reads. No lane production/corpus/counter/claim/VCS changes. Axes: coverage (C1), calibration (C2), and claim-measure validity.

## Decisive counterexample: C1 checks trio presence, not opening trio

The plan's C1 after-state explicitly requires each entry to “opens with the provenance trio” (plan lines 18–22). The frozen counter checks each `^source:`, `^verified-at:`, and `^recheck:` anywhere in the entry (`c1-coverage-counter.py` lines 105–113), then separately checks that a source line contains the expected S125/S129 text. Thus an entry beginning with arbitrary, unsupported prose (or a false claim) and carrying the three labels much later passes these checks; it need not open with provenance, and the expected row need not establish that the claimed content was actually sourced. This is a concrete gap between stated check and predicate, not an allegation about current entry data. The regexes can also match a later source citation while the first `source:` line is unrelated.

**Impacted axes:** C1 coverage and measure validity. **Smallest safe correction:** for any future freeze (not this one), validate the exact initial provenance block at the beginning of the file and bind its source line to the expected row; do not change this frozen predicate/counter or reinterpret this round. The present C1 counter cannot substantiate the stronger “opens with” wording by itself.

## Other counterexample: C2 D-1 ordering is timestamp-only

C2 obtains the census path's latest-touch commit time via `git log -1` and compares ISO committer timestamps to the oldest SOURCES change timestamp (`c2-calibration-counter.py` lines 45–53, 70–77). A commit can be an ancestor of the SOURCES edit yet carry a later committer timestamp (or vice versa); timestamp comparison can therefore reject the required commit ordering or accept the opposite history. If the census file is subsequently touched, `commit_time` is that later touch, not necessarily the receipt's introduction. The plan uses committed-before ordering, which is a history relation, not wall-clock time.

**Impacted axis:** C2 calibration. **Smallest safe correction:** future instrument should derive the first post-base SOURCES-changing commit and census-introduction commit from the ancestry/reachability graph, and test ancestry/order; preserve the frozen instrument unchanged for this claim.

## Additional concrete weakness: C2 D-4 stops at the first matching heading

For each named section, C2 scans from the first exact matching heading and stops on the first malformed pipe row (`break`, lines 135–151). A valid eight-cell first table row followed by a malformed data row in the same section is not fully checked; duplicate section headings after the first are ignored. The claim says every data row. This is directly falsifiable with a synthetic section containing a good row then a five-cell row.

**Impacted axis:** C2 calibration. **Smallest safe correction:** future parser should examine every row in each intended section and reject ambiguity/duplicates; no frozen-predicate modification now.

## Repository evidence / commands

- Read immutable revisions and files; current lane tip observed as `3ecf42981a0b63414de90ade643040d609dbb8a5`.
- `git log --format='%h %cI %s' --reverse aa04633a686d49756763b1feed4be6830d5bb479..HEAD -- .ufo/waves/round-35/claims-canonical.json tools/round-35/c1-coverage-counter.py tools/round-35/c2-calibration-counter.py corpus/SOURCES.md` shows instrument/canonical history through `2323d197`; no SOURCES change in this range. `2323d197` added the canonical snapshot and finalized counter bytes. `3ecf4298` subsequently added the do-nothing control receipts only.
- SHA-256 at working tree: C1 `e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220`; C2 `576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94`; plan `45b644a44851b8302dd0a3699e09220ca3b39aad8685ffeb3ae1b6aca9167138`. Their hashes match the canonical pins. `git show 2323d197:<counter> | sha256sum` produced the same respective digests.
- Executed both counters at the base revision with freeze `2323d197456f1328459d9420aff025cffbcb3e27`. C1: exit 1, missing both target entries, S125/S129 rows, PROVINCE stems, and README filenames. C2: exit 1, D1 census missing, D2 lesson missing, D3 trio/S106 missing, D4 round-32 malformed row and round-34 section missing. These agree with committed control receipts. This verifies the do-nothing failure only; it is not a selftest or a score at a post-data revision.
- Census receipt read: it records 106 rows, `EXIT=0`, and nine W04 warnings; canonical JSON and plan agree on the declared claims. `freeze-status.md` separately documents the earlier round-34 freeze-integrity failure and says later work may only falsify unchanged targets, not re-freeze. Current worktree status showed orchestration-created untracked wave files; no VCS state was changed.

## Limits and disposition

No post-data measured revision was scored, no selftest or synthetic mutation was run, and no source captures were independently reopened. Review findings are static counter/predicate counterexamples; they do not establish that current data files fail or pass C1/C2. The frozen claims, scope, and kill rules remain untouched. Recommend treating the findings as limitations of what the counters prove, not as permission to relax or amend the frozen claims.
