# R41SrcRea — REA 6.5.0 / unblob 26.6.4 source anchors for the SquashFS outcome-triage table v3

**Verdict: DONE** — all four sites located with file:line and ≤25-word quotes; every document is already
pinned by an existing row (S118, S119, S120, S121, S123) except `python/unblob/processing.py`, which needs
new **S129**; and the envelope probes turned up six findings for the v3 text (§6), three of them
calibration faults in the draft's label precedence rather than wording.

Seat: scribe, round 41 wave 1, pre-freeze. Read-only: no lane file, no `corpus/`, no `tools/`, no judge,
no VCS mutation, no subagent. Nothing installed or upgraded this round (`npx rea-agents@6.5.0` was
already cached; the 6.5.0 tarball was re-downloaded to scratch only to compare digests).

## Axes I moved

1. **Anchor resolvability** — every quote carries a file:line and a digest that was re-derived today, so
   the L1 can re-open any of them without my scratch.
2. **Row economy** — extend a row where the *document* is already pinned; mint only where no row covers
   the document at all (exactly one case).
3. **Draft calibration** — check the precedence rules against what the producer can actually emit, not
   against what reads well.
4. **Reproducibility** — every measured claim is a command in `probe.sh` plus a stored envelope.

---

## 1. Where `depth-limited` is minted, and its fields

Minted in three steps, all in the REA package:

- `dist/firmware/FirmwareReports.js:155` `const depths = [];`
- `dist/firmware/FirmwareReports.js:229-230` — `if (record.task.depth >= context.maxDepth)` …
  `depths.push(path);` (the *logical* task path, i.e. `$output/<extract dir>`)
- `dist/firmware/FirmwareReports.js:384` — `depth_limited_paths: depths.sort(),`
- `dist/firmware/FirmwarePublication.js:294-299` — `...normalized.depth_limited_paths.map((input_path) => ({ kind: "depth-limited", input_path, ...emptyGap,` …
- `dist/firmware/FirmwarePublication.js:39-46` — `emptyGap` sets `relative_path`, `handler`, `provider_id`,
  `range`, `root_file_range` to `null` and `dependencies` to `[]`; the row's only real content is
  `input_path` plus `continuation_id`.
- ceiling and continuation: `:23` `const MAX_EXTRACTION_DEPTH = 10;`, `:17` "Rerun extract_firmware with a
  higher max_depth (up to 10) and a fresh output_directory to descend into this path.", `:24-28` the three
  continuation variants, `:245-272` the `reRootablePaths` index used only at the ceiling.
