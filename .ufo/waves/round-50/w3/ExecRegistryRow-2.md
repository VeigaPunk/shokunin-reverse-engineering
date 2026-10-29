# ExecRegistryRow-2 — independent re-verification of the R50-C3 registry row and the B9 coupling

**VERDICT: the row at `tools/round-50-c3/sqfs-triage-v5.py` is correct and the landing is green —
independently re-measured. One correction to the peer seat's finding F4: the "no further
`.py`/`.sh` under `tools/round-50/`" constraint is real but UNDER-stated — the freeze drift is
extension-agnostic, so *any* file added under `tools/round-50/` (a `.md` control table, a
`.json` manifest, a `.txt`) breaks both frozen counters too, and the C3 control fixtures must
land outside that tree as well.**

This seat was dispatched as a duplicate of `ExecRegistryRow` (peer roster id `ExecRegistryRow`,
mine `ExecRegistryRow-2`). The peer had already written the canonical report
`.ufo/waves/round-50/w3/ExecRegistryRow.md` and the canonical row bytes
`.ufo/waves/round-50/w3/ExecRegistryRow/row-final.txt` before I finished; its cleanup also
removed my scratch tree mid-run. I therefore did **not** overwrite the peer's canonical files.
This report is my own independent measurement, written to a distinct path; the L1 should read
both. Where I differ from the peer, the difference is stated explicitly.

## Findings

