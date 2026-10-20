# Fallback readers recheck — PROVINCE.md:62 (round 19, w1)

Seat: KaidokuR19.FallbackReaders (scout, read-only; no patch). No tool installed or upgraded; no pacman
transaction run; nothing written except this report.

Base identity: contract B = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. Working tree `PROVINCE.md` blob =
`99e1ecc4499d6f2e8f8bb8c10406ab84d49eecab` = `git rev-parse B:PROVINCE.md` (both exit 0);
`git --no-optional-locks diff --stat B -- PROVINCE.md` empty (exit 0); `git --no-optional-locks status
--porcelain -- PROVINCE.md` empty (exit 0); `git --no-optional-locks diff --name-only B refs/heads/main --
PROVINCE.md` empty (exit 0). So line 62 is byte-identical at B, at the lane head observed
(`refs/heads/main = 85589ac757f9ca3cb25efcd702d0963e25c9c4df`) and in the working tree: what follows is
**host drift against unchanged text**, not an edit. (A first `git diff --no-optional-locks --stat …` exited 129
because `--no-optional-locks` was misplaced after the subcommand; the corrected form above is the recorded one.)

The row's own probe is `command -v <tool>` (PROVINCE.md:62, column "Liveness / readiness probe"); the absent
cell reads ``absent: `cabextract`, `rizin`, `ltrace`, pacman-contrib``. Lane-wide, only PROVINCE.md:13 and
PROVINCE.md:103-104 speak of fallbacks otherwise.

## Verdict

- **22/22** present-list binaries resolve in the operator shell (`command -v` exit 0), and every one of them
  runs (version probe exit 0). The present list needs no removal.
- **2 of the 4 "absent" entries are now present**: `rizin` and `pacman-contrib`. The row's absent cell is stale.
- `cabextract` and `ltrace` are still absent — those two half of the cell are correct.
- Both installs predate baseline commit `8a8da7e…` (2026-10-20 15:28:02 -03): the row was **already stale at B**
  (roughly 21 h and 7.7 h respectively), not drifted during round 19.

## Present list — every named tool, probed (observation)

Session PATH starts `/run/user/1000/fnm_multishells/4348_…/bin`, then `~/.local/share/fnm`, `~/.opencode/bin`,
`~/.local/bin`, … `/usr/bin`. `Owner` = `pacman -Qo <path>` (rc 0 for every row; node/npx have no pacman owner).

