# R39W2C1Rescore — independent re-score of R39-C1 with the frozen counter

**Verdict: CONFIRMED — R39-C1 re-scores `met_target: true`, `carriers_matched: 6/6`, exit 0 at the
author's measured revision `6fdaf4f1` and at the later `52b0eb29` (and at the lane tip
`e40a25df`); the freeze arm exits 1 at 0/6 for the right reasons (receipts absent, six prose
bindings false, no unevaluable path); the counter is byte-identical at the freeze, both measured
revisions and the lane worktree; no commit in `8fcda41c..52b0eb29` touches any frozen C1 path; the
33-case selftest is green with zero failures.**

Seat: R39W2C1Rescore (leaf). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`; controls `72359309a052284029f8e0331ef211a67fe4b13b`;
base `a2f64e1da78afcf8cc39287106604dbcc270844c`. VCS was read only (`git show/log/clone`); nothing
in the lane was written except this report and `w2/artifacts/R39W2C1Rescore/`.

## 1. What was run (exact commands, exit codes)

Shared clone (read-only, no checkout):

```
S=/fast/scratch/hyaku/kaidoku-r39/R39W2C1Rescore; mkdir -p "$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"
git -C "$S/clone" rev-parse --show-toplevel      # $S/clone   (verified)
```

Each measured revision (counter taken from the clone's worktree, whose blob hash equals the freeze
blob — §3):

```
TMPDIR="$S" HYAKU_SCRATCH="$S" python3 -I -B "$S/clone/tools/round-39/c1-counter.py" \
  --root "$S/clone" --rev <REV> --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --json-out "$A/rescore-<REV>.json"
```

| run | REV | exit | `carriers_matched` | `met_target` | stderr | receipt |
|---|---|---|---|---|---|---|
| primary | `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` | **0** | **6/6** | true | empty | `artifacts/R39W2C1Rescore/rescore-6fdaf4f1.json` |
| later commit | `52b0eb2907c704ed5f184c47b14c723208e5cbbc` | **0** | **6/6** | true | empty | `rescore-52b0eb29.json` |
| **freeze arm** | `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` | **1** | **0/6** | false | empty | `rescore-8fcda41c.json` |
| extra (lane tip, this seat's own addition) | `e40a25df3987d881513de581112d2dad30605673` | **0** | **6/6** | true | empty | `rescore-e40a25df.json` |
| determinism rerun of primary, `PYTHONHASHSEED=1` | `6fdaf4f1` | 0 | 6/6 | true | empty | `rescore-6fdaf4f1-rerun-seed1.json` |
| selftest | — | **0** | — | — | empty | `selftest.txt` |

Selftest: `python3 -I -B .../c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
→ `{"selftest": "c1-counter", "cases": 33, "green_ok": 1, "red_ok": 32, "failures": []}` (exit 0).

Determinism: the `PYTHONHASHSEED=1` rerun is equal to the primary run on every field except
`argv` (`artifact://` helper comparison: `RERUN_IDENTICAL_EXCEPT_ARGV True`).

## 2. Per-carrier result at `6fdaf4f1` (frozen counter output)

| id | pin | oracle files/hits | in-tree / escaping links | gaps | handler | chunks | prov dir (after `/kaidoku-r39/`) | evid | superblock comp id | matched |
|---|---|---|---|---|---|---|---|---|---|---|
| K1 | ok | 5/5 | 0 / 1 | 0 == 0 | `squashfs_v4_be` | no fail | `l1/c1runs/K1-scratch/extract` | ok | 1 | **true** |
| K2 | ok | 3/3 | 1 / 0 | 1 == 1 | `squashfs_v4_be` | no fail | `l1/c1runs/K2-scratch/extract` | ok | 1 | **true** |
| K3 | ok | 4/4 | 0 / 0 | 0 == 0 | `squashfs_v4_be` | no fail | `l1/c1runs/K3-scratch/extract` | ok | 1 | **true** |
| K4 | ok | 4/4 | 0 / 0 | 0 == 0 | `squashfs_v4_be` | no fail | `l1/c1runs/K4-scratch/extract` | ok | 1 | **true** |
| K5 | ok | 10/10 | 2 / 1 | 2 == 2 | `squashfs_v4_be` | no fail | `l1/c1runs/K5-scratch/extract` | ok | 1 | **true** |
| K6 | ok | 8/8 | 1 / 2 | 1 == 1 | `squashfs_v4_be` | no fail | `l1/c1runs/K6-scratch/extract` | ok | 4 (xz) | **true** |

Bindings at `6fdaf4f1`: all of `province_core_section`, `province_core_row`, `frontier_note`,
`entry_present`, `sourced`, `coverage_map_row`, `carriers_spec_ok`, `symlink_coverage`
(in-tree 4, escaping 4, max in-tree per carrier 2), `xz_leg` are true; `frozen_path_changed: []`;
`carriers_unchanged: true`. Full table: `evidence-per-carrier-table.txt`.

