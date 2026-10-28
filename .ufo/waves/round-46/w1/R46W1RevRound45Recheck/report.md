# R46W1RevRound45Recheck — round 45's central sentences, re-read against committed bytes

Seat `R46W1RevRound45Recheck` (reviewer, round 46 wave 1, leaf). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; round-46 freeze
`31820472784284727546808acc31b3ea1e73919b`. Read-only on the lane tree: every probe ran on
**copies** of the frozen round-45 instruments and on throwaway fixture repos under
`S=/fast/scratch/hyaku/kaidoku-r46/R46W1RevRound45Recheck` (`$S` removed after the receipts
were copied here). No installs, no git mutation in the lane, no pacman transaction.

Documents re-read: `.ufo/reports/round-45/kaidoku.md` (fleet root, read-only, 341 lines) and
`corpus/lessons/round-45.md` (247 lines). Instruments re-run: the **frozen** round-45
counters, byte-copied from the freeze commit —
`tools/round-45/c1-counter.py` sha256 `2cfc5a48…a509` (identical at `e715263c`, `1f4b27f8`,
`fedd11bf`, `f59565b7`), `tools/round-45/c2-counter.py` sha256 `50212d0f…b025`,
`tools/round-45/frozen-path-preflight.py` sha256 `633ebc05…523b`.

Receipts (command, cwd, exit, stdout sha256, UTC) are in
`.ufo/waves/round-46/w1/R46W1RevRound45Recheck/receipts.json`; the fixture recipes are the
committed ones (`.ufo/waves/round-45/w1/R45W1CritC1/attacks.py` @`0ee50aaf`, the CritC2
construction in `.ufo/waves/round-45/w1/R45W1CritC2/report.md` §3), so every line below is
re-derivable.

## Verdicts

| # | sentence under re-check | verdict |
|---|---|---|
| **a** | the two artefacts named are *really scored green* ("both counters are shown non-discriminating by wave-1 attacks", `kaidoku.md:15-17`) | **SUPPORTED — independently reproduced**, with one number wrong: the C1 artefact is **40 lines**, not 44 |
| **b** | recorded `block22_refs` sequence **6/7/8/8** (`kaidoku.md:130`, `:258-261`, `:271`) | **SUPPORTED exactly** |
| **c** | "**no seat falsified either claim predicate**" (`kaidoku.md:234-236`) | **UNSUPPORTED as written**; supported only if narrowed to "the numbered score clauses" |
| **d** | wave sizes **40/36**, **15 dead seats** (`kaidoku.md:82-84`, `:239`, `:300-302`) | **SIZES and DEAD SEATS SUPPORTED**; the same bullet's "34 with reports at the record; `R45W2Immutable` and `R45W2Distill` produced no artefact" is **false at HEAD** |

## (a) The two forgeries are green — reproduced, and the 44 is a 40

**C1, cheapest forgery.** Fixture rebuilt from the committed generator
(`R45W1CritC1/attacks.py`, `a6`): 21 plain bullets + one marker block with 8 garbage rows
(`| lorem i | ipsum | i%3 | dolor |`), four line-less refs, and a 4-line stub interpreter
that prints `PREFLIGHT_SELFTEST: cases=11 failures=0`. Scored with the frozen counter at
the fixture's own root commit:

```
# $S/counter45.py is a byte-copy of tools/round-45/c1-counter.py@f762b727 (sha256 2cfc5a48…a509)
/usr/bin/python3 -I -B $S/counter45.py --root $S/fx-a6-… --freeze <fixture root> --rev <same>
→ exit 0, met_target true, rule_blocks 22, block22_present 1, block22_rows 8,
  block22_refs 4, block22_unresolved_citations [], preflight_selftest {cases 11, failures 0, ok true}
```

**C1, garbage rows with the *real* interpreter** (`a2`: same block, REFS4 line-less, real
preflight): exit **0**, `met_target true`, `failing []`. So even without the stub the
predicate is green on content-free rows.

