# ReviewerV8 — review of stop-boundary-repair-battery-v8.py and allowlist-check.py (R98-C2)

Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. B=d0aebc2886…, F=69c581c7c…, L=72346895a….
Clone: `git clone --shared <lane> $S/clone && git -C $S/clone checkout --detach 72346895a35a74af18151b125934fa0c09fe1e3c`
→ `rev-parse HEAD` = 72346895a35a74af18151b125934fa0c09fe1e3c; `rev-parse --show-toplevel` = the clone dir. Verified before any write.
Runtime: Python 3.14.8; /fast had 405G free. No LSP device is mounted in this seat, so semantic checks below are code reads named by line plus executed runs, not LSP proofs.

## 1. Static: v8 vs v7 diff (`diff -u` on the two lane files, exit 1=differs)

The delta is confined to:
1. `COUNT_KEYS`: nine label keys → fourteen (+fresh_far, +fresh_far_refused, +fresh_repaired, +refused, +silent); new `NINE_LABEL_KEYS` (the old nine) used only by the new selftest case.
2. `TOOL` constant path rename (r97→r98) and selftest scratch default `kaidoku-r97/selftest-v7` → `kaidoku-r98/selftest-v8` (benign, part of the rename).
3. Selftest fixture `counts` gains the five new keys; new case `verify-catches-nine-key-stub` expecting exactly `counts-missing-key:` on fresh_far/fresh_far_refused/fresh_repaired/refused/silent.
4. Docstrings/comments only. No function-body logic change; `verify_receipt`, `write_receipt`, `main` bodies are identical.

## 2. COUNT_KEYS equals the key set v3.score emits — code AND run

Code: `tools/round-93/stop-boundary-repair-battery-v3.py:291-306` builds `counts` with exactly the 14 literals
scored, repaired, wrong, unsafe, refused, silent, intact, far, far_refused, fresh_scored, fresh_repaired, fresh_roundtrip, fresh_far, fresh_far_refused.
v8:60-63 `COUNT_KEYS` is the same 14 (set-equal; order differs, irrelevant to `count_problems`).
Note: the v8 docstring cites "v3.score ... lines 288-300"; the dict actually spans 291-306 — citation drift only, no defect.

Run (clone at L, cwd=clone): `python3 -I -B tools/round-98/allowlist-check.py --counter tools/round-98/stop-boundary-repair-battery-v8.py --rev 72346895a35a74af18151b125934fa0c09fe1e3c --work $S/c2 --json-out $S/c2-receipt.json`
→ exit 0, `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1 met True` (wall ≈4.5 s).
The public leg's receipt `$S/c2/public-receipt.json` has counts of exactly 14 keys, and a scripted comparison printed
`COUNT_KEYS==receipt keys: True`, `receipt keys==v3 literals: True`. Confirmed both ways.
`real14=1` in the label is the counter's own accept of that real emitted counts — the leg the spotcheck demanded.

Control (v7 unchanged, same command form with `--counter tools/round-97/stop-boundary-repair-battery-v7.py`, work $S/c2-v7ctl)
→ exit 1, `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1 met False`; public_stderr byte-equal to the frozen
pre receipt `.ufo/waves/round-98/pre/c2-v7-control.json` (five `counts-extra-key:` lines), and `counts_source` is the
real v7 receipt (fallback never fired). Matches the contract control sentence exactly, field-level (label/exit/public_rc all True vs frozen).

Selftest: `python3 -I -B tools/round-98/stop-boundary-repair-battery-v8.py --selftest --work $S/selftest` → exit 0,
`SELFTEST cases=24 failures=0`, including `selftest verify-catches-nine-key-stub: ok`. Matches the L1 executor report.

Field compare vs frozen L1 receipt `l1/scores/c2-at-72346895a….json`: label, met, exit(0), public_rc(0), rev, counter all equal;
`counts_source` = my real public receipt, not the `.ufo/waves/round-97/l1/public/v6-public.json` fallback. Honest-run path exercised end-to-end.

## 3. allowlist-check leg audit vs its docstring

