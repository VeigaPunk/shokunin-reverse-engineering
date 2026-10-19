# RV-5 — seat report (chain c2, reviewer: false-positive hunt on the landed v11)

Wave `arc3-loop1-round2`, 2026-10-19. Seat line: *false-positive hunt — run the
ordinary tree + the r8-era DATED rows + the round-1 records text through landed
v11; the new guards must fire ONLY on their fixtures.*

Reviewed artifact: `.ufo/gates/c1-census-v10.py` (EX-16's write; this seat never
wrote it). Pinned revision at report time: sha256
`d0772ce892223690…` — header-text edit of the unit rationale, behaviour
identical to `a4c167631269e5110fbdcf323b6be2a779eaa1e0ca79c98201419261ba9c6bfb`
and to `df9ffdf963ef…` (the a4c16763 edit was the stale self-description fix —
docstring `C1 stale-statement census instrument v9 … FINAL` → `v10-r9` and the
`Usage: …c1-census-v9.py` line, i.e. the queue-drain rule-#14 discipline applied
to the instrument's own identity). Writes: this
report + `claims/c2/RV-5/**` only. No git mutation, no custody-path byte
touched, no install, scratch under `/dev/shm/rv5-arc3r2` (never `/tmp`).

## 0. Verdict — **CONFIRMED on the pinned landing, with one caught mid-flight false positive and one open label defect**

- On `a4c16763` (`df9ffdf9` behaviour): every legit input reads PASS exit 0
  (ordinary tree at HEAD, the r8-era DATED rows, the round-1 records text in
  both the landed and the drafted form, two historical r8 trees, and five more);
  every injection cell reads FAIL exit 1 with its declared class. The two new
  guards fire only on their fixtures.
- **Caught during the wave's landing churn (now fixed upstream):** revisions
  `076bd621` and `c95a5cf3` floored `g2_ok` per readable file **in the
  current-ok *locus* (block) unit** — the ordinary tree at HEAD then read
  `FAIL … DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']`, refuting the frozen C2
  element "ordinary runs at HEAD stay PASS 0/0/0/0" (receipts
  `T0-ordinary-v11b-FAIL.out`, `T0-ordinary-v11c-FAIL.out`). Cause measured:
  SKILL.md at HEAD has 2 loci / 0 current-ok loci (its only locus-bearing block
  is mixed → record disposition `info`), so any per-file **block** floor
  false-fails it. EX-14's own receipt had already flagged the class
  (`claims/c2/EX-14/live-floor-units.txt`: "hypothetical PER-FILE floor in the
  same unit (blocks): FALSE-FAIL on ['SKILL.md']"); the landed det-unit form
  (`df9ffdf9`+) resolves it.
- **Open nit (wording only):** the report line still says `current-ok loci per
  file` while printing **detection** counts (PROVINCE.md prints 17, its
  current-ok *loci* = 1; SKILL.md prints 3, its current-ok *loci* = 0) — patch
  text `claims/c2/RV-5/proposed-floor-label.patch.md`.

## 1. Work performed (evidence pointers)

- Read the frozen claims (`.ufo/waves/arc3-loop1-round2/claims-frozen.md` C2
  §34-50), the round-1 patch texts the chain merges (RV-11
  `proposed-missing-file-guard.patch.md`, CR-5
  `proposed-g2-positive-floor.patch.md`), the round-1 c3 verdict (H1..H6
  debt), SC-7's records-tree method, and CR-5's `scope-diff.py`.
- Captured every landing revision read-only into `/dev/shm/rv5-arc3r2/
  instruments/` (pinned copies): `6f1d19ff` → `82fb807e` → `3aa7ce91`(brief)
  → `076bd621` → `c95a5cf3` → `df9ffdf9` → `a4c16763` → `d0772ce8`; sha256 of
  each in `claims/c2/RV-5/fixtures.sha256`. Landing churn tracked by
  `claims/c2/RV-5/poll-log.txt` (60 s polls, 25 checks).
- Built a 21-cell fixture battery on `/dev/shm` (three scoped files per tree,
  built from git objects with `git show <rev>:<file>` — read-only):
  repo states `T0_ordinary`, `T1_r8work`(6bc4c29), `T2_r8rec`(276db3f),
  `T3_records`(e845c2b files + HEAD `SCORECARD.md:1337-1417` = the landed
  round-1 records text), `T3a_precommit`, `T4_records_draft`(SC-7 draft,
  BEGIN/END markers), `T13_symlink_ok`, `T16_exact_855`; injections
  `T5_missing_skill`, `T5b_missing_province`, `T5c_missing_scorecard`,
  `T5d_missing_all`, `T8_zero_byte_skill`, `T9_eacces_skill`,
  `T12_dir_in_place`, `T14_dangling_skill`, `T15_truncated_800`,
  `T17_one_short`; instrument variants `T6_blind` (all needles neutered) and
  the partial `PIN`-blind; content extractions `T7_r8rows` (only the r8-era
  DATED rows kept: SCORECARD 534-560 + 619-620 + every declared marker line,
  rest blanked), `T7b_r8rows_files_intact` (same card, PROVINCE/SKILL verbatim
  at HEAD), `T18_rekeyed_rows` (rows 636-702/703-768/769-855 only),
  `X2_all_historical`. Historical trees `T10_r7tree`(679af5d),
  `T11_r4tree`(265e1aa).
- Full battery run per revision; summaries `claims/c2/RV-5/receipts/
  matrix-all.txt`, per-cell quiet outputs, unit analysis `receipts/
  unit-probe.out` (in-memory `classify` import: per-file loci/dets/current-ok
  counts), label evidence `receipts/label-defect.txt`, guard-form
  discrimination cells `receipts/discriminants.txt` (T7b / X2 across v10,
  the interim block-floor, my det-floor prototype, and the landed revision).
- Independent re-run of the chain's own certificate: `python3 claims/c3/
  CR-5/tools/scope-diff.py <v10> <landed>` → `rows before=20 after=20`,
  0 added/removed/changed, `CREEP FLAGS: []` (`receipts/
  scope-diff-v10-to-v11d.txt`, exit 0) — the H1/H3 edit is scope-neutral.
- Cross-read EX-16's landing receipts (`claims/c2/EX-16/receipts/after/`:
  `after-sha256.txt` = df9ffdf9 @ 12:12:15Z, `matrix.md`, `floor-granularity-
  delta.txt`, h1/h3/h5 case logs) and EX-14's floor-unit probe; my per-file
  counts agree with EX-14's blocks table (PROVINCE 1 / SCORECARD 4 / SKILL 0
  current-ok loci) and with their dets table (17/14/3).

## 2. Proposed changes

- `claims/c2/RV-5/proposed-floor-label.patch.md` — one-line report-label fix
  (counts are detections, not loci) + optional header wording; print-text only.
- Nothing else. The mid-flight false positive is already fixed in the landed
  det-unit form, so no further patch text is proposed for it; had the
  block-unit form stood, the fix would have been the same substitution now
  landed (record-count → det-disp count).

## 3. Before→after measurement (chain c2 claim)

Before = `6f1d19ff…` (round-1 landing), after = `d0772ce8…` / `a4c16763…` /
`df9ffdf9…` (behaviour-identical; the battery was run on each).
Command per cell: `python3 <instrument copy> --root <tree> --quiet`
(exit code recorded; live anchors re-derived read-only from the three client
configs: `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`).

| cell | before (v10) | after (landed) | note |
|---|---|---|---|
| T0 ordinary tree (HEAD) | PASS 0/0/0/0 exit 0 | PASS 0/0/0/0 exit 0 | frozen element holds |
| T1 r8-work tree / T2 r8-records tree | PASS / PASS | PASS / PASS | r8-era trees unchanged |
| T3 round-1 records text (landed) | PASS | PASS | loci 6/9/2 |
| T3a pre-records / T4 records draft | PASS / PASS | PASS / PASS | draft text locus-free |
| T7b r8-era DATED rows, files intact | PASS | PASS | faithful r8-rows read |
| T13 SKILL.md via symlink | PASS | PASS | readable ⇒ no fire |
| T16 SCORECARD exactly 855 lines | PASS | PASS | boundary: no UNREADABLE |
| T10 r7 tree / T11 r4 tree | FAIL / FAIL | FAIL / FAIL | class changes only (below) |
| T5 SKILL.md absent | **PASS exit 0** | FAIL, `['UNREADABLE']` | H1 hole closed |
| T8 zero-byte / T9 EACCES / T12 dir / T14 dangling SKILL.md | **PASS** ×4 | FAIL, `['UNREADABLE']` ×4 | error classes named in output |
| T15 SCORECARD 800 lines | **PASS** | FAIL, `['UNREADABLE']` (`800 < declared max 855`) | silent shrink closed |
| T17 SCORECARD 854 lines | **PASS** | FAIL, `['UNREADABLE']` | one-line boundary |
| T5b province / T5c scorecard / T5d all absent | FAIL ×3 | FAIL ×3, `['UNREADABLE']` | class added, verdict unchanged |
| T6 blind needles (instrument variant) | **PASS exit 0** | FAIL, `['BLIND-INSTRUMENT']` | H3 hole closed |
| T7 / T18 / X2 extractions | PASS ×3 | FAIL `['BLIND-INSTRUMENT']` ×3 | see §4 A5 — construction boundary |
| partial blind (PIN only) | PASS | PASS | named residual (EX-16 header), re-measured |

Counts that make the H1/verdict change auditable at HEAD: `lines=None
loci=None` for the unevaluable file, the `UNREADABLE (could-not-evaluate):
[...]` line, `DECLARED FAIL CLASSES`, and `--json` fields `unreadable` /
`declared_fail_classes` (layout unchanged otherwise: legit-cell output is
byte-identical to v10 after stripping the three new line families —
`receipts/matrix-all.txt` + the same-tree outputs).

Mid-flight regression (caught, then fixed upstream):
`076bd621`/`c95a5cf3` → `T0 ordinary: FAIL exit 1, DECLARED FAIL CLASSES:
['BLIND-INSTRUMENT'], "current-ok loci per file: PROVINCE.md=1, SCORECARD.md=4,
SKILL.md=0"`; the same for every legit tree (`receipts/T0-ordinary-v11b-FAIL.out`
= `T0-ordinary-v11c-FAIL.out`). Root cause and the unit that fixes it are in
§0/§4.

## 4. Attacks / refutations attempted (with verdicts)

- **A1 — H1 silent classes beyond absence** (zero-byte, truncated, EACCES,
  is-a-directory, dangling symlink): all five re-read PASS exit 0 under v10 →
  declared FAIL under the landing (T8/T9/T12/T14/T15). **Verdict: closed.**
- **A2 — content shrink without file loss** (SCORECARD truncated to 800/854
  lines: all declared markers still present, rows past EOF silently dropped):
  v10 PASS → v11 FAIL `UNREADABLE` (T15/T17). **Verdict: closed** — this is the
  H1-adjacent class the round-1 patch text did not itself measure.
- **A3 — full blindness**: needles all neutered on the ordinary tree → v10 PASS
  exit 0; landing FAIL `['BLIND-INSTRUMENT']` (T6). **Verdict: closed.**
- **A4 — partial blindness (PIN only neutered)**: landing still PASS exit 0
  (`partial-blind-pin-v11d.out`). **Verdict: residual confirmed, correctly
  named in the landed header** (a token floor is not a coverage floor); only
  the external locus-count + scope-diff audit sees it.
- **A5 — construction boundary (false-positive scan):** trees of my own making
  that blank scoped content — T7 (r8 rows only, SKILL/PROVINCE blanked), T18
  (re-keyed rows only), X2 (all-historical) — read FAIL `BLIND-INSTRUMENT` even
  though they are not instrument-blind. With the files left intact (T7b) the
  same r8-era-row read is PASS. **Verdict: named boundary, not a repo-state
  false positive**; extraction-style `--root` uses (reduced copies) now read as
  collapses by design.
- **A6 — guard-form probe (the wave's real catch):** any per-file floor in the
  current-ok *locus/block* unit false-fails HEAD (SKILL.md = 0); the *det*
  unit holds (SKILL.md = 3). Measured on `076bd621`/`c95a5cf3` (FAIL at HEAD)
  and resolved by `df9ffdf9` (PASS). **Verdict: the interim landing was
  refuted; the pinned landing stands.**
- **A7 — label vs substrate:** printed `current-ok loci per file` counts
  detections (PROVINCE 17 vs 1 locus; SKILL 3 vs 0 loci). **Verdict: open
  wording defect → patch text** (same class as the round-1 `MTIME_UTC` label
  defect); no verdict effect.
- **A8 — historical trees mislabelled as new failures:** r7 (766-line) and r4
  (854-line) trees: FAIL in both revisions; classes change from
  `undeclared`/`SCOPE-ERROR` (v10) to `UNREADABLE: rows beyond EOF` (v11).
  **Verdict: not a false positive; class change worth naming** for the round
  report (re-running v11 against pre-round trees now reads UNREADABLE).
- **A9 — creep/scope movement hidden in the guards:** independent scope-diff
  run, 0 flags, 20/20 rows unchanged. **Verdict: refuted** (no widening).
- **A10 — legit-cell output drift:** after stripping the three new report line
  families, v11 legit-cell outputs are byte-identical to v10 (T0/T1/T2/T3/T3a/
  T4/T7b/T13/T16). **Verdict: no collateral behaviour change.**

## 5. Blockers, gaps, deviations

- **Landing churn (main hazard for this seat):** the target was revised seven
  times inside ~10 minutes (`6f1d19ff` 07:18 → `82fb807e` 12:06Z → `3aa7ce91`
  → `076bd621` 12:10Z → `c95a5cf3` 12:11Z → `df9ffdf9` 12:12:15Z → `a4c16763`
  12:15Z → `d0772ce8` 12:18Z). Every verdict above is pinned to a captured sha;
  if the parent lands
  further edits, re-run `bash /dev/shm/rv5-arc3r2/run-matrix2.sh
  /dev/shm/rv5-arc3r2/instruments/<pinned>.py <label>` (battery is
  sha256-keyed; receipts in `claims/c2/RV-5/receipts/`).
- **EX-16's seat report had not landed** at report time (no `seats/EX-16.md`);
  their receipts dir carries after-sha256/matrix/delta receipts — my verdict is
  against the bytes, not their narrative. `seats/RV-14.md`/`CR-2.md` landed
  during the seat; not cross-read (out of scope for this hunt).
- `/tmp` not used (standing EDQUOT record); scratch `/dev/shm/rv5-arc3r2`,
  kept for re-runs (fixture manifest `claims/c2/RV-5/fixtures.sha256`; the
  EACCES fixture's SKILL.md is mode 000 by construction and is listed as
  unhashable).
- Not attacked (out of this seat's remit, named for the parent): H2
  same-line inline-marker excusal, t5 DATED-shelter, H4 self-certification —
  all still named in the landed header; the H3 floor's cover of per-needle
  partial blindness remains the open residual (A4).
