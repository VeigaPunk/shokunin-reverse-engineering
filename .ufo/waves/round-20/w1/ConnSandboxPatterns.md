# ConnSandboxPatterns — OS sandbox of lane checkers

Seat: KaidokuR20.ConnSandboxPatterns-2. Read-only. No installs. Clock of the host probe: `date -Iseconds` → `2026-10-20T17:51:53-03:00` (exit 0).

Axes: calibration (what ran, against the D6b premise), coverage (unshare / systemd-run / bwrap / firejail across sibling tools and lessons), depth (path:line, exits, the failure that looks like success).

Search: path-scoped, glob `**/*.{py,md,sh}`. Fleet-root search hides lanes: `/home/vgpnk/Projects/shokunin/.gitignore:1` is `*-shokunin/`. Lore hits are the substring inside "unshared", not the binary (`lore-shokunin/.ufo/waves/round-98/seats/V45-byte-prefix-2.md:95`).

## Host, this seat (observation)

| command | result | exit |
|---|---|---|
| `command -v unshare` | `/usr/bin/unshare` | 0 |
| `command -v bwrap` | `/usr/bin/bwrap` | 0 |
| `command -v firejail` | empty | 1 |
| `command -v systemd-run` | `/usr/bin/systemd-run` | 0 |
| `command -v nsjail` | empty | 1 |
| `unshare --version` | `unshare from util-linux 2.42.4` | 0 |
| `systemd-run --version` | `systemd 262 (262-1-arch)` | 0 |
| `bwrap --version` | `bubblewrap 0.13.1` | 0 |
| `pacman -Q bubblewrap` | `bubblewrap 0.13.1-1` | 0 |
| `pacman -Q firejail` | `error: package 'firejail' was not found` | 1 |
| `pacman -Q util-linux` | `util-linux 2.42.4-1` | 0 |
| `pacman -Q systemd` | `systemd 262-1` | 0 |
| `cat /proc/sys/kernel/unprivileged_userns_clone` | `1` | 0 |
| `cat /proc/sys/user/max_user_namespaces` | `122865` | 0 |

This seat did not re-run a bwrap jail or an `unshare --mount` child. Jail outcomes below are sibling transcripts.

## Contradiction (do not smooth)

`contract.md:60` says `bwrap is NOT installed` and points D6b at `unshare` or `systemd-run --user`. Observation now: `/usr/bin/bwrap` is bubblewrap 0.13.1-1. Kotodama's protocol still says "this host: bwrap 0.12.0" (`kotodama-shokunin/reports/round-39/calib/Ca01-protocol.md:271-272`). Kaidoku's 0.11.2→0.12.0 notes are a version-diff of the binary, not a checker jail (`kaidoku-shokunin/corpus/knowledge/2026-10-13-r2-version-diff-compare.md:18`).

## What jailed a checker (bwrap)

The only pattern with both D6b properties — net namespace off, and a write outside the work dir refused — is bwrap 0.13.1.

