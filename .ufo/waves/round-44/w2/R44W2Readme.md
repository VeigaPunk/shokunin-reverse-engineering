# R44W2Readme — `corpus/README.md` round-44 entry and command A (wave-2 falsification)

Seat `R44W2Readme`, role reviewer, axes coverage / depth / calibration. Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base `c29360e3`, freeze
`c48f8a4b`, measured revision `55bcce69`, tip at dispatch `c86ea508`, tip at run
`8bb1090a` (lane clean except the wave's own `.ufo/.../w2.ready*` untracked files).

Nothing in this seat edited a claim, counter, rubric, frozen byte or production doc.
All values below are from commands whose stdout is kept under
`.ufo/waves/round-44/w2/artifacts/R44W2Readme/` (`receipt.json` carries argv, exit
codes, stdout sha256 and wall time).

## 0. Verdict in one paragraph

The three README rows that name `2026-10-28-r44-squashfs-v1v2-core` all read
**measured / not promoted** (`README.md:104`, `:224`, `:275`); none reads as Core,
and no other README row implies a v1/v2 promotion. Command A is stable and green at
base, freeze, measured revision, `c86ea508` and the tip: `138/138` files mapped with
`missing []`, `dangling []`, `21/21` rule blocks at every post-landing revision
(`137/137` before the entry landed). The entry-cell audit shows the 138 are real map
rows, not stems matched out of prose. Six defects follow; none overturns the C1
honest stop or the R44-C2 score, but D1–D3 are record-precision issues the L1 should
act on, D4–D5 are defects in the R44-CL1 fix itself, and D6 is a one-line wording
imprecision.

## 1. Commands run (exit code, stdout sha256, wall)

| id | command | rc | stdout sha256 | wall |
|---|---|---|---|---|
| cmdA-base | `python3 - c29360e3 < SCORECARD recipe A` | 0 | `66a78f75…338529` | 0.083 s |
| cmdA-freeze | `python3 - c48f8a4b < recipe A` | 0 | `2aecd61e…c93d34` | 0.081 s |
| cmdA-55bcce69 | `python3 - 55bcce69 < recipe A` | 0 | `b17d3c1c…d3141f3` | 0.085 s |
| cmdA-c86ea508 | `python3 - c86ea508 < recipe A` | 0 | `087e8465…a21637f3` | 0.080 s |
| cmdA-tip | `python3 - 8bb1090a < recipe A` | 0 | `80a7e347…e13e2ec4` | 0.079 s |
| preflight-55-pathspec | `python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4 --rev 55bcce69 --pathspec tools/round-44` | 0 | `c2cab50a…4f9e5ee4` | — |
| preflight-c86ea508-pathspec | same, `--rev c86ea508` | 1 | `dff05409…f059eb6b` | — |
| preflight-tip-pathspec | same, `--rev 8bb1090a` | 1 | `f4dc5085…1645dfd` | — |
| preflight-55-default | same but **no** `--pathspec` | 1 | `12681996…c99d25` | — |
| provenance-joint | import `tools/round-44/c1-counter.py`, call `provenance_ok`/`trusted_run_root` | 0 | — | — |
| cmdA-fitness-fixture | `python3 - <fixture rev> < recipe A` (red then green) | 0 / 0 | — | — |

The recipe itself is the frozen bash block in `SCORECARD.md` `## Measurement recipes`
A, run verbatim from the lane root with `REV` substituted. Wall time is the shell
`$EPOCHREALTIME` delta around the single `python3` invocation.

`cmdA-55bcce69`:
`{"citation_resolved_rules": 21, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 138, "mapped": 138, "missing": [], "revision": "55bcce69…", "rule_blocks": 21}`

`cmdA-tip`:
`{"citation_resolved_rules": 21, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 138, "mapped": 138, "missing": [], "revision": "8bb1090a…", "rule_blocks": 21}`

## 2. Every README row naming the round-44 entry

`grep -n 'r44\|round 44\|round-44' corpus/README.md` returns exactly three lines.

| line | section | wording (code spans flattened) | measured/not-promoted? | cites S112/S138/S139? |
|---|---|---|---|---|
| 104 | `## Coverage map` (row: `\| SquashFS v1/v2 through REA (round 44) \|` stem `\| state \|`) | `**Measured, not promoted** — REA 6.5.0 extract-firmware matched 4/4 standard v1.0/v2.0 fixtures against the independent unsquashfs 4.7.5 oracle, but R44-C1's frozen claim required an evidence-tree parameters.output_directory while its counter requires /kaidoku-r44/ scratch provenance; the score is not admitted and v1/v2 remain Frontier` | yes (state cell) | no |
| 224 | `## Knowledge` index | `SquashFS v1/v2 measured through REA on four standard fixtures (4/4 counter result); not promoted because the frozen R44-C1 claim and counter disagree on output-directory provenance; no Core claim \| S112, S138, S139; receipts corpus/evidence/round-44/c1/; counter tools/round-44/c1-counter.py` | yes (`no Core claim`) | yes (`S112, S138, S139`) |
| 275 | `## Frontier` note | `SquashFS v1/v2 was measured on four standard fixtures but **remains Frontier** (R44-C1 honest stop: frozen-claim/counter output-directory provenance mismatch; 2026-10-28-r44-squashfs-v1v2-core)` | yes (`remains Frontier`, stronger) | no |

Source-id convention: the whole 95-line coverage map contains exactly two S-id
references (`S084`, `S087`); no `## Frontier` line carries one. So "cites
S112/S138/S139" is only part of this document's convention for the Knowledge index
row. The coverage-map row and frontier note cite the entry stem/path, which is what
the frozen C1 counter's `coverage_map_row` binding actually reads
(`tools/round-44/c1-counter.py:2188-2190`, truthy at 55bcce69). If wave-2 expected
all three rows to carry the three S ids, that expectation is not this document's
convention and is not supported by any counter binding.

No other row in the coverage map, the Knowledge index, the Lessons table or the
Frontier list names the entry or asserts v1/v2 Core. `SquashFS v1/v2` does not appear
as a Core row anywhere at the tip (`grep -i core | grep -i 'v1/v2'` returns only the
round-42 v3 row and the round-44 measured row).

## 3. Command A: tip vs measured revision, and the anchor revisions

| rev | knowledge_files | mapped | missing | dangling | citation_resolved_rules | rule_blocks | coverage | depth |
|---|---|---|---|---|---|---|---|---|
| base `c29360e3` | 137 | 137 | `[]` | `[]` | 21 | 21 | 10.0 | 10.0 |
| freeze `c48f8a4b` | 137 | 137 | `[]` | `[]` | 21 | 21 | 10.0 | 10.0 |
| measured `55bcce69` | 138 | 138 | `[]` | `[]` | 21 | 21 | 10.0 | 10.0 |
| `c86ea508` | 138 | 138 | `[]` | `[]` | 21 | 21 | 10.0 | 10.0 |
| tip `8bb1090a` | 138 | 138 | `[]` | `[]` | 21 | 21 | 10.0 | 10.0 |

This reproduces `SCORECARD.md:3511` (`137/137` at the freeze tree, `21/21`,
`SKILL.md:81-543`) and `SCORECARD.md:3524` (`138/138` at `c86ea508`) exactly. The
`README.md` coverage map did not change between `55bcce69` and the tip
(`git diff 55bcce69..8bb1090a -- corpus/README.md` is empty), so the measured-revision
and tip readings are one artefact.

**Attack — is `coverage 10.0` vacuous?** No. The recipe counts a stem anywhere in
the `## Coverage map` section, so a stem that only appears in a row's prose would
still count. I re-derived each map row's *entry cells* (a cell whose every comma-token
is exactly `` `(knowledge/)?<stem>` ``) at both revisions: 138 stems in entry cells,
`missing_no_entry_cell []`, `entry_cell_no_file []`, `prose_only_stems []`
(`artifacts/R44W2Readme/entry-cell-audit-{tip,55bcce69}.json`). So every file has its
own row and no count comes from prose.

