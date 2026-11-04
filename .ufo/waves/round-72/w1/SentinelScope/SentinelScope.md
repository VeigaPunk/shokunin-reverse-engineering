# SentinelScope — round-72 security review

Read-only review of operative freeze `34fe7aa70b627d92e2d27dbce308d9f5bebda63d`; no instrument remediation or claim adjudication. Axes: execution provenance, read containment, scratch placement, canary disclosure, failure cleanup. Current worktree instruments are changing concurrently; line references below are **frozen** unless explicitly identified otherwise.

Evidence: `observations.json` records executed harmless probes and six frozen source hashes; `frozen-boundaries.json` records source function/call locations; `canary-tracked.txt` records committed canary matches. All are in this report's directory. Reproduce the executed cases with:

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-72/w1/SentinelScope/probe.py
```

The probe extracts frozen source into the single assigned scratch directory, sets child TMPDIR there, retains observations before `finally: shutil.rmtree(S)`, and never executes attacker-supplied shims. The explicit assignment permits that scratch path as an exception to lane-only writes. No tools installed/updated. No git mutations.

## SS72-1 — advisory: PATH is an executable trust boundary, not sanitized by the environment allowlist

**Exploit path:** A11 resolves its purported real `git`/`readelf` with `shutil.which` against caller PATH, writes shell wrappers, then prepends their directory to that same PATH. A hostile earlier PATH entry or symlinked executable is executed as the user; shell wrapper `cat` is also PATH-resolved. Removing environment keys does not restrict filesystem/network access or prevent a replacement program from reading host files. Symlink targets/bytes are neither pinned nor held open, so replacement between lookup and exec remains possible. No offensive execution was performed.

**Evidence:** frozen `seam-probe.py:231-257`, especially 239,245-246,250; `packed-elf.py:210-223,334-348,536-541`. `shlex.quote` correctly quotes the destination and real-tool name and `"$@"` preserves arguments: no shell metacharacter injection found in those interpolations. Fresh `mkdtemp` gives a private 0700 parent, so a different unprivileged user cannot normally preplant shim files; same-user/PATH compromise is the relevant prerequisite.

**Repro (read-only source inspection):** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 34fe7aa70b627d92e2d27dbce308d9f5bebda63d:tools/round-72/seam-probe.py` and inspect `checker_env_arm`; `shutil.which` uses the caller PATH and follows executable symlinks by normal OS exec semantics.

**Impact:** untrusted tool provenance can invalidate environment evidence and execute unintended bytes. This is not a demonstrated remote exploit or a claim that the observed host PATH was hostile.

**Smallest remediation:** resolve approved absolute host tools under a trusted PATH before creating wrappers; use absolute `/usr/bin/cat`; validate/pin executable provenance if hostile same-user replacement is in scope. Keep deliberate test shims private and distinct from approved real tools.

**Wave evidence boundary:** inspected `ExecC1Base/harness.py:23-41,50-60,98-99`: its real tools are hardcoded `/usr/bin/{git,readelf}`, capture destination is generated scratch-owned `LOG`, environ is read-only data, and finally removes scratch. It retains key names plus HOME/TMPDIR/test canary, not arbitrary secret values. Its peer reported a shebang correction/rerun; do not treat intermediate result files as settled. Separately, the peer-produced `CriticClaims/c1-wrapper.json` reports `ok:true` while `real_child_canary_present:true`; this is corroborating **peer evidence**, not a test I executed or independently authenticated.

## SS72-2 — blocking: receipt-selected capsule paths read outside the lane

**Exploit path:** untrusted `child_env_observed.log` selects an absolute host filename, a `../` traversal, or a symlink to an outside file. Checker joins relative paths to root and only tests existence; it never proves resolved containment. The capsule reader opens the selected path and reads the entire file before parsing.

**Evidence:** frozen `packed-elf.py:821-835`; `capsule_audit.py:116-125`. Executed cases used harmless `/etc/hostname`: all three checker cases exit **1** with `capsule.ok:false`, `parse: line 1: JSONDecodeError`, and empty-record failures, **after reading** the outside bytes. Direct audit emits a SHA256 matching `/etc/hostname` (`outside_sha_matches:true`). This is an outside read, not an acceptance bypass. No sensitive file contents were retained.

