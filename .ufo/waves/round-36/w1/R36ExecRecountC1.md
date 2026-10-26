# R36ExecRecountC1 — frozen C1 counter re-run (independent recount)

Seat: `R36ExecRecountC1` (leaf executor, advisory). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Revisions: freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`, base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`,
C1 after receipts `3310d8fa27bfaa95ad858c4aaad6f6377f853982`, lane HEAD at run time `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`.
Nothing in the lane was written except this report; no VCS mutation; no counter, predicate, carrier or oracle touched.

## Environment (observed)

| item | value |
|---|---|
| python | `Python 3.14.8` (`python3 --version`) |
| node | `v24.21.0` |
| git | `git version 2.56.0` |
| rea-agents | 6.5.0 — only package root containing it: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`package.json` `version: 6.5.0`; second npx cache `dea9475797100b20` holds 6.4.0 and was not used) |
| unblob | `26.6.4` (`/home/vgpnk/.local/bin/unblob` → `…/uv/tools/unblob/bin/unblob`) |
| sasquatch | `/home/vgpnk/.local/bin/sasquatch`, sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, `-version` → `unsquashfs version 4.5.1 (2022/03/17)` |
| unsquashfs | `version 4.7.5 (2026/03/01)` (`/usr/bin/unsquashfs`) |

No tool installed or upgraded by this seat (units in the table above were already present; nothing was fetched from a package channel).

## 1. Selftest — exact command, output, exit code

```
$ python3 -I -B tools/round-36/c1-counter.py --selftest \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
{"selftest": "c1-counter", "cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}
EXIT=0
```

14 cases as frozen (1 green, 13 red), `failures: []`. Matches the claim's selftest description exactly.

## 2. Recount at the measured after revision `3310d8fa`

```
$ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-36/c1-counter.py \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev 3310d8fa27bfaa95ad858c4aaad6f6377f853982 \
    --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
{"bindings": {"coverage_map_row": false, "entry_present": false, "entry_source_ids": [], "opened_source_rows": [],
  "province_core_row": false, "province_core_section": false, "sourced": false},
 "carriers_matched": 4, "carriers_unchanged": true, "met_target": false,
 "revision": "3310d8fa27bfaa95ad858c4aaad6f6377f853982"}
EXIT=1
```

**`carriers_matched == 4` confirmed** (target value) and `carriers_unchanged: true`. `met_target: false`, exit 1.

Per-carrier fields (`--json-out` to scratch, same run, `EXIT=1`):

| carrier | oracle_files | before_hits | after_hits | before_sasquatch_gap | after_sasquatch_gap | before/after evidence_id_ok | matched |
|---|---|---|---|---|---|---|---|
| K1 | 3 | 0 | 3 | true | false | true / true | true |
| K2 | 4 | 0 | 4 | true | false | true / true | true |
| K3 | 2130 | 0 | 2130 | true | false | true / true | true |
| K4 | 2130 | 0 | 2130 | true | false | true / true | true |

`oracle_frozen: true` for all four; `before_present/after_present/subject_ok/operation_ok` true for all four.

### Bindings still false at `3310d8fa` (this is why the target is not met)

Five decisive bindings are false — all documentary, none evidential:

1. `entry_present` — `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` absent at that revision (`ls corpus/knowledge | grep -i r36` → none at HEAD either).
2. `province_core_section` — no `## Round-36 additions to Core` heading (`git show d2e46ef5:PROVINCE.md | grep '^## '` ends at `## Round-32 additions to Core (verified 2026-10-23)`).
3. `province_core_row` — no Core row naming `sasquatch` citing the entry (depends on 1+2).
4. `sourced` — no `SOURCES.md` row with `opened == 2026-10-26` whose used-by lists the entry (`git show d2e46ef5:corpus/SOURCES.md | grep -c '^| S107'` → `0`; no S-id is pinned yet, `entry_source_ids: []`).
5. `coverage_map_row` — no `## Coverage map` row in `corpus/README.md` carrying the stem.

## 3. Recount at the base `cab59f22` (the claim's "unmoved" command)

