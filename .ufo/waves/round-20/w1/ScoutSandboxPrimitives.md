# Scout — sandbox primitives for D6b (round 20, no installs)

Scope: probe which host primitives give an unprivileged user (a) network isolation and
(b) a read-only root, for `W20/tools/revexec.py` (D6b, `.ufo/waves/round-20/contract.md:58-61`).
Read-only seat: no lane/repo modification. No tool installs or upgrades were made.
Clock at write: `2026-10-20T17:52:28-03:00` (`date -Iseconds`).

## 1. Measurement identity (observation)

```
id            -> uid=1000(vgpnk) gid=1000(vgpnk) groups=1000,967(docker),992(input),998(wheel)
/proc/self/status -> CapEff: 0000000000000000  Seccomp: 0  NoNewPrivs: 0
uname -r      -> 7.2.11-arch1-1
unshare --version -> util-linux 2.42.4 ; bwrap --version -> bubblewrap 0.13.1 ; systemd 262-1-arch
```

Host `sudo -n id` returns `uid=0(root)` (passwordless sudo exists) — but every sandbox below
blocks `sudo` (see §5). All probes ran as uid 1000 with CapEff=0.

## 2. The four requested probes, verbatim with exit

| # | Command | Observed output | Exit |
|---|---|---|---|
| 1 | `unshare --user --map-root-user --net --mount true` | no output | **0** |
| 2a | `cat /proc/sys/kernel/unprivileged_userns_clone` | `1` | **0** |
| 2b | `cat /proc/sys/user/max_user_namespaces` | `122865` | **0** |
| 3 | `systemd-run --user --pipe --wait -p PrivateNetwork=yes true` | `Finished with result: success` | **0** |
| 4 | `command -v bwrap firejail nsjail` | `/usr/bin/bwrap` (firejail, nsjail absent) | **0** (found bwrap) |

Per-binary presence: `bwrap` `/usr/bin/bwrap` rc 0; `firejail` absent rc 1; `nsjail` absent rc 1;
`unshare` `/usr/bin/unshare` rc 0. Additional sysctls: `max_net_namespaces=122865`,
`max_mnt_namespaces=122865`; `kernel.apparmor_restrict_unprivileged_userns` **does not exist**;
`kernel.yama.ptrace_scope=1`.

**Contract contradiction (observation):** `contract.md:60` says "bwrap is NOT installed".
`/usr/bin/bwrap` exists (bubblewrap 0.13.1-1, `pacman -Q`), mode `-rwxr-xr-x`, no file caps, and it
works unprivileged (§4). The lane already records the package at
`corpus/knowledge/2026-10-13-r2-version-diff-compare.md:18`.

## 3. Network isolation — IP yes, AF_UNIX no (observation unless marked)

Net namespace content under `unshare --user --map-root-user --net --mount`:
`ip -o link` → only `lo: <LOOPBACK> ... state DOWN`; `ip route` empty; `ls /sys/class/net`
still lists `enp7s0` (host sysfs mount is shared — name leak only).
Egress probes inside: `/dev/tcp/1.1.1.1/80` → `Network is unreachable` (exit 1);
UDP `sendto(1.1.1.1:53)` → `OSError [Errno 101] Network is unreachable`.
`unshare --net` **without** `--user` → `unshare failed: Operation not permitted`, exit 1
(CAP_SYS_ADMIN absent; the pair is required). `unshare --user --map-root-user --mount` (no `--net`)
leaves TCP reachable (exit 0). `bwrap` without `--unshare-net` likewise leaves TCP reachable.

**DNS is not isolated.** Inside the netns: `getent hosts archlinux.org` → `2604:cac0:a104:d::3`
(exit 0); Python `getaddrinfo` returns A `209.126.35.79`. `getent -s resolve` exit 0 while
`getent -s dns` exit 2, and `/etc/nsswitch.conf:11` lists `resolve` before `dns`; the path is the
AF_UNIX socket `/run/systemd/resolve/io.systemd.Resolve`, which a network namespace does not
isolate. The same resolution succeeds inside `bwrap --unshare-net` and
`systemd-run --user -p PrivateNetwork=yes` (both `getent` exit 0).
Masking fixes it: `mount -t tmpfs tmpfs /run/systemd/resolve` (unshare, rc 0),
`--tmpfs /run/systemd/resolve` (bwrap), `-p InaccessiblePaths=/run/systemd/resolve` (systemd) →
`getent` exit 2 in all three. [Inference] an unmasked resolver is also an outbound DNS query
channel (exfiltration) even though IP sockets are unreachable.

**Other AF_UNIX services survive the netns** (observation):
- Docker socket `/var/run/docker.sock`, mode `660 root:docker`. Inside `bwrap --unshare-all` it
  displays as `660 65534 65534` (host root/docker unmapped), yet `id -G` prints `1000 65534` and a
  Python `connect()` prints `SOCK_CONNECTED`; same result inside `systemd-run`. Unmapped
  supplementary groups are *displayed* as 65534 but remain effective in the kernel credential
  (the docker group, 967, is not in the printed list, yet the 660 socket accepts the connection).
  [Inference] docker-group access is host-root-equivalent control; the sandboxes do not remove it.
