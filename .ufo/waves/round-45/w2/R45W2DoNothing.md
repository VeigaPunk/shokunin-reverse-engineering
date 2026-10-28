# R45W2DoNothing — the round-45 kill rule under a do-nothing landing

Seat `R45W2DoNothing`, lane `kaidoku-shokunin`, round 45 wave 2 (adversarial falsification).
Read-only on the lane and the fleet repo; all writes under
`.ufo/waves/round-45/w2/R45W2DoNothing/` and `/fast/scratch/hyaku/kaidoku-r45/R45W2DoNothing`
(scratch removed after receipts were copied here). No installs, no mutating git, no
`agent://all`. Lane HEAD observed `a63d109faa050207d4c184471889049741c9ebbf`.

Ground truth used: `plans/round-45-claims.md` (the rule), freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`,
A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`.

Freeze re-derivation (read-only git, both paths agree):

```
$ git -C kaidoku-shokunin log --format=%H -1 -- plans/round-45-claims.md
f762b7273e3f6ca3c710bb37d5de92a4a4417aec
$ git -C kaidoku-shokunin log --format=%H -1 -- tools/round-45/
f762b7273e3f6ca3c710bb37d5de92a4a4417aec
$ git -C kaidoku-shokunin diff --stat f762b72 a63d109 -- tools/round-45/ plans/round-45-claims.md
(empty: frozen paths untouched through HEAD)
```

---

## Verdict table

| # | Attack (what it attacks) | Input | Exit | Verdict |
|---|---|---|---|---|
| A1 | R45-C1 do-nothing control (`ctl-c1-0-do-nothing.json`) | `--freeze f762b72 --rev f762b72` on the lane | **1** | **holds** (0/15 field diffs) |
| A2 | R45-C2 do-nothing control (`ctl-c2-0-do-nothing.json`) | `--freeze f762b72 --rev f762b72` on the lane | **1** | **holds** (0/12 field diffs) |
| A3 | R45-C1 kill rule: relabelled round-42 triage table as block 22 (21 plain + 1) | fixture SKILL.md + frozen interpreter | **0** (`met_target: true`) | **falsified** |
| A4 | R45-C1 predicate discrimination: 8 pure-filler rows | fixture SKILL.md + frozen interpreter | **0** (`met_target: true`) | **falsified** (strongest) |
| A5 | R45-C1 "block 22": marker block placed first, ordinal `1.` | fixture SKILL.md | **0** (`met_target: true`) | **falsified** |
| A6 | R45-C1 selftest case `red-relabelled-21-block` (does it test relabelling?) | 20 plain vs 21 plain, same relabel | **1 / 0** | **falsified** (the case tests the count, not the relabel) |
| A7 | R45-C2 kill rule: six rows naming tools that do not exist | fixture SKILL.md | **1** | **holds** |
| A8 | R45-C2 calibration content: six vacuous rows with correct paths | fixture SKILL.md | **0** (`met_target: true`) | predicate **holds as written**; content claim unenforced (strength limit) |

Exit codes are semantic: 0 met, 1 not met, 2 could-not-evaluate. Every run below used the
bytes at `f762b72` for the counters and for the interpreter copied into the fixtures.
No run was skipped; nothing is reconstructed from memory.

---

## A1 — R45-C1 do-nothing control: holds

```
$ python3 -I -B tools/round-45/c1-counter.py \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec \
    --rev    f762b7273e3f6ca3c710bb37d5de92a4a4417aec \
    --json-out .../controls/c1-do-nothing.json
exit 1   UTC 2026-10-28T15:59:48Z
stdout sha256 e2731609959b489750a703fc12a5605ad4538395c5f808424e142dfff41fb4e1
```

Field-by-field against `.ufo/waves/round-45/controls/ctl-c1-0-do-nothing.json`:
**15 keys, 0 differences** (`counter, freeze, rev, rule_blocks 21, block22_present 0,
block22_rows 0, block22_refs 0, block22_unresolved_citations [], block22_cites {S140:false,
interpreter:false}, block22_header_ok false, preflight_selftest {ok:false, skipped:true},
interpreter_present true, frozen_path_changed [], met_target false, failing`).

The exact clauses that stopped it (all five, verbatim from `failing`):

1. `rule_blocks 21 != 22`
2. `block22_present 0 != 1`
3. `block22_rows 0 < 8`
4. `block22 table header lacks trigger/arm/exit/receipt`
5. `block22_refs 0 < 4`

