## CLAIM
Full mutual-contradiction sweep over all 119 sibling drafts (63 Lane A + 56 Lane B; full read, 16:47 snapshot) against rounds-2-4 landed text: substance converges on all seven items; five interface/record-class contradictions and three landed-text misstatements remain.

## METHOD
Read every `.ufo/waves/luna-round-5/*.md`; verified claims via `git show HEAD:` (r9-02, r5-02, r12-01, r4u-01, asar-surface, PROVINCE, README, LOG, QUALITY, SKILL, SCORECARD, round-4 report) and re-ran the C4/X1 gate predicates in Python on drafted wordings. No probes; only this file written.

## FINDINGS
1. **PIN wording.** D3/V3/F3/G3/DB3 write "pin the exact request bytes" — all fail C4.md:25 and X1.md:32 (literal "pin request bytes") in my sim; VB3/Y1's variant passes. ZB3.md:9 ("D3/V3 pass") is refuted by the same sim. The "exact" form also departs from landings r9-02:168-169, QUALITY.md:25, README.md:170, SKILL.md:218-220.
2. **r12-01 stand-off.** X1's census and C4.md:15-19 require a new append ('supersedes main text', four sites); D7/G7/R2/VB7 say none is needed — a correct integration still reports R12-01 DEBT unless a pointer append lands or the gates change.
3. **Unsatisfiable SIZES check.** X1's matcher tests raw needles '29,367,752'/'84,258,816' against comma-stripped text; it cannot pass any correct erratum (reproduced; CB4.md:11, RB4.md:7). Fix the matcher, not the decimals.
4. **README.** Targets :131/:163 verified; F4/P1/C3 still use :160 (sasquatch) — F4 edits an eighth site and leaves :163 stale. D4/V4's text fails C4/X1 ("4 nits", "2 fixed") vs landed LOG.md:389-401 ("4 nits", "2 fixes applied at integration", one accepted); the LOG-spelled variant passes. Delete vs line-preserving replace unresolved; a restatement keeping "Runtime-obs extended" trips X1's frontier regex (reproduced).
5. **PROVINCE mechanics.** F3's byte-2961 new line shifts PROVINCE ≥34 citations; C2/DB3/Y1/ZB3/RB2 mandate an inline insert at :32 — F3 is the outlier.
6. **Landed-text misstatements.** P0.md:16/C5 say "four variance classes"; the erratum (r12-01:99-104) says "two classes across FOUR sites"; r4-16:750-754 still carries the two-site account (V7's r12-02:750-754 cite is out-of-range: 328 lines). CB8 contests the freshness label (SCORECARD.md:334-335 depth ruling) vs P2's planned "owned axes unchanged" record.

## THREATS
Gates are lexical and simulated on drafted strings; final wording unknown. Lane B was still racing (119 files; sample skew possible). Round-4 carry for items 6-7 exists only in wave files V10a:10-11/V11b:11, not the round-4 report's list (:48-57). No live verification of any pinned /tmp receipt.

## VERDICT
FINDING: harmonize PIN/README/r5-02/r9-02 wordings with gates, fix X1's SIZES matcher, settle r12-01 append and README :163 mechanics, and avoid "four classes"/"pin the exact"/"2 fixed" before integration.
