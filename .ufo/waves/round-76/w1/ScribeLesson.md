# ScribeLesson — round-76 lesson draft

Produced the lesson draft at `.ufo/waves/round-76/w1/ScribeLesson/lesson-draft.md` with the three
required sections: **Mistakes** (one row, class `a self-assessment sentence written before its
artifact existed, and a printed command never executed by its author`, captured by D24 and the
plan-command gate), **Gate** (S286 admit, S287 admit, S288 reject with reason and flip, each with
URL, access date, located quote and digest; plus the census before/after line), and
**Routed-defect disposition** (all eight round-75 routed defects, items 1 and 2 → R76-C1, item 4 →
R76-C2, items 3/5/6/7/8 → unclaimed record corrections with the correction text named).

Evidence in the same directory: `receipt.json`, `gate-fetches.json`, `checks.json`,
`census-after.txt`.

## Findings

1. **Gate digests reproduced independently.** This seat fetched all three pages once on
   2026-11-04: `shlex.html` HTTP 200, 66 497 bytes, sha256 `4c1f8bf6…`; `argparse.html` HTTP 200,
   334 994 bytes, sha256 `14d33eea…`; `bash.1.html` HTTP 200, 497 852 bytes, sha256 `e35fa296…`.
   All three match the committed snapshots under `.ufo/waves/round-76/l1/sources/` exactly, and the
   quotes are literal and located at the lines the rows name (shlex line 229, argparse 2417-2418,
   bash line 477).
2. **Conflict — the W04 count.** The seat brief says 24 W04 warnings at round start; the committed
   receipt `.ufo/waves/round-76/l1/census-start.txt` carries 23 W04 lines (`awk -F'\t'
   '$2=="W04"' … | wc -l` → 23), and the round's post-append run also carries 23. The draft reports
   23 and states the conflict verbatim; the receipt is authoritative.
3. **Conflict — the S288 URL.** The frozen candidate `https://man7.org/linux/man-pages/man1/sh.1.html`
   returns HTTP 404 (196 bytes); man7's section-1 index lists only `sh.1p.html` (line 2900). The
   landed row S288 names the live `bash(1)` page and discloses the substitution; the draft's Gate
   does the same. This is a deviation from the frozen brief, not a silent one.
4. **Census after the rows.** 194 rows, validate exit 0, 0 E-findings, 23 W04
   (`.ufo/waves/round-76/w1/ScribeLesson/census-after.txt`, run with the three rows present). The
   first run, taken before the sourced knowledge entry landed, exited 1 with E11 on both admitted
   rows' used-by path; the entry is on disk now and the rerun is clean. The draft cites only the
   clean run.
5. **Risk — landing receipts absent.** The appended SCORECARD capability rows point at
   `.ufo/waves/round-76/l1/scores/c1-at-landing.json` and `c2-at-landing.json`; neither exists on
   disk at draft time. D24 requires each named row's evidence pointer to resolve at the measured
   revision, so the landing must produce both before the lesson is final.
6. **Risk — landing tree uncommitted.** The S286-S288 rows and the four-row SCORECARD append are
   working-tree changes; the draft cites their landing-tree line numbers (`SCORECARD.md:654-655`,
   `corpus/SOURCES.md:202-204`) and does not treat them as filed bytes.

No lane file was edited; the only writes are this report and the seat evidence directory.
