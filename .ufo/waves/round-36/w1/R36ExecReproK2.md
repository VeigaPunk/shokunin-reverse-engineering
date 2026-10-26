# R36ExecReproK2 — independent reproduction of carrier K2 (round 36, wave 1)

Advisory executor. Independent re-run of R36-C1 carrier **K2** (`k2-le-gzip.sqsh`). No lane file other
than this report was written; all runs happened in scratch, which was removed at the end. Observation
date 2026-10-26. Everything below is observed output unless marked `[INFERENCE]`.

## Verdict

**K2 reproduces.** Every predicate-relevant field of the committed
`corpus/evidence/round-36/c1/K2/{after,before}.json` and `oracle.tsv` is independently regenerated here:

| predicate element (P36-C1) | committed | this reproduction | equal |
|---|---|---|---|
| carrier sha256 | `ce5bf60e…a2084f` | `ce5bf60e…a2084f` (lane fixture, 208896 B) | yes |
| oracle regular files | 4 | 4, `diff -u` vs `K2/oracle.tsv` → **rc 0, no output** | yes |
| after `normalized_result.files` (relative_path, sha256) | 4 | 4 | yes (set-equal, no additions/removals) |
| after oracle hits (counter `matched()` rule) | 4/4 | **4/4** | yes |
| after sasquatch extraction gap | none | none | yes |
| before `normalized_result.files` | 0 | 0 | yes |
| before oracle hits | 0/4 | **0/4** | yes |
| before sasquatch gap | `missing-extractor-dependency`, deps `["sasquatch"]` | same kind/handler/range/deps | yes |
| evidence id recompute (6.5.0 rule) | stored == recomputed for both receipts | stored == recomputed for my two receipts too | yes |
| evidence ids themselves | `ev_c939cd…` / `ev_7506d2…` | `ev_e86a12…` / `ev_5c216f…` | **differ by design — see §6, not counted** |

## 1. Carrier provenance (no download needed)

`corpus/evidence/round-36/c1/carriers.json` gives K2 as a **lane fixture**, not a URL:
`corpus/evidence/round-36/c1/fixtures/k2-le-gzip.sqsh`. Verified in place, read-only:

```
sha256sum …/fixtures/k2-le-gzip.sqsh
ce5bf60e765e9942c1d317cfdd201b8b072b61e546e8dbdb6f87d6fe36a2084f   # == carriers.json K2 sha256
stat -c '%s' → 208896                                              # == before-gap range length
dd skip=0 count=4 → hsqs                                           # bare image, offset 0
/usr/bin/unsquashfs -s → "Found a valid SQUASHFS 4:0 superblock … Compression gzip, Block size 4096,
   Number of inodes 12, Filesystem size 207803 bytes"
```

The superblock matches the frozen K2 description ("LE v4, gzip, 4 KiB blocks, nested dirs + symlink").
No fetch, no copy of the carrier was made.

## 2. Tool identity actually used

| tool | observed | note |
|---|---|---|
| REA | `npx -y rea-agents@6.5.0` → `--version` prints `6.5.0` | lane pin |
| unblob | 26.6.4, `normalized_result.engine.executable_sha256 = 0ce7b624…ba1d09`, path `~/.local/share/uv/tools/unblob/bin/unblob` | **identical string in committed receipts** |
| sasquatch | `~/.local/bin/sasquatch`, sha256 `ad02d27a…774754`, `unsquashfs version 4.5.1 (2022/03/17)` | **identical to committed `after-run.json`** |
| sasquatch-v4be | `~/.local/bin/sasquatch-v4be`, sha256 `fac88740…b7214c6`, same version string | present; irrelevant to LE (see §7) |
| oracle | `/usr/bin/unsquashfs` **4.7.5 (2026/03/01)** | == committed `oracle-run.json` version line |

## 3. Runs (exact commands, exit codes)

`S=/fast/scratch/hyaku/kaidoku-r36/R36ExecReproK2`, `C=<lane fixture>`, `TMPDIR=$S`.
`bp` = `$PATH` with every directory holding an executable `sasquatch` removed (only
`/home/vgpnk/.local/bin` qualified).

