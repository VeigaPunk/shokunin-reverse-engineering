# R45W2CritC1Text — R45-C1's text against its instrument, clause by clause

Seat `R45W2CritC1Text`, round 45 wave 2 (adversarial falsification), lane `kaidoku-shokunin`,
2026-10-28. Scope: the **wording of the R45-C1 claim** versus the **one instrument that
computes it** (`tools/round-45/c1-counter.py`), plus the 10 table rows of `SKILL.md`
rule block 22 against their interpreter (`tools/round-45/frozen-path-preflight.py`).
Read-only on the lane tree: every lane write below is under
`.ufo/waves/round-45/w2/R45W2CritC1Text/`; every mutation was made to a scratch copy of the
HEAD tree, and every fixture repo was created with `git init` in scratch and its
`rev-parse --show-toplevel` asserted equal to the fixture path before the first commit.

## 0. Provenance (verified, not assumed)

| what | value | how |
|---|---|---|
| lane HEAD | `0ee50aaff516571aa607769bbbdf19a3db90dfa5` | `git rev-parse HEAD` |
| freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | `git log --format=%H -1 -- plans/round-45-claims.md` |
| landing / A1 / A3 | `e715263c…`, `1f4b27f8…`, `f59565b7…` | `git log -1 <rev>` |
| `SKILL.md` at A3 vs HEAD | no diff | `git diff --stat f59565b7 0ee50aaf -- SKILL.md` (empty) |
| counter under test | `sha256 2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509` | `sha256sum tools/round-45/c1-counter.py` |
| interpreter | `sha256 633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` | `sha256sum tools/round-45/frozen-path-preflight.py` |
| frozen claims | `sha256 56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e` | `sha256sum plans/round-45-claims.md` |
| frozen paths untouched HEAD | `git diff --stat f762b72..HEAD -- plans/round-45-claims.md tools/round-45/` empty | exit 0 |

Receipts: `receipts.tsv` in this directory — every row is `test, exit, stdout sha256, UTC,
exact command`. Scratch (`/fast/scratch/hyaku/kaidoku-r45/R45W2CritC1Text`) removed after the
receipts and harness were copied here.

## 1. Clause → field → exact failing string

`failing` is a list of strings; exit is `0` iff it is empty, `1` otherwise, and `2` only from
the early returns (no `met_target` key at all). The left column is the frozen claims text;
nothing here is paraphrased from the SKILL block.

| # | clause (`plans/round-45-claims.md` R45-C1) | receipt field | exact `failing` string | verdict |
|---|---|---|---|---|
| 1 | `rule_blocks == 22` | `rule_blocks` | `rule_blocks {n} != 22` | **holds** — 21 at base and freeze, 22 at A1/A3/HEAD |
| 2 | `block22_present == 1` | `block22_present` | `block22_present {n} != 1` | **holds** — byte-identical to the claims wording ("exactly one *block* contains the marker") |
| 3a | `block22_rows >= 8` | `block22_rows` | `block22_rows {n} < 8` | **holds as a pipe-line count**, not as "rule rows" (see F1) |
| 3b | "the table header carries `trigger`, `arm`, `exit`, `receipt`" | `block22_header_ok` | `block22 table header lacks trigger/arm/exit/receipt` | **falsified as "columns are"** (F1) |
| 3c | "every row's exit cell is exactly one of `0`, `1`, `2`" | **no field** — only `len(bad_exit)` inside the message | `block22 exit cells outside {0,1,2}: {n}` | computed, but a report disclosure: the receipt has no field, and no positive field when true |
| 4a | `block22_refs >= 4` | `block22_refs` | `block22_refs {n} < 4` | holds as a mention count; **falsified as "located citations"** (F2) |
| 4b | `block22_unresolved_citations == []` — "every `path:line` or `path:first-last` reference resolves at `--rev`" | `block22_unresolved_citations` | `unresolved citations: {list}` | **falsified as worded** — the domain is two prefixes (F3) |
| 5a | "The block cites `S140`" | `block22_cites.S140` | `block22 does not cite S140` | token presence only; **falsified as provenance** (F4) |
| 5b | "cites … `tools/round-45/frozen-path-preflight.py`" | `block22_cites.interpreter` | `block22 does not cite interpreter` | holds (message names `interpreter`, not the path) |
| 5c | "the interpreter is present at `--rev`" | `interpreter_present` | `interpreter absent at rev` | holds (`cat-file -e` at tip) |
| 6a | selftest "exit 0 and `cases >= 11`, `failures == 0`" | `preflight_selftest` (`exit`,`cases`,`failures`,`ok`) | `preflight selftest {dict}` | holds as computed — 11/0 at every revision |
| 6b | "(the red cases are named: touched, restored, dirty, pathspec-required, unknown freeze, non-ancestor, bulk sweep)" | **no field** — the counter parses only the summary line | — | names are true of the bytes, but **nothing computes them**; falsified as a discriminator (F5) |
| T | "`failing == []`, counter exit 0" | `failing`, `met_target`, exit | — | **holds** at A1, A3 and HEAD (exit 0, `met_target true`) |

