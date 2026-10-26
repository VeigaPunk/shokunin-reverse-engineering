# R40C2TableDraft — SKILL rule block 19 + knowledge entry for SquashFS triage table v2

**Verdict: DONE** — the v2 rule block (11 unique labels, 12 columns, closed 10-token action
vocabulary, zero bare `*` cells) and its knowledge entry are drafted, grounded on published
lane bytes, and pass a 33-vector seat check plus five controls; two freeze decisions and one
verbatim conflict are handed to the L1.

Seat: executor-drafter (leaf). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
`fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`. Nothing frozen by me; the L1 integrates.

## 1. What was produced

| file | shape |
|---|---|
| `artifacts/R40C2TableDraft/block.md` | rule block 19, 43 lines: bullet lead, 5 prose sentences, `<!-- sqfs-triage-table v2 -->`, `<!-- sqfs-triage-actions: … -->`, header + separator + 11 rows (13 table lines, 132 cells) |
| `artifacts/R40C2TableDraft/entry.md` | knowledge entry draft, 122 lines: frontmatter (`source:` S112, S118, S119, S120, S121; `verified-at`; `recheck`), then Features 11-21, domain guard 23-30, labels table 32-53, column ablation 55-67, marker wording 69-81, mixed symlinks 83-90, zero/partial publication 92-100, actions 102-111, status/limits 113-122 |
| `artifacts/R40C2TableDraft/check-draft.py` | seat conformance check (own v2 parser + classifier, reuses the v1 feature extractor by import; no REA, no unblob, no sasquatch, writes only under `TMPDIR`) |
| `artifacts/R40C2TableDraft/check-out.json`, `candidate-check.json` | check output, block mode and candidate-SKILL mode |

Labels, in row order (unique, one row each): `no-squashfs-chunk`, `dep-missing-be`,
`dep-missing-le`, `avm-marker-be-dropped`, `body-extractor-failure`, `partial-body-failure`,
`mixed-symlinks`, `escaping-symlink-removed`, `in-tree-symlink-metadata`, `clean`, `clean-empty`.
Declared vocabulary (10 tokens, one per row, `accept` shared by two labels):
`accept resolve-unpublished expect-removed expect-removed-and-unpublished
install-sasquatch-v4be install-sasquatch rerun-with-be-wrapper keep-failure-evidence
accept-partial-published check-superblock`.

Domain cells: every row carries `operation` = `extract_firmware` and `provider` = `unblob`.
Verified strings, read from published bytes (`corpus/evidence/round-39/c1/K1/after.json`):
`"operation": "extract_firmware"`, `"provider": {"id": "unblob", "name": "Unblob", "version":
"26.6.4"}`. The provider **name** is `Unblob` (capital U) and is a different field from the id —
the table keys on the id.

Placement (candidate assembly, scratch only): inserted after `SKILL.md:343` (block 18's last
table row), so block 18 stays byte-identical and block 19 becomes the 19th top-level `- **`
bullet of `## Queue-drain craft`.

## 2. Gates run (seat checks — not claim gates)

All commands run with `TMPDIR=/fast/scratch/hyaku/kaidoku-r40/R40C2TableDraft`.

```
python3 -I -B check-draft.py --json > check-out.json
  -> rules: 11  vocabulary: 10  cells: 132  bare * cells: 0
  -> 33/33 vectors matched; verdict PASS; exit 0
python3 -I -B check-draft.py --skill $TMPDIR/SKILL-candidate.md --json > candidate-check.json
  -> verdict PASS; 11 rules; 33/33; exit 0      (same block parsed inside a real-SKILL-shaped doc)
python3 -I -B tools/round-39/sqfs-triage.py --skill $TMPDIR/SKILL-candidate.md --table-only
  -> marker line: 333  table line: 334  rules: 8 ; exit 0     (block 18 unharmed)
```

The 33 vectors: the 20 committed round-39 held-out envelopes (`c2/heldout/H01..H20`, expected
labels from their own `manifest.json`), the 6 round-39 Core receipts (`c1/K1..K6`), the two
measured w2 shapes (`w2/artifacts/R39W2C2TableReview/{xz-shape,dirempty-shape}.json`, with the
domain fields REA really emits added), and five out-of-domain mutations of `K1`
(`operation` → `analyze_function`, `operation` → `inspect_firmware_regions`, `provider.id` →
`ghidra`, `provider.id` → `binwalk`, both fields removed). Every vector returns exactly one row
(pairwise-disjoint decision vectors) and the expected (label, action) pair.

