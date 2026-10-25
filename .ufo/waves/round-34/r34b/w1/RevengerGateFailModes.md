# RevengerGateFailModes — R34-C2 gate evasion enumeration

Round 34 re-dispatch, wave 1. Lane: `kaidoku`. Frozen claim: R34-C2 at
`c79bbe7b0959132b9873ff3431cf5eb313b58b33`. Role: bounded read-only attack of the
pre-freeze structure-blind shortcut-replay gate. **Report only — no lane file was
patched, no VCS mutation, no fixture/reader binary executed.**

All probes ran on a byte-identical copy of the frozen instrument under
`/fast/scratch/hyaku/kaidoku-r34b/w1/RevengerGateFailModes/root/`. Pin
verification: `claims.json` lists 26 pinned digests; recomputing SHA-256 over the
working tree gives **0 mismatches** (command and output below), so the scratch copy
is the frozen instrument byte-for-byte.

## Axes

- **(a) Reachability** — does the evasion traverse a real gate/counter code path?
- **(b) Frozen-clause catch** — do the six frozen clauses / config validators see it?
- **(c) Patch minimality** — smallest diff that would catch it, no target/predicate change.
- **(d) Depth** — does the hole invalidate the gate's universal claim, or just one config?

## Baseline reproduction (independent, scratch)

```
cd $S/root
python3 -I -B tools/round-34/replay-gate.py --selftest            # exit 0, 12/12 cases, 3/3 mutants
python3 -I -B tools/round-34/replay-gate.py --root . --config tools/round-34/gate-config-mini.json   # exit 0 CLEAN
python3 -I -B tools/round-34/replay-gate.py --root . --config tools/round-34/gate-config-naive.json  # exit 2 REFUSED
python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b... --json-out log/c2.json  # exit 0
```

Observed verdict lines are identical to
`.ufo/waves/round-34/r34b/after/c2-at-instruments.json`:
`GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0
mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN
green_positive_matched=8 clauses_failed=-` (exit 0, UTC 2026-10-25T07:22:18Z).
Green rows: `structural 8/T`, all 7 shortcuts below; red rows: `label-memorization
8/T` plus 6 below. Note `digest-keyed` matched **0 in both cases** — see Finding F0.

## The five assigned evasions

For each: exact code path, whether the frozen clauses catch it, smallest patch that would.

### E1 — Reader structural on the first N fixtures, memorized the rest

**Mechanism.** `mini-counter.py:score()` iterates `for name in sorted(expected)`
(alpha→zeta, a fixed public order), and runs each reader as
`subprocess.run([sys.executable,"-I","-B",str(reader),str(target)],
env={...,"HOME":str(work)})` inside one `TemporaryDirectory`. `target` is
`work/"opaque-"+sha256(transformed)[:20]+".data"` and **prior files are never
deleted**, so at invocation *i* the directory contains exactly *i* `opaque-*.data`
files. `HOME=work` reaches `Path.home()` (verified: `HOME=/tmp/xyz-test python3 -I
-B -c 'from pathlib import Path; print(Path.home())'` → `/tmp/xyz-test`). So the
reader learns its 0-based fixture index by `len(list(Path.home().glob("opaque-*.data")))-1`
— no decoding, no state file needed.

Probe `readers/probe/hybrid_index.py`: honest `struct` decode for index 0–3,
memorized `expected.json` rows for 4–7.

```
mini-counter --control-reader .../probe/hybrid_index.py  → matched 8, met_target True (UTC 07:22:47)
naive-counter same                                       → matched 8, met_target True
```

Registered as `positive_control` in a green-shaped config:

```
gate --config probe/config-e1pos.json → REPLAY_GATE_CLEAN ... shortcuts_below_target=7 (exit 0)
```

**Frozen clauses catch it?** No. `green_positive_meets_target` requires only
`positive.matched == 8`; the `"structural"` class label is a config-supplied string
the gate never validates. `red_refused` is unaffected. Registered as a *shortcut*,
the gate does refuse it (`shortcuts_over_target=hybrid-index`) — but that is
list-membership enforcement, not detection: the gate's universal claim "no shortcut
meets target" rests on a finite class list, and this reader's discriminating key
(invocation index) is a family the config never names. The deeper point: an
instrument that runs each reader **once, in a fixed public order, with shared
HOME and accumulating temp files** cannot distinguish "decoded 8" from "decoded N
+ replayed 8−N".