| # | command (abridged) | rc | wall |
|---|---|---|---|
| 1 | `REA_UNBLOB_COMMAND=~/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json "$C" "$S/after-out"` | **0** | 1.6 s |
| 2 | same, `PATH=$bp` → `"$S/before-out"` | **0** | 1.5 s |
| 3 | same as 2, `"$S/before2-out"` (determinism probe) | **0** | 1.5 s |
| 4 | same, `PATH=$S/nosq-bin:$ip` where `$S/nosq-bin` symlinks **all 96** other `~/.local/bin` entries except `sasquatch` (isolation probe) | **0** | 1.5 s |
| 5 | `/usr/bin/unsquashfs -no-progress -o 0 -d "$S/oracle-root" "$C"` + sha256 walk | **0** | — |
| 6 | `bash tools/round-36/c1-run.sh after "$C" "$S/harness-after" "$S/harness-scratch-a"` | **0** | — |
| 7 | `bash tools/round-36/c1-run.sh before "$C" "$S/harness-before" "$S/harness-scratch-b"` | **0** | — |

PATH filter evidence (the `sasquatch`-removal is real, not a bash-hash artefact):
`env PATH="$bp" sh -c 'command -v sasquatch || echo NONE'` → `NONE`;
`env PATH="$bp" python3 -I -c 'shutil.which("sasquatch")'` → `None`.

## 4. Oracle reproduction

My own `unsquashfs` walk (regular files only, symlinks excluded) produced byte-identical output to the
committed `K2/oracle.tsv`:

```
usr/lib/kaidoku/blocks.bin      76eaa72beec080e682b667795701938dbaeb4ee32777114f9471c502b9a72e87  200000
usr/lib/kaidoku/text.txt        2defc0b25de7e2c560c87ca2461b0e317dd5b889150323b2e718ba8c1c1ebb94   73890
usr/share/doc/NOTICE            70488b47ee9c7ab20d96e35558afd583adc3b5a3fd68574d83ed145e50342cc9      75
var/small.dat                   87d3d14a123c5a64139b050fe9c33188e1f484d6367d71a30c12fa21fdc9001f       6
diff -u <committed>/K2/oracle.tsv $S/oracle.tsv  →  rc 0, empty
```

Extracted tree also contains the frozen symlink `var/notice-link -> ../usr/share/doc/NOTICE`
(excluded from the oracle by rule; REA reports it as an `unpublished-entry` gap — consistent).

## 5. Receipt comparison against the committed pair

### 5a. Predicate-level (what the counter reads)

`after` (mine → committed):
- `files` = 4 → 4; `(relative_path, sha256)` sets **equal**; no record present in one only.
- Per-file `size`, `sha256`, `reported_sha256`, `mime_type`, `analysis_depth` **all equal**.
  Reported sha256 also equals the on-disk sha256 of every published file (`SAME` ×4), and equals the
  oracle rows.
- `chunks[0]`: `handler=squashfs_v4_le`, `range={0,208896}`, `extraction_failed` **false** (mine) — and
  committed has the same values (the `extraction_failed` leaf is not in the diff list, i.e. equal).
- gaps: one `unpublished-entry` for `firmware.bin_extract/var/notice-link`, `handler=null`,
  `dependencies=[]` — **fully equal including `input_path` and `continuation_id`
  (`602c674b…8cfca`)**.

`before` (mine → committed):
- `files` = 0 → 0.
- gaps: one `missing-extractor-dependency`, `handler=squashfs_v4_le`, `provider_id` differs (§6),
  `range`/`root_file_range` = `{0,208896}` equal, `dependencies=["sasquatch"]` equal,
  `relative_path=null`, `input_path=$input` equal, `continuation_id 4ca863d0…7a07a` **equal**.
- `chunks[0].extraction_failed` **true** → true.

Counter verdict reproduced by hand with the frozen rule
(`sha == fs and (fp == rel or fp.endswith('/' + rel))`): after **4/4**, before **0/4**;
`sasquatch_gap` false after, true before.

### 5b. Whole-envelope leaf diff (calibration of "what actually differs")

Recursive leaf-path diff, mine vs committed: **after 89 differing leaves, before 14**. Every one falls
in exactly three classes; nothing else differs (no file content, no gap kind/deps/range, no
`authority`/`confidence`/`limitations`/`environment`/`evidence_links`/`locations`, no
`version_execution`, no engine identity):

