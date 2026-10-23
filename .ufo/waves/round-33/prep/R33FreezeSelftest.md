# R33FreezeSelftest — `--selftest` for freeze-integrity in isolated fixture repos

- **Seat:** `KaidokuR33.R33FreezeSelftest` (UFO-FSD executor)
- **Base:** `428315a8f5674b952def862910af6e07a6c2224b` (lane HEAD, unchanged before/after)
- **Contract:** `.ufo/waves/round-33/prep-contract.txt`
- **Scope:** own scratch copy only; original `tools/round-32/freeze-integrity.py` untouched; no lane git writes; no installs or updates
- **Execution UTC:** selftest 2026-10-23T08:11:00Z–08:11:00Z; no-arg invocation check 08:11:20Z; final artifact pins 08:11:30Z

## 1. What changed

Own scratch copy `<scratch>/freeze-integrity.py` (sha256 `2afc7f8e…b6d4fda`, 11,732 bytes) adds a `--selftest` path. Original at lane: sha256 `6b5aa1df…041804cd`, 2,979 bytes, unmodified (`git status --porcelain -- tools/round-32/freeze-integrity.py` empty).

- New placed before `main()`: `SELFTEST_BASE`, fixture helpers (`_fixture`, `_write`, `_claims`, `_sha`, `_selftest_commit`, `_run_gate`, `_check`), five case functions, `selftest()`.
- `main()` delta: `--root`/`--round` are no longer argparse-`required`; new `--selftest` flag; first statements are
  `if a.selftest: return selftest()` then `if not a.root or not a.round: ap.error(...)`. The gate body from `claims = …` through the CLEAN/FAIL prints and return codes is byte-identical to the original.
- Case runner re-execs this same file as `sys.executable -I -B <abs script> --root <fixture> --round 99`, so the original `--root/--round` invocation and predicate are what each case actually exercises. `--selftest` itself needs neither flag.

Containment/bounds:

- Fixtures created with `tempfile.mkdtemp(dir=SELFTEST_BASE)` where `SELFTEST_BASE = /fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest`; each fixture is `git init -q`-ed there and removed in `finally: shutil.rmtree(...)`.
- Fixture git calls inherit `git()`'s `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` stripping; child run env sets `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`. Commits use `-c user.name/-c user.email`, `commit.gpgsign=false`, `core.hooksPath=/nonexistent-…`, `--no-gpg-sign`.
- Each fixture payload is bytes-level (<1 KiB total); child gate bounded by `communicate(timeout=120)` in `_run_gate`; on timeout the child is killed with `os.killpg(..., SIGKILL)` (`start_new_session=True`). Whole run bounded by `timeout 600` at the shell.
- No git commands target the lane; fixture repos are standalone under the scratch base. Post-run `find` shows only the five retained artifacts, no fixture dirs.

## 2. Case contract vs observed

| Case | Fixture | Expected | Observed |
|---|---|---|---|
| `clean` | freeze commit adds claims pinning `bin/tool.py` + `data/pins.json`; unrelated commit after freeze | exit 0, `CLEAN pins=2`, both pins `ok … commits_after_freeze=0` | PASS, freeze `e7989d053f22`, exit 0 |
| `tampered_pin` | pinned file rewritten and committed after freeze | exit 1, `FAIL … changed=1`, digest of tampered bytes | PASS, exit 1, `sha=2412b990a7d3`, changed=1 |
| `restored_after_change` | tamper commit then original bytes restored in a second commit | exit 1, digest matches pin but `commits_after_freeze` non-zero | PASS, exit 1, `commits_after_freeze=3c3aa5f,875ddb6` |
| `absent_claims` | repo has a commit, no commit ever adds `…/claims.json` | exit 2, `ERROR no commit adds … at HEAD` | PASS, exit 2 |
| `missing_pinned_file` | claims pin `bin/missing.py`, path never exists | exit 1, `FAIL … sha=absent`, changed=1 | PASS, exit 1, `changed=1` |

## 3. Exact runs, output, exit

Selftest — argv `timeout 600 python3 -I -B freeze-integrity.py --selftest`, cwd `<scratch>`, captured at `<scratch>/selftest-run.log` (sha256 `01a721bf…27fcf13`):

