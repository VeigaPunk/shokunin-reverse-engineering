# R45W2MutC2Landing — mutation probe of the R45-C2 landing

Seat: mutation tester, round 45 wave 2. Target: the R45-C2 calibration landing
(`SKILL.md` `### Round-44/45 instrument registry` vs `tools/round-45/registry-scope.json`),
scored by `tools/round-45/c2-counter.py`.

Lane tree was **read-only**. All mutants were built in `$S` scratch fixtures and scored
by the frozen counter extracted from the lane at
`f59565b782c18b0eb691bec12f52d2f80d9f5032` (sha256
`50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025`). Proof of
non-mutation at the end.

## 1. Method

Fixture per case: fresh `mktemp`-style dir under `$S/fx/<case>`, `git -C "$D" init -q`,
`rev-parse --show-toplevel == $D` asserted before the first commit, contents written from
the lane blobs at A3:

| file | sha256 |
|---|---|
| `SKILL.md` (`git show f59565b7:SKILL.md`) | `36a396ce12f666e1ec1d3449209b866691c927fde377e23bbc4057fda8fe8b1a` |
| `tools/round-45/registry-scope.json` | `6e2dda713a474dd6479a0af1430af9f38013d058a7cf9d2cc3fe293b9bd8dff9` |
| `plans/round-45-claims.md` | `56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e` |

Commit 1 = freeze (all three). Commit 2 = the mutated `SKILL.md` (one case, one mutation).
`--freeze` = commit 1, `--rev` = commit 2, so `frozen_path_changed` is evaluated on real
history and must stay empty (all mutations touch `SKILL.md` only).

Exact command per case (argv recorded per case in `receipts.json`):

```sh
python3 -I -B <lane>/tools/round-45/c2-counter.py \
  --root "$D" --freeze <commit1> --rev <commit2> --json-out <case>.json
```

Mutation anchor for every case: the `tools/round-44/c2-counter.py` row of the
Round-44/45 registry table (`SKILL.md:1654` at A3, unique in the file).

### Controls

| control | result |
|---|---|
| Pristine fixture (freeze = rev) | exit **0**, `met_target true`, `registry_rows 45`, `unregistered []`, `thin []` |
| Frozen counter `--selftest` | exit **0**, `C2_SELFTEST: cases=7 failures=0` (`selftest.txt`, sha256 `aea7e363…`) |
| Real lane, freeze `f762b727`, revs `e715263c` / `1f4b27f8` (A1, measured) / `f59565b7` (A3) / `a63d109f` / `0ee50aaf` (the tip at close, a wave-1 bookkeeping commit) | exit **0**, `met_target true`, `registry_rows 45`, `failing []` at all five (`lane/*.json`) |

Baseline passes, so a mutated-run failure is attributable to the mutation, and a mutated
`met_target true` is a real hole rather than a broken harness.

## 2. Assigned mutations

