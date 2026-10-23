# R33TimestampRepair — round-32 planned-deadline allowlist and able-to-fail control

- **Seat:** `KaidokuR33.R33TimestampRepair` (UFO-FSD executor, leaf)
- **Base:** `428315a8f5674b952def862910af6e07a6c2224b` (round-32 verifier spot-check)
- **Measured (UTC):** 2026-10-23T08:09:39Z first baseline scan; gates 08:13:18–08:13:19Z; fixture controls 08:13:18–08:13:19Z; tool selftest 08:13:29Z; base-red and hash-bound repaired gates 08:19:08–08:19:10Z; hash-bound selftest (incl. clones) 08:19:08–08:19:09Z; final historical-fixture selftest rerun 08:23:28Z; isolated origin selftest 08:28:44Z; installed-copy selftest 08:29:27Z and installed-copy gate 08:29:32Z; report updated 08:29Z
- **Scope:** read-only lane production; no git/jj writes in the checkout; scratch git only under `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/`; no original edits
- **Inputs:** `.ufo/waves/round-33/prep-contract.txt`; `.ufo/waves/round-20/tools/evidence-timestamps.py`; red receipt `.ufo/waves/round-32/a2after/timestamps-strict-at-9ef97f08.txt`; `corpus/lessons/round-32-verifier-spotcheck.md:110-117`
- **Environment:** python 3.14.8, git 2.56.0. No installs or upgrades were needed.

## 1. Retained red receipt and `--allow` API

The prior receipt (committed at `547d6f2c`, committer time 2026-10-23T07:41:55Z) records a strict run at `9ef97f08` over `.ufo/waves/round-32` with `--allow []`: 168 files scanned, 4 findings, exit 1. The four findings are `a2audit-gate.json:14`, `a2audit-settle.json:3`, `a2residual-dispatch.json:17`, `a2residual-settle.json:3`.

`--allow` semantics, read from the tool source and confirmed by the fixture below:

- `--allow FILE:LINE`, repeatable; `FILE` is relative to the `--path` root (the tool strips the scope prefix when it builds the finding key), `LINE` is the 1-based final blob line at `--rev`.
- The key is `(display path, line)`. One entry exempts **every** flagged timestamp occurrence on that line; fields within a line cannot be separated.
- Output `allow[].applied` is `true` only if at least one future-dated finding matched that exact key; a stale or wrong-line entry reports `applied: false`.
- `--strict` exits 1 iff `summary.unexempted_finding_count > 0`. Reads are revision-scoped (`git ls-tree`/`cat-file`/`blame --porcelain`); the worktree is never read. Both runs below report `files_skipped: 0` (no binary blobs).

## 2. Exact four-line allowance (planned deadlines only)

Registered in `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/allowances.json` (sha256 `c54e9e10059388968c7251c4f9d472f53103f5dc2626e428875e2cb178391986`). Each row is a planning cutoff written before the instant it schedules; none is an observed run instant.

| # | `FILE:LINE` (relative to `.ufo/waves/round-32`) | field | value | introducing commit | committer time | reason |
|---|---|---|---|---|---|---|
| 1 | `a2audit-gate.json:14` | `settle_deadline` | `2026-10-23T07:35:00Z` | `33393e594f1e278777fa49020b42c66ac4fa352e` | 06:56:11Z | Dispatch-plan settle cutoff written 38m49s before the cutoff it schedules; the settle recorder consumes it as the wave deadline. |
| 2 | `a2audit-settle.json:3` | `settle_deadline` | `2026-10-23T07:35:00Z` | `bbdd793d55807cfea9193ef5aaf0ae86a5c25a10` | 07:14:24Z | Settle metadata repeats the dispatch cutoff; `observed_cutoff_utc` is 07:12:53 and every seat transcript time is ≤07:07:22, so it is the planned cutoff bounding the settle window. |
| 3 | `a2residual-dispatch.json:17` | `deadline` | `2026-10-23T07:55:00Z` | `bbdd793d55807cfea9193ef5aaf0ae86a5c25a10` | 07:14:24Z | Residual dispatch specification written 40m36s before the deadline it schedules; the field names the authorization window. |
| 4 | `a2residual-settle.json:3` | `deadline` | `2026-10-23T07:55:00Z` | `9ef97f08b655d951650ba5d32f41f1b1cf9653f4` | 07:30:33Z | Settle metadata repeats the residual dispatch deadline; every seat transcript time is ≤07:26:35, so it is the planned cutoff bounding the residual window. |