**Attack — can the recipe go red?** Yes. A throwaway fixture (`mktemp` under scratch,
`git init`, toplevel asserted) with one unmapped file, one ghost map row and one
out-of-range + one absent citation prints
`{"coverage_score": 5.0, "missing": ["2026-10-02-beta"], "dangling": ["2026-10-03-ghost"], "citation_resolved_rules": 1, "rule_blocks": 3, "depth_score": 3.33}`
(the `git show` of the absent file surfaces as a fatal on stderr, rc 0); after
repairing the map and the citations it prints `10.0` / `10.0` / `3/3`
(`artifacts/R44W2Readme/fit-red.json`, `fit-green.json`). The lane's green is therefore
a real two-sided result, not a pass-by-construction.

**Fragility (residual risk, not a defect this round):** the recipe's stem regex is
hard-coded to `2026-10-\d{2}-…`. A knowledge file outside October 2026 would be
reported as `missing` and a map row for it as unmapped (observed: a fixture using
`2026-01-01-*` stems gave `mapped 0`, `missing [both files]`). Every lane file today
is `2026-10-*`, so the round's numbers are unaffected.

## 4. Dangling / missing at the tip

- `dangling` (map stem with no knowledge file): **none** (`[]`).
- `missing` (knowledge file with no map row): **none** (`[]`).
- 138 map-bearing stems (unique), 138 knowledge files, 90 non-header table rows across
  `## Coverage map`. The entry cells carry 140 stem occurrences (two stems are mapped
  twice): 45 in the legacy continuation rows whose first cell is
  `` `knowledge/<stem>` `` and 95 in the `section | entries | state` rows. All resolve.

