# W2 schema authority review — `identify-flutter-build` (REA 6.5.0)

Seat: `KaidokuR22R.SchemaIdentifyFlutterBuild-6` (scout, leaf). This review checks the schema and source only. The target was not executed: no APK was passed to `identify-flutter-build` during this seat. Claim scope is author-side, not outside admission. Lane HEAD observed was `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`, and baseline `7787fea4…` resolves as a commit.

## Verdict

- **Observed:** the CLI schema is exactly one required string `path` with `minLength: 1` and `additionalProperties: false`. It has no command options.
- **Observed:** the CLI binds the operation `identify_flutter_build`. That is exactly what the R22-C1 counter derives through `verb.replace('-', '_')` in `.ufo/waves/round-21/tools/verb-coverage.py:85`. The mapping is consistent, and no special case is needed. Compare `list-objdump-architectures`, which does need one.
- **Observed:** the retained lane record `.ufo/waves/round-22/evidence/c1/identify-godot.evidence.json` binds. The raw `--full-output` envelope next to it is unevaluable to the counter, so extracting its `data` member is required. Probe output is shown below.
- **Calibration risk:** CLI `--schema` does **not** show the output schema, effects, or provider limits. Those come only from source or the MCP contract, as described below. Do not treat `--schema` as authority for effects or limits.

## Commands run (cwd `/tmp` unless noted)

| argv | exit | stdout (essential) | stderr |
|---|---|---|---|
| `npx -y rea-agents@6.5.0 identify-flutter-build --help` | 0 | `Usage: rea identify-flutter-build <path>`; `path  Local APK file to inspect`; global options only (`--filter-output --format <toon\|json\|yaml\|md\|jsonl> --full-output --help --llms --schema --token-count --token-limit --token-offset`) | none |
| `npx -y rea-agents@6.5.0 identify-flutter-build --schema` | 0 | TOON: `args: type: object; properties: path: {type: string, minLength: 1, description: Local APK file to inspect}; required[1]: path; additionalProperties: false` | none |
| `npx -y rea-agents@6.5.0 identify-flutter-build --schema --format json` | 0 | `{"args":{"type":"object","properties":{"path":{"type":"string","minLength":1,"description":"Local APK file to inspect"}},"required":["path"],"additionalProperties":false}}` (no `options`, no output schema) | none |
| `npx -y rea-agents@6.5.0 --version` | 0 | `6.5.0` | none |
| `npx -y rea-agents@6.5.0 identify-flutter-build --llms` | 0 | one-row manifest: `rea identify-flutter-build <path>` | none |
| `npx -y rea-agents@6.5.0 --llms-full` | 0 | 79524 bytes; section `# rea identify-flutter-build` lists only arg `path` (string, required) | none |

The npx cache resolved to `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, with version `6.5.0`. A separate `6.7.0` cache, `a1722018f28f9df2`, also exists and was **not** used. `incur` is version `0.6.1`. Node is `v24.21.0`.

Two helper shell commands failed without affecting any finding. A cache-directory `ls -d` glob exited 2. A `node -p require(...package.json)` loop hit `MODULE_NOT_FOUND` for npx cache directories without `rea-agents`.

### Bounded read-only bind probe (cwd lane root)

| argv | exit | stdout |
|---|---|---|
| `python3 -I -B .ufo/waves/round-21/tools/verb-coverage.py --evidence .ufo/waves/round-22/evidence/c1/identify-godot.evidence.json --verb identify-flutter-build --evidence-id ev_3458b996b71e3dccde0177728ba60ef94800dd373db5a704048e18526d9d866b` | 0 | `{"bound": true, "finding": "evidence_bound", "pathless": false}` |
| same with `--evidence …/identify-godot.envelope.json` | 2 | `{"bound": null, "error": "unsupported_evidence_representation", "finding": "evidence_unevaluable"}` |
| same evidence file, `--verb inspect-dart-aot` | 1 | `{"bound": false, "finding": "evidence_unbound"}` |

Retained file SHA-256 values:

- `identify-godot.evidence.json` `397aeeb7…834f`
- `identify-godot.envelope.json` `1ea324b2…5b0a`
- `identify-godot-run.json` `5c3d94f8…0e88`

The envelope keys are `data`, `meta`, and `ok` (`ok:true`), and `envelope.data == evidence` is `True`. The retained run argv is `npx -y rea-agents@6.5.0 identify-flutter-build <godot android_release.apk> --format json --full-output`, with exit 0.

## Source paths (rea-agents 6.5.0 dist)

Root: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`.

