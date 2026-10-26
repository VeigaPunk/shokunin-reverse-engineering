# R36W2ExecC1Final — R36-C1 frozen counter re-run at the C1 landing and the integration tip

Seat: executor, wave 2 (falsify the integrated landing). Axes: coverage, calibration.
Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Assigned tip
`01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`; the lane HEAD advanced to
`6f2ba761bb5bcd6482d45523379376dcb6a386f6` mid-seat (`.ufo/waves/` only, §1.4), where the counter also
exits 0. Freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`.

**Verdict.** Every assigned measurement reproduces: the frozen counter exits **0 with
`carriers_matched 4` and all bindings true at both `ffc81341` and `01a44dbf`**, and the selftest is
**14/14 (1 green, 13 red), exit 0**. Counter bytes are byte-identical at the freeze, at both measured
revisions and in the worktree. I found **no disagreement** between the counter's outputs and the frozen
claim. I did measure one property the counter does *not* have: a fixture whose four `after` envelopes are
fabricated from the oracle and re-stamped with the package's own digest code scores `met_target true`
(§6) — the M36-4/F1 blind spot, confirmed live at the tip's content. That does not falsify the landing's
data, which I reproduced independently (§5); it bounds what the counter's green proves.

## 1. Exact commands and outputs

All runs: `HYAKU_SCRATCH` and `TMPDIR` pointed at the seat scratch
(`/fast/scratch/hyaku/kaidoku-r36/R36W2ExecC1Final`), removed at the end (§9). `pkg65` =
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` version **6.5.0**;
`node v24.21.0`; `/usr/bin/unsquashfs` **4.7.5 (2026/03/01)**.

### 1.1 Counter at the C1 landing `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95`

```
$ python3 -I -B tools/round-36/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev ffc813417d3bceeeb7b028b12ce0be8a5dc33d95 \
    --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <scratch>/c1-ffc81341.json
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"],
 "opened_source_rows": ["S107", "S108", "S109"], "province_core_row": true, "province_core_section": true,
 "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
 "revision": "ffc813417d3bceeeb7b028b12ce0be8a5dc33d95"}
EXIT=0
```

### 1.2 Counter at the integration tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`

```
$ python3 -I -B tools/round-36/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930 \
    --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <scratch>/c1-tip.json
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"],
 "opened_source_rows": ["S107", "S108", "S109"], "province_core_row": true, "province_core_section": true,
 "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
 "revision": "01a44dbf45913a1bdcabbbfb85b7bb9d232cb930"}
EXIT=0
```

Per-carrier fields from the tip receipt (`--json-out`), identical shape at both revisions:

| carrier | oracle_files | before hits / gap | after hits / gap | subject_sha ok | evidence ids (before, after) | matched |
|---|---|---|---|---|---|---|
| K1 | 3 | 0 / true | 3 / false | true | true, true | true |
| K2 | 4 | 0 / true | 4 / false | true | true, true | true |
| K3 | 2130 | 0 / true | 2130 / false | true | true, true | true |
| K4 | 2130 | 0 / true | 2130 / false | true | true, true | true |

`oracle_frozen` true for all four; `carriers_unchanged` true; `carriers_matched` 4.

### 1.3 Selftest (worktree counter bytes)

```
$ python3 -I -B tools/round-36/c1-counter.py --selftest \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
{"selftest": "c1-counter", "cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}
EXIT=0
```

Selftest from the **freeze-extracted** counter and freeze-archived fixtures (scratch mirror
`<scratch>/freeze-counter/tools/{round-36/{c1-counter.py,selftest},round-27/xpin-attribute.mjs}` built with
`git show 790561d4:… > …` and `git archive 790561d4 tools/round-36/selftest tools/round-27/xpin-attribute.mjs | tar -x`),
run from `<scratch>` as cwd — same result, so the green does not depend on the worktree copy:

