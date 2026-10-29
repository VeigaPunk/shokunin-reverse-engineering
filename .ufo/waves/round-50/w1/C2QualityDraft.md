# C2QualityDraft — round 50 wave 1 (pre-freeze) — QUALITY draft rows from the round-49 closure

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Read-only on the lane tree; all writes under `.ufo/waves/round-50/w1/C2QualityDraft/` and this file. No git mutation, no tool installed (python3 stdlib, `git show`/`ls-tree`/`grep` only). Scratch `/fast/scratch/hyaku/kaidoku-r50/C2QualityDraft` removed after receipts were written; the snapshots it held are lane-committed bytes (sha256 below), so every receipt re-reads them from the base commit.

## Verdict

**Draft rows 90–93 ready for the L1, row 94 optional; the draft locator/registry probe passes its own 8 red/green arms; the closure's claims are checked and three of them are wrong or stale.** Paste-ready text: `.ufo/waves/round-50/w1/C2QualityDraft/draft-quality-rows.md`. Free row numbers at base: 90–94 (`corpus/QUALITY.md` ends at row 89; `grep -c '^| 90 '` = 0).

Plan-affecting findings (fold before the single freeze):
1. **The plan's B6 and the closure both say "FreeBSD is the origin of sysexits". The two snapshots say otherwise** (FreeBSD HISTORY: "The sysexits file first appeared in 4BSD."; man7 HISTORY: "...appeared in 4.0BSD for use by the deliverymail utility"). A B6 correction text that repeats "FreeBSD is the origin" would encode a false provenance fact.
2. **The closure's "rounds 46–48 counters are likewise unregistered" is wrong at its own tip and at base.** 8 of the 9 round-46–48 counter files have registry rows; only `tools/round-48/census2.py` has none. The real registry gap is the six `tools/round-49/*.py|sh` files (the closure named three) plus `census2.py`; rounds 42–44 add eight more pre-existing gaps. B9 should census from `git ls-tree`, not from the closure's list.
3. **None of the three routed row defects has a correction row at base.** `grep -c 'supersedes S149|S138|S147'` at `corpus/SOURCES.md` = 0 each; the only supersedes cells are S145 and S146. The next unused source id is S150 (rows end at S149).

## Findings table

Exit codes: 0 met, 1 not met, 2 could-not-evaluate. Every stdout is in `receipts.txt` with its command and UTC time. Probe `tools/round-50/c2q-probe.py` sha256 `7aa551f0c6fb903cfd7030ce8ffaceeb1334962f2afdc8dd38d5f5ccbfac700a`; `receipts.txt` sha256 `ff10c4bed62cff57ecb4bca3cb8bc448a67880bbe7667e8722918a80a2f5cc0c`; `draft-quality-rows.md` sha256 `e6017ed44b67fd853c372d2b56ec6e82a4e34d453bb7c6cbfe6cc349756bd9c2`.

