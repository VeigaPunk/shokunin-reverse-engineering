# SC-2 injection-results ledger — C2 census fail-closures (arc3-loop1-round2)

Seat SC-2 (scribe, chain c2), 2026-10-19. Task: every fixture × class × before ×
after in one table with evidence pointers.

All rows below are **measured by this seat** (17 + 23 fixture-trees × 4 instrument
families = 92 instrument runs plus 8 direct root runs), not copied from other
seats; the "evidence pointers" column adds the independent seats that made the
same class visible (EX-16 the implementer, VZ-2 the c2 convergence seat, EX-11 /
EX-12 / EX-17 / RV-3 / RV-6 / CR-2 / CR-3 the review side).

Scratch for every fixture is `/var/tmp/sc2-ledger/` (never `/tmp`: quota-exhausted
per the round-1 standing record). Custody paths (`~/.config/devin/mcp_config.json`,
`~/.omp/agent/mcp.json`, `~/.kimi-code/config.toml`) were **read** only — the
census's live-anchor re-derivation reads them; no byte was written.

## 1. Instruments — the "after" is a moving target (seven revisions in one wave)

| revision | sha256 (16) | mtime (local) | ordinary run at repo HEAD | note |
|---|---|---|---|---|
| r1 = BEFORE | `6f1d19ff4b0878ad` | 2026-10-19 07:18 (round-1 landing) | PASS exit 0, 0/0/0/0 | both named holes silent-PASS |
| r2 | `1431620f15979e9f` | 09:05:28 | **CRASH (text mode)** | `lines=None` printed with `%-4d` → TypeError; revision **not preserved** (searched `.ufo` for its sha256: 0 hits); superseded in 82 s |
| r3 | `82fb807e79963f6d` | 09:06:50 | PASS exit 0 | EX-16 landing receipt `receipts/after/after-sha256.txt` |
| r4 | `c95a5cf30201a1f8` | 09:10:56 | **FAIL exit 1** at the live tree | per-file floor counted over *blocks* → `SKILL.md=0` false-FAIL; byte copy preserved at `receipts/instruments/landed2-main.py` |
| r5 | `df9ffdf963efa549` | 09:11:50 | PASS exit 0, 0/0/0/0 | per-file floor over detections; all classes closed |
| r6 = AFTER | `a4c167631269e511` | 09:16:33 | PASS exit 0, 0/0/0/0 | verdicts identical to r5 on all 23 fixtures, text/`--json` parity, scope-diff 0 flags |
| r7 | `d0772ce892223690` | 09:18:40 | PASS exit 0, 0/0/0/0 | latest revision at write time; matrix re-run: 0 mismatches vs r6, text/`--json` parity, scope-diff 0 flags (`receipts/runs/landed5*.json`, `scope-diff-before-to-landed5.txt`, `ordinary-at-head-d0772ce8.txt`) |

Evidence: `receipts/revision-churn-at-head.txt` (four preserved revisions run
back-to-back against the live root, text mode), `receipts/ordinary-at-head-c95a5cf3.txt`
(r4 in both modes) and `receipts/ordinary-at-head.txt` (r5, text + JSON). All
matrix rows below were run against **r5, r6 and r7**: the three landed revisions
agree on every fixture (`receipts/runs/landed3*.json`, `landed4*.json`,
`landed5*.json`, 0 verdict mismatches). Every run re-hashes the instrument before
and after execution and no run straddled a write (`instrument_stable: true`,
46/46 runs per family).

Fixture provenance: byte copies of the three scoped files at HEAD —
`PROVINCE.md d075a3c67e17…` (162 lines), `SKILL.md 483b0eba2745…` (371),
`SCORECARD.md a7c72950094e…` (1417); `receipts/fixture-source-sha256.txt` and
`receipts/repo-state-at-measurement.txt`.

## 2. Matrix — fixture × class × before × after

`AFTER` = landed r6 `a4c16763` in the default text mode (the mode every recipe
and receipt in this repo uses), byte-identical in verdict to r5 `df9ffdf9` and
r7 `d0772ce8`;
`AFTER --json` adds the machine channel;
`patch-text-only cand` = both round-1 patch texts (RV-11 H1 + CR-5 H3) applied
verbatim by this seat to a `/var/tmp` copy of r1 — the independent check that the
frozen patch text alone is *not* what landed.

