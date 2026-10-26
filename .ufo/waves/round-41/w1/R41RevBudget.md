# R41RevBudget — REA 6.5.0 `extract-firmware` staged-entry budget, reversed and measured

**Verdict: CONFIRMED — the budget is the `max_output_files` option (default 10 000, inclusive), it counts
every directory *name* under REA's private extraction root (files, symlinks, directories, specials — but not
the root itself), it is one aggregate and not per depth, `--max-depth` does not change the constant but
changes what is staged, and exceeding it is a hard `AnalysisOutputError` (`code: unreadable_output`) with
**no** result envelope, **no** gap kind and **no** truncation. Prediction: the 5491 nested
`filesystem_core.squashfs` needs 7 367 staged entries at `--max-depth 1` against a budget of 10 000 →
**fits, 26.3 % headroom**, and the model is validated at exactly that scale (7 366-entry carrier: success at
`--max-output-files 7366`, failure at `7365`).**

Round 41, wave 1 (pre-freeze). Seat: `R41RevBudget`, leaf. Base `49096c7e6f226af0c750c4b003be58883cb6049f`.
No reserved carrier was read, run or carved by this seat: every measurement below is on lane-built fixtures
in scratch (`/fast/scratch/hyaku/kaidoku-r41/R41RevBudget`, removed before yield). No vendor bytes were
copied into the lane.

---

## 1. The constant and where it lives

Package: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`rea-agents@6.5.0`, run through
`npx -y rea-agents@6.5.0`).

| surface | declaration | value |
|---|---|---|
| domain schema (`extract_firmware` input) | `dist/domain/firmware/firmwareAnalysis.js:42-46` — `z.number().int().min(1).max(100_000).default(10_000).describe("Staging entry budget, including directories and links")` | **10 000 default, 1…100 000 inclusive** |
| CLI flag on `extract-firmware` | `dist/cli/firmwareCommands.js:48,58` (`maxOutputFiles: extractInput.max_output_files`) → `--max-output-files` (measured in `--help`) | same schema |
| MCP tool contract (duplicate) | `dist/mcp/toolContracts-BW05wpcr.js:1888` and `dist/cli-runtime/cutterToolContracts-TZH9EHr5.js:1763` — identical `default(1e4).describe("Staging entry budget, including directories and links")` | same |
| enforcement | `dist/firmware/FirmwareFiles.js:122-188` `inventoryFirmwareOutput(root, maxBytes, maxEntries, operation, signal)`; throw at `:151-153` | — |
| wiring | `dist/firmware/FirmwareProvider.js:244` (`entries: request.input.max_output_files`), `:260` (post-run inventory), `:224` (`outputRoot = join(root.path,"extracted")`) | — |
| mid-run enforcement | `dist/firmware/FirmwareCommand.js:106-113` — inside `while (!(await supervisor.waitForOutputClose(100)))` it calls the same inventory every **100 ms** | — |

There is **no** separate constant in `FIRMWARE_LIMITS` (`dist/firmware/FirmwareRelease.js:27-33` holds only
`inputBytes`, `reportBytes`, `diagnosticBytes`, `addressSpaceBytes`, `timeoutMs`); the entry budget exists
only as the request field, so **every caller that omits the flag gets 10 000**.

## 2. What it counts — algorithm and measurement

`inventoryFirmwareOutput` (`dist/firmware/FirmwareFiles.js:122-188`), verbatim semantics:

1. `pending = [root]` (`:124`) — a stack; it pops directories LIFO, so the walk is depth-order-agnostic.
2. For each directory it `opendir`s and, **for every entry name**, does `count++` then
   `if (count > maxEntries) throw` (`:148-153`). The type test happens *after* the throw check, so the
   increment is type-blind.
3. Only then it `lstat`s each name: `stat.isDirectory()` → pushed for descent and **not** added to `entries`
   (`:167-169`); regular file → `bytes += stat.size` (`:171-174`); symlink/special → `bytes += 0`.
   Non-directories are appended to `entries` with `kind ∈ {symlink, file, special}` (`:175-186`).
4. The returned array is sorted by code-point order (`:188`).

Therefore, precisely:

- **counted**: every name inside the staging root, one unit each — regular files, symlinks, directories
  (directories are counted once as a name, *and* their children are counted), fifos, sockets, device nodes.
