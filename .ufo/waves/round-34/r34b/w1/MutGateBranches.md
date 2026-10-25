# MutGateBranches — five further mutants of the R34-C2 replay gate

Seat: `L1Kaidoku34-2.MutGateBranches` (mutation-tester, leaf).
Claim under attack: **R34-C2** (pre-freeze structure-blind shortcut-replay gate), frozen at
`c79bbe7b0959132b9873ff3431cf5eb313b58b33`.
Lane VCS: **not written**. R34-C1 production reader and twelve carriers: **not executed, not scored**.
No ELF fixture, reader or carrier was executed as a program; readers run only as `python3`
children of a counter, fixtures only as static bytes.

## 0. Axes named (Godspeed)

| axis | proxy used here | direction |
|---|---|---|
| A1 detectability | does the shipped `--selftest` exit differ from pristine (0)? | more killed = better |
| A2 reach | does the mutant change a verdict on `gate-config-naive` / `gate-config-mini`? | more observable = better |
| A3 blast radius | does the mutant forge CLEAN (false pass) or UNEVALUABLE/REFUSED (false stop)? | false pass is the harmful pole |
| A4 structur blindness | does the mutant leave `rows`/counts inconsistent with the alleged predicate? | any silent row drop = worse |

A3 is the axis that decides severity: a surviving mutant that only ever produces false stops is a
liveness nuisance; a surviving mutant that produces `REPLAY_GATE_CLEAN` is a hole in the freeze
predicate. Exactly one mutant here lands on that pole.

## 1. Baseline reproduced on pinned bytes (A0)

Scratch root `/fast/scratch/hyaku/kaidoku-r34b/w1/MutGateBranches/root` built with

```
cp -a <LANE>/tools/round-34/. $S/root/tools/round-34/          # exit 0, 2026-10-25T07:18:44Z
```

Hashes of the scratch copies equal the `claims.json` pins, and the lane files themselves hash to
the same values (read-only `sha256sum`, 2026-10-25T07:21:27Z):

```
8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558  tools/round-34/replay-gate.py
72b1294171b58ecb276ce84edcff0698c750d9f5e4490a60253e9385086b1428  tools/round-34/gate-config-naive.json
4483f3852429b4390656a1d8235e1d0a676e4da1e7d7841f20bd2b575c12ac9c  tools/round-34/gate-config-mini.json
41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72  tools/round-34/c2-shortcut-gate-counter.py
```

Pristine detector outputs (all with `--root $S/root`, cwd `$S/root`):

| run | command tail | exit | line |
|---|---|---|---|
| selftest | `replay-gate.py --selftest` (2026-10-25T07:18:55Z) | **0** | `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}` |
| red | `--config tools/round-34/gate-config-naive.json` (2026-10-25T07:19Z, file mtime) | **2** | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization` |
| green | `--config tools/round-34/gate-config-mini.json` (2026-10-25T07:19Z, file mtime) | **0** | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` |

Baseline row table (`$S/out/base-naive.json`, `$S/out/base-mini.json`): on **naive** every
shortcut is at 0–1 matched **except `label-memorization` at 8/8** — i.e. the red case has exactly
one over-target class, and it is **the last registered shortcut row**. On **mini** all seven
shortcut classes are 0 and the structural control is 8.

## 2. Method

`/fast/scratch/hyaku/kaidoku-r34b/w1/MutGateBranches/mutate.py` (exit 0, 2026-10-25T07:19:39Z →
07:19:52Z) copies the pristine gate once per mutant, applies **one** exact-string replacement
(anchor occurrence count asserted `== 1`), then runs three detectors per mutant: the mutant's own
shipped `--selftest`, the gate CLI on `gate-config-naive.json`, the gate CLI on
`gate-config-mini.json`. Full matrix: `$S/out/mutants-report.json`; raw stdout per run:
`$S/out/<mutant>.<detector>.stdout|stderr|json`.

"Killed" = shipped `--selftest` exit ≠ 0. "Config-visible" = gate exit/verdict on naive or mini
differs from the pristine 2 / 0 pair above.

## 3. Results — five assigned mutants (six files: (b) at both implementation sites)

