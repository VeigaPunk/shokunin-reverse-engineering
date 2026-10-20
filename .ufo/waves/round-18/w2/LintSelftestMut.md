BROKEN

# LintSelftestMut — frozen --selftest mutation probe

**[OBSERVATION]** Eight independent, single-line mutants: **6 survived, 2 killed, 0 inconclusive**. Every pristine and restored detector run exited 0 with `SELFTEST: CLEAN cases=3`. Every survivor also changed a separate, bounded semantic witness; these are non-equivalent mutants. The killed controls detect zero-caller misclassification and loss of `compare-only`.

**Scope/calibration:** Author-side advisory finding about `--selftest` regression coverage, **not** a finding that C2’s measured 3→0 live-site delta or jj sandbox claim is false. No round judgment, integration, source fix, or contract change. No delegation, REA/Ghidra/OMP invocation, carrier execution, installation, or tool update.

**Axes:** calibration (bounded verdict, no C2 overclaim); operability (exact commands and restoration); depth (context, annotation, and wrapper witnesses).

## Frozen source and detector

- REV: `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Every source anchor below refers to `.ufo/waves/round-18/tools/head-rev-lint.py` **at this REV**, not the moving worktree. Source was opened with `git show REV:path`; isolated checkouts match its SHA-256.
- Expected detector: the unchanged `--selftest` CLI should exit nonzero for a behavioral regression in the documented context/annotation/wrapper rules. Its red fixture asserts live=15, fixture=4, annotated=1 at `.ufo/waves/round-18/tools/head-rev-lint.py:832-836`; callback/uncalled helper cases are at `:715-747`, `:851-854`.
- The documented contract includes wrapper calls (`.ufo/waves/round-18/tools/head-rev-lint.py:14-18`), both annotation names (`:36-40`), and Python `/fixtures/` paths (`:41-46`). The selftest docstring claims “both annotations” at `:62-65`; M03 falsifies that coverage claim, while M04 is killed. The exercised fixture-path file is shell-only (`:856-858`), consistent with the M07 blind spot.
- Scratch: `/tmp/r18-lintselftest-pMJ9ju7k/{M01,…,M08}`, eight separate `git clone --shared --no-checkout` copies. Each had `origin` removed before target checkout. Test-created repositories stayed beneath that clone via `TMPDIR`; no lane Git writes or lane-source edits. Only this report is written in the lane.

## Mutants and observed verdicts

P/M/R = pristine / mutated / exact-byte-restored exit codes. Every mutant’s expected outcome is nonzero.

| Mutant | Frozen source anchor | One-point defect | P/M/R | Verdict |
|---|---|---|---|---|
| M01 | `.ufo/waves/round-18/tools/head-rev-lint.py:518` | Ignore non-call live references to helpers | 0 / 0 / 0 | **SURVIVED** |
| M02 | `.ufo/waves/round-18/tools/head-rev-lint.py:518` | Treat zero-caller functions as fixture-eligible | 0 / 1 / 0 | **KILLED** |
| M03 | `.ufo/waves/round-18/tools/head-rev-lint.py:114` | Stop recognizing red-before | 0 / 0 / 0 | **SURVIVED** |
| M04 | `.ufo/waves/round-18/tools/head-rev-lint.py:114` | Stop recognizing compare-only | 0 / 1 / 0 | **KILLED** |
| M05 | `.ufo/waves/round-18/tools/head-rev-lint.py:421` | Dispatch wrappers against the enclosing function stack | 0 / 0 / 0 | **SURVIVED** |
| M06 | `.ufo/waves/round-18/tools/head-rev-lint.py:467` | Discard assignment-built wrappers instead of registering them | 0 / 0 / 0 | **SURVIVED** |
| M07 | `.ufo/waves/round-18/tools/head-rev-lint.py:528` | Miss the Python /fixtures/ path context | 0 / 0 / 0 | **SURVIVED** |
| M08 | `.ufo/waves/round-18/tools/head-rev-lint.py:282` | Skip the subcommand along with the dynamic repo argument | 0 / 0 / 0 | **SURVIVED** |

Exact substitutions (indentation preserved; one substitution per independent copy):

**M01 — context classifier**
```diff
-            if cs and cs <= fixture and (not refs or refs <= fixture):
+            if cs and cs <= fixture:
```
**M02 — context classifier**
```diff
-            if cs and cs <= fixture and (not refs or refs <= fixture):
+            if cs <= fixture and (not refs or refs <= fixture):
```
**M03 — annotation rule**
```diff
-    r"head-rev-lint:\s*(compare-only|red-before)"
+    r"head-rev-lint:\s*(compare-only)"
```
**M04 — annotation rule**
```diff
-    r"head-rev-lint:\s*(compare-only|red-before)"
+    r"head-rev-lint:\s*(red-before)"
```
**M05 — wrapper detection**
```diff
-        if name in self.wrappers:
+        if name in self.func_stack:
```
**M06 — wrapper detection**
```diff
-                scanner.wrappers.add(node.name)
+                scanner.wrappers.discard(node.name)
```
**M07 — context classifier**
```diff
-    if "/fixtures/" in path:
+    if "/fixture/" in path:
```
**M08 — wrapper detection**
```diff
-            args = args[1:]  # skip the root/repo argument
+            args = args[2:]  # skip the root/repo argument
```

## Detector commands and actual output

Each exact command below ran three times, once in each P/M/R state from its corresponding clone. The command and 60-second bound were unchanged; no `-O`, exception suppression, altered assertions, or detector edits. All 24 stderr streams were empty.

```sh
timeout 60s env TMPDIR=/tmp/r18-lintselftest-pMJ9ju7k/M01 python3 -I -B /tmp/r18-lintselftest-pMJ9ju7k/M01/.ufo/waves/round-18/tools/head-rev-lint.py --selftest  # P=0; M=0; R=0
timeout 60s env TMPDIR=/tmp/r18-lintselftest-pMJ9ju7k/M02 python3 -I -B /tmp/r18-lintselftest-pMJ9ju7k/M02/.ufo/waves/round-18/tools/head-rev-lint.py --selftest  # P=0; M=1; R=0
timeout 60s env TMPDIR=/tmp/r18-lintselftest-pMJ9ju7k/M03 python3 -I -B /tmp/r18-lintselftest-pMJ9ju7k/M03/.ufo/waves/round-18/tools/head-rev-lint.py --selftest  # P=0; M=0; R=0
timeout 60s env TMPDIR=/tmp/r18-lintselftest-pMJ9ju7k/M04 python3 -I -B /tmp/r18-lintselftest-pMJ9ju7k/M04/.ufo/waves/round-18/tools/head-rev-lint.py --selftest  # P=0; M=1; R=0
timeout 60s env TMPDIR=/tmp/r18-lintselftest-pMJ9ju7k/M05 python3 -I -B /tmp/r18-lintselftest-pMJ9ju7k/M05/.ufo/waves/round-18/tools/head-rev-lint.py --selftest  # P=0; M=0; R=0
timeout 60s env TMPDIR=/tmp/r18-lintselftest-pMJ9ju7k/M06 python3 -I -B /tmp/r18-lintselftest-pMJ9ju7k/M06/.ufo/waves/round-18/tools/head-rev-lint.py --selftest  # P=0; M=0; R=0
timeout 60s env TMPDIR=/tmp/r18-lintselftest-pMJ9ju7k/M07 python3 -I -B /tmp/r18-lintselftest-pMJ9ju7k/M07/.ufo/waves/round-18/tools/head-rev-lint.py --selftest  # P=0; M=0; R=0
timeout 60s env TMPDIR=/tmp/r18-lintselftest-pMJ9ju7k/M08 python3 -I -B /tmp/r18-lintselftest-pMJ9ju7k/M08/.ufo/waves/round-18/tools/head-rev-lint.py --selftest  # P=0; M=0; R=0
```

Pristine and restored stdout for every copy, and mutated stdout for M01/M03/M05/M06/M07/M08 (verbatim):

```text
SELFTEST: CLEAN cases=3
```

The killed mutants fail the live-count assertion at `.ufo/waves/round-18/tools/head-rev-lint.py:833-834`: M02 reports 4 rather than 15; M04 reports 16 rather than 15. Complete captured stdout is retained below.

## Non-equivalence witnesses for every survivor

**[OBSERVATION]** The same auxiliary `-c` payload ran on pristine M01, on each surviving mutant, and on restored M01. All eight witness executions exited 0 with empty stderr. It only imports the linter and scans strings; the embedded git snippets are not executed. Hash identity binds the shared pristine/restored witness to all eight copies. These are diagnostics; mutation verdicts come only from unchanged `--selftest`.

| Mutant | Witness key | Pristine/restored value | Mutated value |
|---|---|---|---|
| M01 | `callback_ref` | `[{"context":"live","kind":"rev-parse-HEAD","line":5}]` | `[{"context":"fixture","kind":"rev-parse-HEAD","line":5}]` |
| M03 | `red_before` | `["annotated","head-rev-lint: red-before"]` | `["live",null]` |
| M05 | `wrapper_direct` | `[{"context":"live","kind":"rev-parse-HEAD","line":5}]` | `[]` |
| M06 | `wrapper_assigned` | `[{"context":"live","kind":"rev-parse-HEAD","line":6}]` | `[]` |
| M07 | `fixture_path` | `["fixture","path contains /fixtures/"]` | `["live",null]` |
| M08 | `wrapper_root` | `[{"context":"live","kind":"rev-parse-HEAD","line":5}]` | `[]` |

**[INFERENCE]** M01 can hide a live callback helper as fixture-only; M05/M06/M08 can drop live wrapper-derived sites. M03 can count an annotated reproduction as live; M07 can count a Python fixture as live. These are regression risks proved under mutation, not assertions that pristine code already has those defects.

Reproduction: materialize the pinned target in an origin-free scratch clone (setup transcript below), apply only the corresponding exact substitution, run its recorded detector command, then restore the line. The common witness argument is shown in full. `WITNESS` below denotes these exact `-c` argument bytes; no witness file was written.

```python
import json, runpy, sys
m = runpy.run_path(sys.argv[1], run_name='lint_mutation_witness')
def sites(src, path='.ufo/waves/round-17/probe.py'):
    found, fixtures = m['scan_python'](src)
    return [{'line': n, 'kind': kind, 'context': m['python_context'](path, n, enclosing, fixtures, src.splitlines())[0]} for n, kind, enclosing in found]
