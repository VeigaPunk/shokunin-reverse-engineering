# RevBaseVerify59 — falsify R1 (`round-17/verify.py:59` = `git rev-parse HEAD`)

Scope: baseline `9011581d84527ba34c675f9cf912e54d2e72d470`; target `JjAuditKaidoku.md` §5 R1.
Read-only; only this report written. Tags: **[obs]** = observed in command output; **[inf]** = inference.

## Verdict

1. **The cited lines are still those [obs].** At `9011581d`, `.ufo/waves/round-17/verify.py:58-60` are exactly
   `base` / `source` / `dirty`, and line 59 is the **only** HEAD site in the file (grep over
   `HEAD|merge-base|symbolic-ref|origin/main` returns line 59 alone). Blob sha256
   `2896f53a…`; the line was introduced at `95e34db` and is byte-identical at `d0ab299` and `9011581d`.
2. **`source` feeds exactly four commands plus the record [obs].** Static: `verify.py:130-131`
   (`temporal-sweep --rev source`), `:134` (`controls BASE SOURCE`), `:136` (`measure SOURCE`), `:138-142`
   (`citation-drift --rev source --strict`); record `:170`, print `:183`. Empirical: every one of those argv
   in the retained `verification.json` carries `d0ab299…` (see §2).
3. **R1 is real as a code defect but latent at the current lane state [obs].** `jj-lane.sh state` says
   `head=detached` and `HEAD == refs/heads/main == refs/remotes/origin/main == 9011581d`. An unpatched run at
   this instant would record the correct revision; the hazard needs a divergence event (§3).
4. **No realized incident [obs].** `verification.json` now exists (the audit's F7 “absent/untracked” is
   stale): `source_revision=d0ab299`, `baseline_revision=b563c799`, `b31975d^ == d0ab299`, both are ancestors
   of main, and the record's pins hash `verify.py` as `2896f53a…` = the baseline blob.
5. **The minimal fix keeps `base` untouched.** The in-place fix now in the working tree (reviewed snapshot
   sha256 `b2e32624…`, 233 lines) does exactly that and satisfies every contract clause; it leaves three minor
   nits (N1–N3) and two pre-existing residuals (N4–N5).

## 1. Baseline re-read (observation)

```
$ git show 9011581d:.ufo/waves/round-17/verify.py | grep -n 'rev-parse\|status\|source_revision'
58:    base = git("rev-parse", "--verify", sys.argv[1] + "^{commit}")
59:    source = git("rev-parse", "HEAD")
60:    dirty = git("status", "--porcelain")
170:        "baseline_revision": base, "source_revision": source,
183:                      "source_revision": source}, indent=2))
exit 0

$ git show 9011581d:.ufo/waves/round-17/verify.py | sha256sum
2896f53abaa6c57aea864988ea8c5bc7072f88fc5777ce919350a71d7fcb1903  -
$ sha256sum .ufo/waves/round-17/verify.py          # before the C2 owner began editing
2896f53abaa6c57aea864988ea8c5bc7072f88fc5777ce919350a71d7fcb1903  .ufo/waves/round-17/verify.py
$ git log --oneline -S 'source = git("rev-parse", "HEAD")' -- .ufo/waves/round-17/verify.py
95e34db round-17: w2-hardened tools and frozen replicate expectations (pre-rerun)
exit 0
```

Supporting anchors: `git()` is `subprocess.check_output` with no exception handling (`:51`); the first write
is `os.makedirs(OUT)` (`:61`) after `pins_pre` (`:67`); `__file__` is itself pinned (`:65`). The `dirty` value
is record-only (`worktree_dirty_at_start`, `:171`) — it gates nothing. **[obs]**

## 2. Flow of `source_revision` (observation)

Static flow is exactly the four commands above plus the record. The committed record confirms the runtime
argv (`verification.json`, 79 commands, `unexpected_exits: []`, `pins_compare.equal: true`):

```
temporal-sweep-source  exit 0  ... --rev d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 --sites-rev b563c799…
controls               exit 0  .../controls.py b563c799… d0ab2992149a38794e5ef2474ba5d4ef5ee1e905
measure-source         exit 0  .../measure.py d0ab2992149a38794e5ef2474ba5d4ef5ee1e905
citation-strict        exit 0  .../citation-drift-probe.py --root … --rev d0ab299… --strict
```

`invocation-audit` uses `base`, not `source` (no source-run exists), so the audit's four-command enumeration
is exact. **[obs]**

The lane's citation rule is explicit: `LOG.md:2071` — “Source revision `d0ab299…` (committed and pushed
before the pass)”. A `source` that is `@-` off-branch or unpushed would therefore make both the record and
that sentence false — this is why R1's consequence chain matters even though the mechanism is narrow. **[obs]**

