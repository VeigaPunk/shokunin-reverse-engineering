## CLAIM
Audited row positions for round-7's six new rows in `corpus/README.md` at HEAD `411175e`: map rows after the r14-02 row and before `## Knowledge`; Knowledge-table rows at table end; insertion-neighbor bytes pinned for post-landing verification. No tracked file touched.

## METHOD
Read-only: `sha256sum corpus/README.md` vs `git show 411175e:corpus/README.md`; `grep -n '^## '`; per-line `sed -n '<n>p' | sha256sum` for 60–63, 130–131, 138–141; full-line uniqueness via `grep -c -F`; CR byte scan; `git show 16087e1/4b0c4d6/0f377e8/6645585 -- corpus/README.md` for append convention; regex simulation of `SCORECARD.md:102`.

## FINDINGS
- Worktree equals HEAD blob; both sha256 `9112c05b805b1d5abe494ff02c57ed350ab6567d8de945629361f33db861e12e`.
- Map anchor: `:61` = r14-02 map row, the file's last map row, full-line unique, sha256 `d2f3de9b0145a362f2db6bbca98b10cf2001c7c4d1ac34e4438c165aa5c6f946`; `:62` empty `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`; `:63` = `## Knowledge` `02aa548c21eb50e62f17ac76daf8b86f01f34cfa70a0013bb97763ba7f9c1f4e`. Insert between `:61`/`:62`; block `:60-63` sha `a87b2fac4cb304bb34b12a9739005fea9eee5ca573b4695fddc5e669ddd496b7` (`:60` = r14-01 row).
- Table anchor (instructed literal end; P0:8 "after its last row, before `## Lessons`"): `:139` = r4u-06 row, last Knowledge-table row, unique, sha256 `1625cc1b9ebc5b1471feacac2fa62e839d9c42b8f89bb07cb5a15e8a574af05c`; `:140` empty `01ba4719…`; `:141` = `## Lessons` `6b779597fe3a65ba4d87fe019a67c291b08c480be8c59a5d26fa18458320e2c6`. Insert between `:139`/`:140`; block `:138-141` sha `45aa1dc0d7745abb9c70245195a07ee700186d9ff0ce8956a5d8d8eeb89c210f` (`:138` = r4u-05 row).
- Alternate anchor (four-commit precedent): between `:130` r14-02 Knowledge row (`08dbc0f8021b78f7…`) and `:131` lessons row (`8f0f9bb1fb14a591…`).
- No CR bytes; all anchors free of trailing whitespace; file ends with `\n`. Post-landing, r14-02 must sit immediately above the six new map rows and r4u-06 immediately above the six new table rows, with the blank+heading hashes above closing each block unchanged.

## THREATS
- Placement is claim-critical: `SCORECARD.md:101` scans only the `## Coverage map` section, so the six new map-row tokens count only if inserted before `## Knowledge`.
- Anchor ambiguity: the last four row-append commits all inserted above the trailing `lessons`/r4-05/r4-10/r4u sediment (6645585 inserts the r14 rows after r12-02 and before the lessons row), so `:130`/`:131` is the four-commit precedent while the instruction's literal table end is `:139`/`:140`; both pass Command A/N1. FB3:10's "last row `:131`" contradicts rows `:132-:139`.
- Token hazard: drafts M1:11-13, K3:8-10, K4:10-12 carry underscore stems; simulated `re.findall(r'2026-10-\d{2}-[a-z0-9-]+', '…-l7-01-inspect_go_binary')` → `['2026-10-16-l7-01-inspect']` ⇒ partial token, so `mapped=78` fails (missing+dangling) unless rows land hyphenated per ruling (a).

## VERDICT
FINDING: map insert `:61→:62` verified clean; Knowledge insert must choose `:139→:140` (instructed literal table end) or `:130→:131` (four-commit precedent), and row stems must land hyphenated for mapped=78.