Controls, all behaving:

| control | outcome |
|---|---|
| catch-all row (first row's 8 condition cells → `*`) | loses 33/33 cases |
| label-right/action-wrong (`clean` action → `check-superblock`) | loses 6/33 |
| v1 table transcribed into the v2 shape with `*` domain cells | loses 11/33: `H03`, `H04` (clean-le, v1 rows are BE-only), `K5`, `K6` (mixed), `xz-shape` (partial), `dirempty-shape` (clean-empty), 5 out-of-domain — i.e. R39-CL1, R39-CL2 and R39-CL3 D1/D2 each cost the transcription a case |
| duplicate label | exit 2 |
| action outside the vocabulary | exit 2 |

Column ablation (one condition column → `*`, first-match semantics, of 33):
`operation` 2, `provider` 2, `handler` 1, `gap kinds` 9, `dependencies` 2,
`-be in child argv` 4, `symlink removed` 9, `published files` 2. All eight decide at least one
case; no column is decorative.

Depth: craft section of the candidate spans lines 81-391 with 19 `- **` bullets (18 → 19).

## 3. How the v1 defects are worded in v2

- **R39-CL1 (domain guard).** Both domain cells on all 11 rows. v1 labelled
  `corpus/evidence/round-26/c1/envelopes/function-base.json` (`analyze_function` / `ghidra`) as
  `no-squashfs-chunk` (`.ufo/waves/round-39/w2/R39W2C2AxisFit.md` C2, lines 143-150); v2 reads
  `unclassified`. The ablation prices the guard: dropping either domain column loses exactly the
  5 out-of-domain vectors.
- **R39-CL2 (mixed symlinks).** A `mixed-symlinks` row (`G` = {`unpublished-entry`}, `SR` = yes,
  `P` > 0) above the escaping row, action `expect-removed-and-unpublished`. Grounded on
  `K5`/`K6` (`P` 10 / 8, two in-tree + one escaping on K5, the reverse on K6).
- **R39-CL3 D1/D2 (excluded outcomes).** `partial-body-failure` (`G` = {`extractor-failure`},
  `BE` = yes, `P` > 0) and `clean-empty` (`G` = ∅, `P` = 0), from the two measured w2 shapes
  (`full-be1-xz`, `P` = 6; `full-be-dirempty-gzip`, `P` = 0), both of which v1 sent to
  `unclassified`.
- **R39-CL3 (scored action, unique labels).** `action` is its own column, one token from a closed
  vocabulary declared on the actions line; the `cause` column no longer carries `->` and is not
  parsed. Labels are unique by construction (duplicate → exit 2).
- **The marker row and the genuine AVM layout.** v1's action for `avm-marker-be-dropped` ("rerun
  through a wrapper that appends `-be`") is wrong for a genuine AVM-layout body: unblob omits
  `-be` there too and the extractor **succeeds** (AVM 07.57 BE member, 2 942 files, no `-be` in
  its argv, `.ufo/waves/round-39/w1/R39AssimAvmCritic.md`), while a genuine layout with the marker
  stripped receives `-be` and fails with 0 files. v2 therefore keys the row on
  (`BE` = no) ∧ (`G` = {`extractor-failure`}) ∧ (`P` = 0) — only a body that fails without `-be`
  is the marker artefact — so a genuine layout that publishes files is `clean` and the
  marker-stripped genuine layout lands in `body-extractor-failure`, whose cause sends the reader
  to the little-endian metadata block-length header before keeping `-be`. The timestamp is the
  trigger; the block-length field is the format test (S112 lines 44-50). The row makes no claim
  about genuine AVM layout success — that is C1's ground and appears only as a limit.

## 4. Decisions the L1 must freeze (spec points the table cannot carry)

1. **Actions-line placement.** I implemented the literal reading of the contract: marker line,
   then the `sqfs-triage-actions` line, then the table header — so the actions line is the line
   directly above the table. The frozen interpreter should require exactly that (line `i-1` of
   the header), exactly one such line in the craft section, else exit 2. A finder that skips
   non-table lines between marker and header still works (the v1 finder shape does).
2. **`*` allowances.** My table has zero bare `*` cells. The grammar's per-column enumerations
   omit `*` for `gap kinds`, `dependencies`, `-be in child argv`, `symlink removed`; if the frozen
   interpreter forbids `*` there, this table is unaffected. If it allows `*`, the "best table +
   `*` default row" control is the only thing that benefits — and that control must fail.
3. **`unclassified` has no row and no token.** The pair for a no-match is (`unclassified`,
   `none`). A row for it would need `*` domain cells and would swallow the guard. The generator
   seat proposed a `refuse-out-of-domain` token; that must not enter the vocabulary (see §6).
4. **Interpreter must read `OP`/`PV`, and an absent domain field is a non-match, not exit 2.**
   The round-39 kill-control shapes are bare `normalized_result` objects with no
   `operation`/`provider`; if absence were fatal, those controls become unevaluable.
5. **`dependencies` is load-bearing only because the two dependency rows share the
   `squashfs_v4_*` handler pattern.** With per-endian handler cells the dependency column was a
   restatement of the handler (measured: ablation lost 0 cases); as drafted, the missing binary's
   name — the only value `Command.get_dependencies()` reports (S120 `command.py:101-102`) —
   decides, and the ablation prices it at 2.
6. **Two extra rows from the round-39 AVM critic are refused, with reasons.**
   `avm-layout-be-flag-passed` (`BE` = yes, `G` = {`extractor-failure`}, `P` = 0) is
   feature-identical to `body-extractor-failure`; a row for it would silently steal first match
   from that row and would state a distinction the eight features cannot make — the check lives in
   `body-extractor-failure`'s cause instead. `ok:true-with-zero-output` **is** `clean-empty`
   (D2), so a second row would duplicate a label. Not refused as facts: both are stated as limits
   in the entry (`:113-122`).
7. **`version-minor-mismatch` is not in the claims' v2 class list** but maps to
   `body-extractor-failure` (measured `H19`/`H20`); if the L1 adds it as a class, the label
   stands and no row changes.
8. **Counter must score (label, action) and report the number of distinct matched rows**; the
   vocabulary is read from the frozen actions line, never from prose.

## 5. Findings (measured, not inferred)

- **F1 — the `dependencies` column was decorative in my first draft** (ablation: 0/33 lost). Fixed
  by widening the two dependency rows to `squashfs_v4_*`; now 2/33 lost, handler keeps 1/33 (it is
  what separates `no-squashfs-chunk` from `clean-empty`). Both columns now decide.
- **F2 — v1's transcription loses 11/33 on my vector set**, and every routed defect class is in
  that list (§2 control table). This is the v2 table's own kill control, measured pre-freeze.
- **F3 — `published files` decides only 2/33** (`partial` vs `body`, `clean-empty` vs `clean`),
  which is exactly the R39-CL3 D1/D2 pair; no other row keys on it. It is narrow but not
  decorative.
- **F4 — the 20 committed round-39 held-out envelopes carry no `operation`/`provider`-less case**;
  all 20 are `extract_firmware`/`unblob`, so v2 keeps its 20/20 on the published set and adds the
  two new classes and the guard on top.
- **F5 — `Unblob` vs `unblob` is a real trap**: the provider object carries both, and a table keyed
  on the name would match nothing.

## 6. Conflict reported verbatim (peer seat `R40C2HeldoutGen`, IRC during this wave)

> "Proposed closed action vocabulary, one token per label (12 labels over 13 classes;
> clean-be/clean-le share `clean`): clean -> use-published-files; clean-empty ->
> accept-empty-image; escaping-symlink-removed -> expect-path-absent; in-tree-symlink-metadata ->
> count-gap-publish-nothing; mixed-symlinks -> count-gaps-expect-absent; dep-missing-be ->
> install-sasquatch-v4be-on-path; dep-missing-le -> install-sasquatch-on-path;
> avm-marker-be-dropped -> rerun-through-be-wrapper; body-extractor-failure ->
> quarantine-and-diff-known-good; partial-body-failure -> keep-partial-and-record-failure;
> no-squashfs-chunk -> check-magic-before-rerun; unclassified -> refuse-out-of-domain"

