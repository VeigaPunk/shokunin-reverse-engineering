# C1DepthSource — REA 6.5.0 source re-opening for the `squashfs_v4_le` port (R50-C1)

Verdict: **the round-41 REA reading carries over to `squashfs_v4_le` verbatim; the port may
keep the root rule, the two-namespace strip, and the gap families exactly as they are.** All
three cited round-41 line pins hold at rea-agents 6.5.0 (byte sha256s below). REA has zero
handler-specific code — `squashfs` appears nowhere in dist — so the handler name arrives as an
opaque string from unblob and the port changes only `HANDLER = 'squashfs_v4_be'` →
`'squashfs_v4_le'` (counter lines 287/121/2037 cell text). On the failure question: a
**non-zero sasquatch exit produces a visible gap** (`extractor-failure` or
`missing-extractor-dependency`, empirically reproduced), but the **unblob `-no-exit-code` flag —
which unblob always passes — masks non-fatal sasquatch failures into exit 0, and then NO gap
appears**: the receipt is indistinguishable from a complete run and only the counter's
per-file oracle-equality clause catches the loss. This is the port's load-bearing finding:
`oracle_hits_ok` is the sole tripwire for silent partial extraction, so the frozen oracle must
stay a complete per-file table, never a sample.

## Environment pins (all read directly, sha256 verified)

| component | version | sha256 |
|---|---|---|
| rea-agents package | 6.5.0 (`package.json` `"version": "6.5.0"`) | `a500302319c1214a`…`050a6c` (full in receipts/SHA256SUMS.txt) |
| dist/firmware/FirmwareFiles.js | 6.5.0 | `f6934b7bd71208d8`…`e3073a` |
| dist/firmware/FirmwareReports.js | 6.5.0 | `6885966b78451b3d`…`24cba16` |
| dist/firmware/FirmwarePublication.js | 6.5.0 | `bb4f3246bee70a5b`…`d51029` |
| dist/firmware/FirmwareProvider.js | 6.5.0 | `3c1e929b01be5fc2`…`d81654` |
| dist/domain/evidence.js | 6.5.0 | `f992d93eaf228bf8`…`a78dcff` |
| unblob handlers/filesystem/squashfs.py | 26.6.4 | `2d7b901b54e2ad28`…`d5599287` |
| unblob extractors/command.py | 26.6.4 | `8ae7d2a3980b80b2`…`09f85af` |
| node | v24.21.0 (satisfies REA engines) | — |

Package root: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. unblob tree:
`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob`.

## Findings

| # | question | finding (file:line, quote ≤25 words) | evidence |
|---|---|---|---|
| F1 | cited line `FirmwareFiles.js:177` | line 177 is exactly `relativePath: relative(root, path).split(sep).join("/"),` — the **bare** namespace for `files[]`/`unpublished_entries[]` | awk extract, quotes/FirmwareFiles-165-201.txt |
| F2 | cited lines `FirmwareFiles.js:191-200` | `export const firmwareLogicalPath` maps producer paths to `$input` / `` `$output/${…}` `` and throws outside-root — the **prefixed** namespace | same extract, lines 191-200 |
| F3 | cited lines `FirmwareReports.js:341-357` | the `derivations` builder: `records.flatMap((record) => record.subtasks.map((child) => {` … `handler: origin?.handler ?? null` — derivations from unblob subtasks, handler attached by `(parentPath, blob_id)` via `blobOrigins` | quotes/FirmwareReports-341-359-derivations.txt |
| F4 | how the chunk list is derived | `normalizeUnblobReport` parses unblob's task records; root must be exactly one depth-0 task whose HashReport equals the snapshot digest; `ChunkReport` detail schema = `handler_name`, `is_encrypted`, `extraction_reports` (lines 277-283); bounds validated (`region.parse`, invalid → throw) | quotes/FirmwareReports-255-330-chunks.txt |
| F5 | `chunks[].extraction_failed` | line 284: `const extractionFailed = detail !== null && detail.extraction_reports.length > 0;` — **any** extraction report, i.e. only error reports (unblob emits none on success), turn it true | same |
| F6 | `files[]` | FirmwarePublication.js:87-97: per materialized regular file, `relative_path` (bare), self-hashed `sha256`, `reported_sha256`, `mime_type`, `analysis_depth`, `runtime_address: null`, `original_file_range: null`; digest/size disagreement with the provider report throws (lines 80-85) | quotes/FirmwarePublication-56-115-publish.txt |
| F7 | `unpublished_entries[]` | FirmwarePublication.js:69-75: every inventory entry with `entry.kind !== "file"` pushes `{relative_path, kind, link_target}`; publication coverage demoted to `"partial"` when non-empty (line 103) | same |
| F8 | `extraction_gaps[]` kinds | FirmwarePublication.js:274-306: `extractor-failure` (stage rows + chunks `extraction_failed === true && handler !== null && encrypted !== true` and not already dependency-covered), `unknown-chunk-handler`, `encrypted-chunk`, `depth-limited`, `unpublished-entry`; dependency rows carry kind `missing-extractor-dependency` (lines 168-205) | quotes/FirmwarePublication-274-306-gaps.txt |
| F9 | coverage flag | FirmwareReports.js:419-423: `"partial"` if any depth-limited path, any diagnostic, or any chunk with `handler === null \|\| encrypted === true`; else `"complete"` | quotes/FirmwareReports-415-425-coverage.txt |
| F10 | evidence id | evidence.js:156-181 `semanticProjection` (subject digest/format/architecture, provider, analysis_profile, predicate_type, operation, **parameters**, raw_result, normalized_result, confidence, authority, environment, limitations, locations, evidence_links); line 182: `` `ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}` `` | quotes/evidence-150-186-244-258.txt |
| F11 | `--max-depth` plumbing | FirmwareProvider.js:227-240: REA runs unblob as `--process-num 1 --depth <max_depth> --randomness-depth 0 --report … --log … --extract-dir <root>/extracted <snapshot>`; input snapshot always named `firmware.bin` (FirmwareFiles.js:37) — whole-file chunk root is `firmware.bin_extract` regardless of handler | quotes/FirmwareProvider-224-245-unblob-argv.txt |
| F12 | REA handler opacity | `grep -r squashfs rea-agents/dist` → **no hits**: handler names are opaque; no BE/LE special-casing anywhere in REA | grep receipt (command in §Commands) |

