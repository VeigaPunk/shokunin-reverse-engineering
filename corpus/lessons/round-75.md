# Round 75 — case independence and exact grammars

Base: `3c15a156239af06114e1ece8d1044a0d8205379b`.
Declaration: `8dff07b9ac7dfc3f099c97d98ee97cc5f69efb3a`.
Freeze: `ec149dc497b4de53ccb3e7a125baa226a66daaa7`.
Contract: `plans/round-75-claims.md` and `.ufo/waves/round-75/claims.json`.
Axes: operability (R75-C1, the A12 case set's independence and closure) and
calibration (R75-C2, the record audit's exact atom grammar).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| **A predicate that tests for a token's presence, not for the shape the token must have.** Two faces, one class: (a) the round-74 A12 cases fed values merely equal-ish to the sensitive ones — a real boolean for an `is True` identity check, one sample for a name that may carry several, an exact list for a key-list containment test — so three mutants survived a green selftest; (b) the round-74 audit's D9–D12 accepted four cosmetic constructions (a used-by cell that negates the path it names, a search-log line carrying the field names without the counts, an erratum with the two values reversed, a rejected row with no flip) — the round-74 wave demonstrated all four. | `corpus/lessons/round-74-verifier-spotcheck.md` §6 items 3 and 4; `.ufo/waves/round-74/pre/c1-base-arm.json` (6 survivors on the round-73 blob; the round-74 wave's hand mutations left the 20-case selftest green); `.ufo/waves/round-75/pre/c1-base-arm.json` (the four survivors on the round-74 blob) and its `b-drop-canary-field` two-case failure. | none before this round: no criterion said a case must feed the *distinguishing* input or that a detector must be sole. `QUALITY.md` rows 133 and 134 are added from this lesson. | Case inputs are chosen to differ in the field the mutation changes (identity values, duplicate names, superset key lists); the battery records `sole: failed == [expect_case]` per mutant and the claim requires the canary field to be sole; each atom grammar carries a red fixture in `record-audit.py --selftest`, so a cosmetic pass is shown failable before any record is scored. |

## Gate

All pages below were opened on **2026-11-04** with one fresh GET each (HTTP 200); snapshots,
byte counts and sha256s are in `.ufo/waves/round-75/w1/ScribeRows/`. Quotes are literal
excerpts with their snapshot line. Rows are written after the open, never before.

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S143, `re.fullmatch`, reused (opened round 47; not re-registered) | https://docs.python.org/3/library/re.html | 2026-11-04 (re-opened) | "Page fetched 2026-10-28 (HTTP 200, 257,706 bytes, sha256 f169ed06…); anchor `re.fullmatch(pattern, string, flags=0)`" (the row's own anchor cell) | The whole-string criterion the atom grammars use. **S283 was written for this page and withdrawn the same round: S143 already mines the same page for the same exact-match scope.** Ids are not reused, so S283 stays a gap. |
| S284, `os.path.commonpath`, admit (mined) | https://docs.python.org/3/library/os.path.html#os.path.commonpath | 2026-11-04 | "Return the longest common sub-path of each pathname in the iterable paths." (13 words; `os.path.commonpath` entry, snapshot line 291) | A valid common sub-path, not a string prefix; the containment predicates compose it with `realpath`. This is the round-74 SentinelScope SS74-1 escape class: the lexical version admitted `..`, absolute keys and symlink escapes. |
| S285, `environ(7)`, reject | https://man7.org/linux/man-pages/man7/environ.7.html | 2026-11-04 | "The variable environ points to an array of pointers to strings called the environment." (14 words; DESCRIPTION, snapshot line 75) | The page defines the C-level `environ` array, its `execve(2)` origin and `PR_SET_MM_ENV_START` relocation. It says nothing about `/proc/<pid>/cmdline`: `grep -c cmdline` on the snapshot prints 0. Flip: the page states the cmdline layout or mutability the argv claim needs. |
| S277, `proc_pid_cmdline(5)`, retrospective row (opened round 73, written this round) | https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html | 2026-11-04 (re-opened; first opened round 73) | "Think of this file as the command line that the process wants you to see." (16 words; DESCRIPTION, snapshot line 96) | Row `opened` is the FIRST opening date (round 73); this round only re-opened it and added a consumer. It grounds the argv-as-claim half of the entry; round 74 rejected S279–S282 because they were the umbrella, the boot-cmdline page, the directory overview and the index, not this leaf. |
| S275 used-by change (re-log of the round-74 edit, routed defect 2) | https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html | 2026-11-04 (value from `.ufo/waves/round-74/w1/ScribeRows.md`) | old: `corpus/knowledge/2026-11-04-r72-checker-env-capsule.md, .ufo/waves/round-72/w1/ScoutSource.md`; new: `corpus/knowledge/2026-11-04-r72-checker-env-capsule.md, .ufo/waves/round-72/w1/ScoutSource.md, corpus/knowledge/2026-11-04-r73-kernel-witness-record.md` | The old value was recorded only in the round-74 wave file; the contract requires the change logged in a round lesson. This row is that log; the registry cell itself is unchanged by round 75. |
| S277 used-by change (this round) | https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html | 2026-11-04 | old: `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md`; new: `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md, corpus/knowledge/2026-11-04-r75-a12-case-independence.md` | The round-75 entry cites S277 for the argv-as-claim boundary; the row's `used-by` gains it (append-only in-place field). |

**Convention (row `opened`).** A row's `opened` cell is the date the source was first opened by
this lane; a retrospective row names its opening round in the search log, so a same-date row is
not evidence of a fresh open.

Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exits 0 at the
round start (189 rows, 23 W04 warnings; `.ufo/waves/round-75/l1/census-start.txt`) and at the
round end (191 rows, 23 W04 warnings; `.ufo/waves/round-75/l1/census-end.txt`). Two rows enter
(S284 mined, S285 rejected), one candidate row (S283) is withdrawn as a duplicate of S143, and one
existing row's `used-by` changes (S277).

## What the wave found

- **ExecAuditGrammars** built six cosmetic fixtures that a token-presence predicate would accept
  (a negated path in the used-by list, a bare `x.md`, a search note carrying the field words but no
  integers, a rejection with no flip, a rejection whose reason and flip are one word, an erratum
  naming 23/24 while the measured count is 25). The exact grammar rejects all six, each with a
  defect naming the failed shape, and accepts the two well-formed fixtures — no blocking defect
  (`.ufo/waves/round-75/w1/ExecAuditGrammars.md`).
- **ReviewerClaims** re-derived R75-C1 end-to-end from frozen revisions and found no blocking
  defect: the two target pins match their blobs, the fifteen patch sites each occur exactly once,
  the renamed-case control is red for all seven closed names, and its independent runs of the
  frozen battery reproduce every count in the committed receipts. Its provenance finding (F1): the
  committed base receipt's `runner.sha256` is `d7757ae2…`, the *revised* battery disclosed as
  `ad53c1e1`, while the freeze pins `ec089411…`; the two differ only in the runner-binding block,
  so the receipt's runner field is honest about what executed but does not match the freeze pin.
  Recorded as a known skew, not repaired (re-generating it with the frozen blob would write a
  `null` runner and lose the binding the atom checks).
- **ExecProbeCases** hand-applied five mutants to a scratch copy of the round-74 blob (never
  running the battery): the four closed classes each leave `--selftest` green at 20 cases
  (survivors reproduced independently), and deleting the `canary_present` line fails exactly
  `a12-kernel-multiple-samples` and `a12-kernel-canary-field` — the cross-binding, reproduced by
  hand (`.ufo/waves/round-75/w1/ExecProbeCases.md`).
- **ExecBattery** re-ran both frozen arms at the frozen revisions: `r75probe` 0 survivors, sole
  true, pristine 25; `r75base` exactly the four survivors, canary not sole, pristine 20; both
  `--validate` clean and `--selftest` green (`.ufo/waves/round-75/w1/ExecBattery/receipt-A-r75probe.json`,
  `receipt-B-r75base.json`).
- **L1 determinism check.** Two independent battery runs at the tip (separate `--work` roots)
  produced identical mutant rows (`name, verdict, failed`) with pristine 25 and sole true; the
  receipt pair is `l1/scores/c1-at-tip.json` and `l1/scores/c1-at-tip-rerun.json`.
- **ScoutSource** re-opened both pages (fresh GETs, digests identical to the registry snapshots) and
  located eight passages on `proc_pid_cmdline(5)`: argv mutability, the zombie empty read, NUL
  separation, and the `PR_SET_MM_ARG_START` relocation. Its conclusion: the pages support the
  *boundary* halves of R75-C1 (argv is a claim; an unreadable/absent read is not evidence) and none
  of its predicate halves — the case-independence predicate rests on the lane's own battery, not on
  a man page. It also confirms the two `proc_pid_*` pages are one split family and that S275's cell
  already names the split (`.ufo/waves/round-75/w1/ScoutSource.md`).

## Routed-defect disposition (round-74 spot-check §6)

| # | routed defect | disposition |
|---|---|---|
| 1 | C2's `--validate` conjunct had no committed landing evidence | closed: the audit receipt carries its own `validate` block and a committed `c2-validate-at-landing.json` names the landing receipt (`D16`) |
| 2 | S275's used-by old→new was logged outside the lesson | closed: the Gate table above re-logs both values and names `.ufo/waves/round-74/w1/ScribeRows.md` (`D17`) |
| 3 | `b-drop-canary-field` was not killed by its case alone | closed: the multi-sample case no longer reads `canary_present`; the battery records `sole_detector` and the claim requires it (`D18`) |
| 4 | three further A12 survivors and four cosmetic atom passes | closed: the three classes are in the fifteen-class patch set (`D19`); the four grammars parse the cell and each carries a red fixture (`D20`) |
| 5 | D14/D15 coverage limits | closed: the base receipt binds the executed runner and the freeze pins equal the plan's exact tool set (`D21`); the ledger restates the round-73 standing debt beside the round-75 row |
| 6 | SentinelScope code items SS74-1/3/4/5 | closed in the instruments: containment before open, pin before execution, process-group cleanup, sidecar shims, no raw environment values (`D22`) |
| 7 | retrospective registry rows read as fresh opens | closed: the search log states the row-`opened` convention and the Gate table follows it (`D23`) |
| 8 | report rounding 4/15 = 27% | cosmetic, corrected in the round-75 report (28.6%); not atomised, by reason |