Resolution offered to that seat (message delivered, no reply yet): same 13 classes, same
semantics, but (a) out-of-domain is (`unclassified`, `none`) with no token and no row, per the
contract; (b) freeze the ten tokens in §1 instead, because the frozen table's actions line is the
single source and the manifest must copy it byte-for-byte. Their shapes for the new classes match
my rows exactly (mixed `G` = {`unpublished-entry`} + `SR` yes + `P` > 0; escaping `G` = none;
clean-empty `P` = 0; partial `BE` yes + `P` > 0). If the L1 prefers their strings, only the
actions line, the `action` cells and the entry's token list change — the 11 labels, 12 columns and
all conditions stand as drafted.

## 7. Bounds honoured

- Wrote only `artifacts/R40C2TableDraft/` and this report. No lane file edited (`corpus/`,
  `tools/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `LOG.md`,
  `corpus/knowledge/` untouched — the entry lands there only when the L1 places it).
- No VCS command of any kind except one read-only `git status --porcelain` at the end. It reports
  three untracked entries — `?? .ufo/waves/round-40/` (this wave's tree, mine included),
  `?? detail.log`, `?? plans/round-40-claims.md` — and lane HEAD is still the base
  `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`. I did not observe the pre-work status, so I do not
  claim the last two were untracked before my session; neither is mine and neither was written by
  me (`plans/round-40-claims.md` was read; `detail.log` was never opened).
- **Zero REA runs, zero unblob runs, zero sasquatch runs.** No carrier built or read with an
  extractor. Only published JSON/bytes were read (round-39 receipts, held-out envelopes, w2 shape
  files), plus the installed unblob handler file (grep only) to re-derive its line anchors.
- Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C2TableDraft` removed at exit; the only scratch
  artifact not copied is the assembled `SKILL-candidate.md` (derived, 9 KB) — rebuild:
  `python3 - "$LANE/SKILL.md" block.md cand.md` inserting `block.md` after line 343 with a blank
  line separator (asserted on `| clean |` at line 343).
- No tool installed, upgraded or removed; pacman untouched; `sasquatch`, `sasquatch-v4be`,
  `unblob` untouched.

## 8. Limits

- The 33-vector set is published/development evidence. The scored set is the round-40 held-out set
  generated after the freeze; that its envelopes carry exactly the drafted feature vectors is
  [INFERENCE] from the generator seat's stated shapes plus every dev shape I measured (all
  matched).