```
$ python3 -I -B …/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev cab59f221fe19726b5692bfa4d9a9679e96b8a73 \
    --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 --pkg65 …/rea-agents
{"bindings": {"coverage_map_row": false, "entry_present": false, "entry_source_ids": [], "opened_source_rows": [],
  "province_core_row": false, "province_core_section": false, "sourced": false},
 "carriers_matched": 0, "carriers_unchanged": false, "met_target": false,
 "revision": "cab59f221fe19726b5692bfa4d9a9679e96b8a73"}
EXIT=1
```

Exit 1 at base reproduced, `carriers_matched == 0` (no `K*/before.json`/`after.json` exist at base;
`carriers_unchanged: false` occurs because `corpus/evidence/round-36/c1/carriers.json` does not exist at base, so
`git show <base>:carriers.json` is `None` and cannot equal the freeze bytes — the exit code is the correct one, the
label is only imprecise; see §7.1).

## Extra data point (not requested, cheap): lane HEAD `d2e46ef5`

```
{"bindings": {… all five decisive bindings false …}, "carriers_matched": 4,
 "carriers_unchanged": true, "met_target": false, "revision": "d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be"}
EXIT=1
```

C2's landing (`d2e46ef5`) leaves C1 at the same state as `3310d8fa`: evidence is complete for all four carriers, the
entry/PROVINCE/SOURCES/README documents are still missing. Any green run must happen at a later revision that adds them.

## 4. Frozen-instrument immutability (checked, not assumed)

```
$ git rev-parse <rev>:tools/round-36/c1-counter.py
cab59f22 → MISSING (counter is introduced at the freeze)
790561d4 → 654c3cd0ec2ec0152cdc420cdd5d8e6799c2951c
3310d8fa → 654c3cd0ec2ec0152cdc420cdd5d8e6799c2951c
d2e46ef5 → 654c3cd0ec2ec0152cdc420cdd5d8e6799c2951c
$ git diff --stat 790561d4 3310d8fa -- tools/round-36/c1-counter.py corpus/evidence/round-36/c1/carriers.json \
    'corpus/evidence/round-36/c1/K*/oracle.tsv' corpus/evidence/round-36/c1/fixtures      → (empty, rc=0)
$ git diff --stat 790561d4 HEAD    -- <same paths>                                        → (empty, rc=0)
$ git log --oneline 790561d4..HEAD -- <same paths>                                        → (empty)
```

Counter, carriers.json, all four `oracle.tsv` and both committed fixtures are byte-identical at freeze, at the after
revision and at HEAD. The recount therefore measures the frozen instrument, not a moved one.

## 5. Independent re-derivations (my own implementations, not the counter, not xpin)

### 5.1 Evidence-ID rule of rea-agents 6.5.0, recomputed from the package's own definition

I read `const semanticProjection = …` out of `…/rea-agents/dist/domain/evidence.js` (6.5.0) and the canonical-hash
semantics out of `dist/domain/canonicalDigest.js`, then re-implemented RFC-8785 canonicalisation + sha256 in Python and
hashed the stored `.data` records (no field inserted or defaulted; `relationship_coverage` included only when not null).
All eight committed envelopes recompute to their stored ids:

| envelope | stored == independent |
|---|---|
| K1/before | `ev_df7bef526779b3062cc0a8f149f6c32a2b5849ac2f40150df58b69df00178da3` ✔ |
| K1/after | `ev_b5bd2e7f0ea0b9f6e65d04d68826507464983c2d226b6fa4c542f4dcf64fc860` ✔ |
| K2/before | `ev_7506d2a8715ac018b5b2f7aa1f1c16dd43d78c5f1bbd489fa19ceba6d5767b3c` ✔ |
| K2/after | `ev_c939cd88f616e8759ed2c8656f98745fd8e90aa6589a744b25f33b6366b0c88f` ✔ |
| K3/before | `ev_91e4ab30b6a5edf4ab7a14d5a14867cac75b0e161090c5db7db6b73027e9a44a` ✔ |
| K3/after | `ev_b83bd3056f103a72e2a611a5162f542715119490a44bb60135393b5002f5419b` ✔ |
| K4/before | `ev_fffca90bc4b70989308fcc378c3cdefdd5baaf8ee878d8e624dc31709f5b1a01` ✔ |
| K4/after | `ev_ff0fdb798eea077df0b11dcdd3795794c9069c667424b85c5f67f566c97379fa` ✔ |

