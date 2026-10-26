# R38ExecSelftests — frozen counter selftests (R38-C1 / R38-C2) and their falsification

Leaf executor, round 38 wave 1. Scope: run both frozen counters' selftests with the exact
commands assigned, report the JSON and exit codes verbatim, and then falsify the selftests
themselves — a selftest that prints `failures: []` while testing nothing is exactly the
calibration failure R38-C2 exists to catch, so green output was not accepted as evidence on its
own. No counter, predicate, carrier, oracle, control or harness was changed. No REA invocation.
No install or upgrade (every tool was already on the host). No VCS mutation: only read-only
`git show | rev-parse | log | diff | status | cat-file`.

- Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`; base `77091b49…`; controls `efd5c47a…`.
- Worktree HEAD at start `9c9d496b73cf066b02639dc54647934a0ba4297a`; it moved to `cb4326b2`
  during the window (the L1's harness fix — see §4). The frozen counters are untouched by
  `cb4326b2` (`git rev-parse <rev>:tools/round-38/c{1,2}-counter.py` identical at `e059ca93`,
  `9c9d496b`, `cb4326b2`).
- Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38ExecSelftests`, `TMPDIR="$S"`,
  `HYAKU_SCRATCH="$S"`; **removed at the end** (`ls -d "$S"` → no such file). Everything cited
  below was copied into `.ufo/waves/round-38/w1/artifacts/R38ExecSelftests/` first.
- `considerthese/` absent in this lane (the plan's single allowed line).

## 1. Bytes tested

The counters are pinned by digest at three revisions; the selftest legs below run from a
**scratch mirror of the frozen blobs** so the result cannot depend on worktree drift.

| file | frozen `e059ca93` | `9c9d496b` | `cb4326b2` | sha256 |
|---|---|---|---|---|
| `tools/round-38/c1-counter.py` | `8e33ac68` | `8e33ac68` | `8e33ac68` | `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` |
| `tools/round-38/c2-counter.py` | `04a0bc63` | `04a0bc63` | `04a0bc63` | `7f137b664984595e4d63068a7fa0be2c74a7c57fe5cd5e3a0b794918d2a7b0f7` |

Fixture and helper digests used by the c1 selftest (`git show e059ca93:<path>`): `selftest/dev-after.json`
`d9193aea…ca9`, `dev-before.json` `ff1587fe…a57e`, `dev-oracle.tsv` `69a8abd5…cd67`,
`dev-le-xz.sqsh` `acc64a3d…4b93`, `round-27/xpin-attribute.mjs` `8ea63837…f708`.

## 2. Required results (verbatim)

```
$ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/c1-counter.py \
      --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
{"selftest": "c1-counter", "cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}
EXIT=0

$ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/c2-counter.py --selftest
{"selftest": "c2-counter", "cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}
EXIT=0
```

| counter | bytes | cases | green_ok | red_ok | failures | exit | matches ticket | matches freeze doc |
|---|---|---|---|---|---|---|---|---|
| c1 | worktree at frozen digest `a7a62b09` (03:16–03:21), twice | 15 | 1 | 14 | `[]` | 0 | yes | yes |
| c1 | frozen-mirror of `e059ca93` | 15 | 1 | 14 | `[]` | 0 | yes | yes |
| c2 | worktree / frozen-mirror of `e059ca93` | 14 | 1 | 13 | `[]` | 0 | yes | yes |

Determinism: two consecutive worktree runs and the independent frozen-mirror run produced
byte-identical stdout. **No case failed.**

Case-name audit against `plans/round-38-claims.md` (frozen text, 1:1, no extra and no missing
case):

- c1: green + 14 red = 15, the doc's "oracle **or** carriers changed after freeze" being the two
  cases `oracle changed after freeze` and `carriers changed after freeze`; the other 12 named red
  cases map one-to-one (`do-nothing`, `K2 after receipt missing`, `wrong chunk handler (LE)`,
  `extraction gap present`, `province row outside round-38 section`, `province row without
  handler in first cell`, `province row absent`, `frontier note absent`, `S-id substring S1120`,
  `source row opened earlier`, `used-by lacks entry`, `coverage map lacks stem`).
- c2: green + 13 red = 14, matching the 13 named red cases exactly.

## 3. Falsification of the selftests (mutation probes)

Method: for each probe, a scratch copy of the **frozen** counter was mutated by one exact
single-occurrence string replacement, then `--selftest` re-run (mirrored layout so
`here/selftest` and `here/../round-27/xpin-attribute.mjs` resolve; `HYAKU_SCRATCH` inside my
scratch). The shipped selftest exits 1 when any case mismatches, so **`exit 0` after a mutation
means the selftest did not notice the removed check**. Every probe is recorded with its anchor in
`artifacts/…/mutation-matrix.json`.

### 3.1 c1 — caught mutations, seven checks whose removal goes unnoticed, two masked

Detected (selftest goes red, exit 1):

| probe | outcome |
|---|---|
| final predicate forced `met_target=True` | 14/14 red cases fail |
| `carriers_unchanged` guard dropped | `carriers changed after freeze` fails |
| `coverage_map_row` forced True | `coverage map lacks stem` fails |
| `oracle_frozen` dropped from per-carrier `ok` | `oracle changed after freeze` fails |
| `c[0] in src_ids` → substring membership | `S-id substring S1120` fails (exact-id check is real) |
| `frontier_note` forced True | `frontier note absent` fails |
| `province_core_row` forced True | `province row without handler…` and `province row absent` fail |
| used-by check dropped | `used-by lacks entry` fails |
| opened-date check dropped | `source row opened earlier` fails |

**Not detected — the mutation survives with `failures: []`, exit 0:** dropping
`after_subject_ok`, `after_evidence_id_ok`, `after_oracle_hits == oracle_files`,
`after_operation_ok`, `after_present`, `oracle_files > 0`, `entry_present`. No case varies those
inputs, so the selftest cannot detect their removal.

Masking, proven by an isolating pair:

- `M2` — drop `after_handler_ok` **and** `after_gaps_empty` together → still green (exit 0). In the
  shipped fixture the wrong-handler and gap envelopes are deep copies of the minted envelope, so
  they also break their **stored evidence id**; that binding, not the handler/gap test, is what
  makes those two cases red.
- `P1` — re-mint those two envelopes so their evidence ids are internally consistent (predicate
  unchanged) → still green, i.e. the handler/gap conjuncts really do catch them.
- `P2` — `P1` plus dropping the two conjuncts → exactly `wrong chunk handler (LE)` and
  `extraction gap present` flip green. Attribution settled: predicate correct, shipped fixture
  not isolating.

Positive controls on the predicate (a case the selftest does **not** have): corrupting the stored
`evidence_id` of the otherwise-green envelope, and publishing only 1 of 2 oracle files with the
id re-minted, both make the green case fail (`green: want 0 got 1`, exit 1). So the counter does
catch a wrong stored id and partial publication — the gap is in the selftest's case set, not in
the counter.

### 3.2 c2 — the assertion machinery is never the deciding mechanism

| probe | result |
|---|---|
| `met_target` forced True | exit 1, 13/13 red cases fail |
| **`mismatches = len(unresolved)` (the whole `failed` term deleted)** | **exit 0, `red_ok 13`, `failures []`** |
| assertion comparison disabled (`if False:`) | exit 0, `red_ok 13` |
| `guards_ok` forced True | exit 1; exactly 4 cases flip green |

Deleting `len(failed)` from `mismatches` — i.e. disabling O1–O4 and R1–R3 entirely — leaves the
selftest fully green. Per-case instrumentation (scratch copy printing `unresolved`,
`assertion_mismatches`, `guards_ok`, pointer counts) gives the cause:

- **All 13 red cases have `guards_ok: false`.** The selftest's default fixture `files()` keeps the
  base's unresolved `evidence/doctor/` PROVINCE pointer and never repairs it (only the green case
  overrides `prov_ptr`), so `guards.unrepaired` is non-empty for every red fixture and
  `met_target` is False no matter what the case is named after.
