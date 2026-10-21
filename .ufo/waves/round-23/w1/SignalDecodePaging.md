# SignalDecodePaging — sigrok decoder-annotation paging and the exact loss boundary

Seat: `KaidokuR23.SignalDecodePaging` (leaf scout, round-23 w1). Author-side inspection of the **installed REA parser**, not outside verification. Opened 2026-10-21. No REA CLI or MCP invocation (P3 exercises one internal capture module directly), no sigrok launch, no device/ADB contact, no target or carrier execution.

Scope question: where do `decode_signal_recording` decoder annotations get lost or truncated, and what exactly does `line_offset`/`line_limit` paging cover?

## Verdict

Paging is a **post-hoc window over the already-complete producer stdout**. It cannot page past a hard **4,194,304-byte combined stdout+stderr capture budget**: at 4,194,305 bytes the producer result is discarded and the whole decode fails as a resource-constraint error, so *no annotations are returned at all*. Within a successful capture there is **no line-count cap on annotations** (the 65,536-line budget belongs to `inspect_signal_decoders`, not decoding). The silent loss boundaries are narrower: invalid UTF-8 becomes U+FFFD with no flag in the report, line paging can split a multi-line annotation and drop its sample-range prefix, and a page beyond the end is indistinguishable from an empty page except by comparing `total_lines`.

This is internal REA behavior only. It is **not** T1 evidence for R23-C1 and supplies no external source row.

## Observed facts

All paths below are the installed npm package; versions verified from `package.json`.

### A. The window function (both installed copies identical)

`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/signals/annotationTextWindow.js` (v6.5.0, sha256 `11f176ad20202b8c66a045c513ad463f641ada69e8482472d31ca5cc65475cc7`, 31 lines):

- **:1** — documented as paging "literal LF-separated display lines without interpreting annotation semantics".
- **:7–18** — scans only `"\n"` via `indexOf`; CRLF is not normalized (`\r` stays in the text). `total` increments once per LF-terminated segment; a final segment without LF is counted once.
- **:10–11** — `start` is set only when `total === offset`; if `offset` never equals a line index (including `offset > total`), `start` remains `text.length`, so the page is empty.
- **:12–15** — `end` advances for every selected line; `limit === null` selects all remaining.
- **:22–24** — full-text windows are returned as the original string. Partial windows are copied through `Buffer.from(slice,"utf16le").toString("utf16le")`. Verified lossless for a lone surrogate and an astral code point (probe P2).
- **:28** — `has_more = min(offset,total) + returned < total`. With `offset > total`, `has_more` is `false` and `returned_lines` is `0`; the function does **not** report "offset out of range".

### B. The report schema

`.../dist/domain/signals/signalRecording.js` (v6.5.0, sha256 `0ef15149da472d82559d907bef4bbeabedd19c6de953978f6a04af48f4040171`):

- **:5–9** — each selector, including `annotations`, is one sigrok argument, 1–8192 chars, NUL rejected.
- **:17–20** — `annotations` maps to `--protocol-decoder-annotations=<value>`; REA does not validate annotation-class names against a decoder catalog.
- **:21–26** — `line_offset` nonnegative integer, default 0, **no maximum**.
- **:27–33** — `line_limit` positive integer or null, default **50**, **no maximum**; the description says "Lines are not annotation counts."
- **:35–48** — selector budget: `len(prefix)+len(value)+9` summed over the three non-null selectors must be ≤ 32,768 bytes. Prefix lengths: `--protocol-decoders=` 20, `--input-format=` 15, `--protocol-decoder-annotations=` 31. An `annotations` value alone may be at most 32,728 bytes of the budget, but is independently capped at 8,192 chars by **:5–9**.
- **:64–75** — `annotations_text` is literally "selected literal lines … not a lossless binary protocol representation"; `output_window` carries only `total_lines`, `returned_lines`, `has_more`; `total_lines` is explicitly display lines, "not annotation or sample counts".
- **:101–114** — `superRefine` recomputes the expected line count and rejects a report whose text/window disagree. This validates internal consistency, not producer completeness.

### C. Where the text comes from: whole-output capture, then window

`.../dist/signals/SigrokRecordingProvider.js` (v6.5.0, sha256 `7979bafb84b463d0fc3040d3643e08362326d67fd4543ee690679dc88b2dced7`, 339 lines):

