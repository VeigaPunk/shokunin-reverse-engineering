PARTIAL

# AxisHarmCheck: B→REV harm across the six axes (round 18, wave 2)

Seat `KaidokuR18.AxisHarmCheck`, author-side advisory. This is not an outside review and not an admission.

- B = `9011581d84527ba34c675f9cf912e54d2e72d470`
- REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`
- freeze = `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`
- Every `path:line` below is read at REV with `git show REV:path` unless a revision prefix says otherwise.
- Sandbox: `T=/tmp/axisharm-Z96RxX`. It is a `git clone --no-hardlinks` of the lane with origin removed, plus a B worktree. All tool runs used `HOME=$T/home TMPDIR=$T/tmp`.
- Nothing in the lane was written except this report. I did not run jj, REA, Ghidra or any carrier binary, and I installed nothing.

## Verdict

**PARTIAL.** Within the lane's own control scope, no previously admitted entry became false and no lane proxy went down. Callers passing an explicit SHA as `--rev` get unchanged verdicts.

There is real harm on **operability** and **calibration**:

- REV adds clone-safety guidance that does not hold.
- The edited custody tool breaks when it is run as a copy, which is a pattern the lane has used before.
- One registry count is now false.
- The invocation-audit proxy regressed: unlabelled variants went from 0 to 9.
- Callers passing a literal `--rev HEAD` regress in repos that have no `main` branch.

## Findings, by severity

### F1 — MEDIUM (operability, calibration): the r17 `verify.py` "throwaway clone" advice is false and unsafe

**Where.** `.ufo/waves/round-17/verify.py:10-17` (new at REV) says rerunning "overwrites that retained round-17 evidence … run it only in a throwaway clone". The script hardcodes the real lane path:

- `LANE` at `:30`
- `OUT` at `:33`
- the write to `W + "/verification.json"` at `:234`
- an REA carrier run, `go-carrier-run-replicate`, at `:213-214`

**What happens (observation).** I imported the clone's copy of the script without calling `main()`:
- `LANE` and `OUT` resolve to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/...`.
- `resolve_source()` returns `findings: []`, because the real lane has HEAD = `main` = `origin/main` = REV and its tracked files are clean.

**Consequence (inference, from code; `main()` was deliberately not run).** Following the advice from a clone would pass the new jj guard. It would then overwrite the retained r17 `verification.json` and `verify/` in the real lane and launch `npx rea-agents analyze`. At B the docstring made no clone claim, so this is new false guidance.

**Reproduce:**

```
env GIT_OPTIONAL_LOCKS=0 python3 -I -B -c "import importlib.util as u; p='$T/lane/.ufo/waves/round-17/verify.py'; s=u.spec_from_file_location('v',p); m=u.module_from_spec(s); s.loader.exec_module(m); print(m.LANE, m.OUT); print(m.resolve_source())"
```

Exit 0. It prints the real-lane `LANE`/`OUT` and `'findings': []`. Its git probes on the real lane are read-only, with optional locks off.

### F2 — MEDIUM-LOW (operability): `custody-pair.py` regresses when run as a copy

**Where.** REV pins the repo root as `LANE_ROOT = TOOL_PATH.parents[3]` (`.ufo/gates/custody-pair/custody-pair.py:214`, used at `:744` and as the default at `:1436`). The docstring at `:110` claims this is "the directory containing `.ufo`". That only holds at the canonical path.

**Observation, with extracted copies:**

- **Copy directly under a mkdtemp dir.**
  - B: `capture` exit 0; `selftest` exit 0 (28/28).
  - REV: `capture` exit 1 and `selftest` exit 1, both with `IndexError: 3` at import.
  - Every subcommand fails, including `verify`, which needs no repo at all.
- **Copy four levels deep outside a lane.**
  - REV `capture` exit 0, but it records `# repo-root: /tmp/axisharm-Z96RxX`, `repo-HEAD: (none)` and `repo-HEAD-is-branch-tip: no`. The root is an unrelated directory.

