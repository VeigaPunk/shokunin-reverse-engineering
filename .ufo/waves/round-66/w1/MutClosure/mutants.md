# MutClosure - R66-C1 counter mutation probe (round 66, w1, attempt 1)

Seat: `MutClosure`. Target (frozen, read-only, never edited):

- `tools/round-66/closure-boundary.py` sha256 `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b` (20908 bytes)
- loaded frozen instrument `tools/round-65/jsc-closure-matrix.py` sha256 `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6` (unchanged)
- base `311079d869f068bc083a8d180977e49634120fdf`; operative freeze `7b63dd5d5199ed30bc3f213573d8594434a18eb6`

Five mutants, each an isolated copy at
`/fast/scratch/hyaku/kaidoku-r66/MutClosure/mut/M{1..5}/tools/round-66/closure-boundary.py`, each with a byte-identical
`tools/round-65/jsc-closure-matrix.py` alongside it so that `--selftest` derives `repo = __file__.parents[2]` to the same
mirror root that `--verify --repo` is given; both therefore load the r65 instrument through its sha256 pin.

Scored by BOTH detectors, same invocation shape for every mutant and for the pristine bytes:

```
PY=/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python
TMPDIR=$S/tmp "$PY" <counter> --selftest
TMPDIR=$S/tmp "$PY" <counter> --verify --repo <mirror-or-lane> \
  --probe $R/.ufo/waves/round-64/inputs/probe-electron.jsc \
  --work <fresh dir> --out <receipt.json>
```

## Baseline (pristine bytes, unmutated)

| detector | exit | result |
|---|---|---|
| `--selftest` | 0 | `SELFTEST CLEAN cases=30 failures=0` |
| `--verify` | 0 | `passed 5 of 5`, `ok=true`, arms a1..a5 all `passed=true` |

A baseline failure would have made every kill inconclusive; the pristine counter is green on both.

## Scoreboard

| # | mutant (one-line) | `--selftest` | `--verify` | verdict |
|---|---|---|---|---|
| M1 | post-probe `cache_entries` scan moved before the probe call | exit 1, `SELFTEST FAILED cases=30 failures=3` | exit 1, `passed 4 of 5` | **killed** |
| M2 | `count_ok` term deleted from the `ok` expression | exit 1, `SELFTEST FAILED cases=30 failures=1` | exit 1, `passed 4 of 5` | **killed** |
| M3 | `skip_run_receipt` synthesises `closure.ok=true`, `closure_claimed=true` | exit 1, `SELFTEST FAILED cases=30 failures=2` | exit 1, `passed 4 of 5` | **killed** |
| M4 | `fixture_probe` always passes `-B` + `SUBPROCESS_ENV` | exit 1, `SELFTEST FAILED cases=30 failures=3` | exit 1, `passed 4 of 5` | **killed** |
| M5 | `arm()` returns `passed: True` unconditionally | exit 0, `SELFTEST CLEAN cases=30 failures=0` | exit 0, `passed 5 of 5` | **SURVIVED** |

Which case binds which mutant:

- **M1** - `--selftest`: `red-ok`, `red-cache-names-pyc`, `red-finding-names-cache` (the red fixture now reads an empty
  post-probe cache, so `cache_present` is `[]`). `--verify`: **a2-unguarded-fixture-red** (`ok:true`, `cache_present:[]`).
- **M2** - `--selftest`: `trunc-ok` (`got=True want=False`). `--verify`: **a4-truncated-manifest-red**
  (`ok:true` with `count_ok:false`, `entries:29`, finding `count 29 != 30`).
- **M3** - `--selftest`: `skiprun-closure-none`, `skiprun-not-claimed`. `--verify`: **a5-skip-run-no-closure**
  (`closure:{...ok:true}`, `closure_claimed:true`).
- **M4** - `--selftest`: `red-ok`, `red-cache-names-pyc`, `red-finding-names-cache`. `--verify`: **a2-unguarded-fixture-red**
  (`ok:true`, `cache_present:[]`; a2 is unreachable because the unguarded branch no longer exists).
