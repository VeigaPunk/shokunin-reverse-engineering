# CriticNoHarm2 — round 17 wave 2: attack on "no axis harmed"

Target: lane revision `da64646` (H). Baseline `b563c79` (B). Predictions frozen at `2711674` (P).
Axes: calibration, depth. Seat: author-side advisory critic. I did not judge or admit anything.
Python ran as `-B`. All scratch went to `/tmp/cnh2-*`, which is removed. Nothing was installed.
I wrote nothing in the lane except this file. I did not run any carrier, REA command, or Ghidra.

## Findings

### F1 — HIGH (calibration, false provenance): SKILL rows cite a receipt that does not exist at H
- Where: `SKILL.md:448` (citation-drift) says "exercised argv: `.ufo/waves/round-16/verification.json` and `.ufo/waves/round-17/verification.json`". `SKILL.md:449` (custody-pair) says "exercised argv retained in `.ufo/waves/round-17/verification.json`".
- Command: `git cat-file -e da64646:.ufo/waves/round-17/verification.json`
  → `fatal: path '.ufo/waves/round-17/verification.json' does not exist in 'da64646…'`. The H tree listing of `round-17/` has no `verification.json`.
- Why it matters: claims.json C1(b) asks for "the citation-drift row is re-exercised with its isolated absolute argv and the receipt retained". At H, the registry row names a receipt that is not there. This is the same pattern as R16-INVOCATION, with the citation running in the other direction. It also breaks the corpus rule "an index row is a claim; write the row when the file exists" (fleet `CORPUS.md:46`).
- Mitigating (observation): L1's untracked `round-17/verify.py` (mtime 11:09:48) states it "writes verification.json". Its argv at `:135` and `:141` is `["python3","-I",…]`, which matches the row strings. The peer receipt `w2/citation-drift-head.json` used `python3 -I -B …`. That is a token variant, not the row's argv.
- Smallest fix: land `round-17/verification.json` in the same commit as SKILL rows 448/449, with its `citation-strict` and `custody-capture` argv token-equal to the row text. Until then, these rows must not cite it.

### F2 — MEDIUM (no-harm, frozen r16 dir; false "-B everywhere"): `predict.py --selftest` writes bytecode into `.ufo/waves/round-16/`
- Where: `.ufo/waves/round-17/tools/predict.py:290` spawns `[sys.executable, "-I", str(script), *argv]` without `-B`. Each child imports the absolute `_SELECTION_PATH` (`:69-72`, `:89-97`), which is the real r16 `selection.py`. The registry fixture check is `python3 -I -B …/predict.py --selftest` (`SKILL.md:534`). The outer `-B` does not reach the child.
- Repro (in `/tmp`, with `_SELECTION_PATH` rewired to a `/tmp` copy):
  `python3 -I -B .ufo/waves/round-17/tools/predict.py --selftest` → `SELFTEST: CLEAN cases=17`, exit 0. It leaves `./.ufo/waves/round-16/__pycache__/selection.cpython-314.pyc`. The direct CLI `--go-version go1.25.3 …` under `-I -B` writes nothing.
- Live state: `stat -c '%w birth | %y mod' .ufo/waves/round-16/__pycache__{,/selection.cpython-314.pyc}` → born `2026-10-20 11:08:56`. The H commit time is `11:06:06`. So the directory LOG says was removed has been recreated after the commit. L1's `verify.py:87` (`selftest-predict`) will recreate it on every run.
- Statements this falsifies:
  - `LOG.md:2056-2057`: "`-B` everywhere after a seat's pycache landed in the frozen round-16 dir (removed)".
  - `predict.py:55-56`: "Writes nothing outside the tempfiles created by --selftest".
  - `SKILL.md:534`: "read-only; stdout only" (for the fixture check).
- Scan: `grep -n '"-B"' .ufo/waves/round-17/tools/*.py` → no matches. Only predict's child imports a module; the other children run scripts as `__main__`, which writes no bytecode.
- Smallest fix: add `"-B"` at `predict.py:290`; `pins.py:182` and the others are optional for uniformity. Then delete `.ufo/waves/round-16/__pycache__`. Add a post-run `find .ufo -name __pycache__` emptiness check to `verify.py`, because the git-object controls cannot see ignored files.