**Why it matters.** The lane has run copies this way before:
- `.ufo/waves/arc3-loop1-round4/seats/EX-23.md:26` used `/var/tmp/ex23/custody-pair-BASE-…py`. Under REV, `parents[3]` of that path is `/`.
- `.ufo/waves/arc3-loop1-round2/seats/CU-1.md:105` used `/var/tmp/cu1-r2/custody-pair.py`.

**Reproduce:**

```
git -C $T/lane show $R:.ufo/gates/custody-pair/custody-pair.py > $T/custody-pair-rev.py
HOME=$T/home python3 -I -B $T/custody-pair-rev.py capture --out - --paths $T/fixture.txt
```

Exit 1 with `IndexError: 3`. The same commands with the B blob exit 0.

### F3 — LOW-MEDIUM (operability proxy decreased): unlabelled invocation variants went from 0 to 9

**Observation.** The r17 `invocation-audit.py`, run on the real lane's Git objects, reports:

- **B:** 17 rows, 17 `exercised_match`, 0 `unlabelled_variant`.
- **REV:** 26 rows, 17 `exercised_match`, 9 `unlabelled_variant`. These are the nine new rows `SKILL.md:565` and `:586-593`.

This is the same defect class as R16-INVOCATION, which round 17 closed (`corpus/lessons/round-17.md:82`).

**Inference: four rows will likely stay unlabelled after the planned verification pass.** `.ufo/waves/round-18/verify.py` exercises the argv of `routed-defects`, `head-rev-lint`, `jj-red-before`, `round18-measure` and `round18-structural-controls` (`:178`, `:183-191`, `:234-236`). It does not exercise the registered entry argv of:

- `r18-prediction-freeze` (`SKILL.md:565`)
- `revpin` (`:588`)
- `swiss-misread` (`:590`)
- `go-carrier-run-r18` (`:591`)

`verify.py` only runs `--selftest` for `revpin` and `swiss-misread`. The retained run log records a different argv: `runs/run-log.txt:1`, `bash .ufo/waves/round-18/run-carriers.sh (all labels)`.

**Reproduce:**

```
python3 -I -B $T/lane/.ufo/waves/round-17/tools/invocation-audit.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <B|REV>
```

Exit 0 at both revisions, with the counts above.

### F4 — LOW (calibration: an admitted registry entry is now false)

`SKILL.md:449` (the custody-pair registry row) still says "28 fixture cases". The REV selftest runs 30, because REV added cases 26 and 27 at `custody-pair.py:1336-1387`.

- `python3 -I -B $T/lane/.ufo/gates/custody-pair/custody-pair.py selftest` → exit 0, `CUSTODY_PAIR_SELFTEST: CLEAN cases=30`.
- The B tool prints `cases=28`.

The row also does not mention the new `--repo` flag or the five new header lines.

### F5 — LOW (behaviour regressed for explicit-rev callers): literal `--rev HEAD` in a repo without `main`

**Observation, minimal repro.** Fixture: a repo with branch `master`, HEAD at its tip, and an empty pinned table.

| Tool | Exit | Output |
|---|---|---|
| B | 0 | clean |
| REV | 2 | `head_not_branch_tip … != refs/heads/main (missing)` |

On that refused run, REV also prints `CITATION_DRIFT_REV_RESOLVED: HEAD`, which is not a resolved revision. This comes from `.ufo/gates/citation-drift/citation-drift-probe.py:329-335`, plus the earlier `findings.rev_resolved = rev` at `:348`, which is never reset.

Two related points:

- **Wrong finding id.** `SKILL.md:448` says "(`branch_missing` when the branch is absent)". For `--rev HEAD` the probe emits `head_not_branch_tip` instead; `branch_missing` appears only when `--rev` is omitted.
- **Stdout contract change.** The `CITATION_DRIFT_REVISION:` line is gone, replaced by `_REV_REQUESTED`/`_REV_RESOLVED`/`_BRANCH` (`:397-401`). The only live in-lane parser is `.ufo/waves/round-18/tools/jj-red-before.py:196-198`, which reads `REV_RESOLVED` or falls back to `REVISION`, so it handles both forms. No live caller passes literal `HEAD` except selftests and red-before fixtures (`jj-red-before.py:390`, `:577`). The fleet's `kotoba-shokunin` (branch `master`) cites this probe only as prior art.