callback = 'import subprocess\ndef selftest():\n    helper()\ndef helper():\n    subprocess.run(["git", "rev-parse", "HEAD"])\nLIVE_CALLBACK = helper\n'
direct = 'import subprocess\ndef git(*args):\n    return subprocess.run(["git"] + list(args))\ndef main():\n    git("rev-parse", "HEAD")\n'
assigned = 'import subprocess\ndef git(*args):\n    argv = ["git"] + list(args)\n    return subprocess.run(argv)\ndef main():\n    git("rev-parse", "HEAD")\n'
root = 'import subprocess\ndef git_in(repo, *args):\n    return subprocess.run(["git", "-C", repo] + list(args))\ndef main(repo):\n    git_in(repo, "rev-parse", "HEAD")\n'
print(json.dumps({'callback_ref': sites(callback), 'red_before': m['python_context']('.ufo/waves/round-17/probe.py', 1, ('probe',), set(), ['subprocess.run(["git", "rev-parse", "HEAD"]) # head-rev-lint: red-before']), 'wrapper_direct': sites(direct), 'wrapper_assigned': sites(assigned), 'fixture_path': m['python_context']('.ufo/waves/round-17/fixtures/probe.py', 1, (), set(), ['subprocess.run(["git", "rev-parse", "HEAD"])']), 'wrapper_root': sites(root)}, sort_keys=True))
```

Witness command invocations (payload passed directly as one argument, represented by `WITNESS`):

```sh
timeout 15s python3 -I -B -c "$WITNESS" /tmp/r18-lintselftest-pMJ9ju7k/M01/.ufo/waves/round-18/tools/head-rev-lint.py  # pristine exit=0
timeout 15s python3 -I -B -c "$WITNESS" /tmp/r18-lintselftest-pMJ9ju7k/M01/.ufo/waves/round-18/tools/head-rev-lint.py  # mutated exit=0
timeout 15s python3 -I -B -c "$WITNESS" /tmp/r18-lintselftest-pMJ9ju7k/M03/.ufo/waves/round-18/tools/head-rev-lint.py  # mutated exit=0
timeout 15s python3 -I -B -c "$WITNESS" /tmp/r18-lintselftest-pMJ9ju7k/M05/.ufo/waves/round-18/tools/head-rev-lint.py  # mutated exit=0
timeout 15s python3 -I -B -c "$WITNESS" /tmp/r18-lintselftest-pMJ9ju7k/M06/.ufo/waves/round-18/tools/head-rev-lint.py  # mutated exit=0
timeout 15s python3 -I -B -c "$WITNESS" /tmp/r18-lintselftest-pMJ9ju7k/M07/.ufo/waves/round-18/tools/head-rev-lint.py  # mutated exit=0
timeout 15s python3 -I -B -c "$WITNESS" /tmp/r18-lintselftest-pMJ9ju7k/M08/.ufo/waves/round-18/tools/head-rev-lint.py  # mutated exit=0
timeout 15s python3 -I -B -c "$WITNESS" /tmp/r18-lintselftest-pMJ9ju7k/M01/.ufo/waves/round-18/tools/head-rev-lint.py  # restored exit=0
```

## Byte restoration evidence

**[OBSERVATION]** Common pristine SHA-256, all eight restored copies, and lane target before/after:

```text
5ada7b837368a92e9b7813a37529e476acbf7ce6b1fa62dc9d3ee63ee6c68e36
```

The frozen Git object independently hashes to that same value. Every mutant was reverted with the exact inverse one-line edit even when its detector failed; all restored detector runs returned `SELFTEST: CLEAN cases=3`. The lane target was never mutated.

| Copy | Pristine | Mutated SHA-256 | Restored |
|---|---|---|---|
| M01 | common hash | `569944970e25f524a84065326bf2e01af0db4fd0f8a00b6420ea313a701c1e32` | common hash |
| M02 | common hash | `9ed67b6bfc90cfb3613da7f989814e5afc0641c39f62f12f980e6b1467af6cff` | common hash |
| M03 | common hash | `6ee672e6762d0010b205850fa8b486719baa03e944de737deb13492cd53d751a` | common hash |
| M04 | common hash | `e87a9bbd3f1547bae77e9ffdeac75d035103e7bc2468d16c84cbcf4f460a78ed` | common hash |
| M05 | common hash | `be3a8d9df49cb65a0798e197e1251301421a571f0ac0509d4437408cfdea2968` | common hash |
| M06 | common hash | `3472134468686cd49f1049eabed60b9fa6c53906855300bce0d407a0ad3e9c08` | common hash |
| M07 | common hash | `ede3a34b201bc4a424aa03adbfc881c8b4c921720844dd9e29cd153822692d8b` | common hash |
| M08 | common hash | `839f2880589ea615c9167a51f51fba65169fb3b82a83d29a739150b46cc07813` | common hash |

Hash commands (actual argv, all exit 0; first/last include lane target):

```sh
sha256sum /tmp/r18-lintselftest-pMJ9ju7k/M01/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M02/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M03/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M04/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M05/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M06/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M07/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M08/.ufo/waves/round-18/tools/head-rev-lint.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/head-rev-lint.py  # pristine exit=0
sha256sum /tmp/r18-lintselftest-pMJ9ju7k/M01/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M02/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M03/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M04/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M05/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M06/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M07/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M08/.ufo/waves/round-18/tools/head-rev-lint.py  # mutated exit=0
sha256sum /tmp/r18-lintselftest-pMJ9ju7k/M01/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M02/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M03/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M04/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M05/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M06/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M07/.ufo/waves/round-18/tools/head-rev-lint.py /tmp/r18-lintselftest-pMJ9ju7k/M08/.ufo/waves/round-18/tools/head-rev-lint.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/head-rev-lint.py  # restored exit=0
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/head-rev-lint.py | sha256sum  # exit=0; common hash above
```

## Setup and tool command transcript

Read-only frozen-source command, run from the lane (exit 0):

```sh
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/head-rev-lint.py
```

Scratch creation (exit 0; stdout `/tmp/r18-lintselftest-pMJ9ju7k`):

```sh
mktemp -d -t r18-lintselftest-XXXXXXXX
```

<details><summary>Clone isolation commands — all observed exit 0</summary>

Commands ran concurrently across clones, sequentially within each clone.

```sh
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-lintselftest-pMJ9ju7k/M01  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M01 remote remove origin  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M01 checkout b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/tools/head-rev-lint.py  # exit=0
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-lintselftest-pMJ9ju7k/M02  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M02 remote remove origin  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M02 checkout b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/tools/head-rev-lint.py  # exit=0
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-lintselftest-pMJ9ju7k/M03  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M03 remote remove origin  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M03 checkout b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/tools/head-rev-lint.py  # exit=0
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-lintselftest-pMJ9ju7k/M04  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M04 remote remove origin  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M04 checkout b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/tools/head-rev-lint.py  # exit=0
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-lintselftest-pMJ9ju7k/M05  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M05 remote remove origin  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M05 checkout b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/tools/head-rev-lint.py  # exit=0
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-lintselftest-pMJ9ju7k/M06  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M06 remote remove origin  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M06 checkout b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/tools/head-rev-lint.py  # exit=0
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-lintselftest-pMJ9ju7k/M07  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M07 remote remove origin  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M07 checkout b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/tools/head-rev-lint.py  # exit=0
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-lintselftest-pMJ9ju7k/M08  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M08 remote remove origin  # exit=0
git -C /tmp/r18-lintselftest-pMJ9ju7k/M08 checkout b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/tools/head-rev-lint.py  # exit=0
```

</details>

Installed tools were reused; no installs/updates. Observed version commands:

```text
python3 -I -B --version  # exit=0: Python 3.14.8
git --version           # exit=0: git version 2.56.0
timeout --version       # exit=0: timeout (GNU coreutils) 9.12
```

## Complete failing detector stdout

Both payloads ended with one newline and had empty stderr.

<details><summary>M02 — exit 1; stdout 4090 bytes; SHA-256 d350aa5ff5e00b765c0e2fb07cad1fafe4f0b1685b04a3ded4c9ea5cf6f07516</summary>

```text
SELFTEST: FAILED (4, [{'path': '.ufo/gates/run.sh', 'line': 3, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'R=$(git rev-parse HEAD)'}, {'path': '.ufo/gates/run.sh', 'line': 4, 'kind': 'upstream', 'context': 'live', 'code': 'git rev-parse @{u}'}, {'path': '.ufo/gates/run.sh', 'line': 5, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'V=${REV:-HEAD}; git rev-parse "$V"'}, {'path': '.ufo/gates/run.sh', 'line': 6, 'kind': 'HEAD-colon', 'context': 'live', 'code': 'git show HEAD:LOG.md'}, {'path': '.ufo/waves/round-17/ctx.py', 'line': 5, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "rev-parse", "HEAD"])', 'reason': 'enclosing function selftest()'}, {'path': '.ufo/waves/round-17/ctx.py', 'line': 8, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "rev-parse", "HEAD"])', 'reason': 'enclosing function selftest()'}, {'path': '.ufo/waves/round-17/ctx.py', 'line': 12, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "-C", "r", "rev-parse", "HEAD"])', 'reason': 'enclosing function build_fixture_repo()'}, {'path': '.ufo/waves/round-17/ctx.py', 'line': 17, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"])', 'reason': 'called only from selftest/fixture functions (_commit())'}, {'path': '.ufo/waves/round-17/ctx2.py', 'line': 9, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"])', 'reason': 'called only from selftest/fixture functions (_commit())'}, {'path': '.ufo/waves/round-17/ctx2.py', 'line': 13, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "-C", ".", "rev-parse", "HEAD"])', 'reason': 'called only from selftest/fixture functions (live_helper())'}, {'path': '.ufo/waves/round-17/edge.py', 'line': 5, 'kind': 'HEAD-colon', 'context': 'fixture', 'code': 'subprocess.run(["git", "show", f"HEAD:{path}"])', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/edge.py', 'line': 6, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "rev-parse", "HEAD^{commit}"])', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/edge.py', 'line': 7, 'kind': 'other-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "log", "--format=%H", "HEAD~3"])', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/edge.py', 'line': 8, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "rev-parse", "@"])', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/live.py', 'line': 6, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "-C", ".", "rev-parse", "HEAD"])', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/live.py', 'line': 7, 'kind': 'upstream', 'context': 'fixture', 'code': 'subprocess.run(["git", "branch", "--show-current"])', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/live.py', 'line': 8, 'kind': 'HEAD-colon', 'context': 'fixture', 'code': 'subprocess.run(["git", "show", "HEAD:LOG.md"])', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/live.py', 'line': 9, 'kind': 'other-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "rev-list", "HEAD"])', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/live.py', 'line': 11, 'kind': 'default-HEAD', 'context': 'fixture', 'code': 'ap.add_argument("--rev", default="HEAD")', 'reason': 'called only from selftest/fixture functions (main())'}, {'path': '.ufo/waves/round-17/live.py', 'line': 15, 'kind': 'rev-parse-HEAD', 'context': 'annotated', 'code': 'subprocess.run(["git", "rev-parse", "HEAD"])  # head-rev-lint: compare-only', 'reason': 'head-rev-lint: compare-only'}])
```

</details>

<details><summary>M04 — exit 1; stdout 3276 bytes; SHA-256 0397f96c579c4f5fd63f61fc7262dd3f926c41fd3001e383236cd2f16b014a70</summary>

```text
SELFTEST: FAILED (16, [{'path': '.ufo/gates/run.sh', 'line': 3, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'R=$(git rev-parse HEAD)'}, {'path': '.ufo/gates/run.sh', 'line': 4, 'kind': 'upstream', 'context': 'live', 'code': 'git rev-parse @{u}'}, {'path': '.ufo/gates/run.sh', 'line': 5, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'V=${REV:-HEAD}; git rev-parse "$V"'}, {'path': '.ufo/gates/run.sh', 'line': 6, 'kind': 'HEAD-colon', 'context': 'live', 'code': 'git show HEAD:LOG.md'}, {'path': '.ufo/waves/round-17/ctx.py', 'line': 5, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "rev-parse", "HEAD"])', 'reason': 'enclosing function selftest()'}, {'path': '.ufo/waves/round-17/ctx.py', 'line': 8, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "rev-parse", "HEAD"])', 'reason': 'enclosing function selftest()'}, {'path': '.ufo/waves/round-17/ctx.py', 'line': 12, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'subprocess.run(["git", "-C", "r", "rev-parse", "HEAD"])', 'reason': 'enclosing function build_fixture_repo()'}, {'path': '.ufo/waves/round-17/ctx.py', 'line': 17, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"])'}, {'path': '.ufo/waves/round-17/ctx2.py', 'line': 9, 'kind': 'rev-parse-HEAD', 'context': 'fixture', 'code': 'return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"])', 'reason': 'called only from selftest/fixture functions (_commit())'}, {'path': '.ufo/waves/round-17/ctx2.py', 'line': 13, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'subprocess.run(["git", "-C", ".", "rev-parse", "HEAD"])'}, {'path': '.ufo/waves/round-17/edge.py', 'line': 5, 'kind': 'HEAD-colon', 'context': 'live', 'code': 'subprocess.run(["git", "show", f"HEAD:{path}"])'}, {'path': '.ufo/waves/round-17/edge.py', 'line': 6, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'subprocess.run(["git", "rev-parse", "HEAD^{commit}"])'}, {'path': '.ufo/waves/round-17/edge.py', 'line': 7, 'kind': 'other-HEAD', 'context': 'live', 'code': 'subprocess.run(["git", "log", "--format=%H", "HEAD~3"])'}, {'path': '.ufo/waves/round-17/edge.py', 'line': 8, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'subprocess.run(["git", "rev-parse", "@"])'}, {'path': '.ufo/waves/round-17/live.py', 'line': 6, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'subprocess.run(["git", "-C", ".", "rev-parse", "HEAD"])'}, {'path': '.ufo/waves/round-17/live.py', 'line': 7, 'kind': 'upstream', 'context': 'live', 'code': 'subprocess.run(["git", "branch", "--show-current"])'}, {'path': '.ufo/waves/round-17/live.py', 'line': 8, 'kind': 'HEAD-colon', 'context': 'live', 'code': 'subprocess.run(["git", "show", "HEAD:LOG.md"])'}, {'path': '.ufo/waves/round-17/live.py', 'line': 9, 'kind': 'other-HEAD', 'context': 'live', 'code': 'subprocess.run(["git", "rev-list", "HEAD"])'}, {'path': '.ufo/waves/round-17/live.py', 'line': 11, 'kind': 'default-HEAD', 'context': 'live', 'code': 'ap.add_argument("--rev", default="HEAD")'}, {'path': '.ufo/waves/round-17/live.py', 'line': 15, 'kind': 'rev-parse-HEAD', 'context': 'live', 'code': 'subprocess.run(["git", "rev-parse", "HEAD"])  # head-rev-lint: compare-only'}])
```

</details>

## Handoff

Six surviving mutants identify missing assertions for live callback references, `red-before`, wrapper dispatch/discovery/argument slicing, and Python fixture-path classification. No production change is proposed or made by this seat. All assigned probes and required restoration runs are complete.