- **M5** - nothing binds it: neither the 30 selftest cases nor any of the five `--verify` arms observes `arm()`'s
  `passed` field when the underlying condition is false.

## Survivor finding (M5)

The forced-true `passed` lives at `tools/round-66/closure-boundary.py:219-220`:

```
219: def arm(name: str, passed: bool, detail: dict) -> dict:
220:     return {"arm": name, "passed": bool(passed), "detail": detail}
```

`selftest()` spans lines 331-437 and contains **no call to `arm(`** (calls exist only at 243, 255, 265, 275, 283, all in
`run_verify`). `--verify` consumes the field at line 288 (`passed = sum(1 for a in arms if a["passed"])`) and prints it in
the receipt. On a green host every arm condition at 243/255/265/275/283 evaluates true, so `True` and `bool(passed)` are
byte-identical in the receipt: the scored `--verify` cannot distinguish the mutant from the pristine counter.

The battery is therefore vacuous in the sense that matters for a claim of five boundary arms: the arm predicates are
computed but never exercised red by either scored detector. A controlled red makes the gap visible with the same
`--verify` entry point (only `--python` changed to a path that does not exist, so a1/a2/a3 must go red):

| counter | command variant | exit | passed |
|---|---|---|---|
| pristine | `--verify --python /nonexistent/r66-python` | 1 | 2 of 5 (a1,a2,a3 false; a4,a5 true) |
| M5 | `--verify --python /nonexistent/r66-python` | 0 | **5 of 5** (all detail `ok:false`/`closure_claimed:false`) |

That is a coverage finding against the counter's own `--selftest`/`--verify` pair, not a change to the R66-C1 predicate:
the frozen predicate names five arms, and the instrument reports 5/5 without ever showing that an arm can fail. The
repair, if the owner wants one, would be a selftest case that calls `arm()` with a false condition and asserts
`passed is False` - outside this seat's scope, which is reporting only.

## Per-mutant diffs (unified, against the frozen bytes)

### M1

```
@@ -134,8 +134,8 @@
         elif sha256_file(p) != pin:
             mismatch.append(name)
     pre_cache = mod.cache_entries(root)
+    post_cache = mod.cache_entries(root)
     probe_ok, probe_msg = probe_fn()
-    post_cache = mod.cache_entries(root)
     entries = len(manifest) + 3
     count_ok = entries == expected_count
     findings = []
```

### M2

```
@@ -154,7 +154,7 @@
     if not count_ok:
         findings.append(f"count {entries} != {expected_count}")
     ok = (not missing and not mismatch and not pre_cache and probe_ok
-          and not post_cache and count_ok)
+          and not post_cache)
     return {"entries": entries, "expected_count": expected_count,
             "count_ok": count_ok, "missing": missing, "pin_mismatch": mismatch,
             "cache_before": pre_cache, "cache_present": post_cache,
```

### M3

```
@@ -316,7 +316,9 @@
 def skip_run_receipt(args) -> dict:
     """The do-nothing control: runs nothing, so it claims no closure."""
     return {"tool": TOOL, "predicate": PREDICATE, "skip_run": True,
-            "closure": None, "closure_claimed": False,
+            "closure": {"ok": True, "entries": COUNT, "count_ok": True,
+                        "findings": []},
+            "closure_claimed": True,
             "receipts": [], "runs_total": 0, "runs_matching": 0,
             "verified": False, "exit": 1}
```

### M4

```
@@ -182,12 +182,9 @@
 def fixture_probe(mod, python: str, root: Path, guarded: bool):
     """A real bytecode-writing probe: import the fixture module in `root`."""
     def run():
-        argv = [python] + (["-B"] if guarded else []) + ["-c", "import fixture_mod"]
+        argv = [python] + ["-B", "-c", "import fixture_mod"]
         env = dict(os.environ)
-        if guarded:
-            env.update(mod.SUBPROCESS_ENV)
-        else:
-            env.pop("PYTHONDONTWRITEBYTECODE", None)
+        env.update(mod.SUBPROCESS_ENV)
         env.pop("PYTHONPYCACHEPREFIX", None)
         try:
             r = subprocess.run(argv, cwd=str(root), env=env, capture_output=True,
```