Callers passing an explicit SHA are unchanged:
- Fixture: B and REV both exit 0.
- Strict run on the lane: B at B exits 0 clean; REV at REV exits 0 clean (0 findings).

**Reproduce:**

```
d=$(mktemp -d -p $T/tmp mini-XXXX) && git init -q -b master $d/r && git -C $d/r -c user.email=e@x -c user.name=e commit -q --allow-empty -m c && echo '{"entries": []}' > $d/t.json && python3 -I -c "import hashlib,json,sys;json.dump({'snapshots':{},'pointer_table':{'sha256':hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()}},open(sys.argv[2],'w'))" $d/t.json $d/e.json && for v in base lane; do python3 -I -B $T/$v/.ufo/gates/citation-drift/citation-drift-probe.py --root $d/r --rev HEAD --table $d/t.json --expected $d/e.json --strict; echo "$v exit=$?"; done
```

Result: `base exit=0`, `lane exit=2`.

### F6 — LOW (calibration): the claims amendment's timestamp contradicts its own "before any REA run"

`.ufo/waves/round-18/claims.json:35` stamps the amendment `2026-10-20T13:25:00-03:00 (… before any round-18 REA run)`. But the first REA run started at `13:24:07-03:00` (`runs/run-log.txt:2`).

The substance does hold (observation):
- The amendment is already present at eb6c266, whose committer date is 13:23:55-03:00.
- All 15 `runs/*/producer.json` files record `branch_tip` = eb6c266.
- `corpus/lessons/round-18.md:18` correctly uses the commit time (16:23:55Z) and the first run step (16:24:08Z).

So the stamp itself is false.

### F7 — LOW (calibration): the C1 gate was edited after the freeze commit, without an amendment

`routed-defects.py:277-288` changed between eb6c266 and REV. The old check looked for the placeholder id `mid_map_mismatch`, which the validator never used. The new check requires both real ids.

**Observation, both run at REV:**
- The eb6c266 gate: exit 0, `open_count` 1. R17-PINMAP stays open with "'mid_map_mismatch' only in comments/docstrings or absent".
- The REV gate: exit 0, `open_count` 0.

The new check is stricter in form. But C1's "→0" depends on it, and the edit is disclosed only in a code comment. `git grep` for these ids in `contract.md`, `claims.json`, `lessons/round-18.md` and `LOG.md` exits 1 (no match).

## Held (no harm observed)

- **Lane controls.** r17 `controls.py B REV` exited 0; under `.ufo/waves/` only the six contracted in-place edits and the `SHA256SUMS` line changed. r18 `controls.py B REV` exited 0, with `r17_sums_restored_line.restored_ok: true`.
- **Corpus integrity.**
  - QUALITY rows 1-20 are byte-identical, and row 21 was appended.
  - SOURCES immutable cells are unchanged; rows went from 32 to 36.
  - `LOG`/`SCORECARD` were only appended to.
  - Knowledge and lessons prefixes are preserved (95/95 and 22/22).
  - Verifier spot-checks are byte-identical.
- **Proxies.**
  - r17 `measure.py` at B and at REV (both exit 0) shows only increases: knowledge 95→96, sources 32→36, mined 30→34, tier A 28→31, tier B 3→4.
  - `temporal-sweep` at both revisions (exit 0): 4 sites, 0 unqualified.
- **In-place r17 tools on retained inputs (B tools vs REV tools).**
  - `log-extract`: 26/26 logs, identical shared keys.
  - `compare`: 8/8 identical exit codes and stdout.
  - `receipt-validate`: 9/9 r17 receipts exit 0 under both.
  - Every selftest is green, with more cases at REV: 13→15, 28→30, 15→23, 8→13, 9→18, 2→3.
- **Custody receipt compatibility.** A B-made receipt and a REV-made receipt `verify` as MATCH in both directions, with either tool (exit 0).
- **Frozen predictions.** `.ufo/waves/round-18/predictions/` is byte-identical from eb6c266 to REV. All 15 compares exit 0. 15/15 receipts exit 0 under `--require-mid-maps`.
- **New correction anchors check out.**
  - `9011581:.ufo/waves/round-17/tools/carrier-run.py:479-487` is the verdict-only append.
  - Blob `bc964ac` is at 2711674 and blob `c536e3e` is at 95e34db.
  - There are 29 analyze `pin_checks` at B.
  - The `validate16` summary shows 8 receipts with exit 0.

