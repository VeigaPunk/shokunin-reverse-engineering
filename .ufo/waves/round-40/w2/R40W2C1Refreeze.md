# R40W2C1Refreeze — C1 path-suffix fix prototype (round-41 evidence, NOT a claim)

**VERDICT: DEFECTS FOUND** — R40-C1's 3/4 at `42c10a58` is a counter defect, not a carrier defect.
Replacing `same_rel`'s suffix rule with exact matching relative to the chunk extract root makes the
*same committed receipts*, the same frozen tables and a fresh REA rerun of every carrier score
`carriers_matched == 4`, all bindings true, exit 0 — while the round-40 counter scores 3/4 on the
identical git history.

What I attacked: the L1's reading that L2's only failing clause (`nonregular_unpublished_ok`) is a
`usr/bin/busy` vs `bin/busy` path-suffix false positive. I reproduced it from the committed bytes,
patched `tools/round-40/c1-counter.py` in a sandbox clone, added both-direction selftest cases, ran
the selftest, and re-scored the committed receipts at `42c10a58` against a vendor cache whose bytes
re-hash to the frozen pins. Nothing in the lane was written: every edit is in
`/fast/scratch/hyaku/kaidoku-r40/R40W2C1Refreeze/fx.*/lane` clones (removed at the end).

## 1. The defect, reproduced (not argued)

`same_rel` at `42c10a58` (`tools/round-40/c1-counter.py:610`, byte-identical to HEAD for
`tools/round-40/`):

```python
def same_rel(candidate, rel):
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))
```

Receipt paths are `<chunk>_extract/<rel>` (`firmware.bin_extract/…` in all four committed receipts);
the oracle and non-regular tables are relative to the extracted filesystem's root. So the rule is a
suffix test of a *path* against a *path*, and `firmware.bin_extract/usr/bin/busy` ends with
`/bin/busy`.

L2 is the one carrier where that fires, and the two paths are genuinely different directory entries:

| fact | value | source |
|---|---|---|
| non-regular row (`L2/nonregular.tsv`) | `bin/busy` — `symlink` — target `/usr/bin/busy` | committed table |
| published regular file | `firmware.bin_extract/usr/bin/busy`, sha256 `e28f81fc56768810…`, 40000 bytes | `L2/after.json` |
| counter verdict at `42c10a58` | `carriers_matched 3`, exit 1, L2 `nonregular_unpublished_ok false`, `nonregular_published ["firmware.bin_extract/usr/bin/busy"]` | `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json` |

`usr/bin/busy` is the symlink's *absolute target* — a real file of the image that the oracle lists as a
regular file — so the carrier publishes exactly what it should, and the counter read that publication as
a materialised symlink. Collision counts under the suffix rule, computed on the committed receipts:
V1 0, V2 0, L1 0, **L2 1**. Oracle coverage is unaffected by exact matching: exact hits equal oracle rows
on all four (V1 697/697, V2 8/8, L1 7/7, L2 6/6).

## 2. The patch

Two functions replace the suffix rule (full patch: `c1-counter-exact-match.diff`, 213 lines,
sha256 `8fa0a813…c0a8`, applies cleanly with `git apply --check` to the pristine `42c10a58` counter,
patched file sha256 `8e19a016…`):

```python
def extract_rel(path):
    """A receipt path relative to its chunk extract root. …"""
    if not isinstance(path, str):
        return None
    p = path
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    parts = [x for x in p.split('/') if x not in ('', '.')]
    if parts and parts[0].endswith('_extract'):
        parts = parts[1:]
    return '/'.join(parts)


def same_rel(candidate, rel):
    """Exact match of a receipt path against a filesystem-relative path. …"""
    return bool(rel) and bool(candidate) and extract_rel(candidate) == rel
```

Only the *leading* component is dropped when it is the extract root, so a nested extraction
(`a_extract/b_extract/x` → `b_extract/x`) can never stand in for an outer oracle row. The three
clauses that use the function all become exact: `oracle_hits_ok`, `nonregular_unpublished_ok` and the
path-resolved half of `gaps_ok`; none is relaxed. `rel_suffix` (projection only) is untouched, and the
docstrings that stated "suffix" now state the exact rule.

## 3. Selftest

| counter | cases | green_ok | red_ok | failures | exit |
|---|---|---|---|---|---|
| round-40 frozen (`42c10a58`) | 70 | 5 | 65 | 0 | 0 |
| patched (exact) | **75** | 7 | 68 | 0 | 0 |
| suffix mutant (exact **∪** suffix, i.e. round-40 semantics) | 75 | 6 | 66 | 3 | 1 |

