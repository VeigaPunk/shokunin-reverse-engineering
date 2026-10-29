# ExecB1Impact — C2 B-atom couplings at the planned attempt-2 landing

**VERDICT: the planned landing keeps C2 green (exit 0, `mismatches 0`, 11/11 atoms, battery
clean) — but only if two text rules are honoured, and one is NOT in the attempt-2 plan text:
the round-50 `## Record corrections` section must remain the LAST `##` section of
`SCORECARD.md`, and the Owned-axes coverage row must lead with `140/140 knowledge files
mapped`.** Measured, not assumed: an otherwise-identical landing whose attempt-2 section sits
*after* the corrections section exits **1** with a red battery (5 mutation arms), while the
same landing with the attempt-2 section *before* the corrections section exits **0** with
`battery.failing []`. Every other atom is unaffected by the landing text.

Nothing was run under REA. No lane file outside this seat's directory was written. The C1
freeze `435d41fd4ad9211d1579fc447936fb33d2b74467` was not touched.

---

## Findings table

| # | finding | evidence (exact command; exit; sha256; UTC) | severity |
|---|---|---|---|
| F1 | **SCORECARD section ORDER is a C2 gate.** `c2-record.py` locates the correction lines with `unique_section(vis(SCORECARD.md), '## Record corrections — round 50')`; `sections()` matches a `## ` heading by `startswith`, so a second section whose heading *starts with* the same text is counted as a second copy of it. The attempt-1 landing put `## Record corrections — round 50` last; an attempt-2 landing that appends its own section after it makes `unique_section` fail and turns **B3, B4, B5, B10, B11 red** (`2 `## Record corrections — round 50` sections, want 1`). | `python3 -I -B tools/round-50/c2-record.py --root <clone> --rev <v5> --freeze <v5> --work <S>/w-v5-dupcorr` — exit 1, `mismatches 5`, RED B3/B4/B5/B10/B11; receipt `receipts/v5-dupcorr.txt` (sha256 of stdout `…`, see artifacts) | **blocker for the landing text** |
| F2 | **A/B proof of F1's mechanism, with the corrections section last vs. not.** Two clones, byte-identical landing text except section order: `v7-order-last` (attempt-2 section appended at EOF, after the corrections section) → **exit 1**, `mismatches 0` but `battery.failing = ['B3 duplicate line -> red [] noop []', 'B4 …', 'B5 …', 'B10 …', 'B11 …']`; `v8-order-before` (attempt-2 section inserted *before* the corrections section) → **exit 0**, `mismatches 0`, `battery.failing []`, `mutation_count 52`, `do_nothing_red` = all 11. The red arms are the *duplicate-line* mutations: the battery appends a duplicate `- Bn …` line at the end of `SCORECARD.md`, and when the corrections section is not last that duplicate lands outside the section the counter reads, so the atom no longer flips. The landing is therefore green on the atom verdicts but **red on the battery** — the exact shape the attempt-2 plan's step 4 (`exits 0`) requires. | `runorder.sh` receipts `receipts/v7-order-last.txt` (stdout sha256 `2bf78c7c50a9feebee901e3881d50d094a36a0d6b92eab24ce724bbdf9c0f6f4`) and `receipts/v8-order-before.txt` (stdout sha256 `4a2a25c408d3316315150382b2c46d22dad7f14f4c000c9bda5c13f5686c2a24`); 2026-10-29T20:56:09Z→20:58:14Z | **blocker** |
| F3 | **B1 needs `140/140` as the FIRST `N/N knowledge files mapped` phrase.** `b1` does `fr = re.findall(r'(\d+)/(\d+) knowledge files mapped', rows[0])` and compares only `fr[0]` with the `.md` count under `corpus/knowledge` at REV. Base count is **139**; the attempt-2 landing adds exactly one C1 entry → **140**. Landing the row with the old `139/139` first flips B1 red: `coverage row states 139/139, derived 140 knowledge files`. | `git ls-tree -r --name-only f890bbead20ca2c549487167f56876ae47f1e1a4 -- corpus/knowledge \| grep -c '\.md$'` → exit 0, stdout `139`; `v3-head139` run → exit 1, RED B1 with that text (`receipts/v3-head139.txt`) | must-fix (text rule) |
| F4 | **B1 has a SECOND clause the landing must satisfy: the README coverage map.** Every `.md` under `corpus/knowledge` at REV must be mapped by its backticked stem in `corpus/README.md` `## Coverage map`. Removing the new entry's row flips B1 red on that clause alone: `knowledge files not mapped in README Coverage map: ['corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md']`. The counter accepts `` `stem` ``, `` `knowledge/stem` `` or `` `corpus/knowledge/stem` ``, with or without `.md`. | `v4-nomap` run → exit 1, RED B1 with that text (`receipts/v4-nomap.txt`) | must-fix (text rule) |
| F5 | **The C3 instrument path must stay OUT of `tools/round-50/`.** Both frozen counters freeze that whole tree: `c1-counter.py` `FROZEN_PREFIXES = ('tools/round-50/',)` and `c2-record.py` `FROZEN = ('tools/round-50', 'plans/round-50-claims.md')`. An `A` status under either is drift. Measured with the counters' own derivations at a simulated landing: `tools/round-50/sqfs-triage-v5.py` → C1 `frozen_drift = ['tools/round-50/sqfs-triage-v5.py']` → C1 exit 2; C2 `freeze_check = ('frozen path touched in FREEZE..REV: … A tools/round-50/sqfs-triage-v5.py', 'frozen_path_changed')` → C2 exit 2. At `tools/round-50-c3/sqfs-triage-v5.py` both are clean (`drift []`, `freeze_check (None, None)`). | `c1drift.py` (imports the frozen counter's own `frozen_drift()`) on `clone-in` vs `clone-out`; C2 at the in-tree rev → exit 2 `frozen_path_changed` (`receipts/c2-inside.json`); C2 at the out-of-tree rev → exit 0 | **already mitigated** — the L1 committed `03f852b9` naming `tools/round-50-c3/sqfs-triage-v5.py`; this seat's independent measurement agrees |
| F6 | **B9's census is unchanged at 12 paths, so the new instrument needs NO registry row to keep B9 green — but if it lands in-tree it does.** `census_paths()` = `tools/round-49/**` `.py`/`.sh` at BASE + `tools/round-50/**` `.py`/`.sh` at REV, control fixtures excluded. `tools/round-50-c3/` is invisible to the `tools/round-50` pathspec (measured: `git ls-tree -r --name-only HEAD -- tools/round-50` → 0 hits for `round-50-c3`), so the out-of-tree instrument adds no census path and B9 stays green with the 54-row region untouched. If the instrument were in-tree, B9 turns red without a row: `tools/round-50/sqfs-triage-v5.py: no registry row`. | `v2-noreg` (in-tree, row deleted) → exit 1, RED B9 with that text (`receipts/v2-noreg.txt`); `v1-inside` (in-tree, row present) → exit 0, all 11 green (`receipts/v1-inside.txt`) | disclosed (L1 may still add the row as a gate-registration duty — it is outside the census and cannot break B9) |
| F7 | **The landing does not disturb any atom's BASE reads.** B2 (`BASE` closure-48, `BASE` c2-final/ctl-49 receipts), B3/B4/B5/B11 (`BASE` round-48/49 sections, `BASE` round-48 results + `w1/` tree, `BASE` receipts), B6/B7/B8 (`BASE` SOURCES + `BASE` snapshots, `REV` correction rows) all read their historical inputs at BASE, so editing the landing text cannot move them. The only REV-read surfaces the landing touches are `SCORECARD.md` (B1/B2/B3/B4/B5/B11), `corpus/README.md` (B1), `corpus/SOURCES.md` (B6/B7/B8), `SKILL.md` (B9) and the two B10 self-test files. | read-set map derived from the frozen source (`b1`…`b11` + `_row`/`keeps_sentences`/`_results48`); per-atom map in the artifacts section below | green by construction |
| F8 | **B10 is the one atom the landing can break silently.** B10 runs `tools/round-50/selftest-r49-c2.py` **from the REV bytes** and compares its committed expected file at REV. Both live under `tools/round-50/`, so they are frozen and cannot change — but the correction line `B10` in `SCORECARD.md` must keep `cases=40` and `expected_sha256=0a9ddec8…` (the sha256 of the frozen expected file). Landing a new `B10` line with a different count/hash flips B10 red. | `b10` reads `SELFTEST_PATH`/`SELFTEST_EXPECTED` at REV and re-derives `expected_sha256`; the correction line at the tip states `cases=40 expected_sha256=0a9ddec8dc917f835a609352218854f41b6038a17418962b3047dfc5b033c36f` | must-fix (keep the line) |
| F9 | **The corrections section must keep EXACTLY one `- Bn` line per atom.** `Ctx.corr()` requires one and only one `- B3 …`/`- B4 …`/`- B5 …`/`- B10 …`/`- B11 …` line, with exactly the named keys, inside the corrections section. Appending a second `- B3 …` line (even in a correctly-named section) makes `correction line B3 occurs 2 times` → red. | `b3`/`b4`/`b5`/`b10`/`b11` all call `c.line(atom, keys)`; the battery's own duplicate-line arms rely on this firing | must-fix (append-only) |
| F10 | **The L1's actual in-flight bytes already satisfy B9.** The frozen `b9()` was run directly against the lane worktree `SKILL.md` (sha256 `4d9d13f6…`, containing the L1's uncommitted registry row for `tools/round-50-c3/sqfs-triage-v5.py`) at HEAD `d71829bf`: **0 findings**, census still **12** paths. The row parses as 7 cells, one occurrence, no duplicate cell-0; the marker-bound region holds 55 rows. The C3 instrument is present at `tools/round-50-c3/sqfs-triage-v5.py` and `tools/round-50/` has no new `.py`/`.sh` — exactly the shape F5/F6 require. | `receipts/b9-live-l1-row.txt` (2026-10-29T21:01:51Z) | green as-is |

