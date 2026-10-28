# ScribeBlock24 — craft block 24 prose, and the frozen C1 byte measured

Lane `kaidoku`, round 47, wave 1. Seat: `ScribeBlock24` (leaf, no subagents).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Prompt freeze `5017e1f7299c3a812e87e7950148f54313dd279e` (base `13a9e9e1`).
**The lane advanced while I worked**: the freeze is now a series and the landing already
exists. Every value below names the revision it was measured at; nothing here is a claim
about "the tip", which moved from `3186f69b` to `a631bba0` (nine commits) during the seat.

| rev | subject |
|---|---|
| `5017e1f7` | freeze: `plans/round-47-claims.md` + `tools/round-47/` (exact.py `dcef54f1…`, record.py `af666ce2…`) |
| `3186f69b` | wave-1 spec, dispatch and freeze controls |
| `9018c53b` | **A1** — drop the unreachable window-pair clause (claims +12, record.py) |
| `e856beb5` | **land craft block 24**, record corrections, axis heads, S143 |
| `62e33f7d` | **A2** — window forgery made real; block 24 arm cells carry only the token (claims +9) |
| `2e4ae434` | **A3** — historical seats/window correction (record.py only) |
| `1e2c3102` | **A4** — historical-correction selftest fixture (record.py only) |
| `caafeffa` | record: round section, LOG, lesson, QUALITY 78, S144, both counters' receipts |
| `07d2894e` | **A5** — the ghost-atom forgery lands inside the corrections section |
| `a631bba0` | A5 in the record, the LOG and the lesson; both claims' A5 receipts |

`exact.py` at `a631bba0` is still the freeze byte
`dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`; `record.py` is not
(`af666ce2…` → `abf3525…`).

---

## 1. Deliverable — the block 24 prose

Three artefacts, all in this directory:

| file | what it is | frozen-counter verdict |
|---|---|---|
| `block24.md` | my canonical draft: lead sentence, four-row table, five line-selected refs **including a `corpus/knowledge/` entry** (QUALITY row 77(a)), both pins | **exit 1** as frozen — clause 9 (`battery genuine_green 0`, `v2_green 0`); passes once `_fixture_files` carries the knowledge path (finding **F2**) |
| `block24-passing.md` | the same prose minus the knowledge ref | **exit 0, `failing []`** (`F-P.json`) |
| `landed-block24.md` | the block as landed at `a631bba0`, for diffing | exit 0 at `freeze == rev` (`c1-at-A5.json`); exit 2 at the claims-derived freeze (`F-lane-declared-freeze.json`) |

Values used, all computed, none guessed:

- `interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`
  — `sha256(git show 5017e1f7:tools/round-47/exact.py)`, identical in the worktree and at
  `a631bba0`.
- `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112`
  — `sha256("\n".join(names))` over `exact.MUTATIONS` in order
  (`substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift`),
  cross-checked against the module constant `exact.MUT_DIGEST`.

The lead sentence (`block24.md`), which is what block 23 left as substrings, counts and
conventions:

> Block 23 stated the four routed defect classes and left every check loose in exactly the
> way its own row described: the arm cell passed when a vocabulary token was a **substring**
> of it, so `blobberish` read as `blob`; a routed id passed when it appeared in **some** row,
> so two rows could claim one group while a third group was named by none; `forgeries_total`
> was compared against a **count** the mutation list itself computed, so erasing a mutation
> erased one required failure; and the one flag order that makes the history arm see a
> merge's own resolution was a **convention** in `gate.py` (the history arm's `-m` arm)
> rather than a clause anyone read.

The four rows, in the frozen house shape (`trigger | v2 hole | v3 arm | exit`), arm cells
carrying **only** the token:

| trigger | v2 hole | v3 arm | exit |
| --- | --- | --- | --- |
| R46-CL2 an arm cell reads `blobberish` for `blob` | containment: `token in cell.lower()` passes every superstring of the token | `symbol` | 1 |
| R46-CL3 two rows claim one routed group and a third group is named by none | at-least-once: an id passes if any row carries it, and duplicate rows are never counted | `once` | 1 |
| R46-CL4 one mutation is deleted from the list the claim is judged on | the list is counted, never pinned, so the denominator is the author's to shrink | `digest` | 1 |
| R46-CL6 one flag reorder (`--diff-merges=first-parent -m`) prints a merge twice | the argument order is a code convention no clause reads | `order` | 1 |

