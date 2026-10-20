# ScoutCarrierPackages — carrier package identity (R17 W1)

Seat: `KaidokuR17.ScoutCarrierPackages-3` (leaf, read-only). Date: 2026-10-20.
Scope: package identity only — no carrier execution, no REA analyze/search/decompile, no Ghidra, no
pacman transaction. Sole write: this file.

Tools used (versions observed): Pacman v7.1.0 / libalpm v16.0.1, file-5.48, coreutils `sha256sum`/`stat`
0.8.0, host `uname -m` = x86_64. No installs or upgrades were performed (queries only).

## Reproducing commands (QUALITY #6)

```sh
for f in /usr/bin/shfmt /usr/bin/fzf /usr/bin/gum /usr/bin/runc /usr/bin/ctr /usr/bin/lazygit /usr/bin/docker; do
  pacman -Qo "$f"; done
pacman -Qi shfmt fzf gum runc containerd lazygit docker   # run per package
ls -l /usr/bin/<carrier>; file -b /usr/bin/<carrier>; sha256sum /usr/bin/<carrier>
pacman -Qo /home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.27.7/node_modules/@esbuild/linux-x64/bin/esbuild
```

## A. pacman-owned carriers — name + version + arch (QUALITY #4)

Every path below is a regular root-owned `0755` file (not a symlink), ELF 64-bit LSB, x86-64; Arch
`Architecture` field is `x86_64` for all seven, so the package arch and the ELF machine agree
(observation, two independent fields).

| absolute path | package | version (as pacman `Version`) | pkg arch | ELF class | sha256 | bytes | pacman Install Date |
|---|---|---|---|---|---|---|---|
| `/usr/bin/shfmt` | `shfmt` | `3.14.1-1` | x86_64 | ELF64 PIE, x86-64, dyn | `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459` | 3601168 | 2026-10-19 18:31:23 |
| `/usr/bin/fzf` | `fzf` | `0.74.5-1` | x86_64 | ELF64 PIE, x86-64, dyn | `95e3e6ae8e6092dab968129e5651793b724dc7768590babd235e763e5dc9c540` | 5590288 | 2026-10-20 09:16:37 |
| `/usr/bin/gum` | `gum` | `2.0.2-1` | x86_64 | ELF64 PIE, x86-64, dyn | `957693445e3c00ff26a81280b03b8cfdcee63b2f4cd0af0235010305eacac62b` | 14304016 | 2026-10-20 09:16:38 |
| `/usr/bin/runc` | `runc` | `1.5.2-1` | x86_64 | ELF64 PIE, x86-64, dyn | `5040726d094a01c6aa69a9035b6fceb2c0feb115230be198e2930d41087e199a` | 8761392 | 2026-10-20 09:16:36 |
| `/usr/bin/ctr` | `containerd` | `2.4.2-1` | x86_64 | ELF64 exec, x86-64, dyn | `51a94a844dafd617a5af9cb8667004bc6889edb15402389b7b7e1bf657248253` | 23678968 | 2026-10-20 09:16:36 |
| `/usr/bin/lazygit` | `lazygit` | `0.66.2-1` | x86_64 | ELF64 PIE, x86-64, dyn | `a2461fa387c546f03e47b5676deb351ccc54edacfbc8d157704f6a97f061cd38` | 20964528 | 2026-10-20 09:16:39 |
| `/usr/bin/docker` | `docker` | `1:29.9.1-1` | x86_64 | ELF64 PIE, x86-64, dyn | `566a4e83c1f148720e9628fbee98afcbe00867f0bfec819786f900c40f90d41a` | 30487344 | 2026-10-20 09:16:36 |

Build dates (pacman `Build Date`), same order: shfmt 2026-09-07 05:40:01; fzf 2026-10-11 07:18:11;
gum 2026-09-25 05:15:00; runc 2026-09-25 20:30:59; containerd 2026-10-14 05:29:22; lazygit 2026-10-16
10:28:42; docker 2026-10-15 10:58:57 (all -03).

## B. pnpm-managed esbuild — name + version + arch

Three `@esbuild/linux-x64` copies exist under `/home/vgpnk/Projects/kimi-code`; `pacman -Qo` reports
`error: No package owns …` for the binary (checked for 0.27.7), i.e. **not** pacman-managed. There is no
pacman `Architecture` field here, so QUALITY #4's arch term comes from each `package.json`
`"os": ["linux"], "cpu": ["x64"]` plus the observed ELF machine.

