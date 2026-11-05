# MutationC1 — scoped findings (round 95, attempt 1, lane kaidoku)

Seat: MutationC1 (mutation-tester). Item: mutate-run-revert of the round-95 instruments, plus the
R95-C1 / R95-C2 reproduction. Full table, commands and receipts: `w1/MutationC1/mutants.md`.
Declaration `4bda1d1dd3788973f10e61212b70df18b3b14ea0`; every mutant ran in a fresh clone at that
commit. The lane was not edited, and no git mutation or host change was made.

## Result

- **Baseline (unmutated):** all four checks exit 0 — (i) v5 selftest, (ii) v2 selftest, (iii) forgery
  selftest, (iv) forgery battery over the committed fixtures (`forgeries refused 4 of 4; before admits
  True; honest accepted True`). Pins precheck: 26 of 26 `OK`.
- **Mutants under the frozen kill rule (exit-code difference in (i)-(iv)):** 5 of 10 killed; 5 survived.
  - Killed: M1 (fixed-name temp write follows planted symlink; (i) exit 1), M5 (label-not-frozen removed;
    (i) exit 1), M7 (pins-not-bound removed; (ii)(iii)(iv) exit 1), M8 (label-not-recomputed removed;
    (ii)(iii)(iv) exit 1), M9 (label-not-frozen removed in v2; (ii)(iii)(iv) exit 1).
  - Survived: M2 (fsync deleted), M3 (self-verify forced ok), M4 (fail-closed `code = 1` removed),
    M6 (revision-not-bound removed from v5), M10 (probe verdict hard-coded to hardened / met True).

## Findings

1. **The frozen C1 kill rule has a structural blind spot in the writer and the probe.** None of (i)-(iv)
   calls `main()` of the v5 battery, and none runs `symlink-probe.py`. So the fail-closed exit (M3, M4),
   the revision binding of the public path (M6), and the probe's verdict (M10) are not reachable by the
   frozen counting commands. The honest v5 run (`honest-pos.stdout`: `selfverify ok=True reasons=0`, exit 0)
   is genuinely green, so it cannot discriminate a gate that has been removed. Named kill for each: a
   `main()`-level negative control (short `--rev`, rewritten label, label that does not recompute: must exit
   1) kills M3 and M4; a revision case in the v5 selftest kills M6; a receipt-content check on the probe's
   v4 negative control kills M10 (verified: M10 v4 receipt says `verdict hardened, met True` with
   `victim_intact False`, exit still 1 — exit code alone cannot see it).

2. **M2 (fsync) is invisible to every functional check.** Only an instrumented count of `os.fsync`
   (D-fsync: 1 call on baseline, 0 on M2) catches it. Recorded as a named limit of the writer's
   durability claim.

3. **The M94-f short-`--rev` binding is live in v5 but not in the frozen selftest.** Supplementary D-main
   with a faked verdict and `--rev` = first 9 hex: baseline exit 1 (`selfverify reason: revision-not-bound`),
   M6 exit 0. So the binding works on the public path; it is only uncovered by the frozen gate.

4. **M9 and M8 are caught by the v2 selftest and the forgery battery, as designed.** The honest leg is
   accepted in all killed runs, so the kills come from refusal, not from a blanket refusal.

5. **Probe negative control is the frozen before-side for the symlink (C1 step 3 and its before receipt).**
   Baseline v4: `followed-symlink, victim_intact False, met False, rc 1` (matches
   `pre/c1-symlink-v4-at-base.json`). Baseline v5: `hardened, victim_intact True, met True, rc 0`.

## C2 base-state reproduction (not a draft; read-only at the clone)

At `4bda1d1d` (craft has 33 blocks; block 34 absent):

- `craft-citation-semantic.py --manifest block34-junk.json --block 34` → exit 1: `failing exit 1 - block 34 missing (craft has 33 blocks)`.
- `craft-citation-semantic.py --manifest block34-after.json --block 34` → exit 1, same reason.
- `depth-blocks-v2.py --expect-blocks 34` → exit 1: `blocks 33 resolved 33 expect 34 unresolved 0 met=False`.
- `depth-blocks-v3.py --expect-blocks 34 --shape-from 34` → exit 1: `blocks 33, resolved 33, required-shaped 0/0 expect 34`.

**Attack on the C2 rubber-stamp control:** at base, the junk manifest exits 1 only because block 34 is
missing, not because the keyword atoms fail. The control therefore does not yet discriminate. At landing,
the L1 must check that `block34-junk.json` fails on the keyword atoms specifically (the criterion reason
string), not on the missing-block reason. I did not draft block 34 (outside this seat's item).

## Checks the main agent should run after landing

- Re-run the four frozen commands at the landing commit; record the baseline exit codes.
- Add (as a named candidate for the L1, not applied here): a `main()`-level negative control, a v5 revision
  selftest case, an fsync-count case, and a receipt-consistency check on the probe's v4 negative control.
  These four would have killed M2, M3, M4, M6 and M10 under the frozen rule.
- For C2, check the junk-manifest exit reason string at landing (must not be `block 34 missing`).

## Files written by this seat

- `.ufo/waves/round-95/w1/MutationC1.md` (this report)
- `.ufo/waves/round-95/w1/MutationC1/mutants.md` and `mutant-diffs/M1.diff` … `M10.diff`
- `.ufo/waves/round-95/w1/MutationC1/receipts/` (run4.sh, d-main.py, d-fsync.py, per-mutant logs, detector output, probe receipts, C2 base outputs, `iv-forgery.json`)

Scratch `$S` (`/fast/scratch/hyaku/kaidoku-r95/MutationC1`) was removed after receipts were copied.
No tools were installed or upgraded (none needed: git 2.56.0 and Python 3.14.8 were already present).
