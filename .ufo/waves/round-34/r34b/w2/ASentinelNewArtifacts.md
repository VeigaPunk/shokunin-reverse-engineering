# ASentinelNewArtifacts — containment and no-execution audit of the wave-1 artifacts the stop rests on

Round 34 / r34b / wave 2. Seat: `L1Kaidoku34-2.ASentinelNewArtifacts`.
Lane HEAD at audit time: `5a0435ffb9a8921206144e0b61fe3c12a89b59c2` (2026-10-25T04:35:10-03:00).
Host: linux 7.2.11-arch1-1 · python3 3.14.8 · strace 7.2 · umask 0022 · `TMPDIR` unset.

## 0. Surface, non-actions, provenance of my own work

**Audited artifacts (all tracked at `cd75b92e`, none drifted since — §7):**

| artifact | sha256 | mode |
|---|---|---|
| `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` | `2e8feaea92ee…a88b97` | `0755`, regular, 1 link |
| `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/pathkey.py` | `28acfe5a79b2…481a9` | `0755`, regular, 1 link |
| `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py` | `5181330d07ca…ff5c` | `0755`, regular, 1 link |
| `.ufo/waves/round-34/r34b/claim-stop.json` | `e6303d061da2…` | `0644`, regular |
| `.ufo/waves/round-34/r34b/instruments.json` | `224cc44124c5…` | `0644`, regular |

**Not done, deliberately:** I did not run the R34-C1 production reader or any of its twelve carriers; I did not edit any frozen instrument, `claims.json`, `claim-stop.json`, any corpus/SCORECARD/LOG/SKILL doc, or any lane file other than this report; no VCS mutation; no build/lint/bulk suite; no tool installed (nothing needed). All probes ran from `/fast/scratch/hyaku/kaidoku-r34b/w2/ASentinelNewArtifacts/`; nothing was written inside the lane root (`strace` write-open count against the lane: **0**, §3 C3).

**Load-bearing distinction:** `nameset.py` and `pathkey.py` are *data-only* readers (no imports beyond `json/re/sys/pathlib/hashlib`, no spawn, no socket — §2 C1). `mini-counter-fresh.py` is a *counter*: it is the only one of the five that spawns a process. Its spawn is the whole containment surface of this wave.

## 1. Verdict up front

- **No network use in any of the five artifacts.** Static import graph and syscall trace agree (§2 C1, §6 E22/E23).
- **No path by which any of the five executes a non-Python file.** The only `execve` in a full trace is `/usr/bin/python3` (9×: parent + 8 children). An ELF handed to the counter as `--control-reader` is *parsed* by Python (row exit 1), never executed (§2 C5).
- **No writes outside a temp dir by the counters themselves** — one `tempfile` policy probe file in `$TMPDIR` and eight fixtures under a `0700` `mkdtemp` dir, fully cleaned (§2 C6, E22).
- **But the counter is not a containment boundary for the reader it scores.** A control reader runs with euid 1000, the caller's cwd, full filesystem read/write, an unrestricted network stack, and no process-group cleanup. That is a *by-design* consequence of `subprocess.run` with no sandbox — and it is the one residual risk that matters, because the counter's purpose is to score adversarial shortcut readers (§2 C3, C4, C8).
- **The candidate repair the stop implies is replayable through a published seed.** With `--seed kaidoku-r34-mini-v1` a structure-blind digest-keyed memorizer scores **8/8, exit 0** against `mini-counter-fresh.py`; with a fresh urandom seed the same reader scores **0/8** (§2 C9, E15/E16). The fresh surface's blindness is seed-secrecy-dependent, and nothing enforces seed secrecy.
- **The stop's own evidence reproduces.** `nameset.py` scores 8/8 on `kaidoku-r34-mini-v1`, `alt-1`, `alt-2`; `pathkey.py` scores 0/8; the seven registered classes contain no content-multiset class; and the counter's only transformation provably leaves each fixture's SONAME set invariant (§5). I find no defect in the stop that changes its direction.

## 2. Findings — severity, exploit path, evidence, impact, smallest remediation

