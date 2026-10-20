# Review — in-place edits at `corpus/README.md:35` and `PROVINCE.md:52` (r17/w2)

Target: `git diff b563c799d97774aae4351276fe43cb897311e349 da64646adcb19c1ede7537b799b8c7d283fe43da -- corpus/README.md PROVINCE.md`.
Seat: author-side advisory (leaf). Read-only; no repo file edited except this report.

## 1. What the diff actually is (observation)

`git diff --numstat` → `1 1 PROVINCE.md`, `1 1 corpus/README.md`; `git diff --unified=0` hunks are only `@@ -35 +35 @@` and `@@ -52 +52 @@`. Line counts unchanged: `190` / `162` at both revisions. `git diff --check` exits 0.

Exact insertions (Python `difflib` on the old/new line).

`corpus/README.md:35`, cell 1 token (appended):

```text
, `2026-10-20-r17-go-carrier-diagnostics`
```

cell 2 (appended):

```text
; r17 retains bound Ghidra analyzer logs for eight pinned carriers (1.20–1.27, no-build-info), 8/8 routes matched frozen predictions incl. the 1.25.x fallback WARN
```

cell 3 (appended):

```text
; r17: `bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/run-carriers.sh <LABEL>`, receipts in `.ufo/waves/round-17/runs/`
```