So the counter's `*_evidence_id_ok` is not self-confirming: an independent implementation of the pinned rule agrees.

### 5.2 Independent oracle match (`sha256` equality + `path == rel or path.endswith('/'+rel)`)

| carrier | oracle rows | after hits | after misses | before hits | after files published |
|---|---|---|---|---|---|
| K1 | 3 | 3 | 0 | 0 | 3 |
| K2 | 4 | 4 | 0 | 0 | 4 |
| K3 | 2130 | 2130 | 0 | 0 | 2147 |
| K4 | 2130 | 2130 | 0 | 0 | 2147 |

`published_bytes`: K1 70086, K2 273971, K3 51122564, K4 51792724. The 17 non-oracle K3/K4 after entries are recursive
`*.elf64_extract/carved.elf` + `*.padding` chunks (e.g.
`firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/bin/nvim_extract/0-11170568.elf64_extract/carved.elf`),
i.e. unblob's whole-chunk/recursion output sitting beside the squashfs contents, as disclosed pre-freeze.

### 5.3 Live reproduction of all four carriers with the frozen harness (`tools/round-36/c1-run.sh`)

Carriers taken from `git show 3310d8fa:` (K1/K2 fixtures) and from the frozen URLs (K3/K4); downloaded digests equal
`carriers.json` exactly (`b644d034…f29fb`, `8efcec73…e1c2`). `before` mode removes every PATH dir holding an executable
`sasquatch` (harness exits 2 if one survives; it exited 0), `after` mode requires it to resolve.

| carrier | oracle.tsv byte-identical to committed | after file set (relpath,sha256) identical | before file set identical | after sasquatch gap | before sasquatch gap |
|---|---|---|---|---|---|
| K1 | ✔ (3 rows) | ✔ (3) | ✔ (0) | absent | present (`squashfs_v4_le`) |
| K2 | ✔ (4 rows) | ✔ (4) | ✔ (0) | absent | present (`squashfs_v4_le`) |
| K3 | ✔ (2130 rows) | ✔ (2147) | ✔ (2) | absent | present (`squashfs_v4_le`) |
| K4 | ✔ (2130 rows) | ✔ (2147) | ✔ (2) | absent | present (`squashfs_v4_le`) |

All harness invocations `rc=0`; `after-run.json` recorded `sasquatch_version: unsquashfs version 4.5.1 (2022/03/17)`
and `sasquatch_sha256: ad02d27a…` in every after run, empty in every before run. So the receipts' central claim — sasquatch
on PATH turns "nothing published + `missing-extractor-dependency: [sasquatch]`" into "every oracle regular file
published, no sasquatch gap" — reproduces live on all four frozen carriers.

## 6. Kill-rule controls (frozen receipts re-read, one re-run)

| control | stored exit | revision | result |
|---|---|---|---|
| CTL-C1-0 do-nothing (`cab59f22`) | 1 | `cab59f22…` | reproduced by my §3 run: `carriers_matched 0`, exit 1 |
| CTL-C1-1 no-sasquatch pipeline, all bindings present | 1 | `104dd4a2…` (fixture repo, now gone) | stored: all bindings true, `carriers_matched 0`, exit 1 |
| CTL-C1-2 forged oracle-copy envelope | 1 | `6a16267c…` (fixture repo, now gone) | stored: all bindings true, `carriers_matched 0`, exit 1 |

No control meets the target, so the kill rule did not fire and C1 was allowed to run. CTL-C1-1/CTL-C1-2 ran against
transient scratch fixture repos (`--root /fast/scratch/hyaku/kaidoku-r36/L1/ctl.*`), whose commits are absent from the
lane's objects (`git cat-file -e` → ABSENT), so they cannot be re-run from the repo; their logic is what selftest cases
3 (`after := before`) and 4 (`forged oracle-copy`) exercise, and both were red in my §1 run.

## 7. Observations (advisory — reported, not repaired)

1. **`carriers_unchanged` label.** The key means "carriers.json at the measured revision equals the freeze bytes". At
   base it is `false` only because the file does not exist there yet. Exit code is still correct; the field name
   over-reads if quoted as "carriers were changed". [INFERENCE] A base-relative control receipt quoting
   `carriers_unchanged: false` as evidence of tampering would be misreading it.
