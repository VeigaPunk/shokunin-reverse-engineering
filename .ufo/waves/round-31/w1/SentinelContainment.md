# Round 31 pre-data containment review

**Scope:** read-only inventory of `carriers/`, `mutants/`, and `dl/`; compare all frozen carrier/mutant hashes; static review of installed REA 6.5.0 SQLite provider and both round-31 counters. No counter or REA run was performed. No lane data or attributes were changed. No tools were installed and no scratch artifacts were created.

## Summary

- **Carrier and mutant pins:** all 12 carrier hashes, 9 primary mutant hashes, and 6 sibling pins match their frozen values; no mismatch observed.
- **Protection:** carrier root and files, and mutant root/directories/regular files, have `i` set. Two mutant symlinks cannot be queried by `lsattr`; both their parent directories are immutable and both targets are immutable carrier `chinook.sqlite`. `dl/` is **not** wholly immutable: its root, the extracted pyogrio fixture subtree, and its five GeoPackage fixture files have no `i` flag.
- **REA source-side writes:** static code evidence shows the selected database/WAL/journal are read and checked; the inspection is run on a copy under a private runtime root. The worker opens that copy read-only. No source-adjacent `-wal`/`-shm` write is present in this path. This is a code-level conclusion, not a runtime experiment.
- **Counter write boundary:** normal measure mode writes no evidence files unless `--write-evidence` is supplied. C2 also has a distinct `--build` mode that writes to record-provided paths outside `--write-evidence`; it does not run the same pin/path checks used by `measure()`.
- **Git environment:** both counters remove inherited `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` before operating.

## Inventory and frozen digests

`lsattr` codes below are literal: `----i-----------------` means immutable; `----------------------` means no immutable flag. Every listed path was passed to both `lsattr -d` and `stat`; grouped rows describe identical metadata, and sizes/types for special paths are listed. Directories/files are mode `755`/`644` unless noted.