| File | SHA-256 | Role |
|---|---|---|
| `cli/flutterCommands.js` | `8354ba86…0da18` | CLI spec: `command: CLI_COMMANDS.identifyFlutterBuild` (`cliCommandNames.js:72` = `"identify-flutter-build"`), `argumentSchema z.object({path: z.string().min(1)})`, **`operation: "identify_flutter_build"`**, `toInput` identity. The run returns `settled.value` (Evidence) or `projectAnalysisError(...)`. |
| `application/flutter/FlutterBuildAnalysisService.js` | `57888f89…a754ba4` | `executeProviderOperation(..., flutterRequestSchema, provider, "observed")`, shared by CLI and MCP |
| `application/ProviderOperationExecution.js` | n/a | Re-parses `{operation, input}`. A failure becomes `AnalysisInputError`. Success becomes `createEvidence(subject, provider, {operation, parameters: input, result, rawResult, limitations, locations, confidence:"observed"})`. |
| `domain/flutter/flutterBuildAnalysis.js` | `c8cac805…5ddf2` | Domain input `z.strictObject({path: localPathStringSchema})` and the result schema |
| `domain/localPath.js` | n/a | `localPathStringSchema` = nonempty and NUL-free (`/^[^\x00]*$/u`). This is **stricter than the CLI's** `z.string().min(1)`, so a NUL is refused at service admission as `invalid_request`, not by the CLI parser. |
| `flutter/FlutterBuildProvider.js` | `2c00116a…d191` | Provider identity `{id:"flutter", name:"Flutter build identification", version:null}`, snapshotting, and limits |
| `flutter/FlutterPayloadScan.js` | n/a | Snapshot magic `f5f5dcdc`, hash at +20, 32 hex digits, `MAX_SNAPSHOT_HASH_CANDIDATES=64`, `MAX_TOOLCHAIN_LINES=4`, Dart label `^Dart VM version:` ≤200 characters |
| `contracts/flutter/flutterToolContracts.js` | `8150d522…0d3e` | MCP contract `identify_flutter_build`, `kind:"flutter-provider"`, `outputSchema: evidenceResultOf(flutterResultSchemas.identify_flutter_build)` |
| `contracts/toolEffects.js:245` | `1d12ce7f…14f8` | `identify_flutter_build: effects({mutatesSession:true, writesFilesystem:true})` |
| `composition/flutter.js` | n/a | `new FlutterBuildProvider()`, "needs no external tools" |
| `server/registerFlutterTools.js` | n/a | MCP registration through the same service (not used; MCP is out of bounds for this lane) |

## Exact input limits

**Schema:**

- `path` is required, a string, `minLength 1`, with no other arguments or options.
- At the domain level the path must also contain no NUL.
- The CLI never checks that the path is absolute.

**Provider (observed in source):**

| Limit | Value | Failure code (`projectAnalysisError`) |
|---|---|---|
| APK size before copy | `APK_MAX_BYTES = 2 GiB` | `resource_constraint` (file-size) |
| ZIP metadata read | `APK_METADATA_READ_MAX_BYTES = 8 MiB` | `resource_constraint` (memory) |
| Per library (`libapp.so` / `libflutter.so`) | `LIBRARY_MAX_BYTES = 256 MiB`, checked on the declared size and again while streaming | `resource_constraint` |
| Cumulative extraction | `TOTAL_EXTRACTION_MAX_BYTES = 768 MiB`, checked as a declared preflight and again in the loop | `resource_constraint` |
| ABIs | `MAX_FLUTTER_ABIS = 32`; library path ≤ `1024` bytes | `resource_constraint` (memory) |
| Snapshot-hash candidates | 64 | `resource_constraint` (memory) |
| Duplicate `lib/<abi>/lib{app,flutter}.so` member | refused | `invalid_request` (`invalid_format`) |
| Missing path, non-regular file, or unreadable ZIP | refused | `invalid_request` (`invalid_format`; message "does not exist" / "not a regular file" / "could not be read as a package") |
| `EACCES`/`EPERM` | refused | `access_denied` |
| Source changed or grew during the copy | refused | `artifact_changed` |
| Provider tmp storage I/O failure | refused | `resource_constraint` (file-size, "Provider-owned Flutter snapshot storage failed") |
| Abort | n/a | `cancelled` (may carry `details.partial_observation`) |