**C1 control** (`a1`: 21 plain bullets, no marker): exit **1**, `met_target false`, exactly
the five failing clauses the round-45 control names.

**C2, six fenced rows.** Fixture: the six real scope paths copied from the freeze, the real
`registry-scope.json`, and a 13-line `SKILL.md` whose only content is `## Random notes` and a
fenced `draft, not published` block of six lines
``| see `tools/…` (wrapper) | ?? | 0/1/2 |``. No registry heading, no header row.

```
# $S/c2counter45.py is a byte-copy of tools/round-45/c2-counter.py@f762b727 (sha256 50212d0f…b025)
/usr/bin/python3 -I -B $S/c2counter45.py --root $S/fx-c2-… --freeze <root> --rev <root>
→ exit 0, met_target true, scope_size 6, registry_rows 6, registered = all six,
  unregistered [], thin [], frozen_path_changed []
```

Both round-45 sentences are therefore true in substance: the forgeries are green, and the
defect is the measure, not the landing.

**Correction to the number.** The same generator produces `SKILL.md` at **40 lines / 1,233
bytes** (measured: `len(splitlines()) == 40`, ends with a newline) plus a **4-line**
interpreter. "44-line artefact" (`kaidoku.md:16`, `:138`; `corpus/lessons/round-45.md:143`;
and — frozen — `plans/round-46-claims.md:31,105`) is the sum of the two files, while the
seat's own sentence separates them ("44-line artefact … **and** a four-line stub
interpreter", `R45W1CritC1/report.md:60-64`; same split at `:17`). Round 46 may say
"40-line `SKILL.md` plus a 4-line stub interpreter (44 lines in total)"; it may not present
44 as the artefact's line count measured against the generator.

Adjacent sentence checked and **supported**: the C1 counter's own golden selftest case is
built on the stub — `STUB_OK` is the interpreter in `green()` at
`tools/round-45/c1-counter.py@f762b727`, lines 251-256 and 274-276. So "the instrument's canonical green fixture *is* the forgery"
(`R45W1CritC1/report.md:71-73`) is accurate, which is what R46-C1's clause 6/7 rests on.

## (b) `block22_refs` 6 / 7 / 8 / 8 — exactly

Frozen counter, one run per revision (`--freeze f762b727`, `--json-out` into scratch):

| rev | exit | `met_target` | `block22_refs` | `block22_rows` | `rule_blocks` | `failing` |
|---|---|---|---|---|---|---|
| `e715263c` (landing) | 0 | true | **6** | 10 | 22 | [] |
| `1f4b27f8` (A1) | 0 | true | **7** | 10 | 22 | [] |
| `fedd11bf` (A2) | 0 | true | **8** | 10 | 22 | [] |
| `f59565b7` (A3 = measured) | 0 | true | **8** | 10 | 22 | [] |