**Excluded from the bare four-line list:** `a2after/timestamps-strict-at-9ef97f08.txt:3` is a verbatim copy of the prior run's stdout committed at 07:41:55Z. Its flagged tokens are the two `07:55:00Z` planned-deadline values echoed as finding text. Because `--allow` is line-granular, a bare `--allow` on that line would also exempt any future *actual* run instant pasted into the same receipt line — the exact laundering the original assignment forbids. It therefore stays red under the bare four-line list and is admitted only in §8 under a whole-line SHA256 pin, where any same-line insertion changes the hash and voids every allowance.

## 3. Strict gate at the two revisions

Wrapper: `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/run-round32-gate.sh` (sha256 `76d2239518ff4d819748c47e19b3aa4572adf9e0907386553dcc765bf9f6eafd`), which reads the four `allow` rows from `allowances.json`, unsets `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`, and records start/end/argv/exit. Tool sha256 `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00`, identical to the blob at HEAD (`git status --porcelain` clean for the tool; tool unchanged).

### Run A — lesson-measured revision `9ef97f08` (green)

Retained: `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/receipts-at-9ef97f08/` (`receipt.txt`, `stdout.json` sha256 `c5888db554e93639abe30a692cd781e02a9a95d4aa5535258623200e88bf9375`, 1657 bytes; `stderr.txt` 0 bytes).

```text
utc_start=2026-10-23T08:13:18Z
argv=["env", "-u", "GIT_DIR", "-u", "GIT_WORK_TREE", "-u", "GIT_INDEX_FILE", "python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py", "--root", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "--rev", "9ef97f08b655d951650ba5d32f41f1b1cf9653f4", "--path", ".ufo/waves/round-32", "--strict", "--allow", "a2audit-gate.json:14", "--allow", "a2audit-settle.json:3", "--allow", "a2residual-dispatch.json:17", "--allow", "a2residual-settle.json:3"]
exit=0
utc_end=2026-10-23T08:13:19Z
```

Payload: `files_scanned=168`, `files_skipped=0`, `finding_count=4`, `unexempted_finding_count=0`; all four `allow` entries `applied: true`; all four findings `exempted: true`. This is the gate-green result required by lesson defect 1 at the revision the lesson measured.

### Run B — base `428315a8` (still red, residual named)

Retained: `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/receipts-at-428315a8/` (`receipt.txt`, `stdout.json` sha256 `9c17514b3d9bfa1a06e9aae198cc733fe4b5af2be7058fc6cdb6a21e494404ac`, 2103 bytes; `stderr.txt` 0 bytes).

```text
utc_start=2026-10-23T08:13:19Z
argv=["env", "-u", "GIT_DIR", "-u", "GIT_WORK_TREE", "-u", "GIT_INDEX_FILE", "python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py", "--root", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "--rev", "428315a8", "--path", ".ufo/waves/round-32", "--strict", "--allow", "a2audit-gate.json:14", "--allow", "a2audit-settle.json:3", "--allow", "a2residual-dispatch.json:17", "--allow", "a2residual-settle.json:3"]
exit=1
utc_end=2026-10-23T08:13:19Z
```

Payload: `files_scanned=179`, `files_skipped=0`, `finding_count=6`, `unexempted_finding_count=2`; all four `allow` entries `applied: true`. Findings:

| path | line | timestamp | committer time | exempted |
|---|---|---|---|---|
| `a2after/timestamps-strict-at-9ef97f08.txt` | 3 | `2026-10-23T07:55:00Z` | 2026-10-23T07:41:55Z | false |
| `a2after/timestamps-strict-at-9ef97f08.txt` | 3 | `2026-10-23T07:55:00Z` | 2026-10-23T07:41:55Z | false |
| `a2audit-gate.json` | 14 | `2026-10-23T07:35:00Z` | 2026-10-23T06:56:11Z | true |
| `a2audit-settle.json` | 3 | `2026-10-23T07:35:00Z` | 2026-10-23T07:14:24Z | true |
| `a2residual-dispatch.json` | 17 | `2026-10-23T07:55:00Z` | 2026-10-23T07:14:24Z | true |
| `a2residual-settle.json` | 3 | `2026-10-23T07:55:00Z` | 2026-10-23T07:30:33Z | true |

