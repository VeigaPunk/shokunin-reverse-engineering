# R23 schema review — `identify-flutter-build` (REA 6.5.0)

Seat: `KaidokuR23.SchemaFlutter` (scout, leaf). Scope is the declared CLI surface `--help` / `--schema` plus read-only inspection of the installed 6.5.0 dist to name the exact operation and the exact output fields that separate a partial positive, a negative, and a refusal. **No APK was opened and no target command was executed.** Lane HEAD observed: `a3c92eb6bc70984e90ae5b895412de978840b2c5` (read-only `git rev-parse`, equals the contract revision). Findings are author-side, not outside verification.

Axes used for this seat: (A) declared-surface exactness, (B) operation binding exactness, (C) three-way discriminability from output fields, (D) calibration honesty (observed vs inference).

## Findings

### 1. Declared surface (observed, executed)

All commands ran from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. `npx -y rea-agents@6.5.0` resolved to the existing cache `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (package version `6.5.0`); the separate `6.7.0` cache `/home/vgpnk/.npm/_npx/a1722018f28f9df2` was not used. Node `v24.21.0`; `incur` `0.6.1`.

| argv | exit | stderr | output |
|---|---|---|---|
| `npx -y rea-agents@6.5.0 identify-flutter-build --help` | 0 | empty | below |
| `npx -y rea-agents@6.5.0 identify-flutter-build --schema` | 0 | empty | TOON: `args: type: object; properties: path: {type: string, minLength: 1, description: Local APK file to inspect}; required[1]: path; additionalProperties: false` |
| `npx -y rea-agents@6.5.0 identify-flutter-build --schema --format json` | 0 | empty | below |
| `npx -y rea-agents@6.5.0 --version` | 0 | empty | `6.5.0` |
| `npx -y rea-agents@6.5.0 --help` | 0 | empty | root command list includes `identify-flutter-build`; global options include `--format <toon\|json\|yaml\|md\|jsonl>`, `--full-output`, `--schema` |

Verbatim `--help` stdout:

```text
rea identify-flutter-build — Identify a Flutter build's Dart snapshot hash and engine facts by pure APK parsing

Usage: rea identify-flutter-build <path>

Arguments:
  path  Local APK file to inspect

Global Options:
  --filter-output <keys>              Filter output by key paths (e.g. foo,bar.baz,a[0,3])
  --format <toon|json|yaml|md|jsonl>  Output format
  --full-output                       Show full output envelope
  --help                              Show help
  --llms, --llms-full                 Print LLM-readable manifest
  --schema                            Show JSON Schema for command
  --token-count                       Print token count of output (instead of output)
  --token-limit <n>                   Limit output to n tokens
  --token-offset <n>                  Skip first n tokens of output
