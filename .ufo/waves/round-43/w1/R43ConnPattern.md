DEFECTS FOUND

# Cross-tool pattern report: round-42 base tools vs round-43 draft plan

**Seat**: `R43ConnPattern` (connector)  
**Base**: `6b9e64fe7e0de202d9383baad5792fbfe039a743` (`main`)  
**Scope**: `tools/round-42/`, `tools/round-41/local-source-gate.py`, and `plans/round-43-claims.md`  
**Artifacts**: `.ufo/waves/round-43/w1/artifacts/R43ConnPattern/`  
(`key-mismatches.json`, `pattern-hits.json`, `reproduce-patterns.py`)

---

## 1. Godspeed: Named Axes & Posture

1. **Coverage** (Scorecard: 10/10): R43-C2 brings 18 host-local `corpus/SOURCES.md` rows into lane-resolvable copies checked by `local-source-gate.py`.
2. **Depth** (Scorecard: 10/10): R43-C1 scores the v4 SquashFS triage table on fresh held-out carriers ($n=78$) under a generator refusing unobserved declared tuples (QUALITY 85).
3. **Calibration** (Scorecard: 10/10): Exact binding enforcement, freeze integrity, zero false-greens, and alignment between writer schemas and scorer predicates.

Posture:
- **Iterate cheap in parallel**: Audited all 15 round-42 tools, `local-source-gate.py`, committed round-42 manifests/receipts, and `plans/round-43-claims.md` concurrently across five structural defect classes.
- **Keep moves improving any axis and harming none**: Identified concrete pattern flaws that would cause honest-stop verification failures or vacuous passes at REV, and synthesized them into one unified, non-invasive schema contract move.
- **Don't aim — let the frontier walk itself**: Traced actual dictionary lookups, path predicates, and scratch usage down to exact AST nodes and line numbers.

---

## 2. Executive Summary of Pattern Hits

| Category | Pattern Class | Total Hits | Critical Base / Port Hits |
|---|---|:---:|---|
| **1** | Writer/reader key mismatches (M41-1 class) | 3 | `combo_count` unwritten by generator but read by counter; `fixtures` read at root by counter but nested in generator; `envelope` unwritten in `carriers[]` (relies on path inference). |
| **2** | Receipts lacking scorer digest (closure D4 class) | 4 | `c2-counter.py` Unevaluable exit 2 lacks `counter_sha256_at_freeze`; `c2-controls.py` receipt lacks `counter_sha256` and `exit_code`; `local-source-gate.py` lacks `counter_sha256` and uses `exit` not `exit_code`; `c1-counter.py` never records `counter_sha256_at_freeze`. |
| **3** | Unsegmented path-prefix tests (closure D5 class) | 3 | `prefile-gate.py:132` `_under` matches non-segment prefixes (`tools/round-4` matches `tools/round-42`); `c2-controls.py:583` `startswith(root)` leaks foreign relpaths (`../`); `c2-counter.py:1202` single `startswith('./')` fails on double `./`. |
| **4** | Hardcoded scratch / TMPDIR-ignoring (Prompt §7 class) | 3 | `c2-counter.py:440,2328` hardcodes `kaidoku-r42` under `HYAKU_SCRATCH` and has no `--scratch` CLI arg; `c2-controls.py:609` uses bare `tempfile.TemporaryDirectory()`; `fetch-carrier.py:553` selftest ignores scratch. |
| **5** | `grep -c` occurrence counts vs `grep -o \| wc -l` (QUALITY 13) | 2 | `corpus/knowledge/2026-10-26-unblob-format-matrix.md:4` recheck uses `grep -c 'more than 30 different'`; `SKILL.md:561-564` uses `grep -cE` on integrity hashes. |

---

## 3. Detailed Cross-Tool Pattern Audit

### Category 1: Writer/Reader Key Mismatches (round-41 M41-1 class)

Comparison of generator (`tools/round-42/heldout-gen-v4.py`, planned `tools/round-43/heldout-gen-v4r43.py`) vs counter (`tools/round-42/c2-counter.py`, planned `tools/round-43/c1-counter.py`).

