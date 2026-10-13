<!-- corpus entry — kaidoku-shokunin round 4 unlock wave (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4u/01-firmware-deep.md. -->

# kaidoku-r4u · 01-firmware-deep — firmware gate OPEN: first real `inspect-firmware-regions`/`extract-firmware` runs on all four nvidia blobs; ucodes are stub headers, GSP blobs are signed ELF wrappers around ~29/84 MB `.fwimage` payloads; `rea analyze` still refuses RISC-V (gate is REA-side, not Ghidra-module-absent)

Axes: **coverage** (r2's `capability_unavailable` wall is lifted — every verb now executes end-to-end), **evidence-fidelity** (REA Evidence envelopes carry engine sha256 + verbatim provider argv), **boundary-precision** (binwalk region claims cross-checked against `readelf`/carve/entropy ground truth — one inferred-size under-report caught), **failure-honesty** (typed refusals still recorded verbatim: `target_unavailable` on RISC-V stands even for a carved EXEC).

Env: `REA_BINWALK_COMMAND=/usr/bin/binwalk` (binwalk 3.1.0, engine sha256 `5fc19aac1f357a66a47e8b20a8038a84cb93971cb5d331bd4503b02fcc0a40d6`), `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` → realpath `~/.local/share/uv/tools/unblob/bin/unblob` (unblob 26.6.4, engine sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`). Package `rea-agents@6.4.0` via npx. Ghidra 12.1.4 at `~/.local/opt/ghidra_12.1.4_PUBLIC` (doctor: configured+available). Date: 2026-10-13.

Subjects (`sha256sum`):
- `ucodes_tu10x.bin` 12,032 B `dcbdf512ab09b7f6d946e7f415bcfbc9137f5db1cf0c3c576f4b34b5275acb38`
- `ucodes_ga10x.bin` 31,744 B `3a36ceb211c20694f3d2e33ade2bbd2c3ae0b61ba2f28eaff4362aac547a632c`
- `gsp_tu10x.bin` 29,381,504 B `d157e3b7dd5da2ca8d1ccb6ca98958f9e35d10a9ef7326277ebac133e4b0d1a7`
- `gsp_ga10x.bin` 84,310,168 B `c0156954f3e048d56011524e0c2ae2881bb6db8173b53f9b2f4eb94197f02999`

## Candidate: `inspect-firmware-regions` runs clean on all four blobs — ucodes yield 0 regions, GSPs yield 56/156 regions; REA shells out `binwalk --quiet --search-all --threads 1` under `prlimit`

- claim: With `REA_BINWALK_COMMAND` exported, all four scans RC=0 with `coverage:"signature_scan"`. `ucodes_tu10x` → `ev_7bb0fd1fbbdea321c474bc984722dea56b7ef2411bb5ab3466a66d79033e45a0`, **0 regions**; `ucodes_ga10x` → `ev_edb0c876b502ab809f91730f559c9989922b683d5b363669fc16a42b4c501d23`, **0 regions**; `gsp_tu10x` → `ev_0388cb9ab97c3cf603cae528872db881f094fca2d8550298afe705fa13c198ed`, **56 regions** = elf 2, gpg_signed 50, zlib 2, sha256 1, srecord_generic 1; `gsp_ga10x` → `ev_4009f834a192eb7801d7bd25fbf2864f29873be987ec0841040e20ce0f68407a`, **156 regions** = zlib 60, gpg_signed 45, gzip 26, elf 13, srecord_generic 5, compressd 4, sha256 2, copyright 1. The raw_result records the exact provider invocation: `/usr/bin/binwalk --quiet --search-all --threads 1 --log /tmp/rea-firmware-*/report.json <staged copy>`, plus a `binwalk --version` probe ("binwalk 3.1.0"), all under `resource_limiter:"/usr/bin/prlimit"`. No `--entropy` flag is passed — REA's coverage is signature-only by construction.
- source: `/tmp/r4u-ifr-{tu10x,ga10x,gsp-tu,gsp-ga}.json` evidence envelopes; `Counter(r['signature'])` census; `raw_result.execution.args`.
- verify: `REA_BINWALK_COMMAND=/usr/bin/binwalk npx -y rea-agents@6.4.0 inspect-firmware-regions <blob> --format json | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["evidence_id"],len(d["normalized_result"]["regions"]))'`.
- verified-at: 2026-10-13
- suggested: admit — the r2 gate is resolved; region inventories are now held evidence. `signature_scan` is an honest, narrow coverage claim: signature hits ≠ partition validity (stated verbatim in `limitations[0]`).

## Candidate: both `ucodes_*.bin` are STUB containers — 24 nonzero bytes (`NVUCODES` header + version + count + 8-byte tag) then zero-padding to EOF; that is why binwalk and unblob both return honest zeros

- claim: `ucodes_tu10x.bin` has its last nonzero byte at offset **23**; `ucodes_ga10x.bin` likewise only bytes 0–255 nonzero (range scan: `[(0,256)]`, actual payload 0–23). Header layout both files: `8s magic "NVUCODES"` + `u32=1` (format version) + `u32` (`496` tu10x / `1315` ga10x — plausibly a payload-length or entry-count field) + `8 bytes` tag (`2bae986bab90198d` / `a3251724509f926f`) + zeros. These are the bytes the `nvidia-utils 610.57.04-1` package actually ships (sha256 matches r2 inventory). So the microcode blobs carry a container header and essentially no payload on disk — the 0-region binwalk result is *correct*, not a tool miss.
- source: `xxd -l 64`; python nonzero-range scan + `struct.unpack('<8sIIII')`.
- verify: `python3 -c "d=open('/usr/lib/firmware/nvidia/610.57.04/ucodes_tu10x.bin','rb').read(); print(max(i for i,b in enumerate(d) if b))"` → `23`.
- verified-at: 2026-10-13
- suggested: admit — explains the empty scans positively; also explains why unblob published nothing (below). Whether the payloads are meant to be populated by the driver at load time is out of scope but worth a note in PROVINCE.

## Candidate: `extract-firmware` (unblob 26.6.4) on the ucodes → `coverage:"complete"`, `files:[]`, `published_bytes:0` — a clean empty extraction, not a failure

- claim: `extract-firmware ucodes_tu10x.bin /tmp/rea-fw-ucodes-out` RC=0, `ev_305743ecbe0be7d69868876597dd2264e8b0504c94e7e13f5b0699f07ea3ded0`; same for ga10x → `ev_5964d1086be847cf6ea2397a33db47674282e4a161e5ca5127cb18bf1e20adb9`. Normalized: `selection{offset:0,length:12032,sha256:…}`, `coverage:"complete"`, `files:[]`, `chunks:[]`, `unpublished_entries:[]`, `diagnostics:[]`. unblob's own report contains only `StatReport` + `FileMagicReport{magic:"data",mime:application/octet-stream}` + `HashReport{md5,sha1,sha256}` — no carveable chunks in a stub file. Output dir created but left empty (REA invoked unblob with `--depth 3 --randomness-depth 0 --process-num 1`, staged copy under `/tmp/rea-firmware-*`). Note: unblob's stdout banner says "Extracted files: 1" — that counts the input stat, not a published file; normalized `files:[]` is the true count.
- source: `/tmp/r4u-ef-ucodes{,-ga}.json`; `ls -la /tmp/rea-fw-ucodes-*-out` (both empty, mode 700).
- verify: rerun and read `normalized_result.{files,published_bytes,coverage}`.
- verified-at: 2026-10-13
- suggested: admit — extraction pipeline verified end-to-end on the only bounded in-scope target; honest zero. GSP extraction deliberately not run (bounded task: 29/84 MB images, and the interesting interior needs offset-targeted extraction, a future `--offset/--length` lane).

## Candidate: GSP blobs are ELF64 RISC-V *signature wrappers* — `.fwimage` payload + `.fwversion "610.57.04"` + N×4096 B per-chip `.fwsignature_*` sections; symtab leaks NVIDIA's build path

- claim (non-REA ground truth via `readelf`): `gsp_tu10x.bin` = ELF64 REL RISC-V, 0 program headers, 10 sections: `.fwimage` PROGBITS @0x40 size 0x1c01dc8 (29,358,536 B), `.note.gnu.build-id`, `.fwversion` = ASCII `610.57.04`, **3 `.fwsignature_*` sections named per-chip** (`_ga100`, `_tu11x`, `_tu10x`, 0x1000 B each — signature blocks), `.symtab` (4 syms), `.strtab`, `.shstrtab`. `gsp_ga10x.bin` = same shape, 19 sections: `.fwimage` @0x40 size 0x505b000 (84,242,432 B), **12 `.fwsignature_*` sections** (one per ga10x SKU presumably). The symtabs embed the full build path verbatim: `_binary__dvs_p4_build_sw_rel_gpu_drv_r610_r610_85_drivers_resman_build_gsp__out_Linux_amd64_release_LibOS_riscv64_release_firmware_tu10x_firmware_elf_stripped_{start,end,size}` — i.e., GSP firmware is "LibOS riscv64 release" built from NVIDIA's `sw/rel/gpu/drv/r610/r610_85` tree, `drivers/resman/build/gsp` target. tu10x's fwimage holds `firmware_elf.stripped` while ga10x's holds `firmware.bin` — matching what binwalk sees at their heads (below).
- source: `readelf -h/-S/-sW -x .fwversion`.
- verify: `readelf -S /usr/lib/firmware/nvidia/610.57.04/gsp_tu10x.bin; readelf -sW … | grep _binary`.
- verified-at: 2026-10-13
- suggested: admit — provenance-grade structure data, free from any provider. The 0x1000-byte signature sections corroborate the signature-scan limitation ("signature matches do not establish … encryption").

## Candidate: binwalk's ELF regions are REAL — `gsp_tu10x .fwimage` begins with an embedded ELF EXEC @0x40 spanning ~29.37 MB (binwalk under-reported 766,595 as an inferred length); `gsp_ga10x .fwimage` heads raw RISC-V code and packs 12 embedded EXECs

- claim: carving @64 of gsp_tu10x yields a real `ELF 64-bit RISC-V EXEC`, entry `0x4009000`, 31 program headers, 37 section headers at `e_shoff=29,365,384` (within the embedded image) → true extent ≈29,367,752 B — binwalk's `reported_size:766595` is an *inferred* truncation (the envelope's own `size_basis:"provider_reported_validation_unknown"` + "Binwalk may infer unknown lengths" limitation covers this honestly). So `.fwimage` = one big stripped RISC-V ELF (~29.37 MB) — the driver's GSP binary — followed by build-id/version/signature sections in the outer REL wrapper. On ga10x, `.fwimage` begins with raw RISC-V compressed code (`97c2 0600 9382…` = c.addi16sp etc., no ELF magic) and binwalk finds **12 embedded ELF EXEC regions** at offsets 450,624…19,669,056 (155,648–759,230 B each) — a multi-image payload, plus 26 gzip streams clustered ~14.71–14.93 MB bearing build timestamps `2024-10-28`/`2026-01-23`/`2026-04-20`, `Copyright NVIDIA` @16,945,176, and 4 `compressd` (LZW) regions.
- source: `dd bs=1 skip=64 count=766595` + `readelf -h` on the carve (EXEC confirmed; `e_shoff` read directly, section tail past the carve proves under-report); `dd` heads of both `.fwimage`s; region census above.
- verify: `dd if=gsp_tu10x.bin bs=1 skip=64 count=766595 | readelf -h -` → `Type: EXEC, Machine: RISC-V, Entry 0x4009000`.
- verified-at: 2026-10-13
- suggested: admit — binwalk's signature layer holds up under carve-verification on the ELF hits; the size field is explicitly advisory.

## Candidate: `rea analyze` still refuses ALL RISC-V — `target_unavailable` on the outer REL *and* on the carved inner EXEC; the gate is REA-side, not a missing Ghidra module (install ships 39 processor dirs incl. `RISCV`)

- claim: `rea analyze gsp_tu10x.bin` → `{"code":"target_unavailable","category":"unavailable","reason":"unsupported ELF architecture","retryable":false}` exit 1 — identical to r2's record. New evidence the refusal is architecture-wide: `rea analyze` on the carved **EXEC** embedded ELF → same `target_unavailable` (so it's not REL-vs-EXEC discrimination). `rea inspect` → same. `inspect-binary-layout` → a *different* typed refusal: `unsupported_target` "Initial layout profile requires x86-64 ELF objects." Meanwhile `ls Ghidra/Processors/` = **39 dirs including `RISCV`** — Ghidra itself ships a RISC-V module, but REA's own ELF preflight (`Cannot open artifact: unsupported ELF architecture`) refuses the target before the provider is engaged. Segment/procedure counts via REA: unreachable — the readelf ground truth above substitutes (10/19 sections, 0 program headers on the wrapper; 31 PH / 37 SH on the embedded EXEC).
- source: `/tmp/r4u-analyze-gsp-tu.json` (498 B error envelope), re-run exit-code capture, `/tmp/r4u-ibl-gsp-tu.json`, Ghidra dir listing.
- verify: `npx -y rea-agents@6.4.0 analyze /tmp/r4u-embedded-elf.bin --format json` → same envelope; `ls ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Processors | wc -l` → 39.
- verified-at: 2026-10-13
- suggested: admit — sharpens r2's "ELF-route closed" into "REA's ELF accept-list excludes RISC-V entirely; a present-but-unreached Ghidra RISCV module is not evidence of coverage". A direct `analyzeHeadless` import test is a possible future probe (outside REA verbs).

