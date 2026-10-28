# R45W2ConnFormat — is the `### Round-44/45 instrument registry` the *house* format, or this lane's invention?

Seat `R45W2ConnFormat`, round 45 wave 2 (adversarial falsification). Read-only on the lane: no
lane file was written, no git verb beyond `log/show/diff/grep/rev-parse/status`. Every counter run
below is the frozen instrument invoked with `--json-out` into seat scratch; the fixtures were built
under `/fast/scratch/hyaku/kaidoku-r45/R45W2ConnFormat/fx/` and that scratch is removed, with their
`HEAD` shas and stdout receipts preserved under `receipts/`. Freeze `f762b727`; landing `e715263c`;
amendment A1 `1f4b27f8`; measured revision per the record's own latest amendment is A3 `f59565b7`.

**Headline.** The landed section is **not** the house format. It is the lane's own 7-column
template — the byte-identical header of `### Round-36`, `### Round-40` and
`### Round-35/37/38/39` — and it drops the one field `PROTOCOL.md` mandates that the lane's
template never had: **entry command**. That is a routed defect on the *record's* standing
conformance sentence, not a blocker: R45-C2's predicate is met at every revision claimed, and I
reproduced the lane's own A3 receipt byte-for-byte.

## Verdicts

| # | attack | verdict |
|---|---|---|
| F1 | the section's column set vs the house schema (`PROTOCOL.md:398-403`) | **falsified** — 7 fields, `entry command` absent; house schema is 8 |
| F2 | first-cell convention vs this lane's `### Round-40` and vs ≥3 sibling lanes | **holds as a description, falsified as "house"** — full path is precedented (tameshi) but is a minority convention; Round-40 uses bare names, so the lane carries three cell-0 conventions in one file |
| F3 | "the registry row format is compatible with house conformance" | **falsified, and worse: the two are mutually exclusive** — a house-order row makes the lane's own C2 counter report `thin` |
| F4 | the six rows are accurate at the measured revision | **falsified at A1** (the `c1-run.sh` row; corrected by A3), **holds at A3**; the C2 score is identical at both, so the predicate cannot see the false row |
| F5 | the lane's registry family is a format at all | **falsified** — one of its four 7-column tables has no delimiter row, and 21 of the 45 rows the C2 counter counts come from it |
| F6 | the record's measured-revision sentence | **holds under append-only supersession**; the un-amended header sentence is stale (states A1 as measured) |
| C2 claim itself | `met_target` at the revisions claimed | **holds** — exit 0 at A1 and A3, `registry_rows 45`, `thin []`, `unregistered []`, no frozen path changed |

## F1 — column count and headers: 7, not the house 8

The house schema is written down once, in the protocol, and it binds child lanes:

> **Registry.** The schema is this section's; a child lane's *registry home* is its own `SKILL.md`.
> … Row fields: name, `gate|probe`, entry command, verdict map (code → class), self-test command and
> spelling, pinned-value path, write scope, owner. — `PROTOCOL.md:398-403`

Eight fields. The landed section (`SKILL.md:1623-1645` at A1) declares:

```
| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
```

Seven cells (`sed -n '1634p'` → 7; `grep -ci entry` on that line → 0 matches, exit 1). There is no
`entry command` column: the row tells a reader the self-test invocation, never the invocation that
produces a verdict. Concretely, `tools/round-44/c1-run.sh` (`SKILL.md:1637` at A1) has **no
command in any cell** — cell 4 reads "none in the script — a bad-argument probe only, no self-test".

**This is the lane's own template, not a house one.** The header line is byte-identical to three
earlier kaidoku sections:

```
sha256(sed -n '<L>p' SKILL.md) == 715513ac9ef743b45647bde14423b09340557369787c3ad78fd0d7628b9bff27
L ∈ {1537 Round-36, 1580 Round-35/37/38/39, 1608 Round-40, 1634 Round-44/45}   # A1 numbering
L ∈ {1553, 1596, 1624, 1650}                                                    # HEAD numbering
```

So the new section is a copy of a template the lane has used since round 36. **Fleet census**
(every `*/SKILL.md` table whose nearest heading contains "registry"; `receipts/measure.py`,
`receipts/fleet-census.json`):

- 149 registry tables across 16 lanes; **83 are 8-column and they span 12 lanes** (kagi, kaidoku,
  kake, kasegi, kengaku, kotoba, mado, mori, souji, tabi, tameshi, tsukuroi).