- **not counted**: the staging root itself; anything outside it. In `extract_firmware` the counted root is
  `<rea-root>/extracted` (`FirmwareProvider.js:224`), so `firmware.bin`, `report.json` and `unblob.log`
  (all written to `<rea-root>/`, `FirmwareProvider.js:226-243`) never consume budget.
- **inclusive**: `count > maxEntries` throws, so a budget of N admits exactly N names.
- **one aggregate, not per depth**: a single `count` spans the whole tree; depth only changes how many
  directories/names exist. There is no per-chunk or per-depth allowance.
- **order of work**: directories are *not* returned as entries but *do* consume budget — the budget is
  strictly larger than the published-entry list by the directory count.
- **the returned list is the only source of result rows**: `publishFirmwareExtraction` takes
  `context.entries`, keeps `kind === "file"` for `files` (`FirmwarePublication.js:58-64`), turns every other
  entry kind into `unpublished_entries` (`:66-70,105`) and each of those into an `unpublished-entry` gap
  (`:301-307`). So the budget also caps the number of rows a receipt can carry — for the V4-shaped census
  the inventory returned 6 964 entries (6 349 files + 615 symlinks) out of 7 366 charged names.

### Measured (not inferred)

Direct unit probe of the shipped function
(`artifacts/R41RevBudget/count-entries-probe.mjs`, run against a tree with one of every name kind):

```
tree: inv/  9 names = 4 dirs (d1, deep, deep/a, deep/a/b) + 1 file (d1/f1) + 1 symlink (l1 -> d1/f1)
                     + fifo1 + sock1 + chardev (mknod c 1 3)
probe: budget_that_first_succeeds = 9
       entries_returned = 5   (dirs NOT returned)
       kinds_returned = ["file","special","symlink"]   (fifo, socket, chardev all "special", size 0)
       budgets 1..8 -> AnalysisOutputError "Staging entry budget exceeded (N)"
```

So: 9 names consume 9 units for 5 returned entries — directories and all three special kinds are charged.

End-to-end through the CLI (AVM path included), `artifacts/R41RevBudget/evidence-budget.json`:

| fixture (names) | depth | budget | result |
|---|---|---|---|
| `fx.squashfs` LE gzip, 7 names | 1 | 100 | ok, 3 files, 2 unpublished symlinks, gaps {depth-limited, unpublished-entry} |
| `fx.squashfs`, 7 names | 1 | **8** | **ok** — 8 = 1 (`firmware.bin_extract`) + 7 |
| `fx.squashfs`, 7 names | 1 | **7** | **exit 1**, `details.reason = "Staging entry budget exceeded (7)"` |
| `fx-avm.squashfs` AVM-genuine (BE structural, LE metadata headers, marker), 7 names | 1 | 8 / 7 | ok (`handler squashfs_v4_be`) / exit 1 — identical accounting on the AVM handler |
| `big.squashfs`, 7 365 names (401 dirs, 6 349 files, 615 symlinks) | 1 | **7 366** | **ok**, 12 552 ms, 6 349 files, 615 unpublished, 616 gaps |
| same | 1 | **7 365** | **exit 1** in **1 493 ms** |
| same | 1 | default (10 000) | ok, 33 759 ms |

The AVM fixture matters for R41-C1: unblob 26.6.4 `squashfs_v4_be` (sasquatch-v4be without `-be`) stages the
same name tree as the LE handler, so the budget arithmetic carries straight to V3/V4.

The `big` pair also proves the **mid-run abort**: a 1 493 ms failure versus a 12 552 ms success on identical
input can only come from the 100 ms poll in `FirmwareCommand.js:106-113`, which walks the partially written
tree and throws while unblob is still writing. REA then stops the owned child; the failure is re-thrown after
the supervisor settles (`FirmwareCommand.js:115-128`).

## 3. How `--max-depth` changes it

The constant is untouched by depth; the *consumption* and the *envelope* change:

- `--max-depth` is passed to unblob as `--depth N` with `--randomness-depth 0`
  (`FirmwareProvider.js:226-243`). Each carving level that actually runs creates exactly **one additional
  directory** (`<carved-file>_extract`) plus that level's own names.
