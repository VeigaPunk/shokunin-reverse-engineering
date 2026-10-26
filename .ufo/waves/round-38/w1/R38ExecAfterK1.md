# R38ExecAfterK1 — R38-C1 carrier K1 after-arm

Seat: `R38ExecAfterK1` (leaf executor). Assignment: produce the R38-C1 after-receipt for carrier K1,
run as `REA_UNBLOB_COMMAND=~/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json`,
with **sasquatch off PATH** on the stated premise that "stock unblob handles standard BE v4".
Milestone: round 38 build drafts and first falsifiers. Evidence below is measured, not inferred,
except where marked `[INFERENCE]`.

**Headline: the assignment's premise is false and the frozen predicate P38-C1 cannot be met as
written.** unblob 26.6.4 has no in-process SquashFS extractor: `squashfs_v4_be` shells out to
`sasquatch-v4be`. With sasquatch off PATH the assigned command names the right handler but publishes
**0 files** and records one `missing-extractor-dependency` gap — so verification step (4) fails
(`extraction_gaps == []` is `false`, 0 of 5 oracle rows published). With `~/.local/bin` on PATH the
same carrier publishes **5/5 oracle files, 0 gaps**, and the frozen counter matches K1.
No counter, carrier, oracle or predicate was changed; the defect is reported.

## 1. Inputs and pins

| item | value |
|---|---|
| lane root | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| carrier | `corpus/evidence/round-37/c1/K1/carrier.sqsh`, 9 780 B |
| carrier sha256 (copied into scratch, measured twice: scratch copy and lane file) | `1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e` |
| pin in `.ufo/waves/round-38/c1/carriers.json` | `1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e` — **match** |
| bytes | first 4 = `73 71 73 68` (`sqsh`, BE magic at offset 0); `file`: "Squashfs filesystem, big endian, version 4.0, zlib compressed, 9780 bytes, 11 inodes, blocksize: 4096" |
| oracle | `corpus/evidence/round-37/c1/K1/oracle.tsv`, 407 B, 5 regular-file rows (`bin/run`, `docs/deep/nested/file.dat`, `docs/readme.md`, `empty`, `hello.txt`) |
| toolchain | rea-agents 6.5.0 (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), unblob 26.6.4 (`~/.local/bin/unblob`), engine sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` |

Note for the claim text: the freeze calls K1/K2 "synthetic standard-BE v4 **gzip** images". Measured,
the carrier is a bare BE v4 SquashFS at offset 0 whose blocks are **zlib** compressed — there is no
gzip container around it. Mislabel only; it does not change the carrier bytes or the pin.

## 2. Arms run (exact commands, exit codes, timestamps)

Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38ExecAfterK1`, `export TMPDIR=$S`.
Sanitized PATH for the assigned arm:
`/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/sbin`
(`~/.local/bin` excluded; verified `command -v sasquatch-v4be` → absent, `command -v sasquatch` → absent,
`command -v node`/`npx` → present).

### 2a. Assigned arm (sasquatch off PATH)

```
env PATH=<sanitized> REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json \
  "$S/in/carrier.sqsh" "$S/out-k1" > "$S/envelope.json"
```

| run | start | end | exit | result |
|---|---|---|---|---|
| outdir pre-created (`mkdir -p` first) | 2026-10-26T03:17:22-03:00 | 03:17:22 | **1** | `execution_failure`, `details.provider_id=unblob`, `diagnostics.reason = "Extraction output root already exists"` |
| fresh outdir (no pre-create) | 2026-10-26T03:17:38-03:00 | 03:17:40-03:00 | 0 | envelope written, 7 934 B |

Assigned envelope (`after.json`), measured fields:

- `evidence_id` `ev_fd9baf661461b8d7923896c1d58309eb07d828f5f48ebe27c6930e801bc3b218`
- `subject.digest.sha256` = carrier pin ✓, `subject.name` `carrier.sqsh`
- `operation` `extract_firmware`, `provider` `unblob` 26.6.4
- `normalized_result.chunks[].handler` = `["squashfs_v4_be"]` ✓ (step 4, handler check passes)
- `normalized_result.files` = **0**, `published_bytes` = 0, `coverage` = `partial`
- `normalized_result.extraction_gaps` = **1 entry**:
  `kind=missing-extractor-dependency`, `handler=squashfs_v4_be`, `dependencies=["sasquatch-v4be"]`,
  `range={offset:0,length:9780}`, `input_path=$input`
