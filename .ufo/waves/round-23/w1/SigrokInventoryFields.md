# SigrokInventoryFields — REA signal discovery parser and returned evidence schema

Seat: `KaidokuR23.SigrokInventoryFields` (leaf scout, round-23 w1). Author-side report, not outside admission. Opened 2026-10-21.

## Question

Inspect REA's signal discovery parser and returned evidence schema: are decoder help and the full decoder list complete, capped, or filtered?

## Verdict

- **Catalog mode (`decoder: null`) is complete over every decoder that libsigrokdecode successfully imports from the probe's search paths, and it fails closed otherwise.** The parser consumes every non-empty line after the exact heading and throws on the first malformed or duplicate record; it never skips a bad record to return a partial list. It applies no type, category, tag, or allowlist filter. Observed end to end: 110 catalog records parsed and returned with `--all`, exactly matching 110 decoder lines in the raw producer output.
- **The catalog is not a directory inventory.** In the observed bundle, 112 decoder directories exist: `common` is not a protocol decoder, and `signature` failed to import (Python 3.5.2 rejects `0b..._...` numeric underscores at `pd.py:138`). The catalog therefore reports `examined: 110`; the failed module appears only as free text in `diagnostics` (producer stderr) and is not counted anywhere in `output_window`. This is the one real completeness gap.
- **Paging caps the default response, not the parser.** `limit` defaults to 50 for both catalog and help; `limit: null` (CLI `--all`) returns all remaining. `output_window` exposes `examined`, `matching`, `returned`, `has_more`, and the report schema arithmetically enforces them. A caller that omits `--all` sees 50 of 110 decoders, or 50 of 81 help lines (for `uart`, page 1 ends exactly at the line `Options:`, hiding all option lines).
- **Hard resource caps fail the request instead of truncating it.** 65,536 producer newlines (`line_budget: 65536`) and 4 MiB combined stdout+stderr (`output_bytes: 4194304`) produce typed resource-constraint errors; there is no silently shortened catalog or help page.
- **Help is literal stdout, not a parsed option schema.** For one exact decoder ID, every line is returned verbatim with a 1-based `line_number`, including `ID:`, `Name`, `License`, channels, annotation classes, `Options`, and `Documentation`. The only filtering is the caller's case-insensitive literal substring `query`; the only cap is the same paging/resource budget. Stacks and inline options cannot be requested (input regex forbids `:` and `,`).
- **The returned evidence binds to the configured command, not to the sigrok binary or decoder modules.** For the observed wrapper, `subject.sha256` and `tool.sha256` are the wrapper script's digest (`50fe4359...`), while the executed `runtime/squashfs-root/usr/bin/sigrok-cli` has a different digest (`10fed05a...`) and no digest of libsigrokdecode or any decoder module is recorded. `authority` is the default `shipped-artifact`, `locations` is empty, and `environment` is null.

## Observed end-to-end probes

All REA invocations were `npx -y rea-agents@6.5.0 ... --format json --full-output` from the repo root, with `npm_config_offline=true` and `REA_SIGROK_COMMAND=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/tools/sigrok-cli.sh` (wrapper sha256 `50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902`). `REA_SIGROK_PRLIMIT_COMMAND` was unset, so `/usr/bin/prlimit` (sha256 `092bb6db...`) was used. The wrapper exports `SIGROKDECODE_DIR=<bundle>/usr/share/libsigrokdecode/decoders`, `LD_LIBRARY_PATH=<bundle>/usr/lib`, `LD_PRELOAD=/usr/lib/libgmodule-2.0.so.0`, `PYTHONPATH=<bundle>/usr/share/pyshared`, then execs the bundle's `sigrok-cli`.

