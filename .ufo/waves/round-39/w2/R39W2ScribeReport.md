# R39W2ScribeReport — round-39 landing, scribe/falsification seat

**Verdict: DEFECTS FOUND (record-level).** Neither predicate is falsified at its measured commit —
the C1 and C2 artifact sets I could check agree with their score files — but the round-39 record
contains a control-count mismatch in both claims, one kill-rule control whose evidence is bound to a
superseded, non-existent freeze revision, and a control id with two different committed outcomes.
Details D1–D4 below, quoted verbatim; D5 is a provenance limit and D6 an observed worktree
state already recorded by another seat — neither is a defect of the claims.

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read at HEAD
`e40a25df3987d881513de581112d2dad30605673`. Freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`,
controls `72359309a052284029f8e0331ef211a67fe4b13b`, base `a2f64e1da78afcf8cc39287106604dbcc270844c`,
C2 data `3c07eed7da595b815ce3064dcb12bd5c0788e564`, C1 receipts + Core landing
`6fdaf4f162aff156fcef0e52998a5469c64fd6f0`, record `52b0eb2907c704ed5f184c47b14c723208e5cbbc`.

## What I attacked, and what I did not

I attacked the **reportability and internal consistency of the landing**: whether the numbers the
round states are the numbers its committed receipts contain, whether the frozen paths are undisturbed,
and whether the control record supports "none meets its target". I did **not** re-run REA, unblob or
either counter (the wave-2 repro seats own execution provenance), did not run any campaign tool in
`/home/vgpnk/Projects/shokuknow`, and installed or updated nothing.

Method: read-only git (`show`, `log`, `diff`, `ls-tree`, `cat-file`, `merge-base`, `rev-parse`) plus
local Python over committed bytes. Exact commands and outputs: `checks.md` in the artifact directory.

## Drafted report sections

`report-body.md` (same directory) holds the four sections drafted for the round report — *Work
performed*, *Landed changes*, *Before → after measurements*, *Sources & frontier* — with a pointer
(`path:line` or commit) on every bullet. Nothing from it is filed by this seat.

## Findings

### D1 — C1 control count is 9 in the record and 10 in the evidence; the tenth is bound to a freeze revision absent from the lane

Verbatim:

- `git show -s --format=%s 72359309`: *"round-39: pre-data control receipts (C1 9 controls, C2 8
  controls; none meets target) + wave-1 results"*.
- `corpus/lessons/round-39.md:5-6`: *"Control receipts `72359309a052284029f8e0331ef211a67fe4b13b`
  (C1: 9 controls, C2: 8 controls; none meets its target)."*
- `plans/round-39-claims.md:8-9`: *"Frozen controls are scored with each counter before any claim data
  exists, and their receipts land in their own commit before the first data commit."*
- `.ufo/waves/round-39/controls/` holds exactly nine C1 receipts, numbered
  `ctl-c1-0,1,2,3,4,6,7,8,9` — there is no `ctl-c1-5.json`.
- `.ufo/waves/round-39/w1/artifacts/R39C1Controls/evidence/suite.json` (committed in the freeze) holds
  **ten** entries, `CTL-C1-0 … CTL-C1-9`, including `CTL-C1-5` with `rev == freeze ==
  bc533dda51015ae13fb11c8177e8d2f1a45fbd0a`, `mode in-freeze`, `counter_exit 1`, matched 0.
- `git cat-file -e bc533dda51015ae13fb11c8177e8d2f1a45fbd0a` → absent from the lane, so the counter
  bytes that scored CTL-C1-5 cannot be compared with the frozen `tools/round-39/c1-counter.py`.
- The claims' own kill rule names that control and that directory: *"…receipts added in the freeze
  commit itself (`.ufo/waves/round-39/w1/artifacts/R39C1Controls/`)"* (`plans/round-39-claims.md:72-78`).

Consequence: the stated count (9) and the scored set (10) disagree, and the one control the claims
name for the freeze-commit case was scored against a revision (`bc533dda…`) other than the freeze
`8fcda41c…`; that revision is not in the lane, so the control is not bound to the frozen rule.
[INFERENCE] `bc533dda…` is a pre-freeze draft commit; its counter, predicate and docs bytes were later
changed before `8fcda41c`.

### D2 — "C2: 8 controls; none meets its target" is neither the row count in the receipt nor free of a `met_target: true` row

Verbatim receipt `.ufo/waves/round-39/controls/ctl-c2-dev-scores.json`, `controls` object — ten keys:

| key | exit | matched | met_target |
|---|---|---|---|
| `CTL-C2-0-base-SKILL` | 2 | 0 | false |
| `FREEZE-table-informational` | 0 | 20 | **true** |
| `CTL-C2-1-catch-all` | 0 | 4 | false |
| `CTL-C2-2-gap-count-only` | 0 | 6 | false |
| `CTL-C2-3-gap-kind-only` | 0 | 10 | false |
| `CTL-C2-4-published-only` | 0 | 6 | false |
| `CTL-C2-5-round36-le-transcribed` | 2 | 0 | false |
| `CTL-C2-6-no-be-no-sr` | 2 | 0 | false |
| `CTL-C2-5-round36-le-transcribed.formatfix` | 0 | 8 | false |
| `CTL-C2-6-no-be-no-sr.formatfix` | 0 | 12 | false |

The claims' kill rule names seven controls (`CTL-C2-0 … CTL-C2-6`, `plans/round-39-claims.md:116-122`).
So "8" matches neither the named controls (7) nor the receipt rows (10, eight distinct tables), and
"none meets its target" fails if every row in the receipt counts: `FREEZE-table-informational` scores
20/20 with `met_target true` on the development envelopes. That row is the frozen table checked
against dev envelopes and is expected to score 20/20, so the sentence is presumably meant over the
seven shortcut controls — but as written it contradicts a row of its own receipt. The discriminating
pre-data baseline is 12/20 (`CTL-C2-6-no-be-no-sr.formatfix`), which the lesson does state.

### D3 — One control id has two committed outcomes, and the run that met the target is not reconciled

- `.ufo/waves/round-39/w1/artifacts/R39C1Controls/evidence/suite.json` → `CTL-C1-3`: `counter_exit 0`,
  `expected_exit 0`, `verdict as-expected`, matched 6; `w1/R39C1Controls.md:25`: *"**exit 0, 6/6 as
  drafted** — no receipt-only refusal exists"*.
- `controls/ctl-c1-3.json` (landed at `72359309`): `counter_exit 1`, `expected_exit 0`,
  `verdict unexpected-exit`, `counter_stdout … "frontier_note": false`, matched 6.
- `corpus/lessons/round-39.md:15-17` and `plans/round-39-claims.md:79-82` describe the **landed**
  outcome ("fails only on a documentation binding", the disclosed limit) — i.e. the disclosure of the
  fabrication limit is stated against the run that exits 1, while the freeze-committed run that exits 0
  (6/6, target met) carries no reconciliation sentence.

Both records are committed and neither is annotated against the other; a reader of the lesson alone
cannot tell that the same control met the target once.

### D4 — Closure artifacts are absent, and one stated proxy is stale

- `SCORECARD.md` has no round-39 section and `LOG.md` has no round-39 entry at HEAD (`e40a25df`); the
  only round-39 mention is the round-38 line "planned (round 39)" at `SCORECARD.md:3410`.
- `SCORECARD.md:23` still states `126/126 knowledge files mapped`; `corpus/knowledge` holds 127 files at
  the base, 128 at the freeze and 129 at HEAD, and `corpus/README.md` gained one Knowledge-table row per
  round-39 entry (`113 → 115` rows beginning ``| `2026-``) plus one coverage-map row (`:93`).
