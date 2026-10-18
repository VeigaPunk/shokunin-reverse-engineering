# SC3 — C1 target inventory (91.6MB wall + 17.7MB rung)

**Verdict: IDENTITY-PINNED.** Both C1 targets exist, are unique by basename in the searched trees, and match the recorded digests byte-for-byte. The "91.6MB" / "17.7MB" labels are decimal-MB names for exact sizes 91,662,336 B and 17,694,720 B. `arc2-r6-pe` argv is the wall file and is already `failed` (not in-flight). The mid-rung has one extra exact-size hit: a provider import copy under E9 scratch, `cmp`-identical to the canonical file. Custody not in scope (pre-pair not re-checked). HEAD `54bc9dd90b0aea67c345c1c6aa180e160164d151`. Stamp 2026-10-18T20:46:24Z–20:49:29Z. This seat did not signal the service.

## Identities

| Role | Path | Size (B) | sha256 | PE |
|---|---|---:|---|---|
| Wall (lane label 91.6MB) | `/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe` | 91662336 | `7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292` | PE32+ ARM64 `0xAA64`, 8 sections, GUI, subsystem 2 |
| Mid-rung (lane label 17.7MB) | `/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/agent-browser/bin/agent-browser-win32-x64.exe` | 17694720 | `a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786` | PE32+ AMD64 `0x8664`, 10 sections, console, subsystem 3, characteristics `0x022E` |