| # | Operation (arguments) | exit | Observed result |
|---|---|---|---|
| 1 | `inspect-signal-decoders --limit 5` | 0 | `output_window {unit: decoders, examined: 110, matching: 110, returned: 5, has_more: true}`; IDs `ac97, ade77xx, adf435x, adns5020, am230x`; stdout sha256 `b6967be8838f22519566a67908a05159761a4448a5c7bca36f818771d5bce8d8` |
| 2 | `inspect-signal-decoders --offset 108 --limit 50` | 0 | `{examined: 110, matching: 110, returned: 2, has_more: false}`; IDs `xfp, z80`; stdout sha256 `4969567dcf599485f4df74aac27622053fc8aecda8fcb8e237292e86df11cdac` |
| 3 | `inspect-signal-decoders --decoder uart` (default limit) | 0 | `{unit: help-lines, examined: 81, matching: 81, returned: 50, has_more: true}`; line 1 `ID: uart`, line 50 `Options:`; stdout sha256 `6ab5de409c9ced65232da8d6f00fe97435690c40aa6b4c5ecb7e38fa4f474e2b` |
| 4 | `inspect-signal-decoders --decoder uart --query baud --all` | 0 | `{examined: 81, matching: 1, returned: 1, has_more: false}`; `{line_number: 51, text: "- baudrate: Baud rate (default 115200)"}`; stdout sha256 `59d158a76dd017f9fab28d8e301b0d1dccf29a3656b103fc16b002109b2eec12` |
| 5 | `inspect-signal-decoders --query signature --all` | 0 | `{examined: 110, matching: 0, returned: 0, has_more: false}`; the installed-but-unloadable decoder is absent and no coverage field flags the omission; stdout sha256 `ad613e7f0c31abf3228a2026063f7acf34ea6f813cde6627a2886926c515537e` |
| 6 | `inspect-signal-decoders --decoder signature --all` | 1 | `execution_failure`, `details.diagnostics.exit_code: 1`, `stdout: ""`, stderr carries the Python traceback; no empty or partial help evidence is returned; stdout sha256 `9c99af68f4759e0fce83dbfdfcef5f27335fc8281b1d5934e3dda446e15c2b9e` |
| 7 | `inspect-signal-decoders --format json --full-output` with `REA_SIGROK_COMMAND` unset | 1 | `{"ok":false,"error":{"code":"capability_unavailable","category":"unsupported_provider",...}}`; typed refusal, zero Evidence (falsifier-safe); stdout sha256 `d24b0a56bee07de14be77d48f5abcf2d6635a3739993bebec675a93103567dee` |

Producer-side comparison, same wrapper:

| Raw producer argv | exit | Observed |
|---|---|---|
| `sigrok-cli.sh --dont-scan --list-supported` | 0 | 307 stdout lines; heading `Supported protocol decoders:` at line 196; exactly 110 decoder lines after it; trailing blank line; sorted by ID. stdout sha256 `0e5938406f367ba68d450d37997299083b56aae1bcc55c699d52b319e392e3a9`; stderr sha256 `ada8213392dd099d0656dd0dd277280d8e46a874f7494e47068a5f8d501127f6` (841 bytes) |
| `sigrok-cli.sh --dont-scan --protocol-decoders=uart --show` | 0 | 81 stdout lines, beginning `ID: uart`; stdout sha256 `dfde345065b51f41bc9199f5082db430721ba50157b6423a4dca02d228265acf`; stderr sha256 `58ff3410f8b9a853b9eeda9da7dd2468d6fdff22004deabbf8f8d310c8e46e5d` |

REA's `examined` equals the raw producer counts exactly (110 catalog records; 81 help lines), so the parse is lossless on this installation. The 841-byte inventory `diagnostics` string has exactly the length of the producer's stderr in the companion raw run (841 bytes), consistent with verbatim retention; byte equality across the two runs was not rechecked after the raw file was removed.

The lane's already-retained bound record is `.ufo/waves/round-23/evidence/c1/inventory.envelope.json` (`evidence_id ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0`, CLI `--all`, `examined: 110, returned: 110, has_more: false`). The probes above are author-side re-exercise of the same command; they are not new evidence rows and do not alter the lane's count.

## Parser mechanics (source, rea-agents 6.5.0)

Installed package root: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (package.json version `6.5.0`).