**Repro:** run `probe.py` above; inspect `observations.json.capsule_paths.{absolute,traversal,symlink}` and `direct_outside_audit`. The traversal was `../../../../../etc/hostname` relative to lane root. The symlink was created only inside seat scratch and deleted.

**Impact:** receipt-controlled host-file read and digest disclosure; unbounded `.read()` also exposes a resource-exhaustion boundary for very large files/nonregular targets [INFERENCE, not exercised]. Explicit operator `--capsule` is a separate trusted-input capability and must not silently authorize receipt paths.

**Smallest remediation:** resolve receipt-derived paths against lane root, enforce resolved commonpath containment, require a regular bounded-size file and open without a symlink race. Reject escaped/missing receipt paths explicitly. Current code silently skips an absent receipt-named capsule (`exists` false gives `receipt_capsule:null`); this skip is source-observed, not separately executed here.

## SS72-3 — advisory: default temp allocation ignores supplied --work in one selftest

**Evidence:** all explicit `mkdtemp(...,dir=work)` sites honor the caller parent. Exceptions: checker fallback `packed-elf.py:615` uses default tempfile placement when --work is absent; `capsule-audit.py:128` uses `TemporaryDirectory()` and `main:171-172` does not forward --work to selftest. Both honor Python tempfile's TMPDIR selection, but fall back to the system temp directory if unset/unusable. Thus an assertion that every mode stays under --work is false. There is no literal hardcoded `/tmp` write found in these six instruments. The `/tmp` mentions in prose/pattern tests are not destinations.

**Repro (no extra temp write needed):** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 34fe7aa70b627d92e2d27dbce308d9f5bebda63d:tools/round-72/capsule-audit.py`; inspect `selftest` and `main`. The executed checker fallback test in `observations.json` allocated beneath explicit TMPDIR, confirming TMPDIR is honored.

**Impact:** unexpected placement when a caller supplies only --work to capsule selftest. Default tempfile directories are 0700, not world-writable; observed newly allocated instrument directories were 0700. Checker-created home/tmp under a caller-owned work were 0755, not world-writable.

**Smallest remediation:** forward --work into capsule selftest's TemporaryDirectory(dir=work), or require/set TMPDIR for every invocation and document fallback semantics.

## SS72-4 — advisory: fixed canary strings are committed fixtures, not secrets

**Evidence:** frozen tracked scan found four matches: round-71 probe, round-72 controls (`control-canary`), and two round-72 probe values (`probe-canary-r72`, `probe-canary`). Current lane grep also found source copies, knowledge text and peer evidence containing the values. The value can and does appear in committed files. Canary detection checks the **environment key**, not confidentiality of a random value.

**Repro:** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -F -e probe-canary-r72 -e probe-canary -e control-canary 34fe7aa70b627d92e2d27dbce308d9f5bebda63d -- .`

**Impact:** no disclosed credential is established by a literal match. A fixture-aware lying child can recognize the test; passing absence is not proof that arbitrary secrets never leak.

**Smallest remediation:** describe canary as a nonsecret test marker; do not use grep absence/presence as a secret-safety verdict. If unpredictability becomes a requirement, generate a per-run value instead of claiming these fixtures provide it.

## SS72-5 — blocking: SS-4 failure-cleanup contract is still violated

**Executed repro:** `probe.py` produced these retained-after-return directories, all subsequently removed by the seat's own finally cleanup:

- Checker with JSON root `[]`, no --work, and TMPDIR=S: rc **1**, leaked `kdk-check-ag9u1hbs`. Allocation occurs before root-type rejection and return at `packed-elf.py:632`; cleanup is only at 856-857. Failed git lookup at 637 has the same source-visible leak path.
- `controls.py` with nonexistent --receipt and valid --work: rc **2**, leaked `controls-sw336ung`. Allocation at 115 precedes missing-input return at 124; no cleanup anywhere. Missing packer return at 128 likewise leaks.
- `mutation-check.py` with frozen controls.py as non-selftesting target: rc **2**, leaked `mutation-check-p0c3q343`. Allocation at 157 precedes pristine rejection at 163; no cleanup anywhere.

