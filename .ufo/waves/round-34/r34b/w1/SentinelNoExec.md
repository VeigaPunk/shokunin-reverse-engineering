# SentinelNoExec — no-execution audit of R34-C2 (gate + both counters)

Seat: `L1Kaidoku34-2.SentinelNoExec` (leaf, no dispatch)
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` — read-only; lane VCS untouched after `git archive` (read) and `git show`/`ls-tree`/`ls-files` (read)
Frozen object: `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (frozen claim R34-C2, pre-freeze structure-blind shortcut-replay gate)
Audit window: 2026-10-25T07:19Z–07:23Z (all timestamps UTC, taken with `date -u` before/after each command)
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w1/SentinelNoExec/` (tree extracted with `git archive c79bbe7b | tar -x`; `archive_exit=0`)
Residual limit: **stated in §G — a python reader is arbitrary code; the counters cannot attest its behaviour, and `no execution` is not `no capability`.**

## Axes named (Godspeed)

1. **Exec-origin completeness** — every site in the three instruments and the gate's selftest that can turn a path into a program.
2. **Interpreter binding** — is "python only" a property of the code, or of the two committed configs?
3. **Receipt attestation** — can a receipt prove what was executed, or only what a caller typed?
4. **Non-attestable surface** — what a reader can do that the counters cannot see (cwd, env, expected.json).
5. **Frozen-byte integrity** — is what I audited what the claim pinned.

## A. Exec-origin enumeration — the claim *holds* for the committed instruments

Method: `grep -rn -E "subprocess|os\.system|os\.exec|os\.spawn|popen|Popen|execv|check_output|check_call|shell=True|os\.fork|pty\.|ctypes|sys\.executable|__import__|importlib|eval\(|exec\(" --include=*.py tools/round-34`
Exit 0. Five spawn sites exist in the C2 chain, and nothing else:

| # | Site | argv[0] | Evidence |
|---|------|---------|----------|
| 1 | `tools/round-34/replay-gate.py:77-81` `run_counter` | **`config["counter"]["argv"][0]` verbatim** (no interpreter prefix) | `argv = [part.replace("{reader}", str(reader_path)) …]` → `subprocess.run(argv, cwd=str(root), env={"PATH","HOME","LANG"}, timeout=300)` |
| 2 | `replay-gate.py:266` selftest mutant | `sys.executable -I -B <temp mutant>` | mutant is a `.replace()` copy of the gate's own text written under `tempfile.TemporaryDirectory(prefix="kaidoku-r34-gate-")` |
| 3 | `c2-shortcut-gate-counter.py:35-36,45` | `sys.executable -I -B <root>/tools/round-34/replay-gate.py` | the only caller of `run()`; `--gate` overrides the path but never the interpreter |
| 4 | `mini-fix/mini-counter.py:116-118` | `sys.executable -I -B <reader> <opaque temp copy>` | reader is argv[1]; `env={"PATH","HOME"}`, no `cwd` |
| 5 | `mini-fix/naive-counter.py:48-50` | `sys.executable -I -B <reader> <fixture path>` | reader is argv[1]; `env={"PATH","HOME","LANG"}`, no `cwd` |

Absent everywhere: `os.system`, `os.exec*`, `os.spawn*`, `os.fork`, `pty`, `ctypes`, `eval`, `exec`, `__import__`, `importlib`, `shell=True`. Imports are stdlib only (`replay-gate.py:22-28`; `c2-shortcut-gate-counter.py:16-21`; `mini-counter.py:12-21`; `naive-counter.py:9-13`) — no lane-local module is imported, so import time cannot run tree code.

The two committed configs pin the interpreter as a literal absolute path: `"argv": ["/usr/bin/python3", "-I", "-B", …]` (`gate-config-mini.json`, `gate-config-naive.json`), and R34-C2's `counting_command` (`claims.json`) names no `--gate`, so production uses the pinned default. **With those configs, "the only subprocess calls are python3 runs of readers and of the gate itself" is true.**

Closest approach to a non-python argv: the naive red case passes the fixture path as the reader's **argv[1]** — 64 occurrences of `fixtures/<name>.mrec` in argv position 1 of a `python3` exec, never at argv[0].

## B. Empirical attestation (not a code reading)

Command (scratch tree at c79bbe7, 2026-10-25T07:19:40Z → 07:19:44Z):

```
strace -f -qq -s 400 -e trace=execve,execveat -o $S/trace-c2.txt \
  /usr/bin/python3 -I -B tools/round-34/c2-shortcut-gate-counter.py \
  --root $PWD --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out $S/c2-repro.json
