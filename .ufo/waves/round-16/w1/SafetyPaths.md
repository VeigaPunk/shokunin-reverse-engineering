# SafetyPaths — selection root/path joins and fixture isolation (r16 w1, sentinel)

Axes: depth, calibration. This was a read-only static review. I executed no checks. Tool installs/updates: **none**.

## Artifact status (calibration)

At review time none of these files existed: `round-16/selection.py`, `selfcheck.py`, `selection-fixtures.json`, or `negative-fixtures.json`. Three globs of `round-16/*.{py,json}` showed only claims, spec, dispatch, registration, result, and documentation-red. So no finding below is a code defect.

Each finding is a **contract-level defect or requirement**. It is grounded in two things:
- the wave spec text (`wave1-spec.json` items SelectorModel, SelectorRunner, NegativeFixtures, plus the shared contract on line 3);
- shipped source.

L1 or a reviewer must check each one against the code once that code lands. No pass is claimed.

## Source law for path resolution (verified anchors)

- `GoApiSnapshot.getApiSnapshotFile` builds `typeinfo/golang/%sgo%s.json%s` from `goVer.toString()`. It passes that path to `Application.getModuleDataFile`, and any `IOException` becomes `null`. Source: Base-src.zip `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`, method `getApiSnapshotFile`.
- `GoVer.toString()` returns `"%d.%d.%d"`. File names are therefore built only from parsed ints, never from the raw request text. `GoVer.parse` uses `Integer.parseInt`, so values above `2^31-1` give `INVALID`. Source: Base-src.zip `ghidra/app/util/bin/format/golang/GoVer.java`, `toString` and `parse`.
- `getModuleDataFile(String)` resolves only within the **calling module**, via `getMyModuleRootDirectory`, then `getDataFileInModule`. A directory hit throws `FileNotFoundException`, i.e. it is treated as absent. Source: Generic-src.zip `ghidra/framework/Application.java:354-373, 954-962`.
- `GModule.findModuleFile` probes, in priority order, `moduleRoot`, then `moduleRoot/build` if it exists, then the same-relative module in other app roots. Each probe uses `exists()`. Source: Utility-src.zip `ghidra/framework/GModule.java:61-66, 147-153`. `FileResource.exists/isDirectory` map to `java.io.File` (`generic/jar/FileResource.java:78-80, 139-141`).
- Installed tree checks:
  - `Ghidra/Features/Base/build` is absent.
  - The data dir has no non-regular, non-directory entries; the only directory is `patchverdiffs`.
  - All 123 diff names match `^go1\.[0-9]+\.[1-9][0-9]*\.json\.diff$`.
  - Per-minor counts: 1.15/16/17 = 15/15/13; 1.18/19/20 = 10/13/14; 1.21/22/23 = 13/12/12; 1.24 = 6; 1.25 = none.

  So treating the single `--root` as `Base/data/typeinfo/golang` is **faithful for this installation**. It is a modelling limit, not a defect, for multi-root, dev or `build/` layouts. In those layouts the base and the diff can come from different search roots. The output should say "single-root model" rather than imply it covers every layout.

## Findings

### F1 — Medium: fixture filenames can escape the temp tree (contract says "temp trees only; no live writes")

**Exploit path.** The fixture `files` field maps a relative filename to a JSON object. A runner doing `tmp / key` (or `os.path.join(tmp, key)`) has two failure modes:
- If the key is absolute, the temp root is discarded: `Path('/tmp/x') / '/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.22.0.json'` resolves to the live file.
- If the key contains `..` (e.g. `../go1.22.0.json`), the write lands outside the case root.

A typo or a hostile fixture would then overwrite or create files in the live installed data dir or the repo.

**Impact.** It silently breaks the contract's no-live-writes clause. It can also corrupt the same golang dir that `--root` previews, which falsifies later byte identities.

**Smallest remediation (runner).** Before writing:
1. Reject the key if `PurePosixPath(key).is_absolute()`.
2. Reject it if any part is `..`, `.`, or empty.
3. Check `(case_root / key).resolve().is_relative_to(case_root.resolve())`.
4. Only then call `mkdir(parents=True)` and write.

Any rejection is a fixture error (exit 1 with the case id), not a mismatch.

### F2 — Medium: cases must not share one temp root (isolation)

**Exploit path.** If cases are written sequentially into one tree, files from an earlier case stay visible to later ones. Examples:
- the "future diff ignored" case leaves `patchverdiffs/go1.22.5.json.diff`;
- the "missing base despite diff" case leaves a diff with no base.

A later exact-diff or lower-fallback case then picks up foreign files. Results depend on case order, and false passes or false fails become possible.

**Remediation.** Use one `tempfile.TemporaryDirectory()` per case, pass that directory as `root`, and do not reuse it. The SelectorRunner spec says "isolated temporary fixture roots"; check that this means per case.

### F3 — Low: basename normalization hides wrong-directory selection

**Evidence.** The SelectorRunner spec says "compare expected subset with path basename normalization for base/selected_diff". The source probes `go<M.m.0>.json` at the root and `patchverdiffs/go<M.m.p>.json.diff` in the subdir (`getPatchVerDiffFile` → `getApiSnapshotFile(patchVer, "patchverdiffs/", ".diff")`).

**Failure mode.** A selector that probes the diff at the root, or the base inside `patchverdiffs/`, returns the same basename. It would pass if a fixture placed a same-named decoy in the wrong directory.

**Calibration.** None of the nine planned cases (SelectorFixtures spec) contains such a decoy. Today the bug would surface as a status mismatch instead, so the risk is latent.