Note what did **not** stop it: `interpreter_present` is **true** at the freeze, i.e. the
frozen interpreter already exists and already passes its own selftest (see §Cross-cutting).
The control is red on SKILL.md shape only.

## A2 — R45-C2 do-nothing control: holds

```
$ python3 -I -B tools/round-45/c2-counter.py --root <lane> \
    --freeze f762b727... --rev f762b727... --json-out .../controls/c2-do-nothing.json
exit 1   UTC 2026-10-28T15:59:48Z
stdout sha256 d6e202aac80ee78d9a6fbd1113ea5b62fb51b27503faccb38dec8afdb9216dd0
```

Against `ctl-c2-0-do-nothing.json`: **12 keys, 0 differences** (`registry_rows 39,
scope_size 6, scope` = the six paths, `registered []`, `thin []`, `met_target false`).
The single stopping clause:

```
unregistered: ['tools/round-44/c1-counter.py', 'tools/round-44/c1-run.sh',
 'tools/round-44/c2-counter.py', 'tools/round-45/frozen-path-preflight.py',
 'tools/round-45/c1-counter.py', 'tools/round-45/c2-counter.py']
```

i.e. `by_tool.get(path)` misses for all six (`tools/round-45/c2-counter.py:101`).

---

## A3 — relabelled triage table as block 22: **falsified**

Attack on: the R45-C1 kill rule and the implied reading of `failing == []` ("the depth
work was done").

Fixture `c1-relabelled-h2l2pvpe` (rev `556ed9e3…`), built in scratch with
`git init` + `git rev-parse --show-toplevel` asserted equal, containing exactly the frozen
interpreter bytes and a SKILL.md whose `## Queue-drain craft` section has **21 plain
`- **n. …` blocks plus one block**:

```
- **22. Freeze integrity.** <!-- freeze-integrity-table v1 --> S140 tools/round-45/frozen-path-preflight.py

  | trigger | arm | exit | receipt |
  | --- | --- | --- | --- |
  | container-depth-limited | triage | 0 | receipt-0 |
  | … 7 more, first cells copied verbatim from the real `sqfs-triage-table v4` block … |

  Refs: corpus/lessons/round-44.md:1, corpus/lessons/round-44-verifier-spotcheck.md:1,
        corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:1, plans/round-45-claims.md:1
```

Every row is SquashFS triage text (`container-depth-limited`, …) with the arm column set
to the literal `triage` and receipts `receipt-N`; nothing in the block concerns a freeze.
It is the round-42 triage table relabelled, not a freeze-integrity decision list.

Result (command and receipt in `receipts/c1-relabelled-triage.*`):

```
exit 0   UTC 2026-10-28T16:01:03Z
stdout sha256 a8d346f9f5d60076d81681ee80c92519e332523cf507753a712c4eb6713aa8f2
{"block22_cites": {"S140": true, "interpreter": true}, "block22_header_ok": true,
 "block22_present": 1, "block22_refs": 4, "block22_rows": 8,
 "block22_unresolved_citations": [], "failing": [], "met_target": true,
 "preflight_selftest": {"cases": 11, "exit": 0, "failures": 0, "ok": true},
 "rule_blocks": 22}
```

**Differing value.** `met_target` is `true` (exit 0) where the kill rule's purpose requires
`false` (exit 1) for a relabelled block. The kill rule as written — "a relabelled block that
keeps the 21-block **count** still scores 1" — is literally true and is the problem: the
count is doing all the work. Add one plain block and the relabelled table scores.

**Fix (minimal).** (a) Require the marked block to be anchored: either the last block in
`## Queue-drain craft` or a block whose leading ordinal equals `rule_blocks`. (b) Make the
`arm` cell a member of the interpreter's own arm vocabulary (`commit`, `restored`, `blob`,
`dirty`, `pathspec`, `revision guard`) — `triage` would then be red. (c) Add selftest case
`red-relabelled-22-block` (21 plain + this block, expect 1). The landed block is already
last and already labelled `22.`, so (a) costs the landing nothing.

## A4 — eight pure-filler rows: **falsified** (strongest skip)

Attack on: the R45-C1 predicate's ability to distinguish work from shape.

Fixture `c1-filler-w39xdaul` (rev `ccd9e4af…`). Same 21 plain blocks; block 22's table is:

