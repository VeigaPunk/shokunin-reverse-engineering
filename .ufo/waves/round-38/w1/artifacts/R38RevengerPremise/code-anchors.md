# Code anchors for the round-37 "missing-extractor-dependency" premise

All paths are the installed bytes measured on 2026-10-26 (unblob 26.6.4 uv tool,
rea-agents 6.5.0 npx package). Line numbers are `grep -n` results from those exact files.

## 1. unblob 26.6.4 — `unblob/handlers/filesystem/squashfs.py`

`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`

```
25:    EXECUTABLE = "sasquatch"
26:    V4BE_EXECUTABLE = "sasquatch-v4be"
...
41:                executable = self.V4BE_EXECUTABLE
48:                    is_avm = header.bytes_used == header.mkfs_time
...
69:        return [self.EXECUTABLE, self.V4BE_EXECUTABLE]
...
513: class SquashFSv4BEHandler(SquashFSv4LEHandler):
527:    EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)
```

Consequences:
- BE v4 chunk identification is stock unblob (`SquashFSv4BEHandler`, magic `73 71 73 68`),
  but **extraction shells out to `sasquatch-v4be`** (`-be` unless the AVM heuristic
  `bytes_used == mkfs_time` matches, line 48).
- There is no in-process/Python SquashFS extractor in this release.

## 2. unblob 26.6.4 — `unblob/extractors/command.py`

```
52:            res = subprocess.run(
...
69:        except FileNotFoundError:
70:            error_report = ExtractorDependencyNotFoundReport(
71:                dependencies=self.get_dependencies()
...
101:    def get_dependencies(self) -> list[str]:
102:        return [self._executable]
```

Consequences:
- The extract command is spawned by bare name (`subprocess.run(list)` -> `execvp`), so the
  child resolves `sasquatch-v4be` through **PATH**.
- `FileNotFoundError` -> `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())`
  where `self` is the internally built `Command`, whose `get_dependencies()` returns a single
  name: `["sasquatch-v4be"]`. This is exactly the dependency list the round-37 record names.

## 3. rea-agents 6.5.0 — gap derivation and environment pass-through

`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/cli.js`

```
14397:  const variable = engine === "binwalk" ? "REA_BINWALK_COMMAND" : "REA_UNBLOB_COMMAND";
14443:  hostEnvironment: context.environment,          // child (unblob) inherits the caller env, incl. PATH
14606:  __typename__: z.literal("ExtractorDependencyNotFoundReport"),
14816:  const dependencies = dependencyNames(parsed.extraction_reports);
14823:  kind: dependencies === null ? "extractor-failure" : "missing-extractor-dependency"
15141:  if (processRun.exit_code === 1 && normalized.diagnostics.length === 0) throw ...
```

Consequences:
- REA does not set or sanitise `PATH` for the unblob child; it inherits the caller's PATH.
- `ExtractorDependencyNotFoundReport` inside a `ChunkReport`/`MultiFileReport`
  `extraction_reports` becomes `extraction_gaps[].kind = "missing-extractor-dependency"`
  with `dependencies` copied verbatim.
- A non-zero unblob exit is tolerated when a diagnostic exists, which is why the starved run
  still yields a normal envelope (`coverage: partial`, `published_bytes: 0`) instead of an
  error object.

## 4. Committed round-37 instrument — `tools/round-37/c1-run.sh` (at 77091b49)

```
41:path=$PATH
42:if [[ $mode == before ]]; then
43:  path=$(python3 -I -c 'import os,sys; print(":".join(d for d in sys.argv[1].split(":") if d and not os.access(os.path.join(d,"sasquatch"), os.X_OK) and not os.access(os.path.join(d,"sasquatch-v4be"), os.X_OK)))' "$PATH")
44:  if PATH=$path command -v sasquatch-v4be >/dev/null; then echo "sasquatch-v4be still on PATH" >&2; exit 2; fi
46:  command -v sasquatch-v4be >/dev/null || { echo "sasquatch-v4be not on PATH" >&2; exit 2; }
48:sq=$(PATH=$path command -v sasquatch-v4be || true)
```

Consequences:
- The committed round-37 `before` arm removes PATH **directories that hold the binaries**
  (not directories whose *names* match), and guards the result with `command -v`, exiting 2
  if the extractor would still resolve. The scrub was therefore effective.
- The `after` arm requires `sasquatch-v4be` to resolve and records `sasquatch_v4be`,
  `sasquatch_v4be_sha256` and `sasquatch_v4be_version` in `<mode>-run.json` (line 55-58).
  The before-arm records an empty extractor field, i.e. the two arms are distinguishable.
