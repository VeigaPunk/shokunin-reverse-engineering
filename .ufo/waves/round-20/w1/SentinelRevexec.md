# SentinelRevexec — D6b security review

**Axes:** calibration (separate host facts from implementation claims), coverage (proc/fds/symlinks/environment/network), depth (concrete escape paths and selftest assertions).

## Scope and observations

**Observation:** `.ufo/waves/round-20/tools/revexec.py` was absent when read and when checked again; no implementation was available for source-level review or selftest execution. The binding interface promises revision extraction to `mkdtemp`, `python3 -I -B` in a sandbox, network denial, and outside-workdir write refusal (`.ufo/waves/round-20/contract.md:58-61`). The executor brief requires user/mount/net isolation and specifies a sibling-write probe, host-loopback listener probe, and happy path (`.ufo/waves/round-20/gen-wave1.py:128-134`). Findings below about implementation paths are therefore explicitly conditional, not confirmed defects.

All probes ran with `cwd` in a `tempfile.mkdtemp()` directory under `/tmp`; each scratch directory was removed afterward.

- **Command (namespace capability/proc view):** `unshare --user --map-root-user --net --mount --fork sh -c 'printf "child uid="; id -u; printf "uid_map="; cat /proc/self/uid_map; for n in user mnt net pid; do printf "child ns %s=" "$n"; readlink "/proc/self/ns/$n"; done; printf "proc_net_dev\n"; cat /proc/net/dev; printf "proc_pid1_comm="; cat /proc/1/comm'` — **exit 0**. Host uid was 1000; child uid was 0 with `uid_map=0 1000 1`; user/mount/net namespace IDs changed, but child and host PID namespace IDs were both `pid:[4026531836]`. Child `/proc/net/dev` listed only `lo`; `/proc/1/comm` returned `systemd`.
- **Command (direct host-loopback test):** `unshare --user --map-root-user --net --mount --fork python3 -I -B -c 'import socket,sys; s=socket.socket(); s.settimeout(1); rc=s.connect_ex(("127.0.0.1",54493)); print("connect_ex=%d"%rc); sys.exit(1 if rc==0 else 0)'` — **exit 0**, `connect_ex=101`. The probe had opened a listener on host `127.0.0.1:54493` only for this test. This shows the tested unshare command could not connect to that host listener; it does not test revexec.
- **Command (isolated Python environment):** `python3 -I -B -c 'import os; print(os.environ.get("KR20_REVEXEC_PROBE"))'` — **exit 0**, printed `VISIBLE_TEST_MARKER`. The probe driver explicitly supplied that harmless variable. `-I` does not clear arbitrary inherited environment variables.
- **Command:** `bwrap --version` — **exit 0**, `bubblewrap 0.13.1` (`/usr/bin/bwrap`). This contradicts the host assumption “bwrap is NOT installed” in `.ufo/waves/round-20/contract.md:60` and `.ufo/waves/round-20/gen-wave1.py:128-130`; I did not use bwrap or assess it as a replacement.

## Findings

### High — no implementation available; security claim unreviewable
- **Exploit path:** unknown; the required code is absent, so extraction, mount setup, subprocess options, fallback behavior, and selftests cannot be inspected.
- **Evidence:** target read/check returned “not found”; D6b requirements are at `.ufo/waves/round-20/contract.md:58-61` and `.ufo/waves/round-20/gen-wave1.py:128-134`.
- **Impact:** no evidence supports either a pass or a code-level exploit conclusion. A green named selftest cannot establish the promised boundary without reviewing the implementation.
- **Smallest remediation:** make the exact `revexec.py` implementation available at the contracted path, then review and run its selftests; do not claim D6b security closure from interface text alone.