So `kaidoku.md:130` ("grew 6 → 7 (A1) → 8 (A2/A3)") and `:258-261` ("`block22_refs` grew
6 → 7 → 8 … corrected in `e00b9f6b`") are right, and `99fdb9e4`'s SCORECARD correction is
right. The earlier "the values are identical at …" sentence was already struck; do not
reintroduce it, and do not tighten it the other way either — the verdicts (`exit 0`,
`met_target true`, `failing []`) *are* invariant while `block22_refs` is not.

## (c) "No seat falsified either claim predicate" — true only after narrowing

Two different objects are being merged in that sentence.

1. **The numbered predicate clauses** (`plans/round-45-claims.md:46-59` for C1,
   `:102-110` for C2). My four C1 runs return `failing []` at every recorded revision; the
   wave-2 reruns and the landed six registry rows reproduce too. *No seat falsified these*
   — supported.
2. **The claims file's own binding sentences outside the numbered list.** These were
   falsified, and by wave-2 seats the round's own report quotes:
   - `plans/round-45-claims.md:143-149` — "a touch makes the counter exit 2
     `frozen_path_changed` and print no `met_target`", and the kill rule at `:74-80`. A
     **merge-resolution** touch prints `met_target: true`:
     `R45W2ReviewC1` B1 (`:63`), `R45W2CritC1Text` F7 (`:209`), `R45W2FreezeBytes` V9,
     `R45W2ReviewC2` A5′, `R45W2Immutable` A8/A9 (exit 0, `frozen_path_changed []` — read
     directly), and wave-1 `R45W1RevFreezeCommit` F1 and `R45W1CritC2` F1 (`report.md:26`).
     Distill's B21 lists the same set and routes it CL6.
   - `plans/round-45-claims.md:25-27` — "C2's counter … never reads block 22. Either lands
     and scores without the other." `R45W2CritC2Text` A6 (`report.md:24`) scores a
     block-22-shaped table as six C2 rows: `met_target: true`
     (`receipts/block22seam.stdout`, sha256 `156f1477…`); Distill B14 records "the claims
     file's … is false".

The fleet report says both things: `:234-236` ("no seat falsified either claim predicate")
and `:318-320` ("both counters' freeze arm is merge-blind (R45-CL6)"). One of them has to
give; the second is the measured one.

**My own reproduction of the freeze-arm defect** (so the finding does not rest on a sibling's
receipt): amended-merge topology of `R45W1RevFreezeCommit/fixtures/evil_merge_probe.sh` —
freeze → side branch commits `a.txt` → trunk commits `b.txt` → `merge --no-ff` → append to
`frozen/target.txt` → `commit --amend`. Tip has **2 parents**. Then:

```
git log --name-only --format= F..H -- frozen/                       → ""        (exit 0)
git log -m --diff-merges=first-parent --name-only --format= F..H -- frozen/ → frozen/target.txt
frozen_path_changed() from the frozen c1-counter (FROZEN=["frozen"]) → []
```

**Second topology, same result.** The same fixture built with `git merge --no-ff --no-commit`
followed by the edit and a plain `git commit` (no amend) also yields a 2-parent tip, an empty
plain log, `frozen/t.txt` under `-m --diff-merges=first-parent`, and
`frozen_path_changed() == []`. The blindness is a property of the merge's **own resolution
edit**, not of the amend, so the claim sentence at `:143-149` is false for both.
(`receipts.json` labels `f1-amended-merge`, `f1b-non-amend-merge-resolution`.)

### The converse sentence in the seat report is the one to distrust

`R45W1CritC1/report.md:45` records attack 10 as "**sound** (strongest merge counterexample I
could build; the arm holds)", and `:120-122` concludes "Merge-commit blindness was my
strongest structural hypothesis against the freeze arm; the fixture refuted it (attack 10 →
exit 2), so I report no defect there." **That fixture never built a merge on this host.**
Replaying its exact construction (`attacks.py` `a7`) with `git init -q`:

```
git checkout -q master
→ exit 1, "error: pathspec 'master' did not match any file(s) known to git"
   (init.defaultBranch = main on this host, git 2.56.0)
git rev-list --parents -n1 HEAD   → one parent (tip is an ordinary commit)
```

The appends were therefore committed as a **single-parent** commit on `side`, which the
counter sees normally (exit 2). The seat's "the arm holds" is an artefact of a broken
fixture, and it contradicts `R45W1CritC2` F1 and `R45W1RevFreezeCommit` F1 — which are the
ones my reproduction confirms. Round 46 must quote the **defect** (CL6) and must not carry
the "fixture refuted merge-blindness" sentence into block 23's rationale.

## (d) 40 / 36 and 15 dead — supported; two wave-2 artefact sentences are not

