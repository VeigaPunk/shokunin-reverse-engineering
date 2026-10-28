# RevC1Last — C1 clause 1 attack: `block_is_last` and the `24. ` title

Seat `RevC1Last`, round 47, wave 1. Read-only on the lane tree; every fixture is a
throwaway repo under `/fast/scratch/hyaku/kaidoku-r47/RevC1Last`. Nothing in `SKILL.md`,
`plans/`, `tools/`, `SCORECARD.md` or the fleet repo was written.

| item | value |
|---|---|
| lane | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| freeze named in the assignment | `5017e1f7299c3a812e87e7950148f54313dd279e` |
| measured rev for every case | `62e33f7dd75c8e3285967b26419842c106f6c965` (HEAD when the seat started; it moved to `1e2c3102` mid-seat — see F5) |
| frozen counter | `tools/round-47/exact.py`, byte-identical since `5017e1f7` (`git log -1 -- tools/round-47/exact.py`) |
| landed block under test | `SKILL.md:632` at `62e33f7d`, `- **24. An instrument's binding is an equality…**` + `<!-- exactness-table v3 -->` |
| reproducer | `.ufo/waves/round-47/w1/RevC1Last/revc1last-attack.py` (29 cases) |
| case receipt | `.ufo/waves/round-47/w1/RevC1Last/cases-all.json`, sha256 `e169261f23ea14cba297b4307128d2c524822f1579a686effb163e625a97eae7` (run stdout `cases-all.out`, sha256 `ccfe34d2bb5f613ed1708da8ea3691453d3be4f6fa3c7c6b2adb827075f0786e`) |
| reproducer sha256 | `1aa0a22f014e59f8706054a013d0a9369c747bd790473275b95366ecbb1a0540` |

Each case is a two-commit fixture repo (`c0` = base with block 24 as landed, `c1` = the
attacked `SKILL.md`; the frozen paths are byte-identical in both commits so the freeze arm
is clean), built by the reproducer with `mktemp -d -p "$S"`, `git -C "$D" init -q`, and
`git -C "$D" rev-parse --show-toplevel` asserted equal to `$D` before the first commit. The
counter is then run **as a CLI** against that repo:

```sh
S=/fast/scratch/hyaku/kaidoku-r47/RevC1Last
TMPDIR=$S HYAKU_SCRATCH=$S S=$S python3 -B \
  .ufo/waves/round-47/w1/RevC1Last/revc1last-attack.py --case <CASE>
```

which issues, per case,

```sh
python3 -I -B tools/round-47/exact.py --root <fixture> --freeze <c0> --rev <c1> --no-battery
```

## Verdict

Clause 1 (`exact.py:191`, enforced at `:194-197`) is a statement about a **fence-unaware
line splitter** (`craft_section` `:101-108` splits on the first `\n## `; `blocks_of`
`:109-110` splits on `^- \*\*` at column 0), not about `SKILL.md`. **Ten** documents that
violate the claim's own sentences return **exit 0** (F1 one, F2 three, F3 five, F8 one), and
**six** legitimate documents return **exit 1** (F6 two, F7 one, F8 three); `fence-table`
adds an eleventh exit-0 outside this seat's clause. The single missing assertion that closes
most of it is `rule_blocks == 24`:
`rule_blocks` is computed into the receipt at `:175` and compared with nothing.

`block_present == 1` therefore means "one `- **`-prefixed line contains the marker", not
"rule block 24 exists in the rendered document". `blocks[-1] is block` is correct *given a
correct parse* (the split allocates distinct strings; `dup25-after-nomarker` reports
`block_is_last: false`), so the identity comparison is not itself the hole — the parse is.

## Genuine control (clause 1 met on the real bytes)

| run | command | exit | stdout sha256 | verdict |
|---|---|---|---|---|
| control A | `exact.py --root . --freeze 1e2c3102 --rev 1e2c3102` | **0** | `98ef390e1c1a3eaa1e0d2b9f3a9c635a4870c257b2cdebad4c4a87497616ea6d` (`freeze-eq-rev-HEAD.out`) | `block_is_last true`, `rule_blocks 24`, `marker_occurrences 1`, `refs 8`, `failing []`, battery `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0` |
| control B | `exact.py --root . --freeze 5017e1f7 --rev 1e2c3102` | **2** | `706cf11c4b17acb95c78afc1ac690addc3de81a0d479685ba4f11cd66625790f` | `frozen_path_changed` — see **F5** |