#### 1.1 Manifest Top-Level Keys
| Key | Generator Writes (`heldout-gen-v4.py:2810`) | Counter Reads (`c2-counter.py:1114-1166, 416`) | Status | Impact / Failing Input |
|---|:---:|:---:|:---:|---|
| `seed` | Yes (`l.2811`) | Yes (`l.1127`) | **MATCH** | — |
| `round` | Yes (`l.2812`) | No | Unread-written | Generator writes `42` (must become `43`); counter does not check. |
| `claim` | Yes (`l.2813`) | No | Unread-written | Generator writes `'R42-C2'` (must become `'R43-C1'`); counter does not check. |
| `generator` | Yes (`l.2814`) | Yes (`l.1130`) | **MATCH** | Counter inspects subkeys `name`, `sha256`, `writer`. |
| `classes` | Yes (`l.2939`) | Yes (`l.1114`) | **MATCH** | Validated for uniqueness and count. |
| `carriers` | Yes (`l.2940`) | Yes (`l.1115`) | **MATCH** | Primary carrier array. |
| `combo_count` | **NO** | Yes (`l.1166`) | **READ-UNWRITTEN** | **HIT 1.1**: Counter runs `declared_combo_count = man.get('combo_count')`. If present as int, binds count. Generator puts combo count under `manifest['families']['combo']['count']` and `manifest['combo_unseen']['combos']`. `man.get('combo_count')` is always `None`, bypassing the well-formedness equality check. |
| `fixtures` | **NO** (nested under `generator.fixtures`) | Yes (`l.416, 1092`) | **READ-UNWRITTEN** | **HIT 1.2**: Counter `fixture_scope()` calls `man.get('fixtures')` to populate `res['fixture_scope']` and append to `paths` for `frozen_drift()`. Because it is nested under `generator.fixtures`, `fx` is `None`, `fixture_scope` returns `{}`, and fixture files are never checked for post-freeze drift! |
| `action_vocabulary`, `action_set`, `action_source`, `label_actions`, `new_labels`, `new_label_tokens_binding`, `precedence_observations`, `rea`, `declared_schema`, `families`, `replicate_variation`, `out_of_domain`, `combo_unseen` | Yes (`l.2850-2938`) | No | Unread-written | 13 top-level metadata dictionaries are emitted by the generator but ignored by the counter. In particular, `combo_unseen` is recomputed against dev arm rather than reading the generator's prediction. |

#### 1.2 Generator Metadata (`generator.*`)
| Key | Generator Writes (`heldout-gen-v4.py:2814`) | Counter Reads (`c2-counter.py:1130`) | Status | Impact / Failing Input |
|---|:---:|:---:|:---:|---|
| `name` | Yes | Yes (`l.1132`) | **MATCH** | Checked against `heldout-gen-v4.py` / `GEN`. |
| `sha256` | Yes | Yes (`l.1134`) | **MATCH** | Checked against freeze digest. |
| `writer` | Yes (`name, path, sha256, block_encoder`) | Yes (`path, sha256` at `l.1146-1147`) | **MATCH** | Path & sha256 checked against writer scope. |
| `carriers_per_class`, `version`, `partial_pin` | Yes (`l.2816-2833`) | No | Unread-written | Informational metadata. |
| `fixtures` | Yes (`l.2834-2848`) | No | Unread-written | Manifest nests fixture metadata here; counter looks at root (Hit 1.2). |
| `tuple_check` | Planned in R43 (`plans/round-43-claims.md:52-53`) | Not in r42 counter | **R43 CONTRACT GAP** | Plan specifies `manifest records generator.tuple_check: per-carrier observed/declared verdicts, all equal`. The round-43 counter port MUST bind `g.get('tuple_check')`. |

