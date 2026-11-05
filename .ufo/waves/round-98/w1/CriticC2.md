# CriticC2 — falsification of R98-C2 (allow-list calibration)

Seat: CriticC2 (critic). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Rev under test: L = 72346895a35a74af18151b125934fa0c09fe1e3c (verified via `git -C $S/clone rev-parse HEAD`).
Clone: `git clone --shared <lane> $S/clone && git -C $S/clone checkout --detach 72346895a35a74af18151b125934fa0c09fe1e3c`; `rev-parse --show-toplevel` = clone path before writes. Clone and scratch trap-deleted after scoring. No mutating git in the lane. No tools installed or upgraded. No host change.

## Scoring commands (all run from the clone; frozen predicate `tools/round-98/allowlist-check.py`, rev L)

Form: `python3 -I -B tools/round-98/allowlist-check.py --counter <path> --rev 72346895a35a74af18151b125934fa0c09fe1e3c --work <w> --json-out <j>`

| Counter | Exit | Label | Admitted? |
|---|---|---|---|
| base: `stop-boundary-repair-battery-v8.py` (honest, unmodified) | 0 | `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1` | yes (control matches frozen label) |
| control: `round-97/stop-boundary-repair-battery-v7.py` | 1 | `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1` | no (matches frozen control) |
| F1 `c2forge1-v7-accept-all.py`: count_problems returns [] always (v7 otherwise) | 1 | `legs passed 2 of 4; public 1; real14 1; stub9 0; extra 0` | no |
| F2 `c2forge2-v8-verify-liar.py`: v8 with verify_receipt short-circuited to `{ok: True}` | 0 | `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1` | **YES (forgery admitted)** |
| F3 `c2forge3-public-lie.py`: prints `selfverify ok=True reasons=0` and `met True exit 0`; runs no battery, writes no receipt | 0 | `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1` | **YES (forgery admitted)** |
| F4 `c2forge4-refuse-bogus-only.py`: count_problems refuses only literal key `bogus` | 1 | `legs passed 3 of 4; public 1; real14 1; stub9 0; extra 1` | no (stub9 catches it) |
| F5 `c2forge5-size-fit.py`: count_problems accepts any dict of length 14, refuses others | 0 | `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1` | **YES (forgery admitted)** |
| F6 `c2forge6-missing-blind.py`: missing-key and type checks removed | 1 | `legs passed 3 of 4; public 1; real14 1; stub9 0; extra 1` | no (stub9 catches it) |
| F7 `c2forge7-unevaluable.py`: raises at import | 2 | unevaluable (stderr `RuntimeError`) | no (fails closed) |

Receipts: `.ufo/waves/round-98/w1/CriticC2/{base-v8,ctl-v7,c2forge1-v7-accept-all,c2forge2-v8-verify-liar,c2forge4-refuse-bogus-only,c2forge5-size-fit,c2forge6-missing-blind,f3,f7}.json` (f3 and f7 are the names used for F3 and F7 in the scratch run). Forge sources: `.ufo/waves/round-98/w1/CriticC2/forges/` (diffs against the frozen counter for F1, F2, F4, F5, F6; full files for F3, F7).

Baseline check: base v8 reproduces the frozen label, exit 0; v7 control reproduces `legs passed 1 of 4 ...`, exit 1.

## Forgery mechanics (why three are admitted)

- **F2 and F3 admit through the public leg.** `allowlist-check.py` computes `public = rc==0 and "selfverify ok=True" in stdout`. That is the candidate's own self-printed string. The predicate never reads a receipt the candidate's verifier produced, and never re-runs the frozen `verify_receipt` on it. F2 disables the verifier and still produces a genuine honest public receipt, so the score is green. F3 prints the string without running anything.
- **F3 also escapes the other three legs.** When the public run writes no receipt (`public-receipt.json` absent; I confirmed it is absent for F3), `allowlist-check.py` silently substitutes the committed round-97 counts `.ufo/waves/round-97/l1/public/v6-public.json`. So `real14`, `stub9` and `extra` are evaluated on fixed honest counts, not on anything the candidate produced. A counter that never runs scores 4 of 4.
- **F5 admits through a size test.** I probed F5's `count_problems` directly with 14 junk keys (`j00`…`j13`): it returns `[]` (accepted). The honest v8 returns 28 reasons for the same dict. The predicate's `real14` uses the true key set (accepted, correct), `stub9` uses a 9-key dict (refused by length alone), and `extra` uses a 15-key dict (refused by length alone). None of the three legs tests key identity. Downstream, if F5 were used, `verify_receipt` would reach `recompute_label(counts)` and crash on `counts["repaired"]`, so the forged counter would not produce a green receipt in practice. The predicate still admits it.
- F1, F4, F6 are caught. F1 (accept-all) fails `stub9` and `extra`. F4 and F6 fail `stub9`, so the nine-key stub test is real for those forgeries.

