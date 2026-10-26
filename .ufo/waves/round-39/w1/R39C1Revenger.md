DEFECTS FOUND — the gap mechanism in the draft sentence is exactly right, but the classification sentence is wrong in three tested ways (absolute targets are re-rooted and kept, symlink loops are not removed, chained links are order-dependent). All claims below are from source lines and from 16 REA runs on development BE v4 images built in scratch; no K5/K6 image and no held-out carrier was built or run.

# R39C1Revenger — exact symlink rules of the R39-C1 predicate

Seat R39C1Revenger, round 39 wave 1. Lane base `a2f64e1da78afcf8cc39287106604dbcc270844c`. Normative predicate draft: `plans/round-39-claims.md` (R39-C1). Tools: unblob 26.6.4 (`~/.local/share/uv/tools/unblob`, Python 3.13.16), rea-agents 6.5.0 (`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), sasquatch / sasquatch-v4be 4.5.1 (`~/.local/bin`). Nothing installed or updated; no VCS command that mutates.

## 1. Verdict against the draft sentence

Draft sentence: *"a symlink whose target resolves inside the extraction root is kept as metadata and recorded as one `unpublished-entry` gap; a symlink that escapes is removed by unblob (`MaliciousSymlinkRemoved`) and recorded as no gap."*

| part of the sentence | verdict |
|---|---|
| kept → `unpublished_entries[]` entry + exactly one `unpublished-entry` gap, path not published | **CONFIRMED** (every kept case below) |
| escaped → removed, `MaliciousSymlinkRemoved`, **no** gap, not published | **CONFIRMED** (T2, T7, T9/T10 `A`, T11, T23 `s_dotdot`, T24 `sub/esc`) |
| "resolves inside the extraction root" | **INCOMPLETE**: the root is the *per-chunk* extract directory (`<staged-input>_extract`), not REA's output directory and not the unblob output root (K1 direct evidence); resolution is non-strict/lexical, so dangling in-tree targets are kept (T3, T12) |
| absolute targets | **WRONG IF READ POSIX-STYLE**: an absolute target is not escaping. unblob strips the leading `/` and re-roots it at the extraction dir, then applies the same containment test, and rewrites the link to a relative one (T1, T8, T12, T22, T23 `s_root`). Only absolute targets whose stripped path still climbs out (`/../…`, `/..`) are removed (T2, T23 `s_rootdotdot`) |
| loops | **WRONG**: unblob's loop branch (`extractor.py:58-65`) is dead on CPython 3.13 because `Path.resolve()` no longer raises `RuntimeError`; a 2-cycle is kept as metadata and rewritten to a self-link (T5: `l1 -> l1`, `l2 -> l1`, two gaps) |
| targets through other symlinks | **NOT A FUNCTION OF THE IMAGE ALONE**: the check runs against the on-disk tree while links are being rewritten, in directory-iteration order. The same literal value is kept when the escaping link it names is already deleted (T9/T10: `B -> A` kept, gap; `A -> ../outside.txt` removed) and removed when it is visited first (T11: `A -> Z` removed, no gap; `Z -> ../outside.txt` removed) |

So the replacement rule text must be three clauses plus one exclusion; §4 proposes it, §5 lists what the freeze must change.

## 2. Source chain, quoted with file:line

### 2.1 unblob 26.6.4 — the sanitiser (installed copy, byte-compared to the tag by peer R39SrcUnblobSymlink)

`.../site-packages/unblob/extractor.py`:

```
42: def is_recursive_link(path: Path) -> bool:
43:     try:
44:         path.resolve()
45:     except RuntimeError:
46:         return True
47:     return False
...
58:     if is_recursive_link(path):
59:         logger.error("Symlink loop identified, removing", path=path)
60:         error_report = MaliciousSymlinkRemoved(
61:             link=path.as_posix(), target=path.readlink().as_posix()
62:         )
63:         task_result.add_report(error_report)
64:         path.unlink()
...
67:     raw_target = os.readlink(path)
68:     if not raw_target:
69:         logger.error("Symlink with empty target, removing.")
70:         path.unlink()
71:         return path
...
73:     target = Path(raw_target)
74:     if target.is_absolute():
75:         target = Path(target.as_posix().lstrip("/"))
76:     else:
77:         target = path.resolve()
...
79:     safe = is_safe_path(outdir, target)
...
81:     if not safe:
82:         logger.error("Path traversal attempt through symlink, removing", target=target)
83:         error_report = MaliciousSymlinkRemoved(
84:             link=path.as_posix(), target=target.as_posix()
85:         )
86:         task_result.add_report(error_report)
87:         path.unlink()
88:     else:
89:         relative_target = os.path.relpath(outdir.joinpath(target), start=path.parent)
90:         path.unlink()
91:         path.symlink_to(relative_target)
92:     return path
```

`unblob/file_utils.py:34-39` — the containment predicate; component-wise, equality allowed, fully resolved on both sides:

```
34: def is_safe_path(basedir: Path, path: Path) -> bool:
35:     try:
36:         basedir.joinpath(path).resolve().relative_to(basedir.resolve())
37:     except ValueError:
38:         return False
39:     return True
```

`unblob/report.py:133-138` — the report is a WARNING, fields `link` and `target` (absolute staging path / raw-or-resolved target).

Call sites: `unblob/processing.py:447` (multi-file extraction dir), `:654` (skipped extraction dir), `:678` (every chunk's extraction dir), all `fix_extracted_directory(extract_dir, self.result)`. The reports therefore attach to the task that owns the chunk, not to the `ChunkReport`. `processing.py:746-748` `delete_empty_extract_dir` removes an extraction dir that ends up empty.

How "escaping" is decided, point by point:

- **basis** = the `extract_dir` of the chunk being processed (`<outputRoot>/<staged-input>_extract` under REA), not the output root. Decisive receipt: K1's `link-to-hello -> ../hello.txt` resolves to `<staging>/extracted/hello.txt`, one level *above* `firmware.bin_extract`, and is removed (`round-38/c1/K1/after.json` diagnostic `target` = `…/extracted/hello.txt`). T7 and T24 `sub/esc` reproduce it.
- **relative target** → `path.resolve()`: resolved against the link's own directory, non-strict (`strict=False` is the default, i.e. `os.path.realpath`), all symlinks still present expanded, missing components treated lexically. Absence never matters.
- **absolute target** → leading `/` stripped, then `outdir / stripped`, then the same containment test and a relative rewrite. This is a chroot-style re-root, not POSIX absolute resolution.
- **target through another symlink** → expanded by `path.resolve()`, i.e. it depends on which links still exist when this link is visited.
- **loop** → `Path.resolve()` returns the link itself under CPython 3.13.16 (probe below), so `is_recursive_link` returns False and the loop branch at 58-65 never runs.
- **empty target** → unlinked with no report; unreachable from a real writer (`os.symlink("")` fails, `ln -s ''` fails), so only a hand-crafted image can hit it.

Probe of the loop premise (scratch, unblob's own interpreter):

```
$ /home/vgpnk/.local/share/uv/tools/unblob/bin/python -c "...Path('loop/l1').resolve()..."
3.13.16 (main, Oct  9 2026, 15:23:36) [Clang 22.1.3]
l1 resolve= /fast/scratch/.../pythonprobe/loop/l1
self resolve= /fast/scratch/.../pythonprobe/loop/l1
```

### 2.2 rea-agents 6.5.0 — kept symlink → `unpublished_entries` + `unpublished-entry` gap

`dist/firmware/FirmwareProvider.js:238` runs unblob with `--extract-dir outputRoot`; `:260` inventories the staging root; `:261` publishes.

`dist/firmware/FirmwareFiles.js:122` `inventoryFirmwareOutput` walks the staging root with `lstat`; directories are descended, everything else becomes an entry:

```
179:                 kind: stat.isSymbolicLink()
180:                     ? "symlink"
181:                     : stat.isFile()
182:                         ? "file"
183:                         : "special",
184:                 linkTarget: stat.isSymbolicLink() ? await readlink(path) : null,
```

`dist/firmware/FirmwarePublication.js:66-75` — every non-regular entry is withheld and recorded:

```
66:         const unpublished = [];
68:         for (const entry of context.entries) {
69:             if (entry.kind !== "file") {
70:                 unpublished.push({
71:                     relative_path: entry.relativePath,
72:                     kind: entry.kind,
73:                     link_target: entry.linkTarget,
74:                 });
75:                 continue;
76:             }
```

`:103` `coverage: unpublished.length > 0 ? "partial" : …`; `:301-308` — one gap per entry:

```
301:         ...unpublished.map((entry) => ({
302:             kind: "unpublished-entry",
303:             input_path: `$output/${entry.relative_path}`,
...
305:             relative_path: entry.relative_path,
...
307:             continuation_id: continuation(GAP_CONTINUATIONS["unpublished-entry"]),
```

Schema: `dist/domain/firmware/firmwareAnalysis.js:84-91` (gap kind enum, `unpublished-entry` at `:90`), `:137-141` (`unpublished_entries[] = {relative_path, kind: "symlink"|"special", link_target}`).

The escaping case reaches REA as a *diagnostic*, never a gap: `MaliciousSymlinkRemoved` is not in the `known` report set (`FirmwareReports.js:65-74`) so `:254-255` pushes it, and `:420` counts any diagnostic as `partial`. `link_target` is the value **after** `fix_symlink` rewriting (absolute targets and in-tree chains are flattened), not the value stored in the image.

## 3. The rule as three testable sentences, tested

Test sentence A (in-tree relative): *a symlink whose target — resolved lexically against the link's own directory, non-strict, inside the chunk's extraction dir — lands at or below that dir is kept as metadata and becomes exactly one `unpublished-entry` gap; it is not published.*

Test sentence B (escaping relative): *a symlink whose such target lands strictly above that dir is deleted by unblob, reported as `MaliciousSymlinkRemoved` on the owning task (so a REA diagnostic, not a gap), and never published.*

Test sentence C (absolute): *a symlink whose raw target begins with `/` is judged as if the extraction dir were `/` (leading slash stripped): kept as metadata and rewritten to a relative link when the stripped path stays at or below the dir, deleted when the stripped path climbs out.*

Results (all images are standard BE v4 gzip built with `tools/round-37/gen-squashfs.py … --endian be` in scratch; one image, T21-T24, used my patched copy of the generator because the stock one drops symlink-to-directory entries — see §6). Envelope fields quoted from `data.normalized_result`; full envelopes in the artifacts dir.

| case | tree (targets) | image sha256 (short) | sentence | coverage | published files | `unpublished_entries` (kind:link_target) | gaps | diagnostics |
|---|---|---|---|---|---|---|---|---|
| T1 | `abs-in -> /hello.txt`, `hello.txt` | `20b32fd7…` | C | partial | `hello.txt` | `symlink:hello.txt` | 1 × `unpublished-entry@…/abs-in` | – |
| T2 | `abs-out -> /../etc/passwd`, `sub/abs-out2 -> /../../outside` | `b5aeeb34…` | C (escape) | partial | – | – | – | 2 × `MaliciousSymlinkRemoved` |
| T3 | `dang -> missing.txt` (dangling, in-tree) | `4d9965c3…` | A | partial | `x.txt` | `symlink:missing.txt` | 1 × `@…/dang` | – |
| T4 | `A -> bin/run.sh`, `B -> A`, `bin/run.sh` | `c909b6cb…` | A (chain) | partial | `bin/run.sh` | `symlink:bin/run.sh` ×2 | 2 | – |
| T5 | `l1 -> l2`, `l2 -> l1` (loop) | `e49b1271…` | **A (loop)** | partial | – | `symlink:l1`, `symlink:l1` | 2 | **none** |
| T6 | `dlink -> docs` (stock generator) | `fc945c44…` | generator limit | complete | `docs/readme.md` | – | – | – |
| T7 | `esc -> ../outside.txt` | `32969d3b…` | B | partial | `y.txt` | – | – | 1 × `MaliciousSymlinkRemoved` |
| T8 | `sub/abs -> /sub/x.txt` | `f5cd6f36…` | C | partial | `sub/x.txt` | `symlink:x.txt` | 1 × `@…/sub/abs` | – |
| T9 / T10 | `A -> ../outside.txt`, `B -> A` (two creation orders) | `c1c97f90…` (identical images) | **chain** | partial | `z.txt` | `symlink:A` | 1 × `@…/B` | 1 × removed (`A`) |
| T11 | `A -> Z`, `Z -> ../outside.txt` | `bdfd2a1b…` | **chain, other order** | partial | `w.txt` | – | **none** | 2 × removed (`A`,`Z`) |
| T12 | `absmissing -> /missing/x`, `dot`, `dotdot`, `absroot` (last three lost by stock generator) | `c83f9ddb…` | C (missing) | partial | `a.txt` | `symlink:missing/x` | 1 × `@…/absmissing` | – |
| T21 | `lib -> usr/lib` (dir, patched gen) | `5ad22fbd…` | A (dir target) | partial | `usr/lib/libfoo.so`, `x.txt` | `symlink:usr/lib` | 1 × `@…/lib` | – |
| T22 | `lib -> /usr/lib` (dir, absolute) | `c10e6826…` | C (dir target) | partial | `usr/lib/libfoo.so`, `x.txt` | `symlink:usr/lib` | 1 × `@…/lib` | – |
| T23 | `s_dot -> .`, `s_dotdot -> ..`, `s_root -> /`, `s_rootdotdot -> /..` | `44b348d1…` | C corner | partial | `k.txt` | `symlink:.`, `symlink:.` (`s_dot`,`s_root`) | 2 | 2 × removed (`s_dotdot`, `s_rootdotdot`) |
| T24 | `sub/up -> ..`, `sub/deep/two -> ../..`, `sub/esc -> ../../x` | `8137bc6c…` | A + B nested | partial | `k.txt`, `sub/deep/f.txt` | `symlink:..`, `symlink:../..` | 2 | 1 × removed (`sub/esc`) |

Each run command was exactly:

```
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output "$S/imgs/<T>.sqsh" "$S/envs/<T>"
```

All 16 runs exited 0, `ok: true`, every chunk `handler: "squashfs_v4_be"`, `extraction_failed: false`. Evidence ids and the machine-readable table: `artifacts/R39C1Revenger/summary.tsv`; envelopes `envs/T*.json`; images + `imgs.sha256`; raw unblob reports `unblob-reports/T{1,4,5,11,12}-report.json`.

Round-38 receipts re-read for the same rule: K1 (`link-to-hello -> ../hello.txt`) → 0 gaps, 1 `MaliciousSymlinkRemoved`; K2 (`var/lib/run-link -> ../../a/run.sh`) → 1 gap with `link_target` `../../a/run.sh`, 0 diagnostics; K3/K4 → complete. That is sentence A/B on committed pilots, and it matches every REA case tested here.

Corner facts observed, all consistent with the source:

- equality with the extraction dir is *safe* (`sub/up -> ..` kept, T24; `s_dot -> .` and `s_root -> /` kept, T23), because `relative_to` accepts the empty relative path.
- an absolute target that does not exist is still kept (`/missing/x` → gap, T12).
- in-tree chains are flattened in the recorded target: `B -> A`, `A -> bin/run.sh` yields `link_target: "bin/run.sh"` (T4); a kept loop's target is rewritten to itself (`l1 -> l1`, T5) — `upstream` link_target values are **not** the image's values.
- diagnostics never carry a `relative_path`; `link` is an absolute staging path, and `target` is the *stripped* form for absolute raw targets but the *resolved absolute* form for relative raw targets (T2 `../etc/passwd` vs T7 `…/extracted/outside.txt`). Do not parse `target` to classify.
- every escaping removal leaves `coverage: "partial"` even with zero gaps (T2, T7, T11). A gap-less partial envelope is therefore not a defect signal.
- the empty-target branch (`extractor.py:68-71`) unlinks silently with no report; `os.symlink("")` raises `FileNotFoundError` on this host, so no generator-based carrier can reach it.

## 4. Replacement text proposed for the freeze (P39-C1 rule + oracle definition)

Symlink rule (three sentences, same shape as the draft):

> a. A relative link target is resolved lexically (non-strict) against the link's own directory inside the per-chunk extraction directory; if the result is that directory or below it, the link is kept as metadata, recorded as one `unpublished-entry` gap, and not published.
> b. If that result is above the extraction directory, the link is deleted by unblob, appears only as a `MaliciousSymlinkRemoved` diagnostic on the owning task, and produces no gap and no published path.
> c. A raw target beginning with `/` is first re-rooted by stripping the leading `/` at the extraction directory and is then judged by (a)/(b); it is therefore in-tree whenever the stripped path does not climb above the directory.
> d. Links whose resolution passes through another symlink, and symlink loops, are outside this rule: the first is decided by directory-iteration order at sanitisation time, the second is kept (unblob's loop branch is dead on CPython 3.13).

Oracle `symlinks.tsv` classification must therefore be defined as: relative → lexical normalisation from the link's own directory inside the image root, in-tree iff it does not climb above the root (equality allowed, existence irrelevant); absolute → strip the leading `/`, normalise from the image root, same test. That is *not* the "resolved POSIX-style against the link's own directory" wording in the draft (which, read as POSIX, would call every absolute target escaping).

If the L1 prefers to keep the draft wording, then the six frozen carriers must contain **no absolute symlink targets** — because unblob keeps them and the draft oracle would demand no gap.

## 5. Divergences the freeze must absorb

1. **Absolute targets** — draft calls them escaping; observed: re-rooted, kept, gap (T1, T8, T12, T22, T23, T24-class). Predicate would fail on any carrier with `/bin/sh`-style links. Fix: wording §4c, or forbid absolute targets in K5/K6.
2. **Loops** — draft's parenthetical says escapes are the only removal; source has a loop branch, but it is dead under the pinned interpreter (probe in §2.1), so a loop is a *kept* entry with a gap (T5), not a removal. Any carrier with a loop silently violates "gaps exactly on the oracle's in-tree symlinks" if the oracle calls loops escaping. Fix: keep loops out of K5/K6 or classify them as in-tree/kept.
3. **Chains through symlinks are order-dependent** (T9/T10 vs T11): the same link value (`A -> Z`) is kept in one image and removed in another purely because of which sibling the sanitiser visits first. An independent oracle cannot predict this from the image. Fix: K5/K6 oracle must contain no link whose target paths through another symlink (state this as a build constraint); otherwise the predicate is not decidable from the oracle.
4. **"extraction root"** should say *per-chunk extraction directory* (`<staged-input>_extract`), otherwise K1's `../hello.txt` (inside the unblob output root, outside the chunk dir, removed) contradicts the sentence.
5. **Recorded `link_target` is post-sanitisation**, not the image target. P39-C1 as drafted compares gap paths only, so it is safe today; if the counter ever compares `link_target`, it must compare the rewritten form (absolute → re-rooted relative; chain → flattened; loop → self).
6. **K1/K2 need a `symlinks.tsv` too.** They already carry symlinks (K1 escaping, K2 in-tree) while the round-37 dirs hold only `oracle.tsv`; the freeze's "per carrier" wording must cover K1/K2, or the predicate's "exactly on the frozen oracle's in-tree symlinks" is unmeasurable for them.

## 6. Carrier-build guidance for K5/K6 (tested generator hazards)

`tools/round-37/gen-squashfs.py` classifies by `os.walk`, which follows symlinks for its directory list, so a symlink whose target **exists as a directory on the build host** is turned into a DIR inode and silently lost: `L -> docs` (T16), `L -> .` (T13), `L -> ..` (T14), `L -> /` (T15), `L -> /etc` (T20) all vanish from the image (T13/T14/T15 and T16/T20 produced byte-identical images; `sasquatch-v4be -ll` shows no `L`). This is host-dependent, so `/bin/sh` (file) survives but `/usr/lib` (dir) does not. My patched copy `artifacts/R39C1Revenger/gen-squashfs-symlinkdir.py` reclassifies symlinked dnames as `TYPE_SYMLINK` and reproduces dir-target links (T21 `lib -> usr/lib`, T22 `lib -> /usr/lib`, T23/T24). Empty targets cannot be created at all.

Recommended K5/K6 symlink inventory (each is independently classifiable): one nested in-tree relative (`../..`-style), one dangling in-tree, one absolute in-tree, one absolute-nested in-tree, one escaping relative, one escaping absolute (`/../x`); optionally one symlink-to-directory built with the patched generator. Exclude loops and any link targeted through another symlink.

## 7. Reproduce

```
S=/fast/scratch/hyaku/kaidoku-r39/R39C1Revenger   # removed at the end of the wave
python3 tools/round-37/gen-squashfs.py $S/trees/T1 $S/imgs/T1.sqsh --endian be --comp gzip
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output $S/imgs/T1.sqsh $S/envs/T1     # exit 0
```

Artifacts (`.ufo/waves/round-39/w1/artifacts/R39C1Revenger/`): `summary.tsv`, `envs/T{1..12,21..24}.json`, `imgs/*.sqsh`, `imgs.sha256`, `unblob-reports/T{1,4,5,11,12}-report.json`, `trees.txt` (tree layout of every case), `gen-squashfs-symlinkdir.py` (patched generator used for T21-T24).

## 8. Limits

- All carrier evidence here is development images on this host. K5/K6 were not built, not read, and never run through REA (held-out discipline); the round-38 K1-K4 receipts were re-read only.
- Symlink-to-directory, loop, and chain outcomes are observed on this kernel/filesystem; the directory-iteration order that decides chains is not specified by unblob, so T9/T11 show the *possibility* of both verdicts, not a portable guarantee.
- `special` entries (fifo/device) take the same REA path (`kind: "special"` → `unpublished-entry`) by source reading only; the generator cannot write them. [INFERENCE]
- The empty-target branch is source-only (unreachable via a real writer on this host). [INFERENCE] that only a hand-crafted image can exercise it.
- No tools installed or updated; `npx -y rea-agents@6.5.0` resolved the existing cache at `~/.npm/_npx/ad9a3fdbcad992c6` (version printed from its package.json). Scratch `/fast/scratch/hyaku/kaidoku-r39/R39C1Revenger` deleted at the end.