- Forcing `guards_ok=True` flips exactly 4 cases green:
  `unresolved pointer deleted (fewer pointers)`, `substituted by other document`,
  `range beyond file`, `new unresolved pointer`. Those 4 have **empty `assertion_mismatches` and
  empty `unresolved`** — they are red only via the incidental guard, and their named defect is
  demonstrated nowhere.
- The remaining 9 are genuinely carried by their named assertion (instrumented:
  O1 → `junk count`, `count deleted`; R1+R2 → `craft range off by one`; R3 → `box removed`,
  `adjacent range wrong`; O3 → `calibration count wrong`; O4 → `SHONEN rule count wrong`;
  `do-nothing` and `province unresolved pointer kept` → non-empty `unresolved`).

Second cause for 3 of those 4: the fixtures point at paths the counter's own allowlist rejects.
`c2-counter.py:29` `LANE = ^(corpus/|tools/|\.ufo/|plans/|evidence/|scripts/|considerthese/|
SCORECARD\.md|SHONEN\.md|SKILL\.md|PROVINCE\.md|LOG\.md)`, while the fixtures use `x.md`,
`docs/x.md`, `docs/x.md:1-9`, `d/y.md`, `d/missing.md` — never tokenised. Observed pointer counts
confirm it (green uses the `.ufo/…` path: `pointers 5`; every other case: `pointers 4`).
Consequences: `range beyond file` produces `unresolved: []` although the range `1-9` exceeds the
5-line fixture file; `new unresolved pointer` produces `unresolved: []` although `d/missing.md`
does not exist; `substituted by other document` is indistinguishable from its base fixture.