- The v2 interpreter does not exist yet: my `check-draft.py` parser is *my* reading of the L1
  grammar. If the frozen interpreter differs on any cell rule (e.g. `*` in set columns, actions-line
  position), `block.md` must be re-checked — `check-draft.py` is the tool to re-run.
- Entry line citations in the block (`:11-21`, `:23-30`, `:32-53`, `:55-67`, `:69-81`, `:83-90`,
  `:92-100`, `:102-111`, `:113-122`) were verified by `nl` against `entry.md` as delivered; any
  edit on placement (a title change, a README-mapping line) shifts them.
- Nothing here measures genuine AVM-layout extraction, vendor-mangled images,
  `unknown-chunk-handler`, `encrypted-chunk` or `depth-limited` gaps, or anything about extracted
  programs.

## 9. Artifacts (all paths under `.ufo/waves/round-40/w1/artifacts/R40C2TableDraft/`)

| path | sha256 | note |
|---|---|---|
| `block.md` | `14ea1d7345c11d7fe970d8fbb2e9f9b86591d5f6aa49e09662aedcf23561b800` | rule block 19, insert after `SKILL.md:343` |
| `entry.md` | `22b82d819dfc8c909867f34d1976ace3b9487e22d18f6f0c49646d2d07999a98` | lands at `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` |
| `check-draft.py` | `4fb7a653c6c8efc374958e233c25ace6360fba9e898ad2686759a1ddc2b28272` | `python3 -I -B check-draft.py [--skill F] [--json]` |
| `check-out.json` | `ff0a8feb523290f3e883808fa961740a7048388edd1224a5f197a17e70c58e65` | block mode, PASS, 33/33 |
| `candidate-check.json` | `f951e2bfdc61c98b3ee5265b89f90c0fb90d05397083b31300b4df6877bfc4a2` | candidate-SKILL mode, PASS, 33/33 |

Rebuild hashes: `sha256sum block.md entry.md check-draft.py check-out.json
candidate-check.json` from the artifacts directory.