- `diagnostics` = `ExtractorDependencyNotFoundReport` `{severity:ERROR, dependencies:["sasquatch-v4be"]}`

**Verification step (4) outcome: FAILS on two of three clauses.** handler ✓; `extraction_gaps == []` ✗
(1 gap); "every oracle row appears in `normalized_result.files`" ✗ (0 of 5).

### 2b. Frozen harness `tools/round-38/c1-run.sh after` (same sanitized PATH)

```
bash tools/round-38/c1-run.sh after "$S/in/carrier.sqsh" "$S/harness-out" "$S/harness-scratch"
```
start 2026-10-26T03:18:04-03:00, end 03:18:07-03:00, **exit 1**, stdout = the same
`execution_failure` envelope (`Extraction output root already exists`), stderr empty.

Cause is in the harness itself: its `after` branch does `mkdir -p "$OUT"` before calling REA, and the
REA unblob provider refuses an existing output root. **As committed, `c1-run.sh after` cannot produce
an after-receipt for any carrier.** Reproduced independently twice (2a row 1 and 2b).

### 2c. Diagnostic arm (sasquatch-v4be resolvable) — same command, only PATH differs

PATH prefixed with `$HOME/.local/bin` (`command -v sasquatch-v4be` →
`/home/vgpnk/.local/bin/sasquatch-v4be`), fresh outdir.
start 2026-10-26T03:18:20-03:00, end 03:18:23-03:00, **exit 0**, envelope 18 928 B.