The `52b0eb29` and `e40a25df` outputs are identical to the `6fdaf4f1` output on every field except
`revision` and `argv` (checked field-by-field in-process: `IDENTICAL_EXCEPT_ARGV_REV True`).

## 3. Counter and frozen-input integrity

* `sha256(tools/round-39/c1-counter.py)` is **`efb4b52658b6ccfaebe68516ce2a80794b38ff041a81f464c073974853577a91`
  at every one of** `8fcda41c` (freeze), `6fdaf4f1`, `52b0eb29`, `e40a25df`, the lane worktree and
  the clone worktree (`evidence-counter-hash.txt`). So the tool that produced the author's
  `c1-at-6fdaf4f1.json` and the tool I ran are the same bytes as the frozen one.
* Freeze-drift, per path (`git log --oneline 8fcda41c..52b0eb29 -- <path>`, count of commits):
  **0** for all 22 frozen paths — `plans/round-39-claims.md`, `tools/round-39/c1-counter.py`,
  `tools/round-39/c1-run.sh`, `.ufo/waves/round-39/c1/carriers.json`, and every `carrier.*`,
  `oracle.tsv`, `symlinks.tsv` that `carriers.json` lists (`evidence-drift-paths.txt`). Frontend
  granularity was checked independently of the counter's own `frozen_drift` scanner.
* Byte identity across revs for the three control files — `carriers.json` `df9eb8a6…`,
  `plans/round-39-claims.md` `b806f0a7…`, `tools/round-39/c1-run.sh` `422dbddc…` — equal at
  `8fcda41c`, `52b0eb29` **and** `e40a25df`.
* The counter's own selftest fixtures (`tools/round-39/selftest/{dev-after.json,dev-oracle.tsv,
  dev-symlinks.tsv,r38-k2-after.json}`) are not in the frozen-path list, so I checked them
  separately: no commit in `8fcda41c..52b0eb29` touches them and their bytes are identical at
  freeze and at `52b0eb29`. The selftest therefore grades the frozen semantics, not a retuned
  fixture.
* The four commits in the range (`72359309` controls/w1, `3c07eed7` C2 data, `6fdaf4f1` C1
  receipts + prose, `52b0eb29` lesson/registry/r38 selftests) touch none of the frozen C1 paths.
* `--pkg65` root is rea-agents **6.5.0** (`package.json` name/version read); `unblob --version`
  = **26.6.4**; `python3` 3.14.8; `node` v24.21.0. No tool was installed, upgraded or replaced
  during this seat (nothing to report under the tooling authorization).

## 4. Freeze arm is a genuine miss, not an unevaluable stop

At `8fcda41c` the counter exits 1 with a complete result object (no `unevaluable` key):
`carriers_matched 0`, `receipt_present false` / `receipt_fresh false` / `evidence_id_ok false` for
K1..K6, `carrier_present/pin_ok/oracle_ok/symlinks_ok` true for all six (the frozen inputs were
already present), and exactly six false bindings: `province_core_section`, `province_core_row`,
`frontier_note`, `entry_present`, `sourced`, `coverage_map_row`. That is the "command that shows it
unmoved" named in `plans/round-39-claims.md` R39-C1, reproduced.

## 5. Comparison with `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json`

Field-by-field walk of both JSON trees (`evidence-field-diff-vs-l1.txt`): **1 differing path only —
`/argv`** (`--root` is the clone instead of the lane, `--json-out` is my artifact path, and the tool
is invoked as an absolute path). Every clause, binding, per-carrier record, `carrier_ids`,
`carriers_matched`, `carriers_unchanged`, `frozen_path_changed`, `met_target`, `predicate`, `target`
and `revision` is equal. The author's score file is therefore reproducible byte-for-byte in
substance.

## 6. Independent cross-checks that do not use the counter's own verdict (depth)

* **Evidence-id recompute is real, not an echo.** I took the xpin tool from the freeze
  (`git show 8fcda41c:tools/round-27/xpin-attribute.mjs`, `sha256 8ea63837…`, copy kept at
  `artifacts/R39W2C1Rescore/xpin-attribute-at-freeze.mjs`) and ran it directly on the six committed
  receipts wrapped as `{"data": <envelope>}`: all six report `stored == recomputed == recomputed67`
  and classification `both` (`evidence-xpin-direct-recompute.txt`). Control: mutating one published
  file's `sha256` in K3 without touching `evidence_id` yields stored `ev_af856f08…` vs recomputed
  `ev_f817a8ac…`, class `none` (`evidence-xpin-mutant-nonEcho.txt`) — the check is content-derived.
* **`after.json` ↔ `run.json` consistency** at `52b0eb29`, for all six: committed `after.json` bytes
  hash and length equal the `run.json` receipt record, `evidence_id` matches, the recorded carrier
  pin equals the sha256 of the carrier blob at that rev, `exit 0`, and the recorded gap/file counts
  match the envelope (`evidence-runjson-consistency.txt`). The `run.json` files are *not* covered by
  predicate P39-C1 (it names the after-receipt only), so this was checked outside the counter.
* **Superblock bytes read directly from the git blobs** (not via the counter): K1/K5 magic `sqsh`,
  major 4, minor 0, compression id 1 (gzip); K6 magic `sqsh`, major 4, minor 0, compression id 4
  (upstream xz), block size 4096. That is the `xz_leg` binding and the "standard big-endian" surface
  confirmed at the byte level.
* **Symlink tables vs the claim's stated pre-data rule**: K1 1 escaping, K2 1 in-tree, K3/K4 none
  (empty table, sha256 `e3b0c442…`), K5 2 in-tree + 1 escaping, K6 1 in-tree + 2 escaping — exactly
  the counts written in `plans/round-39-claims.md` and in `carriers.json`; totals in-tree 4 /
  escaping 4 with one carrier at 2 in-tree, and the counter's `symlink_kind_recompute_mismatch` is
  empty for all six (the frozen kind agrees with an independent re-derivation of unblob's
  `is_safe_path` rule).
* **Gap paths are the real link paths**, not suffix coincidences: `firmware.bin_extract/var/lib/run-link`
  (K2), `…/usr/share/demo/link-blob`, `…/usr/share/demo/link-notes` (K5), `…/a/b/link-in` (K6), each
  also present in the envelope's `unpublished_entries` with `kind: symlink`; K1/K3/K4 carry no gap
  and no in-tree link.
* **Prose bindings spot-read at `52b0eb29`** (not just matched by regex): `PROVINCE.md` line 384 is
  the `Round-39 frontier note, 2026-10-26: …` line naming the entry stem; the
  `## Round-39 additions to Core` table has a first cell naming `squashfs_v4_be` and an evidence cell
  naming `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`; the entry's `source:` line names
  `S122`; `corpus/SOURCES.md:128` is `| S122 | … | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md |`;
  `corpus/README.md:93` is the Core coverage-map row naming the stem.

