# AppImageLibraries — sigrok-cli 0.7.2 AppImage: payload metadata and GLib-family resolution

Seat `KaidokuR23.AppImageLibraries` (leaf, read-only except this report and its sandbox). Round 23 w1, 2026-10-21.
Target: `/home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage`, sha256 `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614`, 49,558,848 bytes.
Lane bounds kept: the AppImage was **not launched**; no process attach, no device, no REA/MCP call, no network, no repo or production-lane writes. All extraction went to a private `git clone --shared` sandbox at the frozen rev `a3c92eb6bc70984e90ae5b895412de978840b2c5`.

## Findings

### 1. Container metadata (observation)

| Fact | Value | How observed |
|---|---|---|
| AppImage type | type 2 (`41 49 02` = `AI\x02` at offset 8) | `xxd -l 16 -s 0` exit 0 |
| ELF | ELF64 EXEC, x86-64, stripped, entry `0x405320`, BuildID sha1 `4730933ed8316e83a6e80d2845100297c337d6dd` | `file`, `readelf -h` exit 0 |
| ELF trailer | `e_shoff` = 191,680; 34 × 64-byte section headers end at **193,856** = `0x2F540` | `readelf -h`, `readelf -S` exit 0 |
| SquashFS start | 193,856; `hsqs` magic confirmed at that offset | `xxd -l 96 -s 193856` exit 0 |
| False-positive `hsqs` | offset 33,613 is unrelated runtime bytes; the real payload is at 193,856, exactly ELF end | `grep -abo hsqs` exit 0 |
| Payload | 49,364,992 bytes, sha256 `6c29b7c37e785303d3fdeb029d69c6c7964825953d256717514431a93da8885b` | `tail -c +193857` + `sha256sum` exit 0 |
| SquashFS | type SquashFS, v4.0, gzip (superblock compression id 1), block size 131,072, 1,973 inodes, headers 44,295 B | superblock bytes at 0x2F540; `7z l -tSquashFS` exit 0 |
| Members | **1,750 files + 222 folders** (1,972 entries), 112 decoder directories, 21 firmware files | `7z l -tSquashFS -slt` exit 0 |
| Update info | `.upd_info` 1,024 B **all zero** — no update information | `dd`/`xxd` of `e_shoff`-relative sections exit 0 |
| Signature | `.sha256_sig` 1,024 B and `.sig_key` 8,192 B **all zero** — unsigned | `tr -d '\0' | wc -c` = 0 exit 0 |
| Embedded MD5 | `.digest_md5` = `b9932fd4faeba95020571ade0b957b37`; **matches none** of whole file (`d4c2ce5e…`), 0–193,856 runtime prefix (`28f998d1…`), payload (`aec11f7f…`), or payload `bytes_used` prefix (`890ce1e8…`) | `md5sum` on four regions exit 0 |
| Runtime | AppImageKit-style: strings `APPIMAGE_EXTRACT_AND_RUN`, `TARGET_APPIMAGE`, `APPDIR`, `squashfs-root/`; `.comment` = `GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.11) … AppImage by Simon Peter` | `strings`, `dd` of `.comment` exit 0 |
| Trailing bytes | superblock `bytes_used` = 49,363,717 → 1,275-byte zero pad inside the 49,364,992-byte payload; last non-zero byte at 49,557,568 → 1,279 trailing zero bytes in the file | struct decode of superblock at 0x2F540; byte scan exit 0 |

The runtime ELF itself does **not** set `LD_LIBRARY_PATH`; the only setter is `AppRun`.

### 2. AppRun: host-fallback mechanism (observation)

`AppRun` is an ELF (14,672 B, sha256 `95cb9bd37ed0165a7ce6511f4875ba23c22d0a6397a3008bc66123537b239b56`), the classic `execvp` launcher. Its environment format strings:

- offset 6,984 `PATH=%s/usr/bin/:…`
- offset 7,048 `LD_LIBRARY_PATH=%s/usr/lib/:…/usr/lib/x86_64-linux-gnu/:…/lib64/`
- offset 7,240 `PYTHONPATH=%s`

Every directory in `LD_LIBRARY_PATH` is prefixed with the AppDir (`%s`), so the AppDir is searched **first**, then the loader's default host paths. `AppRun` imports `putenv`, `getenv`, `execvp`, `scandir64` but no `unsetenv`; it neither clears nor filters the path.

### 3. Bundled GLib family (observation)