`PROVINCE.md:52` (inserted after ``…r14-go-version-diagnosis.md`; ``; trailing space before the original text):

```text
current `op` 2.41.0-1 (go1.26.8) observed missing-base bootstrap failure with a bound retained log, a different binary from the historical pair (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`); 
```

## 2. Findings

### F1 — HIGH (support chain): the r17 entry's named recheck exits 1 on **all eight** retained receipts — validator/ producer shape mismatch

Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3` (recheck cited by the README row), `tools/receipt-validate.py:98,284`, `tools/carrier-run.py:275,349`.

Exact command (the entry's own recheck, absolute form):

```
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/pro-op/receipt.json
```

Observed output (excerpt): `"checks_performed": 306`, `"findings": [{"code": "unrecognized_shape", "detail": "receipt matches neither retain nor carrier shape", "where": "$"}]`, `"kind": "unknown"`, `"status": "invalid"`, exit `1`. The same result for all eight `runs/*/receipt.json` (each `invalid: 1`, exit `1`).

Cause (code reading; observation): `carrier-run.py:275` initialises `"steps": {}` and `:349` assigns a **dict** keyed `inspect-go-binary`/`analyze`/`search:*`; `receipt-validate.py:98` classifies the carrier shape only when `isinstance(receipt.get("steps"), list)`. `:284` then iterates `enumerate(receipt.get("steps") or [])`, which would emit a `field_type` finding per dict key even if only the classifier were widened. The validator's selftest fixture is a **list** (`receipt-validate.py:470`), so `--selftest` prints `SELFTEST: CLEAN cases=5` and cannot catch the real producer shape.

Calibration: the 306 generic checks did run; the **only** finding is `unrecognized_shape` — no digest, size, pin or `pins_compare` mismatch was reported. So the README's factual claim (logs retained, bound, pins equal) is not falsified; the **named recheck** is. This matters because claims.json C2 makes the capability row conditional on "its receipt validates"; at da64646 that condition fails under the round's own validator.

Smallest fix: in `receipt-validate.py`, accept `steps` as `dict` in `classify`, iterate `steps.items()` (name-keyed `where`) in the carrier branch, and add one selftest fixture shaped like a real `carrier-run.py` receipt. Do **not** change `carrier-run.py` to a list: that would invalidate the retained receipts the README cites.

### F2 — MEDIUM: the README's rerun command destroys the retained run it points at

Target: `corpus/README.md:35` (added `bash …/run-carriers.sh <LABEL>` clause); `run-carriers.sh:14-15` at da64646.

Exact:

```
git show da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/run-carriers.sh | sed -n '11,16p'
```

Observed:

```
only="${1:-}"
while IFS=$'\t' read -r label path kind; do
  [ -n "$only" ] && [ "$only" != "$label" ] && continue
  out="runs/$label"
  rm -rf "$out"; mkdir -p "$out"
```

Running the README's `<LABEL>` form deletes `runs/<LABEL>` (receipt, logs, observation, compare) before rerunning. The entry's recheck says "then rerun one carrier … and compare `observation.json` fields" — the original `observation.json` is gone, and the new receipt is not the retained one. The worktree has an **uncommitted** mitigation `out="${RUNS_DIR:-runs}/$label"` (git status ` M .ufo/waves/round-17/run-carriers.sh`); it is not in da64646 and the README does not mention `RUNS_DIR`, so the default remains destructive.

Smallest fix: either land the `RUNS_DIR` change and make the README command `RUNS_DIR=/tmp/kr17-rerun bash …/run-carriers.sh <LABEL>`, or state in the README/entry "copy `runs/<LABEL>` first; the script removes it." The former is preferable; it also makes the recheck non-destructive.

### F3 — LOW/MEDIUM: frozen-prediction commit is a transposition typo in two places

Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37`, `run-carriers.sh:2`.

Exact:

```
git cat-file -t 2716747
```

Observed: `fatal: Not a valid object name 2716747`. The frozen commit is:

```
git show -s --format='%H %ci %s' 271167473d87ef710f07ecdd98caf0ce12091686
→ 271167473d87ef710f07ecdd98caf0ce12091686 2026-10-20 10:46:45 -0300 round-17: frozen carrier predictions, …
```

The entry header line 1 has the correct full hash and the predictions are present at that commit (`git cat-file -e 2711674:.ufo/waves/round-17/predictions/pro-op.prediction.json` → present), so the claim is recoverable. But the method paragraph and the producer's own comment name a nonexistent commit, weakening the "frozen predictions" audit trail the README summarizes. Smallest fix: replace `2716747` with `2711674` in both files.

### F4 — LOW: `(1.20–1.27, no-build-info)` reads as a set-wide property; only 1/8 lacks build info

Target: `corpus/README.md:35`.

Exact:

```
python3 -B -c "import json,glob,os; [print(os.path.basename(os.path.dirname(p)), (json.load(open(p))['normalized_result'].get('build_info') or {}).get('go_version')) for p in sorted(glob.glob('.ufo/waves/round-17/runs/*/inspect-go.json'))]"
```

Observed: `go1.20.12`, `go1.23.12`, `go1.25.8`, `go1.25.14`, `go1.26.8`, `go1.27.0-X:nodwarf5`, `go1.27.2-X:nodwarf5`, and `null` only for `pro-esbuild-0.27.7` (entry line 58). Seven carry build info. The parenthetical can be parsed as "the eight have no build info", which is false; it is also a non-contiguous set (1.21/1.22/1.24 absent). Smallest fix: `(1.20–1.27; one no-build-info)` or `(7 build-info + 1 no-build-info)`.

### F5 — LOW: `8/8 routes matched frozen predictions` omits the pilot-informed 2/8

Target: `corpus/README.md:35`.

Exact:

```
sed -n '37,38p' corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
```

Observed: "all eight carriers were committed at `2716747` before the first run. The two `calib-*` carriers had been seen in the pilot. The six `pro-*` carriers had not." The README's headline `8/8` is true (all `compare.json` `all_match:true`), but a reader can take it as eight blind predictions; 2/8 are pilot-informed. Smallest fix: `8/8 (6/6 prospective + 2/2 pilot-informed)` or `8/8, 6/6 blind`.

## 3. Bounded no-findings (what I checked, with evidence)

- **Line counts unchanged / no line added.** `git diff --numstat` → `1 1` each; `wc -l` → `190` / `162` at both revisions; `git diff --unified=0` hunks only `-35 +35` / `-52 +52`.
- **No pinned line shifted.** Pointer table entries for these files are `corpus/README.md:22` (`readme22-*`), `:175` (`readme175-*`), `PROVINCE.md:18` (`prov18-*`); none at 35 or 52. `python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`; `sha256sum .ufo/gates/citation-drift/pointer-table.json` → `7994eec7e764e8c3195dd79efb850b63d437aa610e6a9d96ed24484bb53789d1`, identical to `expected.json` `pointer_table.sha256`. The archived `luna-round-1/V14.md:8` citation to `corpus/README.md:35` still resolves because the r4-10 token and its summary remain on the line.
- **README claims supported by the r17 entry / receipts.** Eight receipts; each `bound_sessions` length 1, `unbound_sessions` 0, `retained_logs[].binding = {logfile_ok: true, target_ok: true}`, one `logs/…/ghidra.log`; all eight `carrier.sha256_pre == sha256_post` and `pins_compare.equal == true`; all eight `compare.json` `all_match:true` with `compare.exit=0`; `carriers.tsv` has eight rows. The r17 entry is committed at da64646 (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`, blob `f4796cb…`). README's `## Knowledge` table has no r14/r15/r16 Go rows either (`grep -n '2026-10-20-r1[4-7]' corpus/README.md` → only line 35, this map row, and line 140, the r4-10 row's source column), so r17's absence there is precedent, not an omission introduced by this edit (also stated in `w1/DraftReadmeRow.md`).
- **No overclaim about the historical `op` pair.** The inserted PROVINCE clause says "a different binary from the historical pair"; the same row retains "precise old cause remains unknown"; the entry's inference (lines 117-120) says the historical 2.40.0 cause stays UNKNOWN and the current 2.41.0-1 is a different binary. The current claim is supported: `pacman -Q 1password-cli` → `1password-cli 2.41.0-1`; `sha256sum /usr/bin/op` → `f4ac474fd0202c73e93cec7ff35e5c7a0b46df593b8717c92a262ecd4d77f818`, equal to the receipt's `sha256_pre`; `runs/pro-op/logs/…/ghidra.log:69-70` → `Untested Go version [1.26.8]` and `Missing Go bootstrap type info`. The phrase "missing-base" is the entry's decision-table label (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:105`), not a claim about the historical pair; the entry's inference that the runs cannot separate range-check from missing base is preserved in the entry, while the source (`GoRttiMapper.java:170-172` only logs) is cited there. No wording change required.
- **Formatting.** No inserted `|` (table cells intact); `git diff --check` exit 0; no trailing-whitespace change.