| quantity | source | value |
|---|---|---|
| wave-1 dispatch | `.ufo/waves/round-45/w1-dispatch.json` `counts` | `spawn 40, total 40` |
| wave-1 ledger | `r45-w1-results.json` | 40 rows, **25 non-empty**, **15 dead**, names identical to `kaidoku.md:302-308` |
| wave-1 role mix | ledger `agent` field | 17 executor, 5 scout, 4 reviewer, 4 critic, 3 mutation-tester, 3 scribe, 1 sentinel, 1 connector, 1 simplifier, 1 revenger — matches `:284-287` (sum 40); non-empty subset 12/3/3/3/2/2 = 25, "8 of 25 attack roles" ✓ |
| wave-2 dispatch | `w2-dispatch.json` `counts` | `spawn 36, total 36` |
| wave-2 ledger | `r45-w2-results.json` | 36 rows, **36 non-empty**, 36 distinct names |
| wave-2 role mix | ledger | 10 reviewer, 8 executor, 5 critic, 4 mutation-tester, 3 sentinel, 2 scribe, 1 scout, 1 simplifier, 1 connector, 1 revenger — matches `:292-294` (sum 36; 22 attack seats, 61% ✓) |
| wave-2 artefacts at HEAD | `git ls-tree -r HEAD -- .ufo/waves/round-45/w2` | **36** `*/report.md`, **34** flat `<seat>.md` |

The 15 dead wave-1 names are exactly the ledger's `output: null` rows; fifteen, no
backfill, and the report's list matches character for character.

