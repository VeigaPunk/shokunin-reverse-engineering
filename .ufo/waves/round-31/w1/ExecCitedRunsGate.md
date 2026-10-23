# ExecCitedRunsGate — cited-runs gate for round-30 routed defect 1

Seat: `KaidokuR31.ExecCitedRunsGate` (executor, leaf).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `c369242fee9f559f895e3f7956b1242076c7b1be`.
Target: round-30 routed defect 1 (`corpus/lessons/round-30-verifier-spotcheck.md:144`):
"the report asserts `settle-gate` PASS at the tip and `prefile: PASS` on a rerun, but neither run is committed. The only committed prefile run is red."

Everything below is read-only work in the lane; the only lane file written is this report.

## What was built

`/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecCitedRunsGate/cited-runs-gate.py`
sha256 `38b94cf811d19a140f05329dc1bb9950c76baa808be83c94212e8f84a6246ee8`, 21,668 bytes, mode 0755, python3 stdlib only (Python 3.14.8 used), git CLI only for reads (`cat-file`, `show`, `rev-parse`).

Usage:

```
cited-runs-gate.py --report <report.md> --lane <LANE> --rev <REV>
cited-runs-gate.py --selftest [--keep-selftest]
```

Semantics (as specified):

- An **assertion line** contains `PASS` (upper case, word-bounded), a positive `CLEAN` (a preceding `NOT` does not count), `exit 0` / `exit=0` / `exit_code=0`, or one or more counter pairs `key=<int>` (`pass=`, `matches=`, `carriers=`, `entry_ok=`, ...). `exit=1` and other non-success values are not assertions.
- Each assertion line must cite at least one lane path under `.ufo/waves/` or `corpus/evidence/` that is a blob at `--rev` and whose committed bytes contain each asserted token. A citation may be full (`corpus/evidence/...`) or relative to the report's round, derived from the report path: `after/x.txt` is tried as `.ufo/waves/<round>/after/x.txt` and `corpus/evidence/<round>/after/x.txt`.
- Findings on stdout: `UNCITED <line>: <excerpt>` (no cited path is a blob at rev) or `UNBACKED <line>: <path> lacks <token>` (a cited path exists, the token does not). Diagnostics and the summary go to stderr.
- Exit 0 when every assertion is backed, 1 on any finding, 2 on usage errors (missing/invalid args, report not a file, lane not a git repo, rev not a commit).

`--selftest` builds a throw-away git repo (`git init`) under the script's directory with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset in every subprocess environment, seeds committed receipts at two commits (one receipt deleted at the tip), then runs the CLI on 17 offline cases: backed PASS, uncited PASS, path absent at rev, same path present at the base rev, token absent (red receipt cited for PASS), red `NOT CLEAN` receipt cited for CLEAN, counter line backed, counter miscount, `exit 0` backed by `exit=0`, `exit 0` against a red receipt, relative shorthand, citation outside the two roots, mixed good/bad lines, no assertion, and three usage errors.

## Acceptance run 1 — selftest

Command (cwd `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecCitedRunsGate`, 2026-10-23T04:12:58Z):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 \
  python3 -I -B cited-runs-gate.py --selftest
```

Exit: **0**. Full stdout:

```
SELFTEST case backed-pass: PASS (exit 0)
SELFTEST case uncited-pass: PASS (exit 1)
SELFTEST case path-absent-at-rev: PASS (exit 1)
SELFTEST case path-present-at-base-rev: PASS (exit 0)
SELFTEST case token-absent: PASS (exit 1)
SELFTEST case red-receipt-clean: PASS (exit 1)
SELFTEST case counter-backed: PASS (exit 0)
SELFTEST case counter-miscount: PASS (exit 1)
SELFTEST case exit0-equals-form: PASS (exit 0)
SELFTEST case exit0-red: PASS (exit 1)
SELFTEST case shorthand-relative: PASS (exit 0)
SELFTEST case outside-prefix: PASS (exit 1)
SELFTEST case mixed-lines: PASS (exit 1)
SELFTEST case no-assertion: PASS (exit 0)
SELFTEST case usage-no-args: PASS (exit 2)
SELFTEST case usage-bad-rev: PASS (exit 2)
SELFTEST case usage-missing-report: PASS (exit 2)
SELFTEST ok cases=17 passed=17
SELFTEST repo=/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecCitedRunsGate/cited-runs-gate-selftest-35792q5o (removed)
```

stderr: empty. Saved at `selftest.out` (sha256 `f58a58696dde3db44419ded37affda363f97a5f03e9e3ed9acd0c0f058c0c77a`), `selftest.err` (sha256 `e3b0c442...b855`, empty).

## Acceptance run 2 — the real round-30 report against the lane

Command (cwd scratch dir, 2026-10-23T04:13:01Z):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 \
  python3 -I -B cited-runs-gate.py \
    --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md \
    --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev c369242fee9f559f895e3f7956b1242076c7b1be
```