Decimal vs binary: 91,662,336 B = 91.662336 MB = 87.416015625 MiB (knowledge's "87.4 MiB" is that figure rounded). 17,694,720 B = 17.69472 MB = 16.875 MiB. Do not resolve the labels by a size band: same directory holds `windows_debug_arm64.exe` at 98,958,848 B and `windows_release_x86_64.exe` at 109,268,480 B.

Recorded pins that this measurement matches: `corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:16-19` (wall sha256, `file` line, 91,662,336 B); `.ufo/waves/arc2-loop1-round3/E6.md:76-80` and `:235-236` (both paths and digests); `PROVINCE.md:139` (91.6 MB Godot ARM64 PE); `SCORECARD.md:800` and `:894` (the 91.6MB leg name). Template dir `version.txt` content is the single line `4.7.2.stable`.

## Evidence

Commands run this seat. Excerpts are observed output, not reconstructed.

```sh
stat -c 'exists size=%s inode=%i mtime=%y mode=%a nlink=%h %n' \
  /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe \
  /home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/agent-browser/bin/agent-browser-win32-x64.exe
file -b <each>
sha256sum <each>
```

```text
exists size=91662336 inode=9021743 mtime=2026-10-11 16:17:46.129033608 -0300 mode=755 nlink=1 …/windows_release_arm64.exe
PE32+ executable for MS Windows 6.00 (GUI), ARM64, 8 sections
7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292  …/windows_release_arm64.exe
exists size=17694720 inode=44452 mtime=2026-10-03 21:16:07.316555640 -0300 mode=644 nlink=1 …/agent-browser-win32-x64.exe
PE32+ executable for MS Windows 5.02 (console), x86-64 (stripped to external PDB), 10 sections
a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786  …/agent-browser-win32-x64.exe
```

PE optional header (python `struct` over the file bytes; sha256 recomputed from the same read matches the table): wall `AEP 0x1000 ImageBase 0x140000000 SizeOfImage 93822976 SizeOfCode 69538816`, sections `.text` raw 69,538,816 / `.rdata` 20,611,584 / `.data` 207,872 / `.pdata` 703,488 / `.tls` 41,472 / `pck` 512 / `.rsrc` 144,384 / `.reloc` 413,184. Rung `AEP 0x1410 SizeOfImage 17727488 SizeOfCode 12141568`, `.text` raw 12,141,568. TimeDateStamp wall `0x6a8269ad` = 2026-08-17T01:53:49Z; rung `0x6abec03d` = 2026-10-01T20:19:09Z. Section raw sizes match `corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:26-28` and `.ufo/waves/arc2-loop1-round3/E6.md:241-242`.

```sh
find /home/vgpnk /var/tmp -xdev -type f \( -size 91662336c -o -size 17694720c \) -printf '%s\t%i\t%p\n'
find /home/vgpnk/.npm /home/vgpnk/.cache /home/vgpnk/.local /var/tmp -xdev \
  \( -name 'windows_release_arm64.exe' -o -name 'agent-browser-win32-x64.exe' -o -name 'target-7a2ccd688f6c.exe' \) -printf '%s\t%p\n'
```

Exact-size hits: the two canonical paths above, plus one copy `17694720 inode=2218964 /var/tmp/arc2-l6r6-E9-mid/tmp/rea-ghidra-CCbpL5/target-a6a9a3654c41.exe`. Basename hits: exactly the two canonical paths. No `target-7a2ccd688f6c.exe` remains. `sha256sum` of the E9 copy equals the rung digest; `cmp -s` against the canonical rung printed `cmp=identical`. Copy mtime `2026-10-18 17:46:10.661182407 -0300`.

Service bind (read-only; no kill/stop/restart):

```text
/run/user/1000/systemd/transient/arc2-r6-pe.service:12
ExecStart=…/npx -y rea-agents@6.5.0 analyze /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe
systemctl --user show: ActiveState=failed SubState=failed Result=exit-code ExecMainStatus=1 NRestarts=0
ActiveEnterTimestamp=Sun 2026-10-18 17:40:58 -03
ExecMainExitTimestamp=Sun 2026-10-18 17:41:06 -03
MemoryPeak=2208227328 MemoryMax=9663676416
```

Envelope `/var/tmp/arc2-l6r6-pe/stdout.json` is 16,692 B, sha256 `4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7`, and is not JSON (`json.loads` fails at column 0). Identity lines: `stdout.json:12` `target_path:` the wall path; `stdout.json:13` `target_sha256: 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292`. Runtime dir named at `:18` (`rea-ghidra-f5rC3Z`) is absent from the scratch listing; no wall-sized copy remains under `/var/tmp`.

At 2026-10-18T20:49:29Z, `ps` showed a live `timeout -k 60 5400` analyze (pid 2279873, etime 03:19) whose argv is the canonical rung path, and a Ghidra `AnalyzeHeadless -import` of the E9 copy above. `lsof` on the two canonical paths at 20:47:59Z returned rc=1 and an empty stdout (no open fd on those paths). Not signaled.

Sibling sizes from `stat -c '%s %n' …/windows_*.exe` (same template dir, not hashed): `windows_release_arm64_console.exe` 159744; `windows_debug_arm64.exe` 98958848; `windows_release_x86_64.exe` 109268480. None equals 91,662,336.

## Verbatim-landable

```text
C1 target inventory (SC3, 2026-10-18T20:49:29Z, HEAD 54bc9dd): wall and mid-rung are pinned. Do not substitute a size-band neighbor.

Wall — lane label "91.6MB" = 91662336 bytes = 91.662336 decimal MB = 87.416015625 MiB (not MiB-91.6):
/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe
sha256 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292
inode 9021743 nlink 1 mtime 2026-10-11 16:17:46.129033608 -0300
PE32+ ARM64 machine 0xAA64, 8 sections, GUI. Godot version.txt = 4.7.2.stable.
Matches corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:16-19.
arc2-r6-pe ExecStart (/run/user/1000/systemd/transient/arc2-r6-pe.service:12) analyzes this path; envelope /var/tmp/arc2-l6r6-pe/stdout.json:12-13 repeats the path and this sha256. Unit already failed (exit 1, 17:40:58–17:41:06 -03). No remaining target-7a2ccd688f6c.exe under the searched trees. Sole 91662336-byte file under /home/vgpnk and /var/tmp.

Mid-rung — lane label "17.7MB" = 17694720 bytes = 17.69472 decimal MB = 16.875 MiB:
/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/agent-browser/bin/agent-browser-win32-x64.exe
sha256 a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786
inode 44452 nlink 1 mtime 2026-10-03 21:16:07.316555640 -0300
PE32+ AMD64 machine 0x8664, 10 sections, console, PDB-stripped. Matches .ufo/waves/arc2-loop1-round3/E6.md:235-236.
Provider import copy (different inode 2218964, cmp-identical, same sha256): /var/tmp/arc2-l6r6-E9-mid/tmp/rea-ghidra-CCbpL5/target-a6a9a3654c41.exe. At 20:49:29Z a live analyze argv named the canonical path and imported that copy. That is not a second source artifact and is not a sealed result.
```

## Labels

- **Observation:** both canonical paths, sizes, inodes, mtimes, nlink, `file` lines, full sha256s, PE machine/section raw sizes, decimal/MiB quotients, basename and exact-size find hits, E9 copy `cmp`/sha256, service ExecStart and failed state, envelope lines 12–13 and envelope sha256, sibling byte sizes, live rung argv at 20:49:29Z.
- **Inference:** the lane labels name these two files and no size-band neighbor; the E9 `target-a6a9a3654c41.exe` is a provider copy of the pinned rung, not a second source; `arc2-r6-pe` is the wall leg and was not in-flight at observation.
- **Unknown:** copies under `/root` or `/boot` (not readable) or outside `/home/vgpnk`+/`/var/tmp` for exact-size (name search also covered `/opt` and `/usr/local`, zero hits). Whether the in-flight rung analyze seals evidence — snapshot only, not this seat's result. Custody 5/5 not re-checked (out of scope).