- `public`: runs the candidate's real battery command (`--expect <cand.v3.FROZEN_LABEL> --json-out rec_path`) and gates on rc==0 + `selfverify ok=True` in stdout. For any candidate shaped like v7/v8, exit 0 exists only through `verify_receipt` (v8 main: `if code == 0 and not selfverify["ok"]: code = 1`), so `public` does go through verify_receipt on the honest path.
- `real14`: `cand.count_problems(counts)` on the emitted/receipt counts — measures exactly the docstring sentence.
- `stub9`: nine-key projection refuses with ≥1 reason on v8 (five missing keys); passes on v7 (its own allow-list) — which is why the control scores stub9=0, correct per the docstring sentence.
- `extra`: `+bogus` key refused on both. Correct.
- Predicate: `TARGET` (`allowlist-check.py:39`) is byte-equal to the plans/round-98-claims.md sentence (plan lines 41-42): `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1`. `met = label == TARGET`; exit 0 iff met. Same sentence.

## 4. Findings

- F1 (medium, frozen-instrument design, routed for a future round — not edited, file is frozen): the fallback counts source can mask a stdout-lying candidate. If a candidate prints `selfverify ok=True`, exits 0, and writes NO receipt (or a receipt whose `counts` is not a 14-key dict), `counts` falls back to the committed `.ufo/waves/round-97/l1/public/v6-public.json` (14 keys), so public=1 while real14/stub9/extra are computed from committed data — a 14-key-allow-list candidate reaches 4 of 4 with its public receipt never schema-checked. On honest failures the fallback never fires (both my v8 run and the v7 control had `counts_source` = the real receipt; the docstring's stated purpose — a failing public leg must not zero the other three — is met for honest candidates). Concrete fix: refuse `met` when `counts_source != rec_path`, or when public==1 but rec_path is absent.
- F2 (low, plan gap): plans/round-98-claims.md's "Not claimed" list names routed defects 3–6 and 7 but omits routed defect 2 (kill rule honest leg `c_dmain` nine-key stub). `git log d0aebc2886..72346895a -- tools/round-97/kill-rule-v3.py` is empty (exit 0, no commits), so defect 2 stays open and unacknowledged in the plan's open list.
- F3 (info): `subprocess.run(..., timeout=3600)` in allowlist-check is unguarded; a hung candidate raises TimeoutExpired → traceback, nonzero exit, no json-out receipt. Fail-closed (predicate cannot be met), cosmetic ledger gap only.
- F4 (info): v8's selftest-default scratch path r97→r98 is inside the rename; no bystander behavior change found elsewhere in the diffstat (B..L = 10 files, 1683 insertions, 0 deletions, all under round-98/pre/ + plans/ + tools/round-98/).

## 5. Round-97 routed defects 1–7 (spotcheck §7) — disposition this round

1. v7 COUNT_KEYS fourteen + nine-key-stub red fixture — CLOSED: v8 allow-list is set-equal to v3's emitted keys (code + run), selftest case green, and the frozen counter adds legs real14/stub9 that feed the producer's real output.
2. Kill-rule honest leg must run the real verdict, not a nine-key stub — OPEN, and unacknowledged in plans/round-98-claims.md (see F2); kill-rule-v3.py untouched B..L.
3. `ownrec` slot measured + key in green receipt — OPEN (declared open in the plan); untouched.
4. Imported pins bound at the named revision; absent file → typed refusal — OPEN (declared open). v8 retains v7's degrade: a failed `blob_sha256` sets `pins_at_rev=None` and verification falls back to live-byte pins, not a typed refusal.
5. K-ownrun recursion bound; real K-cwd leg — OPEN (declared open).
6. Before-side receipts from a clean checkout of the base — OPEN (declared open).
7. Local-source gate FAIL on S082/S302/S321 — OPEN (declared open), pre-existing debt.

## Verdict

R98-C2 instrumentation verified: v8's COUNT_KEYS is exactly the 14-key set v3.score emits, proven by code read and by a
clone run at L whose public receipt keys matched both v8's constant and v3's literals; the frozen command exits 0 with the
frozen label, the v7 control exits 1 with the frozen refusal label matching the frozen pre receipt byte-for-byte in the
checked fields, and the v7→v8 delta is confined to the allow-list + rename + selftest. Two routed observations (F1 fallback
masking against a lying candidate, F2 unacknowledged open defect 2) are recorded for closure routing; neither invalidates
the frozen predicate this round.
