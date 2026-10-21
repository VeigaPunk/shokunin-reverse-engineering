# RuntimeIdentity: R23 W2 source review of launcher, AppImage and dependency pins

Seat: `KaidokuR23.RuntimeIdentity`. Leaf source review. Author-side candidate findings, not independent admission; L1 owns integration.
Candidate: `2838351450ff1ee4baa620c962a1153450d53311`. Base: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Method: candidate bytes read with `git show` and `git grep` at the candidate commit. Host and runtime state read-only (`sha256sum`, `readelf`, `ls`, `find -newermt`, `date`), observed 2026-10-21 about 15:18Z.
Not run: sigrok-cli, the wrapper, REA, the AppImage, `count-c1.py`, `verify.py`, selftests. No clone, no writes outside this file.

Tags: **O** observed (file:line, hash, or command and exit). **I** inferred from observed facts. **U** unknown or unverified.

## Answers to the four scoped questions

1. **Wrapper SHA is not the inner ELF or the installation: confirmed.** Every c1 envelope binds only the 698-byte wrapper `50fe4359…`. The executed ELF `10fed05a…`, two libraries and one decoder are identified only by `tool-runtime-pins.json`, captured 4.0 to 4.9 minutes after the five runs (F3, F9). The payload holds 1,972 entries; 8 are pinned (F4).
2. **Old gmodule / new gio workaround: works for wrapper runs; W1's "cannot start" prediction is superseded for that path.** Mechanism and evidence are in F1. Two side effects are not recorded anywhere: the preload is a hard-coded host path (F1), and the process-wide `LD_LIBRARY_PATH` binds the bundled `libudev.so.1` into host `libusb-1.0.so.0` (F2).
3. **Python 3.5 signature failure: observed and bounded.** One of 111 decoder modules (`signature`) is absent from the catalog. The envelope still reports `ok:true`. Cause: digit-group underscore literal at `pd.py:138`, which Python 3.5 rejects (F5). Not repaired, and the candidate does not claim repair.
4. **One-instant custody: documentary, not enforced (F3).** The pins postdate the runs. There is no committed producer or verifier. The wrapper hashes nothing before `exec`. The runtime tree is gitignored and gains bytecode during runs. A current re-hash shows no drift since the pin instant.

## Findings

### F1. gmodule preload: functional for wrapper runs, fragile by construction (Medium; O+I)

- O: `tools/sigrok-cli.sh:11` `export LD_LIBRARY_PATH="$runtime/usr/lib"`; `:12` `export LD_PRELOAD=/usr/lib/libgmodule-2.0.so.0`; `:15` `exec "$runtime/usr/bin/sigrok-cli" "$@"`.
- O: host `/usr/lib/libgio-2.0.so.0` (`readelf -d`, exit 0) has NEEDED `libgmodule-2.0.so.0`, `FLAGS BIND_NOW`, `FLAGS_1 NOW NODELETE`. An unresolved `g_module_open_full` is therefore fatal at load (I).
- O: runtime banners in `evidence/c1/inventory.envelope.json`, `uart-help.envelope.json`, `decode-uart-hi.envelope.json` report `glib 2.48.2 (rt: 2.90.1/9001:1)` with libsigrok loaded. That requires host libgio to have resolved at load. This is the evidence that the wrapper path starts.
- O: `sigrok-version-attempt1.json` runs the inner ELF with the identical environment, exit 0. Its record has no timestamp, cwd or hash.
- I: an already-loaded object with the same SONAME satisfies a later NEEDED entry, so the bundled 2018 `libgmodule` (`e12eac03…`) is never mapped when the preload succeeds.
- Gaps:
  - The preload path is an absolute host path with no existence or identity check. If it is absent, ld.so (ld.so(8)) prints a "cannot be preloaded … ignored" diagnostic and resolves the bundled copy, which reproduces W1's predicted `undefined symbol: g_module_open_full`. Not run (U for exact text).
  - The identity of the preloaded object at run time appears in no envelope. Its only record is the pin at 14:42:59Z (F3).
  - `export` at line 12 propagates `LD_PRELOAD` to every descendant process.
