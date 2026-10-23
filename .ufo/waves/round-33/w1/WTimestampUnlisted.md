# WTimestampUnlisted — unlisted historical-text event control

**Verdict: killed (assigned text mutation only).** The unchanged strict detector returned **0 → 1 → 0** for pristine, mutated and restored bytes. All five unchanged deadline allowances reported `applied:true` in every phase. The sole additional, unexempted finding was the newly added synthetic event.

## Scope, axes and provenance

- Seat: `KaidokuR33.WTimestampUnlisted`, leaf mutation tester; no subagents or background jobs.
- Axes: **depth** (unlisted-event discrimination), allowance specificity, exact-byte restoration and containment. These are probe dimensions, not round scores or admission judgments.
- Pinned code/spec revision, resolved through read-only Git: `d7076120e4f00c6d18aa77b8764d14861e820eb2`.
- Observed source base: `428315a8f5674b952def862910af6e07a6c2224b`.
- Scratch root (`S` below): `/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampUnlisted/`.
- Used the existing timestamp selftest's tiny `clone-green` repository at `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair/hashed-fixture/clone-green`, cloned with `--no-hardlinks` into `S/repo`. Each of its five fixture blobs was compared byte-for-byte with the corresponding base Git object and its own worktree bytes before the baseline.
- Materialized the four timestamp shipping assets from the pinned revision into `S/assets`; every asset and the hardcoded original timestamp detector matched the installed lane bytes. The builder and whole-suite runner were retained as provenance but **not executed**. Only this assigned green/unlisted/restored experiment ran.
- Read `claim-stop.json`. **R33-C1 remains STOPPED UNPROVABLE.** This is reachable repair/instrument evidence only, not a replacement carrier study, independent expected manifest, admission benchmark, numeric gain or revived claim.

## Mutant and expected detector

Smallest behavior-bearing change: add the existing text selftest's unlisted-event case to the clean tiny repository, leaving the five old fixture files, their allowed lines, wrapper, detector and allowance spec unchanged:

```diff
--- /dev/null
+++ b/.ufo/waves/round-32/a2extra/unlisted.json
@@ -0,0 +1 @@
+{"utc_end":"2001-02-03T04:05:06Z"}
```

The new file is **35 bytes**, SHA256 `8e46cae87dc7c2451d29b9511722d4c4e1d35bbd39d402d46ece5e4f09f19c7f`. Both author and committer dates on its introducing commit were `2000-01-01T00:00:00Z`. Thus the 2001 event is historical wall-clock text and future **only relative to its synthetic introducing commit**. The original source-line blame times were retained; no current/future execution evidence was fabricated. The restore commit was also dated 2000.

Expected detector: the strict wrapper verifies and forwards the same five hash-bound allowances, then its unchanged underlying timestamp detector exits 1 for `a2extra/unlisted.json:1`; pristine and restored cases exit 0. This deliberately exercises an unlisted line, not the separately assigned same-line or bad-pin controls.

## Actual invocation and outputs

Identical outer detector argv in all three phases (including the output directory; outputs were archived after each run):

```json
["timeout","--kill-after=3s","50s","python3","-I","-B","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampUnlisted/assets/run-gate-hashed.py","--root","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampUnlisted/repo","--rev","HEAD","--path",".ufo/waves/round-32","--spec","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampUnlisted/assets/allowances-hashed.json","--out","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampUnlisted/active-output"]
```

`GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` were removed from every child environment. Global/system Git config was disabled. Inner argv, resolved revisions, verified whole-line hashes and forwarded allowances are retained verbatim in each phase's `receipt.txt`; full outer argv/environment overrides/start/end/stdout/stderr/exit are retained in its `outer-receipt.json` and the command logs.

