# R39W2ReproK6 — provenance attack on the committed R39-C1 receipt for carrier K6

**Verdict: CONFIRMED.** An independent post-freeze REA re-run of the frozen K6 carrier bytes reproduces
`corpus/evidence/round-39/c1/K6/after.json` field-for-field on every semantic field (chunk handler,
`extraction_failed`, the 8 `(relative_path, sha256, size)` file tuples, the single `unpublished-entry`
gap, the unpublished entry, the diagnostics `__typename__` set, coverage, published bytes, selection
and subject pin). The independent `sasquatch-v4be -be` oracle agrees byte-for-byte with
`corpus/evidence/round-39/c1/K6/oracle.tsv` and `symlinks.tsv`, and `run.json` is internally consistent
including a byte-identical recovery of its recorded envelope digest from the committed receipt.
No falsifying discrepancy found.

Seat: leaf executor, no subagents. All reads read-only (git show/log/merge-base/cat-file only); writes
confined to this report and `w2/artifacts/R39W2ReproK6/`.

## 1. Frozen target and pins taken from the lane

| item | value |
| --- | --- |
| carrier | `corpus/evidence/round-39/c1/K6/carrier.sqsh` |
| carrier pin (`carriers.json` + `run.json` + `after.json.subject`) | `00152518a3902a1a13892ec4bfd280a258f162d8fdf77260ea2b41f4f482b25b` |
| carrier size | 15867 bytes |
| scratch copy sha256 | identical to the pin (`artifacts/R39W2ReproK6/carrier-pin.out`) |
| oracle.tsv | `5880a0dc7b7e669012245dddb376455d72525ff8a14f6d56c671f5226a651f81` (8 files) |
| symlinks.tsv | `e0a0a72f727218b2f8328daf72fcdef5b3923b6b7fb0574b0ab4cd79872f9a74` (1 in-tree, 2 escaping) |
| after.json at REV `6fdaf4f1` | `ab9b2df8d14d91f8032dca98c27ed362ffa71e9e2def81ec076d0d76d3640a30` (29752 B, one line) |
| freeze commit | `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`, committer time `2026-10-26 14:12:51 -0300` = `2026-10-26T17:12:51Z` |

The carrier, oracle, symlink table and `carriers.json` are byte-identical at the freeze and now
(`vcs-checks.out`); `git cat-file -e 8fcda41:…/K6/after.json` fails, i.e. the receipt did not exist at
the freeze and was first added by `6fdaf4f1`, a strict descendant of the freeze
(`git merge-base --is-ancestor` exit 0). `git log 8fcda41..HEAD -- <K6 carrier|oracle|symlinks|carriers.json>`
is empty.

## 2. Independent re-run (after arm)

```
S=/fast/scratch/hyaku/kaidoku-r39/R39W2ReproK6
cp <lane>/corpus/evidence/round-39/c1/K6/carrier.sqsh "$S/carrier.sqsh"   # sha256 == pin
cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output "$S/carrier.sqsh" "$S/extract" \
  > "$S/envelope.json" 2> "$S/rea.err"
```

exit 0, `rea.err` 0 bytes, fresh outdir `$S/extract`. Envelope kept as
`artifacts/R39W2ReproK6/repro-envelope.json` (26216 B, `sha256 e378d445…c0c377`).

Tool pins seen by my run, matching `run.json` and the frozen rule:

- rea-agents `6.5.0` (`npx -y rea-agents@6.5.0 --version` → `6.5.0`; package root
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, version 6.5.0)
- unblob `26.6.4`, both `~/.local/bin/unblob` (a symlink) and its target
  `~/.local/share/uv/tools/unblob/bin/unblob` = `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`
- sasquatch-v4be `~/.local/bin/sasquatch-v4be` = `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`,
  `unsquashfs version 4.5.1 (2022/03/17)`

## 3. Semantic comparison: re-run vs committed `after.json`

`artifacts/R39W2ReproK6/compare.py` (comparison keyed on the fields named in the assignment) →
`compare.out`:

```
MATCH  chunk handlers + extraction_failed: [["squashfs_v4_be", false, {"length":15867,"offset":0}, {"length":15867,"offset":0}]]
MATCH  files (relative_path, sha256, size): 8
MATCH  extraction_gaps (kind, relative_path): [["unpublished-entry","firmware.bin_extract/a/b/link-in"]]
MATCH  unpublished_entries (relative_path, link_target): [["firmware.bin_extract/a/b/link-in","../../etc/config.ini"]]
MATCH  diagnostics __typename__ set: ["MaliciousSymlinkRemoved"]
MATCH  diagnostics link/target basenames: [["MaliciousSymlinkRemoved","escape-deep","passwd"],["MaliciousSymlinkRemoved","outside","outside"]]
MATCH  coverage / published_bytes: ["partial", 28119]
MATCH  selection (sha256/len/offset)
MATCH  subject digest == carrier pin
MATCH  operation/provider/engine
MATCH  evidence_id recomputes (committed)   ev_d99acec37229d4bc431fb9ad517c6dff58e18e9419de9c4b7d5414b722693ee9
MATCH  evidence_id recomputes (repro)       ev_536542aa49dd45e4639d121b01108c95a6137a0a6b9a8019754598e0aef94a95
MATCH  depth_limited_paths empty
VERDICT: ALL SEMANTIC FIELDS MATCH
```

