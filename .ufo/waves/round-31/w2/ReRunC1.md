# ReRunC1 — R31-C1 counter re-run at lane tip vs committed receipt

Seat: `KaidokuR31.ReRunC1` (v1 falsify wave, round 31, wave 2). Leaf member — no subagents.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Tip: `1288285eed81395e6af7c279a173b117b2c2eaa3` (2026-10-23T04:27:07Z, `%ct` 1792729627). Working dir: `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReRunC1/`.

## What I was asked

1. Re-run the R31-C1 counter at the lane tip in measure mode (no `--write-evidence`).
2. Diff its stdout with the committed receipt `.ufo/waves/round-31/after/c1-sqlite-positive-at-0007731e.txt`.
3. Run `--selftest`.
4. Confirm no commit after `0007731e` changes a file the counter reads.

## Commands run (exact), output excerpts, exit codes, times

### 1. Measure re-run at tip

```
$ date -u +%FT%TZ > start_measure.txt && timeout 900 python3 -I -B \
    /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev 1288285eed81395e6af7c279a173b117b2c2eaa3 > measure.stdout 2> measure.stderr; ec=$?; \
    date -u +%FT%TZ > end_measure.txt; echo "exit=$ec"
exit=0
```

- Start `2026-10-23T04:30:35Z`, end `2026-10-23T04:30:45Z` (10.1 s; REA runs per carrier completed within the counter's 300 s subprocess timeouts).
- `measure.stdout` (13 lines, sha256 `4360d9e51cf1e4d5e57718efad485d618c1339ca0d347e4b8978a242801aad05`):

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

- `measure.stderr`: empty (sha256 of empty = `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

### 2. Diff vs committed receipt

```
$ diff -u /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/after/c1-sqlite-positive-at-0007731e.txt \
    /fast/scratch/hyaku/kaidoku-r31/seats/w2/ReRunC1/measure.stdout; echo "diff_exit=$?"
--- .../after/c1-sqlite-positive-at-0007731e.txt	2026-10-23 01:25:50.355893678 -0300
+++ .../ReRunC1/measure.stdout	2026-10-23 01:30:45.668894354 -0300
@@ -11,4 +11,3 @@
 gpkg-multisurface	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
 gpkg-test-gpkg-nulls	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=64
 carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)
-exit=0
diff_exit=1
```

All 13 counter-emitted lines match byte-for-byte. The sole difference: the receipt has one extra trailing line `exit=0` after the target line, which the counter does not print (the counter's `measure()` prints only 13 lines; `sys.exit` happens after). This is the L1's recording convention, not a counter difference: the same trailing `exit=0` appears in the C2 receipt (`c2-sqlite-refusals-at-0007731e.txt`, last line `exit=0`), the freeze-integrity receipt (last line `exit=0`), and the pre-docs receipts (`c1-sqlite-positive-at-f368a101.txt` ends `... exit=1`, `c2-sqlite-refusals-at-f368a101.txt` ends `... exit=1`). [Observation]

### 3. Selftest

```
$ date -u +%FT%TZ > start_selftest.txt && timeout 900 python3 -I -B \
    /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py \
    --selftest > selftest.stdout 2> selftest.stderr; ec=$?; echo "exit=$ec"
exit=0
```

- Start/end `2026-10-23T04:30:35Z` (0.1 s). `selftest.stdout` (15 lines, sha256 `86edbf914778623dcc762f0da984ac715ccc17b8cc7204ef9ce714dfeb698a9b`): 14 cases (7 judge + 7 province), all `ok`, `selftest cases=14 failures=0`. Stderr empty.

### 4. No post-0007731e change to any file the counter reads

```
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <lane> diff --name-only \
    0007731e 1288285eed81395e6af7c279a173b117b2c2eaa3
.ufo/waves/round-29/claims.json
.ufo/waves/round-31/after/c1-sqlite-positive-at-0007731e.txt
.ufo/waves/round-31/after/c2-sqlite-refusals-at-0007731e.txt
.ufo/waves/round-31/after/freeze-integrity-at-0007731e.txt
LOG.md
SCORECARD.md
exit=0
```

Counter input set, from `tools/round-31/c1-sqlite-positive.py` source (read at lanes `#8240`): `corpus/evidence/round-31/c1/carriers.tsv` (PIN-checked vs `--rev`), `corpus/evidence/round-31/c1/envelopes/<id>.json` (committed_check, read from `--rev`), `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` (entry_ok), `PROVINCE.md` (province_ok, read from `--rev`), `.ufo/waves/round-31/claims.json` (only via `git log --diff-filter=A` for freeze_ct), the 12 carrier files at `/fast/scratch/hyaku/kaidoku-r31/carriers/<id>.<ext>` (sha256-PIN-checked), and `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` (version 6.5.0 + sha256 recorded). None of these is in the diff list above. The six changed files are records (LOG/SCORECARD/after receipts) and the round-29 claims pin (a docstring-only correction supersession entry), none of which the C1 counter reads. [Observation] [Inference: the counter's read set from source inspection is complete]

The changed files differ in content 0007731e → tip (LOG +10 lines, SCORECARD +27, round-29 claims.json +1 line, three after receipts added), and the tip commit `1288285e` includes those exact additions (verified via `git show --stat 840c01e` — the merge of the lint tree containing the same changes — and `git show <tip>:<file>`). The working tree matches tip for the six changed files (`git status --porcelain` lists them nowhere; only untracked w2-seat data). [Observation]

## Findings

### Severity 1 — none

### Severity 2 — none

### Severity 3 (nits)

1. **Committed receipt contains a line the counter cannot print.** `after/c1-sqlite-positive-at-0007731e.txt` ends with `exit=0`, which `c1-sqlite-positive.py` never prints (it prints 13 lines, then `sys.exit(0)`). The `exit=0` line is appended by the L1's recording convention, as in every other after receipt (C2, freeze-integrity, f368a101, both exit 1 and 0). Noise only; a naive `diff` of stdout against the receipt shows a false 1-line mismatch. No action needed beyond documentation.

## Verdicts per checked item

1. **C1 counter re-run at tip matches the committed receipt — HOLDS.** Exact counter command reproduced `exit=0`; all 12 carriers `P1-pass`; target line identical: `carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)`. `diff` of counter stdout vs receipt shows zero content difference (only the L1-appended `exit=0` trailer line, see nit 1). The committed envelope per carrier is equal to the live envelope in every field except `meta` (enforced inside the counter by `committed_check`, `strip_meta` full comparison; any mismatch would flip that carrier to `P1-fail` and drop `pass` below 12 — it did not).
2. **Selftest — HOLDS.** `selftest cases=14 failures=0`, exit 0.
3. **No post-0007731e commit changes a file the counter reads — HOLDS.** Only LOG.md, SCORECARD.md, .ufo/waves/round-29/claims.json (docstring-only supersession pin entry), and the three `after/*.txt` receipts changed; none is read by the counter. All counter inputs (carriers.tsv, envelopes, entry, PROVINCE.md, carrier files, rea-agents package) are unchanged between 0007731e and tip (and the carriers themselves are sha256-PIN-checked by the counter against the frozen list at `/fast/scratch/hyaku/kaidoku-r31/carriers/`).

## Residual risk / verification gaps

- The counter's REA invocation is `npx -y rea-agents@6.5.0 inspect-sqlite-database <path> --schema-scope database --format json --full-output`, cwd `/tmp`, and resists re-pinning to the same commit. The live REA behavior is pinned by the `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` version (6.5.0) + sha256 recorded in the runs table, and by the committed envelopes (any REA behavior drift would fail the full-envelope `committed_check`). I did not open REA's npm tarball; the 12/12 live match to the committed envelopes is the empirical check. [Inference]
- The lane's git object store is the only pin for the receipt blobs; I verified blob equality by reading the objects (`git show`), not by hashing from a fresh clone. [Inference] (Read-only git only, per bounds.)

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReRunC1/`)

| file | sha256 |
|---|---|
| measure.stdout | `4360d9e51cf1e4d5e57718efad485d618c1339ca0d347e4b8978a242801aad05` |
| measure.stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| selftest.stdout | `86edbf914778623dcc762f0da984ac715ccc17b8cc7204ef9ce714dfeb698a9b` |
| selftest.stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| start_measure.txt | `2f347c960f9525bbe9b4ca52c2024f08496b66ec385e7cb71fb2c694119f75c8` (2026-10-23T04:30:35Z) |
| end_measure.txt | `04e22877ae0170a172405f5bde285cc87f4985de18bd6149a0f417598ca13beb` (2026-10-23T04:30:45Z) |
| start_selftest.txt | `2f347c960f9525bbe9b4ca52c2024f08496b66ec385e7cb71fb2c694119f75c8` |
| end_selftest.txt | `2f347c960f9525bbe9b4ca52c2024f08496b66ec385e7cb71fb2c694119f75c8` |

`tmp/` dir created but unused. No tools installed (no installs needed; nothing beyond Python 3, git and npx/npm present — no tooling action taken).

## Bounds compliance

- No writes anywhere inside the lane except this report at `.ufo/waves/round-31/w2/ReRunC1.md` (the only lane path written; target path is inside the lane by contract). Read-only git only (log, diff, show, ls-tree, cat-file, rev-list, status). No `git`/`jj` writes anywhere. No REA outside the counter. No subagents. All commands under `timeout`. No process trees left running.