`dist/signals/parseDecoderDiscovery.js` (sha256 `2fa74a0bacdff46f9155cf10320445fafeda9358b0efe9df2acbe13f3669097e`, 65 lines):

- Lines 8-11: before splitting, counts `\n` in the whole stdout; at the 65,536th newline throws `DecoderDiscoveryBudgetError`. `SigrokRecordingProvider.js:261-267` maps that to `AnalysisResourceConstraintError` with `memory` and `{line_budget: 65536}`. The comment states the budget covers record-object expansion, not the byte cap.
- Lines 12-14: splits on `\r?\n` and pops exactly one trailing empty string; interior blank lines survive.
- Lines 18-21: catalog mode requires the exact line `Supported protocol decoders:`; absence is an error, not an empty result. Everything before the heading (hardware drivers, input formats, output formats, transform modules) is ignored; sigrok-cli prints the decoder section last, so the parse continues to EOF.
- Lines 22-33: after the heading, every non-empty line must match `^ {2}([a-zA-Z0-9_+-]+) +(.+)$`; a non-match or a repeated ID throws `Malformed or duplicate sigrok decoder catalog record`. There is no `continue` on a bad record, so the list is all-or-error. Trailing spaces in the long name are preserved in `name` (the regex leaves them to `(.+)`); an empty long name yields `name: " "` by regex backtracking (checked against the literal pattern in Node).
- Lines 34-35: zero records after the heading throws `sigrok returned an empty decoder catalog`.
- Lines 37-40: help mode requires `lines[0] === "ID: <decoder>"` exactly; every split line is retained with `line_number = index + 1`. No structural parsing of channels, options, defaults, or documentation.
- Lines 42-45: one case-insensitive literal substring filter. Catalog matches against the concatenation `` `${id} ${name}` `` (a query can therefore match across the ID/name boundary); help matches against each line's text. No tokenization, no regex, no field selector, no exclusion filter.
- Lines 46-47: `start = min(offset, matching.length)`; `count = min(limit ?? remaining, remaining)`. `offset` beyond the end returns an empty terminal page with `has_more: false`.
- Lines 49-53: only the returned page is copied (`copyText` UTF-16LE round-trip), so the page is independent of the full producer string.
- Lines 57-63: `output_window` reports `unit`, `examined` (pre-filter record/line count), `matching` (post-filter), `returned`, and `has_more = start + count < matching.length`.

`dist/domain/signals/signalDecoders.js` (sha256 `cb052ebc2ffe3ac5931179b5e137bcf8c8c7c94cb2cdc3c5ae500b29c63040d5`, 69 lines):

- Lines 3-31 input schema: `decoder` matches `^[a-zA-Z0-9_+\x2d]+$`, max 256, nullable, default null; `query` max 8192, default `""`; `offset` non-negative int up to `Number.MAX_SAFE_INTEGER`, default 0; `limit` positive int up to `Number.MAX_SAFE_INTEGER`, nullable, default 50. A stack (`uart:rx=RX`) or inline option is not expressible.
- Lines 32-52 report schema: strict object with `selection`, `decoders[{id,name}]`, `help_lines[{line_number,text}]`, `output_window`, `diagnostics`, `tool`, `resource_limiter`, `limits`, `hardware_acquisition: "not-performed"`.
- Lines 53-68 `superRefine`: recomputes `remaining` and `expected = min(remaining, limit ?? remaining)` and rejects the report unless `unit` matches the mode, `matching <= examined`, `returned === expected`, the active array length equals `expected`, the inactive array is empty, and `has_more === (remaining > expected)`. A parser or paging bug therefore becomes an output error before Evidence is created.

`dist/signals/SigrokRecordingProvider.js` (sha256 `7979bafb84b463d0fc3040d3643e08362326d67fd4543ee690679dc88b2dced7`, 339 lines):

