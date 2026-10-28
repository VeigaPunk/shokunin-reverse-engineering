# R45W2SecWrite — write scope and determinism of the three round-45 instruments

Seat: `R45W2SecWrite` (wave 2, adversarial falsification). Read-only on the lane tree.
Writes confined to this directory. Scratch `$S=/fast/scratch/hyaku/kaidoku-r45/R45W2SecWrite`
(removed before yielding; receipts copied here). No installs, no package changes, no
network. All git use is read-only (`rev-parse`, `log`, `show`, `diff`, `cat-file`,
`merge-base`, `status --porcelain`, `ls-tree`) plus fixture-only `init/add/commit/merge`
inside `mktemp`-style dirs under `$S` with `-C "$D"` and a `rev-parse --show-toplevel`
assertion.

Contract notes: the seat spec's flat path `.ufo/waves/round-45/w2/R45W2SecWrite.md` lies
outside my permitted write root, so the report is here as `report.md` in the seat dir.

## 0. Revision map first — the seat prompt is stale

The prompt names **A1 `1f4b27f8` as "the measured revision"**. The lane record at HEAD does
not agree with itself, and neither surface agrees with the prompt:

| revision | what it is | `block22_refs` | `met_target` | exit |
|---|---|---|---|---|
| `e715263c` | landing | 6 | true | 0 |
| `1f4b27f8` | A1 | 7 | true | 0 |
| `fedd11bf` | A2 (routes CL6..CL12) | 8 | true | 0 |
| `f59565b7` | A3 — seat-named rev, "the final measured revision" in `LOG.md` | 8 | true | 0 |
| `0ee50aaf` | HEAD | 0 (c1 `--rev HEAD`) | true | 0 |

`f59565b7` is **amendment A3**, not a stray sha: `SCORECARD.md:3527` still says
`measured revision 1f4b27f8` and both SCORECARD rows carry `measured at = 1f4b27f8`, while
`LOG.md:3309-3316` says "### Amendment A3 — the final measured revision … A3 is the round's
measured revision". See N2/N1 below. **The verdict is stable across all five revisions**
(`met_target true`, `failing []`, exit 0); only `block22_refs` moves.

## 1. Write scope (primary axis) — verdict: `holds`

### 1.1 Method
Before/after pair around all six invocations (3 scoring + 3 `--selftest`), all run with
`cwd = <lane>` and `--root <lane>`:

- `git -C <lane> status --porcelain` captured before and after → **byte-identical**
  (4 pre-existing untracked `l1/` entries, unchanged).
- `git -C <lane> rev-parse HEAD` before/after → `0ee50aaff516571aa607769bbbdf19a3db90dfa5`
  both times.
- Full-tree stat scan `(relpath → (st_size, st_mtime_ns))`, **44,431 files**, `.git/`
  excluded, this seat's own dir excluded: `changed_files = []`.
- Independent positive control: a fixture copy with `chmod -R a-w` scores unchanged
  (`c1` exit 0, `c2` exit 0, `pf` exit 1 on that fixture's merge-added frozen file,
  `pf --check-dirty` exit 1), with empty stderr — the tools need **no** write access to
  the scored root.

Evidence: `receipts.json`, `evidence-phaseA.json` (`porcelain_identical: true`,
`files_scanned: 44431`, `changed_files: []`, `lane_head_before == lane_head_after`).

### 1.2 The write surface is real but environment-derived, not root-derived — n/a to the claim, reported
`scratch_dir()` / `scratch_root()` resolve `$HYAKU_SCRATCH` → `$TMPDIR` →
`tempfile.gettempdir()`. `--root` never influences where scratch is written. Consequences,
measured, none of which touch the lane under the lane's own `TMPDIR=$S` convention:

| invocation | left behind under the scratch base | bytes |
|---|---|---|
| `c1-counter --selftest` | `kaidoku-r45/` (1 empty dir, 0 files) | 0 |
| `c1-counter --root … ` (scoring) | `kaidoku-r45/` (1 empty dir) | 0 |
| `c2-counter --selftest` | `kaidoku-r45/` (1 empty dir) | 0 |
| `frozen-path-preflight --selftest` | `kaidoku-r45/preflight-selftest/` with **11 fixture repos**, 400 files / 261 dirs — never `rmtree`d | 316,981 |
| `frozen-path-preflight --root …` (scoring) | nothing | 0 |