- The lesson itself marks the claims "closure pending" (`corpus/lessons/round-39.md:11`), so this is a
  gap in the *record at HEAD*, not evidence against either claim; it is listed because a report written
  now inherits it.

### D5 (limit, not a defect) — control receipts are not re-verifiable from lane bytes

Every control receipt names a fixture revision (`rev`, and for the freeze control `freeze`) that is a
scratch clone commit: `git cat-file -e` returns absent for `aa7a7a03…` (CTL-C1-1), `8e1aea55…`
(CTL-C1-3), `26d0841a…` (CTL-C1-3 written set) and `bc533dda…` (CTL-C1-5). The receipts record the
counter argv, exit, stdout and written-file list, which is auditable; the scored bytes are not.

### D6 (observed working-tree state, already recorded by another seat) — the lane's worktree is dirty at four wave-1 paths

`git status --porcelain` at 14:41 (HEAD `e40a25df`) shows, besides the untracked wave-2 tree:

```
 M .ufo/waves/round-39/w1/R39C1IndepReader.md                                   | 24 +++++----
 M .ufo/waves/round-39/w1/R39C1SymlinkK1K4.md                                  | 39 +++++++++-----
 D .ufo/waves/round-39/w1/artifacts/R39C1SymlinkK1K4/evidence/carrier.sqsh     | Bin 365 -> 0 bytes
 M .ufo/waves/round-39/w1/artifacts/R39C1SymlinkK1K4/symlink-tables.py         |  9 +++-
```