`UNREADABLE×n` = the declared could-not-evaluate class fired for n files;
`G2-SUSPECT` = the declared BLIND-INSTRUMENT class.

| # | fixture (recipe) | class | BEFORE v10 6f1d19ff | AFTER landed r6 a4c16763 | AFTER r6 --json | patch-text-only cand | evidence pointers |
|---|---|---|---|---|---|---|---|
| 1 | `base-clean` — pristine copies of the three scoped files at HEAD | control | PASS exit=0 | PASS exit=0 | PASS exit=0 | PASS exit=0 | receipts/{f}/base-clean.out; EX-16 receipts/before|after/t0-baseline.out; VZ-2 before/t0-baseline.out |
| 2 | `h1-missing-skill` — SKILL.md omitted from the root | H1 (closed) | PASS exit=0 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | receipts/{f}/h1-missing-skill.out; EX-16 before/h1-skill-absent.out; VZ-2 before/t1-absent-skill.out; EX-11 receipts/cA-absent-skill.out |
| 3 | `h1-skill-as-dir` — SKILL.md replaced by a directory (IsADirectoryError) | H1 (closed) | PASS exit=0 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | receipts/{f}/h1-skill-as-dir.out; EX-16 before/h1-skill-isdir.out |
| 4 | `h1-skill-chmod000` — SKILL.md mode 000 (PermissionError) | H1 (closed) | PASS exit=0 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | receipts/{f}/h1-skill-chmod000.out; EX-16 before/h1-skill-eacces.out |
| 5 | `h1-skill-symlink-loop` — SKILL.md self-referential symlink (ELOOP) | H1 (closed) | PASS exit=0 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | receipts/{f}/h1-skill-symlink-loop.out; CR-2 evidence/landed__symlink_skill.txt |
| 6 | `ctl-missing-province` — PROVINCE.md omitted | control | FAIL exit=1 SCOPE-ERR×3 | FAIL exit=1 UNREADABLE×1 SCOPE-ERR×3 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 SCOPE-ERR×3 | receipts/{f}/ctl-missing-province.out; EX-16 before/h1-province-absent.out; VZ-2 before/t3 |
| 7 | `ctl-missing-scorecard` — SCORECARD.md omitted | control | FAIL exit=1 SCOPE-ERR×10 | FAIL exit=1 UNREADABLE×1 SCOPE-ERR×10 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 SCOPE-ERR×10 | receipts/{f}/ctl-missing-scorecard.out; EX-16 before/h1-scorecard-absent.out; EX-11 receipts/cB2-absent-scorecard.out |
| 8 | `ctl-empty-dir` — all three scoped files omitted | control | FAIL exit=1 SCOPE-ERR×13 | FAIL exit=1 UNREADABLE×3 SCOPE-ERR×13 | FAIL exit=1 UNREADABLE×3 | FAIL exit=1 UNREADABLE×3 SCOPE-ERR×13 G2-SUSPECT | receipts/{f}/ctl-empty-dir.out; VZ-2 before/t4-no-checks.out |
| 9 | `inj-undeclared-append` — CR-5 t2: stale pin appended past the declared bound | injection | FAIL exit=1 | FAIL exit=1 | FAIL exit=1 | FAIL exit=1 | receipts/{f}/inj-undeclared-append.out; EX-16 before/t2-undeclared-append.out |
| 10 | `inj-marker-strip` — CR-5 t3: DATED marker text removed (PROVINCE.md:40) | injection | FAIL exit=1 SCOPE-ERR×1 | FAIL exit=1 SCOPE-ERR×1 | FAIL exit=1 | FAIL exit=1 SCOPE-ERR×1 | receipts/{f}/inj-marker-strip.out; EX-16 before/t3-marker-strip.out |
| 11 | `inj-ptr-out-of-range` — CR-5 t6: pointer at ~/.kimi-code/config.toml:9999 appended | injection | FAIL exit=1 | FAIL exit=1 | FAIL exit=1 | FAIL exit=1 | receipts/{f}/inj-ptr-out-of-range.out; EX-16 before/t6-ptr-out-of-range.out |
| 12 | `inj-false-current-pin` — CR-5 t1: SKILL.md CURRENT pin 6.5.0 -> 6.3.0 | injection | FAIL exit=1 | FAIL exit=1 | FAIL exit=1 | FAIL exit=1 | receipts/{f}/inj-false-current-pin.out; EX-16 before/t1-false-current-pin.out; EX-11 receipts/cD0 |
| 13 | `res-missing-root` — root path itself absent | H1 extension | FAIL exit=1 SCOPE-ERR×13 | FAIL exit=1 UNREADABLE×3 SCOPE-ERR×13 | FAIL exit=1 UNREADABLE×3 | FAIL exit=1 UNREADABLE×3 SCOPE-ERR×13 G2-SUSPECT | receipts/{f}/res-missing-root.out; CR-2 evidence/landed__live-repo.txt (control) |
| 14 | `res-empty-skill` — SKILL.md present but 0 bytes (VZ-2 t2) | H1 extension | PASS exit=0 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | PASS exit=0 | receipts/{f}/res-empty-skill.out; EX-16 before/h1-skill-zero-byte.out; VZ-2 before/t2-empty-skill.out; CR-2 evidence/landed__empty_skill.txt |
| 15 | `res-skill-decoy-historical` — SKILL.md replaced by a 1-line 'historical stub' (rows beyond EOF) | H1 extension | PASS exit=0 | FAIL exit=1 UNREADABLE×1 | FAIL exit=1 UNREADABLE×1 | PASS exit=0 | receipts/{f}/res-skill-decoy-historical.out; CR-2 evidence/landed__trunc_skill.txt |
| 16 | `inj-dated-shelter` — CR-5 t5 / VZ-2 t8: planted pin inside a DATED range | by design | PASS exit=0 | PASS exit=0 | PASS exit=0 | PASS exit=0 | receipts/{f}/inj-dated-shelter.out; EX-16 before/t5-dated-shelter.out; VZ-2 before/t8-dated-shelter.out |
| 17 | `res-h2-inline-marker` — VZ-2 t6: PROVINCE.md:17 pin -> 6.3.0 plus ' (historical)' on the same physical line | H2 residual | PASS exit=0 | PASS exit=0 | PASS exit=0 | PASS exit=0 | receipts/{f}/res-h2-inline-marker.out; VZ-2 before/t6-inline-marker.out; VZ-3 (c3) A3/A3b |
| 18 | `res-h5-eof-no-gate-token` — VZ-2 t7 / RV-11 A2: appended line with no gate token | H5 residual | PASS exit=0 | PASS exit=0 | PASS exit=0 | PASS exit=0 | receipts/{f}/res-h5-eof-no-gate-token.out; VZ-2 before/t7-gate-free-eof.out |
| 19 | `blind-all-needles` — CR-5: PIN/VER/PTR all replaced by never-matching patterns | H3 (closed) | PASS exit=0 | FAIL exit=1 G2-SUSPECT | FAIL exit=1 | FAIL exit=1 G2-SUSPECT | receipts/{f}/blind-all-needles.out; EX-16 before/h3-blind-all.out; VZ-2 before/t5-blind-instrument.out; EX-11 receipts/cC-neutered-needles.out |
| 20 | `blind-pin-only` — PIN alone neutered (VER/PTR live) | H3 partial residual | PASS exit=0 | PASS exit=0 | PASS exit=0 | PASS exit=0 | receipts/{f}/blind-pin-only.out; EX-16 before/h3-blind-pin.out |
| 21 | `blind-rea-gate` — REA_GATE neutered: no unit is ever classified | H3 (closed) | PASS exit=0 | FAIL exit=1 G2-SUSPECT | FAIL exit=1 | FAIL exit=1 G2-SUSPECT | receipts/{f}/blind-rea-gate.out; EX-16 before/h3-blind-gate.out; CR-3 receipts/v-blind-head.out |
| 22 | `widened-scope` — CR-5 widen: last DATED row end extended over the appended records | H4 residual | PASS exit=0 | PASS exit=0 | PASS exit=0 | PASS exit=0 | receipts/{f}/widened-scope.out; EX-16 before/w1-scope-widen-tail.out; CR-5 receipts/widen-swallow.out |
| 23 | `anchor-fail-empty-home` — HOME pointed at an empty dir: no live anchors re-derivable (CR-5 t4) | anchor | ANCHOR-FAIL exit=2 | ANCHOR-FAIL exit=2 | ANCHOR-FAIL exit=2 | ANCHOR-FAIL exit=2 | receipts/{f}/anchor-fail-empty-home.out; EX-16 before/t4-anchor-fail.out |