## Candidate: signature-scan noise floor is real — 50 `gpg_signed` hits on tu10x are short-magic false positives; `zlib @766659` verified true (`78 da`); `srecord_generic` matched a real byte boundary (`S0` + binary) with an EOF-inferred 13.7 MB span

- claim: the `gpg_signed` regions (50 on tu10x spanning 14,778,314–28,927,986; 45 on ga10x) carry `reported_size` of 5–30 B — classic 2-byte-magic false positives riding on binary data (spot check @14,778,314 shows ordinary RISC-V code bytes, not a PGP packet). `zlib @766,659` shows real `78 da` zlib magic (11 B reported — a stub stream). `srecord_generic @824,363` literally starts `53 30` ("S0") then binary — the signature matched a boundary but the 13,756,760 B "size" is inferred (no real S-record text follows). Confidence field doesn't separate these: gpg hits carry `reported_confidence:250` same as the real zlib — confidence measures signature-strength, not plausibility.
- source: `dd` spot-checks at each signature offset; region JSON census.
- verify: `dd if=gsp_tu10x.bin bs=1 skip=766659 count=4 | xxd` → `78da`.
- verified-at: 2026-10-13
- suggested: admit — the typed limitation "Signature matches … do not establish partition validity" is doing real work here; consumers must treat `gpg_signed`/`srecord` hits as leads, not facts.

