<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/14-crash-surface.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 / 14 — recorded-crashes & runtime-evidence surface (read-only survey, host plazir27)

Survey date: 2026-10-13. All probes read-only: `coredumpctl`, `journalctl`, `ls`, `getfacl`, `sysctl`, `zstd -dc | od`.

## Candidate: systemd-coredump is the sole crash collector and retains 174 compressed ELF cores (~4.0 GB)
- claim: `kernel.core_pattern` pipes every crashing process to `/usr/lib/systemd/systemd-coredump`; `coredumpctl list` shows 175 entries (174 COREFILE "present", 1 "missing"), stored as zstd-compressed ELF cores in `/var/lib/systemd/coredump/` totaling ~4.0 GB, spanning 2026-10-08 → 2026-10-13.
- source: `sysctl kernel.core_pattern` → `|/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %h %d %F %I`; `ulimit -c` → `unlimited`; `coredumpctl list --no-pager`; `du -sh /var/lib/systemd/coredump/` → 4.0G.
- verify: `coredumpctl list --no-pager | tail -n +2 | wc -l; du -sh /var/lib/systemd/coredump/`
- verified-at: 2026-10-13
- suggested: admit — primary runtime-evidence surface; full process memory images per crash, directly usable for RE.

## Candidate: unprivileged (uid 1000) RE access to every core via per-file ACL + coredumpctl
- claim: although core files are `root:root` `rw-r-----`, each carries an ACL grant `user:vgpnk:r--`, so the crashing user reads them without sudo; `zstd -dc` on a core yields a valid ELF header (`7f 45 4c 46`), and `coredumpctl info <pid>` prints full metadata + symbolized stack traces while `coredumpctl debug <pid>` opens gdb (gdb and eu-stack both installed).
- source: `getfacl /var/lib/systemd/coredump/core.waybar.1000.73a8e2fc20cc48749b3cbd24ed5dc7c1.1728.1791898425000000.zst`; `zstd -dc <file> | od`; `which gdb eu-stack` → `/usr/bin/gdb`, `/usr/bin/eu-stack`.
- verify: `getfacl /var/lib/systemd/coredump/*.zst | grep -m1 'user:vgpnk'; coredumpctl info --no-pager 1728 | head -30`
- verified-at: 2026-10-13
- suggested: admit — the reachability path for a reverse engineer: `coredumpctl list` → `coredumpctl info` → `coredumpctl debug` (gdb) or `zstd -d` + offline tooling.

## Candidate: crash corpus is dominated by chromium churn and deliberate self-crash test artifacts, not organic app failures
- claim: of 175 entries, 133 are `/usr/lib/chromium/chromium` (SIGTRAP/SIGABRT renderer/sandbox churn across 2026-10-08/10) and 39 are recorded as EXE `/usr/bin/bash` but actually comm `crash-godot` — a script that kills itself (`kill_builtin` → `si_code: SI_USER`, SIGSEGV) from `/tmp/mint-game-dev-3d/.shokunin/` and `/tmp/g3d-controls/` corpora. Only 3 organic non-chromium crashes exist: godot SIGABRT (2026-10-13 06:40, user project verification script), waybar SIGABRT (2026-10-13 10:33, C++ exception → `__cxa_throw` → abort), localsearch-extractor-3 (2026-10-12 19:36).
- source: `coredumpctl list --no-pager | grep -oP '/usr/\S+' | sort | uniq -c`; `coredumpctl info 1150573` (kill_builtin, SI_USER); `coredumpctl info 2500243` (godot, `__cxa_pure_virtual`); `coredumpctl info 1728` (waybar).
- verify: `coredumpctl list --no-pager | tail -n +2 | grep -oP '/usr/\S+' | sort | uniq -c`
- verified-at: 2026-10-13
- suggested: admit — falsifies the naive reading "39 bash bugs"; bulk of the surface is test noise, and the three organic crashes are the high-value RE targets.

