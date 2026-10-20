# Scout — how a seat can still execute a Go carrier (round 20, D3 recon)

Seat: KaidokuR20.ScoutCarrierExecPaths-2 (read-only leaf; no subagents; **no Go binary executed**; no REA/Ghidra run).
Baseline `14f0260ad319ecc26994381b2415d5a999003375`; lane ref read `refs/heads/main = d1d981d2cc041dda4656c5b01d2c8445d8d17124`.
Taken `2026-10-20T17:52:56-03:00` (`date -Iseconds`). Installs this run: none.
Method: all probes run on C fixtures compiled into `mktemp -d /tmp/kr20-scout.*` (plus copies of `/usr/bin/true`), all removed. Nothing under `/home/vgpnk/.local/opt/go-*` was executed, directly or via a loader.

## Bottom line (all OBSERVED unless marked)

1. The 20 armed carriers are static `ET_EXEC`, `PT_INTERP=0`, mode `0644`; arm content and ctime match `manual-arm.json` (spot check). Direct `execve`, `sudo`/root, userns-root, `bwrap`, `dlopen`, `fexecve` on the file, `/proc/self/fd/N`, and `ld-linux <carrier>` are **all refused on this host**.
2. Of the ticket's four families: `ld-linux <carrier>` is dead here (needs `PT_INTERP`; none of the 20 has one), `go` on PATH is absent, `sudo` cannot exec an x-bit-less file (full caps, still `EACCES`) though it can `chmod` it, and copying works. The contract's declared limit (`contract.md:51-52`) therefore names the two mechanisms that do *not* work and omits the ones that do.
3. Execution is still reachable, **unprivileged and without touching the armed inode**: `memfd_create` + `fexecve` of the carrier bytes (memfd inode mode is `0777`) and `mmap(PROT_READ|PROT_EXEC)` + an in-process ELF loader. Both were demonstrated on fixtures; the second on a `0644` static `ET_EXEC` — the carriers' exact ELF shape.
4. Trivial mode/copy routes remain: `chmod u+x` as owner → `0744`, or copies made by `install -m 0755` → `0755`, or `tar -x` of a retained tarball (archive members are `-rwxr-xr-x`), or re-download.
5. Twenty-eight further Go toolchain ELFs are executable **right now** and outside the 20-file arm: `go-1.25.0` 9 (`755`), `go-1.27.3` 10 (`755`), module-cache 1.25.0 9 (`555`); three of the 28 are `bin/go`, the rest `gofmt` + `pkg/tool/linux_amd64/*`.
6. Committed lanes: `0` hits in all 20 non-kaidoku lanes. Kaidoku at `d1d981d` has `612` hits in `235` files, including two committed **scripts that spawn a Go binary** (`round-17/verify.py:162`, `round-18/carriers/build.sh:16`).

## Environment (observed)