- Direction (not applied): verify the preload path and its digest before `exec`, and record them in the envelope.

### F2. Process-wide `LD_LIBRARY_PATH` binds host libusb to bundled libudev (Low to Medium, latent; O+I)

- O: `readelf -d /usr/lib/libusb-1.0.so.0` (exit 0): NEEDED `libudev.so.1`; no RPATH or RUNPATH; `FLAGS BIND_NOW`. `readelf -V`: its `libudev.so.1` version need is `LIBUDEV_183` only.
- O: bundled `usr/lib/libudev.so.1` (`46954eb7570ac12926716ca23d4f53d1d8aea7310f96e9c55e0e4413e4da22f9`) defines `LIBUDEV_183` through `LIBUDEV_215` (`readelf -V`).
- O: host `/usr/lib/libudev.so.1` (symlink to `libudev.so.1.7.15`) defines up to `LIBUDEV_247` (`readelf -V`).
- O: bundled `libhidapi-hidraw.so.0` also NEEDs `libudev.so.1` (`readelf -d`), so the bundled copy is loaded for bundled consumers regardless.
- I: `LD_LIBRARY_PATH` precedes default directories for objects without RUNPATH (ld.so(8)). Host libusb is therefore satisfied by the bundled libudev, and host `libudev.so.1.7.15` is not mapped in the process. The version need is met, which fits the observed banner `libusb-1.0 1.0.30.12037`.
- Not in any pin, not in candidate knowledge, and not in W1 `AppImageLibraries.md` §3 (its orphan list omits libudev).
- O: decode runs carry `--dont-scan` in `decode-uart-hi.envelope.json` `tool.arguments`. Inventory arguments were not checked.
- U: behaviour difference from the host libudev is unexercised.
- Direction (not applied): pin and compare the bundled libudev, or remove its soname from the search path (untested).

### F3. One-instant custody is documentary, not enforced (Medium; O)

Timeline (UTC):

| Time | Event | Source |
|---|---|---|
| about 14:36 | extraction tree written (symlink mtime 11:36 local, -0300) | `ls -la` on `usr/share/pyshared/sitecustomize.py`; `sigrok-extraction.json` (no timestamp) |
| 14:30:00 to 14:42:59 | all 923 `.pyc` under the runtime tree written (none before 14:30, none after 14:42:59) | `find -newermt`, exit 0 |
| 14:38:06.805 | inventory run | `inventory.run.json` `captured_at` |
| 14:38:07.478 | uart-help run | `uart-help.run.json` `captured_at` |
| 14:38:40.850 | decode-uart-hi run | `decode-uart-hi.run.json` `captured_at` |
| 14:38:58.876 | decode-official-uart run | `decode-official-uart.run.json` `captured_at` |
| 14:38:59.565 | decode-invalid-decoder run | `decode-invalid-decoder.run.json` `captured_at` |
| 14:42:59.167 | `tool-runtime-pins.json` captured | `captured_at` |
| about 15:18 | this review: all 8 pinned files still match | Identity inventory below |