I did not create, restore or revert any of these (mtimes 14:13-14:14, before this seat ran). The same
drift is already documented by `w2/R39W2Sentinel.md:87,105-110` with a full diff in
`w2/artifacts/R39W2Sentinel/08-w1-drift-diff.txt`, which also shows the frozen seven are
byte-identical freeze→HEAD and that the deleted `carrier.sqsh` blob is the same at both revisions —
i.e. this is worktree drift in wave-1 evidence, not frozen-predicate drift. All checks in this report
read committed objects (`git show <rev>:<path>`), never the worktree, so no number above depends on it.

## What checks out (my own recomputation, not a re-run of the claims' instruments)

- **Frozen paths undisturbed** between freeze and measured commit: `git diff --stat 8fcda41c 6fdaf4f1`
  over the claims doc, `c1-counter.py`, `c1-run.sh`, `c2-counter.py`, `sqfs-triage.py`,
  `heldout-gen.py`, `carriers.json` and `SKILL.md` → empty, rc 0. Both scores report
  `frozen_path_changed []` / `frozen_paths_changed []`.
- **Triage table bytes**: my own extraction of the block (marker `SKILL.md:333` to the `clean` row at
  `:343`) hashes `735595030e11584835551095d76e94eca90d4b24ae1ba214646d3dfd273d3438` at **both** the
  freeze and HEAD.
- **Carrier pins**: 18 pinned files (carrier, oracle, symlink table × 6) recomputed at `8fcda41c` and
  `6fdaf4f1` — 36 comparisons, 0 mismatches.
- **C1 receipts**: `subject.digest.sha256` equals the carrier pin for all six; every
  `parameters.output_directory` is under `/kaidoku-r39/`; every receipt names only `squashfs_v4_be`.
  Each envelope's `unpublished_entries` lists exactly the in-tree links, as kind `symlink` with a
  target (K2 1, K5 2 — `link-blob`, `link-notes` — K6 1), and REA's gap kind `unpublished-entry`
  occurs exactly on those links; the escaping links (K1 1, K5 1, K6 2) appear in no gap and no
  `unpublished_entries` row. K6's `superblock_compression` is 4.
- **Held-out set**: 20 carriers, 2 per each of 10 classes, `seed == 8fcda41c…`; every committed
  `carrier.sqsh` sha256 equals its manifest pin; every envelope carries its own digest; every label
  equals the frozen class→label map. 0 anomalies.
- **Scores**: `c1-at-6fdaf4f1` `carriers_matched 6`, `met_target true`, `bindings_false []`;
  `c2-at-6fdaf4f1` `matched 20`, `n 20`, `bindings_false []`, `seed_matches_freeze true`,
  `regenerated_seed_matches_freeze true`, `generator_sha_matches_freeze true`,
  `triage_table_identical true`. Exit maps read from source: `c1-counter.py:586` (`0 if met_target
  else 1`), `c2-counter.py:443` (`0 if met_target else 1`) and `:425-435` (`return 2` on `Unevaluable`, raised at `:165`), which is
  consistent with the recorded before arms (`ctl-c1-0-do-nothing.json` 0/6, `c2-at-freeze.json`
  `no_manifest_at_rev`).
- **Core surface wiring**: `PROVINCE.md:378` row cites the entry; the entry's `source:` line names S122;
  S122's used-by names the entry; `corpus/README.md:93` names the entry stem; `PROVINCE.md:384`
  supersedes the big-endian part of the round-4 `sasquatch` bullet (`:156-157`) and the round-38 note.
- **Registry append-only**: `corpus/SOURCES.md` diff base→HEAD is `5 insertions(+)`, rows 117 → 122,
  tier A 109 → 114, mined 112 → 117, rejected 5 → 5, new rows S118–S122 all tier A/`mined`.
- **Wave-1 record**: 43 seats, 43 reports, 43 ledger results; verdict strings 20 `DONE`, 14 `DEFECTS
  FOUND`, 4 `CONFIRMED`, 5 qualified/non-scalar.

## Out of scope

REA/unblob re-runs and per-carrier publication reproduction (wave-2 repro seats); AVM-BE, vendor-mangled
images, LE body damage, `unknown-chunk-handler`/`encrypted-chunk`/`depth-limited` envelopes (not
claimed); adequacy of the C1 counter's receipt-only design (disclosed at
`plans/round-39-claims.md:79-82`); whether QUALITY 82's gate is strong enough (separate seat); the
round's final closure (SCORECARD section, LOG entry, seat accounting) — still open at HEAD.

## Artifacts

- `.ufo/waves/round-39/w2/artifacts/R39W2ScribeReport/report-body.md` — drafted report sections.
- `.ufo/waves/round-39/w2/artifacts/R39W2ScribeReport/checks.md` — commands run and outputs.
- This report: `.ufo/waves/round-39/w2/R39W2ScribeReport.md`.

Report: .ufo/waves/round-39/w2/R39W2ScribeReport.md