Exit-2 vocabulary (`verdict: could_not_evaluate` added by the CLI): `unknown freeze revision`,
`unknown rev revision`, `freeze is not an ancestor of rev`, `git log failed`,
`frozen_path_changed` (+ list), `SKILL.md absent at rev`.

Freeze-integrity rule sentence ("no commit in `FREEZE..REV` touches a frozen path … a touch makes
the counter exit 2 `frozen_path_changed` and print no `met_target`"): field `frozen_path_changed`,
present **only** in the exit-2 receipt. Direct touch **holds** (T6, exit 2, keys `counter`,
`frozen_path_changed`, `reason`, `verdict` — no `met_target`); restore-after-touch **holds**
(T10, exit 2 although the tip blob equals the freeze blob); **merge-resolution touch is
falsified** (F7).

`Before`: "At the freeze, exit 1: `rule_blocks 21 != 22`, `block22_present 0 != 1`,
`block22_rows 0 < 8`, `block22_refs 0 < 4`." Reproduced exactly (`lane/freeze-do-nothing`,
exit 1) and byte-identical to `controls/ctl-c1-0-do-nothing.json`; the receipt carries a
**fifth** reason the sentence omits: `block22 table header lacks trigger/arm/exit/receipt`.
"At the base the same receipt prints the same values": true — `lane/base-do-nothing` prints
the same five strings (`ctl-c1-0-base.json` matches).

`Kill rule`: the five named `--selftest` cases exist and all pass
(`lane/c1-counter-selftest`, exit 0, `C1_SELFTEST: cases=9 failures=0`).

## 2. Clause with NO field (report disclosure, not claim)

| text | why it is not a claim |
|---|---|
| "every row's exit cell is exactly one of `0`,`1`,`2`" | no receipt field; only a count inside `failing` (T5: exit 1, `failing ["block22 exit cells outside {0,1,2}: 1"]`, no other field changes) |
| "the red cases are named: …" | no field; the counter reads `PREFLIGHT_SELFTEST: cases=N failures=M` only (F5) |
| "The interpreter gains the four arms" (Landed surface) | no field; `interpreter_present` is `cat-file -e` (F5) |
| "a table whose columns are `trigger | arm | exit | receipt`" (Landed surface) | `block22_header_ok` exists but is substring containment; column identity is never computed (F1) |
| "located citations (four or more, all resolving …)" | `block22_refs` counts unlocated mentions too (F2) |
| "The block cites `S140`" read as a resolved source row | `block22_cites.S140` is `re.search(r"\bS140\b", block)` (F4) |
| "Sources … R45-C1 cites two rows … `S141`" | **no field at all**; only `S140` is required (T8) |
| "at least eight rule rows" as *rules* | `block22_rows` counts data lines of the first pipe-table; row content unchecked (T1) |
| block 22: "its `--selftest` carries one red case per arm" | no per-case field in any score receipt; the counter discards the case lines (F5) |

## 3. Fields the text does not mention

