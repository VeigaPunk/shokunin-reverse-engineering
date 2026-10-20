# CustodyRepoRoot — custody-pair `repo-root` is the repository top level (r19 W1)

Carried item: `corpus/lessons/round-18.md:90` (custody-pair `repo-root` records the `--repo`
argument, not the top level; `w2/CustodyReview.md:80-84` F4). Writer seat, own clone.

- Base (observed): `git -C /tmp/kr19-CustodyRepoRoot rev-parse HEAD` →
  `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; working tree clean at clone (0 entries).
- Patch: `.ufo/waves/round-19/w1/patches/CustodyRepoRoot.patch`
  (sha256 `292d946cea9a45a70386ecc8c5b780a60a47414f65d4cc74ac6a8975aeb14fc4`, 148 lines).
  `git apply --check` against a second clean baseline clone: **exit 0**.
- `git -C /tmp/kr19-CustodyRepoRoot diff --cached --stat 8a8da7e`:

```
 .ufo/gates/custody-pair/README.md       | 11 ++++--
 .ufo/gates/custody-pair/custody-pair.py | 68 ++++++++++++++++++++++++++++++++-
 2 files changed, 74 insertions(+), 5 deletions(-)
```

## Change (observation: read from the patched clone)

- `repo_context` now reads `rev-parse --show-toplevel` and records it as `root`
  (`custody-pair.py:408-410`), keeping the `--repo` argument as the new `arg`
  (`:399`) and emitting a new metadata line `# repo-arg:` directly under
  `# repo-root:` (`:438-439`).
- Semantics stated in the docstring (`:387-396`): `root` is the top level; the
  two fields differ exactly when `--repo` names a subdirectory; they are equal at a
  repository root and for an argument outside any work tree (no top level exists,
  so the argument remains the only root the receipt can name — this preserves the
  round-18 selftest's copy-based, non-repo control).
- New red selftest case `repo-root-is-toplevel-not-subdir-arg` (`:1420-1449`): a
  self-contained fixture repo under `mkdtemp`, one empty commit on `main`, capture
  with `--repo <repo>/sub/deep`; asserts `repo-root` is the top level, that the
  subdirectory is absent from `repo-root`, that `repo-arg` carries the argument,
  and that HEAD/tip facts survive the walk-up.
- Tool docstring gains a `ROUND-19 HARDENING` paragraph (`:123-139`); `--repo`
  help text updated (`:1467-1472`); README selftest inventory corrected from the
  stale 28 to the true 31 and the round-18/round-19 case names added
  (`README.md:229-253`).
- **`receipt-version` stays 2.** Not required: `parse_receipt` splits on `^PATH:`
  and never reads the header (`custody-pair.py:514-541`), so every `#` line is
  metadata by construction; the stanza shape is byte-identical and an unchanged
  consumer accepts a new receipt (below). Changing the header is the same
  additive-metadata class round 18 used for its five header lines under v2
  (`:209`).

## Evidence (all [OBS]; commands and exits as run)

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `cd /tmp/kr19-CustodyRepoRoot && python3 -I -B .ufo/gates/custody-pair/custody-pair.py selftest` | **0** | last line: `CUSTODY_PAIR_SELFTEST: CLEAN cases=31 passed=31 failed=0 exit=0`; `EXIT=0` |
| 2 | `git -C /tmp/kr19-CustodyRepoRoot apply --check` of the patch in `/tmp/kr19-CustodyRepoRoot-apply` at B | **0** | patch applies to a clean baseline clone |
| 3 | baseline tool (blob at B, written to `/dev/shm/kr19-cr-probe/base/`) `capture --out - --paths probe.conf --repo repo/sub/deep` | **0** | `# repo-root: /dev/shm/kr19-cr-probe/repo/sub/deep` (**the defect**, F4 reproduced) |
| 4 | patched tool, same capture, `--out new-subdir.txt` | **0** | `# repo-root: /dev/shm/kr19-cr-probe/repo`, `# repo-arg: /dev/shm/kr19-cr-probe/repo/sub/deep`, `repo-branch-tip`/`repo-HEAD-is-branch-tip: yes` unchanged |
| 5 | control copy of the patched tool at `/dev/shm/.../ctl/a/b/c/` (non-repo location, round-18 mutation-harness shape) `selftest` | **0** | `CUSTODY_PAIR_SELFTEST: CLEAN cases=31 passed=31 failed=0 exit=0` — the non-repo fallback keeps `repo-arg-and-lane-root-default` green |
| 6 | mutation M1: copy with `toplevel` forced `None` (pre-fix `root` = argument) `selftest` | **3** | `case repo-root-is-toplevel-not-subdir-arg FAIL (repo-root still records the --repo argument)`; `CUSTODY_PAIR_SELFTEST: DIRTY cases=31 passed=30 failed=1 exit=3` — the new case is red on pre-fix logic and only that case flips |
| 7 | cross-revision pair: baseline-tool receipt (`--repo repo/sub/deep`) vs patched-tool receipt (`--repo repo`), verified by the **patched** tool | **0** | `CUSTODY_PAIR_VERIFY: MATCH paths=1/1 drift=0 exit=0` |
| 8 | same pair verified by the **baseline** tool (unchanged consumer) | **0** | `CUSTODY_PAIR_VERIFY: MATCH paths=1/1 drift=0 exit=0` — the new header line breaks no old consumer |

Mutation/control copies live under `/dev/shm` and were edited there only; the
clone's source and the patch contain only the four edits above.

## Risks / notes

- Behaviour change for an argument **outside** any work tree is deliberately none:
  `repo-root` still falls back to that argument (no top level exists). The residual
  F4-adjacent case `AxisHarmCheck.md:62` (a non-repo `--repo` recorded as root)
  therefore still prints the directory; `repo-arg` now makes that equality visible
  rather than implied. [INFERENCE] Judged out of the carried item's scope; flagged
  for the L1 rather than absorbed.
- Receipts captured before this patch with a subdirectory `--repo` keep the wrong
  `repo-root`; the header is metadata and `verify` never reads it, so no comparison
  outcome changes retroactively.
- `repo-root` for the default (`LANE_ROOT`) is unchanged, as case 27 still asserts
  (green in run 1 and the non-repo control run 5).
- No tool installed or upgraded (no install channel used). No carrier executed, no
  REA/Ghidra call, no `jj` command, no git write in the lane (patch written with a
  shell redirect from the clone only). Blockers: none.