The only GLib-family object in the whole 1,750-file payload is:

- `usr/lib/libgmodule-2.0.so.0`, 14,656 B, sha256 `e12eac03845b378fb93f371be9519efc9b7a69edab33fd8b7976dd42821a61b5`, SONAME `libgmodule-2.0.so.0`, NEEDED `libdl.so.2`, `libglib-2.0.so.0`, `libc.so.6`; exports `g_module_open`, `g_module_close`, `g_module_error`, `g_module_supported`, `g_module_symbol`, `g_module_name`, `g_module_build_path`, `g_module_make_resident`.

**Absent from the payload:** `libglib-2.0.so.0`, `libgobject-2.0.so.0`, `libgio-2.0.so.0`, `libgthread-2.0.so.0` (`find -name 'libg*'` returns only the gmodule file). So the AppImage structurally requires host GLib for the core library, GObject and GIO.

Consumers inside the payload:

- `usr/bin/sigrok-cli` (77,728 B, sha256 `10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd`): NEEDED `libsigrok.so.4`, `libsigrokdecode.so.4`, `libglib-2.0.so.0`, `libpthread`, `libc`; **no RPATH/RUNPATH**.
- `usr/lib/libsigrok.so.4` (1,232,912 B, sha256 `0861b03cb9755fb5b94f6fb44e7334f7acb775bd03579397dbbaf5183b05df3f`): NEEDED `libgio-2.0.so.0`, `libgobject-2.0.so.0`, `libglib-2.0.so.0`, `libusb-1.0.so.0`, plus bundled `libieee1284/libserialport/libftdi1/libhidapi-hidraw/libbluetooth/libzip`; **RPATH `/tmp/s/sr_tarball_64bit/lib`** — a build-host staging path that cannot exist here, and no `$ORIGIN`.
- `usr/lib/libsigrokdecode.so.4` (69,184 B, sha256 `4bfe11a3b76fee2c6847a9638fff82f1b8078ed56d8a9b182f78cba0f28b80b3`): NEEDED `libglib-2.0.so.0`, bundled `libpython3.5m.so.1.0`, `libpthread`, `libc`.

Host-resolved non-system NEEDED (needed by bundled objects, not bundled): `libglib-2.0.so.0`, `libgio-2.0.so.0`, `libgobject-2.0.so.0`, `libusb-1.0.so.0`, `libexpat.so.1`; system libs `libc/libdl/libm/libpthread/librt/libutil/libz/ld-linux` also come from the host.

Orphan bundled copies (present but not NEEDED by any bundled object): `libffi.so.6`, `libselinux.so.1`, duplicate soname copies (`libpython3.5m.so`, `.so.1`, `.a`; `libserialport.so`, `.so.0.1.0`; `libsigrok.so`, `.so.4.1.1`; `libsigrokdecode.so`, `.so.4.2.1`), and `libgmodule-2.0.so.0` within the AppDir itself. `libpcre.so.3` is NEEDED only by the orphaned bundled `libselinux.so.1`, so the entire PCRE1 chain is vestigial: nothing loads it unless host `libselinux` were absent **and** something asked for that soname.

### 4. Decisive check: the bundled gmodule collides with host libgio (observation → inference)

Host: glib2 **2.90.1-1**, libffi 3.8.0-1, pcre2 10.49-1, libusb 1.0.30-1, util-linux 2.42.4-1 (`pacman -Q`, read-only, exit 0).

- Host `/usr/lib/libgio-2.0.so.0` declares `NEEDED libgmodule-2.0.so.0`, and imports **five** `g_module_*` symbols: `g_module_close`, `g_module_error`, `g_module_open_full`, `g_module_supported`, `g_module_symbol` (`readelf --dyn-syms`, exit 0). It has **no** RPATH/RUNPATH, so its `libgmodule` lookup obeys `LD_LIBRARY_PATH` — i.e. the AppDir's 2018 copy wins over `/usr/lib`.
- The bundled copy exports only four of those five; **`g_module_open_full` is missing** (it is `GMODULE_AVAILABLE_IN_2_70`, `/usr/include/glib-2.0/gmodule.h:103-106`; a scan of all 63 bundled ELF objects found 0 providers).
- Host libgio is linked `BIND_NOW` / `FLAGS_1: NOW NODELETE` (`readelf -d`, exit 0), so the unresolved symbol is not deferrable.