## Candidate: entropy boundaries (non-REA; REA passes no `-E`) — `gsp_tu10x .fwimage` holds a solid ~8 MiB entropy-8.00 block (0x400000–0xbc0000) between code-entropy regions: a compressed/encrypted payload inside the embedded ELF

- claim: 256 KiB-window Shannon scan of `gsp_tu10x.bin`: ~3.5–6.4 through 0x0–0x3c0000 (RISC-V code/data), transition at 0x3c0000, **flat 8.000 for 0x400000–0xbc0000 (~8 MiB)** — indistinguishable from encrypted/compressed data — then ~6.2–6.4 to the signature sections (which themselves read ~4.05 in the mixed tail chunk). REA's inspect verb does not request binwalk entropy (`--search-all` only), so these boundaries are recorded as non-REA supplementary evidence.
- source: python `Counter`-based per-window entropy scan.
- verify: rerun the windowed scan; boundaries reproduce exactly (deterministic).
- verified-at: 2026-10-13
- suggested: admit — maps the "what's inside .fwimage" question: code + a large opaque compressed/encrypted block + code; explains why only signature-scan sees interior structure.

## Candidate: the doctor/providers blind spot persists WITH working env — `rea doctor` still inspects only ghidra+ida; `rea providers` names the firmware *operations* but never binwalk/unblob readiness