- O: `.ufo/waves/round-23/.gitignore` contains `/runtime/` and `/worktrees/`. The executed bytes are not in the commit; only pins and hashes bridge them.
- O: `tool-runtime-pins.json` has no committed producer. Its `producer` field reads "Python pathlib.read_bytes/hashlib.sha256 on listed paths". `git grep -c tool-runtime-pins <cand> -- .ufo/waves/round-23/tools .ufo/waves/round-23/verify.py .ufo/waves/round-23/verify` returns no matches (exit 1).
- O: no verifier consumes the pins. `tools/describe-signals.py:42,60,61` hashes envelope and carrier bytes only.
- O: the wrapper verifies nothing before `exec`. Lines 5 to 8 check only `-x`; line 15 execs.
- O: runs mutate the runtime tree. The candidate contains no `PYTHONDONTWRITEBYTECODE` and no `-B` (`git grep`, exit 1). The runtime holds 923 `.pyc` in 155 directories. The pins exclude `__pycache__`.
- O: `run.json` `env_overrides` contains only `REA_SIGROK_COMMAND`. The ambient environment is not recorded, and the wrapper does not clear `PYTHONHOME` or other interpreter variables.
- O (positive): at about 15:18Z the pinned set still matches on disk. Wrapper `50fe4359…`, ELF `10fed05a…`, libsigrok `0861b03c…`, libsigrokdecode `4bfe11a3…`, uart `51a29d0e…`, host libgmodule `b259a089…`, libglib `1e8739af…`, libgio `b38001cc…`. No drift after 14:42:59Z. Nothing covers 14:30 to 14:42:59Z.
- O: the candidate prose is accurate about its limits (`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:102-106`). The gap is enforcement and coverage, not wording.
- Direction (not applied): digest check of the ELF and selected libraries inside the wrapper before `exec`; `PYTHONDONTWRITEBYTECODE=1`; hashes recorded at run time in each envelope; a committed producer and verifier for the pin file.

### F4. Pins cover 8 files; the executed set is far larger (Medium to Low; O)

- O, pinned (8): wrapper, inner ELF, `libsigrok.so.4`, `libsigrokdecode.so.4`, `uart/pd.py`, host libgmodule, host libglib, host libgio.
- O, executed but unpinned:
  - `usr/lib/libpython3.5m.so.1.0`, the bundled interpreter that libsigrokdecode loads (W1 `AppImageLibraries.md` §3). Not measured here (U).
  - 111 decoder packages. Only `uart` is pinned. `signature/pd.py` is `984f1d8c…` and absent from the pins.
  - Bundled `libudev.so.1` (`46954eb7…`, F2).
  - Host libs reached transitively: `libusb-1.0.so.0`, `libz.so.1`, `libmount.so.1`, `libblkid.so.1`, `libsystemd.so.0`, `libpcre2-8.so.0`, `libffi.so.8`. Not measured (U).
  - Bundled libsigrok dependencies: libserialport, libzip, libftdi1, libhidapi-hidraw, libbluetooth, libieee1284. Not measured (U). Only libsigrok's own NEEDED list was read.
  - `prlimit` `092bb6db…`: in envelope `resource_limiter` only. Matches now (O).
  - The stdlib `usr/share/pyshared/*` (for example `os.py`). Not pinned; load-bearing (F5).

### F5. Python 3.5 `signature` decoder: bounded, observed, not repaired (Low for uart claims; Medium for catalog completeness; O)

- O, source: `w1/_uart/libsigrokdecode-0.5.3/decoders/signature/pd.py:138`: `incoming = (bin(shiftreg & 0b0000_0010_1001_0001).count('1') + data) & 1`. Candidate blob `984f1d8c2ccd0cdbc535244dfa2e7b4ea88296887b8c2e48280d7d2909555277`. The runtime copy has the identical hash.
- O, diagnostic in `evidence/c1/inventory.envelope.json` `normalized_result.diagnostics`: `srd: SyntaxError: Failed to load decoder signature … (pd.py, line 138)`, with a traceback.
- O, reconciliation (python over the runtime decoder directories and the envelope `decoders` list, exit 0): 112 installed directories including `common`; 110 returned. Installed minus returned is `{common, signature}`; returned minus installed is empty. `signature` is the only missing decoder module. `common` is a helper package.
- O: envelope `ok:true`; `output_window {examined 110, matching 110, returned 110, has_more false}`. The failure is visible only in diagnostics.
- Language fact: digit-group underscores in numeric literals are Python 3.6+ syntax (PEP 515). The banner reports `Python 3.5.2 / 0x30502f0` (O).
- O: all five c1 envelopes contain "Could not find platform independent libraries <prefix>". `find … -maxdepth 4 -name os.py` finds no `usr/lib/python3.5/os.py`; the only `os.py` is `usr/share/pyshared/os.py`. The stdlib is therefore reached through `PYTHONPATH` (`tools/sigrok-cli.sh:13`) (I). The candidate's wording that exit 0 "did not erase" the diagnostics is accurate.
- Direction (not applied): catalog answers must state that `signature` did not load.