```
argv: timeout 600 python3 -I -B freeze-integrity.py --selftest
start_utc: 2026-10-23T08:11:00Z
case clean: PASS freeze=e7989d053f22 pins=2 exit=0
case tampered_pin: PASS exit=1 changed=1 sha=2412b990a7d3
case restored_after_change: PASS exit=1 digest_matches history_flagged commits_after_freeze=3c3aa5f,875ddb6
case absent_claims: PASS exit=2 claims=.ufo/waves/round-99/claims.json absent
case missing_pinned_file: PASS exit=1 sha=absent changed=1
freeze-integrity-selftest: PASS cases=5 elapsed_s=0.22 base=/fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest
end_utc: 2026-10-23T08:11:00Z
exit: 0
```

Invocation guard (original mode still demands flags) — argv `timeout 30 python3 -I -B freeze-integrity.py`, captured at `<scratch>/invocation-check.log`:

```
argv: timeout 30 python3 -I -B freeze-integrity.py
start_utc: 2026-10-23T08:11:20Z
exit: 2
stderr:
usage: freeze-integrity.py [-h] [--root ROOT] [--round ROUND]
                           [--claims CLAIMS] [--rev REV] [--selftest]
freeze-integrity.py: error: --root and --round are required unless --selftest is given
```

Scratch base `<scratch>` = `/fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest`. Retained artifacts:

| Artifact | Bytes | sha256 |
|---|---|---|
| `freeze-integrity.py` | 11,732 | `2afc7f8ee751cb497bbec57f601c41ff4080182ec633d7280da143a06b6d4fda` |
| `selftest-run.log` | 597 | `01a721bf5f85bf8f0dfd7b949ebb167caae6febe8a0ff4c2c65cb1a16d7fcf13` |
| `invocation-check.log` | 318 | `15028e88df60727689aa789a32ed390ed69a890058f01a10863090a19b7d88f8` |
| `invocation-check.err` | 219 | `8eb2565f74aed5754cec167581ca4bc8fb8374354513a081efb142c31f3a0888` |
| `selftest.diff` (original vs copy, unified) | 10,277 | `24bc8c95d343c5ad612af942ee9b6f10b90f8dc36dc1518f2bfb2188f78ed28a` |

## 4. Evidence the predicate is unchanged

`diff -u tools/round-32/freeze-integrity.py <scratch>/freeze-integrity.py` (`selftest.diff`, 254 lines) contains: docstring addition, 4 imports + constants, ~196 added selftest lines before `main()`, and in `main()` only:

- `--root`/`--round` lose `required=True`;
- add `--selftest`;
- add `if a.selftest: return selftest()` and the missing-flags `ap.error`.

No hunk touches the git-log/show calls, pin merge, digest comparison, `touched` predicate, per-pin print format, or CLEAN/FAIL summary strings. Case outputs confirm both sides of the predicate are live: tamper fails on digest, restore fails on history alone.

## 5. Risks / limitations

- `SELFTEST_BASE` is intentionally hardcoded to the assigned scratch path, so this copy's `--selftest` refuses to use fixtures elsewhere by construction. Porting it to the lane would need the constant adjusted or the scratch path retained.
- Selftest asserts exit codes plus specific predicate/summary substrings, not the full per-case stdout; unrelated line-format changes would surface as case failures.
- Fixture history is synthetic and linear; no merge commits, renames, submodules, SHA-256 repos, or `--claims`/`--rev` overrides are covered. The restored case covers only content restore, not revert/merge topology.
- Host dependency: git 2.56.0 and Python 3.14.8 were used; isolated global/system git config was suppressed for fixture runs, but the fixture build assumes a POSIX filesystem under `/fast`.
- This seat did not edit the original tool, did not wire `--selftest` into any caller/CI, and ran no builds/lints/formatters.

## 6. Verification for main agent (not run by this seat)

- Optional: `cd /fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest && timeout 600 python3 -I -B freeze-integrity.py --selftest` → exit 0, 5 PASS (measured 0.22 s).
- Confirm `tools/round-32/freeze-integrity.py` still matches `6b5aa1df…041804cd`.
- If the selftest is ported to the lane tool, re-run the original `--root <LANE> --round 32` invocation to confirm identical output.

Trailer: `.ufo/waves/round-33/prep/R33FreezeSelftest.md`