## Residual risk and verification gaps

- **HEAD aliases bypass the refusal** (observation; this is C2 scope, not a B→REV regression). In a `main` repo with HEAD one commit off-branch:
  - REV `--rev HEAD` → exit 2.
  - `--rev @` and `--rev HEAD^0` → **exit 0 clean**, grading the off-branch commit (`REV_RESOLVED` ≠ main).

  The docstring scopes the check to a "literal `--rev HEAD`", but the SKILL jj table's "silent without this check" applies to these spellings too.
- **`--require-mid-maps` is not used in verification.** `.ufo/waves/round-18/verify.py:201` validates round-18 receipts without the flag. Yet `SKILL.md:541` names that form as the round-18 one, and `decision-rule.json:2` makes it the binding gate. The current receipts pass both modes, so there is no harm today.
- **Row kind mismatch.** The `custody-pair` row kind is `tool` (`SKILL.md:449`), but `PROTOCOL.md:401-402` (fleet, working tree) allows only `gate|probe`. REV applied that rule to `pins` (`SKILL.md:542`) but not here. This predates REV.
- **Line anchors moved by in-place edits.** 644 unqualified `path:line` tokens that predate REV now resolve to different bytes at REV. They are mostly in retained seat reports. On admitted surfaces:
  - `corpus/lessons/round-17-verifier-spotcheck.md:108,137` cites `carrier-run.py:481-486`. Its header scopes that to revision A, so it is not false.
  - Others are README coverage-map ranges and the rewritten `SKILL.md:448`/`:540-542` rows.
- **Lane-relative path that lives in the fleet repo.** `custody-pair.py:103` cites `.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` as if lane-relative. That file is not in the lane tree; it is tracked only in the fleet repo.
- **Not executed:** r17 `verify.py main()` (F1 consequence is code inference), the REA side of the round-18 runs, and jj-specific states (by contract).

## Commands and exit codes

`L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; `B`/`R` = the hashes above.

1. **Sandbox setup** — exit 0:

   ```
   git clone -q --no-hardlinks $L $T/lane && git -C $T/lane remote remove origin && git -C $T/lane worktree add -q --detach $T/base $B && git -C $T/lane checkout -q --detach $R
   ```
2. `git -C $L diff --name-status $B $R | grep -v '^A\t.ufo/waves/round-18/'` → exit 0 (15 M, 2 A).
3. Probe, strict, explicit rev:
   - B tool on the B tree: exit 0, clean.
   - REV tool on the REV tree: exit 0, clean.
4. Selftests at B and REV: `citation-drift-probe --selftest`; `custody-pair selftest`; r17 `compare`, `log-extract`, `receipt-validate` and `carrier-run` `--selftest`. All exit 0.
5. `python3 -I -B $T/harness.py` → exit 0. It runs B and REV tools on the retained r17/r18 inputs.
6. Controls and proxies, all exit 0:
   - `round-17/controls.py $B $R`
   - `round-18/controls.py $B $R`
   - `round-17/measure.py $B` and `$R`
   - `temporal-sweep.py --root $T/lane --rev <B|R> --sites-rev $B`
7. `invocation-audit.py --root $L --rev <B|R>` → exit 0 at both (F3).
8. `python3 -I -B $T/citedrift.py admitted` and `all` → exit 0: 8 and 644 drifted referents respectively.
9. F1 import → exit 0. F2: B copy exit 0/0; REV copy exit 1/1; deep REV copy exit 0, misrooted. F5 minimal repro: B exit 0, REV exit 2. Aliases `@` and `HEAD^0` → exit 0.
10. Round-18 receipts: `receipt-validate.py [--require-mid-maps] runs/*/receipt.json` → 15/15 exit 0 in both modes.
11. `routed-defects.py --root $T/lane --rev $R`, with the eb6c266 copy and the REV copy → exit 0 for both; `open_count` 1 vs 0.
12. Custody cross-version `verify`, both orders, both tools → exit 0, MATCH.

## Installs

None.