### F6. Dangling host symlink on the bundled Python path (Low; O+I)

- O: `runtime/squashfs-root/usr/share/pyshared/sitecustomize.py -> /etc/python3.5/sitecustomize.py` (`ls -la`, exit 0). Symlink mtime 11:36 local, which is 14:36Z.
- O: `/etc/python3.5` is absent (`ls` exit 2).
- I: `pyshared` is on `PYTHONPATH` (`sigrok-cli.sh:13`) and holds the stdlib (F5), so `site` will attempt to import `sitecustomize` at interpreter start. Today the dangling link yields no import. If a host file ever appears at that path, host code runs inside every bundled-interpreter launch.

### F7. DT_RPATH to `/tmp/s/sr_tarball_64bit/lib` on bundled libsigrok (Low on single-user hosts; O+I)

- O: `usr/lib/libsigrok.so.4` (`0861b03c…`) has `RPATH [/tmp/s/sr_tarball_64bit/lib]` and no RUNPATH (`readelf -d`). Its NEEDED entries include `libserialport.so.0`, `libusb-1.0.so.0`, `libieee1284.so.3`, `libftdi1.so.2`, `libhidapi-hidraw.so.0`, `libbluetooth.so.3`, `libzip.so.4`, plus host `libgio`, `libgobject` and `libglib`.
- O: `/tmp/s` is absent (`ls` exit 2). `/tmp` is `drwxrwxrwt root`.
- I: DT_RPATH is searched before LD_LIBRARY_PATH for objects without RUNPATH (ld.so(8)). Any local account could create `/tmp/s/sr_tarball_64bit/lib/<soname>`, and the next wrapper run would load it ahead of the pinned bundle. Untested. Not in the pins or the knowledge file.
- I: the AppDir copy `tmp/s/sr_tarball_64bit/lib/libserialport.so.0` is not on that search path.
- Direction (not applied): remove the RPATH from the bundled library (untested).

### F8. `setup-sigrok.py`: digest check, then exec by path (Low; O)

- O: `tools/setup-sigrok.py:21` `digest = hashlib.sha256(source.read_bytes()).hexdigest()`; `:22` compares against `EXPECTED` (`:14`); `:30` `argv = [str(source), '--appimage-extract']` executes the path. The bytes hashed and the file executed are not one read (time-of-check/time-of-use).
- O: the wrapper has no equivalent gate (F3).
- O: the origin AppImage matches `49d2f597…` now. W1's observations (zeroed `.sha256_sig`, mismatched `.digest_md5`) were not re-verified here.

### F9. Envelopes bind the wrapper only (confirmed and accurately documented; Info; O)

- O: `tool.sha256` and `subject.digest.sha256` are `50fe4359…` in each envelope that carries a `tool` block (inventory, uart-help, decode-uart-hi checked). The `tool` block holds `configured_path`, `version_banner`, `arguments` and `limits`. It holds no ELF or library digests.
- O (positive): runtime `uart/pd.py` (`51a29d0e…`) and `signature/pd.py` (`984f1d8c…`) are byte-identical to the committed upstream copies under `w1/_uart/libsigrokdecode-0.5.3/decoders/`. This shows consistency, not authentication.

### F10. Launcher history not retained; one W1 description contradicts the c1 bytes (Low to Medium; O)

