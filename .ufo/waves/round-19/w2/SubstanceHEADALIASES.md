# C1 HEAD-ALIASES — wave-2 substance review
Axes assessed: calibration (the finite C1 defect count), freshness (which revision the retained measurement represents), and depth (alias and revision-identity coverage).

## Finding

### Medium — accepted mutable branch selectors are not pinned to the identity reported

**Observation.** The R18 repair for HEAD-derived aliases is present and works for the targeted forms, but the gate’s broader “mutable `--rev`” wording is false for accepted branch references. At immutable main `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, `resolve_rev()` records the resolved commit SHA in `findings.rev_resolved` and then returns the original selector (`.ufo/gates/citation-drift/citation-drift-probe.py:390-393`). `Tree.lines()` later passes that selector, unchanged, to `git show` for each uncached file (`:135-157`). The routed check explicitly treats `refs/heads/main` as a green control if it is not exit 2 (`.ufo/waves/round-19/tools/routed-r18.py:206-213`); the resolver documents branch names/tags as “stable” (`citation-drift-probe.py:359-361`). A branch ref is mutable.

I reproduced the identity mismatch only in `/tmp/kr19-w2-headaliases.6CN0Ec`, a clone created at observed main. With `refs/heads/main` at `d0690fd…`, `resolve_rev(root, "refs/heads/main", "main", findings)` returned selector `refs/heads/main` and recorded resolved identity `d0690fd…`; after moving that clone’s ref to baseline B, `Tree(..., rev, ...).lines(".ufo/gates/citation-drift/citation-drift-probe.py")` read bytes hashing to the B blob, not the recorded main blob. The focused Python probe completed with `MUTATION_PROBE_EXIT=0`. No lane ref or production file was changed by this test.

**Inference / impact.** A concurrent ref update can make one reported evaluation read a different commit than `REV_RESOLVED`, and potentially mix identities across files. This is a false close only for the correction’s broad “mutable `--rev`” / same-identity guarantee, not for the narrow original HEAD-alias defect: canonicalize accepted selectors to the resolved commit before constructing `Tree`, or disallow mutable refs if the contract requires an immutable measurement.

## Counter and independent re-derivation

**Observed commands and exits.** I extracted the counter from the immutable main commit (blob `a9f13ee1a95fe392ca423f09c4fbcd9d9e933c7c`) with `git archive d0690fd44f46d8a7fe9da5f01c6be723d12abd41 .ufo/waves/round-19/tools/routed-r18.py` (archive/extract exit 0), then ran that extracted tool:
```bash
repo=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
tmp=$(mktemp -d)
git -C "$repo" archive --format=tar d0690fd44f46d8a7fe9da5f01c6be723d12abd41 .ufo/waves/round-19/tools/routed-r18.py | tar -xf - -C "$tmp" # exit 0
tool="$tmp/.ufo/waves/round-19/tools/routed-r18.py"
LANE="$repo"
```


```text
python3 -I -B "$tool" --root "$LANE" --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
# exit 1; open_count=7, named_open=7, substance_open=7.
# R18-HEAD-ALIASES: named=false, substance=false; aliases @, HEAD~0,
# HEAD^{commit}, HEAD@{0}, @~0, HEAD^0 each were not refused (exit 1 here).

python3 -I -B "$tool" --root "$LANE" --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
# exit 0; open_count=0, named_open=0, substance_open=0.
# R18-HEAD-ALIASES: named=true, substance=true; six aliases exit 2,
# refs/heads/main evaluates; lint limit registered.
```

The baseline counter above uses the current lane as `--root`; therefore its aliases resolved against the then-current lane checkout and returned 1, not the historical clean result. To re-derive the red behavior against baseline itself, I extracted the citation-drift gate from B and ran it against the isolated clone checked out at B: `@`, `HEAD~0`, `HEAD^{commit}`, `HEAD@{0}`, `@~0`, and `HEAD^0` each returned exit 0. This confirms the baseline gate accepted the aliases.
```bash
repo=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
clone=/tmp/kr19-w2-headaliases.6CN0Ec
git -C "$clone" checkout -q --detach 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 # exit 0
tmp=$(mktemp -d)
git -C "$repo" archive --format=tar 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 .ufo/gates/citation-drift | tar -xf - -C "$tmp" # exit 0
for rev in '@' 'HEAD~0' 'HEAD^{commit}' 'HEAD@{0}' '@~0' 'HEAD^0'; do
  python3 -I -B "$tmp/.ufo/gates/citation-drift/citation-drift-probe.py" --root "$clone" --rev "$rev" --table "$tmp/.ufo/gates/citation-drift/pointer-table.json" --expected "$tmp/.ufo/gates/citation-drift/expected.json" --strict >/dev/null 2>&1
  rc=$?; printf '%s exit=%s\\n' "$rev" "$rc"