Isolation of the residual (`--path .ufo/waves/round-32/a2after`, no allowance, non-strict): 12 files, 2 findings, both at `timestamps-strict-at-9ef97f08.txt:3`, retained at `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/residual-a2after.json` (sha256 `cfccd53fa0af8cb80e853a8c2a41cd706bbbfc8e600a28a2badbeb2f482ee58d`). The four-line allowlist covers every planned-deadline field at base; the only unexempted bytes are the receipt's own copy of two of those values.

## 4. Bounded fixture — actual execution instants still fail, planned field passes

Fixture repo `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/fixture/repo`, built by `build-fixture.sh` (sha256 `21a99d8b4cc5e27606a1f76a9530e4dc4b21a48f37ec74b353f4bd411766d759`), commit `8bec7787fae55b42363abd7fb44637c0a2056fba` at 2026-10-23T06:00:00Z, 29,055 bytes total. The existing tool is invoked unchanged by absolute path; controls script `run-fixture-controls.sh` (sha256 `93469a93e4628e229eaaebf8371675c69bcd32b7a528a6a20b2d63b8775641f3`).

- `mixed/receipt.json` — line 2 `utc_start 05:00:00Z` (past), line 3 `utc_end 07:40:00Z` (actual future execution time), line 4 `settle_deadline 07:30:00Z` (planned deadline).
- `planned/planned.json` — line 2 `settle_deadline 07:30:00Z` only.
- `echo/stdout.txt` — verbatim copy of `mixed/receipt.json`, mirroring a committed receipt echo.

All seven cases passed their planted expectations (`FIXTURE_CONTROLS: CLEAN cases=7`, exit 0); per-case argv/output/exit retained under `fixture-runs/<case>/`:

| case | path | `--allow` | exit | findings (line: exempted) | unexempted |
|---|---|---|---|---|---|
| `mixed-no-allow` | mixed | — | 1 | 3:false, 4:false | 2 |
| `mixed-allow-deadline` | mixed | `receipt.json:4` | 1 | 3:false, 4:true | 1 |
| `mixed-allow-actual` | mixed | `receipt.json:3` | 1 | 3:true, 4:false | 1 |
| `planned-no-allow` | planned | — | 1 | 2:false | 1 |
| `planned-allow-deadline` | planned | `planned.json:2` | 0 | 2:true | 0 |
| `planned-wrong-line` | planned | `planned.json:1` | 1 | 2:false; `applied:false` | 1 |
| `echo-allow-deadline` | echo | `stdout.txt:4` | 1 | 3:false, 4:true | 1 |

The two decisive controls: allowing the planned deadline line alone still exits 1 on the future `utc_end` (`mixed-allow-deadline`), and a planned-only line allowed exits 0 (`planned-allow-deadline`). `echo-allow-deadline` reproduces the round-32 receipt case: the copied deadline token is exempted while the copied actual execution instant still fails.

## 5. Tool integrity

- Tool blob at `428315a8:.ufo/waves/round-20/tools/evidence-timestamps.py` sha256 `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00`; worktree copy identical (`git status --porcelain` empty for the path).
- `--selftest`: exit 0, `SELFTEST: CLEAN cases=5` (`future_line_flagged`, `past_line_clean`, `zulu_and_offset_parsed`, `later_commit_line_uses_own_time`, `alternate_and_large_text`); retained at `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/selftest.txt` (sha256 `d6c7c21a8ed600b5c0d98894eeae555c2dfcf4a30be8c925567931332632753d`).

## 6. Reproduction

```sh
# bare four-line gate (historical measurement), at either revision
/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/run-round32-gate.sh <REV> <OUTDIR>
# e.g. 9ef97f08b655d951650ba5d32f41f1b1cf9653f4 -> exit 0
#      428315a8f5674b952def862910af6e07a6c2224b -> exit 1 (receipt-copy residual, 2 occurrences)

# hash-bound permanent repair (five rows, whole-line SHA256 pins; §8)
python3 -I -B run-gate-hashed.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 428315a8 --path .ufo/waves/round-32 --spec allowances-hashed.json --out OUTDIR   # exit 0
python3 -I -B run-gate-hashed.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 428315a8 --path .ufo/waves/round-32 --spec allowances-empty.json --out OUTDIR    # exit 1, original red
python3 -I -B run-gate-hashed.py --selftest                                              # CLEAN cases=3; unique scratch tempdir, 600s cap, cleanup

# planned-vs-actual fixture and its controls, all in scratch
/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/build-fixture.sh
/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/run-fixture-controls.sh   # exit 0, CLEAN cases=7
```

