# RV-5 — seat report (chain c2, reviewer, mutation test of the frozen-run guard)

Wave `arc3-loop1-round1`, 2026-10-19. Seat line: *"mutation-test the fix: in a
/tmp copy, REVERT the guard (restore pre-guard expected.json) and show the two
injections then pass silently — proving the guard is load-bearing."*

## 0. Verdict

**The guard is load-bearing — but not by the mechanism the seat line assumed.**

- Removing the **guard code** (pre-guard probe + landed `expected.json`) makes
  both injections pass silently (`reported findings=0 exit=0`; `--strict` reads
  `clean`), and turns the landed selftest red (`cases=13 passed=11 failed=2
  exit=1`). That is the load-bearing proof.
- Restoring the **pre-guard `expected.json` only** (pin deleted, landed probe)
  does **not** reproduce silence: the landed guard is *fail-closed on an
  unpinned baseline*, so every run — clean, tampered, absent — reads
  `could-not-evaluate exit=2`, finding `pointer_table_unpinned`. The seat line's
  premise is refuted by measurement; the landed behaviour is strictly stronger
  than "the injections pass silently".
- Residual limit (unchanged by the fix): a writer who tampers the table **and
  recomputes the pin in the same edit** still gets `findings=0 exit=0`
  (co-mutation; independently measured by EX-24 T2). The pin is a drift
  detector, not self-protection.

Landed artifact measured (uncommitted worktree bytes, captured 10:16–10:19Z):
probe `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`,
`expected.json` `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7`,
`pointer-table.json` `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
— identical to EX-16's `after-sha256.txt` and to PL-2's prototype-verified
result hashes (`claims/c2/PL-2/frozen-run-guard.patch.md`); the table is
byte-unchanged from HEAD.

## 1. Work performed (each bullet has an evidence pointer)

- Baseline at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`: probe
  `3067621a…`, expected `4e28ba90…`, table `738b3a56…`
  (`logs/provenance-20261019T100704Z.txt`; `claims/c2/EX-25/logs/before-provenance.txt`
  is an independent capture of the same three hashes).
- Harness (all under `claims/c2/RV-5/`, re-runnable, no repo writes):
  `mutation-harness.sh` (`run()` + TMPDIR redirect), `cells.sh pre` (HEAD state),
  `cells-gate.sh <dir> <label> [--revert]` (any staged gate dir, optional
  pin-deletion mutation), `cells-attack.sh` (co-mutation, reformat),
  `cells-extra.sh` (content-vs-path, stale pin, absent expected),
  `cells-coderevert.sh` (pre-guard probe + landed expected),
  `stage.sh pre|post|postfix|proto` (staging into scratch from git objects /
  the landed worktree), `fixtures.sha256`.
- Injection fixtures built from the real table bytes (`fixtures/`,
  hashes in `fixtures.sha256`): `table-emptied.json` `36a00fc6…`
  (entries+quoted emptied), `table-space.json` `a07994f2…` (real bytes + one
  space), `table-weakened.json` `0d331b71…` (every `must_match` → `.*`),
  `table-reformatted.json` `6a79c202…` (json re-dump), `expected-forged-pin.json`
  `83dc99b4…` (pin recomputed to the emptied table), `expected-stale-pin.json`
  `0bb18a86…` (landed expected with the pin zeroed), `expected-pre.json`
  `4e28ba90…` (HEAD expected.json).
- 92 logged runs in `logs/` (each file carries the probe's full stdout plus an
  `exit=` line); 18 further cells ran in-place against the real gate dir
  (canonical commands, §3).
- Gate dir verified byte-stable after every in-place run (sha256 before ==
  after); no writes to `.ufo/gates/` by this seat.

## 2. Proposed changes

**None.** This is a reviewer seat: no patch text is proposed and no repo file
other than this report and `claims/c2/RV-5/**` was written. The two couplings
the parent should note when integrating are stated as findings in §4 (F3, F5).

## 3. Before → after measurement (chain c2 claim)