```

Verbatim `--schema --format json` stdout:

```json
{
  "args": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "minLength": 1,
        "description": "Local APK file to inspect"
      }
    },
    "required": [
      "path"
    ],
    "additionalProperties": false
  }
}
```

Observed limits of this surface:

- Exactly one positional argument `path`; no `options` member, so no `--abi` or any other command option for this verb.
- The schema does **not** advertise an output schema, error/refusal schema, effects, provider identity, or coverage semantics. Nothing in `--help` or `--schema` distinguishes partial positive, negative, or refusal.
- `path` is only `z.string().min(1)` at the CLI; the stricter domain schema `localPathStringSchema` (nonempty, NUL-free) is applied later at service admission. Source: `dist/cli/flutterCommands.js:15-21`, `dist/domain/localPath.js:18`.

### 2. Exact operation (observed in dist source)

- `dist/cliCommandNames.js:72` — `identifyFlutterBuild: "identify-flutter-build"`.
- `dist/cli/flutterCommands.js:13` binds `command: CLI_COMMANDS.identifyFlutterBuild`; `:18` binds **`operation: "identify_flutter_build"`** explicitly; `:20` is `toInput: (arguments_) => arguments_`, so the input object is exactly `{path}`.
- `dist/domain/flutter/flutterBuildAnalysis.js:31-33` — `flutterRequestSchema` is a discriminated union on `operation`, and `identify_flutter_build` narrowly admits `z.strictObject({path: localPathStringSchema})`.
- `dist/application/flutter/FlutterBuildAnalysisService.js:17-19` — the service calls `executeProviderOperation(..., "observed")`, so the produced Evidence carries `confidence: "observed"`.
- `dist/application/ProviderOperationExecution.js:12-33` — re-parses `{operation,input}`; success builds Evidence with `parameters` equal to the validated input (`{path}`), and cancellation can attach a finished observation as `details.partial_observation`.

The operation name is therefore not derived from the command name by string rewriting; it is declared, and it is exactly `identify_flutter_build`. A counter that maps CLI `identify-flutter-build` to this operation is consistent with the CLI spec.

### 3. Success record: fields that exist (observed in dist source)

A non-refusal outcome is an Evidence object (`dist/domain/evidence.js:234-243`, semantic keys at `:266-299`):

`subject`, `provider{id:"flutter", name:"Flutter build identification", version:null}`, `analysis_profile` (null here), `predicate_type` (`"rea.analysis"`), `operation` (`"identify_flutter_build"`), `parameters`, `raw_result` (null here), `normalized_result`, `confidence` (`"observed"`), `authority` (`"shipped-artifact"`), `environment` (null here), `limitations[]`, `relationship_coverage` (null here), `locations[]`, `evidence_links[]`, `evidence_id` (`ev_<64 hex>`).

`normalized_result` schema (`dist/domain/flutter/flutterBuildAnalysis.js:42-91`) is a strict object with exactly:

- `target{path, bytes, sha256}`
- `flutter_detected: boolean` (`:47`)
- `abis: array` of strict objects (`:48-89`), each with:
  - `abi`
  - `libapp{present, bytes|null, sha256|null, elf_header_valid|null, snapshot_hash_sources: int>=0, snapshot_hash_candidates: 32-lowerhex[], snapshot_hash: 32-lowerhex|null}`
  - `libflutter{present, bytes|null, sha256|null, build_id: 8..128-lowerhex|null, build_id_candidates: 8..128-lowerhex[≤64], dart_version|null, toolchain_lines: string[1..][], dart_version_capped: boolean, toolchain_capped: boolean}`
- `coverage: "complete" | "partial"` (`:90`)

There is **no** `partial_reasons`, `refused`, `error`, `ok`, `confidence` inside `normalized_result`, and no `coverage` at the Evidence top level. `coverage` is only `normalized_result.coverage`.

### 4. Exact predicates separating the classes (observed in dist source)

Coverage is computed at `dist/flutter/FlutterBuildProvider.js:490-504`:

```text
flutterDetected = abis.some(entry => entry.libapp.present)
partial = abis.some(entry =>
            (entry.libapp.present && (
                entry.libapp.snapshot_hash === null ||
                entry.libapp.snapshot_hash_sources !== 2 ||
                entry.libapp.elf_header_valid !== true)) ||
            entry.libflutter.toolchain_capped ||
            entry.libflutter.dart_version_capped ||
            entry.libapp.present !== entry.libflutter.present)
        || facts.some(value =>
            value.libflutter.buildIdFailures.length > 0 ||
            value.libflutter.buildIdCandidates.length > 1)