- Session bus `/run/user/1000/bus` is reachable through `--ro-bind / /`. From inside both the
  bwrap sandbox and the unshare sandbox, `systemd-run --user --pipe --wait /bin/sh -c …` started a
  unit **outside** the sandbox: output `OUTSIDE_OK`, `uid -u` 1000, `ip -o link | wc -l` = 3
  (host interfaces), `test -w /home/vgpnk` = yes. So the sandbox is not a boundary against a
  payload able to spawn processes. (Observation; the units were trivial and exited.)

`systemd-run --user` needs the session bus environment: with
`env -u DBUS_SESSION_BUS_ADDRESS -u XDG_RUNTIME_DIR`, it prints
`Failed to connect to user scope bus via local transport …` and exits **1**. This shell provides
`XDG_RUNTIME_DIR=/run/user/1000` and `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus`.

## 4. Read-only root — construction and enforcement (observation)

`findmnt` shows `/` = btrfs `subvol=/@`, with **separate mounts** `/proc /sys /dev /run
/run/user/1000 /home /var/cache/pacman/pkg /var/log /boot /tmp /fast`. Therefore remounting only
`/` is insufficient: `/tmp` and `/home` (hence the lane) stay writable — verified: after
`mount -o remount,bind,ro /`, `/usr/x` was EROFS but `/tmp/x` succeeded.

**unshare recipe that works** (Order A — bind the work dir *first*, then remount every mount ro):
```
unshare --user --map-root-user --net --mount sh -c '
  mount --bind "$W" /tmp/kr20-work
  for t in $(findmnt -R -n -r -o TARGET /); do
    [ "$t" = /tmp/kr20-work ] && continue
    mount -o remount,bind,ro "$t"
  done
  mount -t tmpfs tmpfs /run/systemd/resolve
  …'
```
Observed: `/usr /etc /home /tmp /run/user/1000 /dev/shm` all `Read-only file system`;
`/tmp/kr20-work` writable; `python3 -I -B` on a script in the work dir prints 42 (rc 0);
`getent` exit 2; TCP unreachable; inner `exit 9` → outer rc **9**.
Order B (remount ro first, then create the mountpoint) fails: `mkdir: … Read-only file system`,
`mount --bind` rc 32. The carve-out must exist before the remount pass.

**bwrap** needs no recipe: `--unshare-all --ro-bind / / --bind "$W" "$W" --dev /dev --proc /proc
--tmpfs /run/systemd/resolve --die-with-parent` → `/usr`, host `/tmp`, `/run/user/1000` EROFS;
work dir writable; `python3 -I -B` 42; `getent` exit 2; TCP exit 1; inner `exit 9` → rc **9**.
`/dev/shm` stays writable but it is a fresh tmpfs inside the sandbox (under `--unshare-all`), not
the host one.

**systemd-run** needs `ReadOnlyPaths=/` plus a carve-out:
`-p PrivateNetwork=yes -p ReadOnlyPaths=/ -p ReadWritePaths=$W
-p InaccessiblePaths=/run/systemd/resolve` → `/usr`, `/home`, `/tmp` EROFS; `$W` writable;
`python3 -I -B` 42; `getent` exit 2; TCP exit 1; inner `exit 9` → **exit 9**.
Trap: adding `-p PrivateTmp=yes` while `ReadWritePaths` points under `/tmp` makes the unit fail to
start: `Main processes terminated with: code=exited, status=226/NAMESPACE`, `systemd-run` exit 226
(its private `/tmp` no longer contains the path).

**Enforcement against the payload differs** — this decides which primitive is a real boundary:
- `unshare --map-root-user`: payload `capsh --print` → `Current: =ep` (CAP_SYS_ADMIN effective in
  the userns). It ran `mount -o remount,bind,rw /tmp` → rc 0, then wrote `/tmp/...` → rc 0;
  it ran `umount /run/systemd/resolve` → rc 0 and DNS resolved again (`getent` rc 0). The
  read-only root and the resolver mask are **advisory** for the payload. Host-root-owned paths
  still refuse (EACCES) because userns root maps to the caller, but user-owned paths become
  writable again after the remount.
- `bwrap`: `capsh --print` → `Current: =` and **empty** bounding set. `mount -o remount,bind,rw /`
  rc 1, `umount /run/systemd/resolve` rc 32 (`must be superuser to unmount`), `mount -t tmpfs …`
  rc 32; mask held (`getent` rc 2). Enforced.
- `systemd-run` (user unit): `Current: =`; `mount`/`umount` answer `must be superuser`; mask held.
  Enforced. (My quoting did not expand the `$?` literals there; the refusal messages are the
  evidence.)