`block22_header_ok`; `block22_cites` as an object (and its key names `S140` / `interpreter`);
`preflight_selftest.exit` and `.ok` (`.ok` silently folds exit 0 + cases≥11 + failures==0 into one
boolean, so one clause is reported as one value); `interpreter_present`; `frozen_path_changed` in
the **met** receipt — it is structurally `[]` whenever `met_target` is true (any non-empty list
returns exit 2 first), so the field is not evidence of a clean range; the exit-2 keys `verdict`
and `reason`; and the fact that the exit-2 receipt has **no** `met_target` (claimed, holds).

## 4. Verdicts

Every row: fixture repo built from `git archive HEAD`, mutated **copy**, exact command, exit,
stdout sha256, UTC (full ledger in `receipts.tsv`). `$S` = the scratch root.

### F1 — `falsified`: the header/rows clause is a substring test, not a column test

Input: block 22's four header lines and ten rows replaced by

```
  | trigger arm exit receipt |
  | --- |
  | 1 |
  … ×10
```
(the rest of the block, its eight citations, `S140` and the interpreter path untouched).

```
python3 -I -B tools/round-45/c1-counter.py --root $S/fix-header --freeze b17849c6… --rev c752af43…
```
exit **0**, `stdout sha256 34d69d389bcecf9c…`, 2026-10-28T16:07:04Z.
Differing value: `block22_header_ok true`, `block22_rows 10`, `met_target true` — while the
landed-surface sentence says "a table whose **columns are** `trigger | arm | exit | receipt`"
and "at least eight **rule rows**". A one-cell header plus ten rows that contain nothing but
`1` satisfies every field. Wave 1 tested reordering only; collapse is the stronger probe.
Fix (SKILL is mutable): change the landed-surface sentence to the predicate's own wording
("the header carries the four words") **or** tighten the counter in round 46 to require four
distinct cells in that order and a non-empty trigger/arm cell per row. The frozen claims
sentence ("carries") is the weaker of the two and already matches the instrument.

### F2 — `falsified`: "located citations" is satisfied by unlocated ones

Input: every `:line`/`:first-last` suffix removed from block 22's eight `.md` references
(`${path}.md`, no line numbers), nothing else changed.

```
… --root $S/fix-unlocated --freeze bd5d9660… --rev b1522301…   # exit 0, sha e0291668…, 16:07:04Z
```
Differing value: `block22_refs 8`, `block22_unresolved_citations []`, `met_target true` — zero
located citations, and the counter still reports eight refs. Corroborates wave-1 probe `e`.
Fix: require `:N` on the counted refs (a `refs_located` field) or drop "located" from the
landed-surface sentence.

### F3 — `falsified`: "every `path:line` reference resolves" is scoped to two prefixes

Input: block 22 prose gains `` `corpus/SOURCES.md:99999` ``, `` `SKILL.md:99999` ``,
`` `tools/round-44/c1-counter.py:9999` `` — all past EOF / out of the regex.

```
… --root $S/fix-extra --freeze 3720dbd9… --rev 1e2fe8f6…        # exit 0, sha 8e57d6be…, 16:07:04Z
```
Differing value: `block22_refs 8` (unchanged), `block22_unresolved_citations []`. The regex is
`((?:corpus/(?:knowledge|lessons)|plans)/[A-Za-z0-9._-]+\.md)` with optional `:N`; three
unresolvable references are invisible. Corroborates wave-1 `f2/f4/f3`.
Fix: widen `REF` to any backticked relative path with `:N` (or at least `corpus/**` and
`tools/**`), or reword to "every `corpus/knowledge|lessons/` and `plans/` `.md` reference".

### F4 — `falsified`: "cites `S140`" is a token test, not a row

Input: the `S140` and `S141` rows deleted from `corpus/SOURCES.md` (block text unchanged;
`corpus/SOURCES.md` is not frozen and not in the regex).

```
… --root $S/fix-sources --freeze 72c94317… --rev a977297b…      # exit 0, sha 1fc2f442…, 16:07:04Z
```
Differing value: `block22_cites {"S140": true, "interpreter": true}`, `met_target true`.
`cites.S140` is `bool(re.search(r"\bS140\b", block))`; the source row's existence, id and
subject are never read. Fix: add a resolution field (`sources.S140.present` against
`corpus/SOURCES.md`) in round 46, or reword the clause to "the block contains the token
`S140`". The second is the honest description of what is computed today.

