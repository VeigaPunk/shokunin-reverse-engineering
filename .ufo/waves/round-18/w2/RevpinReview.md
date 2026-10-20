PARTIAL — revpin.py meets its contract and its docstring, and is green on the lane. But its `pushed` (ancestor) semantics contradict the operator rule at SKILL.md:579 (equality), the selftest can't tell ancestor from equality (a mutant survives), and failure attribution loses information at the consumer and at edge exits.

# RevpinReview — round-18 wave 2 falsify (revpin.py)

Target: `.ufo/waves/round-18/tools/revpin.py` at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. The working copy is byte-identical to REV: sha256 `e4e67e949f7a5cf5…` for both the file and `git show REV:…`. `git diff --quiet b2aad08 -- …/evidence/jj-red-before.json SKILL.md …/round-18/verify.py` exited 0. Axes: selftest fidelity, `pushed` semantics (ancestor vs equality), failure attribution. All anchors are at REV. The work was read-only and installed nothing. Fixtures and mutants were built under `mktemp -d` in /tmp and removed afterward. The lane's tracked tree was untouched.

## Commands at REV (observed)

```
$ python3 -I -B .ufo/waves/round-18/tools/revpin.py --selftest
red cases observed: head_not_branch_tip, branch_not_pushed, branch_missing all raised and exit 2
SELFTEST: CLEAN cases=11
EXIT=0

$ python3 -I -B .ufo/waves/round-18/tools/revpin.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
{"branch":"main","head":"b2aad08cee…","head_equals_source":true,"pushed":true,"remote":"b2aad08cee…","source":"b2aad08cee…"}
EXIT=0
```

Lane refs, read-only: `refs/heads/main` = `refs/remotes/origin/main` = HEAD = `b2aad08cee…`.

## Fixture recipes

Common setup: `CE="-c user.email=f@x -c user.name=f"`. Each `work` repo is `git init` with `-c init.defaultBranch=main`, has a bare `remote.git` added as `origin`, gets `commit -q --allow-empty -m base`, then `push -q -u origin main`.

- **F1 stale-but-pushed:** a second clone `other` fetches, runs `checkout -b main origin/main`, commits `ahead` and pushes. Then `git -C work fetch -q origin`. Result: `pushed: true`, EXIT=0.
- **F2 diverged:** F1, then `git -C work $CE commit -q --allow-empty -m local-side`. Result: `finding: branch_not_pushed`, EXIT=2.
- **F3 no remote:** an init'd repo with one commit and no `origin`. Result: `branch_not_pushed`, `remote: null`, EXIT=2.
- **F4 both conditions fail:** after the push, `commit -m unpushed`, then `checkout -q --detach`, then `commit -m off-branch`. Result: `finding: head_not_branch_tip`, `pushed: false`, EXIT=2.
- **F5 stale tracking ref:** commit c1 and c2, push, then `git -C remote.git update-ref refs/heads/main $(git -C work rev-parse main~1)`. Result: `pushed: true`, `remote = source = d224550…`, EXIT=0. But `git ls-remote remote.git refs/heads/main` prints `7d2cb3a7…` (c1).
- **F6 no arguments:** `python3 -I -B revpin.py`. Result: stdout_bytes=0, stderr_bytes=162 (usage), EXIT=2.
- **F7 nonexistent root:** `--root $R/nope`. Result: `branch_missing` with every field null, EXIT=2.
- **F8c git unfindable:** `env PATH=/nonexistent /usr/bin/python3 -I -B revpin.py --root /tmp`. Result: `FileNotFoundError: … 'git'` traceback, EXIT=1.
- **F9 remote-only branch:** `push -q origin main:side`, then `fetch`. Both `rev-parse --verify refs/remotes/origin/side^{commit}` and `HEAD^{commit}` resolve (`ecef5740…`). `--branch side` gives `branch_missing` with `head: null` and `remote: null`, EXIT=2.
- **F10 orphan HEAD:** `checkout -q --orphan fresh` over an existing main. Result: `head_not_branch_tip`, `head: null`, EXIT=2.

## What holds

1. **Ancestor semantics are implemented as documented.** revpin.py:116 is `remote is not None and _is_ancestor(lane, source, remote)`. The argument order at revpin.py:87-90 tests source ⊆ remote. Each state the docstring claims to cover (revpin.py:34) gets the right label:
   - ahead → red (selftest C2)
   - behind → green (F1)
   - diverged → red (F2)

   F1 confirms the stale-but-pushed rationale at revpin.py:34-35: an equality check would red it. [observation]
2. **Contract met.** The dict, the three findings, the CLI flags, exit 0/2 and the selftest shapes all match contract.md:51-59. contract.md says nothing about ancestor vs equality. "Exercises every finding" (revpin.py:43-44) holds. [observation]
3. **Real-jj evidence from wave 1 holds.** In `.ufo/waves/round-18/evidence/jj-red-before.json`:
   - `d0-revpin-resolve-source` held: `{head_equals_source: true, pushed: true}`.
   - `revpin-resolve-source` held: `head_not_branch_tip`.
   - `all_held: true`.

   F10 attribution (unborn HEAD → `head_not_branch_tip`) is sensible. [observation]

## Findings by severity

