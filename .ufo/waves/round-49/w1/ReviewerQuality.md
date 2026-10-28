# ReviewerQuality — round 49 wave 1 (pre-freeze), QUALITY-bar review

Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Scope: the knowledge-entry draft (`R49EntryDraft`), the S147/S148 rows that `c2-after.py` writes, the C1 landing blocks (`R49C1Doc`), the round-49 lesson draft, and the draft C2 counter, each measured against `corpus/QUALITY.md` rows 70–79 and the rows that bind an entry, a SOURCES row and a lesson. Nothing in the lane tree was written. Work lived in `/fast/scratch/hyaku/kaidoku-r49/ReviewerQuality/` (removed before yield after receipts were copied).

## Verdict

**Not freeze-ready as drafted.** The C2 counter and its battery are sound at the dev-after state (green, 11/11 mutations red, freeze reads 9). The problems are in the text and the quote check around them:

1. The knowledge entry is a round-44 copy. Its status header names the round-44 freeze commit as "the round-49 freeze", carries the round-44 counter sha256 and round-44 scores, and cites a dead commit hash. It is not landable.
2. The two new SOURCES quotes (S147, S148) are not contiguous in the served bytes. The C2 counter accepts them anyway, because it compares after tag-stripping and whitespace-collapsing, and it has no `composite` check. Row 42 rejects exactly this.
3. The reversal pointers are one-way (row 35/36). S145 and S146 do not name S147/S148; the admitting rows name the rejected rows by id only, not by path and line.
4. The C1 landing omits the S138/S139 `used-by` edit that `c1-counter.py` requires (`:30`, `:190`). The entry and the plan call S138/S139 "re-opened this round", but no round-49 capture exists; they are round-44 fetches.
5. The lesson draft has no `## Gate` section, which the plan and row 45 both reference. M49-1 is recorded nowhere in a lesson draft. Proposed row 88 for M49-1 is in `w1/ReviewerQuality/proposed-row-88.md`.

Top three findings: F1 (entry is a round-44 copy with a dead hash and round-44 numbers), F3 (quote check green on what row 42 forbids), F4 (one-way reversal pointers). Report: `.ufo/waves/round-49/w1/ReviewerQuality.md`.

## Findings

Severity: B = blocks freeze/landing; M = must fix before landing; m = minor. Commands run from the lane root unless stated; scratch clone `/fast/scratch/hyaku/kaidoku-r49/ReviewerQuality/clone` built by `mkclone.sh` (DEV_FREEZE `add33972a19820f80d2287e3c865d9beea487f46`), with `c2-after.py` (DEV_AFTER `50a3d699cba5f594d6b266b18b166daab612f03b`). Times are sandbox clock 2026-10-28 (~18:10–18:15 -03:00).