- Measured on `fx2.squashfs` (outer tree: `nested/` dir, `nested/inner.squashfs`, `x`; inner image:
  `f1`, `f2`, `s1`): **depth 1 → 4 entries** (1 chunk dir + 3 names), **depth 2 → 8 entries**
  (4 + `inner.squashfs_extract` + `f1` + `f2` + `s1`). Budget 4 succeeds / 3 fails at depth 1; 8 succeeds /
  7 fails at depth 2.
- Depth also decides the `depth-limited` gap: `FirmwareReports.js:229` pushes every task with
  `task.depth >= maxDepth` into `depth_limited_paths`, and `:419` makes `coverage` **partial** whenever that
  list is non-empty. Measured: `fx` at depth 1 → gap `depth-limited` at `$output/firmware.bin_extract`
  **even though the fixture contains no nested image at all**; the same fixture at depth 2 → no
  `depth-limited` gap. `fx2` at depth 3 → no `depth-limited` gap. Ceiling is 10
  (`FirmwarePublication.js:23-24` `MAX_EXTRACTION_DEPTH = 10`, schema `max_depth.max(10)`).

Consequence for the C1 predicate: **every `--max-depth 1` receipt whose carrier yields a chunk at depth 1
carries `coverage: "partial"` and a `depth-limited` gap** (measured on three fixtures, including one with no
nested image at all), so "no failed chunk" must not be read as "coverage complete".

## 4. What an envelope looks like when the budget is exceeded

It is a **hard typed error**, not a gap, not a truncation, and there is no partial result:

```json
{"ok":false,
 "error":{"code":"unreadable_output",
          "category":"execution_failure",
          "message":"Analysis returned an unreadable result. Run `rea doctor` and review the reported details; repeating the unchanged request is not expected to succeed.",
          "retryable":false,
          "remediation":{"action":"Analysis returned an unreadable result. Run `rea doctor` and review the reported details; repeating the unchanged request is not expected to succeed."},
          "details":{"operation":"extract_firmware","reason":"Staging entry budget exceeded (7)"}},
 "meta":{"command":"extract-firmware","duration":"1328ms"}}
```

(verbatim from the `--format json --full-output` run at budget 7; exit code **1**). Without `--full-output`
the same projection is printed bare, `{"code":"unreadable_output",…}` — still exit 1.

Mechanism for each field: `AnalysisOutputError` (`dist/domain/analysisErrorCore.js:60-77`, tag at `:64`) →
`underlyingErrorCode` → `STATIC_ERROR_CODES.AnalysisOutputError = "unreadable_output"`
(`dist/domain/analysisErrorProjection.js:140`); `category` falls through
`STATIC_ERROR_CATEGORIES[...] ?? "execution_failure"` (`dist/domain/analysisErrorPresentation.js:110`) because
`AnalysisOutputError` has **no** entry in that map — note the internal inconsistency: `code` says
`unreadable_output` while `category` says `execution_failure`. `message` and `remediation.action` are the
generic `unreadable_output` text (`analysisErrorPresentation.js:271,284`); the only carrier of the real cause
is `details.reason` (`analysisErrorProjection.js:206-213`). Exit code 1 comes from
`dist/cliLogging.js:68,72,79`.

What is **absent** on this failure, and therefore cannot be claimed by any C1 receipt:

- no `evidence_id`, no `subject`, no `chunks`, no `handler` name, no `files`, no `extraction_gaps`, no
  `extraction_continuations`, no `partial_observation` (`projectAnalysisError` only attaches
  `partial_observation` where a producer set one; the firmware path never does);
- **no gap kind exists for capacity**: the `extractionGap.kind` enum is exactly
  `missing-extractor-dependency | unknown-chunk-handler | encrypted-chunk | depth-limited |
  extractor-failure | unpublished-entry` (`dist/domain/firmware/firmwareAnalysis.js:78-84`), so a budget
  overflow can never be reported as a gap or as a "supplementary" finding;
- **no "used" count**: `details.reason` prints only the configured budget, never
  `count`/`maxEntries`, so how close the run came is not observable after the fact — the only way to learn
  the entry count is the bisection used here;
