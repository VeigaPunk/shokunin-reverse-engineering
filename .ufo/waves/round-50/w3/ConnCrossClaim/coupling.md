# R50-C1 × R50-C3 coupling matrix — wave-3 build input for the L1

Seat: ConnCrossClaim. Base `f890bbea` (claims), lane tip at analysis time `6f4aba63` (entry-stem
correction; the seat prompt's file name `corpus/knowledge/2026-10-29-r50-le-avm-hsqs-core.md` is
the superseded first draft — the frozen C1 counter pins `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`,
constants `ENTRY`/`STEM`, verified byte-identical at `435d41fd..6f4aba63`).

## Verdict

**One blocking coupling found and proved empirically: the C3 claim's instrument path
`tools/round-50/sqfs-triage-v5.py` cannot land as written — both frozen counters independently
forbid ANY post-freeze add under `tools/round-50/` (C1: exit 2 `frozen_path_changed`;
C2: `frozen_path_changed`).** Mitigation (free now, impossible after the C3 freeze): amend the
C3 section of `plans/round-50-attempt2-claims.md` pre-freeze to land the instrument at
`tools/round-50-c3/sqfs-triage-v5.py` (outside both frozen families) with its registry row. All
other couplings are drafting hazards with concrete shapes, listed below; a full simulated landing
with the moved path scores C2 all-11-atoms green, battery `failing []`, and all nine C1
documentation bindings true (receipt: `receipts/landing-validation.txt`).

## F1 (blocking) — the v5 instrument path vs both freeze walks

| walk | where | rule | effect of landing `tools/round-50/sqfs-triage-v5.py` after `435d41fd` |
|---|---|---|---|
| C1 `frozen_drift` | `c1-counter.py:1661`, `FROZEN_PREFIXES=('tools/round-50/',)` :413-430 | any `A` status under the prefix in `FREEZE..REV` is drift (`A` under a frozen prefix is always a change; selftest case "a new file under tools/round-50 after the freeze" → exit 2, :4252-4254) | `measure()` raises `FrozenPathChanged` → receipt `{"reason":"frozen_path_changed","exit_code":2}`; `met_target` never computed → **C1 cannot exit 0 at any REV ≥ the C3 freeze commit** |
| C2 `freeze_check` | `c2-record.py:1090`, `FROZEN=('tools/round-50','plans/round-50-claims.md')` :124 | (a) `git log --full-history -m --no-renames --name-status FREEZE..REV -- tools/round-50 plans/round-50-claims.md` non-empty, or (b) full-tree blob/mode diff under those prefixes non-empty | both trip: `touched` lists the `A` record and the tree diff lists the added path → step 4 of the attempt-2 landing order ("C2 consistency at the final REV exits 0") fails |

Measured in the fixture clone (receipt `receipts/counter-walks.txt`, sha256
`ccb4b707a6917f45cb213822635c3dec4a0a2a5dc866f61a1d1ea4fd2c5d7a1e`):