**Smallest patch.** In `score()`, per fixture: `work_i = Path(work)/f"{i}-{secrets.token_hex(8)}"`,
`target = work_i/"opaque.data"`, and `env={...,"HOME":str(work_i),"TMPDIR":str(work_i)}`,
`cwd=str(work_i)`; shuffle `sorted(expected)` with an unseeded `random.Random()`;
and default `--seed` to `secrets.token_hex(16)` (currently `"kaidoku-r34-mini-v1"`
— the permutation is deterministic and publicly replayable, so a reader can even
recompute its own input's identity from the algorithm). ≈6 lines. This kills
index-inference; surviving keys (flags/value multiset — see F2) then need explicit
registration as classes.

### E2 — Counter whose predicate is satisfiable by a constant

**Mechanism.** `replay-gate.py:run_counter()` reads exactly three receipt fields —
`matched` (int), `target` (int, must equal `config["target"]`), `met_target` (bool)
— from the last JSON line. Nothing binds `matched` to any fixture execution, and
**the gate never recomputes `met_target`**. Two probe counters, both never opening
a fixture:

- `probe/const_counter.py`: `matched = 8 if basename(reader)=="structural.py" else 0`
  → gate `REPLAY_GATE_CLEAN` (exit 0, `shortcuts_below_target=3`).
- `probe/inconsistent_counter.py`: positive `matched:8, met_target:true`; every
  shortcut `matched:8, met_target:false` → gate `REPLAY_GATE_CLEAN` with
  `shortcuts_below_target=3` **while every shortcut's `matched == target`**
  (rows: `[('structural',8,True),('a',8,False),('b',8,False),('c',8,False)]`).

**Frozen clauses catch it?** No. The pinned config names a real counter, so the
claim is insulated only by the *config pin*, not by the gate. As an instrument the
gate is generic (`"runs whatever counter argv the config names"`), and the gate
receipt itself records **no counter argv, no reader paths/digests** (observed row
keys: `class, exit, finding, matched, met_target, target`; top keys:
`classes_over_target, config, exit, finding, root, rows, verdict`) — the receipt
cannot prove which counter produced it. Worse, `summarise()` computes
`shortcuts_below_target` from `not row["met_target"]`, so an inconsistent receipt
prints a false count.

**Smallest patch.** In `run_counter()`: derive `met = (matched == target)` and
`if met != bool(payload-met-field): raise Unevaluable("counter_receipt_inconsistent")`
(≈3 lines — kills the inconsistent-receipt form). For the constant-counter form,
the gate cannot verify counter internals; the minimal structural fix is
name-invariance: in `evaluate()`, run the positive reader a second time under a
copied, randomized basename (and each shortcut once under the positive's basename),
requiring `matched` to be invariant — ≈8 lines in `evaluate`+`run_counter`. (A
digest-keyed counter still passes; that requires the counter to carry its own
selftest, i.e., a `counter.selftest` argv clause — a bigger, contract-level change.)

### E3 — Config registering three near-identical weak classes

**Mechanism.** `load_config()` enforces only `len(shortcuts) >= MIN_SHORTCUTS` (3,
line `# MUT-A`) and `len(set(classes)) == len(classes)` — class **names**, not
paths or content. Probe: three shortcuts `weak-a/weak-b/weak-c`, all
`path: .../all_false.py` → `REPLAY_GATE_CLEAN, shortcuts_below_target=3`
(exit 0, UTC 07:22:57). The floor is satisfiable by one dead reader renamed three
times; `shortcuts_below_target` in the summary line then reports a padded count.

**Frozen clauses catch it?** No — nothing checks path/digest uniqueness, and
`MIN_SHORTCUTS=3` is the only floor. For the *pinned* config this is latent (it
has 7 classes), but two of those seven are dead weight (F0/F1), so effective
coverage is already thinner than the `7` the summary line advertises.

**Smallest patch.** In `load_config()`, after the class dedupe: resolve each
`item["path"]`, `if len(set(paths)) != len(paths): raise Unevaluable("config_shortcut_duplicate_path")`,
and digest-level `len(set(sha256(path)) != len(paths)` →
`Unevaluable("config_shortcut_duplicate_reader")` (≈4 lines). Optionally require
`item["class"] != positive["class"]` here too (see E5-name).

### E4 — Shortcut reading the counter's own temp paths

**Mechanism.** Same code path as E1 (`HOME=work`, accumulating `opaque-*.data`),
plus a second channel: the reader subprocess **inherits the counter's cwd** (the
gate runs the counter with `cwd=str(root)` and never overrides the reader's cwd),
and the oracle `expected.json` sits at a fixed repo-relative path reachable from
either cwd *or* `Path(__file__).parents[2]` — `readers/` is a sibling of the
oracle. Probe `readers/probe/oracle_leak.py` (never opens `argv[1]`):

```
mini-counter --control-reader .../probe/oracle_leak.py → matched 8, met_target True
naive-counter same                                    → matched 1 (zeta only), met False
```

The naive failure is *incidental* (`HOME=/tmp` there, so the sibling count is 0
and the index drifts to the last fixture) — not a defense. On the permuted counter,
the only instrument that matters for R34-C2, the leak is total.

**Frozen clauses catch it?** No; the class is not in the registered list and no
clause inspects reader I/O. **Smallest patch:** same per-fixture isolation as E1
(`cwd=work_i`, `HOME=work_i`, `TMPDIR=work_i`, delete `work_i` after the run —
`mkdtemp`+`rmtree` per fixture ≈5 lines). This closes sibling-count indexing and
state files, but **not** the `__file__`-relative oracle read — a reader living in
`readers/` can always reach `../expected.json`. The complete fix also requires the
identity-randomization from E1 (random order + unseeded permutation), because with
the oracle public, fixture identity must not be inferable without decoding; today
it is inferable three ways (index, path digest recomputation, sorted order).

### E5 — Reader returning a superset the counter canonicalizes away

**Mechanism.** `canonical()` in both counters builds `sorted(rows, key=(name,flags,
value))` and `score()` compares `observed == want` (a sorted *list*). There is no
dedupe and no length normalization. Probe `readers/probe/superset.py` (correct
rows + one extra): `matched 0` on all 8 — **caught**. Probe
`readers/probe/shuffled_order.py` (same rows reversed): `matched 8` — order
normalization is *intended* (expected.json is stored sorted; `structural.py`
emits file order).

**Frozen clauses catch it?** The strict superset — yes, caught. But the probe
surfaced a residual the clauses miss: `canonical()` accepts
`isinstance(x, int)` for `flags`/`value`, and Python bools are ints
(`isinstance(True,int)`, `True==1`, `{"flags":True}=={"flags":1}`). Probe
`readers/probe/bool_flags.py` emitting `flags: true/false`: `matched 6` — wrong on
gamma/zeta only where expected flags ∈ {2,3}. So a **type-degenerate** record is
canonicalized to equality. **Smallest patch:** `type(record["flags"]) is int` and
`type(record["value"]) is int` (and `type(value["schema"]) is int`) — a three-token
diff, or normalize `flags = int(record["flags"])` after rejecting bool.

## Cross-cutting findings (depth)

- **F0 — `digest-keyed` is a dead class.** Its template key `e1c4d1d5` matches no
  fixture digest (fixture SHA-256 prefixes: alpha `d1de0e6f`, beta `a8547fcf`,
  delta `79ff7036`, epsilon `82f03f99`, eta `5bcabeb2`, gamma `ffb57ecd`,
  theta `b1f87d7c`, zeta `19ff4074`). It returns `[]` on all 8 in both cases,
  identical to `all-false`. Of the 7 registered classes, two (`all-false`,
  `digest-keyed`) can never fire; `record-order-replay` also fails for an
  incidental reason (true `name_off` values 10..63 exceed its 8-entry NAMES table,
  so it drops records rather than exercising the intended mechanism), and
  `fixed-slice`/`string-scan` fail trivially. **The red case's discrimination
  rests on a single class: `label-memorization`** — the only class that meets
  target in red and collapses in green (8→0).
- **F1 — class-label collision bypasses refusal.** `evaluate()`:
  `over = sorted(row["class"] for row in findings if row["met_target"] and
  row["class"] != positive_spec["class"])`. A shortcut declared with class
  `"structural"` is silently excluded from `over`. Probe: red config with
  `label-memorization` relabelled `structural` → `REPLAY_GATE_CLEAN` (exit 0)
  **on the naive config where it scores 8/8**. The gate emits
  `shortcuts_below_target=6` while a shortcut met target. `load_config` dedupes
  shortcut classes only among themselves; nothing compares them to the positive
  class. Smallest patch: `if item["class"] == positive_spec["class"]: raise
  Unevaluable("config_shortcut_duplicate_class")` — 2 lines. (For the pinned
  claim the C2 counter's `red_refused` clause catches the relabel since it asserts
  `"label-memorization" in red_classes`; the gate itself does not.)
- **F2 — surviving-invariant shortcut family unregistered.** `permute` preserves
  `count`, `flags[]`, `value[]`, `name_off` multiset, size, and header bytes
  (all 8 fixtures share `size=512, ver=1, roff=16`). A shortcut keyed on
  `(count, tuple(flags), tuple(values))` uniquely identifies every fixture —
  that class is not registered, so the universal "no shortcut" claim has at
  least one more unnamed member.
- **F3 — `permute()` hardcodes `records_off=16`.** It writes new `name_off` at
  `base = 16 + 8*index` while `decode_fixture` accepts `records_off >= 16`.
  Verified: an `alpha` variant rebuilt with `records_off=24` decodes
  identically, but `permute()` corrupts it (`permute preserves decoded output:
  False` — writes `0x35,0x0` at offset 16 where the real records start at 24).
  Latent only because all pinned fixtures share `roff=16`; the green surface
  never exercises `roff>16`, `count=0`, bad magic, or any negative fixture —
  the counter's `Unevaluable` branches are dead code. Smallest patch:
  `base = records_off + 8*index` (1 token) in `permute`.
- **F4 — receipt is not self-describing.** Gate JSON has no counter argv, no
  reader paths, no digests; combined with `resolve()` accepting absolute paths
  and `load_config` not confining paths to `root`, a config can point outside
  the repo. Smallest patch: record `config["counter"]["argv"]` and per-row
  `reader`+`sha256` in the receipt; reject `resolve()` results escaping `root`.

## Tooling

No installs needed or performed (`python3 3.x` at `/usr/bin/python3` sufficed);
nothing to record per RULES.md.

## Commands and exits (all UTC 2026-10-25)

| Command (cwd=`$S/root`) | Exit | Key line |
|---|---|---|
| pin recompute (26 digests vs claims.json) | 0 | `pins 26 mismatch 0` (07:21:27) |
| `replay-gate.py --selftest` | 0 | `failures 0, mutants_killed 3/3` (07:22:13) |
| gate `--config gate-config-mini.json` | 0 | `REPLAY_GATE_CLEAN ... below_target=7` |
| gate `--config gate-config-naive.json` | 2 | `REPLAY_GATE_REFUSED ... over_target=label-memorization` |
| `c2-shortcut-gate-counter.py --rev c79b...` | 0 | `GATE_COUNTER_OK ... clauses_failed=-` (07:22:18) |
| mini-counter `--control-reader probe/hybrid_index.py` | 0 | `matched 8 met True` (07:22:47) |
| mini-counter `probe/oracle_leak.py` | 0 | `matched 8 met True` |
| mini-counter `probe/superset.py` | 1 | `matched 0` (caught) |
| mini-counter `probe/bool_flags.py` | 1 | `matched 6` (type leak) |
| mini-counter `probe/shuffled_order.py` | 0 | `matched 8` (order normalized) |
| gate `--config probe/config-e3.json` | 0 | CLEAN, 3 same-path weak classes |
| gate `--config probe/config-e5name.json` | 0 | CLEAN on red config (structural-class hole) |
| gate `--config probe/config-e1pos.json` | 0 | CLEAN, half-memorizer as positive |
| gate `--config probe/config-e1short.json` | 2 | REFUSED `hybrid-index,oracle-leak` |
| gate `--config probe/config-e2const.json` | 0 | CLEAN, constant counter |
| gate `--config probe/config-e2inc.json` | 0 | CLEAN, `matched 8 met_target false` rows |
| permute `roff=24` variant | — | `permute preserves decoded output: False` |

## Verdict

`VERDICT: gate holds against the five *registered* classes and the pinned
config, but every assigned evasion except the strict superset (E5) bypasses it:
E1/E4 share one root cause (fixture identity inferable via HOME/temp/cwd/oracle
reachability plus deterministic seed+order), E2 is unchecked (constant and
inconsistent receipts both CLEAN — met_target never recomputed, counter argv not
receipt-bound), E3's floor is satisfiable by one dead reader (no path/digest
dedupe), and E5 leaks only via bool-as-int canonicalization. Two gate-level
holes deepen this: the `positive["class"]` exclusion lets any 8/8 shortcut
relabel itself invisible (CLEAN on the red config), and the receipt is not
self-describing. Smallest total patch ≈ 20 lines across replay-gate.py +
mini-counter.py; the durable fix is the E1 isolation+randomization plus a
registered surviving-invariant class (F2), because the gate's universal claim is
only as strong as its finite class list.`