### C1 — No network use anywhere on this surface · **INFO (verified clear)**
Static: import graph of all three Python files is `{json, re, sys, pathlib, hashlib, argparse, os, random, struct, subprocess, tempfile}`; no `socket/ssl/http/urllib/requests/ftplib/smtplib`. No URL string constants. Syscall: `strace -f -e trace=socket,connect,bind,sendto` over both counters shows **zero** network syscalls attributable to counter code — the 16 observed socket/connect events in the fresh-counter trace are exactly my own probe's 8×(socket+connect to `127.0.0.1:9`). The frozen-counter trace: `net count=0`.
**Caveat that is not about these files:** the *reader* can open sockets (C3), so "no network" is a property of the five artifacts, not of the gate.

### C2 — Spawn site is minimal and correctly hardened at the exec boundary · **INFO (verified clear)**
`mini-counter-fresh.py:score()` spawns exactly once per fixture:
`subprocess.run([sys.executable, "-I", "-B", str(reader), str(target)], capture_output=True, text=True, timeout=60, env={"PATH": "/usr/bin:/bin", "HOME": str(work)})`.
Verified properties:
- argv-list form, no `shell=True`, no string interpolation → no shell metacharacter path.
- `-I` is load-bearing and *empirically* effective: a sibling `json.py` next to the reader is **not** imported (`shadow/SHADOW_MARKER.txt` absent, E8), while the same reader under plain `python3` *does* import it (marker present). `python3 -I -c` reports `safe_path True isolated 1 ignore_env 1`.
- `env` is rebuilt from scratch → `PYTHONPATH`, `PYTHONSTARTUP`, `PYTHONHOME` and every ambient variable are dropped; the child observed only `HOME`(temp), `PATH`, `LC_CTYPE`(CPython locale coercion) — no secret leakage from the invoking shell.
- `HOME` is redirected into the ephemeral temp dir, so `~/.config`/`~/.cache` writes by a reader land in a directory deleted at exit.
**Residual (not a defect):** `sys.executable` is taken from the running interpreter, not pinned to `/usr/bin/python3`; under a venv the child is that venv's python.

### C3 — **HIGH** — the counter grants the reader full host authority; there is no sandbox
Exploit path (executed, not hypothesised): a reader invoked by `mini-counter-fresh.py` runs as a normal child of the counter and can
1. write into the **caller's cwd** — `subprocess.run` passes no `cwd`, so the child inherits it; my probe created `PROBE_CWD_WRITE.txt` relative-path and it landed in the directory the counter was launched from (E2/E22, strace shows `openat(AT_FDCWD, "PROBE_CWD_WRITE.txt", O_WRONLY|O_CREAT…)` ×8);
2. write the **lane repository** — `os.access(<lane>, W_OK)` is `True` from the child (euid 1000, `drwxr-xr-x vgpnk:vgpnk`), and no seccomp/namespace/lsm layer intervenes;
3. **read any file** — `/etc/hostname` read successfully; the child can read the fixtures of *other* fixtures, the counter source, its own pin list, or any host secret readable by uid 1000;
4. **open outbound sockets** — `socket(AF_INET, SOCK_STREAM)` succeeds and `connect(127.0.0.1:9)` reaches the stack (`errno=111 ECONNREFUSED`, i.e. the syscall is permitted, not blocked).
Impact: a wave-2 "control" reader is not a measured object but a peer process with the operator's full authority. One lane-authored control reader that appends to `SCORECARD.md`, rewrites a fixture, or edits `instruments.json` before the gate re-hashes would convert a red measurement into a green one *and* leave the pin check green, because the change happens inside the same measured window. `[INFERENCE]` — the mechanism is observed; I did not build such a reader.
Smallest remediation: run the child under `bwrap`/`unshare` (`--unshare-net --ro-bind /usr /usr --ro-bind <lane> /lane --tmpfs /tmp --chdir /tmp`) or, minimally, `cwd=str(work)` **and** `env={"TMPDIR": str(work), …}` **and** a documented "readers are untrusted code, run this counter in a sandbox" clause on the predicate. `bwrap` and `unshare` are installed on this host.