All four exits are `1` because each defect, when present, lands in `failing[]` and the
counter returns 1; `2` is reserved for could-not-evaluate (unparseable block, dirty frozen
path, unknown rev) and no row of this matrix is that. Verified per forgery in `F-P.json`:
`v2_exit 0 / v3_exit 1` for all four.

Citation line of `block24.md` (five refs, four line-selected inside the validated set, plus
the interpreter by its own sha pin):

`corpus/lessons/round-46.md:57-67`, `corpus/lessons/round-46.md:20-21`,
`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:56-60`,
`plans/round-47-claims.md:89-110`, `tools/round-47/exact.py` (pin only).

Every range was checked against the byte at the revision named:
`git show <rev>:<path> | wc -l` → round-46 lessons 102, that knowledge entry 79,
claims 211, gate.py 247, exact.py 561. `block24-passing.md` drops the knowledge ref and
keeps the other four.

**`tools/round-46/gate.py` may not be named by path in the block** — see **F4**.

---

## 2. Receipts

All commands run with `TMPDIR=$HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/ScribeBlock24`;
stdout captured verbatim, `sha256sum` of that stdout recorded. `MANIFEST.json` in
`receipts/` carries the same table.

| receipt | exit | stdout sha256 | UTC |
|---|---|---|---|
| `A0-canonical-draft-battery.json` — my canonical draft, fixture `fx-genuine.dp0RyI` | 1 | `01edd54e505161d0…` | 17:54:31Z |
| `A-genuine.json` — same, rebuilt at `1e2c3102`, fixture `fx-genuine.3xWCCc` | 1 | `f0e3f4782913778f…` | 17:55:05Z |
| `P-passing-draft.json` — landable draft, fixture `fx-passing.dt9Ug5` | 0 | `ad530474bc6b2bda…` | 17:55:38Z |
| `B-selfamend.json` — clause 5 weakened only | 1 | `afd6334efe19bbf3…` | 17:55:05Z |
| `B2-selfamend-forgery.json` — clause 5 weakened + `substring-arm` no-op + claims paragraph, `freeze == rev` | **0** | `fe547fa959336f8e…` | 17:55:38Z |
| `F-P.json` — landable draft at `a631bba0`, fixture `fx-passing2.1uo1QZ` | 0 | `486371465fadcbb0…` | 17:57:09Z |
| `F-B.json` — self-amending forgery at `a631bba0`, fixture `fx-selfamend3.rl4htV` | **0** | `2c9f1cc9b8298b8e…` | 17:57:09Z |
| `F-lane-declared-freeze.json` — lane, `--freeze 62e33f7d --rev a631bba0` | **2** | `bdb58e730c762199…` | 17:57:09Z |
| `c1-freeze-state-now.json` — lane, `--freeze 5017e1f7 --rev 3186f69b` (pre-landing baseline) | 1 | `01078be64033e0fd…` | 17:53Z |
| `c1-origfreeze-HEAD.json` — lane, `--freeze 5017e1f7 --rev e856beb5` | 2 | `1071e5e715881b8e…` | 17:54Z |
| `c1-amendedfreeze-HEAD.json` — lane, `--freeze 9018c53b --rev e856beb5` | 1 | `26fade635682f39a…` | 17:54:1XZ |
| `c1-at-head-2e4ae434.json` — lane, `--freeze 62e33f7d --rev 62e33f7d` | 0 | `d220eacf6418a23b…` | 17:53:02Z |
| `c1-head-vs-A2freeze.json` — lane, `--freeze 62e33f7d --rev 1e2c3102` | 2 | `98a15294e14bb034…` | 17:53:3XZ |
| `C2-landing-caafeffa.json` — `record.py --rev caafeffa` | 1 | `a38b09df81ed679a…` | 17:56:03Z |
| `C2-rerun.json` — `record.py --rev 07d2894e` | 0 | `d366b080e0112a57…` | 17:56:41Z |

The counting commands are the claims file's own:

```sh
python3 -I -B tools/round-47/exact.py --root <root> --freeze <FREEZE> --rev <REV>
python3 -I -B tools/round-47/record.py --root <root> --rev <REV>
```

No `--json-out` was used: `gate.out_path` refuses any target outside the lane root, and a
lane-internal write is out of my scope. Thresholds were read from the receipts verbatim.

---

## 3. Findings

### F1 (HIGH, live) — the freeze is derived from the file it freezes, so one commit that touches both re-blesses any change