All runs: `python3 <probe> --root <real repo, read-only> --rev <REV>
--table <fixture> --expected <variant>`; log files named
`logs/<label>.txt`. "SILENT" = `reported findings=0 exit=0` (and
`clean findings=0 exit=0` under `--strict`).

| state | probe | expected | clean | tampered-emptied | tampered-space | tampered-weakened | absent | frozen-rev honest | frozen-rev emptied | selftest |
|---|---|---|---|---|---|---|---|---|---|---|
| **pre** (HEAD bytes) | 3067621a | 4e28ba90 | 0 | **SILENT** | **SILENT** | **SILENT** | 2 | 16 findings, rc 0 | **SILENT** (16→0) | 11/11 rc 0 |
| **landed** (EX-16) | e2665074 | ff47bfd6 | 0 | **2** `pointer_table_tampered` | **2** | **2** | 2 `pointer_table_unreadable` | 16 findings, rc 0 | **2** | 13/13 rc 0 |
| **landed + pin deleted** (`--revert`) | e2665074 | 4e28ba90 | 2 `pointer_table_unpinned` | 2 | 2 | 2 | 2 | 2 | 2 | 11 cases run, 11/11 |
| **code reverted, pin kept** | 3067621a | ff47bfd6 | 0 | **SILENT** | — | — | 2 | — | **SILENT** | **11/13, exit 1** (both new cases FAILED) |
| v1 proto (EX-21 draft, skip-on-unpinned) | 776cef6a | 376f9fc5¹ | 0 | 2 | 2 | 2 | 2 | 16 findings | 2 | 13/13 |
| v1 proto + pin deleted | 776cef6a | 4e28ba90 | 0 | **SILENT** | **SILENT** | **SILENT** | 2 | 16 findings | **SILENT** | 11/11 |
| v2 proto (EX-21 draft, fail-closed) | 794e57bc | 3f45a2b5 | 0 | 2 | 2 | 2 | 2 | 16 findings | 2 | 13/13 |
| v2 proto + pin deleted | 794e57bc | 4e28ba90 | 2 `table_pin_absent` | 2 | 2 | 2 | 2 | 2 | 2 | 11/11 |

¹ reconstructed from EX-21's v1 diff + their `proto-selftest.txt` (their v1
selftest log names `pointer_table_tampered`); the prototype rows are design
previews, not the landed artifact.

Canonical in-place runs (landed files, registry-row commands, 10:19Z):

```
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest
SELFTEST_CASE: CLEAN case=table_tampered exit=2 expected=2 finding=pointer_table_tampered
SELFTEST_CASE: CLEAN case=table_absent exit=2 expected=2 finding=pointer_table_unreadable
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0

$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD \
    --table .ufo/gates/citation-drift/pointer-table.json \
    --expected .ufo/gates/citation-drift/expected.json
CITATION_DRIFT_VERDICT: reported findings=0 exit=0      (--strict: clean findings=0 exit=0)
```

Claim-element checklist against the landed artifact:

