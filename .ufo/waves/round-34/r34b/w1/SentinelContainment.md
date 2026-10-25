# SentinelContainment — containment audit of the R34-C2 frozen bytes

Seat: `L1Kaidoku34-2.SentinelContainment`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
(jj-colocated, read-only for this seat). Frozen surface audited: **c79bbe7b0959132b9873ff3431cf5eb313b58b33**
(freeze commit, message `round-34: freeze R34-C2 pre-freeze shortcut-replay gate ...`). UTC window:
2026-10-25T07:18:46Z → 2026-10-25T07:21:35Z. Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w1/SentinelContainment/`.
No lane file was written except this report; no ELF carrier, fixture or reader was executed as a program of
interest; all probes ran on copies in scratch.

## 1. Bytes audited (are the audited bytes the frozen bytes?)

| Check | Command | Result |
|---|---|---|
| 26/26 declared pins match the working-copy bytes | `sha256sum` over the 26 `pins` in `.ufo/waves/round-34/r34b/claims.json` (python, 07:18:46Z) | `verified: 26  mismatched/absent: []` |
| Working copy == c79bbe7b for the instrument tree | `jj diff --from c79bbe7b --to @ --stat -- tools/round-34` | `0 files changed, 0 insertions(+), 0 deletions(-)` |
| Which files in `tools/round-34` are **not** pinned by C2 | find vs pin map | `elf-version-needs.py`, `freeze-integrity.py`, `version-needs-counter.py` (the inherited R34-C1 surface — correctly outside C2's pin set) |

So the containment questions below are asked of exactly the frozen bytes.

## 2. Findings table (pass/fail, line pointer each)

| # | Question | Verdict | Pointer / receipt |
|---|---|---|---|
| C1 | Can a **fixture** execute or spawn anything? | **PASS** | `tools/round-34/mini-fix/fixtures/*.mrec` are eight 512-byte static `MREC` record-chains (`build.py:1-11` format; `mini-counter.py:10` "Never executes fixtures; static bytes only"). Whole-file byte scan (`bash`, 07:19:51Z): **no `\x7fELF`, no `#!`, no ESC** in any fixture; zeta.mrec is the only one with a `0x04` byte, inside a value field. `file -b`: `data` for all eight. They are only ever `read_bytes()`d (`mini-counter.py:112`, `naive-counter.py:47`). |
| C2 | Are the **readers** capable of spawning anything beyond the counter's own subprocess call? | **PASS on committed content, FAIL on capability** | Content: the nine readers import only `json/sys/os/struct/re/hashlib` (complete inventory, 07:21:27Z) and contain **no** `subprocess`, `os.system`, `os.exec*`, `popen`, `eval`, `exec`, `ctypes`, `importlib`, `socket`, `urllib`. Capability: see §3.1 and §4.1 — they run as arbitrary Python at uid 1000. |
| C3 | Do the counters set a restricted env (`PATH`/`HOME`/`LANG`)? | **PASS (gate, C2 driver, red counter), PASS-WITH-NOTE (green counter)** | Gate: `replay-gate.py:79-81` `env={"PATH": "/usr/bin:/bin", "HOME": "/tmp", "LANG": "C"}`. C2 driver: `c2-shortcut-gate-counter.py:36-37` same three. Red: `naive-counter.py:48-50` same three. Green: `mini-counter.py:116-118` sets **only** `PATH` + `HOME` (HOME redirected into its own 0700 tempdir, `mini:109`) and omits `LANG` — an asymmetry with the other three, harmless here (all readers handle ASCII only). |
| C4 | Do the fixtures have mode 0644? | **PASS** | `find … -printf '%m'`: all eight `644`; `git ls-tree -r c79bbe7b` records `100644` for all eight. Owner `1000:1000` (vgpnk), no setuid/setgid bits (`find -perm /6000` empty), no file capabilities (`getcap -r` empty). Note: the nine **readers, both counters and `build.py` are `100755`**, committed as `100755`, with `#!/usr/bin/env python3` shebangs — executable directly and PATH-looked-up if ever invoked as a binary; nothing in the tree does that (all invocation is `python3 -I -B <path>`). |
| C5 | Is there any network access in the pinned instruments? | **PASS** | `grep -nE 'socket\|urllib\|http\|requests\|ftplib\|telnet\|smtplib\|asyncio\|curl\|wget\|connect(\|bind(\|listen('` over gate, C2 counter, both configs, `build.py`, `mini-counter.py`, `naive-counter.py`, all readers → only two hits, both **fixture data strings**: `build.py:30` `"libcurl.so.4"`, `label_replay_full.py:30` `"libcurl.so.4"`. No socket/HTTP import anywhere. |
| C6 | Is the pin surface enforced by the counted command? | **FAIL (material)** | `c2-shortcut-gate-counter.py` imports no `hashlib`, runs no `git`/`jj` (`grep -nE 'jj\|git\|rev-parse\|hashlib\|sha256'` → NO MATCH). It checks only **presence**: `c2:74` `gate_present = (root/args.gate).is_file()`, `c2:83-89` `pinned_input_absent`. The lane's own pin verifier refuses the C2 claims shape: `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/claims.json --rev c79bbe7b` → `freeze-integrity: ERROR schema code=instruments_missing … where=instruments`, **exit 3** (07:20:37Z), because `freeze-integrity.py:92-94` requires an `instruments` map while `r34b/claims.json` carries `claims[0].pins`. The same verifier is functional and CLEAN on the R34-C1 claims (`pins=21 … CLEAN freeze=54a87a51a865 rev=c79bbe7b`, **exit 0**, 07:20:37Z), so this is a shape mismatch, not a broken tool. |

## 3. Bounded probes actually run (command, exit code, UTC)

All probes use byte-identical copies in scratch: `gate-copy.py` sha256 `8fa94b23…1c7558` =
`tools/round-34/replay-gate.py`; `mini-root/mini-counter.py` sha256 `43ef669f…c4b52` =
`mini-fix/mini-counter.py`. Probe counters/readers are my own scratch files, not lane instruments, so no
lane reader ran.

### 3.1 Reader-subprocess environment (the question that matters)

`python3 -I -B mini-root/mini-counter.py --root mini-root --control-reader scratch/probe_reader.py`
(cwd = lane, 07:20:11Z) → **exit 1** (`matched=0`, my probe reader deliberately emits no records), and the probe
reader's own dump, written *outside* its temp workdir:

```json
{"env": {"PATH": "/usr/bin:/bin", "HOME": "/tmp/kaidoku-r34-mini-ohex7jot", "LC_CTYPE": "C.UTF-8"},
 "cwd": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "uid": 1000, "fd_count": 4,
 "fd_targets": {"0": "/dev/null", "1": "pipe:[…]", "2": "pipe:[…]"},
 "can_spawn_abs_binary": true, "can_read_lane_claims": true,
 "can_read_etc_shadow": "PermissionError", "can_write_outside_workdir": true,
 "umask_inherited": "0o22"}
```

Read: the reader sees exactly the env the counter sets (plus `LC_CTYPE`, see 3.3); it inherits the counter's
cwd (which under the gate is `--root`, i.e. the whole lane); it can `execve` `/bin/true`; it can read the lane's
`claims.json`; it can write **outside** its sandbox dir; `/etc/shadow` is denied only by ordinary Unix DAC.
`mini-counter.py:116` passes no `cwd=`, so a reader is not even chdir'd into its workdir — `HOME` is the only
redirect. This is the honest answer to "are readers capable of spawning": yes by capability, no by content.

### 3.2 Gate child environment

`python3 -I -B gate-copy.py --root probe-root --config probe-config.json` (07:19:51Z) → **exit 0**,
`REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=3 shortcuts_over_target=-`.
Child: `env = {PATH:/usr/bin:/bin, HOME:/tmp, LANG:C, LC_CTYPE:C.UTF-8}`, `cwd = --root`, `umask 0o22`,
`fd_count 4` (so `close_fds` is effective — no inherited descriptors), `sys.flags.isolated=1`,
`can_spawn_abs_binary=true`, `can_read_outside_root=true`, `af_inet_socket_created=true`.

### 3.3 The fourth env key is the child's, not the gate's

`env -i PATH=/usr/bin:/bin HOME=/tmp LANG=C /usr/bin/python3 -I -B -c 'print(dict(os.environ))'` (07:21:35Z,
exit 0) → `{"HOME","LANG","PATH","_","LC_CTYPE":"C.UTF-8"}`; adding `LC_ALL=C` → no `LC_CTYPE`. So CPython's
own PEP 538 locale coercion, at child startup, adds `LC_CTYPE`; the gate hands over exactly three keys. No
parent-env leak (no `LD_PRELOAD`, `PYTHONPATH`, `PYTHONSTARTUP`, `BASH_ENV` reach the child).

## 4. Residual risks, ranked, with exploit path and smallest remediation

**4.1 (highest) Reader code is untrusted-equivalent: no sandbox, only env scrubbing.** A reader is executed as
arbitrary Python at uid 1000 with no seccomp/namespace/rlimit/`preexec_fn` anywhere in the tree
(`grep close_fds|preexec_fn|resource\.|setrlimit|unshare|bwrap|firejail|seccomp` → NO MATCH). Path: a future
round adds (or a compromised author swaps in) a "shortcut reader" that, on first invocation, rewrites
`tools/round-34/mini-fix/expected.json` or `gate-config-mini.json` and exits 0. `test -w` (no write performed,
07:21:27Z) shows `expected.json`, `gate-config-mini.json`, `c2-shortcut-gate-counter.py` and `r34b/claims.json`
are **all writable by uid 1000**. The *current* run is unaffected — `mini-counter.py:106` loads `expected.json`
before any reader starts — but the **next** run would score against the tampered expectation and report CLEAN,
and §C6 means nothing would notice. Smallest remediation: run readers with `stdin=subprocess.DEVNULL` and
`cwd=<workdir>` in `mini-counter.py:116` / `naive-counter.py:48`, and (cheap, strong) have the C2 counter
re-hash its 26 pins before scoring, exiting 2 `pinned_input_changed` — that converts 4.1 from silent to loud.

**4.2 (material, provenance) The 26 C2 pins are declared but checked by no committed instrument** (§C6,
`freeze-integrity` exit 3 `instruments_missing`). Consequence: the production receipt
`.ufo/waves/round-34/r34b/after/c2-at-instruments.json` is *self-consistent*, not *self-verifying*; it also
records no uid, env, or instrument digests. `measured_revision` is caller-asserted — `c2:73` writes `args.rev`
into the receipt and the counter never touches VCS, so a dirty tree at any revision yields a receipt labelled
`c79bbe7b`. Smallest remediation: emit the C2 pins in the `{instruments: {...}}` shape `freeze-integrity.py`
accepts (a second file `r34b/claims-instruments.json` suffices) and add one line to the counting command:
`freeze-integrity.py --claims …/claims-instruments.json --rev c79bbe7b`.

**4.3 Config is trusted data executed verbatim.** `replay-gate.py:47-50` validates only that exactly one argv
element contains `{reader}`; `:76-81` then executes `config["counter"]["argv"]` with an unrestricted program
path, and `resolve()` (`:71-73`) accepts absolute and `..`-containing paths for the counter and every reader.
The configs themselves are safe (`gate-config-mini.json:6` pins `/usr/bin/python3` absolutely, so no PATH
hijack), but nothing in the gate keeps a future config honest. Same remediation family as 4.2 (hash the config)
— cheap, and it closes it.

**4.4 Asymmetric env on the gate's own mutant runs.** `replay-gate.py:266-268` spawns the three selftest
mutants **without** `env=`, unlike `:79-81`. It is only transitive scrubbing that keeps this benign: when the
C2 counter drives the gate (`c2:36-37`) the gate's own env is already the three-key set, so the mutants inherit
it too. A human running `python3 replay-gate.py --selftest` from a full shell hands the mutants the full
environment. [INFERENCE: from code, not probed with a canary.] One-line fix: pass the same `env=` literal at `:266`.

**4.5 Timeout arithmetic has no handler at the top.** Inner gate runs are `TIMEOUT=300` (`replay-gate.py:32`)
and the C2 driver allows `timeout=900` (`c2:36`) for **three** gate invocations (selftest, red, green) whose
worst case is exactly 900 s; `c2:36` has no `try/except subprocess.TimeoutExpired`, so a hung counter ends in an
uncaught traceback, exit 1, and **no receipt** rather than a typed `UNEVAILABLE`. [INFERENCE: arithmetic from
the two constants; not reproduced — a 5-minute hang is outside this wave's bounded-probe budget.] Readers
themselves are bounded at 60 s (`mini:118`, `naive:50`).

**4.6 stdin is inherited.** No `stdin=` argument exists in any instrument (`grep -nE 'stdin'` → NO stdin=).
In my probe the reader's fd0 was the driver's `/dev/null`; under an interactive driver a reader would hold the
terminal and could block or consume input up to the 60 s reader timeout. Low, one-line fix, same edit as 4.1.

**Explicitly not residual:** fixtures cannot execute (C1); no instrument reaches the network (C5); the gate's
own `/tmp` receipt (`c2:42-58`, unlinked in `finally`) is `mkstemp`-style 0600 and the gate's `--json-out`
write (`replay-gate.py:307-308`) uses a path whose parent is a sticky `/tmp`, so only same-uid processes could
race it — a same-uid attacker already owns the run.

## 5. Tooling

Nothing installed or upgraded this wave (no `uv`/`npx`/`~/.local/bin` change; no pacman transaction). Tools
used: `/usr/bin/python3` 3.14.8, `git ls-tree`, `jj diff`, `find`, `stat`, `file`, `getcap`, `sha256sum`.

## 6. Draft text for the L1 (not written to any doc by this seat)

- Lesson line: *R34-C2 containment: the eight fixtures are inert 0644 `MREC` data, the nine readers contain no
  spawn or network primitive, and every counter scrubs the child env — but readers still run as full-privilege
  Python at uid 1000, and the round's 26 pins live in a shape the lane's pin verifier rejects (exit 3
  `instruments_missing`), so nothing checks them at run time.*
- Add to the C2 predicate's notes, if the L1 wants it: the gate's guarantees are *content* guarantees
  (no spawn/net code, inert fixtures, scrubbed env) plus a 60 s reader timeout; they are not *capability*
  guarantees.

## Verdict

**CONTAINMENT: PASS on all four asked questions** — fixtures are inert 512-byte 0644 `MREC` data that cannot
execute (C1, C4); no pinned instrument contains a network primitive (C5); the gate, the C2 driver and the red
counter set exactly `PATH`/`HOME`/`LANG`, and the green counter sets `PATH`/`HOME` (C3, with `LC_CTYPE` added by
the child interpreter itself); the readers' committed content contains no spawn primitive (C2-content).
**With two open items the L1 must not let the CLEAN verdict absorb:** readers execute as arbitrary uid-1000
Python with write access to the lane and to `expected.json` (§4.1), and the 26 declared pins are enforced by no
committed checker — `freeze-integrity.py --claims .ufo/waves/round-34/r34b/claims.json` exits 3
`instruments_missing` (§4.2/§C6). Neither falsifies P34-shortcut-replay; both weaken the provenance claim
"frozen before any production run".