| # | check | command (abridged; full argv in receipts.txt) | exit | observed | sha256 / evidence |
|---|---|---|---|---|---|
| F-a | probe selftest, 8 arms (committed snapshots at REV, registry synthetic) | `python3 -I -B c2q-probe.py selftest --root <lane> --rev 7c678ae6…` | 0 | 8/8 arms as expected | stdout sha `c99d2b5a…` |
| F-b | S147 locator green | `locator --snapshot popper.html --quote "falsifiability as his criterion …scientific" --anchor "2. Backdrop to Popper’s Thought"` | 0 | nearest heading `2. Backdrop to Popper’s Thought` | popper.html `2c2d48c6…ec207` = row sha |
| F-c | S147 quote 2 contiguous under the same heading | `locator … --quote "it is consistent with all possible observations, is unscientific"` | 0 | contiguous clause tail under §2 | same |
| F-d | S145 locator (superseded by S147) | `locator … --anchor "2. The Problem of Demarcation"` | 1 | nearest `2. Backdrop…`; the §3 locator is wrong | same |
| F-e | S149 locator as landed (anchor `DESCRIPTION`) | `locator --snapshot freebsd-sysexits.html --quote "EX_USAGE (64) The command was used incorrectly" --anchor DESCRIPTION` | 1 | nearest `ERRORS` (a plain-text man label, not an `<hN>`) | freebsd-sysexits.html `1fc793a2…5dbf` = row sha |
| F-f | S149 locator corrected to `ERRORS` | same, `--anchor ERRORS` | 0 | nearest `ERRORS` | same |
| F-g | S148 locator `SYNOPSIS` | `locator --snapshot sysexits.html --quote "#define EX_USAGE 64 /* command line usage error */" --anchor SYNOPSIS` | 0 | nearest `SYNOPSIS` (`SYNOPSIS top` normalised) | sysexits.html `d9db4b96…340` = row sha |
| F-h | S148 locator `DESCRIPTION` (control) | same, `--anchor DESCRIPTION` | 1 | nearest `SYNOPSIS` | same |
| F-i | fabricated quote | `locator … --quote "…politely"` | 2 | quote not found | selftest arm |
| F-j | registry, round 49 | `registry --root <lane> --rev 7c678ae6… --min-round 49` | 1 | 0 of 6 `tools/round-49/*.py\|sh` registered (`c1-controls.py`, `c1-counter.py`, `c1-oracle.py`, `c1-run.py`, `c1-run.sh`, `c2-mismatch.py`) | row 92 red-before |
| F-k | registry, rounds 46–48 | `registry … --min-round 46` | 1 | 8 of 15 registered; unregistered: `tools/round-48/census2.py` + the six round-49 files | closure claim contradicted |
| F-l | registry, rounds 41+ | `registry … --min-round 41` | 1 | 42 of 57 registered; unregistered 15 (rounds 42–44 eight files; 48 `census2.py`; 49 six) | — |
| F-m | registry at closure tip `623476eef55640258fa5d4ff95a87ba59c49279f`, names 46–48 | `python3 -I -B` import of `skill_registry_paths` over `git show 623476ee:SKILL.md` | 0 | 8 of 9 round-46–48 files have rows at the tip too; `census2.py` none | SKILL.md at tip = base, sha `04a3a865…0b132e` |
| F-n | `supersedes` cells at base | `git show 7c678ae6:corpus/SOURCES.md \| grep -c 'supersedes S149'` (and S138, S147) | 0 (count) | 0, 0, 0; `supersedes S145 —` and `supersedes S146 —` only | SOURCES.md `ae3c1e17…c11` (255 lines) |
| F-o | QUALITY row 90 free at base | `git show 7c678ae6:corpus/QUALITY.md \| grep -c '^| 90 '` | 0 (count) | 0; last row 89 | QUALITY.md `8ada85c4…3fb5d` |
| F-p | FreeBSD HISTORY attribution | `python3` text extraction of `freebsd-sysexits.html` around `HISTORY` | — | "The sysexits file first appeared in 4BSD. AUTHORS This manual page was written by Jorg Wunsch." | sha `1fc793a2…5dbf` |
| F-q | man7 HISTORY attribution | `python3` text extraction (tags stripped, whitespace collapsed) of `sysexits.html` around `CAVEATS`/`HISTORY` | — | "file appeared in 4.0BSD for use by the deliverymail utility, later renamed to sendmail(8)" | sha `d9db4b96…340` |
| F-r | CORPUS tier text | `sed -n 93,98p` of fleet `CORPUS.md` | — | A = primary/authoritative (spec, official docs, source code, original paper, maintainer statement, own re-runnable output); B = strong secondary (expert write-up, survey, textbook); C = lead only; `community` never A | fleet `CORPUS.md` (not hashed; fleet root file) |
| F-s | correction-row rule | `CORPUS.md` `### Rules` 2; `tools/round-38/registry-immutable.sh` present at base | — | "A correction is a new row whose `teaches` opens `supersedes S0NN —`" | gate present at base (`git ls-tree`) |
| F-t | lesson files at base | `git show 7c678ae6:corpus/lessons/round-49-verifier-spotcheck.md \| sha256sum` / `round-49.md` | — | — | `9b7ff596…57b39` / `4380b37f…39a2a` |
| F-u | round-49 S147 quote 2 | snapshot text check | 0 | the closure's "cuts across a clause" is not a splice: the nine-word tail is contiguous in the snapshot, sitting in a list ("…as in the case of psychoanalytic theories, it is consistent with all possible observations, is unscientific") | popper.html `2c2d48c6…` |

## Per-item answers to the assignment

