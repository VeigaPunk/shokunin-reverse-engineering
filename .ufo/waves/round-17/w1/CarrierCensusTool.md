# CarrierCensusTool report (round 17, wave 1)

## Deliverables

- Tool: `.ufo/waves/round-17/tools/carrier-census.py` (new file, Python 3 stdlib only,
  runs under `python3 -I`; `--selftest` prints `SELFTEST: CLEAN cases=10`, exit 0 — observed).
- Output: `.ufo/waves/round-17/w1/carrier-census.json` (this file's data; exit 0, 11/11 carriers read, 0 row errors).

## Contract conformance (`contract.md:110-113`)

For each path the row carries: `sha256`, `size`, ELF magic check (`is_elf` + parsed
`elf.{class,data,machine}` — magic-only, file-style), `inspect` = argv/exit/`go_version`/
`evidence_id`/`module_path`/stderr_tail/error from
`npx -y rea-agents@6.5.0 inspect-go-binary PATH --format json`, and `pacman` = argv/exit/
owner-string/error from `pacman -Qo PATH` (read-only query only). JSON written to `--out`
and echoed to stdout (`sort_keys=True, indent=2`). Exit 0 when emitted; 2 when --out dir is
unwritable or *every* path is unreadable. Per-carrier failures are data, never hidden.
No carrier binary was executed; inspect-go-binary is a static reader.

## Census table (observed, from `w1/carrier-census.json`)

| path | size | sha256 (prefix) | ELF | go_version | module | evidence_id (prefix) | pacman owner |
|---|---|---|---|---|---|---|---|
| /usr/bin/shfmt | 3601168 | 58f76563… | x86_64 | go1.27.0-X:nodwarf5 | mvdan.cc/sh/v3 | ev_f8ef12a8… | shfmt 3.14.1-1 |
| /usr/bin/fzf | 5590288 | 95e3e6ae… | x86_64 | go1.27.2-X:nodwarf5 | github.com/junegunn/fzf | ev_4fc99466… | fzf 0.74.5-1 |
| /usr/bin/gum | 14304016 | 95769344… | x86_64 | go1.27.1-X:nodwarf5 | charm.land/gum/v2 | ev_3b5f2f27… | gum 2.0.2-1 |
| /usr/bin/runc | 8761392 | 5040726d… | x86_64 | go1.27.1-X:nodwarf5 | github.com/opencontainers/runc | ev_6c82a410… | runc 1.5.2-1 |
| /usr/bin/ctr | 23678968 | 51a94a84… | x86_64 | go1.27.2-X:nodwarf5 | github.com/containerd/containerd/v2 | ev_10463eb3… | containerd 2.4.2-1 |
| /usr/bin/lazygit | 20964528 | a2461fa3… | x86_64 | go1.27.2-X:nodwarf5 | github.com/jesseduffield/lazygit | ev_b0a4cc4b… | lazygit 0.66.2-1 |
| /usr/bin/docker | 30487344 | 566a4e83… | x86_64 | go1.27.2-X:nodwarf5 | *(none in module_text)* | ev_0ffaef79… | docker 1:29.9.1-1 |
| ~/.local/bin/gh | 42086560 | 7469124f… | x86_64 | go1.27.1 (no -X suffix) | github.com/cli/cli/v2 | ev_48b90b70… | not owned (`error: No package owns …`) |
| esbuild 0.25.12 | 10358936 | bab29b2c… | x86_64 | go1.23.12 | github.com/evanw/esbuild | ev_0cabcc66… | not owned |
| esbuild 0.21.5 | 9707520 | b567f467… | x86_64 | go1.20.12 | github.com/evanw/esbuild | ev_5c06ecef… | not owned |
| esbuild 0.27.7 | 11120788 | c638273f… | x86_64 | **null** | null | ev_a1e7ac95… | not owned |

Counts (observed): `{"elf": 11, "errors": 0, "go_version_found": 10, "pacman_owned": 7, "total": 11}`.

## Findings relevant to C2 (depth)

1. **Carrier set discriminates in-range vs out-of-range as planned.** Seven pacman Go
   binaries report `go1.27.x-X:nodwarf5` (above GoRttiMapper's declared 1.15–1.25 band per
   claims.json C2), gh reports `go1.27.1` without the experiment suffix, and esbuild
   0.25.12 / 0.21.5 give the intended in-range controls `go1.23.12` / `go1.20.12`
   (claims.json:21). All 11 are x86_64 ELF. [observation]
2. **esbuild 0.27.7 is not a usable Go-version carrier for this protocol**:
   `inspect-go-binary` exits 0 but `normalized_result.build_info` is null; its limitations
   state "No recognized Go build-info record was found in the inspected image". Verified by
   a direct re-run after the census (same result). The binary was likely built with
   build-info omitted; absent metadata does not prove non-Go. L1 should either drop it or
   treat it as a "no build-info" edge case, not as an in-range control. [observation]
3. **`go1.27.x-X:nodwarf5` suffix is pervasive on Arch packages** (7/7 pacman-owned
   binaries) — consistent with `GOEXPERIMENT=nodwarf5` toolchain builds; predict.py
   normalization must strip the `-X:…` suffix exactly as `GoVer.parse` does. [observation
   of version strings; suffix→experiment mapping is inference]
4. **docker's module_text has no `mod` line parseable by the census regex**
   (`module_path: null`) while `go_version` resolved fine — module_text for docker uses a
   different first line. Recorded as data; does not affect version extraction. [observation]
5. **pacman ownership**: 7/11 carriers owned (`pacman -Qo` exit 0); gh and the three
   esbuild binaries are user-installed (exit 1, "No package owns …") — recorded in
   `pacman.error`, not treated as failure. [observation]

## Limits

- `is_elf`/elf fields are magic+header-byte classification only (no section parsing); an
  `is_elf:true` file could still be malformed.
- `evidence_id` is REA's per-call envelope id, not a digest of the binary — use `sha256`
  for pinning.
- inspect-go-binary was run via `npx -y rea-agents@6.5.0` (already cached on this host);
  the census itself performs no installs.
- Census was run once; `generated_at_utc` inside the JSON timestamps it. Only the shfmt
  row's inspect call was duplicated (one pre-implementation shape probe) — both returned
  identical fields except evidence_id, confirming evidence ids are per-invocation.

## Tool installs

None. REA 6.5.0 was invoked through the existing `npx` cache per contract.
