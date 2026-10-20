# Round 19 wave 2 — MutAliases

## Result

**OBSERVATION — one mutant SURVIVED the assigned `routed-r18.py --strict` detector.** Removing only `"FETCH_HEAD", ` from `_PSEUDO_REFS` made citation-drift accept the planted mutable `FETCH_HEAD` and grade baseline B clean (exit 0), while the C1 detector still reported `open_count=0`, `R18-HEAD-ALIASES.substance=true`, exit 0. Pristine and restored runs both refused that same input with `rev_moving_state`, exit 2. This is a demonstrated **C1 closure-detector coverage gap**, not a claim that the pristine pseudo-ref guard accepts `FETCH_HEAD`.

**OBSERVATION — no unintended HEAD-derived expression was accepted in the pristine cases exercised.** The requested `@`, `HEAD^0`, `HEAD^{commit}`, `@~0`, `ORIG_HEAD`, and `FETCH_HEAD` all returned exit 2 with `rev_moving_state`. Literal `HEAD` was accepted deliberately while HEAD equaled the branch tip. The tested hidden-HEAD ranges and bare `:/message` forms returned exit 2 with `revision_unresolvable`, not `rev_moving_state`. Branch-scoped message searches `refs/heads/main^{/round-19}` and `refs/heads/main^{/wave-two}` evaluated T, exit 1 for citation drift; these are branch-derived searches, not HEAD aliases.

**Axes:** calibration (distinguish a coverage finding from a production defect and expected red from mutation failure); freshness (pin the observed integrated main tip); depth (real CLI alias matrix plus committed-object pristine/mutant/restored runs).

## Freshness and isolation

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Only this report was written in the lane; all Git writes, source mutation and detectors ran in the private clone.
- Observed integrated `refs/heads/main` T: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`. Historical B: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`.
- `tempfile.mkdtemp(prefix="kr19-w2-MutAliases-", dir="/tmp")` produced `/tmp/kr19-w2-MutAliases-r5oywvgw`. A `--no-hardlinks --no-checkout` clone was checked out detached at T; clone HEAD and clone main both resolved to T before probing. Main was attached only within this clone to make committed mutant/restoration objects visible to the same detector command.
- The runner captured stdout, stderr and exit codes with per-command timeouts (45–90 seconds for probes), and ran independent pristine cases in batches of at most six. No timeout occurred.
- No delegation, installs/updates, builds, broad suite, formatting, REA/MCP, Ghidra, carrier execution, fleet writes, client-config reads/writes, or sibling edits. Existing Python/Git/sha256sum were sufficient.

Observed lane tip command (read-only; exit 0):

