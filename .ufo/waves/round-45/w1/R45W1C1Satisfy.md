# R45-C1 satisfiability preflight — every clause computes

Seat `R45W1C1Satisfy`, round 45 wave 1. Read-only on the lane tree; all fixtures under
`/fast/scratch/hyaku/kaidoku-r45/R45W1C1Satisfy` (removed after the receipts were copied here).
Frozen bytes used: `plans/round-45-claims.md@f762b7273e3f6ca3c710bb37d5de92a4a4417aec`
(sha256 `56bacf31…b915e`) and `tools/round-45/c1-counter.py@f762b72` (sha256 `2cfc5a48…30a509`),
`tools/round-45/frozen-path-preflight.py@f762b72` (sha256 `633ebc05…30523b`).

**Verdict: satisfiable.** Every clause of the R45-C1 predicate was computed end to end on a
fixture repo (exit 0, `failing == []`) and again on the real tip (exit 0). No clause asks for a
value the instrument cannot derive. The exact bytes that make every clause compute are in
[§4](#4-the-exact-bytes-the-landing-must-contain); the reference block is
`canonical-block22.md` (1226 bytes, sha256 `daa23ef5…7dbb89`), which is the literal text scored 0
in `receipts/v00-canonical.json`.

## 1. Method

Fixture repo `D` per variant: `git -C "$D" init -q`, toplevel asserted equal to `D` before the
first commit, throwaway identity `r45w1c1@fixture` set **inside `$D` only**.

- commit `FREEZE` holds: `SKILL.md` (the real frozen SKILL.md, 21 craft blocks asserted),
  `plans/round-45-claims.md`, `tools/round-45/frozen-path-preflight.py` (real bytes),
  `tools/round-45/c1-counter.py`, and the two corpus files the block cites.
- commit `REV` holds the same bytes except `SKILL.md`, which gains the candidate block 22.
  Only `SKILL.md` changes, so `FREEZE..REV` touches no frozen path (the frozen-path arm is
  exercised separately in `v25`).

Scoring command, verbatim (per variant; `$W` = `TMPDIR=HYAKU_SCRATCH=<scratch>/live`):

```sh
python3 -I -B <scratch>/runner/c1-counter.py --root <fixture> \
  --freeze <FREEZE> --rev <REV> --json-out receipts/<variant>.json
```

`runner/c1-counter.py` is a byte copy of the frozen counter; `runner/frozen-path-preflight.py`
a byte copy of the frozen interpreter that the counter extracts from `REV` anyway. Driver for
replay: `fixture-driver.py` (this directory). 26 variants, 30 receipt files.

## 2. Canonical result — `receipts/v00-canonical.json`

Command, exit, stdout sha256, UTC: see the JSON (`receipts/v00-canonical.json`, sha256
`0d880cf4…42641`) — `exit 0`, stdout sha256
`d010fa0f4cf7bf79ea7b62eb4c1c53a115173e886cc13f59244d659fc33f480f`, 2026-10-28T15:42:57Z.
Every receipt field, verbatim:

| field | value |
|---|---|
| `counter` | `round-45-c1` |
| `freeze` / `rev` | fixture commits (`b4c14758…`, `cb1efb42…`) |
| `rule_blocks` | `22` (== 22, clause 1) |
| `block22_present` | `1` (clause 2) |
| `block22_rows` | `8` (>= 8, clause 3) |
| `block22_refs` | `8` (>= 4, clause 4) |
| `block22_unresolved_citations` | `[]` (clause 4) |
| `block22_header_ok` | `true` — header carries `trigger`/`arm`/`exit`/`receipt` |
| `block22_cites` | `{"S140": true, "interpreter": true}` (clause 5) |
| `interpreter_present` | `true` (clause 5) |
| `preflight_selftest` | `{"exit": 0, "cases": 11, "failures": 0, "ok": true}` (clause 6) |
| `frozen_path_changed` | `[]` |
| `met_target` / `failing` | `true` / `[]` |

Clause 6 with the interpreter run directly from the frozen bytes (standalone, not through the
counter): `receipts/preflight-selftest.w1c1.txt`, exit 0, sha256 `9f03df65…ec06c`, last line
`PREFLIGHT_SELFTEST: cases=11 failures=0`, 11 `"ok": true` cases. The frozen counter's own
selftest: `receipts/c1-selftest.w1c1.txt`, exit 0, sha256 `296734f2…dac6d`,
`C1_SELFTEST: cases=9 failures=0`, nine named cases (green, relabelled-21-block, thin-table,
bad-citation, no-s140, interpreter-fails, bad-exit-cell, frozen-touched-is-exit-2, unknown-rev).

## 3. Which syntactical forms the parser accepts (measured)

`rule_blocks` = number of `^- \*\*` splits inside the text between `"## Queue-drain craft "`
(heading + **one trailing space**) and the next `"\n## "`. `block_table` collects every line
whose `lstrip()` starts with `|`, first one is the header, all others except
`fullmatch(r"\|[\s:|-]+\|")` lines are data rows. Exit column = first header cell containing
`exit`; exit value = cell `.strip("` ")` must be exactly `0`, `1` or `2`. Citations are
`(corpus/(knowledge|lessons)|plans)/<name>.md(:first(-last)?)?` over the whole block.

| variant | form | exit | measurable |
|---|---|---|---|
| `v00-canonical` | spec shape, `\|---\|` separator | **0** | blocks 22, rows 8, refs 8 |
| `v01-table-indented` | every table line indented 4 spaces | **0** | identical to v00 |
| `v02-table-split-by-paragraph` | 4 rows, prose line, 4 rows | **0** | rows 8 |
| `v04-exit-cell-backticked` | exit cells `` `0` ``/`` `1` ``/`` `2` `` | **0** | rows 8, exits accepted |
| `v05-no-separator-row` | separator row deleted entirely | **0** | rows 8 (separator is optional, not required) |
| `v07-marker-twice-same-block` | marker repeated in block 22 | **0** | `block22_present 1` (blocks counted, not occurrences) |
| `v08-nested-bold-bullet` | `  - **note:** …` inside the block | **0** | blocks 22 (block boundary needs column 0) |
| `v10-exit-column-second` | header `trigger\|exit\|arm\|receipt` | **0** | exit found by name |
| `v11-header-cells-backticked` | `` \| `trigger` \| `arm` \| `exit` \| `receipt` \| `` | **0** | header cells strip backticks |
| `v12-table-fenced` | table wrapped in a ``` fence | **0** | rows 8 (fence lines ignored) |
| `v16-citation-without-line` | `corpus/lessons/round-44.md` (no `:line`) | **0** | refs 8, resolves to line 1 |
| `v22-header-exit-code` | header cell `exit code` | **0** | substring match |
| live landing | `\| --- \| --- \| --- \| --- \|` separator, marker on its own line | **0** | 10 data rows counted (`receipts/live-at-HEAD.json`) |

Rejected forms (all exit 1, the failing reason named):

| variant | form | failing |
|---|---|---|
| `v03-split-plus-second-header` | split table with a repeated header row | `exit cells outside {0,1,2}: 1` (rows 9 — the repeated header becomes a data row) |
| `v06-table-before-block-line` | table above the `- **22.` line | `rows 0`, `header lacks …`, `refs 0` (the table belongs to the previous block) |
| `v09-block-line-indented` | `  - **22. …` | `rule_blocks 21`, and the marker now rides inside block 21: `rows 24`, `refs 9`, plus block 21's own citations are then scanned |
| `v13-only-three-citations` | 3 resolvable citations | `refs 3 < 4` |
| `v14-citation-past-eof` | `corpus/lessons/round-44.md:9999` | unresolved `['corpus/lessons/round-44.md:9999-9999']` |
| `v15-s140-hyphenated` | `S-140` | `does not cite S140` (`\bS140\b`) |
| `v17-rows-no-leading-pipe` | rows without the leading `\|` | `rows 0` |
| `v18-bold-exit-cell` | exit cell `**0**` | `exit cells outside {0,1,2}: 8` |
| `v19-two-marked-blocks` | a second marked block | `rule_blocks 23`, `block22_present 2`, selftest skipped |
| `v21-exit-cell-with-annotation` | exit cell `0 (clean)` | `exit cells outside {0,1,2}: 1` |
| `v23-literal-pipe-in-arm-cell` | a bare `\|` inside one arm cell | `exit cells outside {0,1,2}: 1` (naive split shifts the exit column) |
| `v24-block-outside-craft-section` | block under a later `## ` heading | `present 0`, `blocks 21` |
| `v25-canonical-then-frozen-touch` | canonical, then a commit edits the claims file | **exit 2** `frozen_path_changed: ['plans/round-45-claims.md']` |

Two of my a-priori expectations were wrong and the receipt records the truth: I predicted
`v05` (no separator) and `v08` (indented sub-bullet) would fail; both score 0. They are listed
above as accepted forms.

**Crash, not a verdict** — `v20-heading-without-trailing-space`: renaming the section heading to
`## Queue-drain craft` (no trailing space) makes `craft_blocks` raise
`IndexError: list index out of range` at `c1-counter.py:60`. Exit is 1, stdout is empty
(sha256 `e3b0c442…b855`, i.e. no bytes), no `met_target` field is ever printed, and
`--json-out` is not written. This is an instrument defect, not a satisfiability failure: a
crash is reported as "not met" (1) instead of "could not evaluate" (2). `SKILL.md` is not
frozen, so the landing and wave 2 must never edit that heading string; the frozen instrument
cannot be fixed this round.

## 4. The exact bytes the landing must contain

Reference: `canonical-block22.md` (1226 bytes, 12 lines, sha256 `daa23ef5…7dbb89`). Invariants,
each one measured above — a landing need not copy that text, but must satisfy every line:

1. **Placement**: inside the `## Queue-drain craft ` section (that heading keeps its trailing
   space; `## Queue-drain craft (rounds 5-12, distilled in round 13)` is fine), above the next
   `## ` heading. The block line starts `- **22. ` at **column 0**.
2. **Block count**: exactly one new column-0 `- **` line in that section → `rule_blocks == 22`.
   Any second column-0 `- **` line (inside block 22 or appended later, including wave-2
   lesson bullets) makes it 23 and fails clause 1. Sub-bullets inside the block must be
   indented (`  - **…`), never at column 0.
3. **Marker**: `<!-- freeze-integrity-table v1 -->` exactly, inside that one block, on its own
   line or in the prose — one marked block, not two.
4. **Table**: first `|`-leading line inside the block is the header
   `| trigger | arm | exit | receipt |` (any order, backticks optional, `exit code` allowed);
   ≥ 8 data rows; a `| --- |` separator row is optional; indentation and interleaved prose are
   harmless; every row starts with `|`; **no bare `|` inside a cell** (naive split would shift
   the exit column).
5. **Exit cells**: exactly `0`, `1` or `2` — backticks allowed, nothing else (`0 (clean)`,
   `**0**`, `non-zero` all fail).
6. **Citations**: ≥ 4 occurrences matching `(corpus/(knowledge|lessons)|plans)/<name>.md` with
   an optional `:line` or `:first-last`; every one must exist at `--rev` and end within the
   file's line count. A line-less citation resolves to line 1. `tools/round-45/*.py:NN` does
   **not** count toward the four (not matched by the reference regex).
7. **Tokens**: `S140` with word boundaries (`\bS140\b` — `S-140` fails) and the literal
   `tools/round-45/frozen-path-preflight.py`, inside the block.
8. **Frozen side**: no commit in `FREEZE..REV` may touch `plans/round-45-claims.md` or
   `tools/round-45/`; the interpreter must be present at `--rev`.

Resolvable citation targets at the freeze, with line counts (all verified with `git show
<freeze>:<path> | wc -l`): `corpus/lessons/round-44.md` 155 lines, lines 18 (M44-2 row),
63-69 (R44-CL1), 88-92 (R44-CL10); `corpus/lessons/round-44-verifier-spotcheck.md` 233 lines,
lines 89-92 (restore clause); `plans/round-45-claims.md` 175 lines. **`corpus/lessons/round-45.md`
does not exist at the freeze** (first appears in `e715263c`), so a citation to it resolves only
at a rev that contains it.

## 5. The real tip already computes — `receipts/live-at-HEAD.json`

`python3 -I -B tools/round-45/c1-counter.py --root <lane> --freeze f762b72… --rev faa875bc…`
→ **exit 0**, 2026-10-28T15:42:36Z, stdout sha256
`0c83a7b3fc340e8f65f6d052b5d1b2905e6e1e4bf4d836788e3257394226ce14` (the exact stdout bytes are
the `.stdout.json` sibling; the JSON copy is `receipts/live-at-HEAD.json`, sha256
`427bf895…e971c`). Fields: `rule_blocks 22`, `block22_present 1`, `block22_rows 10`,
`block22_refs 7`, `block22_unresolved_citations []`, `block22_cites {"S140": true,
"interpreter": true}`, `block22_header_ok true`, `interpreter_present true`,
`preflight_selftest {exit 0, cases 11, failures 0, ok true}`, `frozen_path_changed []`,
`met_target true`, `failing []`.

Landing revision `e715263c` (SKILL.md sha256 `4e36bafc…d01d1`), amended by `1f4b27f8` (SKILL.md
sha256 `19c20927…a6a7a5`, unchanged at `faa875bc`). Block 22 occupies lines **547-595** of the
live `SKILL.md`; the marker is at line 567. No clause is unsatisfiable on the actual bytes:
`rows 10 >= 8`, `refs 7 >= 4`, and the spaced `| --- |` separator is skipped correctly
(10 rows counted, not 11).

## 6. Findings for the L1

- Satisfiability: **pass**. Every clause computed on fixture and on the tip; no vacuous or
  underivable value. Exit 0 both times; a 2 never counted toward the target.
- Instrument defect (report, do not fix): `craft_blocks` has no guard for a missing
  `"## Queue-drain craft "` literal and crashes with exit 1 / empty stdout instead of 2
  (`v20`). The frozen counter is not fixable this round; the landing and wave 2 must leave that
  heading string alone.
- Docstring/code mismatch, harmless today: the counter's docstring says the marker appears
  "exactly once", the code counts marked **blocks** (`v07` scores 0 with the marker twice in
  one block; `v19` fails on a second marked block). Score block 22 as one marked block.
- Fragility to watch in wave 2: `rule_blocks == 22` is an equality, not a bound. Any later
  column-0 `- **` bullet added to the craft section turns C1 red retroactively; the live tree is
  at exactly 22 now.
- Provenance caveat in the frozen claims file: it locates the S140/S141 quotes in
  `corpus/lessons/round-45.md ## Gate`, but that file is absent at `f762b72` (created in
  `e715263c`). Not a C1 clause, but a verifier replaying the quotes at the freeze will not find
  them there.
- Fixture fidelity limit (stated, not hidden): the fixture copies only
  `corpus/lessons/round-44.md` and `corpus/lessons/round-44-verifier-spotcheck.md`, so `v09`'s
  extra unresolved citation (`corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md`) is a fixture
  artifact — that file does exist at the freeze in the lane repo. It does not affect any
  accepted/rejected conclusion.

## 7. Receipts and cleanup

`receipts/`: one JSON per variant (exact command, exit, stdout sha256, UTC start/end, receipt),
`live-at-HEAD.json` + `live-at-HEAD.stdout.json`, `preflight-selftest.w1c1.txt`,
`c1-selftest.w1c1.txt`; `summary.json` holds all variant records. `canonical-block22.md` and
`fixture-driver.py` are the replay pair (`TMPDIR`/`HYAKU_SCRATCH` set to a scratch dir;
`python3 -I -B fixture-driver.py`). Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W1C1Satisfy`
and every fixture repo under it were removed after the receipts were copied here; nothing was
written under `/tmp`, and no tool was installed or updated.

No file outside this seat directory was modified: `SKILL.md`, `plans/`, `tools/`, `corpus/`,
`LOG.md`, `SCORECARD.md` were read only (`git show`, `git log`, `git cat-file`, `git rev-parse`,
`git status`). No git/jj mutating command was run in the lane repo; all commits were made with
`git -C "$D"` inside throwaway fixtures.
