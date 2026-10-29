# C2MistakeScribe — round 50, wave 1 (pre-freeze), mistake mining

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Read-only on the lane; all git calls were `show`, `ls-tree`, `cat-file`. Instruments and receipts: `.ufo/waves/round-50/w1/C2MistakeScribe/` (`tools/round-50/`, `receipts/INDEX.tsv`). Draft rows: `.ufo/waves/round-50/w1/C2MistakeScribe/round-50-mistakes-draft.md`.

## Verdict

The three candidates hold in substance, but two are mis-stated in the round-49 closure and lesson, and the closure carries one false premise of its own. Folding these before the freeze matters: C2's atoms B6–B9 (S149, S147, S138, registry census) would otherwise freeze the closure's wording rather than the bytes.

1. **M50-1 (attribution/scope) — confirmed, with corrections.** The S149 locator is wrong at base (anchor `DESCRIPTION`, quote under `ERRORS`). The S149 provenance inversion is not established by either snapshot. The S147 tier-B reading is supported by CORPUS text (survey / expert write-up); the closure's claim that CORPUS puts the Linux man page at B is not in CORPUS.md.
2. **M50-2 (landing) — confirmed, widened and corrected.** At base, 15 of 57 `tools/round-4[1-9]` py/sh files have no row in the marker-bound registry: all six round-49 files, plus files from rounds 42, 43, 44 and 48. The closure's "rounds 46–48 unregistered; last registered are round-45's" is false: round 46 (4/4) and round 47 (2/2) are registered, round 48 2 of 3.
3. **M50-3 (vacuous) — confirmed, sharpened.** `frozen_tables_valid` is set True at `tools/round-49/c1-counter.py:2014` (the `L1995` in the w1 report is a draft line). No exit-1 path sets it False. A forced-False mutant turns `--selftest` red, so the binding is wired but has no path to False.
4. **M50-4 (stale-premise, new) — the closure's registry premise is wrong** (see 2).
5. **M50-5 (landing, new) — the round-49 lesson `## Mistakes` is incomplete.** Two mistakes sit in prose outside the table, and M49-1's `captured-by` still says `none` after QUALITY row 88 captured it.

Round-wide sweep: across the `## Mistakes` tables of rounds 45–49, 17 of 19 rows carry a class outside the CORPUS §5 vocabulary and/or a `captured-by` cell naming no criterion; round 48 has no table at all (bullet form). Details in M50-6.

Not run: any `--data-run`; any green-after check of a fix (the lane is read-only; fixes are described, and their red-before states were run where stated); `tools/round-46/registry.py` (the census-scoped gate) was not run; the S138 `teaches` check is by reading, not mechanised.

Tools installed: none. Host tools used: `python3` (stdlib only), `git`, `sha256sum`, `sed`, `awk`, `grep`.

## Findings table

Commands run from the lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, with `B=7c678ae6…`. Each sha256 is of the stdout file named in `receipts/INDEX.tsv`.