| # | finding | evidence | severity |
|---|---|---|---|
| **F1** | **The peer's row passes every frozen predicate, re-checked independently.** Re-applying each `b9()` predicate by hand to `row-final.txt` (sha256 `720976176bdbe082fd4000cf54db8ba3ce11fc3f50ef5371a3179f8d3fb0e62d`, 7 cells, 8 pipes): 12/12 checks pass — seven cells; kind cell opens `gate`; the entry command naming the exact path appears in cells 1 and 3; the verdict cell binds `0`/`1`/`2` to meanings under **both** the round-48 original (`{'0':'success','1':'not-met','2':'unevaluable'}`) and its `c2-record.py` port (no error); the self-test cell is the `--selftest` form; the pinned-value cell names a path; `registry_region()` sees exactly one row for the path and no duplicate cell-0 in the 55-row region; the markers stay singular. | `receipt-validate-peer-row.json` | row confirmed |
| **F2** | **The full simulated C3 landing is green end-to-end.** Landing set = peer row + instrument at `tools/round-50-c3/sqfs-triage-v5.py`, committed together in a throwaway clone, then the **frozen** `c2-record.py` run at that REV with freeze `435d41fd…`: **exit 0, `mismatches 0`, 11/11 atoms green, B9 `ok:true`**, and the C1 counter's own `frozen_drift()` → `[]`. The same landing with the instrument at the **old** in-tree path `tools/round-50/sqfs-triage-v5.py` gives C2 **exit 2** `frozen_path_changed` and C1 `frozen_drift = ['tools/round-50/sqfs-triage-v5.py']`. | `receipt-final-landing.json` | path choice confirmed |
| **F3** | **CORRECTION to the peer F4: the freeze drift is extension-agnostic, not `.py`/`.sh`-only.** `c1-counter.py`'s `frozen_drift()` marks an `A` status under `FROZEN_PREFIXES = ('tools/round-50/',)` as drift for **any** path, and `c2-record.py`'s `FROZEN = ('tools/round-50', …)` walks the same pathspec. Measured, each on its own clone commit against freeze `435d41fd…`: a `.md` control table at `tools/round-50/control-fixtures/c3/ctl-do-nothing.skill.md` → C1 drift `['…ctl-do-nothing.skill.md']`, C2 exit 2 `frozen_path_changed`; a `.json` manifest at `tools/round-50/control-fixtures/c3/manifest.json` → same; a `.txt` at `tools/round-50/anything.txt` → same. The moved path `tools/round-50-c3/…` → drift `[]`, C2 exit 0. **Consequence for the L1: the C3 control fixtures (the sibling seat's `ctl-do-nothing.skill.md` / `ctl-junk.skill.md` / `ctl-guard-deleted.skill.md` / `ctl-action-swapped.skill.md` tables and `envelopes-manifest.json`) must be committed OUTSIDE `tools/round-50/` — e.g. `tools/round-50-c3/control-fixtures/` — or they will make both frozen counters exit 2 at the C1/C2 scoring REV.** The peer seat's F4 says only "no further `.py`/`.sh` may land under `tools/round-50/`"; that is true but leaves the `.md`/`.json` control fixtures unflagged. | `receipt-drift-extension.json` | **correction — L1 action required** |
| **F4** | **B9 cannot police the new row, so the row's own quality is a hand-checked duty, not a machine-checked one.** B9's census is `tools/round-49/**` (at BASE) + `tools/round-50/**` (at REV) filtered to `.py`/`.sh`; `tools/round-50-c3/sqfs-triage-v5.py` is **not** in it (measured: `b9_census_contains_path = False`). Consequence, measured: a **deliberately broken** row for that path (kind cell `helper`, verdict `0=zero; 1=one; 2=two`, empty self-test and pinned cells) still yields `b9_problems = []`. So if the L1 lands a malformed row for the out-of-tree path, **B9 stays green and only the L1's own review catches it**. The row must be reviewed against the round-48 meaning rule by hand — which is why F1 (the hand re-check of all 12 predicates) is load-bearing rather than redundant. The plan states this ("the outside path needs no row for B9, and the lane registry still gets one as a gate-registration duty"), so this is a disclosure, not a defect in the plan. | `receipt-validate-peer-row.json` (`b9_census_contains_path`, `b9_problems_with_deliberately_broken_row`) | disclosure |
| **F5** | **The R48 `registry_extra` clause is already red at HEAD and the new row does not change that verdict.** Re-derived from `tools/round-48/census2.json` (42 paths, rounds 41–48) against the region at base `f890bbe…`: 54 rows, 12 outside the census, 0 duplicates, 0 missing, 0 meaning failures. With the peer row added: 55 rows, 13 outside (the new path is one of them), still 0 duplicates / 0 missing / 0 meaning failures. The R48 failure is the pre-existing 12-row extra set (the six `tools/round-49/**` + six `tools/round-50/**` rows the attempt-1 landing added), not the C3 row. R46 `registry.py` and R45 `c2-counter.py` scope the census to rounds 41–46 / 44–45 respectively and do not see the new path. | `receipt-registry-couplings.json` | pre-existing, no action |
| **F6** | **The peer's cell 4 pinned-value paths are git-tracked and stable.** `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/manifest.json` is tracked (sha256 `1acd4ca21435477b5a7141f0edfef081212526ffb0280810dca4c0e72a20bbb9`, 135 entries) and the 126 `envelopes/*/envelope.json` files are tracked. The row's pinned cell names exactly these two, so it satisfies the B9 pinned-value predicate with paths that exist at the landing REV. | `receipt-registry-couplings.json`, `git ls-files` | confirmed |
| **F7** | **The row's entry command matches the sibling instrument's actual CLI.** The sibling's draft (`.ufo/waves/round-50/w3/ExecTriageV5/tools/round-50-c3/sqfs-triage-v5.py`, already moved to the out-of-tree path) declares `--root --rev --freeze --envelopes --json-out --skill --work --selftest`, and its docstring carries the predicate sentence with the path `tools/round-50-c3/sqfs-triage-v5.py`. The row's cell 1 and cell 3 use the same spelling, so the row documents the command that will actually be run. The sibling's selftest receipt reports **13 cases, pass 13, fail 0, exit 0** (2026-10-29T20:54:28Z) — which lets the L1 replace the row's cell-3 placeholder ("the case count and the exit code are recorded in the freeze receipt") with the measured values. | `ExecTriageV5/receipts/selftest.txt`, `grep add_argument` | L1 edit available |

| **F8** | **The LANDED row is verified green — 13/13 checks on the landed bytes.** While I worked, the L1 landed a row into `SKILL.md` (uncommitted; `git diff` shows it at line 1774, region now 55 rows). I re-read the **landed** bytes — not the peer's draft — and re-applied every predicate: seven cells; cell 0 exactly `` `tools/round-50-c3/sqfs-triage-v5.py` ``; kind cell opens `gate`; the entry command names the path (cells 1 and 3); the verdict cell binds `0`/`1`/`2` to meanings under **both** the round-48 original and its `c2-record.py` port; the self-test cell is the `--selftest` form; the pinned-value cell names a path and **both** named paths are git-tracked at HEAD (`manifest.json` as a file, `envelopes/` as a directory of 126 tracked `envelope.json` files); exactly one row for the path; no duplicate cell-0; markers singular; and the entry command matches the **landed instrument's real CLI** (its argparse declares `--root --rev --freeze --envelopes --json-out --selftest --skill --work`). Landed row sha256 `c7940cfc30fe16d11e9293fda4aa54bbca72a83d17b2f1bbf159473d83da4bb5`; landed instrument sha256 `a2ebb5a431d9f2b37f7b2e7ed0a759e125d6ec3ec39358a946adeb3622cfb052` (93,991 bytes). | `receipt-landed-row.json` | **landed row confirmed** |

## Recommended row (the peer's bytes, unchanged) — with one cell-3 refinement available

The peer row is correct as written; I did not change it. If the L1 wants the attempt-1 house form
(a measured count and date in cell 3, as `tools/round-50/c2-record.py` and
`tools/round-50/c1-counter.py` carry), the sibling's measured selftest gives the values:

```
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest — 13 cases, pass 13, fail 0, exit 0 on 2026-10-29
```

That is a **suggestion for the L1 to apply after re-running the selftest at the C3 freeze**, not
a change I made — I did not run the instrument's selftest myself and will not state a count I
did not measure. The peer row's current cell 3 is honest as it stands ("the committed mutation
battery; the case count and the exit code are recorded in the freeze receipt").

## Provenance note — the 49-byte stub in the lane tree (a correction to the peer seat's F8/F10)

The peer seat's F8 records that `tools/round-50-c3/sqfs-triage-v5.py` in the lane tree held a
49-byte do-nothing stub (sha256 `af1b22ba…`) rather than the real instrument, and its F10
attributes that stub's origin to "a second instance of MY seat" on the strength of a grep hit
on the literal `'#!/usr/bin/env python3\n# simulated C3 instrument\n'` inside
`w3-ExecRegistryRow-2/final-landing.py:64` — **my** scratch file.

**That attribution is wrong, and the evidence is decisive on four independent grounds:**

1. **Static.** The only writes in my four scripts are `full = os.path.join(clone, path)` followed
   by `open(full, 'w')`, where `clone = os.path.join(root, 'clone')` and `root` is a
   `tempfile.mkdtemp(prefix=…, dir=SCRATCH)` under `/fast/scratch`. No `os.chdir`, no relative
   `open()`, no `makedirs` outside the clone. A relative write to `tools/round-50-c3/…` is
   impossible from them.
2. **Step isolation (decisive).** I replayed `final-landing.py`'s eight subprocess steps one at a
   time — `git clone --shared`, `checkout --detach`, `reset --hard`, `git clean -qfd`, the
   instrument write, `git add -A`, `git commit`, and the frozen `c2-record.py` run — recording
   the lane file's (sha256, size, mtime) after each. **Every step left it byte- and
   mtime-identical.** The stub was written into the *clone* (`clone file sha256 af1b22ba…`),
   never the lane.
3. **Chronological.** The stub's mtime is `17:53:28.965200819`; `final-landing.py` — the only
   script of mine containing that literal — has mtime `17:54:35.946025426`, **67 seconds
   later**. A script cannot write a file 67 s before it exists.
4. **Empirical.** Re-running `drift-extension.py` and `final-landing.py` with the lane and fleet
   trees watched: the fleet path stays absent, and the lane path's change observed in that run
   was the **L1's own refresh** (see below), not a write by my scripts.

**What actually happens at that lane path:** the L1 keeps `tools/round-50-c3/sqfs-triage-v5.py`
as a live copy of the sibling `ExecTriageV5` draft. Measured: the sibling draft is 93,991 bytes,
sha256 `a2ebb5a431d9f2b37f7b2e7ed0a759e125d6ec3ec39358a946adeb3622cfb052`, mtime 18:02:41; the lane
copy is byte-identical (`cmp -s` → identical), mtime 18:02:51 — ten seconds later. The lane file
therefore changes as the sibling iterates on its draft, which is why the peer's F8 saw a 49-byte
stub at one moment and the "real" 90,837-byte instrument at the next (the sibling's draft grew
between the two observations, 90,837 → 93,991 bytes). The stub at 17:53 was the L1's misroot
sweep writing the fleet-repo stray back under the lane root; the sweep's own preserved copy sits
in `.ufo/waves/round-50/w3/misroot/fleet-stray-sqfs-triage-v5.py` at the same mtime.

**State at the time of writing: the lane file is correct and live.** It is byte-identical to the
sibling's draft (93,991 bytes, sha256 `a2ebb5a4…`). It remains untracked (`?? tools/round-50-c3/`),
which is the L1's call, not mine.

**One residual hazard the L1 should close, because the stub was not the only thing the sweep
copied:** the stub **fake-greens**. A 2-line file with no `main()` exits 0 and writes no
receipt, so a `--selftest` probe on it returns rc 0 with empty stdout. Any verification the L1
runs against `tools/round-50-c3/sqfs-triage-v5.py` must assert the **stdout content**
("selftest: 13 cases, pass 13, fail 0") and the **receipt file**, not just the exit code — and
must compare the **sha256** against the sibling draft it intends to land, because the lane path
is a live copy that changes under the sibling's edits. The peer's F8 makes the same point; I
re-measure it on the real instrument's own receipt (`ExecTriageV5/receipts/selftest.txt`:
13 cases, pass 13, fail 0, exit 0, 2026-10-29T20:54:28Z).