| fact | probe | result | exit |
|---|---|---|---|
| `go` on PATH | `command -v go` / `type -a go` | empty | 1 / 1 |
| PATH | `echo "$PATH" \| tr ':' '\n' \| nl -ba` | 17 entries, none under `go-*` | 0 |
| go-named files in PATH dirs | `ls ~/.local/bin ~/.grok/bin ~/.opencode/bin ~/.kimi-code/bin ~/.local/share/omarchy/bin \| grep -E '^(go\|gofmt\|compile\|link\|asm\|vet\|cgo)$'` | none | 0 |
| mise | `ls ~/.local/share/mise/shims`; `ls ~/.local/share/mise/installs` | empty; only `.mise-installs.toml` | 0 / 0 |
| distro go | `pacman -Q go`; `ls /usr/lib/go* /usr/local/go /usr/bin/go` | `package 'go' was not found`; all absent | 1 / 2 |
| tree sizes | `find <tree> -type f \| wc -l`; `-perm -u+x \| wc -l` | go-1.24.6: 14175/42; go-1.25.0: 14496/51; go-1.27.3: 15657/54 | 0 |
| remaining x in 1.24.6 | `find … -perm /111 -printf '%M %p\n'` | 42 entries, **all** `.sh/.bash/.rc/.pl/wasm-exec` scripts; 0 ELFs | 0 |
| filesystem | `findmnt -T …` | `/home` btrfs `rw,…,noexec` absent; `/tmp` xfs `rw,nosuid,nodev`, noexec absent | 0 |
| loader | `ls -l /lib64/ld-linux-x86-64.so.2`; `--version` | root:root 755, glibc `2.44` | 0 / 0 |
| sudo | `sudo -n true`; `sudo -n -l` | rc 0; `(ALL : ALL) NOPASSWD: ALL`, also `(ALL) ALL` | 0 / 0 |
| root caps | `sudo -n sh -c 'id -u; grep CapEff /proc/self/status'` | `0`; `CapEff 000001ffffffffff` | 0 |
| groups | `id` | `967(docker),992(input),998(wheel)` | 0 |
| docker | `ls -l /var/run/docker.sock` | `srw-rw---- root:docker` | 0 |
| binfmt | `ls /proc/sys/fs/binfmt_misc/`; `cat …/status` | only `register`,`status`; `enabled` — **no handlers** | 0 |
| vehicles | `command -v …` | have: docker, runc, bwrap, setpriv, unshare, systemd-run, gcc; absent: qemu-*, podman, nix, firejail, nsjail, crun | 0 |
| home repo | `git -C /home/vgpnk rev-parse --show-toplevel`; `check-ignore -v …/bin/go` | `/home/vgpnk`; `~/.gitignore:23:/.local/*` → **untracked**, no `git checkout` restore path | 0 / 0 |

## Carrier state (observed)

| fact | probe | result |
|---|---|---|
| 20 armed ELFs | per-file `stat -c %a` + `readelf -h/-l` | all `644`, `Type: EXEC`, `INTERP=0` (2 `bin/*` + 18 `pkg/tool/linux_amd64/*`) |
| content | `sha256sum …/bin/go` | `d8a308e5…b404` = `manual-arm.json:7` |
| ctime | `stat -c %Z …/bin/go` | `1792528620` = `ctime_ns_after 1792528620603260252` (`manual-arm.json:11`) |
| arm coverage | `manual-arm.json` | 20 entries, all `mode_after "0o644"`; `exec_probe` `PermissionError` errno 13 (`:166-170`) |
| guard tool | `git cat-file -e <rev>:.ufo/waves/round-20/tools/carrier-guard.py` | absent at baseline **and** at `refs/heads/main` (exit 128 both); evidence dir holds only `manual-arm.json` |

## Vector table — "can a seat execute a carrier anyway?"