| id | mutation (exact change) | exit | `met_target` | verdict |
|---|---|---|---|---|
| m1 | delete that tool's registry row | 1 | false — `unregistered: ['tools/round-44/c2-counter.py']`, `registry_rows 44` | **holds** (mutant killed) |
| m2 | that row's first cell → basename `` `c2-counter.py` `` | 1 | false — `unregistered: ['tools/round-44/c2-counter.py']`, `registry_rows 44` | **holds** (killed) |
| m3 | that row's exit cell → `non-zero` | 1 | false — `thin exit-code cells: ['tools/round-44/c2-counter.py']` | **holds** (killed) |
| m4 | that row moved out of the table into a ```` ```text ```` fence placed after the table (line 1659) | **0** | **true** — `registered` still lists all six, `registry_rows 45` | **FALSIFIED — hole** |
| m5 | row duplicated, good copy **second** (first copy exit cell `non-zero`) — `m5a` | 1 | false — `thin: ['tools/round-44/c2-counter.py']`, `registry_rows 46` | **holds** (killed) |
| m5 | same duplication with the good copy **first** — `m5b` (the informative direction) | **0** | **true** — `registry_rows 46`, `thin []` | **FALSIFIED — hole** |

Clause that fires, and why:

- **m1, m2** — `parse_rows` (`c2-counter.py:43-57`) keeps a table line only when
  `ROW_TOOL = re.compile(r"`(tools/[A-Za-z0-9._/-]+\.(?:py|sh))`")` matches **cells[0]**
  (line 31, 52). Both the deletion and the basename rewrite remove the match, so
  `by_tool.get(path)` is `None` at line 100 and `unregistered` is emitted.
- **m3** — `exits_ok` (`:59-60`) requires `\b0\b`, `\b1\b`, `\b2\b` in cells[2];
  `non-zero` carries none, so `thin` is emitted at `:107`.
- **m4** — `parse_rows` has **no fence state**: it tests `s.startswith("|")` on every
  line of the file (`:45-47`) and never asks whether the line is inside a fenced code
  block. A fenced line is rendered as code, not as a registry row, yet it registers.
- **m5** — `by_tool.setdefault(row["tool"], row)` (`:98`) keeps the **first** row per
  path. With the good row first, the contradictory `non-zero` duplicate is never
  examined, so `thin == []`.

## 3. Additional probes (coverage)

| id | mutation | exit | `met_target` | verdict |
|---|---|---|---|---|
| m2b | first cell → `` `tools/round-44/c2-counter.py.bak` `` | 1 | false — `unregistered` | **holds** (the regex is backtick-anchored, so a suffixed path does not match) |
| m4b | the row moved inside an `<!-- … -->` HTML comment near the file head (line 5); the registry table keeps 5 rows | **0** | **true** | **FALSIFIED — hole** (same clause as m4: no comment state) |
| m6 | exit cell → ``non-zero (`0`, `1`, `2` unused)`` | **0** | **true** — `thin []` | **FALSIFIED — hole** |
| m7 | row prefixed `> ` (blockquote) | 1 | false — `unregistered` | holds (conservative; a blockquote row also does not render as a registry row, so this direction is correct) |
| m8 | row duplicated verbatim (both good) | 0 | true — `registry_rows 46` | not a hole by itself; shows `registry_rows` is not a guard and duplication is invisible |
| m10 | exit cell → `` `0` met; `2` could-not-evaluate `` (drops `1`) | 1 | false — `thin` | **holds** (killed) |
| m11 | row appended to block 22's four-column table (`SKILL.md:596`), registry table left with 5 rows | **0** | **true** | **FALSIFIED — hole** |

- **m6** — `exits_ok` is a *presence-of-digit* test over the whole cell
  (`\b0\b`, `\b1\b`, `\b2\b`), so any cell that merely *mentions* the three numbers passes
  even when the verdict map is a bare `non-zero`. This falsifies the claim's sentence "a
  bare 'non-zero' cell is thin" as an instrument property: the cell must be bare **and**
  digit-free.
- **m11** — `parse_rows` scans the whole file (`:43-45`), not the registry sections, so a
  row in any table anywhere (here: the C1 decision table) satisfies registration. The
  claim's surface is "the `SKILL.md` instrument registry"; the instrument's surface is
  "any `|` line in the file".

## 4. Holes, exact inputs, and the minimal fix

Every hole below scores `met_target true` (exit 0) while the rendered `SKILL.md` does not
carry the registered row (or carries a contradictory one).

1. **Fenced / commented rows (m4, m4b).** Input: the row
   ``| `tools/round-44/c2-counter.py` | gate — R44-C2 calibration… | `0` met; `1` not met; `2` could-not-evaluate… | … |``
   placed at `SKILL.md:1659` inside ```` ```text ```` / ```` ``` ```` (m4) or at `SKILL.md:5`
   inside `<!-- … -->` (m4b), with the table row removed. Differing value: `registered`
   contains the path, `thin []`, `met_target true`; the registry table itself renders 5
   rows. Fix: track ```` ``` ```` fence state and `<!-- … -->` state in `parse_rows` and
   skip lines inside either.
2. **Unscoped table (m11).** Input: the same row at `SKILL.md:596`, appended to block 22's
   table. Differing value: `met_target true` with the registry table at 5 rows. Fix: count
   rows only between a `### … instrument registry` heading and the next heading (or
   require the row to belong to a table whose header names `verdict map`/`exit`).
3. **Contradictory duplicate (m5b).** Input: the good row at `:1654` and a second copy at
   `:1655` whose exit cell is `non-zero`. Differing value: `thin []`, `met_target true`.
   Fix: `by_tool.setdefault` → collect a list per path; `thin` if **any** row for the path
   fails `exits_ok`.
4. **Digit smuggling (m6).** Input: exit cell
   ``non-zero (`0`, `1`, `2` unused)``. Differing value: `thin []`, `met_target true`. Fix:
   strip `non-zero`/`nonzero` from the cell before the digit test, or require the three
   codes as separate backticked/bare tokens (`\`0\``, `\`1\``, `\`2\``).

`tools/round-45/c2-counter.py` is byte-frozen at `f762b727`; these fixes are **not**
landable inside round 45 without a new freeze — they are findings for routing, and the
`--selftest` would need four cases (`red-fenced-row`, `red-commented-row`,
`red-dup-thin-second`, `red-digit-smuggled`) to hold them.