## Judgment: does C2 measure the routed defect?

The routed defect (round-97 closure): an honest public run must be accepted, and the nine-key stub must be refused. The predicate's count-level legs do measure part of it. `real14` catches a counter that refuses honest 14-key counts. `stub9` catches an accept-all counter, a bogus-only counter and a missing-key-blind counter. `extra` catches an accept-all counter and a size-blind counter (F1, F4, F6 fail it, F5 passes it only because it refuses 15 keys by length).

It does not measure the public leg as a check on the defect. "Honest public run accepted" is established only by the candidate's own stdout string, so F2 and F3 pass it without any honest run existing. The predicate is therefore weaker than the stated defect. It measures count-function behaviour on mostly-fixed inputs, plus a self-attested public string. It does not measure the verifier, and it does not require a receipt that the public run wrote and that the frozen verifier re-checked.

Verdict on R98-C2 as frozen: it reproduces (honest v8 exit 0, v7 control exit 1), so the frozen label holds for the honest candidate. But it admits three forgeries (F2, F3, F5), so it is not a sufficient falsifier of a counter that fakes the honest public run. I am not re-scoring or re-freezing.

## Findings (routed; no edits to frozen files)

1. **F3 (high) — public leg is self-attested.** A counter that prints `selfverify ok=True reasons=0` with no battery and no receipt scores 4 of 4 and exit 0. Evidence: `.ufo/waves/round-98/w1/CriticC2/f3.json` (public_rc 0, counts_source = v6-public.json fallback, public-receipt absent). Smallest safe correction for the next round: the public leg requires a receipt written by this run, re-verified by the frozen verifier loaded from the frozen counter at the rev (not the candidate module). A missing receipt means `public 0`, with no fallback substitution for the public leg.
2. **F2 (high) — verifier not measured.** A candidate whose `verify_receipt` always returns ok scores 4 of 4. Correction: the frozen predicate should call the frozen `verify_receipt` on the receipt the public run wrote, and treat a candidate-supplied verifier as untrusted.
3. **F5 (medium) — key identity not measured.** A 14-key dict with wrong names is accepted by a length-only `count_problems`. Correction: add a leg asserting `candidate.COUNT_KEYS` equals the verdict's fourteen-key set and that a 14-key dict with one key renamed is refused.
4. **Fallback substitution (medium, design).** Silent substitution of committed counts when the public receipt is absent lets three legs pass for a counter that produced nothing (F3). The fallback was a deliberate choice so a failing public leg cannot zero the others. The coupling is what admits F3, so the fallback and the self-attested public leg should be fixed together.

Scope limits: I falsified only the frozen C2 predicate, not C1. I did not re-run any C1 command.

## Commands run (exit code and label)

- `git clone --shared` + `git checkout --detach 72346895…` + `rev-parse --show-toplevel` / `HEAD`: 0 (HEAD = 72346895a35a74af18151b125934fa0c09fe1e3c)
- `python3 -I -B -m py_compile` on the six forges: 0
- `allowlist-check.py` on F7 → exit 2; F3 → exit 0; F1/F2/F4/F5/F6 (concurrent) → exit 1/0/1/0/1 as in the table; base v8 → exit 0; v7 control → exit 1
- F5 14-junk-key probe (direct `count_problems` call): F5 → `[]`; v8 → 28 reasons
- `git status --porcelain` on the frozen counters in the clone: clean

Tools installed or upgraded: none.

Verdict: C2 reproduces on the honest candidate and the v7 control, but it admits forgeries F2, F3 and F5. The public-run leg is self-attested, so the predicate is weaker than the routed defect.
