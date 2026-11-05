# ExecRepro — R97-C1 independent non-author reproduction

Seat: ExecRepro (executor). Scratch: /fast/scratch/hyaku/kaidoku-r97/ExecRepro
Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone`
then `git -C $S/clone checkout --detach`. Toplevel verified = $S/clone before writes.
No tools installed/changed; python3 only. No mutating git in the lane.

## 1. At landing 867ed98d85f45a18265441c1760386ef353b3d43

`git -C $S/clone rev-parse HEAD` = 867ed98d85f45a18265441c1760386ef353b3d43.

- `python3 -I -B tools/round-97/stop-boundary-repair-battery-v7.py --selftest --work $S/v7-st`
  rc=0, `SELFTEST cases=23 failures=0` (23 cases, 0 failures, as claimed).
- `python3 -I -B tools/round-97/kill-rule-v3.py --selftest --work $S/kr-st`
  rc=0, `SELFTEST cases=8 failures=0` (8 cases, as claimed).

Frozen command A (in clone, rc/exit as below):
`python3 -I -B tools/round-97/kill-rule-v3.py --root . --work $S/kr-repro --mutants .ufo/waves/round-97/mutants.json --fixtures .ufo/waves/round-97/forgery --prefix forge --decl e859a88d78567c44bc1ecfd211afe123755ae1c7 --json-out $S/c1-clone.json`
rc=0, stdout tail `mutants killed 21 of 21; forgeries refused 17 of 17; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1; wlink 2 of 2; durability 2 of 2; bytes 5 of 5; dirtyrefuse 1 of 1; ownrec 1 of 1 met True exit 0`.
Receipt label matches the claim verbatim. Compared to lane receipt
`.ufo/waves/round-97/l1/scores/c1-at-867ed98d85f45a18265441c1760386ef353b3d43.json`:
label equal, exit 0 = 0, counts equal, every honest.* ok flag equal and true
(K-agreement/K-bytes/K-cwd/K-dmain/K-durability/K-forgeries/K-probe/
K-selftest-agreement/K-selftest-counter/K-wlink/r95-battery-regression),
met_target true = true. Receipt copied to
`.ufo/waves/round-97/w1/ExecRepro/c1-clone.json` (JSON only, scratch not copied).

Note: first attempt of command A was killed by the 300s tool timeout (only at
small mutant stage, no receipt, process dead); re-ran with no deadline — total
~1900s under fleet load (sibling seats running the same battery in parallel).

## 2. Before side at base 2a54af0785f75d50912e1136443c8e78e62adf27

After step 1: `git -C $S/clone checkout --detach 2a54af0785f75d50912e1136443c8e78e62adf27`,
HEAD=2a54af0785f75d50912e1136443c8e78e62adf27, tree clean.

Command B as specified in the seat item cannot run verbatim at the base, and
the run confirms why:
`python3 -I -B tools/round-96/kill-rule-v2.py --root . --work $S/kr-before --mutants .ufo/waves/round-97/mutants-before-noc1.json ...`
First attempt (mutants path relative to clone): `FileNotFoundError: .ufo/waves/round-97/mutants-before-noc1.json`, rc=1 (the freeze-era layout is not in the base tree).
Second attempt (absolute mutants+fixtures paths staged from the lane):
`FileNotFoundError: .../clone/tools/round-97/stop-boundary-repair-battery-v7.py`, rc=1 — the
round-96 rule's `build_copy` copies `tools/round-97/...` files named by the
before-table mutants, which do not exist at the base tree. Either way rc != 0,
so the before-side predicate (non-zero exit at the base) holds.
This is a structural property (before-table names round-97 files absent at base),
not a scoring verdict: the freeze-time committed artifacts
(`pre/c1-v2rule-at-base.json` exit=1, label `mutants killed 17 of 10; forgeries
refused 4 of 10; negctl refused 3 of 3; probe consistent 1 of 1; honest
accepted 0 of 1`, `pre/c1-v2rule-at-base.rc`, `pre/c1-v2rule-at-base-crash.txt`
showing the M-c1 KeyError propagating) were measured by the L1 at freeze against
`mutants-before.json`. I did not reproduce the freeze-time partial receipt
(it needs the freeze checkout, not the base), and I state that explicitly.

## 3. Findings

- R97-C1 after-side reproduces independently and byte-for-byte counts/label:
  21/21, 17/17, 3/3, 1/1, 1/1, 2/2, 2/2, 5/5, 1/1, 1/1; both selftests green.
- Before-side non-zero exit confirmed (rc=1 twice, two distinct missing-input
  causes, both ending non-zero). No before-side receipt produced by this seat.
- Findings: 1 (the seat-item command B path assumption; not a claim defect —
  the lane's committed freeze artifacts already cover the before side).

R97-C1 reproduction: PASS. Tooling changes: none.