So the landed block does meet clause 1 at `62e33f7d`/`1e2c3102`; the findings below are
about what the clause *cannot* distinguish, not about the landing's current bytes.

## Findings

### F1 — HIGH (forgery): a fenced `## ` line after block 24 hides a real block 25

`craft_section` ends the craft section at the first `\n## ` with no fence awareness
(`exact.py:101-108`). A documentation fence that contains a `## ` line therefore truncates
the section; any `- **` block after it is outside the counter's world.

* fixture: reproducer case `fence-hides-25` (`SKILL.md` gains, immediately after block 24,
  a ```md fence holding `## Worked example`, then a real block
  `- **25. A visibly landed extra rule block.**`)
* command: `… revc1last-attack.py --case fence-hides-25`
* **exit 0**, `block_is_last true`, `rule_blocks 24`, `failing []`
* `SKILL.md` renders a 25th craft rule block after 24; the claim says 24 is the last one.
* what the claim would have to say: *"the craft section is delimited at fence parity zero,
  and no `- **` line follows the marked block before the next `## ` heading at fence parity
  zero."*

### F2 — HIGH (forgery): the landing can live entirely inside a fenced code block

Two shapes, both `exit 0`:

| case | shape | exit | `rule_blocks` |
|---|---|---|---|
| `fenced-whole-block` | a ```md fence opened in block 23's tail, closed after block 24 — block 24 is literal code text | **0** | 24 |
| `unclosed-fence-whole-block` | the same fence, never closed | **0** | 24 |
| `whole-landing-in-fence-early` | block 24 moved **wholesale** into a ```md fence at the top of the file, before the real craft heading; the real craft section keeps **23** blocks | **0** | **1** |

`whole-landing-in-fence-early` is the complete break: the counter's entire verdict — clauses
1 through 9, including the two sha256 pins — is about a code fence at the top of the file,
and `## Queue-drain craft` has no block 24 at all. `fence-table` (adjacent, clause 2) is the
same root: wrapping the matrix in ```` ```text ```` gives **exit 0** with the matrix not a
rendered table.

* command: `… --case whole-landing-in-fence-early`
* **exit 0**, `block_is_last true`, `rule_blocks 1`, `marker_occurrences 1`, `failing []`
* what the claim would have to say: *"the marked block's first line is at fence parity
  zero — it is not inside an open fenced code block — and its table is a rendered table,
  not fenced text."*

### F3 — HIGH (forgery): `rule_blocks` is reported and never bound

The claim's landed-surface sentence says **"One new rule block"**
(`plans/round-47-claims.md:75`), but no clause compares `rule_blocks` with 24 (`:175`
computes it; `:194-197` never reads it). Consequences, all **exit 0**:

| case | document | exit | `rule_blocks` |
|---|---|---|---|
| `dup25-before` | a second copy of block 24's matrix labelled `25. `, inserted **before** block 24 | **0** | 25 |
| `dup8-before` | the same copy labelled `8. ` | **0** | 25 |
| `continuation-25` | a real `- **25. …**` under `## Queue-drain craft (continued)` after 24 | **0** | 24 |
| `continuation-dup` | block 24's own matrix as `25. ` under that heading | **0** | 24 |
| `eof-25` | a `25.` rule block appended at end of file | **0** | 24 |

The claim says "the block being the **last** craft block" (`:91`), which a duplicate placed
*before* it satisfies literally. The counter reports the second copy as part of the count
and does not care.

* command: `… --case dup25-before` (and the other four)
* **exit 0**, `block_is_last true`, `rule_blocks 25` / 24
* what the claim would have to say: *"`rule_blocks == 24`, and the four ids are named by
  four distinct blocks, so no fifth block can carry a copy of the matrix."*

Note this one assertion also closes F1's `rule_blocks 24` shrug? No — F1 reports 24 because
the 25th block is out of scope; `rule_blocks == 24` alone does **not** catch F1 or
`whole-landing-in-fence-early`'s sibling (`rule_blocks 1` it does catch). Fence-aware
parsing is required for F1/F2 regardless of the count.

### F4 — MEDIUM: the title clause binds a prefix, not a title

`block.startswith("24. ")` (`:196`) accepts a block whose title is exactly `24. ` with no
title text:

* case `title-empty` (`- **24. ** <!-- exactness-table v3 --> …`): **exit 0**,
  `block_title "24. "`.
