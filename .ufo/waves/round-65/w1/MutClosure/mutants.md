# MutClosure — R65-C1 instrument mutation log (round 65, w1)

Instrument under test (frozen, never edited):
`tools/round-65/jsc-closure-matrix.py`, sha256
`79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6`, 24706 bytes, 514 lines.
Baseline selftest of those bytes: `SELFTEST CLEAN cases=34 failures=0`, exit 0.

Raw payloads for every arm below were copied to
`.ufo/waves/round-65/w1/MutClosure/evidence/` before the scratch tree was deleted; the diffs
file there (`diffs.txt`) is the same diff text reproduced in this log.

Method: each mutant is a byte copy of the frozen file with exactly one conceptual change
(M4 is the one two-line change its assignment names: the `-B` argv item and the
`PYTHONDONTWRITEBYTECODE` env entry are one mutation). Each copy was asserted to differ from
the pristine bytes, passed `compile()`, and is stored at
`/fast/scratch/hyaku/kaidoku-r65/MutClosure/ins-M<id>.py`. The frozen file was only ever read.
Every arm was run twice on identical fixtures — pristine bytes then mutant bytes — so a red arm
is attributable to the mutation. Scratch root `S=/fast/scratch/hyaku/kaidoku-r65/MutClosure`.

Fixtures (all under `$S`, all read-only inputs to the instrument):

- `ti` — byte copy of the 27 `CLOSURE` files from `/home/vgpnk/.local/share/kaidoku-jsc`
  plus that venv's `bin/`, cache-free (`__pycache__`/`*.pyc` count 0 at start). Pristine
  `--manifest` on it: `ok=true, entries=30`, exit 0.
- `ti-m4`, `ti-m5`, `ti-m6`, `ti-m6p` — further byte copies of `ti`, each verified cache-free
  (0) and manifest-clean before use.
- `farm-full` — 27 symlinks to the real toolchain files at their pinned relative paths.
  Pristine `--manifest`: `ok=true, entries=30`, exit 0 — the negative controls below differ
  from it by exactly one thing.
- `farm-missing-D2snap` — `farm-full` minus `d8-14.8.178.1/snapshot_blob.bin`.
- `farm-cache` — `farm-full` plus an empty `jsc2js-src/View8/Parser/__pycache__/`.
- Matrix arms use `--probe` = the round-64 `probe-electron.jsc`
  (sha256 `a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710`), `--node` = the
  pinned node v24.21.0 binary (read-only exec), `--python` = the copy's `venv/bin/python`.

Baseline matrix on `ti` (pristine bytes, `--work $S/work-base2` outside the toolchain):
`runs_matching 18/18`, `verified true`, `census.equal true`, exit 0 → every mutant arm below
is compared against a run that is green on the same fixture family.