| # | vector | exact probe (fixture = `/usr/bin/true` or C build, mode `0644`) | observed | verdict |
|---|---|---|---|---|
| 1 | direct `execve` | `"$T/true"` | `Permission denied`, rc 126 | **blocked** |
| 2 | `ld-linux <carrier>` (static `ET_EXEC`, `interp=0`) | `/lib64/ld-linux-x86-64.so.2 "$T/s"` | `ld-linux-x86-64.so.2: cannot execute …: EACCES`, rc 127 | **blocked for these 20** |
| 3 | `ld-linux` condition test: `ET_EXEC` + `PT_INTERP` | `gcc -no-pie` fixture, `chmod 0644`, `ld.so …` | rc **7** (fixture `main`) | works ⇒ `PT_INTERP` is the discriminator |
| 4 | `ld-linux` on PIE (`ET_DYN`+`PT_INTERP`), no X | `gcc` default fixture `0644`, `ld.so …` | rc **7** | works |
| 5 | `ld-linux` on static-PIE (`ET_DYN`, `interp=0`), no X | `gcc -static-pie`, `ld.so …` | `EACCES`, rc 127 | blocked |
| 6 | `sudo <no-X path>` | `sudo -n "$T/true"` | `sudo: …: command not found`, rc 1 (front-end refuses before execve) | **blocked** |
| 7 | root shell `execve` | `sudo -n /bin/sh -c "$T/true"` (uid 0, full caps) | `/bin/sh: …: Permission denied`, rc 126 | **blocked** — kernel requires an x bit even for root here |
| 8 | userns root | `unshare -r -- "$T/true"` | `failed to execute …: Permission denied`, rc 126 | blocked |
| 9 | `bwrap` | `bwrap --dev-bind / / "$T/true"`; control `/usr/bin/true` | `execvp …: Permission denied` rc 1; control rc 0 | blocked |
| 10 | **owner `chmod`** (no privilege) | `chmod u+x "$T/true"`; `unshare -r -- chmod u+x` | `0744`, rc 0 both | **works** (mode restore; D3 `check` detects `mode_restored`+`ctime_changed`) |
| 11 | **`memfd_create`+`fexecve`** | python: `os.memfd_create` → write carrier bytes → `libc.fexecve` | memfd mode `777`; child exit **0** (also with `fchmod 755`) | **works**; inode never touched, invisible to arm/check |
| 12 | `fexecve` on the no-X **file** | `os.open(fx)` → `libc.fexecve(fd)` | `errno 13`, exit 113 | blocked |
| 13 | `exec /proc/self/fd/N` | fork + `os.execve("/proc/self/fd/N")` | `errno 13`, exit 113 | blocked |
| 14 | `dlopen` of static `ET_EXEC` | `ctypes.CDLL(fixture)` | `cannot dynamically load executable` | blocked |
| 15 | `mmap(PROT_EXEC)` of no-X file | `mmap.mmap(fd, 0, prot=READ\|EXEC)` | **OK**, len 43320 | works (primitive) |
| 16 | **custom in-process ELF loader** | 40-line C loader (map `PT_LOAD`s RWX, jump to `e_entry`) on `0644` static `ET_EXEC` | loader exit **7**; direct run 126 | **works**; no execve, no X check |
| 17 | copy, `cp -p` / `cp` | `cp -p` then stat | `644` preserved | no X |
| 18 | copy, `install -m 0755` | `install -m 0755 /usr/bin/true …` | `755` | **works** |
| 19 | copy, `tar -x` | `tar -cf/-xf` of a `0644` fixture | `644` | no X |
| 20 | tarball extraction (real) | `tar -tvzf /tmp/kr18-dl/go1.24.6.linux-amd64.tar.gz go/bin/go …` | `-rwxr-xr-x … go/bin/go`, `gofmt`, `compile`, `link` | **works**: extraction yields 0755 |
| 21 | retained tarballs on disk | `find /home/vgpnk /tmp /var/tmp /var/cache/pacman/pkg -maxdepth 4 -name 'go1.2*linux-amd64*'` | 6 files: `/tmp/kr18-dl/go1.24.6` (78583176 B), `/tmp/kr18-dl/go1.25.0`, `/tmp/kr19-SourcesRowsDraft-fetch/go1.25.0`, `/tmp/go1.25.0`, `/tmp/go1.24.6`, `/tmp/kr20-c3-dl-Ac2DpQ/go1.24.6`; mod-cache zip `64217136 B` | **works** (tar/unzip) |
| 22 | other executable toolchains | per-tree scan of `bin/*` + `pkg/tool/linux_amd64/*` for ELF magic + `-x` | `go-1.25.0` 9 × `755`, `go-1.27.3` 10 × `755`, mod-cache 1.25.0 9 × `555` (28 ELFs: 3 `bin/go`, 3 `gofmt`, 22 `pkg/tool`) | **works, no bypass needed** |
| 23 | `go` on PATH | `command -v go` | absent (see Environment) | not reachable |
| 24 | `binfmt_misc` | handler inventory; qemu absent | enabled, **0 handlers**; qemu not installed | n/a now; a root-registered handler or an installed qemu-user would be a user-mode loader (INFERENCE) |
| 25 | rootful docker | membership + socket only (daemon not contacted) | `docker` group, socket present | **[INFERENCE]** container root can `chmod`/exec a bind-mounted carrier; not exercised |

## D3 declared-limit calibration

Text under review: `contract.md:51-52` — "Declared limit: loader-mapped execution (`ld-linux … <file>`) and root are not prevented."