| Tool (PROVINCE.md:62) | `command -v` exit | Resolved path | Owner (package/version) | Version probe (exit 0 each) |
|---|---|---|---|---|
| `file` | 0 | `/usr/bin/file` | file 5.48-1 | `file-5.48` |
| `readelf` | 0 | `/usr/bin/readelf` | binutils 2.47-4 | `GNU readelf (GNU Binutils) 2.47` |
| `objdump` | 0 | `/usr/bin/objdump` | binutils 2.47-4 | `GNU objdump (GNU Binutils) 2.47` |
| `llvm-readobj` | 0 | `/usr/bin/llvm-readobj` | llvm 23.1.3-3 | `LLVM version 23.1.3` |
| `nm` | 0 | `/usr/bin/nm` | binutils 2.47-4 | `GNU nm (GNU Binutils) 2.47` |
| `strings` | 0 | `/usr/bin/strings` | binutils 2.47-4 | `GNU strings (GNU Binutils) 2.47` |
| `unzip` | 0 | `/usr/bin/unzip` | unzip 6.0-23 | `UnZip 6.00 of 20 April 2009` |
| `tar` | 0 | `/usr/bin/tar` | tar 1.35-5 | `tar (GNU tar) 1.35` |
| `gdb` | 0 | `/usr/bin/gdb` | gdb 18.1-1 | `GNU gdb (GDB) 18.1` |
| `eu-stack` | 0 | `/usr/bin/eu-stack` | elfutils 0.196-1 | `eu-stack (elfutils) 0.196` |
| `coredumpctl` | 0 | `/usr/bin/coredumpctl` | systemd 262-1 | `systemd 262 (262-1-arch)` |
| `pacman` | 0 | `/usr/bin/pacman` | pacman 7.1.0.r9.g54d9411-3 | `Pacman v7.1.0 - libalpm v16.0.1` |
| `zstd` | 0 | `/usr/bin/zstd` | zstd 1.5.7-3 | `Zstandard CLI v1.5.7` |
| `gpg` | 0 | `/usr/bin/gpg` | gnupg 2.4.9-3 | `gpg (GnuPG) 2.4.9`, libgcrypt 1.12.4 |
| `python3` | 0 | `/usr/bin/python3` | python 3.14.8-1 | `Python 3.14.8` |
| `node` | 0 | `/run/user/1000/fnm_multishells/4348_1792501188326/bin/node` | none (fnm shim) | `v24.21.0` |
| `npx` | 0 | same fnm shim dir | none (fnm shim) | `11.19.0` |
| `7z` | 0 | `/usr/bin/7z` | 7zip 26.04-1 | `7-Zip 26.04 (x64)` |
| `xxd` | 0 | `/usr/bin/xxd` → `/usr/bin/tinyxxd` (symlink) | tinyxxd 1.3.17-1 | `tinyxxd 1.3.17` |
| `radare2` | 0 | `/usr/bin/radare2` | radare2 6.2.2-1 | `radare2 6.2.2 +37485 abi:142 @ linux-x86_64` |
| `strace` | 0 | `/usr/bin/strace` | strace 7.2-1 | `strace -- version 7.2` |
| `upx` | 0 | `/usr/bin/upx` | upx 5.2.0-1 | `upx 5.2.0` |

`7z i` was first run through `| head -3`, which reported rc 141 (head's SIGPIPE, not a 7z failure); the
unpiped re-run `7z i > file` exited 0 — that is the recorded result.

## Absent cell — each entry probed with the right probe (observation)

| Entry as written (PROVINCE.md:62) | Probe and exit | Result | Verdict |
|---|---|---|---|
| `cabextract` | `command -v cabextract` → rc 1; `pacman -Q cabextract` → `error: package 'cabextract' was not found`, rc 1 | no path | **still absent** (row correct) |
| `rizin` | `command -v rizin` → rc 0, `/usr/bin/rizin`; `pacman -Q rizin` → `rizin 0.8.2-2`, rc 0; `rizin -v` → `rizin 0.8.2 @ linux-x86-64`, rc 0 | present and runnable | **row WRONG** |
| `ltrace` | `command -v ltrace` → rc 1; `pacman -Q ltrace` → `error: package 'ltrace' was not found`, rc 1 | no path | **still absent** (row correct) |
| `pacman-contrib` | `command -v pacman-contrib` → rc 1 (meaningless: package name, not a binary); `pacman -Q pacman-contrib` → `pacman-contrib 1.13.1-1`, rc 0 | installed | **row WRONG** |

Sync-db state (observed, not installed by this seat): `extra/cabextract 1.11-3`, `extra/ltrace 0.8.1-1`
(`pacman -Ss '^cabextract$|^ltrace$'`, exit 0).

`pacman-contrib 1.13.1-1` members under `/usr/bin` (`pacman -Ql`, exit 0): `checkupdates`, `paccache`,
`pacdiff`, `paclist`, `paclog-pkglist`, `pacscripts`, `pacsearch`, `pacsort`, `pactree`, `rankmirrors`,
`updpkgsums`. Spot-probed: `updpkgsums`, `paccache`, `rankmirrors`, `checkupdates`, `pacdiff` all `command -v`
rc 0; `pacman -Qo /usr/bin/pactree` → `pacman-contrib 1.13.1-1` (rc 0). So the row's present list is also
missing a usable reader family if the row intends `pacman-contrib`'s binaries (`pacman -Qkk` workflows at
PROVINCE.md:53 lean on pacman itself, not contrib).

