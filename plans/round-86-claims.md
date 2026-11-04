# kaidoku — round 86 claim declaration (frozen before data)

Round 86, attempt 1. Base `2cf0b7ff93c698809bed321f7338276a22d6beb9` (lane tip at round start).
Lane axes: coverage, depth, calibration — all at 10.0 on their finite proxies; calibration is
tied-lowest and is worked here. No stagnation waiver: round 84 entered three capability rows, so
the window restarted and round 85 entered none (1/10).

Two claims, two distinct axes, causally separable: C1 can be measured with C2 unlanded and vice
versa. Neither claim narrows a target after landing; a miss is an honest stop.

Carried in from the round-85 non-author spot-check (`corpus/lessons/round-85-verifier-spotcheck.md`
§8): **R85-2** (missing registry row), **R85-3** (S303 count), **R85-5** (docstring status), **R85-6**
(coverage receipt pointer). This round does not re-declare round 85's missed C1.

---

## R86-C1 — calibration — three records re-derived from the bytes they describe

**Surface (named by surface, not by number):** three record cells that state a value about another
committed object — the SOURCES registry row that supersedes S303, the `mutation-closure.py` module
docstring's sentence about an absent declared case, and the SCORECARD `| coverage |` row's receipt
pointer. The claim moves those cells from "carries the right words" to "re-derives the value".

**Predicate (frozen sentence, repeated verbatim in the counter's atom list and the receipt label):**

> `corpus/SOURCES.md`, `tools/round-84/mutation-closure.py` and `SCORECARD.md` agree with the bytes
> they describe on all three declared atoms (`A1-s303-supersede-count`, `A2-docstring-status`,
> `A3-receipt-pointer`), re-derived by `python3 -I -B tools/round-86/record-agreement.py --root .
> --rev <rev> --json-out <receipt>`, whose `mismatches` list is empty.

**Target:** `mismatches` 3 → 0, `agreed` 0/3 → 3/3, at the measured revision. Before-state receipt:
`.ufo/waves/round-86/pre/c1-at-base.json` (exit 1).

**Atom rules (fixed now; never re-worded after a seat scores):**

- **A1-s303-supersede-count** — the newest row of `corpus/SOURCES.md` whose `teaches` cell opens
  `supersedes S303` must state, after the word `count`, the exact number of OTHER rows whose source
  cell carries `rea-agents-6.5.0.tgz` (S303 and the superseding row excluded), and must then list
  exactly those rows' ids. Base state: no such row exists (S303's own cell says "five scopes" while
  eight rows carry the URL) → mismatch.
- **A2-docstring-status** — exactly one sentence of `tools/round-84/mutation-closure.py`'s module
  docstring names an absent declared case, and it must name the status the code assigns in its
  `not case_present` branch (`survived`); no other status word may appear in that sentence. Base
  state: the docstring says "an absent declared case is inconclusive, never a pass" while the code
  says `survived` → mismatch.
- **A3-receipt-pointer** — the SCORECARD `| coverage |` row's own round R (leading integer of its
  last cell) must be covered by a `.ufo/waves/round-M/l1/scores/*.json` receipt with M ≥ R; that
  receipt must be a blob at `--rev` and carry a 40-hex `rev` field. Base state: the row claims round
  85 and names only a round-67 receipt → mismatch.

**Kill rule:** any atom false at the measured revision kills C1; a `--control substring-only`
receipt that does NOT accept the BASE records also kills it (the control must be a false green — a
rule that can refuse the defective record is not the cheap rule it claims to be); rewriting an atom
rule, its file target or its target count after the wave scored kills it; a mismatch list shrunk by
deleting an atom kills it.