| id | mutation | selftest | targeted CLI arm (pristine → mutant) | verdict |
|---|---|---|---|---|
| M1 | delete one `CLOSURE` entry: `"d8-14.8.178.1/snapshot_blob.bin": "601efdc6…e24d"` (line 86) | CLEAN 34/34, exit 0 — **not caught** | `--manifest` on `farm-missing-D2snap`: pristine exit 2, `missing=["d8-14.8.178.1/snapshot_blob.bin"]` → mutant exit 0, `missing=[]`, `ok=true`, `entries=29` | **KILLED** (arm) |
| M2 | `cache_entries()` gets `return []` as its first statement (line 195) | FAILED 2/34, exit 1: `cache-detects-pyc got=False want=True`, `cache-detects-dir got=[] want=['sub/__pycache__']` | `--manifest` on `farm-cache`: pristine exit 2, `cache_present=["jsc2js-src/View8/Parser/__pycache__"]` → mutant exit 0, `cache_present=[]`, `ok=true` | **KILLED** (selftest + arm) |
| M3 | `compare_censuses()` returns `{"equal": True, "added": [], "removed": [], "changed": []}` before any comparison (line 222) | FAILED 3/34, exit 1: `census-added`, `census-changed`, `census-removed` all `got=[]` | `--compare cens-a.json cens-b.json` (differ in one changed + one added path): pristine exit 1, `equal=false, added=["c.bin"], changed=["b.bin"]` → mutant exit 0, `equal=true, added=[], changed=[]` | **KILLED** (selftest + arm) |
| M4 | `SUBPROCESS_ENV = {}` (line 129) **and** drop `"-B"` from the view8 argv (line 324) | CLEAN 34/34, exit 0 — **not caught** | full matrix on the clean copy `ti-m4`: pristine baseline exit 0, `census.equal=true` → mutant exit 1, `runs_matching 18/18`, `closure.ok=true`, `census.equal=false`, `added=8` `*.cpython-315.pyc` under `jsc2js-src/View8/{Parser,Simplify,Translate}/__pycache__/` and `venv/…/parse/__pycache__/` | **KILLED** (arm, census clause) |
| M5 | `classify_dump()` gets `return "dump-ok"` as its first statement (line 146) | FAILED 5/34, exit 1: `dump-empty-rc0`, `dump-sigabrt`, `dump-sigsegv`, `dump-exit-1`, `dump-timeout` all `got='dump-ok'` | full matrix on the clean copy `ti-m5`: pristine baseline exit 0 → mutant exit 1, `runs_matching 6/18`, `census.equal=true`, 12 mismatches: `probe D3` (`dump_rc 139`, 0 bytes) and `typora D1/D2/D3` ×3 reps (`dump_rc 134`, 0 bytes) observed `dump-ok\|view8-empty\|node-skipped` against predicted `dump-exit-139…` / `dump-exit-134…` | **KILLED** (selftest + arm) |
| M6 | `emit()`: `verified = bool(summary["verified"] and closure["ok"]) and not skip_run` — census clause dropped (line 347) | CLEAN 34/34, exit 0 — **not caught** | full matrix with `--work` **inside** the toolchain copy (`$S/ti-m6/work`), so label-matching is separated from census equality: pristine control exit 1, `runs_matching 18/18`, `verified false`, `census.equal=false` → mutant exit 0, `runs_matching 18/18`, `verified true`, `census.equal=false`, `added=42` (the cell files under `work/`) | **KILLED** (arm) |

## Exact diffs

```
===== M1
@@ -83,7 +83,6 @@
     "d8-14.8.178.1/d8": "4060ff2e…",
-    "d8-14.8.178.1/snapshot_blob.bin": "601efdc6…",
     "d8-14.8.178.1/icudtl.dat": "c5da2fc3…",

===== M2
@@ -192,6 +192,7 @@
 def cache_entries(root: Path) -> list[str]:
     """Every __pycache__ directory and every *.pyc file under root."""
+    return []  # M2: cache control disabled
     out = []

===== M3
@@ -219,6 +219,7 @@
 def compare_censuses(before: dict, after: dict) -> dict:
+    return {"equal": True, "added": [], "removed": [], "changed": []}  # M3
     added = sorted(set(after) - set(before))

===== M4
@@ -126,7 +126,7 @@
-SUBPROCESS_ENV = {"PYTHONDONTWRITEBYTECODE": "1"}
+SUBPROCESS_ENV = {}
@@ -321,7 +321,7 @@
-                    [args.python, "-B", "view8.py", "--disassembled",
+                    [args.python, "view8.py", "--disassembled",

===== M5
@@ -143,6 +143,7 @@
 def classify_dump(rc, stdout: bytes) -> str:
+    return "dump-ok"  # M5: any rc
     if rc == "timeout":

===== M6
@@ -344,7 +344,7 @@
-    verified = bool(summary["verified"] and closure["ok"] and delta["equal"]) and not skip_run
+    verified = bool(summary["verified"] and closure["ok"]) and not skip_run  # M6
```

## Mutant hashes (scratch copies)

