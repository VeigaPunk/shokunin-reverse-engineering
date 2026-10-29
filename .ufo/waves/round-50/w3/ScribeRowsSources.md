# ScribeRowsSources — round 50, attempt 2, wave 3: the four SOURCES append rows + the search-log entry

**Verdict: DONE — the four rows (S243, S244, S245, S249) are drafted, every anchor is located against a
fresh 2026-10-29 re-fetch, and the block validates clean on a scratch registry copy (`sources-census.sh
validate --file <copy>` exit 0, one expected `W04` warning, no E-code).** The draft is at
`.ufo/waves/round-50/w3/ScribeRowsSources/rows.md`; it is **not** applied to the lane tree. No REA run, no
data run, no vendor firmware byte fetched, no git mutation, no tool installed.

Two things the L1 must act on, both measured here (F1, F2 below): the entry file and these four rows must
land in **one** commit (otherwise the registry goes red on `E11`), and the entry's `source:` lines must
cite S243/S244/S245/S249 (otherwise the counter's `sourced` binding stays red for a reason no registry
row can fix). The entry draft already satisfies the second half — verified independently here (F15) — so
what is left for the L1 on that point is landing it, not changing it.

**A third, found by two sibling seats and confirmed here (F13): the L1's own landing scripts still carry
the stale stem and would drop these four rows.** `.ufo/waves/round-50/l1/land_sources.py:11-12` and
`land_c1.py:17-18` both set `STEM = '2026-10-28-r50-le-avm-members-core'`, and `land_sources.py:130`
filters the four rows away (`S = {k: S[k] for k in ('S246','S247','S248')}` — "honest stop: C1 rows
S243-S245/S249 are not landed"). Run as they stand, they write the entry under the wrong path and land
none of these four rows, so `entry_present`, `province_core_row`, `frontier_note`, `coverage_map_row` and
`sourced` all stay red. The patch I supply (`artifacts/SOURCES.patched.md`) is computed against the
counter's stem, so the scripts and the patch must be brought onto the same stem before landing.

## Deliverable

| file | what it is |
|---|---|
| `.ufo/waves/round-50/w3/ScribeRowsSources/rows.md` | the four rows, the search-log entry, the round-lesson `## Gate` rows, and the landing constraints (sha256 `c478e7cd74de6b792258dc564e1bc70b9b00ebe7827b97a1ba145e598320825b`) |
| `…/ScribeRowsSources/build-rows.py` | the row builder: cell/enum assertions, the scratch mirror, the census proof |
| `…/ScribeRowsSources/fetch-sources.sh` | the re-fetch driver (exact URL → UTC time → HTTP status → bytes → sha256 → curl exit) |
| `…/ScribeRowsSources/quote-check.py` + `quote-check.out.txt` | the anchor locator (`QUOTE_CHECK located=18 missing=0`, exit 0) |
| `…/ScribeRowsSources/census-validate.txt` | the census output for the block (exit 0) |
| `…/ScribeRowsSources/receipts/` | `receipts.tsv` (8 fetches), `attempt1-digests.tsv`, `census-validate-with-block.txt`, `census-validate-E11-test.txt` |
| `…/ScribeRowsSources/artifacts/SOURCES.patched.md` | the **whole patched registry**, ready to diff or apply: base + the four rows (ascending id order) + the search-log bullet. sha256 `a8fc2772aafc10269497ef66a19ddfce0983e227f0499053b0f64989af7daabc` |
| `…/ScribeRowsSources/artifacts/SOURCES.base.md` | the unmodified base registry the patch was computed against, for the diff. sha256 `2204e6a6475177616caa92446c68ec35c3e6cdcd8f5194e945b7b201d8f189c4` |
| `…/ScribeRowsSources/artifacts/build.log` | the build run's stdout (cell-length report, census exit, counter-binding check) |

## The four rows

Entry path in every `used-by` cell: `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`.

| id | kind | tier | scope | anchor |
|---|---|---|---|---|
| S243 | code | B | the AVM LE/BE symbol definitions and the byte order they select | patch `:7` `+#define AVM_LE 2`; `:17-18` the LE condition selects `__LITTLE_ENDIAN` |
| S244 | dataset | A | which firmware images AVM publishes per model directory and their listed sizes and dates | the four `fritz.os/` model dirs; listing rows with dates and sizes |
| S245 | code | A | the little-endian v4 handler and its sasquatch `-le` argv | `:53-54` `case Endian.LITTLE, _:` → `commands_args.append("-le")`; `:455` `NAME = "squashfs_v4_le"` |
| S249 | docs | A | the AVM firmware licence restricts redistribution of the package | `:850` "The licensee may create only one copy of the software, which may be used exclusively for backup use." (18 words) |

Eleven columns per row; no `|` inside any cell; `status` `mined`; `opened` 2026-10-28; `recheck` 180d
(S243, S245) and 90d (S244, S249); longest cell **199 chars** (S244 anchor), all others ≤ 191.

## Findings

| # | finding | evidence (command → exit; sha256 / value) | action for the L1 |
|---|---|---|---|
| F1 | **The entry file and these four rows must land in the same commit.** The census resolves every `mined` row's `used-by` path on disk. On the scratch copy, with the entry path present: `sources-census.sh validate --file <copy>` → **exit 0**; with it removed: the same command → **exit 1** with exactly four `E11` lines (`S243`, `S244`, `S245`, `S249` — "missing used-by corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md") and no other new finding. The entry does not exist in the lane at the base revision, so a rows-only landing makes the registry red. | `receipts/census-validate-E11-test.txt` (exit 1) vs `receipts/census-validate-with-block.txt` (exit 0); the mirror carries a **mirror-only placeholder** for the not-yet-landed entry — the lane tree is untouched | land the entry and the four rows together (or the rows after the entry) |
| F2 | **The counter's `sourced` binding needs the entry to cite these four ids, not just to exist.** `tools/round-50/c1-counter.py:2468-2476` requires a registry row whose id is among the `S###` tokens of the entry's `source:` lines, whose `opened` is in `OPENED_DATES` (`c1-counter.py:393` = 2026-10-28, 2026-10-29) and whose `used-by` names the entry path or stem. The last two conditions are satisfied by all four rows today (checked: `opened=2026-10-28`, `used_by_ok=True` for each). The first condition is now also satisfied by the entry draft — verified independently in F15 — so the two halves of the binding meet. What remains is the L1 **landing** that entry, not changing it. | counter source read at `c1-counter.py:377-378` (ENTRY/STEM), `:393`, `:2468-2476`; the per-row check printed by `build-rows.py`; F15's tokenizer re-run | land the entry whose `source:` lines name these four ids (the draft already does) |
| F3 | **The dispatch text's entry stem is stale; the frozen counter's is right.** The w3 spec named `2026-10-29-r50-le-avm-hsqs-core`; the counter's `ENTRY`/`STEM` constants are `2026-10-28-r50-avm-le-squashfs-core` (`:377-378`), and the attempt-2 claims file was corrected to that stem by commit `6f4aba63` ("attempt-2 claims corrected — entry stem pinned to the frozen counter constants"). The rows cite the counter's stem. | `git log --oneline 6f4aba63` → `6f4aba63 round-50: attempt-2 claims corrected — entry stem pinned to the frozen counter constants`; `plans/round-50-attempt2-claims.md:106` names `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` | none — but the L1's other drafts must use the same stem, or the landing splits |
| F4 | **The attempt-2 re-open is byte-identical to attempt 1 for all six sources the attempt-1 receipts pin.** Re-fetched 2026-10-29 20:39:30–20:39:37Z, eight HTTP 200s, curl exit 0 each; every digest equals the attempt-1 value (6 of 6 compared, 0 differing). The 7581 and 7582 index digests are new (attempt 1's receipts did not pin them) but their listing bodies (574 B each) match the attempt-1 `## Gate` row's recorded sizes. | `receipts/receipts.tsv` vs `receipts/attempt1-digests.tsv` → `identical=6 differing=0`; patch 101 also byte-identical at Freetz-NG commit `9a723692` (`cmp` exit 0) | none — the sources are stable across the two attempts |
| F5 | **All 18 anchors locate in the served bodies** (`QUOTE_CHECK located=18 missing=0`, exit 0): S243 `:7`, `:8`, `:17`, `:18`; S245 `:40` (`case Endian.BIG, 4:`), `:48` (the only `is_avm`), `:53`, `:54`, `:455`; S249 `:850`; S244's four listing rows (name + date + size, tags stripped) and the four model directories named in the root index. | `quote-check.out.txt`; the first run failed on the four listing rows because the Apache-style HTML puts the file name inside an `<a>` tag — the checker now strips tags before matching (`quote-check.py:62-68`), and the corrected run is exit 0 | none — but the tag-stripping detail is why the first run read MISSING |
| F6 | **`W04` is the only new census finding, as expected.** S245 carries the same URL as S108/S112 with a deliberately different scope (the LE handler, not the BE AVM branch), so the census emits `file\tW04\tS245 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes`. W04 count 18 → 19; no `E04` (the scope differs, which is what keeps it a warning); the baseline registry validates at exit 0 too. | `receipts/census-validate-with-block.txt` (exit 0); baseline run exit 0; `W04 count with block: 19 baseline: 18` | none — the W04 against S112 is expected and allowed |
| F7 | **The registry diff is exactly 5 added lines, 0 changed, 0 removed.** The four rows (S243, S244, S245 after the S149 row; S249 after S248 — ascending id order, the same placement the lane's own `l1/land_sources.py` uses) plus one search-log bullet. `diff` of the patched mirror against the base registry: 5 `>` lines, 0 `<` lines. | `diff <base> <patched> \| grep -c '^[<>]'` → 5; all 5 are `>` | none — the registry stays append-only; no existing row is edited |
| F8 | **Ids are free and the skipped band stays skipped.** S243, S244, S245 and S249 are absent from the registry (it ends at S248; 152 rows). S150-S242 stay skipped: earlier lessons cite them as refused staged rows that were never registered, so reusing one would repoint those historical citations (`w1/C1SrcFreetz.md` F6). | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 152; the row list ends S149 then S246-S248 | none |
| F9 | **The search-log entry reuses attempt 1's counts without double-counting.** The existing 2026-10-28 round-50 entry counted 3 identified / 3 screened / 3 included (the C2 correction rows S246-S248, landed). The new 2026-10-29 entry counts 4 / 4 / 4 / 0 — the four C1 rows only — and says so explicitly, so the two entries do not read as one run. Exclusion reasons: none (S114 is unchanged and stays as it is; the attempt-1 Gate rows for these four sources stay in the lesson as the record of the earlier honest stop). Stop rationale: the four sources are unchanged, the four claims the entry needs are covered by them, no further source family was opened. | `rows.md` §"Search-log entry"; the existing bullet at `corpus/SOURCES.md:249` | none |
| F10 | **Attempt 1's "honest stop" is now reversible, and this seat states the reason.** Attempt 1 held S243/S244/S245/S249 back because no landed entry cited them (`corpus/lessons/round-50.md` `## Gate` + `## Honest stop`). This attempt registers them because the C1 entry lands in the same round and cites all four. The attempt-1 Gate rows and the `## Honest stop` paragraph stay in the lesson as the record; the new Gate rows record the attempt-2 re-open (2026-10-29, same digests). | `corpus/lessons/round-50.md` `## Gate` (read at the base revision); the new Gate table in `rows.md` | integrate the new Gate rows into `corpus/lessons/round-50.md`; leave the attempt-1 rows in place |
| F11 | **The quote at `:850` is the licence clause the chain-pinning rests on, and the surrounding lines agree.** `info_en.txt:850` grants one personal backup copy; `:851`-`:853` forbid copying, propagating, reverse engineering and making the package publicly accessible. The row anchors on `:850` (the one quote the attempt-1 Gate named) and scopes itself to "restricts redistribution". | `info-6490-de.txt` lines 846-856, read from the 2026-10-29 body | none — but the lesson may want `:851-853` too, since those are the redistribution clause proper |
| F12 | **No source text describes an LE AVM layout — the rows do not pretend otherwise.** S243's scope says the patch defines the symbols and the byte order only, and its `teaches` cell says the marker on the LE carriers is an observation of their bytes. S245's anchor records that the only `is_avm` test (`:48`) sits inside the BE branch (`:40`), so the LE path never reads it. This matches attempt 1's `w1/C1SrcFreetz.md` F1-F5 and `w1/C1SrcUnblob.md` F1. | `quote-check.out.txt` lines for `:40`/`:48`; `w1/C1SrcFreetz.md` F1, F4, F5 | none — keep the C1 entry's disclosed limit (1) worded this way |
| F13 | **The L1's landing scripts carry the stale stem and filter these four rows away.** `land_sources.py:11-12` and `land_c1.py:17-18` set `STEM = '2026-10-28-r50-le-avm-members-core'` (the attempt-1 stem), and `land_sources.py:130` reduces `S` to `('S246','S247','S248')` — "honest stop: C1 rows S243-S245/S249 are not landed". Run as they stand, they write the entry under `corpus/knowledge/2026-10-28-r50-le-avm-members-core.md` (not the counter's path) and land **none** of these four rows, leaving `entry_present`, `province_core_row`, `frontier_note`, `coverage_map_row` and `sourced` red. These are the only two occurrences of the stale stem in the lane's `.py`/`.md` files. | `grep -n 'STEM *=' land_sources.py land_c1.py` → `2026-10-28-r50-le-avm-members-core` in both; `grep -n "S = {k: S\[k\]" land_sources.py` → line 130; a lane-wide grep for the stale stem finds only those two files | **the L1 must fix the scripts, not just the rows**: bring both onto `STEM = '2026-10-28-r50-avm-le-squashfs-core'`, drop the `land_sources.py:130` filter so S243/S244/S245/S249 land, and land the entry and the rows in one commit (F1). `artifacts/SOURCES.patched.md` is already computed against the counter's stem, so the scripts and the patch must agree |
| F14 | **The `used-by` cells are plain paths, no backticks** — the census `E11` rule the lane applies resolves the path literally, and a backticked cell would not resolve. `land_sources.py` strips backticks for this reason; my rows need no stripping because they never carried any. | the four `used-by` cells printed above: `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, backtick count 0 | none — keep them plain when applying the patch |
| F15 | **The entry draft's `source:` lines already yield exactly these four ids — the entry-side half of F2 is satisfied.** Verified here independently with the counter's own tokenizer (`SID_RE`, `c1-counter.py:430`; `sid_tokens`, `:589`) applied to `w3/ScribeEntryC1/entry-draft.md`: 4 `source:` lines, `src_ids = {S243, S244, S245, S249}`, and those four are the **only** `S###` tokens anywhere in the file (0 stray ids outside the `source:` lines). So the counter's `sourced` binding has exactly the four ids my rows cover — the two halves of the binding now meet. (The peer's own tokenizer run reached the same result; this is my independent re-run, not a relay of their claim.) | the tokenizer check above, run against `w3/ScribeEntryC1/entry-draft.md` (read-only, sibling seat dir) | none — the remaining work on F2 is the L1 landing the entry that names these four ids |

## Commands, exits and digests

| # | command | exit | result |
|---|---|---|---|
| R1 | `bash .ufo/waves/round-50/w3/ScribeRowsSources/fetch-sources.sh` (`S=/fast/scratch/hyaku/kaidoku-r50/w3-ScribeRowsSources`) | 0 | 8 fetches, all HTTP 200, curl exit 0 each, 2026-10-29T20:39:30Z–20:39:37Z; `receipts/receipts.tsv` |
| R2 | `python3 -I -B …/build-rows.py` | 0 | wrote `rows.md`; built the scratch mirror; ran the census → exit 0; printed the per-row counter-binding check (`opened=2026-10-28`, `used_by_ok=True` ×4) |
| R3 | `python3 -I -B …/quote-check.py` | 0 | `QUOTE_CHECK located=18 missing=0` (`quote-check.out.txt`) |
| R4 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` | 0 | 19 `W04` lines (18 baseline + the expected S245 one), final line `file ok <mirror>/corpus/SOURCES.md` |
| R5 | same, with the mirror's entry placeholder removed | **1** | the same 19 `W04` lines **plus** exactly four `E11` lines, one per new row (F1) |
| R6 | `diff <base SOURCES.md> <patched mirror>` | 0 | 5 added lines, 0 removed, 0 modified (F7) |
| R7 | `sha256sum` of the Freetz-NG commit-pinned copy of patch 101 vs the Freetz `master` copy; `cmp` | 0 / 0 | identical, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707` — the row's digest is stable on both mirrors |
| R8 | secret scan of `receipts/` for `set-cookie`, `authorization`, `session=` | 1 (no hits) | the fetch script strips `Set-Cookie`/`Cookie` headers before keeping any header; no header file is copied into the seat dir |

## Not run / limits

- **No REA run, no counter run, no data run, no `--data-run`.** This wave is build-only; the L1 runs the
  REA-dependent controls and the C1 data run in its own quiet window.
- **No vendor firmware byte was fetched.** Only eight text bodies (one patch, one Python source file, five
  index pages, one licence text) went over the network, into the seat scratch. The carrier images were
  never touched by this seat.
- **The attempt-1 digests are transcribed from the attempt-1 receipts and Gate rows**
  (`w1/C1SrcFreetz.md` receipts, `w1/C1SrcAvmIndex.md` F1/F12, `corpus/lessons/round-50.md` `## Gate`), not
  re-fetched from attempt-1's scratch (removed). The comparison in F4 is therefore digest-vs-digest
  against the recorded attempt-1 values, and the 6 of 6 equality is a check of my fetches against the
  recorded values — not an independent re-fetch of attempt 1.
- **The census proof ran against a scratch mirror** (`$S/mirror/`), whose `corpus/knowledge/` and
  `corpus/lessons/` are symlinks to the lane's real files plus a mirror-only placeholder for the
  not-yet-landed entry. The lane's `corpus/SOURCES.md` is **unchanged** (`git status --porcelain` shows
  only the pre-existing untracked wave directories).
- The `S249` anchor names `:850` as the attempt-1 Gate named it. The redistribution clause proper is
  `:851`-`:853` (F11); the L1 may widen the anchor.
- **Not claimed:** that any AVM LE layout exists as a documented format, that the marker proves vendor
  origin, or that the four carriers are verified — those are the C1 claim's business, not this seat's.

## Tool installs / updates

**None.** No pacman transaction, no `uv tool`/`npx`/release-binary install, no PATH change, no host
service touched. Used only `curl`, `sha256sum`, `python3` (standard library), `diff`, `grep`, `awk` — all
already present. (Channel per `/home/vgpnk/.omp/agent/RULES.md`; the pacman guard was respected: nothing
was installed at all.)

## Scratch

`/fast/scratch/hyaku/kaidoku-r50/w3-ScribeRowsSources` — removed after the receipts were copied into the
seat dir. `scripts/hyaku/disk-guard.sh status` was run before the pass (`/fast/scratch/hyaku` 39% used,
495.7 G free). Nothing was written under `/tmp`.