`plans/round-47-claims.md` defines the freeze as `git log --format=%H -1 --
plans/round-47-claims.md`. Any commit that edits a frozen tool **and** appends a paragraph to
the claims file therefore moves the freeze past itself, and `gate.freeze_state` compares
`freeze..rev` — an empty range — so `frozen_path_changed` is `[]` while the frozen bytes were
rewritten in the same commit. The claims file's own sentence ("Nothing in this file or in
`tools/round-47/` changes after the freeze: a change makes both counters exit 2
`frozen_path_changed`") is false for the first freeze: `5017e1f7..a631bba0` is
`plans/round-47-claims.md 21+0` and `tools/round-47/record.py 21+10`.

Two independent demonstrations:

1. **On the lane.** `--freeze 5017e1f7 --rev e856beb5` → exit 2
   `frozen_path_changed ["plans/round-47-claims.md", "tools/round-47/", "tools/round-47/record.py"]`
   (`c1-origfreeze-HEAD.json`). Every green receipt in `.ufo/waves/round-47/l1/scores/` uses
   `freeze == rev` (`c1-at-A2`, `c1-at-A4`, `c1-at-A5`) or a freeze later than the declared
   one (`c1-at-R1`: `freeze 1e2c3102`, `rev caafeffa`). **No receipt uses the
   claims-derived freeze against a later rev.**
2. **Constructed.** Fixture `fx-selfamend3.rl4htV` (in scratch while the seat ran; recipe
   below), one commit = weakened clause 5 + `substring-arm` body replaced by
   `return block, {}` + a claims-file paragraph + the block's pin recomputed. Command:

   ```
   python3 -I -B <fixture>/tools/round-47/exact.py --root <fixture> \
     --freeze <that commit> --rev <that commit>
   ```

   → **exit 0, `met_target true, failing []`, `frozen_path_changed []`**, with
   `arm_tokens ['order-ish','once','digest','order']` (`F-B.json`, `B2-selfamend-forgery.json`).
   A block whose arm cell is `order-ish` is red under the frozen clause 5
   (`c1-at-L1.json`: "arm cells not exact vocabulary tokens") and green here.

The same construction with **only** clause 5 weakened is still caught — `v3_green 1 != 0`
(`B-selfamend.json`) — so clause 9 is what kills a lazy self-amendment; it does not kill one
that also degrades a mutation (F3).

Repair options, in increasing strength: (a) record the first freeze as a literal hex in the
claims file and require `--freeze` to equal it; (b) derive the freeze from the *base* commit
the claims file names and require `git log -1 -- tools/round-47/exact.py` to be an ancestor
of it; (c) exclude the claims file from the frozen set and pin the freeze as a value the
frozen tools carry.

### F2 (HIGH, live) — clause 9's fixture file set omits `corpus/knowledge/`, so the citation QUALITY 77(a) requires is the one that makes the battery red

`exact.py::_fixture_files` builds every battery repo from exactly

```python
{"SKILL.md", CLAIMS, SELF, GATE46, MUST_CITE, "corpus/lessons/round-45.md"}
```

There is no `corpus/knowledge/` member, so a block that cites a knowledge entry — which
`corpus/QUALITY.md:139` (row 77(a), mined from M46-4) makes mandatory for a new craft block,
because the depth proxy counts only `corpus/knowledge/` citations inside
`## Queue-drain craft` blocks — makes `check_refs` return `absent at rev` inside every
battery repo. Consequence: `genuine_green 0` and `v2_green 0` → clause 9 red.

Measured on the same prose, same bytes otherwise:

| block | knownledge ref | counter |
|---|---|---|
| `block24.md` (canonical) | 1 | exit 1 — `battery v2_green 0 != 4`, `genuine_green 0 != 1` (`A-genuine.json`, `A0-…`) |
| `block24-passing.md` | 0 | exit 0 — `v2_green 4`, `v3_green 0`, `genuine_green 1`, `crash 0` (`F-P.json`) |

So **R47-C1 as frozen is satisfiable only by a block that violates QUALITY row 77(a)**, and
the landed block does exactly that: `grep -c 'corpus/knowledge/'` over
`landed-block24.md` = **0**. That is M46-4 (`proxy-harm-recurrence`) one round later, this
time forced by the instrument instead of by inattention. Repair: add the cited knowledge path
(or the whole `corpus/knowledge/` glob) to `_fixture_files`.

### F3 (MEDIUM, live) — a no-op mutation is counted as a scored `v2_green` forgery, and `fixtures[].error` is never asserted