New cases (V2 fixture; `oracle_over`/`nonreg_over` plumbing added to `build`/`frozen_files` so an oracle
row can be varied per case):

1. `regular usr/bin/busy is not the symlink entry bin/busy` — expect met (the L2 false positive).
2. `regular bin/busy is not the symlink entry usr/bin/busy (reverse)` — expect met (guards an
   over-strict or reversed fix; this direction was already green under the suffix rule).
3. `regular file at the entry path itself is a materialised symlink` — expect
   `nonregular_unpublished_ok` red (the true positive the clause exists for).
4. `deeper file with the oracle row sha256 does not publish oracle bin/busy` — expect
   `oracle_hits_ok` red (the collision in the oracle direction).
5. `gap on usr/bin/busy does not resolve to the symlink entry bin/busy` — expect `gaps_ok` red (the
   collision in the gap-resolution direction).

Mutant control (`mutant-suffix-matcher.diff`, sha256 `0a1cb6fc…`): re-adding the suffix alternative
(`candidate == rel or candidate.endswith('/' + rel) or extract_rel(candidate) == rel`) turns exactly
cases 1, 4 and 5 red and leaves 2 and 3 green — the three failure lines are recorded verbatim in
`selftest-suffixmut.txt`. So each new case is load-bearing in one direction and none of the 70 inherited
cases depends on suffix matching.

## 4. Scoring the committed receipts

Sandbox clones only; `git rev-parse --show-toplevel` asserted on each before any commit; fixture identity
`-c user.name=fx -c user.email=fx@fx`. Vendor carriers came from a cache copied out of
`/fast/scratch/hyaku/kaidoku-r40/_l1/cache` and were re-hashed to the frozen pins by the counter itself
(V1 `ac4098bd…`, V2 `5ccc7614…`); no vendor bytes entered the lane.

| # | counter / tree | rev | freeze | carriers_matched | bindings | exit |
|---|---|---|---|---|---|---|
| 1 | patched, real history, patch uncommitted in the worktree | `42c10a58` | `7fce3086` | **4** | all true | **0** |
| 2 | patched, reconstructed freeze-clean history (patch inside the freeze commit) | `2053b953` | `c7457af1` | **4** | all true | **0** |
| 3 | round-40 counter, same reconstructed history (control) | `2053b953` | `c7457af1` | 3 | L2 `nonregular_unpublished_ok` false | 1 |
| 4 | patched, demotion tip | `4d62ee5` | `7fce3086` | **4** | `province_core_section`, `province_core_row` false | 1 |

Run 1 (`score-1-exact-wt.json`): `met_target true`, `frozen_path_changed []`, `projection_profile
plus-extractor`, and `projection_ok true` on all four — every carrier re-ran through
`npx rea-agents@6.5.0 extract-firmware --max-depth 1` at scoring time and matched its committed receipt,
V1's 697 files included.

Run 2 exists because run 1's patch is uncommitted, which the drift check cannot see. Rebuilding the
history as two commits (freeze = `42c10a58` tree with the patched counter and **no** `after.json`;
then receipts added) puts the fix on the lawful side of the freeze rule: the range touches only the four
receipt files, `frozen_path_changed` is empty, and the score is still 4/4. Run 3 is the identical history
with the round-40 counter: 3/4, exit 1, L2 `nonregular_published ["firmware.bin_extract/usr/bin/busy"]`.
The 3→4 delta is therefore caused by the matcher and by nothing in the reconstruction.

Run 4 is calibration for the plan, not for the round-40 verdict: the demotion commit removed the
`## Round-40 additions to Core` heading, so carriers score 4/4 at the tip but the documentation bindings
fail. A round-41 re-pin is not "re-score with a fixed counter" — it needs the Core row restored *and*
the fixed counter committed at or before a new freeze.

## 5. What this is not

- **Not admissible under P40-C1 and not a claim.** `tools/round-40/c1-counter.py` is a frozen C1 path, so
  any post-freeze edit trips `frozen_path_changed` (by design). The prototype shows what a round-41
  freeze would measure; it does not re-open or upgrade the round-40 landing. Unless the L1 re-opens with
  a fresh freeze, the honest record stays "3/4, honest stop" — with the now-measured cause attached.
- No claim that the receipts are genuine beyond what the counter already checks: the rerun projection
  passing on all four is the same evidence the frozen run had, not new provenance.
- I did not touch the lane, the carriers, the tables, the docs or VCS state; the lane's
  pre-existing `M SKILL.md` is another seat's in-flight edit and was left alone.

