<!-- corpus entry — kaidoku-shokunin round 5 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r5/05-riscv-deep.md. Landed with this lane's independent re-verification (run log below); heavy multi-minute runs cited from the wave and marked [wave]. -->

# kaidoku-r5 · 01-riscv-bypass — `target_unavailable` IS bypassable: 2-byte `e_machine` patch + `REA_GHIDRA_LANGUAGE_ID=RISCV:LE:64:default` yields real RISC-V analysis through REA (94 procedures on a 766 KB slice); direct `analyzeHeadless` needs no patch at all (10,766 functions / 3.14 M instructions on the full 29 MB EXEC)

Axes: **coverage** (RISC-V moves refused → analyzed — REA-routed on bounded slices, direct-Ghidra on the full file), **evidence-fidelity** (the bypass provably works, but the Evidence envelope's `subject.architecture` records the patched value "arm64" — provenance is honest only if the patch is declared), **boundary-precision** (refusal pinned to `dist/domain/binaryTarget.js:105` + the `elfArchitecture` allowlist `:208-222`), **failure-honesty** (honesty tax recorded, ≲1 MB REA-route slice limit, three dead ends verbatim).

Env: `rea-agents@6.4.0` via npx — the three npx-cache copies re-verified md5-identical on `dist/domain/binaryTarget.js` (`b7f89a097373800728bcefb7d673f4f7`) by this lane. Ghidra 12.1.4 at `~/.local/opt/ghidra_12.1.4_PUBLIC`, `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`. Host: Linux x86_64, 32 cores. Date: 2026-10-13.

Subjects (`sha256sum` re-run by this lane, all matching the wave byte-for-byte):
- `/usr/lib/firmware/nvidia/610.57.04/gsp_tu10x.bin` (outer REL wrapper) 29,381,504 B `d157e3b7dd5da2ca8d1ccb6ca98958f9e35d10a9ef7326277ebac133e4b0d1a7`
- `/tmp/r4u-embedded-elf.bin` (r4u truncated EXEC carve) 766,595 B `a92cab9be14e5d3a80f9b64b589c0e9d61d334ac58f1e10d4d4ec2c96b92aad1`
- `/tmp/r5-gsp-tu10x-exec-full.bin` (full EXEC carve @ offset 64) 29,367,752 B `eb4d76c4c3bb3045bafff132c6e4c1d04a538ab32e22a009134843a1fa5acefe`
- `/tmp/r5-embedded-elf-arm64patch.bin` (766 KB carve, e_machine 243→183) `9eb8fc34a47875020ac486bacd65e11c357e01fa4eda20427816758fce635ee1`
- `/tmp/r5-gsp-tu10x-exec-arm64patch.bin` (29 MB EXEC, e_machine 243→183) `1aa4061cfc8ab339cd5a2fe122d301dfc6bd4cdfae8b08e34e3cd8e761bbf997`
- `/tmp/r5-embedded-elf.hop` (truncated carve renamed; bytes identical to `a92cab9b…`)

## Run log (this lane's re-verification; original discovery commands: `.ufo/waves/kaidoku-r5/05-riscv-deep.md` run log)

| # | Command | Result |
| - | ------- | ------ |
| 1 | `sha256sum` on the six subjects above | all match the wave (incl. `gsp_tu10x.bin` at `/usr/lib/firmware/nvidia/610.57.04/`) |
| 2 | `md5sum ~/.npm/_npx/*/node_modules/rea-agents/dist/domain/binaryTarget.js` | three copies identical `b7f89a09…`; `package.json` version 6.4.0 ×3 |
| 3 | `sed -n '91,105p;208,222p' …/dist/domain/binaryTarget.js` | gate confirmed verbatim at the cited lines (candidate 1) |
| 4 | `npx -y rea-agents@6.4.0 analyze /tmp/r4u-embedded-elf.bin --format json` | RC=1 `target_unavailable` "unsupported ELF architecture" — refusal stands on the unpatched carve (`/tmp/r5v-refusal.json`) |
| 5 | `cp /tmp/r4u-embedded-elf.bin /tmp/r5v-reverify.bin && printf '\xb7\x00' \| dd of=… bs=1 seek=18 conv=notrunc` | patched copy sha256 `9eb8fc34…` — the `dd` patch reproduces the wave's python patch byte-identically; on-disk offset 18: `f3 00` → `b7 00` (xxd) |
| 6 | `REA_GHIDRA_LANGUAGE_ID=RISCV:LE:64:default npx -y rea-agents@6.4.0 analyze /tmp/r5v-reverify.bin --format json` | RC=0, `ev_e9a735a2…31df6` (id identical to the wave's), `language_id:"RISCV:LE:64:default"`, `language_selection:"configured-v1"`, **94 procedures**, 8 segments incl. `csr` `csreg:0x0–0x8000`, `subject.architecture:"arm64"` (`/tmp/r5v-bypass.json`) |
| 7 | same command, no env (control) | RC=0, `ev_73581d6b…` (identical to wave), `language_id:"auto-from-header"`, `language_selection` absent, **0 procedures** (`/tmp/r5v-control.json`) |
| 8 | `REA_GHIDRA_LANGUAGE_ID=… npx -y rea-agents@6.4.0 inspect /tmp/r5v-reverify.bin --format json` | RC=0 same shape: `ev_e9a735a2…`, 94 procedures (`/tmp/r5v-inspect.json`) — verb breadth ≥2 |
| 9 | `analyzeHeadless /tmp/r5-ghidra-proj2 r5full -process r5-gsp-tu10x-exec-full.bin -noanalysis -postScript R5Counts.java -scriptPath /tmp/r5-ghidra-scripts -readOnly` (~2 s) | `R5_LANG=RISCV:LE:64:default`, `R5_CSPEC=gcc`, `R5_BLOCKS=39 R5_TOTAL_BYTES=29932990`, `.section_task_rm_elf_text_instance ram:04bfa000 size 16732160 exec=true`, **`R5_FUNCTIONS=10766 R5_INSTRUCTIONS=3141043 R5_DEFINED_DATA=37455 R5_SYMBOLS=42057`** |
| 10 | same with `R5Entry.java` | entry `ram:04009000`: `addiw t0,zero,0x1; slli t0,t0,0x31; addi t0,t0,0x1; slli t0,t0,0xc; addi t0,t0,-0x600; lw t0,0x0(t0); srli t0,t0,0x14 …` — coherent RV64 (hardware-ID read) |
| 11 | `cp → /tmp/r5v-reverify.hop; rea analyze` | RC=1 `provider_unavailable`; candidates `[ghidra,hopper,ida]`, rejections verbatim (candidate 6) |
| 12 | `rea analyze --help`; `rea capabilities --format json \| grep -ioc riscv` | `--target-format` = "Explicit headerless DOS COM interpretation" only; capabilities: 0 `riscv` tokens |

## Candidate: the refusal is a hard-coded 5-member `e_machine` allowlist in REA's ELF preflight — `dist/domain/binaryTarget.js:105` fires `unsupported ELF architecture` because `elfArchitecture()` (`:208-222`) has no EM_RISCV=243 case

- claim: **OBSERVATION** (re-read at the cited lines; all three npx copies identical): `dist/domain/binaryTarget.js` — `parseElf` (line 91) reads `e_machine` at offset 18 (line 102) → `elfArchitecture(machine)` (line 103) → `if (architecture === undefined) return err("unsupported ELF architecture")` at **line 105**. The switch at **lines 208–222** maps exactly {3:x86, 62:x86_64, 8:mips, 40:arm, 183:arm64} then `return undefined` — 243 has no case. `dist/domain/binaryTargetTypes.js:2-8` `BINARY_ARCHITECTURES = ["x86","x86_64","arm","arm64","mips"]` corroborates. Call site `application/BinaryTargetResolver.js:256` (`parseExecutableHeader`) inside `parseBinaryTarget`, whose docstring (`:16`) says it runs "before a provider is selected"; a `BinaryTargetError` with no `systemCode` projects to `target_unavailable` at `domain/analysisErrorProjection.js:69-71`. Live refusal re-run on the unpatched carve: RC=1, `details.reason:"unsupported ELF architecture"` (run log 4) — unchanged in 6.4.0. **INFERENCE**: the gate is a parse-time allowlist ahead of any provider, so it cannot be configured away — only satisfied (patch the header) or bypassed (leave REA).
- source: this lane's `sed` reads at `~/.npm/_npx/*/node_modules/rea-agents/dist/`; `/tmp/r5v-refusal.json`; wave `05-riscv-deep.md` candidate 2.
- verify: `sed -n '91,105p;208,222p' ~/.npm/_npx/*/node_modules/rea-agents/dist/domain/binaryTarget.js && npx -y rea-agents@6.4.0 analyze /tmp/r4u-embedded-elf.bin --format json; echo $?` → allowlist verbatim, RC=1.
- verified-at: 2026-10-13

## Candidate: bypass #1 (REA route, bounded slices) — patch `e_machine` 243→183 in a COPY + `REA_GHIDRA_LANGUAGE_ID=RISCV:LE:64:default` → `rea analyze` RC=0 with real RISC-V analysis: 94 procedures + a `csr` block on the 766 KB carve

- claim: **OBSERVATION** (re-executed end-to-end on a fresh copy): the env knob exists — `config/parseConfig.js:64-72` maps `REA_GHIDRA_LANGUAGE_ID` → `config.ghidraLanguageOverride` (plus optional `REA_GHIDRA_COMPILER_SPEC_ID`), and `ghidra/GhidraLauncher.js:255-262` emits `-processor <languageId>` (+ `-cspec`) in the analyzeHeadless argv when set. Recipe: `printf '\xb7\x00' | dd of=<copy> bs=1 seek=18 conv=notrunc`, then `REA_GHIDRA_LANGUAGE_ID=RISCV:LE:64:default rea analyze <copy> --format json`. Result: RC=0, evidence `ev_e9a735a2975120e5a8f06393808b0a3ddcf76a8944b7b515f7c34649d7b31df6` — the wave's exact id — with `analysis_profile…language_id:"RISCV:LE:64:default"`, `language_selection:"configured-v1"`, `procedure_count:94`, `segment_count:8` including the `csr` block `csreg:0x0–csreg:0x8000` (32,768 B — the RISCV module's CSR register space). `rea inspect` on the same target reproduces the result shape (`ev_e9a735a2…`, 94 procedures) — the bypass holds across ≥2 verbs (run log 6, 8). Ghidra side pins: `Ghidra/Processors/RISCV/data/languages/riscv.ldefs` carries `id="RISCV:LE:64:default"`, `riscv64-fp.cspec` present (existence re-checked). **INFERENCE**: the 2-byte patch only satisfies `elfArchitecture()`; the env override is the active ingredient steering Ghidra to RISCV — isolated by the control below.
- source: `/tmp/r5v-bypass.json`, `/tmp/r5v-inspect.json` (this lane); wave `05-riscv-deep.md` candidate 3 (`/tmp/r5-bypass-analyze.json`, `/tmp/r5-bypass-inspect.json`); Ghidra `Ghidra/Processors/RISCV/data/languages/`.
- verify: `cp /tmp/r4u-embedded-elf.bin /tmp/x.bin && printf '\xb7\x00' | dd of=/tmp/x.bin bs=1 seek=18 conv=notrunc status=none && sha256sum /tmp/x.bin && REA_GHIDRA_LANGUAGE_ID=RISCV:LE:64:default npx -y rea-agents@6.4.0 analyze /tmp/x.bin --format json` → sha256 `9eb8fc34…`, `language_id:"RISCV:LE:64:default"`, `procedure_count:94`.
- verified-at: 2026-10-13

## Candidate: control A/B — patched bytes WITHOUT the override → `auto-from-header` (arm64), 0 procedures; the env var is what makes it RISC-V

- claim: **OBSERVATION** (re-run): same patched file, no env → RC=0, `language_id:"auto-from-header"`, `language_selection` absent, `procedure_count:0`. Paired with candidate 2: identical bytes, identical verb, only the env var differs — **0 vs 94 procedures**. **INFERENCE**: the e_machine patch opens REA's gate; `REA_GHIDRA_LANGUAGE_ID` steers Ghidra's language back to RISCV despite the patched header (Ghidra would otherwise auto-select AARCH64 from the patched e_machine).
- source: `/tmp/r5v-control.json` (this lane); `/tmp/r5-control-arm64.json` (wave).
- verify: `npx -y rea-agents@6.4.0 analyze /tmp/r5-embedded-elf-arm64patch.bin --format json | python3 -c 'import json,sys;d=json.load(sys.stdin);up=d["analysis_profile"]["parameters"]["upstream_analysis_profile"]["parameters"];print(up["language_id"],d["normalized_result"]["procedure_count"])'` → `auto-from-header 0`.
- verified-at: 2026-10-13

## Candidate: honesty tax — the Evidence envelope records the PATCHED identity: `subject.architecture:"arm64"` and the patched copy's sha256

- claim: **OBSERVATION** (re-read from this lane's own fresh envelope): `subject.architecture = "arm64"`, `subject.digest.sha256 = 9eb8fc34…` (the patched copy) in `/tmp/r5v-bypass.json`; the `analysis_profile` likewise records `architecture:"arm64"`. **UNKNOWN**: no envelope field flags the 2-byte mutation. **INFERENCE**: REA's identity record lies wherever the patch does — the analysis itself is honest RISC-V (RISCV language id, 94 procedures, `csr` block) but the manifest is not. Rule for consumers: declare the patch wherever evidence from this route is cited.
- source: `/tmp/r5v-bypass.json` `subject` block; wave `05-riscv-deep.md` candidate 3 caveat.
- verify: `python3 -c 'import json;d=json.load(open("/tmp/r5v-bypass.json"));print(d["subject"]["architecture"],d["subject"]["digest"]["sha256"])'` → `arm64 9eb8fc34…`.
- verified-at: 2026-10-13

## Candidate: bypass #2 (no patch, around REA) — `analyzeHeadless` accepts the unpatched carved EXEC natively (`RISCV:LE:64:default:gcc` auto-detected) and the saved-program counts re-verify: 39 blocks / 10,766 functions / 3,141,043 instructions / 37,455 data / 42,057 symbols, entry = readable RV64

- claim: **OBSERVATION** (counts replay re-run on the wave's saved project, ~2 s): `analyzeHeadless /tmp/r5-ghidra-proj2 r5full -process r5-gsp-tu10x-exec-full.bin -noanalysis -postScript R5Counts.java -scriptPath /tmp/r5-ghidra-scripts -readOnly` → `R5_LANG=RISCV:LE:64:default`, `R5_CSPEC=gcc`, `R5_BLOCKS=39`, `R5_TOTAL_BYTES=29932990`, exec block `.section_task_rm_elf_text_instance` @`ram:04bfa000` size 16,732,160 (the ~16 MB RM task text; `.ga100_text`/`.tu10x_text`/`.bootstrap` also present), **`R5_FUNCTIONS=10766 R5_INSTRUCTIONS=3141043 R5_DEFINED_DATA=37455 R5_SYMBOLS=42057`**. `R5Entry.java` re-run: entry @`ram:04009000` disassembles `addiw t0,zero,0x1; slli t0,t0,0x31; addi …; lw t0,0x0(t0); srli t0,t0,0x14 …` — coherent RV64 (hardware-ID read+compare). **[wave] OBSERVATION** (multi-minute, not repeated): those counts came from a 900 s-capped auto-analysis (`-analysisTimeoutPerFile 900`) that timed out incomplete and saved partial state to the project — full-function analysis of 29 MB needs a longer budget; the outer REL wrapper also imports (RC=0, same auto-detected language) but sections-only (0 program headers), so the carved EXEC is the right target. **INFERENCE**: Ghidra's RISCV module is fully working on this host; REA's preflight is the only wall, and the full EXEC belongs to direct `analyzeHeadless`.
- source: this lane run log 9–10 (saved project `/tmp/r5-ghidra-proj2/r5full`, scripts `/tmp/r5-ghidra-scripts/R5Counts.java`+`R5Entry.java`); wave `05-riscv-deep.md` candidate 5 (`/tmp/r5-ghidra-run.out`, `/tmp/r5-ghidra-analysis.log`).
- verify: the exact `-process … -postScript R5Counts.java … -readOnly` command above (needs only Ghidra + the saved project) → the `R5_*` lines verbatim.
- verified-at: 2026-10-13

## Candidate: REA-route scaling limit — the full 29 MB patched EXEC dies in REA at typed `provider_timeout` (`operation:"list_documents"`) at `timeout_ms:330000` default and `1800000` raised; keep REA-routed slices ≲1 MB

- claim: **OBSERVATION** (envelopes re-read; the ≥30-min waits not repeated): `config/ghidraStartupTimeout.js:3` — `DEFAULT_GHIDRA_STARTUP_TIMEOUT_MS = 330_000`, docstring "absolute deadline for Ghidra import, analysis, bridge, and readiness"; raised via `REA_GHIDRA_STARTUP_TIMEOUT_MS` (plumbed at `config/parseConfig.js:63`). `/tmp/r5-bypass-full-analyze.json` [wave]: `{"code":"provider_timeout",…,"details":{"operation":"list_documents","timeout_ms":330000}}`; `…-analyze2.json` [wave]: same envelope with `timeout_ms:1800000` — the override provably propagated (330000→1800000) and analysis still wasn't done. Consistent with the direct run's 900 s auto-analysis timeout: ~17 MB of execute-section RV64 exceeds half an hour under REA's launch profile. **INFERENCE**: bypass #1 is mechanically size-independent but practically bounded — comfortable at 766 KB (94 procedures; ~50 s end-to-end cold per the wave, seconds warm on re-run); the full EXEC belongs to bypass #2.
- source: `/tmp/r5-bypass-full-analyze.json`, `/tmp/r5-bypass-full-analyze2.json` (wave envelopes, re-read); dist pins `config/ghidraStartupTimeout.js:3`, `config/parseConfig.js:63`; wave `05-riscv-deep.md` candidate 6.
- verify: [wave; heavy] `REA_GHIDRA_STARTUP_TIMEOUT_MS=1800000 rea analyze /tmp/r5-gsp-tu10x-exec-arm64patch.bin --format json` → RC=1 `provider_timeout` `timeout_ms:1800000` after ≥30 min. Cheap proxy: `python3 -c 'import json;print(json.load(open("/tmp/r5-bypass-full-analyze2.json"))["details"])'`.
- verified-at: 2026-10-13

## Candidate: three dead ends, pinned — `.hop` rename skips the ELF parse but every provider refuses `database` kind; `--target-format` is dos-com-only capped at 0xff00 B; `extract-firmware --offset/--length` verifies a slice's sha256 but publishes 0 files

- claim: (i) **OBSERVATION** (re-run): `cp r4u-embedded-elf.bin x.hop; rea analyze x.hop` → RC=1 `provider_unavailable`; `BinaryTargetResolver.js:61-69` routes `.hop` to `kind:"database"` (`architecture:null` — RISC-V never checked), candidates `[ghidra,hopper,ida]` all reject: ghidra `target_kind_unsupported` "Ghidra v1 imports executable targets, not database targets.", hopper `executable_missing` (`/opt/hopper/bin/Hopper`), ida `not_configured` (set `REA_IDA_MCP_CONFIG`) plus a second ida `target_kind_unsupported`. Parse bypass exists; no provider accepts it. (ii) **OBSERVATION** (re-run + dist): `rea analyze --help` offers only "Explicit headerless DOS COM interpretation" for `--target-format`; `domain/dosCom.js:6` caps length at `0xff00` — no ELF (766 KB or 29 MB) can ride it. (iii) **OBSERVATION** (envelope re-read, not re-run): `extract-firmware gsp_tu10x.bin <dir> --offset 64 --length 29367752` [wave] → RC=0 `coverage:"complete"`, `selection.sha256 == eb4d76c4…` (byte-identical to the `tail|head` carve), unblob chunk `handler:"elf64"` — but `files:[]`, `published_bytes:0`: unblob's elf64 handler recognizes yet cannot decompose the ELF, so the verb proves the slice without emitting it. `dd`/`tail` remains the carving method. **INFERENCE**: there is no unmodified-artifact path through REA for RISC-V — the only REA route is the documented 2-byte patch + env override, else direct Ghidra.
- source: `/tmp/r5v-hop.json` (this lane); `/tmp/r5-ef-carve.json` (wave, re-read); `rea analyze --help` output; wave `05-riscv-deep.md` candidate 7.
- verify: `cp /tmp/r4u-embedded-elf.bin /tmp/x.hop && npx -y rea-agents@6.4.0 analyze /tmp/x.hop --format json; echo $?` → RC=1 with the rejections listed above.
- verified-at: 2026-10-13

## Aside: evidence ids were path-stable on this lane's re-runs

- **OBSERVATION**: this lane's `analyze`/`inspect` re-runs executed on a different path (`/tmp/r5v-reverify.bin`) than the wave's (`/tmp/r5-embedded-elf-arm64patch.bin`) with byte-identical content — and minted the identical evidence ids (`ev_e9a735a2…`, `ev_73581d6b…`). For these verbs on identical bytes+params, the id tracked content, not path. **UNKNOWN** whether the r4 path-sensitivity note (`corpus/README.md:133`) applies only to other verbs or param shapes — recorded as a nuance; no corpus claim edited here.
- verify: re-run candidate 2's verify from any path; compare `evidence_id` to `ev_e9a735a2…`.

## Summary

- **The wall is a parse-time allowlist, not a missing engine** — `dist/domain/binaryTarget.js:105` refuses any ELF whose `e_machine` misses {3, 62, 8, 40, 183} (`:208-222`); EM_RISCV=243 falls through and projects to `target_unavailable` (`domain/analysisErrorProjection.js:69-71`) before any provider is consulted (`application/BinaryTargetResolver.js:256`, docstring `:16`).
- **Route A (through REA, bounded slices)**: copy → patch bytes 18–19 `f3 00`→`b7 00` → `REA_GHIDRA_LANGUAGE_ID=RISCV:LE:64:default` (`config/parseConfig.js:64-72` → `-processor` at `ghidra/GhidraLauncher.js:255-262`) → 94 procedures + `csr` block on the 766 KB carve, reproducible across `analyze`/`inspect` (re-verified live; evidence ids byte-stable). Control without the env var: `auto-from-header`/0 procedures. **Honesty tax**: the envelope records `architecture:"arm64"` + the patched sha256 — declare the patch wherever cited.
- **Route B (around REA, full file)**: unpatched carved EXEC imports natively into `analyzeHeadless` (`RISCV:LE:64:default:gcc`); the 900 s-capped analysis [wave] saved a program whose counts re-verified live in ~2 s: 39 blocks / 29,932,990 B / 10,766 functions / 3,141,043 instructions / 37,455 data / 42,057 symbols, entry = real RV64. Budget >30 min for complete auto-analysis of 29 MB.
- **Scaling limit**: REA's absolute session deadline (`REA_GHIDRA_STARTUP_TIMEOUT_MS`, default 330 s at `config/ghidraStartupTimeout.js:3`) kills the 29 MB target at `list_documents` even when raised to 1800 s [wave, envelopes re-read] — keep Route-A slices ≲1 MB.
- **Dead ends pinned**: `.hop` → database-kind refusals from all three providers (arch never parsed); `--target-format dos-com` capped at 0xff00 B (`domain/dosCom.js:6`); `extract-firmware` verifies the slice (sha256 match, `handler:"elf64"`) but publishes 0 files.
- Recipe: RISC-V via REA = `printf '\xb7\x00' | dd of=<copy> bs=1 seek=18 conv=notrunc` + `REA_GHIDRA_LANGUAGE_ID=RISCV:LE:64:default rea analyze <copy>`; full GSP EXEC = direct `analyzeHeadless`.
- Scratch (outside repo, this lane): `/tmp/r5v-refusal.{json,err}`, `/tmp/r5v-bypass.{json,err}`, `/tmp/r5v-control.{json,err}`, `/tmp/r5v-inspect.{json,err}`, `/tmp/r5v-hop.{json,err}`, `/tmp/r5v-reverify.{bin,hop}`. Wave artifacts reused read-only: `/tmp/r5-ghidra-proj2/`, `/tmp/r5-ghidra-scripts/`, `/tmp/r5-*.json`, `/tmp/r4u-embedded-elf.bin`. No repo files touched besides this entry and the four stale-claim rewords ordered by the same assignment.

## Errata (round-6 audit, 2026-10-13, append-only)

- **Candidate 6's timeout mechanism no longer reproduces on the warm host**
  (round-6 audit re-run, 21:32): `rea analyze` on the 29 MB patched EXEC now
  returns RC=0 in seconds via provider `rea-workflow` (`binary_overview`, 1
  procedure) instead of dying at `list_documents` after 330 s/1800 s. The
  entry's conclusion survives — REA still yields no deep analysis of the
  target — but the *mechanism* is wave-scoped; warm-host behavioral change,
  not an entry error. The heavy runs stay `[wave]`-marked.