- O: `git log aa1450b..2838351 -- .ufo/waves/round-23/tools/sigrok-cli.sh` returns one commit, `2b40aec5699607d8d6eb5ca040f64e649936451d` (2026-10-21 11:56:57 -0300). No earlier launcher bytes are committed.
- O: W1 `w1/SchemaSignalInventory.md:303-307` says "For the REA probes the second form was used", where the second form is `LD_LIBRARY_PATH=/usr/lib:<extract>/usr/lib` (line 304). The c1 envelopes carry `50fe4359…`, the LD_PRELOAD form (`sigrok-cli.sh:11-12`).
- I: the W1 sentence is stale for the c1 evidence. It may describe an earlier W1 launcher whose bytes are not retained.

## Re-evaluation of W1 launcher and AppImage findings against 2838351450ff1ee4baa620c962a1153450d53311

| W1 finding (file and location) | Status at candidate | Basis |
|---|---|---|
| `AppImageLibraries.md` §4, line 65: static prediction that the AppImage "cannot start on glib ≥ 2.70" | **Superseded for wrapper runs.** Still a static prediction for an un-preloaded launch (AppRun or direct ELF). Untested at candidate. | F1: `sigrok-cli.sh:12`; banners; attempt1 exit 0 |
| `SchemaSignalInventory.md:294`: "running the AppImage directly, or its AppRun, fails … exit 127" | **Unretained observation.** The string appears only at that location (`git grep`). No argv, env or exit record exists in the candidate. Narrative only. | `git grep -n 'undefined symbol'` |
| `SchemaSignalInventory.md:303-307`: REA probes used `LD_LIBRARY_PATH=/usr/lib:<extract>/usr/lib` | **Contradicted for c1.** Envelope sha `50fe…` is the LD_PRELOAD form. | F10 |
| `AppImageLibraries.md` §5: extraction tree is not pristine (243 extra `.pyc`) | **Confirmed in form.** 923 `.pyc` now. The payload's 680 is W1's count, not re-measured. The candidate still writes bytecode (no `-B`). | F3 |
| `AppImageLibraries.md` §3: AppRun host-fallback mechanism | **Not on the candidate execution path.** The wrapper bypasses AppRun (`sigrok-cli.sh:11-15`). | wrapper text |
| `AppImageLibraries.md` §3: libselinux and libpcre chain is vestigial | **Confirmed for the host NEEDED graph read here.** Host libgio reaches libmount, which reaches libblkid and libsystemd. None NEEDs `libselinux.so.1`. Bundled objects' NEEDED lists were not fully re-derived. | `readelf -d` |
| `AppImageLibraries.md` §3 orphan list (no libudev) | **Incomplete.** Bundled libudev is consumed by host libusb. | F2 |
| `ConnectSourceChain.md:195`: "pins are a single instant" | **Confirmed.** | F3 |
| `SigrokInventoryFields.md:16,153`: identity gap | **Confirmed.** | F9 |
| `CriticSource.md:86`: executed binary is not hashed | **Confirmed for the wrapper** (`sigrok-cli.sh:15`). The REA-side JavaScript claim is outside the candidate and unverified here. | F3 |
| `ReviewVersionPins.md:51`: "three independent records agree" | **Digest still matches** (`49d2f597…`). "Independent" is overstated: the spec (`gen-wave1.py:17`), `setup-sigrok.py:14` and the extraction record are all lane-produced. | identity inventory |
| `ConnectOutsideDebt.md:153-157`: LD_PRELOAD workaround | **Consistent** with F1. | F1 |

## Identity inventory (candidate vs current)

Paths are under `.ufo/waves/round-23/` unless absolute. "Pinned" means listed in `tool-runtime-pins.json` at 14:42:59Z.