## When the two host changes happened (observation, `/var/log/pacman.log`)

- `rizin` — `/var/log/pacman.log:2368` `[2026-10-19T18:31:20-0300] [PACMAN] Running 'pacman -S --needed
  --noconfirm lychee rizin shfmt'`; `:2372` `[ALPM] installed rizin (0.8.2-2)`. Package also provides
  `rz-asm`, `rz-ax`, `rz-bin`, `rz-diff`, `rz-find`, `rz-gg`, `rz-hash`, `rz-run`, `rz-sign`, `rz-test`
  (`pacman -Ql rizin`, exit 0). `pacman -Qi rizin` → Install Date `Mon 19 Oct 2026 06:31:23 PM -03`,
  install reason `Explicitly installed`, `Required By: None`.
- `pacman-contrib` — `:2440` `[2026-10-20T07:45:36-0300] [PACMAN] Running 'pacman -S --needed --noconfirm
  compsize pacman-contrib'`; `:2444` `[ALPM] installed pacman-contrib (1.13.1-1)`. Install Date
  `Tue 20 Oct 2026 07:45:37 AM -03`, `Explicitly installed`, `Required By: None`.

## Calibration notes (all observation unless labelled)

1. **The row's probe is environment-conditional for `node`/`npx`.** Under `env -i PATH=/usr/local/bin:/usr/bin`
   the sweep gives `node` rc 1 and `npx` rc 1 while the other 20 present-list entries stay rc 0. Under a login
   shell (`bash -lc`) both resolve via a *different* fnm multishell dir. So PROVINCE.md:62's `node/npx` claim
   holds only while the fnm block is on PATH; a probe with a scrubbed environment (cf. the carried
   `jj-red-before` env-scrub item) must not assume it. Everything else named in the present list is a
   `/usr/bin` package binary and is PATH-robust under the clean sweep.
2. **`command -v` cannot see version drift.** A `pacman -Syu` at 2026-10-20 09:15:30 (`pacman.log:2462`)
   upgraded four of the five "host-installed 2026-10-13" tools: 7zip 26.03→26.04 (`:2543`), radare2
   6.2.0→6.2.2 (`:2909`), strace 7.0→7.2 (`:2918`), tinyxxd 1.3.16→1.3.17 (`:2923`); `upx` is unchanged
   (5.2.0-1, Install Date 2026-10-13 13:52:22). The row's install date is historically corroborated by
   `pacman.log:2072-2085` (`pacman -S --needed --noconfirm binwalk jadx android-tools radare2 strace upx
   tinyxxd 7zip`, 2026-10-13 13:52:21, installing radare2 6.2.0 / strace 7.0 / upx 5.2.0 / tinyxxd 1.3.16 /
   7zip 26.03). ALPM `Install Date` now reads 2026-10-20 09:16 for the four upgraded ones only because an
   upgrade resets it — so the date word is **not** a defect; no version text exists in the row to go stale.
3. `xxd` resolves to `tinyxxd 1.3.17-1`, not vim's xxd. Presence claim holds; a recipe depending on vim-xxd
   specifics would need its own check (none in PROVINCE.md).
4. `7zz` is not shipped by `7zip 26.04-1` (members `7z`, `7za`, `7zr`; `command -v 7zz` rc 1). The row names
   `7z`, so correct. No lane call site outside `.ufo` uses `7zz` (grep over the lane minus `.git`/`.ufo`
   returned only corpus prose).
5. `llvm-readobj` is an unversioned `/usr/bin` path owned by `llvm 23.1.3-3`; `llvm-readobj-18`, `-19`, `-20`
   all rc 1, so no versioned alternative competes on PATH and the unversioned name in the row is stable.

## Adjacent stale records (freshness candidates; outside this ticket, not edited)

