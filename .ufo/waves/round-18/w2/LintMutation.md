HOLDS

# LintMutation — three isolated single-file reverts

**Axes:** calibration (observed vs inferred), operability (bounded reproducer), depth (independent regression sensitivity). Author-side advisory probe only; no claim admission or outside review.

## Scope and result

[OBSERVATION] Pinned delivered revision: `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; baseline bytes: `9011581d84527ba34c675f9cf912e54d2e72d470`. Three independent `mktemp -d` clones were exercised concurrently. Each clone had its origin removed before checkout/mutation. Only the assigned file was reverted in each mutant commit. The detector itself was never changed.

[OBSERVATION] All three pristine controls passed. Each single-file baseline-byte mutant produced **exactly one live site** and strict exit **1**; every restored control returned zero live sites and exit **0**. Verdicts: **3 killed, 0 survived, 0 inconclusive**. The same detector command was used throughout, bounded by `timeout 30s`; only its revision operand changed. No carrier binaries, REA/Ghidra analysis, jj, or orchestration runtime were invoked. Git/Python detector commands were controlled through the provided Eval tool. No tools were installed or updated.

[INFERENCE] The lint is sensitive to these three complete-file regressions independently. This does not establish sensitivity to arbitrary alternative HEAD constructions or prove the tools’ jj runtime behavior.

## Pinned source anchors

All anchors below are from successful `git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:PATH` calls, not the mutable lane worktree:

- `.ufo/waves/round-18/tools/head-rev-lint.py:54-60`: output/strict-exit contract; `:663-675`: live/fixture/annotated counting; `:679-682`: strict exit 1 iff live count is positive.
- `.ufo/gates/citation-drift/citation-drift-probe.py:311-317` documents branch-tip/default handling; `:590-595` changes `--rev` to `default=None` with `--branch main`.
- `.ufo/gates/custody-pair/custody-pair.py:364-368` documents the contextualized HEAD read; `:407-411` emits the retained HEAD and explicit branch-tip/equality facts; `:1436-1439` defaults `--repo` to the lane root.
- `.ufo/waves/round-17/verify.py:70-80` pins source to `refs/heads/<branch>`; `:90-95` records branch/HEAD/remote refusals.
- `.ufo/waves/round-18/contract.md:150` states the amended fixture/annotation/exclusion rules. These rules were not modified for this probe.

The live-site line numbers below belong to the **mutant/baseline blobs**, not to the delivered revision; the distinction is intentional.

## Actual detector outputs (selected JSON fields)

Detector stdout was valid JSON in all nine runs; stderr was empty in all nine. The table transcribes actual fields; full stdout also included sites, exclusions and limitations. All runs reported `files_scanned=39`.

| Assigned file | Stage / revision | Exit | live | fixture | annotated | Verdict |
|---|---|---:|---:|---:|---:|---|
| `.ufo/gates/citation-drift/citation-drift-probe.py` | pristine `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` | 0 | 0 | 15 | 6 | control passed |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | mutated `9ddcf3f46a022b39ebc9a607d6e65a6a18f4f781` | 1 | 1 | 14 | 5 | killed |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | restored `71591fb1b761f628b95276443571aff953539404` | 0 | 0 | 15 | 6 | control passed |
| `.ufo/gates/custody-pair/custody-pair.py` | pristine `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` | 0 | 0 | 15 | 6 | control passed |
| `.ufo/gates/custody-pair/custody-pair.py` | mutated `df00c5d87d4ef975f5d93377e861274fa1e71871` | 1 | 1 | 14 | 3 | killed |
| `.ufo/gates/custody-pair/custody-pair.py` | restored `27594fcbbc9e2fbd01ff32088119927555ac3a83` | 0 | 0 | 15 | 6 | control passed |
| `.ufo/waves/round-17/verify.py` | pristine `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` | 0 | 0 | 15 | 6 | control passed |
| `.ufo/waves/round-17/verify.py` | mutated `e027bffbd5a0cee495cb4ad28df9bb93048397a8` | 1 | 1 | 15 | 6 | killed |
| `.ufo/waves/round-17/verify.py` | restored `165d8d4b3800940710fdbba1791afc6820150801` | 0 | 0 | 15 | 6 | control passed |

Exactly these live-site objects were emitted for the mutant revisions:

### .ufo/gates/citation-drift/citation-drift-probe.py

```json
[
  {
    "code": "ap.add_argument(\"--rev\", default=\"HEAD\")",
    "context": "live",
    "kind": "default-HEAD",
    "line": 477,
    "path": ".ufo/gates/citation-drift/citation-drift-probe.py"
  }
]
```

### .ufo/gates/custody-pair/custody-pair.py

```json
[
  {
    "code": "[\"git\", \"rev-parse\", \"HEAD\"],",
    "context": "live",
    "kind": "rev-parse-HEAD",
    "line": 327,
    "path": ".ufo/gates/custody-pair/custody-pair.py"
  }
]
```

### .ufo/waves/round-17/verify.py

```json
[
  {
    "code": "source = git(\"rev-parse\", \"HEAD\")",
    "context": "live",
    "kind": "rev-parse-HEAD",
    "line": 59,
    "path": ".ufo/waves/round-17/verify.py"
  }
]
```

## Isolation and exact-byte restoration

[OBSERVATION] Each `git diff --name-only PIN MUTANT` output was exactly its assigned path (one line). For each mutant, `git rev-parse BASE:PATH MUTANT:PATH` returned the same blob twice:

| File | Baseline blob = mutant blob |
|---|---|
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `f88dc287556a97b0d93778876d4013941536419f` |
| `.ufo/gates/custody-pair/custody-pair.py` | `18e21f283a9ea7f1decd7e2c7007f8cd2fda3f18` |
| `.ufo/waves/round-17/verify.py` | `b6852f9f04a081708be6c96837cedb1fd0d2812d` |

SHA-256 from the actual working files, before mutation / after mutation / after restoration:

- `.ufo/gates/citation-drift/citation-drift-probe.py`
  - pristine: `d3e24de4e91c01de1bdaf2c7b9db6cd5b86642eaeebc7c145f77660fd9e8679d`
  - mutant: `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`
  - restored: `d3e24de4e91c01de1bdaf2c7b9db6cd5b86642eaeebc7c145f77660fd9e8679d`
- `.ufo/gates/custody-pair/custody-pair.py`
  - pristine: `171d9089e0acb3ccb470236c6433f6d80b24ffa619701485a7ddf49b6874e448`
  - mutant: `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`
  - restored: `171d9089e0acb3ccb470236c6433f6d80b24ffa619701485a7ddf49b6874e448`
- `.ufo/waves/round-17/verify.py`
  - pristine: `3205f05efe559be5b4e7e0de20adebdf478533f577c6ad7d1d8b9a3a4d19b175`
  - mutant: `2896f53abaa6c57aea864988ea8c5bc7072f88fc5777ce919350a71d7fcb1903`
  - restored: `3205f05efe559be5b4e7e0de20adebdf478533f577c6ad7d1d8b9a3a4d19b175`

Detector SHA-256 stayed `5ada7b837368a92e9b7813a37529e476acbf7ce6b1fa62dc9d3ee63ee6c68e36` in all nine hash outputs. In every clone, `git rev-parse PIN^{tree} RESTORED^{tree}` returned `916922a4419ec1356651771de874f5c2b1d39bac` twice: the complete restored committed tree equals the delivered tree, not merely the target file. Scratch clones are retained at the locations below, fully restored. No lane source or fleet file was edited; the only lane write is this report.

## Reproducing command transcript

Every executed process command is pasted below with its observed exit code. Commands listed under `/tmp` ran there; subsequent commands ran in the specified clone. Detector output fields and restoration hashes are reported above; no unrun check is represented as passed.

### Read-only lane inspection (cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`)