- Lines 140-142 version gate: stdout must start with `sigrok-cli 0.7.2` and contain `libsigrokdecode`. The libsigrokdecode *version* and Python version are not checked (observed bundle: libsigrokdecode 0.5.3, Python 3.5.2).
- Lines 164-166 producer argv: catalog = `--dont-scan --list-supported`; help = `--dont-scan --protocol-decoders=<id> --show`. No `-l`/loglevel, no category flags, no `--protocol-decoder-*` selection.
- Lines 143-161 metadata: full `--version` stdout as `version_banner`, its stderr as `version_diagnostics`, producer argv as `tool.arguments`, prlimit path/sha256/argv as `resource_limiter`, `{...LIMITS, ...effectiveLimits}` as `limits`, `hardware_acquisition: "not-performed"`.
- Lines 168-172: `signalDecodersSchema.parse({selection, ...parseDecoderDiscovery(stdout.text), ...metadata})`. `selection` is the post-validation input, so a CLI `--all` is recorded as `limit: null`.
- Lines 173-180: Evidence subject is the configured command resolved by `realpath`, with `format: "file"` and its sha256; limitations state that help is producer text, that each request re-probes, that decoder modules/libraries are trusted and not fully fingerprinted, and that hardware discovery/recording/acquisition are not requested.

## Evidence schema (returned)

CLI success wrapper (observed): `{"ok": true, "data": <Evidence>, "meta": {"command": "inspect-signal-decoders", "duration": "..."}}`. Failure wrapper: `{"ok": false, "error": {...}, "meta": {...}}`; no partial `data`.

Evidence object (`dist/domain/evidence.js:99-117`, observed keys): `evidence_id`, `subject`, `provider`, `analysis_profile`, `predicate_type`, `operation`, `parameters`, `raw_result`, `normalized_result`, `confidence`, `authority`, `environment`, `limitations`, `relationship_coverage`, `locations`, `evidence_links`. The MCP output schema wraps the same shape plus `normalized_result` (`dist/contracts/toolOutputSchemaPrimitives.js:12-14`).

Observed values for discovery:

- `provider`: `{id: "sigrok-recording", name: "REA sigrok recording adapter", version: "sigrok-cli@0.7.2"}`.
- `predicate_type: "rea.analysis"`, `operation: "inspect_signal_decoders"`, `confidence: "observed"`, `authority: "shipped-artifact"` (default), `analysis_profile: null`, `environment: null`, `relationship_coverage: null`, `evidence_links: []`, `raw_result: null`.
- `parameters`: the validated selection, e.g. `{decoder: null, query: "", offset: 0, limit: null}` after `--all`.
- `subject`: `{name: "sigrok-cli.sh", digest: {sha256: "50fe4359..."}, local_path: "<wrapper>", format: "file", architecture: null}`. This is the configured command; for a wrapper, the executed binary (`10fed05a...`) and all decoder modules are outside the recorded identity.
- `locations: []` for discovery; `locations: [{kind: "artifact-path", path}]` only for decode mode.
- `limitations`: three fixed strings (`SigrokRecordingProvider.js:175-179`); none states that failed decoder imports are omitted from the catalog.
- `normalized_result`: `selection`, `decoders` or `help_lines`, `output_window`, `diagnostics`, `tool`, `resource_limiter`, `limits`, `hardware_acquisition`.
- `diagnostics` is exactly producer stderr (observed 841 bytes including the `signature` SyntaxError and traceback). It is not parsed, classified, or reflected in `output_window`.
- `limits` observed: `{input_bytes: 33554432, output_bytes: 4194304, command_timeout_ms: 30000, address_space_bytes: 1073741824, file_bytes: 67108864, cpu_seconds: 30}` (`dist/process/LinuxResourceLimits.js:10-17`).
- `tool.version_banner` is the complete multi-line `--version` output, including libsigrok/libsigrokdecode/Python versions.

## Caps and filters, precisely