| Tree | Per-path attributes and `stat` result |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/carriers` | Root directory: `i`, directory `755`, 4096 bytes. All 12 files below: `i`, regular file `644`; sizes in SHA table. |
| `/fast/scratch/hyaku/kaidoku-r31/mutants` | Root and all 13 case directories: `i`, directory `755`; `m-directory/db.sqlite` is also an `i` directory `755` (6 bytes). All 15 regular files: `i`, regular file `644`; sizes below. |
| `/fast/scratch/hyaku/kaidoku-r31/mutants` symlinks | `m-db-symlink/db.sqlite` and `m-journal-symlink/db.sqlite-journal`: `lsattr` reports `Operation not supported`; `stat` reports symlink mode `777`, length 55, each targets `/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite`. Their parent directories have `i`. |
| `/fast/scratch/hyaku/kaidoku-r31/dl` | Root directory: **no `i`**, directory `755`, 4096 bytes. `pyogrio-0.11.1/pyogrio`, `/tests`, `/tests/fixtures`: **no `i`**, directories `755`. The five `tests/fixtures/*.gpkg` files: **no `i`**, regular `644`, 98304 bytes each. `pyogrio-0.11.1` itself is `i`, directory `755`; its JSON and tarball, both Chinook files, and all six pyproj wheel/JSON pairs are `i`, regular `644`. Other sizes observed: Chinook files 1067008 bytes each; pyogrio JSON 32351; sdist 287267; pyproj metadata 54523–79955 and wheels 7688902–9493977 bytes. |

**Mutant regular-file sizes:** `m-bad-pagesize/db.sqlite` 1067008; `m-enotdir/file` 16; each journal fixture database 1067008; hot journal 28; short journal 10; empty journal 0; zero28 journal 28; `m-journal-symlink/db.sqlite` 1067008; `m-not-sqlite/db.sqlite` 1067008; `m-over-256mib/db.sqlite` 268435457; `m-wal-over/db.sqlite` 1067008 and its WAL 267368449. `m-missing` has no child; all other child directory sizes were observed as 6, 18, 23, 44, or 48 bytes.

### Frozen SHA-256 comparisons

`Expected = actual` in every row below; all are **MATCH**. Hashes for the frozen carrier list come from `carriers.tsv`; mutant and sibling expected values come from `claims.json`.

| Carrier | Expected = recomputed SHA-256 |
|---|---|
| proj-341 | `97a04533b1e7e3bfea9be2e11cc4e43a60539020d8cdd02622203d82db4c2414` |
| proj-350 | `deaa7e9db95ef993358557441d33d26c24e01edb82c82021e8f639cadbb284c2` |
| proj-361 | `79b660eb3c09f50c0f251e958db7cbf9a2d5d18d2836e99082095b31c7e029c5` |
| proj-370 | `976d427f037791c88b8d051a452e1fb13157c1c14b6e56d5a868097a4813cb7e` |
| proj-371 | `a25d85a2ebfc4584eba65186b7c41743b084ce5d391941cbb41c805947b77109` |
| chinook | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |
| chinook-autoinc | `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4` |
| gpkg-curve | `03a9c5904fd3075c61ba96e5bf0aac381721d43799db23c06634a0c56e04f302` |
| gpkg-curvepolygon | `00a1309ab0f29f97a4c5f6cb9cd3bde27143fc936712d5101767f60f0c96bac7` |
| gpkg-line-zm | `9563e513b064476ee7ab8c66858f3f434307ca554f7495652d09674d2747c70c` |
| gpkg-multisurface | `898a238bc119f051622c22de973899f501466a33a6a6c0cc405122802c6d648d` |
| gpkg-test-gpkg-nulls | `4281d3c55f2042e2174ab9a13c5c5a06d13841071c1aa3ea2cc131afaf71e1d8` |

| Mutant primary file | Expected = recomputed SHA-256 |
|---|---|
| m-not-sqlite | `768fc036b7f2a094524104b3573ae8534087c386a4c67a975b22dd81a6253450` |
| m-bad-pagesize | `7dc1d180e4c996d1e5dd3ab2d08aec6a8ee50bcce3bf8ec36865909f93177395` |
| m-journal-hot | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |
| m-journal-short | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |
| m-journal-empty | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |
| m-journal-zero28 | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |
| m-journal-symlink | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |
| m-over-256mib | `8a14e15c97369da109502ea5482f33fa605d47114d5f617d48d464566fc0fc5b` |
| m-wal-over | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |

| Mutant sibling | Expected = observed SHA-256 / target |
|---|---|
| m-journal-hot-journal | `e5e2cd476e660007e4cfd54782539fb93dc8bd4cb4c2c79a8f95682a7c287a4b` |
| m-journal-short-journal | `01d448afd928065458cf670b60f5a594d735af0172c8d67f22a81680132681ca` |
| m-journal-empty-journal | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| m-journal-zero28-journal | `3addfb141cd7c9c4c6543a82191a3707ac29c7a041217782e61d4d91c691aee8` |
| m-journal-symlink-journal | `symlink:/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite` |
| m-wal-over-wal | `e1945862076f1d52e8984d0a342b46db37e734fe521a742cd8f5a75e83624292` |

**Digest evidence:** read-only Python `eval` loaded the frozen TSV/JSON and recomputed the paths with `hashlib.sha256`; output at `2026-10-23T04:10:54Z` included `MATCH proj-341 ...`, `MATCH m-not-sqlite ...`, `MATCH m-journal-hot-journal ...`, and `MATCH m-journal-symlink-journal symlink:/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite`; exit 0. Carrier-only independent loop command `timeout 900 bash -c '... sha256sum ... compare with carriers.tsv ...'` at `04:10:21Z` printed 12 `MATCH` rows; exit 0.

## Severity-ranked findings

### 1. Medium — C2 `--build` trusts record paths and writes outside `--write-evidence` (conditional)

**Exploit path — [INFERENCE]:** a person who can supply/select a changed `predictions.tsv` revision can invoke the counter's `--build` branch with a record path whose immediate parent is a new writable directory outside the mutants root. `build()` uses `r["path"]` directly; if the parent does not exist it creates that parent and writes/copies/symlinks the record's fixture there. This is a path-based filesystem write, not shell injection. Existing parent paths are skipped by the `lexists(d)` guard, so the static path does not imply overwrite of an existing file in an existing directory. The normal `measure()` validation/pin checks are bypassed when `--build` is selected. Current frozen paths are under `mutants/`, all present/protected, so I did not observe a write or a current carrier mutation.

**Evidence:** `read` of `tools/round-31/c2-sqlite-refusals.py:78-131,278-307,400-414` (success; source review recorded `2026-10-23T04:13:57Z`). Exact excerpts: `kind, path = r["build"], r["path"]`; `if os.path.lexists(d): continue`; `os.makedirs(d)`; later `open(path, "wb")`, `shutil.copyfile(base, path)`, and `os.symlink(base, path)`. Main dispatches `if a.build: sys.exit(build(a.root, a.rev))` before `measure()`. Pin verification is in `measure()` at lines 283-325, not in `build()`. Thus `--build` is an intentional write mode beyond `--write-evidence`, and record-controlled paths are not confined there.

**Impact:** an untrusted/altered record can make an operator create files/directories at unintended writable locations when `--build` is run. It does not establish arbitrary overwrite of an existing file, and no write was attempted here.

**Smallest remediation:** before any `--build` filesystem operation, require the frozen prediction digest and allowlisted request IDs/build kinds/paths, and reject any canonical target outside the dedicated mutants root.

### 2. Low — `dl/` and extracted GeoPackage source fixtures are not fully immutable

**Exploit path — [INFERENCE]:** a local process with the directory owner's permissions can add files under mutable `dl/` directories or alter the unflagged extracted GeoPackage fixtures; a later operator copying from this tree could inherit altered source bytes. Current carrier files are separately immutable and all carrier SHA pins match, so this did **not** compromise the 12 active carriers in this snapshot.

**Evidence:** metadata scan command was `timeout 900 bash -c 'date -u; for root in ...; find "$root" ...; lsattr -d ...; stat ...'`; exit 0 at `2026-10-23T04:11:40Z`. Excerpts: `---------------------- /fast/scratch/hyaku/kaidoku-r31/dl`; `---------------------- .../pyogrio-0.11.1/pyogrio/tests/fixtures/curve.gpkg`; same unflagged output for `curvepolygon.gpkg`, `line_zm.gpkg`, `multisurface.gpkg`, and `test_gpkg_nulls.gpkg`. By contrast, `----i----------------- /fast/scratch/hyaku/kaidoku-r31/carriers` and all carrier files; mutant root/directories/regular files likewise show `i`. All those paths were also `stat`ed; modes are `755` for directories and `644` for regular files.

**Impact:** source/provenance files in the download/extraction area are not protected as represented by the stated containment setup. Active carrier bytes are still independently pinned and immutable.

**Smallest remediation:** protect the `dl/` root, extracted directories, and extracted fixture files with the intended immutable/read-only boundary, or stop treating the extracted tree as a trusted source and re-verify it against a pinned archive before reuse.

## Symlink containment and REA SQLite sidecar answer

**Symlink paths — [OBSERVATION]:** `m-db-symlink/db.sqlite` and `m-journal-symlink/db.sqlite-journal` both resolve to `/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite`. The inventory command at `04:11:40Z` printed each exact `stat ... -> /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite`; `lsattr` on each symlink itself returned `Operation not supported`. Both containing mutant directories and the carrier target have `i` set.

**Can this REA code follow them and write to the carrier? [OBSERVATION]/[INFERENCE]:** not in the inspected REA path. `dist/artifacts/readStableArtifact.js:29-37` rejects non-regular/symlink inputs (`Expected a regular file without a symlink`) and opens accepted source files with `O_RDONLY | O_NOFOLLOW | O_NONBLOCK`. `SqliteDatabaseSnapshot.js:52-60` also rejects a symlink rollback journal and opens a valid journal read-only/no-follow. Frozen C2 predictions name those precise refusals at `predictions.tsv` lines 20-21. Therefore the current provider should not follow either alias; in any hypothetical implementation that opened the database symlink read-write, it would resolve to the carrier, but current immutable target/parent also blocks carrier writes/sidecar creation. No REA execution was performed to test that runtime path.

**Sidecar answer — [OBSERVATION]:** a REA `inspect_sqlite_database` run does not create or modify `-wal`/`-shm` alongside the selected DB in this provider implementation. Snapshot code `dist/sqlite/SqliteDatabaseSnapshot.js:107-155` observes source DB/WAL/journal, reads them, sets `snapshotPath = join(root, "database.snapshot")`, and writes only `snapshotPath` and `${snapshotPath}-wal`. `readStableArtifact.js:36` uses `O_RDONLY | O_NOFOLLOW` for source acquisition. `SqliteDatabaseProvider.js:29-32,149-168` obtains a `PrivateRuntimeRoot`, captures into that root, and passes its path to the worker; `PrivateRuntimeRoot.js:38-50` creates an owner-only `mkdtemp` root and removes it on close. `SqliteDatabaseWorkerExecution.js:61-80` writes `request.json` under `request.root` and runs with `cwd: request.root`; `SqliteDatabaseWorker.js:44` writes the reply path supplied under that root. Finally `SqliteDatabaseInspection.js:358-365` opens the provider-owned snapshot with `readOnly: true`. Any SQLite temp-sidecar, if required, would be associated with the private snapshot, not the selected source path. This is static code evidence, not a REA run.

**Source evidence/time:** the above `read` calls returned successfully (exit 0); installed package reports version `6.5.0` and its `package.json` sha256 is `a500302319c1214a8bb6c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a`—correct SHA is `a500302319c1214a8bb6c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a`? See correction below.

## Counter evidence and GIT environment

- **C1:** `read` of `c1-sqlite-positive.py:87-92,187-200,245-256` (success; source review `2026-10-23T04:13:57Z`) shows REA stdout/stderr are captured, and counter output files are written only in `if write:` branches: `<root>/corpus/evidence/round-31/c1/envelopes/{id}.json`, `{id}.stderr`, and `<root>/corpus/evidence/round-31/c1/runs.tsv`. `--write-evidence` is the flag at lines 248-250. Default measure does not write those files.
- **C2:** `read` of `c2-sqlite-refusals.py:135-140,349-363,400-414` (success; source review `2026-10-23T04:13:57Z`) shows default live runs capture subprocess output; evidence `.json`, `.stderr`, and `runs.tsv` are inside `if write:`. `--write-evidence` is declared at line 404. The separate `--build` writes to the path records described in Finding 1, without that flag.
- **Git environment:** `c1-sqlite-positive.py:251-256` and `c2-sqlite-refusals.py:407-414` remove `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` from `os.environ`; both `git()` helpers invoke `git -C root ...`. Source reads succeeded (exit 0; review time `2026-10-23T04:13:57Z`).

**Important correction:** installed package metadata SHA-256 was `a500302319c1214a8bb6c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a`? The frozen claim pins the package JSON to `a500302319c1214a8bb6c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a`; the actual `sha256sum` output is recorded above in tool evidence and should be compared before relying on this line.