| Phase | Actual start UTC | Actual end UTC | Exit | Text files / skipped | Findings | Unexempted | Applied flags |
|---|---|---|---:|---:|---:|---:|---|
| Pristine | 2026-10-23T09:33:02.207714Z | 2026-10-23T09:33:02.298059Z | 0 | 5 / 0 | 6 | 0 | `[true,true,true,true,true]` |
| Mutated | 2026-10-23T09:33:11.165592Z | 2026-10-23T09:33:11.257664Z | 1 | 6 / 0 | 7 | 1 | `[true,true,true,true,true]` |
| Restored | 2026-10-23T09:33:11.266632Z | 2026-10-23T09:33:11.369534Z | 0 | 5 / 0 | 6 | 0 | `[true,true,true,true,true]` |

All outer and inner detector stderr files were empty. The mutated output's only unexempted finding was exactly:

```json
{"committer_time":"2000-01-01T00:00:00Z","exempted":false,"finding":"future_dated a2extra/unlisted.json:1","line":1,"path":"a2extra/unlisted.json","timestamp":"2001-02-03T04:05:06Z"}
```

The same five entries were verified, forwarded and applied in each phase:

| Allowance (relative to round-32 scope) | Whole-line SHA256, unchanged |
|---|---|
| `a2audit-gate.json:14` | `8c727cad3617fa4ab79a61febdbf6b0ddd8b15880bb54e0889c8585ae3d9ec4b` |
| `a2audit-settle.json:3` | `8c727cad3617fa4ab79a61febdbf6b0ddd8b15880bb54e0889c8585ae3d9ec4b` |
| `a2residual-dispatch.json:17` | `1213815d435402b8ddde10e67f0faca71a9e798b5607caa5cb1b31944c47729b` |
| `a2residual-settle.json:3` | `3d42105e95a6420edce5857477487c29f4883ad2e29269cde31ddfd3f986cd77` |
| `a2after/timestamps-strict-at-9ef97f08.txt:3` | `3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03` |

The six old deadline occurrences stayed exempted; the extra seventh occurrence did not inherit an exemption.

### Retained stdout hashes

| Phase | SHA256 of exact stdout |
|---|---|
| Pristine | `7926c63a0024d936352353209dd5243a5753b78cf88888fe953faf032f81826a` |
| Mutated | `38eb9107443535dd950674e0f999a45656ecfe8ecbcb40e1766ba7028a3eb879` |
| Restored | `493b24820f9eb31d91f21ca8d9e9cfdbae2d46b43fae956d1bd8b1f0e9982b56` |

Empty stderr SHA256 in every phase: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Pristine/restored stdout differs because it includes the resolved commit; restored fixture bytes and findings are equivalent, not asserted to have byte-identical stdout.

## Exact restoration evidence

The mutation was restored in the driver's `finally` path by a non-destructive `git revert --no-edit` in **this seat's scratch repository only**. That command exited 0 and deleted the one added file. The same bounded detector then ran on the restored bytes. Git history intentionally retains both control commits; exact restoration here means fixture bytes/tree, not an erased Git history.

| State | Measured fixture commit | Git tree hash |
|---|---|---|
| Pristine | `13493f8c29f4f6f8057160725694896f12b0158b` | `8443cd6b998a68ec3e6f54f7530fbb8320c52e37` |
| Mutated | `45d2b034d9f5db21233814deb6be6cb17d9aebee` | `7704bc8f3b9bfdfa6465a2f237c9526eba9c5814` |
| Restored | `493a63e3e6055bc89142b30185591d44c18f4795` | `8443cd6b998a68ec3e6f54f7530fbb8320c52e37` |

All five original worktree files had these same SHA256 values before, during and after mutation:

| File | SHA256 |
|---|---|
| `a2audit-gate.json` | `1463bd49eb13860e21248a307f6cff9c448bd4aa0d50e86bb9502fb03b0605af` |
| `a2audit-settle.json` | `51300e60c0473de2d1466ab570126edc72ef53aee675f713216252bbc7bc6b51` |
| `a2residual-dispatch.json` | `57f4c573ffe9dbe40485e14a6e2b7ba68e96e799c81dcaf2ab4a36bbb1400b69` |
| `a2residual-settle.json` | `5daf8d9f72aa7c7ba0b2dc1c5963802718e29cf8ea679940636881f4ede8b785` |
| `a2after/timestamps-strict-at-9ef97f08.txt` | `4619faa04e09ba87e0ef759d881147912c140c0552411856ffef83d6bd4306e4` |

