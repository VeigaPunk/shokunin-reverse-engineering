<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/12-godot-arm64-scale.md. -->

# 12 — Godot ARM64 PE scale test (round 4)

Lane: kaidoku-shokunin, round 4. Date: 2026-10-13 (UTC-3 host). Host: Linux
x86_64, node v24.21.0, `rea-agents@6.4.0`, Ghidra 12.1.4 + JDK 21.0.12.1.
Round 3 held the 13.8 KB `cli-arm64.exe`; this round runs the reserve stress
target — the 91.6 MB Godot 4.7.2-stable `windows_release_arm64.exe` — to find
where the PE axis stops scaling. **Result: the axis boundary is the REA Ghidra
session deadline, not the format.** Auto-analysis never reached bridge
readiness inside `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000`; the verb died with a
typed `provider_timeout` envelope at 15m01.8s wall, exit 1. Not OOM.

Target identity (verified pre-run):

- `sha256sum` → `7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292`
  (matches the spawned Ghidra target name `target-7a2ccd688f6c.exe`).
- `file` → `PE32+ executable for MS Windows 6.00 (GUI), ARM64, 8 sections`;
  91,662,336 bytes (87.4 MiB).
- `llvm-readobj --file-headers` → `Format: COFF-ARM64`, `Machine:
  IMAGE_FILE_MACHINE_ARM64 (0xAA64)`, `SectionCount: 8`, `AddressOfEntryPoint:
  0x1000`, `ImageBase: 0x140000000`, `SizeOfImage: 93,822,976`, `SizeOfCode:
  69,538,816`, `Subsystem: WINDOWS_GUI`; DLL characteristics DYNAMIC_BASE /
  HIGH_ENTROPY_VA / NX_COMPAT / TERMINAL_SERVER_AWARE; export table at RVA
  0x548EC48, exception (.pdata) dir 0xABA30 B, .reloc 0x64DEC B.
- `llvm-readobj --sections` → `.text` 69,538,816 raw B (~66.3 MiB — ~17.4 M
  fixed-width insns upper bound), `.rdata` 20,611,584, `.data` 207,872,
  `.pdata` 703,488, `.tls` 41,472, `pck` 512 (Godot embedded-pack marker
  section), `.rsrc` 144,384, `.reloc` 413,184.

## Candidates

### Candidate 1 — scale boundary is the startup deadline: `provider_timeout` at 900 s — OBSERVED

- **claim:** `rea analyze` on the 91.6 MB ARM64 PE cannot finish Ghidra import +
  auto-analysis + bridge readiness inside a 900 s deadline; it fails with the
  typed envelope `{"error":"Analysis failed","code":"provider_timeout",
  "category":"timeout","retryable":true,"details":{"operation":"list_documents",
  "timeout_ms":900000}}`, exit 1 — the same projection the 90 s probe emits
  verbatim with `timeout_ms:90000`. This is a time boundary, not a format or
  memory refusal: the target passed admission (`NATIVE_AOT_MAX_SOURCE_BYTES =
  128 MiB`, `nativeAotPe.js:7` — 87.4 MiB file admitted), the loader mapped all
  8 sections, and Ghidra's auto-analysis was still progressing when killed.
- **source:** run log row 3 (wall `real 15m1.777s`, `user 28m25.316s`, `sys
  0m47.774s`, `EXIT=1`); filtered stdout artifact `/tmp/godot-arm64-analyze.json`
  = `{}` (3 B — `--filter-output` strips the error envelope because failure
  keys `error/code/category/message/retryable/remediation/details` are none of
  the requested summary paths); verbatim envelope from the 90 s probe
  `/tmp/godot-arm64-timeout-probe.json`; failure path traced in
  `rea-agents@6.4.0` dist: `ghidra/GhidraClient.js:607` + `GhidraClientStartup.js:25`
  (`failure("timeout","Ghidra startup deadline elapsed",{timeoutMs})`) →
  `GhidraProviderClient.js:470` (`kind === "timeout"` → `AnalysisTimeoutError`)
  → `domain/analysisErrorProjection.js:140` (`provider_timeout`, in
  `RETRYABLE_CODES` at :442) → `analysisErrorPresentation.js:122`
  (`category:"timeout"`).
