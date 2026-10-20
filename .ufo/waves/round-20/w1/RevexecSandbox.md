# RevexecSandbox-2 — D6b

## Result

- **Observation — implementation:** the patch adds `.ufo/waves/round-20/tools/revexec.py`; it reads only revision blobs, validates paths, and runs Python through transient `systemd-run` with `PrivateNetwork=yes`, `ProtectSystem=strict`, `ReadWritePaths=<workdir>`, and additional namespace/kernel/device restrictions. The child receives a cleared environment; extracted files and the child workspace are removed on exit. See `tools/revexec.py:6-11,91-112,115-183,313-341`.
- **Observation — required selftest:** `CASE write_outside_refused: PASS`, `CASE net_refused: PASS`, `CASE runs_ok: PASS`; exact last line `SELFTEST: CLEAN cases=3`; exit code `0`. Tests include a listener opened outside the sandbox and importing an `--extra` blob. See `tools/revexec.py:196-310`.
- **Observation — host probes:** the unshare user/net/mount namespace starts, but `mount --bind / /` fails with exit 32, so it was not selected. The tested user `systemd-run` path succeeds; `systemd-run --version` reports systemd 262. Selftest passed using the implementation's stricter transient-unit properties.
- **Observation — residual trust:** same uid, kernel bugs, and root remain outside the security claim, as documented at `tools/revexec.py:8-11`. No tools were installed or updated.
- **Observation — patch:** `/tmp/kr20-RevexecSandbox-2` is based at `14f0260ad319ecc26994381b2415d5a999003375`; cached stat: `.ufo/waves/round-20/tools/revexec.py | 345 +++++++++++++++++++++++++++++++++++`, `1 file changed, 345 insertions(+)`. Patch: `.ufo/waves/round-20/w1/patches/RevexecSandbox-2.patch`.

## Commands and exits

- `unshare --user --map-root-user --net --mount sh -c 'mount --make-rprivate / && mount --bind / / && mount -o remount,ro,bind / && mount -o remount,rw,bind / && printf "UNSHARE_PROBE_OK\\n"'` — exit `32`; output: `mount: /: wrong fs type, bad option, bad superblock on /, missing codepage or helper program, or other error.`
- `systemd-run --user --pipe --wait --collect -p PrivateNetwork=yes -p ProtectHome=read-only -- /usr/bin/python3 -I -B -c 'print("SYSTEMD_PROBE_OK")'` — exit `0`; output included `SYSTEMD_PROBE_OK` and `Finished with result: success`.
- `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-RevexecSandbox-2 && git -C /tmp/kr20-RevexecSandbox-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-RevexecSandbox-2 rev-parse HEAD` — exit `0`; observed base `14f0260ad319ecc26994381b2415d5a999003375`.
- `unshare --user --map-root-user --net --mount sh -c 'printf "NAMESPACE_OK uid="; id -u; mount --make-rprivate /; printf "PRIVATE_RC=%s\\n" "$?"; mount --bind / /; printf "BIND_RC=%s\\n" "$?"; mount -o remount,ro,bind /; printf "REMOUNT_RO_RC=%s\\n" "$?"'` — outer exit `0`; output: `NAMESPACE_OK uid=0`, `PRIVATE_RC=0`, bind mount diagnostic above, `BIND_RC=32`, `REMOUNT_RO_RC=0`.
- `git -C /tmp/kr20-RevexecSandbox-2 check-ignore -v .ufo/waves/round-20/tools/revexec.py; git -C /tmp/kr20-RevexecSandbox-2 status --short` — check-ignore exit `1` (not ignored), status exit `0` (empty); shell exit `0`.
- `systemd-run --version` — exit `0`; `systemd 262 (262-1-arch)`.
- `mkdir -p /tmp/kr20-RevexecSandbox-2/.ufo/waves/round-20/tools` — exit `0`.
- `python3 -I -B /tmp/kr20-RevexecSandbox-2/.ufo/waves/round-20/tools/revexec.py --selftest` — exit `0`; exact last line `SELFTEST: CLEAN cases=3`.
- `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches` — exit `0`; `git -C /tmp/kr20-RevexecSandbox-2 add -A` — exit `0`; `git -C /tmp/kr20-RevexecSandbox-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit `0`, stat above; `git -C /tmp/kr20-RevexecSandbox-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/RevexecSandbox-2.patch` — exit `0`.