**Remediation (same cost).** Compare `PurePath(out_path).relative_to(case_root).as_posix()`, e.g. `patchverdiffs/go1.22.3.json.diff`. Optionally add one decoy case: a root-level `go1.22.3.json.diff` alongside an absent `patchverdiffs/` copy, which must not be selected.

### F4 — Medium: file names must be built from parsed ints, and the regex must be strict ASCII

**Evidence.** The source never puts raw request text into a path (`goVer.toString()` is `%d.%d.%d`).

**Failure modes.** In Python 3.14 (host `python3 --version` = 3.14.7):
- `re.match(r'^\d+\.\d+\.\d+$', s)` accepts a trailing `"\n"`, because `$` matches before a final newline.
- `\d` accepts non-ASCII digits, and `int()` accepts them too (e.g. `'٣'` → 3).
- Leading zeros (`1.22.03`) parse to 3, while a raw-text path would probe `go1.22.03.json`, which Java never probes.

If the raw request string is interpolated into `root / f"go{request}.json"`, these produce paths that differ from the source. They cannot traverse directories, because separators fail the regex.

**Remediation.**
- Use `re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', s, re.ASCII)`.
- Bound each component to at most `2**31-1` (matches `Integer.parseInt`) and exit 2 above that.
- Format names only as `f"go{M}.{m}.{p}.json"` from the ints. Labelling leading-zero rejection as a strict-parse deviation from the lenient `GoVer.parse` is a calibration matter for InvalidSemantics, not a path defect.

`goos` and `goarch` never enter a path in the source; they only form arch keys in `get`. The model must keep it that way.

### F5 — Medium: a literal per-patch probe loop is an unbounded-work hang

**Evidence.** `getPatchVerDiffFile` loops `while (patchVer.getPatch() > 0 && probe == null) patchVer = prevPatch()`, one file probe per patch value.

**Failure mode.** Python ints are unbounded. A request such as `1.22.99999999999` would make about 1e11 `stat` calls before the CLI emits anything. Java's own ceiling is about 2.1e9 probes, at `Integer.MAX_VALUE`.

**Remediation.** Apply the F4 bound, and also compute the same result from one `os.scandir(root/'patchverdiffs')`: the maximum `p` in `[1, request.patch]` whose entry exists and is not a directory. An entry counts **only if** `name == f"go{M}.{m}.{p}.json.diff"` after `int` round-trip. Otherwise a listing that uses `int()` would select decoys such as `go1.22.03.json.diff` or Unicode-digit names, which the Java probe can never hit. A missing `patchverdiffs/` behaves the same as no diff.

### F6 — Low: existence predicate parity and special files

**Source rule.** A file is found when `exists() && !isDirectory()` (Application.java:369-372). Symlinks are followed and broken links count as absent, the same as Python's `exists()`/`is_dir()`. EACCES during stat also means absent: Python 3.14 `Path.exists` delegates to `os.path.exists`, which returns `False` on any `OSError`. That matches `File.exists`.

**Divergence.**
- `Path.is_file()` treats a FIFO or device as absent, whereas Java selects it.
- A faithful `exists and not is_dir` followed by sha256 would block forever on a FIFO.

**Calibration.** The installed tree has no such entries (`find ! -type f ! -type d` returned none), so this only matters for an arbitrary `--root`.

**Remediation.** Use the source predicate for presence. Then, if `not stat.S_ISREG`, report the input as unreadable (exit 2) rather than hashing it.

### F7 — Low: wrong or unreadable root must not degrade into a source outcome

**Evidence.** Under source law a missing file means `getApiSnapshotFile` returns `null`, and `get` then returns `EMPTY`, which corresponds to `missing_base`. An untraversable `--root` also reads as "absent" through `os.path.exists` (F6). The NegativeFixtures spec requires "Keep invalid-input expectations distinct from source outcomes", and the contract says exit 2 means invalid/unreadable.

**Failure mode.** Without an explicit root check, a typo in `--root` produces exit 0 `missing_base`. That is a fabricated source outcome for an input error.

**Remediation.**
- If `not root.is_dir()` or `os.scandir(root)` raises, exit 2.
- An existing, readable directory with no base is `missing_base` (exit 0).
- NegativeFixtures' "wrong-root no base" case should state which of these two it means.

### F8 — Low: import by absolute spec, consistent with the r15 `-I` route

**Evidence.** The r15 route 1 notes that recorded execution used `python3 -I` with an absolute script path (`corpus/lessons/round-15-verifier-spotcheck.md:185`). Under `-I` the script dir is not on `sys.path`, so `import selection` fails; without `-I` it could resolve a different `selection` module.

**Remediation.**
- Load with `importlib.util.spec_from_file_location("kaidoku_r16_selection", Path(__file__).resolve().parent / "selection.py")`.
- Resolve the default `--fixtures` relative to `__file__`, not the CWD.
- Do not mutate `sys.path`.
- Record the exact recheck argv, including `-I`, wherever the command is documented.

## Non-defects (parity confirmed, no requirement invented)

- **Symlink following:** both Java `File` and Python follow symlinks; a symlinked base is hashed through its target in both.
- **`getApiFile` fallback:** `go%d.%d.json` exists in the source but is not on the `get` path. The contract already forbids it, so a decoy `go1.22.json` must be ignored.
- **Derived name `"go%s.json".formatted(goVer)`** in `getApiSnapshotJsonFile` is an FSRL cache name, not a filesystem read.
- **Memory:** loading a roughly 10 MB base JSON to compute `base_matching_buckets` is within the contract.

## Limits

- No selection, runner, or fixture code existed at review time, so F1–F8 are contract-level requirements awaiting checks against real code.
- Single-installation evidence only: ghidra_12.1.4, no build dir, single app root.
- No execution of target or source, and no live writes.
