# WTimestampRun — installed hash-bound timestamp wrapper over the committed round-32 scope

- **Seat:** `KaidokuR33.WTimestampRun` (UFO-FSD fleet executor, leaf; no subagents, no background jobs)
- **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only production; this report is the only lane write)
- **Pinned admissible revision:** `d7076120e4f00c6d18aa77b8764d14861e820eb2` (resolved via `git rev-parse`)
- **Spec base:** `428315a8f5674b952def862910af6e07a6c2224b`
- **Measured (UTC):** `2026-10-23T09:31:43Z`–`2026-10-23T09:32:00Z` (scheduling clock; no future-dated evidence)
- **Scratch (all receipts):** `/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampRun/` (20,322 B in 12 files at close; every file < 1 MiB)
- **Environment:** Python 3.14.8, git 2.56.0, GNU bash 5.3.20. No installs or upgrades were needed or performed.
- **Framing:** this is **repair evidence only**. `R33-C1` remains **STOPPED / unprovable** per `.ufo/waves/round-33/claim-stop.json`; nothing here is a 32-row measurement, an admission benchmark, or a revived carrier claim.

## 1. Artifacts under test (installed at `d7076120`)

Worktree bytes were checked against the Git blobs at the pinned revision before either run; all are identical (`verify/provenance.json`).

| path | blob oid at `d7076120` | sha256 (blob == worktree) |
|---|---|---|
| `tools/round-33/timestamps/run-gate-hashed.py` | `85f3d5e3a7e38fcccca8e82b18119f5df06b9cfe` | `e011ed69e72bed408de30211712b2e65d69fd01b9c002a45eb7ce5acf6055bb0` |
| `tools/round-33/timestamps/allowances-hashed.json` | `59257121d6dd667ae620f4ac3d8ba087af9fa58d` | `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332` |
| `tools/round-33/timestamps/build-hashed-fixture.sh` | `ab3b418173f9865120a23c5500301e452300624b` | `37206762bb48cbdd7b7758b46eda3e8129728077a32c9d71bc98d96088465152` |
| `tools/round-33/timestamps/run-hashed-selftest.sh` | `c070f3da2946d35e980e5a08a22ddb62fbe23dc6` | `d60840374bc75a4bc67d526248786405b00a4b6456dbfcbe7d38ccd03785770e` |
| `.ufo/waves/round-20/tools/evidence-timestamps.py` (unchanged gate tool) | `be0452eb44294d69d121d04ab571cf0252f2d8c2` | `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00` |

`git status --porcelain` for these paths and for `.ufo/waves/round-32` was empty; `git diff d7076120 -- <pin files>` was empty. The wrapper and gate tool are therefore the tracked, installed bytes, not scratch edits.

## 2. Independent pin pre-check (before running)

Each allowance line was re-hashed straight from Git objects at `d7076120` using the wrapper's rule (split blob on LF, hash line bytes, LF excluded), independently of the wrapper:

| `FILE:LINE` | pin `line_sha256` | hash at `d7076120` | hash at base `428315a8` | expected token(s) present |
|---|---|---|---|---|
| `a2audit-gate.json:14` | `8c727cad3617fa4ab79a61febdbf6b0ddd8b15880bb54e0889c8585ae3d9ec4b` | match | match | `2026-10-23T07:35:00Z` yes |
| `a2audit-settle.json:3` | `8c727cad3617fa4ab79a61febdbf6b0ddd8b15880bb54e0889c8585ae3d9ec4b` | match | match | `2026-10-23T07:35:00Z` yes |
| `a2residual-dispatch.json:17` | `1213815d435402b8ddde10e67f0faca71a9e798b5607caa5cb1b31944c47729b` | match | match | `2026-10-23T07:55:00Z` yes |
| `a2residual-settle.json:3` | `3d42105e95a6420edce5857477487c29f4883ad2e29269cde31ddfd3f986cd77` | match | match | `2026-10-23T07:55:00Z` yes |
| `a2after/timestamps-strict-at-9ef97f08.txt:3` | `3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03` | match | match | `2026-10-23T07:55:00Z` x2 yes |

