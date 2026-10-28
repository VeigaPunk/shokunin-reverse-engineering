# R45W2C2Rerun — adversarial falsification of R45-C2's score

Seat: `R45W2C2Rerun` (reviewer, leaf). Wave 2, round 45, lane `kaidoku`.
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`;
A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`; A2; A3 `f59565b782c18b0eb691bec12f52d2f80d9f5032`.
Lane HEAD observed at review time `a63d109faa050207d4c184471889049741c9ebbf` (read-only; no lane
path was written by this seat).
Scratch: `/fast/scratch/hyaku/kaidoku-r45/R45W2C2Rerun` (removed after receipts were copied).
Receipts: `.ufo/waves/round-45/w2/R45W2C2Rerun/receipts/`.
All times UTC; source files carry `-0300` mtimes and are converted below.
No installs were made (nothing needed; pacman untouched).

## Headline

The **measured C2 score survives**: exit 0 at A3, object-identical to the recorded
`c2-at-1f4b27f8.json` and to `c2-at-A3.json`, and identical across all four scored revisions
(landing, A1, A2, A3) except the `rev` field. The assignment's required suffix test also
**holds**: a first cell renamed to `c1-counter.py` is *not* registered.

But the **instrument's stated predicates are weaker than the claim says**, in four ways that are
reachable by editing only `SKILL.md` (the graded, unfrozen surface): the `thin` clause is
first-row-wins, the row scope is "any pipe line anywhere in `SKILL.md` including a fenced code
block", the exit-code column is assumed to be column 3 in a document with 143 five-column tables
whose column 3 is `command`, and `scope_size` is a length rather than a distinct-set check.
None of these is exercised by the measured revision (verified independently below), so they do
not falsify the score — they falsify the *kill rules* and the *predicate wording*, and every one
of them is outside the counter's 7-case selftest.

## Verdicts

| # | attack | verdict | exit | receipt sha256 (stdout) |
|---|---|---|---|---|
| A1 | rerun the score at A3, compare with the recorded A1 receipt | **holds** | 0 | `a352f65c…41d4`¹ |
| A2 | do-nothing control at the freeze | **holds** | 1 | `d6e202aa…6dd0` |
| A3 | required test: first cell = leaf suffix `c1-counter.py` | **holds** (suffix rejected) | 1 | `62037166…c8c5` |
| A4 | first cell = `round-44/c1-counter.py`, `….py.bak`, `x/tools/…`, `/repo/tools/…`, `tools/round-44/deep/…` | **holds** (all rejected) | 1 | see A4 table |
| A5 | duplicate row: good row first, thin row second | **falsified** — `thin []`, exit 0 | 0 | `2442216a…9099` |
| A6 | same duplicate, thin row first (control) | holds (thin detected) | 1 | `0f17f366…622e` |
| A7 | row exists only under `## Sources` (7 cells) | **falsified** — registered, exit 0 | 0 | `2c6718d9…bb7c` |
| A8 | row exists only inside a fenced code block | **falsified** — registered, exit 0 | 0 | `d8c0a282…1ccb` |
| A9 | row in a 5-column table: col3 = `command` naming 0/1/2, col4 = bare `non-zero` | **falsified** — `thin []`, exit 0 | 0 | `e096315d…ce9b` |
| A10 | row in a 5-column table: col3 = plain command, col4 names 0/1/2 | falsified in the safe direction (false `thin`) | 1 | `c8ed83b8…d417` |
| A11 | exit cell names `0`,`1` but not `2` | holds (thin) | 1 | `622ff442…8c01` |
| A12 | exit cell names only `10`,`11`,`12` | holds (thin) | 1 | `6c34b86f…c50f` |
| A13 | scope = 6 entries with one path duplicated, one instrument's row deleted | **falsified** (latent) — exit 0 | 0 | `24f0ecf2…0052` |
| A14 | scope names an instrument that does not exist at rev, row present | **falsified** (latent) — exit 0 | 0 | `c7b1656d…c515` |
| A15 | touch a frozen path, then restore it (round-44 defect) | **holds** — exit 2, blob identical at tip | 2 | console² |
| A16 | registry rows' own factual claims (case counts, exit arms, `--dry-run`, oracle) | **holds** — all reproduce | — | see A16 |
| A17 | scope under-inclusion (claims also name round-42/43 counters) | **holds** — claims:308 marks them audit-only | — | see A17 |