- Envelope in the ruler: `tameshi-shokunin/.ufo/evidence/round-18/defect-probes.py:4-7` and the argv at `:191-205` (`--ro-bind / /`, `--bind` of the work dir onto itself and onto `/mnt`, `--unshare-pid`, `--unshare-net`, `--die-with-parent`). Launch failure is `cannot launch bwrap` (`:239`). Lesson admits that envelope (`corpus/lessons/round-18.md:27`, G10). Limit, same lesson's knowledge: the envelope sandboxes the probes, not a proof of containment for the tools under test (`corpus/knowledge/guard-kill-closure.md:129`).
- Version match with this host: `bwrap --version` exit 0, `bubblewrap 0.13.1` (`tameshi-shokunin/.ufo/waves/round-18/w1/X06DispositionGuards.md:24`).
- Write refusal, pasted in the cold-read receipt: `[23] bwrap read-only: touch into fleet root, mado-shokunin, tameshi-shokunin (Read-only file system, exit 1 each) + scratch (exit 0) -> exit 0`. Same receipt: regression under `bwrap` `--unshare-net` exit 0; `mado-verify.sh --selftest` exit 0 (`tameshi-shokunin/.ufo/waves/round-18/w2/CR14.md:126`, commands [16], [21], [23]).
- Destination must already exist on the ro root. Souji's first wrapper, `--ro-bind / /` plus `--ro-bind … /mutation-sources`, exit 1, stderr `bwrap: Can't create file /mutation-sources: Read-only file system`, before Python (`souji-shokunin/.ufo/waves/round-17/w2/MutateGateExact.md:259-266`). The corrected wrapper binds over the existing path `/var/tmp/souji-r17-MutateGateExact` and the pristine `--selftest` exits 0 (`:283-284`). `command -v` in that seat: `/usr/bin/bwrap` and `/usr/bin/unshare` (`:250-254`).
- Kotodama Tier A is the same shape for a validator, not a new mechanism: `bwrap --ro-bind / / --bind "$S/clone" "$ROOT" … --tmpfs /tmp` (`Ca01-protocol.md:152-170`). Annex: `--check` under Tier A `rc=0` (`:288-289`). The protocol's own limit: the bind "is path-escape containment for the replayed runner, not a security sandbox" (`:262-264`). Tier B is the no-bwrap fallback and forbids publish mode because a non-chdir write reaches the live tree (`:189-215`). The counted Ca02 replay was not that bwrap command: it rewrote `ROOT` to `os.getcwd()` and ran `python3 -B` in a worktree, rc=0 (`Ca02-replay-verify.md:29-42`). Ca02 cites an earlier bwrap C/D run (`:108`, `:160-161`) and says the protocol file did not exist yet (`:134-140`). Fleet summary still calls the landed method bwrap (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/kotodama.md:25-28`).

Round-16 tameshi rejected swapping the pre-registered suite for bwrap (`corpus/lessons/round-16.md:28`, G11). Round-16 also showed the unsandboxed checker: a mutant `fs.writeFileSync` wrote `/tmp/tameshi-r16w2-RX7-escape-marker` (exit 0), and `grep` of `bwrap|unshare|firejail|nsjail|seccomp` in `tools/mutate-and-run.sh` found none (`tameshi-shokunin/.ufo/waves/round-16/w3/RX7.md:73-76`).

## unshare — works for a tmpfs or a net ns, not as a bwrap substitute

- Checker selftest forge: `unshare --user --map-root-user --mount --propagation private` mounts a tmpfs and runs the gate in that child (`chousa-shokunin/tools/research-gate.sh:4636-4658`). Skip if userns+mount is absent (`:4643`, `:4668-4671`). Receipt: cases 103-106 ok, `RESEARCH_GATE_SELFTEST: PASS (106 cases, 0 skipped)` (`chousa-shokunin/corpus/evidence/mount-r14-20261019T132025Z-selftest.log:103-107`). Knowledge: tmpfs inside that ns is the measured bypass/fix (`corpus/knowledge/mount-alias-r14.md:14-17`).
- Recorded claim, no argv transcript found in that evidence log: repo binds inside the ns refused, rc=2 (`chousa-shokunin/.ufo/reports/round-14/chousa.md:16`; comment at `tools/research-gate.sh:4631-4632`). Inference: `mount --bind` of the repo is the refused operation; the passing cases use `mount -t tmpfs`, which the script does run (`:4641`, `:4654`).
- The child does not remount `/` read-only (`research-gate.sh:4653-4658`). Inference: host paths other than the tmpfs stay writable. That is not `write_outside_refused`.
- Net, unprivileged, a real gate: `unshare -rn … run_gate.sh` → `CHECK 2 BLOCKED (network)`, `EXIT=2` (`game-dev-3d-shokunin/reports/round-103/r103-connector.md:155-164`). Same lane, same round, another seat: "Network namespace / `unshare` — not available on this host" with no failing command (`reports/round-103/gate/a4-attack.md:217`). The connector transcript contradicts that sentence.
- Net, privileged: `sudo -n unshare -n … bash tools/test-snapshot.sh` → exit 0, `RESULT pass=30 fail=0` (`kama-shokunin/.ufo/waves/round-16/falsify/advice/ReviewTestSnapshotDiff.md:24`). Not the unprivileged form.
- Hide a host dir: `unshare -rm` tmpfs over `.ufo` moved a clone from 0 dead to 24/24 dead (`kotoba-shokunin/corpus/knowledge/independent-verification-round12.md:110-114`).
- Private `/tmp` for an exporter, not a checker jail: recipe at `game-dev-2d-shokunin/reports/round-101/r101-ver16.md:32`; `:99` says "expect rc=0" and does not paste that command's exit. Tab's harness does not record its own net witness: a Sentinel `unshare -rn` saw only `lo` (`tabi-shokunin/corpus/knowledge/harness-hardening-round-18.md:62`).