**Additional source-observed paths:** `seam-probe.py` has no rmtree/finally for its `seam-probe-`, `a1-`, `a4-`, `a5-`, `a6-`, `a8-`, `a9-`, `a10-`, `a11-` trees; missing-tool A11 return leaves its allocation. `capsule-audit.py` retains `capsule-battery-` on both battery outcomes and exceptions (79-112). Mutation and controls trees likewise persist on success, apparently for evidence, but failures have no bounded cleanup ownership. `packed-elf.py` cleans typed preflight failure and its carrier-loop finally, but failures after preflight and before that finally (git metadata, missing/drifted REA package at 908-919) leave `packed-`. Skip-run deliberately retains a relative env-log tree at 956-960. These additional paths were not executed here. A9's communicate timeout also has no finally to terminate/reap the other Popen children [source-observed].

**Impact:** accumulated scratch, retained observations/fixture bytes, and potentially orphaned probe subprocesses. A caller's outer finally can contain the residue (as this review did), but does not make each instrument failure-clean.

**Smallest remediation:** cover every allocation and subprocess lifetime with an owning try/finally/TemporaryDirectory; copy explicitly requested evidence into receipt-owned storage first. Make intentional retention an explicit contract rather than relying on cleanup after only the happy path.

## SS72-6 — fixed-in-round: observed environ and receipt argv do not grant writes in reviewed paths

**Evidence:** frozen A11 derives record filenames from private scratch plus fixed tool names; `parse_environ_file` only opens input `rb`. Frozen A2 at `seam-probe.py:349-370` compares receipt argv to the independently supplied pinned packer and never copies to argv[0]. `controls.rebase` writes to caller-owned output and puts a supplied log path into receipt data; it does not write to that path. `ExecC1Base` likewise writes only its generated LOG. No QUALITY-120-style receipt-controlled copy/write destination was found in these paths. CLI output/capture destinations are operator inputs, a distinct trust boundary.

**Repro:** inspect frozen `seam-probe.py` with the git-show command in SS72-1, functions `parse_environ_file`, `checker_env_arm`, `check` A2; inspect `ExecC1Base/harness.py:23-41,50-60`.

**Impact/remediation:** the earlier receipt-grants-write pattern is absent in this scoped review; preserve that separation. This does not negate SS72-2's receipt-controlled **read**.

## Six-instrument coverage / limits

- `packed-elf.py`: child env/capture launcher, subprocess invocation, preflight pins/work, receipt provenance/capsule path, score and selftest allocation/cleanup reviewed; outside-read and checker early-exit executed.
- `seam-probe.py`: git extraction/import boundary, invocation, A1–A11 work parents, A2 receipt argv, A11 wrappers, concurrent Popen cleanup, validation/selftest/main inspected. Untrusted revision source executes by design; revision provenance remains caller responsibility.
- `mutation-check.py`: git extraction, pristine and mutation execution, scratch lifetime, receipt validation/output inspected; pristine failure executed.
- `capsule-audit.py`: JSON input/output, single audit, tamper-battery, selftest and CLI dispatch reviewed; battery cleanup and --work gap are static findings.
- `capsule_audit.py`: containment helper, parsing, child census, both summary shapes, seven clauses and tamper-shape generator reviewed; outside-file read executed. HOME/TMPDIR containment is lexical abspath/commonpath, not realpath, so it is not a symlink sandbox.
- `controls.py`: subprocess wrapper, receipt rebasing, pollution fixtures, all five control arms and allocation/output lifetime inspected; missing-input failure executed.

No offensive automation, external network, packer execution, full claim rerun, integration, or instrument edits were performed. No resume_continuity_v1 surface appears in the assigned six instruments; it was not expanded into this review.

Self-evaluation: accuracy 4/5 (static exploit paths clearly separated from executed and peer evidence); completeness 4/5 (all five assigned surfaces/six instruments covered; no hostile executable run by design); clarity 4/5 (frozen line references and one retained repro driver); actionability 4/5 (smallest fixes named, remediation not authorized); conciseness 4/5 (cleanup inventory necessarily spans several modes). Average 4.0. User-facing limits are explicit, not a readiness verdict.