## 5. Attacks on the record

### 5.1 A map row that reads as Core: not at the tip; it exists in history
At `4cc1ac11` (the precursor landing) `corpus/README.md:104` read
`**Core** — rea-agents 6.5.0 extract-firmware …` and `:275` read
`SquashFS v1/v2 is **Core**`. Commit `55bcce69` ("record C1 honest stop on frozen
provenance mismatch") rewrote all three locations to measured/not-promoted
(`git show 55bcce69 -- corpus/README.md`). The current tree is clean; a reader of the
tip cannot see the earlier Core state except through git history. Whether that
withdrawal is disclosed: yes in `LOG.md:3201`, `SCORECARD.md:3525`, `PROVINCE.md:430`
and the entry (`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:224` names the
`4cc1ac11` counter output and `met_target true`); **not** in the README rows — see D2.

### 5.2 C1 verdict at the measured revision: confirmed
`corpus/evidence/round-44/c1/counter-at-4cc1.json` = `exit_code 0`, `met_target true`,
`bindings_false []`, `frozen_path_changed []` at `4cc1ac11`.
`.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` = `exit_code 1`,
`carriers_matched 4`, `met_target false`, `frozen_path_changed []`, with exactly three
false bindings: `province_core_section`, `province_core_row`, `frontier_note`
(every per-carrier clause and `run_provenance_ok`/`evidence_id_ok` true for all four
carriers). All four committed receipts carry
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…/rea-out`; none carries the
`corpus/evidence/round-44/c1/` form the frozen amendment requires. The stop therefore
does follow from the frozen text, and the three false bindings are exactly the
promotion bindings the round declined to claim — consistent, not contradictory.

### 5.3 "No run can satisfy the whole frozen text": overstated (D3)
The frozen text has two `parameters.output_directory` clauses: the wave-1 amendment
item 3 requires it to "name a `corpus/evidence/round-44/c1/` path", the predicate
requires it to "name this round's `/kaidoku-r44/` scratch segment". The counter
implements only the second (`tools/round-44/c1-counter.py:1176-1183`,
`PROV_SEGMENT = '/kaidoku-r44/'` at `:258`). Under a surface (substring) reading one
value satisfies both: `/fast/scratch/hyaku/kaidoku-r44/<run>/corpus/evidence/round-44/c1/<id>`.
I imported the frozen counter and called its own function:

```
actual receipt            provenance_ok=True   names_evidence_segment=False
lane evidence (abs/rel)   provenance_ok=False  names_evidence_segment=True
nested scratch + segment  provenance_ok=True   names_evidence_segment=True   trusted_run_root=…/kaidoku-r44/<run>/corpus/evidence/round-44/c1
```

(`artifacts/R44W2Readme/provenance-joint-satisfiability.json`). So "no run can satisfy
the whole frozen text" (`LOG.md:3201`) / "no real run can satisfy" (`SCORECARD.md:3525`)
is true only under the *referential* reading — the field must be the committed evidence
path, not merely contain that segment. The stop is still the correct call (a nested
scratch path would defeat the amendment's intent and would be a crafted path), but the
record's absolute wording is falsifiable and should be qualified at the next touch.
Do not rewrite the frozen claim.

### 5.4 Measured-at-55bcce69 + M44-2: honest and sufficient, with one README gap
- `c86ea508` changes 8 files under the frozen `tools/round-44/` directory, all status
  **M** (modified; none A) — `git show --name-status c86ea508 -- tools/round-44`.
- The claim's own freeze rule is a range rule (`FREEZE..REV` walk + blob backstop), so a
  score at `55bcce69` is admissible even though a later commit violates the freeze;
  the preflight at `55bcce69` is `clean` (rc 0) and at `c86ea508`/tip is
  `frozen_path_changed` (rc 1, 8 touched + 8 blobs). This is exactly what
  `SCORECARD.md:3530`, `LOG.md:3203` and the lesson header state, and it is the correct
  reading of the frozen rule — not a dodge.
- Sufficiency: the record says the scores are at `55bcce69` and that the tip is
  inadmissible, in the lesson header, `SCORECARD.md:3521/3530` and `LOG.md:3201/3203`.
  The gap is at README level only (D1/D2); the README is not the place the claim's
  measured revision is declared, but it is the corpus index a reader hits first.
- The R44-CL1 fix does catch the violation **when given the pathspec**
  (`--pathspec tools/round-44`): red at `c86ea508` and at the tip, green at `55bcce69`,
  and on a fixture it catches an added file (`status A`), a modified file plus its blob
  backstop, is clean at the freeze rev, and exits 2 on an unknown rev. Its defects are
  D4/D5.

## 6. Numbered defects (for the L1)

**D1 — `corpus/README.md:104` (and `:224`): the round-44 row does not name the measured
revision, so its "4/4" is not reproducible at the tip.**
Command: `python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4 --rev 8bb1090a --pathspec tools/round-44`
→ **exit 1**, `verdict frozen_path_changed`, `touched 8`, `blob_changed 8`. Committed
receipt `.ufo/waves/round-44/l1/c1-score-at-tip.json` → `exit_code 2` at `c86ea508`.
Observed: the README row's `matched 4/4` and `score is not admitted` hold only at
`55bcce69` (`c1-score-at-55bcce69.json`: `carriers_matched 4`, `met_target false`,
`exit_code 1`); the row does not say so. Suggested action: append (never rewrite) a
dated clause naming `55bcce69` and the tip's `exit 2 frozen_path_changed` (M44-2).

**D2 — `corpus/README.md:104` and `:224` omit the instrument-green precursor.**
Command: `/usr/bin/jq '{exit_code,met_target}' corpus/evidence/round-44/c1/counter-at-4cc1.json`
→ `{"exit_code":0,"met_target":true}` at `4cc1ac11`. The README says "the score is not
admitted" / "(4/4 counter result); not promoted" without saying the frozen counter had
already returned `met_target true` and that the withdrawal is a record-level decision
overriding the instrument. The precursor is disclosed at `LOG.md:3201`,
`SCORECARD.md:3525` and the entry `:224`, so the lane record is not silent — only the
README is. Suggested action: one dated clause in the README row, pointing at
`counter-at-4cc1.json`.

**D3 — `LOG.md:3201` / `SCORECARD.md:3525`: "no (real) run can satisfy the whole frozen
text" is an overstatement.**
Command: import `tools/round-44/c1-counter.py` and call `provenance_ok` →
`True` for `/fast/scratch/hyaku/kaidoku-r44/run/corpus/evidence/round-44/c1/v1le`,
which also contains the amendment's `corpus/evidence/round-44/c1/` segment
(`artifacts/R44W2Readme/provenance-joint-satisfiability.json`, rc 0). Observed: the
frozen text is jointly satisfiable on a literal reading; unsatisfiability holds only
under the referential reading. Suggested action: qualify the sentence when the lesson
or SCORECARD is next touched ("no run satisfies it under the reading that the field is
the committed evidence path"), leaving `plans/round-44-claims.md` frozen as is.

**D4 — `tools/round-45/frozen-path-preflight.py:29-30,69`: the documented default is a
false red.**
`--pathspec` help says "Default: none (tree backstop only)", but with no pathspec the
`git log` walk is unfiltered and the tree backstop is skipped (`if pathspec:` at
`:69`). Command:
`python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4 --rev 55bcce69`
→ **exit 1**, `verdict frozen_path_changed`, `touched 110`, `blob_changed 0`, including
`PROVINCE.md`, `SCORECARD.md`, `corpus/README.md` — files the frozen-path section marks
**NOT frozen**. Observed: a caller who wires the gate without `--pathspec` reds every
legitimate landing commit, which is the failure mode that invites ignoring the gate.
Suggested action: default to "no opinion" (require at least one `--pathspec`, or exit 2
`no_pathspec`), and either implement the documented tree backstop or delete the phrase.
Sibling `R44W2Preflight` D-2 cites the same two lines but frames it as misleading help
text; the measured consequence is stronger — the unfiltered walk is a false red on a
*clean* revision, so a wiring that omits the pathspec would block legitimate landings.

**D5 — `tools/round-45/frozen-path-preflight.py:2-8,28`: the tool cannot run "before a
commit".**
The docstring says it is "red before a commit that touches a claim's frozen paths" and
"meant to run on every candidate revision BEFORE the commit is treated as landed", but
its only revision input is `--rev` (`:28`), which must name an existing commit. Command:
the fixture run (`pf-fixture-*`) → a post-commit revision is the smallest evaluable
unit; a pre-commit (index) mode does not exist. Observed: R44-CL1's "wire it into the
round's commit sequence" is achievable only post-commit/pre-close, which the docstring
does not say. Suggested action: add an index/`--index` mode or reword to "before the
commit is treated as landed (post-commit, pre-close)".

**D6 — `corpus/lessons/round-44.md:16`: "added/edited 8 files" is imprecise.**
Command: `git show --name-status c86ea508 -- tools/round-44` → 8 × `M`, no `A`. Low
severity (the files were already at the freeze and were edited); "wrote 8 files" is
accurate. Suggested action: say "modified 8 committed control fixtures".

## 7. Residual risk and verification gaps

- **Not re-executed here:** the C1 and C2 frozen counters. Their values in this report
  are read from committed receipts at `.ufo/waves/round-44/l1/`; re-derivation is other
  seats' instrument. I re-executed only command A and the round-45 preflight.
- **No `lsp` device is mounted in this seat** (`xd://lsp` → "No such tool"). The
  caller/definition checks here are `git`-object and `grep` checks over Markdown and
  Python; no language server exists for these files, so no semantic claim rests on grep.
- Command A cannot distinguish "mapped" from "mapped correctly": a row that names the
  right stem but describes the wrong thing still scores 10.0. The entry-cell audit only
  proves every stem has a row. This is the recipe's known shape, not a round-44 defect
  (D-24 mitigation lives in the C2 content arm).
- `coverage 10 → 10` is arithmetically forced at saturation: 138/138 was 137/137 before
  the entry. It is not evidence of new capability, and the round does not claim it is
  (`SCORECARD.md:3528`: "the numeric axis cannot rise above 10").
- The README row compresses the oracle-independence caveat to "independent
  `unsquashfs` 4.7.5 oracle"; the claim (and D-09) discloses the squashfs-tools lineage
  risk, and the entry and S139 carry it. The README does not assert complete producer
  independence, so this is a compression, not an overclaim — recorded, not filed as a
  defect.
- Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2Readme` (including both throwaway
  fixture repos) was removed before this file was written; no `/tmp` path is cited.
- The preflight demonstrates one frozen-path group (`--pathspec tools/round-44`). The
  frozen-paths section lists further groups — `plans/round-44-claims.md`,
  `tools/round-42/fixtures.json`, the two port-source counters, the four carrier bins,
  the four oracle trees, `tools/round-44/control-fixtures/**`, the held-out receipt
  inputs, `SKILL.md`, `corpus/SOURCES.md` and C2's rubric-pinned score receipts — and
  nothing yet invokes the gate once per group, so "wired" remains a manual procedure.
  `R44W2Preflight` D-3 carries that finding.

## 8. Receipt

`.ufo/waves/round-44/w2/artifacts/R44W2Readme/receipt.json` (seat, argv per command,
exit codes, stdout sha256, wall). Raw stdout kept beside it:
`A-<full-rev>.out` for base, freeze, `55bcce69`, `c86ea508` and tip (`8bb1090a`) plus
`A-tip-again.out`; `preflight-{55,c86,tip}-pathspec.json`;
`preflight-55-default.json` (and its earlier duplicate `preflight-nopathspec-55.json`);
`pf-fixture-*.out|.err`; `entry-cell-audit-{tip,55bcce69}.json`;
`provenance-joint-satisfiability.json`; `fit-red.json`; `fit-green.json`.