| Dimension | Behavior | Grounding |
|---|---|---|
| Decoders per page | default 50; `limit: null` = all remaining; no upper bound besides `MAX_SAFE_INTEGER` | schema lines 23-30; parser 46-47; observed probes 1-2 |
| Help lines per page | default 50; `limit: null` = all remaining | same; observed probes 3-4 |
| Offset | clamped to `matching.length`; past-end returns empty page | parser 46; observed probe 2 |
| Catalog filter | caller `query` only, case-insensitive literal substring over `"<id> <name>"` | parser 43-44 |
| Help filter | caller `query` only, same substring test per line | parser 45; observed probe 4 |
| Type/category/tag filter | none; no allowlist, no exclusion, no "only decoders with options" filter | parser 18-35; provider argv 164-166 |
| Parser line budget | 65,536 newlines across the whole producer stdout; hard error, no partial page | parser 8-11; provider 261-267 |
| Producer output budget | 4 MiB combined stdout+stderr; overflow marks `truncated` and fails the command (`output-limit`), mapped to `AnalysisResourceConstraintError` with `output_bytes` | `ProviderProcess.js:344-365`, `OwnedCommand.js:69-72`, `ArtifactAnalysisResources.js:145-146` |
| Other process limits | 30 s wall clock, 1 GiB address space, 64 MiB file size, 30 CPU s, no core dumps; enforced with `/usr/bin/prlimit` | `LinuxResourceLimits.js:10-26`; observed `resource_limiter.arguments` |
| Input limits | decoder ID max 256 and restricted charset; query max 8192; offset/limit max safe integer | schema 3-31 |
| Complete-set filter | only decoders that libsigrokdecode successfully imports; failed imports omitted from the count | observed 112 dirs vs 110 records; producer source below |
| Environment filter | decoder search paths are inherited from the REA process: system XDG dirs, compiled `DECODERS_DIR`, user data dir, `SIGROKDECODE_DIR` | libsigrokdecode `srd.c:244-275`; wrapper observed setting `SIGROKDECODE_DIR` |

## Producer grammar grounding (official sources)

Downloaded for reading only (not installed; removed after inspection):

- `https://sigrok.org/download/source/sigrok-cli/sigrok-cli-0.7.2.tar.gz` — HTTP 200, 230,354 bytes, sha256 `71d0443f36897bf565732dec206830dbea0f2789b6601cf10536b286d1140ab8`, Last-Modified 2021-03-01.
- `https://sigrok.org/download/source/libsigrokdecode/libsigrokdecode-0.5.3.tar.gz` — HTTP 200, 892,783 bytes, sha256 `c50814aa6743cd8c4e88c84a0cdd8889d883c3be122289be90c63d7d67883fc0`, Last-Modified 2019-12-11.

Facts that make REA's catalog grammar match the default producer output:

- `sigrok-cli-0.7.2/show.c:193-207`: prints `Supported protocol decoders:`, then one `printf("  %-20s %s\n", dec->id, dec->longname)` per decoder, then a trailing blank line. A second indented description line is printed only when `opt_loglevel >= SR_LOG_INFO` (line 201); the default is `SR_LOG_WARN` (`options.c:27`), and REA passes no `-l`, so descriptions are absent. This is why the strict two-space grammar is sufficient.
- `show.c:55-60`: the producer sorts decoders by `strcmp(dec->id)`; REA preserves that order. Observed catalog is sorted and unique.
- `show.c:875-884`: help begins `ID: %s\nName: %s\nLong name: %s\nDescription: %s\nLicense: ...` and continues through inputs/outputs/tags/annotations/channels/`Options:`/`Documentation:`. REA's first-line check matches this producer contract; all subsequent lines are kept verbatim.
- `libsigrokdecode-0.5.3/decoder.c:1033-1071`: `srd_decoder_load_all_path` iterates every directory entry, calls `srd_decoder_load`, and explicitly ignores failures ("keep going"); `srd_decoder_load_all` loops over all search paths. A module that fails import is absent from `srd_decoder_list()` with no catalog marker.
- `decoder.c:679-700`: an already-imported module name returns `SRD_OK` early, so duplicate directory names across search paths collapse to the first; a different module claiming a duplicate `id` would still reach `pd_list` and make REA's `seen` check throw.
- `log.c:180-200`: libsigrokdecode's default callback writes `srd: ...` to stderr regardless of the GLib logger; failed imports therefore land in REA's `diagnostics`, not stdout.
- `srd.c:244-275`: search paths include system XDG data dirs, compiled `DECODERS_DIR`, the XDG user data dir, an optional program path, and `SIGROKDECODE_DIR` (added last). `srd.c:147-164` prints them only at debug level, so they do not appear in `diagnostics` at the default loglevel.

