# R47-C1 block 24 — rows draft (seat C1Struct)


> **Postscript (measured, 2026-10-28T17:59Z).** Block 24 landed while this draft was being
> written, in a different (also green) text; the landed block was re-measured against clauses
> 1–3 at rev `31b092d1` — `exit 0`, `failing []`, `rule_blocks 24`, header exact, four rows of
> four cells, exits `1/1/1/1` (`report.md` §11). This file stays as the pre-landing draft the
> ticket asked for; the anchors and tripwires below are what a re-landing or a re-freeze must
> still satisfy.

Owner of clauses **1–3** of `plans/round-47-claims.md:70-73`:
marker once + one marked block + last craft block + title `24. `; header exactly
`trigger | v2 hole | v3 arm | exit`; `rows == 4`, every row four cells, every exit cell in
`{0,1,2}`. Every number below was measured at freeze
`5017e1f7299c3a812e87e7950148f54313dd279e` with
`tools/round-47/exact.py` (`sha256 dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`).
The full block below is measured **green** (exit 0, battery 4/4/0/1/0) on a one-commit
fixture that preserves the other 23 craft blocks — see `receipts/drive.out`
`candidate-B-full`.

## 1. Insert anchor

Insert as the **last bullet block** of `## Queue-drain craft (rounds 5-12, distilled in
round 13)`: after `SKILL.md:631` (block 23's `Refs:` line at the freeze) and immediately
before `SKILL.md:632` (`## Config custody for live-probe rounds (SOP)`).
At the freeze the section holds 23 blocks (`rule_blocks 23`); the landing must read
`rule_blocks 24`.

## 2. Pins — computed here, not copied from prose

| pin | value | command that produced it |
|---|---|---|
| `interpreter_sha256` | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5017e1f7:tools/round-47/exact.py \| sha256sum` |
| `mutations_sha256` | `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` | `printf 'substring-arm\nduplicate-routed-id\nstale-mutations-digest\nflag-order-drift' \| sha256sum` |

`mutations_sha256` is sha256 over `"\n".join(name for name, _ in MUTATIONS)` with **no
trailing newline** (`tools/round-47/exact.py:92-96`); a trailing newline pins a different
digest and fails clause 6.

## 3. The block — paste as one bullet

File: `candidates/block24-candidate-b.md`, `sha256 b44ef164766ead9817b9ea57e902ec645bd6a9dbb9f2f4ecf72c3b8cc7c1a152`,
10 lines. Inserted into the freeze `SKILL.md` the result is
`candidates/SKILL-with-block24-candidate-b.md`,
`sha256 2819c0e8ad1f491bc6feb22d4c39ef3171683a31a7bb5a87d5cb9d3bcd7a12b9` (1748 lines).

```text
- **24. An exact binding is an equality over one token, one id, one digest and one flag order.** <!-- exactness-table v3 --> The round-46 non-author spot-check routed four instrument defects (R46-CL2, R46-CL3, R46-CL4, R46-CL6); each row states the loose binding that let the defect through, the exact arm that now fails it, and the exit the counter returns when the arm fires. Interpreter `tools/round-47/exact.py` `interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`; the mutation list is pinned by `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` over substring-arm, duplicate-routed-id, stale-mutations-digest, flag-order-drift in that order, so deleting a mutation changes the printed digest. All four forged fixtures exit 1 under v3 and 0 under the ported v2 profile, so the arms are measured, not asserted.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` | the arm-vocabulary check is a lowercased substring test, so any word carrying the token passes | symbol | 1 |
| R46-CL3 a row claims a routed id it does not address | every id need only appear in some row, never exactly once | once | 1 |
| R46-CL4 a deleted mutation changes the denominator | the list is counted but never pinned, so a deletion fails no clause | digest | 1 |
| R46-CL6 one argument reorder blinds the merge arm | `git log --diff-merges=first-parent -m` prints a merge twice, and nothing reads the order | order | 1 |

  Refs: `corpus/lessons/round-46.md:57-59` (R46-CL2, the substring arm), `corpus/lessons/round-46.md:60-62` (R46-CL3, the at-least-once id), `corpus/lessons/round-46.md:63-64` (R46-CL4, the unpinned list), `corpus/lessons/round-46.md:65-70` (R46-CL6, the order-sensitive arm), `corpus/lessons/round-46.md:21` (M46-2, why the list needs a digest), `plans/round-47-claims.md:68-90` (the predicate these rows are scored by).
```

## 4. The rows clause 3 governs

| # | trigger cell | v3 arm cell (exact) | exit cell | measured v3 exit of that forgery |
|---|---|---|---|---|
| 1 | `R46-CL2 blobberish satisfies blob` | `symbol` | `1` | 1 (`battery.fixtures[substring-arm].v3_exit`) |
| 2 | `R46-CL3 a row claims a routed id it does not address` | `once` | `1` | 1 (`…[duplicate-routed-id].v3_exit`) |
| 3 | `R46-CL4 a deleted mutation changes the denominator` | `digest` | `1` | 1 (`…[stale-mutations-digest].v3_exit`) |
| 4 | `R46-CL6 one argument reorder blinds the merge arm` | `order` | `1` | 1 (`…[flag-order-drift].v3_exit`) |

Exit cells are measured, not asserted: each forged fixture returns v3 exit 1 (violation) and
v2 exit 0 (hole), from `receipts/drive.out` `candidate-B-full`. `exit` cells are checked as
`r[3].strip("` ")` in `{"0","1","2"}` (`tools/round-47/exact.py:213-215`), so a bare digit or
a backticked digit both pass; `1.`, `01` and `3` do not.

## 5. Citations — selectors actually resolved at the freeze

| selector | states | resolves at the freeze |
|---|---|---|
| `corpus/lessons/round-46.md:57-59` | R46-CL2 substring arm | yes (file is 102 lines) |
| `corpus/lessons/round-46.md:60-62` | R46-CL3 at-least-once id | yes |
| `corpus/lessons/round-46.md:63-64` | R46-CL4 unpinned list | yes |
| `corpus/lessons/round-46.md:65-70` | R46-CL6 order-sensitive arm | yes |
| `corpus/lessons/round-46.md:21` | M46-2, why the list needs a digest | yes |
| `plans/round-47-claims.md:68-90` | the predicate, clauses 1–9 | yes (file is 190 lines) |
| `tools/round-47/exact.py` (bare, no selector) | the interpreter, identified by its sha pin | exempt by the counter's own `SELF` rule (`tools/round-47/exact.py:150`) |

`corpus/lessons/round-46.md` is cited (clause 8's mandatory citation) and every path token in
the block is inside the validated set. **Do not name `tools/round-46/gate.py` anywhere in the
block** — clause 7 is about that file, but the allowlist is `tools/round-47/` only, so the
path string turns clause 8 red (measured: `receipts/drive2.out`
`probe-cite-gate46-honest-flag-citation`, `["unresolved or unvalidated citations: 1"]`,
`unresolved_citations ["tools/round-46/gate.py: outside the validated path set"]`). Cite
`plans/round-47-claims.md:80-82` for the flag order instead, or say "the round-46 gate".

## 6. Landing tripwires for these three clauses (each measured red)

| tripwire | measured failure |
|---|---|
| the marker string appears anywhere else in `SKILL.md` (even quoted in prose or a fence) | `marker_occurrences 2 != 1` |
| the marker sits in the craft section but outside a `- **` bullet | `marker_block_count 0 != 1` |
| another block is appended after block 24 in the craft section | `marker block is not the last craft block` |
| title `24.` without the trailing space | `marker block title does not start with '24. '` |
| a fifth header cell | `header [... 'note'] != ['trigger','v2 hole','v3 arm','exit']` |
| a pipe character inside a cell (e.g. a regex alternation) | `a row does not have exactly 4 cells` |
| a second table inside the block | `rows 6 != 4` |
| an exit cell of `3` | `exit cells outside {0,1,2}: 1` |
