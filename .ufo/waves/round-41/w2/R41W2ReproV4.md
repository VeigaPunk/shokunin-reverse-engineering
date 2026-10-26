# R41W2ReproV4 — V4 receipt reproduction (5491 nested rootfs)

**CONFIRMED.** The committed V4 after-receipt reproduces exactly from independently rebuilt
vendor bytes: 6349/6349 regular files at the same relative paths with the same sha256 and
size, 611 `unpublished-entry` gaps, 4 `MaliciousSymlinkRemoved` diagnostics at the same
paths, 1 `depth-limited`, same subject digest — and the removal set was **stable across one
committed and five independent REA runs (6/6 identical)**, so the plan's disclosed
iteration-order dependence did not manifest on this carrier. One non-scoring defect found:
`c1-run.sh` cannot write `run.json` for V4 (EPIPE of `MAX_ARG_STRLEN`), leaving the
flagship carrier's only evidence as `after.json` plus a raw shell error line.

Seat: R41W2ReproV4 (leaf). Lane `kaidoku-shokunin`; freeze `d764389e…`, measured
`e9a24d07…`. Nothing outside
`.ufo/waves/round-41/w2/{R41W2ReproV4.md,artifacts/R41W2ReproV4/}` was written; no VCS
mutation in the lane (fixtures only, inside `$S`); no tool installed or upgraded.

## What I attacked

The V4 half of R41-C1's after-receipt, from the bytes up, without reusing any committed
result as input:

1. vendor chain rebuilt with `fetch-vendor.py` at the **freeze** (image → member → nested
   `filesystem_core.squashfs`), pins re-checked by hand;
2. **five** fresh `rea-agents@6.5.0 extract-firmware --max-depth 1 --full-output` runs into
   fresh extraction roots (`unblob 26.6.4`, `sasquatch-v4be 4.5.1` on the child PATH);
3. comparison against `corpus/evidence/round-41/c1/V4/after.json` on every surface the
   claim names, using my own implementation of the exact-path rule (`cmp.py`, `verify.py`,
   `stability.py`; none reads `c1-counter.py`);
4. independent re-derivation of the frozen oracle (reader + second producer), so the receipt
   is checked against a table I validated myself;
5. the frozen counter scored against **my** receipt in a sandbox clone (no lane writes);
6. freeze-integrity spot check on the C1 frozen paths.

## Result — every compared surface

Committed `after.json` (sha256 `1efa815f…b20d60e`, 2,852,279 B; identical at `e9a24d07`,
at tip `7a24ff74` and in the worktree) vs run 1 / run 2 (`cmp-v4.json`):

| surface | committed | run1 | run2 | run3–5 |
|---|---|---|---|---|
| regular files (rel, sha256, size) | 6349 | 6349 | 6349 | 6349 |
| `unpublished-entry` gaps / entries | 611 / 611 | 611 / 611 | 611 / 611 | same |
| `MaliciousSymlinkRemoved` diagnostics | 4 | 4 | 4 | same |
| `depth-limited` gaps | 1 | 1 | 1 | same |
| handler set | `{squashfs_v4_be}` | same | same | same |
| subject digest | `ce27ebca…087f` | same | same | same |
| `evidence_id` | `ev_cb803e60…` | differs | differs | differs |

All five set comparisons (`files`, `unpublished`, `removals`, `gap_unpublished`,
`gap_other`) are **equal** for committed↔run1, committed↔run2 and run1↔run2; zero sha/size
mismatches on the intersection, zero gap-metadata and zero removal-target mismatches
(`cmp-v4.json`). `stability-v4.json`: one distinct projection digest (`bec248e9b190109a…`)
over all six receipts. `evidence_id` differs per run because it digests run-specific
parameters/paths — the counter's `evidence_id_ok` recomputes it, and it is `true` for all
six.

Removal set, identical in all six (path → target):

```
lib/libbroadbandcfg.so            -> /usr/share/ctlmgr/libbroadbandcfg.so.1.0.0
lib/libbroadbandcfg.so.1          -> /usr/share/ctlmgr/libbroadbandcfg.so.1.0.0
usr/www/avm/cgi-bin/system_status -> usr/www/cgi-bin/system_status
usr/www/avme/cgi-bin/system_status-> usr/www/cgi-bin/system_status
```