```
| trigger | arm | exit | receipt |
| --- | --- | --- | --- |
| filler-0 | filler | 0 | filler |
| filler-1 | filler | 1 | filler |
| … through filler-7 | filler | 2 | filler |
```

plus the marker, the literal `S140`, the interpreter path, and four citations to unrelated
real files at `:1`.

```
exit 0   UTC 2026-10-28T16:01:03Z
stdout sha256 0aae1564a7e4afa1c0a515ef58dc0568ac0145ff3ebeb5571b0b43f4335a4a74
failing []   met_target true   rule_blocks 22   block22_rows 8   block22_refs 4
```

**Why this is not a technicality.** The counter's own green fixture is
`GOOD_ROW * 8` — eight *identical* rows (`tools/round-45/c1-counter.py:208,212`). "Green"
in the instrument's own selftest already means "eight rows with a `0/1/2` in column 3";
none of its nine cases feeds a semantically wrong table with the right shape. The predicate
therefore measures a table's **shape**, not the decision list the claim says it carries
(`plans/round-45-claims.md` §R45-C1 "Landed surface", §Kill rule).

Two secondary clauses are also shape-only, evidenced by the same receipt:
- `block22_refs >= 4` (`c1-counter.py:175`) counts any `plans/…md` / `corpus/lessons|knowledge/…md`
  with an in-range line; four unrelated files at `:1` satisfy it (`c1-counter.py:78-91`
  resolves existence and line range only).
- `cites S140` and `cites interpreter` are substring checks on the whole block
  (`c1-counter.py:149-150`); naming them in a sentence suffices.

**Fix.** As A3(b)+(c), and add `red-filler-rows` (this fixture) expecting 1. A vocabulary
check on the `arm` column rejects `filler` and `triage` in one clause; requiring each
`trigger` cell to contain a frozen-path token (`FREEZE`, `REV`, `worktree`, `pathspec`,
`commit`) rejects `filler-N`.

## A5 — marker block at the top: **falsified**

Attack on: the claim's "rule block 22" / `block22_present` framing — the name implies
position/ordinal, which the counter never checks.

Fixture `c1-marker-first-jvha53g5` (rev `8207acae…`): the marked filler block is the
**first** block, labelled `1.`, followed by 21 plain blocks.

```
exit 0   UTC 2026-10-28T16:01:04Z
stdout sha256 f669386092724b115fdc0c229234f8ad65fbf059cdabaac5e519ef6f6d144dee
block22_present 1   rule_blocks 22   failing []   met_target true
```

`block22_present` is just `len([b for b in blocks if MARKER in b])`
(`c1-counter.py:59-62,135-136`). Position and ordinal are free; this is exactly why A3/A4
work. **Fix:** the A3(a) anchor, plus require the marker block's leading ordinal to equal
`rule_blocks` (the landed block satisfies both).

## A6 — the red case `red-relabelled-21-block` does not test relabelling: **falsified**

Attack on: the R45-C1 kill rule's evidentiary claim that a relabelled block is a red case.

Read `tools/round-45/c1-counter.py:278-281`:

```python
def relabelled(d):
    block = good_block().replace("22. Freeze integrity.", "20. Freeze integrity.")
    f = make_repo(d, skill_with(20, block), STUB_OK)     # 20 plain + block = 21 blocks
```

The fixture is 20 plain blocks **and** the block, so `rule_blocks == 21`. Reproduced pair
(receipts `iso-relabel-20plain.*`, `iso-relabel-21plain.*`; script `isolation.py`):

| fixture | plain blocks | `rule_blocks` | exit | `failing` |
|---|---|---|---|---|
| same relabel (`20.`), their shape | 20 | 21 | **1** | `["rule_blocks 21 != 22"]` — **only** reason |
| same relabel (`20.`) | 21 | 22 | **0** | `[]`, `met_target true` |

So the case's redness is 100% the block count; the relabel is never exercised, and the
case name overstates what it proves. **Fix:** rename it `red-21-block-count` and add the
semantic case `red-relabelled-22-block`; the latter fails today, which is the defect A3/A4
report.

---

## A7 — C2 six rows naming non-existent tools: holds

