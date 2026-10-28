# R46W1CritC2 — attack on R46-C2 (`tools/round-46/registry.py`) before data

Seat: critic, round 46 wave 1. Lane `kaidoku-shokunin`. Freeze under test
`31820472784284727546808acc31b3ea1e73919b` (the only commit that ever touches
`plans/round-46-claims.md`: `git log --format='%H' -1 -- plans/round-46-claims.md` →
`3182047…`). I am read-only on the lane tree; every fixture below is a fresh
`git init` in `/fast/scratch/hyaku/kaidoku-r46/R46W1CritC2` (removed before yield).
My report receipts are under `.ufo/waves/round-46/w1/R46W1CritC2/receipts/`.

**Verdict: R46-C2 is not met, and as frozen it is not satisfiable.** The instrument
cannot reach its own target at the freeze (clause 6 is arithmetically unreachable with
the frozen bytes), and at every revision after the freeze it exits 2 (clause 7). The
"met" the lane reports is produced by passing `--freeze` equal to `--rev`, which makes
clause 7 vacuous. Separately, the landed instrument scores **exit 0 / `met_target: true`**
for six artefacts that are not the intended registry, the cheapest being **one table row
plus a one-path `census.json`**.

Nothing in this report edits the instrument. The landed `SKILL.md` registry *content* is
the intended artefact: at `49e6cac4` the marked section parses to 38 rows, every row has
exactly 7 cells, no path is duplicated, and every verdict-map cell binds all three codes
to non-empty meanings (`receipts/landed-registry-audit.out`). The defects are in the
measure, not in the rows — and the measure cannot tell that artefact from a one-row
one.

---

## F1 (decisive) — the freeze argument is caller-supplied and never pinned; the "met" receipt is `--freeze == --rev`

The claims file's own rule: *"Freeze = the commit that first contains this file and
`tools/round-46/`… `git log --format=%H -1 -- plans/round-46-claims.md` re-derives it."*
`registry.py` takes `--freeze` as an argument and `gate.freeze_state` only checks
`merge-base --is-ancestor`; nothing compares it to the claims-file derivation. With
`--freeze == --rev` the range `freeze..rev` is empty, so clause 7 (`frozen_path_changed
== []`) is trivially true.

```sh
python3 -I -B tools/round-46/registry.py --root <lane> \
  --freeze 3182047… --rev 0425224… --no-battery      # exit 2 (the claim's own freeze)
python3 -I -B tools/round-46/registry.py --root <lane> \
  --freeze 0425224… --rev 0425224…                   # exit 0, met_target true
```

| run | exit | receipt |
|---|---|---|
| freeze `3182047`, rev `0425224` (the claimed met rev) | **2** | `reason: frozen_path_changed`, `frozen_path_changed: ["tools/round-46/", "tools/round-46/attest.py", "tools/round-46/gate.py", "tools/round-46/registry.py"]`, `sha256 2f6a9035…` (`receipts/c2-at-0425224.out`) |
| freeze `3182047`, rev `49e6cac4` (HEAD at run time) | **2** | same four paths, `sha256 683ba55f…` (`receipts/c2-at-head.out`) |
| freeze `0425224`, rev `0425224` | **0** | `scope_size 38`, `unregistered []`, `thin []`, `absent_at_rev []`, `battery 7/7/0/1`, `met_target true`, `sha256 d3869553…` (`receipts/c2-freeze-eq-rev.out`) |

The lane's own score file `.ufo/waves/round-46/l1/scores/c2-at-F4.json` is exactly the
third row: `freeze == rev == 0425224756791b414454df28a9abf93dcdf154ce`,
`met_target: true`, `frozen_path_changed: []`. Its `--freeze` is *not* the freeze the
frozen claims file derives. The same pattern is in the "Before" control the claims file
cites: `controls/ctl-c2-0-do-nothing.json` records
`freeze == rev == 50862e4a041499dd2ce0da68d10301b765bb9997`, a post-freeze commit — so
the do-nothing control is not scored against the freeze either.

**Why the freeze is broken at all.** `tools/round-46/` was edited three times after
`3182047` (`50862e4a`, `65678df0`, `0425224`). Blobs at the freeze vs HEAD:

```
tools/round-46/attest.py    25883520…  936910fe…  differ
tools/round-46/gate.py      d7cd9aac…  9ab7e2a3…  differ
tools/round-46/registry.py  6581c1b2…  26f9e9c6…  differ
tools/round-46/ (tree)      bf60ef5d…  517ecf69…  differ
```

Renaming the freeze in a commit message ("declared as the authoritative freeze because
the first freeze commit did not carry the final bytes", `50862e4a`) does not change what
the frozen file says the freeze is. Either the freeze is `3182047` and the instrument
was changed after it (claim dead), or the claims file's freeze rule is revised — which
cannot be done inside a file that is itself frozen.

## F2 — the frozen bytes cannot reach the clause-6 target at all (`battery v1_green 5 != 7`)

At `3182047` the v1 profile is not the loose round-45 port: `score()` consults
`spec["strict_cell"] / strict_exit / presence` without the `hard` guard, so v1 applies
the v2 checks. Two of the seven forgeries (`substring-cell`, `prose-exit`) therefore
score **red under v1**, and `v1_green` is 5, not the required 7.

```
frozen (3182047) evaluate(), freeze==rev, honest two-row artefact:
  exit 1, failing ["battery v1_green 5 != 7"]
  battery {forgeries_total 7, v1_green 5, v2_green 0, genuine_green 1}
  fixtures: substring-cell v1_exit 1, prose-exit v1_exit 1, others v1_exit 0
```
(`receipts/probe3-frozen-full.out`, P1.)

The frozen `--selftest` does not catch it: it prints `cases=12 failures=0`
(`receipts/frozen-selftest.out`). That is the repair `0425224` ("F4") made — the very
edit that makes clause 7 fail.

The claims file's Satisfiability preflight also states the wrong count:
`registry.py --selftest` prints **`cases=12 failures=0`** at the freeze, not `cases=11`
(`attest.py` prints `cases=15`, which matches). Minor, but it is a preflight number the
frozen file asserts and the frozen bytes contradict.

## F3 — the census is trusted data, never re-derived: the cheapest green artefact is one row

`load_scope()` reads `tools/round-46/census.json` and nothing ever compares it with
`census.py`'s derivation. Hand-shrinking the census shrinks the predicate. Full
evaluation with the battery on a fixture whose claims file names two tools while
`census.json` lists one:

```
fixture: claims name tools/round-46/a.py and b.py; census.json {"paths":["tools/round-46/a.py"]}
         SKILL.md registry = one row `| `tools/round-46/a.py` | x | 0=; 1=; 2= | x | x | x | x |`
exit 0, scope_size 1, registry_rows 1, unregistered [], thin [], absent_at_rev [],
met_target true, battery {7, v1_green 7, v2_green 0, genuine_green 1}
```
(`receipts/attack-head.out`, `HEAD cheapest-junk-artefact (full)` and
`HEAD census-shrunk-to-one-row (full)`, both exit 0.)

The seven-forgery battery still passes because every mutation operates on that one-row
table — the battery cannot drift from the artefact, as the claims file intends, but it
also cannot notice that the artefact is one row. The real census is honest (I re-derived
it at `3182047`, `0425224` and `49e6cac4`: 38 paths each, byte-equal to the committed
`census.json`, `named_but_absent []` — `receipts/census-derived-HEAD.json`); the point is
that the *instrument* gives no evidence for that, so the clause "generated by
`census.py` and never edited by hand" is unmeasured.

## F4 — a row can satisfy a census path while describing a different tool

Cell 0 is exact (`row[0].strip()` must be a whole backticked path) but **no other column
is read except the verdict map**. A row whose purpose cell says the tool prints the
weather scores the same as the honest row:

```
| `tools/round-46/a.py` | prints the weather forecast; computes nothing | 0=met; 1=not met; 2=could-not-evaluate | `--selftest` | none | repo | kaidoku |
→ exit 0, met_target true   (frozen and HEAD instruments alike)
```
(`receipts/attack-frozen.out` `lying-purpose-cell`; `receipts/attack-head.out`
`HEAD lying-purpose`.)

This is `R45-CL14 b` (substring cell) re-expressed one column to the right: the round-45
hole was "cell 0 matched by `re.search`"; the v2 hole is "cells 1, 3, 4, 5, 6 are never
read". The house schema names the column *`gate or probe - purpose`*; the predicate never
looks at it.

## F5 — the verdict-map cell binds nothing (`0=x; 1=y; 2=z; <garbage>` passes)

`EXITMAP = \b([012])\s*[=:]` and the only test is `set(keys) == {"0","1","2"}`. All of
these are green (frozen instrument, `receipts/attack-frozen.out`):

| cell | parsed | exit |
|---|---|---|
| `0=; 1=; 2=` | binds all three to **empty** | 0 |
| `0: 1: 2:` | same, colon form | 0 |
| `0=met; 1=not met; 2=could-not-evaluate; 999=padding !!garbage` | trailing garbage accepted | 0 |
| `0 rows, 1 column, 2 bytes` | no `=`/`:` after a digit | **1** (the only one caught) |

So the clause "a cell that merely mentions the digits is thin" is enforced only against
one spelling. `0=; 1=; 2=` *is* a mention — three empty bindings — and it is the cheapest
cell an author can type. The round-45 hole was "any cell containing 0, 1 and 2"; v2
requires `0=`, `1=`, `2=` but does not require a meaning after `=`. Positive control for
the correction: a "non-empty meaning after each binding, no binding outside `{0,1,2}`"
test reds **none** of the 38 honest rows (`landed-registry-audit.out`,
`rows failing the strong verdict test: []`), so tightening this clause costs nothing.

## F6 — fence/comment binding is section-local: an outer fence or comment bypasses clause 1

`split_section` slices between the markers and `rows_in_section` starts with
`fence = comment = False`. A section rendered inside a fenced code block or an HTML
comment — markers **and** rows inside it — registers everything:

```
```markdown
<!-- instrument-registry v2 -->
| tool | … |
|---|---|
| `tools/round-46/a.py` | … |
<!-- /instrument-registry -->
```
→ exit 0, met_target true   (frozen and HEAD)
```
(`attack-frozen.out` `section-inside-outer-fence`, `section-inside-outer-comment`;
`attack-head.out` `HEAD outer-fence`.) The claim's clause 1 says "Rows register only
between them, outside fenced blocks and outside HTML comments" — a reader sees a code
sample and the predicate sees a registry. The declared forgery `fenced` only wraps rows
*after* the open marker, so the battery does not cover this orientation.

Same class, milder: a **section left with an unclosed fence or comment after a complete
table** scores 0 (`unclosed-fence-after-rows`, `unclosed-html-comment-after-rows`). A
malformed document is not a predicate failure here; the C1 claim makes the analogous
malformed heading exit 2, so the two instruments disagree about malformation.

## F7 — a `\|` in a rendered cell diverts the parsed verdict column

`rows_in_section` splits on every `|` after `strip("|")`; it has no escape handling. A
purpose cell containing the Markdown escape `\|` inserts a cell, so the parser's `row[2]`
is a fragment of the *purpose*, while the reader's third column is prose:

```
| `tools/round-46/a.py` | see x\|0=a; 1=b; 2=c | non-zero on failure | `--selftest` | none | repo | kaidoku |
                                    ↑ parser's row[2] = "0=a; 1=b; 2=c"   ↑ reader's verdict map = "non-zero on failure"
→ exit 0 (thin []), frozen instrument      (attack-frozen.out `escaped-pipe-smuggles-verdict`)
```

The rendered artefact has a prose verdict map; the instrument reads digits. Rows also
carry no arity check for C2: a row with three extra cells after `owner` scores 0 with
`registry_rows 2` (`receipts/probe-arity.out`, `{"case": "ten-cell-row", "exit": 0}`), so
the extra cell is not noticed. This is the inverse of `R45-CL14 b` — the substring hole
now runs from reader to parser instead of from path to cell.

## F8 — duplicate registration: first wins, and a fat row shadows the honest thin row

`by_path.setdefault(key, row)` — the first row for a path decides. Order-dependent, and
the claim text does not say which duplicate counts ("*That row's* verdict-map cell"):

| order | exit |
|---|---|
| fat row, then thin honest row (`non-zero on failure`) | **0** — thin one never seen (`duplicate-fat-then-thin`) |
| thin honest row, then fat row | 1 — `thin: ["tools/round-46/a.py"]` (`duplicate-thin-then-fat`) |

The declared forgery `first-wins-shadow` only covers the fenced variant (a good row in a
fence before the honest thin row), so the unfenced shadow is unmeasured. With the L1
pasting 38 rows by hand, a duplicate is one paste away.

**Census duplicates** (the seat's question 6): `load_scope` does
`list(dict.fromkeys(paths))`, so `{"paths":[a, b, a]}` scores with `scope_size 2`, exit 0
(`duplicate-census-path`). De-duplication is the safe behaviour — a repeated census entry
cannot inflate the target — but the receipt reports only the deduped count, so the
input arity is not visible in evidence.

## F9 — `absent_at_rev` is computed from the census ∩ rows: a ghost row outside the census is invisible

`absent = [p for p in registered if files(p) is None]` where `registered` is built by
walking `scope` (the census). A row naming a path that is **not** in the census is never
presence-checked and never thin-checked:

```
| `tools/round-46/ghost.py` | … | 0=met; … | … |            (no such file at --rev)
→ exit 0, met_target true, absent_at_rev []      (frozen and HEAD; registry_rows 3)
```
(`attack-frozen.out` `ghost-row-outside-census`; `attack-head.out`
`HEAD ghost-row-outside-census`.)

Clause 5 reads "*Every registered path* exists at `--rev` (`R45-CL2`)". The instrument's
`registered` means "*census path with a row*". So the `R45-CL2` ghost hole is closed only
inside the census — which matters precisely because F3 shows the census is the shrinkable
part. Inside the census the clause does work: a census path with a row and no file gives
`absent_at_rev: ["tools/round-46/ghost.py"]`, exit 1 (`probe3-frozen-full.out`, P2).

## F10 — `restored` is false provenance whenever the frozen set holds a directory

`blob_changed()` reports a directory path (`"tools/round-46/"`) for a dir entry;
`restored = [p for p in touched if p not in changed]` then compares *file* names in
`touched` against the *directory* entry, so every touched file is reported as
"restored". At `--freeze 3182047 --rev 0425224` the receipt says

```
restored: ["tools/round-46/attest.py", "tools/round-46/gate.py", "tools/round-46/registry.py"]
touched:  same three
blob_changed: ["tools/round-46/"]
```

while all three blobs genuinely differ (ids in F1). The claims file defines `restored` as
"a path the history arm saw and the blob arm finds clean"; the blob arm never examines
those paths. For a directory freeze `restored` is structurally the whole `touched` list.
This is a receipt-truth defect shared with `attest.py` (C1 clause 8) via `gate.py`.

---

## Attack table (frozen bytes `3182047`; HEAD column from `registry.py@49e6cac4`)

| # | attack | expected | observed (frozen) | observed (HEAD) |
|---|---|---|---|---|
| 0 | two honest rows (baseline) | 0 | 0 | 0 |
| 1 | exact cell 0, purpose "prints the weather" | 1 | **0** | **0** |
| 2a | verdict `0=; 1=; 2=` | 1 | **0** | **0** |
| 2b | verdict `0=met; 1=…; 2=…; 999=padding !!garbage` | 1 | **0** | not run |
| 2c | verdict `0: 1: 2:` | 1 | **0** | not run |
| 2d | verdict `0 rows, 1 column, 2 bytes` | 1 | 1 (caught) | 1 |
| 3a | `\|` in purpose diverts parsed column | 1 | **0** | not run |
| 3b | unclosed fence after the rows | 2 malformed | **0** | not run |
| 3c | unclosed HTML comment after the rows | 2 malformed | **0** | not run |
| 3d | section inside an outer fence | 1 | **0** | **0** |
| 3e | section inside an outer HTML comment | 1 | **0** | not run |
| 4a | duplicate: fat then thin | 1 or 2 | **0** | **0** |
| 4b | duplicate: thin then fat | 1 | 1 | not run |
| 5a | ghost row outside the census | 1 | **0** | **0** |
| 5b | ghost path in the census + row | 1 | 1 (`absent_at_rev`) | not run |
| 6 | census lists a path twice | 0 (dedupe) | 0 (`scope_size 2`) | not run |
| 7 | census shrunk below `census.py` | 1 | **1 for the wrong reason**: `battery v1_green 5 != 7` (structural was green) | **0, met_target true** |
| 8 | honest artefact, full battery, at the freeze | 0 | **1** (`v1_green 5 != 7`) | 0 |

Frozen receipts: `receipts/attack-frozen.out`, `receipts/probe3-frozen-full.out`.
HEAD receipts: `receipts/attack-head.out`.

## Cheapest artefact that scores green without being the intended registry

Verified bytes (`attack-head.out`, `HEAD cheapest-junk-artefact (full)`), exit 0,
`met_target true`, battery 7/7/0/1:

`tools/round-46/census.json`
```json
{"paths": ["tools/round-46/a.py"]}
```

`SKILL.md`
```markdown
### Round-46 instrument registry

<!-- instrument-registry v2 -->

| tool | gate or probe - purpose | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
| `tools/round-46/a.py` | x | 0=; 1=; 2= | x | x | x | x |

<!-- /instrument-registry -->
```

one row, a purpose cell that says nothing, a verdict map that binds nothing to nothing.
The claims file names `tools/round-46/b.py` too, so `census.py` derives two paths and the
artefact registers one.

## Impacted axes

- **calibration (C2, the claimed axis):** the claim's target is unreachable at its freeze
  (F2) and unreachable at every post-freeze rev (F1); the "met" receipt is the
  `freeze == rev` degenerate case. Even ignoring admissibility, six classes of non-registry
  score green (F3–F9), the cheapest being one row.
- **depth (C1) — shared infrastructure only:** F10 (`restored`) and the malformed-document
  asymmetry (F6) come from `gate.py`, which both counters share; C1's clause 8 uses the
  same receipt field. Not a C1 claim defect; a shared-receipt defect.
- **coverage:** not touched by C2 — correctly, the claims file gives it no claim.

## Smallest safe corrections (for the L1 to decide, not applied)

1. **Pin the freeze.** In `gate.freeze_state`, after `resolve`, require
   `git log --format=%H -1 -- plans/round-46-claims.md` at `rev` (or at the tip) to equal
   `freeze`; otherwise exit 2 `freeze_not_derived`. One subprocess call. This alone kills
   the `freeze == rev` receipt.
2. **Do not edit the frozen instrument after the freeze.** The instrument must be frozen
   with the claim it scores; `0425224` shows why: the fix is right and it voids the claim.
   If the v1 port is wrong, the freeze must be re-cut *before* the artefact exists, which
   means a new round, not a repair commit.
3. **Re-derive the census.** Add a clause: `census.py` at `--rev` must produce exactly the
   committed `census.json` paths; exit 1 naming the difference. Without it the census is an
   author-supplied number and the 38-row obligation is one line of JSON.
4. **Bind the purpose cell.** Require it to carry a description, not just a token: e.g. at
   least 3 alphabetic tokens and at least one character outside `{0,1,2,=,;,x,:}`. Do
   **not** require a `gate`/`probe` prefix — 7 of the honest 38 purposes do not start with
   either (`landed-registry-audit.out`), so a prefix rule would red the intended artefact.
   That is one regex and it kills `| x |`.
5. **Bind the verdict map to meanings.** Require each `[012]` followed by `[=:]` to be
   followed by ≥1 word character, and reject any `[0-9]+\s*[=:]` binding a code outside
   `{0,1,2}` in the same cell. Kills `0=; 1=; 2=` and the garbage suffix.
6. **Run the fence/comment state machine over the whole file**, and refuse to register when
   either marker sits inside a fence or comment. Also exit 2 on an unclosed fence/comment
   inside the section (match C1's malformed-heading precedent).
7. **Refuse escaped pipes:** split on unescaped `|` only, and reject a row whose cell count
   is not the header's.
8. **Presence-check every row's cell-0 path**, not only the census intersection (F9), and
   **reject duplicate rows** for one path (F8).
9. **Expand directories in `blob_changed`** (F10) so `restored` is not the whole `touched`
   list by construction.
10. **Correct the preflight count** in the claims file for the next round: registry prints
    `cases=12`, not 11.

## Receipts

All commands below were run with `TMPDIR=HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r46/R46W1CritC2`
from the lane root; the frozen instrument bytes were extracted with
`git show 3182047…:tools/round-46/<f>` into `$S/frozen/` and are never re-imported from the
working tree. `manifest.tsv` holds `name, exit, stdout sha256, UTC time`.

| receipt | exit | stdout sha256 |
|---|---|---|
| `c2-at-head.out` | 2 | `683ba55ff0aa4fae5a014596f578be94c43fc47cf677d39d7eb2f41fa5f350d5` |
| `c2-at-0425224.out` | 2 | `2f6a9035929498abc996f622eba92b008aedab406be433600b48c5a6a8c5d63b` |
| `c2-freeze-eq-rev.out` | 0 | `d3869553edf79e572238c1aecac68ccbe408c0daa8b28f51b5971d7314539ac1` |
| `frozen-selftest.out` | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` |
| `frozen-attest-selftest.out` | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` |
| `attack-frozen.out` | 0 | `4fad2571873562baf93557d901452d5a5e9154d0b991893073496389a85667b2` |
| `attack-head.out` | 0 | `9f87fbe047ad4c7d68158c44f11af82806835b480aa0a6f9754cef605b34e066` |
| `probe3-frozen-full.out` | 0 | `8aa1f849fb9c48294fd8f1a773524b8f040eb4b92451ff13400c7c4c3cbc115b` |
| `census-derived-HEAD.json` | — | `573ec008fc3f9173da04589c013484485758e9cf1c901a254bf1d6286d62133e` |
| `landed-registry-audit.out` | 0 | `6b73ae131f6152eb641bd80649ed8ed24b6eaea9b25347840a2a4b1b9f4cd88b` |
| `probe-arity.out` | 0 | `c1366c9f443aa30d0576c8294907265cdd1184fb8d865e88ca80c4948bfea188` |
| `attack.py` | — | `9b5fffed97be69ca43c92f0efb7843d77ccbe95244000cb78231b97086b77aa1` |
| `attack2.py` | — | `ba3376e072accb631d9464108901e60f302b5dbb501667b95773bc66403ceb19` |
| `probe3.py` | — | `8d8d42d10373bda87a04f42c2be23a975b28fd6f5954648b9057de3dadca2088` |

Exact commands:

```sh
# admissibility of C2 at the claimed met rev, and at HEAD
python3 -I -B tools/round-46/registry.py --root <lane> \
  --freeze 31820472784284727546808acc31b3ea1e73919b --rev 0425224756791b414454df28a9abf93dcdf154ce --no-battery
python3 -I -B tools/round-46/registry.py --root <lane> \
  --freeze 31820472784284727546808acc31b3ea1e73919b --rev 49e6cac4f6604986b1a7e9cfcbd9d46704dff390 --no-battery
# the degenerate freeze that scores green
python3 -I -B tools/round-46/registry.py --root <lane> \
  --freeze 0425224756791b414454df28a9abf93dcdf154ce --rev 0425224756791b414454df28a9abf93dcdf154ce
# frozen selftests (frozen bytes imported, not the working tree)
python3 -I -B -c "import sys;sys.path.insert(0,'$S/frozen');import registry;sys.exit(registry.selftest())"
python3 -I -B -c "import sys;sys.path.insert(0,'$S/frozen');import importlib.util;spec=importlib.util.spec_from_file_location('af','$S/frozen/attest.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);sys.exit(m.selftest())"
# the attack batteries
python3 -I -B $S/attack.py    # frozen bytes, 17 structural cases
python3 -I -B $S/attack2.py   # HEAD bytes, 8 cases incl. the cheapest artefact
python3 -I -B $S/probe3.py    # frozen full evaluation: honest artefact + ghost-in-census
# census provenance
python3 -I -B tools/round-46/census.py --root <lane> --rev <rev> --out $S/census-derived-<rev>.json
```

## Not run / limits

- `attest.py` was not attacked beyond its selftest count — C1 is another seat's lane. The
  `restored` and malformed-document findings reach it through `gate.py` and are stated as
  shared-infrastructure defects, not as a C1 verdict.
- The lane moved under me during the seat: HEAD was `1e32827b` at first read and
  `49e6cac4` by the decisive run (L1 commits). Every receipt names its `rev`, and the
  `c2-at-0425224`/`c2-at-head` runs are pinned to explicit commits.
- No tool installed; nothing written outside my seat dir and my scratch; scratch removed
  after the receipts were copied.