Observed accounting: 112 entries in `runtime/squashfs-root/usr/share/libsigrokdecode/decoders`; `common` is present (libsigrokdecode's common module, not a decoder) and `signature` is present but fails import; 112 - 2 = 110 catalog records. The bundle reports libsigrokdecode 0.5.3 / Python 3.5.2. `[INFERENCE]` the cause is Python 3.5 rejecting the PEP 515 underscore literal `0b0000_0010_1001_0001` at `pd.py:138` (underscore literals were added in Python 3.6); the retained traceback is an upstream `SyntaxError`, not a REA parse error.

## Cross-version check

`dist/signals/parseDecoderDiscovery.js` and `dist/domain/signals/signalDecoders.js` are byte-identical between the cached 6.5.0 (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/...`) and 6.7.0 (`/home/vgpnk/.npm/_npx/a1722018f28f9df2/...`) packages (`diff` exit 0 for both). `SigrokRecordingProvider.js` differs only in cancellation/cleanup error plumbing; the producer argv, schema call, and limitations are unchanged at 6.5.0 lines 164-180 and 6.7.0 lines 167-183. `LinuxResourceLimits.js` differs only in file-handle refactoring; the six limit values are unchanged. `signalToolContracts.js` is identical. The findings are therefore not specific to the pinned 6.5.0 patch level for the parser/schema surface.

## Draft source rows (L1 assigns IDs; current highest is S057)

```
| S0xx | rea-agents 6.5.0 installed package — dist/signals/parseDecoderDiscovery.js, dist/domain/signals/signalDecoders.js, dist/signals/SigrokRecordingProvider.js | code | A | Signal discovery parses only the sigrok 0.7.2 `--list-supported` catalog grammar (two-space ID/longname lines) all-or-error, keeps `--show` help literal, filters only by caller literal query, pages with default 50 but reports examined/matching/returned/has_more, and enforces a 65,536-line parse budget; the returned Evidence binds the configured command digest, not decoder modules | Package root `.../rea-agents` version 6.5.0; parser sha256 2fa74a0b…, schema cb052ebc…, provider 7979bafb…; parser lines 8-11, 18-47, 57-63; schema lines 3-31, 53-68; provider lines 140-180 | Whether decoder help and the full list are complete, capped, or filtered for `inspect-signal-decoders`; the catalog is complete only over successfully imported modules, and default paging caps responses at 50 while hard limits fail closed | mined | 2026-10-21 | 90d | .ufo/waves/round-23/w1/SigrokInventoryFields.md |
| S0xx | sigrok-cli 0.7.2 and libsigrokdecode 0.5.3 official release tarballs — https://sigrok.org/download/source/sigrok-cli/sigrok-cli-0.7.2.tar.gz ; https://sigrok.org/download/source/libsigrokdecode/libsigrokdecode-0.5.3.tar.gz | code | A | Producer grammar behind REA's parser: `--list-supported` prints one two-space id/longname line per decoder and description lines only at loglevel >= INFO; `--show` starts with `ID:`; decoder load-all ignores per-module import failures and scans system, user, and `SIGROKDECODE_DIR` paths; failures go to stderr | sigrok-cli sha256 71d0443f… (230,354 B); libsigrokdecode sha256 c50814aa… (892,783 B); show.c:55-60,193-207,875-884; options.c:27; decoder.c:679-700,1033-1071; srd.c:147-164,244-275; log.c:180-200 | Grounds the claimed catalog/help completeness, the 110-vs-112 directory accounting, and the warning that failed modules are omitted from coverage but visible only in `diagnostics` | mined | 2026-10-21 | 90d | .ufo/waves/round-23/w1/SigrokInventoryFields.md |
```

Exact used-by for the claim: this report's parser/schema findings; `.ufo/waves/round-23/evidence/c1/inventory.envelope.json` (`ev_940cf7bb…`, examined 110) and `.ufo/waves/round-23/evidence/c1/uart-help.envelope.json` (`ev_4be13793…`, examined 81). My probes confirm the same counts but are not new evidence rows. No claim is made here that `inspect-signal-decoders` is held; counting belongs to L1.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SigrokInventoryFields.md` — this report. Digest recorded in the final message after writing.
- No other retained outputs. Probe stdout/stderr were ephemeral under `/tmp` (digests above) and were deleted; the official source tarballs and their extraction trees were read-only inspection artifacts and were deleted. No files were written under `evidence/c1`, `runtime/`, `tools/`, or any production lane.

## Installs

- None. No pacman, npm global, uv, cargo, or release-binary install was performed. `npx -y rea-agents@6.5.0` used the pre-existing cache at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/`; it was invoked with `npm_config_offline=true`. Host pacman transactions are paused and were not attempted. Official sigrok tarballs were downloaded only for source reading (URLs and digests above), not installed.

## Open risks

1. **Identity gap.** Discovery Evidence hashes the configured command (here, a Bash wrapper). The wrapper could exec any binary; the executed `sigrok-cli` (`10fed05a…`), libsigrokdecode, and every decoder module are unhashed. The limitation text says modules are trusted/not fully fingerprinted, but the subject name alone does not tell a reader that the sigrok binary is outside the digest.
2. **Silent module omission.** `examined` counts loaded decoders only. The observed `signature` import failure is invisible in `output_window` and `matching`; only the free-text `diagnostics` retains it. A consumer that treats `examined` as "installed decoders" overstates coverage. No schema field counts failed or skipped modules.
3. **Environment-shaped inventory.** `SIGROKDECODE_DIR`, `XDG_DATA_HOME`, and `XDG_DATA_DIRS` are inherited by the probe. The recorded `tool` block does not capture search paths (they print only at debug loglevel), so two runs with the same command digest can list different decoders. The wrapper observed here sets `SIGROKDECODE_DIR` itself, which is why the bundle's decoders appear at all.
4. **Default help page hides options.** For `uart`, the default 50-line page ends exactly at `Options:`; every option line is on later pages. The contract description tells callers to use returned options, so a consumer must pass `--all` or page before using them. This is caller-visible through `has_more`, not a parser defect.
5. **Parser brittleness is fail-closed but total.** A future producer that appends another section after the decoder list, a decoder ID containing a character outside `[A-Za-z0-9_+-]` (the ID comes from the Python module attribute, not validated by libsigrokdecode), a long name containing a newline, or a duplicate `id` across two differently named modules makes the entire catalog request fail. No partial catalog is ever returned.
6. **Hard caps were read, not exercised.** The 65,536-line budget and 4 MiB combined-output failure paths are established from source (`parseDecoderDiscovery.js:8-11`, `ProviderProcess.js:344-365`, `ArtifactAnalysisResources.js:145-146`), not by a probe. A >4 MiB producer output is expected to fail the command, not return a truncated page; that expectation is `[INFERENCE]` from those lines.
7. **Version gate is shallow.** It checks only the `sigrok-cli 0.7.2` banner and the presence of the string `libsigrokdecode`; it does not check libsigrokdecode or Python versions. The observed bundle (libsigrokdecode 0.5.3, Python 3.5.2) passes while one decoder is lost to a numeric-literal syntax feature newer than its interpreter.
8. **Probe scope.** Probes used one bundled installation on this host and no device, recording, or acquisition. `--dont-scan` is a producer flag; its zero-device-enumeration guarantee is not established here (it remains an open question from R22 `PrimarySigrok.md`). No debugger, Frida, ADB, or target execution was used.