**Unsupported at HEAD:** `kaidoku.md:239-240` — "Wave 2 = 36 seats (dispatch `1d04c6af`),
**34 with reports at the record**; `R45W2Immutable` and `R45W2Distill` **produced no
artefact**." At HEAD both seats have a committed `report.md` (both landed at `99fdb9e4`), and
the count is 36/36 — the report itself says so 60 lines later (`:296-298`, "36 reports of 36
seats"). 34 is the count of flat `<seat>.md` deliverables, not of reports, and the same
sentence's two named seats are among the 36. Round 46 must use "36 of 36 seat reports; 34
flat deliverables" or drop the sub-count.

**"11 independent seats reproduce exit 0"** (`:235-236`) is a floor I can only bound from
above: 24 of the 36 wave-2 reports contain both a `f762b727` reference and a `met_target`
field, and 28 name a counter at all (grep over `w2/*/report.md`); that does not prove each of
the 24 ran the counter on the landed bytes, only that the record is dense enough for a
conservative "at least eleven". Not falsified — but it is
not an enumerable count from the committed bytes without Distill's per-report read, so state
it as "at least eleven" or cite Distill's table.

**"Ten distinct forgery fixtures score `met_target: true`"** (`R45W1CritC1/report.md:17`;
`kaidoku.md:51-53`) is supported **only as the union of the two batteries**: the main table
has 11 fixtures and **6** greens (`a2`, `a3b`, `a4`, `a4b`, `a5`, `a6`), and
`follow-results.json` adds 4 more greens (`a3a-22`, `a10`, `a12`, `a13`) = 10. Do not
restate it as "the table shows ten".

## Sentences round 46 must not repeat

1. "**a 44-line forged C1 artefact**" as a measured artefact size → the generator yields a
   **40-line** `SKILL.md`; 44 is 40 + the 4-line stub interpreter. (`kaidoku.md:16,138`;
   `corpus/lessons/round-45.md:143`; frozen `plans/round-46-claims.md:31,105` — the frozen
   file cannot be edited, so correct it in the round-46 report/lesson and in block 23's
   prose if block 23 restates it.)
2. "**no seat falsified either claim predicate**", unqualified → narrow to "no seat
   falsified any numbered score clause of the landed artefact at the measured revisions";
   wave-2 seats **did** falsify the claims file's freeze-integrity rule (merge topology) and
   its causal-separability sentence.
3. "**the merge counterexample was refuted — the arm holds**"
   (`R45W1CritC1/report.md:45,120-122`) → the fixture could not build a merge on this host
   (`git checkout master` exit 1 under `init.defaultBranch=main`); the tip has one parent.
   R45-CL6 is the measured state; quote the amended-merge topology, not this fixture.
4. "**Wave 2 … 34 with reports at the record; `R45W2Immutable` and `R45W2Distill` produced
   no artefact**" (`kaidoku.md:239-240`) → at HEAD 36/36 seat `report.md`, both named seats
   included (landed `99fdb9e4`); 34 is the flat-deliverable count.
5. "**the values are identical at `e715263c`, `1f4b27f8`, `fedd11bf` and A3**" → already
   falsified (`block22_refs` 6/7/8/8) and corrected at `99fdb9e4`; do not reintroduce it in
   any form, including as "the receipts are byte-identical apart from `block22_refs`" if the
   provenance/depth fields are meant.
6. "**ten forgery fixtures score green**" without the split → main battery 6 of 11; ten is
   main + follow-up.

## What round 46 may assert (safe restatements)

- The C1 cheapest forgery is green under the round-45 frozen counter: garbage rows, four
  line-less refs, a 4-line stub interpreter; a **40-line `SKILL.md`**, exit 0,
  `met_target true` (my receipt, this seat).
- The C2 cheapest bypass is green: six fenced rows, no registry heading, no header row,
  contained (not exact) cell 0, `0/1/2` exit cell; 13-line `SKILL.md`; exit 0,
  `met_target true`, `thin []`, `unregistered []` (my receipt).
- The round-45 count of registry/instrument rows and its `block22_refs` progression 6/7/8/8
  are exact.
- Wave shape 40/36 with 15 wave-1 dead seats, named exactly, and role mixes as recorded.
- The C1 counter's own green selftest case is the stub
  (`tools/round-45/c1-counter.py@f762b727`, lines 251-256 and 274-276),
  so a v2 predicate that pins the interpreter by sha256 and requires the nine forgery
  classes red is the right repair — cross-checked: all nine class names in
  `plans/round-46-claims.md:73-77` occur in `tools/round-46/attest.py` (`MUTATIONS` at
  `:355`)
  (`garbage-rows`, `thin-rows`, `lineless-refs`, `header-substring`, `two-markers`,
  `stub-pin`, `self-refs`, `missing-routed-id`, `no-vocab-arm`).

## Residual risk and verification gaps

- **Not run:** the round-46 instruments (`attest.py`, `registry.py`) — other seats own those
  batteries; this seat only re-used the forgery recipes as inputs. Nothing here says the v2
  checks reject the 40-line artefact; that is the battery seats' finding.
- **Not run:** the `git merge --squash` fold (B11), `git replace` (B4), and the
  `--dirty-pathspec` false-clean — carried from round 45's record, not re-measured here.
- **Not re-derived:** Distill's per-report classification of the 34 (35) peer reports; I
  counted candidate reports, not verdicts, so the "11" figure is bounded, not enumerated.
- **Merge-blindness was measured on two topologies, both blind**: an amended merge and a
  `--no-commit` merge-resolution edit committed without amend (2-parent tips, empty plain
  log, `frozen_path_changed []`). The same frozen counter does see an **ordinary
  single-parent** commit touching the frozen path (that is what the `a7` replay actually
  produced: exit 2). No other topology was tested — shallow/replace histories, squash folds
  and renamed directories are out of scope here. Block 23's `-m --diff-merges=first-parent`
  arm is the right repair for the two measured cases; whether it also covers the untested
  ones is the battery seats' question, not this seat's claim.
- Fixture repos were private (`git init` under `$S`, `rev-parse --show-toplevel == $S/...`
  asserted), throwaway identity local to each fixture, `$S` deleted after the receipts were
  copied. The lane tree stayed read-only: `git status --porcelain` shows only pre-existing
  round-45 wave files and round-46 wave files, none written by this seat.