Identity inside: bwrap/`systemd-run` run `uid 1000` in a user namespace (systemd `uid_map`
`1000 1000 1`); host root-owned inodes show as `65534` inside bwrap (`/usr/bin/sudo`,
docker socket), so host root is not mapped. `unshare --map-root-user` shows `uid=0` but that
root is the caller. `sudo -n` rc **1** in all three (setuid root unmapped / no_new_privs).
`bwrap --dev /dev` changes the *displayed* map to `1000 0 1` versus `1000 1000 1` without
`--dev`; host root still displays 65534 and `id -u` is 1000 — [inference] an intermediate
bwrap namespace, not host root.

Namespaces: `bwrap --unshare-all` gives new user/net/mnt/pid/ipc/uts/cgroup (all inodes differ
from host). `unshare --user --map-root-user --net --mount` gives new user/net/mnt only;
pid/ipc/uts/cgroup inodes equal the host's (host `/proc` view, shared IPC/UTS/hostname).
`timeout 2 unshare … sleep 10` → rc 124 (bounded); `unshare --kill-child` is available in
util-linux 2.42.4 and implies `--fork`.

## 5. Verdict — which give network isolation and read-only root for an unprivileged user

| Primitive (uid 1000) | IP network isolated | AF_UNIX/socket isolation | Read-only root | Enforced against payload | Exit-code propagation |
|---|---|---|---|---|---|
| `unshare --user --map-root-user --net --mount` | **yes** (TCP/UDP unreachable) | **no** (resolved, docker, user bus) | **only via the §4 recipe**; not by the base command | **no** (payload has CAP_SYS_ADMIN; remount/umount succeed) | yes (9, 3 observed) |
| `bwrap --unshare-all --ro-bind / / --bind W W` | **yes** | **no** (same sockets; mask resolver) | **yes** (`--ro-bind`) | **yes** (no caps; remount/umount refused) | yes (9, 3 observed) |
| `systemd-run --user -p PrivateNetwork=yes -p ReadOnlyPaths=/ -p ReadWritePaths=W` | **yes** | **no** (same sockets; `InaccessiblePaths` mask) | **yes** | **yes** (no effective caps) | yes (7, 9 observed); start failure 1; namespace failure 226 |
| `firejail`, `nsjail` | absent | — | — | — | — |

Direct answer to the assigned question: **bwrap (installed) and `systemd-run --user` give both IP
network isolation and a read-only root for this unprivileged user, and both enforce them against
the payload; `unshare` gives IP isolation from the base command but read-only root only through the
multi-mount remount recipe, and that recipe is reversible by the payload because
`--map-root-user` grants CAP_SYS_ADMIN in the sandbox.** None of the three isolates AF_UNIX, so
DNS must be masked and the docker socket/session bus remain reachable.

## 6. Calibration notes for D6b implementation and selftests

- `net_refused` should assert a *connection* failure (TCP connect or UDP send → ENETUNREACH), not
  `getaddrinfo`: DNS resolves inside the netns via systemd-resolved (observed), so a
  `getent`-based test would pass while the network is still open in the only sense that matters
  for sockets. If a DNS assertion is wanted, mask `/run/systemd/resolve` first.
- `write_outside_refused` should attempt a real `open(O_CREAT)`/write outside the work dir. Inside
  a userns, `id -G` and ownership displays map unmapped groups/owners to 65534 while the kernel
  credential still holds them (docker-socket connect proves it); `test -w` agreed with the real
  access in my probes, but the printed `id`/`ls -n` output is misleading.
- Carve-out order: bind the work dir into the mount namespace **before** the read-only remount
  pass (Order A); a later `mkdir`/bind in a ro mount fails (rc 32 observed).
- Distinguish systemd-run's three failure shapes: child exit N → N; missing executable → 1; unit
  namespace setup failure → 226/NAMESPACE. `--pipe --wait` is required to get any of them.
- `--die-with-parent` (bwrap) and `timeout` (rc 124) bounded all probes; `unshare --kill-child`
  is available for the unshare path.
- `bwrap --unshare-all` also drops capabilities; if the contract keeps "use unshare or
  systemd-run" (contract.md:60), the unshare recipe above is the only one that satisfies
  `write_outside_refused` against accidental writes, but not against a payload that remounts.
  The L1 should decide whether the fixed-interface wording may use the installed bwrap.

## 7. Residual unknowns / limits

- Docker was only `connect()`ed, never used to start a container; docker-group ⇒ host-root is
  [inference], not exercised.
- bwrap's `--dev` uid_map display (`1000 0 1`) was not resolved beyond the display facts
  (id 1000, host root 65534, no caps); mechanism labelled inference.
- No seccomp/landlock/cgroup (CPU, memory, PID) or signal isolation tested; no PID-namespace
  behavior tested for `unshare` (it shares the host pidns).
- All probes are one host/revision (`7.2.11-arch1-1`, util-linux 2.42.4, bubblewrap 0.13.1,
  systemd 262); no ARM or other-kernel generalization.
- Transient `systemd-run` units used for the escape/exit probes exited immediately; no host
  service was restarted or reconfigured. Probe files were created only under `mktemp -d`
  (`/tmp`, `/run/user/1000`) and removed; one stray `/home/vgpnk/.kr20-x` created by the
  `ProtectSystem=strict` check was deleted in the same session. No installs.