- `corpus/knowledge/2026-10-13-pacman-packages.md:63-68` — dated 2026-10-13 candidate "toolset tiering …
  pacman-contrib absent". Now contradicted three ways: (a) `pacman-contrib 1.13.1-1` is installed; (b) its
  member list contains `pactree` but **not** `paccheck` or `pacfiles`, so the file's parenthetical
  "`paccheck`, `pactree`, `pacfiles` (pacman-contrib)" is wrong about the package's contents; (c) the line-66
  self-check `command -v paccheck pactree pacfiles || echo "pacman-contrib absent"` now exits 0 on `pactree`
  and can no longer emit its own absent message. Erratum candidate (that file already carries an append-only
  `## Erratum` section at :71-73).
- `corpus/knowledge/2026-10-13-pe-surface.md:65` — dated record: "`rabin2`, `r2`, `radare2`, `rz-bin`, …,
  `xxd` are all missing from PATH". Now `radare2 6.2.2-1`, `rizin 0.8.2-2` and `xxd` (tinyxxd) are all
  present. Whether that sweep ran before the 2026-10-13 13:52:22 install transaction is not observable, so
  this is a historical snapshot, not a defect claim; it should not be cited as current absence.
- `PROVINCE.md:103-104` — "gdb scripting, strace/ltrace, unpacking by execution … (unowned)": `ltrace` is still
  absent, `strace` present; the sentence is about lane ownership of non-REA dynamic analysis, not presence, so
  no change is indicated by this ticket.

## Suggested minimal row correction (advisory only; the writer/L1 owns PROVINCE.md)

- Present list: add `` `rizin` `` (drop it from absent). If contrib binaries matter, name them
  (`` `pactree` ``, `` `paccache` ``, etc.) rather than the package.
- Absent cell becomes ``absent: `cabextract`, `ltrace` ``.
- Optional date refresh on the probe (e.g. "rechecked 2026-10-20") — the row currently carries no date in its
  evidence column; `PROVINCE.md:40` dates the surface table "verified on this host 2026-10-13", which is the
  only date anchor near this row.

## Commands and exit codes (all read-only; no REA, no Ghidra, no carrier executed)

1. `git hash-object PROVINCE.md` → exit 0 (`99e1ecc…`); `git rev-parse B:PROVINCE.md` → exit 0 (same blob);
   `git ls-files -s PROVINCE.md` → exit 0; `git log -1 --format='%H %ci %s' B` → exit 0.
2. `git --no-optional-locks diff --stat B -- PROVINCE.md` → exit 0 (empty); `… status --porcelain -- PROVINCE.md`
   → exit 0 (empty); `… diff --name-only B refs/heads/main -- PROVINCE.md` → exit 0 (empty). (Earlier
   `git diff --no-optional-locks …` → exit 129, usage error from option placement, superseded.)
3. `for t in file readelf objdump llvm-readobj nm strings unzip tar gdb eu-stack coredumpctl pacman zstd gpg
   python3 node npx 7z xxd radare2 strace upx; do command -v "$t"; done` → every tool printed, 22/22 exit 0.
4. Clean sweep `env -i PATH=/usr/local/bin:/usr/bin bash -c '…command -v…'` → exit 0; inside it `node` rc 1,
   `npx` rc 1, other 20 rc 0.
5. Login shell `bash -lc '…command -v node npx rizin pacman-contrib cabextract ltrace'` → exit 0; node/npx
   rc 0 (fnm dir `/run/user/1000/fnm_multishells/3383583_…`), rizin rc 0, the other three rc 1.
6. `command -v cabextract` rc 1; `command -v ltrace` rc 1; `command -v rizin` rc 0; `command -v pacman-contrib`
   rc 1; `command -v 7zz` rc 1.
7. `pacman -Q cabextract ltrace` → rc 1 (`error: package … was not found` for both); `pacman -Q pacman-contrib`
   → rc 0 (`pacman-contrib 1.13.1-1`); `pacman -Q rizin` → rc 0 (`rizin 0.8.2-2`);
   `pacman -Q rizin radare2 pacman-contrib p7zip 7zip r2ghidra` → rc 1 (only `r2ghidra` not found; the rest
   printed).