Attack on: the R45-C2 kill rule ("six rows naming other tools still report six
unregistered").

Fixture `c2-ghost-d9p1j3_k` (rev `a32d64b0…`): registry header plus
`| \`tools/round-99/ghost-N.py\` | gate | \`0\` met; \`1\` not met; \`2\` unevaluable | \`--selftest\` |`
for N=0..5.

```
exit 1   UTC 2026-10-28T16:01:04Z
stdout sha256 c9fe792a9157123f5c29f504680234f638b563f6fcdf147071e7638bd76bb3a3
registry_rows 6   registered []   failing: ["unregistered: [ …the six scope paths… ]"]
```

The stopping clause is the exact-path-equality lookup (`c2-counter.py:101`); naming a tool
that does not exist cannot satisfy a scope path. The specified kill case works.

## A8 — C2 six vacuous rows: predicate holds as written; calibration not enforced

Attack on: the R45-C2 claim's calibration value ("the registry says which instruments exist
and what their exits mean").

Fixture `c2-vacuous-u1dlg9wx` (rev `8e8d93f6…`): six rows with the **correct** scope paths
and no content — `| \`<scope path>\` | x | 0 1 2 | x |`.

```
exit 0   UTC 2026-10-28T16:01:04Z
stdout sha256 64d0bf2fe280d6111e2f3684bfec0f757420c42bc5ea003d7a87ce007029f4e0
registered [all six]   thin []   failing []   met_target true
```

`exits_ok` (`c2-counter.py:59-60`) only asks that each of the digit tokens `0`, `1`, `2`
appears in the cell; it never asks that a code be paired with a meaning, and the gate cell
(`cells[1]`) and selftest cell (`cells[3]`) are never read. A one-letter gate and a
four-space exit cell score.

Verdict: the claim's predicate is met **exactly as written**, so this is not a predicate
falsification — it is a strength limit: the calibration gain the claim asserts is not
measured, and the kill rule's "row counting cannot substitute for path equality" leaves
this shape open. **Fix:** require the exit cell to pair each code with a word
(`0` met/clean, `1` not met/violation, `2` could-not-evaluate) and require the gate cell to
be non-filler; add selftest case `red-vacuous-row` (this fixture) expecting 1.

---

## Cross-cutting — what the C1 predicate actually measures

1. **The interpreter clause is frozen-bytes evidence, not landing evidence.** The
   interpreter's arms were added **inside `base..freeze`**, not inside the scored range:

   ```
   $ git -C kaidoku-shokunin diff --stat 149133d4 f762b72 -- tools/round-45/ plans/round-45-claims.md
    tools/round-45/frozen-path-preflight.py | 318 ++++++++++++++++-----   (55 deletions)
   $ git show 149133d4:tools/round-45/frozen-path-preflight.py | grep -c selftest
   0
   $ git show 149133d4:tools/round-45/frozen-path-preflight.py | grep -oE 'restored|dirty' | sort -u
   (empty)
   ```

   The freeze's interpreter has 11 named cases (`green-clean`, `green-dirfreeze-pathspec`,
   `green-dirty-without-arm`, `green-empty-range`, `red-bulk-sweep`,
   `red-dirfreeze-no-pathspec`, `red-dirty`, `red-nonancestor`, `red-restored`,
   `red-touched`, `red-unknown-freeze`) and passes 11/0 (A3/A4 receipts).

2. **The counter scores `freeze..rev` only** (`c1-counter.py:52-53,122-127`) and the scored range
   touches no frozen path (diff above is empty through HEAD). So clause 6 is identical for
   a do-nothing landing and for the real landing: my fixtures passed it with **zero**
   interpreter edits. The entire C1 delta the counter can see is SKILL.md block 22's shape.

3. **Consequence for the claim text.** `plans/round-45-claims.md` §R45-C1 asserts "the
   interpreter gains the four arms and an `--selftest`" but cites no receipt for that delta,
   and its own counter cannot observe it. Suggested: record the base→freeze diff (or a
   `interpreter_changed_since_base: true/false` field in the receipt) so the sentence is
   falsifiable, and state that clause 6 certifies the frozen bytes, not the landing.

This is the depth reading the L1 asked for: R45-C1's *table* clause is a shape check and
its *interpreter* clause is satisfied before the landing starts.

---

## Residual risk and verification gaps