### M5

```
@@ -217,7 +217,7 @@
 
 
 def arm(name: str, passed: bool, detail: dict) -> dict:
-    return {"arm": name, "passed": bool(passed), "detail": detail}
+    return {"arm": name, "passed": True, "detail": detail}
 
 
 def run_verify(args) -> int:
```

## Per-mutant detector outputs (verbatim lines)

```
M1 selftest exit=1
FAIL red-ok got=True want=False
FAIL red-cache-names-pyc got=False want=True
FAIL red-finding-names-cache got=False want=True
SELFTEST FAILED cases=30 failures=3
M1 verify exit=1  passed 4 of 5
  a1 True {"ok": true, "cache_present": [], "findings": []}
  a2 False {"ok": true, "cache_present": [], "findings": []}
  a3 True {"ok": true, "count_ok": true, "entries": 30}
  a4 True {"ok": false, "count_ok": false, "entries": 29, "findings": ["count 29 != 30"]}
  a5 True {"closure": null, "closure_claimed": false}

M2 selftest exit=1
FAIL trunc-ok got=True want=False
SELFTEST FAILED cases=30 failures=1
M2 verify exit=1  passed 4 of 5
  a4 False {"ok": true, "count_ok": false, "entries": 29, "findings": ["count 29 != 30"]}

M3 selftest exit=1
FAIL skiprun-closure-none got={'ok': True, 'entries': 30, 'count_ok': True, 'findings': []} want=None
FAIL skiprun-not-claimed got=True want=False
SELFTEST FAILED cases=30 failures=2
M3 verify exit=1  passed 4 of 5
  a5 False {"closure": {"count_ok": true, "entries": 30, "findings": [], "ok": true}, "closure_claimed": true}

M4 selftest exit=1
FAIL red-ok got=True want=False
FAIL red-cache-names-pyc got=False want=True
FAIL red-finding-names-cache got=False want=True
SELFTEST FAILED cases=30 failures=3
M4 verify exit=1  passed 4 of 5
  a2 False {"ok": true, "cache_present": [], "findings": []}

M5 selftest exit=0
SELFTEST CLEAN cases=30 failures=0
M5 verify exit=0  passed 5 of 5  ok=true
```

Full receipts for each mutant (`verify.json`, `selftest.out`, `verify.out`) existed only under the deleted scratch tree;
the values above are the complete rows of those files that bear on the scoreboard.

## Incidental observation - a4 is not specific to the count clause

While validating the harness I ran the pristine counter with `--probe /nonexistent/probe-electron.jsc`. a4 still passed
(`ok:false`, `count_ok:false`, `entries:29`) with `findings` = `["missing 1: probe", "count 29 != 30"]`, i.e. the arm is
red for two independent reasons at once. The a4 conjunction does not require the probe to have run, so it cannot by itself
show that the count assertion - rather than a missing external - is what turned `ok` false. a3 caught the same condition
(`findings: ["missing 1: probe"]`, exit 1, 4/5). This is a specificity limit of a4, not a defect that any of the five
assigned mutants exercises, and no verdict above depends on it.

## Environment and integrity

- interpreter `/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python` (3.15); toolchain root `/home/vgpnk/.local/share/kaidoku-jsc`
  read only - the probes ran with `-B` + `PYTHONDONTWRITEBYTECODE=1`, and the post-probe scan stayed empty on the a3 arm;
  nothing was written into the toolchain, no copy of it was made.
- scratch `/fast/scratch/hyaku/kaidoku-r66/MutClosure` only; `disk-guard.sh status` read before the pass
  (`/fast/scratch/hyaku` 54% used, 370.2G free).
- no git/jj command was run; no file outside the seat report dir and the seat scratch dir was written.
- restoration evidence: the frozen counter was never written. sha256 after every run:
  `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b` (20908 bytes, mtime 2026-11-03 21:09:31 -0300,
  unchanged); `tools/round-65/jsc-closure-matrix.py` `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6`.
  The only mutated bytes lived in the five scratch copies and were deleted with the scratch tree.