```sh
git show -s --format=fuller b2aad08ceeee8dd125ce0d316056d8bd766c7f94 # exit=0
git count-objects -v # exit=0
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/head-rev-lint.py # exit=0
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/contract.md # exit=0
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/gates/citation-drift/citation-drift-probe.py # exit=0
git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/gates/citation-drift/citation-drift-probe.py # exit=0
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/gates/custody-pair/custody-pair.py # exit=0
git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/gates/custody-pair/custody-pair.py # exit=0
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-17/verify.py # exit=0
git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/verify.py # exit=0
```

### Clone 1: `/tmp/kaidoku-r18-lintmutation-1.GUF5ZG`

```sh
# cwd: /tmp
mktemp -d /tmp/kaidoku-r18-lintmutation-1.XXXXXX # exit=0
git -c core.hooksPath=/dev/null clone --no-checkout --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kaidoku-r18-lintmutation-1.GUF5ZG # exit=0
# cwd: /tmp/kaidoku-r18-lintmutation-1.GUF5ZG
git remote remove origin # exit=0
git remote -v # exit=0
git -c core.hooksPath=/dev/null -c core.autocrlf=false checkout --detach b2aad08ceeee8dd125ce0d316056d8bd766c7f94 # exit=0
sha256sum .ufo/gates/citation-drift/citation-drift-probe.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --strict # exit=0
git -c core.autocrlf=false restore --source=9011581d84527ba34c675f9cf912e54d2e72d470 --worktree -- .ufo/gates/citation-drift/citation-drift-probe.py # exit=0
sha256sum .ufo/gates/citation-drift/citation-drift-probe.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
git add -- .ufo/gates/citation-drift/citation-drift-probe.py # exit=0
git -c core.hooksPath=/dev/null -c commit.gpgsign=false -c gc.auto=0 -c maintenance.auto=false -c user.name=LintMutation -c user.email=lintmutation@invalid commit -m 'mutation probe: baseline bytes only for .ufo/gates/citation-drift/citation-drift-probe.py' # exit=0
git rev-parse --verify 'HEAD^{commit}' # exit=0
git diff --name-only b2aad08ceeee8dd125ce0d316056d8bd766c7f94 9ddcf3f46a022b39ebc9a607d6e65a6a18f4f781 # exit=0
git rev-parse 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/gates/citation-drift/citation-drift-probe.py 9ddcf3f46a022b39ebc9a607d6e65a6a18f4f781:.ufo/gates/citation-drift/citation-drift-probe.py # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev 9ddcf3f46a022b39ebc9a607d6e65a6a18f4f781 --strict # exit=1
git -c core.autocrlf=false restore --source=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --staged --worktree -- .ufo/gates/citation-drift/citation-drift-probe.py # exit=0
git -c core.hooksPath=/dev/null -c commit.gpgsign=false -c gc.auto=0 -c maintenance.auto=false -c user.name=LintMutation -c user.email=lintmutation@invalid commit -m 'mutation probe: restore exact pinned bytes for .ufo/gates/citation-drift/citation-drift-probe.py' # exit=0
git rev-parse --verify 'HEAD^{commit}' # exit=0
sha256sum .ufo/gates/citation-drift/citation-drift-probe.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
git rev-parse 'b2aad08ceeee8dd125ce0d316056d8bd766c7f94^{tree}' '71591fb1b761f628b95276443571aff953539404^{tree}' # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev 71591fb1b761f628b95276443571aff953539404 --strict # exit=0
```

