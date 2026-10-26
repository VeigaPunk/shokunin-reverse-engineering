# R36SentinelInstall — sasquatch install security review + AppImage execution boundary

- Wave: kaidoku-shokunin round 36, wave 1 (build drafts + first falsifiers). Lane root
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`.
- Seat: leaf sentinel. Advisory only — nothing frozen changed (no counter, predicate, carrier,
  oracle, receipt, PROVINCE/README/SCORECARD line touched). No subagents, no background jobs, no
  `agent://all`.
- Scratch: `/fast/scratch/hyaku/kaidoku-r36/R36SentinelInstall` — created, used, removed at exit.
  Every artifact cited below is inlined here; nothing depends on a scratch path.
- Tooling: **nothing installed or upgraded** (`pacman` untouched; no `uv`/`npx`/release binary added).
  Used as found: `curl 8.23.0`, `ar`/`tar` 1.35, `readelf`/`objcopy` (binutils 2.45), `strace 7.2`,
  `unsquashfs`/`mksquashfs` 4.7.5, `getcap`/`getfattr`/`getfacl`, `python3 3.14.8`, `sha256sum`.
- No VCS mutation of any kind; no REA invocation (not this seat's route).

## Verdict

**PASS with two low-severity provenance findings and one extractor-behaviour defect.** The installed
`sasquatch` and `sasquatch-v4be` are byte-for-byte the payload of the official onekey-sec
`sasquatch_1.0_amd64.deb` (release tag `sasquatch-v4.5.1-6`), whose upstream-published GitHub asset
digest is `efbc92bd…ade95`; neither binary carries setuid/setgid bits, file capabilities, xattrs,
ACLs or RPATH/RUNPATH; both link only system libraries that all resolve; neither contains network or
exec primitives (traced: 1 `execve` — itself — and 0 network syscalls on a full extraction). Nothing
else named `sasquatch` resolves on this PATH. The residual risks are (a) the extractor binary is
resolved by **bare name over PATH**, where three user-writable directories precede `~/.local/bin`
(thirteen of the twenty PATH entries are user-writable), and the frozen C1 counter never reads the
digest the harness records; (b) sasquatch
opens output paths with `openat(AT_FDCWD, …, O_WRONLY|O_CREAT|O_TRUNC)` — **no `O_NOFOLLOW`** — so a
pre-existing symlink inside `-d` redirects writes outside the output tree (reproduced; blocked in the
REA pipeline by unblob's Landlock sandbox, which I verified independently). On the AppImage question:
the C1 pipeline never executes the AppImage runtime — but a wave-1 peer seat did execute it
(`R36ExecAppImageExtract.md`), and that is the real boundary: `--appimage-extract` runs an 11 MB
third-party static binary as the invoking user, and nothing in the type-2 runtime gates extraction on
signature verification.

| # | severity | surface | one-line |
|---|---|---|---|
| S1 | LOW | extractor provenance in the frozen measurement | `c1-counter.py` never compares the recorded `sasquatch_sha256` to a frozen digest |
| S2 | LOW | PATH resolution | bare-name `execvp` lookup with 3 user-writable dirs ahead of `~/.local/bin` (13 of 20 entries writable); unblob inherits the full environment (incl. `LD_PRELOAD`) |
| S3 | LOW (INFO in-pipeline) | extractor write path | `sasquatch -f -d D I` follows symlinks already present under `D` and overwrites the target outside `D` |
| S4 | INFO | parser on untrusted input | memory-unsafe C parser, unprivileged, FS-confined only by Landlock — no seccomp/namespace isolation |
| S5 | INFO | AppImage boundary | `--appimage-extract` executes shipped code; digest gate, not a signature check, is the only integrity control |
| S6 | INFO | post-extraction metadata | mode bits preserved (incl. 0700), setuid/setgid stripped, `user.*` xattrs from the image are planted in the extraction tree |

---

## 1. Artifacts under review

```
-rwxr-xr-x 1 vgpnk vgpnk 382824 Oct 26 01:22 /home/vgpnk/.local/bin/sasquatch
-rwxr-xr-x 1 vgpnk vgpnk 436232 Oct 26 01:22 /home/vgpnk/.local/bin/sasquatch-v4be
```

| property | `sasquatch` | `sasquatch-v4be` |
|---|---|---|
| sha256 | `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` | `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` |
| md5 | `44be48a21751dd2f9368a5c92df8addc` | `33445a06b126873ec7e9198e20b5871a` |
| size | 382824 | 436232 |
| type | ELF 64-bit LSB **pie** executable, x86-64, dynamically linked, stripped | same |
| interpreter | `/lib64/ld-linux-x86-64.so.2` | same |
| BuildID[sha1] | `96e3fa396ab92666dd5845e8b9cd44b1b704fa87` | `8facea802d3b89a59b136fe76e336c88cfe8a87d` |
| mode / owner / links | `755`, `vgpnk:vgpnk`, nlink 1, regular file (not a symlink) | `755`, `vgpnk:vgpnk`, nlink 1, regular file |
| `-version` | `unsquashfs version 4.5.1 (2022/03/17)` / `copyright (C) 2022 Phillip Lougher` | identical |

Two **distinct builds**, not a copy: different BuildIDs, sizes, section offsets and hashes; the
`.gnu_debuglink` names embed each BuildID (`e3fa396ab926…debug` / `acea802d3b89…debug`), matching the
upstream `sasquatch-dbgsym_1.0_amd64.deb` naming. Both derive from squashfs-tools 4.5.1 and print the
same version banner — the `sasquatch` patch adds vendor-image support, `sasquatch-v4be` is the
big-endian variant unblob selects for BE v4 images.

## 2. Privilege and hardening surface

Setuid/setgid/capabilities/attributes — all clean:

```
$ find ~/.local/bin/sasquatch ~/.local/bin/sasquatch-v4be -maxdepth 0 \( -perm -4000 -o -perm -2000 \) -print
(no output)
$ getcap ~/.local/bin/sasquatch ~/.local/bin/sasquatch-v4be            -> (no output)
$ getfattr -d -m - ~/.local/bin/sasquatch                              -> (no output)
$ getfacl -p ~/.local/bin/sasquatch
user::rwx group::r-x other::r-x                                        (no ACL entries)
$ stat -c 'mode=%a uid=%u gid=%g links=%h' …                           -> mode=755 uid=1000 gid=1000 links=1
$ lsattr ~/.local/bin/sasquatch ~/.local/bin/sasquatch-v4be
---------------------- /home/vgpnk/.local/bin/sasquatch                (no immutable/append-only bits)
```

ELF hardening:

| check | `sasquatch` | `sasquatch-v4be` |
|---|---|---|
| RPATH / RUNPATH (`readelf -d \| grep -Ei 'rpath\|runpath'`) | none | none |
| PIE | `Type: DYN`, `FLAGS_1: PIE` | same |
| BIND_NOW / full RELRO | absent (`grep -c BIND_NOW` = 0) → partial RELRO (GNU_RELRO present) | same |
| GNU_STACK | `RW` (no `E`) → NX stack | same |
| stripped | yes (no `.symtab`; only `.gnu_debuglink`/`.gnu_debugaltlink`) | yes |

No appended data — the file ends exactly where the section header table ends, so nothing is smuggled
past the last section:

```
sasquatch   e_shoff=380840  e_shnum=31  e_shentsize=64  SHT_end=382824  file=382824  tail_pad=0
v4be        e_shoff=434248  e_shnum=31  e_shentsize=64  SHT_end=436232  file=436232  tail_pad=0
```

Dynamic dependencies — system libraries only, all resolve from `/usr/lib`:

```
libpthread.so.0 libz.so.1 liblzma.so.5 liblzo2.so.2 liblz4.so.1 libzstd.so.1
libstdc++.so.6 libm.so.6 libgcc_s.so.1 libc.so.6      (both binaries, identical set)
$ ldd ~/.local/bin/sasquatch | grep -c 'not found'   -> 0
```

Static string surface: no `http(s)://` fetch, no `curl`/`wget`, no `/bin/sh`, no `system(`/`popen`/
`execv*`, no `dlopen`/`LD_PRELOAD`, no `/tmp/` paths. The only URLs are documentation pointers
inherited from squashfs-tools:

```
read here https://github.com/plougher/squashfs-tools/blob/master/README-4.5.1
https://github.com/plougher/squashfs-tools/blob/master/USAGE
```

Runtime syscall profile (`strace -f -e trace=network,execve,execveat`, full extraction of a 2-file
image, exit 0): **exactly one `execve`** — the process itself — and **zero** `socket`/`connect`/
`sendto`/`bind` lines. The binary neither spawns helpers nor talks to the network.

## 3. Provenance — upstream digest chain, closed end to end

Every link below was observed in this seat, not carried over:

| link | evidence |
|---|---|
| upstream-published asset digest | GitHub asset row for `sasquatch_1.0_amd64.deb` in `releases/expanded_assets/sasquatch-v4.5.1-6` carries `sha256:efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95` (183 KB) |
| downloaded deb | `curl -fsSL -o deb-sasquatch-v4.5.1-6.deb …/releases/download/sasquatch-v4.5.1-6/sasquatch_1.0_amd64.deb` → 187244 bytes, sha256 `efbc92bd…ade95` (**matches** the assignment value and the upstream digest) |
| deb structure | `ar t` → `debian-binary`, `control.tar.xz`, `data.tar.xz`; `data.tar.xz` holds `./usr/bin/sasquatch` (382824) and `./usr/bin/sasquatch-v4be` (436232), mode `-rwxr-xr-x root/root`, mtime `2022-02-26 14:38` |
| deb-internal checksums | `control.tar.xz:/./md5sums` declares `44be48a2…  usr/bin/sasquatch` and `33445a06…  usr/bin/sasquatch-v4be` — equal to the md5 of the installed files |
| installed vs payload | `cmp -s` → **IDENTICAL** for both binaries (byte-for-byte) |
| receipts | every `K1..K4/after-run.json` records `sasquatch: /home/vgpnk/.local/bin/sasquatch`, `sasquatch_sha256: ad02d27a…c774754`, `sasquatch_version: unsquashfs version 4.5.1 (2022/03/17)` — equals the binary audited here |

Deb control (provenance context, not a trust anchor of its own — the deb carries no signature;
fields verified verbatim in `control.tar.xz:/./control`, shown here compressed onto fewer lines):

```
Package: sasquatch   Version: 1.0   Architecture: amd64
Maintainer: Marton Illes <marton.illes@onekey.com>
Depends: libc6 (>= 2.14), libgcc-s1, liblz4-1, liblzma5, liblzo2-2, libstdc++6, libzstd1, zlib1g
Homepage: https://github.com/onekey-sec/sasquatch
Description: Tool to extract vendor specific SquashFS images
```

Caveats, stated plainly:

- The deb is **not signed** (no `debsig`/`dpkg-sig` member), and neither GitHub release publishes a
  checksum sidecar file (asset list checked: only `.deb`, `-dbgsym`, and source archives). Authenticity
  therefore rests on TLS to `github.com` plus GitHub's asset-digest metadata, which is what the table
  above closes. That is stronger than "the L1 downloaded something" and weaker than a signed artifact.
- Installed mtime is `2026-10-26 01:22` while the payload's is `2022-02-26 14:38` — consistent with an
  `ar`/`tar` extraction + copy into `~/.local/bin` (i.e. **not** a `dpkg -i`), which is exactly what
  the operator rule ("official release binary into `~/.local/bin`") prescribes. Byte-identity, not
  mtime, is the evidence that matters here.
- `Installed-Size: 811` (KiB) is consistent with the 800 KiB of binaries; nothing else is shipped
  except `changelog.gz` (143 B) and `copyright` (1647 B).

## 4. PATH shadowing

Method: walk every `PATH` element, test `-e`/`-x` for both names; then `command -v`/`type -a`/
`compgen -A command`; check shell aliases and exported functions; check `pacman -Qo` (no package owns
either file); scan `/usr`, `/usr/local`, `/opt`, `/var/lib`, `~/.cache`, `~/.npm`, `/fast/scratch` for
any other `sasquatch*` executable.

```
PATH-HIT /home/vgpnk/.local/bin/sasquatch       -> /home/vgpnk/.local/bin/sasquatch
PATH-HIT /home/vgpnk/.local/bin/sasquatch-v4be  -> /home/vgpnk/.local/bin/sasquatch-v4be
/usr/bin, /usr/local/bin, /usr/local/sbin: no such file
pacman -Qo /home/vgpnk/.local/bin/sasquatch -> error: No package owns …
bash -ic 'alias | grep -i sasq' -> (none);  declare -F | grep -i sasq -> (none);  env | grep BASH_FUNC -> (none)
find /usr /usr/local /opt /var/lib ~/.cache ~/.npm /fast/scratch -maxdepth 8 -name 'sasquatch*' -> (no hits)
```

**No shadow exists today.** But the resolution path is unpinned and the PATH is largely user-writable
— **three** directories precede `~/.local/bin` (entries 1-3), and thirteen of the twenty entries are
writable by `vgpnk`, all mode `755` owned by `vgpnk`:

| # | directory | owner | precedes `~/.local/bin`? |
|---|---|---|---|
| 1 | `/run/user/1000/fnm_multishells/6713_…/bin` | vgpnk | yes |
| 2 | `/home/vgpnk/.local/share/fnm` | vgpnk | yes |
| 3 | `/home/vgpnk/.opencode/bin` | vgpnk | yes |
| 4 | `/home/vgpnk/.local/bin` | vgpnk | — (the audited entry) |
| 5,6 | `~/.local/share/mise/{installs/node/latest/bin,shims}` | vgpnk | no |
| 7,9 | `/run/user/1000/fnm_multishells/{2590,1600}_…/bin` | vgpnk | no |
| 8 | `~/.local/share/omarchy/bin` | vgpnk | no |
| 10-16 | `/usr/local/{sbin,bin}`, `/usr/bin`, `/usr/lib/jvm/default/bin`, perl dirs | root | no |
| 17-20 | `~/.minimax/bin`, `~/.minimax-code/bin`, `~/.grok/bin`, `~/.kimi-code/bin` | vgpnk | no |

How the extractor is actually resolved (so the exploit path is concrete, not hypothetical):

- `~/…/unblob/handlers/filesystem/squashfs.py:25-26` — `EXECUTABLE = "sasquatch"`,
  `V4BE_EXECUTABLE = "sasquatch-v4be"`; argv built at `:54` and `:56-62`:
  `["sasquatch", "-le"|"-be", "-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"]`.
- `~/…/unblob/extractors/command.py` — `subprocess.run(cmd, …)` with `cmd` a **list** (`shlex.join` is
  only for the debug log): no shell, so no word-splitting/filename-injection; but the executable is a
  bare name → `execvp` PATH lookup at exec time, and the call passes **no `env=`**, so the parent
  environment (`PATH`, `LD_PRELOAD`, `PYTHONPATH`) is inherited by the extractor.
- The missing-dependency report is raised only from the `FileNotFoundError` handler. A **shadow that
  exists but misbehaves** produces a different signal (`ExtractCommandFailedReport`) — so
  "`missing-extractor-dependency`" proves *absence*, not authenticity.

## 5. Extractor behaviour on hostile input (parser tests, all in scratch)

Crafted images with `mksquashfs` 4.7.5 (uncompressed metadata for patching), run with unblob's exact
argv. sasquatch 4.5.1 behaves defensively on the classic squashfs extraction CVEs:

| probe | result |
|---|---|
| directory entry renamed `aa` → `..` (length-preserving patch at offset 290) | `File system corrupted: invalid characters in name` / `FATAL ERROR: dir_scan: failed to read directory out`, **rc=1**, 0 files written — names containing `.`/`..` are rejected before any path is built (the same message `unsquashfs` 4.7.5 emits; **[INFERENCE]** this is the squashfs-tools 4.5 name-sanitisation series, not verified against an upstream commit here) |
| truncated multi-file image (data table/id table cut off) | `Read on filesystem failed because EOF` / `read_id_table: failed to read id index table` / `FATAL ERROR: File system corruption detected`, **rc=1**, 0 files — `-no-exit-code` does **not** mask fatal corruption |
| image storing mode `4755` (verified stored: `-rwsr-xr-x` via `unsquashfs -ll`) | extracted as `-rwxr-xr-x` 755 with `umask 000` → **setuid stripped**; ordinary modes preserved (`0700`→700, `0640`→640) |
| image carrying `user.k="planted"` | extracted with the xattr (`getfattr` → `user.k="planted"`), same as unsquashfs 4.7.5 — `security.capability` would need privilege we do not have |

**Defect found — writes are not confined to `-d`.** sasquatch opens each output path relative to the
CWD with no `O_NOFOLLOW` and no `dirfd`:

```
$ strace -e trace=openat -o tl.txt sasquatch -le -no-exit-code -f -d outL i2.sqsh
openat(AT_FDCWD, "outL/target.txt", O_WRONLY|O_CREAT|O_TRUNC, 0644) = 4        # -f  (unblob's argv)
openat(AT_FDCWD, "outN/target.txt", O_WRONLY|O_CREAT, 0644)        = 4        # no -f
```

With `outL/target.txt` pre-created as a symlink to `../victimL.txt`:

```
before: victimL.txt = "ORIGINAL-OUTSIDE\n"     sha256 f4890b17…abc14
after : victimL.txt = "FROM-IMAGE\n"           (outL/target.txt is still a symlink)
no -f : victimN.txt = "FROM-IMAGE\nNTINEL-MARKER\n"  (25 B — prefix overwritten, no truncate)
```

The same probe against `unsquashfs` 4.7.5 **replaces** the symlink with a regular file and leaves the
outside file untouched (`victim2.txt` still `ORIGINAL-OUTSIDE`). So this is a genuine sasquatch-only
weakness, not a general squashfs-tools property, and it is exactly the class modern unsquashfs
hardened.

Containment in the REA pipeline — verified, not assumed. unblob wraps extraction in a Landlock
sandbox (`unblob/sandbox.py`: `AccessFS.read("/")` plus read-write only on `extract_root`,
`/dev/shm`, the log and the report parent), and Landlock is live on this host
(`/sys/kernel/security/lsm` = `capability,landlock,lockdown,yama,bpf`). I drove unblob's own binding
directly:

```
$ ~/.local/share/uv/tools/unblob/bin/python -c 'restrict_access(AccessFS.read("/"), AccessFS.read_write(base+"/allowed"))'
restrict_access(*rules): applied
inside-allowed:            ALLOWED-WRITE  <base>/allowed/fresh.txt
outside:                   DENIED  PermissionError: [Errno 13] Permission denied
symlink-inside->outside:   DENIED  FileNotFoundError: [Errno 2]   (target left untouched)
```

Two caveats worth recording: `Sandbox._try_enter_sandbox` **swallows** `SandboxError` and continues
with a warning ("Sandboxing FS access is unavailable on this system, skipping"), and `--no-sandbox`
exists. REA attests it does not pass that flag (receipt limitation [2]: *"Unblob's default sandbox and
skip rules remain enabled. … Extracted code is never executed; only regular files are published,
without executable permission bits."*), and `--no-sandbox` appears **nowhere** in
`dist/firmware/FirmwareProvider.js` (`grep -c` → 0; the string exists only in the browser/chromium
modules). The quoted flag literals in that file — which cover both engines — are `--depth
--extract-dir --log --process-num --quiet --randomness-depth --report --search-all --threads`.
Landlock is
**filesystem-only**: it does not bound memory, CPU or syscalls, so a memory-corruption bug in the C
parser remains an RCE inside the user's session (unblob is additionally wrapped in `/usr/bin/prlimit`
by REA per `raw_result.execution`/`version_execution`).

## 6. AppImage execution boundary

What the C1 pipeline does with K3/K4 — **data only, no execution**:

- no `appimage` handler exists in unblob; the after receipts show the AppImage split as
  `elf64` + `padding` chunks plus one `squashfs_v4_le` chunk at the ELF end —
  K3 `{offset: 944632, length: 10510336}` (ends exactly at EOF 11454968), K4
  `{offset: 936456, length: 10420224}` (ends at EOF 11356680) — then extracted by sasquatch.
- the frozen C1 harness (`tools/round-36/c1-run.sh`) has no AppImage invocation: the only
  `AppImage` token under `tools/round-36/` is a prose comment (`c1-run.sh:12`, describing the ELF-end
  offset), and no `--appimage` flag appears in any `.sh`/`.py` under `tools/round-36/`. Lane-wide the
  only executable `.sh`/`.py` hits are scaffolding, not the pipeline:
  `.ufo/waves/round-23/tools/setup-sigrok.py:30` builds `argv = [str(source), '--appimage-extract']`
  for a third-party sigrok AppImage, and the wave generators (`.ufo/waves/round-{22,23}/gen-wave1.py`,
  `.ufo/waves/round-36/w1-gen.py:59,85`) carry that route in dispatch prose. **Executing AppImages is
  a lane-tooling precedent, not a C1 pipeline property.**

What `--appimage-extract` would do — and did do in this wave, in a peer seat, not in the pipeline
(`R36ExecAppImageExtract.md`: `chmod 0755` then `./nvim-linux-x86_64.appimage --appimage-extract`,
under `strace`, exit 0). Facts I established **without executing** the carrier (byte inspection only):

```
e_ident[8:11] = b'AI\x02'            type-2 ABI marker
sections: .appimage (magic), .static, .digest_md5, .upd_info, .sha256_sig, .sig_key
file type: ELF 64-bit LSB pie, static-pie linked, stripped, no NEEDED entries
ELF end = e_shoff + e_shnum*e_shentsize = 944632 (K3) / 936456 (K4) = first 'hsqs' byte
runtime help (rodata @ 557705): "--appimage-extract [<pattern>]  Extract content from embedded filesystem image",
  "--appimage-signature  Print digital signature embedded in AppImage", "--appimage-offset", "--appimage-mount"
runtime strings: fusermount, /AppRun, "Failed to open squashfs image", "mkdir_p error",
  squashfuse + zlib/lzma/lzo/lz4/zstd decompressor identifiers
```

Boundary statement:

1. `--appimage-extract` (and even `--appimage-offset`) **executes the shipped runtime** — ~11 MB of
   third-party code (here `type2-runtime@8f39b89` built on squashfuse, static-pie) running as the
   invoking user, with the user's filesystem and network reach. The artifact author controls every
   byte of that runtime; the payload and the runtime are one signed-or-not blob.
2. Nothing in the type-2 runtime verifies `.sha256_sig` on the extraction path — the section is only
   *printed* (`--appimage-signature`). [INFERENCE: derived from the help text plus the absence of any
   `verify` string in the runtime; the load-bearing, observed part is that extraction proceeds with no
   signature input.] So the only integrity control is the digest comparison, which is what the lane
   did **before** executing: `carriers.json` K3 `b644d034…f29fb`, K4 `8efcec73…e1c2`, and I re-derived
   both — downloads reproduce those digests exactly, and GitHub's own asset rows publish the same two
   values (`nvim-linux-x86_64.appimage` → `b644d034…`, `nvim-linux-arm64.appimage` → `8efcec73…`).
3. Peer containment during that execution was `strace` + scratch isolation (they recorded 1 `execve`,
   0 forks, no `/dev/fuse` access) — *observation*, not *confinement*. Anyone repeating the AppImage
   route should treat the exec as arbitrary-code execution: run it in a throwaway namespace/`bwrap`
   or at minimum a scratch cwd, never with privileges, and only after the sha256 gate.
4. Once extracted, `AppRun` (91 B), `usr/bin/nvim` etc. are **data** as far as REA is concerned; the
   published 2147-file set in `K3/after.json` includes them but nothing runs them, and REA publishes
   without executable bits.

## 7. Findings, exploit paths, smallest remediation

**S1 — the frozen counter does not pin the extractor binary (LOW).**
Evidence: `tools/round-36/c1-counter.py` checks `provider.id == 'unblob'` (line 173), the carrier
digest against `carriers.json` (line 172), the gap kind (line 124-127) and the oracle-file binding
(line 188-189) — but it never reads `after-run.json`'s `sasquatch_sha256`, which the harness records
for exactly this purpose. Exploit path: a run whose `sasquatch` is a shim (e.g. a script that calls
`/usr/bin/unsquashfs`) satisfies `carriers_matched == 4` and `met_target` while the coverage claim
("sasquatch on PATH" ⇒ the onekey-sec binary) is false. Impact: not fabricated data — the oracle
binding and the committed before/after receipts still have to line up — but **non-reproducible
provenance inside a frozen claim**: the claim's own text says sasquatch, the counter cannot tell. The
payload-forgery control (CTL-C1-2) does not cover it. Smallest remediation (next round, not this
frozen commit): have the counter require `after-run.json:sasquatch_sha256 == ad02d27a…c774754` for all
four carriers, and/or make `c1-run.sh` fail closed (`[[ $sqsha == <frozen> ]] || exit 2`) so the
receipts cannot record a substituted binary in the first place.

**S2 — PATH-resolved extractor with user-writable predecessors (LOW).**
Evidence §4: bare-name `execvp`, three `vgpnk`-owned dirs before `~/.local/bin` (thirteen of twenty
PATH entries user-writable), no `env=` sanitisation, no `O_NOFOLLOW`-style verification of the
executable. Exploit path (no privilege
boundary crossed, but a supply-chain one): any code already running as `vgpnk` — an `npx`/npm
postinstall, an editor plugin, a downloaded script — drops `~/.opencode/bin/sasquatch`; the next
`c1-run.sh after` executes it during extraction, exit 0, receipts green. Impact: lane evidence minted
by attacker-chosen code with the user's privileges. Smallest remediation: run the harness with a
minimal PATH (`PATH="$HOME/.local/bin:/usr/bin:/bin"` is sufficient here — `unblob` is invoked by
absolute path, `npx`/`sha256sum`/`timeout`/`jq` live in `/usr/bin`), plus the digest fail-closed check
from S1. Both are harness-local and do not touch the frozen predicate.

**S3 — sasquatch follows pre-existing symlinks out of the output tree (LOW in-pipeline / INFO).**
Evidence §5 (`openat(AT_FDCWD, "outL/target.txt", O_WRONLY|O_CREAT|O_TRUNC, 0644)`, victim clobbered;
unsquashfs 4.7.5 replaces the link instead). Impact today: none in the REA path — unblob always
extracts into a fresh `extract_root` and Landlock denies the escape (verified). Impact tomorrow: any
direct `sasquatch -d <dir>` call against a reused or caller-influenced directory (ad-hoc probes, a
scratch dir that survived a run, `-d ~/somewhere`) can overwrite arbitrary files the user can write.
Smallest remediation: keep every direct call on a fresh `mktemp -d` (the frozen harness already does
this transitively via unblob); if the lane ever adds a direct sasquatch step, `mkdir` a fresh `-d` per
invocation inside the sandboxed scratch and never reuse it.

**S4 — prebuilt C parser on untrusted input, unprivileged, FS-only confinement (INFO).**
Landlock limits where writes land, not what the process may do with memory/CPU. Mitigating facts
observed: no network syscalls, no exec, unprivileged UID, setuid bits stripped, `prlimit` wrapper from
REA. Residual: a hostile squashfs that triggers memory corruption yields code execution as `vgpnk`.
Smallest remediation (documentation-level): record in the round-36 knowledge entry that extraction is
unprivileged + Landlock-confined + `prlimit`-bounded but not syscall-filtered, so carriers must remain
digest-verified artifacts, never arbitrary "let me try this firmware" inputs.

**S5 — AppImage `--appimage-extract` executes shipped code (INFO, boundary note).** §6. Smallest
remediation: state the rule in SKILL/lesson material — *AppImage runtime flags are execution*; gate
any such run on the published digest first (as the lane did for K3/K4) and run from scratch.

**S6 — post-extraction metadata (INFO).** Ordinary mode bits survive (0700/0640 exact), which is
correct for fidelity; setuid/setgid do not survive (image `4755` → `755`), so an unprivileged
extraction cannot plant a setuid binary; `user.*` xattrs from the image are planted into the tree
(attribute-level data hiding in extracted corpora). No action needed for C1; worth one line wherever
extraction fidelity is described.

## 8. Calibration notes for R36-C1 (read-only; nothing changed)

- The receipts do record what a reviewer needs — `sasquatch`, `sasquatch_sha256`,
  `sasquatch_version`, `unblob`, `carrier_sha256` — and the recorded digest equals the audited binary.
  The gap (S1) is that the *counter* does not consume it.
- `get_dependencies()` returns **both** `sasquatch` and `sasquatch-v4be`, and the missing-dependency
  report is raised only on `FileNotFoundError`. The harness's "before" mode strips PATH entries that
  hold an executable `sasquatch`; both binaries live in the same directory, so both disappear together
  — consistent with the committed before receipts (`extraction_gaps[0].kind =
  missing-extractor-dependency`, `dependencies = ["sasquatch"]`, `handler = squashfs_v4_le`,
  `evidence_id = ev_b5bd2e7f…`, `K1`). K1 after: `gaps = []`, 3 published files; K2 after: 4 files
  with one `unpublished-entry` gap (`var/notice-link`, the symlink); K3/K4 after: 2147 files each with
  `unpublished-entry` gaps for the two AppImage symlinks (`.DirIcon`, `nvim.png`) — regular files only,
  as the oracle is regular-file-only by construction.
- Attestation limit, quoted from the receipts themselves (`limitations[4]`): *"The actual launcher
  executable is hashed. Interpreter, shared libraries and installed Python package dependencies are
  not independently attested"* — the same holds for the **extractor**: sasquatch's `libstdc++`/
  `libzstd`/`liblzma` come from `/usr/lib` and are unattested, and `unblob` itself is a `uv`-tool
  symlink (`~/.local/bin/unblob` → `~/.local/share/uv/tools/unblob/bin/unblob`, recorded in
  `raw_result.version_execution.command`) that is user-writable and unpinned by digest.
  [INFERENCE] A `libzstd`/`liblzma` downgrade on this host could change extraction behaviour without
  any receipt changing — a reason the round-36 knowledge entry should carry the interpreter/library
  caveat rather than claiming "official sasquatch ⇒ identical outputs".

## 9. Commands run (verbatim, with exit status)

```
sha256sum/stat/file/readelf -d|-h|-lW|-SW/-p .comment/getcap/getfattr/getfacl/lsattr/ldd   both binaries   exit 0
python3 (SHT accounting: shoff+shnum*shentsize vs st_size)                                  exit 0
strings -a | grep -E 'https?://|curl|wget|/bin/sh|system\(|execv|popen|LD_PRELOAD|dlopen'   exit 0 (2 doc URLs only)
curl -fsSL .../sasquatch-v4.5.1-6/sasquatch_1.0_amd64.deb -o deb-sasquatch-v4.5.1-6.deb     exit 0  187244 B
sha256sum deb-sasquatch-v4.5.1-6.deb   -> efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95  exit 0
ar t / ar x / tar -xf data.tar.xz ; tar -xOf control.tar.xz ./control ./md5sums              exit 0
cmp -s data/usr/bin/{sasquatch,sasquatch-v4be} ~/.local/bin/{sasquatch,sasquatch-v4be}      exit 0  (identical)
md5sum data/usr/bin/* ~/.local/bin/*                                                        exit 0  (44be48a2…, 33445a06…)
get https://github.com/onekey-sec/sasquatch/releases/expanded_assets/sasquatch-v4.5.1-6      exit 0  (digest row for the .deb)
get https://github.com/neovim/neovim/releases/expanded_assets/v0.12.6                       exit 0  (b644d034…, 8efcec73…)
curl -fsSL .../neovim/releases/download/v0.12.6/nvim-linux-{x86_64,arm64}.appimage           exit 0  11454968 / 11356680 B
sha256sum nvim-linux-*.appimage   -> b644d034…c35f29fb (K3), 8efcec73…5ac9efe1c2 (K4)        exit 0
python3 (read 64 B header + section table; 'hsqs' at ELF end; never chmod, never executed)   exit 0
strace -f -qq -e trace=network,execve,execveat sasquatch -le -no-exit-code -f -d outS i2.sqsh exit 0
   -> 1 execve (self), 0 network syscalls
strace -f -qq -e trace=openat,open sasquatch -le -no-exit-code [-f] -d out{L,N} i2.sqsh      exit 0
   -> openat(AT_FDCWD,"outL/target.txt",O_WRONLY|O_CREAT|O_TRUNC,0644); symlink followed
mksquashfs/unsquashfs (crafted probes: '..' name, truncation, 4755, user.k xattr)           exit 0
sasquatch on '..'-name image -> rc=1 'invalid characters in name', 0 files                 exit 1
sasquatch on truncated image -> rc=1 'File system corruption detected', 0 files            exit 1
unblob python: restrict_access(*rules) + 3 write attempts                                  exit 0
   -> inside allowed; outside PermissionError; symlink-to-outside FileNotFoundError
grep -n on c1-counter.py / squashfs.py / command.py / sandbox.py / FirmwareProvider.js      exit 0
```

Tools installed/upgraded: **none**. `pacman` transactions: **none**.

## 10. Limits

- I did **not** execute either AppImage (deliberate: executing the artifact is what §6 warns about, and
  a peer already ran it under `strace`). My AppImage evidence is byte/ELF/string inspection plus the
  peer's execution report, cited.
- I did **not** fuzz sasquatch for memory corruption; "no exploitable parser defect found" is not
  claimed — only the four specific extraction behaviours in §5.
- `sasquatch-v4be` was audited statically and by `-version`; no big-endian carrier exists in the frozen
  set, so its extraction path was not exercised.
- Landlock containment was proven by driving unblob's `restrict_access` binding directly and by reading
  unblob's sandbox/command code — I did not run a full `unblob` extraction of a malicious image to
  observe the block end-to-end (that would be a new extraction run, outside this seat).
- **[INFERENCE]** markers are confined to two statements: no signature verification on the extract
  path (§6.2) and the shared-library-attestation consequence (§8).

## 11. Hygiene

Scratch removed: `rm -rf /fast/scratch/hyaku/kaidoku-r36/R36SentinelInstall` (deb, extracted payload,
both AppImages, crafted images, traces, string dumps). Only this report was written; no lane file, no
sibling lane, no `/home/vgpnk/Projects/shokuknow`, no VCS operation.
