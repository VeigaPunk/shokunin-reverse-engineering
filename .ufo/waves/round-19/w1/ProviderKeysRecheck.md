# ProviderKeysRecheck — PROVINCE.md:26 provider-key inventory (round 19, W1)

Seat: read-only advisory (author side). Baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`.
Scoped to `PROVINCE.md:26` (`Provider-key inventory remains historical, not re-probed 2026-10-16`).
Line 26 sha256 at baseline == working tree (`cd3b3b8d…36bce5c`), so all anchors below are baseline lines.
No files written except this report. No tools installed. No secrets printed: every value below is a
filesystem path; the token-bearing `.bashrc:72-78` block was never read, copied, or sourced.

## Observation — exports and line numbers

`grep -nE 'REA_|HOPPER_' ~/.bashrc ~/.profile` → exit 0

| key | `~/.bashrc` | `~/.profile` |
|---|---|---|
| `REA_PWNTOOLS_PYTHON` | :63 | :7 |
| `REA_BINWALK_COMMAND` | :64 | :8 |
| `REA_UNBLOB_COMMAND` | :65 | :9 |
| `REA_APKTOOL_COMMAND` | :66 | :10 |
| `REA_ADB_PATH` | :67 | :11 |
| `REA_WAKARU_COMMAND` | :68 (computed at source time) | — absent |
| `REA_JADX_MCP_JAR` | :69 | :12 |
| `REA_IDA_MCP_CONFIG` | — absent | — absent |
| `HOPPER_LAUNCHER_PATH` | — absent | — absent |

`.bashrc` is 84 lines, `.profile` 15 lines (`wc -l`, exit 0). A second, broader scan
`grep -nE 'REA_|HOPPER_'` over both files returned the same lines and nothing else — no commented,
unset, or non-export assignments of either prefix exist there (exit 0).

## Observation — referenced path existence

`stat`/`readlink -f`/`file` per path (exit 0 for all):

| key | value (path) | state |
|---|---|---|
| `REA_PWNTOOLS_PYTHON` | `~/.local/share/kaidoku-pwnenv/bin/python` | symlink → `/home/vgpnk/.local/share/uv/python/cpython-3.11.17-linux-x86_64-gnu/bin/python3.11`; target exists, executable |
| `REA_BINWALK_COMMAND` | `/usr/bin/binwalk` | ELF 64-bit PIE, 3 893 960 B, 0755 |
| `REA_UNBLOB_COMMAND` | `~/.local/bin/unblob` | symlink → `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`; target is an executable Python script; `unblob --version` → `26.6.4` (exit 0) |
| `REA_APKTOOL_COMMAND` | `/usr/bin/apktool` | 2 271 B bash wrapper; `exec java … -jar "$libdir/$jarfile"` at :77 with `libdir=/usr/share/java/android-apktool` :46, `jarfile=apktool.jar` :45; `/usr/share/java/android-apktool/apktool.jar` exists, 15 478 013 B; `apktool --version` → `3.0.3` (exit 0) |
| `REA_ADB_PATH` | `/usr/bin/adb` | ELF 64-bit PIE, 4 707 704 B, 0755 |
| `REA_JADX_MCP_JAR` | `~/.local/opt/jadx-headless-mcp/jadx-headless-mcp-0.7.1-all.jar` | JAR/zip, 42 619 858 B, 0644 |
| `REA_WAKARU_COMMAND` | `$(find "$(npm root -g)/wakaru/node_modules/@wakaru/cli-linux-x64" -maxdepth 1 -name wakaru -type f \| head -n1)` | resolves non-empty to `…/node_modules/@wakaru/cli-linux-x64/wakaru`: ELF 64-bit PIE, 26 793 296 B, 0755, stripped. `npm root -g` → `/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules` (exit 0). Package versions: `wakaru` 1.14.0 and `@wakaru/cli-linux-x64` 1.14.0 |

`REA_WAKARU_COMMAND` is consumed by rea-agents 6.7.0 only when absolute
(`isAbsolute(environment.REA_WAKARU_COMMAND ?? "")`, package source) and its own requirement string
names "Wakaru ^1.13.0 … verified with 1.14.0"; the resolved 1.14.0 ELF satisfies both, and the find is
rooted at an absolute `npm root -g` (observation).

## Findings

**F1 — inventory is current for `.bashrc`.** All seven names PROVINCE.md:26 lists as previously recorded
are still exported, `.bashrc:63-69`, and every one binds an existing path. The sentence's "not re-probed
2026-10-16" is now falsified by this probe (2026-10-20): the set is unchanged, only the anchor moved.

**F2 — `.profile` diverges.** Six of seven (`:7-12`); `REA_WAKARU_COMMAND` is missing there. A POSIX
(non-bash) login shell therefore has no wakaru binding and REA's wakaru provider would refuse with its
explicit requirement message. Inference from the two files; not exercised.

**F3 — "recorded unset" still holds, in these files.** Zero occurrences of `REA_IDA_MCP_CONFIG` and
`HOPPER_LAUNCHER_PATH` in either file. This is absence-of-assignment only, not proof of unset in any
running process (see Unknowns).

**F4 — stale anchor in PROVINCE.md:26.** The sentence cites the r5-audit C8 correction as
"`.bashrc:61` → `/usr/bin/apktool`". Live: `REA_APKTOOL_COMMAND=/usr/bin/apktool` at `.bashrc:66`
(`.profile:10`). The value claim is correct, the line anchor is off by five in the current file. Inference:
the file grew above the block since the audit; historical `:61` cannot be re-derived because `.bashrc` is
untracked and no copy exists in the lane.

**F5 — the REA block sits below the interactive guard, contrary to its own comment.** `.bashrc:26-27`
states the REA block is "Above the interactive guard so agent shells (`bash -lc`, MCP launchers) see it
too", but the guard `[[ $- != *i* ]] && return` is at `.bashrc:34` and the exports are at `:63-69`. Only
`GHIDRA_INSTALL_DIR`/`JAVA_HOME` (`:28-29`) are above the guard. Guard semantics demonstrated on a
synthetic three-line file with the same construct (`bash --noprofile --norc -c 'source …'`): prints
`BEFORE` only, never `AFTER` (exit 0). Because `~/.bash_profile:5` does `. ~/.bashrc`, a non-interactive
login shell (`bash -lc`) reaches `:34` and returns before the exports. Inference (high confidence): such
shells get no `REA_*` at all; an interactive shell gets all seven. This contradicts the stated intent and
is the one finding here that can change REA provider availability, not just documentation.

**F6 — `.profile` is dead for bash logins.** `~/.bash_profile` exists (8 lines) and sources `.bashrc` at
`:5`; bash reads the first of `.bash_profile`/`.bash_login`/`.profile`, so `.profile` applies only to
non-bash login shells. Its own header says so (`~/.profile:1-2`). Combined with F2, the duplicate block is
maintained twice with a silent one-key drift.

**F7 — names are canonical, coverage is partial by design.** All seven exported names appear in
rea-agents 6.7.0 (`/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents`) with no deprecated
variants: `REA_JADX_MCP_JAR` 34, `REA_PWNTOOLS_PYTHON` 30, `REA_BINWALK_COMMAND` 13,
`REA_WAKARU_COMMAND` 10, `REA_ADB_PATH` 9, `REA_APKTOOL_COMMAND` 8, `REA_UNBLOB_COMMAND` 7 mentions.
The package names 89 distinct `REA_*`/`HOPPER_*` identifiers; the path-selecting ones not exported in
either file include `REA_KUNA_COMMAND`, `REA_TSHARK_COMMAND`, `REA_SIGROK_COMMAND`, `REA_ILSPY_CMD_PATH`,
`REA_WABT_BIN_DIRECTORY`, `REA_JEB_MCP_URL` (plus the F3 pair). Inference: these fall back to provider
defaults or stay unavailable; the inventory's seven are the ones this host chose to pin explicitly.

## Unknowns / not probed

- Live environment of the current Devin/OMP shells: not read. Sourcing `.bashrc` would also execute the
  token block at `:72-78`, which the host rules forbid touching; F5 is therefore inference from line
  order plus demonstrated `return` semantics, not an observed `env`.
- Whether REA MCP launchers inherit their environment from an interactive shell or start fresh (F5's
  practical blast radius) — not traced; out of this seat's question.
- Whether the historical `.bashrc:61` anchor was correct at audit time — unverifiable (untracked file,
  no snapshot in the lane).

## Commands (all pasted with exit)

```
grep -nE 'REA_|HOPPER_' ~/.bashrc ~/.profile                       # exit 0
wc -l < ~/.bashrc; wc -l < ~/.profile                              # 84; 15, exit 0
stat -c '%F %s bytes mode=%A' <7 paths>                            # all EXISTS, exit 0
readlink -f ~/.local/share/kaidoku-pwnenv/bin/python ~/.local/bin/unblob   # exit 0 (R1=0,R2=0)
find "$(npm root -g)/wakaru/node_modules/@wakaru/cli-linux-x64" -maxdepth 1 -name wakaru -type f | head -n1
                                                                    # non-empty, exit 0
