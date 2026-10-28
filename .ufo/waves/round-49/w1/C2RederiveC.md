# C2RederiveC — independent re-derivation of C2 atoms A7, A8, A9 (pre-freeze, draft instruments)

Verdict: **A7, A8, A9 re-derive independently and agree with `c2-after.py` and the draft counter; no disagreement.** The after-state fixture scores `mismatches 0` and the freeze state 9. Three weaknesses are real but do not change the numbers: A7 is blind to which entry the quote sits under, A8 does not bound `identified`, and A9 is a string-presence check over a file unchanged since the base. UTC 2026-10-28; scratch removed; artifacts in `w1/C2RederiveC/`.

| # | check | command / method | result | exit | sha256 |
|---|---|---|---|---|---|
| A7a | snapshot after tag strip carries `EX_USAGE 64` and the 22-word quote | `python3 -I -B` inline: regex strip `<[^>]+>`, `html.unescape`, whitespace-collapse of `draft/snapshots/sysexits.html` | `EX_USAGE 64` present; quote present; `len(q.split())==22`; quote sits directly after `EX_USAGE` in the DESCRIPTION list (preceded by "The meaning of the code is approximately as follows:"); `EX_USAGE` occurs exactly 2x, the quote 1x. The raw HTML does NOT contain the quote or `EX_USAGE 64` as plain strings (tags/newlines intervene), so stripping is mandatory | 0 | snapshot `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` |
| A7b | live fetch today | `curl -sS -A 'Mozilla/5.0' https://man7.org/linux/man-pages/man3/sysexits.h.3head.html` at 2026-10-28T21:07Z and again | HTTP 200, 12725 B, sha256 equals the snapshot, both fetches byte-identical (`cmp`) | 0 | `d9db4b96…b340` (`sysexits.today.html`) |
| A7c | the old S146 URL | `curl … sysexits.h.3.html` | still HTTP 404, 196 B, `80c3fe2a…f6faf880`, matching the S146 row | 0 | `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880` |
| A8a | registry row counts | `git show <rev>:corpus/SOURCES.md` + `grep -cE '^ {0,3}\|\s*S[0-9]{3,}\s*\|'` | 61b87d74 → **144** (S001–S144, no duplicate ids); 8847042a → **146**; e4f2cfa5 → **146**, file byte-identical to 8847042a (`68e6d028…e712`; 61b87d74 file `ad6ddf4d…93b1ae`) | 0 | see files |
| A8b | new-id split 61b87d74→8847042a | `diff` of the two blobs | exactly two added rows: S145 status `mined` (included), S146 status `rejected` (excluded) → included 1, excluded 1, rows 144 → 146 | 0 | |
| A8c | pre-existing search-log entry for round 48 | `grep 'round 48'` in the tip registry | none (only the S145 row); last log entry is round 33 — the late round-48 entry is genuinely absent at base | 0 | |
| A8d | round-49 split | S147, S148 (both `mined`) → included 2, excluded 0, rows 146 → 148 | agrees with `c2-after.py` `e49` | — | |
| A9 | closure states the verdict | `grep` of `corpus/lessons/round-48-verifier-spotcheck.md` | line 7 states "Admission: **rejected-harmed**"; line 107 is a table row `\| calibration \| harmed \| …`; lines 125/141 repeat it; both counter checks (`rejected-harmed` substring, regex `\|\s*calibration\s*\|\s*harmed\s*\|`) hit the base blob | 0 | |
| fix | `c2-after.py` vs derivation | mkclone → c2-after (`DEV_FREEZE=660f6563…`, `DEV_AFTER=1b754f10…`), `c2-mismatch.py --rev AFTER` | `e48` "identified 2, screened 2, included 1, excluded 1; rows 144 → 146" and `e49` "included 2, excluded 0; rows 146 → 148" equal my numbers; counter exit 0 mismatches 0 (`after.out` `7614d87b…`); at freeze exit 1 mismatches 9; `--battery` exit 0, `failing []`, do-nothing red on all nine (`bat.out` `41660aa3…`) | 0/1/0 | |

## Forgery / fragility probes (fixtures: scratch clone `clone/`, branches f1–f6 on `DEV_AFTER`; none touched the lane)

| id | mutation | counter result | reading |
|---|---|---|---|
| F1 | replace `corpus/evidence/round-49/c2/sysexits.html` with a one-line fake containing only `EX_USAGE 64` + the quote, re-pin its sha in S148 | exit 0, `mismatches 0` | **A7 is satisfiable by a forged snapshot**: the pin is circular (the row pins the committed file). Only the live re-fetch (A7b, above) ties the snapshot to the page. Acceptable if disclosed; the counter never touches the network, so wave 2 should repeat the fetch compare. |
| F4b | in the S148 row only, swap the quote for the EX_DATAERR sentence "The input data was incorrect in some way." | exit 0, `mismatches 0` | **A7 does not check the quote belongs to the EX_USAGE entry** although the row's anchor says "EX_USAGE entry" and the atom is about EX_USAGE. A6 checks the section heading above the quote; A7 has no analogue. Suggested: assert the quote is the text immediately following `EX_USAGE` in the normalised snapshot. |
| F3 | change the round-48 entry to "identified 99, screened 2" | exit 0 | `identified` is only bounded `>= screened`; the "identified" count is unverified (the docstring says "every number is re-derived" — true for rows/included/excluded only). |
| F5 | append other claims to the A9 line (`… calibration=harmed (and every other axis improved, calibration 10 -> 10)`) | exit 0 | A9 is substring presence of a constant; the source file is unchanged since base, so A9 is red only while the SCORECARD line is missing, and re-derives nothing beyond what the base already holds. SCORECARD `## Round 48` line 3739 still says `calibration 10 → 10` unannotated; A9 does not bind that contradiction to the correction. |
| F6 | add an extra row S149 after S148 at REV | exit 1, A8 red (`derived 146 -> 149`) | **A8 round-49 entry is fragile**: any other registry row added in round 49 (wave seats, L1 landing, a new source) falsifies the entry. Fix the plan text or the entry at landing: the plan names only S147–S148 as C2 rows; if L1 adds any row, the round-49 entry must be written with that final count. |

Note: my first F4 attempt also edited the S145 row (`(22 words)` replace) and correctly turned A6 red (`S145 was rewritten (append-only)`), a side confirmation that the base-blob equality check works.

## Disagreements with `c2-after.py`
None. Its hard-coded entry numbers (2/2/1/1, 144→146; 2/2/2/0, 146→148) equal the independent derivation. The two search-log entries are consistent with the registry as committed.

Tooling: none installed. Not run: any C1 command; battery mutations other than via the counter's own `--battery`.