The 1-byte envelope-size difference run1↔run2 is `meta.duration` (`"10648ms"` vs
`"9376ms"`); the path-normalised structural diff (`canon-*.txt`) shows the committed
receipt and my runs differ in exactly 8 fields — `provider_blob_id`/`chunk.provider_id`,
the three `/raw_result/execution/args` scratch paths and the REA staging-dir token. That is
what a receipt of these bytes from this toolchain looks like; it is consistency evidence,
not proof of which process wrote the committed file (R40-CL2 stays open, as disclosed).

## Independent oracle check (my code, not the counter)

`verify-v4.json` — all six receipts pass, `ok: true`, zero failures:

* R1 every oracle regular file published at its exact `rel` with the same sha256 **and**
  size: 6349/6349, 0 missing, 0 extra, 0 mismatched;
* R2 no non-regular oracle row published as a file: 0;
* R3 symlink partition exact: 615 symlink rows = 611 `unpublished-entry` gaps + 4 removals,
  each row accounted **exactly once** (0 unaccounted, 0 double-accounted, 0 accounted rows
  that are not symlinks); the gap path set equals the `unpublished_entries` path set;
* R4 every removal resolves to a symlink row: 4/4;
* R5 structural gaps: at most one `depth-limited` (1), no `unknown-chunk-handler`, no other
  kind; the 401 directories and the 1 char device are invisible, as the gap rule allows;
* R6 subject digest == carrier pin.

Oracle provenance re-derived, not trusted (`oracle-repro.json`):

* the **frozen** `tools/round-41/sqfs-list.py` (sha256 `a8e633f5…`) re-run on the carrier
  reproduces the committed `oracle.tsv` (6349 rows) and `nonregular.tsv` (1017 rows:
  615 symlink, 401 dir, 1 char-device) **byte-identically** (`cmp` exit 0);
* a second, unrelated producer — `sasquatch-v4be -f -no-exit-code -n` (no `-be`) — agrees
  6349/6349 on rel+sha256+size, 0 missing, 0 extra, 0 mismatched.

Carrier identity measured straight off the bytes (`carrier-check.json`): magic `sqsh`,
major 4, `mod_time == bytes_used == size == 32,720,860` (the AVM marker), first metadata
block header `e807` = 2024 LE bytes (plausible) vs 59,399/26,631 BE (implausible), xz
compression (id 4), block size 65,536, `inode_count` 7367 = 6349 files + 1017 non-regular
+ 1 root — the staged-entry count the claim sets against REA's 10,000 budget.

## The frozen counter accepts an independently produced receipt

Sandbox clone of the lane at `e9a24d07`, V4 `after.json` replaced by my run 1
(sha256 `9e4b18be…`), fixture commit `85bfe86d…`, then the frozen counter with
`--rev 85bfe86d… --freeze d764389e…` (`score-myreceipt.json`):

`exit 0`, `met_target: true`, `carriers_matched: 4`, `frozen_path_changed: []`, V4
`matched: true` with `projection_ok: true` / `projection_diff: []`,
`oracle_hits 6349/6349`, `gaps_ok` note "612 gaps (1 structural), 4 removals, 0 silent, on
1017 non-regular entries", `receipt_fresh: true` (first add = the committed `e9a24d07`),
`run_provenance_ok: true` for **my** output directory. So the V4 bindings are not keyed to
the committed bytes' run-specific fields, and the claim's counter-time rerun clause passes
against a receipt produced by an unrelated seat.

Freeze integrity (independent of the counter): `git diff --name-only d764389e…e9a24d07`
over the C1 frozen paths is empty; the frozen harness is byte-identical at freeze and at
the measured revision (`c1-run.sh bdb97632…`).

## Defects