## Boundaries kept

- **Read-only on the lane tree.** The only files I wrote are under
  `.ufo/waves/round-50/w3/ExecRegistryRow-2/` and this report. I did **not** overwrite the peer
  seat's canonical `ExecRegistryRow.md` or `ExecRegistryRow/` artifacts.
- **No REA run.** No `npx rea-agents`, no `rea`, no `--data-run`. `c1-counter.py` was never run
  end-to-end; its frozen `frozen_drift()` derivation was called directly, which is the arm that
  decides the path question.
- **No mutating git in the lane or the fleet repo.** Every commit was in a throwaway clone under
  my scratch; `git -C "$clone" rev-parse --show-toplevel` was asserted equal to the clone path
  before the first commit, and `user.name`/`user.email` were set in that clone only. Lane-side
  git calls were read-only (`cat-file`, `ls-tree`, `rev-parse`, `log`, `show`, `merge-base`).
- **No downloads.** No vendor firmware, no network.
- **Scratch**: `/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2` (a distinct name after the
  peer's cleanup removed the first one mid-run). Removed after the receipts were copied here.
  The disk guard was consulted before the clone work (`disk-guard.sh status`, exit 0).
- **No tool was installed or upgraded** (nothing needed installing; the RULES.md tooling
  directive was read and no pacman/`uv`/`cargo` transaction was made).

## Not run (stated, not claimed)

- `tools/round-50/c1-counter.py` end-to-end (needs REA + the chain-pinned vendor carriers).
- The v5 instrument's own selftest by me (the sibling's receipt is cited, not re-run).
- `tools/round-42/sqfs-triage-v4.py --selftest`.
- `tools/round-46/registry.py` and `tools/round-45/c2-counter.py` end-to-end (their relevant
  clauses were re-derived by hand instead).