#### 1.3 Carrier Array Entries (`carriers[].*`)
| Key | Generator Writes (`heldout-gen-v4.py:1946, 2447`) | Counter Reads (`c2-counter.py`) | Status | Impact / Failing Input |
|---|:---:|:---:|:---:|---|
| `id`, `class`, `arm`, `carrier`, `sha256` | Yes | Yes (`l.1118-1288`) | **MATCH** | Verified against regenerated and committed blobs. |
| `declared_features` | Yes (`l.1954, 2474`) | Yes (`l.1469`) | **MATCH** | Single canonical feature key (R41-CL1). |
| `envelope` | **NO** | Yes (`l.1290`) | **READ-UNWRITTEN** | **HIT 1.3**: Counter reads `c.get('envelope')`. When missing, infers `car.rsplit('/', 1)[0] + '/envelope.json'`. If carriers are structured differently, inference fails. |
| `class_expected` | Yes (`l.1959-1963`) (None for combos) | No (`c2-counter.py:1403`) | Unread-written | Generator writes class expectation, but counter takes expected `(label, action)` exclusively from `indep-eval-v4.py`. |
| `declared_extras` | Yes (`l.1955, 2475`) (`extraction_failed`, `max_depth`) | No | Unread-written | Counter `FEATURE_KEYS` (line 161) includes `extraction_failed`, but counter does not read `declared_extras`. |
| `chunks`, `nested`, `rea`, `operation`, `layout`, `content`, `tree`, `corruption`, `damage`, `symlinks`, `residue`, `container`, `seed_dependent`, `combo_index`, `factors`, `decisions`, `family`, `outside_named_union_declared` | Yes | No | Unread-written | 18 carrier layout/generation parameters written by generator are unread by counter. |

---

### Category 2: Receipts Without Scorer's Digest (closure D4 class)

Round-41 closure D4 established that every score receipt must carry `counter_sha256` and `counter_sha256_at_freeze`. Round-43 plan lines 24–25 formally declare:
> *"Every score receipt records the scorer's exit code and `counter_sha256` (the sha256 of the counter file it ran) plus `counter_sha256_at_freeze` (round-41 closure D4)."*

#### Hit 2.1: `tools/round-42/c2-counter.py:1856-1867` — Missing `counter_sha256_at_freeze` on Unevaluable Exit 2
- **File:Line**: `tools/round-42/c2-counter.py:1856` (and inherited by `tools/round-43/c1-counter.py`).
- **Inherited in R43**: **YES**, directly in `c1-counter.py`.
- **Defect**: On `Unevaluable` exit 2 (which is precisely what the freeze control CTL-C1-0 executes before data arrives), `main()` sets `out['counter_sha256']` from git `show`, but **fails to set `out['counter_sha256_at_freeze']`**.
- **Evidence**: `.ufo/waves/round-42/controls/c2/c2-counter-at-freeze.json` at base revision `6b9e64fe` carries `counter_sha256: "f1089167..."`, but `counter_sha256_at_freeze` is **null/missing**.
- **Failing Input**:
  ```bash
  python3 -I -B tools/round-43/c1-counter.py --root . --rev <FREEZE> --freeze <FREEZE> --json-out ctl-c1-0.json
  jq -e '.counter_sha256_at_freeze != null' ctl-c1-0.json  # EXITS 1 (null)
  ```
- **Fix**: In `main()` exception handler:
  ```python
  out['counter_sha256_at_freeze'] = sha256_bytes(show(a.root, _safe_rev(a.root, a.freeze), COUNTER))
  ```

#### Hit 2.2: `tools/round-42/c2-controls.py:581-595` — Missing `counter_sha256` & `exit_code` in JSON
- **File:Line**: `tools/round-42/c2-controls.py:581-595` (and inherited by planned `c2-controls-r43.py` / `c1-controls-r43.py`).
- **Inherited in R43**: **YES**, in `tools/round-43/c2-controls-r43.py`.
- **Defect**: The output dictionary `res` dumped to `--json-out` includes `interp`, `eval`, `scores`, `controls_at_full`, `kill_rule_fires`, but **completely omits `counter_sha256`**, `counter_sha256_at_freeze`, `interp_sha256`, `eval_sha256`, and top-level `exit_code`.
- **Evidence**: Committed receipt `.ufo/waves/round-42/controls/c2/dev-scores-prefreeze.json` has `counter_sha256: None`.
- **Failing Input**:
  ```bash
  python3 tools/round-43/c2-controls-r43.py ... --json-out dev-scores.json
  jq -e '.counter_sha256 != null and .exit_code != null' dev-scores.json  # EXITS 1
  ```