## The failure question — what REA does for a `squashfs_v4_le` chunk

Chain (each hop quoted or observed; unblob **always** passes the flag — squashfs.py:56-64 builds
`[-no-exit-code, -f, -d, {outdir}, {inpath}]` for every squashfs v4 chunk, LE included; the real
command line is visible in receipt R2's diagnostic):

1. **sasquatch exits non-zero (fatal).** unblob `Command.extract` raises
   `ExtractCommandFailedReport` on `res.returncode != 0` (command.py:56-64). The chunk's
   `extraction_reports` becomes non-empty (processing.py:661-691), so REA reports
   `extraction_failed: true`, one `extractor-failure` gap naming handler + provider_id, a
   diagnostics row with the base64 stdout/stderr, coverage `partial` — **and no `derivations[]`
   edge**, so the counter's root lookup fails closed (`extract_root: null`). **A gap appears.**
   Empirically reproduced (receipt `rea-sasquatch-exit1.json`: `derivations: []`, `files: []`,
   gap `extractor-failure`).
2. **sasquatch absent from the child PATH.** `FileNotFoundError` →
   `ExtractorDependencyNotFoundReport` naming only the executed binary (LE runs `sasquatch`
   alone; `sasquatch-v4be` is never needed for LE — squashfs.py:24-26, 68-69, command.py
   `get_dependencies` → `[self._executable]`). REA: chunk gap `missing-extractor-dependency`
   with `dependencies: ["sasquatch"]` — exactly the plan's CTL-C1-3 kind. Reproduced
   (`rea-sasquatch-absent.json`).
3. **sasquatch partial failure under `-no-exit-code` (the AVM-relevant case).** sasquatch's own
   usage: `-no-exit[-code]  don't set exit code (to nonzero) on non-fatal errors`; exit 2 =
   "Non-fatal errors … Unsquashfs continued and did not abort" (receipt `sasquash-help.txt`).
   Non-fatal losses (xattr/symlink/permission/write-classes) therefore exit 0 → unblob emits no
   report → `extraction_reports` empty → `extraction_failed: false` → **no gap of any kind;
   coverage can read `complete`** (F9). Files sasquatch skipped are absent from disk, so
   unblob emits no StatReport for them and REA's materialization cross-check
   (FirmwarePublication.js:61-63) passes trivially — both sides agree on the absence. The
   receipt is semantically identical to a fully successful run. Leg 3 is [INFERENCE from the
   quoted usage text + observed chain]; legs 1-2 and the full happy path are executed
   receipts. A fatal-error variant was executed: exit 1 stays exit 1 **with** the flag
   (receipts `sasquatch-fatal-plain.txt` / `sasquatch-fatal-noexitcode.txt`) — the flag masks
   non-fatal only.

Consequence for the port and the plan: CTL-C1-4's "standard LE carrier scores red on the
marker clause alone" and the per-file oracle equality are the only guards against this silent
loss; the disclosed limits should name it (suggested wording: "sasquatch non-fatal failures are
exit-0-invisible to unblob and REA under unblob's `-no-exit-code`; the oracle's complete
per-file table is the counter's only tripwire").

## Round-41 cited lines and the root rule verbatim?

- `FirmwareFiles.js:177` and `:191-200` — **hold exactly** at 6.5.0 (F1/F2): bare
  `relativePath` for published entries vs `$output/`-prefixed logical paths; the counter's
  `strip_output` strip-once rule (counter lines 27-36) reads the same receipt unchanged.
- `FirmwareReports.js:341-357` — **holds** (F3); the flatMap's object literal spans 352-358, so
  the cited window is if anything one line short, content identical.
- Root rule (`derivations[]` child path of every `squashfs_v4*` handler): **applies verbatim to
  `squashfs_v4_le`.** REA builds derivations from unblob subtasks with handler attached from the
  chunk id (F3); unblob names the LE handler `squashfs_v4_le` (squashfs.py:454-455) and carves
  to `{start}-{end}.{handler.NAME}` (extractor.py:131) + `_extract` suffix
  (processing.py:125-126, extract_suffix at :104) → carved root
  `<…>/<start>-<end>.squashfs_v4_le_extract`; whole-file root `firmware.bin_extract` (F11).
  Observed in receipt R1: `derivations: [{parent_path: "$input", child_path:
  "$output/firmware.bin_extract", handler: "squashfs_v4_le", …}]`. The counter's
  `SQUASHFS_PREFIX = 'squashfs_v4'` (line 288) already matches the LE name; only `HANDLER`
  (line 287) and the docstring/cell text change. Keep the prefix broad so CTL-C1-1's planted
  BE receipts still trip the red path.
- unblob's AVM marker check (`is_avm = header.bytes_used == header.mkfs_time`) exists only in
  the **big-endian** branch (squashfs.py:48-50, selecting sasquatch-v4be and omitting `-be`);
  for LE the extractor always passes plain `-le` (squashfs.py:53-54) and the marker is invisible
  to unblob and sasquatch flag selection — confirms plan disclosed limit (1) at source level.

## Port cautions for C1CounterPort (receipt-shape facts, all observed in R1)

1. The published `normalized_result` has **no `failed_extraction_stages` key** (stages are
   folded into `extraction_gaps`); the round-41 counter never reads it (grep: 0 hits) — keep it
   that way.
2. With `--max-depth 1` the root extract dir itself is always a `depth-limited` gap
   (`depth_limited_paths: ["$output/firmware.bin_extract"]`, coverage `partial`) — the frozen
   gap rule's `structural: {depth-limited: 1}` family is mandatory, not incidental
   (round-41 gap-rule.json confirms the shape; copy in receipts/).
3. `subject.digest.sha256` equals the snapshot = the carrier bytes' sha256 (verified equal for
   R1) — the `subject_pin_ok` clause binds the whole-file selection unchanged.
4. `parameters` is inside the semantic projection (F10) — `run_provenance_ok`'s
   output-directory prefix test and `evidence_id_ok` stay coupled as in round 41; port the
   scratch segment check to `/kaidoku-r50/`.
5. A dependency-missing receipt names only `["sasquatch"]` for LE — any CTL-C1-3 text that says
   "extractor dependencies" should not promise the v4be binary's name.

## Commands (exact; all under `S=/fast/scratch/hyaku/kaidoku-r50/C1DepthSource`)

- Quote extraction: `awk '{printf "%d\t%s\n", NR, $0}' <file> | sed -n '<ranges>'` (per-quote
  ranges in quotes/ filenames); exit 0 each; artifacts sha256 in receipts/SHA256SUMS.txt.
- `sha256sum` over cited sources and artifacts; exit 0.
- `sasquatch -h > $S/sasquatch-help.txt 2>&1`; exit 0.
- Lab build: `mksquashfs $S/noexit-lab/tree $S/noexit-lab/img.sqfs -comp xz -noappend -quiet
  -no-progress`; exit 0; image sha256 `2e9ee99821d1fbafaf514036ccf81f6bb657123dc74970ce00bba9710ff2afec`.
- R1/R2/R3 REA runs and R4/R5 sasquatch runs: commands, exit codes, UTC times, stdout sha256s in
  `receipts/RECEIPTS.txt`.

## Not run / limits

- No AVM vendor image was downloaded or extracted here (not this seat's slice); case 3
  (non-fatal exit-0 masking) is source+usage-text-derived, not executed — no local non-fatal
  trigger was reproducible as an unprivileged user (xattr-on-symlink is EPERM even at image
  build time; create-file failures are FATAL).
- `evidence_id` re-minting was not exercised (round-27 xpin does that; the rule is quoted, not
  re-run).
- No lane file outside my seat dir/report was written; no git mutation anywhere; no tool
  installs (pacman untouched).