## 6. Residual risks for the round-41 design

- `rel_suffix` (projection keys only) still strips at the first `*_extract` component *anywhere* in a
  path, not only at the root: an image path like `usr/foo_extract/bar` would collapse to `bar`. Zero
  such paths exist in the four receipts (checked over all 1066 file/unpublished rows), and the projection
  applies it to both sides, so it cannot have produced this defect — but it is the same class of
  conflation and worth tightening when the file is next frozen.
- Exact matching fails **closed**: a receipt whose chunk directory is not `<x>_extract` would now fail
  `oracle_hits_ok` instead of matching loosely. unblob's `extract-firmware` always names it that way, so
  this is a no-op today and a loud red (not a silent green) if REA's naming ever changes.
- The five new cases run on fixture carriers; the real-data proof is the L2 re-score in run 1/2.
- `extract_rel` drops only the leading root; a receipt that keeps `$output/` handled, one that carries an
  absolute output path prefix (`/fast/scratch/…/firmware.bin_extract/…`) would *not* have its root found
  by this function, because the root is no longer the first component. No committed receipt does that
  (`relative_path` is `<chunk>_extract/…` in all four), but round 41 should either normalize absolute
  path prefixes the way `rel_suffix` does or assert the shape.

## 7. Artifacts

`.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/`

| file | content | sha256 |
|---|---|---|
| `c1-counter-exact-match.diff` | the patch (213 lines, apply-checked at `42c10a58`) | `8fa0a813…c0a8` |
| `mutant-suffix-matcher.diff` | the one-hunk suffix mutant used as control | `0a1cb6fc…d8e4` |
| `selftest-exact.txt` | 75 cases, 7/68, no failures, exit 0 | `ae3c6141…37f9` |
| `selftest-suffixmut.txt` | 75 cases, 3 failures, exit 1 | `5b1ab6ab…99bc` |
| `selftest-orig-round40.txt` | frozen counter baseline: 70 cases, 5/65, exit 0 | `fa876cd5…f024` |
| `score-1-exact-wt.json` | patched, real history, `42c10a58` → 4/4 exit 0 | `9eb09845…9d3a` |
| `score-2-exact-recon.json` | patched, freeze-clean history → 4/4 exit 0 | `31d613e2…ea4` |
| `score-3-orig-recon.json` | round-40 counter, same history → 3/4 exit 1 | `4689151a…29c3` |
| `score-4-exact-tip.json` | patched at `4d62ee5` → 4 carriers, doc bindings false, exit 1 | — |
| `summary.json` | machine-readable roll-up of everything above | — |

## 8. Commands and exit codes

All with `TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku`, `S=/fast/scratch/hyaku/kaidoku-r40/R40W2C1Refreeze`,
`PKG=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.

```text
git clone -q --shared <lane> $D/lane ; git -C $D/lane checkout -q 42c10a58…    # toplevel asserted
python3 -I -B tools/round-40/c1-counter.py --selftest --pkg65 $PKG             # patched: exit 0, 75/7/68
python3 -I -B tools/round-40/c1-counter-suffixmut.py --selftest --pkg65 $PKG   # mutant:  exit 1, 3 failures
python3 -I -B tools/round-40/c1-counter-orig.py --selftest --pkg65 $PKG        # frozen:  exit 0, 70/5/65
python3 -I -B <patched> --root $D/lane --rev 42c10a58… --freeze 7fce3086… \
  --pkg65 $PKG --carrier-cache $S/cache --json-out score-1-exact-wt.json       # exit 0, 4/4
python3 -I -B <patched>  --root $D2/lane --rev 2053b953… --freeze c7457af1… …  # exit 0, 4/4
python3 -I -B <orig>     --root $D2/lane --rev 2053b953… --freeze c7457af1… …  # exit 1, 3/4
python3 -I -B <patched>  --root $D/lane  --rev 4d62ee5…  --freeze 7fce3086… …  # exit 1, carriers 4/4
```

Wall clock: 7.6 s selftest, 8.6 s / 16.7 s / 8.9 s per score run (four REA reruns inside each).

## 9. Tooling

No installs and no upgrades, so nothing to record beyond the pinned tools actually used: `npx
rea-agents@6.5.0` from the existing npx cache, `~/.local/bin/unblob` 26.6.4 untouched (never
reinstalled or moved), `sasquatch-v4be` on PATH for the `squashfs_v4_be` handler. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40W2C1Refreeze` was removed after the artifacts were copied out.