- **:89–107** — one `runOwnedCommand` per sigrok invocation (version probe, then the decode), with `diagnosticBytes: LIMITS.output_bytes` and `acceptNonZeroExit: true`.
- **:191–202** — decode argv is `--dont-scan --input-file=recording --protocol-decoders=… --protocol-decoder-samplenum [--input-format=…] [--protocol-decoder-annotations=…]`. No sigrok-side paging or line cap is requested.
- **:203** — the **entire** producer run completes *before* any page is selected.
- **:211–220** — `windowAnnotationText(output.stdout.text, input.line_offset, input.line_limit)` is applied to the full captured stdout; `diagnostics` is the full captured stderr.
- **:228–233** — limitations state annotations are the decoder's interpretation; sample ranges/text are not parsed into a stream; "combined output at 4 MiB. Output overflow fails."

### D. The capture budget: exact arithmetic

`.../dist/process/LinuxResourceLimits.js` (sha256 `00980570c40ed7d911e9e71bf4aa064d244187d19a805e2db241a319e214bbd6`):

- **:10–17** — `BOUNDED_PRODUCER_LIMITS = { input_bytes: 32 MiB, output_bytes: 4*1024*1024 = 4,194,304, command_timeout_ms: 30,000, address_space_bytes: 1 GiB, file_bytes: 64 MiB, cpu_seconds: 30 }`.

`.../dist/process/ProviderProcess.js` (sha256 `cb5e08694201a121761965111b18d05af4cc1eb2696204ab92aab9fcf8d14ae4`):

- **:341–364** — `remaining = maxDiagnosticBytes − stdout.retainedBytes − stderr.retainedBytes`; each chunk retains only `min(chunkBytes, remaining)`; any shortfall sets `diagnosticTruncated` and emits `{truncated:true}`. The budget is **shared** by stdout and stderr, in arrival order.
- **:392–407** — retained bytes are decoded with `buffer.toString("utf8")`; an `invalidUtf8` flag is computed with a fatal `TextDecoder` and returned on the snapshot.

`.../dist/process/OwnedCommand.js` (sha256 `a0f3b29ddc6722ec2efaed79bb11723853e05e077aeeeaab5ccf9683bca2668e`):

- **:61–76** — any `truncated` output event sets `exceeded`.
- **:99–100** — after output closes, `exceeded` throws `OwnedCommandFailure("output-limit", …)` with a snapshot of the *partial* retained streams.
- **:101–110** — non-zero exit/signal is also a failure (provider asks to accept it only so it can wrap the failure itself).

`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/process/ArtifactAnalysisResources.js` (cited lines 127–146): `output-limit` is projected to `AnalysisResourceConstraintError(operation,"memory", …, { output_bytes: 4,194,304 }, detail)`, where `detail` includes `capturedOutput` (`stdout.text`, `stderr.text`, `truncated`, `exit_code`, `signal`).

`.../dist/signals/SigrokRecordingProvider.js:269–270` routes `OwnedCommandFailure` there. **Consequence:** a decode whose combined output exceeds the budget yields a typed failure, not a `signalRecordingSchema` report. There is no partial report and no page beyond the boundary.

### E. The adapter drops the invalid-UTF-8 marker

`ProviderProcess.js:406` computes `invalidUtf8: true` for the stream snapshot, but `SigrokRecordingProvider.js:108–114` (`capturedOutput`) and `:211–220` (report) copy only `stdout.text`, `stderr.text`, `truncated`, `exit_code`, `signal`. The `decode_signal_recording` report schema has no invalid-UTF-8 field (`signalRecording.js:56–99`, `strictObject`). So bytes that are not valid UTF-8 become U+FFFD and are indistinguishable from decoder-emitted U+FFFD. This is the one **silent byte-level loss inside an otherwise successful report**.

### F. Discovery paging is a different parser with different limits

`.../dist/signals/parseDecoderDiscovery.js` (sha256 `2fa74a0bacdff46f9155cf10320445fafeda9358b0efe9df2acbe13f3669097e`):

- **:6–11** — throws `DecoderDiscoveryBudgetError` when the 65,536th `"\n"` is examined, mapped at `SigrokRecordingProvider.js:261–267` to a memory constraint with `{line_budget: 65536}`. At most 65,535 LFs are accepted.
- **:12–14** — splits `/\r?\n/u` and pops one trailing empty line (CRLF normalized, unlike annotations).
- **:18–35** — catalog mode rejects a missing heading, malformed records, duplicates, or an empty catalog; no partial catalog is returned.
- **:40** — help `line_number` is 1-based over the **whole** help text before query filtering; paging `offset`/`limit` applies to matching help lines, so returned `line_number`s are non-contiguous.
- **:46–62** — `offset`/`limit` clamp to `matching.length`; `has_more = start+count < matching.length`.