- **verify:**
  - `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000 timeout 1500 npx -y rea-agents@6.4.0
    analyze <pe> --format json --filter-output '<summary keys>'` → real
    15m01.8s (≈ 900 s deadline + ~1.8 s teardown), exit 1. Outer `timeout 1500`
    did NOT fire (would be exit 124 at 25:00) — the kill is REA's internal
    session deadline, which `dist/config/ghidraStartupTimeout.js` documents as
    covering "Ghidra import, analysis, bridge, and readiness" (default
    330_000 ms).
  - Ghidra-side timeline from the live log `/tmp/rea-ghidra-hKzt9I/ghidra.log`
    (dir removed at `-deleteProject` cleanup): JVM spawned 13:47, `-import`
    done and `ANALYZING all memory and code` at 13:47:21 (~20 s import); PDB
    skipped (none embedded); auto-analysis then ran ~12.4 min: PngDataType
    error on `pck`-adjacent rsrc bytes (13:48:09), DecompileCallback pcode
    warnings (13:52), `VarnodeContext: out of address spaces` register-pressure
    errors (13:55:16–30, ~30 instances), ApplyDataArchiveAnalyzer applied
    `windows_vs12_64` + `rust-common` gdt (13:59:47), FidAnalyzer "No FID
    Libraries apply for language AARCH64:LE:64:v8A" (13:59:47 — language
    auto-detect correct). Killed mid-analysis ~14:02.
  - JVM observed: `java … AnalyzeHeadless -import target-7a2ccd688f6c.exe
    -readOnly -deleteProject`, `-Xmx2G` (default; overridable via
    `GHIDRA_HEADLESS_MAXMEM`/`GHIDRA_MAXMEM`, `GhidraJavaLaunch.js:53`); RSS
    peaked ~2.36 GB at 9.5 min, fell back to ~1.95 GB — no OOM signature in
    log, process was CPU-bound (~85–96%) not heap-floored when killed.
  - Probe: same command with `REA_GHIDRA_STARTUP_TIMEOUT_MS=90000` → real
    1m32.9s, exit 1, verbatim envelope above (operation `list_documents`,
    `timeout_ms:90000`) — identical code path, deterministic reproduction.
