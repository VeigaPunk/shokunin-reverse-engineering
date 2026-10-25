# ExecSeatSelftests — outer-CLI selftest sweep at c79bbe7b (R34-C2, wave 1)

Seat: `L1Kaidoku34-2.ExecSeatSelftests`, executor, round 34 run-6 re-dispatch.
Scope: bounded read-only verification. No lane file written except this report; every
probe ran in a fresh clone under
`/fast/scratch/hyaku/kaidoku-r34b/w1/ExecSeatSelftests/`. No lane VCS command, no
`pacman`, no network, no ELF carrier/fixture/reader executed as a program of interest.
The inherited R34-C1 (GNU version-needs) reader and its twelve carriers were neither run
nor scored.

Reproduction tree: `…/ExecSeatSelftests/clone74`, `git clone --no-hardlinks` of the lane,
`git rev-parse HEAD = c79bbe7b0959132b9873ff3431cf5eb313b58b33`, `git status --porcelain`
empty at start (`clone-rc=0`, 2026-10-25T07:18:15Z).

## 0. Bottom line

The three assigned outer-CLI selftests are **green, deterministic and independent of cwd**,
and the C2 counter's production receipt from this fresh clone is **field-for-field identical**
to the committed lane receipt `after/c2-at-instruments.json`. Green selftest ≠ green production
run, in three concrete senses documented below (§3).