## 7. Residual observations (non-blocking; none changes the verdict)

1. `same_rel()` accepts a suffix match, so a gap/file path with an arbitrary prefix would satisfy
   oracle/gap/escape matching. This is what the frozen predicate sentence says ("same relative-path
   suffix") and REA prefixes `firmware.bin_extract/`; the six committed envelopes carry exactly that
   prefix and nothing else, so the looseness is not exercised. Reported as residual, not a defect.
2. `provenance_ok()` is an absolute-path + substring `/kaidoku-r39/` + no-`..` test, matching the
   predicate literally. A fabricated envelope could name any path under a `/kaidoku-r39/` segment;
   this is the fabrication limit already disclosed in `plans/round-39-claims.md` ("Disclosed limit",
   QUALITY 78) and is not this counter's job.
3. The extraction directories the receipts name
   (`/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K{1..6}-scratch/extract`) **no longer exist**: that
   directory now holds empty `K1..K6-out` dirs and zero-byte `K*.log` files (mtime 14:16–14:17
   local = 17:16–17:17Z, consistent with `run.json` `start_utc`). Provenance is therefore carried by
   the receipt bytes and `run.json` only, not by surviving on-disk trees. The predicate does not
   require the directory to survive, and wave-2 re-run seats cover re-execution; recorded so nobody
   mistakes the empty dirs for evidence of a run.
4. The counter invokes xpin with `--pkg65 P --pkg67 P` (the same 6.5.0 root for both), so the
   "6.7.0 rule" column is evaluated with 6.5.0 code. This is intentional — the stored ids were
   minted by rea-agents 6.5.0 and the predicate asks for the 6.5.0 rule — and the recompute agrees
   with the stored id for all six receipts.
5. Not done here by design (other seats): re-executing REA on the six carriers to reproduce the
   envelopes from scratch. This seat's scope was the re-score; [INFERENCE] that a fresh run
   reproduces the same semantic payload rests on the sibling repro seats plus points 2–6 above.

## 8. Boundary compliance

* Files written: this report and `w2/artifacts/R39W2C1Rescore/` only (23 files: 5 counter JSONs,
  8 stdout/stderr files, 7 evidence text files, the frozen xpin copy, `selftest.txt`). No write
  under `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`,
  `LOG.md`, the fleet repo or any sibling lane.
* VCS untouched: only `show/log/ls-tree/cat-file/merge-base/rev-parse/clone` were used.
* Scratch `$S=/fast/scratch/hyaku/kaidoku-r39/R39W2C1Rescore` (clone, xpin workspace, counter
  scratch under `$S/kaidoku-r39/counter`) removed before finishing; every cited output was first
  copied into the artifacts dir.
