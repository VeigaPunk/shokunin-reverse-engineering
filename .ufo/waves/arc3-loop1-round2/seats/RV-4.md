# Seat RV-4 — reviewer, chain c2 (arc3-loop1-round2)

Task as dispatched: **mutation-test H3 — revert ONLY the H3 floor → neutered
needles must return to blind PASS.** Verdict: **confirmed.** The revert restores
the blind PASS on both the pre-landing patch construction and EX-16's landed
instrument; the H3 floor is therefore load-bearing (the mutation is killed by
the floor and by nothing else).

Artifacts: `.ufo/waves/arc3-loop1-round2/claims/c2/RV-4/mutation-h3.md` (main),
`instruments/` + `instruments/real-target/`, `receipts/` + `receipts/real-target/`,
`harness/`, `DIGESTS.md`. Scratch: `/var/tmp/rv4-mutation/` (never `/tmp`).

## 1. Work performed (evidence pointers)

Instruments under test — `.ufo/gates/c1-census-v10.py` at three revisions; this
seat wrote none of them:

- pre-patch `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`
  (round-1 close; CR-5's H3 target);
- EX-16 landed `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`
  (560 lines, mtime 09:06:50 −0300; stamped in EX-16's own
  `receipts/after/after-sha256.txt`). The census moved twice mid-seat
  (`7b5a0e88…` → `a4553911…` → `82fb807e…`); every receipt is stamped with the
  bytes actually run.
- H3 floor in the landed form: `c1-census-v10.py:518` `g2_ok = n_current_ok > 0`,
  with `:519` `declared = … BLIND-INSTRUMENT` and `:521` verdict gate.

The mutation = that one line reverted to the old disjunct
(`… > 0 or (not stale and not unatt and not undecl and not unres)`), no other
edit: `instruments/real-target/mutation-landed.diff` (1 hunk, 1 line) and
`instruments/mutation.diff` (same revert against the patch construction).
Injection = CR-5's needle neutering (PIN/VER/PTR → never-matching), plus an
independent second channel (`REA_GATE` → never-matching).

Receipts: `receipts/real-target/REAL-TARGET-MATRIX.txt` + 6 runs (`landed82fb807e[-nog2][-neut|-gate].out`),
`-json.out`, `.rerun.out`; pre-landing matrix `receipts/MATRIX.txt` +
`instr-head*`, `instr-h3*`, `instr-h3-nog2*`; attribution control
`receipts/instr-h3-noprint-neut.out`; separability probe
`receipts/instr-h3{,-nog2}-emptyroot-quiet.out`; residuals
`receipts/instr-h3{,-nog2}-narrowgate.out`, `…‑pinonly.out`.

## 2. Proposed changes

**None.** The H3 floor is already landed by EX-16 (C2's designated implementer);
this seat's product is the mutation verdict, not a patch. Two reviewer notes for
the chain (no patch text offered, both already consistent with EX-16's header):
(i) the floor is the *sole* detector of the blind class — no other assertion
separates blind from clean — so its removal is invisible outside injection;
(ii) partial needle/`REA_GATE` narrowing is not caught by the floor (measured
below) and correctly stays a named H4/external-audit residual.

## 3. Before → after measurement (chain claim slice: the H3 injection)

Chain claim: "every round-1 silent-PASS injection now reproduces as a declared
FAIL". This seat measured the H3 (blind-instrument) injection end to end.

Before — pre-patch instrument, needles neutered:

```
$ python3 /var/tmp/rv4-mutation/work/instr-head-neut.py --root <repo>
PROVINCE.md lines=162 loci=0 / SCORECARD.md lines=1417 loci=0 / SKILL.md lines=371 loci=0
G2 positive-assertion guard: ok
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)          exit=0
```

After — landed instrument, same injection:

```
$ python3 …/work/landed82fb807e-neut.py --root <repo>
PROVINCE.md lines=162 loci=0 / SCORECARD.md lines=1417 loci=0 / SKILL.md lines=371 loci=0
G2 positive-assertion guard: SUSPECT (current-ok loci=0, total loci=0, floor=1)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)          exit=1
```

**Mutation result** — landed instrument with only `:518` reverted, same injection:

```
$ python3 …/work/landed82fb807e-nog2-neut.py --root <repo>
G2 positive-assertion guard: ok (current-ok loci=0, total loci=0, floor=1)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)          exit=0
```

Ordinary runs unaffected: landed and mutant at the live root are byte-identical
(`a9cd6886…`, PASS 0/0/0/0, loci 6/9/2, current-ok 5). `--json` carries it too:
`g2_ok false`/`declared_fail_classes ["BLIND-INSTRUMENT"]`/exit 1 vs
`g2_ok true`/`[]`/exit 0. All key runs re-run byte-identical.

## 4. Attacks / refutations attempted

| # | attack | verdict |
|---|---|---|
| A1 | Revert only the floor (the dispatched mutation) → does blind PASS return? | **Confirmed** on landed bytes and on the patch construction: PASS exit 0, all counters 0 (`landed82fb807e-nog2-neut.out`). Mutation not survived. |
| A2 | Could the FAIL be an artifact of CR-5's diagnostic print rather than the boolean? | **Refuted**: floor intact + print reverted + needles neutered still FAILs (`instr-h3-noprint-neut.out`). The kill is attributable to the floor. |
| A3 | Second blindness channel — neuter `REA_GATE` instead of the needles (different code path, same class). | **Both hold**: landed → FAIL + `['BLIND-INSTRUMENT']`; floor-reverted → PASS (`…-gate.out`, `…-nog2-gate.out`). |
| A4 | Ordinary-run collateral: does the floor (or its absence) change a normal run? | **No**: byte-identical output both sides at the live root (`a9cd6886…`); floor is conditional on zero loci. |
| A5 | Is some other assertion a backstop (redundant detector)? | **No — sole detector**: under injection `SCOPE-ERRORS []`, `G11 []`, `G7 []`, all four counters 0 on both sides. Removal is invisible outside injection. |
| A6 | Partial blindness: does the floor catch needle/`REA_GATE` narrowing that leaves loci > 0? | **Refuted (bound stated)**: `REA_GATE` narrowed to `rea-agents` drops loci 17 → 8 and PASSes on floor *and* mutant (identical digests `4c1efd19…`); PIN-only neuter leaves loci unchanged, PASS. Guarantee = "not silent", not "no regression"; matches EX-16's H4 note. |
| A7 | Does reverting H3 mask/resurrect H1's absent-file class (cross-contamination of the two fail-closures)? | **No**: empty root fails both ways on `SCOPE-ERRORS` (`…-emptyroot-quiet.out`). Classes separable. |
| A8 | Round-1 defeat claim re-check: is the round-1 CR-5 defect still reproducible at the pre-patch revision? | **Reproduced independently** (A1's before-row, own run, not a citation). |
| A9 | Does the mutant hide behind the declared-class machinery (e.g. label retained)? | **No — it loses it**: `DECLARED FAIL CLASSES: []` on the mutant's blind run (label is derived from `g2_ok`), a second independent tell. |

## 5. Blockers

None. Two caveats for the integrator:

1. The census revision was moving during the seat (`7b5a0e88…` → `a4553911…` →
   `82fb807e…`). The real-target verdict is pinned to `82fb807e…`; if EX-16
   revises again, `harness/run-landed.py <tag>` reproduces the whole test in one
   command against the new bytes (it asserts the floor line is uniquely present
   and aborts loudly if the floor's form changed).
2. `/tmp` was not used; all scratch is `/var/tmp/rv4-mutation/` and all writes
   are confined to `claims/c2/RV-4/` + this seat report.