| Component | Path | sha256 | Size (bytes) | Committed | Pinned | In c1 envelope | Current (about 15:18Z) |
|---|---|---|---|---|---|---|---|
| origin AppImage | `/home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage` | `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614` | 49,558,848 (W1) | no | no | no | match |
| launcher (wrapper) | `tools/sigrok-cli.sh` | `50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902` | 698 | yes (2b40aec) | yes | yes (`tool.sha256`) | match |
| inner ELF | `runtime/squashfs-root/usr/bin/sigrok-cli` | `10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd` | 77,728 | no | yes | no | match |
| libsigrok | `runtime/squashfs-root/usr/lib/libsigrok.so.4` | `0861b03cb9755fb5b94f6fb44e7334f7acb775bd03579397dbbaf5183b05df3f` | 1,232,912 | no | yes | no | match |
| libsigrokdecode | `runtime/squashfs-root/usr/lib/libsigrokdecode.so.4` | `4bfe11a3b76fee2c6847a9638fff82f1b8078ed56d8a9b182f78cba0f28b80b3` | 69,184 | no | yes | no | match |
| uart decoder | `runtime/squashfs-root/usr/share/libsigrokdecode/decoders/uart/pd.py` | `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62` | 23,007 | upstream copy | yes | no | match |
| signature decoder | `runtime/squashfs-root/usr/share/libsigrokdecode/decoders/signature/pd.py` | `984f1d8c2ccd0cdbc535244dfa2e7b4ea88296887b8c2e48280d7d2909555277` | not measured | upstream copy | no | no | match |
| bundled libgmodule | `runtime/squashfs-root/usr/lib/libgmodule-2.0.so.0` | `e12eac03845b378fb93f371be9519efc9b7a69edab33fd8b7976dd42821a61b5` | 14,656 (W1) | no | no | no | match |
| bundled libudev | `runtime/squashfs-root/usr/lib/libudev.so.1` | `46954eb7570ac12926716ca23d4f53d1d8aea7310f96e9c55e0e4413e4da22f9` | not measured | no | no | no | measured now only |
| AppRun | `runtime/squashfs-root/AppRun` | `95cb9bd37ed0165a7ce6511f4875ba23c22d0a6397a3008bc66123537b239b56` | 14,672 (W1) | no | no | no | match; unused by wrapper |
| host libgmodule | `/usr/lib/libgmodule-2.0.so.0` (to `.so.0.9000.1`) | `b259a089b405eaa747fa15b62800301dfc948523f547dec84ec5ea679cd51a4b` | 22,464 | host | yes | no | match |
| host libglib | `/usr/lib/libglib-2.0.so.0` (to `.so.0.9000.1`) | `1e8739af791b1a2f1f01fc7c6f3b9158888387d5a816195475e406438d41b688` | 1,457,576 | host | yes | no | match |
| host libgio | `/usr/lib/libgio-2.0.so.0` (to `.so.0.9000.1`) | `b38001cca69b2890a22fd3f6590bea7392bf489009de7ddfb6dbf296a133685e` | 1,969,504 | host | yes | no | match |
| prlimit | `/usr/bin/prlimit` | `092bb6db10a743ecccfc7d6e72055007064abf8910c85d736832fb53697fff96` | 27,320 | host | no | yes (`resource_limiter`) | match |
| pins file | `tool-runtime-pins.json` | `02ef8379734f3bf9d25b893b7170e36aaab32805c542c613e399307490a68f73` | n/a | yes | n/a | n/a | matches W1 citation |
| extraction record | `sigrok-extraction.json` | `2b84f466e5a81e99c447554863bc01e0108aec29b3279cbeef6476b04c39e5e2` | n/a | yes | n/a | n/a | matches W1 citation |
| setup script | `tools/setup-sigrok.py` | `a6e46c7a907682b85a423589cc19c6043ce42220f5f3c2c329fdb130f4d9bef7` | n/a | yes | n/a | n/a | n/a |

## Command log (exercised; abridged; cwd is the kaidoku root)