done
# Each probe exit 0; loop/archive command completed exit 0.
rm -rf "$tmp" # exit 0
```


For immutable main gate bytes, direct CLI probes returned exit 2 with finding `rev_moving_state` for `CHERRY_PICK_HEAD` and for `main@{0}`. I also invoked the archived main gate for the six counter aliases and the eight named pseudo-refs (`ORIG_HEAD`, `FETCH_HEAD`, `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `REBASE_HEAD`, `BISECT_HEAD`, `AUTO_MERGE`); all 14 returned exit 2. The two direct findings and the classifier/ordering in `citation-drift-probe.py:331-348,384-389` establish refusal before ordinary revision resolution, not merely an unresolved-ref failure.
```bash
repo=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
tmp=$(mktemp -d)
git -C "$repo" archive --format=tar d0690fd44f46d8a7fe9da5f01c6be723d12abd41 .ufo/gates/citation-drift | tar -xf - -C "$tmp" # exit 0
for rev in '@' 'HEAD~0' 'HEAD^{commit}' 'HEAD@{0}' '@~0' 'HEAD^0' 'ORIG_HEAD' 'FETCH_HEAD' 'MERGE_HEAD' 'CHERRY_PICK_HEAD' 'REVERT_HEAD' 'REBASE_HEAD' 'BISECT_HEAD' 'AUTO_MERGE' 'main@{0}'; do
  python3 -I -B "$tmp/.ufo/gates/citation-drift/citation-drift-probe.py" --root "$repo" --rev "$rev" --table "$tmp/.ufo/gates/citation-drift/pointer-table.json" --expected "$tmp/.ufo/gates/citation-drift/expected.json" --strict >/dev/null 2>&1
  rc=$?; printf '%s exit=%s\\n' "$rev" "$rc"
done
# All 15 probe exits 2; archive/loop command completed exit 0.
rm -rf "$tmp" # exit 0
```


**Result.** No false open found for the narrow R18-HEAD-ALIASES defect: the baseline behavior is red, the exact main revision refuses the tested HEAD aliases and pseudo-refs, and the append-only correction exists in both `corpus/lessons/round-19.md:59` and `SCORECARD.md:2486`. No conclusion here on the six sibling routed defects beyond the counter output.

## Freshness, depth, and limits

- The retained `evidence/routed-r18-integrated.json:22-26,46-49` is an earlier measurement at `4f6c73f81ae8d31de18377d7ff57e4e10140ce48` (HEAD-ALIASES says six aliases; overall open_count is 1). It is not a measurement at current main. My extracted-main counter run supplies the fresh observation above; the retained integrated JSON should not be presented as the final-tip result.
- The exact main counter tests six aliases (`routed-r18.py:38-40,192-213`), not every revision expression in the lesson’s broad phrase. The main gate’s own `ALIAS_CASES` adds pseudo-ref and branch-reflog cases (`citation-drift-probe.py:539-558`); the counter itself does not call the gate selftest. The current classifier covers the tested pseudo-ref family and arbitrary `@{` selectors (`:326-348`), but counter coverage remains narrower than the prose.
- The nested `head-rev-lint` blind spot is explicitly registered, not fixed: `SKILL.md:587` names the wrapper-hidden reads at `round-17/verify.py:83` and `round-18/tools/revpin.py:108`; the lesson also keeps this in its Open list (`corpus/lessons/round-19.md:96`). The counter only checks for the path/name tokens in the SKILL row (`routed-r18.py:209-213`); it does not prove linter behavior. This is an honestly disclosed limit, not a false closure of the documented limit.
- The axis statement stays calibrated: SCORECARD reports C1’s finite proxy as 10.0→10.0 (delta 0) and says saturation/window and SHONEN status are unchanged (`SCORECARD.md:2493,2497-2499`). No broader saturation or domain-calibration claim is supported here.
- `lsp` was unavailable: `read xd://lsp` returned “No such tool” and the mounted-device list contained no LSP device. I therefore made no references/definition/diagnostics claims; source lines and the direct CLI/probe results above are the evidence. Grep was used only to locate lines, not as semantic proof.
- The worktree counter did not match the immutable main blob (`git rev-parse d0690fd…:.../routed-r18.py` = `a9f13ee…`; `git hash-object .ufo/waves/round-19/tools/routed-r18.py` = `1f48be…`). All reported counter results use the extracted immutable main blob, not that worktree copy.