```
5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5  <scratch>/freeze-counter/tools/round-36/c1-counter.py
{"selftest": "c1-counter", "cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}
EXIT=0
```

14 cases = the claim's 1 green + 13 named red cases; `failures: []`.

### 1.4 The lane tip moved during this seat — measured there too

While this seat ran, the lane HEAD advanced from the assigned tip `01a44dbf…` to
`6f2ba761bb5bcd6482d45523379376dcb6a386f6` ("wave-1 results (43/43 settled) and last report; wave-2
spec/dispatch"). That commit touches only `.ufo/waves/round-36/` (results, one wave-1 report, w2 spec and
dispatch), and none of the files the C1 counter reads:

```
$ git diff --stat 01a44dbf 6f2ba761 -- corpus/evidence/round-36/c1 PROVINCE.md corpus/README.md \
    corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md corpus/SOURCES.md tools/round-36
(no output)

$ … --rev 6f2ba761bb5bcd6482d45523379376dcb6a386f6 …
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"],
 "opened_source_rows": ["S107", "S108", "S109"], "province_core_row": true, "province_core_section": true,
 "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
 "revision": "6f2ba761bb5bcd6482d45523379376dcb6a386f6"}
EXIT=0
```

So the assigned measurement at `01a44dbf` is also the measurement at the current HEAD.

### 1.5 Sensitivity on the real repo (the counter is not vacuous)

```
$ … --rev cab59f221fe19726b5692bfa4d9a9679e96b8a73 …
{"bindings": {"coverage_map_row": false, "entry_present": false, "entry_source_ids": [],
 "opened_source_rows": [], "province_core_row": false, "province_core_section": false, "sourced": false},
 "carriers_matched": 0, "carriers_unchanged": false, "met_target": false,
 "revision": "cab59f221fe19726b5692bfa4d9a9679e96b8a73"}
EXIT=1

$ … --rev d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be …
{"bindings": {"coverage_map_row": false, "entry_present": false, "entry_source_ids": [],
 "opened_source_rows": [], "province_core_row": false, "province_core_section": false, "sourced": false},
 "carriers_matched": 4, "carriers_unchanged": true, "met_target": false,
 "revision": "d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be"}
EXIT=1
```