1. **Derived id** — `/evidence_id` (1 leaf each).
2. **Absolute paths** — `parameters.path`, `parameters.output_directory`,
   `subject.local_path`, `normalized_result.output_directory`, `normalized_result.files[*].path`,
   `raw_result.execution.args[7,9,11,12]`, every `raw_result.report[*]…path` (temp extraction dir
   `rea-firmware-XXXXXX`). Caused by different carrier path + different output dir.
3. **Run-scoped numeric ids** — `provider_id` / `blob_id` / `reports[3].id` of the form `NNNNNN:1`.

`subject.digest.sha256`, `subject.format`, `subject.architecture`, `subject.name` are equal.

## 6. Evidence-id difference — attributed, not counted

Frozen xpin tool (`tools/round-27/xpin-attribute.mjs --pkg65 …6.5.0 --pkg67 …6.5.0`, envelopes wrapped
as `{"data": …}` like the counter does):

| envelope | stored | recomputed 6.5.0 | recomputed 6.7.0 | parseEvidence 6.5.0 |
|---|---|---|---|---|
| committed after | `ev_c939cd…0c88f` | `ev_c939cd…0c88f` | same | accept |
| committed before | `ev_7506d2…67b3c` | `ev_7506d2…67b3c` | same | accept |
| my after | `ev_e86a12…73f5` | `ev_e86a12…73f5` | same | accept |
| my before | `ev_5c216f…e53` | `ev_5c216f…e53` | same | accept |

Both committed receipts and both of mine are **self-consistent** under the 6.5.0 rule (and 6.7.0). The
ids differ between mine and committed, and that difference is structural, not evidence drift:

- 6.5.0 `semanticProjection` (read from `rea-agents/dist/domain/evidence.js:156-180`) hashes
  `parameters`, **`raw_result` in full** and **`normalized_result` in full** — i.e. the output directory,
  the carrier path, the random `rea-firmware-XXXXXX` staging names and the run-scoped `NNNNNN:1` ids all
  feed the id. `subject.local_path`/`name` are *excluded* (only `digest`/`format`/`architecture`).
- Confirmed by controlled substitution on my own after envelope: changing only
  `subject.local_path` → id unchanged (`ev_e86a12…`); changing `parameters.output_directory` → id moves
  to `ev_aa3135…`; changing `output_directory` **and** `path` → `ev_bb949b…`. Neither substitution can
  reach the committed id, because the committed run's `raw_result`/`normalized_result` paths and
  `NNNNNN:1` ids are different too. (The two substituted variants then fail `parseEvidence` with
  `Evidence semantic identifier does not match its record`, as expected for a tampered record.)
- **Therefore the evidence-id mismatch between my receipts and the committed ones carries no
  information about the extraction and is not counted**, exactly as the seat brief states. It is not a
  defect: no two independent runs of this operation can share an id under this rule.

## 7. Isolation probes (what actually causes the before/after delta)

- **Third identical `before` run**: same gap kind/handler/deps/range, same `continuation_id`, but
  `provider_id` = `544469:1` (vs `531049:1` on run 2 and `244895:1` committed). `provider_id` is
  run-scoped and **non-deterministic**; the counter never compares it (`c1-counter.py` `sasquatch_gap()`
  and `matched()` read only kind/deps/relative_path/sha256). `[INFERENCE]` the number is a per-run
  unblob task/blob counter (same family as `blob_id`), not derived from content.
- **Isolation run**: with a mirror directory symlinking *all 96 other* `~/.local/bin` entries (including
  `sasquatch-v4be`) and only `sasquatch` withheld, the run still yields `files=0`,
  `extraction_failed=true` and `missing-extractor-dependency … dependencies=["sasquatch"]`. So the
  delta between run 1 and run 2 is caused by `sasquatch` alone, not by some other `~/.local/bin` tool.
  `/usr/bin/unsquashfs`, `/usr/bin/7z`, `/usr/bin/7za`, `/usr/bin/binwalk` were present in **both**
  runs, so unblob 26.6.4 does not fall back to any of them for `squashfs_v4_le`.
- Cross-check for `R36ScoutUnblobHandler`'s `[INFERENCE]` ("only `sasquatch` is ever spawned for LE,
  `sasquatch-v4be` is irrelevant"): in the isolation run `sasquatch-v4be` **was present** and the gap
  still named only `sasquatch`. Observed, and it matches `Command.get_dependencies → [self._executable]`.

## 8. Frozen harness reproduces the same receipts