| id | mutation (one anchor) | sha256 | selftest | naive | mini | verdict | config-visible? |
|---|---|---|---|---|---|---|---|
| M1 drop class de-dup | `if len(set(classes)) != len(classes):` → `if False:` | `5e0f0b37…d36f` | **1** (fails `duplicate-class-unevaluable`) | 2 REFUSED | 0 CLEAN | **killed** | no |
| M2a all-UNEVALUABLE, in-process | `raise Unevaluable("forced_unevaluable")` first line of `evaluate()` | `5d7f889d…4b84` | **1** (9 cases fail) | 3 UNEVALUABLE | 3 UNEVALUABLE | **killed** | yes |
| M2b all-UNEVALUABLE, CLI | after `evaluate()`, rewrite `result` to `REPLAY_GATE_UNEVALUABLE/3` in `main()` | `09efc90d…3231` | **1** (0 verdict cases fail; only `no-positive-check` + `vacuous-no-shortcut-floor` fail) | 3 UNEVALUABLE | 3 UNEVALUABLE | **killed, incidentally** | yes |
| M3 ignore last shortcut row | `for item in config["shortcuts"]:` → `[:-1]` | `9ffbb7e9…8844` | **0** (12/12 cases, 3/3 mutants) | **0 CLEAN** | 0 CLEAN | **SURVIVED** | **yes — red inverted to CLEAN** |
| M4 counter exit code as verdict | `met = payload.get(…"met_target")` → `met = run.returncode == 0` | `c736457b…7d6` | **1** (`clean`, `boundary-below`, `positive-below`) | 2 REFUSED (identical) | 0 CLEAN (identical) | **killed, incidentally** | no |
| M5 `over` includes positive control | drop `and row["class"] != positive_spec["class"]` | `1e3b7ae0…e89a` | **1** (`clean`, `boundary-below`) | 2 REFUSED, over=`label-memorization,structural` | **2 REFUSED**, over=`structural` | **killed** | yes (green inverted) |

Anchors verified in the pristine source at lines 65 (de-dup), 95 (`met`), 112 (shortcut loop),
123 (`over`), 138 (`summarise`), 209/232 (selftest calls `evaluate()` in-process), 309 (CLI exit).

### M1 — survives every production surface; only the selftest sees it
Mutation output (verbatim, `$S/out/M1-drop-class-dedup.selftest.stdout` last line):
`{"cases": 12, "failed": ["duplicate-class-unevaluable"], "failures": 1, "mutants": 3, "mutants_killed": 3}`.
Both shipped configs register seven distinct classes, so `classes` is de-duplicated for free and
the gate exits 2 / 0 exactly as pristine. **Missing case (detector gap, not a gate defect):** none
needed in the selftest — `duplicate-class-unevaluable` exists and kills it. The gap is at *config*
level: no shipped config can exercise the de-dup branch, so if the branch were deleted in the frozen
revision, only the selftest (and the file hash) would notice. Named absence:
`config-level duplicate-class case` (e.g. a third pin on a duplicate-class fixture config).

### M2 — same defect, two sites; the selftest is blind to the CLI site
* M2a (in-process) dies loudly: `failed = ["clean","red-one","red-two","boundary-below","positive-below","counter-garbage","positive-absent","no-positive-check","vacuous-no-shortcut-floor"]`, `mutants_killed=1`.
* M2b (CLI) reports `"failures": 2` — **no verdict case fails**, because `SELFTEST_CASES` invoke
  `evaluate()` directly (line 209) and never `main()`. It is caught only because the `MUTANTS` block
  runs mutant files through the CLI and expects exit 2. If the three shipped mutant expectations had
  been written against `evaluate()` instead of the CLI, M2b would have shipped a report line saying
  `failed: []`.
* **Missing selftest case: `cli-red-refused`** — run the shipped CLI as a subprocess on the red
  scenario config and assert `exit == 2` and `REPLAY_GATE_REFUSED` on stdout, plus `--json-out`
  content equal to the printed verdict. Draft (for the L1, not applied):

```python
        # CLI-level case: the verdict a caller sees must equal evaluate()'s verdict
        cases += 1
        cli_config = config_for("cli-red", {"target": 4, "matched": {"pos.py": 4, "s1.py": 4,
                                                                    "s2.py": 1, "s3.py": 0}})
        out_path = root / "cli-red.json"
        cli = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                              "--root", str(root), "--config", str(cli_config),
                              "--json-out", str(out_path)],
                             capture_output=True, text=True, timeout=TIMEOUT)
        payload = json.loads(out_path.read_text()) if out_path.is_file() else {}
        line = cli.stdout.strip().splitlines()[-1:]
        ok = (cli.returncode == 2 and line[:1] == ["REPLAY_GATE_REFUSED finding=shortcut_meets_target "
                                                   "shortcuts_below_target=2 shortcuts_over_target=s1"]
              and payload.get("verdict") == "REPLAY_GATE_REFUSED" and payload.get("exit") == 2)
        print(json.dumps({"case": "cli-red", "ok": ok, "observed": line}, sort_keys=True))
        if not ok:
            failures.append("cli-red")
```