- Only 11 tables are 7-column, and only **3 distinct 7-column headers** exist fleet-wide:
  - kaidoku's, 4 uses, **no entry field** (F1 above);
  - kama `| Name | Kind / entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |`
    (`kama-shokunin/SKILL.md:430,681,728,915`) and a `(code → class)` variant at `:396` — 7 columns
    that **keep** the entry command by merging it with `kind`.

kama proves 7 columns is not the defect; dropping the field is. kaidoku's header is the only
7-column registry header in the fleet with no entry command at all.

## F2 — first-cell convention: bare filename → full path is a local flip

| section (A1 lines) | cell 0 | rows |
|---|---|---|
| `### Round-40 instrument registry` (`:1604`, header `:1608`, first row `:1610`) | **bare filename** (`` `c1-counter.py` ``, `` `sqfs-list.py` ``, …) | 12 |
| `### Round-44/45 instrument registry` (`:1623`, header `:1634`, rows `:1636-1641`) | **full path** (`` `tools/round-44/c1-counter.py` ``, …) | 6 |

Fleet, same classifier (`fullpath` = a backticked `tools/…py|sh` anywhere in cell 0):

| lane | full-path cell 0 | bare | display name |
|---|---|---|---|
| kaidoku | **45** | 12 | 35 |
| tameshi | **18** | 0 | 53 |
| other 14 registry-bearing lanes | **0** | 0 | all |

So the answer to "does any sibling lane already use the full-path first cell?" is **yes — tameshi**,
and it is *house-shaped* while doing it: `tameshi-shokunin/SKILL.md:1999-2003` is an 8-column table
(`| Name | Kind | Entry | Verdict map | Self-invocation | Persisted values | Write scope | Owner |`)
whose cell 0 is `` `tools/env-diff.py` ``, `` `tools/wave-route-mix.py` ``,
`` `tools/round21-measure.py` ``, `` `.ufo/evidence/round-21/coldread/measure.py` ``. Three
sibling lanes for comparison, all name-first with the path in the entry-command column:

- `tsukuroi-shokunin/SKILL.md:1707` — 8 cols; row `| host-census | gate | bash tools/tsukuroi-census.sh | … |`
- `kengaku-shokunin/SKILL.md:562` — 8 cols; cell 0 is a slug (`hermetic-grader`), path in cell 3.
- `kasegi-shokunin/SKILL.md:979` — 8 cols; `name | type | entry command | …`.

**Verdict.** The bare→full flip against Round-40 is real and is *precedented* (tameshi) but is not a
house convention: `PROTOCOL.md:401` names field 1 "name", and 14 of 16 lanes put a human name or slug
there. Inside this one file the lane now carries **three** cell-0 conventions — 35 display-name rows
(the local gate registry plus Rounds 22-24, 27-29, 32, 34), 12 bare rows (Round-40), 45 full-path rows
(Rounds 30/31/34-run-6/36/35-37-38-39/44-45).
That is the definition of a local convention, not a house one.

## F3 — the C2 instrument *requires* the non-house shape (the falsifying experiment)

The frozen counter resolves the verdict-map cell **positionally** and never reads a header:

- `tools/round-45/c2-counter.py:31` — `ROW_TOOL` requires `tools/…py|sh` inside backticks in cell 0;
- `:52` — `m = ROW_TOOL.search(cells[0])` (search, not equality; the claim's sentence is tighter);
- `:106-107` — `# cells[2] is the "verdict map (exit codes)" column of the registry table` then
  `if len(row["cells"]) < 3 or not exits_ok(row["cells"][2]): thin.append(path)`;
- `:59-60` — `exits_ok` needs a word-boundary `0`, `1` and `2` somewhere in that cell.

Under the house schema the verdict map is field **4**, i.e. `cells[3]`. I built two fixture repos
from the six landed rows verbatim: identical paths, identical verdict-map text, identical self-test,
pinned-path, scope and owner cells. The only difference is the mandated `entry command` column
inserted at index 2 (`ab-house`) or absent (`ab-local`).

| fixture | HEAD commit | command | exit | stdout sha256 | `met_target` | `thin` |
|---|---|---|---|---|---|---|
| `ab-local` (landed 7-col) | `f67b0a7f` | `python3 -I -B tools/round-45/c2-counter.py --root <fx> --freeze f67b0a7f --rev f67b0a7f` | 0 | `a5ebbce7…` | true | 0 |
| `ab-house` (PROTOCOL 8-col) | `1ecb5828` | same shape | **1** | `bec465e2…` | **false** | **6 of 6** |

`ab-house` `failing` = `thin exit-code cells: [all six]`, `unregistered []` — the paths are found, the
exit cells "fail" only because `cells[2]` is now the entry command.

**This is the contradiction the L1 must hold open:** the round's calibration claim is scored on a
registry row that cannot satisfy the protocol's own field list. A lane that "fixes" its registry to
conform turns R45-C2 red; a lane that keeps R45-C2 green must keep the non-conformant shape. The
counter's comment at `:106` names the local header as if it were the schema. (Related but distinct
from the routed items: R45-CL14 is "the counter never validates a header"; this is "the counter's
fixed index makes the header unvalidatable *and* makes conformance a failure"; R45-CL9/A6 is the
loose `\b0\b/\b1\b/\b2\b` cell test; R45-CL8 is suffix/contains lookups.)

## F4 — a row inside the measured frame was false, and the score could not see it

At A1 (`SKILL.md:1637`):

```
| `tools/round-44/c1-run.sh` | probe — the after-freeze data procedure: one REA `extract-firmware`
  run per carrier plus the independent oracle arm | `0` every carrier produced a receipt; … |
```

