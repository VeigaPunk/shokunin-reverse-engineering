# R39-C1 provenance limit — R39W2C1Fabricate

**FALSIFIED** — the frozen R39-C1 counter's run-provenance binding: six after-receipts built
without any REA run, committed over the real ones at a commit whose parent is
`6fdaf4f162aff156fcef0e52998a5469c64fd6f0`, score **6/6, exit 0, `met_target: true`**
(`c1-fabricated.json`). The receipts that actually landed, however, **do not look fabricated**:
every field that could have exposed a cheap forgery is consistent with a real REA run on this
host (§3), including a PID-derived `blob_id` chain that matches the host's measured PID-allocation
rate and the committed run times.

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; freeze `8fcda41c…`; author rev
`6fdaf4f1…`. Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2C1Fabricate` (removed at the end).
Artefacts: `.ufo/waves/round-39/w2/artifacts/R39W2C1Fabricate/` (`commands.txt`,
`fabricated/K1..K6/after.json`, `c1-fabricated.json`, `c1-real.json`, `unblob-K1/`,
`unblob-K5/`, `probe-K4.json`, `fab.err`). Nothing was installed or upgraded; no VCS mutation
outside the scratch clone.

## 1. Arm A — fabrication with no REA, scored by the frozen counter

```
cd "$S/clone" && python3 -I -B .ufo/waves/round-39/w1/artifacts/R39C1Controls/_harness/fabricate_receipts.py \
  --carriers .ufo/waves/round-39/c1/carriers.json --lane-root "$S/clone" --mode forge-remint \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --out "$S/fab" --outdir-base /fast/scratch/hyaku/kaidoku-r39/R39W2C1Fabricate/ctlruns   # exit 0
# cp fab/K*/after.json over corpus/evidence/round-39/c1/K*/after.json; commit -> 9d5b60e3 (parent 6fdaf4f1)
python3 -I -B tools/round-39/c1-counter.py --root "$S/clone" --rev 9d5b60e3371a2504b658f972dadc4a8d47580e2b \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out "$S/c1-fabricated.json"
```

The harness reads only `carriers.json`, `oracle.tsv` and `symlinks.tsv`; its single subprocess is
`node tools/round-27/xpin-attribute.mjs` for the evidence ids. No REA, unblob or sasquatch process
was started. The `output_directory` it writes (`…/R39W2C1Fabricate/ctlruns/K#-after`) **does not
exist on disk** (`ls` → ENOENT): the provenance clause is satisfied by the string alone.

Counter result (`c1-fabricated.json`, exit 0):

```
carriers_matched 6, met_target true, carriers_unchanged true, frozen_path_changed []
K1..K6: matched true, oracle_hits == oracle_files (5/5, 3/3, 4/4, 4/4, 10/10, 8/8),
        gaps_ok true (0,1,0,0,2,1 == in-tree symlinks), escaping_ok true,
        run_provenance_ok true, evidence_id_ok true, receipt_fresh true
bindings: province_core_section, province_core_row, frontier_note, entry_present, sourced,
          coverage_map_row, carriers_spec_ok, symlink_coverage, xz_leg — all true
```

Control arm at the author's rev `6fdaf4f1` with the *real* receipts: also 6/6, `met_target true`
(`c1-real.json`) — so the fabricated clone and the landed tree are scored identically.

### 1.1 What the fabricated receipts got wrong (all ungraded)

Structural diff of committed K1 receipt vs fabricated K1 (22 leaf differences; the graded ones are
none of them):

| field | real (committed) | fabricated (scored 6/6) |
|---|---|---|
| `raw_result` keys | `execution`, `report`, `version_execution` | `report` only |
| `normalized_result.engine` | unblob 26.6.4 + `executable_sha256` | `null` |
| `limitations` | 6-item REA text | `null` |
| `coverage` | `partial` (K1: escaping link removed) | `complete` |
| `derivations` | 10 | 6 |
| `diagnostics[].report.link/target` | absolute REA scratch paths | relative image paths |
| `files[].mime_type` | libmagic values (`inode/x-empty`, `text/x-shellscript`) | generic octet-stream |
| `raw_result.report` | 11 tasks, md5+sha1+sha256, unblob report verbatim | 5 tasks, md5/sha1 `null` |