| id | sha256 | bytes |
|---|---|---|
| M1 | `a6adb10867e31c836f7cc7ac81a49953a19a6ac5ef6fccb641138d8b70c531bb` | 24599 |
| M2 | `184677e019a8c9eb2a60e1af60649f09031327933c9fbff2d21ffed65329e527` | 24750 |
| M3 | `df9e0345e7c58d607c5635ba6b8a3492cb9ae1795b596c00ba05e1e90e22b79f` | 24782 |
| M4 | `8ab56f8fb994b7b0aa784d93ec85ee2ba2331ad9359d0aaf4629bbd14bd25f1c` | 24670 |
| M5 | `31014bc95fa159857b729c53aab7931c81ca552e079e2620ca9791142bad5cce` | 24741 |
| M6 | `48e2f6fd0c21aca4799354516986b8516f46663b8346acf4fd73123f41c02a36` | 24693 |

## Verdict

6 mutants, 6 killed, 0 survived. Two of the six (M1, M4) and M6 are invisible to
`--selftest` and are caught only by an end-to-end arm; that asymmetry is a coverage
finding, not a defect in the frozen instrument (see the seat report).

## Commands and observed exits

Legend: `S=/fast/scratch/hyaku/kaidoku-r65/MutClosure`;
`P=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-64/inputs/probe-electron.jsc`;
`N=/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node`;
`IN=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-65/jsc-closure-matrix.py`.
Every run below was issued once; exits are the shell exits of that one run.

Selftest (all seven files), `TMPDIR=$S/tmp python3 <file> --selftest`:

| bytes | exit | printed |
|---|---|---|
| pristine `IN` | 0 | `SELFTEST CLEAN cases=34 failures=0` |
| `ins-M1.py` | 0 | `SELFTEST CLEAN cases=34 failures=0` |
| `ins-M2.py` | 1 | `FAILED cases=34 failures=2` |
| `ins-M3.py` | 1 | `FAILED cases=34 failures=3` |
| `ins-M4.py` | 0 | `SELFTEST CLEAN cases=34 failures=0` |
| `ins-M5.py` | 1 | `FAILED cases=34 failures=5` |
| `ins-M6.py` | 0 | `SELFTEST CLEAN cases=34 failures=0` |

Manifest arms (`--manifest --probe $P --node $N`):

| fixture | bytes | command tail | exit |
|---|---|---|---|
| `$S/farm-full` | pristine | `--toolchain-root $S/farm-full --python $S/ti/venv/bin/python` | 0 |
| `$S/farm-missing-D2snap` | pristine | `--toolchain-root $S/farm-missing-D2snap --python $S/ti/venv/bin/python` | 2 |
| `$S/farm-missing-D2snap` | M1 | same, `python3 $S/ins-M1.py` | 0 |
| `$S/farm-cache` | pristine | `--toolchain-root $S/farm-cache --python $S/ti/venv/bin/python` | 2 |
| `$S/farm-cache` | M2 | same, `python3 $S/ins-M2.py` | 0 |

Compare arm: `python3 <file> --compare $S/cens-a.json $S/cens-b.json` → pristine 1, M3 0.

Matrix arms (all with `--probe $P --node $N --timeout 600`; `--python` = that copy's
`venv/bin/python`, `--work` as listed):

| arm | bytes | toolchain / work | exit | wall |
|---|---|---|---|---|
| pristine baseline | `IN` | `$S/ti` / `$S/work-base2` | 0 | 511 s |
| M4 | `ins-M4.py` | `$S/ti-m4` / `$S/work-m4` | 1 | 576 s |
| M5 | `ins-M5.py` | `$S/ti-m5` / `$S/work-m5` | 1 | 574 s |
| M6 pristine control | `IN` | `$S/ti-m6p` / `$S/ti-m6p/work` | 1 | 558 s |
| M6 | `ins-M6.py` | `$S/ti-m6` / `$S/ti-m6/work` | 0 | 560 s |

(A first baseline attempt was launched with the tool harness's 300 s default deadline and was
killed at 300 s before `emit`; it wrote no output file and its cells are discarded. The 511 s run
above is the baseline used. No fixture bytes were shared between attempts.)
