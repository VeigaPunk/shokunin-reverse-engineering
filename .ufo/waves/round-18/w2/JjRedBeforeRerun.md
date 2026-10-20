# JjRedBeforeRerun — wave-2 falsify re-run of `jj-red-before.py`

**Verdict: HOLDS**

Re-ran the round-18 C2 red/green probe and its `--selftest` at lane tip
`b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. The fresh receipt reports
`all_held: true` with **14/14 expectations held** and `not_runnable: []` —
the same outcome as the wave-1 retained evidence
`.ufo/waves/round-18/evidence/jj-red-before.json` (which was produced at
tip `9011581d…`, i.e. baseline B, so its absolute SHAs differ; see Notes).
The lane's `refs/heads/main` is unchanged before/after and the tool wrote
nothing under the lane.

## Commands and exits (all observation)

Pre-run lane state:

```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain
?? .ufo/waves/round-18/gen-wave2.py
?? .ufo/waves/round-18/w2/
?? .ufo/waves/round-18/wave2-dispatch.json
?? .ufo/waves/round-18/wave2-result.txt
?? .ufo/waves/round-18/wave2-spec.json
exit 0
$ git -C ... rev-parse refs/heads/main
b2aad08ceeee8dd125ce0d316056d8bd766c7f94
```

Main run:

```
$ python3 -I -B .ufo/waves/round-18/tools/jj-red-before.py --out /tmp/kr18w2-jjrb.json
exit 0   (receipt JSON on stdout + written to /tmp/kr18w2-jjrb.json)
```

Selftest:

```
$ python3 -I -B .ufo/waves/round-18/tools/jj-red-before.py --selftest
SELFTEST: CLEAN cases=5
exit 0
```

Post-run lane state:

```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
b2aad08ceeee8dd125ce0d316056d8bd766c7f94        # identical to pre-run
$ git -C ... merge-base --is-ancestor 9011581d... refs/heads/main && echo yes
B_ANCESTOR=yes                                # baseline still reachable
$ git -C ... status --porcelain               # exit 0
?? .ufo/waves/round-18/carriers/bin/          # new vs pre-run
?? .ufo/waves/round-18/wave2-assignments.json # new vs pre-run
?? .ufo/waves/round-18/wave2-registration.json# new vs pre-run
?? .ufo/waves/round-18/wave2-registry.json    # new vs pre-run
?? .ufo/waves/round-18/gen-wave2.py           # pre-existing
?? .ufo/waves/round-18/w2/                    # pre-existing (report dir)
?? .ufo/waves/round-18/wave2-dispatch.json    # pre-existing
?? .ufo/waves/round-18/wave2-result.txt       # pre-existing
?? .ufo/waves/round-18/wave2-spec.json        # pre-existing
```

Tool file identity (so line anchors are valid):

```
$ git -C ... show b2aad08c:.ufo/waves/round-18/tools/jj-red-before.py | sha256sum
cc2d7fb4d04b2ad6ef51d2aed52d743da780ec024defcd8891df9d4c3743a892
$ sha256sum .ufo/waves/round-18/tools/jj-red-before.py
cc2d7fb4d04b2ad6ef51d2aed52d743da780ec024defcd8891df9d4c3743a892   # identical
```

## Fresh receipt vs retained evidence (observation)

`/tmp/kr18w2-jjrb.json` (sha256 `a4fa0228…c797`) vs
`evidence/jj-red-before.json` (sha256 `b42ede20…5f5b`):

- `all_held`: true in both; `not_runnable`: `[]` in both.
- 14 expectations in both, same name set, all `held: true` in the re-run.
- New tip-sensitive values, all consistent:
  `setup.main_sha` = `b2aad08c…` (was `9011581d…`),
  `head_sha_d1` = `44acd9dcd64039b4fd5a2c743534cd7124b30aef` (new
  off-branch commit; old run's was `6bf1ca41…` — commit content differs
  because `main_sha`/tree differ, expected),
  `mutation` = `SCORECARD.md:59` entry `sc59-stanza-key-anchor` (same
  pointer-table target as before),
  `lane_tip` before == after = `b2aad08c…`.
- `baseline-citation-drift` observed `reported_rev: "HEAD"` with
  `head_is_off_branch: true`; the cited-line finding `SCORECARD.md:59`
  was present (`baseline-citation-drift-finding`) and absent at
  `--rev refs/heads/main` (`baseline-citation-drift-control`) — the red
  is content-level, not just the printed rev.
- `fixed-citation-drift` resolved `rev_resolved` to the new main tip
  `b2aad08c…` exit 0; `--rev HEAD` refused exit 2 `head_not_branch_tip`.
- `baseline-custody-capture` recorded `repo-HEAD` = the off-branch sha
  (cwd-keyed red); `fixed-custody-capture` recorded
  `repo-HEAD-is-branch-tip: no` with `repo-branch-tip` = `b2aad08c…`.
- `revpin-resolve-source` raised `RevPinError: head_not_branch_tip` at
  D1 and returned clean (`head_equals_source: true, pushed: true`) at D0.
- `baseline_extracts`: both `git show 9011581d:…` extractions exit 0
  (22376 + 65902 bytes) — B blobs still reachable.
- No `setup_error`; `setup.commands` = 7, all exits 0.
- `ls -d /tmp/jj-red-before-*` after the run shows only leftover wave-1
  output files, no `sb` sandbox dirs — the `finally: rmtree` cleanup ran
  (tools/jj-red-before.py:720-722).

## Path:line anchors at REV b2aad08c (file verified byte-identical, see sha256 above)

- `.ufo/waves/round-18/tools/jj-red-before.py:229` sandbox root is
  `mkdtemp(dir="/tmp")`; `:105-110` refuses paths under lane/fleet root.
- `:258-266` origin remote removed and asserted empty, fake
  `refs/remotes/origin/main` written by `update-ref` — cannot push to lane.
- `:350-352` lane tip captured before; `:700-704` `lane-tip-unchanged`
  expectation compares before/after — held with the new tip.
- `:706-708` `all_held` requires every runnable expectation held and no
  skips; `:709-716` receipt shape; `:1036-1042` `--out` write + exit code.
- `:903-989` selftest: 5 fixture cases (green, regressed-cd, regressed-cp,
  green-baseline, absent-tools) — all passed (`SELFTEST: CLEAN cases=5`).

## Notes / inference

- [INFERENCE] The claim in `claims.json` amendments ("jj-red-before.py
  receipt: 14/14 expectations held") is **reproduced at the delivered
  revision**: prior evidence was captured at tip `9011581d` (baseline B
  was also the tip in wave 1); the wave-1→wave-2 tip advanced to
  `b2aad08c`, and every tip-relative expectation re-anchors correctly to
  the new SHA. Not a stale-evidence artifact.
- [INFERENCE] The 4 new untracked paths in the post-run `status` delta
  (`carriers/bin/`, `wave2-assignments.json`, `wave2-registration.json`,
  `wave2-registry.json`) are concurrent wave-2 fleet artifacts, not
  products of this tool: the tool writes only under `/tmp` mkdtemp and
  the `--out` path (`tools/jj-red-before.py:229,996-1002`), and its own
  `lane-tip-unchanged` check plus my `rev-parse` before/after show
  `refs/heads/main` unmoved. Reproducing check for the lane-write claim:
  `git -C LANE rev-parse refs/heads/main` before/after — identical
  `b2aad08c…` (observation, above).
- [OBSERVATION] No installs performed; `jj 0.45.1` at
  `/home/vgpnk/.local/bin/jj`, `python3 3.14.8`, git — all pre-existing.

## Blockers

None.
