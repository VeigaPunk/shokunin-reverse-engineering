SELFTEST COVERAGE GAP — 5 of 8 single-clause mutants survived (C1: 4/4; C2 v3: 1/4). No frozen acceptance target was evaluated.

# A2SelftestHoles — round 32 attempt 2

- UTC: 2026-10-23T06:46:07+00:00 through 2026-10-23T06:49:45+00:00.
- Axes: **coverage** (entry source, complete envelope/evidence association, post-freeze provenance) and **calibration** (description threshold, frozen anchors, reverse closure).
- Result: **3 killed, 5 survived, 0 inconclusive**. Every pristine and restored invocation exited 0 with `selftest cases=18 failures=0`.
- Exactly eight private one-line mutations; exactly 24 existing `--selftest` invocations. Independent fixtures ran concurrently within each pristine/mutated/restored phase. Restored exact frozen source bytes in `finally` before the restored phase.
- No data/carrier access, live REA, Ghidra, carrier execution, production counter change, target/predicate change, Git/jj write, model/runtime switch, subagent dispatch, or held-item inspection.
- No tools installed or updated. Read operator rules first. `/fast` space check before fixture creation: 245 GiB available (70% used); no rebuild performed.

## Frozen inputs and local sandbox provenance

Sandbox is an eight-directory source extraction, not a Git clone; its provenance is the following immutable source revisions. Each `git show` exited 0 with empty stderr.

