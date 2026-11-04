# The kernel's record: a producer-independent environment witness, and the lying-shim control

source: S277 — Linux man-pages 6.19, proc_pid_cmdline(5), "Think of this file as the command line that the process wants you to see." (opened 2026-11-04, https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html#DESCRIPTION); S275 — proc_pid_environ(5), "This file contains the initial environment that was set when the currently executing program was started via execve(2)." (opened 2026-11-04, https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html#DESCRIPTION).
verified-at: 2026-11-04 — measured at lane `kaidoku-shokunin` revision `d36c6ee00122e9c991d7c8efc2e179dc0a10d9ed`; receipts `.ufo/waves/round-73/l1/scores/c1-at-landing.json` (12 of 12, `A12_kernel_witness` true), `.ufo/waves/round-73/pre/c1-at-base.json` (8 of 12, A2/A10/A11/A12 false), `.ufo/waves/round-73/pre/c1-at-base-r72probe.json` (the round-72 probe: 11 arms, no A12).
recheck: re-run the frozen R73-C1 command in `plans/round-73-claims.md` (`python3 -I -B tools/round-73/seam-probe.py … --json-out …`) and read `A12_kernel_witness.observed`: the genuine kernel samples must be exactly HOME/LANG/PATH/TMPDIR with `canary_present false` and both containment flags true, the forged child dumps keys-exact and canary-free, and at least one forged kernel sample dirty.

## What the channel is

A11 (round 72) asks each shim what environment it received: the shim writes its own
`/proc/self/environ` bytes and the checker writes its own child log. Both are **claims by
the producer** — a wrapper that writes a plausible four-key dump while running under the
caller's 275-key environment satisfies every clause. Round 72 recorded that as a class
boundary (`corpus/knowledge/2026-11-04-r72-checker-env-capsule.md`, Limits), not as a
measured class.

A12 (`tools/round-73/seam-probe.py`) reads the same fact from the other side. While the
checker runs, the probe polls `/proc`, selects a process whose argv names the run's shim
directory **and whose parent chain reaches a pid the arm itself started**, and reads
`/proc/<pid>/environ` — the kernel's record of what that process was started with. Two
guards were added after the round-73 wave: the ancestry check closes a decoy process on
the host being sampled instead of the child (CriticClaims, SentinelScope S1), and the
record stores key names plus two containment booleans, never HOME/TMPDIR values
(QUALITY row 128).

## The control that falsifies the arm

The arm is true only when its own forged world is convicted:

| sub-run | producer | child-side dump | kernel record | required |
|---|---|---|---|---|
| genuine | the route's checker (`build_child_env`) | four keys, no canary | four keys, no canary, HOME/TMPDIR under the run root | clean |
| forged | a fixture producer that inherits the caller env | four keys, no canary (the lie) | 275 keys, canary present | dirty |

Measured at `d36c6ee0`: genuine `git`/`readelf` samples `["HOME","LANG","PATH","TMPDIR"]`,
`canary_present false`, `home_under true`, `tmpdir_under true`; forged samples 275 keys
with the canary; `forged_detected true`, `lie_clean true`, `genuine_ok true`; the probe
reports 12 of 12 arms.

## Limits (what a wrapper can still do)

- **argv is what the process wants you to see** (S277). Selection by argv is therefore
  producer-writable: a wrapper that names its process something else is simply not
  sampled, and the arm fails closed (a missing class, not a green one).
- **`/proc/pid/environ` is the initial environment**, not the live one (S275): a child's
  `putenv` scrubbing is *not* reflected, which helps the observer, not the attacker. The
  page also records that a process may relocate the region with
  `PR_SET_MM_ENV_START`; that is a privileged operation (`CAP_SYS_RESOURCE`), so the
  channel raises the cost of a forged environment from "write a file" to "hold a
  capability".
- The witness covers the processes the poller samples during their 0.4 s shim window; a
  child that execs and exits faster than the poll interval is missed (fail-closed, and
  the shim it instruments is the lane's own).
- This is not wrapper authentication, not a descendant census, and not evidence for
  another operating system.

## Receipts

- `.ufo/waves/round-73/l1/scores/c1-at-landing.json` — 12/12, A12 observation with both
  sub-runs.
- `.ufo/waves/round-73/pre/c1-at-base.json` — the same probe against the round-72 route:
  8/12 (A2/A10/A11/A12 false; the route receipt is bound to the round-73 producer).
- `.ufo/waves/round-73/pre/c1-at-base-r72probe.json` — the round-72 probe at the same
  revision: 11 arms, 11 passed, no A12 (the comparator the freeze erratum names).
- `tools/round-73/seam-probe.py --selftest` — 14 cases, `a12-kernel-cases` binds the
  verdict, the kinship guard is exercised by the arm itself.