Library match regex: `^lib\/([^/]+)\/(libapp|libflutter)\.so$`. Other native libraries are ignored, so an empty `abis` array means only that no Flutter libraries were found, not that the APK has no native code.

## Exact effects

- **Contract:** `mutatesSession: true` and `writesFilesystem: true`. Every other flag is false: `mutatesTarget`, `launchesProcess`, `accessesNetwork`, `changesUiState`, `mayDiscardData`, `executesForeignCode`, and `mutatesDevice`. `idempotent` is true.
- **Filesystem writes:** the provider does `mkdtemp(os.tmpdir()/"rea-flutter-")`. It copies the APK to `input.apk` with `wx`, then `chmod 0400`. It writes each `libflutter.so` to `engine-<n>.so`, which is needed to read ELF build IDs. It removes the root in `finally` and again on `close()`. A cleanup failure keeps the root and raises `cleanup_incomplete`.
- **Not written:** the original APK is opened read-only with `symlinks:"follow"`. It is never modified, installed, or run.
- **Not performed:** network access, subprocess launch, engine use, or a Dart SDK lookup. The snapshot hash maps to an SDK only through an external dataset that REA does not consult.

## Output and operation binding

The success output is an Evidence object. Observed top-level keys in the retained record:

`analysis_profile, authority, confidence, environment, evidence_id, evidence_links, limitations, locations, normalized_result, operation, parameters, predicate_type, provider, raw_result, relationship_coverage, subject`

- `operation`: `"identify_flutter_build"`
- `evidence_id`: `ev_<64 hex>`, a canonical digest of the semantic projection
- `parameters`: `{path}`
- `subject`: `{name, digest:{sha256}, local_path, format:"apk", architecture:null}`

`normalized_result` follows `flutterResultSchemas.identify_flutter_build`:

- `target{path, bytes, sha256}`
- `flutter_detected`
- `abis[]`, where each entry has:
  - `libapp{present, bytes, sha256, elf_header_valid, snapshot_hash_sources, snapshot_hash_candidates[], snapshot_hash}`
  - `libflutter{present, bytes, sha256, build_id, build_id_candidates[≤64], dart_version, toolchain_lines[], dart_version_capped, toolchain_capped}`
- `coverage: complete | partial`

Coverage is `partial` if any of these hold:

- `libapp` is present but has no single hash, or its sources ≠ 2, or its ELF header is invalid
- a cap was hit
- `libapp` and `libflutter` presence do not match
- build-ID failures occurred, or there is more than one build-ID candidate

A non-Flutter APK is a **success**: `flutter_detected:false`, `abis:[]`, `coverage:"complete"`, plus the limitation "No lib/*/libapp.so was found…". That is what the lane already retained for the Godot release template.

### Counter mapping (R22-C1) — observed in source

`count-c1.py` sets T1 to include `identify-flutter-build` and `EVIDENCE_PREFIX = .ufo/waves/round-22/evidence/c1/`. Each step below must hold:

1. A knowledge entry with a `source:` S051+ row (mined 2026-10-21, and `used-by` names the entry) mentions `identify-flutter-build` or `identify_flutter_build` (`command_pattern`).
2. That entry cites the evidence file by full path.
3. The entry contains an `ev_<64hex>` id (`HEX64`).
4. `bind()` finds a top-level, list, or `evidence`/`evidences`/`records`/`result`-wrapped record whose `evidence_id` and `operation == "identify_flutter_build"` match exactly, with no structural refusal.