## systemd-run — lifetime and memcg, not a write/net jail

`systemd-run --user --scope` contained a Ghidra run at its own 7G cap and then died with the launcher (`kaidoku-shokunin/corpus/lessons/2026-10-18-caller-independent-services.md:8-13`; `SKILL.md:219-224`). The service form without `--scope` is what rounds 6-7 used (`:14-17`). LOG: both r6 runs were `systemd-run --user` services (`kaidoku-shokunin/LOG.md:1249-1250`). Mori cites those units as OOM at their own cap (`mori-shokunin/.ufo/waves/round-14/build/NoHarmReview.md:23`). No sibling lesson shows `systemd-run` refusing a write outside a work dir or dropping a checker's network. Tsukuroi's `systemd-run -p CapabilityBoundingSet=CAP_SYS_ADMIN` line is a predicted probe (`tsukuroi-shokunin/corpus/knowledge/snapper-eacces-mechanism.md:26`). Mado only denylists the binary (`mado-shokunin/tools/mado-tripwire.py:231`, `:1079-1080`).

## firejail — absent, unused

Not installed (table above). Mentions are a wrapper denylist (`mado-shokunin/.ufo/waves/round-16/w1/reports/ExecBasename.md:50-52`), a future-hardening aside that says probes are not OS-sandboxed (`kotodama-shokunin/reports/round-47/op/O02-probe-registry.md:242`), and the round-16 grep that found no firejail in the tameshi mutator (`RX7.md:76`). `gen-wave1.py:325` and `:520` are this wave's prompts, not a run.

No matches for the four tokens in tools or lessons of kumitate, kengaku, kasegi, kake, kagi, audio, revenger, tameshi-shokukin.

## Move (one)

Point D6b `revexec` at the installed bwrap 0.13.1 envelope — `defect-probes.py:191-205` and the souji argv that exited 0 (`MutateGateExact.md:283`) — and strike `contract.md:60`'s "bwrap is NOT installed". Bind the mkdtemp directory onto itself (it already exists). Do not invent a new mount point (`/mutation-sources` failed closed, exit 1). Do not implement the jail as `unshare … mount --bind` of the repo (recorded rc=2) or as `systemd-run` (no write/net refusal in the lessons). If bwrap is refused anyway, the chousa child can only be a tmpfs forge, and write refusal still needs a remount-ro that no sibling checker showed.

Risks: `--ro-bind / /` still exposes the host read-only (kotodama `:262-264`; tameshi `:129`). An unshare port that only adds a tmpfs fails open on writes outside that tmpfs (inference from `research-gate.sh:4653-4658`). A new bwrap destination fails closed before `runs_ok`. Kotodama's `0.12.0` pin does not match this host's 0.13.1.

Verification: the host table above. Sibling exits are quoted from the cited lines, not re-run.