`tools/round-36/c1-run.sh` (read-only use; OUTDIR and SCRATCH under my scratch) in both modes, rc 0:

- `after-run.json`: `sasquatch=/home/vgpnk/.local/bin/sasquatch`, `sasquatch_sha256=ad02d27a…774754`,
  `sasquatch_version=unsquashfs version 4.5.1 (2022/03/17)` — **identical to the committed
  `K2/after-run.json`** fields.
- `before-run.json`: `sasquatch=""`, `sasquatch_sha256=""` — identical shape to committed.
- `harness-after/after.json` `normalized_result.files` `(relative_path, sha256, size)` compared to
  `K2/after.json`: `diff` → **rc 0, identical**.
- gaps: `unpublished-entry` (after) / `missing-extractor-dependency` `["sasquatch"]` (before).

So the committed receipts are reproducible by the frozen harness from the lane fixture, without the
L1's scratch carrier copy.

## 9. Observations (none is a predicate defect; nothing repaired)

1. `provider_id` / `blob_id` / `reports[3].id` (`NNNNNN:1`) are run-scoped and differ on every run
   (`244895:1`, `531049:1`, `544469:1`, `555766:1`, `527806:1`, `348734:1` observed). Not compared by
   the counter; only affects the evidence id (see §6). Any future predicate that pins `provider_id`
   would be unsatisfiable.
2. Minor, harness-only fragility (did **not** affect any run here): `command -v` in an *already
   primed* interactive bash can report a hashed path that no longer exists on the filtered `PATH`
   (I saw this in my own session shell before switching to a fresh `sh -c` / `shutil.which`). The
   harness is unaffected because its `command -v` runs inside its own fresh bash process, and its two
   runs here behaved correctly (rc 0, correct gap). Recording it so nobody re-derives the before-run
   by hand in a primed shell and mistakes the stale hit for a filter failure.
3. `K2/after.json` and `K2/before.json` embed the L1 scratch paths
   (`…/kaidoku-r36/L1/carriers/k2-le-gzip.sqsh`, `…/c1-run.Xx3qPx/out`), which are dead today. Harmless
   for the counter (it never resolves them) but it means the receipts are not byte-reproducible, only
   semantically reproducible — which is exactly what §5/§6 measure.

## 10. Risks / limits

- I reproduced **K2 only**; K1/K3/K4 were not run by this seat. `carriers_matched == 4` therefore
  remains unverified by me.
- The oracle side used the **installed** `/usr/bin/unsquashfs 4.7.5`, same as the committed
  `oracle-run.json`; the frozen oracle is a byte artifact, so this is an independent re-derivation of
  the same tool, not of an independent implementation. `sasquatch` itself embeds unsquashfs 4.5.1 code;
  agreement between the two is therefore expected `[INFERENCE]`, and the oracle is not a fully
  independent extractor.
- The `.tsv` oracle excludes symlinks by construction; K2's symlink is therefore only observable
  through REA's `unpublished-entry` gap, which I verified but did not independently justify as correct
  behaviour.
- Run times (~1.5 s) are far below the harness `timeout 900`; no timing claim is made.
- I did not run `c1-counter.py` (its inputs are the committed receipts; running it is the L1 gate) and
  did not modify any counter, carrier, oracle or frozen predicate.

## 11. Tooling

No tool was installed, upgraded or removed by this seat. `RULES.md` was read; nothing was needed.
Used only pre-existing: `npx`-cached `rea-agents@6.5.0`, the L1-installed
`~/.local/bin/sasquatch` (+ `sasquatch-v4be`), the uv-tool `unblob` 26.6.4, system
`/usr/bin/unsquashfs` 4.7.5, `jq`, `node`, `python3` (stdlib). No pacman transaction, no service
restart, no VCS mutation (no git/jj call was made at all in the lane; the only lane reads were `read`
of fixture/receipt/counter/harness files and one `bash` invocation of the lane harness, which writes
only to my OUTDIR).

## 12. Scratch

`/fast/scratch/hyaku/kaidoku-r36/R36ExecReproK2` (carrier-side envelopes, wrapped xpin inputs,
extracted trees, mirror dir, harness OUTDIRs) was removed at the end of the seat; nothing cited above
lives outside the lane or inside `/tmp`. The numbers, hashes and diffs quoted here are transcribed from
that scratch before removal.
