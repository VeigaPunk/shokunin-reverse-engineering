<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/09-firmware.md. -->

# kaidoku r2 — REA firmware surface probe (inspect-firmware-regions / extract-firmware)

Host: Arch-flavored Linux. REA `rea-agents@6.4.0` via npx. All probes read-only against
`/usr/lib/firmware/nvidia/610.57.04/`; no output directory was ever created (provider gate
precedes filesystem effects — verified below). Every typed error was captured verbatim.

## Candidate: firmware inventory — the `nvidia-utils 610.57.04-1` package owns four blobs, two of them RISC-V ELF
- claim: `/usr/lib/firmware/nvidia/610.57.04/` holds exactly four files, all owned by
  `nvidia-utils 610.57.04-1` per `pacman -Qo`: `ucodes_tu10x.bin` (12032 B, `data`,
  sha256 `dcbdf512ab09b7f6d946e7f415bcfbc9137f5db1cf0c3c576f4b34b5275acb38`, ASCII
  magic `NVUCODES` at offset 0), `ucodes_ga10x.bin` (31744 B, `data`, sha256
  `3a36ceb211c20694f3d2e33ade2bbd2c3ae0b61ba2f28eaff4362aac547a632c`),
  `gsp_tu10x.bin` (29381504 B) and `gsp_ga10x.bin` (84310168 B) — the two `gsp_*`
  files are `ELF 64-bit LSB relocatable, UCB RISC-V, soft-float ABI, not stripped`
  (`readelf -h`: `Machine: RISC-V`, `Type: REL`). The dir sits beside ~40 sibling
  chipset dirs (`ga102`…`tu117`, `tegra*`) under `/usr/lib/firmware/nvidia/`.
- source: `ls -la`, `file`, `sha256sum`, `readelf -h`, `pacman -Qo`, `strings -a -n 8 | head` (→ `NVUCODES`)
- verify: `file /usr/lib/firmware/nvidia/610.57.04/*.bin; pacman -Qo /usr/lib/firmware/nvidia/610.57.04/ucodes_tu10x.bin; head -c 8 /usr/lib/firmware/nvidia/610.57.04/ucodes_tu10x.bin`
- verified-at: 2026-10-13
- suggested: admit — smallest `.bin` selected as primary target (`ucodes_tu10x.bin`); pacman attribution already held from r1 wave 12 applies to firmware blobs unchanged.

## Candidate: `inspect-firmware-regions` is NOT binwalk-free — it hard-requires `REA_BINWALK_COMMAND` (Binwalk 3.1.x), absent on this host
- claim: The dispatch assumption "signature-scan only ⇒ works without Binwalk" is
  false. Bare call returns `{"code":"capability_unavailable","category":"unsupported_provider","retryable":false,"details":{"provider_id":"binwalk","operation":"inspect_firmware_regions","reason":"This integration requires Linux and an absolute REA_BINWALK_COMMAND path to the caller-supplied tool"}}` with process exit 1. Neither `binwalk` nor any candidate exists on PATH. The env contract is strict: a non-absolute value (`REA_BINWALK_COMMAND=true`) reproduces the same "absolute path" refusal; a nonexistent path yields `ENOENT: no such file or directory, realpath '/nonexistent'`; and a pointing-at-wrong-tool path (`REA_BINWALK_COMMAND=/bin/true`) reaches a version gate: `Unsupported tool version true (GNU coreutils) 9.11 …; accepted releases are Binwalk 3.1.x (verified with 3.1.0)` — REA shells out `<cmd> --version` and parses the banner. No region signatures were identified on `ucodes_tu10x.bin`; the `NVUCODES` magic was observed via `strings`, not via REA.
- source: `inspect-firmware-regions --help` (schema: single required `path`, "never executed"); four probe runs: unset env, `=true`, `=/nonexistent`, `=/bin/true`
- verify: `timeout 120 npx -y rea-agents@6.4.0 inspect-firmware-regions /usr/lib/firmware/nvidia/610.57.04/ucodes_tu10x.bin --format json` → `capability_unavailable`; `command -v binwalk` → absent
- verified-at: 2026-10-13
- suggested: admit — corrects the catalog expectation: signature inspection is itself provider-gated. Prerequisite is operator-owned: install Binwalk 3.1.x and export an absolute `REA_BINWALK_COMMAND`.