`[INFERENCE]` Consequence on this host: loading `libsigrok.so.4` pulls host `libgio-2.0.so.0`, whose `NEEDED libgmodule-2.0.so.0` resolves to the older bundled AppDir copy; `BIND_NOW` forces resolution and fails with `undefined symbol: g_module_open_full`. The AppImage's binaries therefore cannot start on glib ≥ 2.70 with this AppDir layout. Not executed here — the lane forbids launching — so this is a static link-graph prediction, not an observed error string.

Counter-check: the fallback is otherwise symbol-clean. All **273** distinct `g_*` symbols imported by `sigrok-cli`, `libsigrok.so.4` and `libsigrokdecode.so.4` are exported by the host GLib family (`libglib` 1,885 / `libgobject` 480 / `libgio` 2,155 exports; `comm -23`, `LC_ALL=C`, exit 0 → empty). So the failure is **version interposition of the one bundled GLib-family object**, not a missing host GLib.

Conditions under which the fallback would work: a host whose GIO predates GLib 2.70 (no `g_module_open_full` import), or a loader order that puts the host `libgmodule` ahead of `AppDir/usr/lib`, or removal/renaming of the bundled `libgmodule`. None is exercised here.

### 5. Prior extraction tree is not pristine (observation)

`.ufo/waves/round-23/sigrok-extraction.json` records another actor's `argv ["/home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage","--appimage-extract"]`, cwd `round-23/runtime`, exit 0. I did not run it. Comparing that tree to the raw payload:

- Payload contains 680 `.pyc`; the extraction tree contains **923** — **243 `.pyc` files exist only in the extraction**, with same-day mtimes (11:36–11:38). Python 3.5 clearly ran against that tree after extraction, so it must not be treated as a pristine payload dump.
- Independent verification still holds for the objects that matter: `AppRun`, `usr/bin/sigrok-cli`, `libgmodule-2.0.so.0`, `libsigrok.so.4`, `libsigrokdecode.so.4` extracted with `7z x -tSquashFS` from my own payload slice are byte-identical (sha256 above) to the files in the prior tree.
- Payload also contains an absolute symlink `usr/share/pyshared/sitecustomize.py -> /etc/python3.5/sitecustomize.py`; extraction-following tools may resolve outside the AppDir.

### 6. Selected probes (argv, exit, observation)

All commands read-only; `LC_ALL=C` set only for sort/`comm` steps; no env overrides otherwise; no REA invocation (none was needed and none is claimed as evidence).

| argv (cwd) | exit | observation |
|---|---|---|
| `sha256sum /home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage` | 0 | `49d2f597…9f50b614`; `stat` 49,558,848 B |
| `file …AppImage`; `readelf -h …AppImage` | 0 | ELF64 EXEC stripped; `e_shoff` 191,680; 34 shdrs ×64 = end at 193,856 |
| `xxd -l 16 -s 0 …AppImage` | 0 | `7f45 4c46 0201 0100 4149 0200` → AppImage type 2 |
| `grep -abo hsqs …AppImage` | 0 | 33,613 (runtime false positive) and 193,856 (payload) |
| `tail -c +193857 …AppImage > sigrok-cli.payload.squashfs`; `sha256sum`; `stat` | 0 | 49,364,992 B; `6c29b7c3…a8885b` |
| `7z l -tSquashFS -slt sigrok-cli.payload.squashfs` | 0 | SquashFS 4.0 gzip; 1,750 files, 222 folders, headers 44,295 |
| `readelf -d` on `AppRun`, `usr/bin/sigrok-cli`, `usr/lib/*.so*` | 0 | NEEDED/RPATH sets in §3; `libsigrok.so.4` RPATH `/tmp/s/sr_tarball_64bit/lib` |
| `readelf --dyn-syms --wide` bundled binaries; `comm -23` vs host exports | 0 | 273 imported `g_*`; zero missing (§4) |
| `readelf -d usr/lib/libgmodule-2.0.so.0`; `readelf --dyn-syms` exports | 0 | SONAME `libgmodule-2.0.so.0`; no `g_module_open_full` |
| `readelf --dyn-syms /usr/lib/libgio-2.0.so.0` + `readelf -d … | grep FLAGS` | 0 | imports `g_module_open_full`; `BIND_NOW`, `NOW NODELETE` |
| `grep -n -A2 GMODULE_AVAILABLE_IN_2_70 /usr/include/glib-2.0/gmodule.h` | 0 | declaration at lines 103-106; enum docs "Since: 2.70" |
| `pacman -Q glib2 libffi pcre2 libusb util-linux` | 0 | 2.90.1-1, 3.8.0-1, 10.49-1, 1.0.30-1, 2.42.4-1 |
| `md5sum` over whole/runtime/payload/bytes_used regions | 0 | none equals embedded `b9932fd4…` |
| `7z x -tSquashFS` of 5 key members + `sha256sum` vs prior tree | 0 | byte-identical for all five |
| `python3` set comparison of 7z paths vs extraction tree | 0 | 680 vs 923 `.pyc`; 243 extra in extraction |

