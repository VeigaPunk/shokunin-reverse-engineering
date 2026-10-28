# R45W2CritC2Text — falsifying R45-C2's text against its own instrument

Seat `R45W2CritC2Text` (critic, wave 2). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`;
amendment A1 / measured revision `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`.

Instrument under test: `tools/round-45/c2-counter.py`, sha256
`50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025` (identical in the worktree and
at A1, verified below); scope file `tools/round-45/registry-scope.json` sha256
`6e2dda713a474dd6479a0af1430af9f38013d058a7cf9d2cc3fe293b9bd8dff9` (same at A1).
Rule followed: `plans/round-45-claims.md` is the rule; frozen bytes read-only; every attack ran
against fixture repos or against the lane read-only. Scratch
`S=/fast/scratch/hyaku/kaidoku-r45/R45W2CritC2Text`, `TMPDIR=$S`, removed after receipts were copied.

## 0. Verdicts

| # | attack | verdict | receipt |
|---|---|---|---|
| A1 | scope identity: "the instruments named by the round-44 and round-45 frozen claim files" == the six paths in `registry-scope.json` | **falsified** — 9 tool paths are named; 6 are in scope. Wording defect, already partly routed (R45-CL17 / R45-CL3); the correction did not propagate to three editable record surfaces (new) | `receipts/rederive.out` sha256 `069d0e35…` |
| A2 | "thin" = "exit-code cell (third column) names `0`, `1` and `2`" matches code's `\b0\b/\b1\b/\b2\b` | **holds** for the landed six and for the literal words; the code's test is token presence, so **A2b** (a cell that names them only to negate them) is **falsified** | `receipts/mutations.json` |
| A3 | "some `SKILL.md` **registry** row" — code accepts any table row | **falsified** — rows under a non-registry heading, or inside a code fence, register | `receipts/mut.log` |
| A4 | "first cell **is exactly** that path" | **falsified** — `re.search`; extra prose beside the path registers | `receipts/mut.log` |
| A5 | duplicate rows: "some row" (existential) vs `by_tool.setdefault` (first wins) | **falsified** — thin-first/good-second is a false red; good-first/thin-second is a silent false green (new direction) | `receipts/mutations.json` |
| A6 | "C2's counter … never reads block 22" (causal separability) | **falsified** — a block-22-shaped table (`<!-- freeze-integrity-table v1 -->`, `trigger\|arm\|exit\|receipt`) whose third cell is `0, 1, 2` scores `met_target: true` (new; wave 1 did not name this) | `receipts/block22seam.stdout` sha256 `156f1477…` |
| A7 | exit 2 "freeze not an ancestor" arm | **holds** functionally (live exit 2); **no selftest case** covers it (new gap) | `receipts/nonancestor.stdout` sha256 `c1b9db74…` |
| A8 | Before/after numbers (freeze exit 1, six unregistered; base exit 2; A1 exit 0) | **holds** — receipt byte-identical to the committed control and to `.ufo/waves/round-45/l1/scores/c2-at-1f4b27f8.json` | `receipts/real.json`, `freeze.stdout`, `base.stdout` |
| A9 | six landed rows genuine (exact first cell, third cell a real exit map, one row each) | **holds** | `receipts/parser2.json` |
| A10 | "`grep -c 'round-44' SKILL.md` printed 0"; lesson citation `…spotcheck.md:166` | **holds** — 0 at base and at freeze (8 at A1); line 166 is the registry-row routing item | §3 |

Nothing below says the landing's bytes are fake. The six rows are real, the before is authentic,
the after receipt reproduces exactly. The defects are **text-vs-instrument**: sentences in the
frozen claim and in the editable record that assert a stricter check than the 268-line counter
performs. Wave 1 already routed F2/F3/F4 of the same family (`R45-CL14`, `R45-CL9`); §9 states
which part of each finding is already on record and which is new.

## 1. Scope honesty — re-derived from the two claim files

Command: `python3 -I -B $S/rederive.py` (UTC 2026-10-28T16:03:36Z, exit 0, stdout sha256
`069d0e359ae7b803f789b8ef9236e3b3f1c37661aba494ef4e8b1db7bafd54ce`). It extracts every
`tools/*.{py,sh,mjs}` token from each claim file and diffs against `registry-scope.json`.

```
round-44-claims.md names: tools/round-27/xpin-attribute.mjs, tools/round-42/c1-counter.py,
  tools/round-43/c1-counter.py, tools/round-44/c1-counter.py, tools/round-44/c1-run.sh,
  tools/round-44/c2-counter.py                                    (6)
round-45-claims.md names: the three tools/round-44/* above + tools/round-45/{c1-counter.py,
  c2-counter.py, frozen-path-preflight.py}                        (6)
union named = 9; scope = 6; named_minus_scope = [round-27 xpin-attribute.mjs,
  round-42/c1-counter.py, round-43/c1-counter.py]; scope_minus_named = []
```

So the six are **not** "the instruments named by the round-44 and round-45 frozen claim files";
they are the round-45 claim's own enumeration (its six-item list), which is exactly what
`registry-scope.json`'s `paths` array holds. The extras are not incidental: round-44 names
`tools/round-43/c1-counter.py` as its "Freeze-walk port source" (`plans/round-44-claims.md:28`),
`tools/round-42/c1-counter.py` as the counter it ports (`:120`), both as byte-frozen
"audit-only port sources" (`:308`), and `tools/round-27/xpin-attribute.mjs` as a vendored
missing-input (`:55`).

Exact words that are false under that re-derivation:

- `plans/round-45-claims.md:23` (claim table): "the `SKILL.md` instrument registry vs **the
  instruments the two most recent frozen claim files name**"
- `plans/round-45-claims.md:92-93` (Scope): "**the instrument set named by** `plans/round-44-claims.md`
  and `plans/round-45-claims.md`"
- `tools/round-45/registry-scope.json:2`: "the instruments named as instruments by the round-44
  and round-45 frozen claim files"
- `tools/round-45/c2-counter.py:5-6` (docstring): "the instruments named by the round-44 and
  round-45 frozen claim files"
- `SCORECARD.md:3533`: "vs **the six instruments the round-44 and round-45 frozen claim files
  name**"
- `LOG.md:3239-3240`: "**the six instruments named by** the round-44 and round-45 frozen claim
  files each carry a `SKILL.md` registry row"
- `corpus/lessons/round-45.md:80-81` (R45-CL3): "The C2 scope is **the six instruments the two
  most recent frozen claim files name**. Rounds 41–43 tools (`tools/round-41/*`,
  `tools/round-42/*`, `tools/round-43/*`) remain unregistered" — the second sentence concedes
  the first is not a derivation.

What is *true*: the six are the claim-carrying instruments of the two rounds (three round-44
claim instruments + three round-45); the port-source counters are explicitly "audit-only" and
the `.mjs` is a vendored input, so excluding them is defensible — but that exclusion rule exists
only in `registry-scope.json`'s `why` field ("the whole claim-carrying instrument set"), not in
the claim text, and the `why` census itself stops at the two triples ("plans/round-44-claims.md
names c1-counter.py, c1-run.sh and c2-counter.py"), which is incomplete for that file.

**Already on record.** `R45-CL17` (`corpus/lessons/round-45.md:188-196`) corrects the *scope
file's* sentence, and `R45-CL3` (`:80-83`) carries the widening. **New in this seat:**
(1) the correction did not propagate — `SCORECARD.md:3533`, `LOG.md:3239-3240` and the lesson's
own CL3 still assert the corrected-away wording, and all three are editable (the claim names
`SKILL.md`, `LOG.md`, `SCORECARD.md` and the lesson as **not** frozen, `plans/round-45-claims.md`
§"Frozen paths"); (2) CL17's own census names **eight** paths, missing
`tools/round-27/xpin-attribute.mjs` — the ninth; (3) the `.mjs` could never register even if
widened, because `ROW_TOOL` is `tools/…\.(?:py|sh)` (`c2-counter.py:31`): a `.mjs` scope entry
returns `unregistered` and `scope_size 7 != 6` (fixture `mjs-scope-path`, exit 1).

**Smallest safe correction.** Replace the scope sentence everywhere it appears with the CL17
wording plus its census: "the six instruments this round's claim enumerates, three carried over
from round 44; `tools/round-42/c1-counter.py` and `tools/round-43/c1-counter.py` are round-44
audit-only port sources and `tools/round-27/xpin-attribute.mjs` a vendored input — all three are
outside the scope and their registration is R45-CL3." Apply it to `SCORECARD.md:3533`,
`LOG.md:3239-3240` and CL3 now; the frozen three (`claims.md`, `registry-scope.json`,
`c2-counter.py`) are a round-46 refreeze, which CL3/CL17 already route.

## 2. The `thin` definition against the code

Claim (`plans/round-45-claims.md:108-109`): "`thin == []` — that row's exit-code cell (third
column) names `0`, `1` and `2`; a bare "non-zero" cell is thin."
Code (`c2-counter.py:59-60`): `exits_ok(cell) = all(re.search(r"\b%d\b" % d, cell) for d in (0,1,2))`,
applied to `row["cells"][2]` (`:107`), where cells are the naive `split("|")` strip (`:49`).

- Third column ↔ `cells[2]`: **holds**. All six landed rows have `ncells=7` and `exits_ok=True`
  (`receipts/parser2.json`), i.e. column 3 is the verdict map for this table shape.
- "names 0, 1 and 2" ↔ three word-boundary tokens: **holds literally**. A bare `non-zero` cell
  has no digits → `thin` (selftest `red-thin-exit-cell`; my `empty-exit-cell` → `thin`).
- **A2b falsified**: the test is presence, not a declared map. Fixture
  `negation-cell-names-0-1-2` gives the row exit cell "never `0`; never `1`; never `2`" →
  counter exit **0**, `thin []` (`receipts/mutations.json`, receipt sha
  `637a60eb0e765eb1df12010e4a7413b9c977b984e54871436fd04b14cd2819c9`). A cell that declares no
  reachable exit code passes. The same escape is already on record as `R45-CL9` A6 / `R45-CL14(d)`
  ("`0 rows, 1 column, 2 bytes`"); the negated shape is new but the class is routed.
- Live context for the column claim: `parse_rows` does not know what a column means. It takes
  any `|`-line; 11 of the 45 parsed rows sit under `### Round-30/31 **measurement** registry`
  headings whose third column is a shell command (`receipts/parser2.json`,
  `rows_outside_instrument_registry: 11`). A scope path in that table would be scored against a
  command line, and `registry_rows: 45` counts all of them.

**Smallest safe correction.** Require the three codes as ordered code spans —`` `0` … `1` … `2` ``
— in the exit cell, and reject a cell whose code token is preceded by a negation (`not|never|no`).
That keeps every real registry row (all six use `` `0` …; `1` …; `2` … ``) and closes A2b.

## 3. What holds, measured

All UTC 2026-10-28; commands as given; `receipts/` holds the captures.

| check | command | exit | stdout sha256 |
|---|---|---|---|
| A1 score | `python3 -I -B tools/round-45/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze f762b727… --rev 1f4b27f8… --json-out $S/real.json` (16:01:30Z) | **0** | `2b401a9ae5a6e562178561fba15b2ae2199f019e9b1059b0b6f65175d5e4d1ca` |
| selftest | `python3 -I -B tools/round-45/c2-counter.py --selftest` (16:01:30Z) | **0** | `aea7e363…b40b0f2d`; `C2_SELFTEST: cases=7 failures=0` |
| do-nothing at freeze | `… --freeze f762b727… --rev f762b727…` (16:01:41Z) | **1** | `d6e202aa…9216dd0`; `unregistered` = all six, `registered []`, `thin []`, `registry_rows 39` |
| base | `… --freeze 149133d4… --rev 149133d4…` (16:01:41Z) | **2** | `ab4227f8…4d9f254`; `{"reason": "scope file absent at rev"}` |

The A1 stdout JSON is **identical** to `.ufo/waves/round-45/l1/scores/c2-at-1f4b27f8.json` (diff
empty), and identical to the "after" values in `SCORECARD.md:3533`. The freeze and base receipts
are the committed controls (`controls/ctl-c2-0-do-nothing.json`,
`controls/ctl-c2-0-base-unevaluable.json`) field for field. `registered` lists all six; each of
the six appears in exactly **one** row (no duplicates in the landed text); `cell0` is the exact
backticked path and `cell2` a real map for every one (`receipts/parser2.json`, 45 parsed rows).
`registry_rows` goes 39 → 45 (+6), matching "six `SKILL.md` registry rows".

Other text claims checked: `grep -c 'round-44'` = 0 at base `149133d4` **and** at the freeze (8
at A1), so "printed 0 before this round" is true and conservatively so; the round-44 closure
citation `corpus/lessons/round-44-verifier-spotcheck.md:166` resolves to the "**no SKILL.md
registry rows** for the round-44 counters" item; `c2-counter.py` contains no craft-section or
`freeze-integrity-table` token (static grep), and `c1-counter.py` contains no registry read.

## 4. "Registry row" vs any table row (A3) and first-cell exactness (A4)

Fixtures (`receipts/mut.log` sha256 `12bba3a9…`, UTC 16:02:01Z; driver `receipts/driver.py`,
frozen counter run unmodified with `-I -B --root $D --freeze $F --rev $F`; `--show-toplevel`
asserted equal to `$D` before every commit):

| case | expect | got | receipt sha256 |
|---|---|---|---|
| `green-registry` (registry heading, 7-col rows) | 0 | **0** | `f71d8a96…` |
| `decoy-heading-not-a-registry` (`## Counting commands (not a registry)` only) | 0 | **0**, all six registered | `d6ec9877…` |
| `fenced-code-block` (rows inside ` ``` `) | 0 | **0**, all six registered | `34163ee5…` |
| `first-cell-extra-prose` (`` the `PATH` gate ``) | 0 | **0**, registered | `66289720…` |
| `duplicate-first-thin-second-full` | 1 | **1**, `thin ["tools/round-44/a.py"]` | `a80fce46…` |
| `duplicate-first-full-second-thin` | 0 | **0**, `thin []` | `308051b1…` |
| `mjs-scope-path` (scope includes the round-27 `.mjs` + a row for it) | 1 | **1**, `scope_size 7`, `unregistered [.mjs]` | `a9e41bc1…` |

A3 and A4 are `R45-CL9` A3/A4 and `R45-CL14(a)/(b)` verbatim in class; the two duplicate
directions are the new datum. `by_tool.setdefault(row["tool"], row)` (`:97-98`) keeps the first
row and silently drops the rest, so **a corrected row appended below a thin row cannot clear
`thin`** (false red), and **a thin duplicate below an honest row is invisible** (false green).
CL14(c) records only the shadow direction ("a fenced good row shadows an honest thin row").
The landed text has one row per path, so the landing is unaffected.

## 5. The separability sentence is false (A6, new)

Claim (`plans/round-45-claims.md:25-27`): "C2's counter reads the registry rows and the scope
file; **it never reads block 22**. Either lands and scores without the other."

The counter calls `show(root, tip, "SKILL.md")` (`:91`) and hands the **whole file** to
`parse_rows`, which has no section state (`:43-56`). Fixture `block22seam` (UTC 16:04:13Z, exit
**0**, stdout sha256 `156f147713039140ad9640850eab28763d28a50033b100fa45823c6aa2d84552`):
`## Queue-drain craft` + `- **rule**` + `<!-- freeze-integrity-table v1 -->` + a 4-column
`trigger | arm | exit | receipt` table whose cell 0 is a scope path and whose cell 2 is
`0, 1, 2` → `{"met_target": true, "registered": [all six], "thin": [], "unregistered": []}`.
So C2 is satisfiable **inside C1's own artifact**: the two surfaces are not disjoint, and a
single block-22 table can carry both claims. The sentence is false as written, and the wave-1
critic never named it (`grep 'separab\|block 22\|block22'` on `.ufo/waves/round-45/w1/R45W1CritC2/report.md` → no match).

The landed revision is **not** contaminated: block 22's ten cell-0 triggers are prose and the
only `tools/` text inside the block's span is prose at `SKILL.md:609`, outside the table; no
parsed row falls in the block. Impacted axis: the claim's causal-separability architecture
(provenance of the two scores), plus calibration.

**Smallest safe correction.** Either drop the sentence to "the two counters share `SKILL.md` but
read different structures; a row placed in any table, including block 22's, would count for C2"
(round-46 refreeze), or adopt §4's section-scoped parser, which makes the sentence true.

## 6. The untested non-ancestor arm (A7, new)

Claim/docstring exit-2 list includes "freeze not an ancestor" (`c2-counter.py:11-13`); the live
arm is correct — orphan-branch fixture, `freeze=73d46e1c…`, `rev=e86c0675…`, UTC 16:03:36Z,
exit **2**, `{"reason": "freeze is not an ancestor of rev"}`, stdout sha256
`c1b9db741fabb5e758958cbff3172c9280589cc972b826d84379129bbf3efe59`. The 7-case selftest covers
`green`, `red-unregistered`, `red-wrong-path-rows`, `red-thin-exit-cell`, `red-unknown-rev`,
`red-frozen-touched`, `red-scope-size` — **none** exercises non-ancestry. `R45-CL8` names two
selftest holes (suffix lookup, any-cell lookup); this is a third, of the same kind.

## 7. Impacted axes

- **calibration (R45-C2's own axis)** — the measure overstates its strictness in five sentences
  (§1, §2, §4, §5), and `SCORECARD.md:3533` / `LOG.md:3239-40` / CL3 re-assert the over-claim
  that the lesson's CL17 corrects. The scoring number (`unregistered 6 → 0`, `thin 0`) stands.
- **record provenance** — a correction that landed only in the lesson while three editable
  surfaces still print the corrected-away rule; and CL17's census is 8 of the 9 named paths.
- **not impacted**: coverage (no domain surface), depth (C1's block is genuine; §5 only shows
  the C2 predicate can be satisfied by it, not that C1's rows are fake).

## 8. Disposition

- The landing **survives** as a score: A1 receipt exit 0, byte-identical to the committed score;
  six genuine rows; authentic before; the do-nothing control cannot reach it.
- What must change is the **description**: the scope sentence (all sites, per §1), the "registry
  row" / "first cell is exactly" / "never reads block 22" sentences, and the `thin` test's
  token-presence escape. The three frozen carriers are a round-46 refreeze (already routed as
  R45-CL2/CL3/CL14/CL17); `SCORECARD.md`, `LOG.md` and the round-45 lesson are editable and
  should carry the corrected wording in this round's record.
- No mutation of any frozen path was attempted; the lane tree was read-only; fixtures lived
  under `$S` and were removed.

## 9. What was already on record (calibration, not padding)

| finding | already on record? |
|---|---|
| any-heading / fenced / extra-prose / token-presence escapes | **yes** — `R45-CL9` A3/A4/A6, `R45-CL14(a)(b)(d)`, wave-1 `R45W1CritC2` §0 F2-F4 |
| scope over-attribution to the two claim files | **partly** — `R45-CL17` (scope file only), `R45-CL3` |
| correction not propagated to SCORECARD/LOG/CL3; ninth path missing | **no** — new here |
| block-22 separability is false in practice | **no** — new here |
| duplicate thin-first false red / thin-second false green | **partly** — `R45-CL14(c)` names one direction |
| non-ancestor exit-2 arm has no selftest case | **no** — new here (CL8 names two other holes) |

## 10. Receipt index (`receipts/`)

`real.stdout` `2b401a9a…d5e4d1ca` · `real.json` `0daf63d3…3c0abb9` · `st.stdout` `aea7e363…0f2d`
· `freeze.stdout` `d6e202aa…6dd0` · `base.stdout` `ab4227f8…f254` · `mut.log` `12bba3a9…25b703`
· `mutations.json` `fe6cbb50…98ad86` · `rederive.out` `069d0e35…fd54ce` · `nonancestor.stdout`
`c1b9db74…3efe59` · `block22seam.stdout` `156f1477…d84552` · `parser.json` `c1e42ac6…a2d2ae`
(2390 B) · `parser2.json` `4f3f3d17…b76d4148a` (4003 B, the cited dump) · `driver.py`
`rederive.py` (harnesses).

Discipline note: one batch contained a stray `cp … /tmp/x`; `/tmp/x` was deleted immediately and
nothing in this report cites anything under `/tmp`. Scratch `$S` removed after the copy.