## 3. Residuals — measured, named, not closed

| fixture | landed verdict | why it is not a closure |
|---|---|---|
| `inj-dated-shelter` | PASS exit=0 | DATED rows are historical by construction (documented refusal of tail expansion) |
| `res-h2-inline-marker` | PASS exit=0 | G12/INLINE_MARKER excuses a locus whose own physical line says 'historical' (H2, named in the landed header) |
| `res-h5-eof-no-gate-token` | PASS exit=0 | unit has no gate token, so it is not a locus at all (H5/unit boundary; scanner-level, not fixable by a verdict guard) |
| `blind-pin-only` | PASS exit=0 | one live needle family still yields current-ok loci, so the tree-level floor cannot see the loss (H4/self-certification) |
| `widened-scope` | PASS exit=0 | scope widening is fail-open by construction; only the external scope-diff audit sees it (H4) |

## 4. Findings

**F1 — revision churn changed verdict semantics twice; one intermediate revision
false-FAILs the live tree.** r4 (`c95a5cf3`, 09:10:56) FAILs an ordinary run at the
live repo root in *both* modes (`per file: PROVINCE.md=1, SCORECARD.md=4,
SKILL.md=0`, `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']`, exit 1) because its
floor counted current-ok *blocks*; SKILL.md's only locus-bearing CURRENT block is
mixed and disposes `info`, so it contributes 0 blocks while contributing 3 dets.
r5 fixes it by counting detections (the landed code says so at
`.ufo/gates/c1-census-v10.py:529-541`). Measured on the preserved r4 byte copy:
`receipts/ordinary-at-head-c95a5cf3.txt`; the churn row-by-row:
`receipts/revision-churn-at-head.txt`. Wave-level consequence: for ~55 s the
committed instrument could not PASS on its own repo — any seat that ran the
census in that window read a false FAIL.

