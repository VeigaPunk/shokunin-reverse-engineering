# Round 65 — lesson draft: two Mistakes rows and one QUALITY candidate

Seat ScribeLesson, round 65 w1. Drawn only from evidence already on disk at base
`c99e907cb5576c13a7b22755d776b356fdfc1752` (`corpus/QUALITY.md` blob sha256
`f0d8e5df7a77166399c3a1ec5d3522929951a02050d7f494b343e73ee30c1d80`, byte-identical to the
worktree at this write). No matrix run, no clone, no scratch; the commands under each row are
read-only resolutions of the pointer, and each was run once.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M65-1 | process/scope: a measuring run wrote Python bytecode caches into the retained toolchain it was measuring | `.ufo/waves/round-65/prep/precache-dirs.txt` (4 `__pycache__` dirs: `View8/Parser`, `View8/Simplify`, `View8/Translate`, `venv/…/parse`) plus `.ufo/waves/round-65/prep/README.md` (15 `*.pyc` counted at the cleanup pass; the filenames were not retained, which the receipt states as a limit); the blocking finding itself is `.ufo/waves/round-64/w1/ReviewerMatrix/review.md:24` F2 | r64 ReviewerMatrix F2 — blocking, but no QUALITY criterion and no predicate clause: the r64 predicate pinned sha256 only. The seat spec's cell read "none before this round"; refined here to the recorded F2 because it is committed at the base (F-3 below) | r65 C1 clause (i) "no Python bytecode cache present before the first run", plus `-B` and `PYTHONDONTWRITEBYTECODE=1` on every subprocess. Red/green: `.ufo/waves/round-65/w1/ExecControls/cache-present.json` exit 2, `cache_present` names 2 entries, `ok: false`; the same tree after removal, `cache-clean.json` exit 0, `ok: true`, 30 entries. Live tree at this write: 0 `__pycache__`, 0 `*.pyc` |
| M65-2 | number-drift/stale-premise: a measurement recipe derived its denominator from its own date filter | `git show c99e907cb5576c13a7b22755d776b356fdfc1752:SCORECARD.md` lines 5011-5012 — the r64 SCORECARD records that "the old measurement A regex accepts October-dated names only" and was not reinterpreted as a current score; measured at the same base, `.ufo/waves/round-65/l1/c2-before-date.json` reads `knowledge_files` 144, `population` 142, `population_dropped` 2, `mismatches` 2, `exit` 1, against `.ufo/waves/round-65/l1/c2-after-stem-at-base.json` 144/144, `mismatches` 0, `exit` 0 | the r64 SCORECARD note — recorded, no criterion (counting `denominator` in the base `corpus/QUALITY.md` blob prints 0; command under "Commands resolving each pointer"). The defect was invisible on an all-dated revision: at `df727606` both recipes report 142/142, `population_dropped` 0, exit 0 (`w1/ExecCoverage/c2-ctrl-date-df727606.json`) | repaired stem recipe keys the denominator on the full `corpus/knowledge` blob list, so the drop is reported instead of absorbed; QUALITY row 102 as numbered per F-1 (the seat spec's "#94" collides). The two hidden names need a separate command because the frozen receipt carries only the count (F-2) |

## Commands resolving each pointer

### M65-1

```
wc -l /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/prep/precache-dirs.txt
# 4
grep -n 'pyc\|Removal\|F2' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/prep/README.md
# the 15-count line, the removal line, the "why" line naming r64 F2
find /home/vgpnk/.local/share/kaidoku-jsc -name '__pycache__' -type d -print | wc -l   # 0
find /home/vgpnk/.local/share/kaidoku-jsc -name '*.pyc' -print | wc -l                  # 0
grep -o '"ok": [a-z]*' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ExecControls/cache-present.json
# "ok": false   (cache_present lists jsc2js-src/View8/__pycache__ and .../x.pyc)
grep -o '"ok": [a-z]*' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ExecControls/cache-clean.json
# "ok": true
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show c99e907cb5576c13a7b22755d776b356fdfc1752:.ufo/waves/round-64/w1/ReviewerMatrix/review.md | sed -n '24p'
# | F2 | L204-207, L211-212 (cwd=view8_dir) | side-effect / rule 7 | **blocking** | ...
```

The arm that shows it red is described at
`.ufo/waves/round-65/w1/ExecControls/findings.md` § D: a scratch copy of the toolchain gets
`jsc2js-src/View8/__pycache__/x.pyc` planted, `--manifest` refuses with exit 2; removing the
directory restores exit 0 with 30 entries. The planted name `x.pyc` is synthetic, so this
establishes the clause's refusal behaviour, not the round-64 file set — that set is the four
directories in the prep receipt.

### M65-2

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show c99e907cb5576c13a7b22755d776b356fdfc1752:SCORECARD.md | nl -ba | sed -n '5011,5012p'
# 5011  The old measurement A regex accepts October-dated names only; it cannot measure these
# 5012  November/non-date-named additions and is not reinterpreted as a current score.
cat /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/l1/c2-before-date.json
# recipe "date", knowledge_files 144, population 142, population_dropped 2, missing [], dangling [], mismatches 2, exit 1
cat /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/l1/c2-after-stem-at-base.json
# recipe "stem", knowledge_files 144, population 144, population_dropped 0, mismatches 0, mapped 144, exit 0
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only c99e907cb5576c13a7b22755d776b356fdfc1752 -- corpus/knowledge \
  | grep '\.md$' | awk -F/ '{print $NF}' | sed 's/\.md$//' | grep -vE '^2026-10-[0-9]{2}-[a-z0-9-]+$'
# jsc-mapper-cli-contract
# jsc-mapper-release-inventory
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show c99e907cb5576c13a7b22755d776b356fdfc1752:corpus/QUALITY.md | grep -c denominator
# 0  (no criterion covers a recipe's own filter; exit 1 from grep -c is expected on a zero count)
```

The date recipe's `mismatches` 2 is `missing` 0 + `dangling` 0 + `population_dropped` 2: the
whole count is its own filter. The same run on the all-dated revision `df727606`
(`w1/ExecCoverage/c2-ctrl-date-df727606.json`) is 142/142, dropped 0, exit 0 — the shape the
r1-era recipe was written inside.

## QUALITY candidate

### F-1 — number conflict, stated before the row

The seat spec says "highest criterion number is 93; the next free is 94". Measured at the base,
that is false for the file as a whole: the table rows stop at 93, but the appended
correction-block bullets already carry **94 through 101** (row 94 is
"a disposition rule is derived per carrier class…", `corpus/QUALITY.md:151` in the base blob).
The next free number is **102**, and this draft is numbered 102. Filing the text below as #94
would duplicate a live criterion.

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show c99e907cb5576c13a7b22755d776b356fdfc1752:corpus/QUALITY.md \
  | grep -oE '^\| [0-9]+ \|' | tr -dc '0-9\n' | sort -n | tail -1        # 93  (table rows)
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show c99e907cb5576c13a7b22755d776b356fdfc1752:corpus/QUALITY.md \
  | grep -oE '^- \*\*Row [0-9]+' | tr -dc '0-9\n' | sort -n | tail -1    # 101 (appended bullets)
```

### Row 102 (seat-spec number 94)

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 102 | **Row 102 (a recipe's denominator is the population it claims, never a filter of it).** A coverage or census recipe must derive its denominator from the population it claims to measure — never from the same name filter that supplies its numerator — and must report every file that filter keeps out as a named drop, because a recipe that cannot see a file must not be able to report it clean. | `corpus/lessons/round-65.md` M65-2; the defect was recorded without a criterion in the r64 record `SCORECARD.md:5011-5012` at base `c99e907`, and measured at the same base by `c2-before-date.json` (144 → 142, dropped 2, exit 1) against `c2-after-stem-at-base.json` (144/144, exit 0); companion to row 34, which already forbids a repaired result substituting for the frozen one | sharpens 11, 97 |

Pipe-free check on the criterion cell: no `|` outside the table separators. One sentence in the
body, wrapped with the file's bold-title convention.

## Findings (for the canonical judge; not part of the rows)

- **F-2 — the frozen receipt counts the drop but does not name it.** `assess()` computes
  `dropped = len(files) - len(population)` (`tools/round-65/coverage-recipe.py:104`) and returns
  it as an integer (`:108`); `missing` and `dangling` are empty on the date arm. The R65-C2
  predicate's clause "reports a non-zero `population_dropped` naming the files it hides" is
  therefore not discharged by `c2-before-date.json` alone: the two names exist in the plan
  (`plans/round-65-claims.md:90`) and in the read-only `git ls-tree` command above, not in the
  instrument's output. Any filing that cites the receipt for the naming half is citing prose.
- **F-3 — M65-1's captured-by cell.** The assigned value was "none before this round". The
  r64 ReviewerMatrix F2 row is committed at the base and is the observation; what was missing
  was a criterion and a predicate clause, which is what this round's clause (i) supplies. The
  row states the recorded capture rather than "none".
- **F-4 — the stale premise is revision-dependent.** On `df727606` the date recipe drops
  nothing and exits 0 (`w1/ExecCoverage/c2-ctrl-date-df727606.json`, 142/142). The recipe is
  only observably wrong once a non-dated entry exists, which is why the r1-era premise survived
  to round 64; the lesson should not say the recipe was always red.
- **F-5 — M65-1's fix is demonstrated on a synthetic cache entry.** `x.pyc` is planted in a
  scratch copy; the refusal is exercised, the round-64 file set is not reconstructed (the prep
  receipt says its 15 filenames were not retained). No claim in this draft asserts the original
  15 bytes.