coverage = partial ? "partial" : "complete"
```

| Class | Discriminating fields | Distinguishing from the other two |
|---|---|---|
| **Partial positive** | Evidence present (`evidence_id`, `operation:"identify_flutter_build"`); `normalized_result.flutter_detected == true`; `normalized_result.coverage == "partial"`; at least one per-ABI clause: `libapp.present && snapshot_hash == null`, or `snapshot_hash_sources != 2`, or `elf_header_valid != true`; or `toolchain_capped == true`; or `dart_version_capped == true`; or `libapp.present != libflutter.present`; or any un-serialized `buildIdFailures`; or `build_id_candidates.length > 1` | Positive (not refusal) because the Evidence exists; partial (not complete success) because `coverage == "partial"` |
| **Complete positive** | Evidence present; `flutter_detected == true`; `coverage == "complete"`; every `libapp.present` entry has non-null 32-hex `snapshot_hash`, `snapshot_hash_sources == 2`, `elf_header_valid == true`; both libraries present for every ABI; no caps; `build_id_candidates` length 0 or 1 | Same Evidence identity as partial; only `coverage` and the per-ABI fields differ |
| **Pure negative** | Evidence present; `flutter_detected == false`; `abis == []`; `coverage == "complete"`; a limitation line exactly `No lib/*/libapp.so was found; the target does not carry a Flutter AOT payload` (`FlutterBuildProvider.js:538`) | Not a refusal: it carries `evidence_id` and `operation`. A non-Flutter APK is a successful parsed observation |
| **Partial negative** | Evidence present; `flutter_detected == false`; `abis != []` (a `libflutter.so`-only ABI); `coverage == "partial"` because `libapp.present != libflutter.present` | Shows that `coverage` alone cannot split negative from partial positive — `flutter_detected` is the primary split |
| **Refusal** | No Evidence identity: top-level `code`, `category`, `message`, `retryable`, `remediation{action}`, optional `details` (`dist/domain/analysisErrorProjection.js:46-60`). Absent: `evidence_id`, `operation`, `normalized_result`, `subject`, `provider`, `confidence`, `authority`, `limitations` | Cannot bind as a T1 held record: operation and evidence id exist only inside `details` for some error tags, never at top level |

Exact edge cases worth preserving:

- `build_id == null` does **not** imply partial. It is null when `buildIdFailures.length > 0` **or** `buildIdCandidates.length !== 1` (`FlutterBuildProvider.js:453-455`), so `build_id:null` with `build_id_candidates:[]` and no failures leaves `coverage:"complete"`.
- For an entry with `libapp.present:true`, `snapshot_hash:null` always implies `coverage:"partial"` (0 or ≥2 distinct hashes). `snapshot_hash` is `null` unless the distinct candidate count is exactly 1 (`:473-475`).
- The reasons for `buildIdFailures` are **not serialized** as fields; they appear only as limitation strings `lib/<abi>/libflutter.so: <reason>` and `... has conflicting GNU build IDs` (`FlutterBuildProvider.js:508-518`). A consumer that sees `coverage:"partial"` must read `limitations[]` to learn which non-field causes applied; the per-ABI field causes are directly recoverable.
- `dart_version == null` is normal for release engines and is stated as "absence is reported, not guessed" (`:510`); it does not by itself imply partial. `dart_version_capped` is set for an over-long/ungrammatical or disagreeing label (`FlutterPayloadScan.js:147-153`), and `toolchain_capped` when a line overflows, fails the grammar, or a fifth distinct accepted line is seen (`:154-170`, `MAX_TOOLCHAIN_LINES = 4`).
- `abis[]` is built only from `lib/<abi>/{libapp,libflutter}.so` members (`FlutterBuildProvider.js:143-167`); an empty `abis` means no Flutter libraries were found, not that the APK has no native code.

### 5. Refusal boundary and CLI representation (source-observed; not executed)

Refusal projections for this operation, from `FlutterBuildProvider.js` and the shared projector:

| Trigger (source) | `code` | `category` | `retryable` | `details` |
|---|---|---|---|---|
| Missing/non-regular/unreadable APK, duplicate Flutter member, NUL path | `invalid_request` | `invalid_input` | true (`invalid_request` is in `RETRYABLE_CODES`, `analysisErrorProjection.js:458-466`) | `{operation, issues[]}` when `mapInputFailure` supplies an issue; absent for a pure schema re-parse failure (`issues.length == 0`) |
| `EACCES`/`EPERM` | `access_denied` | `unavailable` | false | `{operation, path, system_code, boundary:"filesystem-read"}` |
| APK > 2 GiB; library > 256 MiB; cumulative > 768 MiB; ABI/path/hash-candidate caps | `resource_constraint` | `resource_constraint` | only when `resource == "capacity"` (never from this provider) | `{operation, resource, reason, reported_limits}` |
| Source identity/size changed during snapshot | `artifact_changed` | `integrity_mismatch` | true | `{operation, path, reason, boundary:"stable-artifact-read"}` |
| Cancellation | `cancelled` | `cancelled` | true | `{operation, cleanup}`; may carry `partial_observation` Evidence |
| Provider-owned temp storage I/O failure | `resource_constraint` | `resource_constraint` | false | `{operation, resource, reason:"file-size", reported_limits:null}` (message names provider storage) |
| Cleanup incomplete on a typed error | `cleanup_incomplete` | inherits | per base code | `{cleanup:"incomplete", resources[], execution_failure, ...}` |

`message` is not a reliable discriminator: for `AnalysisResourceConstraintError` it is just the `reason` string (`analysisErrorPresentation.js:160-161`); for `AnalysisInputError` it is the fixed sentence "Analysis input is invalid. Check the arguments and try again." unless a `userMessage` is supplied (`:166-168`). The path-specific text lives in `details.issues[].message`.

Representation facts relevant to R23-C1 counting:

- Default CLI format is TOON (`incur/dist/Cli.js:1016`, `:1924`; `validFormats` at `:1913`). Use `--format json`.
- Without `--full-output`, the CLI writes the data member only; with `--full-output`, it writes `{ok, data, meta}` (`incur/dist/Cli.js:1088-1130`). The earlier round-22 finding that a `--full-output` envelope does not bind while its extracted `data` does remains consistent with this source.
- **Inference (source path, not executed):** a refusal projection is *returned* as command data by `flutterCommands.js:59-65`, so incur's `result.ok` branch (`incur/dist/Cli.js:1366-1393`) writes `{ok:true, data:<refusal>, meta}` and does not call `exit(1)`; the projection itself has no `ok:false`. A refused invocation therefore likely exits **0**. The only local exception is `provider.close()` rethrowing a non-`AnalysisError` `AggregateError` (`flutterCommands.js:55-63`), which incur would convert to `ok:false` and exit 1. Not executed this seat.
- Consequently, exit code is not a refusal discriminator for this verb; the absence of top-level `evidence_id` plus `operation == "identify_flutter_build"` is. This satisfies the claim's falsifier "typed refusal envelope counts" without needing a runtime probe.
- Separate pre-dispatch class: missing or extra arguments are refused by incur before the service runs and produce `{ok:false, error:{code:"VALIDATION_ERROR", message, fieldErrors}}` with exit 1 (`incur/dist/internal/command.js:170-180`, `incur/dist/Cli.js:1404`). That is distinguishable from both a provider refusal (returned as data under `ok:true`) and Evidence.

### 6. Ceiling of this evidence

- `--help` and `--schema` expose only the single `path` argument. Every partial/negative/refusal distinction above is read from the installed dist implementation, not from the declared CLI surface. Do not present the CLI schema as authority for effects or output classes.
- No positive, negative, or partial instance was produced here. The class boundaries are source predicates; their runtime serialization is unverified in this seat.
- No target sha256 is recorded because zero targets were selected or opened. Commands executed: help, schema (TOON and JSON), version, root help; all exit 0 with empty stderr.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SchemaFlutter.md` — this report. SHA-256 of the final bytes is reported in the seat's final message after the last write (cannot be embedded without changing the hash).
- No other files were created. Transient `/tmp` captures of the help/schema stdout were removed after transcription; their digests at capture time were `abe0662a2f5383d2eaf5ec957dae249e5c9c076691266eca97aaab2cc9ec65b1` (`--help`) and `92268a78183f62385bf10eadb9ca00d1b301e1d5c7d532520ba29ac7b3c24f85` (`--schema --format json`), and their content is reproduced verbatim above.

Source files read (SHA-256, all under `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`):

- `dist/cli/flutterCommands.js` `8354ba86bc42c73a785c3ed9b99f0f8a702d1b0be5fe6d798b76d6ee35da0d18`
- `dist/domain/flutter/flutterBuildAnalysis.js` `c8cac80550d266e1741142bfd9e88a87381fc0fd25485b4ea6ed0db25538ddf2`
- `dist/flutter/FlutterBuildProvider.js` `2c00116a02ee3e9a483886a14ec84d7f224899c8807c84c999bcca49b043d191`
- `dist/flutter/FlutterPayloadScan.js` `9f5e10f502a14078d9ded1df6705814ba25068a490d5e39da06963be0f5f8b7e`
- `dist/domain/analysisErrorProjection.js` `9abea51a183f5b2f85e20881fdf4b90293e40f5a17bf351e04bf5e2fed49baf9`
- `dist/domain/evidence.js` `f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff`
- `dist/application/ProviderOperationExecution.js` `f73d581c25fd184aeda5f7cc1845da06e960857c756682c5187aad882dde58d0`
- `dist/domain/localPath.js` `c14e7c62c21f1beaab25774a8248615e7814a1dd189828f53e5169040269f31a`
- `dist/cliCommandNames.js` and `incur/dist/Cli.js` were also read; their hashes were not captured.

## Installs

None. No pacman or other package transaction was attempted; no uv/npx install beyond the already-cached `npx -y rea-agents@6.5.0` resolution. No global install or config edit.

## Open risks

- The refusal exit-status statement is inference from `incur@0.6.1` source, not an executed refusal; if a probe is later run, verify `ok:true`/exit 0 with `--format json --full-output`.
- `build_id` failure reasons are only in `limitations[]`; any counting or knowledge rule that keys on structured partial reasons will silently miss that cause.
- A `libflutter.so`-only APK is a negative with `coverage:"partial"`. A rule that equates `coverage:"partial"` with a partial *positive* would be wrong.
- `--format json` is required for bindable records; default TOON and `--full-output` envelopes are not decodable by the prior round's binder.
- Nothing here verifies provider presence over time, authentication, or any dynamic/debugger ownership; those remain unresolved and out of this wave's boundary.