`frozen-path-preflight.py:186` (`d = tempfile.mkdtemp(dir=base)`) mkdtemps one repo per
case and `selftest()` has **no cleanup** (contrast `c1-counter.py:337` and
`c2-counter.py:239`, which do `shutil.rmtree`); `scratch_root()` also leaves the
`kaidoku-r45/preflight-selftest` parent behind (`:50-58`). No claim asserts cleanup, and the registry rows say only "selftest
fixtures under `$HYAKU_SCRATCH` or `$TMPDIR`" — so this is a hygiene defect, not a
falsified claim.

**The sharp part:** point the scratch base *inside* the scored tree and the tool writes
`<root>/tmpinside/kaidoku-r45/` into the tree under test (reproduced:
`new: ['tmpinside/', 'tmpinside/kaidoku-r45/']`), and **`git status --porcelain` reports
nothing** — an empty directory is invisible to the worktree arm that this round's gate and
this seat's own contract both rely on (`S140` porcelain). So the prescribed pair
"`git status --porcelain` before/after **and** a directory scan" is not redundant: porcelain
alone structurally cannot see this class of write, and the mtime scan must be dir-aware
(files only → 0 hits; files+dirs → 2 hits). Consequence for any seat repeating this check:
use the directory-aware scan, porcelain only as the tracked-content half. Severity: LOW
(requires a misdirected env; the lane's own convention is correct).

## 2. Determinism (primary axis) — verdict: `holds`, with one self-description defect

### 2.1 Receipts are byte-deterministic; no timestamps, no tmp paths
Two runs each, **different scratch roots**, plus three rev spellings (`1f4b27f8`,
`f59565b7`, `f762b727` short, `^{commit}`-peeled, relative `--root .`, trailing-slash
`--root …/`). Every pairing is byte-identical:

| receipt | exit | stdout sha256 | UTC |
|---|---|---|---|
| c1 @A1 run1 | 0 | `d30817c559e0949ab8500a9f04e5349db79cac5d2bb8df2d8f88f6732463a32b` | 2026-10-28T16:06:12Z |
| c1 @A1 run2 | 0 | `d30817c559e0949ab8500a9f04e5349db79cac5d2bb8df2d8f88f6732463a32b` | 2026-10-28T16:06:13Z |
| c1 @A3 run1 | 0 | `90597e617067fe4f17399c7e114f36ff5ce7e7da24cb3ce7d06d3b43e57b6f18` | 2026-10-28T16:06:13Z |
| c1 @A3 run2 | 0 | `90597e617067fe4f17399c7e114f36ff5ce7e7da24cb3ce7d06d3b43e57b6f18` | 2026-10-28T16:06:13Z |
| c2 @A1 run1 | 0 | `2b401a9ae5a6e562178561fba15b2ae2199f019e9b1059b0b6f65175d5e4d1ca` | 2026-10-28T16:06:13Z |
| c2 @A1 run2 | 0 | `2b401a9ae5a6e562178561fba15b2ae2199f019e9b1059b0b6f65175d5e4d1ca` | 2026-10-28T16:06:13Z |
| pf @A1 run1 | 0 | `7fc4f592413f6b2c5b70428ec896f4282071138932be4d60670897546e24dde6` | 2026-10-28T16:06:13Z |
| pf @A1 run2 | 0 | `7fc4f592413f6b2c5b70428ec896f4282071138932be4d60670897546e24dde6` | 2026-10-28T16:06:13Z |
| pf @A1 **+`--check-dirty`** | 0 | `7fc4f592413f6b2c5b70428ec896f4282071138932be4d60670897546e24dde6` | 2026-10-28T16:06:13Z |
| c1 `--selftest` | 0 | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` | 2026-10-28T16:06:13Z |
| c2 `--selftest` | 0 | `aea7e363e5661efcc038df11f2e88380c11815b480d9458f9cc26370b40b0f2d` | 2026-10-28T16:06:14Z |
| pf `--selftest` | 0 | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` | 2026-10-28T16:06:14Z |

Also identical: the `--json-out` file bytes across three runs (c1, c2), and c1's receipt
for `--root <lane>`, `--root <lane>/`, `--root .` with `cwd=<lane>`, short shas,
`^{commit}`-peeled refs. **No nondeterministic field exists to report**: no timestamp, no
scratch path, no host, no pid, no absolute root. `sort_keys=True` everywhere.
The single state-dependent field is by design: `pf`'s `dirty[]` reads the live worktree.

Negative control worth recording: `--freeze F --rev F` gives exit **1**
(`rule_blocks 21 != 22`, `block22_present 0`), matching the do-nothing control in the claim.

### 2.2 N5 (NEW, undisclosed): the receipt cannot prove which arms ran — LOW/MEDIUM
`pf @A1` and `pf @A1 --check-dirty` are **byte-identical** on a clean tree (row 7 vs row 9
above), because the receipt never records the flag: keys are exactly
`blob_changed, dirty, freeze, freeze_paths, gate, pathspec, restored, rev, touched,
verdict`. `require_pathspec` is likewise absent. So a "clean" receipt cannot evidence that
the worktree arm — the arm block 22 calls "the one that matters most" — was switched on,
nor that the directory freeze was gated rather than scanned whole-tree. The round cites
gate receipts as proof the arm ran before each L1 commit (R45-CL1); that inference is not
supported by the receipt's own bytes.

Smallest fix (one line, receipt only, no arm change):
`receipt["check_dirty"] = check_dirty` and `receipt["require_pathspec"] = require_pathspec`
in `frozen-path-preflight.evaluate()` (`frozen-path-preflight.py:143-155`). Frozen file, so
round 46.

## 3. Clause-level attacks — all land, all already routed (independent reproduction)

I reproduced these before reading the routed list; they are **not new**. Recorded because
independent reproduction is the only evidence that a routed item is real rather than
asserted. Fixtures built from the frozen instruments' own helpers so the baseline is green
by construction (baseline c1/c2/pf = 0/0/0).

| # | attack (exact input) | observed | routed as | status |
|---|---|---|---|---|
| F1 | evil merge: `merge --no-ff --no-commit side` (side touches `other.txt` only), then the merge resolution rewrites `tools/round-45/frozen-path-preflight.py` | frozen blob F `813f0a5e…` ≠ M `6c72dfef…`; counter arm (`git log --name-only … -- plans/… tools/round-45`) = `[]`; **c1 exit 0 `met_target true`**, **c2 exit 0 `met_target true`**; preflight exit 1 `frozen_path_changed`, `blob_changed` names the file | R45-CL6 (HIGH) | confirmed |
| F1b | same, merge resolution **adds** `tools/round-45/EXTRA-frozen.py` | counters `met_target true`; preflight exit 1, `touched[{status:"A"}]` (its `-m --diff-merges=first-parent` sees it) | R45-CL6 | confirmed; gate is robust here |
| F1c | control: plain commit adds a frozen file | c1 exit 2 `frozen_path_changed: ["tools/round-45/EXTRA2.py"]`, c2 exit 2, pf exit 1 | — | arm correct when linear |
| F2 | six scope rows moved into a table under `## Scratch notes (not a registry)` | c2 exit 0, `met_target true`, `registered` 6 | R45-CL14(a) / CL9(A3) | confirmed |
| F3 | exit cell `0 warnings; 1 author; 2 modes` | c2 exit 0, `thin []` | R45-CL14(d) / CL9(A6) | confirmed |
| F5 | `## Queue-drain craft` heading without the trailing space | uncaught `IndexError`, exit 1, no JSON — a could-not-evaluate reads as not-met | R45-CL13(f) | confirmed |
| F6 | 10 rows `\|  \|  \| 1 \|  \|` (empty trigger/arm/receipt) | c1 exit 0, `block22_rows 10` | R45-CL4 / CL13 | confirmed; block 22 itself states this limit |
| F7 | block adds `corpus/SOURCES.md:99999` and `tools/round-45/gone.py:7` (absent) | `block22_unresolved_citations []`, refs 4, exit 0 | R45-CL9(A2) / CL13(b) | confirmed |

Root cause for F1/F1b is one line in each counter (`c1-counter.py:52-53`,
`c2-counter.py:63-64`): plain `git log --name-only` prints no diff for a merge commit.
**It does not touch the measured figure**: `rev-list --count f762b727..1f4b27f8` = 3,
`rev-list --merges` = empty (same for `..HEAD`), and every changed path in the range is
`SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md` or `.ufo/waves/…` — none
frozen. So the score stands at every revision I measured; the rule sentence does not.

## 4. New findings (not in R45-CL1..CL17)

Disclosure check: `grep -ci` over `corpus/lessons/round-45.md@HEAD` for `12-17`,
`mislocat`, `leftover`, `cleanup`, `rmtree`, `TMPDIR`, `check_dirty` → all 0. The routed
list covers the *measure*; the items below are either record text, the landing's own
citation, or write/hygiene.

### N1 — `LOG.md` "reports the same values" is false (record; cheapest fix)
`LOG.md:3314-3316`: "A3 is the round's measured revision; every earlier measurement
(`e715263c`, `1f4b27f8`, `fedd11bf`) reports the same values."
Measured `block22_refs`: **`e715263c` 6, `1f4b27f8` 7, `fedd11bf` 8** — three different
values among the three revisions the sentence names, and the sentence's own paragraph
records `block22_refs 8` for A3 two lines earlier. The lane's own receipts agree:
`.ufo/waves/round-45/l1/scores/c1-at-1f4b27f8.json` → `block22_refs 7`;
`…/c1-at-A3.json` → `block22_refs 8`.
Fix: "the same verdict (`met_target true`, `failing []`, exit 0); `block22_refs` rises
6 → 7 → 8 as A1/A2 add citations." No claim value changes; `>= 4` holds throughout.

### N2 — the record names two different measured revisions at the same HEAD (MEDIUM)
`SCORECARD.md:3527` `measured revision 1f4b27f8`, and both claim rows carry
`measured at = 1f4b27f8` with the A1 `block22_refs 7` in the "after" cell — while
`LOG.md:3309` heads "### Amendment A3 — the final measured revision" and
`1d04c6af` (same HEAD) adds `scores/c1-at-A3.json`, `scores/c2-at-A3.json`,
`preflight-at-A2-both.json`. A reader cannot tell which revision the verdict is bound to,
and the SCORECARD "after" cell states a value (7) that the declared measured revision (A3)
does not produce (8).
Fix: SCORECARD line 3527 → "measured revision `f59565b7` (A3); landing measurement
`1f4b27f8`", and set the two `measured at` cells to `f59565b7` with the A1 value noted, or
revert LOG's "final" wording. Nothing about the verdict changes.

### N3 — the landing's citation `corpus/lessons/round-45.md:12-17` is mislocated (LOW/MEDIUM)
Block 22 (the reference sits at `SKILL.md:608` at HEAD, `:591` at `1f4b27f8`):
"Placement inside the fleet's own sweep path is not a lane edit — the fleet scripts are
read-only for a lane — so it stays an operator/integrator request and the report says so
(`corpus/lessons/round-45.md:12-17`)."
Lines 12-17 of that file are `## Mistakes`, its table header/separator, and rows **M45-1**
(sweep contamination) and **M45-2** (unopened-descendant-credit) — checked at both
revisions, and 12-17 contains **zero** occurrences of `read-only` or
`operator/integrator`. The supporting sentence is in `## Routed defects` → R45-CL1 ("the
fleet's `scripts/hyaku/` tree is read-only for this lane … so placement in the
sweep/pre-push path is an operator/integrator request"): **`:67-68` at `1f4b27f8`** and
**`:71-72` at `f59565b7`/HEAD** (A2 inserted four lines; the file grows 91 → 187 lines).
Range 12-17 resolves at every revision, which is why `block22_unresolved_citations == []`
and why F7's class of hole exists.
Fix: point the reference at the R45-CL1 sentence for the revision being scored
(`:67-68` at A1, `:71-72` at A3). One line, in the graded (unfrozen) surface.
Calibration: this is a counterexample to R45-CL13's broader conclusion that "the landed
artefact is genuine … the defect is the measure, not the landing". The *measure* cannot see
it (bounds-only); here the *landing* is also wrong in one citation. Everything else in CL13
about the landed artefact (ten real rows, arms matching the interpreter, 11 real fixtures)
survives my read.

### N4 — write-scope leftovers and the porcelain blind spot
See §1.2. New, LOW. Minimal fix for round 46: `shutil.rmtree` the per-case dirs at the end
of `frozen-path-preflight.selftest()` (mirroring c1/c2), and remove the `kaidoku-r45`
parent after use; optionally refuse a scratch base that is inside `--root`.

### N5 — receipt does not record `--check-dirty` / `--require-pathspec`
See §2.2. New, LOW/MEDIUM.

## 5. Verdict table

| attack | verdict | evidence |
|---|---|---|
| tools write into the lane tree on scoring / selftest | **holds** (nothing written) | 44,431-file stat scan delta `[]`; porcelain identical; HEAD unchanged; read-only-root probe scores |
| `c1-counter --rev f59565b7` twice, diff receipts | **holds** (byte-identical) | sha `90597e61…` both runs; `--json-out` bytes identical |
| determinism of c1/c2/pf across scratch roots, rev spellings, root spellings | **holds**; no timestamp/tmp-path field | table §2.1 |
| receipt is self-describing about which arms ran | **falsified** (N5) | `pf` and `pf --check-dirty` byte-identical, keys lack both flags |
| freeze arm catches a merge-introduced frozen touch | **falsified** for counters, **holds** for the gate | F1/F1b; already routed CL6; measured range has no merge → score unaffected |
| c2 measures "the registry names the instruments" | **falsified as instrumented** (rows anywhere) | F2/F3; already routed CL14 |
| block 22 citations all resolve *to their proposition* | **falsified** once (N3) | `:12-17` vs `:67-68` |
| `LOG.md` "same values" across revisions | **falsified** (N1) | refs 6/7/8/8 from four live runs + two lane receipts |
| record names one measured revision | **falsified** (N2) | SCORECARD:3527 vs LOG:3309, same HEAD |
| no scratch leftovers | **falsified** (N4) | 400 files/261 dirs/317 KB per `pf --selftest` |
| `--dirty-pathspec` false-clean; arm isolation; docstring `-z`; two-marker; 23-block; suffix lookup | **not run** — already reproduced in wave 1 and routed (CL15, CL15, CL11, CL13(d), CL7, CL8); re-running adds no evidence | — |
| r44 counters at tip (CL5) | **not run** — out of seat | — |

## 6. Why "not run" is not a gap
Every `not run` above is either (a) already reproduced with a named fixture by a wave-1
seat and routed to round 46, or (b) outside this seat's surface (r44 instruments). The
three surfaces this seat owns — lane write scope, receipt determinism, and the record's
claim that the receipts are the evidence — were executed end to end, including a
read-only-root positive control and a negative control (empty range → exit 1).

## 7. Tooling / hygiene
No installs (`pacman` untouched; nothing added to any `PATH` dir). `git` and `python3`
(3.x, stdlib only) as shipped. Scratch `$S` deleted after copying receipts into this
directory. This seat's only lane write is this directory; `git status --porcelain` shows it
as one untracked path (`?? .ufo/waves/round-45/w2/R45W2SecWrite/`), which no round-45
counter's pathspec reads.

## 8. Receipt index (this directory)
- `receipts.json` — the 12 primary runs: exact argv, cwd, exit, stdout/stderr sha256, UTC,
  scratch dir.
- `receipt-00 … receipt-11` — their verbatim stdout.
- `evidence-phaseA.json` — write-scope before/after pair (scan counts, porcelain, HEAD).
- `evidence-f1-evil-merge.json`, `evidence-f1b-f1c.json` — merge fixtures (F, M, parent,
  blob ids, all three tools' verdicts, the raw counter arm output).
- `evidence-mutants.json` — F2/F3/F4/F5/F6/F7 per-case receipts.
- `evidence-det.json`, `evidence-det2.json` — determinism matrix (scratch roots, rev/root
  spellings, `--json-out` byte identity, leftover inventories).