| ID | Sev | Criteria | Finding | Evidence (command → exit, sha256) | Fix |
|---|---|---|---|---|---|
| F1 | B | 4, 6, 8, 10, 18, 34 (no fabricated output) | Entry `2026-10-28-r49-squashfs-v1v2-core.md` is a round-44 copy. (a) Header: "scored … against the round-49 freeze `c48f8a4bfd…`" — `git log -1 c48f8a4…` is `round-44: freeze C1/C2 claims, carriers, counters, and controls` (2026-10-28T09:35:19-03:00), an ancestor of base. (b) "counter sha256 `9f2cc140…`" — equals `counter_sha256` in `git show e4f2cfa5:.ufo/waves/round-44/controls/pos/counter.json`; the draft `c1-counter.py` sha is `d6d70cb7…`. (c) "revision `6b58a898…`" — `git cat-file -t 6b58a898` → `fatal: Not a valid object name` (dead hash, the round-48 A2 class). (d) `carriers_matched 4/4`, `met_target true`, `exit 0`, `failing []` are pre-data numbers from round 44. Also cites round-44 receipts as the round-49 scored run (the plan's CTL-C1-4 shortcut). | `sha256sum .ufo/waves/round-49/draft/tools/round-49/c1-counter.py` → `d6d70cb7ecc789b5…`; `git show e4f2cfa5…:.ufo/waves/round-44/controls/pos/counter.json \| grep -o '"counter_sha256"…'` → `9f2cc140e1fa7875…`; `git cat-file -t 6b58a898` → fatal (exit 128) | Rewrite the header from the post-data round-49 `after.json`/counter receipt only; delete every round-44 number and hash; add a counter/landing check that every 40-hex hash in the entry resolves via `git cat-file -t` and that the counter sha equals `sha256(c1-counter.py)` at FREEZE. |
| F2 | M | 18 (no floating "this round"; name historical round/date) | Entry says "(round 44, Core)" in the title, "Round 44 adds the `## Round-49 additions to Core` row", "Before this round", "this round's digest census" (occurrences at lines 1, 20, 21, 123, 194, 200, 212). `R49C1Doc/block-c` README row is labelled "SquashFS v1/v2 through REA (round 44)" beside stem `2026-10-28-r49-…`. | `grep -n -o -i -E 'this round\|round 44' …/2026-10-28-r49-squashfs-v1v2-core.md` → 7+ hits; block-c line 1 | Replace each with the dated round-49 wording or the round-44 date it really refers to. |
| F3 | B | 42 (`## Gate`/quote contiguous, composite label), 17 (manual check under #1), 79 (predicate reads the field it claims) | S147 quote ("falsifiability as his criterion … it is scientific") and S148 quote ("The command was used incorrectly … or whatever.") are **not** contiguous in the served bytes. popper.html: `<em>falsifiability</em> as` then newline then `his criterion … if a theory is` / newline / `incompatible …`. sysexits.html: `…with the wrong` newline `number of arguments, …`. Neither carries a `composite` label (`grep -c composite` on the entry = 0; `c2-mismatch.py` has no `composite` token). The counter's A6/A7 quote check uses `html_norm` (strip tags + collapse whitespace, `c2-mismatch.py:197–207`, quote test at `:395–402`) and so **accepts** the quote. | `grep -c -F "falsifiability as his criterion" corpus/evidence/round-49/c2/popper.html` (scratch clone) → `0`, exit 1; same on `sysexits.html` for "The command was used incorrectly, e.g., with the wrong number" → `0`; `tr -s` whitespace collapse then grep → `0`, exit 1; after tag strip → present. `c2-after-battery.txt` sha256 `e1e3842a…`: A6 `ok true`. | Label both quotes `composite` in S147/S148 (both cross markup or line wrap). Make the counter red on an unlabelled quote that is not a raw contiguous run, and add that forgery (`unlabelled-composite-quote`) to the battery; a forgery that differs only in whitespace or tags is not a forgery of the bytes. |
| F4 | M | 35, 36 (reversal traceable both ways), 42 | Reversal pointers are one-way. S145 status `mined`, used-by `corpus/lessons/round-48.md`; S146 `rejected`, used-by `—`. Neither names S147/S148. S147 and S148 name the rejected row by id ("supersedes S145/S146") and not by path and line (`corpus/SOURCES.md:151`, `:152`). Lesson corrections say `A6 row=S147`, `A7 row=S148` with no path/line of the rejected rows. Row 36 requires the reversing lesson and the admitting anchor cell to name the rejected decision by path and line. | `git show e4f2cfa5:corpus/SOURCES.md \| awk -F'\|' '$2 ~ /S145\|S146/'` → S145 `mined` / used-by round-48; S146 `rejected` / `—`. Scratch clone diff of `corpus/SOURCES.md` (`git diff HEAD~1 HEAD`) touches only insertion of S147/S148 and the search log. | Add a `superseded-by S147 (corpus/SOURCES.md:<line>)` pointer on S145, `…S148` on S146 (S146 is outside the "rejected" flip clause, so state the flip). Put path and line in S147/S148 anchor cells and in the lesson corrections. Note S147's correction is itself right: the quote sits at `popper.html` line 388, under §2 "Backdrop" (heading line 319); §3 starts at line 400. S145's "§2 The Problem of Demarcation" is wrong. |
| F5 | B | 1, 29 (source line → used-by), 44 (pre-seen items named), 45 (scope of "new") | C1 needs S138/S139 `used-by` to list the r49 entry (`c1-counter.py:30`, `:190` "entry (path or stem) in used-by"). Base `used-by` for both is only `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`. No landing block edits `corpus/SOURCES.md` S138/S139 (`R49C1Doc/` has only PROVINCE A, PROVINCE B, README C). The entry and the plan say "re-opened this round", but there is no round-49 fetch artifact for S138/S139; the cited evidence is the round-44 oracle manifest (`corpus/evidence/round-44/oracle/manifest.json`). | `git show e4f2cfa5:corpus/SOURCES.md \| awk -F'|' '$2 ~ /S138\|S139/ {print $2, $NF-1}'` → used-by r44 only. `ls .ufo/waves/round-49/w1/artifacts/R49C1Doc/` → 3 files, none SOURCES. | Add the S138/S139 `used-by` landing edit to the C1 landing list. Either re-open S138/S139 in round 49 with a receipt (then the claim may say "re-opened") or say "round-44 fetch, opened 2026-10-28" everywhere the word "re-opened" appears. |
| F6 | M | 34 (placeholders), 18 | `<AFTER-DATA: …>` placeholder markers in `R49C1Doc/block-a` line 5 and `block-c` line 1. The plan has no check that they are gone at landing. | `grep -n -o 'AFTER-DATA[^>]*' .ufo/waves/round-49/w1/artifacts/R49C1Doc/*.md` → 2 hits. | Add a landing gate: `grep -c AFTER-DATA` over `corpus/` and `PROVINCE.md` must be 0 (exit 1 on any hit). |
| F7 | M | 73 (receipt states what produced it) | Plan's receipt fields are exit code, stdout sha256, counter sha256. No argv, no UTC instant, no reader digest (unblob, sasquatch, unsquashfs) in the counter receipt fields named in the plan. `c1-controls.py:555` does record argv/exit/wall for the control runs. | Plan text, "Every receipt records exit code, stdout sha256 and counter sha256." | Add argv, UTC instant (`utc_start`), and sha256 of the reader binaries to the counter receipt, or mark them `caller_asserted`. |
| F8 | M | 71 (gate mutants scored on triple `(exit, verdict, over-set name)`) | C1 red controls assert `exit non-zero` plus `carriers_matched 0`, and at most one named flag (`failing_includes ['projection_ok']`, `c1-controls.py:716–717`). They do not assert the full failing-binding set, so an over-target reader that flips a different binding is not caught by name. | `sed -n '714,720p' .ufo/waves/round-49/draft/tools/round-49/c1-controls.py` | Assert the full failing-binding set by equality on the control's expected set, and the verdict string, for CTL-C1-0..5. |
| F9 | M | 74 (registry edit verified by row count AND per-status tallies AND anchor re-read) | C2 checks S145–S148 per row (`c2-mismatch.py:371`, `:378`) and S145 against base (`:360–366`). No per-status tally of the whole registry against the base blob, so a landing that alters another row's status (or swaps rows) is not seen. The plan says SOURCES is not frozen. | `grep -n 'base_rows\|tally' .ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py` → `base_rows` used only for S145. | Add a tally check: per-status counts at REV equal base counts plus exactly {S147: mined, S148: mined}, and every other row byte-identical to base. |
| F10 | M | 22 (seat status: cutoff + per-seat cause), 76 | Lesson correction A4 reads `seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers` with no observation cutoff and no retained per-seat cause line. The C2 battery checks the arithmetic only. | `c2-after-battery.txt` A4 mutation red (arithmetic); no cutoff or cause text in the draft lesson. | Add the cutoff instant and a per-missing-seat cause line (terminal error or result pointer, or `cause unknown` with what was tried). |
| F11 | M | 80 (control generators land in the freeze commit) | `c2-after.py` builds the GREEN C2 fixture; it sits in `draft/`, outside `tools/round-49/`, and is not in the plan's frozen-path list. The green fixture is therefore not reproducible from FREEZE. It is also authored by the same seat as the counter (row 28 spirit). | `git -C <dev-after> show --stat HEAD` → touches SCORECARD, lessons, SOURCES, evidence c2 (generator not in tree). | Either freeze `c2-after.py` with the counter, or state that it is dev-only and that no receipt cites its output. |
| F12 | m | 44/45 | S147/S148 cite `plato.stanford.edu` and `man7` URLs with `accessed 2026-10-28` and sha; no HTTP status or byte count recorded (S145 also lacks them). | S147/S148 cells. | Add HTTP status and byte count, as the S138 row does. |
| F13 | M | 36 (lesson Gate) | The round-49 lesson draft (`clone/corpus/lessons/round-49.md`, written by `c2-after.py`) has no `## Gate` section (`grep -c '## Gate'` → 0). The plan says C1's access dates live in `## Gate`, and row 45 requires the new row to be listed there. M49-1 is not recorded. | `grep -c '## Gate' clone/corpus/lessons/round-49.md` → `0`. | Draft the real lesson with `## Gate` (access dates, quotes with locators), `## Mistakes` (M49-1), and the A1–A9 corrections. |
| F14 | m | 1 (source consistency) | PROVINCE block-a cites S108 (`:101–102`, `:158–159`, `:24–26`, `:51–54`, `:68–69`) and the entry cites S112 (`:24–69`, `:101–155`, `:158–196`) for the same unblob 26.6.4 squashfs.py. Two rows, one file; neither `used-by` names the r49 entry. | `git show e4f2cfa5:corpus/SOURCES.md` rows S108, S112. | Cite one row id per file, and add the r49 entry to its `used-by`. |

## Criteria applied (rows that bind a new entry, a SOURCES row, a lesson; plus rows 70–79)

Status key: MET / PARTIAL / UNMET / N-A. "Draft" = the drafts as written. Row numbers are QUALITY rows.

| Row | Binds | Draft | Note |
|---|---|---|---|
| 1 resolvable source | entry, S147/S148, lesson | PARTIAL | URLs and sha256 resolve (below); no fetch receipt; S138/S139 "re-opened" unsupported (F5). |
| 4 artifact identity | entry | UNMET | Counter sha and freeze in header are round-44 values (F1). Carrier sha/size table is correct (MET for carriers). |
| 5 observation/inference/unknown | entry | MET | Observed / Inferred / Unknown sections present. |
| 6 REA claim cites Evidence ID or reproducing call | entry | UNMET pre-data | Cites round-44 receipts; round-49 after-receipts do not exist yet. Must be the post-data receipts. |
| 7 what was not examined | entry | MET | Limits section (4 fixtures, no symlink/device/fragment, same-lineage unblob tree). |
| 8 pins versions | entry, PROVINCE | MET | rea-agents 6.5.0, unblob 26.6.4, sasquatch 4.5.1, unsquashfs 4.7.5 named. The counter pin is wrong (F1). |
| 10 held/works | entry | UNMET pre-data | "works through REA on these bytes" rests on round-44 measurement. Admit only from round-49 after-receipts. |
| 11 zero findings state | entry | PARTIAL | "gaps none", "extra_published []" are round-44 observations; restate as round-49 receipt results. |
| 12 synthesized carriers pinned | entry | MET | Four fixtures pinned by sha256 and size. |
| 16/17 quote fidelity, manual check under #1 | S147/S148, lesson Gate | UNMET | HTML-rendered quotes not contiguous; manual check fails (F3). |
| 18 execution evidence; no floating "this round" | entry, block-c | UNMET | Floating "this round" and "round 44" labels (F2); execution evidence is round-44's. |
| 22 seat status cutoff and cause | lesson A4 | UNMET | No cutoff, no per-seat cause (F10). |
| 23 evidence timestamps | corpus/evidence/round-49 | MET (tree) | `evidence-timestamps.py --strict` exit 0, `files_scanned 2`, `skipped []`. Entry not in scanned tree; "not run" for entry. |
| 29 source line → used-by | entry → S138/S139 | UNMET in landing | used-by lacks the r49 entry; no landing edit (F5). |
| 35/36 reversal, both ways, path and line | S145/S146/S147/S148, lesson | UNMET | One-way pointers, id-only (F4). The S147 correction itself is right. |
| 42 `## Gate` quote, contiguous, composite | S147/S148, lesson Gate | UNMET | Two quotes cross markup or wrap; no `composite` label (F3). |
| 44 pre-seen items | C1 carriers, entry | PARTIAL | Plan discloses "not new data"; entry says "re-opened this round" (F5). |
| 45 claim_row (new row) | C1 | N-A | S138/S139 are base rows, not new; no claim_row needed. Plan's "re-opened" wording is the defect (F5). |
| 70 class set equality | C1 carriers | PARTIAL | Count equality (`c1-counter.py:901–902`, `len(ids)!=target`) and carrier sha pins (`:916–930`) present. Id-name equality to the four frozen ids: not verified in full by this seat. |
| 71 triple scoring | C1 controls | PARTIAL | Exit plus `carriers_matched` plus one flag; no full failing-binding set (F8). |
| 72 cross-check own claim | C1 counter receipt | not verified | `met_target` appears 5 times in `c1-counter.py`; the `met == (matched == target)` cross-check was not traced by this seat. |
| 73 receipt provenance | C1 receipts | PARTIAL | argv/exit/wall in controls; no UTC instant or reader digests (F7). |
| 74 registry edit tallies | SOURCES | PARTIAL | Per-row checks only (F9). |
| 77 enumerate every occurrence | C2 search-log, pins | not fully verified | `re.findall` used for pins (`c2-mismatch.py:378`); search-log checks per entry (`:455–456`). |
| 78 fullmatch, forgery differs in named dimension | C2 | MET | `HEX40.fullmatch` at `:251`, `:265`; do-nothing overlay red 9/9 over 5 paths. The quote forgery is missing (F3). |
| 79 predicate reads the candidate; battery exercises green | C2 | MET at dev-after | Green dev-after: exit 0, mismatches 0; 11/11 mutations red with `noop []`; freeze: exit 1, mismatches 9. Quote field A6 reads the tag-stripped text (F3). |
| 80 control generator in freeze | C2 green fixture | UNMET as planned | `c2-after.py` outside freeze (F11). |
| 81 pointer repair bound to intended doc | S145→S147 | PARTIAL | A6 pins the snapshot sha in the row (`:380`) — MET for sha; quote part UNMET (F3). |
| 83/84 dry run on sandbox clone | C1, C2 | PARTIAL | C2 dry-run done here (dev-after / freeze). C1 end-to-end dry run not run by this seat. |
| 87 claim prose the instrument implements | C1 | not in scope | Covered by the C1 seat. |

## Positive checks (for the record)

- Snapshot sha256 match the S145/S147 and S148 pins: `popper.html` `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`; `sysexits.html` `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` (both `sha256sum`, exit 0).
- S147's section correction is right: quote at `popper.html` line 388 under §2 "Backdrop to Popper's Thought" (heading line 319), §3 at line 400.
- S148's `EX_USAGE 64` claim is in the page: `sysexits.html` line 80 `#define EX_USAGE 64`.
- `c2-mismatch.py` at dev-after: exit 0, `mismatches 0`, `atoms_total 9`, battery `failing []`, 11 mutations each `red == [atom]`, `noop []`, do-nothing red 9 of 9 over 5 paths.
- `c2-mismatch.py` at freeze (`--rev` = FREEZE, no battery): exit 1, `mismatches 9`.
- Evidence-timestamp check on `corpus/evidence/round-49` at dev-after: exit 0, `finding_count 0`.
- C1 PROVINCE block-a heading `## Round-49 additions to Core` follows the existing Core-addition table convention (`## Round-42 additions to Core` at PROVINCE.md:410), which satisfies row 54 on placement.

## Commands, exit codes, receipts

| Command (scratch clone, DEV_FREEZE `add33972…`, DEV_AFTER `50a3d699…`) | Exit | stdout sha256 | Receipt |
|---|---|---|---|
| `python3 -I -B tools/round-49/c2-mismatch.py --root <clone> --rev 50a3d699… --freeze add33972… --battery` | 0 | `e1e3842a095357ea16880dfa641b5a9b45f7383c413297a6ea735ed3d1554e2f` | `w1/ReviewerQuality/c2-after-battery.txt` |
| `python3 -I -B tools/round-49/c2-mismatch.py --root <clone> --rev add33972… --freeze add33972…` | 1 | `ced5b8c94fb3b3c9c5c7aaebbdf56f464adb452d22d8e32ab56ba67889a7d63e` | `w1/ReviewerQuality/c2-freeze.txt` |
| `python3 -I -B tools/round-49/c2-mismatch.py --root <clone> --rev 50a3d699… --freeze add33972…` | 0 | `82f768ced16e84809aa1b79917615accd88575e6868a91ebd2e64757dfff19c1` | `w1/ReviewerQuality/c2-after-nobattery.txt` |
| `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py --root <clone> --rev 50a3d699… --path corpus/evidence/round-49 --strict` | 0 | not recorded | stdout `finding_count 0`, `files_scanned 2`, `files_skipped 0` |
| `grep -c -F "falsifiability as his criterion" corpus/evidence/round-49/c2/popper.html` | 1 (count 0) | — | raw bytes |
| `git cat-file -t 6b58a898` | 128 | — | `fatal: Not a valid object name` |
| `git log -1 c48f8a4bfd449300c975668e59aae5b5538b6a84` | 0 | — | `round-44: freeze C1/C2 claims, carriers, counters, and controls` |
| `sha256sum .ufo/waves/round-49/draft/snapshots/*` | 0 | `2c2d48c6…` (popper), `d9db4b96…` (sysexits) | snapshot pins |
| `sha256sum .ufo/waves/round-49/draft/tools/round-49/c1-counter.py` | 0 | `d6d70cb7ecc789b5ceb7ee5b656abeea395cea9a158249d9a4723a95779` | — |
| `git show e4f2cfa5…:.ufo/waves/round-44/controls/pos/counter.json` (counter_sha256) | 0 | `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993` | round-44 counter |

Tools installed: none. Channels considered: none needed (python3, git, grep, sha256sum were present).

Not run: C1 counter (`c1-counter.py`) and controls (`c1-controls.py`); any `--data-run`; `c1-run.sh`; the full `met_target` cross-check (row 72) and the full class-id equality (row 70) — left to the C1 seat.

## Proposed QUALITY row 88 (M49-1, reference-drift)

Full text in `.ufo/waves/round-49/w1/ReviewerQuality/proposed-row-88.md`. Summary: a lesson's declared-freeze line must name the SCORECARD's declared commit and that commit must be the first claim-file commit; amendments are dated correction lines; a counter's freeze check must be proven by a swap mutation red with no no-op (the C2 atom A1 and its battery mutation `A1 swap declared/stale`). Captured-by: none (rows 33, 55, 66, 68 bind pins and predicates, not a lesson's prose header). Supersedes none; sharpens 33, 68, 79.

## Cleanup

Scratch `/fast/scratch/hyaku/kaidoku-r49/ReviewerQuality/` removed after the receipts were copied into `.ufo/waves/round-49/w1/ReviewerQuality/`. No lane file, no git mutation, no fleet-repo write.
