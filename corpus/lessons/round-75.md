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
| S283, `re.fullmatch`, admit (mined) | https://docs.python.org/3/library/re.html#re.fullmatch | 2026-11-04 | "If the whole string matches the regular expression pattern, return a corresponding Match." (15 words; `re.fullmatch` entry, snapshot line 1152) | Whole-string matching is the difference between a value that contains a matching substring and a value that *is* the shape. The atom grammars parse the whole cell (`^…$`-anchored patterns over stripped cells); the round-74 cosmetic passes were values that contained the token. |
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
round end (191 rows; `.ufo/waves/round-75/l1/census-end.txt`). Three rows enter (S283 and S284
mined, S285 rejected) and one existing row's `used-by` changes.

## What the wave found

(to be completed after the wave settles)