**F2 — r2 could not report any H1-class failure in text mode.** With
`counts[f]["lines"] = None` and the old `"%-4d"` format, the text report died
before the class line:

```
Traceback (most recent call last):
  File ".ufo/gates/c1-census-v10.py", line 557, in <module>
    sys.exit(main())
  File ".ufo/gates/c1-census-v10.py", line 534, in main
    print("%-14s lines=%-4d loci=%s" % (f, c["lines"], c["loci"]))
TypeError: %d format: a real number is required, not NoneType
```

Observed by this seat at 09:05:28–09:06:5x; the revision is not preserved by any
seat, so this is transcript evidence, not a re-runnable receipt — named here
because `--json` was the only channel that would have shown the class. r3 fixed
the format; r5 uses `%-4s`.

**F3 — the frozen patch text alone does not close the zero-byte / truncated file
class.** The `cand` column: H1 and H3 close (rows 2-5, 19, 21 FAIL with the
declared class) but `res-empty-skill` (0 bytes) and `res-skill-decoy-historical`
(1-line stub) stay **PASS**, because a readable-but-short file is not an OSError.
The landed revisions close both with the rows-beyond-EOF guard
(`len(lines) < max_end`) — measured: rows 14-15 FAIL at r5 and r6. This is the one
place where the landed instrument is strictly stronger than the frozen patch
texts, and the extra class is exactly what EX-16's before-matrix called the
"truncated (rows beyond EOF)" case.

**F4 — text and `--json` agree on exit code and class for all 23 fixtures under
r5, r6 and r7** (0 PASS / 1 FAIL / 2 ANCHOR-FAIL on both channels, rows 1-23; 0
mismatches between `landed4` and `landed4-json`, and none in `landed5`). An apparent
mode disagreement during this wave's measurement (text FAIL vs JSON PASS on the
same root, ~80 ms apart) was **not** a same-revision defect: it straddled the
09:10:56 → 09:11:50 revision swap. Re-measured deterministically on preserved
copies: r4 FAILs in both modes, r5 PASSes in both (`receipts/revision-churn-at-head.txt`).
This seat's lesson, recorded for the round report: a verdict-changing instrument
under live edit must be hash-pinned per run, not per session.