The 4 MiB byte budget still applies first. For decoder help whose average line is at or under 64 bytes, the 65,536-LF budget can bind before 4 MiB; for normal catalogs, the byte budget binds first.

### G. Version comparison of the two installed copies

- `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` = **6.5.0**; `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` = **6.7.0**.
- `diff` of `domain/signals/annotationTextWindow.js` 6.5.0 vs 6.7.0 → no differences (exit 0).
- `diff` of `domain/signals/signalRecording.js` 6.5.0 vs 6.7.0 → no differences (exit 0).
- `diff` of `signals/SigrokRecordingProvider.js` 6.5.0 vs 6.7.0 → 7 changed lines, all cancellation-cause and cleanup-callback plumbing; no paging, budget, UTF-8, or schema change. 6.7.0 sha256 `b25a6d0a3c60cbbf0708c51a33d37d612d7d42f71665fb86099b3f91cfad42c8`, 346 lines.
- The MCP bundle embeds an identical window/schema (`mcp/toolContracts-BW05wpcr.js` sha256 `26cd1e1b009e13bffb1e6b018c8a9ef6a6605e287f2e56581d75f3306ce415cd`: window at 217–241, input shape 253–260, superRefine 310–318, tool description 400).
- **MCP delivery adds a separate transport boundary.** `mcp/main-kBXHZ8S5.js` (sha256 `12a70d8ab2a57de0cc71d794e38470031bfbdde855ba4a435e0ac0613f2fe82e`): `createEvidenceToolHandler` at 17791–17809 passes the schema-validated result to `ToolResultDelivery` (27247–27328). Its budget defaults to `STDIO_DEFAULT_MAX_BUFFER_SIZE` (10,485,760 bytes; `@modelcontextprotocol/server/dist/src-Cqbh3MYc.mjs:7159`) minus 1,024 = **10,484,736 bytes**, unless `mcpMaxResponseBytes` overrides it (68910, 69350). `encodeToolResult` (26958–26980) charges the structured JSON part **and** an escaped text copy (`JSON.stringify(part)`) against that budget. A 4 MiB `annotations_text` made mostly of LF characters serializes as ~4 MiB structured plus ~8 MiB escaped, exceeding the default budget, so `successResult` (27307–27328) returns an `AnalysisResourceConstraintError` with `boundary: "mcp-response"`, `constraint: "receive-buffer"`, and "The analysis result was not truncated." The CLI `--format json --full-output` path has no such budget.

### H. CLI presentation

`.../dist/cli/signalCommands.js` (sha256 `f033461c4c136296b4abeb3315e8572438a5654bc7615283626abf0b671b3eef`):

- **:44–53** — the CLI override makes `line_limit` positive + optional, so it is not nullable at the CLI layer; an omitted value falls through to the decode schema's default **50**, and `--all-lines` is a separate boolean.
- **:55–61** — `--all-lines` and `--line-limit` are mutually exclusive.
- **:64–68** — `--all-lines` maps to `line_limit: null`.
- With `--format json --full-output`, a successful result is `{ok:true,data,meta}` and is not token-sliced (`dist/cli/cliResultOutput.js:134–139`; `fullFailureEnvelope` slicing at 172–187 applies only to failures and only when `--token-limit/--token-offset` are supplied).

## Exact loss / truncation boundary

Let `S` = retained stdout bytes, `E` = retained stderr bytes, `B = 4,194,304`.