**Representation constraints for future retains:**

- The default CLI output is **TOON**. TOON is not decodable as JSON, so `bind` would return exit 2 (unevaluable). Use `--format json`.
- `--full-output` emits `{ok, data, meta}` (incur `Cli.js:1099–1119`). `records()` does not descend into `data`, so the result is `unsupported_evidence_representation` (exit 2). This is confirmed by the probe above.
- Use plain `--format json`, or extract `data` as the lane did and say so explicitly.
- Error projections: `flutterCommands.js` *returns* `projectAnalysisError(...)` as command data instead of throwing. `[INFERENCE]` A refused call therefore probably still exits 0 with `ok:true`, carrying `{code, category, message, retryable, remediation, details?}`. This was not executed.
  - Such a projection has no `evidence_id`/`operation`, so it can never bind (falsifier "typed refusal envelope counts" holds).
  - Flutter error codes `resource_constraint`, `access_denied`, `artifact_changed`, `cancelled`, and `cleanup_incomplete` are **absent** from `REFUSALS` in `verb-coverage.py:16-20`. That is harmless only because those projections lack a record. A partial observation nested in `details.partial_observation` (on cancellation) is not descended into, so it is also not counted.
  - **Do not rely on exit code 0 alone as proof of success.** Check that `evidence_id` and `operation` are present.

## Host/provider prerequisites

- **Node.js and npx:** v24.21.0 observed. `npx -y rea-agents@6.5.0` needs the npm cache, which is present, or registry access to fetch it.
- **Input:** a local regular-file APK (symlinks followed), readable, ≤2 GiB, with ZIP metadata ≤8 MiB and Flutter libraries ≤256 MiB each and ≤768 MiB in total.
- **Temp space:** a writable `os.tmpdir()` with free space ≥ APK size plus total `libflutter.so` size. `TMPDIR` is unset, so this is `/tmp`, which has 28 GB free.
- **Not needed:** no external tools, ADB, device, Flutter engine, or Dart SDK. `inspectAvailability()` always returns `available` with `engine:"static-apk-parsing"`. `REA_ADB_PATH` does not apply here.
- **For a positive result:** the APK must carry `lib/<abi>/libapp.so`. In a home-directory search, `find /home/vgpnk -xdev -name '*.apk'` was cut off at 25 s (exit 124, partial). It found only the Godot `android_debug.apk` and `android_release.apk`, neither a known Flutter carrier. **Unknown:** whether any Flutter APK exists on the host. This is the blocker for any positive snapshot-hash claim. Do not overclaim the existing negative.

## Comparison to claims.json

- R22-C1 `t1` lists `identify-flutter-build`. The counting path above matches the CLI operation exactly, so the claim's binding can be achieved.
- **Falsifiers:**
  - "mention without bound record": a mention alone fails at step 4.
  - "typed refusal counts": a refusal projection has no record.
  - "evidence id absent from cited file": `bind` requires the id in the blob.
  - "lacks S### citation": `source_rows` gating.
  - All four hold against this schema.
- **Lane state (HEAD `2ee3d9f`):**
  - `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md` already cites S051–S053 and `ev_3458b996…866b`.
  - The bound record shows the success was a parsed negative.
  - The entry's own wording keeps it narrow: no positive Dart, runtime, or source claim. That is consistent with the schema and effects above.
  - **Not verified here:** whether the full `count-c1.py --rev 2ee3d9f` counts it. That was not run because it was outside this seat's bounded scope.
- `not_claimed` names "Evidence authentication". That is consistent: `bind` is local record binding, and `evidence_id` is a content digest, not a signature.

## Unknowns

- Actual exit code and envelope for a refused CLI call (`[INFERENCE]` exit 0 with `ok:true`). Not observed.
- Positive-Flutter output shape on a real carrier. No fixture located; the search was partial.
- Whether a `6.7.0` schema differs. Not examined, and out of scope.

## Tooling

No install or update. Pacman was untouched, and `/home/vgpnk/.omp/agent/RULES.md` was not needed because no install happened. REA was used only through `npx -y rea-agents@6.5.0`, not through MCP devices.