¹ stdout hash of the compact JSON. The `--json-out` object is **object-equal** to
`.ufo/waves/round-45/l1/scores/c2-at-A3.json` (parsed-JSON comparison returned `True`); the file
is written with `indent=1`/`sort_keys`, so it is not byte-identical to the compact stdout.
² receipt `receipts/a15-touch-restore.txt`, sha256
`fa5d14caa843bad4fb4830c61de6ce3d6a1219482f99dbbb2fa651c063dbb29e`, 2026-10-28T16:04:13Z.

## A1 — the score, rerun at A3 (holds)

```sh
python3 -I -B tools/round-45/c2-counter.py --root . \
  --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec \
  --rev f59565b782c18b0eb691bec12f52d2f80d9f5032 \
  --json-out $S/c2-at-f59565b.json
```

`exit 0`, stdout sha256 `a352f65c098e76f8a00dcb8a86725036f85fc26e86aef0d57db61061e42041d4`,
2026-10-28T15:59:24Z.

```json
{"registered": [all six], "unregistered": [], "thin": [], "scope_size": 6,
 "registry_rows": 45, "frozen_path_changed": [], "met_target": true, "failing": []}
```

Diff against `.ufo/waves/round-45/l1/scores/c2-at-1f4b27f8.json`: **one field** — `rev`
(`1f4b27f8…` → `f59565b7…`). Every other field, including `registry_rows: 45`, is identical.
Extending the comparison to `c2-at-e715263c.json`, `c2-at-A2.json`, `c2-at-A3.json`: all four are
the same object modulo `rev`. The A1→A3 amendments therefore did not move the C2 measurement —
consistent with `git diff e715263c 1f4b27f8 -- SKILL.md` showing no `|` line changes.

Record note (for L1): `SCORECARD.md:3533` cites `c2-at-1f4b27f8.json` as the after-receipt while
`SCORECARD.md:3589-3590` says "**The measured revision for the round is A3**" with
`…/c2-at-A3.json`. Two receipts name one measurement. The values agree, so this is a citation
defect, not a value defect; the L1 should say which receipt is canonical.

## A2 — the before (holds)

```sh
python3 -I -B tools/round-45/c2-counter.py --root . \
  --freeze f762b7… --rev f762b7…
```

`exit 1`; sha256 `d6e202aac80ee78d9a6fbd1113ea5b62fb51b27503faccb38dec8afdb9216dd0`;
object `==` `.ufo/waves/round-45/controls/ctl-c2-0-do-nothing.json` (compared as parsed JSON:
`True`). `registered []`, `registry_rows 39`, six unregistered, `scope_size 6`. The claim's
premise sentence also reproduces: `git show f762b7…:SKILL.md | grep -c round-44` → `0` (grep
exit 1).

At the freeze the frozen instrument exists (`registry_rows` is read from `SKILL.md`, and the
scope file resolves), so the before is a real do-nothing, not an unevaluable: exit **1**, not 2.

## A3 — the assignment's exact-equality test: suffix (holds)

Fixture: `git init` in fresh dir, `rev-parse --show-toplevel` asserted equal to the fixture, byte
copies of the lane's `SKILL.md`, `plans/round-45-claims.md` and `tools/round-45/registry-scope.json`
committed as the freeze; then **one** edit — the first cell of the
`tools/round-44/c1-counter.py` row becomes `` `c1-counter.py` `` — committed as the scored rev.
`--root` is the fixture; the freeze/rev are its own commits.

Result: `exit 1`, sha256 `6203716685fa493a543f0ea8d5fec0ac86d1fb8a7648b707e7fa1c300c1ed8c5`:

```json
{"unregistered": ["tools/round-44/c1-counter.py"], "registered": [5 paths], "thin": [],
 "registry_rows": 44, "failing": ["unregistered: ['tools/round-44/c1-counter.py']"]}
```

**Answer to the question asked: no — the counter does not report that path registered.** The
mutated row is dropped from the row set entirely (`registry_rows` 45 → 44) and the path is
reported unregistered. The suffix is treated as "this row names no tool", not as an alias.

Mechanism (why the whole near-miss family fails): `ROW_TOOL` is
`` re.compile(r"`(tools/[A-Za-z0-9._/-]+\.(?:py|sh))`") `` — the literal backticks anchor the
token on both sides and it must begin `tools/` and end `.py`/`.sh`. So the comparison is a
backticked relative-path equality, which is stronger than the claim's wording requires and
strong enough for the suffix test.

## A4 — near-miss first cells (holds, 5/5)

Same fixture construction, one first cell replaced, scored at `freeze..rev`:

| case | first cell | exit | unregistered | stdout sha256 |
|---|---|---|---|---|
| A4.1 | `round-44/c1-counter.py` | 1 | the path | `78bb1350…1a3e` |
| B | `tools/round-44/c1-counter.py.bak` | 1 | the path | `99eaa71c…8c15` |
| C | `x/tools/round-44/c1-counter.py` | 1 | the path | `3619c5a6…e38e` |
| D | `/repo/tools/round-44/c1-counter.py` | 1 | the path | `c499f148…e7b8` |
| E | `tools/round-44/deep/c1-counter.py` | 1 | the path | `f2d898f7…4f45` |

E is the sharp one for the claim's "a row naming another tool does not count": same leaf name,
different directory, and it does not register. A11 and A12 bound the other side of the `thin`
clause: a cell naming `0`/`1` without `2` is thin, and a cell naming only `10`/`11`/`12` is thin
(the `\b\d\b` token test does not accept embedded digits).

## A5/A6 — the `thin` clause is first-row-wins (falsified)

Claim kill rule (`plans/round-45-claims.md`, R45-C2): "a row that names the path but writes a
bare 'non-zero' exit cell reports `thin`". That is only true for the *first* row for that path.

A5 input: the A3 `SKILL.md`, line 1652 kept **verbatim**, and immediately after it a duplicate row
for the same path whose third cell is `non-zero on any failure`:

```
| `tools/round-44/c1-counter.py` | gate — … | `0` met; `1` not met; `2` could-not-evaluate | … |   <- original
| `tools/round-44/c1-counter.py` | gate — … | non-zero on any failure                        | … |   <- duplicate
```

`exit 0`, sha256 `2442216ad4e5ca3e4dc693d3579b99a82b57b78aadd71eb9e8058275e6ce9099`,
`thin []`, `unregistered []`, `registry_rows 46`, `met_target true`.

A6 control: the same two rows with the thin row **first** → `exit 1`,
sha256 `0f17f366b9838cbd82ea8e3eae76701559eb5a027d6ef07da16104295cce622e`,
`thin ["tools/round-44/c1-counter.py"]`. So the check exists; it is applied to one arbitrary
row (`by_tool.setdefault`, c2-counter.py:122-124).

Differing value: recorded/claimed `thin == []` ⇒ "that row's exit-code cell names 0, 1 and 2"
for the path; observed: `thin == []` can coexist with a bare `non-zero` row for that path.

Fix (round 46; the tool is byte-frozen this round): make `by_tool` a list per path and report
`thin` if **any** row for the path omits 0/1/2, or make a second row for a scope path itself a
failing condition (`duplicate_rows`), since the registry is meant to have one row per instrument.

## A7/A8 — the row scope is the whole file, fences included (falsified)

Claim predicate: "some `SKILL.md` **registry row's** first cell is exactly that path".
Implementation: `parse_rows` (c2-counter.py:51-64) scans every line beginning with `|`, requires
≥3 cells, and never looks at the enclosing heading or a fence state.

