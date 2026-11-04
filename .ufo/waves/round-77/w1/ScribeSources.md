# ScribeSources — round-77 w1: three source rows and two knowledge entries drafted under evidence

Seat: ScribeSources (scribe). Date: 2026-11-04. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Evidence: `.ufo/waves/round-77/w1/ScribeSources/`. No production file was written by this seat.

## Behaviour

The seat spec's five steps were executed against the committed frozen snapshots in
`.ufo/waves/round-77/l1/sources/`. Outcome:

1. **Three quotes verified byte-exactly** at the named lines, each occurring once per file:
   RFC 8259 line 298, Bash manual line 4435, `ast` docs line 2760 (`bytes_verified: true` for all three in
   `receipt.json`; `quotes.txt` holds the `grep -n` run).
2. **Three rows drafted** with 11 cells each and no literal or escaped pipe: `S289` RFC 8259 §3 (admit, `mined`,
   `spec`, tier A), `S290` GNU Bash Reference Manual Edition 5.3 §3.7.5 (admit, `mined`, `docs`, tier A),
   `S291` `ast.literal_eval` (REJECT with reason and flip, `docs`, tier C). Full text in `rows-draft.md`;
   `check-rows.py` reports `failures: []`.
3. **Id collision check read from the registry**: the freeze tip's highest id is `S288`, so the next free numbers
   are `S289`–`S291`; those ids are already committed for these same three sources (`fd0b95bd`, `## Gate` of
   `corpus/lessons/round-77.md`). The drafts therefore replace the committed rows. Appending them beside the
   committed rows makes the census print `E03` ×3 (fixture `fix-r77app`, exit 1); replacing yields exit 0, no
   E-code, the baseline's 23 `W04` unchanged.
4. **Duplicate URLs named**: the RFC URL is held by **S049** (`https://www.rfc-editor.org/rfc/rfc8259`) and the
   JSON URL by **S050** (`https://docs.python.org/3/library/json.html`). The `…/rfc8259.txt` path is a different
   normalized string, so S289 does not collide; a row citing the HTML URL would print
   `W04 <id> duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes`, the warning class fixed at
   `scripts/sources-census.sh:33` (warnings never change a clean lane's exit; only `E04` is an error, and only
   inside one scope).
5. **Two knowledge entries drafted**, one per admitted row, each with a `## Gate` block carrying the URL, the
   access date 2026-11-04, the full snapshot sha256, the located quote with its line, and the consumer site.
   The reject's Gate records the consumer search.

## Gates and checks run (all read-only)

```text
$ sha256sum .ufo/waves/round-77/l1/sources/{rfc8259.txt,page-721dd237.html,page-298eb5f5.html}
61a5378f…4cd2d7  rfc8259.txt        28360 B
78d0eefb…1e2b4b  page-721dd237.html 1040954 B
8cacd731…d8dcb2  page-298eb5f5.html 362493 B

$ grep -n 'A JSON value MUST be an object' rfc8259.txt                     -> 298
$ grep -n 'Bash itself returns the exit status of the last command' page-721dd237.html -> 4435
$ grep -n 'Evaluate an expression node or a string containing only a Python literal or' page-298eb5f5.html -> 2760

$ python3 -B check-rows.py                   -> failures: [], words 14/10/13, quotes line-exact, occurrences 1
$ grep -c 'literal_eval' tools/round-77/verdict-bind.py   -> 0, grep-exit=1

$ bash ../scripts/sources-census.sh validate --today 2026-11-04 --file corpus/SOURCES.md
  exit 0 · 23 W04 · ok · no E-code
$ bash ../scripts/sources-census.sh census --today 2026-11-04 --file corpus/SOURCES.md
  exit 0 · 197 rows · tier A 181 / B 9 / C 7 · mined 179 / rejected 18

$ TMPDIR=<scratch> bash ../scripts/sources-census.sh validate --today 2026-11-04 <scratch>/fix-r77repl-shokunin
  exit 0 · 23 W04 (identical to baseline) · no E-code
$ TMPDIR=<scratch> bash ../scripts/sources-census.sh validate --today 2026-11-04 <scratch>/fix-r77app-shokunin
  exit 1 · E03 S289 / E03 S290 / E03 S291 duplicate id · 26 W04
```

Measured revision: HEAD `509c105140e90f7299b024796914e2639c206cb9` (base `188562d4…`, declaration `819cf30e…`,
freeze `6767a879…`, all ancestors). Instrument pins recomputed and equal to the frozen pins:
`verdict-bind.py` `45280392…d932a9e7`, `prefile-receipt.py` `174eedb5…bac2d3fd`.

The fixture builder `build-fixtures.py` reproduces the replace transcript byte-for-byte from the live registry plus
`rows-draft.md`; the first attempt that used `--file` into a bare scratch dir produced spurious `E11` findings and
is recorded as not-evidence in `sources-rows.md` §3.

## Touched surfaces

- Written, inside the seat's own evidence dir only: `rows-draft.md`, `sources-rows.md`,
  `knowledge-rfc8259-section3.md`, `knowledge-bash-exit-status.md`, `receipt.json`, `check-rows.py`,
  `check-rows.json`, `build-fixtures.py`, `quotes.txt`, `consumer-search.txt`, four `census-*.txt` transcripts.