### F3 — MEDIUM (depth/integrity): pins on `selection.py` do not bind the executed code, because a matching-header `.pyc` is loaded even under `-I -B`
- `-B` stops bytecode writes, not reads. `spec_from_file_location(...).exec_module` uses `__pycache__` whenever the header's mtime and size match the source.
- Repro (all in `/tmp/cnh2-x`; the source restored afterwards):
  1. Compile a same-length edit (`"missing_base"` → `"FORGED_PYC__"`) with the original mtime.
  2. Restore the original bytes and mtime. `sha256sum` of the source is `6917da09…ef430`, equal to the lane file.
  3. `python3 -I -B …/predict.py --go-version go1.26.2 --golang-root <installed golang>` → `FORGED_PYC__ {'fallback_to': '1.26.0', 'missing_bootstrap': False, … 'snapshot_route': 'fallback'}`. The prediction flips while every source pin stays equal.
- Bounding (observation):
  - The live lane `.pyc` is byte-identical to a fresh `py_compile` of the lane source with `dfile` set to the lane path (`bytes_eq True 14852 14852`, `code_eq True`). It is benign.
  - All 7 tool-derived frozen predictions at P replay identically with no `__pycache__` present (`expected`/`selection` equal for calib-esbuild-0.25.12, calib-shfmt, pro-aether, pro-containerd-shim, pro-esbuild-0.21.5, pro-notesmd-cli and pro-op; pro-esbuild-0.27.7 is a hand prediction). `pycache_after False`.
  - `predictions/SHA256SUMS` verifies (`SUMS_OK`). `git diff --stat P H -- predictions claims.json contract.md` is empty.
  - So no frozen prediction was harmed. The weakness is in the provenance mechanism.
- Smallest fix: in `_load_selection_module`, read the source bytes, check their sha256 against the pinned value, then `exec(compile(src, path, "exec"), module.__dict__)`. This loader never reads a `.pyc`. The alternative is to pin `__pycache__` absence in carrier-run/receipts.

### F4 — LOW (frozen gate dir, unrecorded residue): `.ufo/gates/citation-drift/__pycache__/citation-drift-probe.cpython-314.pyc`
- `stat`: born `2026-10-20 10:34:14`. That is after B (05:55) and before H, and the file is still present.
- `git status --short --ignored -uall .ufo/gates` → `!! …citation-drift-probe.cpython-314.pyc`. Nothing tracked changed.
- The module name shows the probe was imported by file path, not run. No tracked round-17 `.py` imports it; the only reference, `verify.py:135`, runs it as a script. The writer is unattributed.
- LOG names only the r16 removal.
- `.ufo/gates` and `.ufo/gates/custody-pair` both have directory mtime `08:14:08` (an entry was added or removed). Their tracked files are clean, and their mtimes are from 2026-10-19.
- Fix: delete it, and let the `__pycache__` check from F2 cover `.ufo/gates/`.

### F5 — LOW (SOURCES section discipline; tradeoff, not a registry violation): Leads bullets edited in place
- `git diff B H -- corpus/SOURCES.md` shows the old Leads text was replaced at `corpus/SOURCES.md:63` and `:65`: "no release source was opened…" → "resolved 2026-10-20 by S030…", and the GP-6528 lead was folded into a parenthetical.
- CORPUS rule 2 ("Only status, recheck and used-by change in place") covers registry rows, so these edits are not a row violation.
- However, the section header is `## Leads (unopened)` (`:59`), and it now holds opened/resolved text. The r17 `controls.py` checks registry cells only, so it cannot see these edits.
- Fix: leave only the unopened residue in each bullet ("whether v3.3/v3.4.1 recover types on a 1.26 carrier"). The resolution already lives in the round-17 Search-log entry and in rows S029/S030.

### F6 — LOW (intra-round evidence rewrite): a P-committed w1 report was rewritten before H
- `python3 -I -B .ufo/waves/round-17/controls.py 2711674… da64646…` → `prior_wave_evidence_blobs` names `w1/ConnProvenanceRoutes.md` (+25/−21), `tools/temporal-sweep.py` and `tools/buildinfo-probe.py`.
- The tool edits are expected integration. The report edit renumbers anchors (`:83-95`→`:83-93`, `:187-202`→`:179-195`) and replaces recommendation 3 (the `exercised_modulo_cwd` / `equivalence_unproven` classes become `exercised_path_normalized`).
- The pre-run evidence state at P is therefore not what H shows. The B→H control cannot see this, because the file did not exist at B.
- Fix: add an addendum under the original text. A rewrite should not replace a committed report.

