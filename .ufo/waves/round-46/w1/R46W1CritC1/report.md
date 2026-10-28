# R46W1CritC1 — R46-C1 falsified before data

Seat: `R46W1CritC1` (critic, wave 1). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Read-only on the lane tree; every instrument byte under test came from a byte copy in
scratch (`git cat-file -p <rev>:path`), never from the working tree.

**Verdict: R46-C1 is not met at any declared freeze, and its predicate as frozen is
*satisfiable by a forgery* on five independent axes. A forgery is also not needed at all:
the claim's own `Counting command` exits 2 at every revision after the freeze. R46-C2
scores 38/38 at HEAD but has three escapes of its own. All measured below.**

Measured revision: `c0112995817b4d8caddd86705b08e89bdac99640` (HEAD at measure time).
Instrument bytes measured (sha256 of the exact files loaded):

| file | sha256 |
|---|---|
| `tools/round-46/attest.py` | `c405613170f0581661b9e2afb4bf278da8ac1f936eeb00eb4b456a9e70ad8e5c` |
| `tools/round-46/gate.py` | `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c` |
| `tools/round-46/registry.py` | `5e16e4af69ebf714f0ee48b5a714aa682592f0ce5e32cdeec699b963d3f2da73` |

`SKILL.md` block 23 at that rev pins `sha256:c4056131…e5c`, which **does** equal
`sha256(attest.py bytes at rev)`. Clause 6 is satisfied as written.

## The six assigned attacks

Harness: `receipts.py` in this directory. Every attack replaces only block 23 of the
genuine `SKILL.md` at the measured rev and scores it with the frozen `attest.py`
`--profile v2` plus its full 9-forgery battery. Artefact sha256 and per-attack stdout
sha256 are in `receipts-C1.json`.

Baseline (`GENUINE`): exit 0, `rows 13`, `refs 9`, `battery {9,9,0,1,0}`.

| # | attack | expected if the claim is sound | observed | verdict |
|---|---|---|---|---|
| 1 | every row keeps its id + arm + exit, but all 13 `v1 hole` cells → `lorem ipsum` | red — the block should carry actionable content | **exit 0, `met_target: true`**, battery green | **FAILS** |
| 2 | marker repeated in a later section (`## Config custody…`) | red | exit 1, `marker_occurrences 2 != 1` | holds for a *literal* second marker |
| 2b | second `## Queue-drain craft ` heading *before* the real one, carrying the genuine block; the real sections' block 23 emptied | red | **structural exit 0, 13 rows, 9 refs** | **FAILS (see F5 below)** |
| 3 | pin vs bytes | binds bytes at `--rev` | yes — `pin == sha256(git show rev:attest.py)`; but see **F2/F3**: it does not bind the *executing* file and does not cover `gate.py` | partially holds |
| 4 | every arm cell → `blobberish` | red (not an arm) | **exit 0, `met_target: true`** | **FAILS** |
| 5 | refs → six line-selected citations, all to `corpus/lessons/round-45.md` | red or acceptable-by-design | **exit 0, `met_target: true`**, `cited` set has one file | **FAILS as evidence** (claim does not forbid it) |
| 6 | one row whose cell 0 names all 13 routed ids; 12 filler rows | red — each row should carry one routed defect | **exit 0, `met_target: true`** | **FAILS** |
| 6b | ids only as `R45-CL2x` (prefix of a longer token) | red | exit 0 — `re.finditer(r"R45-CL\d+")` matches the prefix | **FAILS** |
| — | `S142` satisfied by `Source S1420 v9.` | red | **exit 0** — `token in block` is substring test | **FAILS** |

### The cheapest artefact that scores green and is not the intended table

`cheapest-green-block.md` (this directory) — 13 rows, exit 0, all battery counters green:

```
| R45-CL2 R45-CL6 … R45-CL24 | nothing | commit | 1 |
| filler 0 | nothing | commit | 1 |
… 11 more identical filler rows …
  Refs: `corpus/lessons/round-45.md:1-5`, …:10-14, …:20-24, …:30-34, …:40-44, …:50-54
```