- branch `c3-in-frozen` (`94749500`, adds the file at the claim's literal path):
  C1 `frozen_drift -> ["tools/round-50/sqfs-triage-v5.py"]`; C2 `freeze_check ->
  {"code":"frozen_path_changed"}`, tree diff `["tools/round-50/sqfs-triage-v5.py"]`.
- branch `c3-outside` (`509a3d54`, adds `tools/round-50-c3/sqfs-triage-v5.py`): both walks clean.
- branch `c3-docs` (`d1c4dc05`, only SKILL.md registry row inside the markers + a
  `## Rule block 22` section): both walks clean.

**Mitigation (INTEGRATED while this seat ran).** The L1 landed exactly this move: `03f852b9`
moved the claim's instrument path to `tools/round-50-c3/sqfs-triage-v5.py` (hyphenated spelling;
this seat's fixture proved the equivalent `tools/round-50c3/` — both dodge C1's trailing-slash
prefix `'tools/round-50/'` and C2's `tools/round-50` pathspec), and `d71829bf` added the C3
pre-freeze amendments. Both commits touch only `plans/round-50-attempt2-claims.md` (frozen for
neither counter), and the frozen walk `435d41fd..d71829bf` over every C1 frozen path and the C2
`FROZEN` pathspecs is EMPTY (re-verified at tip `d71829bf` after the landings). The pending
`SKILL.md` registry row for `tools/round-50-c3/sqfs-triage-v5.py` (uncommitted at analysis time)
matches the F5 shape below. Keep the claim's own guard "no other .py/.sh lands under
`tools/round-50/`" — it now protects C1 as well as B9. Alternatives that would NOT work: any path
under `tools/round-50/`; a C1 freeze amendment (forbidden — "no new C1 freeze, no amendment");
scoring C1 before the C3 commit (the closure re-runs the counting command at the final tip).
For reference, the amendment that this seat's demonstration justified — amend the C3 claim
pre-freeze so the instrument lives outside both frozen families, in the predicate sentence,
counting command, C3-freeze bullet and registry row.

## The matrix (who writes what, who reads it)

| File | C1 (coverage) | C3 (depth) | Reader / atom | Binding that can flip |
|---|---|---|---|---|
| `tools/round-50/sqfs-triage-v5.py` | — | writes (claim text) | C1 `frozen_drift`; C2 `freeze_check` + B9 census | **F1: any post-freeze add under `tools/round-50/` = C1 exit 2 + C2 frozen_path_changed** |
| `tools/round-50-c3/sqfs-triage-v5.py` (proposed) | — | writes | C2 B9 (optional: outside census prefixes); nothing else | none, if the claim text is amended pre-freeze |
| `SCORECARD.md` | Owned-axes coverage row head 139/139 → 140/140 (same commit as the entry); capability row; attempt-2 section | C3 attempt-2 section | C2 B1 (coverage row + README map + knowledge count), B2 (calibration row), B3/B4/B5/B10/B11 via `## Record corrections — round 50`, battery `mutations()`/`_line_of` whole-file scan | B1 flips on wrong/absent head, unmapped stem, duplicate `| coverage |` row. B3-B5/B10/B11 flip on a second corrections section, duplicated correction lines, `- B<n>` decoy bullets, or the corrections section no longer being the file tail (see F3) |
| `LOG.md` | one entry | same or second entry | nothing reads it | none (confirmed: no C1/C2 atom reads LOG.md) |
| `SKILL.md` | **no edit needed** (confirmed: the C1 counter reads only PROVINCE/entry/SOURCES/README + frozen tools) | rule block 22 + one registry row inside `<!-- instrument-registry v2 -->` markers | C2 B9 (`registry_region`, `meaning_classes`, entry/selftest/pin regexes); round-48 `census2.json` property noted, old counters not re-run | B9 flips if: markers doubled/reversed, row outside markers, inside fence/comment (`vis` strips both), ≠7 cells, kind not `gate|probe`, verdict map not three distinct 0/1/2 meanings (placeholder text caught), selftest cell not `<interp> <path> ... --selftest` or `none — <reason>`, pinned cell naming no path; a second row for a census path flips B9 |
| `PROVINCE.md` | new `## Round-50 additions to Core` section + `Round-50 frontier note` line | possibly round-49 row residue (recommend: do not touch) | C1 bindings `province_core_section`/`province_core_row`/`frontier_note` (whole-file line scan for the note) | row's first cell must match `squashfs_v4_le` (word-bounded), row must name an `AVM marker` word and cite the full entry path; the note line needs the literal `Round-50 frontier note`, the stem, and an `LE-AVM`/`LE AVM`/`AVM-LE` token outside the stem; a second `## Round-50 additions to Core` heading is read by `section()`'s first-match — keep exactly one |
| `corpus/README.md` | coverage-map row naming the backticked stem | — | C1 `coverage_map_row`; C2 B1 `map_token` over every knowledge file | row must be a `|` line **inside `## Coverage map`** (`section()` stops at the next `## ` — an end-of-file append is invisible; measured, see F2); token = `` `stem` `` / `knowledge/stem` / `corpus/knowledge/stem`, optional `.md` |
| `corpus/SOURCES.md` | rows S243/S244/S245/S249 (11 cells; opened 2026-10-28 or -10-29; used-by cites the entry path or stem) | — | C1 `sourced` binding; C2 B6/B7/B8 read the correction rows by `supersedes S...` teaches; `registry_rows` duplicate-id check | new rows must not duplicate existing ids or disturb S246/S247/S248; the C1 binding checks `len(cells)==11`, `c[8]` opened date, `c[10]` used-by containing the entry path/stem |
| `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` | the entry | — | C1 `entry_present` + `source:` scan; C2 B1 counts it and maps it | `source:` lines at column 0 citing S-ids (`S\d{3,}`); the stem is frozen-counter-pinned — the `2026-10-29-r50-le-avm-hsqs-core` name from the claims first draft fails `entry_present` |
| `tools/round-50/` (frozen family) | reads (frozen) | must NOT write | C1 `frozen_drift`; C2 `freeze_check`; B10 exports the REV tree to run the r49 selftest | any A/M/D under the prefix after `435d41fd` flips both counters |

## F2 (measured) — the README coverage-map row must land inside the section

First validation run of the simulated landing scored C2 B1 red:
`knowledge files not mapped in README Coverage map: ['corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md']`
because the draft row was appended at end-of-file, outside `## Coverage map`
(receipt `receipts/landing-validation.txt` first run, sha256
`02cefa8a41b7c12ecc88016d253f3ab8926e989b290a574629d2c3b13b7c5855`). Fixed by inserting the
row as a table line immediately after the map's header separator; re-validated green.

## F3 (measured) — SCORECARD tail order is load-bearing for the C2 battery

With the attempt-2 section appended AFTER `## Record corrections — round 50`, the battery's five
`duplicate line` mutations (B3/B4/B5/B10/B11, `c2-record.py` `_line_of`/append-at-EOF) escape the
corrections section (`corr()`/`sections()` stop at the next `## ` heading) and fail to flip their
atoms: `failing=["B3 duplicate line -> red [] noop []", ... "B11 duplicate line ..."]`
(measured, same receipt file). The real file's tail IS the corrections section (`grep '^## '
SCORECARD.md | tail -1` → `3790:## Record corrections — round 50`), which is how attempt-1 C2
passed its battery. **Landing rule: insert new round sections BEFORE `## Record corrections —
round 50`; never append any `## ` heading after it.**

## F4 — SCORECARD bullet hygiene

`_line_of` (battery mutation source) scans the WHOLE file for `^ {0,3}- (B\d+)` and returns the
first hit; `corr()` requires exactly one corrections section and one line per atom. New sections
must therefore: use bullets like `- **C3:**`, never `- B3 ...`; not add a second
`## Record corrections — round 50`; not touch `## Round 48` / `## Round 49` sections
(B3/B4/B5/B11 keep-sentences and section-equality checks).

## Safe landing order (all commits descend from `6f4aba63`; C1 freeze `435d41fd` fixed)

1. **C3 freeze commit:** `plans/round-50-attempt2-claims.md` already amended in-lane (`03f852b9`,
   path → `tools/round-50-c3/…`; `d71829bf` pre-freeze amendments) + add the instrument + one
   registry row (inside the
   markers, 7 cells, shape per F-table) + C3 SCORECARD section inserted before the corrections
   heading + one LOG entry. Controls + before-run receipts under `.ufo/waves/round-50/` (unfrozen).
2. **C3 after-run commit:** SKILL.md rule block 22 lands; after-run receipt. (SKILL.md edit is
   drift-free for both counters — measured branch `c3-docs`.)
3. **C1 landing commit (one commit):** after-receipts + run receipts under
   `corpus/evidence/round-50/c1/`, the entry, PROVINCE section + frontier note, README map row
   inside the section, SOURCES S243-S245/S249, coverage head 140/140 + capability row + attempt-2
   section before the corrections heading. Then the L1 runs the C1 counting command at the tip.
4. **C2 consistency** at the final tip (`--battery`): all 11 atoms green, `failing []`.

C1 and C3 are verifiable without each other once F1 is fixed; the order above is the claims
doc's order with the path fix.

## Single riskiest coupling + mitigation (summary)

F1: the C3 instrument path vs the frozen C1 `FROZEN_PREFIXES` and C2 `FROZEN` trees. It is the
only coupling that cannot be repaired by drafting care after the C3 freeze, because both counters
walk the commit RANGE `435d41fd..REV`, not the endpoint tree — deleting or moving the file later
still leaves the `A` record in range ("a later restore does not un-block", c1 docstring
`:277-279`). Mitigation: move the instrument to `tools/round-50-c3/sqfs-triage-v5.py` and amend
the claim text in the same C3-freeze commit. Cost: one unfrozen file's path string; benefit: both
frozen counters keep their walks clean (measured).
