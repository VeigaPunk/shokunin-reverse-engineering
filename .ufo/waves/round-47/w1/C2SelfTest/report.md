# C2SelfTest — audit of `tools/round-47/record.py --selftest` and its battery

Round 47, lane `kaidoku`, wave 1. Seat **C2SelfTest** (leaf; no dispatch). Read-only on the lane; every mutation ran on a scratch copy.

| item | value |
|---|---|
| ticket freeze | `5017e1f7299c3a812e87e7950148f54313dd279e` |
| claims file's own re-derived freeze (`git log -1 -- plans/round-47-claims.md`) | `62e33f7dd75c8e3285967b26419842c106f6c965` |
| audited bytes | `tools/round-47/record.py` @ `1e2c3102` = sha256 `c704c3d4…`; re-checked @ `07d2894e` = `abf35257…` |
| lane tip at final capture (17:59:41Z) | `31b092d17e77f5064c919383a9bc1e6cbfd2d1ff` |
| installs | none |

The lane moved while this seat measured it: `A1`…`A6` landed between 14:50 and 14:59 local (17:50–17:59Z), each changing `tools/round-47/` after the declared freeze. Every claim below is pinned to a commit and a sha256, never to "HEAD".

## 1. Verdict

`record.py --selftest` is **green and honest about what it runs (10 cases, 0 failures), but it is not calibrated against its own predicate**: of 41 single-clause deletions, **18 turn at least one case red and 23 do not**. Of those 23, **4 are caught by the landing card anyway and 19 change neither the selftest nor the landing verdict**. The two most valuable findings are outside the case set:

1. **The `axes` correction class is unparsable.** `CORR` accepts only `seats|window|path|rev`. The landing `SCORECARD.md` carries four `- corrects` lines; the counter reads **two**. A false or contentless `- corrects axes …` line scores **green**. Claims-file predicate 3's axes arm is dead and the landed card contains two correction lines that are not evidence.
2. **The battery's `correction_forgeries == 3` is a constant, not a measurement.** `forged()` increments it once per call, unconditionally, including when the fixture records `error: no corrections section`. A card with no corrections section reports `{3, 0}` with three errors. Only `forgeries_green` measures anything.

Two structural facts the L1 must reconcile before landing evidence is drafted:

- **`record.py` has no freeze guard.** No `--freeze`, no `gate.freeze_state`. At tip `31b092d1` it exits **0** while `exact.py` exits **2** `frozen_path_changed` for the same instrument, contradicting the claims-file sentence "a change makes both counters exit 2 `frozen_path_changed`".
Re-checked at tip `09a9f912` (18:03:35Z, after the seat's first capture): `exact.py --freeze 62e33f7d --rev 09a9f912` → **2**; `--freeze 09a9f912 --rev 09a9f912` → **0**; `record.py --rev 09a9f912` → **0** with `corrections 2` and battery `3/0`. The relationship did not change with the later commits.

- **At this tip, the only scoring freeze argument is `31b092d1` itself.** Freeze `5017e1f` → 2; freeze `62e33f7d` → 2; freeze `31b092d1` (= rev) → 0. Any freeze whose `tools/round-47/` bytes equal the measured revision scores 0 by construction, so the guard cannot detect the drift it exists to detect.

## 2. Instrument identity

| revision | commit subject | `record.py` sha256 | `exact.py` sha256 |
|---|---|---|---|
| `5017e1f` (ticket freeze) | freeze the exactness counter and the self-assessment counter | `af666ce2…` | `dcef54f1…` |
| `9018c53b` (A1) | drop the unreachable window-pair clause | `787f909a…` | `dcef54f1…` |
| `62e33f7d` (A2) | window forgery becomes a real forgery | `1888605e…` | `dcef54f1…` |
| `1e2c3102` (A4) | historical-correction fixture gets its round-3 dispatch | `c704c3d4…` | `dcef54f1…` |
| `07d2894e` (A5) | ghost-atom forgery lands inside the corrections section | `abf35257…` | `dcef54f1…` |
| `31b092d1` (A6/A7 + record) | A6 battery fixture citations | `abf35257…` | `01a4bca7…` |

Frozen sources are retained at `sources/record-at-5017e1f.py`, `sources/record-at-9018c53b.py`, `sources/record-at-1e2c3102.py`, `sources/record-at-07d2894e.py` with `sources/sha256sums.txt`.

## 3. Registered cases

`--selftest` is **not runnable as documented**: `--root` and `--rev` are `required=True` even on the selftest path, so `python3 -I -B tools/round-47/record.py --selftest` exits 2 with `error: the following arguments are required: --root, --rev` (measured 17:49:16Z). With dummy `--root/--rev`:

| bytes | cases | failures | exit | stdout sha256 |
|---|---|---|---|---|
| `5017e1f` (frozen) | **9** | 0 | 0 | `94681834…` |
| `1e2c3102` (audited) | **10** | 0 | 0 | `702b1bb2…` |
| `07d2894e` | **10** | 0 | 0 | `32e13978…` |

The ten cases at `1e2c3102` (eight built through `run()`, two appended directly): `red-seats-false-no-correction`, `green-seats-false-superseded`, `red-unverifiable-window-uncorrected`, `red-ghost-exemption`, `red-correction-total-false`, `red-one-correction`, `green`, `green-historical-correction` (added by A3/A4), `red-non-empty-window`, `battery-discriminates`.

Every case asserts **only** `got == expect` (exit code). None asserts the `failing` list. Two deletions therefore change only a diagnostic string and no verdict — including A1's own removed clause, whose deletion changes one red case's `corrections_bad` count from 2 to 1 while the case stays red.

## 4. Clause-deletion matrix — 41 mutations

Method: `git show 1e2c3102:tools/round-47/record.py` into a scratch lane (`tools/round-47/record.py` + `tools/round-46/gate.py`), one clause edited per run, then `python3 -I -B record.py --root <scratch> --rev HEAD --selftest` with `HYAKU_SCRATCH` set. 23 mutations are syntactic deletions; 18 are one-expression neutralisations (`return X == got` → `return True`), because deleting those expressions would not parse. All 41 are recorded as unified diffs in `mutations.json` and replayable with `replay.py`.

Counts: **18 guarded / 23 unguarded**; of the unguarded, **4 are caught by the landing card** (`SCORECARD.md@1e2c3102`: 50 atoms, 48 verified, 2 exempted, exit 0) and **19 are caught by neither**.

| # | clause deleted/neutered | kind | selftest cases that go red | landing-card exit after deletion | caught by |
|---|---|---|---|---|---|
| M01 | clause 5: len(secs)!=2 -> exit 2 | delete | — | 0 | **nothing** |
| M02 | clause 2: missing_classes check | delete | — | 0 | **nothing** |
| M03 | clause 1: mismatches != 0 | delete | red-non-empty-window | 0 | **selftest** |
| M04 | clause 3: corrections >= CORR_MIN | delete | red-one-correction | 0 | **selftest** |
| M05 | clause 3: corrections_bad empty | delete | red-ghost-exemption, red-correction-total-false, battery-discriminates | 0 | **selftest** |
| M06 | clause 4: exempted <= EXEMPT_MAX | delete | — | 0 | **nothing** |
| M07 | clause 6: battery keys 3/0 | delete | — | 0 | **nothing** |
| M08 | collect: seats sum form | delete | green-seats-false-superseded, green, green-historical-correction | 0 | **selftest** |
| M09 | collect: seats pair form | delete | — | 1 | **landing card only** |
| M10 | collect: window atoms | delete | green-seats-false-superseded, green, green-historical-correction | 1 | **selftest** |
| M11 | collect: window 'is empty' filter | delete | green-seats-false-superseded, green, green-historical-correction | 1 | **selftest** |
| M12 | collect: path atoms | delete | green-seats-false-superseded, green, green-historical-correction | 1 | **selftest** |
| M13 | collect: rev atoms | delete | green-seats-false-superseded, green, green-historical-correction | 1 | **selftest** |
| M14 | collect: axes atoms | delete | green-seats-false-superseded, green, green-historical-correction | 1 | **selftest** |
| M15 | derive: seats-sum equality | neuter | — | 0 | **nothing** |
| M16 | derive: seats-pair equality | neuter | — | 0 | **nothing** |
| M17 | derive: window emptiness | neuter | red-non-empty-window | 0 | **selftest** |
| M18 | derive: window pathspec extraction | neuter | — | 0 | **nothing** |
| M19 | derive: path existence | neuter | — | 0 | **nothing** |
| M20 | derive: axes equality | neuter | — | 0 | **nothing** |
| M21 | derive: rev ancestor-of-rev | neuter | — | 0 | **nothing** |
| M22 | derive: unreadable dispatch -> error | delete | green-seats-false-superseded, green, green-historical-correction | 1 | **selftest** |
| M23 | exempt: placeholder window atom | delete | — | 1 | **landing card only** |
| M24 | exempt: window pair equality | neuter | red-non-empty-window | 0 | **selftest** |
| M25 | exempt: class+key equality | neuter | — | 0 | **nothing** |
| M26 | corrections: ghost-atom existence | delete | — | 0 | **nothing** |
| M27 | corrections: A3 historical exemption | neuter | green-historical-correction | 0 | **selftest** |
| M28 | corrections: seats total re-derived | neuter | red-correction-total-false, battery-discriminates | 0 | **selftest** |
| M29 | corrections: window emptiness re-derived | neuter | battery-discriminates | 0 | **selftest** |
| M30 | corrections: axes arm (dead code) | delete | — | 0 | **nothing** |
| M31 | corrections: 'round-' key normalization | delete | green-seats-false-superseded, green, green-historical-correction | 1 | **selftest** |
| M32 | sections: last two headings only | neuter | — | 2 | **landing card only** |
| M33 | battery: missing-corrections-section branch | delete | — | 0 | **nothing** |
| M34 | battery: no-op mutation counted green | neuter | — | 0 | **nothing** |
| M35 | battery fixture: wrong-seat-total mutation | neuter | battery-discriminates | 0 | **selftest** |
| M36 | battery fixture: non-empty-window mutation | neuter | battery-discriminates | 0 | **selftest** |
| M37 | evaluate: battery wiring | neuter | — | 0 | **nothing** |
| M38 | evaluate: unknown-revision guard | delete | — | 0 | **nothing** |
| M39 | main: --json-out guard | delete | — | 0 | **nothing** |
| M40 | corrections: duplicated axes block (unreachable) | delete | — | 0 | **nothing** |
| M41 | derive: depth_pair always None | neuter | — | 1 | **landing card only** |

### 4.1 Clauses whose deletion the selftest does not notice, split by what still catches it

**Caught by the landing card only** (the selftest cannot see the regression, the landed data can):

- `M09` seats **pair** collector — the fixture card contains only the `Waves: A + B = C` sum form; the real `## Round 45` section contains `Wave 1: … seats; wave 2: … seats`, so deleting the pair collector turns the landing red (exit 1). The pair *equality* is still unguarded (`M16`).
- `M23` the window placeholder exemption (`atom["pair"] is None → exempt`) — the clause that makes A1's repair route work at all; deleting it turns the landing red (exit 1) with `mismatches 1`. No selftest case has a placeholder atom *plus* a window correction.
- `M32` `sections(): heads[-2:]` — the fixture has exactly two `## Round N` sections, so "last two" is a no-op there; with `heads` the landing exits 2 (`fewer than two ## Round N sections`, 33 headings seen).
- `M41` `depth_pair` — the fixture `files` map has no `SKILL.md` and `_card` has no `depth` row, so the only reachable outcome is `None`; with `depth_pair → None` the landing exits 1 (`axes:depth` unobservable).

**Caught by nothing** (selftest green and landing card green after the deletion):

| id | clause | why nothing catches it |
|---|---|---|
| M01 | `len(secs) != 2 → exit 2` | never fires on a 2-section card |
| M02 | clause 2 `missing_classes` | no case lacks a class; the landing has all five |
| M06 | clause 4 `exempted <= EXEMPT_MAX` | landing has 1–2 exemptions; no case exceeds 3 |
| M07 | clause 6 battery keys inside `evaluate_text` | no case passes a battery into `evaluate_text`; the landing battery is already 3/0 |
| M15 | seat-sum equality `(a,b,c) == got` | the landing's only false sum atom is exempted by a correction, so the equality never decides anything |
| M16 | seat-pair equality | same; and the fixture has no pair atom |
| M18 | window `pathspec` extraction | the fixture window is `A..A` (empty for any pathspec); the landing correction window is empty for its paths |
| M19 | `path` existence | no case and no landing atom names a missing path |
| M20 | `axes` equality | landing fractions currently match; fixture coverage matches |
| M21 | `rev` ancestor-of-`rev` | every landing rev resolves and is an ancestor; fixture rev is `tip` |
| M25 | exemption key equality | no case or landing correction carries a wrong key |
| M26 | "exempts an atom that does not exist" | the fixture ghost also fails path existence, so the case stays red for the other reason |
| M30/M40 | `corrects()` axes arm and its duplicated block | **unreachable** (see §6) |
| M33 | battery branch for a card with no corrections section | never exercised by a case |
| M34 | no-op mutation counted green | the fixture never produces a no-op |
| M37/M38/M39 | `evaluate()` battery wiring / unknown-rev / `--json-out` | the selftest never calls `evaluate()` or `main()` |

`M26` is not harmless: on a hostile card where the ghost path **exists** (`- corrects path tools/round-46/gate.py: landed`), the truthful instrument exits 1 (`exempts an atom that does not exist`) and the `M26` mutant exits 0. The selftest's ghost uses a missing path, which trips two checks at once and hides the dedicated guard.

## 5. Battery verification — truthful vs forged

### 5.1 The real landing card

`record.py@1e2c3102` against `SCORECARD.md@1e2c3102`: exit **0**, 50 atoms, 48 verified, 2 exempted, `corrections 2`, and

```
battery: correction_forgeries 3, forgeries_green 0
  correction-wrong-seat-total   exit 1  ['corrections that do not re-derive: 1']
  correction-window-not-empty  exit 1  ['corrections that do not re-derive: 1']
  correction-ghost-atom         exit 1  ['corrections that do not re-derive: 2']
```

Forged variants of the same card (in-memory text, read-only):

| forgery | exit | evidence |
|---|---|---|
| `2 waves, 76 seats total` → `77` | **1** | `corrections_bad` names the line |
| coverage row head `138/138` → `137/138` | **1** | `mismatches ['axes:coverage']` |
| extra `- corrects axes depth: 0/0` inside the section | **0** | `corrections` stays 2; line is never parsed |
| extra `- corrects axes coverage: nonsense` inside the section | **0** | same |
| extra `- corrects path tools/round-46/gate.py: landed` (path exists) | **1** | `exempts an atom that does not exist` |

The axes rows are green in every case because the counter's `CORR` regex cannot see the line: `CORR.match("- corrects axes coverage: 138/138")` is `None`, `CORR.match("- corrects seats round-45: …")` is a match. The landing's two `- corrects axes …` lines are inert text.

### 5.2 End-to-end fixture lane (full CLI, not just `evaluate_text`)

A 12-commit fixture repo under the seat scratch (`git rev-parse --show-toplevel` asserted equal to the fixture) with two dispatch waves (2+3), a real empty window over `tools/x/` (`c1..c2`), a 2/2 depth section and three truthful corrections. Run with the `07d2894e` bytes and `--json-out` inside the fixture:

| run | exit | detail |
|---|---|---|
| truthful | **0** | 7 atoms, 7 verified, 3 corrections, battery `3/0`, all three fixtures exit 1 |
| forged seats total 5 → 6 | **1** | `corrections that do not re-derive: 1`, line named |
| extra `- corrects axes coverage: 0/999` | **0** | `corrections 3`, `failing []` |

The same fixture establishes the CLI guards the selftest never touches: `--json-out` into `SKILL.md` → 2 (`inside a graded or frozen surface`); `--json-out` outside the lane → 2; `--rev deadbeef…` → 2. **`--json-out` into a non-existent directory raises `FileNotFoundError` outside `gate.main_guard` → traceback and exit 1**, not 2: a could-not-evaluate reported as not-met.

### 5.3 The `correction_forgeries == 3` clause is a tautology

`forged()` runs exactly three times and increments `correction_forgeries` on every path, including the early `error: no corrections section` return. Removing the corrections section from the landing card gives

```
battery: {correction_forgeries: 3, forgeries_green: 0}
  all three fixtures: {"error": "no corrections section"}
full receipt: exit 1, failing ['mismatches 2 != 0', 'corrections 0 < 2']
```

— the battery contributes nothing to that red. `evaluate_text` never inspects `fixtures` for `error`. As written, clause 6's first half cannot fail for any input, and `forgeries_green == 0` is satisfiable with **zero** evaluated forgeries. A clause that binds a constant, plus one that a missing section satisfies vacuously, is the round-46 `R46-CL4` defect class again.

### 5.4 A1 and A2 red-befores, independently reproduced

- Frozen bytes (`af666ce2`) at the landing card: exit 1, `corrections_bad: ["window pair names no atom in scope"]` — A1's stated red-before.
- A1 bytes (`787f909a`) at the landing card: exit 1 `battery forgeries_green 1 != 0`, with the window fixture **exit 0**. Bad: `332f4884..<tip>` over `tools/round-46 plans/round-46-claims.md` prints nothing, so `<A>..tip` was empty and the "forgery" was a no-op — A2's stated red-before.
- A2's replacement (`root..tip`) is non-empty over those paths, so the forgery is real. It remains a heuristic on the correction's pathspec: a correction whose paths entered at the root commit and were never touched again would make the forgery a no-op again (safe failure — the battery flags itself — but not a proof).

## 6. The `axes` correction class: frozen clause, dead implementation

Claims-file predicate 3 names three correction shapes and requires that every correction line re-derive. The implementation parses only four of the five classes:

```
CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")
```

`corrects()` still carries an `axes` arm (`CORR_AXES`, `<resolved>/<total>`) — unreachable, because no entry of class `axes` can exist — and a second, duplicated `axes` block that references an undefined `atom` and would raise `NameError` if it were ever reached. A `sys.settrace` over a full card+battery evaluation shows the only `corrects` lines executed are 280 (the arm's class test, reached as a fall-through for `path`/`rev`), 290 and 291; **lines 281–289 and 292–299 never execute**.

Consequences for the frozen claim, all measured:

- landing `corrections` = **2**, while the card writes **4** correction lines; `corrections >= 2` is met exactly at the minimum, by lines from two classes only;
- a false `axes` correction is green (§5.1), so "every correction line itself re-derives" is false of the landed card;
- `known_pairs` — A1's other half — is now computed and never read, so nothing binds a `window` correction to a specific atom beyond the class/key existence check.

## 7. Freeze and revision integrity

Measured at 17:59:41Z, tip `31b092d1`:

| command | exit | reason / changed |
|---|---|---|
| `exact.py --freeze 5017e1f… --rev 31b092d1` | **2** | `frozen_path_changed`: `plans/round-47-claims.md`, `tools/round-47/`, `…/exact.py`, `…/record.py` |
| `exact.py --freeze 62e33f7d… --rev 31b092d1` | **2** | `frozen_path_changed`: `tools/round-47/`, `…/exact.py`, `…/record.py` |
| `exact.py --freeze 31b092d1… --rev 31b092d1` | **0** | freeze == rev |
| `record.py --rev 31b092d1` | **0** | no freeze argument exists; no `gate.freeze_state` call |

Facts, not adjudication: (a) the instrument changed after the freeze in A1, A2, A3, A4, A5 (`record.py`) and A6 (`exact.py`); (b) the claims file still contains "Nothing in this file or in `tools/round-47/` changes after the freeze" and "a change makes both counters exit 2 `frozen_path_changed`", which `record.py` cannot honour; (c) the claims file's own re-derivation rule now yields `62e33f7d`, from which `exact.py` exits 2 at tip; (d) the only scoreable pair is `freeze == rev`, where the guard is vacuous. Any landing evidence for C2 must state which pair it used, and C2 currently scores through a state C1 rejects.

## 8. Dead weight introduced or left by the amendments

- `known_pairs` (computed, never read after A1) and `exempt_keys` (computed, never read) — both single-occurrence names.
- the duplicated `axes` block in `corrects()` (`NameError` if reached) and its `CORR_AXES`;
- `collect(section_text, rnd, files, root, rev)` takes three unused parameters;
- `selftest.run(..., with_battery=False)` takes a parameter it never reads — no case ever feeds a battery to `evaluate_text`, which is why `M07` survives.

## 9. What I did not run

- No audit of `exact.py`'s selftest or its battery (C1's surface, another seat).
- No edits to `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, or the fleet repo; no git/jj mutation anywhere, including the lane; frozen bytes were only read (`git show`) and copied to scratch.
- No landing-gate build/lint/test run: parent owns post-integration verification.
- I did not construct a card that exercises `exempted > 3`; the clause is reported unguarded rather than falsified.

## 10. Receipts

| file | what |
|---|---|
| `receipts.json` | every command, exit, digest and measured value in one object |
| `mutation-matrix-p2.json` | raw per-mutation selftest verdicts (41 rows) |
| `clause-matrix.json` | per-mutation category: guarded / landing-only / nothing |
| `mutations.json` + `replay.py` | the 41 unified diffs and the driver that re-runs them |
| `fixture-e2e.json` | truthful + forged end-to-end receipts of the fixture lane |
| `receipts/exact-final-*.json`, `receipts/record-final.json` | freeze-argument sensitivity at `31b092d1` |
| `receipts/fixture-truthful-cli.json` | `--json-out` receipt written by the counter itself |
| `sources/` | the four pinned `record.py` byte images + `sha256sums.txt` |

Scratch root `/fast/scratch/hyaku/kaidoku-r47/C2SelfTest` was removed after these receipts were copied; nothing in `/tmp` was used.

### Reproduction

```sh
export HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47 C2=/path/to/.ufo/waves/round-47/w1/C2SelfTest
python3 $C2/replay.py --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --scratch $HYAKU_SCRATCH/replay
python3 -I -B tools/round-47/record.py --root . --rev 31b092d1 --selftest   # needs --root/--rev
python3 -I -B tools/round-47/exact.py --root . --freeze 62e33f7d --rev 31b092d1  # 2
python3 -I -B tools/round-47/record.py --root . --rev 31b092d1                  # 0
```