## 3. Is R1 real under the current lane state? (observation, then inference)

```
$ scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin
state branch=main local=9011581d84527ba34c675f9cf912e54d2e72d470 \
      remote=9011581d84527ba34c675f9cf912e54d2e72d470 ahead=0 behind=0 \
      head=detached tracked=0 untracked=1
exit 0

$ git -C … rev-parse HEAD main origin/main
9011581d…   (three identical lines)
exit 0
$ git rev-parse --verify 'refs/heads/main^{commit}';  git rev-parse --verify 'HEAD^{commit}';
  git rev-parse --verify 'refs/remotes/origin/main^{commit}'
9011581d… ×3, exit 0
$ ls -d .jj        → .jj, exit 0        # colocated
```

So the **precondition** holds (HEAD is detached) but the **material divergence does not** at this instant:
all three refs are the same commit. **[obs]**
`HEAD` resolving to the landed commit while detached (rather than to a distinct working-copy commit) is
consistent with the audit's sandbox F1/F2 and with the contract's own statement
(`contract.md:17-18`, “Git HEAD is detached after a helper commit; the branch tip is `refs/heads/main`”);
I did not run `jj` in LANE, so the `@` vs `@-` label is the audit's observation, not mine. **[inf]**

Reachability under the lane's rules:

| event | HEAD vs main | main vs origin | line 59 result | allowed? |
|---|---|---|---|---|
| quiescent helper commit + push | equal | equal | correct | yes — live state |
| helper `commit` with push failure (`jj-lane.sh:239`, exit 3) | equal | **ahead** | **records an unpushed tree silently** | yes — documented helper outcome |
| direct `jj`/`git` write in LANE | **differs** | either | records an unlanded tree | no — `contract.md:17-21` forbids it |

**[obs]** for the helper paths (`jj-lane.sh:231-239`: `@-` hash → `bookmark set main` → `push`), **[inf]** for
the classification. Net: the audit's “highest risk in the lane” label is defensible for **silent wrongness**,
but under contract-compliant operation the reachable trigger is the exit-3 push failure, not an off-branch
HEAD; the off-branch shape requires a contract violation. The guard is still worth its ~8 lines because the
failure is silent in both shapes.

## 4. Realized-incident check (observation)

```
$ python3 -c '…verification.json…'
baseline_revision = b563c799d97774aae4351276fe43cb897311e349
source_revision   = d0ab2992149a38794e5ef2474ba5d4ef5ee1e905
worktree_dirty_at_start = []      commands = 79      unexpected_exits = []   pins_equal = True
$ git rev-parse b31975d^            → d0ab299…            exit 0
$ git merge-base --is-ancestor d0ab299 9011581d   → exit 0
$ git merge-base --is-ancestor b563c799 9011581d  → exit 0
$ sha256sum .ufo/waves/round-17/verification.json ; git show 9011581d:…/verification.json | sha256sum
af312ef66cd2…  (both)                                    exit 0
pins_pre["…/verify.py"].sha256 = 2896f53a… (pre and post, size 10047)
```

`b31975d` is the commit that added the record, and its parent is the recorded source, so at run time
`HEAD == main == d0ab299`; `d0ab299` is an ancestor of the pushed tip, matching `LOG.md:2071`. The pins prove
the run used the **pre-change** bytes (`2896f53a…` = baseline blob), which is exactly the fact the round-18
contract requires the fix header to state. R1 has **never been realized** in this lane. **[obs]**

## 5. Minimal change at the baseline, and the applied fix

### 5.1 Minimal change that preserves explicit-rev behaviour

Only line 59 moves; line 58 (`base`) is untouched, so every caller-supplied rev (including the deliberately
older `b563c799` baseline) resolves exactly as before:

```python
    base = git("rev-parse", "--verify", sys.argv[1] + "^{commit}")          # 58 unchanged
    source = git("rev-parse", "--verify", "refs/heads/main^{commit}")       # was: rev-parse HEAD
    head = git("rev-parse", "--verify", "HEAD^{commit}")
    try:
        remote = git("rev-parse", "--verify", "refs/remotes/origin/main^{commit}")
    except subprocess.CalledProcessError:
        print('{"refused": true, "findings": ["branch_not_pushed"]}'); return 2
    gate = git("status", "--porcelain", "--untracked-files=no")
    if head != source: print(...); return 2        # head_not_branch_tip
    if remote != source: print(...); return 2      # branch_not_pushed
    if gate: print(...); return 2                  # worktree_dirty
    dirty = git("status", "--porcelain")           # 60 unchanged, record only
    os.makedirs(OUT, exist_ok=True)                # 61 — after the gate: zero-artifact refusal
```