- claim: with both `REA_*_COMMAND` vars exported and both verbs verified working, `rea doctor --format json` `providerInspections` remains `["ghidra","ida"]` only; `rea providers --format json` lists `extract_firmware`/`inspect_firmware_regions` in the tool catalog (`surface:"firmware-provider"`) but contains zero occurrences of `binwalk`/`unblob` — provider *readiness* for the firmware surface stays invisible to both inventory verbs.
- source: doctor/providers JSON dumps under the exported env.
- verify: `REA_BINWALK_COMMAND=… REA_UNBLOB_COMMAND=… npx -y rea-agents@6.4.0 doctor --format json | grep -c binwalk` → 0.
- verified-at: 2026-10-13
- suggested: admit — confirms r2's candidate verbatim and hardens it: the blind spot is not env-dependent; PROVINCE must keep carrying the Binwalk/Unblob prerequisite as prose.

## Run log

| # | Command | Result |
| - | ------- | ------ |
| 1 | `export REA_BINWALK_COMMAND=/usr/bin/binwalk REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` | both resolve: binwalk 3.1.0, unblob→`~/.local/share/uv/tools/unblob/bin/unblob` 26.6.4 |
| 2 | `inspect-firmware-regions ucodes_tu10x.bin --format json` | RC=0 `ev_7bb0fd1f…45a0`, 0 regions, `signature_scan` |
| 3 | `inspect-firmware-regions ucodes_ga10x.bin --format json` | RC=0 `ev_edb0c876…d23`, 0 regions |
| 4 | `inspect-firmware-regions gsp_tu10x.bin --format json` | RC=0 `ev_0388cb9a…8ed`, 56 regions (elf 2, gpg 50, zlib 2, sha256 1, srecord 1) |
| 5 | `inspect-firmware-regions gsp_ga10x.bin --format json` | RC=0 `ev_4009f834…07a`, 156 regions (zlib 60, gpg 45, gzip 26, elf 13, srecord 5, compressd 4, sha256 2, copyright 1) |
| 6 | `extract-firmware ucodes_tu10x.bin /tmp/rea-fw-ucodes-out` | RC=0 `ev_305743ec…ded0`, files:[] published:0 coverage:complete; dir created, empty |
| 7 | `extract-firmware ucodes_ga10x.bin /tmp/rea-fw-ucodes-ga-out` | RC=0 `ev_5964d108…db9`, same honest zero |
| 8 | `rea analyze gsp_tu10x.bin --format json` (twice) | RC=1 `target_unavailable` "unsupported ELF architecture", 498 B envelope |
| 9 | `rea inspect gsp_tu10x.bin` | RC=1 same `target_unavailable` |
| 10 | `rea inspect-binary-layout gsp_tu10x.bin` | RC=1 `unsupported_target` "requires x86-64 ELF objects" |
| 11 | `dd skip=64 count=766595` carve + `readelf -h` | embedded ELF EXEC RISC-V entry 0x4009000, 31 PH, 37 SH @29,365,384 → true ~29.37 MB |
| 12 | `rea analyze /tmp/r4u-embedded-elf.bin` | RC=1 same `target_unavailable` (RISC-V EXEC also refused) |
| 13 | `readelf -h/-S/-sW/-x` both GSP blobs | ELF64 REL RISC-V wrappers; `.fwimage` 0x1c01dc8/0x505b000; `.fwversion`="610.57.04"; 3/12 ×0x1000 `.fwsignature_*`; symtab build-path leak `…_LibOS_riscv64_release_firmware_{tu10x_elf.stripped,ga10x_bin}_*` |
| 14 | `xxd -l 64` + nonzero-range scan, ucodes | `NVUCODES`+ver1+496/1315+8B tag; last nonzero byte = 23 (tu10x) — stub containers |
| 15 | windowed entropy scan, gsp_tu10x | code ~3.5–6.4 to 0x3c0000; flat 8.00 0x400000–0xbc0000; ~6.4 tail |
| 16 | `dd` spot-checks: zlib@766659 (`78 da` real), srecord@824363 (`S0`+binary), gpg@14778314 (code bytes — FP) | signature-noise calibration |
| 17 | `ls Ghidra/Processors` | 39 dirs incl. `RISCV` — module present, unreached by REA preflight |
| 18 | `rea doctor`/`rea providers` with env exported | providerInspections still ghidra+ida only; catalog names ops not providers |