Exit: **1**. Full stdout:

```
UNBACKED 16: .ufo/waves/round-30/settle.tsv lacks PASS
UNCITED 59: | R30-C2 | `python3 -I -B tools/round-30/c2-rust-refusals.py --root <LANE> --rev <REV>` | exit 2 (predictions absent)...
UNCITED 64: - `axis-fit-gate` exit 0.
UNCITED 65: - `prefreeze-gate` CLEAN.
UNCITED 66: - `settle-gate` PASS.
UNCITED 67: - `tools/round-29/prefile-check.sh`: `prefile: tree clean`, both freeze ledgers exit 0, `prefile: PASS`, exit 0 (reru...
UNCITED 82: - Round start: `kaidoku ok`, six W04 warnings, exit 0.
UNCITED 83: - Round end: `kaidoku ok`, exit 0, with the W04 warnings unchanged plus a new one: S090 and S083 share the same tarba...
```

Full stderr:

```
note: line 16 asserts 'PASS'; cited .ufo/waves/round-30/settle.tsv lack(s) it at c369242fee9f559f895e3f7956b1242076c7b1be
note: line 59 cites no path that is a blob at c369242fee9f559f895e3f7956b1242076c7b1be; tried .ufo/waves/round-30/tools/round-30/c2-rust-refusals.py, corpus/evidence/round-30/tools/round-30/c2-rust-refusals.py, .ufo/waves/round-30/verb/entry, corpus/evidence/round-30/verb/entry
note: line 67 cites no path that is a blob at c369242fee9f559f895e3f7956b1242076c7b1be; tried .ufo/waves/round-30/tools/round-29/prefile-check.sh, corpus/evidence/round-30/tools/round-29/prefile-check.sh
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

Saved at `round30-run.out` (sha256 `d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5`) and `round30-run.err` (sha256 `1f28ca622430193b3f46d040142c36779d58411c61835d172aa241f230a03d55`).

The two lines the ticket requires the gate to name:

- **settle:** line 16, `.ufo/waves/round-30/settle.tsv` returns `settle: PASS` — the committed TSV contains no `PASS` at all (`git show c369242:...settle.tsv | grep -c PASS` = 0; it is a seat/status/hash ledger, statuses `returned`). Also line 66, `settle-gate` PASS, with no path cited.
- **prefile:** line 67, `prefile: PASS`, exit 0 — the line cites only the commit id `328ca4f4`, not a lane path under the two evidence roots; the only committed prefile output at the rev, `.ufo/waves/round-30/after/prefile-check.txt`, says `prefile: tree NOT CLEAN (3 paths)`, `prefile: FAIL`, `prefile_exit=1`.

Assertion-line census of the report (by the gate's own detector): lines 16, 58, 59, 64, 65, 66, 67, 82, 83 = 9 assertion lines. Line 58 (R30-C1 `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`, exit 0, citing `after/c1-rust-positive-at-tip.txt`) is the single backed one; `assertions=9 findings=8` confirms exactly that split.

## Supplementary controls (same rev, same lane)

1. The backed line alone, copied verbatim from line 58, passes — the gate is not fail-only. Report `reports/round-30/control-cited-line.md`, 2026-10-23T04:13:11Z:

```
$ python3 -I -B cited-runs-gate.py --report reports/round-30/control-cited-line.md --lane .../kaidoku-shokunin --rev c369242...
cited-runs-gate: ok assertions=1 report=reports/round-30/control-cited-line.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
exit=0
```

2. The red receipt is refused for a PASS claim — the exact defect, on the real committed bytes. Report line: `` - `tools/round-29/prefile-check.sh`: `prefile: PASS`, exit 0 (`.ufo/waves/round-30/after/prefile-check.txt`) ``:

```
UNBACKED 1: .ufo/waves/round-30/after/prefile-check.txt lacks PASS
note: line 1 asserts 'PASS'; cited .ufo/waves/round-30/after/prefile-check.txt lack(s) it at c369242...
exit=1
```

(`exit 0` is satisfied here because that receipt's two freeze-ledger lines read `exit=0`; the verdict token `prefile: PASS` is absent. See limitation 1.)

## Findings

- **Observation.** The gate exists, is stdlib-only, and its 17-case offline selftest exits 0 with all cases as expected (backed, uncited, absent-at-rev, base-rev-present, token-absent, red-CLEAN, counter-backed, counter-miscount, exit0-equals, exit0-red, shorthand, outside-prefix, mixed, no-assertion, 3 usage errors).
- **Observation.** On the real round-30 report at `c369242`, the gate exits 1 and names the settle line (16, `UNBACKED ... settle.tsv lacks PASS`; 66 uncited) and the prefile line (67, `UNCITED`). Eight findings over nine assertion lines; line 58 is backed.
- **Observation.** `.ufo/waves/round-30/after/prefile-check.txt` at the rev is red on the tree check (`prefile: FAIL`, `prefile_exit=1`), matching the lesson's "the only committed prefile run is red".
- **Inference.** The remaining six findings (lines 59, 64, 65, 82, 83) are the same defect class outside the two named gates: the C2 table row asserts the tip target line and the `24da3459` red run (`skill_ok=0`, exit 1) while citing only commit ids; the three tip gates are stated without receipts; the census exit-0 lines have no committed receipt. A report rewritten to cite committed receipts would have to add them or stop asserting them.
- **No frozen target line applies.** This item is not R31-C1/C2 and has no line in `claims.json`; it also did not run REA. The negative target ("the gate must fail such a report") is met (exit 1); the positive acceptance (selftest exit 0) is met. The script is not copied into the lane; the L1 owns `tools/round-31/` integration, and the sha256 above is the copy identity.

## Known limitations (disclosed, not hidden)

1. Token presence, not verdict semantics. A receipt that contains `exit=0` on a subordinate line and `FAIL` overall (exactly `after/prefile-check.txt`) backs an `exit 0`-only assertion. The gate refuses the same receipt for `PASS`, so the round-30 prefile claim is still caught; a report claiming only `exit 0` from a red multi-line receipt would pass. This is the specified token rule; tightening it needs a per-tool verdict grammar.
2. `UNCITED` covers both "no citation at all" and "cited path is not a blob at rev"; the reason is on stderr, stdout stays in the specified two-form format.
3. Relative shorthand resolution uses the round name found in the report path (`round-30`); a report placed outside a `round-NN` path must cite full `.ufo/waves/` or `corpus/evidence/` paths.
4. Assertion tokens are matched per token, and different cited files may back different tokens of one line (wording: "at least one lane path ... contain the asserted token").
5. Markdown code fences are not skipped: a quoted receipt inside a fence is treated as an assertion. Stricter than the incident requires; no false positive in the round-30 report.
6. `exit 1` / `FAIL` / `NOT CLEAN` are not assertions, so a report that only claims failures is not gated (it is not making a success claim).
7. The gate reads the lane with `git cat-file`/`git show` only and writes nothing there; it needs `git` on PATH and does not use LSP.

## Files changed

- Lane: `.ufo/waves/round-31/w1/ExecCitedRunsGate.md` (this report) — the only lane write.
- Scratch (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecCitedRunsGate/`):
  - `cited-runs-gate.py` — sha256 `38b94cf811d19a140f05329dc1bb9950c76baa808be83c94212e8f84a6246ee8`
  - `selftest.out` — `f58a58696dde3db44419ded37affda363f97a5f03e9e3ed9acd0c0f058c0c77a`
  - `selftest.err` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)
  - `round30-run.out` — `d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5`
  - `round30-run.err` — `1f28ca622430193b3f46d040142c36779d58411c61835d172aa241f230a03d55`
  - `control-cited-line.out` — `d76c772d1fc33c7bb873dade9006fa3bf4973d3c2b1e928769d309fb91a94df3`
  - `control-cited-line.err` — `e3b0c442...b855` (empty)
  - `control-prefile-red.out` — `71b86282e43632416d06d82d33006cf70559afa8969524d458c7bc2ffacd8d59`
  - `control-prefile-red.err` — `9a3adbf778b5d1983a45a474ee4fc3e0a52c700f95a4e2c7a3ff8c2fdab916ec`
  - `reports/round-30/control-cited-line.md` — `b55212e9df92ae409a0891adaf5b569a4b9834a43425bb0d174a6412b7ae8e3f`
  - `reports/round-30/control-prefile-red.md` — `f9aef82a12873e7f414c4cf29b639c4e1ad65305c2ce70de681558d935198e5f`

No tool installs or updates (nothing needed; python3 and git already present). No REA run. No carrier, mutant, downloads directory, lane index or jj state touched. No processes left running; every command was capped with `timeout`.

## Risks / blockers

- None blocking. Residual: limitation 1 above (token-level `exit 0` backing); the gate targets success claims only; the script must be copied to `tools/round-31/cited-runs-gate.py` by the L1, and a later lane-side run should use a committed report copy, since the fence/token rules assume the report text is committed evidence itself.