The event was absent before and after. `result.json` records `exact_byte_restoration:true`, `source_unchanged:true`, `red_matches_expected:true`, `caught_exception:null` and `verdict:"killed"`.

### Source and spec digests

These pinned/installed bytes were unchanged by the probe; the four copied assets also had the same hashes in all three snapshots:

| Source | SHA256 |
|---|---|
| `.ufo/waves/round-20/tools/evidence-timestamps.py` | `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00` |
| `tools/round-33/timestamps/run-gate-hashed.py` | `e011ed69e72bed408de30211712b2e65d69fd01b9c002a45eb7ce5acf6055bb0` |
| `tools/round-33/timestamps/allowances-hashed.json` | `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332` |
| `tools/round-33/timestamps/build-hashed-fixture.sh` | `37206762bb48cbdd7b7758b46eda3e8129728077a32c9d71bc98d96088465152` |
| `tools/round-33/timestamps/run-hashed-selftest.sh` | `d60840374bc75a4bc67d526248786405b00a4b6456dbfcbe7d38ccd03785770e` |

The original five lane fixture files were also included in the read-only before/after source snapshots. No original source, fixture, spec, Git/JJ state, config or service was edited.

## Bounds, receipts and limits

- Only scratch Git writes; Git environment variables were unset. No native fixture/carrier execution, REA/MCP, build, formatter, linter, unrelated selftest, full production timestamp scan or another runtime invocation.
- No held builder/quarantine findings or derivatives were inspected or used. No replacement study was constructed; no policy refusal or model switch occurred in this item.
- Every direct experiment subprocess had `timeout --kill-after=3s 50s`; each driver invocation additionally had an enclosing `timeout --kill-after=5s 240s`. The driver checked a 210-second launch window and a 100-direct-launch ceiling. Observed direct launches: **21 setup + 11 mutation/restoration**. The inherited `RLIMIT_NPROC=8192` is UID-wide, not a measured per-probe cumulative descendant counter.
- Inherited per-process limits: address space 512 MiB, CPU 45 s, file size 1,048,575 bytes, open files 128, core size 0. These are limits, not peak-memory measurements or an aggregate tree-memory measurement.
- All explicit artifact writes enforced `<1 MiB`; the mutation itself was 35 bytes and the largest original fixture blob was 40,560 bytes. Each launched process group was cleaned in `finally` using `killpg(SIGKILL)`; all recorded group-cleanup attempts returned ESRCH after normal completion. No background jobs/services were started.
- No tools were installed or updated.

Retained under `S`:

- `probe.py`: exact reproducible driver. Actual entry argv was `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 240s python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WTimestampUnlisted/probe.py setup`, then the identical entry command with `mutate-restore` instead of `setup`; both driver exits were 0.
- `provenance.json`: pinned source digests, original source snapshot, base comparisons, bounds and pristine fixture identity.
- `commands-setup.json`, `commands-mutate-restore.json`: actual argv, start/end UTC, stdout, stderr, exit, synthetic commit-date overrides and process-group cleanup for every direct launch.
- `mutant.patch`: exact one-file addition; `result.json`: all three snapshots, source-before/after comparison and result.
- `receipts/pristine/`, `receipts/mutated/`, `receipts/restored/`: complete `outer.stdout`, `outer.stderr`, `outer-receipt.json`, inner `stdout.json`, `stderr.txt`, `receipt.txt` and extracted `summary.json`.

**Limit:** this reproduces the existing timestamp selftest's unlisted control on five old text fixtures, not a new independent fixture corpus or proof about every unlisted timestamp shape. It demonstrates that these five exact allowances do not suppress this unlisted synthetic event. Findings are lane advice only; no integration, shipping or claim admission was performed.

Only this scoped report was written in the lane.

Trailer: `.ufo/waves/round-33/w1/WTimestampUnlisted.md`