A7: the real registry row deleted, and re-added under `## Sources` in a 7-column table
(`| tool | gate or probe | verdict map (exit codes) | … |`) → `exit 0`,
sha256 `2c6718d95968ee58ecfc7058f51fa9cab5ec15b751727efdc625c96f75b6bb7c`, all six registered,
`thin []`.

A8: the same, but the row lives only inside a fenced code block:

```
```
| `tools/round-44/c1-counter.py` | gate | `0` met; `1` not met; `2` … | x | y | kaidoku |
```
```

→ `exit 0`, sha256 `d8c0a282c3264eacbc3fea67782cab58cf92be9930a04fdd6f23de042d721ccb`,
registered. A8 is the cleaner falsification: a fenced block is unambiguously not a registry row,
and it is also not a rendered table.

Fix: bind the row set to the registry section(s), i.e. start parsing only under a
`### … instrument registry` heading and reset on the next heading of the same or higher level;
skip fenced blocks.

## A9/A10 — the exit-code column is positional, and `SKILL.md` has 143 five-column tables (falsified)

`thin` reads `cells[2]` unconditionally (c2-counter.py:127-129, comment "cells[2] is the
'verdict map (exit codes)' column of the registry table"). That is true of the 7-column registry
(`SKILL.md:1650`) and false of every 5-column table (`SKILL.md:1291,1335,1506`:
`| tool | purpose | command | exit codes | selftest |`). Independent parse of the A3 `SKILL.md`:
433 pipe rows with ≥3 cells, of which **143 have 5 columns** and 49 have 7.

A9 (false pass): move the row into a 5-column table with
cells[2] = `` `--mode 0 --retry 1 --code 2` `` and cells[3] = `non-zero on any failure`
→ `exit 0`, sha256 `e096315d0311920b883352f6a0fac31e536545b06a057a6117d71444ba18ce9b`,
`thin []`. The row's *actual* exit cell is a bare `non-zero`; the counter passed it by reading
the command cell.

A10 (false thin, safe direction): a 5-column row whose command cell has no digits and whose
fourth cell names `0`/`1`/`2` → `exit 1`, `thin` reported, even though the row does state the
exit map. Same root cause, opposite sign: the verdict depends on table shape, not on the cell.

Fix: resolve the column by header name per table (`exit codes` or `verdict map (exit codes)`), or
apply A7's fix and accept only the 7-column registry header.

## A13 — `scope_size` is a length, not a distinct set (falsified, latent)

Fixture freeze carries a scope file of six entries where `tools/round-44/c1-counter.py` appears
twice and `tools/round-45/c2-counter.py` is absent; the scored rev deletes the
`c2-counter.py` row. Result: `exit 0`,
sha256 `24f0ecf2d8deeba44f24967e6c0a4fe292040a5efcedadee8b723b13db9e0052`,
`registered` lists the duplicated path twice, `scope_size 6`, `unregistered []`.

So five distinct instruments satisfy `scope_size == 6`. Not live at the measured revision: the
frozen scope file has six distinct paths (read from `git show f762b7…:tools/round-45/registry-scope.json`),
and that file lives under `tools/round-45/`, so any post-freeze edit that could create this shape
makes the counter exit 2 `frozen_path_changed` first. Fix: `len(set(scope)) == 6`, or fail on a
duplicate entry.

## A14 — registration never checks the instrument exists (falsified, latent)

Scope replaces `tools/round-45/c2-counter.py` with `tools/round-45/ghost-instrument.py` (never
created in the tree); a registry row names it. Result: `exit 0`,
sha256 `c7b1656d397bf17be5d91298ae7680632d0c26a18ca64944a8a290c79e51c515`, all six registered.
Control with the row omitted: `exit 1`, `unregistered: ['tools/round-45/ghost-instrument.py']`
(sha256 `1043ac16…2d72`). So the counter certifies "the registry names the instruments" without
ever asking whether the instrument exists. Not live: `git ls-tree f59565b tools/round-44/ tools/round-45/`
contains all six scope paths. Fix: `git cat-file -e <rev>:<path>` per scope entry.

## A15 — touch-then-restore does not un-block (holds)

Fixture: freeze → commit that rewrites `tools/round-45/frozen.py` → commit that restores the
original bytes. The tip blob hash equals the freeze blob hash
(`dcc27807b20456027b6a152f9756c62360e229d6` on both sides) and `git diff --quiet <freeze> HEAD`
reports **no difference at all** (`tree_equal_freeze=yes`), and the counter still says:

```json
{"counter":"round-45-c2","verdict":"could_not_evaluate","reason":"frozen_path_changed",
 "frozen_path_changed":["tools/round-45/frozen.py"]}
```
with `exit 2`. Two related arms also exit 2 on the real lane-derived fixture: a new file at
`tools/round-45/new-instrument.py` (`d081d2cf…2b34`) and a nested one at
`tools/round-45/sub/deep.py` (`428ec75c…35ba`). The round-44 defect (tip equality as the test) is
closed in this counter — the arm reads `git log --name-only F..R` over the directory pathspec.

## A16 — the six registry rows' own claims (holds, 6/6)

Each row was checked against the instrument it names, not against the counter:

| row (`SKILL.md` line at A3) | claim | observed |
|---|---|---|
| 1652 `round-44/c1-counter.py` | `--selftest` 47 cases, green 2026-10-28 | `{"cases": 47, "failures": []}`, exit 0 |
| 1653 `round-44/c1-run.sh` | no oracle; `--dry-run` prints and writes nothing; 0/1/2 map | `grep -i oracle` → none in `c1-run.sh` **and** none in `c1-run.py`; `extract-firmware` at `c1-run.py:347`; `--dry-run` "writes nothing at all" at `c1-run.py:18`, branch at `:901`; `err(){…exit 2;}` at `c1-run.sh:37`; "Exit: 0 … 1 … 2 could not evaluate" in the header |
| 1654 `round-44/c2-counter.py` | `--selftest` green | exit 0, last case `P44-C2 ok` |
| 1655 `round-45/frozen-path-preflight.py` | 11 cases; arms commit/restored/blob/dirty/pathspec; `2` includes `pathspec_required` and unknown/non-ancestor rev | `PREFLIGHT_SELFTEST: cases=11 failures=0`; fixture arms: `pathspec_required` → exit 2 (`uncovered_frozen_dirs: ["tools/round-45"]`), non-ancestor → exit 2 (`freeze is not an ancestor of rev`) |
| 1656 `round-45/c1-counter.py` | 9 cases | `C1_SELFTEST: cases=9 failures=0` |
| 1657 `round-45/c2-counter.py` | 7 cases | `C2_SELFTEST: cases=7 failures=0` |

The A3 correction to the `c1-run.sh` row is accurate: neither the shell wrapper nor the Python
sibling mentions an oracle, and `--dry-run` is real. One wording nit: the row's self-test cell
for `round-44/c1-counter.py` carries the placeholder `<rea-agents 6.5.0 root>` rather than a
pinned path — not a falsehood (47 cases do reproduce; `--pkg65` is optional, `c1-counter.py:209`)
but not a runnable command either.

## A17 — scope under-inclusion (holds)

`plans/round-44-claims.md` also names `tools/round-42/c1-counter.py` and
`tools/round-43/c1-counter.py`. Excluding them from the six is correct: line 308 of that file
lists those two as "(audit-only port sources)", and the scope's own definition
(`registry-scope.json` `why`) is "the instruments named as instruments". `tools/round-44/c2-rubric.json`,
`carriers.json` and the `control-fixtures/` trees are inputs, not instruments. No under-inclusion.

## Severity, residual risk, gaps

**S1 (material, `SKILL.md`-reachable): A5 duplicate-row escape.** The `thin` clause can be
satisfied while a bare-"non-zero" row for a scope path exists, as long as the good row comes
first. `SKILL.md` is the graded surface and is explicitly *not* frozen, so any later edit that
appends a row silently defeats the check.

**S2 (material): A7/A8 row scope.** Registration is satisfied by a row in an unrelated section or
inside a code fence. The count `registry_rows: 45` therefore has no scoping meaning.

**S3 (material): A9/A10 column position.** With 143 five-column tables in the same file, the
`thin` verdict is decided by table shape. This is the only hole with both signs (false pass and
false thin).

**S4/S5 (low, latent): A13 `scope_size`, A14 existence.** Unreachable at the measured revision
because the scope file is frozen and correct, but they mean the predicate's two "counting cannot
substitute" claims are weaker than stated.

**Why the score still stands.** Independent parse of the A3 `SKILL.md`: each of the six scope paths
has **exactly one** row with that first cell, all six are in `### Round-44/45 instrument registry`,
all six rows have 7 cells, and each third cell names `0`, `1`, `2`. None of S1–S5 is exploited by
the measured revision; the measurement is real.

**Residual risk / verification gaps.** (i) The counter's selftest set is 7 cases and covers none
of S1–S5, so the instrument cannot detect its own holes; a round-46 hardening should add three
red cases (`dup-thin-after` → expect `thin`, `row-in-codeblock` → expect `unregistered`,
`legacy-column` → expect `thin`). The tool is byte-frozen this round, so no fix lands now.
(ii) `SCORECARD.md` names two receipts for one measurement (A1 and A3) — values agree.
(iii) Not run: `tools/round-44/c1-run.sh --dry-run` (it would enter the lane's data-procedure
path; I read the wrapper header and the sibling's dry-run branch instead) and
`tools/round-44/c1-counter.py --pkg65 <real root>` (no pinned root available to this seat), so the
r44 oracle arm is source-read, not exercised by me.

## Receipts

Written to `.ufo/waves/round-45/w2/R45W2C2Rerun/receipts/`; all commands are the ones quoted
above, run with `TMPDIR`/`HYAKU_SCRATCH` = the seat scratch.

| file | sha256 | UTC |
|---|---|---|
| `c2-at-f59565b.stdout` (A1 stdout) | `a352f65c098e76f8a00dcb8a86725036f85fc26e86aef0d57db61061e42041d4` | 15:59:24 |
| `c2-at-f59565b.json` (A1 `--json-out`) | `6c322c7c375e81a8…` | 15:59:24 |
| `do-nothing.stdout` (A2) | `d6e202aac80ee78d9a6fbd1113ea5b62fb51b27503faccb38dec8afdb9216dd0` | 16:02:15 |
| `attacks.json` (A3–A4, plus three invalid runs superseded by `attacks2.json`) | `00c7bedc318935c72b879f81a6b1d2357a57d1c2e6a3076c50c523ab971bca59` | 15:59:59 |
| `attacks2.json` (A5–A12) | `f626bdb50665824861f91e3b9f96eb8e71a698ff1f0fd7cf44330684b4af67c9` | 16:00:54 |
| `attacks3.json` (A13–A14) | `08f181574b24d7ffe662a3610157d0579c3371419d3aafbd86cc667ce2d23580` | 16:01:49 |
| `preflight-pathspec-required.json` (A16) | exit 2 in file | 16:02:41 |
| `preflight-non-ancestor.json` (A16) | exit 2 in file | 16:02:41 |
| `a15-touch-restore.txt` (A15) | `fa5d14caa843bad4fb4830c61de6ce3d6a1219482f99dbbb2fa651c063dbb29e` | 16:04:13 |
| `score-*.json`, `score2-*.json`, `score3-*.json` | per-case `--json-out` receipts | — |
| `drive.py`, `drive2.py`, `drive3.py` | the fixture drivers (byte-identical to the scratch copies) | — |

`attacks.json` contains three invalid cases from the first driver pass (a wrong table-header
anchor and a hand-typed row that did not match the real row); they are recorded as they ran and
their replacements are in `attacks2.json`. No result was edited after the fact.