- schema: `dist/domain/firmware/firmwareAnalysis.js:83-104` ("One unextracted region or failing
  task/stage, with a supported continuation"), `:88` the kind enum, `:150` `depth_limited_paths`.
- input cell that sets the ceiling: `dist/cli-runtime/cutterToolContracts-TZH9EHr5.js:1761`
  `max_depth: z.number().int().min(1).max(10).default(3).describe("Extraction depth; reaching it yields
  partial analysis")`; flag mapping `dist/cli-runtime/cli.js:15282,15293`.

**S-row: existing S119** (same tarball, digest already pinned) — append the anchor text in
`row-drafts.md §C`; the `max_depth` input cell belongs to **S123** ("operation surface"). No new row.

Measured (`env-depth1.json`, `--max-depth 1`, own fixture `fixtures/outer.sqfs`):

```
depth_limited_paths ["$output/firmware.bin_extract"]
gap kind depth-limited, input_path "$output/firmware.bin_extract",
    relative_path null, handler null, provider_id null, range null, root_file_range null, dependencies []
files [firmware.bin_extract/inner.sqfs 4096 B]   coverage "partial"   diagnostics []
control at --max-depth 3 (env-depth3.json): files 2, gaps [], coverage "complete"
```

## 2. Where `missing-extractor-dependency` is minted — REA, not unblob (R40-CL5 L3)

- unblob raises a **report class**, never a "kind": `report.py:118-119`
  `class ExtractorDependencyNotFoundReport(ErrorReport):` "Describes an error when the dependency of an
  extractor doesn't exist."; raised at `extractors/command.py:69-77` on `FileNotFoundError`, carrying
  `dependencies=self.get_dependencies()`, and `command.py:101-102` is `return [self._executable]` — the
  one executable that branch ran.
- REA maps it: `dist/firmware/FirmwareReports.js:171-188` `dependencyNames` parses the report
  (`return reported ? { names, unnamed } : null;`), `:210-223` `noteChunkMissingDependencies`,
  `:320-335` `kind: dependencies === null ? "extractor-failure" : "missing-extractor-dependency"`.
- REA mints the row: `dist/firmware/FirmwarePublication.js:165` (chunk), `:186` (stage), `:198`
  (task-wide), with `dependencies: [...dependencies]` and the unnamed variant at `:20`.
- suppression of the parallel failure row: `:239-241` "Chunks whose failure a dependency row already
  covers stay out of the generic extractor-failure emission." and `:288-293`.

**S-rows: existing S119** (kind + row shape), **S120** (raise site, one-name list), and **S112** already
covers the handler's `lines 24-70` (executable choice `:37-54`; handler list `:68-69`).

Measured negative: `grep -rn "missing-extractor-dependency\|extractor-failure\|depth-limited"` over the
installed unblob 26.6.4 package → **0 matches**. The three kind strings exist only in REA.

Measured positive (sasquatch unreachable, `$HOME/.local/bin` stripped from the child `PATH`):

| fixture | handler | gap `dependencies` | chunk `extraction_failed` |
|---|---|---|---|
| LE v4 (`outer.sqfs`) | `squashfs_v4_le` | `["sasquatch"]` | true |
| genuine AVM-BE (`avm-pad.sqfs`) | `squashfs_v4_be` | `["sasquatch-v4be"]` | true |

Both envelopes keep `handler`, `provider_id` and `range` on the row (unlike the depth row) and expose the
raw class in `diagnostics[0].report.__typename__ = "ExtractorDependencyNotFoundReport"` with
`severity: "ERROR"`. **The gap names only the executable the branch chose** — never the handler's
two-name list.

## 3. unblob's empty-target symlink branch that removes the link with no report (L6)

`extractor.py:67-71`:

```python
raw_target = os.readlink(path)  # noqa: PTH115
if not raw_target:
    logger.error("Symlink with empty target, removing.")
    path.unlink()
    return path
```

No `task_result.add_report(...)` — unlike the recursive-link branch (`:58-65`) and the escaping-target
branch (`:81-87`), both of which add `MaliciousSymlinkRemoved`. Dispatch is `fix_extracted_directory`
`extractor.py:95-113` (`if path.is_symlink(): fix_symlink(path, outdir, task_result)`), called from
unblob after every extraction (`processing.py:447`, `:678`), i.e. before REA inventories the tree — so the
removal can appear in neither `unpublished_entries` nor `extraction_failures`.

**S-row: existing S118** (same file, digest pinned) — append `:58-71,95-113` and add the scope clause for
the unreported removal.

Measured reachability probe (new, negative): the branch's input cannot be produced on this host —
`ln -s '' empty` → `ln: failed to create symbolic link 'empty': No such file or directory` (exit 1) and
`python3 -c "import os; os.symlink('','x')"` → `FileNotFoundError [Errno 2]`. sasquatch creates links with
the same syscall: `unsquashfs.c:1199-1205` `res = symlink(i->symlink, pathname);` … `EXIT_UNSQUASH_STRICT(…)`.
So L6 is a true source fact with an unreachable population through this extractor (see §6 F4).

## 4. Where `extractor-failure` gaps carry published files (partial)

- The gap row carries **no** file: `dist/firmware/FirmwarePublication.js:225-238` (`chunkGaps` spreads
  `...emptyGap`) and `:275-285` (stage rows, `dependencies: []`).
- The failure signal is per chunk: `dist/firmware/FirmwareReports.js:284`
  `const extractionFailed = detail !== null && detail.extraction_reports.length > 0;` → `:295-308`
  `extraction_failed: extractionFailed`.
- The files come from the whole staging tree with no per-chunk filter:
  `dist/firmware/FirmwareFiles.js:121-188` "Inventory private output without following links, enforcing
  aggregate staging budgets."; `FirmwarePublication.js:58-64` requires every *reported* file to exist,
  `:68-98` writes them, non-file entries become `unpublished_entries`, `:103` can force
  `coverage: "partial"`.
- unblob keeps the partial output: `processing.py:666-670` collects `e.reports` on `ExtractError`,
  `:677` "we want to get consistent partial output even in case of unforeseen problems", `:678-679`
  sanitise then `delete_empty_extract_dir` (only an empty dir goes, `:746-748`), `:681-688` add the
  surviving directory as a subtask at depth + 1.

**S-row: existing S119** for the REA side; **new S129** for `python/unblob/processing.py` — no existing row
cites that document (`grep -c processing.py corpus/SOURCES.md` → 0).

Measured `env-fatal.json` (fatal corruption, `fixtures/lebig-corrupt2.sqfs`):

```
coverage "partial"  files []
gap {kind:"extractor-failure", handler:"squashfs_v4_le", provider_id:"3685440:1",
     range:{offset:0,length:8192}, dependencies:[]}
diagnostics[0].report {__typename__:"ExtractCommandFailedReport", severity:"WARNING", exit_code:1,
  command:"sasquatch -le -no-exit-code -f -d …/firmware.bin_extract …/firmware.bin",
  stderr: base64("read_fragment_table: failed to read fragment table index\nFATAL ERROR: File system corruption detected\n")}
```

The producer's own argv in that diagnostic is the direct evidence for §6 F1.

---

## 5. S-row disposition — one table for the L1

| target | document | verdict |
|---|---|---|
| 1, 2, 4 (REA side) | rea-agents 6.5.0 tarball (`FirmwarePublication.js`, `FirmwareReports.js`, `FirmwareFiles.js`, `firmwareAnalysis.js`) | **extend S119** anchor + `teaches`; no new row |
| 1 (`max_depth` input cell, flag) | same tarball (`cutterToolContracts-TZH9EHr5.js`, `cli.js`) | **extend S123** anchor + one scope clause |
| 2 (report class, raise site, one-name list) | unblob `report.py`, `extractors/command.py` | **extend S120** anchor |
| 2 (executable per endianness) | unblob `handlers/filesystem/squashfs.py` | **no change** — inside S112's existing `lines 24-70` |
| 3 (silent empty-target removal) | unblob `extractor.py` | **extend S118** anchor + scope clause |
| 3, 4 (symlink(2) writer, `-no-exit-code` exit control) | sasquatch `unsquashfs.c` | **document is S121**; extend S121, or mint **S130** if one fact set per row is preferred (draft ready) |
| 4 (partial-output retention, depth gate, empty-dir deletion) | unblob `processing.py` | **NEW S129** (draft ready) |

Drafts and pasteable anchor text: `artifacts/R41SrcRea/row-drafts.md`. Highest row at base is S126; S127
and S128 belong to `R41SrcAvm`, so the new id is **S129**.

Identity checks (all re-run today, `anchors.md §6`): 6.5.0 tarball sha256 `531717a0…` = S119/S123 pin and
the five cited dist files byte-identical between tarball and installed copy; `extractor.py` `1bb49811…` =
S118 = installed; `report.py` `2329783f…` = S120 = installed; `file_utils.py` `87d4dc9a…` = S122 =
installed; **`processing.py` `599afe91…`, 32013 B** = installed; `unsquashfs.c` `ece42b66…`, 120167 B =
S121 pin.

---

## 6. Findings that should change the v3 text (draft attack)

**F1 — rule 4 (`extractor-failure` ∈ G and P > 0 → `partial-body-failure`) cannot arise from a
non-fatal SquashFS extraction.** unblob always passes `-no-exit-code` to sasquatch
(`squashfs.py:56-64`); sasquatch returns `exit_code` 0 or 2 gated on `set_exit_code`
(`unsquashfs.c:4019-4021`, `4575-4618`); unblob raises only when `res.returncode != 0`
(`command.py:59-68`). A partial-but-non-fatal run therefore reports nothing — it lands on `clean` /
`clean-empty` with `coverage` possibly still `"complete"`. Only fatal failures survive (measured exit 1
with and without the flag). Consequence: the row may exist as an envelope-level class, but the entry must
not assert a *cause* for it beyond "the producer returned a failed exit for this chunk". Flip condition: a
measured REA envelope on a `squashfs_v4_*` chunk with `extractor-failure` and `files > 0`.

**F2 — `depth-limited` never means "nothing below it was published".** Measured: gap present, a 4096-byte
file published at `$output/firmware.bin_extract/inner.sqfs`, and the gap names the *directory* with every
identity field null. A generator class map that treats depth-limited as "empty nested region" would
disagree with every real envelope.

**F3 — `dependencies` is the one chosen executable, not the handler's dependency list.** Measured
`["sasquatch"]` for the LE branch and `["sasquatch-v4be"]` for the AVM-BE branch, although
`squashfs.py:68-69` returns both names. Rule 3's "D names X" wording is safe; a cell expecting both names
(a v4be-only absence producing two dependencies, or a BE image naming `sasquatch`) is false.

**F4 — the L6 edge is real but unreachable through sasquatch.** The silent branch is at
`extractor.py:67-71`; the input needs a symlink whose target is the empty string, and `symlink(2)` refuses
it on this host (two measured refusals), while sasquatch creates links with `symlink(2)`
(`unsquashfs.c:1199`). Recommend the repair read "the branch exists and reports nothing; no image can
reach it through sasquatch 4.5.1", and that no held-out class is scored on it. [INFERENCE] for a foreign
filesystem that might accept an empty target.

**F5 — `coverage` is derived, not observed.** `FirmwareReports.js:419-423` makes it `"partial"` when a
depth ceiling was hit, a diagnostic exists, or any chunk has a null handler or is encrypted. Any silent
partial (F1) reads `"complete"`. If v3 uses `coverage` as a feature, it inherits that blind spot; the
table should key on `G`, `D`, `P` and the diagnostic reports, not on `coverage`.

**F6 (minor) — do not read severity as a failure signal.** `ExtractCommandFailedReport` is
`Severity.WARNING` (`report.py:94`, measured in the diagnostic), and the dependency report is `ERROR`.
The trustworthy per-stage facts are the report `__typename__`, `exit_code`, and the chunk's
`extraction_failed`.

---

## 7. Exact commands and outcomes

All runs from `/fast/scratch/hyaku/kaidoku-r41/R41SrcRea`; `unblob.log` and all outputs there; the three
fixtures are lane-built (no vendor bytes).

```
python3 -I -B gen-squashfs.py --endian avm-genuine avmtree avm.sqfs   -> "wrote avm.sqfs 322 bytes, inodes 4 mode avm-genuine"
mksquashfs inner-src inner.sqfs -comp gzip -noappend -quiet -all-root  -> outer.sqfs 4096 B, sha256 91a530e2…
truncate -s 4096 avm-pad.sqfs                                          -> sha256 319a0239…
(write zeros at 4000..4300 of an 8192 B mksquashfs image)              -> lebig-corrupt2.sqfs sha256 853fb41a…

cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
   --format json --full-output --max-depth 1 "$S/mk/outer.sqfs" "$S/out-d1"          -> CLI exit 0
   … --max-depth 3 …                                                                -> CLI exit 0
   … PATH without $HOME/.local/bin, --max-depth 2, outer.sqfs                        -> CLI exit 0
   … PATH without $HOME/.local/bin, --max-depth 2, avm-pad.sqfs                      -> CLI exit 0
   … --max-depth 2, lebig-corrupt2.sqfs                                              -> CLI exit 0
$HOME/.local/bin/sasquatch -le -no-exit-code -f -d q lebig-corrupt2.sqfs    -> exit 1, 0 files, "FATAL ERROR"
$HOME/.local/bin/sasquatch -le           -f -d q lebig-corrupt2.sqfs        -> exit 1, 0 files (suppression does not cover fatal)
ln -s '' empty                                                              -> exit 1 ENOENT
grep -rn "missing-extractor-dependency\|extractor-failure\|depth-limited" $UNBLOB | wc -l  -> 0
```

Every envelope keeps the producer identity: `provider.version` `26.6.4`, `engine.executable_sha256`
`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`.

## 8. Limits (what I did not establish)

- **P > 0 together with `extractor-failure` was not constructed.** Two attempts: zeroing the fragment
  table → fatal, 0 files; zeroing 100 bytes inside a data block → sasquatch's multi-decompressor retry
  recovered, exit 0 with all files intact. F1's chain is measured link by link but the compound envelope
  is [INFERENCE].
- The `EXIT_UNSQUASH` / `EXIT_UNSQUASH_STRICT` macro **bodies** were not traced (absent from
  `unsquashfs.c` and `unsquashfs.h` at that tag). The one fatal path I did exercise exits 1 with and
  without `-no-exit-code`, which is all F1 needs.
- Empty-target reachability was tested on this host's filesystem only; a foreign FS that accepts an empty
  target would reopen F4.
- I did not run REA on the round-40 carriers V1/V2/L1/L2 (they need the vendor rebuild) — the five probes
  use lane-built fixtures only. **No reserved image was read, run or carved.**
- REA stages inputs under `/tmp/rea-firmware-*` (its own behaviour, not controllable by `TMPDIR`); the
  leftover from my runs was removed, and nothing of mine remains in `/tmp`.

## 9. Out of scope / not claimed

No claim about any vendor image, about whether the 5490/5491 members are AVM-BE, about sasquatch's
brute-force recovery quality, or about the round-41 C1/C2 scores. I edited no lane file, minted no row in
`corpus/SOURCES.md`, and ran nothing from the judge or the campaign tools.

## 10. Artifacts

`.ufo/waves/round-41/w1/artifacts/R41SrcRea/`

- `anchors.md` — anchors table (4 targets, 48 anchors), S-row disposition, identity checks.
- `row-drafts.md` — S129 (new, `processing.py`), optional S130 (sasquatch writer/exit), pasteable anchor
  and scope addenda for S118, S119, S120, S121, S123.
- `env-depth1.json`, `env-depth3.json`, `env-nodep-le.json`, `env-nodep-avmbe.json`, `env-fatal.json` —
  reduced REA envelopes (`parameters`, `subject`, `provider`, `evidence_id`, `normalized_result`).
- `probe.sh` — the five invocations and the reduction.
- `fixtures/{outer.sqfs,avm-pad.sqfs,lebig-corrupt2.sqfs,sha256sums.txt,build.sh}` — 4 KiB / 4 KiB /
  8 KiB lane-built fixtures with their rebuild script.