1. **Success boundary.** Given a configured `REA_SIGROK_COMMAND` that passes the `sigrok-cli 0.7.2 + libsigrokdecode` gate and a working `prlimit`, a decode returns a report iff `S + E ≤ B`, exit code 0, wall clock < 30,000 ms, CPU < 30 s, address space ≤ 1 GiB, and the private recording copy is unchanged. Verified at `S+E = B` exactly (probe P3-D, success) and `S+E = B+1` (probe P3-B/P3-C, `output-limit`, failure). P3 exercised the real capture supervisor with the configured limits but did not wrap the child in `prlimit`; the byte-budget behavior is independent of that wrapper.
2. **Annotations available to any page:** at most `B − E` stdout bytes. Stderr consumes the same budget 1:1; warnings shrink the annotation allowance. At the boundary, the chunk that arrives when the budget is exhausted is cut, so retained stdout can end **mid-line and mid-codepoint** (`ProviderProcess.js:347–354`). That partial text is available only as `captured_output` on the failure, never as a page.
3. **Line-count cap on annotations:** none. The only count limit is bytes. With non-empty LF-terminated lines the maximum is `floor((B−E)/2)` lines (2 bytes minimum per line); with empty lines (`"\n"`) it is `B−E` lines. There is no 65,536-line cap on this path.
4. **Page semantics:** `line_offset` skips completed LF-separated segments; `line_limit: null` returns all remaining retained lines; `line_limit` may exceed the total. `offset > total` returns `""`, `returned_lines: 0`, `has_more: false`, while `total_lines` still reports the true count — an out-of-range page is not flagged.
5. **Unaddressable phantom line:** text ending in `"\n"` has no extra empty line; `"x\n\n"` reports `total_lines: 2`, and `offset: 2` returns empty with `returned 0` (probe P1). A trailing LF-terminated line is counted; the position after it is not.
6. **Silent substitution:** any non-UTF-8 byte in either stream becomes U+FFFD in `annotations_text`/`diagnostics`, with no report flag. A partial multibyte sequence cut at the byte budget is likewise replaced, and on the failure path its origin is unknowable.
7. **Annotation completeness:** lines are not annotation records. A page boundary inside a multi-line annotation yields continuation text without that annotation's sample-range prefix (inference: depends on the decoder emitting embedded newlines, unobserved). `total_lines` cannot tell a caller how many annotations or samples a page covers.
8. **Selector boundary:** `annotations`/`decoders`/`input_format` combined must fit `len(prefix)+len(value)+9 ≤ 32,768`, and each value ≤ 8,192 chars. Longer annotation-class selections are rejected before any run.
9. **MCP-only transport boundary:** the provider may succeed while the MCP result is refused. `ToolResultDelivery` charges both structured JSON and its escaped text copy against `mcpMaxResponseBytes − 1,024` (default 10,484,736). Worst-case LF-heavy 4 MiB text is ~12 MiB encoded, so `line_limit: null` on a large decode can return `resource_constraint`/`transport` with `boundary: "mcp-response"` and `constraint: "receive-buffer"` instead of annotations. The result is not truncated; it is replaced by that error. The CLI `--format json --full-output` path has no such budget.

## Empirical probes

Cwd `/tmp` for all; no environment overrides (child and probe inherited `process.env`); Node **v24.21.0**. Every probe process exited **0**; the `ok:false` lines below are REA's rejection of the child, with the child's own exit shown as `exit:0`.

P1 — window edge cases (actual argv: `node --input-type=module -e 'import { windowAnnotationText as w } from ".../dist/domain/signals/annotationTextWindow.js"; …cases…'`), exact printed results:

```
""       0 null  {"annotations_text":"","output_window":{"total_lines":0,"returned_lines":0,"has_more":false}}
""       0 0     {"annotations_text":"","output_window":{"total_lines":0,"returned_lines":0,"has_more":false}}
"a\n"    0 null  {"annotations_text":"a\n","output_window":{"total_lines":1,"returned_lines":1,"has_more":false}}
"a\n"    1 null  {"annotations_text":"","output_window":{"total_lines":1,"returned_lines":0,"has_more":false}}
"a\n"    2 null  {"annotations_text":"","output_window":{"total_lines":1,"returned_lines":0,"has_more":false}}
"a\nb"   0 null  {"annotations_text":"a\nb","output_window":{"total_lines":2,"returned_lines":2,"has_more":false}}
"a\nb"   1 1     {"annotations_text":"b","output_window":{"total_lines":2,"returned_lines":1,"has_more":false}}
"a\nb"   0 1     {"annotations_text":"a\n","output_window":{"total_lines":2,"returned_lines":1,"has_more":true}}
"a\r\nb\r\n" 0 null {"annotations_text":"a\r\nb\r\n","output_window":{"total_lines":2,"returned_lines":2,"has_more":false}}
"x\n\n"  0 null  {"annotations_text":"x\n\n","output_window":{"total_lines":2,"returned_lines":2,"has_more":false}}
"x\n\n"  1 1     {"annotations_text":"\n","output_window":{"total_lines":2,"returned_lines":1,"has_more":false}}
"x\n\n"  2 1     {"annotations_text":"","output_window":{"total_lines":2,"returned_lines":0,"has_more":false}}
"x\n\n"  3 1     {"annotations_text":"","output_window":{"total_lines":2,"returned_lines":0,"has_more":false}}
```

