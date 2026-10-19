# PL-2 seat report — C2 planner: citation-drift probe frozen-run guard

Wave arc3-loop1-round1, chain c2, 2026-10-19. Role: planner. Real target not
touched (EX-16's territory); all execution on scratch copies.

## 1. Work performed

- Read the frozen claims/roster/rules: `.ufo/waves/arc3-loop1-round1/claims-frozen.md`
  (C2 claim at :46-54; roster/counting at :90-104).
- Traced the debt to its source: `SCORECARD.md:925-926` (round-4 carried debt,
  R6: "expected.json pins no digest of pointer-table.json — probe-exempt by
  kind, gate-blocking if ever promoted"); r5 disposition context at
  `SCORECARD.md:1054-1060`; capability row at `SCORECARD.md:918-919`.
- Read the instrument: `.ufo/gates/citation-drift/citation-drift-probe.py`
  (467 lines; `run_check` :270-296, `Findings.verdict` :69-84, selftest
  harness :381-439), `expected.json` (1 line; 11 selftest rows, `snapshots`,
  `frozen_run`), `pointer-table.json` (331 lines, 31 entries+quoted), and the
  registry row `SKILL.md:371`.
- Studied the frozen-run precedent the debt points at: the recovery gate's
  digest loop `.ufo/rounds/interactive-r1/verify-recovery.py:68-72`
  (`snapshot_missing` / `snapshot_tampered`, both exit 2) and the probe's own
  snapshot machinery (`_snapshot` :130-156, `unpinned_legacy` exit 2).
- Measured the before-state (§3) and reproduced the silent-tamper gap with a
  valid-JSON emptied table on a scratch copy.
- Designed the guard, the two selftest cases, and the SKILL.md row wording;
  built and ran a scratch prototype of all three; validated the patch text
  end-to-end (`patch -p1` on a fresh copy → byte-identical to the prototype).
- Wrote artifacts: `claims/c2/PL-2/plan.md` (design + evidence),
  `claims/c2/PL-2/frozen-run-guard.patch.md` (patch text for probe,
  expected.json, SKILL.md row).

## 2. Proposed changes

- `.ufo/waves/arc3-loop1-round1/claims/c2/PL-2/frozen-run-guard.patch.md` —
  patch text for: (a) `citation-drift-probe.py` (guard + 2 CNE ids + harness
  pin per case), (b) `expected.json` (`pointer_table.sha256` pin, 2 case rows,
  `_doc`), (c) `SKILL.md:371` full replacement row (protected file → patch text
  only). EX-16 applies (a)+(b) to the real target; parent integrates (c).
- `.ufo/waves/arc3-loop1-round1/claims/c2/PL-2/plan.md` — the design artifact
  (spec, alternatives, attacks, after-measurement checklist).
- No other file in the repo was created or modified by this seat.

## 3. Before→after measurement (chain claim)

Before (real target, this seat; scratch = `/home/vgpnk/.pl2-tmp` because `/tmp`
is quota-exhausted — see §5):

```
$ sha256sum .ufo/gates/citation-drift/{pointer-table.json,expected.json,citation-drift-probe.py}
738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f  pointer-table.json
4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33  expected.json
3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f  citation-drift-probe.py
$ git rev-parse HEAD   → e845c2b524ad2e59871e004c51a1386e192a74ab

$ python3 …/citation-drift-probe.py --selftest --expected …/expected.json
CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0

$ python3 …/citation-drift-probe.py --root . --rev HEAD --table …/pointer-table.json --expected …/expected.json
CITATION_DRIFT_VERDICT: reported findings=0 exit=0

$ python3 …/citation-drift-probe.py --root . --rev HEAD --table <tampered copy: valid JSON, entries: []> --expected …/expected.json
CITATION_DRIFT_VERDICT: reported findings=0 exit=0        ← THE GAP: silent false-clean
```

After (measured on the scratch prototype — byte-verified patch result, sha256
`e2665074…` probe / `ff47bfd6…` expected; NOT the real target):

```
$ python3 <prototype> --selftest --expected <prototype expected>
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
  (table_tampered exit=2 finding=pointer_table_tampered;
   table_absent   exit=2 finding=pointer_table_unreadable)

$ prototype, pinned clean table, HEAD      → reported findings=0 exit=0
$ prototype, tampered table                → could-not-evaluate exit=2 (pointer_table_tampered,
                                             sha256 1ee2bd73… != pinned 738b3a56…)
$ prototype, absent table                  → exit=2 pointer_table_unreadable
$ prototype, unpinned baseline             → exit=2 pointer_table_unpinned
$ prototype, tampered + --strict           → exit=2 (CNE class wins in both modes)
$ prototype, rev 679af5d… (16 live drift findings)
      probe mode → reported … exit=0;  --strict → failed … exit=1   (probe kind preserved)
$ patch -p1 of the artifact patch on a fresh copy → sha256 e2665074… == prototype (applies clean)
```

EX-16 must re-run the selftest (13/13), the live HEAD run (findings=0) and the
two injection demos on the real target and record file sha256s.

## 4. Attacks / refutations attempted

- A1 "tampered table is already caught by JSON parsing" — REFUTED by run:
  valid-JSON emptied table grades `findings=0 exit=0` (silent false-clean).
- A2 "absent table already exits 2, so the guard adds nothing" — PARTIALLY
  TRUE, stated honestly: absent was already exit 2 via
  `pointer_table_unreadable`; new value = the tampered class, the pinned
  contract, and the explicit case (absent had no selftest coverage).
- A3 "guard bypassable by deleting the pin" — CLOSED by fail-closed
  `pointer_table_unpinned` (exit 2, measured).
- A4 "pin can't defend expected.json tampering" — TRUE, out of scope: baseline
  of record, same trust class as the committed case table.
- A5 "expected-before-table reorder changes behavior" — CHECKED: missing
  expected file produces IDENTICAL output on original and prototype (exit 2,
  same finding/detail); no existing case has an unreadable expected file.
- A6 "guard only fires in gate mode" — REFUTED: CNE set is checked before the
  `--strict` branch; probe-mode tampered run exits 2.
- A7 "guard breaks drift reporting" — REFUTED: 16 live drift findings at the
  frozen rev → rc 0 probe / rc 1 strict; `verdict()` changed only by 2 CNE ids.
- A8 "selftest harness change could weaken existing cases" — CHECKED: all 11
  existing case verdicts byte-identical in the 13/13 run (per-case
  `exit=… expected=… finding=…` lines).

## 5. Blockers and flags

- `/tmp` (tmpfs, `usrquota`) is exhausted fleet-wide: even a 4 KiB write fails
  ("Disk quota exceeded"; 13G/16G used at 07:00 local). The probe selftest
  needs writable temp dirs → this seat ran everything with
  `TMPDIR=/home/vgpnk/.pl2-tmp` (scratch, removed after). Pure environment
  workaround; the round-4 `/tmp-quota abort` defect note shows this hazard
  class. The first selftest attempt (quota-failed, `git add` exit 128) and the
  first `patch` attempt (write error) are recorded in this session.
- Flag for EX-16/C3: `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc`
  (untracked, mtime 2026-10-19 07:04:16 -0300) appeared in the gate dir this
  wave — a concurrent seat imported the census module; keep it out of commits.
- Observed (not this seat's): `git status` shows `.ufo/waves/arc2-loop1-round10/C3.md`
  modified (+184/-29; a "Revision note for the parent" in the working copy) — a
  concurrent seat editing a previous wave's tracked report file. Flagged for
  the wave integrator; PL-2 touched nothing outside its two artifact paths.
- No other blockers. Scratch removed after the report: `/home/vgpnk/.pl2-tmp`,
  `/tmp/pl2-scratch`, `/tmp/citation-drift-selftest-imbn2lym` (this seat's).
