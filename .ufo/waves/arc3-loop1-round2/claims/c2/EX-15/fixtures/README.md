# EX-15 fixture pack — census fail-closure fixtures (chain c2, arc3-loop1-round2)

Reusable, hermetic fixture roots + harness for the two declared new fail classes
of the C2 claim:

* **H1 / `UNREADABLE`** — a scoped file that cannot be evaluated (absent,
  zero-byte, truncated below its declared max end, EACCES, directory, dangling
  symlink) must FAIL exit 1 with the declared class, whatever its row classes.
* **H3 / `BLIND-INSTRUMENT`** — the G2 positive floor must FAIL a run whose
  readable files contribute no current-ok locus. The landed r9 floor is
  **per readable file over current-ok detections** (`>= 1` per file the run
  could read).

Validated against the frozen pre-edit instrument (v10, sha `6f1d19ff…`, 490
lines) and the live landed r9 revisions (`82fb807e…` → `c95a5cf3…` (transient,
claim-breaking — PL-2 §0) → `df9ffdf9…` → `a4c16763…` → `d0772ce8…`; the last
three are behaviorally identical, header/Usage/docstring text only).

## Layout

```
fixtures/
  gen_fixtures.py        deterministic fixture builder (parses SCOPE from the instrument)
  run_fixtures.py        harness: materialize -> run -> check cases.json expectations
  cases.json             the contract: classes, phase pins, per-case expectations
  manifest.sha256        sha256 + length of every generated file (33 files)
  fakehome/              hermetic HOME: all three clients pinned to rea-agents@9.9.9
  roots/<case>/…         materialized scratch roots (PROVINCE.md / SKILL.md / SCORECARD.md)
  measurements/<phase>-<sha8>/    raw per-case output + results.json (+ instrument snapshot)
```

## Design rules

* **Hermetic anchors.** H1/H3 roots run under `fakehome/` (`HOME` env), so no
  outcome depends on the live custody configs or on repo-file drift. The
  `ctl-head` control deliberately runs under the real HOME on the repo's own
  files — it is the claim's "ordinary run stays PASS" clause.
* **Derived, not hard-coded, marker placement.** `gen_fixtures.py` parses the
  `SCOPE` table out of the instrument and asserts each DATED row's marker regex
  against the text it places at the declared line; a re-keyed SCOPE table makes
  the generator fail loudly instead of emitting a broken tree. Natural file
  length = the file's declared max end (PROVINCE 131 / SKILL 20 / SCORECARD 855),
  so the r9 truncation rule (G19) is never tripped by accident.