**M1: revpin's `pushed` contradicts the operator decision table on exactly the semantics under review.**
- SKILL.md:575-579 is in "Revision pins under jj — round 18" (SKILL.md:567). Its signal "Tip differs from `refs/remotes/origin/main`" leads to "Refuse "landed" records (`branch_not_pushed`)". That is an equality rule.
- revpin.py:116 uses ancestry instead. On F1 (the tip differs from origin/main because it is behind), revpin greens: `pushed: true`, EXIT=0. The skill says that state is refused.
- `.ufo/waves/round-17/verify.py:94` (`if remote != source:`, mandated by contract.md:83-85) matches the skill. revpin is the outlier.
- SKILL.md:588 lists revpin as the probe for this exact finding ("0 … tip pushed, 2 finding … `branch_not_pushed`").
- Reproduce: build F1, run `python3 -I -B revpin.py --root $F1/work` (EXIT=0), then `git show b2aad08:SKILL.md | sed -n 579p`.
- One side needs amending: either SKILL.md:579 should say "tip not contained in (`merge-base --is-ancestor`)", or revpin should switch to equality. [observation; which side to amend is a judgment]

**M2: the selftest can't tell ancestor from equality (mutation-confirmed).** None of F1, F2, F3 or F4 is a selftest case. Each mutant was a mkdtemp copy of revpin.py with line 116 changed using the edit tool, then run as `python3 -I -B <mutant> --selftest`:

| mutant (line 116) | selftest | behavior change observed |
|---|---|---|
| `eq`: `remote is not None and source == remote` | **CLEAN cases=11, EXIT=0 (survives)** | F1: original `pushed: true` EXIT=0 → mutant `branch_not_pushed` EXIT=2 |
| `noguard`: `_is_ancestor(lane, source, remote)` | **CLEAN cases=11, EXIT=0 (survives)** | F3: original `branch_not_pushed` EXIT=2 → mutant `TypeError: expected str, bytes or os.PathLike object, not NoneType` EXIT=1 |
| `swap`: `_is_ancestor(lane, remote, source)` | FAILED (`unpushed-api`, `unpushed-cli`, `unpushed-waived-cli`), EXIT=1, killed by C2 | — |

So whichever way M1 is settled, the gate's own self-invocation (SKILL.md:588 "same command with `--selftest`") would not catch a change in either direction. [observation]

**M3: the sole in-lane consumer drops the failure detail (consumer-side, verify.py).**
- revpin.py:28-29 says the error carries `.finding` and `.result` "so callers can still emit the observation".
- `.ufo/waves/round-18/verify.py:93-99` emits only `{"refused", "revpin_finding": str(exc), "source": "unresolved…"}`. It discards `exc.result`.
- A refusal record therefore can't tell F3 (`remote: null`, no remote) from F2 (diverged), or show which sha HEAD was on.
- verify.py:92 is the only real `resolve_source` call on the lane at REV, checked with tree-wide `git grep -n 'resolve_source('`. `measure.py:579`'s `import revpin` is inside the stub string `STUB_HEAD_OK` (measure.py:577-599), and jj-red-before.py targets a sandbox.
- Reproduce: read the code at `git show b2aad08:.ufo/waves/round-18/verify.py | sed -n 90,99p`. [observation of code; the impact is inference]

**L1: a stale remote-tracking ref gives a silent green.** F5: `pushed: true`, EXIT=0, while the remote's main is the parent commit. The tip is not reachable from the remote's `main`. Revpin's definition (revpin.py:32-33) is local-ref-only, and SKILL.md:579's Limit column admits the cause ("`origin/main` is the last fetched position, not live remote state"). Neither revpin's docstring nor its output carries this caveat, though. `git ls-remote origin refs/heads/<branch>` is read-only and would close the gap. [observation; the operational impact is inference]

**L2: exit 2 is overloaded.** F6: an argparse usage error (revpin.py:303-304) exits 2 with an empty stdout. contract.md:57-58 and revpin.py:41-42 define exit 2 as a named finding with JSON on stdout. A caller that keys on exit 2 and then parses stdout gets nothing. [observation]

**L3: a multi-failure run reports one finding, and the order is undocumented.** F4 names only `head_not_branch_tip`, although `pushed: false` is in the dict. The head-before-pushed precedence (revpin.py:118-121) is stated in neither the docstring nor the contract. [observation]

**L4: `branch_missing` is a catch-all, and its result is less than best-effort.** F7 (no repo), F9 (remote-only branch) and selftest C4 (non-repo, unborn) all return an all-null dict. revpin.py:99-107 raises before resolving HEAD or the remote. In F9 both of those resolve (`ecef5740…`), yet the output reports `head: null` and `remote: null`. [observation]

**L5: unhandled exception when git is missing.** F8c: a traceback and EXIT=1 with no JSON, which is outside the 0/2 contract (revpin.py:41-42). [observation]

## Residual risk / verification gaps

- Not tested: ancestry faked through `refs/replace/` or a shallow boundary. [inference: merge-base honors both; contrived for this lane]
- F8b (`env -i`, PATH unset) did not isolate the git-missing path, because Python falls back to `os.defpath` and still finds `/usr/bin/git`. F8c is the valid reproduction. [inference for the cause]
- `pushed` currently has three meanings at REV:
  - revpin uses ancestry.
  - r17 verify.py:94 and SKILL.md:579 use equality.
  - citation-drift-probe.py has no remote check at all: `grep -i -E 'origin|remote|pushed'` exited 1. That matches contract.md:73-77.

  jj-red-before.py:863's fixture stub uses existence only (`remote is not None`). The same lane state (behind origin) is green for r18 verify and red for r17 verify. [inference from code]