## 7. Risks and limitations

- **Base red is now the control, not the state.** The bare four-line list makes the gate green at `9ef97f08` but not at base `428315a8` (2 receipt-copy occurrences). §8 adds a fifth, whole-line hash-bound row; with it the base gate is green (exit 0, 6/6 exempted) while the empty spec still reproduces the original red (exit 1, 6 unexempted) side by side.
- **Hash pins are deliberately strict.** A pin binds the exact line bytes at `--rev`. Any byte change — a legitimate reflow, an added field, or an inserted execution instant — invalidates **all** allowances until the spec is re-pinned and the selftest is re-run. Default-deny is the intended behavior; do not auto-repin.
- **No registration in tracked config.** The allow rows exist in scratch (`allowances-hashed.json`, JSON self-contained with schema/base/rule/hashes/tokens/reasons) and this report only. Registering the wrapper or spec in a tracked gate invocation is an L1/integrator decision, out of scope for this leaf.
- **Line-granular exemption still applies to the tool.** The hash wrapper protects a pinned line from edits, but within a matched line the tool still exempts every flagged occurrence; future evidence should keep actual execution instants and planned deadlines on separate lines as the §4 fixture shows.
- **Scope and bounds.** Only `.ufo/waves/round-32` was scanned; no claim, score, build, formatter, or REA run. Scratch outputs are bounded (largest payload 2,178 bytes; hashed fixture tree 438,704 bytes, all clones under `/fast/scratch`), each process capped with `timeout`, none left running.

## 8. L1-directed permanent repair — whole-line hash-bound allowances (side by side)

The bare four-line list cannot admit the receipt echo without laundering same-line execution instants. The repair keeps the line-granular tool unchanged and binds each allowance to the SHA256 of the **entire source line** at the gated revision, so the echo is admissible only while its bytes are identical to base.

- **Spec (tracked-ready):** `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/allowances-hashed.json` (sha256 `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332`), schema `r33-hashed-allow-gate-v1`, scope `.ufo/waves/round-32`, base `428315a8f5674b952def862910af6e07a6c2224b`, rule "sha256 of the entire source line bytes at --rev, LF delimiter excluded (Git object bytes)". Five rows, each carrying `tokens` and a `token_rule` naming the deadline-only token(s).
- **Wrapper:** `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/run-gate-hashed.py` (sha256 `e011ed69e72bed408de30211712b2e65d69fd01b9c002a45eb7ce5acf6055bb0`). For every row it reads `<rev>:<scope>/<file>` as a Git object, splits on LF, and hashes the exact line. Only if **all** rows match does it forward the five `--allow` arguments to the unchanged tool. On mismatch, missing path, or missing line it exits 1 with stable JSON `{"error":{"code":"allowance_line_changed",…}}`, records `tool_run:false`, and forwards no allowance at all (the gate is not invoked).
- **Source gate untouched:** the tool remains sha256 `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00`; no lane file was edited.

Pinned line hashes (all verified against base Git objects):

| `FILE:LINE` | line sha256 | deadline-only tokens |
|---|---|---|
| `a2audit-gate.json:14` | `8c727cad3617fa4ab79a61febdbf6b0ddd8b15880bb54e0889c8585ae3d9ec4b` | `07:35:00Z` |
| `a2audit-settle.json:3` | `8c727cad3617fa4ab79a61febdbf6b0ddd8b15880bb54e0889c8585ae3d9ec4b` | `07:35:00Z` |
| `a2residual-dispatch.json:17` | `1213815d435402b8ddde10e67f0faca71a9e798b5607caa5cb1b31944c47729b` | `07:55:00Z` |
| `a2residual-settle.json:3` | `3d42105e95a6420edce5857477487c29f4883ad2e29269cde31ddfd3f986cd77` | `07:55:00Z` |
| `a2after/timestamps-strict-at-9ef97f08.txt:3` | `3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03` | `07:55:00Z` ×2 (echoed finding timestamps) |