### F5 — `falsified`: "the interpreter gains the four arms" / "one red case per arm"

Three inputs, all accepted at exit 0:

1. **stub** — `tools/round-45/frozen-path-preflight.py` replaced (in the *freeze* commit, so no
   frozen path is touched) by three lines printing `PREFLIGHT_SELFTEST: cases=11 failures=0`
   and `sys.exit(0)`:
   `… --root $S/fix-stub --freeze b3006520… --rev b3006520…` → exit 0, sha `bf31cbd8…`,
   `preflight_selftest {"cases":11,"exit":0,"failures":0,"ok":true}`, `met_target true`.
2. **`restored` arm deleted** (the `restored.append(path)` branch removed):
   `… $S/fix-drop-restored …` → exit 0, sha `c621a066…`, 11/0.
3. **`blob` arm deleted** (`blob_changed = []` forced before `ok`):
   `… $S/fix-drop-blob …` → exit 0, sha `bc156fac…`, 11/0.

Differing value: the predicate's clause 6 reports the *same* `{cases:11, failures:0}` for a
working interpreter, a stub and two arm-deleted interpreters. There is no per-case name, no
arm field, and no code inspection. This is also the block-22 sentence "its `--selftest` carries
one red case per arm (11 cases)" — the seven printed red cases are `red-touched`,
`red-restored`, `red-dirty`, `red-dirfreeze-no-pathspec`, `red-unknown-freeze`,
`red-nonancestor`, `red-bulk-sweep`: no case isolates `blob`, and `red-restored` still exits 1
with the `restored` branch gone because `touched` is non-empty. **A3's own prose in the same
block says exactly this** ("arm-covering but not arm-isolating … deleting the `restored`
classification or the `blob` arm alone still reads 11/0"), so block 22 contradicts itself
20 lines apart. Fix (SKILL, mutable): replace "carries one red case per arm" with the A3
sentence; and in round 46 make the counter parse and require the seven case names
(`red-touched`, `red-restored`, `red-dirty`, `red-dirfreeze-no-pathspec`, `red-unknown-freeze`,
`red-nonancestor`, `red-bulk-sweep`), which the stub fails.

### F6 — `falsified`: the commit arm does not parse the `-z` form the Sources section credits

Frozen text: S141 is "`--name-status` with `-z` uses NUL field terminators … the commit arm
parses **that**". Instrument (`frozen-path-preflight.py` `evaluate`):

```
log = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status", "--format=%x00%H", …)
```
no `-z`; the parser splits fields on `\t`. Differing value: the arm parses tab-separated
`--name-status`, not NUL-terminated records. A3 already says so in block 22
("the `-z` form is the machine-safe variant this arm does not use yet (routed R45-CL11)") —
so the **frozen claims sentence is the false one**, and the SKILL text is the correction.
Fix: add `-z` to the arm and split on NUL (next round: `tools/` is frozen), then the frozen
sentence becomes true; the path that cannot be edited this round is named in §6.

### F7 — `falsified`: a merge-resolution edit of a frozen path is invisible to the counter

Input: fixture with `F0` = freeze; `side` and `main` each commit an unrelated file; merge with
`--no-ff --no-commit`, edit `plans/round-45-claims.md` **during the merge**, commit the merge
`c3dc2bd4…` (parents `e5995182…`, `337a9aeb…`).

```
… --root $S/fix-merge --freeze 6ef42c37… --rev c3dc2bd4…         # exit 0, sha 4ca044b0…, 16:07:06Z
```
Differing value: `frozen_path_changed []`, `met_target true` — while
`git log --name-only F0..M -- plans/round-45-claims.md` prints nothing and
`git log -m --diff-merges=first-parent --name-status` prints the change. The preflight on the
same fixture exits **1** (`blob_changed ["plans/round-45-claims.md"]`, sha `b9bae3bd…`).
So the frozen rule "no commit in `FREEZE..REV` touches a frozen path" fails open for the
history shape that most easily smuggles a frozen edit. A3 discloses this ("both round-45
counters have exactly that blindness (HIGH, routed R45-CL6)") but the frozen rule stays
unconditional. Fix (next round, `tools/` frozen): `git log --name-only -m
--diff-merges=first-parent` in `frozen_path_changed`, or per-commit `diff-tree -r
--name-only -m --first-parent`; meanwhile the round-45 record must not cite the rule as
covering merges.

### F8 — `falsified as worded` (disclosed at A3): the dirty row's exit 1 is flag-conditional

Table row: "the worktree is dirty under the frozen pathspec | dirty (`git status --porcelain -z`,
S140) | 1 | `dirty[]` from `--check-dirty`". Input: fixture `data/frozen.txt` dirty in the
worktree, `--pathspec data/ --freeze-path data --check-dirty`:

- default: exit **1**, `dirty [" M data/frozen.txt"]`, sha `f5fa9254…`, 16:07:06Z;
- with `--dirty-pathspec other/`: exit **0**, `dirty []`, sha `3b4df200…`, 16:07:06Z.

The row states exit 1 for the trigger, unconditionally; `dirty_pathspecs or pathspecs`
*replaces* the scope. A3 discloses it (R45-CL15). Fix: make the trigger cell read "dirty under
the pathspec passed to `--check-dirty` (defaults to `--pathspec`); `--dirty-pathspec`
replaces, not widens" — the block's prose already says this, the table cell does not.

### F9 — `holds`: direct touch is exit 2 with no `met_target`

`… $S/fix-touch` (append to the frozen claims file): exit **2**, sha `66314013…`, receipt keys
`counter`, `frozen_path_changed ["plans/round-45-claims.md"]`, `reason`, `verdict` — no
`met_target`. Matches the rule sentence.

### F10 — `holds`: history, not tip equality

Touch then restore to the exact freeze blob (`tip_blob_equals_freeze_blob true`): counter exit
**2**, sha `66314013…` (same receipt as F9); preflight exit **1** with
`restored ["plans/round-45-claims.md"]` and `blob_changed []` — the restored list is disjoint
from `blob_changed`, as row 2 claims.

### F11 — `holds`: the recorded numbers reproduce

`lane/A1` → exit 0, sha `d30817c5…`; its receipt values are identical, field for field, to
`.ufo/waves/round-45/l1/scores/c1-at-1f4b27f8.json` (measured: `rule_blocks 22`,
`block22_rows 10`, `block22_refs 7`, `unresolved []`, `preflight 11/0`, `met_target true`).
`lane/A3` → identical to `c1-at-A3.json` (`block22_refs 8`). `lane/HEAD` → same predicate values
as A3. `lane/freeze-do-nothing` and `lane/base-do-nothing` are byte-identical to the two
stored controls. The `block22_refs 7 → 8` step is A3's added prose, not a drift.

### F12 — `holds`: table rows 1, 2, 3, 5, 6, 7, 8, 9, 10

- row 1 (commit, exit 1) and row 6 (bulk sweep, exit 1): `touched[]` records
  `{commit, status, path}` — confirmed by the preflight's own `red-touched` / `red-bulk-sweep`
  cases (11/0) and by the merge-adjacent `touched` record in F7.
- row 3 "a directory entry is its tree oid, not a file": `--freeze-path data` with a change
  under `data/sub/` → `blob_changed ["data", "data/sub/f.txt"]`, exit 1, sha `791604ee…`
  (`dir-oid/blob-arm`). Note the cell does not say the directory appears *alongside* its files.
- rows 5, 7, 8, 9, 10: `red-dirfreeze-no-pathspec`, `red-unknown-freeze`, `red-nonancestor`,
  `green-clean`, `green-empty-range` all pass at 11/0.

### Not run

- Preflight `subprocess.run(..., timeout=300)` raising `TimeoutExpired` — uncaught; would exit
  1 (traceback) where the claims' semantics require 2. No receipt; not exercised.
- `craft_blocks` `IndexError` if the `## Queue-drain craft ` heading loses its trailing space —
  reachable only by editing the graded heading; not exercised.
- Independent reproduction of `red-bulk-sweep` as a hand-built fixture (covered by the
  instrument's own case; the `touched` mechanism was exercised in F7).

## 5. Does the claim assert anything the counter cannot falsify?

Yes — seven assertions in the frozen claim and in block 22 are not falsifiable by the
instrument that scores them:

1. **"The interpreter gains the four arms"** and **"one red case per arm"** — no field; a
   three-line stub and two arm-deleted interpreters score `met_target true` (F5).
2. **"the red cases are named: …"** — no field; only `cases`/`failures` are parsed (F5).
3. **"the table whose columns are `trigger | arm | exit | receipt`"** and **"at least eight
   rule rows"** — one cell carrying four words plus ten `1` cells passes (F1).
4. **"located citations (four or more)"** — eight unlocated mentions pass (F2).
5. **"every `path:line` … resolves"** — three resolvable-looking but wrong references to
   out-of-domain paths pass (F3).
6. **"cites `S140`"** as provenance — the source rows can be deleted and the field still reads
   `true` (F4); **`S141`** has no field at all (the parenthetical Sources sentence is true of
   the bytes today, but its absence cannot be detected: `S141` → `S14x` in block 22 still
   scores exit 0, sha `22d10acb…`, 16:07:05Z).
7. **The freeze-integrity rule for merges** — the field exists and reads `[]` while a
   merge-resolution edit is present (F7).

Two lesser ones are conditional rather than unfalsifiable: the dirty row's exit 1 (F8, flag
dependent) and the `-z` parsing sentence (F6, contradicted by the instrument and already
corrected in SKILL prose).

## 6. Smallest safe correction, per finding

| finding | smallest correction | surface |
|---|---|---|
| F1 | reword the landed-surface sentence to the predicate's "header carries the four words", or require four distinct header cells + non-empty trigger/arm cells | SKILL (mutable) / counter (round 46) |
| F2 | require `:N` on the counted refs, or delete "located" | counter (46) / SKILL |
| F3 | widen `REF` to any backticked relative path with `:N`, or scope the sentence to `corpus/{knowledge,lessons}/` and `plans/` | counter (46) / claims wording (46) |
| F4 | add a resolution field against `corpus/SOURCES.md`, or reword to "contains the token `S140`" | counter (46) / claims wording (46) |
| F5 | replace block 22's "one red case per arm" with the A3 sentence (already in the block); require the seven case names in the counter | SKILL (now) / counter (46) |
| F6 | add `-z` and split on NUL, or strike "the commit arm parses that" from the next claims file | interpreter (46) / claims (46) |
| F7 | `git log --name-only -m --diff-merges=first-parent` in `frozen_path_changed`; until then do not cite the arm as merge-covering | counter (46) / record (now) |
| F8 | qualify the row's trigger with `--check-dirty`'s own scope | SKILL (now) |
| F9 (Before list) | add the fifth reason (`block22 table header lacks …`) to the recorded control text | record (now) |

Nothing here is a request to weaken the claim: F1–F5 are wording that outruns the instrument
(the honest fix is to make the sentence as strong as the field, or the field as strong as the
sentence); F6–F8 are sentence-versus-instrument contradictions that the frozen text cannot
absorb and that the next claims file must carry.

## 7. Calibration — what wave 1 already had

Wave 1 found the ref-domain gaps (`R45W1C1HeaderBoundary` probes `e`, `f2`, `f3`, `f4`), the
header-substring weakness under *reordering* (`b1`–`b3`), and two counter-selftest holes
(`R45W1C1CounterMutants` m1/m2). F2 and F3 corroborate those independently; F1 (collapse to a
single cell, rows of `1`), F4 (S140 row deleted), F5 (stub and arm-deletion acceptance), F6
(`-z`), F7 (merge blindness receipt), F8 (dirty false-clean receipt) and the S141 null-field
test are new here, and F5/F7 are the two that a reader of the claim's own wording would not
expect to pass. The stored controls and all three score receipts reproduce field-for-field:
the record is honest about the numbers it reports; the gap is between the numbers and the
sentences wrapped around them.

## 8. Tooling

No installs, no upgrades, no package-manager calls. Python 3.14 stdlib and the lane's own git
were sufficient. Harness copied to `harness/` in this directory; scratch removed after the
receipts were written.