### C4 — **HIGH** — no process-group cleanup: a reader outlives the counter
Exploit path (executed): a reader forks a grandchild, closes `0/1/2` in it (so `communicate()` does not block on the inherited pipe), and exits. The counter returns normally while the grandchild is still running.
Evidence (E18, 07:35:56Z): counter exit **1**; `ps -o pid,ppid,stat,cmd -p 3733451` → `S /usr/bin/python3 -I -B …/orphan_probe.py …`, ppid already reparented (1493, not the counter); `kill -0` → alive; it self-exited after its own 4 s sleep only because I wrote it that way.
Impact: every scored run can leave arbitrary code running in the operator's session, after the receipt is written. `subprocess.run(timeout=60)` on `TimeoutExpired` kills only the direct child (no `start_new_session`/`killpg`), so the timeout path leaks too. `[STATIC]` for the timeout path; `[OBSERVED]` for the normal-return path.
Smallest remediation: `start_new_session=True` and, on return and on `TimeoutExpired`, `os.killpg(run.pid, SIGKILL)`; or forbid `os.fork` by running the child under a PID namespace (same `bwrap` line as C3).

### C5 — Non-Python control readers are refused or inert; no ELF execution path · **INFO (verified clear)**
| control reader | exit | row exits | interpretation |
|---|---|---|---|
| `/dev/null` (char device) | **3** | — | `unevaluable:Unevaluable:reader_absent` (`is_file()` false) |
| a directory | **3** | — | same typed refusal |
| `/bin/true` (ELF) | **1** | all `1` | Python *parsed* the ELF and failed (`SyntaxError`), exit 1 per row — it was never `execve`d; trace shows 9 execve, all `/usr/bin/python3` |
| symlink → `probe_reader.py` | 1 | all `0` | accepted and run **via the symlink path** (`argv[0]` = the symlink) |
Missing `--control-reader` → argparse exit **2**.
Impact: the "readers run only as python via a counter" rule is structurally enforced by the exec site, not merely by convention.

### C6 — Writes by the counters themselves stay inside temp; cleanup is complete · **INFO (verified clear)**
Write-mode opens in the fresh-counter trace: 8 × `/tmp/kaidoku-r34-fresh-<rand>/opaque-<sha256[:20]>.data`, 1 × `tempfile` default-dir policy probe (`/tmp/h_47oaym`, `O_EXCL|O_NOFOLLOW|0600`, immediately `unlink`ed — that is `tempfile._get_default_tempdir()`), and nothing else attributable to the counter. `mkdir("/tmp/kaidoku-r34-fresh-…", 0700)`. After every run, `ls -d /tmp/kaidoku-r34-fresh-*` → **0** leftovers.
**Residual L1:** `TemporaryDirectory` honours the parent's `TMPDIR`; with `TMPDIR` set to a path inside the lane the fixtures would be written there (E17: fixtures followed `TMPDIR` to my scratch, then were removed; 0 entries left). Not exploitable on this host (`TMPDIR` unset), but it means "writes only in temp" is really "writes only in `$TMPDIR`".
**Residual L2:** `target.write_bytes()` uses plain `O_CREAT|O_TRUNC` (no `O_NOFOLLOW`), and `is_file()`→`execve` is a TOCTOU pair. Both are inside a fresh random `0700` directory with a digest-derived name, so the window is not reachable in practice; note only.

### C7 — `--root` is parsed and never used; reader path is unbounded · **MEDIUM**
`main()` accepts `--root` (default `.`) and `score()` never receives it; `--control-reader` is used verbatim. Evidence: my reader lives **outside** `--root=/home/…/kaidoku-shokunin` and was executed (E1/E2/E6); a symlinked reader is followed (E6). So the counter will run *any* Python file on the host as the "control", including one that is not a control at all.
Impact: the gate has no notion of "registered control"; registration lives only in `gate-config-mini.json`, which this counter does not read. A wave-2 seat can point the fresh counter at a reader outside the lane and report its score.
Smallest remediation: require `--root`, resolve `--control-reader` with `Path.resolve()` and refuse unless `root in path.parents` and `not path.is_symlink()`.