A deeper normalized diff of the whole `raw_result` (recursively, after replacing the two runs'
staging roots and unblob's per-run `provider_blob_id`s) is **equal** (`raw_result equal after norm: True`),
and unblob's stdout text is equal modulo the staging root. The `__typename__` census of
`raw_result.report` is identical: `ChunkReport 1, FileMagicReport 9, HashReport 9,
MaliciousSymlinkRemoved 2, StatReport 20` — no `FailureReport`/`ErrorReport`.

Published tree of my run (`artifacts/R39W2ReproK6/repro-extract-files.tsv`) diffs clean against
`oracle.tsv` (`oracle-vs-repro-extract.diff` empty, exit 0); `published_bytes` 28119 = sum of oracle sizes.
`find extract -type l` in the published tree: 0 links (the in-tree link is an `unpublished-entry` gap,
the two escaping links are removed), so no escaping path is published — the receipt's
`escaping_ok`/`gaps_ok` shape is reproduced, not merely asserted.

Files are `firmware.bin_extract/<oracle relpath>` at `analysis_depth 1` with
`sha256 == reported_sha256 == oracle.tsv` for all 8.

## 4. Oracle cross-check (`sasquatch-v4be`, independent of REA/unblob)

```
cd "$S" && sasquatch-v4be -be -no-exit-code -f -d "$S/x" "$S/carrier.sqsh"   # exit 0
```

> `Reading a different endian SQUASHFS filesystem on …/carrier.sqsh` /
> `Trying to decompress using default xz decompressor…` / `Successfully decompressed with default xz decompressor`
> / `created 8 files / created 10 directories / created 3 symlinks`

- `sasquatch-files.tsv` vs `oracle.tsv`: **no diff** (`oracle-vs-sasquatch.diff` empty, exit 0).
- `sasquatch-symlinks.tsv` is exactly the symlink table: `a/b/link-in → ../../etc/config.ini`,
  `data/escape-deep → ../../../../etc/passwd`, `outside → ../outside` — the in-tree link is kept,
  and sasquatch removes nothing (removal of escaping links is unblob's job, which is what the receipt
  reports as `MaliciousSymlinkRemoved` on exactly those two links).
- Superblock read independently (`superblock.txt`): magic `sqsh`, big-endian fields → 21 inodes,
  block size 4096, **compression id 4 (XZ)**, major/minor 4/0 — the xz-leg/`squashfs_v4_be` claim holds
  for K6 itself, not only via handler naming. Running `sasquatch-v4be` *without* `-be` fails
  (`SquashFS version [1024.0] … different endianess`, `FATAL ERROR: File system corruption detected`),
  confirming the image is genuinely big-endian.
- Direct unblob (`unblob --extract-dir "$S/ub-extract" carrier.sqsh`, exit 0) shows the same tree:
  8 regular files + the one in-tree symlink; the two escaping links are absent. Its summary line
  `Extracted files: 9 / links: 1` therefore counts 8 files + the kept symlink — every non-directory
  entry is accounted for by the receipt's 8 published files plus its 1 gap.

## 5. `run.json` internal consistency

`artifacts/R39W2ReproK6/run-consistency.out`:

- **argv / outdir**: argv is `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output
  <lane>/…/K6/carrier.sqsh /fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K6-scratch/extract`; that path
  equals both `extraction_root` and the receipt's `parameters.output_directory`;
  `run_provenance_segment_ok: true` and the outdir does contain `/kaidoku-r39/`.
- **times**: `start_utc 2026-10-26T17:17:13Z`, `end_utc 2026-10-26T17:17:16Z`, `duration_ms 3905`.
  Freeze committer time is `17:12:51Z`, so the run starts 4 m 22 s after the freeze; the receipt's
  first-add commit `6fdaf4f1` is stamped `14:18:32 -0300` (17:18:32Z), i.e. after `end_utc`, and the
  file mtime (14:17) also precedes the commit. Second-resolution stamps are consistent with
  `duration_ms` (13.0 → 16.9 s truncates to 13/16).
- **envelope digest recovered byte-identically** (strongest single check in this seat): the harness
  writes `after.json` as `jq -c '.data'` of the `{ok,data,meta}` envelope (`tools/round-39/c1-run.sh`
  after arm). Re-serialising `{"ok":true,"data":<committed after.json>,"meta":{"command":"extract-firmware",
  "duration":"2527ms"}}` + `"\n"` yields exactly **29829 bytes with sha256
  `2aff645a7e0fecf549ce831e07f6a039c0c783cd6f6a992a11b800893e6cc85e`** — the digest and byte count
  recorded in `run.json.envelope`. So the recorded envelope digest, the recorded receipt digest
  (`ab9b2df8…`, verified against the committed bytes) and the committed receipt bytes are mutually
  bound: an edit to `after.json` after the run would break the envelope digest. The implied REA internal
  duration (2527 ms) is below the 3905 ms wall time, as expected under `npx` overhead.
- **pins**: `sasquatch_v4be.sha256 fac887…b7214c6` / version `4.5.1` match the binary on this host;
  unblob `env_value`/`command_env`/sha/version match the installed 26.6.4; `rea.package_root` is the
  6.5.0 package actually used; `child_path` contains `$HOME/.local/bin` (so `sasquatch-v4be` was
  reachable, the arm's precondition); `previous_after_json_sha256: null` (first add, consistent with
  the file being absent at the freeze).

## 6. Evidence-id recomputation (rea-agents 6.5.0 rule)

Reimplemented from `dist/domain/evidence.js`: `ev_` + sha256 of canonical JSON
(sorted keys, compact separators, non-ASCII unescaped) of `semanticProjection`, which hashes
`subject{digest,format,architecture}` (not `local_path`/`name`), provider, analysis_profile,
predicate_type, operation, parameters, raw_result, normalized_result, confidence, authority,
environment, limitations, relationship_coverage (when non-null), locations, evidence_links.

- committed receipt → `ev_d99acec37229d4bc431fb9ad517c6dff58e18e9419de9c4b7d5414b722693ee9` = stored id (**match**);
- my re-run → `ev_536542aa49dd45e4639d121b01108c95a6137a0a6b9a8019754598e0aef94a95` = its own stored id (**match**).

The two ids differ only because `parameters.output_directory` (hashed) names each run's own scratch
extract root; that is expected and is exactly the `run_provenance_ok` mechanism the claim discloses.

## 7. What differs between my run and the committed receipt (all non-semantic)

| difference | committed | my re-run | why it is not semantic |
| --- | --- | --- | --- |
| `provider_blob_id` / chunk `provider_id` | `3197140:1` | `701382:1` | unblob-assigned per-run blob id; appears in `derivations`/`chunks` only |
| REA staging root | `/fast/scratch/…/l1/c1runs/K6-scratch/rea-firmware-N2ZrFH` | `/tmp/rea-firmware-NFVNRF` | I did not export `TMPDIR=$S` for this run; every absolute path outside semantic fields, and normalisation makes `raw_result` equal |
| diagnostic `target` of `data/escape-deep` | `<staging>/etc/passwd` | `/tmp/etc/passwd` | same re-rooted escaping target under each run's own staging root |
| `files[].path`, `normalized_result.output_directory`, `parameters.{path,output_directory}` | lane carrier + L1 scratch | scratch carrier + seat scratch | absolute paths, and the reason the ids differ |

Nothing else differs: after replacing those roots/blob ids the entire `raw_result` and
`normalized_result` are equal.

## 8. Limits / inference

- A byte-identical semantic reproduction cannot distinguish a genuine receipt from one produced by a
  *different genuine run of the same frozen carrier with the same pinned tools* — those are the same
  observation, and the disclosed QUALITY-78 limit (a re-minted fabrication defeats receipt-only
  counters) is not narrowed further by this seat. What this seat does establish: the committed payload
  is reachable from the frozen carrier bytes with the pinned toolchain, and it is internally sealed by
  the envelope-digest recovery in §5. [INFERENCE] applies only to that residual equivalence argument.
- The envelope-duration `2527ms` recovered in §5 is derived, not recorded in `run.json` (only the wall
  `duration_ms` 3905 is); the recovery is exact because the digest matched at 29829 bytes, but the
  duration value itself is an inference from that match.
- `coverage: "partial"` with 1 gap on K6 is expected by the frozen rule (gaps exactly on in-tree
  symlinks, escaping links removed silently); it is disclosed in the receipt, not hidden. I make no
  judgement on the PROVINCE/README wording beyond the K6 receipt.
- I did not run `tools/round-39/c1-counter.py` (the author's instrument; score already recorded as
  `met_target` at `6fdaf4f1`), and did not modify, move or re-freeze any predicate, counter, carrier,
  oracle or table.

## 9. Artifacts (`.ufo/waves/round-39/w2/artifacts/R39W2ReproK6/`)

`compare.py`, `compare.out`, `repro-envelope.json` (my REA envelope), `repro-extract-files.tsv`,
`oracle-vs-repro-extract.diff` (empty), `sasquatch-extract.log`, `sasquatch-files.tsv`,
`sasquatch-symlinks.tsv`, `oracle-vs-sasquatch.diff` (empty), `unblob-direct.out`,
`superblock.txt`, `carrier-pin.out`, `run-consistency.out`, `vcs-checks.out`, `repro-command.txt`,
`extract-tree-symlinks.txt`.

Tooling: nothing installed or upgraded (only the already-cached `npx -y rea-agents@6.5.0` was invoked;
`~/.npm/_npx` cache untouched apart from reuse). Scratch
`/fast/scratch/hyaku/kaidoku-r39/R39W2ReproK6` was removed after the artifacts above were copied out.
