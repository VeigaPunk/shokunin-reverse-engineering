author: hyaku closure (non-author integrator, @m_zfl)

# Round 49 verifier spot-check — kaidoku

## Closure result

Lane status: **ok**. Admission: **admitted**. Both declared claims re-measure from committed bytes, no owned axis is harmed, and the discernment sample agrees with the gate on the admit and the reject, with reasoning/tier disagreements routed below. Re-measured 2026-10-28 against lane tip `623476eef55640258fa5d4ff95a87ba59c49279f` (base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`).

Driver digest (`.ufo/watchdog.log`): `2026-10-28T17:40:44-03:00 launch kaidoku round=49 pgid=945663 driver=hyaku-inline attempt=1`; `2026-10-28T20:12:35-03:00 complete kaidoku round=49; hyaku-inline attempt=1`.

## Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-49/kaidoku.md` | `kaidoku-shokunin 86fc63a2f0aa297cf65fedd9af60a27703720200` (2026-10-28 19:52 -0300, before the 20:12 completion line) |
| `SHONEN` heading, one line per box | read report lines 52-57 | four `[~]` lines, one per box |
| cited commits are ancestors of `main` | `git merge-base --is-ancestor <hash> main` for all 11 cited hashes (`14936cb9`, `decc5697`, `76d7ad6f`, `4aabb0b4`, `3847f393`, `188ddeea`, `b58f9b19`, `29883d4e`, `5855962d`, `00b18504`, `623476ee`) | all 11 `anc ok` |
| pushed, clean | `jj-lane.sh state …` / `git status --porcelain` / `ls-remote` | `ahead=0 behind=0 tracked=0 untracked=0`; remote `refs/heads/main` = `623476eef55640258fa5d4ff95a87ba59c49279f` |
| prompt carries contract | `.ufo/prompts/kaidoku-round-49.md` headings | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 commit scope, §6 hyaku addendum, §7 scratch — present |
| not a marker | report names 88 seats, 11 resolvable hashes, evidence pointers | real report |

Conformance defects (status-neutral): (1) the fleet repo's `git status` shows staged `.scratch/` paths from sibling closures (not lane debt, not kaidoku); (2) lane-owned counters `tools/round-49/c1-counter.py`, `c1-run.sh`, `c2-mismatch.py` have **no registry row** at the lane registry home (`SKILL.md` "Local round-evidence gate registry"; the last counters registered are round-45's) — PROTOCOL §Gate standard "Delivery": closure grades no gate conformant until its row exists; `c2-mismatch.py` also has no `--selftest` (`w2/W2C1Selftest.md` finding 3). Rounds 46-48 counters are likewise unregistered (pre-existing); (3) wave-1 seat `C2SourcesReopen` settled without a report (disclosed by the lane).

## Per-claim re-check