**D1 — `c1-run.sh` cannot produce `run.json` for V4 (real, size-driven, scoring-neutral).**
Committed log: `tools/round-41/c1-run.sh: line 547: /home/vgpnk/.local/bin/jq: Argument
list too long`. Causally complete account in `artifacts/…/harness-failure.md`: the `receipt`
assignment passes `--argjson summary "$summary"` where `$summary` is **146,561 bytes**
(compacted here from the committed receipt with the harness' own filter); Linux caps a
single argv string at `MAX_ARG_STRLEN = 32×PAGE_SIZE = 131,072` (probed: 130,000 ok,
131,072 → `errno 7`; reproduced from a script file with the identical message, exit 126).
Line 541 already moved `after.json` into place, `set -e` aborts at 547, `run.json` is never
written — so V4, the only carrier over the cap (V3 18,441 B, L3 1,479 B, L4 1,465 B), is
also the only one with no argv/toolchain/timing/envelope record. Disclosed in the commit
message of `5ca6941b`; the counter does not read `run.json`
(`run_provenance_ok = provenance_ok(parameters.output_directory)`), so no binding moves.
The residual risk is future: any receipt with ≳1,090 gap+unpublished rows [INFERENCE: ≈119 B/row] silently loses
`run.json`; a `--slurpfile`/`--rawfile` hand-off instead of `--argjson` removes the limit.

**D2 — `oracle-run.json` names the wrong reader (cosmetic).** V4's committed
`oracle-run.json` records `tools/round-40/sqfs-list.py` (sha256 `1079fa9b…`), while the
claim names the frozen `tools/round-41/sqfs-list.py` (`a8e633f5…`; 231 diff lines, all
in-memory/`--extract` additions). Re-running the frozen reader reproduces both tables
byte-identically, so the claim text overstates what its artifact shows, but the oracle is
sound.

**D3 — link-target representation is not comparable to the oracle (reviewer trap,
unscored).** REA's `unpublished_entries[].link_target` is the *resolved* target
(`dev/log`: `../var/tmp/log`), the oracle's `nonregular.tsv` detail column is the literal
stored target (`../tmp/log`, confirmed by `readlink` on the sasquatch extraction), and
removal targets are resolved one chain further
(`lib/libbroadbandcfg.so` → `/usr/share/ctlmgr/libbroadbandcfg.so.1.0.0`). 135 of 611
unpublished targets and 4/4 removal targets differ by representation only
(`link-targets.json`). No scored binding compares them; a reviewer diffing the two columns
will see a false alarm.

## Limits, calibration

* Attacked: V4 only (my seat), plus the oracle and reader it is scored against, plus the
  counter's V4 binding. Not attacked: V3/L3/L4 receipts, `c1-extra.py`'s landing-document
  bindings, any C2 item.
* Stability is conditional: five runs on this host, this filesystem and this pinned
  toolchain, all with `--max-depth 1`. The disclosed order-dependence is not disproved in
  general — only not observed here. The counter now binds the rerun to the same removal
  paths, which is what protects the claim if an order-sensitive host ever differs.
* What could have falsified and did not: a different removal set, one file with a different
  sha256/size, an unaccounted or double-accounted symlink row, a second `depth-limited`, a
  projection diff at scoring time, or a counter that refused my receipt.
* Vendor bytes were never copied: the carrier stays in scratch as
  `ce27ebca…b80f.bin` (sha256 cited); envelopes are kept gzipped
  (`run1/run2.envelope.json.gz`, 349 KB each; raw sha256s in `commands.txt`) and are
  rebuildable with the command in `commands.txt` §2. Scratch
  `/fast/scratch/hyaku/kaidoku-r41/R41W2ReproV4` was removed at the end of the seat.

## Evidence

`artifacts/R41W2ReproV4/`: `cmp-v4.json`, `stability-v4.json`, `verify-v4.json`,
`link-targets.json`, `carrier-check.json`, `oracle-repro.json`, `canon-committed-vs-run1.txt`,
`canon-run1-vs-run2.txt`, `harness-failure.md`, `commands.txt`, `score-myreceipt.json`
(+`.stdout`), `run1.envelope.json.gz`, `run2.envelope.json.gz`, and the four scripts used
(`cmp.py`, `verify.py`, `canon.py`, `stability.py`).

Report: .ufo/waves/round-41/w2/R41W2ReproV4.md