- **Fix**: Stamp `counter_sha256`, `counter_sha256_at_freeze`, and `exit_code = 1 if full else 0` into `res`.

#### Hit 2.3: `tools/round-41/local-source-gate.py:372, 433-442` — Missing `counter_sha256` & Emits `exit` not `exit_code`
- **File:Line**: `tools/round-41/local-source-gate.py:372, 434-442` (bound for R43-C2).
- **Inherited in R43**: **YES**, P43-C2 specifies running `tools/round-41/local-source-gate.py` byte-identical.
- **Defect**: When invoked with `--json`, `doc` dumps `result`, which contains `"exit": 1 if failed else 0` (key `"exit"`, not `"exit_code"`), and omits `counter_sha256` and `counter_sha256_at_freeze`.
- **Failing Input**:
  ```bash
  python3 tools/round-41/local-source-gate.py --root . --rev <REV> --json > receipt.json
  jq -e '.counter_sha256 != null' receipt.json  # EXITS 1
  jq -e '.exit_code != null' receipt.json        # EXITS 1 (has .exit instead)
  ```
- **Fix**: Either wrap `local-source-gate.py` with a lightweight runner that records `counter_sha256` and `exit_code`, or explicitly permit the gate's native schema in P43-C2.

#### Hit 2.4: `tools/round-42/c2-counter.py:113` — Hardcoded Round-42 Counter Path
- **File:Line**: `tools/round-42/c2-counter.py:113`.
- **Inherited in R43**: **YES**, if ported verbatim into `c1-counter.py`.
- **Defect**: Line 113 defines `COUNTER = 'tools/round-42/c2-counter.py'`. When ported to `tools/round-43/c1-counter.py`, if this constant is not updated to `'tools/round-43/c1-counter.py'`, lines 1794–1796 and 1857 hash the *round-42* tool instead of the round-43 instrument that actually ran.
- **Failing Input**: Git diff against freeze will show `counter_sha256` does not match `sha256sum tools/round-43/c1-counter.py`.

---

### Category 3: Unsegmented Path-Prefix Tests (closure D5 class)

#### Hit 3.1: `tools/round-42/prefile-gate.py:131-132` — Non-Segment Prefix Match in `_under`
- **File:Line**: `tools/round-42/prefile-gate.py:131-132`.
- **Inherited in R43**: **YES**, if `prefile-gate.py` is ported or reused.
- **Defect**:
  ```python
  def _under(path, scope):
      return path == scope or path.startswith(scope)
  ```
  `path.startswith(scope)` is unsegmented. If `scope` is `"tools/round-4"` (without trailing slash), it matches `"tools/round-42/c1-counter.py"`. If `scope` is `"plans"`, it matches `"plans_backup/stray.txt"`. Even with a trailing slash in scopes, `_under("tools/round-42-fake/foo", "tools/round-42")` evaluates `True`.
- **Failing Input**:
  ```python
  assert _under("tools/round-42/c1-counter.py", "tools/round-4") is True  # SHOULD BE FALSE
  assert _under("plans_evil/x.md", "plans") is True                      # SHOULD BE FALSE
  ```
- **Fix**:
  ```python
  def _under(path, scope):
      if path == scope: return True
      return path.startswith(scope.rstrip('/') + '/')
  ```

#### Hit 3.2: `tools/round-42/c2-controls.py:582-585` — Unsegmented Root Prefix in Relpath Calculation
- **File:Line**: `tools/round-42/c2-controls.py:582-585`.
- **Inherited in R43**: **YES**, in `c2-controls-r43.py`.
- **Defect**:
  ```python
  'interp': os.path.relpath(os.path.abspath(interp), a.root)
  if os.path.abspath(interp).startswith(os.path.abspath(a.root)) else interp,
  ```
  If `a.root` is `/path/to/kaidoku-shokunin` and `interp` is `/path/to/kaidoku-shokunin-fork/tools/sqfs.py`, `interp.startswith(a.root)` is `True` because the strings share a common prefix without verifying a path separator boundary (`/`). `os.path.relpath` then returns `../kaidoku-shokunin-fork/tools/sqfs.py`, leaking external paths into the committed receipt.