(a) **Tier, provenance, locator.** Tier: S147 (SEP, an expert encyclopedia entry on Popper) is **B** by the CORPUS text's "survey"/"expert write-up" clause; the closure's disagreement with the lane's tier A is correct (F-r). S148 (a man7 page) is contestable: CORPUS A lists "official docs" and "maintainer statement", and man7 republishes the Linux man-pages project's own page, so the closure's "CORPUS puts the Linux man page at B" is not forced by the text. The draft row 90 requires the category to be named, so the L1 decides S148 with the category written, not by analogy. Provenance direction: the origin is 4BSD / 4.0BSD by both snapshots' HISTORY text (F-p, F-q); neither FreeBSD nor man7 is the origin, and S149's "second mirror of S148" wording does not name the origin. Locator: S147's locator is correct (F-b, F-c); S145's `§3` locator is wrong (F-d); S149's anchor `DESCRIPTION` is wrong, the quote sits under `ERRORS` (F-e). Man pages carry their section headings as plain text, so a locator check that reads only `<hN>` elements misses the S149 case; the draft probe reads the man labels too.

(b) **Counter registry at landing.** Draft row 92. Red-before is F-j (0 of 6 round-49 files registered at base) and F-l. The PROTOCOL §Registry and §Delivery clauses already require the row; no QUALITY row asks for it at landing (M50-2 `landing`).

(c) **Correction rows are new rows, not in-place edits.** The rule already exists, but not as a QUALITY row: the fleet `CORPUS.md` `### Rules` 2 says "A correction is a new row whose `teaches` opens `supersedes S0NN —`", and `tools/round-38/registry-immutable.sh` checks that a base row changes only in `status`, `recheck`, `used-by`. QUALITY.md's header (lines 4–5) makes the same rule for criteria, and rows 35–36 cover reversals. So the rule is row-less in QUALITY; draft row 93 adds only the closure consequence (a routed defect closes by a `supersedes` row), with red-before F-n.

## Draft rows (paste-ready, in `draft-quality-rows.md`)

- **90** tier by the category CORPUS.md's tier text assigns; `## Gate` names the category. Red-before: S147 `docs | A`. Reviewer-checked (judgement), disclosed as such.
- **91** locator names the nearest preceding heading or man-page label in the committed snapshot; a mirror's origin comes from the origin's own attribution sentence. Red-before: F-d, F-e, F-p, F-q. Sharpens 16 and 42.
- **92** a counter lands with its registry row in the same commit or before filing; the census covers every round. Red-before: F-j, F-k, F-l. Sharpens 61 and the PROTOCOL Delivery clause.
- **93** a routed registry defect closes only by a new `supersedes S0NN —` row. Red-before: F-n. Sharpens 35–36 and restates CORPUS Rule 2.
- **94** (optional) a `teaches` cell claims no wider than its located quote or cited receipt; red-before S138 (`teaches` six-carrier agreement; scope 22-member census; located quotes name a listing element and a `<title>`). Judged by non-author review.

## Limits of this seat's work

- The probe is a draft. Its registry check reads cell-0 paths only and does not verify the verdict map or the self-test spelling (the row content). Its locator uses a fixed vocabulary of 20 man-page labels and fails closed on unknown layouts (exit 1 on a mismatch, exit 2 on a missing quote); a heading vocabulary the probe does not know would be a false exit 1 and must be re-checked on the four round-49 snapshots before freeze.
- Row 90's category is a judgement; no counter enforces it.
- I did not open the S147/S148/S149 sources on the live web; every check is on the committed snapshots, whose sha256 match the rows (F-b to F-q).
- I did not verify the plan's other atoms (B1–B5, B10, B11) or the round-50 counters; they belong to other seats.

## Calibration note for the L1

The round-49 closure is right on S147 tier, S149 reason and anchor, S138 scope, and the missing QUALITY criterion. It is wrong on the S149 origin ("FreeBSD is the origin"), wrong that rounds 46–48 are unregistered, and under-counts the unregistered round-49 counters (three named, six present). Its S147 quote-2 complaint ("cuts across a clause") does not hold. These are reported as findings, not as closure defects.

## Artifacts

- `.ufo/waves/round-50/w1/C2QualityDraft/tools/round-50/c2q-probe.py` (draft probe; `selftest`, `registry`, `locator`)
- `.ufo/waves/round-50/w1/C2QualityDraft/receipts.txt` (every command, exit, stdout sha256, UTC)
- `.ufo/waves/round-50/w1/C2QualityDraft/draft-quality-rows.md` (paste-ready rows 90–94)

Installs or upgrades: none.
