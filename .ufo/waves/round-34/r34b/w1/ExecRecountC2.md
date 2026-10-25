# ExecRecountC2 — fresh-clone recount of R34-C2 and field-by-field diff

Seat: `L1Kaidoku34-2.ExecRecountC2` (leaf, read-only verification). Axis worked: depth (independent reproduction + falsifier probes of the receipt's own claims).
Claim under attack: **R34-C2** (capability acquisition, axis depth), frozen instruments at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`.
R34-C1 was not touched: its production reader and twelve carriers were not executed, read as programs, or scored. No ELF/fixture was executed as a program; readers were executed only as python child processes of the pinned counters.

**Headline: the production receipt reproduces byte-for-byte on a fresh clone (exit 0, all 30 fields equal, identical sha256).** Two claims *inside* the frozen claim record do not survive the probes: the `predicate_identity` assertion is false (two distinct sentences, not one), and the counter cannot detect a dropped green-surface shortcut class even though the kill rule forbids exactly that. Both are falsifiers of the instrument's own stated guarantees, not of the six-clause target.

---

## 1. Environment and reproduction

| # | UTC | command | exit | note |
|---|---|---|---|---|
| R1 | 2026-10-25T07:18:14Z | `mkdir -p /fast/scratch/hyaku/kaidoku-r34b/w1/ExecRecountC2 && git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin lane` | 0 | read-only clone, scratch only |
| R2 | 2026-10-25T07:18:14Z | `cd lane && git checkout -q c79bbe7b0959132b9873ff3431cf5eb313b58b33` | 0 | `git rev-parse HEAD` = `c79bbe7b0959132b9873ff3431cf5eb313b58b33`, `git status --porcelain` = 0 lines |
| R3 | 2026-10-25T07:18:24Z | `/usr/bin/python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out recap.json` | **0** | completed 07:18:26Z (2.7 s) |
| R4 | 2026-10-25T07:18:36Z | same as R3, `--json-out recap2.json` | 0 | determinism replay |
| R5 | 2026-10-25T07:18:48Z | `/usr/bin/python3 -I -B tools/round-34/replay-gate.py --root . --config tools/round-34/gate-config-mini.json --json-out green-rows.json` | 0 | per-class green rows |

Verdict line (R3, verbatim, single line):

```
GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-
```

Python: `/usr/bin/python3` (system). No tool was installed or upgraded for this seat — nothing was needed, so no tooling record applies.

Evidence: `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecRecountC2/lane/recap.json` (= `recap.json`), `.../lane/recap2.json`, `.../lane/green-rows.json`.

## 2. Pin verification (26/26)

All 26 `claims.claims[0].pins` sha256 values recomputed on the fresh clone at `c79bbe7b`: **26 checked, 0 mismatched**. Spot values:

| instrument | sha256 |
|---|---|
| `tools/round-34/c2-shortcut-gate-counter.py` | `41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72` (= pin) |
| `tools/round-34/replay-gate.py` | `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` (= pin) |
| `tools/round-34/gate-config-mini.json` | `4483f3852429b4390656a1d8235e1d0a676e4da1e7d7841f20bd2b575c12ac9c` (= pin) |
| `tools/round-34/gate-config-naive.json` | `72b1294171b58ecb276ce84edcff0698c750d9f5e4490a60253e9385086b1428` (= pin) |

Eight fixtures: sizes `{512}`, modes `{0o644}` — static bytes, never executed.

## 3. Field-by-field diff — fresh `recap.json` vs committed `after/c2-at-instruments.json`

Leaf-field diff (recursive over dicts/lists; key sets identical, 30 leaves). **DIFFERENT fields: 0.**

| field | receipt value | fresh value | result |
|---|---|---|---|
| `clauses.gate_present` | `True` | `True` | equal |
| `clauses.green_clean` | `True` | `True` | equal |
| `clauses.green_positive_meets_target` | `True` | `True` | equal |
| `clauses.mutants_killed` | `True` | `True` | equal |
| `clauses.red_refused` | `True` | `True` | equal |
| `clauses.selftest_clean` | `True` | `True` | equal |
| `exit` | `0` | `0` | equal |
| `finding` | `shortcut_gate_discriminates` | `shortcut_gate_discriminates` | equal |
| `gate_path` | `tools/round-34/replay-gate.py` | `tools/round-34/replay-gate.py` | equal |
| `gate_present` | `True` | `True` | equal |
| `green.exit` | `0` | `0` | equal |
| `green.line` | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` | same | equal |
| `green.positive_matched` | `8` | `8` | equal |
| `green.shortcuts_below_target` | `7` | `7` | equal |
| `green.verdict` | `REPLAY_GATE_CLEAN` | `REPLAY_GATE_CLEAN` | equal |
| `measured_revision` | `c79bbe7b0959132b9873ff3431cf5eb313b58b33` | same | equal |
| `met_target` | `True` | `True` | equal |
| `mutants_killed` | `3` | `3` | equal |
| `predicate` | `P34-shortcut-replay: the committed replay gate refuses the shape-only counter whose label-keyed memorization meets its target, …` | same (351 chars) | equal |
| `red.classes_over_target` | `["label-memorization"]` | `["label-memorization"]` | equal |
| `red.exit` | `2` | `2` | equal |
| `red.line` | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization` | same | equal |
| `red.verdict` | `REPLAY_GATE_REFUSED` | `REPLAY_GATE_REFUSED` | equal |
| `selftest_exit` | `0` | `0` | equal |
| `selftest_failures` | `0` | `0` | equal |
| `selftest_line` | `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3, "selftest": "replay-gate"}` | same | equal |
| `target.green_verdict` | `REPLAY_GATE_CLEAN` | `REPLAY_GATE_CLEAN` | equal |
| `target.mutants_killed` | `3` | `3` | equal |
| `target.red_verdict` | `REPLAY_GATE_REFUSED` | `REPLAY_GATE_REFUSED` | equal |
| `target.selftest_failures` | `0` | `0` | equal |

Whole-file identity (not just fields):

```
da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9  lane/recap.json
da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9  …/r34b/after/c2-at-instruments.json
```

`sorted`-key JSON with `indent=1` is identical, so the receipt is reproducible byte-for-byte. R4 replay: `cmp -s recap.json recap2.json` → exit 0 (`DETERMINISTIC=0`), i.e. two independent runs produce identical bytes.

## 4. Independent reproduction of the control set

Re-ran the counter with `--gate` pointed at the four committed control gates (read-only python; each run in the fresh clone under `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecRecountC2/lane/recontrols/`). Recursive diff against `controls/gate-*.py.json`: **the only differing field in all four receipts is `gate_path`** (relative path in the committed receipt vs the absolute path I passed) — 29/29, 29/29, 30/30, 30/30 remaining fields equal.

| control | UTC | my exit | verdict line | vs committed |
|---|---|---|---|---|
| `gate-always-clean.py` | 07:19:26Z | 1 | `GATE_COUNTER_MISS … clauses_failed=red_refused,selftest_clean` (selftest_failures=2) | equal except `gate_path` |
| `gate-junk-clean.py` | 07:19:26Z | 1 | `GATE_COUNTER_MISS … clauses_failed=red_refused` | equal except `gate_path` |
| `gate-no-positive-check.py` | 07:19:29Z | 1 | `GATE_COUNTER_MISS … mutants_killed=2 … clauses_failed=mutants_killed,selftest_clean` | equal except `gate_path` |
| `gate-vacuous-no-floor.py` | 07:19:32Z | 1 | `GATE_COUNTER_MISS … selftest_failures=1 … clauses_failed=selftest_clean` | equal except `gate_path` |
| do-nothing (my own gate-less root) | 07:19:39Z | **2** | `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad…` | same branch/finding/exit |

Note on the committed do-nothing receipt: it was produced with `--gate tools/round-34/absent-gate.py` (a path that does not exist) against the frozen revision, so it exercises `gate_absent` through the path check. I reproduced the same branch independently by copying the clone, deleting `tools/round-34/replay-gate.py`, and running the **default** gate path: same `finding=gate_absent`, same exit 2. The committed control is therefore faithful but slightly weaker than "root with no gate"; my run closes that gap.

## 5. Structural attestation of the six clauses (not just the aggregate)

Green gate `green-rows.json` shows 8 registered classes: `structural` matched 8/8 `met_target=true`; `all-false` 0, `size-keyed` 1, `fixed-slice` 0, `digest-keyed` 0, `string-scan` 0, `record-order-replay` 0, `label-memorization` 0 — 7 shortcuts below target 8, matching `green.shortcuts_below_target=7`.

Red gate: `label-memorization` is the single class over target under the shape-only `naive-counter`; `classes_over_target=["label-memorization"]`, exit 2.

Selftest arithmetic attested by reading `tools/round-34/replay-gate.py` + the printed `cases: 12`: 6 `SELFTEST_CASES` + 2 config-refusal cases (`two-shortcuts-unevaluable`, `duplicate-class-unevaluable`) + 1 `positive-absent` + 3 mutant-kill runs = 12. The three mutants patch exactly the three branches the predicate names: `if over: → if False:` (refusal), `if not positive["met_target"]: → if False:` (positive control), `len(shortcuts) < MIN_SHORTCUTS → ` (shortcut floor, `MIN_SHORTCUTS=3`). Each is killed by the case with the expected exit mismatch.

## 6. Attacks and falsifiers (probes on scratch copies only)

**F1 — `predicate_identity` in `claims.json` is false: there are two distinct predicate sentences, not one.**
- Sentence **A** (237 chars, sha256 `7c6c17f0cca6c680…`): `P34-shortcut-replay: a finite structural-decoding counter is frozen only after registered structure-blind shortcut readers are scored under the counter's own predicate and none meets the target, while a registered structural reader does.` Carriers at the freeze commit: `tools/round-34/gate-config-mini.json`, `tools/round-34/gate-config-naive.json`, and `claims.json`'s own `claims[0].predicate`.
- Sentence **B** (351 chars, sha256 `8340aea51154fc0e…`): `P34-shortcut-replay: the committed replay gate refuses the shape-only counter whose label-keyed memorization meets its target, …`. Carriers: `tools/round-34/c2-shortcut-gate-counter.py` (`PREDICATE`) and **every receipt** — `after/c2-at-instruments.json` `predicate`, `controls/do-nothing.json` `predicate`, my `recap.json`.
- `A == B` is `False`. `claims.json` asserts "The same sentence is the gate config's `predicate` field, the C2 counter's PREDICATE constant and the receipt label"; the assertion fails twice: (i) config/counter carry different sentences; (ii) the receipt has no `label` field at all — its labels are the `REPLAY_GATE_*` verdict strings. Net effect: the production receipt's `predicate` field does not quote the frozen predicate it is supposed to bind; a reader diffing `claims.json.predicate` against the receipt's `predicate` gets a mismatch. This is a claim-record defect, not a production-run defect, and it is exactly the kind of identity the predicate-identity clause exists to prevent.