| Command | Exit | Result |
|---|---|---|
| `git show <cand>:.ufo/waves/round-23/tools/sigrok-cli.sh \| sha256sum`, and `\| wc -c` | 0 | `50fe4359…`; 698 bytes |
| `git show <cand>:` `tool-runtime-pins.json` and `sigrok-extraction.json`, each `\| sha256sum` | 0 | `02ef8379…`; `2b84f466…` (match W1 citations) |
| `git show <cand>:` `…/signature/pd.py` `\| sed -n 136,140p` and `\| sha256sum` | 0 | line 138 as quoted in F5; `984f1d8c…` |
| `git grep -n` for `g_module_open_full`, `undefined symbol`, `LD_PRELOAD`, `PYTHONDONTWRITEBYTECODE`, `appimage-extract`, `tool-runtime-pins` | 0 | hits in F1, F3, F10; none for `PYTHONDONTWRITEBYTECODE` in tooling |
| `git grep -c tool-runtime-pins` over `tools`, `verify.py`, `verify` | 1 | no committed consumer |
| `sha256sum` of origin AppImage; host gmodule, glib, gio; runtime pinned set; runtime signature, AppRun, libgmodule, libudev; `/usr/bin/prlimit` | 0 | matches listed in the inventory |
| `readelf -d` and `readelf -V` on host libgio, libglib, libgobject, libusb-1.0, libmount, libsystemd, libblkid, host libudev; bundled libsigrok, libselinux, libudev, libhidapi-hidraw | 0 | F1, F2, F7 |
| `ls -la /etc/python3.5 /tmp/s /tmp/s/sr_tarball_64bit/lib` | 2 | all absent |
| `ls -la /usr/lib/libselinux.so.1 /usr/lib/libpcre.so.3 /usr/lib/libffi.so.6 /usr/lib/libffi.so.8` | 2 | first three absent; `libffi.so.8` present |
| `ls -la …/usr/share/pyshared/sitecustomize.py` | 0 | dangling symlink to `/etc/python3.5/sitecustomize.py` |
| `find … -name '*.pyc' -newermt 2026-10-21T14:30:00+00:00 ! -newermt 2026-10-21T14:50:00+00:00` | 0 | 923 files. (A form with a bare `UTC` suffix failed to parse, exit 1.) |
| `find … -newermt 2026-10-21T14:42:59+00:00 \| wc -l` and the `!` form | 0 | 0 newer; 923 not newer |
| `find … -maxdepth 4 -name os.py` (under `usr`) | 0 | only `usr/share/pyshared/os.py` |
| python reconciliation of envelope decoder list against runtime decoder directories | 0 | `{common, signature}` |
| `date -u`; `date`; `ls -ld /tmp` | 0 | 15:18:09Z; -0300; `drwxrwxrwt root` |

## Open risks and unverified items

- U1. No dynamic run. Loader text for a missing preload, and for an un-preloaded launch, is unobserved. W1's `undefined symbol` text is narrative only (`SchemaSignalInventory.md:294`).
- U2. Run-time bytes for 14:30 to 14:42:59Z (ELF, libraries, host gmodule) were not captured. The pins cannot prove the runs' identities.
- U3. F2's behaviour under host libusb is unexercised. Decode runs used `--dont-scan`. Inventory arguments were not checked.
- U4. Not measured: libpython3.5m, bundled libzip, libftdi1, libhidapi-hidraw, libbluetooth, libserialport, libieee1284, and host libusb, libz, libmount, libblkid, libsystemd, libpcre2, libffi. W1's claims about bundled NEEDED sets were not re-derived.
- U5. F7 exploitability depends on host account layout. Untested.
- U6. Provenance of the committed upstream tarballs (`w1/_uart/*.tar.gz`) is not authenticated. The runtime decoders match only the extracted committed copies.
- U7. The AppImage is unsigned (W1). Its digest is the only identity.
- U8. REA-side claims (realpath handling, no hashing in `SigrokRecordingProvider.js`) lie outside the candidate and are not verified here.
- Checks not run, and therefore not passed: `count-c1.py`, `verify.py` (including selftest), sigrok-cli, REA, and any dynamic loader test.

## Produced files and hashes

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w2/RuntimeIdentity.md` (this report). Its sha256 is reported in the final message.
- No other files created. No peer report edited.

## Installs

None. No pacman, uv, npm, cargo or release-binary installs. Pacman transactions remain paused. Tools used were already present: git, sha256sum, readelf (binutils), find, ls, date, python3 (read-only evaluation).