**Side by side at base `428315a8`** (same tool, same scope, strict):

| measurement | spec | exit | findings | unexempted | retained stdout |
|---|---|---|---|---|---|
| original base-red | `allowances-empty.json` (`allow: []`) | 1 | 6 | 6 | `receipts-hashed-base-red/stdout.json`, sha256 `de2e83f02f83da1150f23b114ab3a030c82a93a1cf5e7808b56aedee25999fff` |
| bare four-line (historical, §3) | `allowances.json` (4 rows, no hashes) | 1 | 6 | 2 | `receipts-at-428315a8/stdout.json` |
| **repaired** | `allowances-hashed.json` (5 rows, hash-verified) | **0** | 6 | **0** | `receipts-hashed-repaired/stdout.json`, sha256 `afef2d70317e65a2f914896d29264fd9922efc3b2600db3648919386b40bd070` |

Repaired run receipt: `utc_start=2026-10-23T08:19:09Z`, `exit=0`, `utc_end=2026-10-23T08:19:10Z`, `resolved_rev=428315a8f5674b952def862910af6e07a6c2224b`, 2,178 stdout bytes; all five allowances `applied:true`, all six findings `exempted:true`. Exact forwarded argv (from `receipts-hashed-repaired/receipt.txt`):

```text
["env","-u","GIT_DIR","-u","GIT_WORK_TREE","-u","GIT_INDEX_FILE","python3","-I","-B","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py","--root","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","--rev","428315a8f5674b952def862910af6e07a6c2224b","--path",".ufo/waves/round-32","--strict","--allow","a2audit-gate.json:14","--allow","a2audit-settle.json:3","--allow","a2residual-dispatch.json:17","--allow","a2residual-settle.json:3","--allow","a2after/timestamps-strict-at-9ef97f08.txt:3"]
```

The empty-spec control at `utc_start=2026-10-23T08:19:08Z`, `exit=1`, `utc_end=2026-10-23T08:19:09Z`, forwards no allowance and reproduces the original red (the 08:09:39Z raw baseline had the same 6 findings).