It carries exactly one id-bearing row (all thirteen ids concatenated), twelve rows whose
trigger is the word `filler`, one vocabulary token `commit` doing duty as every arm, no
`v1 hole` content, and six citations to one file with arbitrary line ranges. Nothing in it
is a defect class, an arm, or an exit that the table's own prose would recognise. It is
the round-45 forgery — a table of rows that name the vocabulary — with the surface
vocabulary satisfied and no content. **This is the round-45 hole re-opened at a higher
price, not closed.**

## F: additional defects found (beyond the assigned six)

### F1 (HIGH) — the declared freeze makes the claim unreachable

The prompt and the claims file both name freeze `31820472784284727546808acc31b3ea1e73919b`.
`plans/round-46-claims.md` says the freeze "re-derives" as
`git log --format=%H -1 -- plans/round-46-claims.md`; that command returns
`31820472…` correctly. But the frozen set includes `tools/round-46/`, and **three later
commits touch it while the claims file does not change**, so the counter's own freeze arm
refuses every revision after the freeze:

```
python3 -I -B tools/round-46/attest.py --root <lane> \
  --freeze 31820472784284727546808acc31b3ea1e73919b --rev <rev> --no-battery
freeze=31820472 rev=31820472   exit=1  marker_occurrences 0 != 1   (the do-nothing control)
freeze=31820472 rev=50862e4a   exit=2  frozen_path_changed
freeze=31820472 rev=65678df0   exit=2  frozen_path_changed
freeze=31820472 rev=6e018068   exit=2  frozen_path_changed
freeze=31820472 rev=04252247   exit=2  frozen_path_changed
freeze=31820472 rev=781e19ae   exit=2  frozen_path_changed
freeze=31820472 rev=17a72375   exit=2  frozen_path_changed
freeze=31820472 rev=HEAD       exit=2  frozen_path_changed
```

Sweep over all 25 commits in `31820472..HEAD`: **0 greens, 2 exit-1, 23 exit-2**
(`attacks9.json` → `declared_31820472`). `frozen_path_changed` names
`tools/round-46/{attest.py,gate.py,registry.py}` at every post-freeze rev, ``restored``
lists the same three — i.e. the counter reports its own instrument as tampered.

The receipts that *do* score green use a **different** freeze, `0425224756791b414454df28a9abf93dcdf154ce`
(`.ufo/waves/round-46/l1/scores/c1-at-F4.json`, `c2-at-F4.json`). That commit is titled
"round-46 F4" and is **not** the freeze the claims file re-derives; it is a later commit
that itself modifies `tools/round-46/registry.py`. So:

- measured at the declared freeze → exit 2, never `met` (a 2 never counts);
- measured at the receipts' freeze → exit 0, but that freeze post-dates the artefact and
  was chosen after the fact, and it is not what `plans/round-46-claims.md@31820472` says.

Sweep at `04252247`: 8 of 25 revs green, including `04252247`, `1e32827b`, `deee6595`,
`47b5e265`, `3ffbe0f8`. The green set is "every commit from F4 onward", i.e. the counter is
green for revisions *after* the instrument it is supposed to guard was last modified —
which is the freeze-integrity inversion the claim exists to prevent.

**Primitive defect:** a directory freeze plus a post-freeze instrument edit makes the
freeze arm fire on the artefact's own tooling, so the claim can only be scored against a
freeze that is not the declared one. The claims file's own words ("Nothing in this file or
in `tools/round-46/` changes after the freeze: a change makes both counters exit 2") are
**honoured by the counter and violated by the lane**: the change happened, so the honest
score is exit 2.

**At the measured rev this is now total.** Even the receipts' freeze is dead at HEAD,
because `332f4884` (F5) edited `attest.py` and `gate.py` after it:

```
$ python3 -I -B tools/round-46/attest.py --root <lane> --freeze 31820472… --rev c0112995… --no-battery
rc=2  frozen_path_changed ['tools/round-46/', '…/attest.py', '…/gate.py', '…/registry.py']
$ python3 -I -B tools/round-46/attest.py --root <lane> --freeze 04252247… --rev c0112995… --no-battery
rc=2  frozen_path_changed ['tools/round-46/', '…/attest.py', '…/gate.py']
```

