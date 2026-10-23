# CtlC1DoNothing — R31-C1 pre-data do-nothing control

Seat: KaidokuR31.CtlC1DoNothing (critic, leaf). Wave: round 31, w1. Lane base
`c369242fee9f559f895e3f7956b1242076c7b1be`, freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`
(`.ufo/waves/round-31/claims.json` first added by that commit, ct `1792728307` = 2026-10-23T04:05:07Z).

**Verdict: `CONTROL CtlC1DoNothing: met=no score=0/12`** — exit 1 under the frozen argv. The control
holds for C1, with one clause-level defect in the counter that the control itself cannot expose but
that a sibling control plus one flag can (F2 below).

## 1. Control built (nothing in the tree changed)

Sandbox clone per Contract, `git` env vars unset for every command:

```
mkdir -p /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/tmp
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C clone checkout -q -B ctl 35ba7c522dba55f9be27eb161d4254eacaa24330
# -> HEAD 35ba7c522dba55f9be27eb161d4254eacaa24330, status --porcelain: 0 lines, 2026-10-23T04:10:02Z
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C clone \
  -c user.name=ctl -c user.email=ctl@local commit --allow-empty -q -m ctl
# -> 34c2787cb46a08cfe3588c81dae1a52faf72e4f4, ct 1792728658 (2026-10-23T04:10:58Z), parent 35ba7c52
```

Tree state at the control commit, read from the clone at 04:10Z (observation):

| Path | State |
|---|---|
| `corpus/evidence/round-31/c1/envelopes/` | absent (no envelope in any ref: `git log --all --diff-filter=A -- 'corpus/evidence/round-31/c1/envelopes/*'` -> 0 lines) |
| `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | absent |
| `PROVINCE.md` | `grep -c inspect-sqlite-database` -> no match (0) |
| `corpus/evidence/round-31/c1/carriers.tsv` | present, 12 rows, equals working tree |
| `.ufo/waves/round-31/claims.json` | sha256 `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` |

No entry, no PROVINCE row, no SOURCES row, no envelope — the do-nothing input the control requires.

## 2. Counter runs (frozen argv, REA 6.5.0 live on all 12 carriers)

Both runs: cwd `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing`,
`TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/tmp`.

### 2a. Before the control commit (comparison), `--rev 35ba7c522dba55f9be27eb161d4254eacaa24330`

```
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/clone/tools/round-31/c1-sqlite-positive.py \
  --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

UTC 2026-10-23T04:10:38Z -> 04:10:49Z, **exit 1**, stderr empty, full stdout:

```
proj-341	P1-fail	committed envelope absent
proj-350	P1-fail	committed envelope absent
proj-361	P1-fail	committed envelope absent
proj-370	P1-fail	committed envelope absent
proj-371	P1-fail	committed envelope absent
chinook	P1-fail	committed envelope absent
chinook-autoinc	P1-fail	committed envelope absent
gpkg-curve	P1-fail	committed envelope absent
gpkg-curvepolygon	P1-fail	committed envelope absent
gpkg-line-zm	P1-fail	committed envelope absent
gpkg-multisurface	P1-fail	committed envelope absent
gpkg-test-gpkg-nulls	P1-fail	committed envelope absent
carriers=12 pass=0 target=12 entry_ok=0 (entry absent) province_ok=0 (no PROVINCE table row names the verb and the entry)
```

### 2b. At the control commit, `--rev HEAD` (the assigned command, run literally in bash as well)

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing && \
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/clone/tools/round-31/c1-sqlite-positive.py \
  --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/clone --rev HEAD
```

UTC 2026-10-23T04:11:02Z -> 04:11:15Z, **exit 1**, stderr empty, full stdout (byte-identical to 2a;
literal bash re-run at 04:14:43Z also byte-identical, `EXIT=1`):

```
proj-341	P1-fail	committed envelope absent
proj-350	P1-fail	committed envelope absent
proj-361	P1-fail	committed envelope absent
proj-370	P1-fail	committed envelope absent
proj-371	P1-fail	committed envelope absent
chinook	P1-fail	committed envelope absent
chinook-autoinc	P1-fail	committed envelope absent
gpkg-curve	P1-fail	committed envelope absent
gpkg-curvepolygon	P1-fail	committed envelope absent
gpkg-line-zm	P1-fail	committed envelope absent
gpkg-multisurface	P1-fail	committed envelope absent
gpkg-test-gpkg-nulls	P1-fail	committed envelope absent
carriers=12 pass=0 target=12 entry_ok=0 (entry absent) province_ok=0 (no PROVINCE table row names the verb and the entry)
```