8. `pacman -Qi rizin pacman-contrib` → exit 0 (Install Date / reason / Required By as quoted);
   `pacman -Qi 7zip tinyxxd radare2 strace upx` → exit 0.
9. `pacman -Qo <path>` for `/usr/bin/{file,readelf,objdump,nm,strings,unzip,tar,gdb,coredumpctl,pacman,zstd,gpg,
   python3,llvm-readobj,7z,rizin,radare2,upx,eu-stack,pactree}` → exit 0 each; `readlink -f /usr/bin/xxd` →
   `/usr/bin/tinyxxd`, exit 0.
10. `pacman -Ql 7zip`, `pacman -Ql pacman-contrib`, `pacman -Ql rizin` (grepped to `/usr/bin/`) → exit 0 each.
11. `pacman -Ss '^cabextract$|^ltrace$'` → exit 0 (`extra/cabextract 1.11-3`, `extra/ltrace 0.8.1-1`).
12. Version probes: `file --version`, `readelf --version`, `objdump --version`, `llvm-readobj --version`,
    `nm --version`, `strings --version`, `unzip -v`, `tar --version`, `gdb --version`, `eu-stack --version`,
    `coredumpctl --version`, `pacman --version`, `zstd --version`, `gpg --version`, `python3 --version`,
    `node --version`, `npx --version`, `7z i`, `xxd -v`, `radare2 -v`, `rizin -v`, `strace -V`, `upx --version`
    → exit 0 each (first line quoted in the table; `7z i` rc 141 only when piped to `head`, unpiped rc 0).
13. `grep -E 'installed (rizin|pacman-contrib) ' /var/log/pacman.log` → exit 0 (2 lines); `grep -nE
    '\[2026-10-19T18:3[01]|\[2026-10-20T07:4[45]' /var/log/pacman.log` → exit 0 (transaction lines
    2368/2372, 2440/2444); `grep -nE '\[2026-10-20T09:16.*(7zip|tinyxxd|radare2|strace|upx)'` → exit 0
    (`:2543`, `:2909`, `:2918`, `:2923`); `grep -nE '\[2026-10-1[23]T.*(7zip|tinyxxd|radare2|strace|upx|xxd)'`
    → exit 0 (`:2072`, `:2081-2085`).
14. Lane greps (`grep -rn --exclude-dir=.git --exclude-dir=.ufo` for `Host fallback readers`, `rizin`,
    `pacman-contrib`, `cabextract`, `ltrace`, `7zz`, `paccheck`, `pacfiles`, `pactree`) → exit 0; hits only at
    PROVINCE.md:13,62,103 and the two corpus files quoted above (plus a `device not found…` regex false hit at
    `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:90`).
15. `grep -c -i rizin ~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/reverseEngineering.js`
    → `2`, exit 0 (read of the cached 6.7.0 package; no REA CLI run).

## Remaining unknowns

- Whether the new host `/usr/bin/rizin` changes any REA verb's availability (`rizin_debug_command`,
  `execute_rizin_command` appear in the cached 6.7.0 catalog schemas; the dist mentions rizin twice). Not
  probed: out of this ticket and REA state is C2's. [INFERENCE] a PATH `rizin` is the usual host-side lookup,
  but nothing here observes REA resolving it.
- Whether the 2026-10-20 09:15:30 `pacman -Syu` (`pacman.log:2462`) predates the host-wide pacman pause; the
  pause declaration time is not observable from the lane. It explains the four version bumps only.
- Whether the operator intends `rizin`/`pacman-contrib` to remain installed — host state is operator-owned and
  PROVINCE follows the host (round-19 non-goal: no client-config edit).
- Not probed by this seat: `cabextract`/`ltrace` usability, and anything about REA providers or Ghidra.