| absolute package.json | package name | version | declared os/cpu | package.json sha256 | binary sha256 | binary bytes |
|---|---|---|---|---|---|---|
| `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.21.5/node_modules/@esbuild/linux-x64/package.json` | `@esbuild/linux-x64` | `0.21.5` | linux / x64 | `cfcc162c440e93cc43afbf1edc478f4fc286c6ad16b8b850f3adc3e045a27165` | `b567f467fdac92c606717c86ea5cd1d6c30145c616776c0f2ff5429ad48586ba` | 9707520 |
| `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/package.json` | `@esbuild/linux-x64` | `0.25.12` | linux / x64 | `fdf02f1b53a4651a3eea731e2ad0a9c7d4fd8646430a5935d551e610e8d469fc` | `bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014` | 10358936 |
| `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.27.7/node_modules/@esbuild/linux-x64/package.json` | `@esbuild/linux-x64` | `0.27.7` | linux / x64 | `6b9abce611e097bff4eabc91090ecd5943af7ca00cdc56686453efe987d23585` | `c638273fcf95573ca74af586677800b4dd874c55f8f945adb54316d6902ba14b` | 11120788 |

Binary paths are `<package.json dir>/bin/esbuild`; all three are `ELF 64-bit LSB executable, x86-64,
statically linked, stripped`. Package.json sizes 372/373/372 B, distinct mtimes 2026-10-15 04:58:51–52.

Why three versions — direct lock evidence (observation):
- `0.21.5` ← `vite@5.4.21` dependency — `/home/vgpnk/Projects/kimi-code/pnpm-lock.yaml:18104-18106`.
- `0.25.12` ← `vite@6.4.2` dependency — `pnpm-lock.yaml:18114-18116`.
- `0.27.7` ← `vite@8.0.8` optionalDependency `pnpm-lock.yaml:18130-18139`; also `tsx@4.21.0`
  dependency `pnpm-lock.yaml:17888-17890`, and `vitest@4.1.4` peer chain
  `pnpm-lock.yaml:71`/`:252`. Each `<esbuild@V>` snapshot lists `'@esbuild/linux-x64': V`
  (`pnpm-lock.yaml:14251-14320`), so the installed platform packages match their host wrapper versions
  exactly (JS wrapper `package.json` versions: `.pnpm/esbuild@0.21.5:3`, `@0.25.12:3`, `@0.27.7:3`).

## Observations (O) / inference (I) / unknown (U)

- **O1** `/usr/bin/ctr` is owned by **containerd 2.4.2-1**, not `docker`. Any report pairing `ctr` with
  `docker 1:29.9.1-1` misattributes the file.
- **O2** `docker`'s pacman `Version` is the epoch form `1:29.9.1-1`. Upstream version is `29.9.1`,
  pkgrel `1`; the `1:` prefix is not part of the upstream version and must not be stripped in a pin.
- **O3** Dependency direction from `pacman -Qi`: `runc` ← Required By `containerd docker`;
  `containerd` ← Required By `docker`; `runc` `Depends On: libpathrs libseccomp`, `containerd`
  `Depends On: runc`. `shfmt`, `fzf`, `gum`, `lazygit` are required by nothing; `docker` Required By
  `ufw-docker`.
- **O4** Two install transactions, not one: `shfmt` 2026-10-19 18:31:23 versus the other six at
  2026-10-20 09:16:36–39. A pin taken before 2026-10-20 09:16:39 would have missed six of seven.
- **O5** `file(1)` prints `Go BuildID=…` for esbuild `0.21.5`/`0.25.12` but **not** for `0.27.7`, and
  for none of the seven pacman carriers. `file` output therefore neither proves nor disproves Go build
  info; do not use it as a Go-version probe.
- **O6** All seven pacman carriers are `Installed Size` 3.44–119.36 MiB packages whose `Validated By`
  is `Signature` — pacman's *record* of validation, not a re-verification performed here.
- **I1** The three esbuild versions coexist because three Vite majors (5/6/8) each pin their own esbuild;
  `0.27.7` is the one shared by `vite@8.0.8`, `tsx@4.21.0` and the `vitest@4.1.4` chain. (The lock
  edges are observed; "each major requires its own copy" is inference from the peer structure.)
- **U1** Go build-info versions for all seven pacman carriers and the three esbuild binaries were **not**
  read here (out of this ticket's package-identity scope; `rea inspect-go-binary` is the sibling lanes'
  surface). Nothing in this report should be read as a Go version claim.
- **U2** Did not run `pacman -Qkk` (file-list/checksum verification), did not hash the esbuild JS wrapper
  packages or install receipts, did not check `pacman -Qm`/signature keys. Only the binaries and
  package.json files named above were hashed.

## Calibration notes for QUALITY #4 use

1. Admissible identity for the pacman carriers: absolute path + package name + version + `x86_64`
   **and** the sha256 above; the weaker "package name + version + arch" fallback is unnecessary because
   hashing was practical (all < 31 MB).
2. For esbuild write `@esbuild/linux-x64 0.21.5/0.25.12/0.27.7 (os linux, cpu x64)` — never
   "Architecture: x86_64", which is a pacman field that does not exist for pnpm artifacts.
3. A sha256 here is "same bytes at the instant hashed", not stability across a run; pair it with the
   pre/post pin maps from `W/tools/pins.py` if a claim spans execution.