### 7. Interpretation

- **Observation:** the bundle ships **one** GLib-family library (`gmodule`), and it is a 2018-era build; `glib`, `gobject`, `gio` are deliberately or accidentally left to the host, with AppRun putting the AppDir first anyway.
- **Inference:** on this host the fallback is fatal by interposition, not by absence: host `libgio` requires the post-2.70 `g_module_open_full` from the `libgmodule` soname that the AppDir older copy occupies.
- **Unknown:** whether a dynamic run produces exactly `undefined symbol: g_module_open_full` (not executed); why `.digest_md5` matches no reconstructible region; the AppImageKit runtime version; whether any behavior mismatch beyond symbol resolution would appear if the gmodule collision were worked around.
- **Claim hygiene:** this is archive metadata and link-graph analysis only. It produced no bound REA record, exercises none of the six T1 verbs, and must not be counted toward R23-C1 or any cumulative k/6.

## Produced files

Absolute paths (all inside the frozen sandbox unless noted):

| Path | sha256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/sigrok-cli.payload.squashfs` | `6c29b7c37e785303d3fdeb029d69c6c7964825953d256717514431a93da8885b` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/appimage-metadata.json` | `249611bd12b4434641068946e191f91b59b7f61c0f123aec3c8094bd8069ddd6` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/gio-gmodule-symbol-check.txt` | `b860438ff77317919b2d14097da2940428f4ccfeaf78c1369a26f596d1abfdc0` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/indep/AppRun` | `95cb9bd37ed0165a7ce6511f4875ba23c22d0a6397a3008bc66123537b239b56` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/indep/usr/bin/sigrok-cli` | `10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/indep/usr/lib/libgmodule-2.0.so.0` | `e12eac03845b378fb93f371be9519efc9b7a69edab33fd8b7976dd42821a61b5` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/indep/usr/lib/libsigrok.so.4` | `0861b03cb9755fb5b94f6fb44e7334f7acb775bd03579397dbbaf5183b05df3f` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/indep/usr/lib/libsigrokdecode.so.4` | `4bfe11a3b76fee2c6847a9638fff82f1b8078ed56d8a9b182f78cba0f28b80b3` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/list-7z.txt` | `bf62d936d8501f120c7b2efd5d0f4d568a84657e1a6675948b673493f622f8eb` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/output/list-extract.txt` | `64369fbda6fb506911f25aa18c45e6ef7b616bdbc04a7a51cdb5916c695061d2` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/AppImageLibraries.md` | this report |

Sandbox HEAD verified `a3c92eb6bc70984e90ae5b895412de978840b2c5`; no production file was edited.

## Installs

None. No pacman/uv/npx/cargo/npm transaction; all tools used were already on the host (`7z` 26.04, `readelf`/`objdump` binutils, `python3`, `bsdtar`). Host pacman transactions remain paused per directive.

## Open risks

- The `g_module_open_full` failure is a **static prediction**; a dynamic lane (outside this wave) must confirm the exact loader diagnostic before it is called observed.
- The AppImage is **unsigned** (zeroed `.sha256_sig`/`.sig_key`) and its embedded MD5 matches no reconstructed region, so provenance rests solely on the recorded sha256; do not treat `.digest_md5` as an integrity check.
- The shared extraction tree `round-23/runtime/squashfs-root` has 243 generated `.pyc` files beyond the payload and an absolute `sitecustomize.py` symlink; other seats must not treat it as a pristine dump.
- A loader-order workaround (expose AppDir libs but exclude the bundled `libgmodule`) is untested; the bundled `libsigrok`/`libsigrokdecode` also rely on the AppDir path via a dead RPATH, so any such workaround needs its own verification.
- Host glib2 is nine minor generations ahead of the 2018 bundle; future host changes can remove further old symbols, and the AppDir's stale `libffi.so.6`/`libselinux.so.1`/`libpcre.so.3` remain available for accidental interposition by soname.