P2 — copy path and budget constants: `w("L1\u{1F600}X\nL2\n",0,1)` returned `"L1😀X\n"`; `w("A\uD800B\nC\n",0,1)` returned a string whose UTF-16 units are `41 d800 42 0a`; full-window identity held. Prefix lengths printed `20/15/31`; max standalone `annotations` value from the selector budget `32728` bytes.

P3 — capture boundary (actual argv: `node --input-type=module -e 'import { runOwnedCommand } from ".../dist/process/OwnedCommand.js"; …'`), using the real default `spawnOwnedProviderProcess` launcher and the same limits as `BOUNDED_PRODUCER_LIMITS` (`timeoutMs:30000, diagnosticBytes:4194304, acceptNonZeroExit:true`); children were local `node -e` writers, no target/carrier:

```
A_stdout_exactly_4MiB        {"ok":true,"stdoutBytes":4194304,"stdoutObserved":4194304,"stderrBytes":0,"truncated":false,"invalidUtf8":false,"exit":0}
B_stdout_4MiB_plus_1         {"ok":false,"reason":"output-limit","stdoutBytes":4194304,"stdoutObserved":4194305,"stderrBytes":0,"truncated":true,"exit":0}
C_stdout_plus_stderr_total_plus1 {"ok":false,"reason":"output-limit","stdoutBytes":4193999,"stdoutObserved":4194000,"stderrBytes":305,"truncated":true,"exit":0}
D_total_exactly_4MiB         {"ok":true,"stdoutBytes":4194294,"stdoutObserved":4194294,"stderrBytes":10,"truncated":false,"invalidUtf8":false,"exit":0}
E_invalid_utf8_stdout        {"ok":true,"stdoutBytes":3,"stdoutObserved":3,"stderrBytes":0,"truncated":false,"invalidUtf8":true,"exit":0}
```

Case C retained exactly `4,193,999 + 305 = 4,194,304` bytes while the child wrote `4,194,000 + 305 = 4,194,305`; the stream snapshot reports `truncated:true`. Case E proves the snapshot computes `invalidUtf8:true` while the adapter's report/captured-output object has no slot for it (`SigrokRecordingProvider.js:108–114`).

Host availability check (context, not a failure of this seat): `command -v sigrok-cli` printed nothing (exit 1); `python3 -c "import sigrokdecode"` → `ModuleNotFoundError` (exit 1). No runnable sigrok was used.

## Explicit unknowns

- **sigrok-cli 0.7.2 producer behavior was not observed.** Whether an unknown value in `--protocol-decoder-annotations`, an unknown decoder option, or a decoder runtime error exits non-zero, warns on stderr, or silently emits nothing is unestablished here. REA converts non-zero exit to a typed failure with `captured_output`; exit-zero decoder-side drops would appear only in `diagnostics`.
- **Whether sigrok decoders emit embedded newlines inside one annotation** is unobserved; the "page can split an annotation" hazard is therefore `[INFERENCE]`, not observed loss.
- **Whether a real recording can produce >4 MiB of annotations** was not exercised; the failure mapping is code-observed and probe-observed at the capture layer, not with sigrok.
- **The operator's actual MCP response budget and client receive buffer** are configuration values not read here; the default is code-observed (10,485,760 − 1,024), and the CLI full-output path avoids the boundary entirely.
- **Dynamic/debugger ownership** remains adjacent and unresolved, per wave boundary.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SignalDecodePaging.md` (this report; no other outputs written). Its own sha256 is reported in the seat's final message because embedding it would change the file's digest.
- No probe artifacts: probes were inline `node -e`, wrote no files; all inspected-file digests are listed in sections A–H.

## Installs

None. No pacman/uv/npx/global install or config edit; host pacman transactions untouched.

## Open risks

- Treating `line_offset`/`line_limit` as a way to read a decode larger than 4 MiB is false; the run fails before paging.
- Mistaking the failure's `captured_output.stdout` (first ≤4 MiB, possibly cut mid-line/mid-codepoint, `truncated:true`) for a valid page.
- Forgetting stderr shares the 4 MiB budget, so warning volume reduces annotation capacity.
- Treating a `U+FFFD` in `annotations_text` as decoder output when it may be the adapter's UTF-8 decode of arbitrary annotation bytes.
- Equating `total_lines` with annotation count or sample coverage, or assuming a page boundary aligns with an annotation.
- Using `line_limit: null` over MCP on a large successful decode: the provider result may be replaced by an MCP `resource_constraint`/`transport` error because the structured-plus-escaped response exceeds the default 10,484,736-byte budget; the CLI `--format json --full-output` path does not have this boundary.

Report: `.ufo/waves/round-23/w1/SignalDecodePaging.md`