| Source | Frozen revision | SHA-256 |
|---|---|---|
| `tools/round-32/c1-arm64x-positive.py` | `9a73680af21b002e3b99956c89234b2bbde2a71b` | `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a` |
| `tools/round-32/c2-capability-calibration-v3.py` | `f382e3b7978e6091a19ca93277c15a75c0016b43` | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` |
| `tools/round-32/arm64x_oracle.py` | `9a73680af21b002e3b99956c89234b2bbde2a71b` | `17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686` |

Exact read-only extraction argv (the child environment separately omitted `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`):
```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 9a73680af21b002e3b99956c89234b2bbde2a71b:tools/round-32/c1-arm64x-positive.py
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show f382e3b7978e6091a19ca93277c15a75c0016b43:tools/round-32/c2-capability-calibration-v3.py
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 9a73680af21b002e3b99956c89234b2bbde2a71b:tools/round-32/arm64x_oracle.py
```

Each counter quote below is a single source clause (under 25 words), re-opened on the actual private frozen file on 2026-10-23 before mutation. The source links identify its file and line; hashes above identify original bytes. No external-source conclusions are made.

## Mutation table

| ID | Clause location | Observed single-clause replacement | Pristine / mutant / restored exit | Mutant stdout summary | Verdict |
|---|---|---|---|---|---|
| C1-1 | [L132](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C1-1/c1-arm64x-positive.py#L132) | `if CLAIM_ROW not in text:` → `if not text:` | 0 / 0 / 0 | `selftest cases=18 failures=0` | **survived** |
| C1-2 | [L121](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C1-2/c1-arm64x-positive.py#L121) | `if strip_meta(committed) != strip_meta(live):` → `if committed.get("data") != (live or {}).get("data"):` | 0 / 0 / 0 | `selftest cases=18 failures=0` | **survived** |
| C1-3 | [L124](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C1-3/c1-arm64x-positive.py#L124) | `if not eid or eid not in entry_text:` → `if not eid:` | 0 / 0 / 0 | `selftest cases=18 failures=0` | **survived** |
| C1-4 | [L115](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C1-4/c1-arm64x-positive.py#L115) | `if freeze_ct is None or added is None or added <= freeze_ct:` → `if freeze_ct is None or added is None or added < freeze_ct:` | 0 / 0 / 0 | `selftest cases=18 failures=0` | **survived** |
| C2-1 | [L168](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C2-1/c2-capability-calibration-v3.py#L168) | `if len(shared) < MIN_DESC_WORDS:` → `if len(shared) <= MIN_DESC_WORDS:` | 0 / 0 / 0 | `selftest cases=18 failures=0` | **survived** |
| C2-2 | [L163](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C2-2/c2-capability-calibration-v3.py#L163) | `good = sorted(p for p in set(rel_paths(cells[2], True)) if p in anchors and exists(p))` → `good = sorted(p for p in set(rel_paths(cells[2], True)) if exists(p))` | 0 / 1 / 0 | `selftest cases=18 failures=2` | **killed** |
| C2-3 | [L163](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C2-3/c2-capability-calibration-v3.py#L163) | `good = sorted(p for p in set(rel_paths(cells[2], True)) if p in anchors and exists(p))` → `good = sorted(p for p in set(rel_paths(cells[2], True)) if p in anchors)` | 0 / 1 / 0 | `selftest cases=18 failures=1` | **killed** |
| C2-4 | [L180](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C2-4/c2-capability-calibration-v3.py#L180) | `named = rounds_named(cells[-1]) & closed` → `named = rounds_named(cells[-1]) & {n for n, _ in stmts}` | 0 / 1 / 0 | `selftest cases=18 failures=1` | **killed** |

Expected detector in every row: the unchanged existing `--selftest` should exit nonzero if it discriminates the mutated clause. This is an expected contract-sensitive detector, not a claim that the existing suite already contained each required case.

## Concrete missing checks and observed kills

Defect effects and the proposed discriminatory inputs in this section are **[INFERENCE] from the one-line changes and frozen source**. Only the existing selftests above were executed; no supplementary function-level or end-to-end acceptance probe was run.

- **C1-1 — entry source (survived):** Accept any nonempty entry instead of requiring S099. Required discriminator: A nonempty entry with no S099 must fail entry_ok.
- **C1-2 — full-envelope association (survived):** Compare data payload only; ignore non-meta outer envelope fields. Required discriminator: Same data with a changed committed top-level ok or other non-meta field must fail committed_check.
- **C1-3 — entry evidence association (survived):** Stop requiring the live evidence_id to appear in the entry. Required discriminator: A live evidence_id omitted from entry text must fail committed_check.
- **C1-4 — post-freeze provenance (survived):** Accept first-added timestamps equal to the freeze. Required discriminator: An otherwise valid envelope first added exactly at freeze_ct must fail committed_check.
- **C2-1 — description-overlap boundary (survived):** Require at least six rather than at least five shared words. Required discriminator: An otherwise valid row with exactly five distinct anchored words must match.
- **C2-2 — frozen anchor membership (killed):** Accept a resolving evidence path that is not a frozen anchor. Required discriminator: Existing irrelevant-but-resolving path and fake-outside-anchor selftests must fail the mutant.
  Captured failing case(s):
  ```text
  FAIL	irrelevant but resolving evidence path	match=4 reverse=0
  FAIL	fake outside anchor row added at REV is ignored	match=4
  ```
- **C2-3 — anchor path resolution (killed):** Accept a frozen anchor path absent from the revision tree. Required discriminator: Existing anchor-path-not-in-the-tree selftest must fail the mutant.
  Captured failing case(s):
  ```text
  FAIL	anchor path not in the tree	match=4 reverse=0
  ```
- **C2-4 — reverse closure (killed):** Reverse-check only rounds with capability statements, omitting closed rounds with none. Required discriminator: Existing over-claim-row-for-round-30 selftest must fail the mutant.
  Captured failing case(s):
  ```text
  FAIL	over-claim row for round 30	match=4 reverse=0
  ```

Bounded source explanation: C1 selftest lines 226–277 invoke `judge` and `province_ok`, not `entry_ok` or `committed_check`. Its four survivors are uncovered source-citation/commit-association clauses, not observed acceptance-counter shortcuts. C2 selftest lines 233–254 use a shared long description and a junk description, but no exactly-five-shared-word passing row; the threshold-tightening mutant survived. The anchor-membership, anchor-resolution and closed-round-with-no-capability reverse mutants were each killed by their named existing negative controls.

## Exact detector argv

Each listed argv was run unchanged three times on the same private path: pristine, mutated, restored. CWD was the scratch root below; `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were absent from the child environment. The timeout and prlimit apply to each fixture independently.