* what the claim would have to say: *"the title is `24. ` followed by a non-empty
  sentence"* — otherwise "An instrument's binding…" is not required by any clause.

### F5 — HIGH (landing blocker, both counters): the freeze clause forbids the round's own amendments

`freeze_state` (`tools/round-46/gate.py:144-196`) unions the frozen set derived at both ends
and exits 2 if *any* frozen path was touched in `freeze..rev`. After the freeze the round
amended frozen paths four times:

```
5017e1f7  freeze
9018c53b  A1  M plans/round-47-claims.md  M tools/round-47/record.py
62e33f7d  A2  M plans/round-47-claims.md  M tools/round-47/record.py
2e4ae434  A3  M tools/round-47/record.py
1e2c3102  A4  M tools/round-47/record.py
```

Measured at rev `1e2c3102`:

| freeze | exit | stdout sha256 | reason |
|---|---|---|---|
| `5017e1f7` (the assignment's freeze) | **2** | `706cf11c4b17acab95c78afc1ac690addc3de81a0d479685ba4f11cd66625790f` → see file | `frozen_path_changed` `['plans/round-47-claims.md','tools/round-47/','tools/round-47/record.py']` |
| `62e33f7d` (the claims file's own derivation `git log -1 -- plans/round-47-claims.md`) | **2** | `98a15294e14bb03410a39fde64c0af80c1bc08e68a3bc19904f718d5e6e1dd01` | `frozen_path_changed` `['tools/round-47/','tools/round-47/record.py']` |
| `1e2c3102` == rev | **0** | `98ef390e1c1a3eaa1e0d2b9f3a9c635a4870c257b2cdebad4c4a87497616ea6d` | clean |

(exact stdout sha256 for the first row: `706cf11c4b17acb95c78afc1ac690addc3de81a0d479685ba4f11cd66625790f`,
captured in `.ufo/waves/round-47/w1/RevC1Last/freeze-5017e1f7@rev-HEAD.out`.)

Consequences the L1 must reconcile before landing evidence is cited:

1. **Only `freeze == rev` scores.** Anything else is exit 2 `frozen_path_changed`, for both
   counters, for the rest of the round. Each new amendment (A5…) needs a new freeze, and
   each new freeze invalidates the previous controls.
2. **The before-state and the after-state are measured on different frozen bytes.** Both C1
   controls (`controls/ctl-c1-0-do-nothing.json`, `ctl-c1-2-freeze-battery-absent.json`) were
   produced at `freeze == rev == 5017e1f7`; the landing can only be measured at
   `freeze == rev == <landing>`. The "do-nothing control cannot reach the target" argument
   holds, but its instrument revision is not the landing's.
3. Good news for C1 specifically: `tools/round-47/exact.py` is byte-identical since
   `5017e1f7`, so F1–F4/F6–F9 are stable properties of the frozen counter, not of `record.py`.
4. what the claim would have to say: *"the freeze is re-derived as the last commit touching
   the frozen paths, the scoring configuration is `freeze == rev`, and the controls are
   re-derived at that pair"* — or in-round amendments to frozen paths must be forbidden and
   the freeze re-declared before wave 1 closes.

### F6 — MEDIUM (false rejection): a trailing comment makes the landing unscoreable

A comment-only `- **` line after block 24 is parsed as a new block and breaks clause 1:

* case `comment-after` (`- **<!-- craft section ends here; block 24 is the last rule -->**`):
  **exit 1**, `block_is_last false`, `rule_blocks 25`,
  `failing ["marker block is not the last craft block"]`
* case `bare-dash-after` (a bare `- **` line): **exit 1**, same failing

The symmetric case is worse news for the claim: `comment-before` — the *same* comment-only
line placed before block 24 — is **exit 0** with `rule_blocks 25`, i.e. it is silently
counted as a rule block. The grammar is positional, not semantic.

* what the claim would have to say: *"a `- **` line whose body is solely an HTML comment
  does not start a block."*

### F7 — MEDIUM (false rejection): a fenced example inside block 24 splits the block

* case `fence-inside-block`: a ```text fence inside block 24's own body whose first line is
  `- **24. an example of the table format**` → **exit 1**, `block_is_last false`,
  `rule_blocks 25`, `failing ["marker block is not the last craft block"]`

Rule 24 cannot document a `- **` sample without going red. Same root as F1/F2.

### F8 — LOW (diagnostics): with two markers the counter scores the first one

`block = marked[0]` (`:186-190`) rather than the last, and `marker_occurrences` is a raw
substring count over the whole file (`:179-183`). So:

* `marker-prose-early` — an early block's prose naming `` `<!-- exactness-table v3 -->` `` in
  backticks → **exit 1**, `marker_occurrences 2` (claim-conformant, but it means `SKILL.md`
  may never quote its own marker);
* `marker-fenced-early` — a fenced example quoting the marker → **exit 1**,
  `marker_occurrences 2`;
* `section-in-fence-early` — a fenced excerpt of the `## Queue-drain craft ` heading at the
  top of the file → the *first* heading wins, the real section is out of scope,
  `rule_blocks 1`, `marker_occurrences 2` → **exit 1**. The same top-of-file fence placement
  gives **exit 0** in `whole-landing-in-fence-early` (F2), because there the fenced content
  is the genuine block 24; here it is a one-row sample. The verdict follows the fenced
  content, never the rendered structure.
* `block = marked[0]` (`:186-190`) scores the **first** marker-bearing block of the section,
  not the landing block: in `section-in-fence-early` the fenced excerpt's one-row block is
  what gets scored (`rows 1 != 4`, `routed cardinality {'R46-CL2': 1}`) while the real block
  24 is unreachable. In `marker-fenced-early` the marker at the top of the file is outside
  the craft section, so only `marker_occurrences 2 != 1` fires. Diagnosis is therefore a
  function of fence placement, not of what the document says.

### F9 — the clauses that hold (calibration evidence, not defects)

| case | expectation | exit | evidence |
|---|---|---|---|
| `title-nospace` `- **24.An exact…` | reject | **1** | `title does not start with '24. '` |
| `title-dot-only` `- **24.** …` | reject | **1** | same |
| `title-double-space` `- **  24. …` (two spaces after the dash; not a block at all) | reject | **1** | same |
| `title-nbsp` `24.<NBSP>` | reject | **1** | byte-strict prefix — good |
| `title-tab` `24.<TAB>` | reject | **1** | same |
| `dup25-after-nomarker` / `dup25-after-marker` | reject | **1** | `block_is_last false`; the marker copy also trips `marker_occurrences 2` |
| `indent25-after` (`  - **25.` two-space indented) | reject | **1** | not via the block grammar: the indented table merges and `rows 9 != 4`. An indented rule block is invisible as a block and fails for an unrelated reason |
| `block23-relabelled` (the kill rule's own case, `plans/round-47-claims.md` "Kill rule") | reject | **1** | `header ['trigger','v1 hole','v2 arm','exit']`, `rows 13 != 4`, routed cardinality `{}` |
| `comment-inside-indented` (indented comment inside block 24) | accept | **0** | control |
| `genuine` | accept | **0** | control |

## The 29-case matrix (verbatim from `cases-all.json`, sha256 `e169261f…`)

| case | document | exit | `block_is_last` | `rule_blocks` | `marker_occurrences` |
|---|---|---|---|---|---|
| `genuine` | landed SKILL.md unchanged | 0 | True | 24 | 1 |
| `title-nospace` | `- **24.An exact...` — no space after the number | 1 | True | 24 | 1 |
| `title-double-space` | `- **  24. An exact...` — two spaces after the dash | 1 | True | 24 | 1 |
| `title-nbsp` | `- **24.<NBSP>An exact...` | 1 | True | 24 | 1 |
| `title-tab` | `- **24.<TAB>An exact...` | 1 | True | 24 | 1 |
| `title-dot-only` | `- **24.** An exact...` | 1 | True | 24 | 1 |
| `title-empty` | title is exactly `24. ` with no title text | **0** | True | 24 | 1 |
| `comment-after` | block 24 followed by a comment-only `- **` line | **1** | False | 25 | 1 |
| `bare-dash-after` | block 24 followed by a bare `- **` line | **1** | False | 25 | 1 |
| `comment-before` | a comment-only `- **` line immediately BEFORE 24 | 0 | True | 25 | 1 |
| `comment-inside-indented` | an indented HTML comment inside block 24 | 0 | True | 24 | 1 |
| `dup25-after-nomarker` | a 25. block carrying 24's text, marker stripped, after 24 | 1 | False | 25 | 1 |
| `dup25-after-marker` | same, marker kept | 1 | False | 25 | 2 |
| `dup25-before` | a 25. block carrying 24's text, BEFORE 24 | **0** | True | 25 | 1 |
| `dup8-before` | the same copy numbered 8, before 24 | **0** | True | 25 | 1 |
| `indent25-after` | a 25. copy indented two spaces, after 24 | 1 | True | 24 | 1 |
| `fence-inside-block` | a fenced `- **24. ...**` example inside block 24 | **1** | False | 25 | 1 |
| `fence-hides-25` | fenced `## ` line after 24; a real 25 follows | **0** | True | 24 | 1 |
| `continuation-25` | a real 25. under `## Queue-drain craft (continued)` | **0** | True | 24 | 1 |
| `continuation-dup` | 24's own text as 25. under that heading | **0** | True | 24 | 1 |
| `eof-25` | a 25. block appended at end of file | **0** | True | 24 | 1 |
| `fence-table` | the matrix wrapped in ```` ```text ```` | **0** | True | 24 | 1 |
| `fenced-whole-block` | block 24 inside a fence opened in 23's tail | **0** | True | 24 | 1 |
| `unclosed-fence-whole-block` | same, fence never closed | **0** | True | 24 | 1 |
| `whole-landing-in-fence-early` | block 24 moved into a fence at the top; real section has 23 blocks | **0** | True | **1** | 1 |
| `section-in-fence-early` | fenced excerpt of the heading + merged 24. at the top | **1** | True | 1 | 2 |
| `marker-fenced-early` | fenced example quoting the marker line | 1 | True | 24 | 2 |
| `marker-prose-early` | an early block naming the marker in backticks | 1 | True | 24 | 2 |
| `block23-relabelled` | block 23's text relabelled `24. ` + marker | 1 | True | 24 | 1 |

Bold exit 0 in a row whose document violates the claim = forgery; bold exit 1 in a row whose
document is legitimate = false rejection.

## What clause 1 would have to say (drop-in replacement, for the L1 to reconcile)

> `marker_occurrences == 1`; `rule_blocks == 24`; the marked block is the last block of the
> craft section and no `- **` line follows it anywhere in `SKILL.md`; its title is `24. `
> followed by at least one sentence; the craft section is the first `## Queue-drain craft `
> heading **at fence parity zero**, and a `## ` or `- **` line inside an open fenced code
> block neither ends the section nor starts a block; a `- **` line whose body is solely an
> HTML comment is not a block; the marked block's first line is at fence parity zero and its
> table is a rendered table, not fenced text.

Every clause above is decidable from the same bytes the counter already reads; none requires
a new input. `rule_blocks == 24` alone closes `dup25-before`, `dup8-before`, `comment-before`
and `whole-landing-in-fence-early` (1 ≠ 24); the fence-parity rule closes `fence-hides-25`,
`fenced-whole-block`, `unclosed-fence-whole-block`, `section-in-fence-early` and
`fence-inside-block`.

**This is a recommendation only.** `tools/round-47/exact.py` and
`plans/round-47-claims.md` are byte-frozen; I did not edit them. A counter that implements
the above is a new freeze (see F5) and a new round's claim.

## Residual risk and verification gaps

* Not run: the C2 counter (`record.py`) — outside this seat. Not run: the frozen counter's
  own `--selftest` (it builds its own fixtures; it is the L1's check, and it does not cover
  any of the classes above).
* The battery in clause 9 scores exactly four forgeries, none of them a block-grammar case,
  so `v3_green 0` says nothing about F1–F4/F6–F8. Closing them needs new mutation classes
  (`duplicate-block`, `fenced-section`, `comment-line`) — a new freeze, not an edit.
* F5's churn is live: `record.py` changed again between my first and last measurement
  (`62e33f7d` → `2e4ae434` → `1e2c3102`). Any freeze cited in the landing report must be
  re-derived at citation time, not copied from this report.
* The fixtures are deleted after each run by design; the reproducer rebuilds them
  deterministically from `62e33f7d`'s bytes. The one hard-coded input is `REV` in the
  reproducer — re-point it if the counter is ever re-frozen.
* Not tested: Windows/CRLF line endings, a `- **` block inside a blockquote, and a
  craft section whose heading carries a trailing-space variant (`## Queue-drain craft` with
  no trailing space raises `Malformed` → exit 2, per the selftest's own case).

## Tooling

No installs. `python3 3.14.8`, `git`. Scratch root `/fast/scratch/hyaku/kaidoku-r47/RevC1Last`
(`TMPDIR`/`HYAKU_SCRATCH` exported for every run); removed after the receipts were copied here.