2. **Counter binding set is a strict superset of the literal P36-C1 sentence.** `c1-counter.py:230` requires
   `coverage_map_row` (`corpus/README.md` `## Coverage map` row carrying the stem, line 228) in addition to the four
   document bindings named in the predicate sentence (PROVINCE Core row, entry present, SOURCES row opened
   2026-10-26 with used-by, province Core section). P36-C1 as written in `plans/round-36-claims.md` never names a
   README coverage-map row. Consequence: a revision satisfying the letter of P36-C1 but without that README row would
   still exit 1. Not a defect in the observed runs (both fail for the same reason), but the L1 must land the README
   coverage-map row as well, or the target is unreachable.
3. **Reproducibility boundary of the "recompute to stored evidence id" clause.** Recomputing the *stored* envelope is
   exact (§5.1). Re-*running* the pipeline at a different output directory does not reproduce the stored id: the
   pinned projection hashes `parameters.output_directory`, every `normalized_result.files[].path`, `raw_result.report`,
   and unblob's per-run `provider_id` / `provider_blob_id` (observed K3 after: `564135:*` vs `348751:*`). The clause
   therefore proves envelope integrity, not run reproducibility; reproducibility of the evidential content is what §5.3
   shows (identical `relative_path`/`sha256` sets).
4. **K2 after carries a `unpublished-entry` gap** (coverage `partial`) while still publishing all 4 oracle files with no
   sasquatch gap; K3/K4 after carry two `unpublished-entry` gaps each (`partial`), K1 after is `complete`. Predicate
   binds only the sasquatch dependency gap, so this is in-scope-consistent — but any later prose calling the after runs
   "complete extraction" would be false for K2/K3/K4.
5. **`rea` field in `*-run.json` is a harness literal** (`{…"rea":"rea-agents@6.5.0"…}` hard-coded in `c1-run.sh`), not
   an observed version. The observed pins in those receipts are `provider.version 26.6.4` and
   `engine.executable_sha256 0ce7b624…`; the REA pin is only observable from the `npx -y rea-agents@6.5.0` argument
   plus the cache layout checked in §Environment.

No observation above changes any exit code I measured, and none is a counter/predicate defect that I repaired.

## 8. Limits and non-claims

- K3/K4 carrier bytes are not committed (URL-fetched); their integrity rests on the sha256 match I performed against
  `carriers.json` (§5.3) and, per the claim, GitHub's published digest. I did not independently verify GitHub's digest
  page — only that the downloaded bytes hash to the frozen value.
- Only extraction was exercised. Nothing here speaks to loader/execution behaviour of the extracted payloads, to
  big-endian/AVM SquashFS, or to the 7z fallback (matching the claim's "Not claimed" list).
- CTL-C1-1/CTL-C1-2 could not be re-executed (fixture revisions absent from lane objects); only their stored receipts
  plus the equivalent selftest cases were checked.
- The `--json-out` detail file and all reproduced receipts lived in
  `/fast/scratch/hyaku/kaidoku-r36/R36ExecRecountC1/` (removed on completion, per bounds); every number quoted above is
  reproduced by the commands or read-only git reads in this report, not by a scratch path.

## Verdict

`carriers_matched == 4` at `3310d8fa27bfaa95ad858c4aaad6f6377f853982`, `carriers_unchanged: true`, counter exit **1**;
`met_target: false` with the five documentary bindings still false (`entry_present`, `province_core_section`,
`province_core_row`, `sourced`, `coverage_map_row`), and `entry_source_ids: []` / `opened_source_rows: []`. Base
`cab59f22` exits 1 with `carriers_matched 0`. Selftest 14/14 as frozen, exit 0. Frozen counter/carriers/oracles/fixtures
byte-identical across freeze, after and HEAD. Evidence side of P36-C1 is independently confirmed (ids recomputed with my
own implementation of the 6.5.0 rule; oracle matches counted with my own matcher; all four carriers re-run live with the
frozen harness reproducing the committed file sets, gaps and oracle.tsv). P36-C1 is an honest "not yet" that is blocked
only on the round-36 entry, the PROVINCE Core row, the SOURCES row opened 2026-10-26 whose used-by lists that entry, and
the `corpus/README.md` coverage-map row the counter additionally requires.