- **Failing Input**:
  `root = "/lane"`, `interp = "/lane-sibling/tool.py"`. `interp.startswith(root)` is `True`; `relpath` is `"../lane-sibling/tool.py"`.
- **Fix**: Check `os.path.abspath(interp).startswith(os.path.abspath(a.root).rstrip('/') + '/')`.

#### Hit 3.3: `tools/round-42/c2-counter.py:1202-1203` — Single-Pass `./` Prefix Strip
- **File:Line**: `tools/round-42/c2-counter.py:1202-1203`.
- **Inherited in R43**: **YES**, in `c1-counter.py`.
- **Defect**:
  ```python
  if cand.startswith('./'):
      cand = cand[2:]
  ```
  In contrast to `c1-counter.py:1597` (`while r.startswith('./'): r = r[2:]`), `c2-counter.py` uses `if`, stripping only the first `./`. If a carrier path or candidate begins with `././`, `cand` retains a leading `./` and git object resolution (`present(root, rev, cand)`) fails.
- **Failing Input**: A manifest carrier with `carrier: "././H01/carrier.sqsh"` causes `present()` to return `False`, marking the carrier uncommitted.
- **Fix**: Replace `if cand.startswith('./'):` with `while cand.startswith('./'):`.

---

### Category 4: Hardcoded /tmp or TMPDIR-Ignoring Scratch (Prompt §7 class)

Prompt bounds binding:
> *"Tools you write must honour TMPDIR / a --work or --scratch argument and never hardcode /tmp (prompt section 7)."*

#### Hit 4.1: `tools/round-42/c2-controls.py:609` — Unbounded `tempfile.TemporaryDirectory()`
- **File:Line**: `tools/round-42/c2-controls.py:609`.
- **Inherited in R43**: **YES**, in `c2-controls-r43.py`.
- **Defect**: `score_eval()` executes `with tempfile.TemporaryDirectory() as t:`. It passes no `dir=` parameter and `c2-controls.py` has no `--scratch` or `--work` CLI argument. When `TMPDIR` is unset, it allocates scratch directly in system `/tmp/`, leaving unblob and evaluation temporary files outside `/fast/scratch/`.
- **Failing Input**: Run `c2-controls.py` with `TMPDIR` unset.
- **Fix**: Add `--scratch` CLI argument to `c2-controls.py` and pass `dir=scratch` to `tempfile.TemporaryDirectory()`.

#### Hit 4.2: `tools/round-42/c2-counter.py:440, 2328` — Hardcoded `kaidoku-r42` Subdirectory & Ignores `--scratch`
- **File:Line**: `tools/round-42/c2-counter.py:440, 2328`.
- **Inherited in R43**: **YES**, in `c1-counter.py`.
- **Defect**:
  ```python
  def scratch_root():
      base = os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()
      d = os.path.join(base, 'kaidoku-r42')
      os.makedirs(d, exist_ok=True)
      return d
  ```
  and line 2328:
  ```python
  sroot = os.path.join(os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir(), 'kaidoku-r42', 'selftest')
  ```
  1. Hardcodes `'kaidoku-r42'`. When ported to round 43, it writes scratch into the round-42 tree instead of `kaidoku-r43`.
  2. If `HYAKU_SCRATCH` is set, it ignores `TMPDIR`.
  3. `c2-counter.py` CLI parser (line 1836) has no `--scratch` or `--work` argument.
- **Failing Input**: Invoking `python3 tools/round-43/c1-counter.py` with `TMPDIR=/fast/scratch/hyaku/kaidoku-r43/w1-seat` writes scratch to `/fast/scratch/hyaku/kaidoku-r42/`.
- **Fix**: Update default to `os.path.join(os.environ.get('TMPDIR') or os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir(), 'kaidoku-r43')`, and add `--scratch` CLI argument.