### Clone 2: `/tmp/kaidoku-r18-lintmutation-2.5LID95`

```sh
# cwd: /tmp
mktemp -d /tmp/kaidoku-r18-lintmutation-2.XXXXXX # exit=0
git -c core.hooksPath=/dev/null clone --no-checkout --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kaidoku-r18-lintmutation-2.5LID95 # exit=0
# cwd: /tmp/kaidoku-r18-lintmutation-2.5LID95
git remote remove origin # exit=0
git remote -v # exit=0
git -c core.hooksPath=/dev/null -c core.autocrlf=false checkout --detach b2aad08ceeee8dd125ce0d316056d8bd766c7f94 # exit=0
sha256sum .ufo/gates/custody-pair/custody-pair.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --strict # exit=0
git -c core.autocrlf=false restore --source=9011581d84527ba34c675f9cf912e54d2e72d470 --worktree -- .ufo/gates/custody-pair/custody-pair.py # exit=0
sha256sum .ufo/gates/custody-pair/custody-pair.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
git add -- .ufo/gates/custody-pair/custody-pair.py # exit=0
git -c core.hooksPath=/dev/null -c commit.gpgsign=false -c gc.auto=0 -c maintenance.auto=false -c user.name=LintMutation -c user.email=lintmutation@invalid commit -m 'mutation probe: baseline bytes only for .ufo/gates/custody-pair/custody-pair.py' # exit=0
git rev-parse --verify 'HEAD^{commit}' # exit=0
git diff --name-only b2aad08ceeee8dd125ce0d316056d8bd766c7f94 df00c5d87d4ef975f5d93377e861274fa1e71871 # exit=0
git rev-parse 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/gates/custody-pair/custody-pair.py df00c5d87d4ef975f5d93377e861274fa1e71871:.ufo/gates/custody-pair/custody-pair.py # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev df00c5d87d4ef975f5d93377e861274fa1e71871 --strict # exit=1
git -c core.autocrlf=false restore --source=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --staged --worktree -- .ufo/gates/custody-pair/custody-pair.py # exit=0
git -c core.hooksPath=/dev/null -c commit.gpgsign=false -c gc.auto=0 -c maintenance.auto=false -c user.name=LintMutation -c user.email=lintmutation@invalid commit -m 'mutation probe: restore exact pinned bytes for .ufo/gates/custody-pair/custody-pair.py' # exit=0
git rev-parse --verify 'HEAD^{commit}' # exit=0
sha256sum .ufo/gates/custody-pair/custody-pair.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
git rev-parse 'b2aad08ceeee8dd125ce0d316056d8bd766c7f94^{tree}' '27594fcbbc9e2fbd01ff32088119927555ac3a83^{tree}' # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev 27594fcbbc9e2fbd01ff32088119927555ac3a83 --strict # exit=0
```