## Candidate: `extract-firmware` routes to a different provider — `REA_UNBLOB_COMMAND` (Unblob 26.6.x), with caller-supplied absent output dir
- claim: `extract-firmware <path> <outputDirectory>` requires `REA_UNBLOB_COMMAND`
  (not binwalk): unset → `capability_unavailable`/`unsupported_provider`,
  `provider_id:"unblob"`, `operation:"extract_firmware"`, exit 1. `=/bin/true`
  reaches the version gate: `accepted releases are Unblob 26.6.x (verified with
  26.6.4)`. Schema contract: `outputDirectory` is an "Absolute absent output
  directory; parent must exist"; `--offset`/`--length` are paired (offset alone →
  `{"code":"invalid_request","category":"invalid_input","retryable":true}` — and
  this arg validation fires BEFORE provider resolution); `--max-depth` 1–10 default
  3; `--max-output-bytes` default 256 MiB, hard cap 512 MiB; `--max-output-files`
  default 10000. Provider resolution precedes all filesystem effects: three runs
  pointed at absent `/tmp/rea-fw-*` targets left nothing on disk.
- source: `extract-firmware --help` + `--schema` (required `[path, outputDirectory]`, `additionalProperties:false`); probes: unset env, `=/bin/true`, `--offset 16` alone, existing dir, missing-parent dir
- verify: `npx -y rea-agents@6.4.0 extract-firmware /usr/lib/firmware/nvidia/610.57.04/ucodes_tu10x.bin /tmp/x --format json` → `capability_unavailable`; `command -v unblob` → absent
- verified-at: 2026-10-13
- suggested: admit — caller-supplied-output-dir contract recorded; expected failure is `capability_unavailable` (NOT `provider_unavailable` — the typed code differs from `inspect-binary-layout`'s r1 code).

## Candidate: validation ordering — arg schema → provider gate → filesystem effects
- claim: `--offset` without `--length` fails `invalid_request`/`invalid_input` even
  with `REA_UNBLOB_COMMAND` unset-provider conditions looming; provider failure
  (`capability_unavailable`) precedes outputDirectory existence/parent checks —
  an existing dir and a missing-parent dir both returned the unblob version-gate
  error, and no directory was created. Typed JSON error envelopes exit with code 1.
- source: paired probes above; `echo $?` captured without pipes (bare exit=1 for both verbs)
- verify: rerun any gated call and `echo $?` → 1
- verified-at: 2026-10-13
- suggested: admit — determines where contract fixes land: installing unblob is necessary but arg-shape bugs still surface first.

## Candidate: firmware providers are invisible to `rea doctor` and `rea providers` — the gate is only discoverable by calling the verb
- claim: `rea doctor --format json` `providerInspections` lists exactly `["ghidra","ida"]`
  — no binwalk/unblob check exists; `rea providers --format json` returns 18
  capability entries, none firmware (`inspect_firmware_regions`/`extract_firmware`
  absent). The only in-band signals are the verb's own typed refusal and the
  shipped README matrix (r1 wave 02: "firmware needs Binwalk/Unblob").
- source: doctor JSON dump (parsed), providers JSON (18 caps enumerated)
- verify: `npx -y rea-agents@6.4.0 providers --format json | grep -i firmware` → empty; `doctor` providerInspections ids
- verified-at: 2026-10-13
- suggested: admit — a doctor blind spot: environment verdicts cannot certify or flag the firmware surface; SKILL/PROVINCE must carry the Binwalk/Unblob prerequisite as prose (PROVINCE already does, now confirmed with typed evidence).

## Candidate: ELF-route fallback is closed too — `analyze` on `gsp_tu10x.bin` fails `target_unavailable` (unsupported ELF architecture)
- claim: Because the `gsp_*.bin` files are RISC-V relocatable ELF, the held Ghidra
  path was tried as a frontier move: `rea analyze gsp_tu10x.bin` →
  `{"code":"target_unavailable","category":"unavailable","reason":"unsupported ELF architecture","retryable":false}`,
  and `rea analyze ucodes_tu10x.bin` → `target_unavailable` / `unsupported binary
  format`. Ghidra 12.1.4 does not lift this RISC-V REL target, so no REA verb
  currently reaches any byte of the nvidia firmware set.
- source: two `analyze` runs, JSON envelopes, exit 1 each
- verify: `npx -y rea-agents@6.4.0 analyze /usr/lib/firmware/nvidia/610.57.04/gsp_tu10x.bin --format json`
- verified-at: 2026-10-13
- suggested: admit — closes the escape hatch; firmware is frontier, not partially-held-by-ELF. Non-REA readers (`readelf`, `strings`, `binwalk`-less magic) remain the only current coverage.

## Run log
- `ls -la /usr/lib/firmware/nvidia/610.57.04/` → 4 files; `file`/`sha256sum`/`readelf -h`/`pacman -Qo`/`strings` → inventory above (smallest `.bin` = `ucodes_tu10x.bin`, 12032 B, `NVUCODES` magic).
- `npx -y rea-agents@6.4.0 inspect-firmware-regions --help` + `--schema` → signature confirmed (`<path>` only).
- `inspect-firmware-regions ucodes_tu10x.bin --format json` → `capability_unavailable`/`unsupported_provider`, `provider_id:binwalk`, needs absolute `REA_BINWALK_COMMAND`; exit 1.
- `REA_BINWALK_COMMAND=true` → same absolute-path refusal; `=/nonexistent` → `ENOENT … realpath`; `=/bin/true` → version gate "Binwalk 3.1.x (verified with 3.1.0)".
- `extract-firmware --help` + `--schema` → `<path> <outputDirectory>` (absent dir, existing parent), paired `--offset/--length`, `--max-depth 1–10 d3`, `--max-output-bytes` 256 MiB d/512 MiB cap, `--max-output-files` d10000.
- `extract-firmware ucodes_tu10x.bin /tmp/rea-fw-out --format json` → `capability_unavailable`, `provider_id:unblob`, needs `REA_UNBLOB_COMMAND`; exit 1. `=/bin/true` → "Unblob 26.6.x (verified with 26.6.4)". `--offset 16` alone → `invalid_request`/`invalid_input` (retryable). Existing-dir and missing-parent targets → provider gate first; nothing created.
- `rea doctor --format json` → providerInspections = ghidra + ida only. `rea providers --format json` → 18 caps, zero firmware ops.
- `analyze gsp_tu10x.bin` → `target_unavailable` "unsupported ELF architecture"; `analyze ucodes_tu10x.bin` → `target_unavailable` "unsupported binary format"; both exit 1.
- `command -v binwalk unblob` → both absent. `pacman -Qo` → all four blobs owned by `nvidia-utils 610.57.04-1`.

## Summary
Firmware region inspection is **frontier**, not held. Both catalog verbs are
provider-gated on caller-supplied tools that do not exist on this host:
`inspect-firmware-regions` → `REA_BINWALK_COMMAND` (Binwalk 3.1.x, version-parsed),
`extract-firmware` → `REA_UNBLOB_COMMAND` (Unblob 26.6.x). The failure is typed
`capability_unavailable`/`unsupported_provider`, exit 1, pre-filesystem — clean and
honest, but it means zero region signatures were identified. The ELF-route fallback
is also closed (`target_unavailable` on both ELF and raw blobs). Unblock path is
operator-owned: install Binwalk 3.1.x and/or Unblob 26.6.x and export the absolute
`REA_*_COMMAND` paths — after which `ucodes_tu10x.bin` (12 KiB, `NVUCODES` magic)
is the designated first probe target. Note the doctor/providers blind spot: this
surface's readiness is invisible to `rea doctor`; it must stay tracked in PROVINCE.