Both claims rest on lane-owned counters, so the frozen-run verdicts are *evidence-verified* and the substance is *re-measured* with plain commands I ran (I did not execute the lane's gates).

### R49-C1 — coverage, SquashFS v1/v2 Frontier → Core through REA 6.5.0 `extract-firmware` (re-measured + evidence-verified)

Reported: before exit 1 / `carriers_matched 0` at the freeze; after exit 0 / `carriers_matched 4`, `failing []`, 3/3/4/4 members, `gaps []`.

- Evidence verified: `sha256sum .ufo/waves/round-49/l1/scores/c1-final.json` → `d9e00d4116b6…` (report cites `d9e00d41…`); `c1-final.json` has `carriers_matched 4`, `bindings_false []`; `git diff --stat decc5697… 623476ee… -- tools/round-49 plans/round-49-claims.md` is **empty** (counters frozen, unchanged since the freeze); `FREEZE` file = `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`; C1 counter `--selftest` tally from the committed w2 seat `W2C1Selftest.md`: `cases 52, failures []`, controls selftest 11/11 (seat evidence, not run by me; the same file records that the frozen counter kills 43 of 75 single-point mutants, so it is a weak gate, as the lane discloses).
- Re-measured: `jq` over `corpus/evidence/round-49/c1/{v1be,v1le,v2be,v2le}/envelope.json`: `ok true`; handlers `squashfs_v1`, `squashfs_v1`, `squashfs_v2`, `squashfs_v2`; `.data.normalized_result.extraction_gaps` = `[]` on all four; `unblob --version` `26.6.4`; `manifest.json` every carrier `exit_code 0` with fixture sha256 equal to `sha256sum corpus/evidence/round-42/c2/fixtures/{v1-be,v1-le,v2-be,v2-le}--*.bin` (`529e1077…`, `b45925fa…`, `79c0f388…`, `7c62dbe3…`). Published members per `extract-tree.tsv` (data rows): 3, 3, 4, 4. Every member sha256 appears in the frozen oracle `tools/round-49/carriers.json` (v1be 3/3, v1le 3/3, v2be 4/4, v2le 4/4).
- Independent oracle: `sasquatch -le|-be -lls <fixture>` (`~/.local/bin/sasquatch`) lists 3 regular files for the two v1 fixtures (`apple/banana/cherry.txt`) and 4 for the two v2 (`apple1-4.txt`) — equal to the receipts.
- Landing: `PROVINCE.md:436,438` Core row and frontier note; `corpus/README.md:105,226,278`; entry `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` exists; knowledge `.md` files `git ls-tree … | grep -c '\.md$'`: base 138 → tip 139 (SCORECARD's "138 → 139" reproduces); S112 line cites in the entry (`:24-26`, `:51-54`, `:68-69`, `:101-102`, `:158-159`) match `raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` byte for byte.
- Bounds (lane-disclosed, confirmed): same four round-44 fixtures — a re-run under a restated predicate, not new data; receipt does not authenticate writer/round; documentation bindings are presence checks. These bound the *expansion* trend, not the claim's truth.

Verdict: **verified**, coverage **improved** (bounded to four fixtures).

### R49-C2 — calibration, nine round-48 self-assessment atoms A1–A9 (re-measured A1–A5, A6, A7, A9; evidence-verified A8 and the battery)

Reported: before `mismatches 9` (do-nothing control), after `mismatches 0`, 16 mutations each red on its own atom, do-nothing red ×9.

- Evidence verified: `sha256sum …/c2-final.json` → `544167f2a6a7…` (report `544167f2…`); fields `atoms_total 9`, `mismatches 0`, `battery.failing []`, `battery.do_nothing_red [A1..A9]`, `counter_sha256 == counter_sha256_at_freeze` (`9b80b3b0…`), `freeze decc5697…`, `rev 00b18504…`.
- Re-measured from committed bytes: **A1** `sed -n 4p corpus/lessons/round-48.md` names `0f06251b…`; `grep -c b6f7ca2a SCORECARD.md` = 3 (the amended declared freeze), so `declared=b6f7ca2a… stale=0f06251b…` is right. **A2** `git rev-parse 663f30ee` → `663f30ee751694fb0970e7de68fe88356e680822` (= the lesson's `actual=`). **A3** `grep -n` in `LOG.md`: `2e785632` → 3440,3441,3445; `33f65a91` → 3440,3441,3444; `c093e798` → 3440,3441,3445; `577a02a5`, `8847042a`, `7fe11332` → no hit (the lesson's `unnamed=` triple). **A4** from `.ufo/waves/round-48/r48-w1-results.json` (`seats 75`) and the `w1/` tree: seats with a non-empty `.md` at `w1/<seat>.md` or under `w1/<seat>/` = 72; missing `C1Meaning, C1Battery, ScribeReportNumbers` — equals the lesson's `seats=75 reports=72`. **A5** `git show e4f2cfa5:.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json | sha256sum` → `6320c5d240e4…` and c2 → `d1bb87d883ea…` (the lesson's `c1_raw`/`c2_raw`). **A6/A7** SOURCES rows S147/S148 exist (`grep -nE '^ {0,3}\|[[:space:]]*S14[5-9]' corpus/SOURCES.md`; S145/S146 diff-clean vs base: only S112/S138/S139 rows changed in `git diff e4f2cfa5 623476ee -- corpus/SOURCES.md`). **A9** the SCORECARD closing line `A9 verdict=rejected-harmed source=corpus/lessons/round-48-verifier-spotcheck.md calibration=harmed` is present and matches that lesson's closure verdict.
- Limits (lane-disclosed, accepted): C2 is a consistency check of the record; it misses a second unmarked search-log entry, non-`is` second statuses, duplicate keys, and the round-49 lesson's own freeze header lies outside every atom; its battery misses 13 of 30 wave-2 mutations; ten further round-48 mismatches (`w1/C2SelfAssess.md`) are not repaired. The lesson's own header and SCORECARD agree this round (single freeze `decc5697…` in lesson, SCORECARD, report, `FREEZE`), i.e. no repeat of the round-48 defect.

Verdict: **verified**, calibration **improved** (the nine named defects are corrected by appended lines, the filed round-48 lesson untouched; bounded as above).

## Per-axis verdicts (match the MANIFEST entry)

`git diff e4f2cfa5… 623476ee… -- SCORECARD.md`: scores `10 → 10` on coverage/depth/calibration with a capability row and the round-49 section; the A9 correction line sits beside the unchanged round-48 entry.

| axis | verdict | basis |
|---|---|---|
| coverage | improved | R49-C1 re-measured: four fixtures, handlers and members equal receipts, oracle and `sasquatch` list; Core row landed; bounded to the same four round-44 bytes |
| calibration | improved | R49-C2 re-measured: nine atoms correct against committed bytes; round-48 calibration harm repaired by append-only corrections; instrument misses disclosed |
| depth | unchanged | unclaimed; SKILL decision-table row added, but the v4 triage table is known to mis-route v2ns (`w2/W2Skill.md`), not credited |

No axis harmed.

## Discernment spot-check (LEARNING.md)

Sample from `corpus/lessons/round-49.md` `## Gate`; all sources re-opened 2026-10-28 (HTTP 200; sha256 of each body equals the sha the lane recorded).

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| S147 (SEP, Popper) | admit, tier A, mined | `https://plato.stanford.edu/entries/popper/` — 118,135 B, sha256 `2c2d48c6…ec207`; "substantive revision Fri Jul 31, 2026" present | **agree admit; disagree tier A** | quote "falsifiability as his criterion … it is scientific" (21 words) is verbatim and sits under `2. Backdrop to Popper’s Thought` (before `3. The Problem of Demarcation`), correcting S145's wrong locator. SEP is an expert survey of Popper, which CORPUS tier text puts at **B** ("strong secondary … survey"), not A ("primary or authoritative"); the lane's own wave-2 seat said the same and the row was left. The second quote ("it is consistent with all possible observations, is unscientific") is a verbatim fragment but cuts across a clause. Admit stands: the row backs an analogy, nothing rests on tier A |
| S148 (man7 `sysexits.h.3head`) | admit, tier A, mined, supersedes S146 | `https://man7.org/linux/man-pages/man3/sysexits.h.3head.html` — 12,725 B, sha256 `d9db4b96…340`; "Linux man-pages 6.19 2025-09-21" | **agree** | "#define EX_USAGE 64 /* command line usage error */" (9 words) located verbatim; the row correctly replaces S146's wrong "no locator" reason and its 404 URL; primary header documentation for this scope |
| S149 (FreeBSD sysexits(3)) | reject, tier C | `https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3` — 59,251 B, sha256 `1fc793a2…5dbf` | **agree reject; disagree stated reason and anchor** | "EX_USAGE (64) The command was used incorrectly" is verbatim but sits under `ERRORS`, not the cited `DESCRIPTION`; and "a second mirror of the value S148 already carries" inverts provenance (FreeBSD is the origin of sysexits, man7 the Linux rendering). The reject itself is right — it adds no claim S148 cannot carry (redundant, lead only) — but the row's stated reason and anchor are wrong and left append-only without an in-row correction |
| S138 keep `mined` | kept | (not re-fetched for membership; quote check only) tree page `<title>` and the entry's 22-member census are lane-reproduced in `w1/C1S138Reopen.md` | **agree keep, note** | the located quote grounds a directory name, not the member census; the census rests on the fetched member bytes (carriers.json shas), so keeping `mined` is defensible, but the row's `teaches` is wider than its quote — the lane's seat disagreed too |

`corpus/SOURCES.md` new-row check: S147 row re-opened (quote, locator, sha256, 118,135 B all reproduce); S148 and S149 quotes ≤25 words and verbatim in the normalised body (tags stripped, whitespace collapsed). Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, 15 `W04` duplicate-URL lines (S033 … S142; unchanged from round start per the lane's start/end census), final line `kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`; rows 146 → 149 (S147–S149 added only).

## Trend verdicts

- **expansion: improved** — one admitted entry on ground the coverage map held only as Frontier, citing mined rows (S112, S138, S139), capability row added; bounded to the four round-44 fixtures (no new data).
- **quality: unchanged** — S145/S146 record errors are superseded (S147/S148, ~20 wrong entry sentences repaired at the tip), offset by new-row defects left in place (S149 reason/anchor, S147 tier, S138 over-wide `teaches`) and unrepaired counter misses; no admitted entry is found false and left unmarked (the disagreements are recorded in the lesson, not in the rows).
- **discernment: unchanged** — the outside sample agrees with the gate on the admit (S147/S148) and the reject (S149), but disagrees on one tier and one reject rationale; the lane recorded the disagreements as "the learning" yet added no grounded QUALITY criterion for source tiering or provenance direction (rows 88–89 concern freeze naming and plan quantifiers). Not harmed because the disagreement is on record in the lesson; not improved until it becomes a criterion.

## SHONEN

All four boxes are `[~]` in the report. The SKILL decision-table row, the REA `extract-firmware` end-to-end task (`corpus/evidence/round-49/c1/`, re-measured here), and the PROVINCE row look checkable by a non-author; "executable instructions" has now a non-author re-run of the counting commands' *outputs* (not the gates). Promotion is operator-owned; `[x]` not written.

## Routed defects (lane fixes next round)

1. Register `tools/round-49/c1-counter.py`, `c1-run.sh`, `c2-mismatch.py` (and the round-46–48 counters) at the SKILL.md gate registry with verdict map and self-test spelling; give `c2-mismatch.py` a `--selftest` with committed expected values.
2. Append a named correction entry for S149 (reason: FreeBSD is the origin of sysexits; locator is `ERRORS`) and for the S147 tier (B per CORPUS) in the next round; add a QUALITY criterion citing this lesson: tier by CORPUS text, state provenance direction, and quote locators must name the actual heading.
3. Narrow S138 `teaches` or add a row that grounds the member census to the fetched member bytes, not the directory name.
4. Repair the counter misses listed in `corpus/lessons/round-49.md` `## Wave 2` (C2 A7/A8 quantifiers, duplicate keys, the round-49 lesson header outside any atom; C1 freeze walk for quoted names/copy status), and the ten further round-48 mismatches.
5. One new-data v1/v2 carrier if a published image becomes fetchable (the round-49 C1 is the same bytes as round 44).
6. Credential-class: session-cookie headers remain in pushed history (`14936cb9`); redacted at tip only — operator decision on purge.