* **Token scan.** The blind base is proven to carry zero `REA_GATE` matches
  (pattern parsed from the instrument's own regex), so `blind-nonempty` is a
  *legitimate* data-side twin of round-1 CR-5's needle-neutering attack.
* **Per-file loud controls.** The r9 floor is per readable file, so every
  legitimate root carries one current-ok locus per shipped file
  (`PROVINCE.md:20`, `SCORECARD.md:58`, `SKILL.md:19`; `omp pin rea-agents@9.9.9
  receipt 2026-10-19 alignment note.`). Floor probes are built by collapsing
  exactly one file (`partial-blind-skill`, `hist-only`).
* **No repo or custody writes.** The harness materializes cases under
  `/dev/shm/ex15-fixtures` (never `/tmp`, per the round's EDQUOT record) and
  removes them unless `--keep`. Custody paths are never opened by this pack.

## Usage

```bash
python3 gen_fixtures.py                  # rebuild roots/ + fakehome/ + manifest.sha256
python3 run_fixtures.py --phase before \
  --instrument .ufo/waves/arc3-loop1-round2/claims/c2/EX-16/tools/census-before.py \
  --expect-sha 6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b --json-check
python3 run_fixtures.py --phase after \
  --instrument .ufo/gates/c1-census-v10.py --json-check   # --expect-sha optional but recommended
```

Exit 0 iff every `hard`-severity case matches its phase expectation; `advisory`
cases report as WARN; `reading` cases report which mechanism the instrument
exhibits. Raw output per case, the instrument sha, and `results.json` land under
`measurements/<phase>-<sha8>/`. If EX-16 lands a new revision, re-run
`--phase after` and record the new sha (the harness refuses a stale `--expect-sha`).

## Cases and measured behaviour

Measured 2026-10-19: before = `6f1d19ff…` (EX-16's frozen copy), after =
`d0772ce8…` (live target, r9 at this seat's close; docstring/naming-only deltas
vs `df9ffdf9…`/`a4c16763…`).

| case | class | before | after (r9) |
|---|---|---|---|
| `ctl-head` (repo files, real HOME) | control | PASS exit 0 | PASS exit 0 (`PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3`) |
| `current-ok-ctl` (1 loud locus/file, fakehome) | control | PASS exit 0 | PASS exit 0 (`…=1` per file) |
| `blind-nonempty` (non-empty, zero loci) | H3 | PASS exit 0, `loci=0` | FAIL exit 1, `['BLIND-INSTRUMENT']` |
| `partial-blind-skill` (only SKILL.md blind) | H3 | PASS exit 0 | FAIL exit 1, `SKILL.md=0`, others `=1` |
| `hist-only` (SCORECARD historical locus only) | reading | GLOBAL (PASS) | PER-FILE (FAIL, `SCORECARD.md=0`) |
| `miss-skill` | H1 | PASS exit 0 (silent — the H1 injection) | FAIL exit 1, `['UNREADABLE']`, `SKILL.md: FileNotFoundError` |
| `miss-skill-dir` | H1 | PASS exit 0 | FAIL exit 1, `IsADirectoryError` |
| `miss-skill-dangling` | H1 | PASS exit 0 | FAIL exit 1, `FileNotFoundError` |
| `miss-skill-mode000` (EACCES, uid 1000) | H1 | PASS exit 0 | FAIL exit 1, `PermissionError` |
| `miss-province` | H1 | FAIL exit 1 (marker uncheckable) | FAIL exit 1, `['UNREADABLE']` + SCOPE-ERRORs |
| `miss-scorecard` | H1 | FAIL exit 1 (marker uncheckable) | FAIL exit 1, `['UNREADABLE']` + SCOPE-ERRORs |
| `miss-all` (empty root) | H1 | FAIL exit 1 | FAIL exit 1, all three named |
| `empty-skill` (zero-byte, H1b residual) | advisory | PASS exit 0 | FAIL exit 1, `0 lines < declared max 20` |
| `h2-inline-excuse` (fabricated pin + `superseded`) | advisory | PASS exit 0 | PASS exit 0 — H2 stays open |
| `fold-mixed-block` (folded current-ok+historical) | reading | VACUOUS-PASS | ASSERT-COUNT (PASS, `SCORECARD.md=1`) |
| `h5-gate-free` (`6.7.0` statement, no gate token) | advisory | PASS exit 0 | PASS exit 0 — H5 unit boundary by design |

Full raw output: `measurements/before-6f1d19ff/` and `measurements/after-d0772ce8/`.

## Findings handed to the chain

* **F-1 (floor granularity, now fixed and pinned).** A folded block whose asserts
  mix `current-ok` + `historical` aggregates to `info`; a *block-counted* floor
  undercounts it. Measured across the r9 revisions: r1 `82fb807e` global floor
  FAILs a fabricated-block tree with `current-ok loci=0, total loci=1`; r2
  `c95a5cf3` (per-file, blocks) FAILs with `SCORECARD.md=0`; r3+ `df9ffdf9`
  (per-file, detections) PASSes with `SCORECARD.md=1`. The same class was
  independently found by EX-14/PL-2 at HEAD (SKILL.md's only locus-bearing block
  is mixed, so block-counting false-FAILs the ordinary run). `fold-mixed-block`
  pins the reading: `ASSERT-COUNT` / `UNIT-COUNT` / `VACUOUS-PASS`.
* **F-2 (self-identity churn).** The instrument moved five times inside the round
  (`82fb807e` → `c95a5cf3` → `df9ffdf9` → `a4c16763` → `d0772ce8`); receipts
  captured at one revision go stale at the next (PL-2 §0 names the r1 citation
  in `after-sha256.txt`; the file now cites `d0772ce8…`). This pack sidesteps
  the hazard by keying each measurement dir to the instrument sha and
  snapshotting the measured revision beside the raw output.
* **F-3 (residuals that stay open, measured).** H2 (inline-marker excusal) and
  H5 (gate-free version statement) still read PASS after the fix — both are
  declared-not-closed in the landed header; `h2-inline-excuse` and
  `h5-gate-free` pin that state. The landed header also names per-needle partial
  blindness as residual (EX-16's `h3-blind-pin` reads PASS by design).
* **F-4 (cosmetic, patch text).** The landed header carries the "Still named,
  NOT closed here" bullet twice (`:82-85`, still present at `d0772ce8`). Patch
  text: `proposed-header-dedup.patch.md`.

## Contract caveats

* Expectations name the declared class labels as landed (`UNREADABLE
  (could-not-evaluate)`, `BLIND-INSTRUMENT`, `DECLARED FAIL CLASSES:`, the
  `current-ok loci per file` G2 substratum). If a future revision renames a
  label, edit `classes` in `cases.json` — it is the single knob.
* The per-file floor means fixture roots are only valid under the r3+
  semantics; the `partial-blind-skill` / `hist-only` readings detect a revert.
* `empty-skill` and `h2-inline-excuse` are `advisory`: a differently-worded
  (stronger or weaker) implementation is reported, not failed.
* Files in `roots/` are generated; regenerate after any SCOPE re-key rather
  than editing them by hand (`manifest.sha256` will show the drift).