Depth result (§4, F8): the frozen **green** surface is not identity-defeating. An
**unregistered** shortcut class — memorization keyed on the part of the file that the counter's
name-pool permutation never touches (record `(flags, value)` pairs, fixed record base 16) —
scores **8/8** under the same counter, on the same permuted copies, with exit 0. Registering that
class in a scratch config turns the gate to `REPLAY_GATE_REFUSED ... shortcuts_over_target=value-keyed`
(exit 2), i.e. the *mechanism* is sound; the **frozen class set is incomplete**. The frozen
predicate survives on its exact wording (it is scoped to *registered* classes); the prose it is
read with does not ("Only a reader that walks the record array can associate a name with its
record" — falsified).

## 1. Axes named (Godspeed)

- **A1 Assigned-sweep reproduction** — three specified argv forms, exact exit, stable summary line, UTC.
- **A2 Determinism** — same argv, repeated, byte-identical stdout.
- **A3 Selftest↔production binding** — what a green selftest certifies about the committed
  instruments, configs and fixtures, versus what a green production run certifies.
- **A4 Anti-vacuity of the selftest harness itself** — can the gate's own acceptance suite be
  emptied, shortened or mis-scored while still exiting 0?
- **A5 Trust boundary** — does the gate verify the counter's numbers, or only relay them?
- **A6 Class completeness of the green surface** — does the identity-defeating counter defeat
  every structure-blind memorizer, or only the seven registered representatives?
- **A7 Pin integrity** — are clone, lane working tree and commit blob the same bytes?

## 2. Pin integrity (A7)

`sha256sum` of the three instruments is equal in the clone worktree, the lane working tree, and
`git hash-object` of each file equals its `git ls-tree c79bbe7b` blob:

| instrument | sha256 | blob at c79bbe7b |
|---|---|---|
| `tools/round-34/replay-gate.py` | `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` | `5125454ca18968477ab61d7e1839d6316b1988e1` |
| `tools/round-34/mini-fix/mini-counter.py` | `43ef669ff6ea9fe752798cc376d9dfe83819fa8a2425afea4b275d5cc47c4b52` | `eaadea4bfefb1107f16a7f0e3396ec83f41ad249` |
| `tools/round-34/c2-shortcut-gate-counter.py` | `41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72` | `b38e7bef6c25eae3b072802df563456ca054c1d1` |

Lane `git status --porcelain` shows only untracked `.ufo/waves/round-34/r34b/**` wave artifacts
(10 lines); no tracked instrument is dirty. Environment: `/usr/bin/python3` 3.14.8, git 2.56.0,
jj 0.45.1. **No tool installed or upgraded** — nothing was needed, so there is no
tool/version/channel/reason entry.

## 3. The assigned sweep (A1, A2)

All runs: `cwd = …/ExecSeatSelftests/clone74`, `python3 = /usr/bin/python3`.

### 3.1 replay-gate selftest — exit 0, 07:18:35Z → 07:18:36Z

```
python3 -I -B tools/round-34/replay-gate.py --root . --selftest
```

exit **0**. Stable summary line (last stdout line):

```
{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3, "selftest": "replay-gate"}
```

Per-case lines (`out/gate-selftest.stdout`) cover clean / red-one / red-two / boundary-below /
positive-below / counter-garbage, then `two-shortcuts-unevaluable`,
`duplicate-class-unevaluable`, `positive-absent`, then three mutant kills.

### 3.2 mini-counter selftest — exit 0, 07:18:35Z

```
python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader tools/round-34/mini-fix/readers/structural.py --selftest
```

exit **0**. Summary line:

```
{"matched": 8, "selftest": "structural_reader_meets_target", "target": 8}
```

### 3.3 C2 counter — exit 0, 07:18:43Z → 07:18:46Z (2.69 s)

```
python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . \
  --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out ../out/c2-counter.json
```

exit **0**. Stable line:

```
GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 \
red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-
```

### 3.4 Determinism (A2)

Two immediate repeats (`out/gate-selftest.r1`, `.r2`, `out/mini-selftest.r1`, `out/c2.r1`, `.r2`,
07:18:58Z–07:19:00Z) and a third stamped repeat (07:23:01Z → 07:23:04Z, `out/repeat-*.stdout`)
produced **byte-identical** stdout for all three commands (`diff` → `GATE_STDOUT_IDENTICAL`,
`MINI_STDOUT_IDENTICAL`, `C2_STDOUT_IDENTICAL`); all nine runs exited 0.

### 3.5 Independent reproduction of the committed production receipt

`out/c2-counter.json` vs `.ufo/waves/round-34/r34b/after/c2-at-instruments.json`, compared field
by field: `exit`, `finding`, `met_target`, `gate_path`, `measured_revision`, `selftest_exit`,
`selftest_line`, `selftest_failures`, `mutants_killed`, `green.{exit,verdict,line}`,
`red.{exit,verdict,line}`, `clauses` — **all SAME**, `clauses` dict depth-equal `True`.
Reproduced lines: green `REPLAY_GATE_CLEAN … shortcuts_below_target=7 shortcuts_over_target=-`
(exit 0); red `REPLAY_GATE_REFUSED … shortcuts_below_target=6 shortcuts_over_target=label-memorization`
(exit 2).

Underlying production scores (production path, both counters, `out/gate-green.json`,
`out/gate-red.json`, 07:19:14Z/07:19:15Z):

| reader | green counter (mini, permuted) | red counter (naive, shape-only) |
|---|---|---|
| structural | 8/8 met | 8/8 met |
| label-memorization | 0/8 | **8/8 met** |
| size-keyed | 1/8 | 1/8 |
| all-false, fixed-slice, digest-keyed, string-scan, record-order-replay | 0/8 | 0/8 |

So the red signal is carried by exactly one class (`label-memorization`) and only because the
naive counter exposes the basename; the green surface separates structural (8/8) from every
registered shortcut (≤1/8).

## 4. Green selftest ≠ green production run (A3), and the falsifiers (A4–A6)

### F1 — the gate's selftest never touches the tree it is run against

```
python3 -I -B tools/round-34/replay-gate.py --root /nonexistent-root-xyz --selftest
```

exit **0**, `{"cases": 12, …, "mutants_killed": 3}` (07:19:53Z, `out/gate-selftest-badroot.out`).
`selftest()` builds a synthetic counter and four readers in a `tempfile.TemporaryDirectory` and
ignores `--root` entirely (replay-gate.py:216–301). Consequence: this green is evidence about the
*gate's branch logic only*; it cannot regress on the committed fixtures, configs or counter.

By contrast the mini-counter selftest **is** root-bound:
`--root /nonexistent-root-xyz --selftest` → exit **1**, `Unevaluable: reader_absent`
(07:19:53Z, `out/mini-selftest-badroot.out`). It also runs correctly from a foreign cwd with an
absolute `--root` (exit 0, 07:19:53Z).

### F2 — the mini-counter selftest ignores its own `--control-reader`

```
python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader tools/round-34/mini-fix/readers/label_replay_full.py --selftest   # exit 0
python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader tools/round-34/mini-fix/readers/all_false.py --selftest          # exit 0
```

Both print `{"matched": 8, "selftest": "structural_reader_meets_target", "target": 8}`
(07:23:52Z–07:23:53Z, `out/mini-selftest-label_replay_full.stdout`,
`out/mini-selftest-all_false.stdout`). Cause: `main()` hardcodes
`Path(args.root)/"tools/round-34/mini-fix/readers/structural.py"` under `--selftest`
(mini-counter.py:139–146). The supplied reader is required by argparse and then discarded. A
green mini selftest therefore says nothing about *your* reader — only that the pinned structural
reader still decodes the pinned fixtures. Production with those same readers gives 0/8 exit 1
(§3.5).

### F3 — the gate's acceptance-case count is not pinned

| mutant (scratch) | gate selftest | C2 counter |
|---|---|---|
| delete `("counter-garbage", …)` tuple | exit **0**, `cases: 11, failures: 0` | `GATE_COUNTER_OK` exit **0** |
| `SELFTEST_CASES = []` | exit **1**, `cases: 6, failed: ["no-positive-check"]` | `GATE_COUNTER_MISS` exit 1 (`mutants_killed,selftest_clean`) |
| `MUTANTS = []` | exit **0**, `mutants: 0, mutants_killed: 0, failures: 0` | `GATE_COUNTER_MISS` exit 1 (`mutants_killed`) |

07:19:53Z–07:20:10Z; `out/gate-drop-one-case.selftest`, `out/gate-empty-cases.selftest`,
`out/gate-empty-mutants.selftest`, `out/c2-gate-*.json`, mutant sources `mut/gate-*.py`.
Reading: the mutant count **is** pinned by the C2 counter (`mutants_killed == 3`), but no clause
pins `cases`, so deleting an acceptance case is invisible end-to-end. `SELFTEST_CASES = []`
is caught only incidentally — the mutant loop reuses `config-positive-below.json`, which the case
loop creates, so its absence makes the mutant score exit 3 and "survive".
Also note the gate's own selftest exits 0 with **zero forced mutants**; only the outer counter
refuses that.

### F4 — the mutant loop runs against a stale `scenario.json`

`selftest()` creates the red scenario last (`config_for("red-mut", …)`), then in the `MUTANTS`
loop writes a mutant file and runs it against `config-<case_name>.json` **without rewriting
`scenario.json`** (replay-gate.py:259–272). Every mutant therefore reads the red-mut table
(`pos 4, s1 4, s2 1, s3 0`), not its intended case. Observed exits in the pinned run: 0, 2, 2
against expected 2, 3, 3 — killed, but `no-positive-check` (intended `positive-below`) and
`vacuous-no-shortcut-floor` (intended `two-shortcuts-unevaluable`) were killed by the red
scenario's refusal, never exercising the mutated branch.

I re-ran the same three mutants with `scenario.json` written per case
(`corrected_mutant_harness.py`, 07:19:40Z, `out/corrected-harness.json`): exits 0, 0, 0 against
expected 2, 3, 3 — **still 3/3 killed**. So `mutants_killed=3` is a true number obtained by a
harness whose kills are not case-attributable; the defect is diagnostic (a mutant that only
breaks one case could be masked if that case's mutant happened to be caught by the red scenario),
not a false pass at the frozen configuration.

### F5 — the gate relays `met_target` without checking it against `matched`

`run_counter` type-checks `matched`/`target`/`met_target`, checks `target == config["target"]`,
and then uses only `met_target` for both the positive control and the over-target list
(replay-gate.py:96–101, 160–172). Nothing asserts `met_target == (matched == target)`.
Synthetic counter, target 8, three shortcuts (`synth/counter.py`, table-driven):

| counter self-report | gate verdict | exit |
|---|---|---|
| structural 8/true; s1 **8/false**; s2 0/false; s3 0/false | `REPLAY_GATE_CLEAN … shortcuts_below_target=3 shortcuts_over_target=-` | **0** |
| structural **0/true**; all shortcuts 0/false | `REPLAY_GATE_CLEAN … shortcuts_below_target=3 shortcuts_over_target=-` | **0** |
| structural 8/true; s1 **0/true** | `REPLAY_GATE_REFUSED … shortcuts_over_target=s1` | 2 |

07:21:27Z, `synth/contradiction-*.out.json`, `synth/sanity-*.out.json`. Both contradictions clear
the gate. Latent, not active: the committed mini-counter computes
`matched = sum(row["ok"])`, `met_target = matched == TARGET` (mini-counter.py:130–134), so its
self-report is honest today. This is a trust boundary, not a defect in the frozen verdict.

### F6 — `measured_revision` is a free-form string; no instrument digest is bound

```
python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . \
  --rev 0000000000000000000000000000000000000000 --json-out ../out/c2-bogus-rev.json
```

exit **0**, `GATE_COUNTER_OK … clauses_failed=-`, receipt `measured_revision` =
`0000000000000000000000000000000000000000` (07:19:14Z, `out/c2-bogus-rev.json`). The counter
never compares `--rev` to the checkout and records no hash of the gate, configs, fixtures or
`expected.json`. The receipt is therefore bound to bytes only by the reviewer's re-hash, which I
performed separately (§2) — not by the instrument. Positive control on the same seam: a scratch
gate with `if over:` → `if False:` scores `GATE_COUNTER_MISS` exit 1
(`red_refused,selftest_clean`), matching the lane control `controls/gate-always-clean.py.txt`
(07:19:17Z, `out/c2-gate-always-clean.json`); `if not positive["met_target"]:` → `if False:`
gives `MISS` exit 1 (`mutants_killed,selftest_clean`), matching
`controls/gate-no-positive-check.py.txt` (07:19:20Z).

### F7 — positive result: the green config is not satisfiable by shrinking the fixture set

Copy the tree, delete three of eight fixtures and their `expected.json` entries, run the pinned
gate with the pinned green config: exit **3**,
`REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target shortcuts_below_target=7`
(07:23:53Z, `out/spec-shrink.txt`). The structural positive control's 8-target binds the fixture
set: you cannot weaken the corpus and keep CLEAN.

### F8 — the green surface is defeatable by an unregistered class (primary depth finding)

The `permute()` transform rewrites only `name_off` per record and reorders the **name pool**; the
record array's `(flags, value)` pairs and their order stay byte-identical (verified for all eight
fixtures: `(flags,value)_preserved=True`, `sha_changed=True`, records_off=16 for all,
07:23:35Z).

- `readers/value_keyed.py` — walks the record array, **never** resolves `name_off`, keys a
  memorized table on the per-record `(flags, value)` sequence.
- `readers/value_keyed_fixed.py` — parses nothing but `count` and the eight-byte records at the
  **fixed base 16**, same memorized table.

```
python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader …/readers/value_keyed.py        → exit 0, matched 8/8 met True  (07:22:30Z)
python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader …/readers/value_keyed_fixed.py  → exit 0, matched 8/8 met True  (07:23:35Z)
```

`out/value-keyed-mini.json`, `out/value-keyed-fixed-mini.json`. Both also score 8/8 under the
naive counter (`out/value-keyed-naive.json`) — they are memorizers, not decoders.

Registering that class as an eighth shortcut in a **scratch** green config
(`mut/gate-config-ninth.json`) and running the pinned gate:

```
python3 -I -B tools/round-34/replay-gate.py --root . --config ../mut/gate-config-ninth.json
→ REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 \
  shortcuts_over_target=value-keyed        exit 2   (07:22:40Z → 07:22:41Z, out/gate-ninth.json)
```

Rows: `structural 8/true`, `value-keyed 8/true`, the other seven ≤1/false.

Interpretation, stated at its exact strength:

- The frozen predicate is satisfied **as worded** ("… where every *registered* shortcut class
  stays below target"): 7/7 registered classes are below target on the green counter, and the
  red refusal is reproduced.
- The capability label it is read with does **not** hold: the counter is not identity-defeating
  against memorization keyed on the immutable record array, and the mini-counter docstring's
  "Only a reader that walks the record array can associate a name with its record"
  (mini-counter.py:4–8) is falsified by construction — these readers walk the array and associate
  names from a table without ever reading the name pool.
- This is a **class-coverage** gap, not a mechanism defect: registered, the class is refused
  correctly (exit 2). The registered `fixed-slice` representative
  (`readers/fixed_slice.py`, printable runs at 32-byte strides) is far weaker than its own class
  family; `size-keyed`, `digest-keyed` and `record-order-replay` likewise each cover one
  instantiation.

Design direction for the L1 (NOT run — no claim): make the permutation touch the invariants a
memorizer can key on — permute record order and rewrite `name_off` accordingly, and add a
per-fixture value transform that the counter applies to `expected` in lockstep. Only then can
"structure-blind" be asserted generally. This is a draft recommendation, not a measured result.

## 5. What each green actually certifies (A3 summary)

| command | green means | green does **not** mean |
|---|---|---|
| `replay-gate.py --selftest` | the gate's refusal / positive-control / shortcut-floor branches behave on a synthetic counter in a tempdir; 12 cases and 3 mutant kills as scripted | anything about the committed counter, configs, fixtures or `--root`; the mutant kills are case-attributable (F4) |
| `mini-counter.py --selftest` | the pinned `structural.py` still decodes the 8 pinned fixtures, permuted at the default seed, under `--root` | anything about the `--control-reader` you passed (F2); anything about shortcuts; anything about a production reader |
| `c2-shortcut-gate-counter.py` | red refused + green clean with positive 8/8 + gate selftest clean + 3 mutants killed, **on this checkout's bytes** | the revision it stamps (F6); the class-completeness of "CLEAN" (F8); honesty of a counter's `met_target` (F5); an unshortened acceptance suite (F3) |

The only binding green is the third; the first two are component greens.

## 6. Boundaries and limits

- Everything was run in the clone; the lane tree was only read (`sha256sum`, `git status`, `cat`).
- `--seed` was left at the configs' default (`kaidoku-r34-mini-v1`); seed sensitivity is another
  seat's surface (`LabratSeedSensitivity.md`), not re-run here.
- F8's readers are scratch artifacts, not lane readers; the ninth-class config is scratch. No
  claim that the lane should adopt these exact files.
- One abandoned probe (a "lying mini-counter" variant) failed on its own patch and is not used as
  evidence; the clean trust-boundary evidence is F5's synthetic counter.
- No tool install/upgrade was performed, so no tool receipt applies.

## 7. Draft text for the L1 (not landed)

LOG line (draft):
> W1 ExecSeatSelftests: gate/mini/C2 selftests green, deterministic, cwd- and repeat-stable at
> c79bbe7b; fresh-clone C2 receipt field-identical to `after/c2-at-instruments.json`. Green
> selftest ≠ green production (gate selftest ignores `--root`; mini selftest ignores
> `--control-reader`; only the C2 counter binds configs+fixtures, and it binds no digests and
> does not check `--rev`). Falsifier: an unregistered value-keyed memorizer scores 8/8 on the
> green surface; registered, the gate refuses it (exit 2) — frozen predicate holds as worded,
> class set is incomplete.

Lesson candidate (draft): a pre-freeze replay gate certifies exactly its registered classes and
exactly the transform's invariants; permuting the name pool defeats label/size/digest keys but not
keys on the untouched record array, so the class list must be closed over every invariant the
counter leaves fixed.

## Verdict

`SWEEP_GREEN_REPRODUCED_ATTACK_PARTIAL` — all three assigned selftests run at c79bbe7b with exit 0,
stable lines and UTC above; the production C2 receipt reproduces exactly and the red/green
discrimination is real (structural 8/8 vs label 0/8 green, 8/8 red). The frozen R34-C2 predicate
survives as worded, but its green verdict is class-incomplete (F8: `value-keyed` memorizer 8/8,
gate REFUSED only when registered) and its discrimination is delegated to counter self-report
(F5) on an unverified revision string (F6); the gate selftest is root-independent (F1) and its
mutant kills are not case-attributable (F4), while a deleted acceptance case is invisible
end-to-end (F3).