Scope invariance: the `.ufo/waves/round-32` tree oid is `09698a00b18362639b03e92b39378cd3041b17aa` at **both** `428315a8` and `d7076120`, and `git diff --stat 428315a8 d7076120 -- .ufo/waves/round-32` is empty. Source-file blob identities at `d7076120` (full blob sha256 in `verify/provenance.json`):

| scope file | blob oid | bytes |
|---|---|---|
| `a2audit-gate.json` | `e71514175804f838be6241c90a521f55ef28ea7e` | 619 |
| `a2audit-settle.json` | `91302a8151f79f7de9c85aec4aa910659cd8aa94` | 14,030 |
| `a2residual-dispatch.json` | `47a71e21dcf6597fa754568c5e8441595b836bf1` | 40,560 |
| `a2residual-settle.json` | `37a30ed509746d782c5a03c9001e863072ce5eb5` | 7,642 |
| `a2after/timestamps-strict-at-9ef97f08.txt` | `c79f6ea9a8a2a3e8604a33ba65db0db35d2fa1f4` | 1,868 |

## 3. Gate run — exact five-entry spec over the committed round-32 scope

Outer invocation (verbatim argv, `cwd=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` removed from the child environment, outer wall cap 300 s):

```text
["timeout","300","python3","-I","-B","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/timestamps/run-gate-hashed.py","--root","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","--rev","d7076120e4f00c6d18aa77b8764d14861e820eb2","--path",".ufo/waves/round-32","--spec","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/timestamps/allowances-hashed.json","--out","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampRun/gate/out"]
```

| field | value |
|---|---|
| `utc_start` | `2026-10-23T09:31:43Z` |
| `utc_end` | `2026-10-23T09:31:44Z` |
| `exit` | **0** |
| stdout | 2,178 B, sha256 `9390f34c394b7bb3a43d4d4134c8a788deefbbaaa2f6ba9df172a7aacabd2c67` |
| stderr | 0 B, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Wrapper receipt (`gate/out/receipt.txt`, sha256 `04dc332207dc90cf2e1c5ec6041942726c51f6404f428afefedae8cc693602d4`): `utc_start=2026-10-23T09:31:43Z`, `utc_end=2026-10-23T09:31:44Z`, `exit=0`, `resolved_rev=d7076120e4f00c6d18aa77b8764d14861e820eb2`, `tool_sha256=489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00`, `spec_sha256=0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332`; `verified_lines` records all five pin hashes; `allow_forwarded` lists all five keys. Hash verification passed for every row **before** any allowance was forwarded.

Exact forwarded argv, including every applied flag (verbatim from the receipt):

```text
["env","-u","GIT_DIR","-u","GIT_WORK_TREE","-u","GIT_INDEX_FILE","python3","-I","-B","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py","--root","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","--rev","d7076120e4f00c6d18aa77b8764d14861e820eb2","--path",".ufo/waves/round-32","--strict","--allow","a2audit-gate.json:14","--allow","a2audit-settle.json:3","--allow","a2residual-dispatch.json:17","--allow","a2residual-settle.json:3","--allow","a2after/timestamps-strict-at-9ef97f08.txt:3"]
```

Payload: `files_scanned=179`, `files_skipped=0`, `finding_count=6`, `unexempted_finding_count=0`. All five allowance entries report `applied:true`:

| `file:line` | applied | flagged timestamp | exempted |
|---|---|---|---|
| `a2audit-gate.json:14` | true | `2026-10-23T07:35:00Z` | true |
| `a2audit-settle.json:3` | true | `2026-10-23T07:35:00Z` | true |
| `a2residual-dispatch.json:17` | true | `2026-10-23T07:55:00Z` | true |
| `a2residual-settle.json:3` | true | `2026-10-23T07:55:00Z` | true |
| `a2after/timestamps-strict-at-9ef97f08.txt:3` | true | `2026-10-23T07:55:00Z` (x2 occurrences) | true |

