# SC-2 — scribe, chain c2 (arc3-loop1-round2), 2026-10-19

Task: injection-results ledger — every fixture × class × before × after in one
table with evidence pointers.

## 1. Work performed (evidence pointers)

Built a measurable ledger rather than transcribing other seats: a fixture builder
+ matrix runner on `/var/tmp/sc2-ledger` (never `/tmp`), 18 fixture trees, 4
instrument families, 92 instrument runs, each run re-hashing the instrument
before and after execution (`instrument_stable: true`, 46/46 on the landed
family; no run straddled a write).

- Artifact: `claims/c2/SC-2/injection-ledger.md` (23-row matrix, residuals,
  findings F1-F7, reproduction, cross-seat evidence index).
- Harness + receipts: `claims/c2/SC-2/receipts/` — `harness.py`, `gen_ledger.py`,
  `runs/<family>/<fixture>.out` (raw stdout + exit; families `before`, `landed`
  =r3, `landed2`=r4, `landed3`=r5, `landed4`=r6, `cand`), `runs/<family>.json`,
  `instruments/` (byte copies of r1/r3/r4/r5 + the patch-text candidate, with
  `instrument-sha256.txt`), `revision-churn-at-head.txt`,
  `ordinary-at-head.txt` (r5), `ordinary-at-head-c95a5cf3.txt` (r4),
  `scope-diff-before-to-{landed,cand}.txt`, `fixture-source-sha256.txt`,
  `repo-state-at-measurement.txt` (209 files, 2.2 MB).
- Proposed patch text: `claims/c2/SC-2/proposed-per-run-hash-recipe.patch.md`.
- Cross-seat corroboration cited per row: EX-16 (implementer), VZ-2 (c2
  convergence), EX-11 / EX-12 / EX-14 / EX-17 / EX-21 / RV-3 / RV-6 / RV-8 /
  CR-2 / CR-3 — all under `claims/c2/`.

Custody: the five custody paths were read only (live-anchor re-derivation); no
git mutation; no LOG/SCORECARD/SHONEN/corpus/SKILL write; the census's real target
was written only by EX-16.

## 2. Proposed changes

`claims/c2/SC-2/proposed-per-run-hash-recipe.patch.md` (one recipe line: hash-pin
the instrument per run). **No code change proposed** to
`.ufo/gates/c1-census-v10.py` or the probe.

## 3. Before→after measurement for the C2 claim

Instruments: BEFORE `6f1d19ff` (v10 at r1); AFTER `a4c167631269e511` (landed
r6; verdict-identical at r5 `df9ffdf9` and r7 `d0772ce8`, 0 mismatches);
patch-text-only candidate assembled by this seat from the two frozen patch texts;
preserved intermediates r3 `82fb807e`, r4 `c95a5cf3`.

```
$ python3 /var/tmp/sc2-ledger/harness.py run before src-before.py
[before] h1-missing-skill   exit=0 PASS        (H1 class silent)
[before] blind-all-needles  exit=0 PASS        (H3 class silent)
[before] base-clean         exit=0 PASS
$ python3 /var/tmp/sc2-ledger/harness.py run landed4 src-landed4.py   # r6 = a4c16763
[landed4] base-clean        exit=0 PASS
[landed4] h1-missing-skill  exit=1 FAIL unreadable=1
[landed4] blind-all-needles exit=1 FAIL        (G2 SUSPECT / BLIND-INSTRUMENT)
[landed4] res-empty-skill   exit=1 FAIL unreadable=1   (patch text alone: PASS)
$ python3 .ufo/gates/c1-census-v10.py --quiet            # ordinary run, r5/r6
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)     exit=0
```

- Class closure: **9 fixtures flipped PASS→FAIL**, each with a printed class,
  `DECLARED FAIL CLASSES: [...]`, exit 1 — H1 variety (absent, is-a-dir, EACCES,
  ELOOP, missing root), H1 extension (0-byte, 1-line decoy), H3 (all needles,
  gate). 5 fixtures PASS by design and stay named (DATED-shelter, H2 inline
  marker, H5 gate-free EOF, PIN-only partial blindness, scope widening).
- Ordinary run at HEAD: PASS 0/0/0/0 at r1, r3, r5, r6, r7; **FAIL at r4** (F1).
- Scope bounds: `scope-diff.py` r1→r5, r1→r6, r1→r7 = 20/20 rows, 0
  added/removed/changed, `CREEP FLAGS: []`. Text vs `--json` exit codes agree on
  all 23 fixtures at r5, r6 and r7, and the three revisions agree
  fixture-for-fixture (0 mismatches).

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | H1 in 4 flavours (absent / directory / EACCES / ELOOP) + a missing root | closed at r5 (declared `UNREADABLE`, exit 1); all four silent at r1; missing root was already FAIL at r1 |
| A2 | H3 blindness: all three needles, gate regex only, PIN only | all-needles and gate closed; **PIN-only still PASS** — refutes any general "blindness is closed" reading, matches the landed header's named H4 residual |
| A3 | over-tightening: does the new floor break a legitimate run? | **yes at r4**: per-file floor over blocks gave `SKILL.md=0` and FAILed the pristine HEAD tree in both modes; r5 (and r6) counting detections fixes it (measured on preserved copies) |
| A4 | H1 bypass by substitution (0-byte file, 1-line "historical" decoy) | **patch text alone fails** (PASS); landed r5 closes both via the rows-beyond-EOF guard; this is where the landed instrument is strictly stronger than the frozen patch text |
| A5 | mode attack: text vs `--json` disagree? | no disagreement at any single revision; the one apparent split was my own mid-swap capture (revision changed between two invocations) — corrected by deterministic re-runs |
| A6 | scope creep / laundering (widen the last DATED bound) | not detectable by the instrument itself (PASS by construction) but `scope-diff.py` reports 0 flags for r1→r5 and r1→r6, so no creep occurred |
| A7 | residual perimeter (H2 inline-marker, H5 gate-free EOF, DATED shelter, widening) | all still PASS; each named (landed header or VZ-2/RV-11 receipts) — none silent |

## 5. Blockers

None for this seat; the artifact is complete and every row is a run I performed.
Two things the round report must carry:

1. Revision churn: four writes in 9 minutes after the 09:06:50 landing; r2
   crashed in text mode (`TypeError: %d format ... not NoneType`, revision not
   preserved by any seat) and r4 false-FAILed the live tree for ~55 s in both
   modes. Any seat that ran the census in that window read a false verdict.
   The ledger's after column was measured at r6 `a4c167631269e511…` and
   re-verified at r7 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
   (and r5 `df9ffdf9…`); if a further revision lands, re-run the matrix with
   `harness.py run landedN <copy>` — one command, 24 fixtures, ~1 s.
2. EX-16's `receipts/after/` (mtime 09:12:15) post-date r5 (09:11:50) and are
   consistent with it; my ledger's "after" column is r5.