- The C1 data run and the C1 controls (the L1's job, in the quiet window).

## Artifacts (this seat)

| file | what it is |
|---|---|
| `ExecRegistryRow-2/receipt-validate-peer-row.json` | the 12 hand-applied `b9()` predicates on the peer row; the census-membership measurement; the deliberately-broken-row control |
| `ExecRegistryRow-2/receipt-drift-extension.json` | the extension-agnostic frozen-drift matrix (5 cases × C1 drift and C2 exit) |
| `ExecRegistryRow-2/receipt-final-landing.json` | the full simulated C3 landing at both paths, run through the frozen `c2-record.py` |
| `ExecRegistryRow-2/receipt-registry-couplings.json` | the R48 / R46 / R45 registry-coupling re-derivation |
| `ExecRegistryRow-2/validate-peer-row.py` | the script behind the first receipt |
| `ExecRegistryRow-2/drift-extension.py` | the script behind the second receipt |
| `ExecRegistryRow-2/final-landing.py` | the script behind the third receipt |
| `ExecRegistryRow-2/registry-couplings.py` | the script behind the fourth receipt |
| `ExecRegistryRow-2/receipt-attribution.txt` | the stray-stub provenance test (static + chronological + empirical) |
| `ExecRegistryRow-2/receipt-step-isolation.txt` | the step-by-step replay proving no step of my fixture scripts writes to the lane |
| `ExecRegistryRow-2/attribution.py` | the script behind the fifth receipt |
| `ExecRegistryRow-2/step-isolation.py` | the script behind the sixth receipt |
| `ExecRegistryRow-2/RECEIPTS.md` | the receipt index with every command, exit code and sha256 |
| `ExecRegistryRow-2/receipt-landed-row.json` | the 13/13 verification of the **landed** `SKILL.md` row |
| `ExecRegistryRow-2/verify-landed-row.py` | the script behind that receipt |
