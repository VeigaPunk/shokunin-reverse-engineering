# Draft landing text — `corpus/SOURCES.md` `## Search log` (A8), for L1 to adopt or amend

Not a landed artifact. Every number carries its command (CORPUS.md: "A count carries its command"). Bracketed items are facts the L1 must confirm from the round-48 Gate or the round-49 re-open before writing; do not land a bracket.

Format note: the counter's regex needs the header `- 2026-10-28 round 48` (the line must contain `late entry`) and `- 2026-10-28 round 49`, and the exact tokens `identified N, screened N, included N, excluded N` and `rows N → M` (or `->`). Keep those tokens verbatim.

## Round 48 (late entry)

```
- 2026-10-28 round 48 (late entry, written in round 49; searched in round 48, Gate in corpus/lessons/round-48.md) — Question: which primary source grounds the falsifiability criterion that makes a clause which cannot fail "not a check", and does a primary source ground exit 2 as a usage refusal? Where searched: no search engine [L1 confirm: no query run in round 48]; two fetches of URLs named in the round-48 Gate: https://plato.stanford.edu/entries/popper/ (HTTP 200, 118,135 bytes, sha256 2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207, accessed 2026-10-28) and https://man7.org/linux/man-pages/man3/sysexits.h.3.html (HTTP 404, 196 bytes, sha256 80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880, accessed 2026-10-28). Identified 2, screened 2, included 1 (S145, tier A, mined), excluded 1 (S146, rejected). Exclusion reason: HTTP 404 at the URL as written; the reachable sibling sysexits.h.3head.html was not opened in round 48 (opened in round 49, see below). Negative-claim sweep for "no primary source grounds exit 2 at this URL": the 404 fetch above; it is a sweep of one URL, not of the literature. Stop: both named candidates were the only ones opened in round 48 [L1 confirm]. Counts: rows 144 → 146 — `git show 61b87d74:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 144; same at 8847042a → 146; 2026-10-28.
```

## Round 49

```
- 2026-10-28 round 49 — Question: do the S145 locator (§2 "The Problem of Demarcation") and the S146 rationale (sysexits at the 404 URL; "no locator exists") survive a re-open of the two pages? Answer: no; both are corrected by supersession rows S147 and S148, not by rewriting S145 or S146. Where searched: re-open only, no new search; https://plato.stanford.edu/entries/popper/ (HTTP 200, 118,135 bytes, sha256 2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207, re-fetched 2026-10-28; the quote sits under the heading "Backdrop to Popper's Thought", before §3 "The Problem of Demarcation") and https://man7.org/linux/man-pages/man3/sysexits.h.3head.html (HTTP 200, 12,725 bytes, sha256 d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340, re-fetched 2026-10-28; `EX_USAGE 64`). Both re-fetched bytes equal the sha256 pins of rows S147/S148. Identified 2, both already-known families: 0 new families. Screened 2. Included 2, both as supersession rows (S147 supersedes S145; S148 supersedes S146); no new family. Excluded 0; no exclusion reasons. Stop: the two corrections answer the question; the claim needs no further source. Counts: rows 146 → 148 — `git show e4f2cfa5:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 146; at REV `git show <REV>:corpus/SOURCES.md | grep -cE …` → 148; 2026-10-28.
```

Decision for L1 (before freeze): the counter counts supersession rows as `included` (non-rejected new rows). Precedent is split: round-23 W2 correction kept "identified5/screened5/included4/excluded1" and called added supersession rows "corrections, not discovery"; round-25 residual counted three supersessions as included families. The text above states the convention, so the counter needs no change. If L1 instead wants `included 0`, the counter must change before freeze (plan sentence changes), not after.

## Contract elements the counter does not check (L1 writes by hand)

| element (SOURCES rule 5 / CORPUS) | in drafts | counter checks | action |
|---|---|---|---|
| question/query | both, round-49 question unanswered in draft | no | state the answer |
| where searched (URLs/databases, query, HTTP status, bytes, sha) | no | no | write per entry above; say "no query" if none |
| date of search | header only | header literal | keep `2026-10-28 round N` verbatim |
| identified | yes | only `identified ≥ screened` | self-reported and unbounded (`identified 999` passes); disclose or bound |
| screened | yes | screened = included + excluded | ok |
| included | yes | derived: non-rejected new rows (`queued` counts) | state supersession convention |
| excluded | yes | derived: rejected new rows | a padded rejected row passes (see F4); name the excluded ids |
| exclusion reasons | round 48 only in row S146, not in entry | no | write per excluded item |
| stop rationale | no | no | write |
| "a count carries its command" (CORPUS.md) | no | no | write the command beside each number |
| negative-claim sweep (SOURCES "a negative claim carries its sweep"; CORPUS) | no (round-48 "does not ground exit 2") | no | cite the 404 fetch and the 3head fetch |
| Gate: URL, access date, ≤25-word quote + location per new row (SOURCES rule 1; CORPUS `## Gate`) | draft lesson has no `## Gate` section | no | write the Gate table for S147/S148 in `corpus/lessons/round-49.md` |
| census before→after line (round-48 routed defect 4) | no | no | add the line to the landed lesson |
| used-by of S147/S148 lists the lesson | yes | A6/A7 partially | the lesson must exist before the census runs |