- `evidence_id` `ev_5353626b369930076388d2e02e6833315fc41095673fc52d539c882eed576686`
- handler `squashfs_v4_be` ✓, `extraction_gaps` **`[]`** ✓, `published_bytes` 9 656 (= 18+9000+609+0+29)
- `files` = 5, root `firmware.bin_extract/…` (REA stages the input as `firmware.bin`; oracle rows are suffixes, which is what the counter's `matched()` compares)
- extra diagnostic: `MaliciousSymlinkRemoved` WARNING — the carrier's `link-to-hello` symlink is dropped
  by unblob's sandbox (target resolves outside the extraction root). The oracle lists only regular
  files, so this is oracle-compatible.

| oracle row | sha256 | published `relative_path` | match |
|---|---|---|---|
| `bin/run` | `299001868f…a6a9cbba` | `firmware.bin_extract/bin/run` | ✓ |
| `docs/deep/nested/file.dat` | `b7e769c3ad…4cddfa21` | `firmware.bin_extract/docs/deep/nested/file.dat` | ✓ |
| `docs/readme.md` | `98f8c3bfbe…2dbdb742` | `firmware.bin_extract/docs/readme.md` | ✓ |
| `empty` | `e3b0c44298…7852b855` | `firmware.bin_extract/empty` | ✓ |
| `hello.txt` | `0da249108f…4d62951ff` | `firmware.bin_extract/hello.txt` | ✓ |

### 2d. Evidence-id recomputation (frozen rule, `tools/round-27/xpin-attribute.mjs`, `--pkg65 --pkg67` = rea-agents 6.5.0 root)

Both envelopes, wrapped as `{"data": <envelope>}`, exit 0, stored id == recomputed id and ends `both`:
`after.json` → `ev_fd9baf66…bc3b218`; diagnostic → `ev_5353626b…ed576686`. `after_evidence_id_ok` holds.

### 2e. Counter, measured on a throwaway fixture repo (both envelopes)

Fixture: `D=$(mktemp -d "$S/fx.c1.XXXX")`, `git -C "$D" init -q`, toplevel verified = `$D`; contents =
lane `carriers.json`, lane `K1/oracle.tsv`, lane `tools/round-27/xpin-attribute.mjs`, and
`corpus/evidence/round-38/c1/K1/after.json` (nothing else; K2–K4 absent). Counter invoked with
`--root $D --rev … --freeze … --pkg65 <rea-agents 6.5.0 root>`.

| `after.json` content | freeze / rev | counter exit | `carriers_matched` | K1 block |
|---|---|---|---|---|
| diagnostic (sasquatch on PATH) | `c067b982` / `c067b982` | 1 | **1** | `matched: true`, gaps_empty true, handler_ok true, subject_ok true, operation_ok true, evidence_id_ok true, oracle_hits 5 / oracle_files 5 |
| assigned (sasquatch off PATH) | `c067b982` / `90510ec3` | 1 | 0 | `matched: false`, `after_gaps_empty: false`, `after_oracle_hits: 0`, everything else true |

The counter file exercised in the table above is the **worktree** `tools/round-38/c1-counter.py`
(sha256 `f27f982bb4c8dbedb8b7ef1bcadad3bd02df8d2fb7af6a7f78a43ce3093e83fa`), which is **not** the frozen
bytes: `git -C <lane> show e059ca93…:tools/round-38/c1-counter.py` hashes
`a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` (see D5). Because another wave member
had already modified the counter, the fixture was re-run against the **frozen bytes** restored from git
(`c1-counter.frozen.py`, sha `a7a62b09…`), same fixture shape, fresh repo:

| `after.json` content | freeze / rev (frozen bytes) | counter exit | `carriers_matched` | K1 block |
|---|---|---|---|---|
| diagnostic (sasquatch on PATH) | `f741cf98` / `f741cf98` | 1 | **1** | `matched: true`, `after_gaps_empty: true`, `after_oracle_hits: 5`, `oracle_files: 5`, all other `after_*` true |
| assigned (sasquatch off PATH) | `f741cf98` / `4f3857db` | 1 | 0 | `matched: false`, `after_gaps_empty: false`, `after_oracle_hits: 0`, all other `after_*` true |

Both counter generations agree, so the verdict does not depend on the drift. `met_target` is false in
every fixture run only because the PROVINCE/knowledge/SOURCES/README bindings do not exist in the
fixture; the K1 per-carrier block is the measured subject. So: **the gap-free receipt is the only
receipt that scores K1; the assigned arm's receipt scores 0/5 oracle rows.**

## 3. Mechanism (why the premise is false)

Read from the installed unblob 26.6.4 (`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob`),
excerpts committed as `artifacts/R38ExecAfterK1/unblob-26.6.4-citations.txt`:

- `handlers/filesystem/squashfs.py:24-26` — `class SquashFSExtractor(Extractor): EXECUTABLE = "sasquatch"; V4BE_EXECUTABLE = "sasquatch-v4be"`.
- `…squashfs.py:38-48` — `(Endian.BIG, 4)` selects `V4BE_EXECUTABLE` and appends `-be` unless
  `header.bytes_used == header.mkfs_time` (the AVM heuristic). There is no in-process extractor branch.
- `…squashfs.py:527,553` — `squashfs_v4_le` **and** `squashfs_v4_be` both use `SquashFSExtractor(4, …)`;
  the same holds for v1–v3 in this file. **Every** SquashFS handler in 26.6.4 is external.
- `extractors/command.py:66-75` — exec `FileNotFoundError` → `ExtractorDependencyNotFoundReport(dependencies=…)`,
  i.e. "extractor not installed", which REA surfaces as the `missing-extractor-dependency` gap.
- `dependencies.py:18-34` — `shutil.which(command)` is the only installation probe, so availability is
  purely a `PATH` question.

Consequence `[INFERENCE]`: the round-37 probe whose extraction tree is committed at
`.ufo/waves/round-37/probes/rea/K1/firmware.bin_extract/` necessarily ran with `sasquatch-v4be`
resolvable (the L1 installed it into `~/.local/bin`, which is on the default PATH). The round-38 claim's
"corrected premise" — "stock unblob handles standard BE v4 … without any external extractor" — was read
off an ambient-PATH run, not off the toolchain. It does not hold when that directory is off PATH.

## 4. Artifacts written (all under `.ufo/waves/round-38/w1/artifacts/R38ExecAfterK1/`)

| file | bytes | sha256 | what |
|---|---|---|---|
| `after.json` | 7 934 | `a6a9694c96a20e907217d627dd12b6716a67e8f0c66f0763e8960ecd790ab7aa` | **byte-exact output of the assigned arm** (sasquatch off PATH; gap present, 0 files) |
| `after.sasquatch-on-path.json` | 18 928 | `3b8daf904d378f68723c2c463fbcc581cf79d1203293f054ed8a1cea55a8a480` | diagnostic envelope: 5/5 oracle, 0 gaps, `ev_5353626b…` |
| `after.repro.sasquatch-off-path.json` | 7 946 | `cb58fcf13b6164f14e3d7ef1ba378e8a0a6ed692cef6cd4b7838c5df9eff57ee` | second assigned-arm run (determinism check) |
| `after.repro.sasquatch-on-path.json` | 18 970 | `92edab9a3b1c666783be81046562054576b88842485d6ecd06eeed62fecccb4e` | second diagnostic run |
| `counter-fixture.K1-sasquatch-on-path.json` | 1 770 | `bff34e867988496301efa5c6c14a67f2f09c5b94a7c0aac5d3bce1156b933f22` | counter receipt, fixture rev `c067b982` |
| `counter-fixture.K1-sasquatch-off-path.json` | 1 775 | `d056b8d60dca944aca1bb01a344a0ae7d3dbea76f4f7e5183a1dca63c006190c` | counter receipt, fixture rev `90510ec3` |
| `counter-frozen-bytes.K1-sasquatch-on-path.json` | 1 784 | `7510e6b0b921c75990ca3005ef21f6fde502958b12f86a8429039747fbbedf67` | re-run with **frozen counter bytes** `a7a62b09…`, freeze/rev `f741cf98` |
| `counter-frozen-bytes.K1-sasquatch-off-path.json` | 1 787 | `2b3b94e3b5087049afedc3f9d1d37846d800b3d84d7abac1f8ae79b30959601e` | re-run with **frozen counter bytes**, freeze `f741cf98` / rev `4f3857db` |
| `harness-after.envelope.json` | 526 | `d78ab7f71697688851a93f47f5d3730bb64604909d0b95a8381f9b29795d2475` | `c1-run.sh after` output (exit 1) |
| `harness-after.stderr.txt` | 0 | `e3b0c442…7852b855` | harness stderr (empty) |
| `K1-oracle.tsv` | 407 | `0c993e7421338a8c08e311914f71e0ebf9fda2849931b4f544e3774c78f13aab` | oracle bytes used for matching |
| `summary.json` | 8 819 | `7ae2f3ee9366330b5b08c594eef53dc9e8323c2faff57ab5158e1b8a8db4312b` | machine-readable roll-up (commands, exits, timestamps, match table, citations) |
| `ENV-NOTE.md` | 822 | `0fe4f685bbfb9666bbd30afcae456a65051393efe914b7b268fb0d4fbab35fde` | **not written by this seat** — pre-existing L1 note (discovery via `R38CrossToolK1`) recording the same corrected premise and that the L1 regenerates receipts at integration; left untouched |
| `unblob-26.6.4-citations.txt` | — | `8da9b9dd8a799cc50a663716ea9483fcb90d13034f241f159de7e010932b4955` | source excerpts for §3 |

Nothing was written outside this directory and this report; `corpus/evidence/round-38/`, `PROVINCE.md`,
`SCORECARD.md`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/` untouched. No VCS mutation
(the fixture repo was `mktemp -d` under scratch and every git call named `-C "$D"`). Scratch removed
after the artifacts were copied.

## 5. Defects / mismatches for the L1 (reported, not repaired)

1. **D1 — the frozen predicate's toolchain clause is false (blocking for C1 as written).**
   P38-C1 requires "the committed REA extract-firmware after-receipt (run with stock unblob 26.6.4;
   **no external extractor dependency**)" and "carries no extraction gap". unblob 26.6.4's SquashFS
   handlers are external-only; a gap-free, oracle-publishing receipt is obtainable **only** with
   `sasquatch-v4be` resolvable (§2c/§2e). So the four receipts can satisfy the predicate's *observable*
   target while contradicting its *parenthetical*, and they cannot satisfy it with the parenthetical
   honoured. Either the parenthetical and the plans/round-38-claims.md "corrected premise" sentence are
   corrected before scoring, or C1 is an honest stop. This also invalidates the kill-rule control
   framing that assumed a stock-blob-only pipeline (CTL-C1-2's "wrong (LE) handler" arm is unaffected).
   **Corroboration:** the L1's own `ENV-NOTE.md` (already in this seat's artifact directory, discovery via
   `R38CrossToolK1`) reaches the same correction and states the L1 will regenerate both before and after
   receipts with explicit env control at integration. This seat arrived there independently by measuring
   the same carrier twice with only `PATH` differing, and adds the quantification the note asks for:
   sasquatch available → 5/5 oracle files, `0` gaps, `published_bytes` 9 656, counter `matched: true`;
   unavailable → `0` files, `1` `missing-extractor-dependency` gap, `matched: false`.
2. **D2 — `tools/round-38/c1-run.sh after` is unusable as committed.** It `mkdir -p`s `OUT` before
   invoking REA; REA's unblob provider rejects an existing output root, so every `after` invocation
   exits 1 with `execution_failure` (§2b, reproduced twice). Receipts must come from the direct CLI
   invocation unless the harness is changed — and the harness is named in the frozen claim, so changing
   it post-freeze is itself a disclosure item.
3. **D3 — receipts are not byte-reproducible across independent runs.** Two runs of the same arm on the
   same carrier produce identical `normalized_result` signatures (handler, file list + shas, gap list,
   `published_bytes`) but **different `evidence_id`**s, because the digest covers REA's per-run staging
   paths and provider blob ids (`rea-firmware-XXXXXX`, `provider_id` `1584821:1` vs `1769444:1`,
   `parameters.output_directory`, `raw_result.execution.args[]`). Stored-id-vs-recomputed-id is still
   true (that is what the counter checks), but (a) the committed envelope must be copied **byte-exact**
   (any normalisation of those paths breaks `after_evidence_id_ok`), and (b) the envelope embeds dead
   scratch paths after cleanup, so a verifier cannot re-copy the receipt's own staging tree. Relevant to
   carried defect R36-CL6 ("receipt identity = subject digest, not `local_path`"): the 6.5.0 xpin rule
   demonstrably digests more than the subject.
4. **D4 — claim-text mislabels (calibration).** K1's carrier is zlib-compressed inside, not "gzip"; the
   plan's K1/K2 description should read "synthetic standard-BE v4 (zlib) images". Also: the extraction
   root is `firmware.bin_extract/`, so every oracle comparison is a suffix match (already how
   `c1-counter.py matched()` works) — a receipt with a different staged name would still match, which is
   fine, but worth knowing when reading receipts.
5. **D5 — the frozen counter has already been rewritten in the worktree (not by this seat).**
   `git status` reports `M tools/round-38/c1-counter.py`; the worktree bytes hash
   `f27f982b…` against the frozen `a7a62b09…` (`e059ca93:tools/round-38/c1-counter.py`). The diff changes
   the predicate docstring to the corrected `sasquatch-v4be available` wording, adds a paired
   `before.json` arm per carrier (`before_present`, `before_oracle_hits`, `before_missing_extractor_gap`)
   and moves the per-carrier `ok` conjunction onto those. This is exactly the shape D1 implies, but it is
   a post-freeze change to frozen scoring tooling: reconciliation belongs to the L1 (§2e re-runs prove
   the K1 verdict is identical under both generations, so no measured value here depends on the drift).
   Anyone integrating receipts must read the counter **from the measured revision**, not the worktree.
6. **Advisory for K2** (`[INFERENCE]`, not measured here): K2's oracle has 3 regular-file rows and no
   symlink row, so unblob's `MaliciousSymlinkRemoved` behaviour will not by itself cost K2 oracle rows;
   its unicode/space-bearing name (`space name.txt`) and nested `var/lib/data.bin` are the rows to watch.

## 6. Bottom line for the L1

The assigned command, run exactly as instructed, **does not** produce a valid K1 after-receipt: it names
`squashfs_v4_be` but publishes nothing and declares `sasquatch-v4be` missing. The same carrier yields a
fully matching receipt (`5/5`, 0 gaps, counter `matched: true`) only when `sasquatch-v4be` is on PATH.
Both envelopes are committed as artifacts above, byte-exact, with recomputation-verified evidence ids,
so the L1 can choose the arm but cannot claim the "no external extractor dependency" premise.

Deliberate labelling: `after.json` holds the **assigned arm's** output (gap present, 0 files) rather
than the scoring one, because that is what the assignment's command produces; it must not be integrated
as the scoring receipt for K1. The scoring-shape envelope is `after.sasquatch-on-path.json`
(`ev_5353626b…`). Copy whichever is used **byte-exact** — normalising the embedded staging paths breaks
`after_evidence_id_ok` (D3). The L1's `ENV-NOTE.md` says the L1 regenerates its own receipts at
integration with explicit env control; if so, these two files are the cross-check, and both must agree
with the L1's regeneration at the level of handler, file list + sha256, gap count and `published_bytes`
(the `evidence_id` will differ per run by construction).