- **G1 (not run).** Every fixture used `freeze == rev`, so the `frozen_path_changed` arm is
  vacuous in all of them. The same skip shapes with `freeze != rev` were not exercised;
  `git log --name-only f762b72..rev -- tools/round-45/ plans/round-45-claims.md` is empty
  through HEAD, so the range arm cannot differ, but this is inference, not a run.
- **G2 (design, not exercised).** Both counters read only git objects (`git show`,
  `git log`, `git cat-file`); the lane's 24 untracked paths under `.ufo/waves/round-45/`
  cannot affect them. A dirty *frozen* path was not exercised here.
- **G3 (out of scope).** I did not score the landed SKILL.md at landing/A1; other seats own
  that. I state only its shape: block 22's table is 12 lines (header + separator + 10 data
  rows), so A3/A4's `rows >= 8` is cleared with margin — which is exactly why the count
  cannot be the discriminator.
- **G4 (already routed, not re-tested).** The `--dirty-pathspec` false-clean and the
  `git log --name-only` merge blindness are recorded in block 22 itself as R45-CL15 and
  R45-CL6; this seat did not duplicate them.
- **G5 (honest limitation).** The fixture repos lived in `/fast/scratch/.../fx/` and were
  deleted with the scratch tree. The durable evidence is the receipt set copied here plus
  the two scripts (`driver.py`, `isolation.py`) that rebuild every fixture byte-identically
  from the lane's frozen objects.

## Receipts (in `receipts/`, provenance in `receipts/manifest.tsv`)

| name | tool | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| c1-relabelled-triage | c1-counter.py | 0 | `a8d346f9f5d60076d81681ee80c92519e332523cf507753a712c4eb6713aa8f2` | 16:01:03Z |
| c1-filler-rows | c1-counter.py | 0 | `0aae1564a7e4afa1c0a515ef58dc0568ac0145ff3ebeb5571b0b43f4335a4a74` | 16:01:03Z |
| c1-marker-first | c1-counter.py | 0 | `f669386092724b115fdc0c229234f8ad65fbf059cdabaac5e519ef6f6d144dee` | 16:01:04Z |
| c2-six-ghost-rows | c2-counter.py | 1 | `c9fe792a9157123f5c29f504680234f638b563f6fcdf147071e7638bd76bb3a3` | 16:01:04Z |
| c2-six-vacuous-rows | c2-counter.py | 0 | `64d0bf2fe280d6111e2f3684bfec0f757420c42bc5ea003d7a87ce007029f4e0` | 16:01:04Z |
| iso-relabel-20plain | c1-counter.py | 1 | `cd4f83c4ff2943cc6f9154f0ccc897eb49fb05d79e8e8848145eaa86d18c7d42` | 16:01:28Z |
| iso-relabel-21plain | c1-counter.py | 0 | `6c7859f3c6a7317e465a5dc7d744a26b52d8cf292adade00fcb2f24ce940ea73` | 16:01:28Z |

Controls re-scored from scratch (`controls/`): C1 exit 1
`e2731609959b489750a703fc12a5605ad4538395c5f808424e142dfff41fb4e1` 15:59:48Z;
C2 exit 1 `d6e202aac80ee78d9a6fbd1113ea5b62fb51b27503faccb38dec8afdb9216dd0` 15:59:48Z.

Reproduce: `S=<scratch> TMPDIR=$S/tmp HYAKU_SCRATCH=$S/tmp python3 driver.py`
(A3–A8) and `python3 isolation.py <S> <lane>` (A6); both create `$S/fx/<name>/`, `git init`
there, assert `rev-parse --show-toplevel`, and copy the interpreter and citation targets
from the lane with read-only `git show`.

## What the L1 should route

1. **R45-C1 kill rule is evadable by one plain block + eight filler rows** (exit 0). Either
   amend the predicate with the A3(a)+(b) anchors or record that the depth claim is
   shape-only and lower its weight.
2. **`red-relabelled-21-block` tests the count, not the relabel** — rename or replace with
   the 22-block semantic case.
3. **C1 clause 6 certifies pre-landing bytes** and the claim's "the interpreter gains the
   four arms" has no receipt; record the base→freeze delta.
4. **R45-C2 rows can be vacuous** (`| path | x | 0 1 2 | x |` scores) — the calibration
   value claim is not enforced; add the exit-cell meaning check and `red-vacuous-row`.
5. **Both do-nothing controls reproduce exactly**, so nothing in the record's *before*
   values is wrong — the exceptions are the kill rules and one selftest case name.