**Hash-bound selftest and relocatable shipping copy** (own bounded clones only; final installed-copy run 2026-10-23T08:29:27Z, retained `installed-copy-selftest.txt`, sha256 `34bcd305521efada862f08c2d0ee23a9397290ed0c74074d119fe69bb195ffcc`). `--selftest` creates a unique `tempfile.mkdtemp(prefix="selftest-", dir=/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair)`, copies exactly the four shipping files there, runs the runner under `timeout 600` (each case also capped at `timeout 120`), replays its output, and removes the directory in a `finally`; missing assets return `selftest_assets_missing` and an unavailable scratch root returns `selftest_scratch_unavailable` (both exit 2). `build-hashed-fixture.sh` and the runner resolve `BASE=${HASHED_FIXTURE_BASE:-$HERE/hashed-fixture}`, so all Git fixture writes stay inside the unique copied directory and nothing is written beside the installed tools. Builder sha256 `37206762bb48cbdd7b7758b46eda3e8129728077a32c9d71bc98d96088465152`, runner sha256 `d60840374bc75a4bc67d526248786405b00a4b6456dbfcbe7d38ccd03785770e`, allow JSON sha256 `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332` (unchanged). The builder copies the five exact base blobs into four source commits with base blame times `2026-10-23T06:56:11Z / 07:14:24Z / 07:30:33Z / 07:41:55Z` (the parent base's own timeline), then clones and adds two derived control commits dated `2000-01-01T00:00:00Z` whose injected instants are `2001-02-03T04:05:06Z` — historic wall-clock, future only relative to their synthetic 2000 introducing commits. The wrapper predicate and the original gate are unchanged.

| clone (HEAD) | case | exit | observed |
|---|---|---|---|
| `clone-green` `13493f8c29f4f6f8057160725694896f12b0158b` | known-line echo unchanged | 0 | 6 findings, 0 unexempted, 5/5 applied |
| `clone-sameline` `3adfeda72bf27123394024090cfd733ad7f69108` | `{"utc_end":"2001-02-03T04:05:06Z",…}` inserted into the allowed echo line; control commit dated 2000 | 1 | `allowance_line_changed`, `tool_run:false`, no allowance forwarded |
| `clone-unlisted` `45d2b034d9f5db21233814deb6be6cb17d9aebee` | extra `a2extra/unlisted.json` with unlisted `2001-02-03T04:05:06Z`; control commit dated 2000 | 1 | 7 findings, 1 unexempted at `a2extra/unlisted.json:1`; 5/5 applied |

Counterfactual proving the hash binding is what prevents laundering: invoking the unchanged tool directly on `clone-sameline` with the same five raw `--allow` arguments exits 0 and exempts the inserted `2001-02-03T04:05:06Z` execution instant (13 findings, all exempted; the 2000 control commit also makes that line's 2026 echo tokens future, and the same line allowance exempts them too — precisely why the hash pin is required). Retained at `hashed-selftest-runs/sameline-raw-five-allows.json`, sha256 `7344533abd051405d0c37c65365ad3586893c7a71e05df2a8343b5cbccdb595f`. The wrapper refuses the whole spec instead, leaving the inserted instant unexempted by construction.

**Installed-copy verification (shipping prerequisite):** copied exactly the four files to `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/installed-copy-test/` and ran `installed-copy-test/run-gate-hashed.py --selftest` → exit 0, `HASHED_SELFTEST: CLEAN cases=3` with the same deterministic clone commits (`13493f8c…`, `3adfeda7…`, `45d2b034…`); the copy directory still contained only the four files and zero `selftest-*` tempdirs remained. The installed copy then ran the base gate unchanged: `utc_start=2026-10-23T08:29:32Z`, `exit=0`, `resolved_rev=428315a8f5674b952def862910af6e07a6c2224b`, 6 findings / 0 unexempted / 5-of-5 applied; receipts `installed-copy-gate/` (`receipt.txt` sha256 `53e8f1a1b19e7caaca446108e6bca74d5177d03482be92edab9253fbf7ae64d6`, `stdout.json` sha256 `afef2d70317e65a2f914896d29264fd9922efc3b2600db3648919386b40bd070`, byte-identical to the repaired run's tool output).

**Exact four files to ship** (L1 installs this set; the gate tool itself is read from its original path unchanged):

| file | sha256 | role |
|---|---|---|
| `run-gate-hashed.py` | `e011ed69e72bed408de30211712b2e65d69fd01b9c002a45eb7ce5acf6055bb0` | hash-verifying wrapper; isolated `--selftest` |
| `allowances-hashed.json` | `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332` | five pinned allowance rows |
| `build-hashed-fixture.sh` | `37206762bb48cbdd7b7758b46eda3e8129728077a32c9d71bc98d96088465152` | fixture builder (BASE env/HERE-relative) |
| `run-hashed-selftest.sh` | `d60840374bc75a4bc67d526248786405b00a4b6456dbfcbe7d38ccd03785770e` | three-case selftest runner |

`allowances-empty.json` is not part of the shipping set; it is the scratch-only empty spec used to reproduce the base-red side-by-side, and the raw tool without `--allow` produces the same red.

 the four source commits replicate the parent base's blame times so the copied pinned lines reproduce base findings; the two derived control commits are dated `2000-01-01T00:00:00Z` and their injected instants are `2001-02-03T04:05:06Z`. No literal in the shipping fixture or this report is future at first-add. An earlier draft fixture injected same-day future control instants and produced draft receipts; that draft is **excluded from shipping**, retained only under `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/excluded-futureliteral-20261023/` with an `EXCLUDED-not-admission.txt`, and no receipt from it is cited here. Only the final historical-fixture run receipts are admission evidence. The fixture tree is 438,704 bytes (< 1 MiB), all clones under `/fast/scratch`, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset for every build and gate call.

**Limit:** a pin binds the whole line, so any legitimate edit — including reflow — invalidates every allowance until re-pinned and re-selftested. That is intended default-deny; the spec is tracked-ready but deliberately not registered here.

**Files changed by this seat:** only `.ufo/waves/round-33/prep/R33TimestampRepair.md` (this report). Scratch artifacts are under `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/`; no tracked file, tool, claim, or round-32 evidence was modified.

Trailer: `.ufo/waves/round-33/prep/R33TimestampRepair.md`