**No freeze in the lane now scores R46-C1 green at HEAD** (`g-final-*.out`). The claim's
`Counting command` cannot produce a `met_target` for any `<FREEZE>` the round has declared.
This is not a documentation slip: it is the predicate's own freeze-integrity rule applied
honestly to the lane's history.

### F2 (CRITICAL) — the pin binds committed bytes, not the executing file

`attest.py` computes `want = sha256(files(spec["pin"]))` (line 241–247), always through
`git show <rev>:path`. The counter *executes* from the worktree. A patched copy placed
outside the root and pointed at a genuine repo scores green:

```
$ python3 -I -B /scratch/elsewhere-tools/attest.py --root <lane> \
    --freeze 04252247… --rev c0112995… --no-battery
exit=0   met_target=true    ← patched copy: every clause short-circuits to met
$ python3 -I -B <lane>/tools/round-46/attest.py … (same args)
exit=2   frozen_path_changed          ← only because HEAD moved after F5
```

And on a committed do-nothing artefact (`attacks9.json`):

| instrument | fixture | exit | met |
|---|---|---|---|
| honest pinned `attest.py` | do-nothing `SKILL.md` | **1** | false |
| patched `attest.py` (elsewhere) | do-nothing `SKILL.md` | **0** | **true** |

The patched file's own sha256 is `3bf010c3…eab7` while the block pins `c4056131…e5c`; the
pin is never consulted in that run because the patched copy returns before the pin clause.
So `sha256:<64 hex>` identifies bytes that were *read*, not bytes that *ran*. F5 (below)
closes the uncommitted-worktree case (`frozen_worktree_dirty`); it does not close the
"run a different file" case, because nothing binds `sys.argv[0]` to the pinned path.

Worse, when the forged tool is committed into the fixture repo and the block's pin is
recomputed to the forged tool's own hash, the counter reads its pin *from the same commit
it is scoring* — the pin is then self-referential, and case 2/3 of `attacks10.json` both
score `exit 0, met true` with `pin`/`pin_expected` absent from the receipt:

```
2 patched+recomputed pin: exit 0, met true, newpin 3bf010c3…, realpin c4056131…
3 patched+stale pin     : exit 0, met true
```

### F3 (HIGH) — the pin covers `attest.py` only; `gate.py` decides the freeze verdict

`gate.freeze_state` is the only thing that produces `frozen_path_changed`. It is not
pinned. A fixture with an honest `attest.py` and a `gate.py` whose
`if receipt["frozen_path_changed"]:` guard is neutralised scores:

```
tamper a frozen path (append to tools/round-46/attest.py, commit):
  honest gate   exit 2  reason frozen_path_changed  fpc ['tools/round-46/','tools/round-46/attest.py']
  patched gate  exit 1  reason None                 fpc []
```

An exit 1 is a *scored* not-met; the tampered run presents itself as an ordinary failure
rather than the exit-2 refusal the claim promises, and the tamper is invisible in the
receipt (`frozen_path_changed: []`). `gate.py` sha256 changes from `c3ba6b93…` to
`59efee7a…` with no pin anywhere in `SKILL.md`.

### F4 (MEDIUM) — the refs floor is enforced by a side effect, with the wrong diagnostic

Clause 5 of the claim requires **six citations carrying a line selector**, and the counter's
own bound is `refs >= 6` where `refs` also counts the pinned interpreter path (which is
exempt from a selector). So five citations + the pin satisfies the counter's clause 5 at
`refs 6`, while the claim's prose asks for six citations. Measured on
`A6b_five_refs_plus_pin`: structural exit **0**, `refs 6` — and the run then exits **1**
with `battery v1_green 1 != 9`.

The mechanism is not the mutation but the v1 port's own regex: with `hard=False`,
`refs_in` uses `LOOSE_REF`, which matches only `corpus/(knowledge|lessons)|plans/*.md`
and therefore **cannot see `tools/round-46/attest.py`**. v1 then counts 5 refs against
`refs_min 6` and marks every fixture red for `refs 5 < 6` — including the ones whose real
defect the v1 set is supposed to accept. So:

- the artefact must carry **six citations plus the pin (`refs 7`)** to keep `v1_green == 9`;
- when it does not, the counter blames `battery v1_green`, naming a battery counter for a
  refs-floor defect — the diagnostic points at the wrong clause;
- `refs >= 6` in the receipt is therefore not the operative bound, and the claim's own
  clause 5 text ("at least six citations") is not what the clause computes.

I did not call this a forgery: it is a calibration defect in which the number the receipt
prints (`refs`) is not the number the predicate enforces.

Also: from the landed battery receipt (`c1-at-A3.json`), the nine forgeries are all red —
but `garbage-rows` is caught by `routed ids not named` **and** `arm cells outside the
vocabulary`, and `thin-rows` by `rows 8 < 13` plus missing ids. No fixture is red because a
row's *content* is not a defect: the content test does not exist. That is the same gap as
attack 1.

### F5 (LOW, already fixed at HEAD) — `craft_section` reads the first heading

`craft_section` splits on the **first** `## Queue-drain craft `, so a decoy craft heading
placed above the real one makes the real section unread. Measured: a forged `SKILL.md`
whose decoy section carries the genuine block and whose real craft section holds
`- **23. removed.** nothing` scores **structural exit 0, 13 rows, 9 refs**
(`attest.py:88`). Full battery run: `forgeries_total 9, v1_green 0` → exit 1, so the
battery happens to catch it today (`v1_green` mismatch), not the structural clauses. A
decoy that preserved the refs count would go green. Forged sha256
`8f35c111368a0e4909525d5a4c3bcb13885e5b6b7f59f2a18de3cbf2460de8d7`.

### F6 (LOW) — vacuous `v2_crash == 0`

`v2_crash` counts `c2 == 2` over the nine fixtures. Because `score()` returns 1 for any
failing clause and only 2 for a malformed heading or a freeze refusal, and the fixtures
share the genuine heading, `v2_crash` is 0 by construction. It is a counter that cannot
fail; report it as such or drop it.

## R46-C2 — two escapes

Registry baseline at the measured rev: exit 0, 38 registered, `unregistered []`,
`thin []`, `absent_at_rev []`. Census independently re-derived with
`census.py --rev c0112995…`: 38 paths, **set-equal** to the committed
`tools/round-46/census.json` (`census-regen.json`). Clause 3 and clause 5 hold.

- **G1 (HIGH) — columns 3–6 are never validated.** Replacing the `self-test command`,
  `pinned-value path`, `write scope` and `owner` cells of all 38 rows with `` `false` ``,
  `sha256:000…0`, `/`, `nobody` scores **exit 0**. `registry.py` reads cell 0 (exact), cell 2
  (verdict map) and nothing else. A registry that names a self-test command it never runs
  and a pinned-value path that does not exist passes the schema that advertises both.
- **G2 (HIGH) — the verdict map validates keys, not values.** All 38 rows set to
  `0=unknown, 1=unknown, 2=unknown` scores **exit 0** (`EXITMAP.findall` at
  `registry.py:196` only checks the key set is `{0,1,2}`). The claim's own words
  ("a cell that merely mentions the digits is thin") are met literally and violated in
  substance.
- **H2 (CRITICAL) — the census is trusted, and shrinking it shrinks the claim.** Scoring
  with a census file containing only the six round-44/45 paths gives **exit 0** with 6
  registered: the 32 missing instruments simply leave the scope. `registry.py:126` reads
  `files(spec["census"])` and never re-derives it, so the guard against "the record drifted
  from the instrument" is itself a record the subject can rewrite. There is no pin on
  `census.json` (unlike `attest.py`), and `census.json` lives under the frozen
  `tools/round-46/` only for *committed* bytes — the same F2/F3 gap applies.
  Truth: the census is a *derived* document (`census.py` is deterministic and the
  regeneration is set-equal); the counter must re-derive rather than trust, or pin it.

## Impacted axes

