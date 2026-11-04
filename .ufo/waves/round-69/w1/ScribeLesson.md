# ScribeLesson — round 69 w1 report

Seat: ScribeLesson (scribe). Lane `kaidoku-shokunin`, round 69 attempt 1, wave `r69-w1`.
Base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`; operative freeze
`f15998102f1ce3569e61faa2ac6f286bc414538e` (re-derived with
`git log --diff-filter=A --format=%H -1 -- .ufo/waves/round-69/claims.json`).
Role: draft `corpus/lessons/round-69.md` under my wave dir; the L1 lands it. No verdict is claimed.

## Behavior

1. Read the three prior lessons (`round-68.md`, `round-68-verifier-spotcheck.md`, `round-67.md`), the
   declaration (`plans/round-69-claims.md`) and the frozen container (`.ufo/waves/round-69/claims.json`).
2. Re-derived the before-arm values from the committed pre receipts myself (parse, key dump, then
   `git show <rev>:corpus/SOURCES.md` for the census population) rather than restating them.
3. Opened four sources live (curl, bytes + sha256 measured) and recorded the receipts in
   `fetches.json`: UPX `doc/upx.1` and `doc/upx-doc.txt` at `v5.2.0`, the GitHub release page, the Arch
   man-page mirror. ScoutSource had produced no `sources.md` (its dir was empty), so the Gate rows are
   my own opens.
4. Read the peer drafts that had landed by then (`ReviewerGates/{attacks.json,review.md,
   freeze-integrity.json}`, `SentinelScope/audit.md`, `ExecC3/c3-at-landing-exec3.json`,
   `ExecRepairs/evidence/`) and mined them only where a source read could corroborate the mechanism.
5. Wrote `lesson.md` (Gate / Mistakes / Outcome / Census), `sources-opened.md`, `fetches.json`.
6. Scratch `/fast/scratch/hyaku/kaidoku-r69/ScribeLesson/` created and removed; `ls` after removal
   prints `No such file or directory` (**observation**).

## Gates (the lesson's source decisions)

| row | decision | basis |
|---|---|---|
| `doc/upx.1` at `v5.2.0` (S270) | **ADMIT** | HTTP 200, 40 077 B, sha256 `09552b3c…` = the row's pin; line 164 is `\&\fB\-\-version\fR: print the version of \fBUPX\fR` (rendered `--version: print the version of UPX`, 6 words); checksum sentence lines 112-114 |
| `doc/upx-doc.txt` at `v5.2.0` (S269's URL) | **not a row** | same sentence, same tag, literal this time (line 99, offset 3 653, 6 words, sha256 `4dc547ed…` = S269's pin); a second row would duplicate URL and scope → secondary locator inside S270's anchor cell |
| GitHub release page `v5.2.0` | **REJECT as this round's row** | 0 occurrences of the flag contract; two fetches of the same URL returned 162 743 B / `d9770b01…` and 162 744 B / `53033ceb…` — not byte-stable |
| Arch man-page mirror | **REJECT** | 47 791 B / `aed1c12a…`; renders `upx 5.2.0` and the sentence once, but is bound to the distro package build, not the upstream tag |

## Touched surfaces

- Written, mine: `.ufo/waves/round-69/w1/ScribeLesson/{lesson.md,sources-opened.md,fetches.json}` and
  this report `.ufo/waves/round-69/w1/ScribeLesson.md`.
- Scratch: `/fast/scratch/hyaku/kaidoku-r69/ScribeLesson/` (created, removed).
- Everything else read-only: `git log/show/diff/status/rev-parse`, `read`/`grep`, `python3` parsers,
  `curl` GET, `scripts/sources-census.sh census` (text parse, exit 0).
- **No** tracked lane file, index, commit, push, jj command, fleet-root file, `PATH` directory, clone or
  pacman transaction was touched. No tool was installed or upgraded.

## Findings

All labels are per item: **observation** = seen in tool output; **inference** = derived from code or
evidence; **unknown** = not established.

- **F1 (observation) — the C3 base receipt was not JSON, and its in-place repair loses the command.**
  The filed bytes (`git show HEAD:.ufo/waves/round-69/l1/pre/c3-at-base.json`) begin with a shell echo
  (`+ /usr/bin/python3 -I -B tools/round-69/packed-elf.py --check-receipt …`), so `json.load` raises
  `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`; the body from line 2 parses to
  `target 2`, `carriers_matched 2`, `met false`, `kinds [null]`, five failing clauses. At 23:40:51 the
  working tree removed exactly that line (`git diff`: one deletion) and the file now parses — but the
  command survives nowhere, and the body still carries no `rev` and no `instrument.sha256`, unlike the
  other three pre receipts (the checker's output schema at `packed-elf.py:309-314` has no such keys).
  Mined as M69-3; the rewrite is the L1's to disclose, not mine to reverse.
- **F2 (observation) — S270 is staged, not committed.** `git status --porcelain` shows
  ` M corpus/SOURCES.md`; `git show <rev>:corpus/SOURCES.md | grep -c 'S270'` = 0 at the base, the
  declaration and the freeze. The +2-line diff adds S270 only. Its source re-derives (F-row above);
  its quote is a roff-rendering, and the row does not say so — the literal twin is `doc/upx-doc.txt:99`.
- **F3 (observation) — word-count drift recurs.** The working-tree lesson draft
  (`corpus/lessons/round-69.md`, 23:38:19, not mine) says the quote is "(5 words)";
  `printf '%s' '--version: print the version of UPX' | wc -w` = **6**. This is the R68-V5 class in the
  round that was meant to close it. Mined as M69-8; my draft states 6.
- **F4 (observation) — the release page is not byte-stable.** Two fetches of the same URL, minutes
  apart, differ in size and digest (mine 162 743 B / `d9770b01…`; the draft's 162 744 B / `53033ceb…`).
  Independent of the reject: a page whose bytes move cannot anchor a sha256 row.
- **F5 (observation + inference) — the frozen C3 checker passes absence.** From
  `w1/ReviewerGates/attacks.json`: `missing-identity-arm` rc 0 `met true` (jq's arms omit
  `identity_ok`); `one-carrier-no-arms` rc 0 `met true` (one carrier, `arms {}`, top-level
  `carriers_matched 3`); `nan-ratio` rc 0 `met true`. I corroborated the mechanism in the frozen source
  and did **not** re-run the fixtures: `:283-284` compares the receipt's `carriers_matched` to
  `len(CARRIERS)` and never to `len(receipt["carriers"])`; `:299-301` iterates supplied arms only;
  `:303` rejects only `not isinstance(ratio,(int,float)) or ratio > 0.75`, so NaN passes. Boundaries
  behave (`0.75` passes in `boundary-075`; `0.7501` fails in `boundary-over075`), and an explicitly
  false arm is rejected (`explicit-false-arm` rc 1). Mined as M69-4 and M69-5.
- **F6 (observation + inference) — validators check arithmetic, not inventory.**
  `mutation-invented-kills` rc 0 `{"defects": [], "mutants": 1, "ok": true}` and `probe-invented-arms`
  rc 0 `{"arms": 6, "defects": [], "ok": true}`; `mutation-check.py:173-203` and
  `contract-probe.py:219-247` check row shape, booleans and `arms_passed`/`failed` derivation only.
  Mined as M69-6.
- **F7 (observation, attributed) — the C2 probe passes a foreign receipt.** The reviewer's
  `foreign-probe` runs the frozen probe at `--rev f1599810…` with `--receipt
  foreign-instrument-receipt.json` (`instrument.path different-instrument.py`, all-zero hash, `rev
  unrelated-revision`, `argv ["not-upx","--best"]`) and exits 0 with `arms_passed: 6`. This is the
  reviewer's run, not mine. **Inference:** it bears on the predicate's "with the measured run's
  receipt" clause and on A5/A6 provenance; the L1/judge must read it, and the frozen instrument cannot
  be edited to fix it. I record it; I do not judge it.
- **F8 (observation) — the peer after-battery ran at the freeze, not the landing.**
  `attacks.json` `battery-r69.argv` carries `--rev f15998102f1ce3569e61faa2ac6f286bc414538e`; the
  frozen predicate and atom A9 require the *measured* revision. Its result (rc 0, five `killed`, each
  `failed` exactly its declared case, `cases 20`; `battery-r68` at `--rev d7d9a62c…` five `survived`,
  `cases 13`) is peer evidence, not the L1's after-arm. My Outcome block is placeholders only.
- **F9 (observation) — the sentinel's undated status claim.** `w1/SentinelScope/audit.md` §1.1
  concludes "No tracked file is modified" from a `git status --porcelain --untracked-files=no` that
  prints no instant; four tracked files carried modifications dated 23:36:55-23:37:20 (`PROVINCE.md`,
  `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/2026-11-03-r68-packed-elf-route.md`), more
  followed by 23:40:51 (`LOG.md` 23:39:55, `corpus/QUALITY.md` 23:39:42,
  `corpus/claim-freezes-v2.tsv` 23:40:12, `tools/round-29/prefile-check.sh` 23:38:55,
  `l1/pre/c3-at-base.json` 23:40:51), the audit file's own mtime is 23:37:50, and my `git status` at
  02:42Z lists all of them as ` M`. Mined as M69-7: the defect is the missing instant, not the drafts
  (they are the landing set).
- **F10 (observation) — census population.** 176 rows at the base, the declaration and the freeze
  (`git show <rev>:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3}'`); 177 in the uncommitted working tree
  (`sources-census.sh census … kaidoku` → `kaidoku rows 177`, `tier.A 163 B 9 C 5`, `mined 168`,
  `rejected 9`). `census-start.txt` records 19 W04 and `ok` but no count field; the 176 is my
  measurement. The end value must be read at the landing revision, not the working tree.