`d2e46ef5` (C2 landing, before C1's entry) is the sharp control: all four carrier pairs already score
4/4 there, and the run still exits 1 on the missing bindings — the counter's green at `ffc81341`
depends on the C1 entry/PROVINCE/SOURCES/README landing, not only on the receipts.

## 2. Counter bytes at both revisions equal the freeze bytes

```
$ for r in 790561d4… ffc81341… 01a44dbf…; do printf '%s  ' "$r"; \
    git show "$r:tools/round-36/c1-counter.py" | sha256sum; done
790561d4e3aca732a434081aa9573ec2fa5fd7d0  5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5  -
ffc813417d3bceeeb7b028b12ce0be8a5dc33d95  5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5  -
01a44dbf45913a1bdcabbbfb85b7bb9d232cb930  5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5  -
$ sha256sum tools/round-36/c1-counter.py
5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5  tools/round-36/c1-counter.py
```

History of the file is a single commit, and the freeze is an ancestor of both measured revisions:

```
$ git log --oneline --follow -- tools/round-36/c1-counter.py
790561d4 round-36: freeze R36-C1/C2 predicates, counters, selftests, carriers, oracle and before receipts
$ git merge-base --is-ancestor 790561d4 <rev>   # ffc81341: freeze is ancestor; 01a44dbf: freeze is ancestor
```

The selftest fixtures and the xpin tool it reads are also unchanged between freeze and tip
(`git diff --stat 790561d4 01a44dbf -- tools/round-36/selftest tools/round-27/xpin-attribute.mjs` → empty).

## 3. Calibration against wave 1's stored receipt

My `ffc81341` receipt and wave-1's `.ufo/waves/round-36/after/c1-at-ffc81341.json` are equal field-for-field
(`revision`, `freeze`, `target`, `carrier_ids`, all four `carriers` dicts, `bindings`, `carriers_matched 4`,
`carriers_unchanged true`, `met_target true`); the only differences are `argv` (`--root .` vs the absolute
lane path, and the `--json-out` path). The freeze-extracted counter run from a scratch cwd at the tip
produced a receipt identical to the worktree run with `argv` stripped (`a==b` after `pop('argv')`), so the
measurement is cwd-independent and worktree-independent.

## 4. Wave-1's C1 inputs were not edited after landing

```
$ git diff --stat ffc81341 01a44dbf -- corpus/evidence/round-36/c1 PROVINCE.md corpus/README.md \
    corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md corpus/SOURCES.md tools/round-36
(no output)
```

Nothing the counter reads changed between the C1 landing and the tip, which is why the two assigned
measurements are identical by construction as well as by execution.

## 5. Independent corroboration (not the counter)

### 5.1 All four frozen oracles regenerate byte-identically from carrier bytes

Carrier bytes: K1/K2 committed fixtures (digests equal `carriers.json`); K3/K4 downloaded in scratch from
the frozen URLs and matching `carriers.json` exactly —
`b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb` (x86_64) and
`8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2` (arm64). Oracle regenerated with the
lane harness (`tools/round-36/c1-run.sh oracle …`) and diffed against `git show 01a44dbf:…/K*/oracle.tsv`:

| carrier | carrier sha256 | offset | unsquashfs | rows | `diff -q` vs committed |
|---|---|---|---|---|---|
| K1 | `93802938…9b8a589` | 0 | 4.7.5 | 3 | byte-identical |
| K2 | `ce5bf60e…a2084f` | 0 | 4.7.5 | 4 | byte-identical |
| K3 | `b644d034…c35f29fb` | 944632 | 4.7.5 | 2130 | byte-identical |
| K4 | `8efcec73…c9efe1c2` | 936456 | 4.7.5 | 2130 | byte-identical |

So the frozen oracle is exactly what `/usr/bin/unsquashfs` 4.7.5 produces on the frozen carrier bytes, and
the oracle's provenance (which tool, which offset) — which the counter never reads — checks out.

### 5.2 Independent matcher at the tip

A one-off script (not the counter) reading `git show 01a44dbf:…` and applying the predicate's rule
(`same relpath suffix AND same sha256`, regular files only) reproduces the counter's numbers exactly:

```
K1 before: oracle=3   published=0    hits=0    sasquatch_gap=1  subject_sha_ok=True
K1 after : oracle=3   published=3    hits=3    sasquatch_gap=0  subject_sha_ok=True
K2 before: oracle=4   published=0    hits=0    sasquatch_gap=1  subject_sha_ok=True
K2 after : oracle=4   published=4    hits=4    sasquatch_gap=0  subject_sha_ok=True
K3 before: oracle=2130 published=2   hits=0    sasquatch_gap=1  subject_sha_ok=True
K3 after : oracle=2130 published=2147 hits=2130 sasquatch_gap=0  subject_sha_ok=True
K4 before: oracle=2130 published=2   hits=0    sasquatch_gap=1  subject_sha_ok=True
K4 after : oracle=2130 published=2147 hits=2130 sasquatch_gap=0  subject_sha_ok=True
```

The no-sasquatch receipts publish nothing from the oracle (K3/K4 publish only the carved ELF and the carved
squashfs chunk). The 17 extras per AppImage are recursion artefacts (`…_extract/0-…elf64_extract/carved.elf`,
`…_extract/…padding`) and the `unpublished-entry` gaps are the two symlinks `.DirIcon` and `nvim.png`
(K2: `var/notice-link`) — neither is a regular file, so "every regular file of the oracle" holds literally.

### 5.3 Live re-runs at the tip environment

Harness `after`/`before` on the committed K1 fixture and `after` on K2, into scratch
(`sasquatch` = `/home/vgpnk/.local/bin/sasquatch`, sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`,
self-reported `unsquashfs version 4.5.1 (2022/03/17)` — the sha256 and version the PROVINCE Core row states):

```
K1 after EXIT=0   after-run.json: exit 0, sasquatch_sha256 ad02d27a…, carrier_sha256 93802938…
K1 before EXIT=0  before-run.json: exit 0, sasquatch ""
K2 after EXIT=0
K1 before: files live==committed True (0 vs 0); gaps live==committed True (1 vs 1)
K1 after : files live==committed True (3 vs 3); gaps live==committed True (0 vs 0)
K2 after : files live==committed True (4 vs 4); gaps live==committed True (1 vs 1)
```

Live evidence ids differ from the committed ones (run-specific envelope content) and each recomputes to
itself under the freeze xpin tool with pkg65 (`stored==recomputed True` for all three). The committed
receipts' own ids also recompute (counter fields `before/after_evidence_id_ok true`, §1.2). The entry's
stated `recheck:` line (`c1-run.sh after` on the K1 fixture → `{"files":3,"gaps":0}`) is exactly what I
measured; I used my seat scratch as `S` instead of the entry's `/fast/scratch/hyaku/recheck-r36`.

### 5.4 Committed run sidecars (which the counter never reads)

`K*/{oracle,before,after}-run.json` are present at the tip and consistent: oracle and before stamped
`2026-10-26T04:17:49Z`, after `2026-10-26T04:22:42Z` (oracle frozen before any sasquatch-enabled run);
before sidecars record no sasquatch; after sidecars record `ad02d27a…` / 4.5.1; every `exit` is 0; the
oracle sidecars record `unsquashfs version 4.7.5 (2026/03/01)` and `regular_files` 3/4/2130/2130.

## 6. Falsification measured: the counter cannot tell a fabricated receipt from a real one

Wave-1 F1 / lesson M36-4 said a re-hashed oracle-copy envelope scores `met_target`. I confirmed the
mechanism at the tip's content and then measured the acceptance end-to-end, in a scratch fixture repo
(`git -C "$D" rev-parse --show-toplevel` == `$D` verified before the first commit):

1. Fixture freeze commit `0943d115837306e4fd30658e2fb53af32148ad60`: freeze bytes of `carriers.json`,
   `K*/oracle.tsv`, `K*/before.json`, `tools/round-27/xpin-attribute.mjs`; tip bytes of `PROVINCE.md`,
   the R36 entry, `corpus/SOURCES.md`, `corpus/README.md`.
2. For each carrier, forge `after.json` from the committed `before.json`: set
   `normalized_result.files` to `{relative_path: 'firmware.bin_extract/'+rel, sha256: sha}` for every oracle
   row, set `extraction_gaps` to `[]`, then **stamp** `evidence_id` with the id the package's own code
   computes (wrap as `{"data": env}`, run `xpin-attribute.mjs --pkg65 <6.5.0> --pkg67 <6.5.0>`, take the
   recomputed field, write it back; verified `stored==recomputed` afterwards). No sasquatch-enabled run
   happened anywhere in this fixture.
3. Data commit `10ca2b1c018c2c06366a32c703e3af255a182109`; then the frozen counter, unmodified:

```
$ python3 -I -B tools/round-36/c1-counter.py --root <fixture> --rev 10ca2b1c… --freeze 0943d115… \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"],
 "opened_source_rows": ["S107", "S108", "S109"], "province_core_row": true, "province_core_section": true,
 "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
 "revision": "10ca2b1c018c2c06366a32c703e3af255a182109"}
EXIT=0
K3 flags {'after_evidence_id_ok': True, 'after_oracle_hits': 2130, 'after_sasquatch_gap': False,
          'before_evidence_id_ok': True, 'before_oracle_hits': 0, 'before_sasquatch_gap': True}
```

The stored control `ctl-c1-2-forged-oracle-copy.json` shows the same envelopes rejected *only* by the id
check (`after_evidence_id_ok false`, `after_oracle_hits` 3/4/2130/2130, `after_sasquatch_gap false`), so the
frozen selftest's "forged oracle-copy envelope" red case covers the un-stamped variant, not this one.

What this does and does not mean: the counter's green is a statement about *structure* — oracle coverage,
gap absence, id self-consistency, and the documentation bindings. It is not a statement about provenance.
The landing's provenance rests on the receipts being real, which I corroborated independently in §5
(live re-runs reproduce the committed `files`/`gaps` exactly; four wave-1 seats reproduced K1–K4). A
round-37 criterion that makes a receipt's *production* verifiable (e.g. a sidecar the counter must read and
cross-check: carrier sha, sasquatch sha on PATH, exit code, envelope digest) would close this; I did not
change the frozen counter.

## 7. Instrument limits observed (recorded, not repaired)

- `sasquatch_gap()` (`tools/round-36/c1-counter.py:124-129`) matches only
  `kind == 'missing-extractor-dependency'` with `'sasquatch' in dependencies`. The tip's after receipts do
  carry `unpublished-entry` gaps (K2 one, K3/K4 two) which it ignores. This agrees with the predicate as
  written ("every regular file … no sasquatch extraction gap"): the gaps are the symlinks, verified in §5.2.
- The counter never reads `K*/{before,after,oracle}-run.json`, so "run with sasquatch on PATH" is unverified
  by it — the sidecar evidence in §5.4 is outside the scored predicate.
- `evidence_ids()` (`:81-107`) passes `pkg65` as both `--pkg65` and `--pkg67`; this matches the claim
  ("under the rea-agents 6.5.0 rule") but means a 6.7.0-rule divergence is not observable here.
- `selftest()` reads its fixtures from `os.path.dirname(__file__)/selftest` and xpin from the worktree, not
  from a revision. Freeze↔tip bytes are identical (§2) and the freeze-archive copy passes (§1.3), so this
  is not load-bearing this round.

## 8. Observations for the L1 (not counter disagreements)

- `PROVINCE.md:156-157` still reads `- **sasquatch** — unblob's squashfs recursion extractor (AUR-only);
  7z fallback covers the carved-image path today.` The supersession is a separate Frontier note at
  `PROVINCE.md:374` ("… is superseded for little-endian SquashFS v4 as measured above; its "(AUR-only)" was
  wrong as a route statement …"). A reader who reads the Frontier list alone still sees the stale route
  statement; the README counterpart (`corpus/README.md:232-233`) at least carries its dated note on the
  adjacent line. The frozen predicate only requires the Core row, so this is not a miss — it is the one
  place where the moved surface's old text reads as current.
- The Core row (`PROVINCE.md:372`) and the README coverage-map row (`corpus/README.md:89`) state the same
  counts I measured (3/3, 4/4, 2130/2130, 2130/2130) and the same "symlinks stay `unpublished-entry`"
  reading; no drift found.

## 9. Cleanup and tooling

- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ExecC1Final` (fixtures, downloaded AppImages, receipts,
  freeze mirror, forge inputs) removed at the end of the seat; the fixture repo was removed after scoring.
  No `find`/`du` under `/fast/scratch` was run; no lane file other than this report was written; no VCS
  mutation in the lane (all git calls were `show`/`log`/`diff`/`ls-tree`/`archive`/`merge-base --is-ancestor`,
  plus `init`/`add`/`commit` inside scratch fixtures).
- No installs or upgrades. Used the already-present `node v24.21.0`, `python3`,
  `/usr/bin/unsquashfs` 4.7.5, `sasquatch` 4.5.1 at `~/.local/bin/sasquatch` (untouched), `unblob` 26.6.4
  via `~/.local/bin/unblob`, `npx`-cached `rea-agents` 6.5.0. No pacman transaction.