file -b <binwalk|apktool|adb|jadx jar|unblob>                      # exit 0
~/.local/bin/unblob --version → 26.6.4                             # exit 0
/usr/bin/apktool --version → 3.0.3                                 # exit 0
ls -l /usr/share/java/android-apktool/                             # exit 0; apktool.jar 15478013 B
bash --noprofile --norc -c 'source /tmp/kr19-guard-probe.sh'       # prints BEFORE only, exit 0
python3 -c '<package.json name/version read>'                      # wakaru 1.14.0, cli-linux-x64 1.14.0, exit 0
grep -rhoE '\b(REA|HOPPER)_[A-Z0-9_]+' <rea-agents 6.7.0> | sort -u | wc -l   # 89, exit 0
git --no-optional-locks show 8a8da7e…:PROVINCE.md | sed -n '26p' | sha256sum # cd3b3b8d…36bce5c, exit 0
```

## Suggested PROVINCE.md:26 replacement (for L1's C2 rewrite)

> Provider-key inventory re-probed 2026-10-20: `.bashrc:63-69` exports `REA_PWNTOOLS_PYTHON`,
> `REA_BINWALK_COMMAND`, `REA_UNBLOB_COMMAND`, `REA_APKTOOL_COMMAND` (live at `.bashrc:66`, not the
> audit's `:61`), `REA_ADB_PATH`, `REA_WAKARU_COMMAND` (resolves to the 1.14.0 `@wakaru/cli-linux-x64` ELF),
> and `REA_JADX_MCP_JAR`; every referenced path exists. `~/.profile:7-12` duplicates six of them and omits
> `REA_WAKARU_COMMAND` (reachable only by non-bash login shells; `.bash_profile:5` routes bash logins to
> `.bashrc`). `REA_IDA_MCP_CONFIG` and `HOPPER_LAUNCHER_PATH` remain unset. The block is below the
> `.bashrc:34` interactive guard despite the `:26-27` comment, so non-interactive shells see none of the
> seven.

No installs, no upgrades, no REA/Ghidra runs, no carrier execution.