### Clone 3: `/tmp/kaidoku-r18-lintmutation-3.BQJKz3`

```sh
# cwd: /tmp
mktemp -d /tmp/kaidoku-r18-lintmutation-3.XXXXXX # exit=0
git -c core.hooksPath=/dev/null clone --no-checkout --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kaidoku-r18-lintmutation-3.BQJKz3 # exit=0
# cwd: /tmp/kaidoku-r18-lintmutation-3.BQJKz3
git remote remove origin # exit=0
git remote -v # exit=0
git -c core.hooksPath=/dev/null -c core.autocrlf=false checkout --detach b2aad08ceeee8dd125ce0d316056d8bd766c7f94 # exit=0
sha256sum .ufo/waves/round-17/verify.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --strict # exit=0
git -c core.autocrlf=false restore --source=9011581d84527ba34c675f9cf912e54d2e72d470 --worktree -- .ufo/waves/round-17/verify.py # exit=0
sha256sum .ufo/waves/round-17/verify.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
git add -- .ufo/waves/round-17/verify.py # exit=0
git -c core.hooksPath=/dev/null -c commit.gpgsign=false -c gc.auto=0 -c maintenance.auto=false -c user.name=LintMutation -c user.email=lintmutation@invalid commit -m 'mutation probe: baseline bytes only for .ufo/waves/round-17/verify.py' # exit=0
git rev-parse --verify 'HEAD^{commit}' # exit=0
git diff --name-only b2aad08ceeee8dd125ce0d316056d8bd766c7f94 e027bffbd5a0cee495cb4ad28df9bb93048397a8 # exit=0
git rev-parse 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/verify.py e027bffbd5a0cee495cb4ad28df9bb93048397a8:.ufo/waves/round-17/verify.py # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev e027bffbd5a0cee495cb4ad28df9bb93048397a8 --strict # exit=1
git -c core.autocrlf=false restore --source=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --staged --worktree -- .ufo/waves/round-17/verify.py # exit=0
git -c core.hooksPath=/dev/null -c commit.gpgsign=false -c gc.auto=0 -c maintenance.auto=false -c user.name=LintMutation -c user.email=lintmutation@invalid commit -m 'mutation probe: restore exact pinned bytes for .ufo/waves/round-17/verify.py' # exit=0
git rev-parse --verify 'HEAD^{commit}' # exit=0
sha256sum .ufo/waves/round-17/verify.py .ufo/waves/round-18/tools/head-rev-lint.py # exit=0
git rev-parse 'b2aad08ceeee8dd125ce0d316056d8bd766c7f94^{tree}' '165d8d4b3800940710fdbba1791afc6820150801^{tree}' # exit=0
timeout 30s python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev 165d8d4b3800940710fdbba1791afc6820150801 --strict # exit=0
```