### Medium — `/proc` remains in the host PID namespace (conditional on using only the specified three namespaces)
- **Exploit path (inference):** code running in the user/mount/net namespaces can still enumerate host PID entries through inherited `/proc`; same-UID process details or `/proc/<pid>/fd` may be accessible subject to kernel ptrace/proc permissions. A mount namespace alone does not create a private PID view.
- **Evidence:** the harmless unshare probe above observed the same PID namespace inode and `systemd` at `/proc/1/comm`; the assigned invocation names only user/net/mount namespaces (`gen-wave1.py:129-131`).
- **Impact:** host process metadata and, where permissions allow, process descriptors/environment may be exposed; this is not proof of arbitrary host access.
- **Smallest remediation:** if host-process isolation is intended, add a PID namespace and mount a fresh `/proc` inside it; otherwise document `/proc` visibility as residual trust and do not imply it is hidden.

### High — writable open descriptors can bypass read-only path mounts (conditional)
- **Exploit path (inference):** a child with an inherited writable fd can write through it even after its pathname's filesystem is remounted read-only; with host `/proc` visible, an accessible same-UID parent `/proc/<pid>/fd/<n>` is another possible route. This bypasses a path-only `write_outside_refused` check.
- **Evidence:** D6b calls for outside writes to be refused (`contract.md:59-61`) and the brief proposes read-only mounts except for workdir (`gen-wave1.py:130-132`); no implementation was present to establish fd closure. The proc exposure is observed above; access to a particular parent fd is not tested.
- **Impact:** any qualifying writable fd can mutate a file outside the workdir notwithstanding read-only mounts.
- **Smallest remediation:** close all non-stdio descriptors before exec (`close_fds=True`, no `pass_fds`/inheritable fds), avoid retaining writable host fds, and restrict host `/proc` visibility. Selftest with a controlled writable fd to a scratch sibling and assert the marker is unchanged.

### High — extracted symlinks can redirect execution or writes (conditional)
- **Exploit path (inference):** if extraction preserves a Git symlink and the runner invokes `workdir/entry` by pathname, an absolute or escaping relative target can execute code outside the selected revision; an extractor that follows symlinked parents can also write outside its extraction root before sandboxing.
- **Evidence:** revision blobs are extracted before execution (`contract.md:58-60`); implementation and extraction semantics are unavailable.
- **Impact:** revision pinning and sandbox assumptions can be bypassed, including executing bytes not authenticated as the selected entry blob.
- **Smallest remediation:** reject symlink entries for `--entry`/`--extra`, or materialize verified Git blob bytes as regular files using no-follow operations; validate resolved paths remain under the extraction root. Add relative- and absolute-symlink fixtures whose targets are harmless markers in the temp parent; assert refusal before execution and unchanged markers.

### Medium — `-I -B` does not sanitize the environment (conditional)
- **Exploit path (inference):** if revexec inherits its environment, extracted code can read arbitrary non-Python variables and print their values to captured stdout; network isolation does not prevent that output channel.
- **Evidence:** the harmless environment probe above preserved `KR20_REVEXEC_PROBE` with `python3 -I -B`; D6b specifies those interpreter flags (`contract.md:58-60`).
- **Impact:** inherited credentials/configuration can leak to the supervising checker or influence code behavior.
- **Smallest remediation:** launch with a minimal explicit environment allowlist and no secrets. Selftest with a canary parent variable and prove it is absent inside the target.

## Selftest acceptance bar

`write_outside_refused` must assert an outside scratch marker is unchanged after attempts via `..`, absolute/symlinked paths, and a controlled inherited-fd/proc-fd route—not merely check a nonzero child exit. `net_refused` must use a real host-loopback listener, as required by `.ufo/waves/round-20/gen-wave1.py:132-134`; the direct unshare probe above passed but does not validate revexec. `runs_ok` must show the selected revision's regular-file entry executes with expected output/status. All namespace/mount setup failures must fail closed (never execute the target unsandboxed); assert this explicitly. Also test malformed/escaping `--entry`/`--extra` paths, symlink refusal, environment canary removal, and scratch cleanup, keeping all fixtures under `mkdtemp()`.

**Overall:** host unprivileged user/mount/net namespaces work on this host, and the tested network namespace refused a host-loopback connection. D6b implementation security remains **unverified** because the target source was unavailable. No tools were installed or updated.