**Counting command (the closure's one command):**

```sh
python3 -I -B tools/round-86/record-agreement.py --root . --rev <40-hex measured revision> --json-out <receipt>
```

**Do-nothing control, scored before the freeze:** `.ufo/waves/round-86/pre/c1-at-base.json` — the
records untouched at BASE give `mismatches` 3, so the target is not reachable without the work.
**Cheap-rule control, scored before the freeze:** `.ufo/waves/round-86/pre/c1-control-substring-at-base.json`
— `--control substring-only` (a record is agreed when the file contains the token it talks about)
reports `mismatches 0` at BASE, i.e. it accepts the defective records; it is therefore rejected as a
counter and retained as the evidence that the target is failable.

---

## R86-C2 — operability — the round-85 gate is registered, and its row re-derives by running it

**Surface:** the `SKILL.md` instrument-registry row for `tools/round-85/predicate-bind.py` — entry
command, verdict map, pinned values, owner. Round 85 landed the gate and left it unregistered, so a
reader of the lane's own checklist cannot find or run it (R85-2).

**Predicate (frozen sentence):**

> `SKILL.md`'s instrument-registry section holds exactly one row for
> `tools/round-85/predicate-bind.py` whose five declared fields re-derive by
> `python3 -I -B tools/round-86/gate-registry.py --root . --rev <rev> --work <scratch> --json-out
> <receipt>` with `mismatches` empty.

**Target:** `agreed` 0/5 → 5/5, `mismatches` empty, at the measured revision. Before-state receipt:
`.ufo/waves/round-86/pre/c2-at-base.json` (exit 1).

**Atom rules (fixed now):**

- **G1-row-present** — the registry section (between `<!-- instrument-registry` and
  `<!-- /instrument-registry -->`) holds exactly one row whose cell 0 is exactly
  `` `tools/round-85/predicate-bind.py` ``.
- **G2-exit-map-observed** — that row's verdict-map cell declares all three exits (`0=`, `1=`,
  `2=`) and the observed `--selftest` exit equals the declared success exit 0.
- **G3-self-invocation** — the row's self-test cell names a `python3` command on that tool path and
  an `exit N`; the command's argv is executed with no shell in `--root` under a four-key child env
  (`PATH`, `HOME`, `TMPDIR`, `LANG`) and its observed exit must equal the declared one.
- **G4-pinned-blob** — the row's pinned-value cell names at least one
  `.ufo/waves/round-<N>/claims.json` that is a blob at `--rev`.
- **G5-owner-round** — the row's owner cell is `kaidoku-r<N>` with the same N as the tool's own
  `tools/round-<N>/` directory.

**Kill rule:** any atom false at the measured revision kills C2; a `--control file-exists` receipt
that does NOT accept the BASE state kills it (the control must be a false green); a row that passes
only by naming a command the tool cannot honour (G3 red) kills it; a row whose declared exit map is
copied without the observed exit agreeing kills it; changing an atom rule after the wave scored
kills it.

**Counting command:**

```sh
python3 -I -B tools/round-86/gate-registry.py --root . --rev <40-hex measured revision> --work <scratch> --json-out <receipt>
```

**Do-nothing control, scored before the freeze:** `.ufo/waves/round-86/pre/c2-at-base.json` —
`agreed` 0/5 at BASE. **Cheap-rule control:** `.ufo/waves/round-86/pre/c2-control-file-exists-at-base.json`
— `--control file-exists` accepts the unregistered state (mismatches 0), rejected as a counter and
retained as failable-target evidence.

---

## Frontier items (§2b, inside the claim cap)

1. **SOURCES curation.** Open S255 (git-show documentation) this round for the C1 knowledge entry;
   add the S303 supersession row required by SOURCES rule 2 (a new row whose `teaches` opens
   `supersedes S303 —`, preserving the old row). Census before/after with
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`.
2. **Mined mistake.** `corpus/lessons/round-86.md` `## Mistakes`: the round-85 correction for S303
   was filed in a lesson while the registry row kept the wrong count — a correction recorded where
   it cannot be re-derived is not a correction.
3. **Sourced claim.** C1's knowledge entry cites the S255 row re-opened this round (access date,
   located ≤25-word quote in the lesson `## Gate`).
4. **Assimilation:** `merge/kaidoku/` is not adopted this round (`Assimilation: none`); the claim
   budget carries the two routed-defect closures. `considerthese/` does not exist in this lane.

## Wave plan

One v1 wave `r86-w1`, 12 seats (policy band 8–16): 3 executor, 2 scribe, 1 scout, 2 reviewer, 1
critic, 1 mutation-tester, 1 sentinel, 1 connector. Attack roles 5/12 = 41.7 % ≥ 25 %; one
connector; the L1 holds the planner seat (disclosed deviation, never a swarm role).

## Do not change

The two counters' atom rules and targets, the two BASE receipts under
`.ufo/waves/round-86/pre/`, the frozen instruments pinned in `.ufo/waves/round-86/claims.json`,
`MANIFEST.json`, the fleet root, and every other lane.