**F5 — scope bounds byte-stable.** `scope-diff.py` (round-1 CR-5 tool) r1→r5 and
r1→r6: 20 rows before, 20 after, 0 added, 0 removed, 0 changed, `CREEP FLAGS: []`,
exit 0 (`receipts/scope-diff-before-to-landed.txt`, `-landed4`,
`-before-to-cand.txt`). Independently reproduced by RV-6
(`claims/c2/RV-6/logs/creep-audit-landed.txt`) and EX-16
(`claims/c2/EX-16/receipts/after/scope-diff.txt`).

**F6 — claim status against the frozen text.** "Every round-1 silent-PASS
injection now reproduces as a declared FAIL": true for the named H1 and H3
classes in all their measured variants (rows 2-5, 8, 13-15, 19, 21 — 9 fixtures
flipped PASS→FAIL, each with a printed class, `DECLARED FAIL CLASSES: [...]`, and
exit 1). "Ordinary runs at HEAD stay PASS 0/0/0/0": true at r5 (row 1;
`receipts/ordinary-at-head.txt`), false at r4 (F1). "Scope bounds byte-stable
(creep audit 0 flags)": F5. "H4 self-certification residual stays named": true —
rows 20 and 22 remain PASS and are what the external audit exists for.

**F7 — the perimeter is not closed, and none of it is silent.** Five measured
fixtures still PASS by design (Section 3) and each is either named in the landed
instrument's header (H2, t5/DATED-shelter, H4) or in a sibling seat's receipt
(H5 gate-free EOF: VZ-2 `before/t7-gate-free-eof.out`, RV-11 A2). Nothing in this
ledger closed without a printed class, and no check here is cited unrun.

## 5. Reproduction

```
python3 /var/tmp/sc2-ledger/harness.py build          # fixtures + instrument variants
python3 /var/tmp/sc2-ledger/harness.py run landed3 /var/tmp/sc2-ledger/src-landed3.py
python3 /var/tmp/sc2-ledger/harness.py run landed3-json /var/tmp/sc2-ledger/src-landed3.py --json
python3 /var/tmp/sc2-ledger/harness.py run landed5 /var/tmp/sc2-ledger/src-landed5.py   # r7, re-verified 0 mismatches
python3 /var/tmp/sc2-ledger/gen_ledger.py             # regenerates this table from the run JSONs
```

Harness and generator are copied into `receipts/`; run JSONs in `receipts/runs/`;
raw stdout+exit of every run in `receipts/runs/<family>/<fixture>.out`. The
family→revision map is `before`=r1, `landed`=r3, `landed2`=r4, `landed3`=r5,
`cand`=patch-text-only. Instrument byte copies: `receipts/instruments/` with
`instrument-sha256.txt`.

## 6. Cross-seat evidence index (for the round report)

- Implementer: `claims/c2/EX-16/receipts/{before,after}/` (class matrix, landing
  diff, ordinary run, residuals), `tools/injections-r9.py`.
- Convergence: `claims/c2/VZ-2/tools/injections.md` (t0-t8 recipes),
  `VZ-2/proposed-census-floor-and-unreadable.patch.md`.
- Before-state injections: `claims/c2/EX-11/receipts/` (cA-cD8),
  `claims/c2/EX-12/evidence/` (patch fuzz + fixture matrix),
  `claims/c2/EX-17/before-*.txt`.
- Floor modelling: `claims/c2/EX-14/` (`scope-locus-map.md`, `pff-matrix.out`,
  `proposed-h3-floor-scoping.patch.md`), `claims/c2/RV-3/receipts/model-run/`.
- Audits: `claims/c2/RV-6/logs/` (creep + differ, 0 flags),
  `claims/c2/EX-21/` (scope audit), `claims/c2/CR-2/evidence/` (landed fixture
  battery incl. rename/rekey), `claims/c2/CR-3/receipts/` (blindness variants by
  row/class/file/global), `claims/c2/RV-8/` (header-stanza audit + projections).