- **F11 (observation) — a landing-path lesson draft already exists and is being rewritten.** The
  untracked `corpus/lessons/round-69.md` was 6 696 B at 23:38:19 and 7 410 B at 23:40:05; it still says
  the 6-word quote is "(5 words)" (F3), and its Gate preamble says every row was opened by the L1 or by
  "a seat whose fetch is committed under `.ufo/waves/round-69/w1/ScoutSource/`" while that directory is
  empty (measured `ls`, 02:42Z) — a pointer that does not resolve. It is not mine; my draft sits under
  my seat dir and differs materially (6-word count, 8-row mistake table, `[L1]`-only Outcome). The L1
  must reconcile the two before landing one.
- **F12 (observation) — `l1/scores/` was still empty at 02:42Z**, so no after number exists in any form
  the round owns; the Outcome block is placeholders only.

## Out of scope (not done, by rule)

- No edit to any frozen instrument, the claims container, the declaration, the counter, or the judge.
- No verdict on R69-C1, R69-C2 or R69-C3; no narrowing, widening or re-freezing.
- No re-run of the after-arms, the mutation battery, the contract probe, the controls or the carriers;
  the peer values above are attributed, never adopted as my measurement.
- No commit, push, or jj command; no write to `corpus/`, `PROVINCE.md`, `SKILL.md` or any other tracked
  path (the working-tree edits found in F2/F9/F11 are not mine).

## Tooling

None installed or upgraded (no `uv`, `npm`, `cargo`, release binary, and **no** pacman transaction —
the host-wide pause was respected). Used: `curl` (GET only), `python3` 3.14 (`-I -B` for parsers where
the interpreter was used as a library), `git` read-only, `grep`/`awk`/`sha256sum`/`sed` for byte
locators.

## Artifacts

- `.ufo/waves/round-69/w1/ScribeLesson/lesson.md` — the draft to land as `corpus/lessons/round-69.md`.
- `.ufo/waves/round-69/w1/ScribeLesson/sources-opened.md` — every source this seat opened.
- `.ufo/waves/round-69/w1/ScribeLesson/fetches.json` — url / http / bytes / sha256 for the four opens.
- `.ufo/waves/round-69/w1/ScribeLesson.md` — this report.