```

- exit `0` → `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`
- **execve total 183; distinct exec path count 1: `/usr/bin/python3` (183/183).** `execveat` 0. Failed execs (`= -1`) 0.
- argv shapes observed: 1 counter, 3 gate (`--selftest`, red, green), 8 naive-counter, 8 mini-counter, 16 execs of each of the 8 registered readers, 32 execs of the selftest counter, 3 mutants. No fixture, reader or ELF ever occupied argv[0].
- child env sizes: 2 vars (mini-counter readers), 3 vars (all gate/counter/naive-reader spawns), 4 vars (mutant grandchildren — consistent with PEP 538 C-locale coercion adding `LC_CTYPE` to the gate process after it was spawned with the 3-var literal; not chased further). Ambient caller env is never inherited at a leaf spawn: every leaf gets a literal dict.
- **Reproduction is byte-identical**: `sha256(c2-repro.json) = da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9` = `sha256(.ufo/waves/round-34/r34b/after/c2-at-instruments.json)` — the receipt carries no timestamp, so the production receipt is exactly reproducible.

Frozen-byte check (F5 closure): all 26 pins in `claims.json` R34-C2 recompute identical to the frozen sha256 (`pins 26 mismatched 0`), and the eight audited instruments match `git show c79bbe7:<path>` sha256 (`replay-gate.py 8fa94b23…`, `c2-shortcut-gate-counter.py 41d59703…`, both configs, `build.py`, `mini-counter.py`, `naive-counter.py`, `expected.json`). Committed modes at c79bbe7: fixtures `100644`, readers `.py` `100755` with `#!/usr/bin/env python3`; **no committed blob under `tools/round-34` carries ELF magic `7f454c46`**; all eight fixtures begin `4d 52 45 43` (`MREC`) and are 512 bytes.

## C. Findings

### F1 — "no ELF/reader/fixture execution" holds, but only by config, not by code — **severity: medium (hardening; fail-closed)**
Exploit path: `replay-gate.py:49-50` accepts any counter argv that contains exactly one `{reader}` element anywhere; `replay-gate.py:77-81` executes `argv[0]` verbatim. A caller-supplied `--config` therefore names the program the gate runs. Proven with probe P1 (2026-10-25T07:20:04Z), whose `counter.argv[0]` is the committed 0644 JSON `tools/round-34/gate-config-mini.json`:

```
strace -f -qq -e trace=execve -o $S/trace-p1.txt /usr/bin/python3 -I -B tools/round-34/replay-gate.py \
  --root $PWD --config $S/probe-argv0-unpinned.json
# gate_exit=3  REPLAY_GATE_UNEVALUABLE finding=counter_spawn:PermissionError
# 3357638 execve("tools/round-34/gate-config-mini.json", [...], /* 3 vars */) = -1 EACCES (Permission denied)
```

Impact: the guarantee "the gate cannot execute a carrier" is not structural; it is inherited from two config files, and the gate accepts any `--config` path. Mitigating fact: every spawn failure maps to `Unevaluable("counter_spawn:…")` → `REPLAY_GATE_UNEVALUABLE`, exit 3 — the gate never reports CLEAN off a failed exec.
Smallest remediation (draft only, L1 lands it): in `load_config`, require `Path(counter["argv"][0]).resolve() == Path(sys.executable).resolve()` (or an allowlist of `python3*` basenames), so an interpreter pin is a config invariant rather than a convention.

### F2 — `{reader}` may occupy argv[0]: a committed reader *is* an executable program — **severity: medium**
`replay-gate.py:49` counts occurrences of `{reader}` but not its position; `:77` substitutes it into any slot. Probe P2 (2026-10-25T07:20:04Z), `counter.argv = ["{reader}", "--root", "."]`:

```
/usr/bin/python3 -I -B tools/round-34/replay-gate.py --root $PWD --config $S/probe-reader-at-argv0.json
# gate_exit=3  REPLAY_GATE_UNEVALUABLE finding=counter_spawn:PermissionError
# 3357645 execve("<repo>/tools/round-34/mini-fix/expected.json", [...]) = -1 EACCES
```

The config passed `load_config` (the refusal came at `execve`, not at `config_counter_reader_placeholder`), which proves the position is unconstrained. I deliberately pointed argv[0] at a **0644 JSON**, never at a reader: readers are committed `100755` with a shebang, so a config placing a reader at argv[0] would run it as a program — exactly the operation the round forbids. **I did not execute that path**, by rule; the kernel refusal in P2 is the whole receipt.
Impact: a control run can silently change from "reader scored on data" to "reader run as a program"; results would not be comparable, and the audit trail would not show it (§D).
Smallest remediation: require the `{reader}` index to be `>= 1` (ideally `== len(argv)-1`), and/or ship readers `0644` since they are only ever read as source.

### F3 — receipts cannot attest the exec set — **severity: info (documentation-of-limit)**
`replay-gate.py:100-101` returns only `{matched,target,met_target,finding,exit}` per row; `:304-305` adds `config`/`root` absolute paths. `c2-shortcut-gate-counter.py:73,100-110` records `measured_revision`, clauses and three verdict lines. **No receipt field records argv, environment or the executed program.** The five control receipts + `after/` + `before/` therefore support "what verdict was printed", never "what was executed". The only attestation of §A is the code read plus the external trace in §B.
Smallest remediation: add `"counter_argv": argv` (and the interpreter's `sys.executable`) to each row of the gate payload, so the receipt is self-attesting.

### F4 — `measured_revision` is caller-asserted provenance — **severity: info (adjacent surface, observed)**
`c2-shortcut-gate-counter.py:73` writes `"measured_revision": args.rev` into the receipt without resolving HEAD in `--root`; nothing compares the two. A receipt can name c79bbe7 while the tree is elsewhere. My own run closes this by construction (tree extracted from c79bbe7 by `git archive`, all 26 pins sha256-verified), but the production receipt alone does not.
Smallest remediation: resolve `HEAD` (read-only `git rev-parse`) under `--root` and refuse (`GATE_COUNTER_UNEVALUABLE finding=revision_mismatch`) when it differs from `--rev`.

### F5 — receipts argv audit (the assignment's second half) — **C2: clean**
- C2 receipts (`r34b/after/c2-at-instruments.{json,txt}`, `r34b/before/c2-at-base.txt`, `r34b/controls/*.json|txt`): **zero argv fields**. Their only program-bearing field is `gate_path`, always a `.py` run under `sys.executable` (`gate_path` = `tools/round-34/replay-gate.py` in production; `.ufo/waves/round-34/r34b/controls/gates/gate-*.py` in controls). All four control gates are `Python script, ASCII text`; three are the pinned gate with exactly one line changed (`if over:`→`if False:`, `if not positive["met_target"]:`→`if False:`, `len(shortcuts) < MIN_SHORTCUTS` dropped) and `gate-junk-clean.py` is an 11-line constant printer with no spawn at all. No receipt shows a non-python program on the C2 path.
- Round-wide, one receipt *does* carry a non-python argv, and it is not C2's: `claim-stop.json` (`counterexample_argv`, 23 elements) begins `/usr/bin/timeout … /usr/bin/prlimit --as=… --nproc=… --nofile=… --fsize=… --cpu=… -- /usr/bin/python3 -I -B <scratch>/version-needs-counter.py --control-reader <scratch>/size_lookup.py`. `timeout` and `prlimit` are coreutils limit wrappers, not carriers; the payload is python3; no ELF carrier, fixture or reader occupies argv[0]. That argv's scratch root `/fast/scratch/hyaku/kaidoku-r34/w1/CtlLabels` **no longer exists** (`ls` → ENOENT), so the receipt is not re-runnable as written. I did not run it: R34-C1 is stopped and must not be executed or scored.
- `prep/R34Expected-files/**/readelf-sections.txt` etc. are *captured output* of readelf, not argv this wave ran; out of scope (C1/prep), reported only as present.

## D. The residual limit (required statement)

**A python reader is arbitrary code. The counters can attest only that a reader process was spawned with `python3 -I -B <reader> <data>` under a literal 2–3 var env; they cannot attest what that process did, read, or spawned.** `-I` (isolated mode) and the scrubbed env block env-var and user-site injection, and the counters' own receipt schema cannot express reader behaviour, so nothing in the pipeline constrains it. Registered classes are the *only* coverage: an unregistered shortcut class is invisible to CLEAN.

I made the limit concrete (scratch only, 2026-10-25T07:21Z):
1. `mini-counter.py:116-118` passes **no `cwd`**, and the gate spawns the counter with `cwd=str(root)` (`replay-gate.py:80`), so a reader's cwd is the repo root. A reader can therefore read `tools/round-34/mini-fix/expected.json`. Verified: `strace -e trace=openat` on the green harness shows 9 opens of `mini-fix/expected.json`, including the reader process's `openat(AT_FDCWD, "tools/round-34/mini-fix/expected.json", O_RDONLY)`.
2. A 20-line oracle reader that never associates a name with a record — it matches the multiset of NUL-terminated names that survive `permute()` and replays `expected.json` — scores **8/8** on the green (identity-defeating) harness: `{"finding":"records_match","matched":8,"met_target":true,"target":8}`, `rows_ok=[True×8]`, `mini_exit=0`.
3. Registered as a class, the gate catches it: `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=3 shortcuts_over_target=oracle-expected-json`, `gate_exit=2`. So the gate is sound *over its class list* and silent *outside it* — CLEAN means "none of the seven registered shortcuts met target", never "the counter is structure-sensitive".

Consequence for R34-C2's wording: the clauses are honestly scoped ("refuses the shape-only counter … clears the identity-defeating counter … kills every mutant of its own branches"), but any downstream doc that reads REPLAY_GATE_CLEAN as "no shortcut exists" over-reads it. The green fixture set also has a public answer key inside the graded tree; a reader-side filesystem restriction (unreadable `expected.json`, or `cwd` = the opaque temp dir) would remove that specific path without changing the predicate.

## Commands, exits, times (condensed)

| UTC | Command | Exit |
|---|---|---|
| 07:19:04Z | `git rev-parse HEAD` → `c79bbe7b…`; `git status --porcelain` → only untracked `.ufo/waves/round-34/r34b/**` | 0 |
| 07:19:40Z→07:19:44Z | strace'd `c2-shortcut-gate-counter.py` on the c79bbe7 scratch tree (§B) | 0 |
| 07:20:04Z | probe P1 (argv[0] unpinned) | 3 |
| 07:20:04Z | probe P2 (`{reader}` at argv[0]) | 3 |
| 07:21:26Z | oracle reader vs `mini-counter.py` under `openat` trace | 0 (matched 8/8) |
| 07:21:27Z | gate with oracle registered as a class | 2 (REFUSED) |
| 07:23Z | 26-pin sha256 recomputation; mode/magic scan; `file` on control gates | 0 |

Tool installs: **none** (no pacman, no `uv tool`, no binary fetched). Tools used are pre-existing: `/usr/bin/python3` (3.14), `/usr/bin/strace`, `git` in read-only form.

## Verdict

**PASS WITH LIMITS.** From the committed code and an external `execve` trace of the pinned production command, neither the gate nor either counter executes a carrier, fixture or ELF at c79bbe7b: 183/183 execs are `/usr/bin/python3`, no `execveat`, no failed exec, and the only spawn origins are the five sites in §A — two python3 runs of readers, two python3 runs of the gate/selftest counter, one python3 run of the selftest mutant. The no-execution property is a property of the two committed configs, not of `replay-gate.py`: the gate executes `config["counter"]["argv"][0]` verbatim and does not constrain the `{reader}` slot away from argv[0] (probes P1/P2, exit 3, fail-closed). No C2 receipt records any argv, so a receipt cannot attest execution — only the external trace can. Residual limit: **a python reader is arbitrary code reachable at the repo root (cwd inherited, `expected.json` readable); the counters cannot attest reader behaviour, and REPLAY_GATE_CLEAN is a statement about the seven registered classes only.**