### C8 — **MEDIUM** — `mini-counter-fresh.py` is an unpinned, unpublished executable counter
- Not in `instruments.json` (26 pins, verified hash-match, none is this file).
- Not mentioned in `claims.json`, `instruments.json`, or `claim-stop.json` (`grep -c` → 0, 0, 0).
- Mode `0755` with `#!/usr/bin/env python3`.
- It spawns a process (C3–C4) and is the artifact wave 2 would adopt as "the repair".
Impact: the moment this file becomes the gate, the gate's own bytes are outside every pin, and the round's freeze-integrity cannot see it change. The same applies to the two control readers: `instruments.json` pins the nine *frozen* readers and none of the two new controls, so a post-freeze edit to `nameset.py` is invisible to `freeze-integrity` (visible in git, but not in the pin check the stop cites as the enforcement mechanism).
Smallest remediation: put the repair counter and both controls into the pin container before any wave-2 seat scores against them, and land the pin before the run (freeze-before-data).

### C9 — **HIGH (for the repair's validity)** — the fresh surface is replayable through a published seed
The predicate claims "eight synthetic record-chain fixtures generated per run from a fresh seed … the association is unpublished, so only record-array traversal recovers it." The code does not enforce that:
`parser.add_argument("--seed", default=None)` … `seed = args.seed if args.seed is not None else os.urandom(16).hex()` … and the receipt **prints** `"seed": "…"`.
Exploit path (executed end to end): take the seed from any published receipt (or the frozen counter's own default `kaidoku-r34-mini-v1`), regenerate the eight fixtures offline with the artifact's own `generate()`, build `{basename: records}`, and ship a reader that reads neither the header, nor the record array, nor `name_off`.
Results: `--seed kaidoku-r34-mini-v1` → `matched 8, met_target true, exit 0` (E15). Same reader, no `--seed` (urandom) → `matched 0, exit 1` (E16). The two shortcut controls from wave 1 score 0/8 against the same counter on a random seed (E13/E14), so the counter *does* close the classes the stop found — it does not close digest memorization once the seed is known.
Impact: the stop's own failure mode (a structure-blind class meeting the green target) reappears one indirection out, and reproducibility pressure makes it likely: any wave-2 seat that wants a re-runnable receipt will pass `--seed`.
Smallest remediation: refuse `--seed` when scoring controls (or accept only a commitment, `--seed-commitment <sha256>`), draw the seed internally, and either omit it from the receipt or print only `sha256(seed)` — then the receipt proves the run without publishing the association.

### C10 — `instruments.json`'s "enforced" container is opt-in and drops the verifier's own pin · **MEDIUM**
Verified positive: 26/26 pins resolve and hash-match the working tree; the map is **byte-for-byte identical** to `claims[0].pins` (confirmed by dict equality), matching the note's claim that only the container is added.
Verified negative: the claim "enforced" holds only for a non-default invocation.
- `freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/instruments.json --rev HEAD` → **exit 0**, `CLEAN pins=26 freeze=b917ea64ebbe` (E19).
- `freeze-integrity.py --root . --round 34 --rev HEAD` (the documented default) reads `.ufo/waves/round-34/claims.json` — a *different, older* freeze (21 pins) — and returns **exit 1, FAIL changed=1** on `corpus/knowledge/2026-10-23-r34-elf-version-needs.md` touched by `66b84027` after freeze `54a87a51` (E20).
- `… --claims .ufo/waves/round-34/r34b/claims.json` → **exit 3** `code=instruments_missing` (E21) — F1 reproduced exactly as disclosed.
- **No receipt in `after/` or `controls/` invokes `freeze-integrity` at all** (`grep` → no hits), so the container's CLEAN is a state I had to produce; the round never recorded it.
- The container omits `tools/round-34/freeze-integrity.py`, which the older round-level map *does* pin (`sha=fe955c578912`). Relative to that regime the new container is a pin-coverage regression: the verifier is unpinned.
Impact: F1's repair exists but nothing in the round's evidence chain reaches it; a reader who runs the documented command gets a red verdict about a different claim.
Smallest remediation: land a receipt that shows the `--claims instruments.json` invocation, and add `freeze-integrity.py` to the container.

### C11 — the stop's recorded commands are not fully determined · **MEDIUM (evidence integrity)**
- `decisive_counterexample.argv` is `["python3", "-I", "-B", "tools/round-34/mini-fix/mini-counter.py", "--root", ".", …]`: interpreter resolved through `PATH`, a **relative** script path, and `--root "."` — all relative to a cwd the record does not state. From any other cwd the same argv executes a different file or nothing. Reproduced only because I inferred the lane root (§5).
- The seed is absent from the argv; the run therefore used the counter's *constant default* `kaidoku-r34-mini-v1`. A reader of the record cannot know that without opening the instrument.
- `frozen_counter_verdict.command` is not a command but a placeholder template: `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev c79bbe7b… --json-out <RECEIPT>` — executing it verbatim fails. The receipt it points at does exist and matches the quoted line (E24).
- `l1_rerun_utc` is `"2026-10-25T07:28:00Z (approximate; exact clock in the wave report)"` — a timestamp that is explicitly not a measurement.
Impact: the stop is reproducible only with unstated context. That is a provenance weakness, not a falsification: I supplied the context and the claim held (§5).
Smallest remediation: record `cwd`, absolute interpreter, absolute script, and the effective seed; replace the `<LANE>`/`<RECEIPT>` template with the executed argv.

### C12 — the JSON artifacts are inert data · **INFO (verified clear)**
Both parse as strict UTF-8 JSON, no BOM, trailing newline present, no `..` segments, no NUL/control bytes, no shell metacharacter strings. `decisive_counterexample.argv` is a JSON *array* (a consumer cannot accidentally word-split it into a shell); nothing in either file is passed to `eval`, `sh -c`, or a glob. The only execution-adjacent content is exactly what C11 describes.

## 3. Evidence table (exact argv, exit, UTC)

All `python3` = `/usr/bin/python3` 3.14.8. `LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. `SCRATCH=/fast/scratch/hyaku/kaidoku-r34b/w2/ASentinelNewArtifacts`. `FRESH=$LANE/.ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py`; `FROZEN=$LANE/tools/round-34/mini-fix/mini-counter.py`; `NS=$LANE/.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py`; `PK=…/pathkey.py`.

| # | UTC 2026-10-25 | argv (cwd) | exit | result |
|---|---|---|---|---|
| E1 | 07:30:17Z | `python3 -I -B $FRESH --root $LANE --control-reader $SCRATCH/probe_reader.py --seed sentinel-r34b-probe` (cwd `$SCRATCH`) | 1 | `records_mismatch matched 0` |
| E2 | 07:30:23Z | same, probe writes `$SCRATCH/probe_diag.json` | 1 | child `cwd=$SCRATCH`; env `{HOME=/tmp/kaidoku-r34-fresh-jrzfo_94, PATH=/usr/bin:/bin, LC_CTYPE=C.UTF-8}`; `socket_created_connect_refused:errno=111`; `write_cwd/write_home/write_tmp ok`; `read_etc_hostname_bytes 9`; `lane_writable_now true`; `executable /usr/bin/python3` |
| E6 | 07:31:47Z | `… --control-reader $SCRATCH/probe_link.py --seed s-symlink` | 1 | symlink reader executed; child `argv[0]=…/probe_link.py`, `cwd=$SCRATCH` |
| E4 | 07:31:48Z | `… --control-reader /bin/true --seed s-elf` | 1 | every row `exit=1` (Python parse failure); ELF not executed |
| E5a | 07:31:47Z | `… --control-reader /dev/null --seed s-dev` | 3 | `unevaluable:Unevaluable:reader_absent` |
| E5b | 07:31:47Z | `… --control-reader $SCRATCH --seed s-dir` | 3 | `unevaluable:Unevaluable:reader_absent` |
| E7 | 07:31:47Z | `… --seed s-no` (no `--control-reader`) | 2 | argparse: required: `--control-reader` |
| E8 | 07:32:10Z | `… --control-reader $SCRATCH/shadow/reader.py --seed s-shadow` | 1 | rows `exit=0`; `shadow/SHADOW_MARKER.txt` **absent** → `-I` blocks sibling `json.py`. Control `python3 $SCRATCH/shadow/reader.py` → marker **present** |
| E9 | 07:32:50Z | `python3 -I -B $FROZEN --root . --control-reader $NS` (cwd `$LANE`) | 0 | `matched 8 target 8 met_target true` |
| E10 | 07:32:50Z | `… $FROZEN … --control-reader $PK` | 1 | `matched 0`, all rows `exit=3` |
| E11 | 07:32:50Z | `… $FROZEN … --control-reader $NS --seed alt-1` | 0 | `matched 8` |
| E12 | 07:35:40Z | `… $FROZEN … --control-reader $NS --seed alt-2` | 0 | `matched 8 met_target true` |
| E13 | 07:32:50Z | `python3 -I -B $FRESH --root . --control-reader $NS` | 1 | `matched 0`, rows `exit=3`, seed `5e7b9448a10c4ca61d6d7f86ba8fa8fa` |
| E14 | 07:32:50Z | `… $FRESH … --control-reader $PK` | 1 | `matched 0`, seed `977366faf3e234251874655bfed3b9e1` |
| E15 | 07:33:08Z | `… $FRESH --control-reader $SCRATCH/digest_replay_reader.py --seed kaidoku-r34-mini-v1` | **0** | `matched 8 target 8 met_target true`, rows `exit=0` |
| E16 | 07:33:08Z | same reader, no `--seed` | 1 | `matched 0`, seed `779cacb4b2d18dd8390043ab293727f7` |
| E17 | 07:35:40Z | `TMPDIR=$SCRATCH/tmpdir python3 -I -B $FRESH --control-reader probe_reader.py --seed s-tmpdir` | 1 | fixtures created under `$SCRATCH/tmpdir`, 0 entries left |
| E18 | 07:35:56Z | `… $FRESH --control-reader $SCRATCH/orphan_probe.py --seed s-orphan` | 1 | grandchild pid 3733451 alive after return, `ppid=1493`, self-exit ≈4 s |
| E19 | 07:34:06Z | `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/instruments.json --rev HEAD` | 0 | `CLEAN pins=26 freeze=b917ea64ebbe` |
| E20 | 07:34:06Z | same with `--round 34` only | 1 | `FAIL pins=21 changed=1 freeze=54a87a51a865`; changed path `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`, `commits_after_freeze=66b84027` |
| E21 | 07:34:06Z | same with `--claims .ufo/waves/round-34/r34b/claims.json` | 3 | `schema code=instruments_missing … where=instruments` |
| E22 | 07:34:17Z | `strace -f -qq -e trace=execve,execveat,socket,connect,bind,sendto,openat,unlink,unlinkat,rename,renameat,mkdir,mkdirat -o strace_fresh.log python3 -I -B $FRESH --control-reader $SCRATCH/probe_reader.py --seed s-strace` | 1 | 9 execve, all `/usr/bin/python3`; 16 net syscalls = my probe only; `mkdir(…,0700)`; lane write-opens **0**; `/tmp/kaidoku-r34-fresh-s9ygb2lx/*` ×8 |
| E23 | 07:34:31Z | `strace -f -qq … python3 -I -B $FROZEN --root . --control-reader $NS` | 0 | 9 execve, all `/usr/bin/python3`; `net count=0`; no write-open outside `/tmp`; `nameset.py` opened `O_RDONLY` only; `matched 8` |
| E24 | — (read) | `after/c2-at-instruments.json` | — | `exit 0`, `finding shortcut_gate_discriminates`, `selftest_failures 0`, `mutants_killed 3`, all six clauses `true`, `green.positive_matched 8`, `green.line … shortcuts_below_target=7 shortcuts_over_target=-` — matches the line quoted in `claim-stop.json` |

Supporting static probes (no execution of the artifacts): AST import/call inventory per file (§2 C1); `stat`/`readlink` for mode, link count, ownership, symlink-ness (§0); 26-pin hash verification; `git log --format=%h cd75b92e..HEAD -- <file>` for drift (§7).

## 4. Residual risk register (ranked, all evidence above)

1. **Reader = full operator authority** (C3): lane-write, arbitrary read, unrestricted egress, inherited cwd. No mitigation exists in the artifact; only invoker discipline.
2. **Reader outlives the counter** (C4): normal-return leak demonstrated; timeout path leaks grandchildren by construction.
3. **Seed secrecy is the only thing separating the repair from the stopped class** (C9): 8/8 ↔ 0/8 on the same reader, toggled by one CLI flag that the receipt publishes.
4. **Repair counter and both new controls are unpinned and unpublished** (C8, C10): freeze-before-data has no teeth for the wave-2 artifacts.
5. **`--root` inert, reader path unbounded, symlink followed, TOCTOU** (C7): the counter can be aimed at any Python file on the host.
6. **`0755` + `#!/usr/bin/env python3`** on all three: direct invocation runs a `PATH`-resolved interpreter. `PATH` hijack is the classic escalation here, and the three files do not need the exec bit. Smallest fix: `chmod 0644` and always invoke via an absolute `python3 -I -B`.
7. **`instruments.json` "enforced" is opt-in, unpinned verifier, no receipt** (C10).
8. **Record commands underdetermined** (C11): cwd, interpreter, seed unstated; one "command" is a `<LANE>` template; one timestamp is explicitly approximate.
9. **`TMPDIR`-anchored writes** (C6/L1) and non-`O_NOFOLLOW` fixture creation inside a random `0700` dir (C6/L2): negligible on this host.

## 5. The stop's own evidence, checked (not my surface to judge — reported because the audit touched it)

- `nameset.py` meets the green target on the frozen counter with the counter's default seed and with `alt-1`, `alt-2` (E9/E11/E12, exit 0 each). The stop's `observed` block reproduces.
- The stated mechanism holds mechanically: for all eight fixtures, the counter's only transformation (`permute`) leaves the sorted SONAME **set** invariant (`set_invariant: true` ×8, verified by extracting tokens from the fixture and from `permute(fixture, Random("kaidoku-r34-mini-v1"))`). The `nameset.py` keys match exactly those eight sets.
- `pathkey.py` (path-stem + raw-SHA-256 keying) scores **0/8** (E10): it is not the class that meets the target, consistent with the stop attributing 8/8 to the content-multiset control and not to digest keying. Digest keying fails on the frozen counter precisely because the counter transforms the bytes; the same keying succeeds on the fresh counter only when the seed is known (C9).
- The registered set is seven classes (`all-false`, `size-keyed`, `fixed-slice`, `digest-keyed`, `string-scan`, `record-order-replay`, `label-memorization`) and none is content-multiset / name-set keyed — so "this class is unregistered" is accurate.
- `[STATIC, not adjudicated here]` `replay-gate.py` has `MIN_SHORTCUTS = 3` with a `<` length check only and no equality assertion against the registered count; the receipt's own line reports `shortcuts_below_target=7`. That is consistent with record defect F3; verifying it is another seat's job, so I make no finding.
- F1 reproduced (E21) and its repair verified as *present and correct* (E19) but *unreached* (C10). F2 (predicate identity), F4 (mutant M3), F5 (receipt tracking) are outside this surface; F5's landed state is consistent with what I observed — all five artifacts are tracked at `cd75b92e` and `b917ea64` is an ancestor of it (`git merge-base --is-ancestor` → true).

## 6. Environment / tooling record

No installs, no upgrades, no `pacman`. Tools used: `/usr/bin/python3` 3.14.8, `strace` 7.2, `git`, coreutils. `bwrap` and `unshare` are present but were **not** used (I did not need to sandbox my own probe; it wrote only to scratch and unlinked after itself). Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/ASentinelNewArtifacts/` (`probe_reader.py`, `probe_link.py`, `orphan_probe.py`, `digest_replay_reader.py`, `seed_table.json`, `build_seed_table.py`, `shadow/`, logs `E*`/`R*`/`strace_*.log`).

## 7. Drift check

For each of the five artifacts: `sha256(working) == sha256(git show cd75b92e:<path>)` and `git log --format=%h cd75b92e..HEAD -- <path>` is empty. No post-stop mutation of any audited artifact. The 26 pinned instruments also report `commits_after_freeze=0` and hash-match at HEAD.

## 8. Verdict

**CONTAINMENT: CLEAR for the five artifacts as written — no network, no non-Python execution path, no writes outside temp, no symlinked artifacts, clean cleanup — and NOT CONTAINED for the reader the counter scores: full host authority, inherited cwd, unrestricted egress, and no process-group cleanup (C3, C4). The stop's evidence reproduces (8/8 on three seeds, set-invariance proven per fixture, seven registered classes with no content-multiset class), and the fresh-seed candidate repair closes both wave-1 controls (0/8) while remaining 8/8 replayable by a structure-blind digest memorizer whenever the seed is published (C9). Residual risk is concentrated in three places: an unsandboxed child, an unenforced seed, and an unpinned repair counter.**