`grep -c` over `tools/round-39/c1-counter.py`: `raw_result` 0, `engine` 0, `execution` 0,
`version_execution` 0, `limitations` 0, `published_bytes` 0. The nine `coverage` hits are the
unrelated `coverage_map_row` binding and the docstring.

### 1.2 Why each receipt clause passes a fabricator

- `run_provenance_ok` (`c1-counter.py:219`) is `os.path.isabs` + substring `/kaidoku-r39/` +
  no `..` segment. It proves a string, not a run.
- `receipt_fresh` uses `git log --diff-filter=A`, i.e. the **oldest add** of the path. The receipts
  were already added at `6fdaf4f1` (itself after the freeze), so overwriting them passes
  `add != freeze` and `merge-base --is-ancestor freeze add` without any new add.
- `evidence_id_ok` is self-consistent: re-minting with the frozen `xpin-attribute.mjs` makes the
  stored and recomputed ids agree. It proves the receipt was hashed after writing, nothing else.
- `oracle_hits`, `gaps_ok`, `escaping_ok` are recomputed from frozen `oracle.tsv`/`symlinks.tsv` —
  exactly the inputs the fabricator consumes. A receipt built *from* the oracle necessarily hits it.
- `subject_pin_ok`, `operation_ok`, `handler_ok`, `chunks_ok` are single scalars copied from
  `carriers.json` and the handler name.

## 2. Arm B — can the committed receipts be told apart?

I probed every field a fabricator would find expensive. Independent tooling only: `unblob` 26.6.4
direct (not REA) on all six carriers, staged as REA stages them (input copied to `firmware.bin`),
plus one REA 6.5.0 probe on K4 to establish blob-id semantics.

| probe | result on the six committed receipts |
|---|---|
| `raw_result.execution.stdout.text` vs my standalone unblob banner | **byte-identical for all six** (K1, K6 via `$S/unblob-*`; K2–K5 via `$S/stage-*`). Banner sizes match each carrier's size exactly (9780→9.55 KB, 307→0.30 KB, 26813→26.18 KB, 15867→15.50 KB, 1606→1.57 KB, 4096→4.00 KB). |
| magic of the input (raw report, last task) vs `file -b <carrier>` | equal for all six after unblob's `\012- data` suffix (checked programmatically). |
| `raw_result.report` vs unblob `report.json` | K5: 24 entries both; equal **exactly** after rewriting only the extraction root and the pid. So raw_result carries no REA-specific provenance beyond path+pid. |
| `blob_id` / `chunks[].provider_id` | unblob task id = `f"{os.getpid()}:{n}"` (`unblob/identifiers.py:17`); each receipt's id equals the `pid=` on the first line of that run's `unblob.log`. So the six ids 2559184, 2674572, 2779683, 2889070, 3028394, 3197140 are six unblob PIDs. |
| PID chain vs run times | strictly increasing, matching run order; deltas over the 7/7/7/6/7 s start gaps = 16 484, 15 016, 15 627, 23 221, 24 107 pids/s. Host measured now: 21 342/s (17:32:08→13Z) and 30 874/s (17:35:12→17Z); own unblob runs at 17:30–17:34 land at 11.7k–21k/s. Epoch check: K6 pid 3 197 140 @17:17:16Z → my pid 528 604 @17:30:41Z is 4 wraps / 805 s = 22 737/s. [INFERENCE: wrap count assumed; band is the measured one.] |
| `run.json` times vs commit | runs 17:16:39→17:17:16Z, 4 s each, 3 s between; commit `6fdaf4f1` author time 17:18:32Z = 76 s after the last end. |
| receipt digest | `run.json.receipt.sha256`/`bytes` equal the committed `after.json` for all six (19 238/17 236/13 140/13 145/35 151/29 752 B). `envelope.bytes` − receipt bytes = 77 for all six; the envelope itself is not committed, so its sha256 cannot be recomputed. |
| internal path chain | all 14 checks pass on all six: `--extract-dir`/`--report`/`--log`/`firmware.bin` under one `rea-firmware-XXXXXX` sibling of the output dir; every raw-report task under that temp dir; `cwd` = its parent; `extraction_root` = `parameters.output_directory`; every `files[].path` under the output dir; every diagnostic under the temp dir; the input task's `sha256` equals the frozen pin. Six distinct temp suffixes (MSincj, 8t1CES, ozYaAd, gE4MB0, 8WPLS1, N2ZrFH). |
| body vs round 38 | K1–K4 (same carriers): **byte-identical to the round-38 receipts after normalising only run identity** (paths, pids, evidence id). That is correct for a deterministic extractor, and it means the r39 evidence for K1–K4 adds no new extraction content over `3b960fe5`. |