Cross-check against the committed prep receipt (`.ufo/waves/round-33/repairs/timestamps/receipts-hashed-repaired/stdout.json`, sha256 `afef2d70317e65a2f914896d29264fd9922efc3b2600db3648919386b40bd070`, base `428315a8`): the only differing top-level key is `revision` (base vs pinned rev); `findings`, `summary` and `allow` are equal after JSON parse (`verify/prep-crosscheck.json`). The gate result is stable across the unchanged scope.

## 4. Isolated `--selftest` — run exactly once

Outer invocation (`cwd` lane, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`HASHED_FIXTURE_BASE` removed; outer wall cap 660 s around the wrapper's own 600 s cap and the runner's 120 s per-case caps):

```text
["timeout","660","python3","-I","-B","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/timestamps/run-gate-hashed.py","--selftest"]
```

| field | value |
|---|---|
| `utc_start` / `utc_end` | `2026-10-23T09:32:00Z` / `2026-10-23T09:32:00Z` |
| `exit` | **0** |
| stdout | 443 B, sha256 `34bcd305521efada862f08c2d0ee23a9397290ed0c74074d119fe69bb195ffcc` |
| stderr | 0 B |

Full stdout (`selftest/outer.stdout.txt`):

```text
green 13493f8c29f4f6f8057160725694896f12b0158b
sameline 3adfeda72bf27123394024090cfd733ad7f69108
unlisted 45d2b034d9f5db21233814deb6be6cb17d9aebee
green exit=0 findings=6 unexempted=0 applied=[True, True, True, True, True]
PASS green
sameline exit=1 code=allowance_line_changed tool_run=False actual=cccf4e79322bd4e8
PASS sameline
unlisted exit=1 findings=7 unexempted=1 path=a2extra/unlisted.json
PASS unlisted
HASHED_SELFTEST: CLEAN cases=3
```

Observed behavior from that single run: the unchanged known-line clone is green with 5/5 allowances applied; the same-line inserted future `utc_end` is refused with `allowance_line_changed`, `tool_run:false` (no gate run, no allowance forwarded); the unlisted synthetic future timestamp stays red at `a2extra/unlisted.json:1` while 5/5 listed allowances still apply.

Isolation/cleanup: the wrapper created its unique `selftest-*` tempdir under the hardcoded `SCRATCH_ROOT` (`/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair`), copied exactly the four shipping assets there, and removed it in a `finally`. Shallow scratch listing before and after: 28 entries to 28 entries; **no `selftest-*` directory remains** (the only `selftest-` name is the pre-existing regular file `selftest-origin-isolated.txt` from the prep seat). The stdout sha256 is identical to the prep seat's committed installed-copy selftest receipt (`34bcd305…`), i.e. the installed selftest reproduces deterministically.

## 5. Retained evidence map (own scratch)

All paths relative to `/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampRun/`:

| file | bytes | sha256 |
|---|---|---|
| `gate/outer.meta.json` (outer argv/UTC/exit/hashes) | 1,565 | `4c0e90db38a44fa14ae844ba7efdc6ca5d2bbe6b403c5f995e1a317f568846d8` |
| `gate/outer.stdout.json` (wrapper stdout relay) | 2,178 | `9390f34c394b7bb3a43d4d4134c8a788deefbbaaa2f6ba9df172a7aacabd2c67` |
| `gate/outer.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `gate/out/stdout.json` (gate payload) | 2,178 | `9390f34c394b7bb3a43d4d4134c8a788deefbbaaa2f6ba9df172a7aacabd2c67` |
| `gate/out/stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `gate/out/receipt.txt` (forwarded argv, verified lines, applied flags) | 2,115 | `04dc332207dc90cf2e1c5ec6041942726c51f6404f428afefedae8cc693602d4` |
| `selftest/outer.meta.json` | 1,095 | `36d22aa51c15846cd1f1b703a351ee1358c03a64ed496683359adb24f31cea9d` |
| `selftest/outer.stdout.txt` | 443 | `34bcd305521efada862f08c2d0ee23a9397290ed0c74074d119fe69bb195ffcc` |
| `selftest/outer.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `verify/pinned-lines.json` (independent line hashes at rev and base, tokens, line text) | 5,385 | `7c8d1c0bec0a0cea873433804bd305abe44637de0da258d4553447700b1c759c` |
| `verify/provenance.json` (blob oids, worktree equality, scope tree identity) | 4,777 | `85298c8c9adbc97377fc5c5a8b0b14fe9375ac21c952bf87086bdb450cef1a17` |
| `verify/prep-crosscheck.json` (base-receipt diff) | 586 | `a8227fd826b0d7707ef4859f9d17169d10f80438359b109aceff0dbc73afb0ff` |

## 6. Interpretation

- The installed wrapper at `d7076120` verifies all five whole-line pins against Git objects at the pinned revision and forwards the five `--allow` flags only after every pin matches; the strict gate over `.ufo/waves/round-32` then exits 0 with `unexempted_finding_count=0`.
- The binding is what carries the exemption: the installed selftest's `sameline` case (inserted future `utc_end` on an allowed line) makes the wrapper exit 1 with `allowance_line_changed` and `tool_run:false`, so no allowance is forwarded and the inserted instant cannot inherit the exemption. The `unlisted` case still fails on a new future timestamp.
- The committed round-32 scope is byte-identical at base `428315a8` and pinned revision `d7076120` (same tree oid), so this gate run measures the same evidence set the spec's `base` names; the only payload difference from the committed base receipt is the `revision` echo.

## 7. Risks and limits

- `--selftest` uses the wrapper's hardcoded `SCRATCH_ROOT` (`/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair`, the prep seat's directory) for its unique tempdir. This is installed behavior; patching it would change the wrapper hash under test. The tempdir is created with `mkdtemp`, used only for local git clones, and removed; no persistent write landed there (28→28 entries, no `selftest-*` dirs).
- Pins bind whole lines: any legitimate edit (even reflow) voids **all** allowances until re-pinned and re-selftested. That default-deny is intended.
- The underlying tool is line-granular: one `--allow FILE:LINE` exempts every occurrence on that line. The hash pin is the only protection against same-line insertion; it is exercised by the selftest, not by an additional edit of the lane evidence.
- Scope is only `.ufo/waves/round-32` at the pinned revision; 179 tracked text blobs were scanned, 0 skipped.
- The empty-spec base-red control was **not** re-run by this seat (it is retained at `.ufo/waves/round-33/repairs/timestamps/receipts-hashed-base-red/`, and adverse same-line/bad-pin/unlisted cases are assigned to separate `WTimestamp*` seats). No additional experiment beyond the assigned gate run and single selftest was performed.
- Findings here are lane advice and repair evidence; they are not outside/non-author verification, not an admission benchmark, and not a replacement for the stopped 32-row carrier measurement.

## 8. Containment compliance

- No access to the R33FixtureBuilder quarantine or any of its code, manifests, predictions, fixtures or derivative receipts; the held item was not inspected or retried; no replacement fixture construction was attempted.
- No native carrier execution, no REA/MCP calls, no upstream/domain-source writes, no config/routing edits, no host service changes.
- No lane/fleet git or jj writes (read-only `git cat-file`/`rev-parse`/`diff`/`status` only); sandbox git writes were not needed. Lane `git status` shows only pre-existing/peer untracked wave metadata, none from this run.
- Bounded execution: outer caps 300 s / 660 s, wrapper cap 600 s, runner per-case cap 120 s; no leftover processes (`pgrep -af 'run-gate-hashed|evidence-timestamps|hashed-fixture|run-hashed-selftest'` empty after both runs); scratch footprint 20,322 B in 12 files.

**Files changed by this seat:** only `.ufo/waves/round-33/w1/WTimestampRun.md` (this report). All other artifacts are under `/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampRun/`.

Trailer: `.ufo/waves/round-33/w1/WTimestampRun.md`
