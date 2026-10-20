# Sandbox/security review — round 19 wave 2

**Scope:** audited the baseline-to-main changes in the four `.ufo/waves/round-19/tools/*.py` files, `.ufo/waves/round-18/tools/jj-red-before.py`, `.ufo/gates/citation-drift/citation-drift-probe.py`, and `.ufo/gates/custody-pair/custody-pair.py`.

**Axes:** calibration (scope and finding confidence), freshness (pinned source tip), depth (adversarial path/environment checks).

**Freshness / commands:** observed `refs/heads/main` at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; comparison base was `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`.

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
exit=0  d0690fd44f46d8a7fe9da5f01c6be723d12abd41

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --numstat 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- .ufo/waves/round-19/tools/routed-r18.py .ufo/waves/round-19/tools/province-pins.py .ufo/waves/round-19/tools/wave-outcomes.py .ufo/waves/round-19/tools/rea-catalog.py .ufo/waves/round-18/tools/jj-red-before.py .ufo/gates/citation-drift/citation-drift-probe.py .ufo/gates/custody-pair/custody-pair.py
exit=0
```

The only behavioral probes ran in `/tmp/kr19-w2-sandboxsecurity.f3wksQ/clone`, cloned without hardlinks and checked out at that observed tip; the scratch clone was removed (`rm -rf -- /tmp/kr19-w2-sandboxsecurity.f3wksQ`, exit 0). No lane code was edited. No carrier, REA, Ghidra, build, or broad suite was run; no tools were installed.

## Findings

### High (conditional) — inspection tools execute target-controlled code with caller privileges

**Observation:** `routed-r18.py` extracts Git-revision content and imports it with `spec.loader.exec_module` (`.ufo/waves/round-19/tools/routed-r18.py:63-85`). The checker imports `receipt-validate.py` and `routed-defects.py` from the selected revision (`:90-95`, `:118-127`), and runs the extracted citation probe (`:192-206`). `jj-red-before.py` executes baseline/fixed Python probes and imports the selected `revpin.py` directly into its process (`.ufo/waves/round-18/tools/jj-red-before.py:516-523`, `:580-599`, `:643-648`, `:764-772`). `rea-catalog.py` imports modules from the selected npx cache and runs its `scripts/rea.mjs` (`.ufo/waves/round-19/tools/rea-catalog.py:51-66`, `:106-153`). Those imports/launches are real code execution, not static inspection. Python `-I -B` does not sandbox filesystem/network access. The `rea-catalog.py` Node subprocess does not set a restricted `env`; `jj-red-before.py` removes `GIT_*`, `JJ_*`, and `TMPDIR` but otherwise inherits the caller environment (`:123-138`, `:189-205`). Its child stdout/stderr are retained in the receipt.

**Exploit path:** run a checker against a tainted Git revision, modified probe path, or poisoned npx cache. Module initialization / CLI code can read available credentials, alter files outside the clone, or use the network; retained output can also carry data into the receipt. This is conditional on selecting malicious target code, not evidence that the current target is malicious.

**Impact [INFERENCE]:** these are not safe read-only analyzers for untrusted inputs; a malicious source/cache can compromise the invoking user's files and secrets despite the clone/write guards.

**Smallest remediation:** statically inspect authenticated source where possible; otherwise execute only digest-pinned inputs in a disposable OS sandbox with a minimal environment, read-only inputs, no network, and a bounded writable scratch directory. Do not describe `-I` or `--no-local` as a code-execution boundary.

**Carrier check:** no scoped code launches the Go 1.25 carrier executables. `inspect-go-binary`/`analyze` appear as fixture strings only (`routed-r18.py:99-102`); there is no Go binary path or direct execution call in the inspected tools.

### Medium — snapshot slug escapes the declared snapshot directory

**Observation:** citation targets beginning `@` are passed to `_snapshot` (`.ufo/gates/citation-drift/citation-drift-probe.py:145-155`). `_snapshot` joins the caller/table-provided `slug` to `snapshot_dir` without rejecting absolute paths, separators, or `..` (`:159-185`). A digest check follows the file read, but a table/expected pair that pins the escaped file is accepted.

**Adversarial probe:** in the isolated clone, supplied `file: "@../canary.txt"`, a matching table digest, and a matching snapshot digest, with `canary.txt` outside `snap/`. The tool read that file and returned `CITATION_DRIFT_VERDICT: clean`, exit 0. Executed argv was:

```text
python3 -I -B /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --table /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.sandbox-security-probe/pointer-table.json --expected /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.sandbox-security-probe/expected.json --snapshot-dir /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.sandbox-security-probe/snap --strict
exit=0
```

**Impact [INFERENCE]:** a crafted pointer-table/expected pair can make the probe read and fingerprint a local file outside the snapshot root; finding behavior can be used as a content-match oracle. This is read escape, not a demonstrated write.

**Smallest remediation:** require a single safe basename for each slug and verify the resolved file remains beneath the resolved snapshot root before opening it.

### Medium — predictable temporary output follows a planted symlink

**Observation:** `wave-outcomes.py` writes to the predictable sibling `f"{path}.tmp.{pid}"` with ordinary `open(..., "w")`, then replaces the requested output (`.ufo/waves/round-19/tools/wave-outcomes.py:356-365`). A symlink at the temporary name is followed before `os.replace`.

**Adversarial probe:** in the isolated clone, a harness created `receipt.json.tmp.<child-pid>` as a symlink to a synthetic `victim.txt`, then `exec`'d the tool with `--out receipt.json`. The CLI returned exit 0, overwrote `victim.txt` with the outcome JSON, and left `receipt.json` as a symlink to the victim. The child argv was:

```text
python3 -I -B /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.ufo/waves/round-19/tools/wave-outcomes.py --registration /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.sandbox-security-probe/registration.json --report-dir /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.sandbox-security-probe/reports --causes /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.sandbox-security-probe/causes.json --out /tmp/kr19-w2-sandboxsecurity.f3wksQ/clone/.sandbox-security-probe/receipt.json
exit=0; victim_overwritten=true; receipt_symlink=true
```

`rea-catalog.py` has the same class of issue with the fixed `<out>.tmp` name and `write_text` before `os.replace` (`.ufo/waves/round-19/tools/rea-catalog.py:253-260`).

**Impact [INFERENCE]:** a local actor able to plant the temp-name symlink in the output directory can redirect the tool's write to another file accessible to the invoking user; the PID suffix makes the wave-outcomes case race/prediction-dependent, while the rea-catalog name is fixed.

**Smallest remediation:** create a unique temporary file in the destination directory using exclusive creation (`mkstemp`/`O_EXCL`, no-follow), write it, then atomically replace the requested output.

### Medium — inherited Git/temp environment can redirect evidence and scratch writes

**Observation:** the Git subprocesses in `province-pins.py` (`:118-142`), `routed-r18.py` (`:46-53`), citation-drift (`:120-124`, `:284-317`), and custody-pair (`.ufo/gates/custody-pair/custody-pair.py:368-379`) omit an explicit environment. `--no-optional-locks` does not neutralize `GIT_DIR`, `GIT_WORK_TREE`, or related Git variables. `routed-r18.py` also calls `tempfile.mkdtemp(prefix="kr19-routed-")` without an explicit safe directory (`:292-307`); Python's temp selection honors `TMPDIR`. In contrast, `jj-red-before.py` explicitly filters `GIT_*`, `JJ_*`, `TMPDIR` and fixes its sandbox under `/tmp` (`:123-138`, `:296-313`).

**Exploit path:** invoke an otherwise read-only checker with Git environment overrides to make `git -C <root>` inspect another repository; set `TMPDIR` to the lane and run `routed-r18.py` to place its transient extraction directory inside the lane. The temp write is later removed, but it is still an unsandboxed repo write during execution.

**Impact [INFERENCE]:** false or misleading revision evidence, and environment-dependent writes outside the intended scratch boundary. No such environment override was applied during this audit.

**Smallest remediation:** provide a clean allowlisted environment for Git and set scratch directories explicitly to a validated path outside the lane/fleet root; use an absolute trusted Git executable if executable-path integrity is required.

## Data handling and non-applicable contract

- **Observation:** `province-pins.py` emits config paths, parsed REA pin tokens, a whole-file SHA-256, and mtime—not config bytes (`:203-231`, `:310-325`); its self-test checks a synthetic secret sentinel is absent (`:402-418`). No credential values or real config contents were emitted by this audit. `custody-pair.py` records host/user/cwd, paths, hashes, metadata, and symlink targets (`.ufo/gates/custody-pair/custody-pair.py:325-360`, `:424-463`), not file contents. `wave-outcomes.py` deliberately copies caller-provided cause/source text into its JSON result (`.ufo/waves/round-19/tools/wave-outcomes.py:179-203`, `:328-350`); treat that record as potentially sensitive and untrusted, although those fields are JSON data, not shell input.
- **Resume contract:** canonical `run-logic.md` §2.1 (`/home/vgpnk/Projects/ufo-fsd-alpha/skills/ufo/references/run-logic.md:177-197`) requires exact stable session identity plus matching agent/cwd and zero mutation on missing/mismatched evidence. None of the scoped tools implements session selection/resume or run-state/pane mutation, so there is no `resume_continuity_v1` rejection path here to exercise; the zero-mutation check is not applicable to this surface.
- **Intentional writes:** `--out` in `wave-outcomes.py`, `rea-catalog.py`, `jj-red-before.py`, and `custody-pair.py` is an explicit caller-selected output path. I did not treat a requested output outside the lane as an implicit write; the symlink findings concern redirection away from the requested destination.