- the output directory is **never created** (`out-7`, `out-nofull2`, `big-out-7365` all absent afterwards)
  and REA's staging tree is cleaned (`/tmp/rea-firmware-*` and `$S/rea-firmware-*` empty), because the
  inventory runs **before** `publishFirmwareExtraction` (`FirmwareProvider.js:260-267`).

Option-schema refusals are a different envelope: `--max-output-files 0` and `100001` are rejected before any
extraction with `{"code":"VALIDATION_ERROR","message":"Too small|Too big…","fieldErrors":[…]}`
(`maxOutputFiles` path), exit non-zero.

## 5. Adjacent budgets measured, because they interact

- **Byte budget** `max_output_bytes` (default 256 MiB, 1…512 MiB; `firmwareAnalysis.js:35-41`) sums **regular
  file sizes only** (`FirmwareFiles.js:171-174`; symlinks/specials add 0). `fx` needs 10+20+3 = 33 B:
  budget **32** fails with `details.reason = "Staging byte budget exceeded (32)"`. Budget **33** is *not* a
  clean pass test, because the same number becomes the child's file-size limit (next bullet) and the report
  dies first — the staging sum itself is proven by the 32-byte failure plus the code path.
- **`--max-output-bytes` also becomes the child's `RLIMIT_FSIZE`** (`FirmwareCommand.js:59`,
  `--fsize=${context.outputBudget?.bytes ?? FIRMWARE_LIMITS.reportBytes}`). Measured at exactly 33 bytes the
  run dies **before** the staging budget is consulted, with a different reason —
  `"Tool report is not valid complete JSON; stdout (1436 bytes) …"` from
  `readFirmwareReport` (`FirmwareFiles.js:103-116`, `JSON.parse` of unblob's `--report` file). [INFERENCE]
  the 33-byte file-size limit cut that report write; the observable fact is only that the report was
  unparseable. So: a tight byte budget poisons the provider report, and a C1 seat must leave
  `--max-output-bytes` at its default.
- **wall deadline** 120 000 ms (`FirmwareRelease.js:32`, enforced at `FirmwareCommand.js:107-108`) — this is
  the real risk for a big carrier, not the entry budget, and not the file-size limit: unblob's `--report`
  output is a *task* summary, only 1 441 bytes for the 7 366-entry fixture (`raw_result.report`), while
  REA's own published JSON for the same run is 2 497 764 bytes (that one is a published artifact and never
  passes through `RLIMIT_FSIZE`). So the `--fsize` pinch only appears when a caller sets
  `--max-output-bytes` absurdly low (measured at 33 B, §5).
- **Poll cost**: the 100 ms poll re-walks the whole staging tree; measured
  `inventoryFirmwareOutput` at 7 366 names = **80–140 ms per walk** (3 warm walks: 140/101/80 ms). During a
  long extraction the poll therefore runs nearly back-to-back and `lstat`s the same tree unblob is writing.
  For a 7 367-entry carrier expect ~100 ms per poll, i.e. roughly 0.1 M–1 M `lstat`s per 10–100 s of run.

## 6. Prediction for the reserved carriers (sqfs counts only — no REA run on any reserved image)

Census sources (read only): `artifacts/R41C1VendorV4/{oracle.tsv,nonregular.tsv,budget.json,chain-walk.json,provenance.json}`
and `artifacts/R41C1VendorV3/{oracle.tsv,nonregular.tsv,superblock.json}`; 7430 figure from
`.ufo/waves/round-40/w1/R40C1VendorScout.md:33`. I re-counted the TSVs myself
(`oracle.tsv` has no header: 6 349 rows; `nonregular.tsv` has no header: 1 017 rows = 401 `dir`, 615
`symlink`, 1 `char-device` at `dev/led 247:0`).

| carrier | names = files + dirs + symlinks + specials | + unblob chunk dir | staged entries | budget | headroom | verdict |
|---|---|---|---|---|---|---|
| **V4 = 5491 nested `filesystem_core.squashfs`** (carved `[0, 32720860)`) | 6 349 + 401 + 615 + 1 = **7 366** | +1 (`firmware.bin_extract`) | **7 367** | 10 000 | **2 633 (26.3 %)** | **fits** |
| V4 fallback = 5491 wrapper member `./var/tmp/filesystem.image` | 8 + 9 + 85 + 1 = 103 | +1 | 104 | 10 000 | 9 896 | fits |
| V3 = 5490 member `./var/tmp/filesystem.image` | 8 + 9 + 85 + 1 = 103 | +1 | 104 | 10 000 | 9 896 | fits |
| 7430 nested core (cross-check datum) | 7 524 inodes ⇒ 7 523 names ±1 | +1 | **7 524** | 10 000 | 2 476 (24.8 %) | fits |