- [O] Neither named mechanism runs these 20 files: `ld-linux <carrier>` prints `cannot execute …: EACCES` and exits 127 (mechanism below is [I]: a `PT_INTERP=0` target falls back to a re-exec, where the kernel's X check applies), and root's `execve` of an x-bit-less file is refused (rows 2, 5, 7). Both statements are empirically false *for the armed carriers*, though each is true of other object classes (dynamic/PIE files; a root who first chmods).
- [O] The working routes are not named: memfd+`fexecve` (row 11) and a custom mmap loader (rows 15-16) run the bytes with the inode unchanged, and owner `chmod`/copy routes (rows 10, 18, 20, 22) are unprivileged or one command away.
- [O] Consequence for `check`: arm/check compares mode, ctime and sha256 only (`contract.md:47-49`). A green `check` is therefore compatible with a carrier having run via rows 11/16 — the same gap `corpus/lessons/round-19.md:90` records ("SHA-256 checks do not detect prior execution"). `check` is a *tamper detector for the inode*, not an execution detector.
- [O] Scope gap: the arm covers 20 ELFs under `go-1.24.6`; **28** more toolchain ELFs are executable now (row 22), and `1.25.0`/`1.27.3` were never armed (independently noted by `w1/ScoutGo1273Exposure.md:133-136`).

Suggested replacement wording (drop-in for `contract.md:51-52`): "Not prevented, by construction: (a) mode restore by the owner or root (`chmod`) — arm is detection-only, and an arm without `check` is not evidence of non-execution; (b) any copy made from the bytes (`install -m`, `tar -x` of the 0755 archive members, re-download, module-cache); (c) memory-only execution that never touches the inode — `memfd_create`+`fexecve` and `mmap(PROT_EXEC)`+custom loader — for which `check` can be green; (d) the 1.25.0/1.27.3/module-cache trees outside the manifest. Not effective for the 20 armed carriers on this host: `ld-linux <file>` (all are `ET_EXEC`, `PT_INTERP=0`; glibc 2.44 refuses with `EACCES`) and direct root exec (kernel refuses x-bit-less files; root's route is `chmod`, which `check` sees)."

## Committed references to the Go trees as tools

- [O] Non-kaidoku lanes: `for d in /home/vgpnk/Projects/shokunin/*-shokunin; do git --no-optional-locks -C "$d" grep -I -n -E -e '\.local/opt/go-1\.(24\.6|25\.0|27\.3)|toolchain@v0\.0\.1-go1\.' <main|master> | wc -l; done` → **all 20 lanes `hits=0`**; exit 0. (No other lane references these paths at all.)
- [O] Kaidoku at `d1d981d`: `612` hits in `235` files. Execution-shaped committed code:
  - `.ufo/waves/round-17/verify.py:162` — `run(… ["/home/vgpnk/.local/opt/go-1.27.3/bin/go", "version", "-m", …])`: a committed tool that spawns an unarmed (0755) toolchain binary.
  - `.ufo/waves/round-18/carriers/build.sh:16` — `GO=$HOME/.local/opt/go-$ver/bin/go`, then `$GO build …`: committed build recipe that executes 1.24.6/1.25.0.
  - Historical run receipts in reports: `round-18/w1/ScoutAbiSwissLayout.md:146-149` (`bin/go version`, `env GOEXPERIMENT`, exit 0), `round-18/w2/CarrierRebuild.md:11`, `round-18/w1/DraftAbiRow.md:38` (`go run main.go`), `round-18/w2/Runs1250noswissnomethods.md:111` (`go build`), `round-18/w1/CarrierRecipeAudit.md:78,84`, `round-17/w2/ReopenS026.md:76,78`.
  - Admission of the round-19 breach: `.ufo/waves/round-20/gen-wave1.py:103` ("a seat ran `bin/go version` despite the no-carrier-execution contract").
- [O] Remaining hits are subject metadata / predictions / receipts (e.g. `round-19/runs/*/receipt.json`), not invocations; `round-19/gen-predictions.py:27` uses `"bin/go"` as a **label**.
- Method note: the `grep` tool with path `/home/vgpnk/Projects/shokunin/*-shokunin` returned "No matches" for a pattern that provably exists (contract.md:88) — the glob is not expanded by that tool. Lane-wide scan was therefore done per repo with `git grep` at each lane's branch; a single-path `grep` probe was used only to validate the finding.

## Residual unknowns (declared)

- [INFERENCE] `qemu-x86_64` is absent; if installed it would open the carrier read-only and map it (the mmap primitive in row 15 is observed, qemu itself was not run). Same class: `rc`/`fastload`-style user-mode loaders.
- [INFERENCE] rootful `docker`/`runc` (`docker` group + socket observed) can chmod a bind-mounted carrier, then exec it as root with X present; the daemon was not contacted, so this is untested.
- [INFERENCE] No Go carrier was run under the custom loader (forbidden); the demonstrated object is a `0644` static `ET_EXEC` C fixture. A Go `ET_EXEC` also needs its runtime's stack/TLS setup, which `_rt0_amd64` performs itself — plausible, not observed.
- [INFERENCE] `ld.so` behaviour is glibc 2.44-specific; the observed `PT_INTERP` dependence is a property of this loader build, not asserted for other versions.
- Kernel exec semantics (root refused without an x bit) are observed on Linux 7.2.11 only.

## Command ledger (each with exit)

1. `command -v go` → empty, 1; `type -a go` → 1.
2. `ls -d /usr/lib/go* /usr/local/go /usr/bin/go /usr/local/bin/go` → all missing, 2; `pacman -Q go` → not found, 1.
3. `find /home/vgpnk/.local/opt/go-1.24.6 -type f -perm /111 -printf '%M %p\n'` → 42 scripts, 0.
4. `for f in …/bin/* …/pkg/tool/linux_amd64/*; do stat+readelf; done` → 20 × `644 EXEC interp=0`, 0.
5. `sha256sum …/bin/go` → `d8a308e5…`, 0; `stat -c 'mode=%a ctime=%Z'` → `644`, `1792528620`, 0.
6. `git -C <lane> cat-file -e <rev>:…/carrier-guard.py` → fatal, **128** (both revs).
7. `T=$(mktemp -d); cp /usr/bin/true $T/true; chmod 0644`; `$T/true` → `Permission denied`, **126**.
8. `printf 'int main(){return 7;}' | gcc -static …; chmod 0644; $T/s` → 126; `ld.so $T/s` → `EACCES`, **127**; `chmod 0755; ld.so $T/s` → **7**.
9. `gcc -no-pie …; chmod 0644; ld.so $T/e` → **7**; `gcc -static-pie …; chmod 0644; ld.so $T/sp` → `EACCES`, **127**.
10. `sudo -n $T/true` → `command not found`, **1**; `sudo -n sh -c "$T/true"` → `Permission denied`, **126**.
11. `unshare -r -- $T/true` → **126**; `bwrap --dev-bind / / $T/true` → **1** (control `/usr/bin/true` → 0).
12. `chmod u+x` / `unshare -r -- chmod u+x` → **0**, mode `744` both.
13. python memfd: `memfd_default_mode: 777`; `memfd_fexecve_default_mode: exit=0`; `file_fexecve_noX: exit=113`; `proc_self_fd_exec_noX: exit=113`; `dlopen_static_EXEC: refused`; `mmap_PROT_EXEC_on_noX: OK len=43320`.
14. custom loader: `$T/f` → **126**; `$T/ldr $T/f` → **7**.
15. `install -m 0755` → `755`; `cp -p` → `644`; `tar -x` of `0644` member → `644`.
16. `tar -tvzf /tmp/kr18-dl/go1.24.6.linux-amd64.tar.gz go/bin/go …` → `-rwxr-xr-x` ×4, 0.
17. `find /home -xdev -maxdepth 10 -type f -name go -perm -u+x` → 3 paths, 0; mod-cache `pkg/tool` → 7 × `555`, 0.
18. lane scan: 20 lanes `hits=0`; kaidoku `612` hits / `235` files, 0.
19. `git grep -n -e 'bin/go' refs/heads/main -- '*.py' '*.sh'` → 6 files, 0 (2 execution sites, 3 text/comment, 1 false positive `godot`).
20. `date -Iseconds` → `2026-10-20T17:52:56-03:00`, 0. Fixture dirs removed (`rm -rf`, 0).