Placing the gate before `os.makedirs` / `pins.snapshot` keeps a refusal free of mutations. Equality of
commit ids is the correct test: the healthy lane is **detached** yet equal, so any `symbolic-ref` /
`--abbrev-ref` / `--show-current` check would refuse the normal state. **[obs]** for the live state,
**[inf]** for the code shape.

### 5.2 Review of the in-place fix actually applied (snapshot `b2e32624…`, 233 lines)

The C2 owner landed the change while I was verifying; the file moved through three snapshots
(`2896f53a…` → `29cf2fc5…` → `b2e32624…`). Anchors below are for `b2e32624…`. Transient defects observed
during the edit (a duplicate `pins_equal` dict key, and at `29cf2fc5…` a duplicated header tail) are **gone**
at `b2e32624…` and are not reported as current.

Diff hunks (`git diff -U0`) are exactly five, and **none touches a command block**:
`@@ -9,0 +10,7 @@` (header), `@@ -53,0 +61,27 @@` (`resolve_source`), `@@ -59 +93,10 @@` (gate),
`@@ -170,0 +214 @@` (record fields), `@@ -183 +227 @@` (print). **[obs]**

Conformance check:

| requirement | anchor | verdict |
|---|---|---|
| `source` = branch tip | `:70` `refs/heads/{branch}^{commit}` | met **[obs]** |
| exit 2 unless HEAD == tip | `:71` + `:99-101` | met **[obs]** |
| tip == `refs/remotes/origin/main` | `:73-75`, `:80-81` | met; absent remote → `remote=None` → `branch_not_pushed` **[obs]** |
| tracked-clean gate (`--untracked-files=no`) | `:76`, `:82-83` | met; record-only `dirty` stays untracked-inclusive at `:103` **[obs]** |
| zero artifacts on refusal | gate `:99-101` precedes `os.makedirs` `:104` and `pins_pre` `:110` | met **[obs]** |
| record `source_branch`, `head_equals_source` | `:214` | met **[obs]** |
| header names change + `d0ab299` pre-change bytes | `:10-15` | met; verified true by pins (§4) **[obs]** |
| explicit-rev unchanged | `:92` == baseline `:58` | met **[obs]** |

Nits (all minor, none contract-breaking):

- **N1 — lint blind spot.** `head = git("log", "-n", "1", "--format=%H")` (`:71`) is HEAD resolution by other
  spelling; the docstring says this is deliberate (`:73-74`). The C2 `head-rev-lint` kinds
  (`rev-parse-HEAD`, `default-HEAD`, `HEAD-colon`, `upstream`) will not flag it, so `live_count` for this file
  drops to 0 while a HEAD read remains. Its safety now depends entirely on the equality check three lines
  later. Recommendation: add a `revisionless-log`/implicit-HEAD kind (a `git log`/`git rev-parse` with no
  revision argument) to the lint, or keep `rev-parse HEAD^{commit}` with an explicit allow-list entry.
  **[obs]** for the pattern set, **[inf]** for the regression argument.
- **N2 — finding mislabel.** The outer `except subprocess.CalledProcessError → {"findings":["branch_missing"]}`
  (`:94-98`) also catches failures of `git log` (e.g. unborn HEAD) and `git status`; those are not a missing
  branch. Wrap each resolution separately so the named finding stays true. **[obs]**