| claim element (`claims-frozen.md:46-54`) | measured | verdict |
|---|---|---|
| pins the sha256 of `pointer-table.json` in `expected.json` | key `pointer_table.sha256` = `738b3a56…` = the table's digest | ✅ |
| tampered table → declared preflight CNE (exit 2), never silent | 3 tamper shapes → exit 2, `pointer_table_tampered`, both modes | ✅ |
| absent table → exit 2 | exit 2, `pointer_table_unreadable` | ✅ (already true pre-fix — F5) |
| selftest 11 → 13 at exit 0 | 13/13 exit 0; +2 cases (`table_tampered`, `table_absent`) | ✅ (the "clean-tree" in the claim's parenthetical is the existing `clean` case, not a third new one) |
| findings = 0 at HEAD | `findings=0 exit=0`; `--strict` clean | ✅ |
| frozen-run leg restated as a manual rerun at the pinned revision | at `679af5d…` the honest table reports 16 findings rc 0, **identical pre and post guard** | ✅ unchanged |

## 4. Attacks / refutations attempted (with verdicts)

- **F1 — pin deletion (the seat line's revert), landed design.** `--revert`
  cells: every run exit 2 `pointer_table_unpinned`. **Verdict: the seat line's
  premise is refuted**; deleting one JSON key cannot silence the probe. (v1
  prototypes *are* silence-on-pin-deletion — measured — which is why the
  fail-closed choice matters; consistent with EX-24 T3/T4.)
- **F2 — guard-code removal.** Pre-guard probe + landed pin: injections
  `findings=0 exit=0` (strict-clean), selftest 11/13 exit 1 with
  `SELFTEST_CASE: FAILED case=table_tampered` and `... case=table_absent`.
  **Verdict: the code half is load-bearing and the two new cases are a real
  regression gate**, not decoration. The pin alone does nothing.
- **F3 — co-mutation (residual).** Emptied table + pin recomputed to match it
  (`expected-forged-pin.json`): `findings=0 exit=0`, strict-clean — in the
  landed state, both prototype states, and pre-guard. **Verdict: the guard
  detects drift relative to the pin, not re-baselining.** The honest value is
  that re-baselining now forces a visible diff to `expected.json` (EX-24 R3
  recommends the registry row say so; EX-20's current row text — "a tampered
  table can never read as silent findings" — is true only against a stale pin).
- **F4 — byte-exactness cost.** A semantically identical reformat
  (`table-reformatted.json`) reads exit 2 `pointer_table_tampered` post-guard
  (silent pre-guard). **Verdict: intended fail-loud semantics; workflow cost
  is real** — any future table edit must re-pin in the same commit (also
  measured: stale pin + honest table → exit 2).
- **F5 — the absent-table leg is not load-bearing in the run path.** Absent
  table → exit 2 `pointer_table_unreadable` in **every** state (pre, landed,
  pin-deleted, code-reverted). Pre-fix behaviour already satisfied the claim's
  absent clause (`claims/c2/EX-25/logs/before-absent-table.txt`; EX-24 §3 T9).
  Its new value is the selftest case + the registry statement. **Verdict: the
  11→13 delta is one behaviour-changing case (`table_tampered`) plus one
  regression pin for a pre-existing class** — worth stating in the round report
  so the "+2" is not read as two new behaviours.
- **F6 — no silent path from configuration errors.** Absent `expected.json` →
  exit 2; byte-identical table copy at another path → clean (guard binds
  content, not path); `--strict` and probe modes agree on every guard cell.
  **Verdict: no counterexample found.**

## 5. Blockers, gaps, and deviations

- **EX-16 landed late** (gate dir first changed at 10:15:03Z; before-legs at
  10:15Z, after-legs 10:16–10:18Z). All measurements above are against the
  landed worktree bytes captured 10:16–10:19Z; if the parent amends those
  bytes, re-run `stage.sh post && cells-gate.sh` (the harness is sha256-keyed).
- **/tmp was unusable this wave.** The shared `vgpnk` tmpfs quota was
  exhausted: `cp -a` of the 67 MB repo failed (`Disk quota exceeded`) and a
  later 37 KB copy failed the same way (80 KB was the largest write that
  succeeded). Scratch was redirected to
  `/home/vgpnk/.cache/kaidoku-rv5-arc3r1` (outside the repo; removed at seat
  close). Same ceiling hit by RV-6, RV-8 (`/var/tmp`), EX-24 (`/var/tmp`).
- **Not in this seat's scope, flagged to the parent:** the `SKILL.md:371`
  registry-row patch (EX-20 text, SC-4-verified as applying cleanly) and
  whether its "unpinned" token matches the landed id — the landed code emits
  `pointer_table_unpinned`, PL-2's row text uses exactly that token (EX-20's
  draft wrote `table_tampered`/no unpinned token; SC-4 §5 lists the
  substitution points). Also EX-24 R3 (state the co-mutation limit in the row).
- **Not attacked:** same-authority re-baselining beyond F3; normalized-table
  or prefix-comparison pin designs (none proposed).