## Candidate: no alternative crash-evidence collectors exist on this host
- claim: `/var/crash` does not exist; neither apport nor abrt is installed (`which apport abrtd` → not found); no `/var/lib/apport` or `/var/spool/abrt`; `/etc/systemd/coredump.conf` is entirely defaults (all lines commented: external storage, zst compress, ProcessSizeMax=32G, no drop-ins in `coredump.conf.d/`).
- source: `ls /var/crash` → No such file; `which apport abrtd`; `cat /etc/systemd/coredump.conf`.
- verify: `ls /var/crash /var/lib/apport /var/spool/abrt 2>&1; grep -v '^#' /etc/systemd/coredump.conf | grep -v '^\['`
- verified-at: 2026-10-13
- suggested: admit — systemd-coredump is the complete enumeration; nothing else to survey.

## Candidate: journal retains 10 boots but error surface is noise-dominated; no kernel panic/oops recorded
- claim: `journalctl --list-boots` shows 10 retained boots (2026-10-04 → 2026-10-13), journal uses 165.3M; `journalctl -p err -b` is almost entirely `sr0` optical-drive READ errors and `Buffer I/O error` noise (plus benign TDX/snapper/keyring lines); the only `panic|oops|BUG:` matches are false positives (`[drm] Registered N planes with drm panic`); 173 `dumped core` messages across all boots corroborate the coredumpctl count.
- source: `journalctl --list-boots`; `journalctl -p err -b --no-pager`; `journalctl -k | grep -inE 'panic|oops|BUG:'`; `journalctl --disk-usage`.
- verify: `journalctl -p err -b --no-pager | grep -v 'sr0\|Buffer I/O'; journalctl -k --no-pager | grep -icE 'oops|general protection fault'`
- verified-at: 2026-10-13
- suggested: admit — bounds the host's runtime-evidence horizon (~9 days of logs) and rules out kernel-level crash evidence.

## Candidate: coredump retention is unbounded-config but already decaying — earliest entry lost its file
- claim: the oldest recorded entry (chromium SIGTRAP, 2026-10-08 14:01) lists COREFILE `missing` with no size, while its journal metadata persists — i.e., default vacuuming (MaxUse/KeepFree unset → compiled defaults) has already reaped at least one core; evidence degrades oldest-first.
- source: first row of `coredumpctl list --no-pager`; `/etc/systemd/coredump.conf` (no MaxUse/KeepFree overrides).
- verify: `coredumpctl list --no-pager | head -3`
- verified-at: 2026-10-13
- suggested: admit — timeliness matters: an RE pass over the ~30+ chromium cores should run before vacuuming shrinks the window.

## Candidate: `coredumpctl debug` + gdb gives a complete on-host RE loop against retained cores
- claim: `coredumpctl debug 1728` attaches gdb to the decompressed waybar core non-interactively resolvable; combined with `coredumpctl info`'s per-thread stack traces (13+ threads shown for waybar, with libc/libstdc++/libglib offsets) and `eu-stack`, an RE can extract frames, maps, and registers without root.
- source: `coredumpctl debug --no-pager 1728` (smoke-tested, header returned); `coredumpctl info 1728` full thread listing; `/usr/bin/gdb`, `/usr/bin/eu-stack` present.
- verify: `echo 'bt' | coredumpctl debug 1728 2>&1 | head -20`
- verified-at: 2026-10-13
- suggested: admit — establishes the exact toolchain path for follow-on deep-dive lanes on the godot/waybar cores.

## Summary
Host plazir27 retains a rich, user-readable crash surface: systemd-coredump (sole collector, `core_pattern` piped, `ulimit -c` unlimited) holds 174 zstd ELF cores (~4.0 GB) over 5 days — 133 chromium, 39 deliberate `crash-godot` self-kills (SI_USER test noise), and 3 organic crashes (godot, waybar, localsearch) — all reachable unprivileged via `coredumpctl info/debug` + gdb/eu-stack; journal keeps 10 boots (165.3M) with no kernel panics and only sr0 I/O noise; retention is already decaying oldest-first.
