# ReviewerInstruments — round-96 w1 report (surgical correctness review of the round-96 instruments)

Reviewed: `tools/round-96/*` at lane HEAD `3baac2ef4b9b2830d299125b8184ca06d9e6584d`
(declaration `e4d1f7de`, base `0ea695e8`). Working tree byte-identical to HEAD for
`tools/round-96` (`git diff HEAD --stat -- tools/round-96` → empty), so line numbers below
are both HEAD and worktree. Attack log with per-attack evidence:
`.ufo/waves/round-96/w1/ReviewerInstruments/attack.md`. Scratch
`/fast/scratch/hyaku/kaidoku-r96/ReviewerInstruments/` (clone + selftest work dirs), removed
at the end of the seat. No lane file written except the two named seat paths. Python
3.14.8; no tools installed (none needed).

## Verification performed (all commands run at HEAD in the shared clone)

| Check | Command (abbreviated) | Result |
|---|---|---|
| Pins vs HEAD | sha256 over all 60 paths in `.ufo/waves/round-96/pins.sha256` | 0 mismatches |
| Compile | `py_compile` × 8 instruments | 8/8 ok |
| Mutant table | find-count + `compile()` on each replaced file, M0-M10 | 11/11 find-once, compile ok |
| v6 selftest | `python3 -I -B tools/round-96/stop-boundary-repair-battery-v6.py --selftest --work $S/v6-st` | exit 0, cases=13 failures=0 |
| kill-rule selftest | `python3 -I -B tools/round-96/kill-rule-v2.py --selftest --work $S/kr-st` | exit 0, cases=4 failures=0 |
| met-None probes | `verify_receipt` on met_target-absent / null receipts | ok=True (the HIGH-1 finding) |
| resolve_rev | `HEAD`, `"HEAD "`, bogus, `HEAD~1` | resolves / None / None / resolves |
| Fixture isolation | 6 fixtures vs honest template + pins.sha256 | each violates exactly one binding |

## Findings by severity

### HIGH

**H-1. `verify_receipt` admits receipts with `met_target` absent or null — a seventh
unbound-field class (M95-g class).**
`tools/round-96/stop-boundary-repair-battery-v6.py:170-172` only tests
`rec.get("met_target") is True` and `is False`; a receipt omitting the field (or carrying
`null`) skips both directional bindings and verifies `{'ok': True, 'reasons': []}`
(reproduced from the HEAD clone on honest label/counts/pins/revision/head). `main` then
prints `met None … exit 0` (v6:393) and exits 0 — a green exit whose receipt asserts no met
direction at all, i.e. the printed verdict is unbound. No frozen fixture class, mutant, or
K-check covers it, so the frozen claims and the committed green receipts
(`honest-pos.json`, `c1-at-decl-worktree.json`) are NOT invalidated; the six frozen
forgery classes still refuse with exactly their intended single reasons. But the round's
own doctrine — "every field the receipt claims is bound" — is not fully met by its own
successor counter.
Minimal fix sketch (v6:170-172):
```python
if rec.get("met_target") not in (True, False):
    reasons.append("met-not-typed")
```
placed outside the `elif not schema:` branch so it fires regardless of label state; the six
fixtures keep exactly-one-reason (their met_target is True/False). Companion work for a
later round (frozen-table edit, not now): 7th forgery `forge-met-absent` →
`met-not-typed`, and an M11 hard-coding the None-pass.

### MEDIUM

**M-1. `build_copy` never checks that the replaced file still compiles.**
`tools/round-96/kill-rule-v2.py:297-318` enforces find-once (306-309) but nothing checks
the replaced bytes (310-316). The declaration's table property "every replaced file still
compiles" is therefore unenforced at run time: a syntax-breaking replace would be "killed"
by K-selftest rc≠0 — indistinguishable from a genuine gate-coverage kill, silently
inflating the calibration count the claim exists to protect. Static check at HEAD: 11/11
mutants compile, so the frozen run is not affected today; this is an enforcement gap, not a
current-bytes defect.
Fix sketch: after the replace, `compile(data, dst, "exec")` (raise `ValueError` on
SyntaxError), mirroring the find-once guard.