A3 `f59565b7` rewrites cell 2 to "… each written as a receipt tree; **it does not run the oracle**
(`c1-oracle.py` is the counter's)" and adds `--dry-run` to the `0` arm
(`git log -S "it does not run the oracle" -- SKILL.md` → `f59565b7`). So at A1 that row was
factually wrong about the instrument it registers, while satisfying both C2 clauses exactly —
first cell path-equal, `cells[2]` naming 0/1/2.

Measured: C2 exit 0 at A1 and at A3 with **identical** `registered`/`thin`/`unregistered`
(`receipts/c2-lane-at-a1.json`, `receipts/c2-lane-at-a3.json`). A false registry row and a true one
are indistinguishable to the predicate. The LOG discloses the correction append-only
(`LOG.md:3311-3316`); the Round-45 SCORECARD "after" cell does not mention it.

**Verdict.** `c1-run.sh` row at A1: **falsified** (by the lane's own A3). C2 claim: **holds** as
specified — but the specification is presence-of-a-row, so the calibration axis is credited for an
artefact that was false inside the measured frame (under the SCORECARD header sentence; not under
LOG/SCORECARD's A3 amendment — see F6).

## F5 — 21 of the 45 counted rows come from a table that does not render

`### Round-35/37/38/39 instrument registry` (A1 `:1580`, HEAD `:1596`) opens with the 7-column
header and then **no `|---|---|…` row** — the next line is the first data row. Markdown renders the
header and all 22 rows as one paragraph of pipes; it is not a table to a reader. Census flags it
(`kaidoku:1596 (7 cols) sep:false`) alongside three kumitate tables. The frozen parser does not care
— and the provenance of the counter's own number shows the split (`receipts/row-provenance-at-a1.txt`):

```
total parsed rows: 45
   21  ### Round-35/37/38/39 instrument registry     <- separator-less
    6  ### Round-30 measurement registry
    6  ### Round-44/45 instrument registry
    5  ### Round-31 measurement registry
    5  ### Round-34 run-6 instrument registry …
    2  ### Round-36 instrument registry
Round-40 rows parsed: 0                              <- 12 bare-name rows, all dropped
```

So `registry_rows 45` in every R45-C2 receipt is *not* "45 rows a reader sees as registry rows":
21 of them are in a broken table and 12 real Round-40 rows are invisible. The landed six are all
7 cells with `exits_ok` true — that part holds.

## F6 — the record's measured revision

`SCORECARD.md:3527`'s Round-45 header sentence still reads "measured revision `1f4b27f8`", while two
later append-only amendments supersede it: `:3580-3581` ("the measured revision for the round is
therefore A2") and `:3583-3590` ("**The measured revision for the round is A3**"). `LOG.md:3315` says
the same. Both receipts exist and are identical in content (`c2-at-1f4b27f8.json`, `c2-at-A3.json`).
**Verdict: holds under the lane's append-only supersession**; the un-amended sentence is stale and is
what a reader of the header table alone — and this seat's own brief — repeats.

## Proposed move (bounded, one)

Do **not** rewrite the six rows into house order: `ab-house` shows that costs the C2 score (F3), and
`SKILL.md` is not frozen, so the round-46 counter could then be repaired, but not this round. Instead
append a **house-schema companion table after the landed one**, for the same six paths, with the
`entry command` column present, and pin round 46's counter to resolve the verdict-map cell by header
name. Measured on fixture `ab-both` (`f7c0fc6f`, landed 7-col rows followed by an 8-col table):
exit **0**, `met_target true`, `registry_rows 12`, `thin []`, `unregistered []`
(`receipts/c2-ab-both.stdout`, sha256 `1edf741c…`). First-wins dedupe keeps the landed rows for the
predicate, so the frozen measurement does not move, while the section finally carries every field
`PROTOCOL.md:401-403` requires. Improves calibration and depth (the registry becomes protocol-shaped
and readable), harms nothing measured.

## Risks / second-order effects

1. Any future house-order row for a scope path scores `thin`; the pressure is to keep the
   non-conformant shape, or to smuggle `0`/`1`/`2` into an entry command so the positional test passes
   (`\b0\b/\b1\b/\b2\b` already passes on junk — R45-CL9/A6).
2. First-wins (`by_tool.setdefault`, `:104`) means a house-conformant row appended **above** the six
   flips all six to `thin`; a row appended **below** is invisible. The section's future is
   order-dependent, which makes the round-46 re-freeze (CL14's "explicit registry section bound by
   marker") a breaking change unless `cells[2]` is repaired first.
3. The stale header sentence (F6) is what a falsifier is briefed with; two amendments later, the
   artefact it points at contains a row the lane itself corrected.

## Receipts (`receipts/`, UTC 2026-10-28T16:04:26-34Z, all exit codes as printed)

`manifest.jsonl` (sha256 `acf776cd494be64b3974367869f77fc7e4fe565035385b3019f4aa327aae6d46`)
records command/root/freeze/rev/t0/t1/exit/stdout-sha256 for each run:

| case | exit | stdout sha256 | note |
|---|---|---|---|
| `lane-at-a1` (`--freeze f762b727 --rev 1f4b27f8`) | 0 | `2b401a9ae5a6…` | `registry_rows 45`, `thin []`, `unregistered []`, `frozen_path_changed []` |
| `lane-at-a3` (`--freeze f762b727 --rev f59565b7`) | 0 | `a352f65c098e…` | JSON identical to the lane's `.ufo/waves/round-45/l1/scores/c2-at-A3.json` |
| `ab-local` | 0 | `a5ebbce79d38…` | 7-col landed shape |
| `ab-house` | **1** | `bec465e2e060…` | 8-col house shape, `thin` = all six |
| `ab-both` | 0 | `1edf741c72dd…` | proposed companion table, still green |

Also copied: `fleet-census.json` (sha256 `61f01d50b980…`, 149 tables / 83 eight-column / 12 lanes),
`census.json` (first classifier, sha256 `328c3f9f49bf…`), `measure.py` (the census source, so the
numbers can be recomputed), `row-provenance-at-a1.txt` (sha256 `cc66b21c2f1c…`),
`c2-lane-at-a{1,3}.{json,stdout}`, `c2-ab-{local,house,both}.{json,stdout}`.

Read-only git used: `rev-parse`, `log`, `show`, `grep`, `diff --stat`, `log -S`; no mutating verb, no
lane write, no install. Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W2ConnFormat` removed after the
copy above.

## Not run / unknowns

- `c2-counter.py --selftest` was not run (its tally is not part of this attack; the C1/C2 selftest
  tallies are other seats' claims).
- The preflight (`frozen-path-preflight.py`) was not run; the freeze arm is exercised by the counter
  itself in both lane runs (`frozen_path_changed []`).
- Whether the aggregator/fleet index consumes lane registry rows by cell 0 is not verifiable from this
  repo; `PROTOCOL.md:403` says a fleet index is "pointers to lane rows", so a cell-0 path *and* a
  cell-0 name are both pointer-compatible. Not measured.
- Whether a rendered Markdown viewer actually collapses the separator-less table (F5) was not rendered;
  the claim is structural (no delimiter row), not a screenshot.