## Summary

**Firmware surface: partially held — the provider layer is fully open and honest; the deep-analysis route remains frontier.** `inspect-firmware-regions` now executes on all four blobs (4 Evidence envelopes, RC=0): the ucodes return 0 regions because they are *stub containers* (24 real bytes + zero-padding — a positive explanation, not a miss), while the GSP blobs return 56/156 regions whose ELF hits carve-verify as real embedded RISC-V executables. `extract-firmware` completes cleanly on both ucodes (`coverage:"complete"`, 0 files — correct on stubs; GSP extraction deliberately deferred to an offset-targeted lane). The wrappers are signature carriers: `.fwimage` + `.fwversion 610.57.04` + 3/12 per-chip `.fwsignature_*` blocks, with NVIDIA's full `r610_85` LibOS-riscv64 build path in the symtab. `rea analyze`'s RISC-V refusal (`target_unavailable`) is unchanged and now proven architecture-wide (carved EXEC also refused) and REA-side (Ghidra ships a `RISCV` module — 39 processor dirs — that never gets reached); `inspect-binary-layout` is x86-64-only. Persistent blind spot: doctor/providers still cannot see firmware-provider readiness even when it's configured and working. Frontier for r5: `--offset/--length` targeted `extract-firmware` on the GSP `.fwimage` region, Ghidra `analyzeHeadless` directly on the carved EXEC, and entropy-boundary-guided carving of the 8 MiB entropy-8.00 block.