| # | Claim / candidate | Command (exit) | Observed | Verdict |
|---|---|---|---|---|
| F1 | S149 locator (`SOURCES.md:155`, anchor `DESCRIPTION`) | `python3 tools/round-50/snap-locator.py <freebsd snapshot> "EX_USAGE (64) The command was used incorrectly" DESCRIPTION "DESCRIPTION\|ERRORS\|SYNOPSIS\|SEE ALSO"` (**1**) | `quote_at=13857 nearest_heading='ERRORS' anchor='DESCRIPTION' match=False`. Snapshot `git show B:corpus/evidence/round-49/c2/freebsd-sysexits.html` sha256 `1fc793a2…5dbf` = the row's sha. The stripped body reads: DESCRIPTION paragraph ("deprecated … discouraged"), then the `ERRORS` heading, then the quote. stdout sha `52abb8b1…` | **confirmed** |
| F2 | S147 locator (`SOURCES.md:153`, `2. Backdrop`) | `snap-locator.py <popper snapshot> "falsifiability as his criterion …" "2. Backdrop to Popper’s Thought" "…\|3. The Problem of Demarcation\|1. Life"` (**0**) | `nearest_heading='2. Backdrop to Popper’s Thought' match=True`; snapshot sha `2c2d48c6…ec207` = row sha; stdout sha `4c794c9e…` | locator correct (the closure's S147 locator note is right) |
| F3 | S148 locator (`SOURCES.md:154`, `SYNOPSIS`) | `snap-locator.py <man7 snapshot> "#define EX_USAGE 64 /* command line usage error */" SYNOPSIS "NAME\|LIBRARY\|SYNOPSIS\|DESCRIPTION"` (**0**) | `nearest_heading='SYNOPSIS' match=True`; snapshot sha `d9db4b96…340` = row sha; stdout sha `373a1204…` | locator correct |
| F4 | S149 provenance "second mirror of S148" / closure's "FreeBSD is the origin" | `git show B:…freebsd-sysexits.html \| grep -o 'The sysexits file first appeared[^<]*'`; man7 snapshot HISTORY section | FreeBSD HISTORY: "The sysexits file first appeared in 4BSD." man7 HISTORY: "The <sysexits.h> file appeared in 4.0BSD for use by the deliverymail utility, later renamed to sendmail(8)." Neither snapshot names FreeBSD as origin | **not established**; the reject stands on redundancy, but "mirror of S148" and "inverted" are unsupported as written |
| F5 | S147 tier A vs CORPUS tier text | `sed -n '93,97p' /home/vgpnk/Projects/shokunin/CORPUS.md` | B = "strong secondary (expert write-up … survey, textbook)"; A = "primary or authoritative … official docs, original paper, maintainer statement". SEP is an expert survey entry | **B is the better reading** (judgment, not mechanical). Man7 (S148) is an "official docs" candidate for A; the closure's "CORPUS puts the Linux man page at B" is not in the text |
| F6 | S138 `teaches` over-wide | `git show B:corpus/SOURCES.md \| awk -F'\|' '/^\| S138 /{…}'` (0) | cell 6 (anchor): LICENSE:5-8, 10 listings, 22 members / 152 B, tree digest. Cell 7 (`teaches`) also asserts "`unsquashfs` 4.7.5 agrees path-for-path … on all six carriers, with 7-Zip 26.04 providing a distinct-reader cross-check" — none of that is in the anchor or the quote, and the quote grounds a directory name | **confirmed** (by reading) |
| F7 | Registry census, all `tools/round-4[1-9]` py/sh | `python3 tools/round-50/registry-sweep.py B` (**1**) | markers `1/1` (SKILL.md:1715, 1762); `registered_rows_in_marker_section=42`; `files_total=57 unregistered=15`: round-42 `c1-extra.py`; round-43 `build-copies-r43.py c2-controls-r43.py receipt-wrap.py`; round-44 `c1-controls.py c1-oracle.py c1-run.py c2-controls.py`; round-48 `census2.py`; round-49 `c1-controls.py c1-counter.py c1-oracle.py c1-run.py c1-run.sh c2-mismatch.py`. stdout sha `60ad60c3…` | **confirmed; wider than the closure states** |
| F8 | Closure's "rounds 46–48 unregistered; last registered are round-45's" (`corpus/lessons/round-49-verifier-spotcheck.md:22`) | same sweep; `grep -n 'tools/round-4[6-8]/' SKILL.md` | rows at SKILL.md:1753-1761: all four round-46, both round-47, `meanings.py` and `record2.py` of round-48 | **false** (round 48 partial only) |
| F9 | Registry rule the lane owes | `sed -n '418,420p' /home/vgpnk/Projects/shokunin/PROTOCOL.md` | "closure grades no gate conformant until its registry row exists at the lane's registry home" | the protocol rule that should have caught M50-2; it did not reach the lane's QUALITY.md |
| F10 | `frozen_tables_valid` assignment (M50-3) | `git show B:tools/round-49/c1-counter.py \| grep -n frozen_tables_valid` (0) | `182` (doc), `345` (binding list), `2014` `res['frozen_tables_valid'] = True`, `2228` `b[...] = bool(...)`; lines 2008-2013 parse carriers.json and raise `Unevaluable` (exit 2) before the set | **confirmed**, with the precise wording above |
| F11 | Forced-False mutant (shows binding is wired) | scratch copy of the base counter, line 2014 changed to `False`; `python3 -I -B tools/round-49/c1-counter.py --selftest --work <scratch>` (**1**) | `{"cases": 52, "failures": ["green (four v1/v2 carriers, receipts, docs): want 0 got 1"]}`; stdout sha `d9eb8fa7…` | a code change, not a flag, is needed to reach exit 1 from this binding; it is not decorative |
| F12 | Base selftest, unmodified | `python3 -I -B tools/round-49/c1-counter.py --selftest --work <scratch>` on the base blob (**0**) | `cases 52 failures []`; stdout sha `cda33fb6…` | baseline. The w1 draft reported 47 cases; the base has 52 (the L1 amended the draft) |
| F13 | Round-49 `## Mistakes` sweep | `python3 tools/round-50/mistake-sweep.py B 49` (**1**) | table rows 3; M49-1 `captured-by:none` (QUALITY 88 exists but the cell was not updated); M49-2 OK (QUALITY 87; pointers resolve); M49-3 OK (QUALITY 83/84; pointers resolve); `prose_mistake_bullets_outside_table=1` (M49-4 at lesson line 56; M49-5 is inline in that paragraph and the script does not count it); stdout sha `4449f8a9…` | **not all captured**: M49-1 cell stale, M49-4/M49-5 outside the table |
| F14 | Mistake sweep rounds 45–48 | `mistake-sweep.py B 45` (**1**), `46` (**1**), `47` (**1**), `48` (**0**) | r45: 3/3 rows flagged (off-vocabulary classes; `none` in 2). r46: 4/4 flagged (off-vocabulary classes; `none` in 2; one pointer `.ufo/waves/round-46/l1/scores/c1-v1-gap.json` is not a git-tracked path at B). r47: 9/9 flagged (off-vocabulary classes; `none` in 5). r48: 0 table rows (M48-1 is a bullet with `captured-by none`) | **cross-round finding**, see M50-6 |
| F15 | QUALITY coverage of tier / provenance / locator / registration | `grep -n -i 'tier' corpus/QUALITY.md`; `grep -n -i 'registry' corpus/QUALITY.md` | only line 110 defers tier to SOURCES; `registry` appears only in row 74 (a row-count rule for edits) | **no criterion** for M50-1 or M50-2 |

## Mistake rows (round-50 `## Mistakes` candidates)

Full text in the draft file. Summary:

- **M50-1 · `attribution` + `scope`** — S147 tier A vs CORPUS B-text (F5); S149 anchor vs located heading (F1); S149 provenance unsettled (F4); S138 `teaches` wider than its quote (F6). `captured-by` none (F15). Fix: a QUALITY row (tier by CORPUS text; locator equals anchor; teaches tokens appear in anchor or quote). Red-before: F1 exit 1. The teaches check is not built.
- **M50-2 · `landing`** — 15 unregistered counters (F7); the closure's claim false for rounds 46–47 (F8); protocol rule not in QUALITY (F9). Fix: `registry-sweep.py` is red at base; append 15 rows, then expect exit 0 (not run).
- **M50-3 · `vacuous`** — binding with no exit-1 path (F10); wired, not decorative (F11); base green (F12). `captured-by`: rows 84 and 89 were not applied to code bindings. Fix not built; a freeze-time shape-failure case would need a fixture commit (not run).
- **M50-4 · `stale-premise`** — the closure's registry premise (F8); fix: the rev-pinned sweep.
- **M50-5 · `landing`** — lesson table shape and a stale `captured-by` (F13).

## M50-6 (round-wide): class vocabulary and capture cells

The CORPUS rule says classes "come from the `mistakes.md` §5 vocabulary (`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider`)". `.ufo/waves/kaika-w1/mistakes.md:447-449` lists the same nine as a *suggested* vocabulary. Off-vocabulary classes appear in rounds 45–47 (e.g. `sweep-contamination`, `unopened-descendant-credit`, `proxy-only-target`, `freeze-moved-four-times`, `proxy-harm-recurrence`, `unreachable-clause`, `scope-rule-broken-by-the-record`, `claim-that-failed-its-own-clause`, `record-misquotes-its-own-receipt`, and M46-1's long control-named class), and round-49 M49-5 uses `credential-class`. Either the CORPUS list is extended (a rule change, not a per-round fix) or these rows are reclassified. `captured-by: none` recurs in 45–47 (M45-1, M45-2, M46-2, M46-3, M47-1, M47-3, M47-7, M47-8, M47-9). Caveat: the sweep flags a `captured-by` cell that names no criterion, so an honest "none" is also flagged; the sweep is a shape check, not a judgment of the capture.

## Routed to the L1 (fold before the freeze)

1. S149: correct the anchor to `ERRORS` (append-only correction row, supersedes S149); do not assert "mirror" or "origin" without a source that says so. Consider the reject reason as "redundant with S148" only.
2. S147: correct the tier to B (supersedes row), grounded in CORPUS.md:93-96; keep the locator.
3. S138: narrow `teaches` to the directory-name grounding, or add a located quote for the census.
4. Registry: the 15-row append; the round-49 counters need rows before any round-50 gate is conformant under PROTOCOL.md §Gate standard "Delivery".
5. C2 atoms: B8/B9 should include the teaches-token rule and the registry sweep above, so the freeze reads the same facts.
6. C1 counter `frozen_tables_valid`: decide whether to delete it or let a freeze-shape failure set it False; the change must be in the frozen bytes or disclosed as a routed miss.
7. Closure pointers: replace the draft line `L1995` with the base line `2014` in any routed text.

## Receipts

`receipts/INDEX.tsv` (sha256 of stdout): registry-sweep-base `60ad60c3…`; mistake-sweep r45 `9237f2de…`, r46 `0b334aaf…`, r47 `bc553e04…`, r48 `a967ebf1…`, r49 `4449f8a9…`; locator S147 `4c794c9e…`, S148 `373a1204…`, S149 `52abb8b1…`; selftest base `cda33fb6…`, forced-False `d9eb8fa7…`. Input snapshot sha256 (from base blobs, not copied into the seat): popper `2c2d48c6…ec207`, freebsd `1fc793a2…5dbf`, man7 sysexits `d9db4b96…340`, each equal to its SOURCES row. Scratch `/fast/scratch/hyaku/kaidoku-r50/C2MistakeScribe` removed after the receipts were copied.