### M3 — SURVIVES the shipped selftest and forges CLEAN on the frozen red config

Mutation: `for item in config["shortcuts"][:-1]:` (line 112) — the final registered shortcut class
is never resolved, never run, never scored. `summarise`'s `shortcuts_below_target` drops by one
because it iterates `result["rows"]`.

Observed (`$S/out/M3-ignore-last-shortcut-row.selftest.stdout`, `…naive.json`, `…mini.json`, UTC
2026-10-25T07:19:4xZ):

```
selftest exit=0  {"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}
naive    exit=0  REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=-
mini     exit=0  REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=-
```

Because `label-memorization` — the **only** over-target class in the red case — sits last in
`gate-config-naive.json`, dropping the last row turns the frozen RED case **CLEAN with exit 0**.
That is the exact defect the frozen claim's kill rule forbids ("no shortcut class may be dropped to
reach CLEAN"), and the gate's own selftest does not see it: every `SELFTEST_CASES` scenario puts the
over-target reader in slot `s1` or `s2` (lines 157–160), and no case asserts
`shortcuts_below_target` or `len(rows)`, so both row-drop and count drift are invisible.

Two production-shaped probes of the missing cases:

**(i) `red-last` — minimal config whose only over-target row is the last** (3 rows = `MIN_SHORTCUTS`
floor: `all-false`, `size-keyed`, `label-memorization`; naive counter; `$S/root/config-last-only-red.json`,
`$S/out/lastonly.log`, 2026-10-25T07:20:26Z):

```
pristine  exit=2  REPLAY_GATE_REFUSED … shortcuts_over_target=label-memorization
M3        exit=0  REPLAY_GATE_CLEAN   … shortcuts_over_target=-
```

**(ii) order-dependence** — same three classes, over-target moved to the middle
(`all-false`, `label-memorization`, `size-keyed`; `$S/out/notlast.log`, 2026-10-25T07:21:57Z):

```
pristine  exit=2  … shortcuts_over_target=label-memorization shortcuts_below_target=2
M3        exit=2  … shortcuts_over_target=label-memorization shortcuts_below_target=1
```

Identical exit and verdict; only an unasserted counter string drifts. So M3's detection by the
production red case is **an accident of row order**, not a property of the gate.

**Missing selftest cases (both, they kill M3):**

1. `red-last` — only `s3` meets target, expect exit 2 and `shortcuts_over_target=s3`.
2. `all-shortcuts-scored` — assert `len(payload["rows"]) == 1 + len(shortcuts)` and pin
   `shortcuts_below_target` in the clean case (the count is printed but never asserted).

Draft:

```python
    ("red-last", {"target": 4, "matched": {"pos.py": 4, "s1.py": 1, "s2.py": 2, "s3.py": 4}},
     (2, "REPLAY_GATE_REFUSED", "shortcuts_over_target=s3")),
```
plus a row-count assertion inside the case loop:
```python
            want_rows = 1 + len(json.loads(config.read_text())["shortcuts"])
            result["row_count_ok"] = len(result.get("rows") or []) == want_rows
            ok = ok and result["row_count_ok"]
```

### M4 — the configs cannot see it at all; the selftest kill is a stub artefact
`met = run.returncode == 0` replaces the receipt's `met_target`. Both shipped counters exit
`0 if met_target else 1` (`mini-counter.py`: `return 0 if result["met_target"] else 1`;
`naive-counter.py`: `return 0 if matched == TARGET else 1`), so on both configs the mutation is
**exactly equivalent**: exits 2 / 0 and byte-identical verdict lines to pristine.

The selftest kills it (`failed = ["clean","boundary-below","positive-below"]`) only because the
stub `SELFTEST_COUNTER` has constant exit 0, so every stub row reads as met. A counter whose exit
encodes met — like the real ones — makes M4 invisible. Direct proof with a lying-exit stub
(`$S/lie/lying-counter.py`: reports `matched=8, met_target=true` for `structural.py`, `0` for every
shortcut, and always exits 3; `$S/out/lie.log`, 2026-10-25T07:21:49Z):

```
pristine  exit=0  REPLAY_GATE_CLEAN      finding=no_shortcut_meets_target
M4        exit=3  REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target
```