`git -C clone status --porcelain` after the run: 0 lines — the non-write path mutates nothing.
Neither run printed `PIN ... absent or altered`, so all 12 carriers matched their frozen sha256 and
`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` was 6.5.0
(sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`) at 04:10Z.

Wall time 11-14 s for 12 live REA invocations, so the Contract's 900 s cap is comfortable.

## 3. Attack findings

### F1 — the control is refused, and only by the committed-receipt clause (observation; holds)

The reason string `committed envelope absent` is returned by `committed_check()` alone, and
`committed_check()` is reached only when `judge()` already returned `P1-pass`. Therefore every one of
the 12 live runs exited 0 with an `ok` envelope whose operation was `inspect_sqlite_database`, whose
subject sha256 equalled the frozen carrier sha256 and whose normalized result equalled the oracle —
and the control still scored 0. The single clause that held the line is, in `measure()`:

```python
if verdict == LABEL and not write:
    ok, why = committed_check(root, rev, r["id"], env, freeze_ct, entry_text or "")
```

Producing command: 2b. Exit 1. 2026-10-23T04:11:15Z. Conclusion: **holds**. `entry_ok` and
`province_ok` are secondary here — they were already 0 because the entry is absent and PROVINCE names
no such verb.

### F2 — `--write-evidence` removes the receipt clause and lets the exact frozen target line print with zero committed envelopes (observation; fails)

`--write-evidence` is a declared option of the counter and is not in the frozen command. With it,
`committed_check` is skipped entirely (the `and not write` above), and the pass count becomes 12.
Combined with two committed stub doc lines (entry file containing `S096`, one PROVINCE table row under
`## Core` naming the verb and the entry path) — no envelope, no SOURCES row, nothing produced by REA
being committed — the counter prints the frozen target line and exits 0:

```
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/clone2/tools/round-31/c1-sqlite-positive.py \
  --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/clone2 --rev HEAD --write-evidence
```

UTC 2026-10-23T04:12:51Z -> 04:13:09Z, **exit 0**, full stdout:

```
proj-341	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-350	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-361	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-370	P1-pass	tables=37 indexes=21 views=7 triggers=36 columns=395
proj-371	P1-pass	tables=38 indexes=21 views=7 triggers=36 columns=396
chinook	P1-pass	tables=11 indexes=11 views=0 triggers=0 columns=64
chinook-autoinc	P1-pass	tables=12 indexes=11 views=0 triggers=0 columns=66
gpkg-curve	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-curvepolygon	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-line-zm	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-multisurface	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-test-gpkg-nulls	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=64
carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

Same tree, same rev, frozen argv (no flag) — UTC 04:13:09Z -> 04:13:23Z, **exit 1**:

```
... 12x "P1-fail  committed envelope absent" ...
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

Probe tree: `clone2`, branches `ctl` -> `c2a7bab7ad9579d8cb6537c885c56e334e82c213` ("probe: junk doc
rows, no envelopes", ct 1792728767) on top of the control commit; the two doc edits are the stubs in
§5. The counterexample is decisive: **the frozen target line `carriers=12 pass=12 target=12 entry_ok=1
province_ok=1` plus exit 0 does not by itself prove that any envelope is committed**, when the flag is
present. The do-nothing control cannot exercise this (its doc gates are 0), but the junk-row control
plus `--write-evidence` does. This is exactly premature saturation through false provenance: an L1
that runs the collection step with `--write-evidence` and reads the exit code as the target would
admit R31-C1 with zero committed receipts, and the string comparison the claim demands would agree.

Reproduce: the run is deterministic (F3), so a re-run of the probe command on a copy of the probe tree
gives the same 12 lines and exit 0.

### F3 — live half is green and deterministic outside `meta` (observation; supports passability)

Two consecutive `--write-evidence` runs on the same tree (04:12:51Z and 04:13:37Z) produced 12
envelopes whose `strip_meta` payloads are pairwise equal (`strip_meta mismatches across two live runs:
NONE`; a third capture at 04:13:37Z reproduces stdout sha256 `4360d9e5...` exactly). The only volatile
field observed is `meta.duration` (`"298ms"` then `"186ms"` for `proj-341`); `data.evidence_id` is
stable across runs and distinct for all 12 carriers (`unique evidence_ids 12 of 12`), e.g.
`ev_a51082b2...` for proj-341 (`sha 97a04533b1e7`). Consequence (inference): the committed-vs-live
full-envelope rule of M30-3 is satisfiable — a committed envelope will still equal a later live run —
so a later genuine pass is reachable and today's `pass=0` is a receipts gap, not an unsatisfiable
predicate. It also means an entry can name an evidence_id once and stay valid.

### F4 — doc gates are read from the rev, not the working tree (observation; holds)

With the entry file and the PROVINCE row present on disk but uncommitted (`clone2` at 04:12:31Z), the
counter printed `entry_ok=0 (entry absent) province_ok=0 (...)` — `show(root, rev, ...)` is the only
source. So staging is not enough; the doc rows must be committed. Sensitivity limit (inference):
`entry_ok` is a bare substring test for `S096`, so a two-line stub entry satisfies it (F2's tree
passes with a 64-byte file). That is a content-quality gate, not a provenance gate; it does not help
do-nothing, which has no entry at all.

### F5 — the 900 s process cap and the immutables are not stressed (observation)

Twelve live REA invocations cost 11-14 s wall each run; the `/fast/scratch/hyaku/kaidoku-r31/carriers`
files were only read (12/12 sha256 matched, no `PIN` line). No chattr, copy or move was attempted.

### could-not-evaluate

- Whether `committed_check`'s "first added after the freeze" branch (`added <= freeze_ct`) rejects a
  pre-freeze envelope: untestable now — no envelope exists in any ref of the lane, and fabricating one
  before the freeze commit is impossible after the fact. Static read only (inference: it rejects,
  because `freeze_ct` is not `None` here and `added <= freeze_ct` returns False).
- Whether a committed envelope copied from another carrier's committed file under this id is rejected:
  that is the "shortcut keyed on ids/labels" control, not this seat's.

## 4. Impacted axes and smallest safe correction

- **Coverage (C1, the axis under test):** control holds; `met=no score=0/12`. The coverage gain cannot
  be claimed from this control's input class (empty receipts), which is what the control was for.
- **Calibration / provenance (basis of the `P1-pass` label):** F2 exposes that the frozen target line
  is only a receipts proof under the frozen argv. An exit-0 from an invocation carrying
  `--write-evidence` proves live-reader health plus two doc strings, nothing about committed
  envelopes.
- **Depth:** unaffected (C2's counter has its own write path and its own do-nothing control).

Smallest safe correction, in order of preference:

1. Procedural, for this round (instruments are pinned by sha256 in `claims.json` and may not be
   edited): accept the C1 target only from an invocation whose argv is exactly
   `python3 -I -B tools/round-31/c1-sqlite-positive.py --root <LANE> --rev <REV>`, record that argv in
   `LOG.md` next to the receipt, and treat any `--write-evidence` exit code as a collection result, not
   a verdict.
2. Instrument fix for the next round (one line, removes the class): in `measure()`, evaluate
   `committed_check` regardless of `write` — let `--write-evidence` dump bytes only — so a write run
   reports `pass=0` until the envelopes are committed. This leaves the documented collection workflow
   intact (write, commit, then verify with the frozen command) while making the printed target line
   impossible to reach without receipts.

## 5. Probe-only edits (scratch clone2 only; never in the lane)

```
clone2 corpus/knowledge/2026-10-23-r31-sqlite-positive.md  (64 bytes, "PROBE STUB ... S096")
clone2 PROVINCE.md  line 44 inserted under `## Core`:
  | `inspect-sqlite-database` (PROBE ONLY) | stub | stub | `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` |
```

Neither file exists in the lane, and neither was copied back.

## 6. Pins, environment, installs, sources

- REA: `npx -y rea-agents@6.5.0` through the counter only (`package.json` version 6.5.0, sha256
  `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`); no standalone REA, no MCP.
- Instrument sha256 as read in the clone (agree with `claims.json.instruments`):
  `c1-sqlite-positive.py 048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0`,
  `sqlite_oracle.py aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b`.
- Freeze: `claims.json` sha256 `6b090a3363...9e51`; first-added ct 1792728307.
- Installs: none. No pacman/uv/npx install was run in this seat.
- Sources opened over the network: none (no HTTP fetch in this seat); every input was a local file or
  the frozen counters.

## 7. Artifacts (all under /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1DoNothing/)

```
a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e  freezerev.stdout.txt        (680 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  freezerev.stderr.txt        (0 B)
a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e  ctl.stdout.txt              (680 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  ctl.stderr.txt              (0 B)
a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e  literal_head.log            (680 B)
4bd08c9d3452d2c0050ef3fe7b62c9e7d400909e45dbcb56da2eabac25e49495  probeA_write_evidence.stdout.txt          (991 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  probeA_write_evidence.stderr.txt          (0 B)
4bd08c9d3452d2c0050ef3fe7b62c9e7d400909e45dbcb56da2eabac25e49495  probeB_write_plus_docs.stdout.txt         (991 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  probeB_write_plus_docs.stderr.txt         (0 B)
a76e62b9e646e5455d8c0376f95342632fd47d05c6750c833f268a7a21d9507e  probeC_frozen_cmd_docs_no_commit.stdout.txt (680 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  probeC_frozen_cmd_docs_no_commit.stderr.txt (0 B)
4360d9e51cf1e4d5e57718efad485d618c1339ca0d347e4b8978a242801aad05  probeD_write_plus_committed_docs.stdout.txt (933 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  probeD_write_plus_committed_docs.stderr.txt (0 B)
d487177216bfee8a01b9c3d155c85be7bd4d09ce504d933376c1a6d0b8a10687  probeE_frozen_cmd_committed_docs.stdout.txt (622 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  probeE_frozen_cmd_committed_docs.stderr.txt (0 B)
4360d9e51cf1e4d5e57718efad485d618c1339ca0d347e4b8978a242801aad05  probeF_rerun_for_determinism.stdout.txt   (933 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  probeF_rerun_for_determinism.stderr.txt   (0 B)
```

Captured live envelopes, first `--write-evidence` run (`envs_run1/`, 12 JSON + 12 empty `.stderr`):

```
1858ba7d15be9c2d79370836be2bac7f6dc23db6ce9721d1e8a4ecb8ffc0edb4  proj-341.json
968f9a7a31f18aa881ac30f88e68a9925d173d56a7b17f83c9b6e8f844c89819  proj-350.json
77e73611c36f7b6548fe96ac7c8d4256cd791f5e4c0b654373c8f2a338455f36  proj-361.json
6ef70a993cf1dff36cd112c78b9a677a5e7bcaeaff5a5ef011054750571f7bc0  proj-370.json
a6456b4856557ba44383ad36b0593e333d2fcaffd7e18449155f923f5ab04433  proj-371.json
d62d9d2ab00a098a11c8c2df2b53bcdb38ad43ad38f0d96dec58af0be47a2432  chinook.json
6f4fd12504270596438590a730694220029d0e47bffef7eec9f24473b74e6a1a  chinook-autoinc.json
3215fb0a84d00152ffd2f49271fc7785c8f819f1842dfca2860ef523b634cfa1  gpkg-curve.json
aaf385379afd26a116759147f977a2920bd88c31dc4fd74d2bc36d29521ec9b2  gpkg-curvepolygon.json
a3bc4d167f336d8c79dccd8e14fd523a47f458d29d143eb864b853c9555688b8  gpkg-line-zm.json
f3f7cd9b6aa914319bcec584ffff1e070ce483431dd1295d7ade44536cb0ff56  gpkg-multisurface.json
cb470ea405a2c62485d55158de30688446b0bf7e45250c24b5460cd56504e46a  gpkg-test-gpkg-nulls.json
manifest (sorted name+sha256, sha256 of that list): 19fd2a0cbb24a3ea5055deffef4e32ab9a5b4d0b6bb83bbf3b937f73f0deae1a
```

`envs_run2/` (second run, 04:13:37Z) has the same 12 names; every file differs from run1 only in
`meta.duration` (strip_meta equality verified field by field), manifest
`6579f03f3a882946faedab0f52335e4d95db5d155fbf1cc6bfd7ba45ab3da5c2`. These envelopes are
**not** receipts: they were never committed anywhere and must not be integrated as C1 evidence.

Clone commits: `clone` = `34c2787cb46a08cfe3588c81dae1a52faf72e4f4` (`ctl`, on 35ba7c52);
`clone2` = `c2a7bab7ad9579d8cb6537c885c56e334e82c213` (probe doc stubs, on the control commit).

## 8. One-line verdict

`CONTROL CtlC1DoNothing: met=no score=0/12`