**F2 — `measured_revision` is an unverified echo.** The counter copies `--rev` into the receipt and never checks it against `git rev-parse HEAD` or the pins (grep of the script: `measured_revision` is assigned from `args.rev` only; no `git` call anywhere in the file). Probe: same clone at `c79bbe7b`, same instruments, `--rev ec3125ad3d130d92f888a4128dfaa2982f36fff7` (the round's base revision):
`GATE_COUNTER_OK finding=shortcut_gate_discriminates … clauses_failed=-`, exit **0**, receipt identical to `recap.json` **except** `measured_revision`. Evidence: `lane/recap-bogusrev.json` (07:18:50Z). Consequence: "the receipt says revision R" is not evidence that R was measured; it is evidence that the operator typed R.

**F3 — the counter cannot detect a dropped green-surface shortcut class, the exact hazard the kill rule forbids.** Kill rule text: "no shortcut class may be dropped to reach CLEAN." Probe: scratch copy `lane-drop`, removed the `label-memorization` entry from `gate-config-mini.json` (7 → 6 registered shortcuts; gate floor `MIN_SHORTCUTS=3` still satisfied), ran the unmodified counter against it:
`GATE_COUNTER_OK … green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`, exit **0**, `green.shortcuts_below_target` = **6**. Evidence: `lane-drop/drop.json` (07:19:07Z). Cause: the `green_clean` clause tests only `green.exit==0 and verdict==REPLAY_GATE_CLEAN`, and `green_positive_meets_target` tests only `structural.matched==8`; nothing compares the registered class set to an expected inventory, and `green.shortcuts_below_target` is recorded but never asserted (it is absent from `clauses`, and it is absent from `TARGET`). The counter also performs no pin check, which is why the mutated config was accepted silently.

**F4 — the red side is defended, the green side is not.** Same drop applied to `gate-config-naive.json` (`lane-reddrop`, 07:19:54Z): `GATE_COUNTER_MISS … red=REPLAY_GATE_CLEAN … clauses_failed=red_refused`, exit 1. So the class that carries the refusal test protects itself: remove it and the red side stops refusing and the claim misses honestly. Only the green inventory is unprotected (F3). The residual risk is therefore narrow and nameable: an operator who drops exactly one green-registered shortcut gets a green CLEAN receipt with a smaller floor and no failing clause.

**F5 — the green surface is record-level, not byte-integrity.** Two one-byte mutations of `mini-fix/fixtures/alpha.mrec` under scratch copies:
- offset 100 (`0x64`, inside the zero padding after the 3-record array; header shows `records_off=0x10`, `names_off=0x28`, 3×8-byte records ending 0x28): XOred `0x01` → `GATE_COUNTER_OK … clauses_failed=-`, exit **0**, `green_positive=8` unchanged (07:19:54Z, `lane-tamper/tamper.json`). Semantically inert because the byte is padding.
- offset 0 (`'M'` of the `MREC` magic): XOred `0x01` → `GATE_COUNTER_MISS`, `green=REPLAY_GATE_UNEVALUABLE`, `red=REPLAY_GATE_UNEVALUABLE`, `green_positive_matched=None`, `clauses_failed=green_clean,green_positive_meets_target,red_refused`, exit **1** (07:20:03Z, `lane-tamper0/tamper0.json`). The structural reader's `data[0:4] != b"MREC"` guard turns a broken magic into UNEVALUABLE, which the counter correctly refuses.
  Reading: the gate's green verdict says "records decode as expected", not "the fixture bytes are the frozen bytes". Pin verification of the eight fixtures (done separately in §2, 8/8 match) is what supplies byte identity; the gate itself does not carry it.

**F6 — control receipts are workdir artifacts, not revision-bound.** `git ls-files .ufo/waves/round-34/r34b` at `c79bbe7b` returns **exactly one** file, `claims.json`. `after/`, `before/`, `controls/` and `assimilation/` are untracked in the lane workdir (`git check-ignore` returns nothing, so they are simply uncommitted). The freeze commit therefore binds instruments and claims, but not the receipts the claim cites; anyone can add or overwrite `after/c2-at-instruments.json` without changing a revision. My recount reproduces its bytes, so the receipt is *true* at `c79bbe7b`, but it is not *anchored* to `c79bbe7b` by the VCS. This is the strongest remaining gap after F1–F3.

Also checked and clean: `before/c2-at-base.txt` reads `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad…` — consistent with the claim's before-state; the counter's `run()` environment is `PATH=/usr/bin:/bin, HOME=/tmp, LANG=C`, so no ambient `PYTHONPATH` or user site could affect the gate or the readers; the twelve carriers of the stopped R34-C1 were not touched at any point.

## 7. Risks / limits of this seat

- Lane VCS untouched: no `git add/commit/stash/checkout/reset/pull/push` in the lane; every checkout, copy, mutation and run happened under `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecRecountC2/` (`lane`, `lane-drop`, `lane-reddrop`, `lane-tamper`, `lane-tamper0`, `lane-nogate`, `lane/recontrols`).
- Only the lane repo path `git clone` was read; no network used at all.
- F1/F3/F6 are defects in the *frozen claim record and its wiring*, not in the six-clause measurement: at `c79bbe7b`, with pinned instruments, all six clauses are genuinely true and the target is genuinely met. I did not re-score, relabel or widen the claim, and I recommend no post-freeze change to target, counter, predicate text or registered classes — the honest options are (a) record F1/F3/F6 as known gaps of the frozen instrument in the round text, or (b) stop the claim as a measure defect if the L1 judges the predicate-identity breach material.
- Draft text only; nothing outside this report was written.

**Verdict: `RECOUNT_C2_REPRODUCES` — fresh clone at `c79bbe7b`, exit 0, receipt sha256 `da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9` identical to the committed after-receipt across all 30 fields; 26/26 pins match; controls reproduce (gate_path-only diffs). Three falsifiers of the claim record's own wording, none of the six clauses: `predicate_identity` false (two sentences, A≠B, no receipt `label` field), `measured_revision` an unverified echo, green-surface shortcut drop undetected (`clauses_failed=-` with `shortcuts_below_target=6`), plus receipts unanchored in VCS.**