**Missing selftest case: `exit-status-ignored`** — a stub that reports `met_target` and exits
contradictorily, asserting the gate ignores the process status. Draft: extend `SELFTEST_COUNTER`
with `scenario.get("exit", 0)` and add
```python
    ("exit-status-ignored", {"target": 4, "exit": 3,
                             "matched": {"pos.py": 4, "s1.py": 1, "s2.py": 2, "s3.py": 0}},
     (0, "REPLAY_GATE_CLEAN", "")),
```

### M5 — killed in the safe (fail-closed) direction
Widening `over` to count the positive control kills the mutant on `clean` and `boundary-below`, and
on the green config it turns `REPLAY_GATE_CLEAN` into `REPLAY_GATE_REFUSED`
(`shortcuts_over_target=structural`, exit 2). That is a false stop, not a false pass: specificity
damage, caught by both the shipped selftest and the C2 counter's `green_clean` clause. No missing
case is required; the only observation is that no case asserts the printed
`shortcuts_below_target`/`classes_over_target` split between `rows` (includes the control) and
`over` (must exclude it) beyond the verdict token.

## 4. Downstream: does the pinned C2 counter catch the survivor?

```
c2-shortcut-gate-counter.py --root $S/root --rev scratch-baseline            → exit 0
  GATE_COUNTER_OK … selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-
c2-shortcut-gate-counter.py --root $S/root-m3 --rev scratch-m3 \
  --gate tools/round-34/replay-gate.py                                       → exit 1
  GATE_COUNTER_MISS … selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_CLEAN green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=red_refused
```

(`$S/out/c2-baseline.json`, `$S/out/c2-m3.json`, 2026-10-25T07:20:27Z / 07:20:30Z; `$S/root-m3` is a
scratch copy whose `tools/round-34/replay-gate.py` is M3, sha `9ffbb7e9…8844`.)

So the frozen C2 claim's `red_refused` clause is load-bearing and would refuse this gate. But that
catch is **order-coincidental**: the clause passes only because the shipped red config's single
over-target class happens to be the last row (§3 M3 probe (ii) shows a reordered config leaves M3
undetected by both the selftest and the gate's verdict). The gate's selftest contributes **zero**
detection of dropped classes; the production detector contributes it by luck of ordering.

## 5. Restoration / immutability evidence

* Lane tree: only read. `git -C <LANE> status --porcelain -- tools/round-34` → empty (07:21:27Z).
  No `git`/`jj` mutating command was run; no file under the lane was created or edited except this
  report.
* Pristine scratch copy hash before and after the whole wave:
  `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` both times
  (`$S/out/mutants-report.json` → `pristine_sha256` == `pristine_after_sha256`). Mutants are
  separate files under `$S/mutants/`; the pristine tree was never mutated in place.
* Scratch roots `root-m3`, `root-m4` are disposable one-mutant copies and are left in place as
  receipts; declare them disposable if you prefer.
* No tool was installed or upgraded (no `uv`/`npx`/`pip`/`pacman` transaction); `python3` is
  `/usr/bin/python3` (3.14 per traceback path `/usr/lib/python3.14`).

Shell note for reproduction: this harness's bash aborts the remainder of a call when any command
returns non-zero, so every gate invocation above was either captured to a file or run with
`set +e`; the exit codes quoted are the recorded `$?` values, not inferred.

## 6. Verdict

```
MUTGATE_BRANCHES mutants=6 (5 assigned; b split in-process/CLI) killed=5 survived=1
  survivor=M3-ignore-last-shortcut-row sha=9ffbb7e9df0fa6a02da98cb4b6dacef79eeecb099002b8a94805b3d738b78844
  survivor_effect=gate-config-naive REPLAY_GATE_REFUSED/2 -> REPLAY_GATE_CLEAN/0 (false pass)
  selftest_gap=M3 red-last, all-shortcuts-scored; M2b cli-red-refused; M4 exit-status-ignored
  incidental_kills=M2b (mutant-kill block only), M4 (stub exit constant 0), M1 (config-invisible)
  downstream=C2 counter red_refused catches M3 on the shipped order, not on a reordered config
  lane_files_written=none (report only); pristine_sha_before_after=8fa94b23…7558
```

Severity: **one false-pass survivor at the gate-selftest layer**, contained at the claim layer by
`red_refused` on the shipped config ordering. Coverage finding, not a contract change: the gate's
selftest should gain `red-last` + a row-count assertion (M3), `cli-red-refused` (M2b) and
`exit-status-ignored` (M4); the red config should not rely on the over-target class being last.