Arithmetic is `staged = names + 1` (one directory per executed chunk at `--max-depth 1`, measured twice:
`fx` 8 = 1+7, `big` 7 366 = 1+7 365, `fx2` depth 2 = 8 = 1 + 3 + 1 + 3). The byte budget is also clear:
Σ regular-file sizes from `oracle.tsv` = **110 187 475 B** of 268 435 456 B (41.0 %), and unblob's own
`--report` output for a tree this size is only ~1.4 KB (measured), so `RLIMIT_FSIZE` (= the byte budget,
`FirmwareCommand.js:59`) is never the limiter for V4.

Confidence and residuals:

- **HIGH** that 7 367 ≤ 10 000 passes: the counting rule is read in code, unit-probed, and validated
  end-to-end **at the same scale** (7 366 names: pass at 7 366, fail at 7 365), and separately on an
  AVM-genuine carrier through the `squashfs_v4_be` handler. The end-to-end validation was on a lane-built
  census, not on the vendor bytes.
- ±1 on the special: if sasquatch cannot `mknod` `dev/led` as an unprivileged user, the staged count is
  7 366 instead of 7 367; either way it passes. Precedent that a char-device carrier does not abort: the
  round-40 V1 carrier (`corpus/evidence/round-40/c1/V1/nonregular.tsv`) also contains one `char-device` and
  its REA run published 697 files with `extraction_failed: false`. [INFERENCE] the device node itself may be
  skipped or created; the budget is unaffected.
- **Depth 1 is load-bearing.** At the default depth 3 unblob would descend into anything inside the rootfs
  (V4's `oracle.tsv` names **no** `.squashfs`/`.cramfs`/`.jffs2` file — 0 matches — but does carry
  `etc/fiber/sfp_fw.image` 3 145 732 B and `lib/firmware/ath_tgt_fw2.fw` 11 950 340 B, which a deeper run
  may carve). Any extra level costs one dir plus that level's names, and each extra level also changes the
  gap set. The C1 predicate's `--max-depth 1` keeps the count at 7 367.
- **Time, not entries, is the plausible failure mode.** My 7 366-entry fixture took 12 552 ms warm /
  33 759 ms cold; V4 additionally xz-decodes ~110 MB. That must finish inside the 120 s wall deadline while
  ~100 ms of every 200 ms is spent re-walking the staging tree. [INFERENCE] V4 lands well inside 120 s, but
  this is the axis to watch, and it is worth re-measuring on the actual freeze run.

## 7. What this does to the draft claims (calibration)

1. **R41-C1's predicate is safe but conditional on the flag.** `--max-output-files` is not in the draft's
   command line; it is not needed for V3/L3/L4 (104/—/small), but if a seat ever sets
   `--max-output-bytes` tightly, the *report* truncates before the staging budget is reached (§5), producing
   a `unreadable_output` receipt with a completely different `details.reason`. Keep default byte budget.
2. **A budget overflow cannot be scored as partial.** It yields no receipt at all (no evidence id, no
   handler, no gaps). So the C1 counter would see a *missing* after-receipt, not a failing one — the draft's
   "names the `squashfs_v4_be` handler with no failed chunk" would fail as an absence, and the honest
   read is "the carrier is too large for REA", not "REA mis-extracted". With 2 633 entries of headroom this
   does not happen for V4.
3. **The expected V4 envelope is a COMBINED gap set.** Measured on a synthetic carrier with this exact census
   (401 dirs / 6 349 files / 615 symlinks, AVM-neutral LE gzip): 6 349 published regular files + 615
   `unpublished-entry` gaps (all symlinks are unpublished — publication publishes regular files only,
   `FirmwarePublication.js:58-70`) + 1 `depth-limited` gap at the chunk root, `coverage: "partial"`,
   616 gaps total. That is `depth-limited + symlinks`, i.e. **exactly C2 rule 7's combined class** — the v3
   table's `depth-limited-nested` must win over `mixed-symlinks` for the carrier the C1 claim is built on,
   and C1's frozen gap rule must admit both kinds. Both drafts currently allow this; a C1 gap rule written
   for "depth-limited only" would fail on its own carrier.
