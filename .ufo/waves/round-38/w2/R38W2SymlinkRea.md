# R38W2SymlinkRea — REA side of the K2 gap: the code path, and whether "no extraction gap" is unreachable

**Verdict: DEFECTS FOUND.** The mechanics the entry reports are exact and reproduce byte-for-byte
from a fresh run of the frozen carriers, but the entry's generalisation
`So "no extraction gap" is unreachable on any carrier with an in-tree symlink`
(`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md:40`) is **falsified as written
by the entry's own K1**: K1 contains a symlink (`link-to-hello -> ../hello.txt`, verified by direct
listing of the frozen carrier) and its committed after-receipt carries **zero** extraction gaps. The
sentence is true only with the qualifier the entry states one bullet earlier for K2 — target
*resolving inside* the extraction tree. Below: the code, the four-line rule, the experiment that
separates the two branches, and the calibrated rewording (advisory only; I edit nothing).

Axes walked: (a) code-path coverage for symlink → gap, (b) reachability prediction for the
first-freeze clause, (c) consistency with round 36, (d) calibration of the terms used
("in-tree", "extraction root", "gap-free", "published").

## 1. The code that turns an extracted symlink into an `unpublished-entry` gap

rea-agents 6.5.0 root: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
(canonical sources under `dist/`; the shipped CLI and MCP bundles carry the same inlined logic —
`dist/cli-runtime/cli.js:14034` (kind/linkTarget), `:14280-14286` (the gap map), `:14070` (the
continuation string); `dist/mcp/main-kBXHZ8S5.js:51133,51377-51382`).

**Step 1 — inventory of the private extraction tree** (`dist/firmware/FirmwareFiles.js:122-188`,
`inventoryFirmwareOutput`). Directories are traversed but never emitted as entries
(`FirmwareFiles.js:167-170`); everything else is emitted with a `kind`:

```js
kind: stat.isSymbolicLink()
    ? "symlink"
    : stat.isFile()
        ? "file"
        : "special",
linkTarget: stat.isSymbolicLink() ? await readlink(path) : null,
```
— `FirmwareFiles.js:179-184`. `lstat` only: the link is never followed
(`if (directoryStat.isSymbolicLink()) continue;` at `FirmwareFiles.js:137-140` for the pending
stack; the child `lstat` at `FirmwareFiles.js:158`). So a symlink is a **non-file entry carrying its
raw `readlink` target**.

**Step 2 — publication splits the inventory by `kind`** (`dist/firmware/FirmwarePublication.js`,
`publishFirmwareExtraction`, called with these entries from `FirmwareProvider.js:260-261`). The
condition, verbatim (`FirmwarePublication.js:69-74`):

```js
for (const entry of context.entries) {
    if (entry.kind !== "file") {
        unpublished.push({
            relative_path: entry.relativePath,
            kind: entry.kind,
            link_target: entry.linkTarget,
        });
        continue;
    }
```

**Step 3 — every `unpublished` row becomes exactly one gap**, with no filter, no dedup, no
per-kind exception (`FirmwarePublication.js:301-308`):

```js
...unpublished.map((entry) => ({
    kind: "unpublished-entry",
    input_path: `$output/${entry.relativePath}`,
    ...emptyGap,
    relative_path: entry.relativePath,
    dependencies: [],
    continuation_id: continuation(GAP_CONTINUATIONS["unpublished-entry"]),
})),
```

The continuation is a fixed string (`FirmwarePublication.js:18`)
`"The entry is retained as metadata; only regular files are published, without executable permission bits."`,
interned as `sha256(instruction)` (`FirmwarePublication.js:216`), which is why the id is a constant —
`602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca` in the round-36 receipts, the
round-38 K2 receipt and every fixture I built. Schema: `kind` enum includes `unpublished-entry`
(`dist/domain/firmware/firmwareAnalysis.js:84-91`); the metadata rows are `unpublished_entries`
(`:137`).

Coverage is forced off `complete` as soon as one such entry exists
(`FirmwarePublication.js:103`): `coverage: unpublished.length > 0 ? "partial" : context.normalized.coverage`.

So the REA rule is one line wide: **`kind !== "file"` ⇒ unpublished ⇒ gap**. There is no path by
which a symlink that is present in the extracted tree is published, dropped, or reported without a
gap.

## 2. What it does with the files it does publish