`run_battery`:

```python
if text == block and not overrides:
    out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
    out["forgeries_total"] += 1
    out["v2_green"] += 1
    continue
```

Clause 9 checks `forgeries_total == 4`, `v2_green == 4`, `v3_green == 0`, `genuine_green == 1`,
`crash == 0` and never looks at `error`. A mutation degraded to `return block, {}` therefore
scores green on both sides of the comparison, and `mutations_sha256` (names only, in order)
does not move. `F-B.json` / `B2-selfamend-forgery.json` show
`fixtures[0] = {"substring-arm": "mutation was a no-op"}` with `v2_green 4, v3_green 0` and the
counter at exit 0. Repair: `crash += 1 if fixtures[].error` and/or a `noop == 0` clause — the
digest cannot cover bodies, so the battery is the only body test and it currently accepts a
non-mutation.

### F4 (MEDIUM) — clause 8's path set excludes `tools/round-46/`, so the block cannot cite the file clause 7 measures

`ALLOW = ("corpus/lessons/", "corpus/knowledge/", "plans/", "tools/round-47/")`. Writing
`tools/round-46/gate.py` anywhere in the block yields
`unresolved or unvalidated citations: 2` with detail
`tools/round-46/gate.py: outside the validated path set` (my first fixture run,
`A0-canonical-draft-battery.json` era). The landed block dodges this by writing the bare
token `gate.py`, which the path regex does not match and therefore never resolves — a reader
cannot follow it, and no clause notices. Either admit `tools/round-46/` to `ALLOW` or require
the bare name explicitly in the claim.

### F5 (MEDIUM, closed while I measured) — the ghost-atom forgery was green at `caafeffa`

`python3 -I -B tools/round-47/record.py --root <lane> --rev caafeffa` → exit 1,
`battery forgeries_green 1`, fixture `correction-ghost-atom` **exit 0**
(`C2-landing-caafeffa.json`), independently reproducing the L1's own `c2-at-R1.json`. Cause:
the forged `- corrects path does/not/exist/…` line was appended at the end of the document,
outside `## Record corrections — round 47`, and `corrections()` only parses the section body,
so the forgery was a silent no-op. Closed by **A5** `07d2894e` (insertion after the heading);
re-measured at `07d2894e`: exit 0, `forgeries_green 0`, all three fixtures exit 1
(`C2-rerun.json`). Recorded because the round's record commit `caafeffa` shipped a *red* C2
receipt as the landing evidence.

### F6 (LOW, closed) — the block landed at `e856beb5` failed clause 5

`--freeze 9018c53b --rev e856beb5` → exit 1, `arm_tokens` were the four prose cells
(`symbol: the arm cell must equal one token…`), i.e. the landing violated the very clause it
documents (`c1-amendedfreeze-HEAD.json`). Fixed at **A2** `62e33f7d` (cells carry the bare
token); green at `freeze == rev == 62e33f7d` (`c1-at-head-2e4ae434.json`).

### F7 (LOW, live) — claims-file citations are rev-relative and clause 8 only checks bounds

Line-number citations into `plans/round-47-claims.md` shift with every amendment, and
`check_refs` validates `1 <= start <= end <= line_count` only. The landed block cites
`plans/round-47-claims.md:45-113` as "the R47-C1 predicate and its nine clauses" — at
`a631bba0` line 45 is inside *Causal separability* and the predicate is 89–110 — and
`:141-176` as "the R47-C2 predicate and its result", where the C2 `**Target.**` line is 182,
**outside** the cited range. Both resolve and both mislabel: R45-CL9's class ("a citation
resolves but names nothing about the defect"), which the round's own kill rule claims to
close. Either cite section headings by name instead of line, or have the counter assert the
cited range contains the heading the label names.

### F8 (INFO) — the landed block carries no knowledge citation

`grep -c 'corpus/knowledge/' landed-block24.md` → `0`, against `corpus/QUALITY.md:139`
row 77(a). This is not a counter clause (`ALLOW` permits knowledge, nothing requires it), so
the block is green on C1 and still costs the depth proxy. See F2 for why the two cannot both
hold today.

---

## 4. Lane state, measured

- **Declared-freeze verdict at the last revision I read** (`a631bba0`), freeze
  `62e33f7d` (the claims-file re-derivation): **exit 2, `frozen_path_changed
  ["tools/round-47/", "tools/round-47/record.py"]`** (`F-lane-declared-freeze.json`).
  A3, A4, A5 and the A5 record all edited `record.py` after A2 without touching the claims
  file, so the freeze did not advance with them. Both counters are therefore unmeasurable at
  the tip under the claim's own definition, while every published receipt is green because it
  was run with `freeze == rev`.