## 3. Verdict on the committed receipts

**Not fabricated, as far as local evidence can tell.** The three things a forger on this lane
would most likely miss — REA `execution`/`version_execution`, `engine`, and the real unblob banner —
are all present and exact. The one field a forger could not copy from a template without doing
work is the unblob PID, and the six PIDs are phase-consistent with the claimed 17:16–17:17Z window
and with the host's current fork rate (§2). No cross-carrier contamination (each banner names its
own size/chunk compression), no impossible size, no non-monotone PID, no timing inversion.

But this is *consistency*, not provenance: the counter never reads any of it, and every other
authenticity field is free — the banner and the whole `raw_result.report` are reproduced by one
0.87 s standalone `unblob` invocation (proved byte-identical), magic is `file -b` plus a suffix,
`engine.executable_sha256` is this host's constant, and `run.json` is written by the harness, not
by REA. A forger who runs unblob (or copies the round-38 body and edits paths/pids) reproduces the
landed receipts; §1 shows the counter cannot distinguish the result from the real thing.

## 4. Impacted axes

- **Coverage (R39-C1):** the axis is scored on receipt *contents*, and the only clause that claims
  a run happened (`run_provenance_ok`) is a substring test on a path the claimant writes.
  The 6/6 at `6fdaf4f1` says "six self-consistent envelopes exist", not "extract-firmware ran six
  times this round". The author's verdict is reproducible but does not certify provenance.
- **Depth (R39-C2):** unaffected. C2's held-out material has a generator-run binding (seed = freeze
  hash, `tools/round-39/heldout-gen.py`), a shape the C1 predicate lacks.
- **Calibration:** nothing to retire; the counter's `selftest` and the freeze-drift binding are
  untouched by this result.

## 5. Smallest safe correction

Only one correction is safe and minimal enough to name: **stop grading the claimant-written
receipt as the evidence of a run.** Have the counter itself execute
`REA_UNBLOB_COMMAND=<abs unblob> npx -y rea-agents@6.5.0 extract-firmware --format json
--full-output <carrier> <counter-chosen fresh outdir>` (with `sasquatch-v4be` on the child PATH)
and score handler / no-failed-chunk / oracle file set + sha256 / gap kind + path set from **its
own** envelope, keeping the committed receipt as an optional cross-check on normalized fields
never on ids or `raw_result`. That is the same recommendation wave 1 made (`R39C1Controls.md` §5)
and the freeze did not take it.

If a counter-owned run is unacceptable, the minimum extra binding is: require
`raw_result.version_execution.exit_code == 0` and `command == engine.executable_path` with
`engine.executable_sha256` equal to the hash of the unblob the **counter** resolves at scoring
time, plus `raw_result.execution.stdout.text` equal to the banner the counter gets from its own
`unblob <carrier>` run. That raises the forger's cost from "write JSON" to "run unblob" — it does
**not** make the receipt evidence, because running unblob at fabrication time reproduces all of it
(§2). The PID chain is the only residual check, and it is unbound and would have to be frozen
explicitly as `blob_id == <pid from the run's unblob.log>` with the log committed, which is still
claimant-authored.

## 6. Limits

- One REA invocation (K4 probe) was used only to establish that `blob_id` is a PID; the fabricated
  receipts do not use it.
- No counter-owned re-run of K1–K6 was performed (that is the correction, not this seat's job).
- PID phase-consistency is [INFERENCE] on the wrap count; the rate band is measured.
- The K1–K4 "identical to round 38 modulo run identity" result compares committed bodies only;
  it does not show round 39 was a copy — only that a copy would be indistinguishable.
