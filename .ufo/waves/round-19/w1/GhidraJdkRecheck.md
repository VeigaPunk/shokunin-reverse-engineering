# Ghidra/JDK recheck — PROVINCE.md:25 (round 19, w1)

Seat: KaidokuR19.GhidraJdkRecheck (read-only; no patch). Lane observed at
`refs/heads/main = 85589ac757f9ca3cb25efcd702d0963e25c9c4df` (2026-10-20 15:37:18 -0300).
PROVINCE.md is byte-identical at contract baseline `8a8da7e…` and at main (`git diff --name-only B main`
lists 19 files, none PROVINCE.md; `git status --porcelain -- PROVINCE.md` is empty) — the claim below is the
same text at both revisions, and at `B:PROVINCE.md:25` (`git show B:PROVINCE.md | grep -n 'Reverified Ghidra'`
→ line 25, exit 0).

## Verdict: all five VALUES match; all `.bashrc` ANCHORS are stale by +5 lines

PROVINCE.md:25 (one long line) asserts: `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`,
`application.version=12.1.4` (build `2026-Sep-21 1613 UTC`), `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`,
Java `21.0.12.1`, and anchors `Ghidra/application.properties:17`, `~/.bashrc:23-24`, plus the exact quoted
first line of `java -version`.

| Claim (PROVINCE.md:25) | Observed now | Verdict |
|---|---|---|
| `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` | `~/.bashrc:28` `export GHIDRA_INSTALL_DIR="$HOME/.local/opt/ghidra_12.1.4_PUBLIC"`; `bash -lc` expands to the claimed path (`HOME=/home/vgpnk`) | value MATCH, anchor STALE (`:23-24` → `:28-29`) |
| `application.version=12.1.4` at `Ghidra/application.properties:17` | line 17 `application.version=12.1.4`; exactly one such key in a 17-line file | MATCH |
| build `2026-Sep-21 1613 UTC` | line 2 `application.build.date=2026-Sep-21 1613 UTC`; line 1 header `#Mon Sep 21 16:13:00 UTC 2026` (same instant, other format) | MATCH |
| `JAVA_HOME=/usr/lib/jvm/java-21-openjdk` | `~/.bashrc:29` `export JAVA_HOME=/usr/lib/jvm/java-21-openjdk` | value MATCH, anchor STALE |
| Java `21.0.12.1`; quote `openjdk version "21.0.12.1" 2026-08-18` | `java -version 2>&1 \| head -n 1` prints exactly that line | MATCH (byte-exact) |

Observation: the values are current; only the `.bashrc` line numbers moved. The claim's own date word
("reverified 2026-10-18") is not falsified by anything here — it is the anchors that no longer hold.

Collateral drift, same root cause (outside the ticket's five values, reported for the L1's freshness pass):
- PROVINCE.md:26 `APKTOOL_COMMAND_ENV=…`, `.bashrc:61` → `/usr/bin/apktool`: today `.bashrc:66`
  (`grep -n 'apktool\|/usr/bin' ~/.bashrc` → `:64 REA_BINWALK_COMMAND`, `:66 REA_APKTOOL_COMMAND`,
  `:67 REA_ADB_PATH`, exit 0).
- PROVINCE.md:49 (Core JDK row) `.bashrc:24` → today `:29`; its other anchor `.profile:4` is still correct
  (`~/.profile:4` `export JAVA_HOME=/usr/lib/jvm/java-21-openjdk`).

## Why the anchors are stale (observation, then inference)

Observation — a retained pre-change copy, `~/.bashrc.bak.1792084648` (mtime 2026-10-15 14:17:28 -0300,
3412 bytes; `date -d @1792084648` → `2026-10-15 14:17:28 -0300`, exit 0) holds the cited anchors exactly:
`grep -n` → `23:export GHIDRA_INSTALL_DIR=…`, `24:export JAVA_HOME=…`, `61:export REA_APKTOOL_COMMAND=/usr/bin/apktool`
(exit 0). Current `~/.bashrc` mtime is 2026-10-19 18:46:35 -0300. `diff -u backup current` (exit 1) shows
11 insertions and 0 deletions: +5 lines in the fnm block before the exports (comment lines about
`__fnmcd`/`unalias cd`) and +6 lines at the tail (`grok installer` PATH block). 23+5=28, 24+5=29, 61+5=66.

Inference [INFERENCE]: the cited `:23-24` were correct for the .bashrc state at and before the 2026-10-18
reverification (the 10-15 backup is the only retained old copy), and a 2026-10-19 18:46 edit shifted the
REA block by +5 without touching the exported values. No retained copy of the exact 2026-10-18 state exists,
so "the 10-18 read landed on 23-24" is inferred from the 10-15 backup, not directly observed.

Operational reachability (observation): the REA block sits above the interactive guard
(`~/.bashrc:32` `[[ $- != *i* ]] && return`); `~/.bash_profile` unconditionally sources `~/.bashrc`, and
`bash -lc 'printf …'` returned `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`,
`JAVA_HOME=/usr/lib/jvm/java-21-openjdk` (exit 0) — so agent/MCP shells still see both after the shift.

## Depth corroboration (extra checks beyond the five values)