- Not written: every production file, including `corpus/SOURCES.md`, `corpus/lessons/round-77.md`, the two
  `corpus/knowledge/2026-11-04-r77-*.md` entries, `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, any `tools/` file,
  the fleet root, any sibling lane, `~/.local/bin`, `.ufo/state/`. No git/jj write; no commit, push, stash or
  checkout. Scratch `/fast/scratch/hyaku/kaidoku-r77/ScribeSources/` deleted before yield.

## Findings (reported; the L1 decides)

1. **The landing was committed mid-seat.** At first read the registry carried the rows uncommitted (`M
   corpus/SOURCES.md`); by the time of the byte checks HEAD was `509c1051` and `fd0b95bd` had committed the two
   admitted rows, the reject, the two knowledge entries, the lesson and the SKILL registry rows. This seat wrote
   none of them and did not edit them; the drafts here are the independently byte-verified replacement text.
2. **Gate word counts are wrong in the committed lesson.** It states 16 / 11 / 15 words; `wc -w` on the quoted
   strings gives **14 / 10 / 13**. All under the QUALITY #42 ceiling of 25, so the quotes are admissible and only
   the counts misstate them.
3. **`(QUALITY row 36)` is a mis-citation.** Both the committed S291 `teaches` cell and the lesson Gate cite
   QUALITY row 36 for the consumer search; row 36 is the source-decision reversal-traceability rule and has no
   consumer-search clause (no QUALITY row does). The round-76 S288 reject is the precedent that actually uses a
   consumer search; the draft states the search and drops the citation.
4. **`HTTP 200` is unretained.** The lesson Gate and the rows assert HTTP 200 for all three GETs, and the lesson
   says "one GET each", but `.ufo/waves/round-77/` holds no fetch transcript (status, size, time). The retained
   bytes and digests are verified here; the HTTP status is carried from the committed prose, not re-observed.
5. **S290 names the wrong version class.** Committed: `Bash 5.x manual`. Snapshot line 9: `This is Edition 5.3,
   last updated 18 May 2025`. The draft names Edition 5.3 and carries the sentence's syntax-error exception
   (lines 4436-4437), which the committed `scope` omits — the exception bounds the exit-status claim.
6. **S291's committed source cell does not pin the build.** `Python 3 standard library` vs the page's own
   `Python 3.15.2 documentation` (title line 20). The draft pins 3.15.2.
7. **Committed digests are 16-hex prefixes** in the two admitted rows' source cells and absent from their anchor
   cells; the drafts carry the full sha256 in the anchor. No census rule requires a digest, so this is a
   strengthening, not a defect.
8. **No id or URL collision exists for the drafts.** S289/S290/S291 collide only if appended beside themselves
   (E03), and the RFC `.txt` URL does not collide with S049's HTML URL. The `W04` class is a warning by contract;
   the lane's 23 baseline W04 warnings are unchanged by a clean replacement.

## Out of scope

- Fetching or re-fetching any URL; judging the instruments, the claims, or the round's verdicts; editing the
  registry, lesson, knowledge entries, SKILL registry, PROVINCE/SCORECARD; the round-76 routed-defect repairs;
  commit/push; fleet census over the real lane.

## Artifacts

- `sources-rows.md` — the three rows, quote verification, id and URL analysis, the six divergences.
- `rows-draft.md` — the three rows verbatim (the file `check-rows.py` and `build-fixtures.py` read).
- `knowledge-rfc8259-section3.md`, `knowledge-bash-exit-status.md` — the two entries with their `## Gate` blocks.
- `receipt.json` — `quotes` (source, line, `bytes_verified`, snapshot sha256), `ids` (proposed, collision check,
  fallbacks), `duplicate_urls`, consumer searches, instrument pins, census results, divergences, limits.
- `check-rows.py` / `check-rows.json`, `build-fixtures.py`, `quotes.txt`, `consumer-search.txt`,
  `census-head.txt`, `census-rows.txt`, `census-fix-repl.txt`, `census-fix-app.txt`.

## Limits

- Snapshots were not re-fetched; only the retained bytes are claimed. A live-page drift is outside the draft.
- The census ran against symlinked scratch lanes, not the fleet root; the L1's fleet run remains the round's gate.
- The committed rows and entries are another hand's work; this report records their state at `509c1051` without
  asserting what the L1 will keep.

## Live conflict observed after the byte checks (reported verbatim, not edited)

While this seat was finishing, another hand edited the worktree (`HEAD` still `509c1051`; `git diff --stat`:
`SKILL.md 2`, `corpus/QUALITY.md 1`, `corpus/SOURCES.md 2`, `corpus/lessons/round-77.md 6`). Two changes bear on
this seat's evidence:

1. **Correction that agrees.** The lesson Gate's three quote word counts are now `14 / 10 / 13`, matching `wc -w`
   on the quoted strings (finding 2 above is therefore already being repaired).
2. **Regression, contradicting verified bytes.** The S289 quote line was changed from `298` to `303` in both
   `corpus/SOURCES.md` line 205 (`December 2017, section 3 Values, line 303; opened 2026-11-04`) and the lesson
   Gate (`section 3 Values, line 303`). The measured bytes put the quote on line **298**; line 303 is the literal
   name `true`:

```text
$ sed -n '296,305p' .ufo/waves/round-77/l1/sources/rfc8259.txt | cat -n
    1	3.  Values
    2	
    3	   A JSON value MUST be an object, array, number, or string, or one of
    4	   the following three literal names:
    5	
    6	      false
    7	      null
    8	      true
    9	
   10	   The literal names MUST be lowercase.  No other literal names are
```

   The drafts here keep line 298 (the quote's line) and name 301-303 as the literal-name span; QUALITY #42
   requires the quote's own line. This is reported for the canonical judge and not edited.

`corpus/QUALITY.md`'s addition is a row-135 addendum on verdict binding; it adds no consumer-search rule, so
finding 3 stands.
