# ExecAntiVacuityProbe — R34-C2 anti-vacuity probe (round 34, run-6 re-dispatch, wave 1)

Seat: `L1Kaidoku34-2.ExecAntiVacuityProbe`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: read-only verification, bounded probes, drafting. No lane file written except this report; all
probe artifacts live under `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecAntiVacuityProbe/` (referred to
below as `$S`). No VCS command run, no ELF executed, no fixture executed as a program.

## 0. Bottom line

**Yes.** A positive control that scores below the frozen target forces
`REPLAY_GATE_UNEVALUABLE` (exit 3, `finding=positive_control_below_target`) and can never yield
`REPLAY_GATE_CLEAN`. Measured at five shortfall magnitudes — 7/8, 4/8, 0/8 by field defect, 0/8 by
reader exit 3, 0/8 by non-JSON stdout — and reproduced on an independent scratch copy of the tree.
The near-miss case (7 of 8, one field clamped) is the sharp one: the gate does not round, does not
accept `matched >= target`, and does not consult the counter's exit code to decide.

## 1. Axes named (Godspeed)

- A1 **Shortfall magnitude** — does the refusal hold at 7/8, 4/8, 0/8, and at unevaluable readers,
  not only at 0?
- A2 **Defect locality** — is a reader that is structurally correct except one decoded field treated
  as below target (i.e. is the counter's score really per-fixture equality, not a shape check)?
- A3 **Substitution** — can a registered shortcut reader be smuggled in *as* the positive control?
- A4 **Root/cwd independence** — does the verdict survive execution against a copied tree with
  relative paths?
- A5 **Receipt trust and target binding** — is the CLEAN guarantee a property of reader behaviour, or
  of the counter's self-reported receipt / a counter-supplied target?
- A6 **Branch precedence** — when the positive is below target *and* a shortcut meets target, which
  verdict wins and is the red signal retained?

## 2. Instruments and pins verified before probing (UTC 2026-10-25T07:19:20Z)

`sha256sum` against `R34-C2.pins` in `.ufo/waves/round-34/r34b/claims.json` (26 pinned keys; the gate
itself is pinned there too):

| instrument | sha256 observed | pin match |
|---|---|---|
| `tools/round-34/replay-gate.py` | `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` | yes (pin present, value equal) |
| `tools/round-34/mini-fix/mini-counter.py` | `43ef669ff6ea9fe752798cc376d9dfe83819fa8a2425afea4b275d5cc47c4b52` | yes |
| `tools/round-34/gate-config-mini.json` | `4483f3852429b4390656a1d8235e1d0a676e4da1e7d7841f20bd2b575c12ac9c` | yes |
| `tools/round-34/gate-config-naive.json` | `72b1294171b58ecb276ce84edcff0698c750d9f5e4490a60253e9385086b1428` | yes |
| `tools/round-34/mini-fix/readers/structural.py` | `2f399cab36450c052f72c996ef6f3cbb5a57914a2053a6f2a9a31c214eb9b4b6` | yes |
| `fixtures/{alpha,beta,delta,epsilon,eta,gamma,theta,zeta}.mrec`, `expected.json`, `build.py` | see §8 run log | all 10 equal to pins |

Pinned gate selftest re-run read-only at 2026-10-25T07:21:47Z:
`python3 -I -B tools/round-34/replay-gate.py --selftest` → **exit 0**,
`{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}`.
32 fixtures are unmodified synthetic bytes; Python = `/usr/bin/python3` (3.14.8).

## 3. Readers built (A1/A2)

All four are correct MREC decoders (magic, `<HHI` header at 4, `names_off` at 12, 8-byte records at
`records_off`, NUL-terminated ASCII pool) with **exactly one field defect** in the first two, plus two
channel-degenerate controls. None keys on size, basename, digest, fixed offsets or record order.

| reader | sole defect | predicted | scored (`mini-counter.py`) |
|---|---|---|---|
| `$S/readers/value_low16.py` | `value & 0xFFFF` (u16 truncation) | 4/8 — fails the four fixtures holding a value > 0xFFFF (alpha, beta, delta, eta) | **matched 4, met_target false**, exit 1; passing set exactly `{epsilon, gamma, theta, zeta}` |
| `$S/readers/name_cap20.py` | name clamped to 20 bytes | 7/8 — only zeta's `libwayland-client.so.0` (22 B) exceeds 20 | **matched 7, met_target false**, exit 1; failing set exactly `{zeta}` |
| `$S/readers/zero_fields.py` | all three fields zeroed, count traversal correct | 0/8 | matched 0, met_target false, exit 1 |
| `$S/readers/crash_exit3.py` | exits 3, no stdout | 0/8 | matched 0, exit 1 (per-fixture counter row `exit`: 3) |
| `$S/readers/garbage_stdout.py` | exit 0, prints `not a receipt` | 0/8 | matched 0, exit 1 |
| `tools/…/readers/structural.py` (control) | none | 8/8 | matched 8, met_target true, exit 0 |

Predicted failure sets matched observed failure sets exactly, so the score differences are caused by
the single field defect and nothing else — the counter scores per-fixture decoded equality, not shape.

Reproduce any row:
`/usr/bin/python3 -I -B tools/round-34/mini-fix/mini-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --control-reader <path>`
(one JSON line; exit 0 iff `met_target`; receipts archived at `$S/logs/score-<name>.json`).

## 4. Gate ladder (A1, A3, A4)

Each run (from the lane root, config copies under `$S/configs/*.json`, all paths absolute inside
those copies):

```
python3 -I -B tools/round-34/replay-gate.py --root . --config $S/configs/<case>.json --json-out $S/receipts/<case>.json
```

| case | positive reader | positive matched | verdict line | exit |
|---|---|---|---|---|
| `positive-structural` | structural.py | 8 | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` | **0** |
| `positive-value_low16` | value_low16.py | 4 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target shortcuts_below_target=7 shortcuts_over_target=-` | **3** |
| `positive-name_cap20` | name_cap20.py | **7** | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target …` | **3** |
| `positive-zero_fields` | zero_fields.py | 0 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target …` | **3** |
| `positive-crash_exit3` | crash_exit3.py | 0 (reader exit 3) | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target …` | **3** |
| `positive-garbage_stdout` | garbage_stdout.py | 0 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target …` | **3** |
| `positive-as-record_order_replay` | shortcut `record_order_replay.py` | 0 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target …` | **3** |
| `positive-as-label_replay_full` | shortcut `label_replay_full.py` | 0 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target …` | **3** |
| `positive-as-string_scan` | shortcut `string_scan.py` | 0 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target …` | **3** |
| `scratch-root-relative` | value_low16.py, root = `$S/root-copy` | 4 | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target …` | **3** |
| `scratch-root-structural` | structural.py, root = `$S/root-copy` | 8 | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target …` | **0** |

Gate timestamps: ladder 2026-10-25T07:19:41Z–07:19:52Z; scratch-root 07:20:26Z. `$S/root-copy` is a
`cp -a` of `tools/` (gate `8fa94b23…` and counter `43ef669f…` byte-identical), run with
`--config` carrying relative reader/counter paths and `--root .` from inside the copy.

A4 result: verdicts are identical in the copied tree, so the branch under attack does not depend on
lane cwd or on the lane tree being the root. A3 result: substituting a *registered shortcut* as the
positive control does not open the gate — the counter renames every input to an opaque hash path, so
label-keyed (`label_replay_full`, 0/8), order-replay (0/8) and string-scan (0/8) positives all land
below target and force UNEVALUABLE.

## 5. Why the primary answer is what it is (evidence pointer per claim)

- Decision site: `tools/round-34/replay-gate.py:119-122` —
  `if not positive["met_target"]: return {"verdict": "REPLAY_GATE_UNEVALUABLE", "exit": 3, "finding": "positive_control_below_target", "rows": findings, "classes_over_target": []}`.
  It is a plain `not met_target` test on the counter's boolean, so **any** shortfall (7 of 8 included)
  routes here; `met_target` itself is `matched == TARGET` in `mini-counter.py:score()`.
- `matched < target` never reaches `over` / CLEAN because line 119 returns first; `over` (line 123-127)
  and CLEAN (128-130) are only reachable when the positive met the target.
- No `matched >= target` path exists, and no "positive within N of target" tolerance exists.
- The selftest case `positive-below` encodes the same contract
  (`replay-gate.py:160`, expected `(3, REPLAY_GATE_UNEVALUABLE, positive_control_below_target)`), and
  the mutant `no-positive-check` (`replay-gate.py:167`) is killed in the live selftest run (§2).

## 6. Secondary findings (A5, A6) — boundaries, not breaks of the frozen claim

**F1 — the positive check runs after the full shortcut sweep, and UNEVALUABLE masks a REFUSED
condition.** Order: positive once, then all 7 shortcuts, then the line-119 test. So even when the
positive is known below target the gate still spends all 7 counter runs (receipts show `rows` = 8,
each row carrying its own `matched`). Probe `below-positive-plus-meeting-shortcut` (positive
`value_low16` 4/8; `structural.py` additionally registered as shortcut class `structural-as-shortcut`):
verdict `REPLAY_GATE_UNEVALUABLE`, exit 3, `classes_over_target: []` — while the receipt rows show
`structural-as-shortcut matched=8 met_target=true`. The red evidence exists in `rows` but is dropped
from `classes_over_target` and from the printed line. Direction is conservative (never CLEAN), but a
reader of the verdict line alone cannot tell "all shortcuts below target" from "a shortcut met target
behind a bad positive"; only the JSON rows carry that. Evidence: `$S/receipts/below-positive-plus-meeting-shortcut.json`,
run 2026-10-25T07:19:52Z, exit 3.

**F2 — class labels are trusted strings; duplicate paths are not rejected.** Positive `structural.py`
(class `structural`) plus a shortcut entry `{"class": "structural-as-shortcut", "path": …/structural.py}`
yields `REPLAY_GATE_REFUSED` exit 2, `shortcuts_over_target=structural-as-shortcut`
(2026-10-25T07:21:32Z). `load_config` rejects duplicate *class names* only
(`replay-gate.py:83-85`), never a shortcut path equal to the positive path, so a clean counter can be
refused by listing the positive reader twice under two labels. Conservative direction again
(false REFUSED, never false CLEAN).

**F3 — the CLEAN guarantee is receipt-shaped, and the target is counter-supplied; the freeze's pins,
not the gate, carry the binding.** The gate never observes reader behaviour: it parses the last JSON
line of the counter (`replay-gate.py:96-102`) and ignores the counter's exit code (recorded as `exit`,
never tested). Measured:
- `forged-selective` — scratch counter (not the pinned one) reporting `matched=8` only for
  `value_low16.py`: gate → `REPLAY_GATE_CLEAN`, exit 0 (07:20:25Z).
- `forged-exit7` — same, counter exiting 7 on every invocation: still `REPLAY_GATE_CLEAN`, exit 0;
  receipt row `positive.exit = 7` (07:20:26Z).
- `counter-target4-with-defective-positive` — scratch copy of `mini-counter.py` with `TARGET = 8`
  changed to `4`, positive `value_low16.py` (4/8): gate → `REPLAY_GATE_CLEAN`, exit 0 (07:21:33Z),
  because `config.target` equals the counter's self-reported target and 4 == 4.
- Config-side target edits alone are caught: `config-target-lowered-4` (config 4 vs counter 8) →
  `REPLAY_GATE_UNEVALUABLE finding=counter_target_mismatch`, exit 3 (07:21:33Z), i.e. the gate binds
  config↔counter but cannot bind either to the real predicate target.

Reading: within the frozen claim this is sound because `claims.json` pins the counter hash
(`43ef669f…`), the config hash (`4483f385…`) and the fixture/expected hashes, so swapping the counter
or retargeting it breaks the pin set, not the gate. It is still the correct statement of the guarantee:
*the gate refuses a below-target positive control; it does not and cannot certify that the positive
control was scored honestly.* Any future re-freeze must keep the counter+config+fixtures in the pin
list, since the gate alone would pass a forged or retargeted counter. Evidence:
`$S/receipts/{forged-selective,forged-exit7,counter-target4-with-defective-positive,config-target-lowered-4}.json`.

One harness slip, recorded for honesty: an earlier run pointed `--config` at
`forged-selective-exit7.json` (name not yet created) → `REPLAY_GATE_UNEVALUABLE finding=FileNotFoundError:…`,
exit 3 (07:20:13Z); retried as `forged-exit7` with the config present. The gate behaved correctly
(OSError → UNEVALUABLE), the error was mine.

## 7. What this does and does not establish for R34-C2

- Establishes, independently and from a fresh scratch tree: the positive-control branch is real,
  fires on a 7/8 near miss, fires on structurally-correct-but-one-field-wrong readers, fires on
  crash/garbage readers, and cannot be reached by relabelling a registered shortcut as the positive.
- Establishes the red branch is still reachable with an honest positive (green config reproduced:
  CLEAN exit 0 with the pinned structural reader at 8/8) and that a shortcut meeting target is
  refused (pinned red config result `label-memorization` `shortcuts_over_target`, reproduced by the
  production receipt and by my `structural-plus-duplicate-path` run in the opposite direction).
- Does **not** establish reader-behaviour certification (F3) or that a below-target positive keeps the
  red signal visible in the verdict line (F1); both are conservative-only and should be stated as
  boundaries in any doc text the L1 lands.
- Not tested here, and not claimed: the naive/red config line itself (only its receipt and my
  duplicate-path analogue), the `c2-shortcut-gate-counter.py` clause arithmetic, and anything in
  R34-C1 (inherited stop; production reader and twelve carriers not executed or scored).

Suggested one-line draft for the claim text (L1 lands it, not me): *"A registered positive control
that scores below the frozen target produces REPLAY_GATE_UNEVALUABLE (exit 3,
positive_control_below_target), including a 7-of-8 near miss; the CLEAN verdict is therefore
conditional on a positive control that actually meets the target, and on the pinned counter/config/
fixture hashes that make that score honest."*

## 8. Run log (exact commands, exit codes, UTC)

```
# pins, 2026-10-25T07:19:20Z
sha256sum tools/round-34/{replay-gate.py,gate-config-mini.json,gate-config-naive.json} \
  tools/round-34/mini-fix/{mini-counter.py,expected.json,build.py,readers/structural.py} \
  tools/round-34/mini-fix/fixtures/*.mrec                                    # exit 0, all equal to R34-C2.pins
#   alpha d1de0e6f… beta a8547fcf… delta 79ff7036… epsilon 82f03f99… eta 5bcabeb2…
#   gamma ffb57ecd… theta b1f87d7c… zeta 19ff4074… expected 5ebb5349… build c6718051…

# scoring, 2026-10-25T07:19:25Z (one line per reader, exit 0 iff met_target)
/usr/bin/python3 -I -B tools/round-34/mini-fix/mini-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --control-reader <reader>
#   structural exit 0 matched 8; value_low16 exit 1 matched 4; name_cap20 exit 1 matched 7
#   zero_fields exit 1 matched 0; crash_exit3 exit 1 matched 0; garbage_stdout exit 1 matched 0

# gate ladder, 2026-10-25T07:19:41Z .. 07:19:52Z
python3 -I -B tools/round-34/replay-gate.py --root . --config $S/configs/<case>.json --json-out $S/receipts/<case>.json
#   positive-structural 0 | positive-value_low16 3 | positive-name_cap20 3 | positive-zero_fields 3
#   positive-crash_exit3 3 | positive-garbage_stdout 3 | positive-as-record_order_replay 3
#   positive-as-label_replay_full 3 | positive-as-string_scan 3 | below-positive-plus-meeting-shortcut 3

# copied-tree reproduction, 2026-10-25T07:20:26Z (cd $S/root-copy)
python3 -I -B tools/round-34/replay-gate.py --root . --config $S/configs/scratch-root-{relative,structural}.json
#   3 (value_low16) and 0 (structural)

# trust-boundary probes, 2026-10-25T07:20:25Z .. 07:21:33Z
python3 -I -B tools/round-34/replay-gate.py --root . --config $S/configs/{forged-selective,forged-exit7}.json   # 0, 0
python3 -I -B tools/round-34/replay-gate.py --root . --config $S/configs/{structural-plus-duplicate-path,config-target-lowered-4,counter-target4-with-defective-positive}.json  # 2, 3, 0

# pinned gate selftest, 2026-10-25T07:21:47Z
python3 -I -B tools/round-34/replay-gate.py --selftest                            # exit 0, 0 failures, 3/3 mutants killed
```

Artifacts: `$S/readers/` (5 probe readers + 3 forged counters + `mini-counter-target4.py` scratch copy,
9 files), `$S/configs/` (18 configs), `$S/receipts/` (19 gate receipts: 18 configs plus the
missing-config run), `$S/logs/` (18 files: 12 gate/stdout transcripts, 6 counter scores),
`$S/root-copy/` (tools copy, 1 probe reader). Probe reader hashes: `value_low16.py`
`87a579677eae5c4f50febaa053763884b346692b8e1e149e7f15f07f5b1400d8`, `name_cap20.py`
`7e4f8819f2bfc3ebe5952b226bdb4128eed2489b03bcffb080d91638fe4c4ac6`.

**Tooling record:** no installs or upgrades were needed or attempted (no pacman, no uv, no network);
the probes used `/usr/bin/python3` 3.14.8 and coreutils `sha256sum` only.

**Risks / blockers:** none blocking. Residual: F1/F3 are properties of the gate's design and should be
carried as stated boundaries rather than fixed inside a frozen instrument; nothing outside my scratch
and this report was written.

**Verdict:** R34-C2 anti-vacuity probe PASSES — a below-target positive control (7/8 included) forces
`REPLAY_GATE_UNEVALUABLE` exit 3, never CLEAN; the guarantee is conditional on the pinned counter
receipt and target (F3) and UNEVALUABLE masks a coincident REFUSED (F1), both conservative-only.