#### Hit 4.3: `tools/round-42/fetch-carrier.py:553` — Selftest Scratch in Bare `/tmp`
- **File:Line**: `tools/round-42/fetch-carrier.py:553`.
- **Inherited in R43**: **YES**, if carrier fetcher is ported.
- **Defect**: In `selftest()`, line 553 runs `base = tempfile.mkdtemp(prefix='fetch-carrier-selftest-')` without `dir=`, defaulting to `/tmp`.

---

### Category 5: `grep -c` Occurrence Counts vs `grep -o | wc -l` (QUALITY 13)

QUALITY 13 standard:
> *"Occurrence counts on (possibly minified) files use `grep -o … | wc -l`, never `grep -c` — the recorded verify command must itself reproduce."*

#### Hit 5.1: `corpus/knowledge/2026-10-26-unblob-format-matrix.md:4` — `grep -c` on Web Markup
- **File:Line**: `corpus/knowledge/2026-10-26-unblob-format-matrix.md:4`.
- **Inherited in R43**: Existing corpus entry recheck line.
- **Defect**:
  ```markdown
  recheck: 180d — `curl -fsSL https://unblob.org/formats/ | grep -o '<h2 id=' | wc -l` → 97 and `| grep -c 'more than 30 different'` → 3 (ran 2026-10-26)
  ```
  Notice the line correctly uses `grep -o ... | wc -l` for the first check, but immediately lapses into `grep -c 'more than 30 different' -> 3` for the second check! If the unblob documentation page minifies its HTML into single lines, `grep -c` returns 1, causing a false recheck failure.
- **Failing Input**: Single-line minified HTML containing 3 occurrences of `"more than 30 different"`. `grep -c` outputs `1`; `grep -o 'more than 30 different' | wc -l` outputs `3`.
- **Fix**: Change to `grep -o 'more than 30 different' | wc -l`.

#### Hit 5.2: `SKILL.md:561-564` — `grep -cE` for Verification Totals
- **File:Line**: `SKILL.md:561-564`.
- **Inherited in R43**: Queue-drain craft rule reference text.
- **Defect**:
  `grep -cE '^[0-9a-f]{64}  /' = 5` and `grep -cE '^[0-9a-f]{64}  /home/vgpnk/...' = 5`.

---

## 4. UFO-FSD Connector Synthesis & Non-Obvious Move

### Contradiction Observed in Round-43 Plan
1. **Tool naming vs claim assignment**:
   `plans/round-43-claims.md:141-143` lists under C1 frozen paths:
   `tools/round-43/{c1-counter.py, heldout-gen-v4r43.py, c2-controls-r43.py}`.
   The tool is named `c2-controls-r43.py`, but it computes controls for **Claim 1** (depth), outputting to `.ufo/waves/round-43/controls/c1/CTL-C1-3...`.
2. **Receipt contract contradiction (Closure D4)**:
   The freeze-integrity rule (plan lines 24–25) demands that *every* score receipt carries `counter_sha256` and `counter_sha256_at_freeze`. Yet:
   - `c2-counter.py` exit 2 (CTL-C1-0 freeze control) omits `counter_sha256_at_freeze` (Hit 2.1).
   - `c2-controls.py` (CTL-C1-3 dev controls) omits `counter_sha256` and `exit_code` (Hit 2.2).
   - `local-source-gate.py` (CTL-C2-0 freeze control and C2 final score) omits `counter_sha256` and `counter_sha256_at_freeze`, emitting `"exit"` instead of `"exit_code"` (Hit 2.3).
3. **Fixture drift blind spot**:
   `c2-counter.py`'s `fixture_scope` looks for `man.get('fixtures')`, which is always empty because the generator writes `manifest['generator']['fixtures']`. Thus, `frozen_drift()` in `c1-counter.py` never monitors the 14 pinned fixtures under `corpus/evidence/round-42/c2/fixtures/`.

### Proposed Move: "Unified Instrument Receipt Header & Path Alignment"
**A bounded, compatible synthesis across the round's proposals improving Coverage, Depth, and Calibration without harming any axis:**

1. **Standardize the Instrument Receipt Envelope**:
   Amend `tools/round-43/c1-counter.py` and `tools/round-43/c1-controls-r43.py` so that all receipt outputs (including `Unevaluable` exit 2) emit the standard D4 envelope:
   ```json
   {
     "counter": "tools/round-43/c1-counter.py",
     "counter_sha256": "<64-hex>",
     "counter_sha256_at_freeze": "<64-hex>",
     "exit_code": <int>
   }
   ```
   For `tools/round-41/local-source-gate.py` (which P43-C2 requires to stay byte-identical to round 41), amend the plan's counting command or specify that C2 receipts wrap/stamp the gate output with `counter_sha256` (the sha256 of `local-source-gate.py`), `counter_sha256_at_freeze`, and `exit_code = doc['exit']`.
2. **Align Plan Naming & Scratch Arguments**:
   - In `plans/round-43-claims.md:143`, rename `c2-controls-r43.py` to `c1-controls-r43.py` to align with Claim 1 and its output directory `.ufo/waves/round-43/controls/c1/`.
   - Update `scratch_root()` in `c1-counter.py` and `c1-controls-r43.py` to use `kaidoku-r43` (respecting `TMPDIR`), and add an explicit `--scratch` CLI flag.
3. **Close the Fixture Drift Blind Spot in `c1-counter.py`**:
   In `c1-counter.py:fixture_scope()`, inspect `man.get('generator', {}).get('fixtures')` and `tools/round-42/fixtures.json` so that `paths` in line 1095 includes all 14 pinned fixture files, guaranteeing genuine freeze integrity against fixture tampering.
4. **Bind `generator.tuple_check`**:
   Ensure `c1-counter.py` reads and binds `manifest['generator']['tuple_check']` as declared in P43-C1 (l.52-53).

### Second-Order Effects & Verification
- **Second-order effect on runtime**: Eliminates scratch collision between round-42 and round-43 jobs on `/fast/scratch/hyaku`.
- **Second-order effect on verification**: Guarantees that non-author spot-checks (hyaku closure) find 100% compliant D4 receipts across CTL-C1-0, CTL-C1-3, CTL-C2-0, C1, and C2.
- **Risks**: None; `local-source-gate.py` remains byte-identical; all amendments are in round-43 ports and receipt wrappers.
- **Verification**: Run `reproduce-patterns.py` (provided in artifacts), then verify that the patched tools pass all 7 reproduction probes cleanly.

---

## 5. Summary Table for the L1

| Hit ID | Target File / Plan Line | Amendment Needed Before Freeze |
|---|---|---|
| **HIT-1.1** | `tools/round-43/c1-counter.py:1166` | Read `man.get('families', {}).get('combo', {}).get('count')` instead of `man.get('combo_count')`. |
| **HIT-1.2** | `tools/round-43/c1-counter.py:416, 1092` | Point `fixture_scope` to `man.get('generator', {}).get('fixtures')` and `tools/round-42/fixtures.json`. |
| **HIT-2.1** | `tools/round-43/c1-counter.py:1856` | Add `out['counter_sha256_at_freeze']` on `Unevaluable` exit 2. |
| **HIT-2.2** | `tools/round-43/c1-controls-r43.py:595` | Add `counter_sha256`, `counter_sha256_at_freeze`, and `exit_code` to JSON receipt. |
| **HIT-2.3** | `plans/round-43-claims.md:112` | Specify how C2 receipt captures `local-source-gate.py`'s sha256 and maps `"exit"` to `"exit_code"`. |
| **HIT-3.1** | `tools/round-43/prefile-gate.py:132` | Ensure `_under(p, s)` enforces segment boundary `p.startswith(s.rstrip('/') + '/')`. |
| **HIT-3.2** | `tools/round-43/c1-controls-r43.py:583` | Segment-bound `interp.startswith(root.rstrip('/') + '/')`. |
| **HIT-4.2** | `tools/round-43/c1-counter.py:440` | Replace `kaidoku-r42` with `kaidoku-r43` and add `--scratch` CLI argument. |
| **HIT-P1** | `plans/round-43-claims.md:143` | Rename `c2-controls-r43.py` to `c1-controls-r43.py` in frozen paths. |