- `Ghidra/application.properties`: 17 lines; `sha256 e84c26b08545eee63d24a1a8a4dd7905e4209538e2e7192093877c435c64eb67`;
  mtime 2026-09-21 16:37:24 -0300 — install file untouched since build, so the version/build pair is not a
  later patch-level edit. `support/analyzeHeadless` present (2388 bytes, mtime 2026-09-21 16:38:14 -0300).
- Version triple corroboration: `application.release.name=PUBLIC` (:13), `application.revision.ghidra=8b6bbb85…`
  (:14) matches PROVINCE.md:46's "rev 8b6bbb85"; `application.java.min=21` (:8).
- JDK identity: `java -XshowSettings:properties -version` → `java.home=/usr/lib/jvm/java-21-openjdk`,
  `java.version=21.0.12.1`, `java.runtime.version=21.0.12.1+1`, `java.specification.version=21`,
  `java.vendor=Arch Linux` (exit 0). `JAVA_HOME/release` → `JAVA_VERSION="21.0.12.1"`,
  `IMPLEMENTOR="Arch Linux"`, `OS_ARCH="x86_64"`. `/usr/bin/java` → `/usr/lib/jvm/java-21-openjdk/bin/java`;
  `readlink -f /usr/lib/jvm/{default,default-runtime}` both → `java-21-openjdk`; `/usr/lib/jvm` children are
  `default`, `default-runtime`, `java-21-openjdk`, i.e. one JDK — corroborates "sole Java on host". So Ghidra's
  `java.min=21` is met by 21.0.12.1 (inference from the two observed values, no launch of Ghidra required).

## Commands and exits (all read-only)

1. `grep -n -E '^(application\.version|application\.release\.name|application\.build\.date|application\.build\.revision)=' /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties` → exit 0 (`2:build.date`, `13:release.name`, `17:version`).
2. `java -version 2>&1 | head -n 1` → exit 0 (`openjdk version "21.0.12.1" 2026-08-18`); `java -version` → exit 0 (Runtime/VM lines `21.0.12.1+1`).
3. `grep -n -E 'GHIDRA_INSTALL_DIR|JAVA_HOME' /home/vgpnk/.bashrc` → exit 0 (`28:`, `29:`).
4. `bash -lc 'printf "HOME=%s\nGHIDRA_INSTALL_DIR=%s\nJAVA_HOME=%s\n" …'` → exit 0 (values as claimed).
5. `grep -c '^application.version=' <props>` → `1`, exit 0; `sha256sum <props>` → exit 0 (hash above); `wc -l <props>` → `17`, exit 0.
6. `grep -n 'apktool\|/usr/bin' /home/vgpnk/.bashrc` → exit 0 (`1:`, `64:`, `66:`, `67:`).
7. `ls -1a /home/vgpnk/ | grep -i 'bashrc\|bash_profile\|bash_login'` → exit 0 (`.bash_profile`, `.bashrc`, `.bashrc.bak.1792084648`).
8. `java -XshowSettings:properties -version 2>&1 | grep -E 'java\.(home|version|vendor|runtime\.version) =|java\.specification\.version'` → exit 0 (values above).
9. `date -d @1792084648 …`, `stat -c '%y %s %n' <backup>`, `grep -n 'GHIDRA_INSTALL_DIR\|JAVA_HOME\|REA_APKTOOL_COMMAND' <backup>` → exit 0, exit 0, exit 0 (`23:`, `24:`, `61:`).
10. `diff -u /home/vgpnk/.bashrc.bak.1792084648 /home/vgpnk/.bashrc` → exit 1 (expected: 11 insertions, 0 deletions).
11. `git -C LANE show 8a8da7e…:PROVINCE.md | grep -n 'Reverified Ghidra'` → exit 0 (line 25); `git -C LANE diff --name-only 8a8da7e… refs/heads/main | head -n 20` → exit 0 (no PROVINCE.md); `git -C LANE status --porcelain -- PROVINCE.md` → exit 0 (empty).
12. `readlink -f` on `/usr/lib/jvm/java-21-openjdk`, `/usr/bin/java`, `/usr/lib/jvm/{default,default-runtime}`, `ls -1 /usr/lib/jvm`, `stat -c` on the Ghidra prop + analyzeHeadless, `grep -E '^(JAVA_VERSION|…)=' /usr/lib/jvm/java-21-openjdk/release` → all exit 0.
13. `grep -n '^application.revision.ghidra=\|^application.java.min=\|^application.build.date=\|^application.version=' <props>` → exit 0 (`2`, `8`, `14`, `17`).

No REA analyze/search/decompile, no Ghidra `analyzeHeadless`, no carrier executed, no git/jj writes, no writes
outside this report. No tool installed or upgraded (nothing needed).

## Remaining unknowns

- What/whom the 2026-10-19 18:46:35 .bashrc edit came from (diff shows the fnm alias note + `grok installer`
  PATH block, not the actor or intent).
- Whether the 2026-10-18 reverification actually observed `.bashrc:23-24` at that time; the 10-15 backup is the
  nearest retained evidence and matches the cited anchors.
- Whether L1 wants PROVINCE.md:25's date word advanced to 2026-10-20 and the three `.bashrc` anchors
  (`:23-24` here, `:61` at :26, `:24` at :49) corrected — value claims need no change; anchor text does.
- Not probed here: live `rea doctor` / `binary_session` provider state for Ghidra (out of this ticket's five
  values; would add no information about the properties file or JDK).