## Bounded no-findings (what I checked)
- **LOG append-only.** `cmp` of B:LOG.md with the B-size prefix of H:LOG.md → `LOG_PREFIX_OK`; the file goes from 2031 to 2067 lines. SCORECARD and SHONEN are absent from `git diff --name-status B H`, so both are unchanged.
- **Lessons and knowledge.** Every B blob under `corpus/lessons` and `corpus/knowledge` has the same object id at H (my loop printed no `CHANGED`). r17 controls agree: lessons 20/20, knowledge 94/94, prior verifiers 12–16 unchanged. The only additions are `lessons/round-17.md` and `knowledge/2026-10-20-r17-go-carrier-diagnostics.md`.
- **Frozen r14–r16 bytes.**
  - `git diff --name-status B H -- .ufo/waves/round-1[0-6]` → empty. Controls B→H: `prior_wave_evidence_blobs` 14943/14943 unchanged, `quote_script_unchanged: true`.
  - My run's output equals the peer's `w2/controls.json`, apart from the invocation block.
  - On disk, tracked files are clean. `find … -newermt '2026-10-20 05:56'` lists nothing new under `round-14/15/16` except the F2 `__pycache__`.
- **Deleted r16 `__pycache__` left no tracked change.** Tracked `__pycache__`/`.pyc` count is 0 at B, P and H. `git check-ignore -v` → `.gitignore:1:__pycache__/`. Git shows the file only as `!!`; it has nevertheless been recreated (see F2).
- **SOURCES immutability.**
  - Cell diff by row: S003 and S023 each changed only cell 10 (`used-by`), and the old value is a prefix of the new one. No rows were removed. S024–S030 were added.
  - The old→new log at `corpus/lessons/round-17.md:64-65` matches B's used-by exactly (`True`/`True`).
  - Each new row has a Gate quote at `:39-55`.
  - The census commands from `CORPUS.md` report 30 rows, 0 malformed, no duplicate ids, no enum or tier-inflation violations, and no missing used-by paths. Controls agree: `immutable_cells_unchanged: true`, `immutable_violations: {}`.
- **QUALITY rows 1–18.** `difflib` opcodes show only `insert B29-28 H29-30`. Controls: `prior_rows_byte_identical: true`, `removed_rows: []`. Rows 19 and 20 have 4 cells each and cite lessons; both say "sharpens…" rather than superseding a row.
- **Citation pins.**
  - My own `python3 -I -B …citation-drift-probe.py --root <lane> --rev da64646… --table … --expected … --strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
  - In-place edits touch `PROVINCE.md:52`, `corpus/README.md:35` and `SKILL.md:448-449` without shifting lines.
  - `git grep` over SHONEN, SKILL, LOG, PROVINCE, README, SCORECARD, corpus and `.ufo/gates` finds no pointer into those lines. The one exception is `corpus/lessons/round-17.md:74`, which correctly describes `SKILL.md:448`/`:449` at baseline.
  - The line-shifted ranges (SOURCES ≥30, QUALITY ≥29) are cited only by frozen wave reports pinned to their own revisions.
  - All 36 new `path:line` citations in the added text were bounds-checked. The 17 unresolved ones are `Base-src.zip` Java paths and the out-of-lane fleet report. The one out-of-range flag is a false positive from glob resolution: `runs/pro-aether/…/ghidra.log` has 244 lines, which covers `:97-177`.
- **Coverage map.** All 96 `corpus/knowledge/*` files at H appear in the `corpus/README.md` map. The only map name that does not resolve, `lessons/round-13-distillation` (`README.md:138`), predates r17 and is not touched by the diff.
- **Edit footprint.** Outside `round-17/`, B→H modifies only LOG, PROVINCE (1 line), SKILL (2 rows rewritten plus an appended section), QUALITY (+2), README (1 row), SOURCES (2 used-by cells, 7 rows, Paths/Search-log additions, 2 Leads bullets), and adds the lesson and the knowledge file. B→P touches nothing outside `round-17/`.

## Impacted axes
- Calibration: F1 (false provenance in a registry row), F2 (LOG, docstring and registry claims falsified), F5, F6.
- Depth: F3 (the pins are weaker than they read). No retained run or prediction was harmed (replay is equal).
