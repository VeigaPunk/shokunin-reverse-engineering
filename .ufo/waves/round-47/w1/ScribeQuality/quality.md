# Round 47 — QUALITY.md candidate rows (ScribeQuality)

Drafted from the round's own frozen instruments and the landing at `a07537869cf37963dff559fc75271dfa8fbb2542`
(2026-10-28T17:59Z). Nothing in `corpus/QUALITY.md` was edited: the L1 lands these or rejects them.
Both rows are written in the file's own admission-table shape (`| # | criterion | why (lesson) | supersedes |`);
the next free number is 88 (the table ends at 87).

## Rows as they would land

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 88 | **A forgery battery scores constructed artefacts, never attempted ones.** Every forged artefact is hashed before it is scored and must differ from the genuine artefact's bytes; a fixture that produced no artefact, mutated nothing, or hashes equal is a battery defect (exit 1, named in the receipt), never a `hole-measured`/`killed` increment. The per-class target is computed over scored forgeries only, so `N forgeries green` cannot be reached with `N-1` constructions plus one no-op. The pin that freezes the mutation set covers the forged artefact digests (behaviour), not the mutation names: a name-only digest cannot see a body that stopped mutating. | Round 47 A2's disclosed red-before: `.ufo/waves/round-47/l1/scores/c2-at-L1.json` scored `battery.forgeries_green 1` because the `correction-window-not-empty` forgery was byte-identical to the genuine correction — a no-op counted as a surviving forgery; the same shape is live in the C1 counter, where `tools/round-47/exact.py:367-371` increments `v2_green` for a mutation that changed nothing (receipt `.ufo/waves/round-47/w1/ScribeQuality/receipt-noop-mutation.json`: `forgeries_total 4 / v2_green 4 / v3_green 0`, `score()` exit 0 `met_target true`). Round 46 M46-1 is the same family from the control side: a control named "at the freeze" whose subject could not exist there (`corpus/lessons/round-46.md`, M46-1). | sharpens 71; extends 40, 69 |
| 89 | **A machine-read repair or exemption section is a closed grammar.** The set of classes the counter's line pattern accepts, the set its dispatcher implements, and the set the claim text declares are one set, asserted at run time; a line that opens with the section's marker and does not parse is a defect (exit 1, named), never silently skipped. Every declared class carries at least one selftest case in which a false value of that class keeps the counter red, so a class whose parser branch is unreachable is caught by the counter's own tests rather than by a reviewer. A repair line the counter cannot evaluate is not evidence that an atom was repaired. | Round 47, at the landing `a0753786`: `## Record corrections — round 47` carries four `- corrects` lines and `tools/round-47/record.py:50` parses two (`corrections: 2`; `.ufo/waves/round-47/w1/ScribeQuality/c2-at-head.json`); both `- corrects axes …` lines are dropped, the `axes` branch at `record.py:280` is unreachable, and its twin at `record.py:292` references an undefined `atom`; replacing the landing's true `138/138` with `999/999` still exits 0 with `corrections_bad []` (`.ufo/waves/round-47/w1/ScribeQuality/receipt-axes-correction-unparsed.json`). Round 36 M36-3 (row 77) is the neighbouring failure — a shadow row overwriting rather than a line being dropped. | sharpens 77, 87; no change to 74 |

## Red-before receipts for row 88

Command (argv, exit, stdout sha256, UTC in `.ufo/waves/round-47/w1/ScribeQuality/runs/manifest.txt`):

```sh
python3 -I -B .ufo/waves/round-47/w1/ScribeQuality/probe-noop-mutation.py \
  --rev a07537869cf37963dff559fc75271dfa8fbb2542 \
  --json-out .ufo/waves/round-47/w1/ScribeQuality/receipt-noop-mutation.json
```

The probe imports the frozen `tools/round-47/exact.py` unmodified, replaces `MUTATIONS[0]`
(`substring-arm`) **in memory** with an identity mutation, and calls the counter's own
`run_battery`/`score`:

| battery | forgeries_total | v2_green | v3_green | genuine_green | fixture entry | score |
|---|---|---|---|---|---|---|
| frozen list | 4 | 4 | 0 | 1 | all four scored, `v2_exit 0 / v3_exit 1` | exit 0, `met_target true` |
| one identity mutation | 4 | 4 | 0 | 1 | `substring-arm`: `"error": "mutation was a no-op"`, no exits | **exit 0, `met_target true`, `failing []`** |

The frozen clause tuple (`exact.py:290`) reads five counters and never reads
`fixtures[*].error`, and the no-op branch (`exact.py:367-371`) adds to `forgeries_total` **and**
`v2_green` — the flattering side. `mutations_sha256` is sha256 over
`"\n".join(name for name, _ in MUTATIONS)` (`exact.py:96`), i.e. names only, so a mutation
whose body stopped mutating keeps the pin. `interpreter_sha256` does see the file, but it is
re-computed from the same measured revision and re-pinned in the same landing commit, so the
pair of pins binds the artefact to the counter's bytes, not the counter's behaviour.

Historical instance in the sibling claim: `.ufo/waves/round-47/l1/scores/c2-at-L1.json` —
`battery.forgeries_green 1`, fixture `correction-window-not-empty` exit 0; disclosed as A2 in
`plans/round-47-claims.md`.

## Red-before receipts for row 89

```sh
python3 -I -B .ufo/waves/round-47/w1/ScribeQuality/probe-axes-correction.py \
  --rev a07537869cf37963dff559fc75271dfa8fbb2542 \
  --json-out .ufo/waves/round-47/w1/ScribeQuality/receipt-axes-correction-unparsed.json
```

| value | landing |
|---|---|
| `- corrects` lines in the card's section | 4 |
| lines `record.py:corrections()` returns | 2 (`seats 45`, `window 46`) |
| lines dropped | `- corrects axes coverage: 138/138`, `- corrects axes depth: 24/24` |
| counter exit with the true fraction | 0 (`corrections 2`, `corrections_bad []`) |
| counter exit with `axes coverage: 999/999` | **0** (`corrections_bad []`, `mismatches 0`, `met_target true`) |

So the claims file's clause 3 sentence "an `axes` correction must state `<resolved>/<total>`"
(`plans/round-47-claims.md`, R47-C2 predicate 3) is a requirement no frozen line evaluates, and
the landing's two axes correction lines certify nothing.

## Rows checked for duplication

Read in full: rows **1–87**, the `Signals of weak material` table (1–6), and the three appended
correction blocks (round 20 wave 2, round 34 run-6). Nearest neighbours compared line by line:

- **40** (a gate ships the legitimate look-alike it could refuse) — my row 88 is the mirror case:
  the *illegitimate* look-alike (a forgery equal to the genuine artefact) is counted as scored.
  Not the same check, and 40 does not constrain a no-op arm.
- **67/69/70/71** (replay classes, invariant coverage, class-set equality, mutant triple) — all
  assume the mutation produced an artefact; none constrains construction failure.
- **77** (enumerate every occurrence; keep duplicates as separate units) — 89 is about lines the
  parser never admits, not about occurrences collapsing into one key.
- **87** (claim prose the instrument does not implement) — 89 is a strictly narrower, mechanically
  checkable instance: the repair grammar's closure and its per-class selftest. If the L1 judges 89
  redundant with 87, the surviving half is the per-class selftest requirement, which 87 does not
  state.
- **21/73** (a verdict is not the compared object; a receipt states what produced it) — 88's
  hashing-before-scoring clause is adjacent but not covered: neither requires the forged input to
  differ from the genuine one.

## Not drafted (reported as findings instead)

three further holes are real but do not generalise to a criterion in this round's evidence:
the C2 counter takes no `--freeze` (no frozen-path or dirty-worktree guard, though the claims file
says both counters exit 2 on a frozen-path change); a `window` atom whose pathspec matches no
tracked path is scored `atom_ok: true, empty: true` while the same window over a real path is not
empty, and the same true claim written with the paths in backticks is scored red because the
regex captures nothing (`receipt-window-pathspec.json`, three arms); and the claims file's freeze
re-derivation command returns the last touch, not the first freeze. They are recorded in
`../ScribeQuality.md` with receipts.
