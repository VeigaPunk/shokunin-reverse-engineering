# RevpinWording — revpin.py `@-` wording fix (R19 w1, calibration)

Seat `KaidokuR19.RevpinWording` (`wave1-assignments.json:9`; spec `wave1-spec.json:48`).
Axis: **calibration** (tied-lowest 10.0, `claims.json:7`); freshness checked; depth not claimed.
Move: docstring/comment wording only — corrects the carried item at `corpus/lessons/round-18.md:92`
and cites S036. No code, no behavior, no fixture change.

## Delivered

- Patch: `.ufo/waves/round-19/w1/patches/RevpinWording.patch` — `a11a7d21233fc10b48dc314f4f0a7b754933d0ca0308231b4c42f33de048841f`,
  `git diff --cached --stat B`: `.ufo/waves/round-18/tools/revpin.py | 17 +++++++++++------`, 1 file changed, 11 insertions(+), 6 deletions(-).
- `git -C /tmp/kr19-RevpinWording-check apply --check` against a fresh clone at `8a8da7e…` (exit 0) and at lane main `85589ac…` (exit 0); a real `git apply` at B reproduces the edited blob exactly (`revpin.py` sha256 `1272ea1a…` on both sides, exit 0).

Changed locations in the delivered blob (clone at B, blob `e4e67e94…` → edited):

| anchor | change |
|---|---|
| `.ufo/waves/round-18/tools/revpin.py:5-8` | Added `Source: S036 (corpus/SOURCES.md); jj 0.45.1 docs/git-compatibility.md lines 114-116 (usually a detached HEAD with no current branch) and 208 (the colocation recipe points .git/HEAD at the working-copy commit's parent).` [OBS] |
| `:10-11` | `HEAD detached on the working-copy commit` → `HEAD detached on the working-copy parent (`@-`, the commit before the working-copy commit `@`)` [OBS] |
| `:216` | Selftest C3 comment `the jj working-copy shape` → `the jj working-copy-parent shape` [OBS] |

`grep -n 'working-copy'` after the edit returns only `:7,:10,:11,:216`, all now parent-correct (exit 0).
No other line in `revpin.py` repeats the error: `HEAD^{commit}` reads at `:18,:96,:108,:174,:189,:290,:296` are
subject-label reads, not claims that HEAD names the working-copy commit [OBS].

## Selftest (final delivered revision)

```
red cases observed: head_not_branch_tip, branch_not_pushed, branch_missing all raised and exit 2
SELFTEST: CLEAN cases=11
SELFTEST_EXIT=0
```

Exact last line `SELFTEST: CLEAN cases=11`; exit code `0`. Run as `python3 -I -B revpin.py --selftest` in
`/tmp/kr19-RevpinWording/.ufo/waves/round-18/tools/`. This proves syntax/fixture health only; the edit is
docstring/comment text, so no behavior claim beyond the unchanged code is made [OBS].

## Command ledger (every command, with exit)

| # | command | exit |
|---|---|---|
| 1 | `git -C LANE cat-file -t 8a8da7e…` + `git show -s --format='%H %s'` for B and main | 0 (B = `8a8da7e… round-18 verifier spot-check…`; main = `85589ac… round-19: declared claims…`) |
| 2 | `git -C LANE rev-parse refs/heads/main`; `rev-parse HEAD` | 0 (both `85589ac…`; lane main is one round-19 declaration commit past B) |
| 3 | `git -C LANE status --porcelain -- revpin.py corpus/SOURCES.md` | 0 (empty) |
| 4 | `git clone -q --no-hardlinks LANE /tmp/kr19-RevpinWording`; `checkout -q --detach B`; `rev-parse HEAD`; `status --porcelain \| wc -l` | 0 (`HEAD = 8a8da7e…`, dirty count `0`) |
| 5 | `git show B:.ufo/waves/round-18/tools/revpin.py \| sha256sum`; worktree `sha256sum` | 0 (both `e4e67e94…`; baseline blob confirmed) |
| 6 | `git -C LANE diff --stat B 85589ac… -- revpin.py corpus/SOURCES.md` | 0 (empty: target unchanged B→main) |
| 7 | `awk 'length>79' revpin.py` after edit v1 / v2 | 0 (only pre-existing `:144`=80, then `:145`=80 after the +1-line docstring; untouched) |
| 8 | `python3 -I -B revpin.py --selftest` (v1 wording) | 0 (`SELFTEST: CLEAN cases=11`) |
| 9 | `python3 -I -B revpin.py --selftest` (final wording, table above) | 0 |
| 10 | `git add -A`; `git diff --cached --binary B > …/RevpinWording.patch` | 0 (patch sha `bf3e450a…`, then normalised prefixes → `a11a7d21…`) |
| 11 | `git -C /tmp/kr19-RevpinWording-check apply --check <patch>` at B / at `85589ac…`; `git apply` at B + `sha256sum` both sides | 0 / 0; 0 (`1272ea1a…` both sides) |
| 12 | `git config --show-origin --get diff.mnemonicPrefix`; `--get diff.dstPrefix` | 0 (`file:/home/vgpnk/.config/git/config true`); 1 (unset) |
| 13 | exploratory `ls …/w1/patches` before creation | 2 (absent; created with `mkdir -p`) |

No installs, no upgrades, no REA/Ghidra/`jj` invocation, no carrier execution.

## Calibration / freshness notes

- [OBS] S036 (`corpus/SOURCES.md:42`) registers the row as "jj usually leaves the Git repo in a
  detached-HEAD state with no current branch" with anchors `114-116` and `208`, tag `v0.45.1`. The
  working-copy-parent sentence is recipe commentary at `docs/git-compatibility.md:208` (quoted in
  `.ufo/waves/round-18/w1/CriticSourcedClaim.md:74-75`), not the prose at `114-116`; the docstring keeps
  that distinction ("the colocation recipe points…") and says "usually" for the prose claim.
- [OBS] Sibling lane tools already use the parent wording: `.ufo/waves/round-17/verify.py:74-75`,
  `.ufo/gates/custody-pair/custody-pair.py:366-367`. No lane doc besides `revpin.py:6` (now fixed) carried
  the wrong form — `grep 'working-copy|working copy'` over round-18 `contract.md` and `SKILL.md` exit 1.
- [INF] No live `jj` observation was made (contract forbids running `jj` in the lane); the parent semantics
  rest on S036's recipe line plus the round-18 sandbox receipts already routed at
  `corpus/lessons/round-18-verifier-spotcheck.md`. The lane at dispatch happened to have
  `HEAD == refs/heads/main == 85589ac…`, which does not exercise the `@`/`@-` divergence — the fix is
  textual correctness, not a new measurement.

## Risks / blockers

- Docstring/comment-only; the selftest result is of unchanged logic. The only risk is citation fidelity,
  mitigated by citing S036's exact anchors and its "recipe" qualification [INF].
- Patch prefixes were normalised to `a/`…`b/` because the host git config (`~/.config/git/config`) sets
  `diff.mnemonicPrefix=true`, which would otherwise emit `c/`…`i/`; both forms apply (`git apply --check`
  exit 0 at B and main). If the L1 expects `<agent-id>.patch` rather than `<seat>.patch`
  (`wave1-assignments.json:9`), rename on integration — content is unchanged.
- No blockers. LANE writes: this report and `w1/patches/RevpinWording.patch` only.