CWD: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles`

```sh
timeout --kill-after=5s 900s prlimit --as=4294967296 --fsize=1048576 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C1-1/c1-arm64x-positive.py --selftest
timeout --kill-after=5s 900s prlimit --as=4294967296 --fsize=1048576 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C1-2/c1-arm64x-positive.py --selftest
timeout --kill-after=5s 900s prlimit --as=4294967296 --fsize=1048576 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C1-3/c1-arm64x-positive.py --selftest
timeout --kill-after=5s 900s prlimit --as=4294967296 --fsize=1048576 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C1-4/c1-arm64x-positive.py --selftest
timeout --kill-after=5s 900s prlimit --as=4294967296 --fsize=1048576 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C2-1/c2-capability-calibration-v3.py --selftest
timeout --kill-after=5s 900s prlimit --as=4294967296 --fsize=1048576 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C2-2/c2-capability-calibration-v3.py --selftest
timeout --kill-after=5s 900s prlimit --as=4294967296 --fsize=1048576 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C2-3/c2-capability-calibration-v3.py --selftest
timeout --kill-after=5s 900s prlimit --as=4294967296 --fsize=1048576 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/C2-4/c2-capability-calibration-v3.py --selftest
```

## Per-invocation timestamps and exits

| Fixture / phase | Start UTC | End UTC | Exit |
|---|---|---|---|
| C1-1 / pristine | 2026-10-23T06:47:20.866075+00:00 | 2026-10-23T06:47:20.899754+00:00 | 0 |
| C1-1 / mutated | 2026-10-23T06:47:54.468135+00:00 | 2026-10-23T06:47:54.501062+00:00 | 0 |
| C1-1 / restored | 2026-10-23T06:47:54.549617+00:00 | 2026-10-23T06:47:54.583328+00:00 | 0 |
| C1-2 / pristine | 2026-10-23T06:47:20.868618+00:00 | 2026-10-23T06:47:20.902455+00:00 | 0 |
| C1-2 / mutated | 2026-10-23T06:47:54.469871+00:00 | 2026-10-23T06:47:54.503232+00:00 | 0 |
| C1-2 / restored | 2026-10-23T06:47:54.551445+00:00 | 2026-10-23T06:47:54.587739+00:00 | 0 |
| C1-3 / pristine | 2026-10-23T06:47:20.870577+00:00 | 2026-10-23T06:47:20.904354+00:00 | 0 |
| C1-3 / mutated | 2026-10-23T06:47:54.471701+00:00 | 2026-10-23T06:47:54.505240+00:00 | 0 |
| C1-3 / restored | 2026-10-23T06:47:54.553280+00:00 | 2026-10-23T06:47:54.585764+00:00 | 0 |
| C1-4 / pristine | 2026-10-23T06:47:20.872462+00:00 | 2026-10-23T06:47:20.907765+00:00 | 0 |
| C1-4 / mutated | 2026-10-23T06:47:54.474001+00:00 | 2026-10-23T06:47:54.507974+00:00 | 0 |
| C1-4 / restored | 2026-10-23T06:47:54.555012+00:00 | 2026-10-23T06:47:54.589720+00:00 | 0 |
| C2-1 / pristine | 2026-10-23T06:47:20.874272+00:00 | 2026-10-23T06:47:20.906101+00:00 | 0 |
| C2-1 / mutated | 2026-10-23T06:47:54.475940+00:00 | 2026-10-23T06:47:54.513322+00:00 | 0 |
| C2-1 / restored | 2026-10-23T06:47:54.556747+00:00 | 2026-10-23T06:47:54.590683+00:00 | 0 |
| C2-2 / pristine | 2026-10-23T06:47:20.876213+00:00 | 2026-10-23T06:47:20.909485+00:00 | 0 |
| C2-2 / mutated | 2026-10-23T06:47:54.477951+00:00 | 2026-10-23T06:47:54.511534+00:00 | 1 |
| C2-2 / restored | 2026-10-23T06:47:54.558517+00:00 | 2026-10-23T06:47:54.592699+00:00 | 0 |
| C2-3 / pristine | 2026-10-23T06:47:20.878401+00:00 | 2026-10-23T06:47:20.911117+00:00 | 0 |
| C2-3 / mutated | 2026-10-23T06:47:54.479833+00:00 | 2026-10-23T06:47:54.515033+00:00 | 1 |
| C2-3 / restored | 2026-10-23T06:47:54.562329+00:00 | 2026-10-23T06:47:54.594674+00:00 | 0 |
| C2-4 / pristine | 2026-10-23T06:47:20.880344+00:00 | 2026-10-23T06:47:20.913230+00:00 | 0 |
| C2-4 / mutated | 2026-10-23T06:47:54.481814+00:00 | 2026-10-23T06:47:54.520284+00:00 | 1 |
| C2-4 / restored | 2026-10-23T06:47:54.564175+00:00 | 2026-10-23T06:47:54.596875+00:00 | 0 |

## Full relevant stdout (identical captures grouped)

All 24 stderr captures were empty. The five blocks below are complete, not excerpts.

### Capture group 1

Invocations: `C1-1/pristine`, `C1-1/mutated`, `C1-1/restored`, `C1-2/pristine`, `C1-2/mutated`, `C1-2/restored`, `C1-3/pristine`, `C1-3/mutated`, `C1-3/restored`, `C1-4/pristine`, `C1-4/mutated`, `C1-4/restored`.

```text
ok	exact	segments=1 procedure_count=2
ok	exit 1	exit 1 ok True
ok	wrong sha	subject sha256 differs from the frozen carrier
ok	not ARM64X by oracle	oracle does not classify the carrier as ARM64X
ok	procedure_count = EC export count	report differs from the oracle: procedure_count
ok	oracle and envelope agree, frozen prediction differs	procedure_count 2 differs from the frozen prediction 3
ok	segment differs	report differs from the oracle: segments
ok	architecture x86-64 (EC view)	report differs from the oracle: architecture
ok	wrong operation	operation 'inspect_artifact'
ok	refusal	exit 1 ok False
ok	no envelope	no JSON envelope (exit 0)
ok	row under Core heading	ok
ok	row under round Core-addition heading	ok
ok	row under Frontier	row sits under '## Frontier', not a Core heading
ok	row under Adjacent exclusion	row sits under '## Adjacent — Core exclusion', not a Core heading
ok	prose, not a table row	no PROVINCE table row names ARM64X and the entry
ok	ARM64X without entry	no PROVINCE table row names ARM64X and the entry
ok	absent	PROVINCE absent
selftest cases=18 failures=0
```

### Capture group 2

Invocations: `C2-1/pristine`, `C2-1/mutated`, `C2-1/restored`, `C2-2/pristine`, `C2-2/restored`, `C2-3/pristine`, `C2-3/restored`, `C2-4/pristine`, `C2-4/restored`.

```text
ok	all four rows	match=4 reverse=0
ok	do-nothing: base section (only round 27)	match=1 reverse=0
ok	one row naming all four capabilities and rounds	match=0 reverse=1
ok	four copies of one row with four rounds each	match=0 reverse=4
ok	names and rounds, no evidence path	match=3 reverse=1
ok	irrelevant but resolving evidence path	match=3 reverse=1
ok	anchor path unticked	match=3 reverse=1
ok	junk what-it-can-do cell	match=3 reverse=1
ok	anchor path not in the tree	match=3 reverse=1
ok	rows outside the section	match=0 reverse=0
ok	label only: right round, wrong capability	match=0 reverse=1
ok	right capability, wrong round	match=0 reverse=0
ok	round 170 is not round 17	match=0 reverse=0
ok	over-claim row for round 30	match=4 reverse=1
ok	prose, not a row	match=0 reverse=0
ok	empty	match=0 reverse=0
ok	fake outside anchor row added at REV is ignored	match=3
ok	uncovered MANIFEST item refuses	key list does not cover MANIFEST round 31 item 'new'
selftest cases=18 failures=0
```

### Capture group 3

Invocations: `C2-2/mutated`.

```text
ok	all four rows	match=4 reverse=0
ok	do-nothing: base section (only round 27)	match=1 reverse=0
ok	one row naming all four capabilities and rounds	match=0 reverse=1
ok	four copies of one row with four rounds each	match=0 reverse=4
ok	names and rounds, no evidence path	match=3 reverse=1
FAIL	irrelevant but resolving evidence path	match=4 reverse=0
ok	anchor path unticked	match=3 reverse=1
ok	junk what-it-can-do cell	match=3 reverse=1
ok	anchor path not in the tree	match=3 reverse=1
ok	rows outside the section	match=0 reverse=0
ok	label only: right round, wrong capability	match=0 reverse=1
ok	right capability, wrong round	match=0 reverse=0
ok	round 170 is not round 17	match=0 reverse=0
ok	over-claim row for round 30	match=4 reverse=1
ok	prose, not a row	match=0 reverse=0
ok	empty	match=0 reverse=0
FAIL	fake outside anchor row added at REV is ignored	match=4
ok	uncovered MANIFEST item refuses	key list does not cover MANIFEST round 31 item 'new'
selftest cases=18 failures=2
```

### Capture group 4

Invocations: `C2-3/mutated`.

```text
ok	all four rows	match=4 reverse=0
ok	do-nothing: base section (only round 27)	match=1 reverse=0
ok	one row naming all four capabilities and rounds	match=0 reverse=1
ok	four copies of one row with four rounds each	match=0 reverse=4
ok	names and rounds, no evidence path	match=3 reverse=1
ok	irrelevant but resolving evidence path	match=3 reverse=1
ok	anchor path unticked	match=3 reverse=1
ok	junk what-it-can-do cell	match=3 reverse=1
FAIL	anchor path not in the tree	match=4 reverse=0
ok	rows outside the section	match=0 reverse=0
ok	label only: right round, wrong capability	match=0 reverse=1
ok	right capability, wrong round	match=0 reverse=0
ok	round 170 is not round 17	match=0 reverse=0
ok	over-claim row for round 30	match=4 reverse=1
ok	prose, not a row	match=0 reverse=0
ok	empty	match=0 reverse=0
ok	fake outside anchor row added at REV is ignored	match=3
ok	uncovered MANIFEST item refuses	key list does not cover MANIFEST round 31 item 'new'
selftest cases=18 failures=1
```

### Capture group 5

Invocations: `C2-4/mutated`.

```text
ok	all four rows	match=4 reverse=0
ok	do-nothing: base section (only round 27)	match=1 reverse=0
ok	one row naming all four capabilities and rounds	match=0 reverse=1
ok	four copies of one row with four rounds each	match=0 reverse=4
ok	names and rounds, no evidence path	match=3 reverse=1
ok	irrelevant but resolving evidence path	match=3 reverse=1
ok	anchor path unticked	match=3 reverse=1
ok	junk what-it-can-do cell	match=3 reverse=1
ok	anchor path not in the tree	match=3 reverse=1
ok	rows outside the section	match=0 reverse=0
ok	label only: right round, wrong capability	match=0 reverse=1
ok	right capability, wrong round	match=0 reverse=0
ok	round 170 is not round 17	match=0 reverse=0
FAIL	over-claim row for round 30	match=4 reverse=0
ok	prose, not a row	match=0 reverse=0
ok	empty	match=0 reverse=0
ok	fake outside anchor row added at REV is ignored	match=3
ok	uncovered MANIFEST item refuses	key list does not cover MANIFEST round 31 item 'new'
selftest cases=18 failures=1
```

## Restoration evidence

C1 original/restored hash: `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a`.

C2 original/restored hash: `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f`.

| Fixture | Mutated SHA-256 | Restored SHA-256 | Exact bytes |
|---|---|---|---|
| C1-1 | `755721f56ed3e9388299e6bf0ad22660ab111dfc459fc53b29c17529369cf15a` | `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a` | yes |
| C1-2 | `dec1be17d75080ab2763eb516116e5a91f09b8bcd6b8c761331f72967568f3f1` | `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a` | yes |
| C1-3 | `aeb6f0e66299dcafd027baeff368efa69b9d20d35ebd948816f4578457464936` | `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a` | yes |
| C1-4 | `88d635e9c3d82f1698b543c13c1a37c055518b99aa55ff128cdc89dc92356a41` | `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a` | yes |
| C2-1 | `a2b9f7b622b083db9a94486e8f371172c94fe4cb63ce81c32463914ffe11c4b5` | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` | yes |
| C2-2 | `e125eae63a1962800df957bdca4151a5240024462ee3a190696e6cfee2fcc7e8` | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` | yes |
| C2-3 | `08b1a18e58cf95a587b5bf3710708437cef71ae155e913c1eea04d20e80f39c2` | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` | yes |
| C2-4 | `c3dc7a91fbb00a923c154009424a4e60633313238627e82f84c3b9ec6eb8abb2` | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` | yes |

The recorded SHA-256 before/after each detector invocation was unchanged within that invocation. Each restored detector passed on the original hash. After every invocation the launched process group was absent; no process tree remains from this probe.

Full machine-readable records (all exact argv arrays, full stdout/stderr, UTC start/end, per-phase before/after hashes, mutation clauses and restoration write responses): `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2SelftestHoles/evidence.json`.
Evidence JSON SHA-256: `de8fc53dcc3600da4c32c58d8d48da747c095113d7929cb5eb832e698b49c56b`.

No inference of C1/C2 acceptance-target validity or failure is made from these selftest-coverage findings; frozen instruments were not repaired.

Report: .ufo/waves/round-32/a2audit/A2SelftestHoles.md