## 5. Calibration: what this does and does not falsify

- The landed R45-C2 **target is not falsified at any recorded revision**: at
  `e715263c`, `1f4b27f8`, `f59565b7` and `a63d109f` under freeze `f762b727` the frozen
  counter reports exit 0, `met_target true`, `registry_rows 45`. The six landed rows are
  real in-table rows with real exit maps; I found no defect in the registered content.
- What is falsified is the **predicate's plain reading** and the **kill rule's
  completeness**: "some SKILL.md registry row's first cell is exactly that path" is
  computed as "some `|`-line in the file contains the backticked path", and "a row that
  names the path but writes a bare 'non-zero' exit cell reports `thin`" is computed as
  "the cell lacks the digits 0, 1, 2". Four mutants (`m4`, `m4b`, `m5b`, `m6`, plus
  `m11`) survive at exit 0. Recorded as holes, not as a claim failure.
- The claims file's satisfiability sentence ("the three `--selftest` receipts under
  `controls/` cover every red clause") is true only for the red clauses the claim text
  enumerates. The 7-case selftest has no case for fence placement, comment placement,
  duplicate ordering, registry scoping or digit smuggling; those are exactly the four
  surviving mutants. That is a coverage statement about the instrument, not a false claim.
- Direction check for m5: the counter is conservative in one direction (`m5a`, good row
  second, is killed) and over-permissive in the other (`m5b`, good row first). A registry
  that carries a good row plus a contradictory `non-zero` row still scores `met`.

## 6. Receipts

All paths relative to this directory.

| artefact | sha256 |
|---|---|
| `receipts.json` — every case: argv, exit, stdout, stdout sha256, UTC, counter sha256, fixture-`SKILL.md` sha256 before/after | `db24ce1851bb29b69e407b55495bc61642f29ac10a49953eecb724c145c3c53c` |
| `run.log` — driver transcript incl. `SUMMARY` | see file |
| `selftest.txt` — frozen counter `--selftest` | `aea7e363e5661efcc038df11f2e88380c11815b480d9458f9cc26370b40b0f2d` |
| `mutations.txt` — the mutated row lines per case, with line numbers | `d5773b7f8bffdddac94e788fd5363034a6892fb8ebad4241b4a6840e1c90418d` |
| `lane/e715263cb51b713c342ab992d527fe9d61d6f8ff.json` | `3efa93b556a14435bfc11a5ba08516c457a130b0d34d50a4393e85c2d9c79447` |
| `lane/1f4b27f82353d6544dc0c8048b3cfdadd8525d12.json` | `0daf63d3d13068a376af8adce4e37c9830f312d21cdaf2649d98478bf3c0abb9` |
| `lane/f59565b782c18b0eb691bec12f52d2f80d9f5032.json` | `6c322c7c375e81a87726d2761b0333b2b3b8cc05f29b6cf142ecae316851dc76` |
| `lane/a63d109f.json` | `df3d4257f8c636a3e41f5038b020537f4496432c99143be510fed689236e2d7d` |
| `lane/0ee50aaf.json` | `5b90355634efcaaa3dd663ebeeb2ede919d8e69d1a21d435aa6cb40477010978` |

UTC: the final full pass ran 2026-10-28T16:01:31Z → 2026-10-28T16:01:32Z (14 cases,
per-case stamps in `receipts.json`). The `--selftest` and the four real-lane scores ran
earlier in the same session; those commands printed no UTC stamp of their own, so their
window is bounded by the driver runs either side of them and is not asserted here.

## 7. Non-mutation of the lane

```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain -- SKILL.md plans tools corpus LOG.md SCORECARD.md
(empty)
$ git -C <lane> show f59565b7:SKILL.md | sha256sum
36a396ce12f666e1ec1d3449209b866691c927fde377e23bbc4057fda8fe8b1a  -
```

Scratch `$S` was removed after these receipts were copied here; every fixture repo was
disposable and lived only under `$S/fx/`. No write, stage, commit or stash touched the
lane tree or the fleet repo. No tool install was needed (python3 + git only).

The lane advanced during this seat by one commit, `a63d109f` → `0ee50aaf` ("land the wave-1
falsification record"), written by another seat. That commit touches neither `SKILL.md` nor
the frozen paths (`git log --name-only a63d109f..HEAD -- plans/round-45-claims.md tools/round-45/`
is empty), and `tools/round-45/c2-counter.py` at `0ee50aaf` hashes to
`50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025` — the same bytes this
seat scored with. All scores in this report are pinned to the named revision.