Net: the c2 selftest is a real test of pointer resolution and of the guards, but **it does not
test the assertion comparisons it is named for** to any depth a mutation probe can see, and 4 of
its 13 named red cases are not demonstrated at all.

## 4. Live drift in the frozen c1 counter (disclosed, not repaired)

While I worked, `tools/round-38/c1-counter.py` in the worktree was rewritten by another process.
Observed (read-only; `git status --porcelain -- tools/round-38` → ` M tools/round-38/c1-counter.py`):

| time (-03:00) | sha256 | equals frozen? | selftest |
|---|---|---|---|
| 03:16–03:21 | `a7a62b09…16db8` | yes | 15 / 1 / 14 / `[]` / exit 0 |
| 03:22:04 | `f27f982b…e83fa` | no | still green (drift invisible at this stage) |
| 03:23:27 | `12f09870…f5a39` | no | **no verdict**: `AttributeError: 'NoneType' object has no attribute 'get'` at `c1-counter.py:186` (`gaps(envs.get('before'))`) via `:135`, exit 1 |

What the edit does (diffs saved at `artifacts/…/lane-drift-c1-counter.diff` and
`…-0323.diff`):

- It rewrites the module docstring's frozen P38-C1 sentence from "stock unblob 26.6.4; **no
  external extractor dependency**" to "**sasquatch-v4be available**, as unblob 26.6.4's
  `SquashFSExtractor` requires", and adds a requirement that a paired before-receipt "publishes
  none of them and names sasquatch-v4be as a missing extractor dependency". That contradicts
  `plans/round-38-claims.md`, which says the before-arm "does not reproduce on these carriers and
  is reported as a corrected premise", and it is a frozen predicate sentence.
- It adds a `before` leg to `measure()` and, at the last snapshot, requires
  `before_present`, `before_subject_ok`, `before_operation_ok`, `before_missing_extractor_gap`,
  `before_oracle_hits == 0` in the per-carrier `ok` — a semantic change to the frozen target, and
  at the intermediate snapshot `before_missing_extractor_gap` was computed but never required.

I did not author, stage or revert any of it (no `git add/commit/checkout/reset/stash/restore`).
Consequences for the round: any after-receipt or counter JSON produced from this worktree while it
sits at `f27f982b`/`12f09870` is not at frozen bytes and the counter currently returns no verdict
at all; the frozen-mirror leg in §2 is the reproducible one. Also note HEAD advanced
`9c9d496b` → `cb4326b2` in the same window (`tools/round-38/c1-run.sh` changed after the freeze:
`rm -rf "$OUT"` added because REA refuses an existing extraction root; counters untouched).

## 5. Secondary observations (no repair)

- `--selftest` without `--pkg65` crashes: `TypeError: expected str, bytes or os.PathLike object,
  not NoneType` (c1-counter.py:291 `mint` → :283 `subprocess.run`), exit 1 and no usage line,
  whereas the measure path returns exit 2 for missing arguments.
- The c1 selftest leaves `$HYAKU_SCRATCH/kaidoku-r38/mint.wrapped.json` behind (it writes that
  file at the scratch **root**, not in a per-case temp dir), so every invocation rewrites one
  shared path. 6 concurrent `--selftest` runs sharing one `HYAKU_SCRATCH`, 4 rounds: **24/24
  exit 0, `failures: []`** — no collision observed, but the write→read window on that shared file
  remains. The c2 selftest leaves no residue (per-case dirs are removed).

## 6. Limits — what this does not claim

- These are properties of the frozen selftests only. They say nothing about whether either
  counter meets its target on the real carriers / repo; that is the counting command's job and
  the C1 claim data is not mine.
- Mutation results describe the frozen *logic*; they were produced on byte-identical scratch
  copies, not on the (drifting) worktree.
- No claim data, no target verdict, no control re-run, no repair of any found defect. The selftest
  defects in §3.1/§3.2 are disclosed, not fixed; the lane drift in §4 is reported, not reverted.

## 7. Files

- Report: `.ufo/waves/round-38/w1/R38ExecSelftests.md` (this file).
- `artifacts/R38ExecSelftests/selftest-runs.json` — every run: bytes, command, stdout, exit.
- `artifacts/R38ExecSelftests/mutation-matrix.json` — all 24 c1 probes and 4 c2 probes with anchors,
  outcomes and the c2 per-case attribution table.
- `artifacts/R38ExecSelftests/lane-drift-observation.json` — drift timeline, digests, selftest
  outcome at each snapshot.
- `artifacts/R38ExecSelftests/lane-drift-c1-counter.diff`, `…-0323.diff` — the two captured
  worktree diffs of the frozen counter.