```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse --verify refs/heads/main
# exit=0
```
```text
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

All path:line source citations below refer to bytes at T, preserved in the clone. The claim being challenged is `.ufo/waves/round-19/claims.json:10-14`; the universal alias wording is in `SCORECARD.md:2486`, `corpus/lessons/round-19.md:59`, and `SKILL.md:448`. The original routed defect is `corpus/lessons/round-18-verifier-spotcheck.md:196`.

## One mutation, expected detector, actual result

Smallest behavior-bearing change: `.ufo/gates/citation-drift/citation-drift-probe.py:326` only.

```diff
-_PSEUDO_REFS = ("ORIG_HEAD", "FETCH_HEAD", "MERGE_HEAD", "CHERRY_PICK_HEAD",
+_PSEUDO_REFS = ("ORIG_HEAD", "MERGE_HEAD", "CHERRY_PICK_HEAD",
```

`ORIG_HEAD` and `FETCH_HEAD` were planted only in the clone and both named B. `git update-ref ORIG_HEAD B` succeeded. `git update-ref FETCH_HEAD B` refused to update that pseudoref (exit 128); the fixture was then written through the file-write tool to `/tmp/kr19-w2-MutAliases-r5oywvgw/.git/FETCH_HEAD` as 75 bytes:

```text
8a8da7e19375aadc66c6bcbff0bbcbb596048fb0		kr19-w2-MutAliases local fixture
```

`git rev-parse --verify 'FETCH_HEAD^{commit}'` confirmed B, exit 0. This setup matters: acceptance cannot be confused with a nonexistent pseudo-ref or an input that merely happens to name the current tip.

**Expected detector:** if the stated mutable-pseudo-ref prohibition is covered by C1, dropping `FETCH_HEAD` should make `R18-HEAD-ALIASES.substance=false` and the strict detector exit 1. The direct semantic control should change from refusal (2) to evaluation (0 or 1). No contract was changed.

Same bounded closure-detector argv, run once in each state:

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --rev refs/heads/main --strict
```

| State | Committed revision inspected | Detector exit | open / named-open / substance-open | Direct `--rev FETCH_HEAD` exit |
|---|---|---:|---|---:|
| pristine | `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` | 0 | 0 / 0 / 0 | 2 (`rev_moving_state`) |
| mutant | `a9429179e1c13fd4c6869b01ac11a749ce93739a` | 0 | 0 / 0 / 0 | 0 (resolved B, clean) |
| restored | `e382e43266d9a5c8844d3dd36bde524c4a6d87a0` | 0 | 0 / 0 / 0 | 2 (`rev_moving_state`) |

Each state emitted the identical HEAD-ALIASES result:

```json
{
  "id": "R18-HEAD-ALIASES",
  "named": true,
  "substance": true,
  "why": "6 aliases exit 2, refs/heads/main evaluates; lint limit registered"
}
```

The historical red control used the T version of the counter with `--rev B`, which extracts the tested gate from B: exit 1, `open_count=7`, `named_open=7`, `substance_open=7`. Its HEAD result was:

```json
{
  "id": "R18-HEAD-ALIASES",
  "named": false,
  "substance": false,
  "why": "HEAD aliases not refused: @->1, HEAD~0->1, HEAD^{commit}->1, HEAD@{0}->1, @~0->1, HEAD^0->1"
}
```

**Verdict: SURVIVED.** The mutation baseline was the passing pristine T detector, not the intentionally red historical B control. Thus this is not an inconclusive baseline failure and not a killed mutant. The direct before/after/refusal restoration establishes a real semantic regression despite the surviving closure detector.

## Pristine revision-expression observations

All direct commands used the pristine T gate and its unchanged T pointer table/expected file. “Evaluated” means the revision passed input refusal; it does **not** mean citation correctness. For T, exit 1 was existing citation drift, not rejection of the revision. The same current gate/table over B returned clean, exit 0. This does not substitute the T gate for historical B gate behavior; the separate C1 red control above extracts the B gate itself.

| `--rev` input | Exit | Actual result / source scope |
|---|---:|---|
| `@` | 2 | `rev_moving_state`; no citation tree graded |
| `HEAD^0` | 2 | `rev_moving_state`; no citation tree graded |
| `HEAD^{commit}` | 2 | `rev_moving_state`; no citation tree graded |
| `@~0` | 2 | `rev_moving_state`; no citation tree graded |
| `ORIG_HEAD` | 2 | `rev_moving_state` although fixture resolves to B |
| `FETCH_HEAD` | 2 | `rev_moving_state` although fixture resolves to B |
| `refs/heads/main` | 1 | evaluated T; citation drift |
| `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` | 1 | evaluated T; citation drift |
| `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` | 0 | evaluated B; clean |
| `HEAD` | 1 | accepted by the explicit branch-tip exception, evaluated T |
| `HEAD~0` | 2 | `rev_moving_state` |
| `HEAD@{0}` | 2 | `rev_moving_state` |
| `refs/heads/main..HEAD` | 2 | `revision_unresolvable`, not lexical moving-state refusal |
| `refs/heads/main...HEAD` | 2 | `revision_unresolvable`, not lexical moving-state refusal |
| `refs/heads/main..@` | 2 | `revision_unresolvable`, not lexical moving-state refusal |
| `:/round-19` | 2 | `revision_unresolvable` |
| `:/HEAD` | 2 | `revision_unresolvable` |
| `HEAD^{/round-19}` | 2 | `rev_moving_state` |
| `@^{/round-19}` | 2 | `rev_moving_state` |
| `refs/heads/main^{/round-19}` | 1 | evaluated T; branch-reachable message search, not HEAD-derived |
| `refs/heads/main^{/wave-two}` | 1 | evaluated T; branch-reachable message search, not HEAD-derived |
| `refs/heads/main^{/HEAD}` | 2 | `revision_unresolvable` for this repository state |

Also exercised: exact subject-anchored searches (bare `:/...` and branch-scoped `^{/...}`), plus bare `:/round-19`/`:/wave-two`/`:/HEAD` searches with a trailing `|`; all those additional cases returned `revision_unresolvable`, exit 2. Exact argv/output are in the transcript appendix.

Raw Git `rev-parse --verify :/round-19` resolved T (exit 0), whereas Git with the gate's appended `^{commit}` returned exit 128. Therefore rejection of the bare message syntax here is an observed resolution outcome, **not** proof that `moving_rev_cause` parses and rejects all message-search expressions. No off-branch HEAD acceptance was demonstrated; the literal-HEAD control was tested only while HEAD equaled main.

## Source scope and why the mutant survives

- **OBSERVATION (source):** `.ufo/gates/citation-drift/citation-drift-probe.py:331-348` checks lexical prefixes, pseudo-ref names, and `@{` selectors. `:374-389` handles literal HEAD with a branch-tip comparison and rejects named moving-state causes. `:290-305,390-411` verifies explicit inputs as a single commit with `^{commit}`; this is where the tested ranges/bare message searches failed. `:120-155,392-393,437-442` shows in-repo citation content is read with `git show REV:path`; tables and expected values are filesystem inputs loaded at `:413-435`.
- **OBSERVATION (source):** `.ufo/waves/round-19/tools/routed-r18.py:38` fixes the C1 alias corpus at exactly `@`, `HEAD~0`, `HEAD^{commit}`, `HEAD@{0}`, `@~0`, `HEAD^0`. `.ufo/waves/round-19/tools/routed-r18.py:192-213` probes only those six and the stable `refs/heads/main` control, then checks the nested-read registry wording. Neither `ORIG_HEAD`, `FETCH_HEAD`, revision ranges, nor message syntax is in that C1 corpus.
- **OBSERVATION (source and commands):** `.ufo/waves/round-19/tools/routed-r18.py:46-69,193-198,292-312` reads/extracts committed objects. The mutant was committed to clone main before measurement, so the C1 detector inspected the mutated Git blob, not stale pristine bytes from another revision. The driver `routed-r18.py` itself was unchanged throughout.
- **OBSERVATION (source):** the citation gate's own `ALIAS_CASES` includes a `FETCH_HEAD` refusal at `.ufo/gates/citation-drift/citation-drift-probe.py:539-559` (specifically `:554`), and its selftest consumes that corpus at `:602-605,657-670`. The full selftest was **not run**. This finding is limited to the assigned routed C1 detector, not an assertion that every existing detector lacks this case.
- **INFERENCE:** a one-name omission from the mutable-ref denylist can regress the published pseudo-ref contract without reopening C1, because the closure detector samples only the six HEAD aliases. A surviving mutant is a coverage finding, not authority to weaken or amend the promised contract. No production fix or integration was attempted.

## Exact restoration evidence

The same line was restored with the surgical edit tool and committed in the private clone. No second mutant was introduced.

| Bytes | Pristine SHA-256 | Mutant SHA-256 | Restored SHA-256 |
|---|---|---|---|
| `citation-drift-probe.py` | `cc23dcabcb2934391780ce8e5c97e7f8d0973b5353864a470315bbb8def9a1ed` | `1dcab74fc08c4913982392fa6920ca2dcb26afd3463efb6b40cd0792c0039880` | `cc23dcabcb2934391780ce8e5c97e7f8d0973b5353864a470315bbb8def9a1ed` |
| `routed-r18.py` | `dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b` | same | same |

The in-memory exact-byte comparison returned `exact_probe_bytes_restored=True`. The recorded `git rev-parse T^{tree} RESTORED^{tree}` returned the identical tracked-tree object twice:

```text
b344427155950539dd93926882071beea28970a4
b344427155950539dd93926882071beea28970a4
```

The clone retains its deliberately planted pseudo-ref fixtures and local mutation/restoration history for provenance; this is a tracked-tree/source restoration claim, not an assertion that `.git` metadata is byte-identical to its initial clone state. Main-lane production bytes were never edited.

## Command and output transcript

The following are the captured commands and actual exits/stdout/stderr; they are not reruns. Working directory for every command below was `/tmp/kr19-w2-MutAliases-r5oywvgw`. Parallel cases are listed in the order their records were collected. File-tool operations were: create the 75-byte FETCH_HEAD fixture after Git's refusal; remove one token on line 326; restore that token; write this report. Those API operations have success results rather than process exit codes. Both source edits were acknowledged by the edit tool; restoration returned the original source snapshot tag `3822`.

### 1. clone-observed-tip

```sh
git clone -q --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-MutAliases-r5oywvgw
# exit=0
```

stdout/stderr: empty.

### 2. checkout-observed-tip

```sh
git -C /tmp/kr19-w2-MutAliases-r5oywvgw checkout -q --detach d0690fd44f46d8a7fe9da5f01c6be723d12abd41
# exit=0
```

stdout/stderr: empty.

### 3. clone-identities

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse HEAD refs/heads/main
# exit=0
```

stdout:

```text
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

### 4. message-selectors

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw log -5 '--format=%H %s' d0690fd44f46d8a7fe9da5f01c6be723d12abd41
# exit=0
```

stdout:

```text
d0690fd44f46d8a7fe9da5f01c6be723d12abd41 round-19: wave-two assignment records and verification expected-red safeguards
5e364bd5e6016f030a04b4b8c81830477ebdaf51 round-19: anchored install-section parser and integrated measurements, falsification spec
4f6c73f81ae8d31de18377d7ff57e4e10140ce48 round-19: wave-one integration, routed fixes, freshness, held-out run evidence and corpus
a1140e76fffdc1be032d9d813dbb686157803bbc round-19: frozen C3 predictions and decision rule (go1.25.0 toolchain held-out, D={t1250-vet}), runner (pre-run)
85589ac757f9ca3cb25efcd702d0963e25c9c4df round-19: declared claims, seat contract, wave-1 spec/dispatch/registration, baseline census and emulator prescan
```

### 5. plant-ORIG_HEAD

```sh
git -C /tmp/kr19-w2-MutAliases-r5oywvgw update-ref ORIG_HEAD 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
# exit=0
```

stdout/stderr: empty.

### 6. plant-FETCH_HEAD

```sh
git -C /tmp/kr19-w2-MutAliases-r5oywvgw update-ref FETCH_HEAD 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
# exit=128
```

stderr:

```text
fatal: update_ref failed for ref 'FETCH_HEAD': refusing to update pseudoref 'FETCH_HEAD'
```

### 7. verify-fetch-fixture

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify 'FETCH_HEAD^{commit}'
# exit=0
```

stdout:

```text
8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
```

### 8. pristine-alias-ORIG_HEAD

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev ORIG_HEAD
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: ORIG_HEAD
CITATION_DRIFT_REV_RESOLVED: ORIG_HEAD
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=ORIG_HEAD 'ORIG_HEAD' is a mutable pseudo-ref rewritten by Git; pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 9. pristine-alias-@~0

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev '@~0'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: @~0
CITATION_DRIFT_REV_RESOLVED: @~0
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=@~0 '@~0' is HEAD-derived (the '@' spelling of HEAD); pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 10. pristine-alias-FETCH_HEAD

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev FETCH_HEAD
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: FETCH_HEAD
CITATION_DRIFT_REV_RESOLVED: FETCH_HEAD
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=FETCH_HEAD 'FETCH_HEAD' is a mutable pseudo-ref rewritten by Git; pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 11. pristine-alias-HEAD^{commit}

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'HEAD^{commit}'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: HEAD^{commit}
CITATION_DRIFT_REV_RESOLVED: HEAD^{commit}
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=HEAD^{commit} 'HEAD^{commit}' is HEAD-derived; a pinned revision must not read HEAD; pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 12. pristine-alias-HEAD^0

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'HEAD^0'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: HEAD^0
CITATION_DRIFT_REV_RESOLVED: HEAD^0
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=HEAD^0 'HEAD^0' is HEAD-derived; a pinned revision must not read HEAD; pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 13. pristine-alias-@

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev @
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: @
CITATION_DRIFT_REV_RESOLVED: @
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=@ '@' is Git's shorthand for HEAD (a moving revision); pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 14. pristine-alias-HEAD~0

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'HEAD~0'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: HEAD~0
CITATION_DRIFT_REV_RESOLVED: HEAD~0
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=HEAD~0 'HEAD~0' is HEAD-derived; a pinned revision must not read HEAD; pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 15. pristine-alias-HEAD@{0}

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'HEAD@{0}'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: HEAD@{0}
CITATION_DRIFT_REV_RESOLVED: HEAD@{0}
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=HEAD@{0} 'HEAD@{0}' is HEAD-derived; a pinned revision must not read HEAD; pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 16. pristine-alias-d0690fd44f46d8a7fe9da5f01c6be723d12abd41

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41
# exit=1
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
CITATION_DRIFT_REV_RESOLVED: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: citation_dead entry=prov18-stamp-named PROVINCE.md:18 lacks '17:55:49Z receipt'
CITATION_DRIFT: citation_dead entry=sc69-readme-177 SCORECARD.md:69 cites corpus/README.md:180-180, which lacks 'held, not frontier' (holds '- adb device surface — 22/24 verbs need a live device/emulator.')
CITATION_DRIFT: citation_dead entry=readme175-sc1217 corpus/README.md:175 states no resolvable pointer (pattern 'SCORECARD\\.md:(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r7range corpus/README.md:175 states no resolvable pointer (pattern 'r7-pe-wall\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r8e2 corpus/README.md:175 states no resolvable pointer (pattern 'round8/E2\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT_VERDICT: failed findings=5 exit=1
```

### 17. pristine-alias-8a8da7e19375aadc66c6bcbff0bbcbb596048fb0

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
# exit=0
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
CITATION_DRIFT_REV_RESOLVED: 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

### 18. pristine-alias-refs/heads/main

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev refs/heads/main
# exit=1
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: refs/heads/main
CITATION_DRIFT_REV_RESOLVED: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: citation_dead entry=prov18-stamp-named PROVINCE.md:18 lacks '17:55:49Z receipt'
CITATION_DRIFT: citation_dead entry=sc69-readme-177 SCORECARD.md:69 cites corpus/README.md:180-180, which lacks 'held, not frontier' (holds '- adb device surface — 22/24 verbs need a live device/emulator.')
CITATION_DRIFT: citation_dead entry=readme175-sc1217 corpus/README.md:175 states no resolvable pointer (pattern 'SCORECARD\\.md:(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r7range corpus/README.md:175 states no resolvable pointer (pattern 'r7-pe-wall\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r8e2 corpus/README.md:175 states no resolvable pointer (pattern 'round8/E2\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT_VERDICT: failed findings=5 exit=1
```

### 19. pristine-alias-HEAD

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev HEAD
# exit=1
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: HEAD
CITATION_DRIFT_REV_RESOLVED: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: citation_dead entry=prov18-stamp-named PROVINCE.md:18 lacks '17:55:49Z receipt'
CITATION_DRIFT: citation_dead entry=sc69-readme-177 SCORECARD.md:69 cites corpus/README.md:180-180, which lacks 'held, not frontier' (holds '- adb device surface — 22/24 verbs need a live device/emulator.')
CITATION_DRIFT: citation_dead entry=readme175-sc1217 corpus/README.md:175 states no resolvable pointer (pattern 'SCORECARD\\.md:(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r7range corpus/README.md:175 states no resolvable pointer (pattern 'r7-pe-wall\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r8e2 corpus/README.md:175 states no resolvable pointer (pattern 'round8/E2\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT_VERDICT: failed findings=5 exit=1
```

### 20. pristine-alias-refs/heads/main...HEAD

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev refs/heads/main...HEAD
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: refs/heads/main...HEAD
CITATION_DRIFT_REV_RESOLVED: refs/heads/main...HEAD
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=refs/heads/main...HEAD not a commit object (git rev-parse --verify refs/heads/main...HEAD^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 21. pristine-alias-refs/heads/main..HEAD

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev refs/heads/main..HEAD
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: refs/heads/main..HEAD
CITATION_DRIFT_REV_RESOLVED: refs/heads/main..HEAD
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=refs/heads/main..HEAD not a commit object (git rev-parse --verify refs/heads/main..HEAD^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 22. pristine-alias-refs/heads/main..@

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev refs/heads/main..@
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: refs/heads/main..@
CITATION_DRIFT_REV_RESOLVED: refs/heads/main..@
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=refs/heads/main..@ not a commit object (git rev-parse --verify refs/heads/main..@^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 23. pristine-alias-:/^round-19: wave-two assignment records and verification expected-red safeguards$

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev ':/^round-19: wave-two assignment records and verification expected-red safeguards$'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: :/^round-19: wave-two assignment records and verification expected-red safeguards$
CITATION_DRIFT_REV_RESOLVED: :/^round-19: wave-two assignment records and verification expected-red safeguards$
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=:/^round-19: wave-two assignment records and verification expected-red safeguards$ not a commit object (git rev-parse --verify :/^round-19: wave-two assignment records and verification expected-red safeguards$^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 24. pristine-alias-refs/heads/main^{/^round-19: wave-two assignment records and verification expected-red safeguards$}

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'refs/heads/main^{/^round-19: wave-two assignment records and verification expected-red safeguards$}'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: refs/heads/main^{/^round-19: wave-two assignment records and verification expected-red safeguards$}
CITATION_DRIFT_REV_RESOLVED: refs/heads/main^{/^round-19: wave-two assignment records and verification expected-red safeguards$}
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=refs/heads/main^{/^round-19: wave-two assignment records and verification expected-red safeguards$} not a commit object (git rev-parse --verify refs/heads/main^{/^round-19: wave-two assignment records and verification expected-red safeguards$}^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 25. pristine-routed-main

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --rev refs/heads/main --strict
# exit=0
```

stdout:

```text
{
  "defects": [
    {
      "id": "R18-MIDMAP-LISTSTEP",
      "named": true,
      "substance": true,
      "why": "non-analyze-only list receipt -> mid_checks_absent; analyze-carrying list receipt clean"
    },
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": true,
      "why": "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"
    },
    {
      "id": "R18-STRICT-BASELINE",
      "named": true,
      "substance": true,
      "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"
    },
    {
      "id": "R18-HEAD-ALIASES",
      "named": true,
      "substance": true,
      "why": "6 aliases exit 2, refs/heads/main evaluates; lint limit registered"
    },
    {
      "id": "R18-DEADSEAT-RECORD",
      "named": true,
      "substance": true,
      "why": "4 seats without a report at a245bb0, each with cause and source"
    },
    {
      "id": "R18-REGISTRY-PINNED",
      "named": true,
      "substance": true,
      "why": "both rows name an existing path or state no persisted baseline"
    },
    {
      "id": "R18-INSTALL-RECORD",
      "named": true,
      "substance": true,
      "why": "go1.24.6 and go1.25.0 recorded with full sha256 and go.dev channel"
    }
  ],
  "named_open": 0,
  "open_count": 0,
  "rev": "d0690fd44f46d8a7fe9da5f01c6be723d12abd41",
  "substance_open": 0
}
```

### 26. historical-baseline-routed

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
# exit=1
```

stdout:

```text
{
  "defects": [
    {
      "id": "R18-MIDMAP-LISTSTEP",
      "named": false,
      "substance": false,
      "why": "list-shaped receipt with pin_checks only on a non-analyze step is accepted"
    },
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": false,
      "substance": false,
      "why": "no _validator_pin/VALIDATOR_REV/RECEIPT_VALIDATE at REV (format-only check)"
    },
    {
      "id": "R18-STRICT-BASELINE",
      "named": false,
      "substance": false,
      "why": "strict-baseline receipt for 9011581d8452 absent"
    },
    {
      "id": "R18-HEAD-ALIASES",
      "named": false,
      "substance": false,
      "why": "HEAD aliases not refused: @->1, HEAD~0->1, HEAD^{commit}->1, HEAD@{0}->1, @~0->1, HEAD^0->1"
    },
    {
      "id": "R18-DEADSEAT-RECORD",
      "named": false,
      "substance": false,
      "why": "r18-dead-seats.json absent"
    },
    {
      "id": "R18-REGISTRY-PINNED",
      "named": false,
      "substance": false,
      "why": "pins: Pinned values names no path that exists at REV; go-buildinfo-probe: Pinned values names no path that exists at REV"
    },
    {
      "id": "R18-INSTALL-RECORD",
      "named": false,
      "substance": false,
      "why": "round-19 lesson absent"
    }
  ],
  "named_open": 7,
  "open_count": 7,
  "rev": "8a8da7e19375aadc66c6bcbff0bbcbb596048fb0",
  "substance_open": 7
}
```

### 27. pristine-message-:/round-19|

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev ':/round-19|'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: :/round-19|
CITATION_DRIFT_REV_RESOLVED: :/round-19|
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=:/round-19| not a commit object (git rev-parse --verify :/round-19|^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 28. git-message-:/round-19

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify ':/round-19^{commit}'
# exit=128
```

stderr:

```text
fatal: Needed a single revision
```

### 29. pristine-message-:/wave-two|

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev ':/wave-two|'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: :/wave-two|
CITATION_DRIFT_REV_RESOLVED: :/wave-two|
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=:/wave-two| not a commit object (git rev-parse --verify :/wave-two|^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 30. pristine-message-:/round-19

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev :/round-19
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: :/round-19
CITATION_DRIFT_REV_RESOLVED: :/round-19
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=:/round-19 not a commit object (git rev-parse --verify :/round-19^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 31. git-message-:/round-19|

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify ':/round-19|^{commit}'
# exit=128
```

stderr:

```text
fatal: Needed a single revision
```

### 32. pristine-message-:/HEAD|

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev ':/HEAD|'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: :/HEAD|
CITATION_DRIFT_REV_RESOLVED: :/HEAD|
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=:/HEAD| not a commit object (git rev-parse --verify :/HEAD|^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 33. git-message-:/wave-two|

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify ':/wave-two|^{commit}'
# exit=128
```

stderr:

```text
fatal: Needed a single revision
```

### 34. git-message-refs/heads/main^{/wave-two}

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify 'refs/heads/main^{/wave-two}^{commit}'
# exit=0
```

stdout:

```text
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

### 35. git-message-:/HEAD|

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify ':/HEAD|^{commit}'
# exit=128
```

stderr:

```text
fatal: Needed a single revision
```

### 36. git-message-refs/heads/main^{/round-19}

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify 'refs/heads/main^{/round-19}^{commit}'
# exit=0
```

stdout:

```text
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

### 37. pristine-message-refs/heads/main^{/wave-two}

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'refs/heads/main^{/wave-two}'
# exit=1
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: refs/heads/main^{/wave-two}
CITATION_DRIFT_REV_RESOLVED: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: citation_dead entry=prov18-stamp-named PROVINCE.md:18 lacks '17:55:49Z receipt'
CITATION_DRIFT: citation_dead entry=sc69-readme-177 SCORECARD.md:69 cites corpus/README.md:180-180, which lacks 'held, not frontier' (holds '- adb device surface — 22/24 verbs need a live device/emulator.')
CITATION_DRIFT: citation_dead entry=readme175-sc1217 corpus/README.md:175 states no resolvable pointer (pattern 'SCORECARD\\.md:(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r7range corpus/README.md:175 states no resolvable pointer (pattern 'r7-pe-wall\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r8e2 corpus/README.md:175 states no resolvable pointer (pattern 'round8/E2\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT_VERDICT: failed findings=5 exit=1
```

### 38. pristine-message-refs/heads/main^{/round-19}

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'refs/heads/main^{/round-19}'
# exit=1
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: refs/heads/main^{/round-19}
CITATION_DRIFT_REV_RESOLVED: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: citation_dead entry=prov18-stamp-named PROVINCE.md:18 lacks '17:55:49Z receipt'
CITATION_DRIFT: citation_dead entry=sc69-readme-177 SCORECARD.md:69 cites corpus/README.md:180-180, which lacks 'held, not frontier' (holds '- adb device surface — 22/24 verbs need a live device/emulator.')
CITATION_DRIFT: citation_dead entry=readme175-sc1217 corpus/README.md:175 states no resolvable pointer (pattern 'SCORECARD\\.md:(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r7range corpus/README.md:175 states no resolvable pointer (pattern 'r7-pe-wall\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT: citation_dead entry=readme175-r8e2 corpus/README.md:175 states no resolvable pointer (pattern 'round8/E2\\.md:(\\d+)-(\\d+)' absent)
CITATION_DRIFT_VERDICT: failed findings=5 exit=1
```

### 39. git-plain-message

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify :/round-19
# exit=0
```

stdout:

```text
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

### 40. git-branch-message-head

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse --verify 'refs/heads/main^{/HEAD}^{commit}'
# exit=128
```

stderr:

```text
fatal: Needed a single revision
```

### 41. pristine-extra-HEAD^{/round-19}

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'HEAD^{/round-19}'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: HEAD^{/round-19}
CITATION_DRIFT_REV_RESOLVED: HEAD^{/round-19}
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=HEAD^{/round-19} 'HEAD^{/round-19}' is HEAD-derived; a pinned revision must not read HEAD; pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 42. pristine-extra-@^{/round-19}

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev '@^{/round-19}'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: @^{/round-19}
CITATION_DRIFT_REV_RESOLVED: @^{/round-19}
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=@^{/round-19} '@^{/round-19}' is HEAD-derived (the '@' spelling of HEAD); pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 43. pristine-extra-:/HEAD

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev :/HEAD
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: :/HEAD
CITATION_DRIFT_REV_RESOLVED: :/HEAD
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=:/HEAD not a commit object (git rev-parse --verify :/HEAD^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 44. pristine-extra-refs/heads/main^{/HEAD}

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev 'refs/heads/main^{/HEAD}'
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: refs/heads/main^{/HEAD}
CITATION_DRIFT_REV_RESOLVED: refs/heads/main^{/HEAD}
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: revision_unresolvable entry=refs/heads/main^{/HEAD} not a commit object (git rev-parse --verify refs/heads/main^{/HEAD}^{commit} failed)
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 45. attach-clone-main

```sh
git -C /tmp/kr19-w2-MutAliases-r5oywvgw switch --quiet main
# exit=0
```

stdout/stderr: empty.

### 46. pristine-tool-hashes

```sh
sha256sum /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py
# exit=0
```

stdout:

```text
cc23dcabcb2934391780ce8e5c97e7f8d0973b5353864a470315bbb8def9a1ed  /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py
dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b  /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py
```

### 47. stage-mutant

```sh
git -C /tmp/kr19-w2-MutAliases-r5oywvgw add -- .ufo/gates/citation-drift/citation-drift-probe.py
# exit=0
```

stdout/stderr: empty.

### 48. commit-mutant

```sh
git -c user.name=MutAliases -c user.email=mutaliases@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null -C /tmp/kr19-w2-MutAliases-r5oywvgw commit --quiet -m 'mutation probe: omit FETCH_HEAD from moving-ref guard'
# exit=0
```

stdout/stderr: empty.

### 49. mutant-identity

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse refs/heads/main
# exit=0
```

stdout:

```text
a9429179e1c13fd4c6869b01ac11a749ce93739a
```

### 50. mutant-tool-hashes

```sh
sha256sum /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py
# exit=0
```

stdout:

```text
1dcab74fc08c4913982392fa6920ca2dcb26afd3463efb6b40cd0792c0039880  /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py
dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b  /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py
```

### 51. mutant-fetch-control

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev FETCH_HEAD
# exit=0
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: FETCH_HEAD
CITATION_DRIFT_REV_RESOLVED: 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

### 52. mutant-routed-main

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --rev refs/heads/main --strict
# exit=0
```

stdout:

```text
{
  "defects": [
    {
      "id": "R18-MIDMAP-LISTSTEP",
      "named": true,
      "substance": true,
      "why": "non-analyze-only list receipt -> mid_checks_absent; analyze-carrying list receipt clean"
    },
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": true,
      "why": "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"
    },
    {
      "id": "R18-STRICT-BASELINE",
      "named": true,
      "substance": true,
      "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"
    },
    {
      "id": "R18-HEAD-ALIASES",
      "named": true,
      "substance": true,
      "why": "6 aliases exit 2, refs/heads/main evaluates; lint limit registered"
    },
    {
      "id": "R18-DEADSEAT-RECORD",
      "named": true,
      "substance": true,
      "why": "4 seats without a report at a245bb0, each with cause and source"
    },
    {
      "id": "R18-REGISTRY-PINNED",
      "named": true,
      "substance": true,
      "why": "both rows name an existing path or state no persisted baseline"
    },
    {
      "id": "R18-INSTALL-RECORD",
      "named": true,
      "substance": true,
      "why": "go1.24.6 and go1.25.0 recorded with full sha256 and go.dev channel"
    }
  ],
  "named_open": 0,
  "open_count": 0,
  "rev": "a9429179e1c13fd4c6869b01ac11a749ce93739a",
  "substance_open": 0
}
```

### 53. stage-restoration

```sh
git -C /tmp/kr19-w2-MutAliases-r5oywvgw add -- .ufo/gates/citation-drift/citation-drift-probe.py
# exit=0
```

stdout/stderr: empty.

### 54. commit-restoration

```sh
git -c user.name=MutAliases -c user.email=mutaliases@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null -C /tmp/kr19-w2-MutAliases-r5oywvgw commit --quiet -m 'mutation probe: restore exact citation-drift source bytes'
# exit=0
```

stdout/stderr: empty.

### 55. restored-identity

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse refs/heads/main
# exit=0
```

stdout:

```text
e382e43266d9a5c8844d3dd36bde524c4a6d87a0
```

### 56. restored-tool-hashes

```sh
sha256sum /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py
# exit=0
```

stdout:

```text
cc23dcabcb2934391780ce8e5c97e7f8d0973b5353864a470315bbb8def9a1ed  /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py
dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b  /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py
```

### 57. restored-fetch-control

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --table /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/expected.json --strict --rev FETCH_HEAD
# exit=2
```

stdout:

```text
CITATION_DRIFT_ROOT: /tmp/kr19-w2-MutAliases-r5oywvgw
CITATION_DRIFT_REV_REQUESTED: FETCH_HEAD
CITATION_DRIFT_REV_RESOLVED: FETCH_HEAD
CITATION_DRIFT_BRANCH: main
CITATION_DRIFT_TABLE: /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT: rev_moving_state entry=FETCH_HEAD 'FETCH_HEAD' is a mutable pseudo-ref rewritten by Git; pass a full commit id, refs/heads/main, or an ancestor
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

### 58. restored-routed-main

```sh
python3 -I -B /tmp/kr19-w2-MutAliases-r5oywvgw/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutAliases-r5oywvgw --rev refs/heads/main --strict
# exit=0
```

stdout:

```text
{
  "defects": [
    {
      "id": "R18-MIDMAP-LISTSTEP",
      "named": true,
      "substance": true,
      "why": "non-analyze-only list receipt -> mid_checks_absent; analyze-carrying list receipt clean"
    },
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": true,
      "why": "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"
    },
    {
      "id": "R18-STRICT-BASELINE",
      "named": true,
      "substance": true,
      "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"
    },
    {
      "id": "R18-HEAD-ALIASES",
      "named": true,
      "substance": true,
      "why": "6 aliases exit 2, refs/heads/main evaluates; lint limit registered"
    },
    {
      "id": "R18-DEADSEAT-RECORD",
      "named": true,
      "substance": true,
      "why": "4 seats without a report at a245bb0, each with cause and source"
    },
    {
      "id": "R18-REGISTRY-PINNED",
      "named": true,
      "substance": true,
      "why": "both rows name an existing path or state no persisted baseline"
    },
    {
      "id": "R18-INSTALL-RECORD",
      "named": true,
      "substance": true,
      "why": "go1.24.6 and go1.25.0 recorded with full sha256 and go.dev channel"
    }
  ],
  "named_open": 0,
  "open_count": 0,
  "rev": "e382e43266d9a5c8844d3dd36bde524c4a6d87a0",
  "substance_open": 0
}
```

### 59. restoration-tree-identities

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutAliases-r5oywvgw rev-parse 'd0690fd44f46d8a7fe9da5f01c6be723d12abd41^{tree}' 'e382e43266d9a5c8844d3dd36bde524c4a6d87a0^{tree}'
# exit=0
```

stdout:

```text
b344427155950539dd93926882071beea28970a4
b344427155950539dd93926882071beea28970a4
```