**M-2. kill-rule-v2 does not bind its own green exit to a verified receipt.**
`tools/round-96/kill-rule-v2.py:494-497`: `--json-out` is optional for the kill rule
itself; the receipt is written when given but never re-read, and the printed
label/met/exit derive from `met` regardless. The round's M95-g closure rule — "a green
verdict exists only through a verified receipt" — is enforced by v6 for the battery but not
by the round's flagship counting command for its own receipt. Mitigations: a failed write
raises (non-zero crash, fail-closed), and the frozen command passes `--json-out`. Still an
unforced asymmetry in the very instrument that polices the doctrine.
Fix sketch: require `--json-out` on the public path (exit 2 `receipt-required`, same as
v6) and re-read + schema-check the written receipt (label matches the counts dict,
met_target is bool, world_revision == HEAD) before returning 0.

### LOW

- **L-1** `count_problems` conflates explicit `null` with a missing key (v6:135):
  `fresh_scored: null` → `counts-missing-key:fresh_scored`. Typed refusal preserved; reason
  string slightly lies. Fix: distinguish `k not in counts` from `counts[k] is None`.
- **L-2** `count_problems` ignores keys outside COUNT_KEYS (v6:128-138); label unaffected;
  schema laxity only.
- **L-3** `write_receipt` fsyncs the file but not the directory (v6:94-96; kill-rule-v2:97-99;
  symlink-probe-v2:72-74): the rename is not crash-durable. The stated contract "Complete
  JSON or absent" still holds (content fsync + atomic replace), so this is a strict
  durability upgrade, not a contract break: `os.open(d, os.O_DIRECTORY)` + fsync after
  replace.
- **L-4** `r95-unbound-at-base.py:110-118`: the nojson leg's work dir is hardcoded from
  `HYAKU_SCRATCH` (no `--work` arg), and `receipt_written: False` is an asserted constant,
  not a measurement (structurally true — v5's main has no receipt path without `--json-out`
  — but the receipt field claims an unchecked fact).
- **L-5** `probe-writer-legs.py:8` docstring says "a writer path that does not exist", but
  `run_leg` (line 48) passes the existing `identity_noop`; the docstring's next sentence
  describes the real mechanism (noop rejects the battery args). Doc-only.
- **L-6** `symlink-probe-v2.py:101`: `subprocess.run(..., timeout=1200)` TimeoutExpired is
  uncaught → traceback instead of a typed refusal; fail-closed direction preserved (no
  receipt → K-probe not-ok).
- **L-7** Un-hardened receipt writers outside the claim counters: `legacy-kill-rule.py:140-144`
  and `fresh-source2-check.py:124-127` use plain `open(..., "w")`. Before-arm/supplementary
  tools, low stakes; inconsistent with the round's writer doctrine.
- **L-8** v6 `_selftest`: `full()` reads `name_of[0]` (v6:253) assigned later (first at 258);
  NameError if `full()` were called earlier. Naming-only; not triggerable in the 13 cases.

## Verified clean (item checklist, all grounded)

1. **v6 writer**: mkstemp/fsync/os.replace/cleanup correct; planted-tmp immunity and
   unknown-type-raises-clean exercised green by the selftest.
2. **resolve_rev**: whitespace rejected pre-git; symbolic names accepted (HEAD →
   3baac2ef…, HEAD~1 → e4d1f7de…); unresolvable → None (fail-closed everywhere it is
   consumed: `revision-unresolvable`, `head-not-bound`).
3. **count_problems**: bool rejection explicit (v6:137); typed reasons for missing/non-int;
   L-1/L-2 nuance only.
4. **verify_receipt exactly-one-reason**: all six committed fixtures violate exactly one
   binding (cross-checked against pins.sha256 and the honest template); refusal reasons
   match `mutants.json forgery_reasons` one-for-one.
5. **main mandatory --json-out + fail-closed**: refuse-before-scoring exit 2
   (`receipt-required`, selftest case green); `code = 1` gate at v6:387-388; the disclosed
   supersession red evidence (`honest-pos-red-head-not-bound.*`) is exactly this gate
   firing on the pre-fix bytes.