- **depth (C1)** — the claim cannot land as stated. `failing == []` is reachable only
  against a non-declared freeze (F1), and the artefact class it certifies is satisfiable by
  the cheapest table (attacks 1, 4, 6, 6b, S142). The depth proxy would score a table that
  carries no depth.
- **calibration (C2)** — G1/G2/H2 mean the registry's self-assessment is still
  unvalidated in exactly the way the axis measures: the rows assert a self-test command and
  a pinned value that nothing executes.

## Smallest safe corrections

1. **F1**: make the freeze commit the one the counter can actually score — i.e. the freeze
   must be the last commit that touches `tools/round-46/`, and the claims file must
   re-derive *that*. Concretely: replace the declared freeze with
   `0425224756791b414454df28a9abf93dcdf154ce` (or later) in
   `plans/round-46-claims.md`, or restate the freeze as
   `git log --format=%H -1 -- tools/round-46/ plans/round-46-claims.md` and prove the two
   agree at freeze time. Keep the "0 greens at the declared freeze" sweep as a control.
2. **F2**: bind execution to the pin. Before scoring, assert
   `sha256(open(__file__,'rb').read()) == <pin read from the block>` and refuse (exit 2)
   otherwise; and require the pin to resolve at a rev **strictly before** the measured one.
3. **F3**: extend the pin to `gate.py` (a second `sha256:` in the block, or one pin over
   the concatenation), because `freeze_state` is the verdict's only authority.
4. **Attacks 1/4/6/6b/S142**: make each row's cells *typed*: the `trigger` cell must match
   `^R45-CL\d+\b` and carry exactly one id (drop the whole-cell sweep), the `v2 arm` cell
   must equal one vocabulary token exactly (not `in`), `S142` must match `\bS142\b`, and the
   `v1 hole` cell must be non-trivial (≥ N words, no `lorem|ipsum|nothing|filler`). Add the
   cheapest-green artefact above as a tenth forgery class so the battery proves it red.
5. **F5**: `craft_section` should take the **last** craft heading, or reject a document
   with two `## Queue-drain craft ` headings (exit 2, ambiguous heading).
6. **C2 G1/G2**: validate cell 3 by *running* it (or at least requiring it to name a path
   that exists at `--rev` and is executable), cell 4 by resolving the pinned path, and cell
   2 by a value grammar (`0=<word>[,;]\s*1=<word>` …), not a key set.
7. **C2 H2**: re-derive the census from `census.py` at score time and require set equality
   with the committed file; a mismatch is `census_drift` exit 2.

## Honest limits of this seat

- Not run: `attest.py --selftest`, `registry.py --selftest` (out of scope for a read-only
  falsification seat; the claims file asserts `cases=15`/`cases=11`, which I did not
  verify).
- Not run: the freeze arm's merge-commit behaviour on a real merge (`R45-CL6`); all
  fixtures were single-commit histories.
- The patch I used to demonstrate F2/F3 is a synthetic one-line short-circuit; it proves
  the *guard is absent*, not that any real patch was attempted. No lane file was modified.
- No installs. Nothing was written outside `.ufo/waves/round-46/w1/R46W1CritC1/` and
  scratch.

## Receipts

All under `.ufo/waves/round-46/w1/R46W1CritC1/`:

| file | content |
|---|---|
| `receipts-C1.json` | the six attacks + GENUINE, each with command, exit, stdout sha256, UTC, artefact sha256 |
| `cheapest-green-block.md` | the cheapest artefact that scores green and is not the intended table |
| `attacks.json` … `attacks10.json` | per-round raw measurements (freeze sweeps, pin circularity, census tamper) |
| `freeze-matrix.json` | 25-revision × 2-freeze admissibility sweep |
| `matrix-round-46.json` | the six-attack matrix re-run on the newest frozen bytes |
| `census-regen.json` | independently re-derived census (set-equal to the committed copy) |
| `receipts.py`, `matrix.py`, `attack9.py` | the harnesses |
| `g-*.json`, `g-*.out` | the exact counting commands at each freeze/rev pair, with stdout |
| `measured-rev.txt` | the revision all of the above was measured at |

Scratch `/fast/scratch/hyaku/kaidoku-r46/R46W1CritC1` was removed after these files were
copied here.