## 4. Residual risks / verification gaps

- F1 is a **tool** defect, not a falsification of the README/PROVINCE wording: the raw receipts and the validator's 306 generic checks show no digest/pin mismatch. But a reader following the entry's recheck gets `status: invalid, exit 1`; fix the validator before the capability row / C2 "receipt validates" is presented as discharged.
- F2's worktree mitigation is uncommitted (`git status` shows ` M .ufo/waves/round-17/run-carriers.sh`); the reviewed commit remains destructive. If it lands, the README command must mention `RUNS_DIR` or the default still overwrites.
- The two `calib-*` predictions are pilot-informed and `pro-esbuild-0.27.7` was hand-written (entry line 39-40); the 8/8 is not eight blind predictions. The README compression drops both qualifiers (F5/F4 are the visible parts).
- Carrier paths for the three pnpm esbuild carriers live under `~/Projects/kimi-code/node_modules/.pnpm/…` (mutable); receipts pin the bytes, and the entry warns about package upgrades — the README's "pinned carriers" is true at run time, not a durability claim.
- Review pinned to `da64646…`; the worktree also has untracked `verify.py` and wave-2 files. `corpus/README.md` and `PROVINCE.md` are clean in the worktree, so the line evidence above is against the reviewed commit.

## 5. Tools / installs

No installs or upgrades. Commands: `git show/diff/log/cat-file/ls-tree`, `python3 -I -B` (stdlib, `-B`), `sha256sum`, `pacman -Q` (read-only), `grep`, `sed`, `jq`, `nl`, `find`. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier execution.