- **N3 — refusal payload.** `{"refused": true, **res}` (`:100`) omits the tracked-dirty path list, so the L1
  sees `worktree_dirty` without knowing which files; include the list (or the record's `dirty`). **[obs]**

Residuals (pre-existing, not introduced by this fix):

- **N4.** An invalid `BASELINE_REV` still raises `CalledProcessError` → traceback/exit 1 at `:92`, while the
  contract's convention is exit 2 could-not-evaluate. Baseline `:58` had the same behaviour. **[obs]**
- **N5.** The gate runs only at start; a helper commit *during* the pass (verify.py takes no lock; the helper
  takes a flock) can move `main`/`origin/main`. Every downstream command is hash-pinned, so the pass stays
  internally consistent, but the “source is the tip” reading can drift. Optional: re-check the three refs at
  the end and record `refs_unchanged_during_pass`. **[inf]**

## 6. Comparison with the round-18 contract

`contract.md:83-85` mandates exactly the preflight above, with `--untracked-files=no` and the two record
fields; §5.2 shows the applied fix meets it clause-for-clause. Two contract-level gaps worth stating:

1. **`W18/verify.py` import mechanism (`contract.md:146`).** It says the pass is “source pinned by
   `revpin.resolve_source`”. Under the mandated invocation `python3 -I -B`, the script directory is **not** on
   `sys.path` (observed: a sibling-module `import` raises `ModuleNotFoundError`, exit 1). A plain
   `import revpin` would therefore fail with exit 1, not 2. It must use
   `importlib.util.spec_from_file_location` (the existing pattern at `verify.py:50-53` in the fixed snapshot;
   baseline `:43-46`; also `tools/receipt-validate.py:92`, `tools/retain.py:57`) or insert the tools dir
   explicitly — and it must map
   `RevPinError` to exit 2 (the contract states the exception, not the exit mapping). **[obs]** for the
   `-I` behaviour, **[inf]** for the mapping requirement.
2. **Two implementations of one gate.** The in-place W17 fix inlines the logic (contract: “Inline the logic
   (stdlib)”), while `W18/verify.py` is to use `revpin`. They must be kept semantically identical; nothing in
   the contract cross-checks them. A reviewer/controls check comparing `resolve_source` output to
   `revpin.resolve_source` output on the same lane would close this. **[inf]**

**The audit's recommendation #1 over-reaches on `base`.** It says “Apply the same to `base`”; that is wrong
for this file: `base` is the *before* revision by construction (`b563c799`, an ancestor of the tip, used for
every baseline/controls comparison; `verify.py:128-134`). Pinning `base` to the branch tip would erase the
base/source pair and change explicit-rev behaviour. The contract correctly omits it, and the applied fix
leaves `:92` untouched. **[obs]** (base is an ancestor; argv in §2), **[inf]** for the consequence.

**Verifier-files check**: the r18 controls' “verifier files” no-harm clause means `corpus/lessons/*-verifier-spotcheck.md`
only (`round-17/controls.py:55`), so editing `.ufo/waves/round-17/verify.py` does not contradict it. The
retained record's pin of the old bytes (`2896f53a…`) also appears nowhere outside `verification.json`
itself, so the in-place edit invalidates no registered hash. **[obs]**

## 7. Command log (all exit codes observed)

| # | command | exit |
|---|---|---|
| 1 | `git rev-parse HEAD main origin/main` (lane) | 0 (three × `9011581d…`) |
| 2 | `scripts/hyaku/jj-lane.sh state <lane>` | 0 (`head=detached tracked=0 untracked=1`) |
| 3 | `git show 9011581d:…/verify.py \| grep -n …` | 0 (58/59/60/170/183) |
| 4 | `git show 9011581d:…/verify.py \| sha256sum` | 0 (`2896f53a…`) |
| 5 | `git log --oneline -S 'source = git("rev-parse", "HEAD")'` | 0 (`95e34db`) |
| 6 | `python3 -c … verification.json` | 0 (`d0ab299`, 79 cmds, pins equal) |
| 7 | `git rev-parse b31975d^` | 0 (`d0ab299…`) |
| 8 | `git merge-base --is-ancestor d0ab299 9011581d` | 0 |
| 9 | `git merge-base --is-ancestor b563c799 9011581d` | 0 |
| 10 | `sha256sum verification.json` vs blob at 9011581d | 0 (both `af312ef6…`) |
| 11 | `git status --porcelain --untracked-files=no` (first read) | 0 (empty) |
| 12 | `git status --porcelain` (later reads) | 0 (`M compare.py`, `M carrier-run.py`, `M verify.py` — concurrent seats) |
| 13 | gate simulation (`rev-parse`/`log`/`status`) | 0 (`head==source==remote`, `findings=["worktree_dirty"]`) |
| 14 | `python3 -I -B` sibling-import fixture (mktemp, removed) | 1 (`ModuleNotFoundError`); normal run 0 |
| 15 | `git diff -U0 -- .ufo/waves/round-17/verify.py` | 0 (five hunks, no command block) |
| 16 | `ast.parse` of the applied fix | 0 (parses; earlier duplicate dict key absent at `b2e32624`) |

## 8. Residual risk and verification gaps

- The lane was **live** during this review: three seats wrote `.ufo/waves/round-17/verify.py`,
  `tools/compare.py`, `tools/carrier-run.py`. Baseline anchors are immutable (`9011581d`); applied-fix anchors
  are pinned to sha256 `b2e32624…` and should be re-checked after the owner's final commit.
- I did **not** execute the W17 fix, its selftests, or the r18 pass (they write/have side effects); the gate
  behaviour was reproduced with the same three read-only git commands (§3).
- `HEAD` = working-copy parent (`@-`) is taken from the audit's sandbox F1/F2 and `contract.md:17-18`; no
  `jj` command was run in LANE, per contract.
- The audit's F7 (“verify.py untracked; verification.json absent”) was true at audit time but is now stale:
  both are tracked/committed at `9011581d`, and `verify.py` is byte-identical to `d0ab299`'s blob.
- No tools were installed or upgraded for this review.