4. **The C1 draft's "fits REA's entry budget at depth 1" clause is falsifiable and now measured**, not
   inferred: 7 367 of 10 000.

## 8. Evidence

Scratch root (removed at yield): `/fast/scratch/hyaku/kaidoku-r41/R41RevBudget`,
`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`, cwd `$S` for every REA run. REA's staging root follows the
**invoking shell's** `TMPDIR` (measured: with `TMPDIR=$S` the report path became `$S/rea-firmware-viOxmQ/…`);
the first fixture runs ran without it and staged under `/tmp` (REA removed every staging tree itself — no
residue remained, checked). All later runs pinned `TMPDIR=$S`.

```
# AVM-genuine fixture (same tree as fx, real AVM layout)
python3 -I -B <lane>/tools/round-40/gen-squashfs.py --endian avm-genuine --comp xz "$S/tree" "$S/fx-avm.squashfs"
npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 \
    --max-output-files 8 "$S/fx-avm.squashfs" "$S/avm-8"      # exit 0, handler squashfs_v4_be
npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 \
    --max-output-files 7 "$S/fx-avm.squashfs" "$S/avm-7"      # exit 1, unreadable_output / Staging entry budget exceeded (7)
```

Artifacts (all under `.ufo/waves/round-41/w1/artifacts/R41RevBudget/`):

| file | content |
|---|---|
| `evidence-budget.json` | every run: parameters, exit outcome, files/unpublished/gap kinds/gap count/durations, byte-budget runs, validation refusals, walk timings, mid-run-abort proof |
| `inv-probe.json` | direct `inventoryFirmwareOutput` probe on the 9-name all-kinds tree (first successful budget 9, 5 returned entries, 1..8 throw) |
| `count-entries-probe.mjs` | the probe driver (imports the shipped dist module; builds nothing, runs no extractor) |
| `build-budget-fixture.py` | V4-shaped census builder (401 dirs / 6 349 files / 615 symlinks) + writer invocation |
| `fixtures/fx.squashfs` | 496 B, LE gzip, 7 names, sha256 `616b9e78…f19bd` |
| `fixtures/fx-avm.squashfs` | 505 B, AVM-genuine xz, 7 names, sha256 `aedc3228…4a38c3` |
| `fixtures/fx2.squashfs` | 466 B, LE gzip, nested squashfs, 3 names, sha256 `121a3116…4ec3b2` |
| `fixtures/sha256.txt` | hashes of the fixtures and of `big.squashfs` (455 298 B, sha256 `df57bc61…048f20`, 7 365 names) |

`big.squashfs` is not copied (rebuild instead):
`python3 -I -B build-budget-fixture.py "$S/big" "$S/big.squashfs"` (defaults = 401/6 349/615, LE gzip;
the writer prints `names=7365 … staging_entries_at_depth1=7366`).

## 9. Limits of this seat

- I did **not** run REA, unblob or any extractor on FRITZ!Box 3490/5490/5491/7560 or on L3/L4; I did not read
  the reserved images at all. V3/V4/7430 censuses are inherited from the named artifacts and recounted
  arithmetically, not re-derived from vendor bytes.
- The end-to-end validation is on lane-built LE and AVM-genuine fixtures; the vendor images add xz-compressed
  metadata blocks and real scale in bytes, which the count model does not distinguish [INFERENCE].
- I did not test `sasquatch`'s handling of device nodes as an unprivileged user beyond the round-40 V1
  precedent; the ±1 entry is outside the decision.
- No tool was installed, upgraded or removed (npx cache `rea-agents@6.5.0`, uv-tool `unblob` 26.6.4 and
  `~/.local/bin/sasquatch{,-v4be}` 4.5.1 were already present and untouched; no pacman transaction, no
  network fetch). Node `v24.21.0`; REA's resource limiter default `/usr/bin/prlimit`
  (`FirmwareCommand.js:37`, util-linux 2.42.4) was present and used unchanged.