- Consistency gate before writing: every regular file the provider reported must exist in the
  materialized output, else `AnalysisOutputError("extract_firmware", "Reported regular file is
  absent from materialized output: …")` (`FirmwarePublication.js:61-63`).
- Per file: `sha256` recomputed from the extracted bytes (`:79`) and cross-checked against the
  provider report's digest and size; disagreement throws `Extracted bytes disagree with provider
  report` (`:80-85`).
- Write is atomic and verified: `tree.write(entry.relativePath, createReadStream(entry.path),
  { sha256, bytes: entry.size }, signal)` (`:86`), which creates with
  `O_CREAT|O_EXCL|O_WRONLY|O_NOFOLLOW`, **mode `0o600`** (`dist/artifacts/SafeOutputTree.js:119`),
  re-hashes the stream, rejects size/digest drift, `fsync`s, and re-reads the file to verify
  (`SafeOutputTree.js:120-155`).
- The published record is metadata-only, no mode/uid/gid/mtime/xattr: `relative_path`, `path`,
  `size`, `sha256`, `reported_sha256`, `mime_type`, `analysis_depth`, `runtime_address: null`,
  `original_file_range: null` (`FirmwarePublication.js:87-97`); `published_bytes` is their size sum.
- Whole-report commit is all-or-nothing; on failure the tree rolls back and a result is returned
  only if the tree already published (`FirmwarePublication.js:113-146`).

Measured consequence: a source member with mode `0755` arrives as `0600`
(`stat -c '%a' fxA-out/firmware.bin_extract/hello.txt` → `600`; `fxE-out/…/real.bin` → `600` from
`755`). The continuation's "without executable permission bits" is true but **understates** the
loss: the published set has no group/other read at all.

## 3. Which symlinks reach REA at all — unblob deletes some first

REA runs stock unblob 26.6.4 (`engine.executable_sha256 0ce7b624…1d09`, as in the receipts) and
inventories what unblob leaves on disk. Before that, unblob rewrites or deletes symlinks
per extraction task:

- `unblob/extractor.py:50-90` `fix_symlink`, called from `fix_extracted_directory(extract_dir, …)`
  (`processing.py:678`, i.e. **the per-chunk extraction directory**, not the whole output tree).
- `unblob/file_utils.py:34-39` `is_safe_path` = resolved target must stay under `basedir`.
- Removal branches: target outside `extract_dir`
  (`extractor.py:81-87`, logged `Path traversal attempt through symlink, removing` + a
  `MaliciousSymlinkRemoved` WARNING report); empty raw target (`extractor.py:67-71`, **no report**);
  symlink loop (`extractor.py:58-65`, guarded by `except RuntimeError`).
- Absolute targets are *rewritten*, not removed: leading `/` is stripped and the link is re-pointed
  relatively (`extractor.py:73-77,88-91`) — so `/etc/hostname` survives as `etc/hostname` and **does**
  produce a gap (measured, fxA).

Therefore the operative boundary is **`extract_dir` = `<output>/extracted/firmware.bin_extract`**.
K1's `../hello.txt` resolves to `<output>/extracted/hello.txt` — still inside REA's own output
directory, but outside the chunk directory — and is deleted. K1's committed receipt proves the
boundary: `MaliciousSymlinkRemoved` with `link …/extracted/firmware.bin_extract/link-to-hello`,
`target …/extracted/hello.txt`.

## 4. Prediction: can a carrier with an "in-tree symlink" satisfy "carries no extraction gap"?

Two readings, two answers:

**(a) "the image contains a symlink" — YES, it can be gap-free.** Every symlink unblob deletes never
reaches the inventory, so no entry, no gap. K1 is an existence proof inside the frozen carrier set
(below). Any claim whose clause is "carries no extraction gap" is therefore satisfiable by a
symlink-bearing carrier.

**(b) "the extraction retains a symlink" (non-empty target resolving inside `extract_dir`) — NO,
never.** It is a code-level guarantee, not a measured coincidence: the symlink is a `kind: "symlink"`
entry (`FirmwareFiles.js:179-184`), publication sends every non-file to `unpublished`
(`FirmwarePublication.js:69-74`), and every `unpublished` row becomes a gap
(`FirmwarePublication.js:302`). There is no counterexample to construct short of unblob deleting the
link — which is reading (a), not (b). `coverage` is simultaneously forced to `partial`
(`FirmwarePublication.js:103`), so such a carrier can be **neither** gap-free nor `complete`.

**Consequence for R38-C1 under the first freeze.** The frozen predicate requires, per carrier,
"carries no extraction gap" (`plans/round-38-claims.md` at `e059ca9`, Predicate P38-C1), scored as
`d['after_gaps_empty'] = gaps(env) == []` (`tools/round-38/c1-counter.py:178`, bound at `:189`). The
frozen K2 is defined as "synthetic standard-BE v4 gzip (tree2, **symlink** + unicode name)"
(`.ufo/waves/round-38/c1/carriers.json`), and its link target stays inside `extract_dir`, so K2
*fails that clause in every possible run*. The honest stop (`carriers_matched 3`, `met_target false`)
is forced by carrier + REA, not by a counter or predicate defect — no counter amendment can make K2
gap-free without changing the carrier or the clause.

## 5. Experiment — the two branches, on the frozen carriers and on fresh fixtures

Commands and exit codes: `artifacts/R38W2SymlinkRea/commands.txt`. Raw envelopes:
`artifacts/R38W2SymlinkRea/runs/{fxA,fxA-run2,fxB,fxC,fxD,fxE,kK1,kK2}-run.json`. Fixtures
(squashfs v4 LE gzip, 4 KiB blocks, `mksquashfs`, system 4.7.5) plus source manifests and digests:
`artifacts/R38W2SymlinkRea/fixtures/`.

| run | image symlinks | target resolves | `unpublished_entries` | `extraction_gaps` | exit |
|---|---|---|---|---|---|
| fxA | `dir/in-link -> ../hello.txt`, `abs-link -> /etc/hostname` | inside | 2 | **2 `unpublished-entry`** | 0 |
| fxA rerun (fresh outdir) | same | inside | 2 (same paths) | 2 (same paths) | 0 |
| fxB | `a-loop -> b-loop`, `b-loop -> a-loop` | loop, survives as `a-loop`/`a-loop` | 2 | 2 `unpublished-entry` | 0 |
| fxD | `dangling-link -> missing-file.txt` | inside, dangling | 1 | 1 `unpublished-entry` | 0 |
| fxE | `same-link -> real.bin` (same dir) | inside | 1 | 1 `unpublished-entry` | 0 |
| **fxC** | `sub/out-link -> ../../outside.txt` | **outside** `extract_dir` | **0** | **0** | 0 |
| **K1 rerun** (frozen carrier, sha256 `1cfb6c33…117e`) | `link-to-hello -> ../hello.txt` | **outside** `extract_dir` (inside REA output) | **0** | **0** | 0 |
| K2 rerun (frozen carrier, sha256 `403cb0a8…9154`) | `var/lib/run-link -> ../../a/run.sh` | inside | 1 | **1 `unpublished-entry`** | 0 |

K1's symlink is not inferred from the round-37 source tree: the frozen carrier itself lists it —
`sasquatch-v4be -be -ll corpus/evidence/round-37/c1/K1/carrier.sqsh` →
`lrwxrwxrwx vgpnk/vgpnk 12 … squashfs-root/link-to-hello -> ../hello.txt`.

**Reproduction fidelity.** Both frozen carriers were re-run from committed bytes; projecting
`coverage`, `files` (path/size/sha256), `unpublished_entries`, `extraction_gaps`
(kind/input_path/relative_path/handler/continuation_id), `published_bytes`, `chunks` and diagnostics
from my run and from `corpus/evidence/round-38/c1/K{1,2}/after.json` gives **IDENTICAL** for both
(script in the transcript; K1 `published_bytes 9656`, K2 `10283`, K1 one `MaliciousSymlinkRemoved`).
So "one `unpublished-entry` gap on every run" (entry line 37-38) is a property of the frozen bytes,
not of the attempt-1 receipt: four independent runs of that shape (K2, fxA, fxA2, and the sibling
fixtures) agree, with the same continuation id `602c674b…cfca`.

## 6. Agreement with the round-36 LE entry

`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:115-127` records
`unpublished_entries` as `{kind: "symlink", link_target: …}`, one `unpublished-entry` gap each with
`handler: null`, `dependencies: []` and the shared continuation id `602c674b…`, and states
"it does not make an image with symlinks gap-free" (`:126`) and "Not gap-free extraction" (`:188`).
That is the same mechanism and the same id, measured on LE AppImage carriers (K2/K3/K4 there). The
round-38 sentence "This is the same behaviour the round-36 LE entry recorded" is **supported** — with
the same missing qualifier: the round-36 K3/K4 also show that symlinks *retained* cost a gap, not
that any image containing a symlink does.

## 7. Divergences found (severity ordered)

| # | finding | evidence | status |
|---|---|---|---|
| D1 | Line 40's universal is false as written: K1 is a carrier with an in-tree symlink that carries **0** extraction gaps, on the lane's own frozen carrier + receipt | §5 K1 row; `runs/kK1-run.json`; committed `K1/after.json` | **FALSIFIED** (literal) |
| D2 | "points outside the extraction root" (line 35) hides the operative root. K1's target resolves *inside* REA's `output_directory` (`…/extracted/hello.txt`) and is still deleted, because unblob's root is the per-chunk dir `…/extracted/firmware.bin_extract` (`processing.py:678`, `extractor.py:79-87`) | K1 receipt diagnostic `MaliciousSymlinkRemoved.target`; fxC | wording defect (low) |
| D3 | "0 gaps" ≠ complete: K1's committed receipt is `coverage: "partial"` **with 0 gaps**, because any diagnostic (the `MaliciousSymlinkRemoved` WARNING) forces partial (`dist/firmware/FirmwareReports.js:419-425`) | `K1/after.json`; `kK1-run.json` | calibration hazard (low) |
| D4 | `unpublished-entry` is not symlink-specific: `kind` is `"symlink"` *or* `"special"` for every non-regular, non-directory entry (`FirmwareFiles.js:179-183`), and both take the same branch | code only; no carrier exercised `special` | [INFERENCE] scope note |
| D5 | The quoted continuation ("without executable permission bits") understates: published regular files are `0600`, i.e. no group/other access either (`SafeOutputTree.js:119`), so a `0755` member arrives `0600` | `stat` on fxA/fxE outputs | measured, low |
| D6 | unblob's loop-removal branch is dead on Python 3.13 (`is_recursive_link` catches `RuntimeError`; `extractor.py:42-47`, venv is 3.13.16), so loop symlinks survive as self-links and still yield gaps | fxB: both links present, rewritten to target `a-loop`, 2 gaps | effect measured; cause [INFERENCE] |
| — | "empty target symlink produces no gap" (`extractor.py:67-71` unlinks silently) is unreachable through SquashFS input: Linux/mksquashfs cannot create an empty link target | code path only, not exercised | [INFERENCE], non-operative |

Everything else the entry asserts about the K2 gap is **CONFIRMED**: gap kind, `$output/…`
`input_path`, `handler: null`, `dependencies: []`, `relative_path` naming the link, the link kept as
`{kind: "symlink", link_target: "../../a/run.sh"}` metadata, continuation id `602c674b…cfca`, and
K2's 3/3 oracle files still published with `published_bytes 10283`.

**Recommended wording (advisory; I do not edit corpus/).** Replace lines 40-41 with the
conditional that the code actually proves, e.g.:

> So "no extraction gap" is unreachable on any carrier whose extraction retains a symlink: REA sends
> every non-regular entry to `unpublished_entries` and emits one `unpublished-entry` gap for each
> (`FirmwarePublication.js:69-74,302`). A symlink is only exempt when unblob deletes it first — its
> target resolves outside the per-chunk extraction directory (K1: `../hello.txt` leaves
> `…/extracted/firmware.bin_extract` for `…/extracted/hello.txt`, `extractor.py:79-87`) — which is
> why K1 is gap-free while K2 is not.

## 8. Limits

- Nothing here is a claim about BE-vs-LE handling of symlinks beyond what K1/K2 (BE) and my LE
  fixtures show; both handlers delegate to the same unblob `fix_symlink` + REA inventory.
- `special` entries (FIFO/device) are code-read only; no carrier carried one.
- I did not run the lane's counters or judges (not my seat); the counter lines quoted are read-only
  from `git show e059ca9391642d5b71b6662cabcbdce0d9308719:tools/round-38/c1-counter.py`.
- `mksquashfs`/`unsquashfs` 4.7.5 (system), unblob 26.6.4 (`~/.local/bin/unblob`, venv Python
  3.13.16), `sasquatch-v4be` 4.5.1 for the BE listing, `npx rea-agents@6.5.0` from the pre-existing
  npx cache `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`. **No installs or upgrades were performed**
  (no pacman, no uv/npx download), so there is nothing to record beyond this line.
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2SymlinkRea` was removed after the artefacts above
  were copied into the lane; nothing cited here lives only in scratch.