6. **Receipt field order**: head (378) and repair/counter/verdict pins (371-377) recorded
   before `write_receipt` (383) and `verify_receipt` (384-386).
7. **Selftest 13 cases**: each asserts what its name says; the usage case restores
   `v3.score` in `finally` (v6:328-337); 13/13 ok, exit 0.
8. **Mutant application**: find-once enforced (kill-rule-v2:306-309); 11/11 apply once and
   compile; copy deps `[v3, round-92 battery, round-92 battery-v2]` are the exact
   transitive module-level import closure (v3:77 → b92:62 → battery-v2; R87/R88 lazy).
9. **c_selftest conventions**: counter `--selftest --work d` (flag), agreement `--selftest
   d` (value; agreement main:262-265) — the supersession split correctly encoded
   (kill-rule-v2:122-131).
10. **c_verify_forgeries pins**: `counter_pins` hashes root-relative `mod.TOOL`/`mod.V3_TOOL`
    and `--repair-pin` (default round-92 upx repair) — matching the fixtures' baked repair
    digest; exact mode for the six new fixtures, refusal-only for the four r95 ones.
11. **c_agreement_exact**: forgery legs at `--rev R95_WORLD_REV` (b5331db1…), honest leg at
    `--rev R95_INSTRUMENT_REV` (4bda1d1d…) against the committed r95 honest receipt;
    exits 1/0 semantics correct.
12. **c_dmain**: pos exit 0; shortrev/rewrite/notrecomp non-zero; nojson exit 2; score
    restored in finally (kill-rule-v2:245). Kill matrix closes: M3→shortrev, M4→shortrev,
    M6→shortrev (via head-not-bound — the recorded head is computed by main, not
    claimable), M5→K-selftest, M1→K-selftest planted-tmp, M2→K-fsync, M7-M9→K-agreement
    F3/F1/pos, M10→K-probe.
13. **c_fsync**: os.fsync monkeypatched and restored in finally (258-262); ≥1 kills M2.
14. **c_probe**: timeout 1800; consistency predicate `(verdict == "hardened") ==
    (victim_intact and receipt_valid)` and `met is truth`; unreadable receipt → not-ok.
    Honest leg runs the round-94 writer, whose predictable `path + ".tmp"`
    (round-94:60-67) really follows the planted link — so the honest leg is the negative
    case and M10's hard-coded `hardened`/True is genuinely inconsistent → killed.
15. **Identity control**: M0 runs the full counter check set; `met` requires
    `identity_not_killed`.
16. **Label arithmetic vs counts dict**: 10/10/10/3/1/1 consistent between label string,
    counts dict (kill-rule-v2:479-489), and the committed green receipt
    `c1-at-decl-worktree.json`.
17. **fresh-source2-check (S321)**: sha-pin gate exits 2 before any work on drift;
    determinism, public-carrier collision, intact identity, and fail-closed near/far
    denominators all correct; consistent with the committed
    `pre/s321-fresh-source2-at-base.json` (2/2 repaired, 2/2 far-refused, 1/1 intact).

## Residual risk and verification gaps

- I did not re-run the full kill rule (mutant arm + K-probe with the real round-94 battery)
  or the honest v6 battery — out of my item's scope (selftests + surgical review); the
  committed greens (`c1-at-decl-worktree.json`, `honest-pos.json`) plus my static/pin
  checks cover the frozen predicates. Main can re-derive with the frozen commands.
- H-1 is not covered by any frozen fixture/mutant; until a successor counter binds
  met_target's type, a consistently-lying writer can ship a green receipt lacking the met
  direction. Frozen-table work (new forgery class + mutant) is next-round material, not
  this round.
- Selftests were run under Python 3.14.8 only; no other interpreter was exercised.
- K-probe's honest leg depends on the round-94 writer staying byte-identical — it is
  pin-listed and my pin check confirms it matches HEAD.

Report: .ufo/waves/round-96/w1/ReviewerInstruments.md