- **Block 24 at the tip is green** when measured the way the receipts measure it:
  `c1-at-A5.json` (`freeze == rev == 07d2894e`): `met_target true`, battery 4/4/0/1/0.
- **C1 is byte-stable**: `exact.py` = `dcef54f1…` at the freeze and at `a631bba0`, so the
  interpreter pin in `block24.md` and in the landed block is still correct.
- `tools/round-47/__pycache__/` exists in the worktree and is **ignored**, so `gate.dirty()`
  (no `--ignored`) does not see it; it is not a freeze violation. Recorded because it is
  untracked material inside a frozen directory.

---

## 5. Incident — I wrote the fleet repo's local git identity, and restored it

An early fixture helper called `mktemp -d -p $S fx-genuine` with no `X` characters; `mktemp`
failed, returned an empty path, and the next `git -C "" … init/config` calls executed in the
process cwd — the fleet root `/home/vgpnk/Projects/shokunin`. Effect:
`.git/config` gained

```
[user]
	email = fx@round47
	name = round47 fixture
```

overwriting whatever the fleet repo used. Restoration, immediately, same shell session:
`git config --local user.name kengaku-shokunin` and
`user.email kengaku@shokunin.local` (the identity the fleet repo's own commits carry:
`git log -1 --format='%an <%ae>'` → `kengaku-shokunin <kengaku@shokunin.local>`), after which
the section reads

```
[user]
	email = kengaku@shokunin.local
	name = kengaku-shokunin
```

No fleet tracked file was created or modified (`git status --porcelain` at the fleet root
shows only the pre-existing `.scratch/`/`.ufo/` entries). Key order inside `[user]` is not
recoverable and has no behavioural effect. All later fixtures use
`mktemp -d -p $S <tag>.XXXXXX`, assert the path is a non-empty directory under `$S`, and
assert `git -C <fixture> rev-parse --show-toplevel` equals the fixture before any commit.

---

## 6. Not run, and limits

- No write to `SKILL.md`, `plans/`, `tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`, or the
  fleet repo; no git mutation outside my scratch fixtures; no commit, stage, stash.
- I did not run `record.py --selftest` or `exact.py --selftest`; the selftest is a claim
  about the counter's own red cases, and my evidence is the four battery fixtures and the
  self-amendment fixture instead.
- The `frozen_path_changed` receipts at `e856beb5`/`3186f69b` were taken **before** the
  freeze series moved; they are history, not the current verdict.
- `C2-landing-caafeffa.json` was produced from the worktree copy of `record.py` at
  `17:56:03Z`; I captured neither its sha nor `git status` at that instant, and the worktree
  was seen dirty under `tools/round-47/` at other moments of this seat. The *value* it
  reports is corroborated by the L1's own `c2-at-R1.json` (same exit, same fixture), and the
  cause is confirmed by reading `corrections()`; the run itself is not pinned to a blob.
  `C2-rerun.json` **is** pinned: `record.py` worktree sha `abf3525…` == `HEAD` blob, clean.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r47/ScribeBlock24` (fixtures `fx-genuine.*`,
  `fx-passing*`, `fx-selfamend*`) is removed after the receipts above were copied here; the
  fixture recipes are in F1 and in §1 and are reproducible from `a631bba0` in one `git init`
  plus two commits.
- No installs, no package manager, no `~/.local/bin` write. Tooling: `/usr/lib/python3.14`
  (`python3 -I -B`) and `git` already present.

---

## 7. Artifacts

```
.ufo/waves/round-47/w1/ScribeBlock24.md              this report
.ufo/waves/round-47/w1/ScribeBlock24/block24.md      canonical draft (5 refs, knowledge cited) — red as frozen, F2
.ufo/waves/round-47/w1/ScribeBlock24/block24-passing.md  landable draft — exit 0, failing []
.ufo/waves/round-47/w1/ScribeBlock24/landed-block24.md   the block as landed at a631bba0
.ufo/waves/round-47/w1/ScribeBlock24/receipts/MANIFEST.json
.ufo/waves/round-47/w1/ScribeBlock24/receipts/*.json    15 counter stdout captures
.ufo/waves/round-47/w1/ScribeBlock24/receipts/*.err     stderr of the fixture runs (all empty)
```