- **verified-at:** 2026-10-13T17:05Z
- **suggested:** admit — the PE axis has a measured scale boundary: a
  ~90 MB / ~70 MB-.text ARM64 PE exceeds the 900 s session envelope on this
  host (with three sibling Ghidra lanes concurrently resident — contention is
  real but representative of fleet conditions). Segment/procedure counts and
  evidence id are *absent by construction*: the session died before
  `list_documents` returned, so no Evidence was sealed. Follow-on `search` /
  `decompile` were NOT attempted — every verb spawns a fresh ephemeral
  `-deleteProject` session under the same deadline class; they would hit the
  identical wall. To push the boundary: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`
  to ~3600000 (bounded only by `MAX_TIMER_DELAY_MS` 2³¹−1) and/or
  `GHIDRA_HEADLESS_MAXMEM` to 6–8 G for a 100k+ procedure program, or wait for
  a quieter host. The `retryable:true` flag is honest — the failure is pure
  deadline, not capability.

### Candidate 2 — admission + language detection still correct at scale — OBSERVED

- **claim:** nothing in the front half of the pipeline mis-handles the big
  file: REA's target snapshot admission cap (`128 MiB`, `nativeAotPe.js:7`)
  accepts the binary; PeLoader mapped all 8 sections including Godot's custom
  `pck` section; Ghidra picked `AARCH64:LE:64:v8A` with zero FID libraries and
  ran the standard analyzer chain (ApplyDataArchiveAnalyzer, FidAnalyzer,
  decompiler-assisted passes) — identical in shape to the 13.8 KB exe's run,
  just past the deadline.
- **source:** ghidra.log excerpts in run log; `NATIVE_AOT_*` constants;
  small-exe control run this round (`ev_f4e02f93…` unchanged from r3 —
  `analysis_profile.parameters.upstream_analysis_profile.provider` = ghidra
  12.1.4, `architecture: "arm64"`, `import_mode: ephemeral-source-immutable`).
- **verify:** re-run `analyze` on the small `cli-arm64.exe` with the same
  filter — identical evidence id `ev_f4e02f932f3f6078d763d9ac3334632bd07731096388e798c86e86d33411facf`,
  7 segments / 136 procedures / 77 strings (12.1 s) — the provider itself is
  unchanged since r3; only target size differs.
- **verified-at:** 2026-10-13T16:50Z
- **suggested:** admit as the comparison anchor: the failure is strictly a
  size-vs-deadline interaction; ARM64 detection, admission, and analyzer
  selection all held at 91.6 MB.

## Run log

| # | Command | Wall | Result |
| - | ------- | ---- | ------ |
| 1 | `sha256sum`, `file`, `llvm-readobj --file-headers`, `llvm-readobj --sections` on `windows_release_arm64.exe` | <1 s | identity above: 0xAA64, 8 sections, 91,662,336 B, `.text` 69.5 MB, `pck` section present |
| 2 | `analyze …/cli-arm64.exe --format json --filter-output '<summary keys>'` (control + filter calibration) | 12.1 s | OK — `ev_f4e02f93…` (byte-identical to r3), `provider.id: rea-workflow`, 7/136/77 counts; learned `architecture` lives at `subject.architecture` / `analysis_profile…parameters.architecture`, not `normalized_result` |
| 3 | `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000 timeout 1500 npx -y rea-agents@6.4.0 analyze windows_release_arm64.exe --format json --filter-output 'evidence_id,…,normalized_result.segments,limitations,analysis_profile…'` (stdout→`/tmp/godot-arm64-analyze.json`) | **real 15m1.777s**, user 28m25.3s | **EXIT 1 — `provider_timeout`** (deadline 900000 ms). Filtered stdout = `{}`; live Ghidra log showed import@20 s then auto-analysis until kill; no evidence sealed |
| 4 | probe: same `analyze` with `REA_GHIDRA_STARTUP_TIMEOUT_MS=90000`, unfiltered | real 1m32.891s | EXIT 1 — verbatim `{"error":"Analysis failed","code":"provider_timeout","category":"timeout","message":"Analysis took too long. Try a smaller request, then run \`rea doctor\` if it continues.","retryable":true,"remediation":{"action":"Analysis took too long…"},"details":{"operation":"list_documents","timeout_ms":90000}}` |
| 5 | source trace of failure path | — | `GhidraClient.js:607` → `AnalysisTimeoutError` → `provider_timeout`/`timeout`/`retryable:true` (`analysisErrorProjection.js:140,442`, `analysisErrorPresentation.js:122`); startup deadline = import+analysis+bridge+readiness (`ghidraStartupTimeout.js:3`, default 330 s) |

Concurrent-host note: during run 3 the host also carried ≥3 other fleet
Ghidra JVMs (`op-2.34.1`, `op-2.40.0`, `signal-desktop` asar lane) plus
`demangler_gnu` — 30 GB RAM total, no swap pressure; the boundary measured is
under real fleet contention, not isolation.

## Summary

**The PE axis boundary at 91.6 MB is the session deadline — `provider_timeout`,
not a format, admission, or memory wall.** The Godot ARM64 export template
(sha256 `7a2ccd68…`, COFF-ARM64, 8 sections incl. a custom `pck` section, 69.5
MB `.text`) passed REA's 128 MiB source-snapshot admission, imported in ~20 s,
detected `AARCH64:LE:64:v8A` correctly, and was still inside Ghidra
auto-analysis when `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000` fired at
real 15m01.8s → exit 1 with the typed `provider_timeout` envelope
(`retryable:true`, `operation:list_documents`). No Evidence was sealed — no
evidence id, no segment/procedure counts — so `search`/`decompile` were
correctly skipped (each would re-pay the same doomed import). The small-exe
control (`cli-arm64.exe`, same filter, same provider chain) reproduced r3's
`ev_f4e02f93…` byte-for-byte, isolating size as the only variable.
Compare: r2 needed ~800 s for 33k-procedure Go binaries; a ~17M-instruction
ARM64 template plausibly needs 30–90 min — the knob is `REA_GHIDRA_STARTUP_TIMEOUT_MS`
(cap ~2³¹ ms) with `GHIDRA_HEADLESS_MAXMEM` heap headroom as the second
frontier. Practical reading for the fleet: REA's Ghidra path on this host tops
out somewhere between ~33k procedures/<800 s (works) and ~100k+ procedures/>900
s (doesn't) under load; the honest next probes are a ~2–5 MB PE binary and a
re-run at 3600 s on an idle host.