**Not run:** no REA, no `--data-run`, no vendor download, no `c1-counter.py` end-to-end run
(its frozen `frozen_drift()` derivation was exercised directly instead — that is the arm that
decides the path question); `tools/round-42/sqfs-triage-v4.py --selftest` was not run; the
round-48/49 older counters were not re-run (they are not gates this round, per
`plans/round-50-claims.md`).

---

## 1. B1 — the coverage head and the README row

**Counts.** Base `f890bbead20ca2c549487167f56876ae47f1e1a4`:
`git ls-tree -r --name-only f890bbead20ca2c549487167f56876ae47f1e1a4 -- corpus/knowledge | grep -c '\.md$'` → **139**
(exit 0). The attempt-2 landing adds exactly one knowledge file
(`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, the stem the frozen C1 counter
pins at `tools/round-50/c1-counter.py:377-378`) → **140** at the landing. No other wave-3
draft adds a `.md` under `corpus/knowledge/` (the lesson file is `corpus/lessons/round-50.md`,
outside the counted tree).

**The exact text the coverage row must lead with.** `b1` reads the single `| coverage |` row
of `SCORECARD.md` `## Owned axes` and takes `fr[0]` — the **first** match of
`(\d+)/(\d+) knowledge files mapped` in that row — comparing it to `(140, 140)`. So the row's
**first** such phrase must be:

```
140/140 knowledge files mapped
```

A landing that leaves `139/139 knowledge files mapped at the round-50 landing` as the first
phrase is red (F3). Because `fr[0]` is the only match compared, the later historical
fractions (`138/138`, `133/133`, …) are inert; but per sibling `CritB1Text` the trailing
"round 50 added no knowledge entry" wording is now false for attempt 2 and should be
reworded or scoped to attempt 1 — a documentation defect the counter does not catch, not a
B1 predicate defect.

**The second B1 clause.** The README `## Coverage map` must contain the new entry's stem in
backticks (F4). Any of these satisfy the counter's `map_token`:
`` `2026-10-28-r50-avm-le-squashfs-core` ``, `` `knowledge/2026-10-28-r50-avm-le-squashfs-core` ``,
`` `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core` `` (each with optional `.md`).
The C1 counter's own `coverage_map_row` binding wants the stem on a line starting with `|` in
that section — one row satisfies both atoms.

---

## 2. B9 — the registry region at the planned landing

**Derivation (the sibling seat's method, re-derived against the frozen bytes).**
`registry_region(t)` keeps the two marker lines visible
(`<!-- instrument-registry v2 -->` … `<!-- /instrument-registry -->`; one pair, lines 1715/1774
at the tip), takes every line between them matching `^ {0,3}\|\s*`` and keys it by cell-0
with the backticks stripped. At the tip the region holds **54** rows; the marker pair is
single and ordered (no row may sit outside the markers).

**Census.** `census_paths()` = every `tools/round-49/**` `.py`/`.sh` at **BASE** plus every
`tools/round-50/**` `.py`/`.sh` at **REV**, control fixtures excluded. At the planned landing
this is still **12** paths (6 round-49 + 6 round-50), measured at the simulated final
landing rev: the new `tools/round-50-c3/sqfs-triage-v5.py` is invisible to the `tools/round-50`
pathspec (`git ls-tree -r --name-only <rev> -- tools/round-50` → 0 hits for `round-50-c3`).

**Per-row requirements for the 12 census paths** (all satisfied today, re-verified green at
the tip): exactly one row each; exactly 7 cells; cell-1 opens `gate`/`probe`; cells 1–4 carry
an entry command naming the path; cell-2 parses as `0=…;1=…;2=…` with three distinct meanings
(exit 0 success / exit 1 not-met / exit 2 unevaluable, under the round-48 rule ported into
`c2-record.py`); cell-3 is either `<interpreter> <path> … --selftest` or `none — <reason>`;
cell-4 names a pinned path or `none — <reason>`.

**`sqfs-triage-v5.py` is the ONLY new `.py`/`.sh` under `tools/round-50/`** — and it is not
under `tools/round-50/` at all. Measured at the simulated final landing: the round-50 census
is exactly the six pre-existing paths (`c1-controls.py`, `c1-counter.py`, `c1-run.sh`,
`c2-record.py`, `fetch-vendor.py`, `selftest-r49-c2.py`) — no additions. **Constraint for the
L1: nothing else may land under `tools/round-50/`.** Any new helper there would (a) re-trip
the C1 freeze-drift arm (F5) and (b) enter the B9 census and need its own registry row.

---

## 3. Every other atom — what it reads, and whether the landing can flip it

Read-set map (derived from the frozen source; `BASE` = `7c678ae6…`, `REV` = the landing):

| atom | reads at BASE | reads at REV | can the planned landing flip it? | risk / mitigation |
|---|---|---|---|---|
| B1 | — | `SCORECARD.md` (Owned-axes coverage row), `corpus/README.md` (Coverage map), `corpus/knowledge/**.md` tree | **YES — twice** | Row must lead `140/140 …` (F3) and the README must map the new stem (F4). Both measured red when violated. |
| B2 | `corpus/lessons/round-48-verifier-spotcheck.md`, `.ufo/waves/round-49/l1/scores/c2-final.json`, `.ufo/waves/round-49/controls/ctl-c2-0-do-nothing.json` | `SCORECARD.md` (Owned-axes **calibration** row) | **YES, but only via the calibration row** | B2 requires the row to name `rejected-harmed`, the closure path, the `c2-final.json` path, and the literal `mismatches 9 -> 0` (the numbers re-derived from the BASE receipts: CTL-49 = 9, c2-final = 0). A landing that rewrites the calibration row (e.g. to "mismatches 11 -> 0" for round 50, or drops the round-49 receipt reference) flips B2 red. **Mitigation: leave the calibration row untouched.** |
| B3 | `SCORECARD.md` (round-48 section), `.ufo/waves/round-48/r48-w1-results.json`, `.ufo/waves/round-48/w1/**` | `SCORECARD.md` (correction section + round-48 section) | **YES, via the correction section and section order** | One `- B3 seats=… reports=… blocked=… aborted=… missing=…` line only (F9); the round-48 section must keep `all 75 seats settled`; a second corrections section breaks it (F1). |
| B4 | `SCORECARD.md` (round-48 section), closure-48 | `SCORECARD.md` (correction + round-48 sections) | **YES, same mechanism** | One `- B4 …` line, exactly the 8 named keys; round-48 section keeps `quality **improved on the instruments**` and `discernment **improved**`. |
| B5 | `SCORECARD.md` (round-48 section), closure-48, closure-49, `.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json`, `c2-final-33f65a91.json` | `SCORECARD.md` (correction + round-48 sections) | **YES, same mechanism** | The `- B5 receipt=33f65a91 tip=8847042a c1_sha256=… c2_sha256=…` line must survive unchanged, and the round-48 section must still NOT name `33f65a91`/`8847042a` (the atom checks both). |
| B6 | `corpus/SOURCES.md`, closure-48 | `corpus/SOURCES.md`, `corpus/lessons/round-50.md`, the two committed snapshots | **NO** (the correction rows S246/S247/S248 already exist and are untouched by the landing) | The landing's NEW SOURCES rows (S243/S244/S245/S249) must not open `supersedes S149 —` / `S147 —` / `S138 —`: `any_sup` counts any row whose teaches cell starts `supersedes S1xx` and requires exactly one. They must also not duplicate an existing id and must keep 11 cells. |
| B7 | `corpus/SOURCES.md` | `corpus/SOURCES.md`, `corpus/lessons/round-50.md`, `corpus/evidence/round-49/c2/popper.html` | **NO** | Same constraint; `used-by` must still list `corpus/lessons/round-50.md` and the snapshot pin must match. |
| B8 | `corpus/SOURCES.md` (S138's own line at BASE), `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` | `corpus/SOURCES.md`, the round-50 S138 snapshot | **NO** | S138's own line must be unchanged (append-only) and the correction row's census number must still match the BASE figure. |
| B9 | (registry is REV-only) | `SKILL.md` (marker-bound region) | **NO, at the planned landing** | The out-of-tree instrument adds no census path (F6). Only a new `.py`/`.sh` **under `tools/round-50/`** would (F5/F6). |
| B10 | — | `tools/round-50/selftest-r49-c2.py` + `.expected.json` (frozen) | **YES, via the correction line only** | The `- B10 selftest=… cases=40 expected_sha256=0a9ddec8…` line must stay exactly as-is (F8). The two files themselves are frozen and cannot change. |
| B11 | `SCORECARD.md` (round-49 section), closure-49 | `SCORECARD.md` (correction + round-49 sections) | **YES, via the correction section and section order** | One `- B11 …` line; the round-49 section must stay byte-identical to BASE (`a != b` is a mismatch) and must still carry `the non-author spot-check is pending`. |

**Cross-atom summary.** The landing text can only move **B1, B2, B3, B4, B5, B10, B11** — all
of them through `SCORECARD.md` (plus `corpus/README.md` for B1). B6/B7/B8/B9 are structurally
immune at the planned landing. Every red in the table above is a *text* rule, not a
structural one: the landing can be green, but only if the L1 keeps the existing correction
lines and their section intact and appends nothing after it.

---

## 4. The re-run command the L1 runs at the final REV

Exact argv (from the lane root; `<REV>` = the final landing commit):

```
python3 -I -B tools/round-50/c2-record.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev <REV> \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 \
  --battery \
  --work /fast/scratch/hyaku/kaidoku-r50/c2-w3 \
  --json-out .ufo/waves/round-50/l1/scores/c2-final-attempt2.json
```

`--battery` is required, not optional: without it the battery arm never runs and the
section-order defect (F2) is invisible — the run would report `mismatches 0` and exit 0 while
the landing is actually broken. With `--battery`, a green landing reports
`atoms_total 11`, `mismatches 0`, `battery.failing []`, `battery.do_nothing_red` = all 11
atoms, `exit 0`. The `--work` scratch must be under `/fast/scratch/hyaku/kaidoku-r50/` (the
counter refuses `/tmp`).

The matching C1 arm (the L1 runs it after the controls and the data run):

```
python3 -I -B tools/round-50/c1-counter.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev <REV> \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r50/c1-w3 \
  --carrier-cache /fast/scratch/hyaku/kaidoku-r50/carrier-cache \
  --json-out .ufo/waves/round-50/l1/scores/c1-final-attempt2.json
```

Its `frozen_path_changed` must be `[]` — the C1 counter's own `frozen_drift()` was exercised
at the simulated final landing and returns `[]` with the out-of-tree instrument
(receipt `receipts/c1-drift-final-landing.json`).

---

## 5. The lane state observed at yield (for the L1's landing)

At the time of this report the lane tip was `d71829bffbe35996872bc12350f87a7042f59d19`
("C3 pre-freeze amendments from wave-3 attacks"), with the C3 instrument present at
`tools/round-50-c3/sqfs-triage-v5.py` and the L1's registry row added to `SKILL.md` in the
worktree. Measured against those bytes:

- `tools/round-50/` has **no** new `.py`/`.sh` — the F5 drift arm is clean (C1
  `frozen_drift() = []` at the final landing simulation; the C2 `freeze_check` returns
  `(None, None)`).
- The B9 census is still **12** paths and the frozen `b9()` returns **0 findings** on the
  L1's actual `SKILL.md` (F10).
- `SCORECARD.md` is **not yet landed** for attempt 2: the coverage row still leads
  `139/139 knowledge files mapped at the round-50 landing` and the corrections section
  `## Record corrections — round 50` is still the last `##` section. Both are the correct
  *pre-landing* states; they must change together at the landing commit (F1, F3, F4).

**The landing commit therefore has exactly one safe shape**, and it is the one measured green
in section 6: the attempt-2 `SCORECARD.md` section inserted **before**
`## Record corrections — round 50`, the corrections section left **last**, the coverage row's
first `N/N knowledge files mapped` phrase changed to `140/140`, the README coverage map
extended with the new entry's stem, and no new `.py`/`.sh` under `tools/round-50/`.

---

## 6. Capstone — the full simulated landing, measured

`mkfinal.py` builds the complete attempt-2 landing in a fixture clone (C3 instrument at
`tools/round-50-c3/` + registry row + SKILL rule block 22 + C1 entry + PROVINCE section +
README row + SOURCES S243/S244/S245/S249 + coverage head `140/140` + attempt-2 SCORECORD
section **before** the corrections section + corrections section left last).

| arm | command | exit | result |
|---|---|---|---|
| C2 battery at the final landing | `python3 -I -B tools/round-50/c2-record.py --root <final-landing> --rev aa4edc906f0936b7c0870cff25c7a92a0230060f --freeze 435d41fd… --battery --work <S>/w-final --json-out <S>/receipts/final-landing.json` | **0** | `atoms_total 11`, `mismatches 0`, 11/11 atoms green, `battery.failing []`, `do_nothing_red` = all 11 |
| C1 drift at the final landing | `c1drift.py <final-landing> 435d41fd… aa4edc90…` (the frozen counter's own `frozen_drift()`) | 0 | `drift []` |
| B9 census at the final landing | `git ls-tree -r --name-only aa4edc90… -- tools/round-49 tools/round-50 \| grep -E '\.(py\|sh)$' \| grep -v control-fixtures` | 0 | 12 paths, unchanged |

---

## 7. Artifacts

Under `.ufo/waves/round-50/w3/ExecB1Impact/`:

| file | content |
|---|---|
| `impact.md` | this report (same text as the seat report) |
| `mklanding.py` | simulated landing builder (inside / outside instrument path) |
| `mkvariant2.py` | the five atom-isolation variants (v1-inside, v2-noreg, v3-head139, v4-nomap, v5-dupcorr) |
| `mkorder.py` | the section-order A/B builder (v7-order-last, v8-order-before) |
| `mkfinal.py` | the capstone final-landing builder |
| `runvariants.sh`, `runorder.sh` | receipt-recording runners (exact argv, exit code, stdout/json/stderr sha256, UTC start/end) |
| `c1drift.py` | calls the **frozen** `c1-counter.py`'s own `frozen_drift()` (imports the counter; no REA) |
| `receipts/` | every receipt (`*.txt` = command/exit/sha256/UTC; `*.json` = the counter's own output) |
| `receipts/atom-read-set.txt` | the per-atom BASE/REV read-set map of section 3 |
| `receipts/c1-drift-final-landing.json` | C1 drift at the simulated final landing (`drift []`) |

**Boundary kept.** Read-only on the lane tree: the only lane files written are this seat's
directory and this report. No REA run, no `--data-run`, no download, no commit/push/stage/
stash or any other mutating git in the lane or fleet repo — every fixture commit was made in
a `git clone --shared` scratch clone with `user.name`/`user.email` set in that clone only and
`git -C "$D" rev-parse --show-toplevel` asserted equal to the clone path before the first
commit. No tool was installed or upgraded. Scratch
`/fast/scratch/hyaku/kaidoku-r50/w3-ExecB1Impact` was removed after the receipts were
copied in. The disk guard was consulted before the clone work (exit 0).
