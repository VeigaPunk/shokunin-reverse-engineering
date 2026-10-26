# R41C1DevCore — REA depth 1 on a genuine AVM-BE **rootfs** carrier (dev image 7430 07.31)

**Verdict: DEFECTS FOUND** — the extraction half of the hypothesis is confirmed (REA 6.5.0 `extract-firmware
--max-depth 1` publishes all 6 485 regular files of the nested AVM-BE rootfs at their exact paths, one
extract root, no budget overflow, 17.9 s), but the round-40 gap rule does **not** fit a rootfs carrier: four
symlinks are removed with a `MaliciousSymlinkRemoved` diagnostic and *no* gap, so the frozen model's
`required.symlink: true` fails, and the removal set is **iteration-order dependent**, so it cannot be frozen
as a fixed number. R41-C1's V4 carrier (and any rootfs-shaped carrier) needs the gap-rule amendment in §7
before the freeze. R41-C1's V3-shaped wrappers are unaffected (measured: 0 removals, 0 at-risk links).

Everything below was run on development inputs only: the public `FRITZ.Box_7430-07.31.image` (sha256
`3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4`, already burned in round 40), my own
carves of it, and two synthetic AVM-layout carriers I built. No reserved carrier (3490/5490/5491/7560,
L3, L4) was downloaded, opened, extracted, or read; no extractor ran on one.

Artifacts (all relative to this file's `artifacts/R41C1DevCore/`): receipts, oracle tables, probe outputs and
the three probe programs are listed in §12. The carriers themselves are **not** committed (vendor bytes):
`REBUILD-7430-carriers.sh` re-derives both from the public image with digest checks at every step.

---

## 1. Item and answer, clause by clause

| hypothesis clause | measured | verdict |
|---|---|---|
| REA `--max-depth 1` extracts a **full** AVM-BE rootfs (thousands of entries) through `squashfs_v4_be` | exit 0, handler `squashfs_v4_be`, no failed chunk, 6 485 regular files + 6 485 exact oracle hits, 17 967 ms | **confirmed** |
| without budget overflow | 6 824 staged entries of 10 000, 111 615 238 B of 268 435 456 B; hard failure measured at 10 150 entries | **confirmed** (with a margin rule, §7.4) |
| one unpublished-entry gap **per symlink** | 628 symlink rows → 624 gaps; 4 removals carry a diagnostic and **no** gap | **falsified** |
| … per **special**: devices invisible | 1 char device (`dev/led` 247:0) is absent from the receipt entirely — no file, no unpublished entry, no gap | **confirmed** |
| the round-40 gap rule fits a rootfs carrier | the round-40 counter's own `gap_check` returns `(False, "required gap absent on ['lib/libbroadbandcfg.so', 'lib/libbroadbandcfg.so.1', 'usr/www/avm/cgi-bin/system_status', 'usr/www/avme/cgi-bin/system_status']")` | **falsified** |
| published paths sit under one `<name>_extract/` root | one root, `firmware.bin_extract`; 0 oracle rows published at another depth | **confirmed** |
| gap kinds limited to unpublished-entry + depth-limited | 624 `unpublished-entry` (all symlinks) + 1 structural `depth-limited` at `$output/firmware.bin_extract`; zero `unknown-chunk-handler`, zero `missing-extractor-dependency`, zero `extractor-failure`; every gap has `dependencies: []` | **confirmed** |

The two failures are the same underlying fact (§5–§6): unblob 26.6.4 deletes a class of symlink instead of
leaving it unpublished, and *which* members of that class it deletes depends on directory iteration order.

## 2. Commands (exact, with exit codes)

Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C1DevCore`; downloads, unblob, extractions, fixtures and the
synthetic carriers all live there. The rootfs REA runs were invoked without `TMPDIR` exported in their own
shell, so REA staged them in `/tmp/rea-firmware-<rand>` (~137 MB, removed at exit); the last run (§8.5) exported
`TMPDIR=$S/rea-tmp` and staged there instead.
`REA` below is `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1` with
`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`, run from `$S` (package root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`).

1. download the image → sha256 matches the pinned `3dd6…ecf4`, 28 856 320 B — exit 0.
2. `unblob -e . 7430.image` (default depth) → exit 0; `var/tmp/filesystem.image` (AVM wrapper) and, under it,
   `0-25825280.squashfs_v4_be_extract/filesystem_core.squashfs` (the rootfs member).
3. carve each to its `bytes_used` with `head -c` (`25824314` wrapper, `25194540` rootfs) → hashes in §3.
4. `sqfs-list.py --layout avm --files … --nonregular … --inspect …` on both carves → exit 0 (3.1 s).
5. **REA run 1** on the rootfs carve → `{"ok":true}`, exit 0, `meta.duration 17967ms`,
   `evidence_id ev_9b09a8336d967e0259ffd3511e7e65c299ec657ff40d3688ffbeae808a6a1d83`.
6. **REA rerun** into a fresh output dir → exit 0, `21359ms`, `ev_384bf7d2af137b4ab972884b1e3b0fb1cc8895a4e880834c841562e3df1c522b`;
   `c1-counter.projection()` at profiles `core`, `plus-mime`, `plus-extractor` compares **equal**
   (`projection_diff` → `True, []` for all three), `published_bytes` 111 615 238 in both.
7. **REA on the wrapper carve** (V3 shape) → exit 0, `2311ms`, 8/8 files, 90/90 links gapped, 0 removals.
8. **REA on a synthetic 9 951-entry AVM-genuine carrier** → exit 0 (budget pass case).
9. **REA on a synthetic 10 150-entry AVM-genuine carrier** → exit 1,
   `{"code":"unreadable_output", "details":{"operation":"extract_firmware","reason":"Staging entry budget exceeded (10000)"}}`
   (budget fail case).
10. `sasquatch-v4be -be -f -d sxbe -n -no-xattrs carrier/7430-core.sqsh` → exit 1,
    `read_id_table: failed to read id table block / FATAL ERROR: File system corruption detected`
    (negative control: the layout is not standard BE); the same binary **without** `-be` extracts
    6 485 files / 628 symlinks / 409 dirs.
11. `devcore-probe.py`, `removal-predict.py`, `symlink-order-probe.py` (this seat's tools) — §12.

## 3. Carrier provenance and layout evidence

| step | value |
|---|---|
| image | `FRITZ.Box_7430-07.31.image`, sha256 `3dd6940c…a6ecf4`, 28 856 320 B |
| wrapper member | `./var/tmp/filesystem.image`, sha256 `b919a6a218a57c8bf69e64baeab28bd6cb4c77bfd1fe2e8e4c1880edb9342c6c`, 25 825 288 B, `bytes_used 25824314` |
| wrapper carve | `c88ba9faa038e73ed1a3ca264be9b1da89aae51cf800a9b7605bd865c06c9c5a`, 25 824 314 B |
| rootfs member (nested) | `filesystem_core.squashfs`, sha256 `14dc8e550482c7608943fb1adad8960a989d3da16e7444e1fdf9a0652fb08329`, 25 198 592 B |
| **rootfs carve (carrier)** | `1588129540dfdcce09cb8304f724a66fd50aa1eb0bc6481cc6a2246670aa628f`, 25 194 540 B |

Superblocks (both big-endian `sqsh`, v4.0, `mkfs_time == bytes_used`, xz id 4, block_size 65 536,
metadata length header **little-endian**):

* rootfs: `inodes 7524`, `bytes_used 25194540`, `mkfs_time 25194540`, marker **true**;
  `block_length_signal: layout-avm`, data-block field `00005428` decodes structurally to 21 544
  (swapped: 5 505 024, implausible); fragment entry structural 14 036 (swapped 3 560 308 736). 4 052 trailing
  bytes beyond `bytes_used` are dropped by the carve. Source image sha → wrapper-member sha → carrier sha is
  the R40-CL6 chain, each link digest-checked by `REBUILD-7430-carriers.sh`.
* wrapper: `inodes 109`, `bytes_used 25824314`, marker **true**; 8 regular files, 9 dirs, 90 in-tree
  symlinks, 1 char device, 0 escaping.

Rootfs oracle (`sqfs-list.py --layout avm`): 6 485 regular files totalling **111 615 238 B**, 409 dirs,
628 symlinks, 1 char device, 0 escaping symlinks; the whole table + hash pass takes 3.1 s.

## 4. What REA published (rootfs carrier, depth 1)

Single chunk `squashfs_v4_be`, `extraction_failed: false`, `coverage: partial`, one derivation
`$input → $output/firmware.bin_extract`, single extract root **`firmware.bin_extract`**. The root name is not
the carrier's: REA stages the input as `/tmp/rea-firmware-<rand>/firmware.bin`, so the `<name>_extract`
component is always `firmware.bin_extract` (`raw_result.execution.args`:
`unblob --process-num 1 --depth 1 --randomness-depth 0 … /tmp/rea-firmware-rte1JZ/firmware.bin`).

* 6 485 published regular files = 6 485 oracle rows; **0 absent, 0 sha mismatch, 0 published at another
  depth, 0 extra files** (exact match after dropping the leading `_extract` root).
* 0 published paths collide with a non-regular oracle row (no materialised symlink/device).
* `unpublished_entries`: 624, all `symlink`.
* `extraction_gaps`: 625 — 624 `unpublished-entry` on those 624 symlinks (exact paths) and 1 structural
  `depth-limited` with `relative_path: null` at `$output/firmware.bin_extract`;
  `depth_limited_paths: ['$output/firmware.bin_extract']`.
* Invisible non-regular rows (`invisible_nonregular_count 414`): 409 dirs, the char device, and 4 symlinks
  (§5). Directories are expected (71 of them hold no published descendant, so REA's regular-file-only tree
  has no such path: `dev`, `dev/pts`, `proc`, `sys`, `usr/www/avm/cgi-bin`, …). `published_bytes`
  111 615 238 = the oracle's total.
* Devices: unsquashfs cannot mknod unprivileged — direct-extraction log line
  `create_inode: could not create character device sx/dev/led, because you're not superuser!`, `created 0 devices`.
  The receipt mentions `dev/led` nowhere: not published, not an unpublished entry, **no gap**. The round-40
  rule's `allowed: {char-device: []}`, `required: {char-device: false}` describes this correctly and needs no
  change; a *regression* in this area is undetectable from the receipt, which is worth stating in the claim
  prose (the oracle-hit rule still catches any real regular-file loss).
* Wrapper carrier (V3 shape) for contrast: 8/8 files, 90/90 links each with an exact `unpublished-entry` gap,
  1 structural `depth-limited`, **0 removals**, **0 statically at-risk links**, 14 staged entries,
  26 828 000 B, 2 311 ms; executed against the frozen round-40 model its `gap_check` returns
  `(True, '91 gaps (1 structural) on 100 non-regular entries')` — the same model, same code, opposite verdict
  on the two carrier shapes. Depth-1 truncation always yields exactly one `depth-limited` gap at the extract
  root — measured on all three carriers, so `structural: {depth-limited: 1}` is right (and exact, not a
  ceiling) for depth 1.

## 5. Defect — four symlinks are removed with a diagnostic and **no** gap

```
MaliciousSymlinkRemoved  lib/libbroadbandcfg.so              → /usr/share/ctlmgr/libbroadbandcfg.so.1.0.0
MaliciousSymlinkRemoved  lib/libbroadbandcfg.so.1            → /usr/share/ctlmgr/libbroadbandcfg.so.1.0.0
MaliciousSymlinkRemoved  usr/www/avm/cgi-bin/system_status   → /usr/www/cgi-bin/system_status
MaliciousSymlinkRemoved  usr/www/avme/cgi-bin/system_status  → /usr/www/cgi-bin/system_status
```

Each is an oracle `symlink` row with a non-empty target; none is published as a file; none has a gap; none is
listed as an unpublished entry. So `required.symlink: true` in `.ufo/waves/round-40/c1/gap-rule.json` cannot
be satisfied by a real AVM rootfs — proven by executing the frozen counter's own helper on the receipt:

```
>>> c1-counter.gap_check(nr['extraction_gaps'], nonregular_rows, round40_rule)
(False, "required gap absent on ['lib/libbroadbandcfg.so', 'lib/libbroadbandcfg.so.1',
                                 'usr/www/avm/cgi-bin/system_status', 'usr/www/avme/cgi-bin/system_status']")
```

Mechanism (unblob 26.6.4 `extractor.fix_symlink` + `file_utils.is_safe_path`, read in
`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/extractor.py:47-90`):

* the first hop of an **absolute** target is re-rooted at the extraction root
  (`Path(target.as_posix().lstrip("/"))` + `basedir.joinpath(...)`), so a one-hop absolute link stays safe and
  is rewritten to a portable relative link;
* but a **relative** target is resolved with `path.resolve()`, and a later hop whose target is absolute is
  resolved from the **host** root (`/usr/share/ctlmgr/…`, `/usr/bin/system_status`), so the resolved path
  leaves the extraction root, `is_safe_path` is false, and the link is unlinked with a report;
* an **empty** target is unlinked with **no report at all** (`if not raw_target: path.unlink(); return path`).
  This image has no empty-target link; a lane-built carrier that adds one would lose the link with *no*
  receipt evidence whatsoever.

`removal-predict.py` turns this into a static, image-only predicate: a link is **at risk** iff its target
chain, with the first absolute hop re-rooted, meets an absolute target at hop ≥2 (or is empty). Measured: 6
at-risk links of 628, of which unblob removed 4 (the receipt's diagnostics) and kept 2
(`usr/www/{avm,avme}/html/flash.html`, whose `../flash.html` hop resolves through `usr/www/*/flash.html →
/var/flash.html`, and which survives only because that intermediate link was rewritten first).

## 6. The removal set is iteration-order dependent — do not freeze it as a number

`symlink-order-probe.py` transcribes `fix_extracted_directory`/`fix_symlink`/`is_safe_path` verbatim and
applies it to three copies of a plain `sasquatch-v4be` extraction of the same bytes, varying only the
`iterdir()` order:

| order | removed | set |
|---|---|---|
| natural (`os.listdir`) | 4 | exactly the receipt's four |
| sorted | 4 | exactly the receipt's four |
| reverse | **3** | `usr/www/avm/html/flash.html`, `usr/www/avme/html/flash.html`, `usr/www/kids/html` — **neither cgi-bin link** |

In reverse order the `html/` directory is visited before `flash.html`, so `../flash.html` still resolves
through an absolute link and is removed; in natural order `flash.html` is rewritten first and both `html/`
links survive. Consequence for the freeze:

* the *candidate* set is image-determined (6), the *actual* set is extractor-and-order-determined (4 here,
  3 there, and on another filesystem even a different partition of the same 6);
* a claim clause pinning "4 removals" or "these 4 links" is flaky by construction;
* what is stable and falsifiable is the **partition**: every oracle symlink row is either an
  `unpublished-entry` gap at its exact path or a `MaliciousSymlinkRemoved` diagnostic at its exact path,
  never both, never neither, and every removal diagnostic lands on a symlink row (§7).
  Measured partition: 624 + 4 = 628, exactly.

## 7. Gap-rule changes a rootfs carrier needs (smallest safe correction)

### 7.1 Rule data — add a third, extractor-determined family

```json
{
  "claim": "R41-C1",
  "allowed": {
    "symlink": ["unpublished-entry"],
    "char-device": [], "block-device": [],
    "fifo": ["unpublished-entry"], "socket": ["unpublished-entry"],
    "dir": []
  },
  "required": { "symlink": true, "char-device": false, "block-device": false,
                "fifo": false, "socket": false, "dir": false },
  "removed": {
    "diagnostic": "MaliciousSymlinkRemoved",
    "kinds": ["symlink"],
    "disposition": "exclusive",
    "silent": { "symlink": ["empty-target"] }
  },
  "structural": { "depth-limited": 1, "unknown-chunk-handler": 0 }
}
```

Semantics the counter must implement (three clauses, all data-driven):

1. **disposition** — for every non-regular row whose kind is `required`, exactly one of
   {an allowed path-resolved gap at its exact path, a removal diagnostic at its exact path} exists.
   `required.symlink` keeps its meaning ("every symlink is accounted for"), it just admits two dispositions.
2. **removal binding** — every `MaliciousSymlinkRemoved` diagnostic must resolve (exact path) to a
   non-regular row of a listed kind; a diagnostic on a path that is not such a row fails the carrier
   (prevents an extractor from quietly deleting a *directory* of files under cover of the allowance).
   A row may not be both gapped and removed.
3. **silent removals** — a row whose kind/detail is listed under `silent` (empty-target symlinks, which unblob
   deletes without any report) is admitted with **no** receipt record, but the counter must then also require
   that the *count* of such rows in the oracle equals the count of unaccounted rows (§7.2). If the L3/L4
   generators simply never emit an empty target (recommended), keep this list empty and the clause inert.

The rootfs's measured numbers satisfy this model: 624 gap / 4 removal / 0 silent / 1 structural.

### 7.2 Counter port (round-41 `c1-counter.py`)

* keep the R40-CL1 exact-match fix and extend `extract_rel` (§8.1) for removal diagnostics;
* `gap_check` → `disposition_check(gaps, removals, nonreg, model)` implementing 7.1.1–7.1.3;
* fail a carrier on any row that is neither gapped nor removed (that is the round-40 failure, now diagnosable
  per path), and on any removal that resolves to no row.

### 7.3 Projection (rerun binding)

`c1-counter.projection()` currently projects `diagnostics` as *typenames only*
(`sorted((d['report']['__typename__'] …))`). With removal diagnostics admitted, a rerun that removed a
**different** symlink would still match. Project them as `[__typename__, rel_path]` (rel path via the same
`extract_rel`) so the rerun binding covers *which* links disappeared, and keep the R40-CL2 note in mind: the
projection is a consistency check, not a provenance proof.

### 7.4 Budget clause for V4

Measured boundary (code at `dist/cli-runtime/cli.js:13992-14030`: `count` per directory entry, `maxEntries`
default `1e4` in `cutterToolContracts-TZH9EHr5.js:1763`; bytes are regular-file sizes, default 256 MiB):

| carrier | staged entries | bytes | outcome |
|---|---|---|---|
| rootfs 7430 (real) | 6 824 of 10 000 | 111 615 238 of 268 435 456 | pass, 17.9 s |
| wrapper 7430 (real) | 14 | 26 828 000 | pass, 2.3 s |
| synthetic 9 900 files + 51 dirs | 9 951 | 0 | pass |
| synthetic 10 098 files + 52 dirs | 10 150 | 0 | **fail**: `unreadable_output` / `Staging entry budget exceeded (10000)`, `retryable: false` |

So `max_output_files` is a hard, non-retryable ceiling at 10 000 entries: a rootfs whose oracle has more than
~10 000 (files + dirs) staged entries cannot be a C1 carrier at all, and the counter should therefore
pre-check the oracle's row counts against the constants *before* running REA (cheap, needs only the frozen
oracle table, no extractor). Recommendation for the draft's V4: the freeze must record the 5491 rootfs's
`sqfs-list` file+dir count (a reader, no extraction) and keep the wrapper fallback if it exceeds ~9 500
entries — I could not measure it (reserved carrier) **[INFERENCE]** that the 5491 rootfs is larger than
7430's 7 523-entry tree.

## 8. Other traps for the R41-C1 port

1. **`extract_rel` is not reusable for diagnostics.** The R40-CL1 prototype strips the leading component only
   when it ends in `_extract`. Gap and unpublished paths are `$output/firmware.bin_extract/…`, but a removal
   diagnostic carries the **host absolute** path
   `/tmp/rea-firmware-<rand>/extracted/firmware.bin_extract/<rel>`. A verbatim port produced four bogus
   "unpredicted removal" rows in my first pass (`tmp/rea-firmware-rte1JZ/extracted/firmware.bin_extract/…`).
   The port must locate the first `_extract` component and take the remainder (`removal-predict.py:rel_of`).
2. **`link_target` is rewritten, not the image target.** 484 of 624 unpublished entries match the oracle's
   detail column; **140 differ**, because unblob rewrites every kept link to the *resolved* target, relative to
   the link's parent (`bin/supportdata_argo.dpm`: image `/bin/supportdata.dpm` → receipt `supportdata.dpm`;
   `dev/log`: image `../tmp/log` → receipt `../var/tmp/log`, the `tmp → ./var/tmp` link collapsed).
   Do not bind `link_target` to the oracle target; if a target binding is wanted it must chain-resolve
   image-side, which is extra machinery the draft does not ask for.
3. **`mime_type` is null on every file** at depth 1 (no per-file scan happens before the depth limit), exactly
   as in the round-40 receipts (`V1/V2/L1` all `None`). `plus-extractor` therefore compares
   path/sha/size + null mime/hash columns, engine, `published_bytes`, `coverage`, `derivations` — weaker than
   the profile's name suggests, but *equal across the two runs* (verified) and equal in strength to the
   round-40 receipts, so the rerun binding is neither better nor worse for a rootfs carrier.
4. **Extract-root name is REA's, not the carrier's** (`firmware.bin_extract` for every carrier). Any
   round-41 selftest that hardcodes `<carrier filename>_extract` will be wrong; the `<name>_extract` strip
   rule is the right one.
5. **Operational footprint**: REA stages the run under `$TMPDIR/rea-firmware-<rand>` — verified by exporting
   `TMPDIR` for one run and reading `raw_result.execution.args`
   (`…/rea-tmp/rea-firmware-81t5rs/{report.json,unblob.log,extracted}`); when `TMPDIR` is *not* exported the
   stage falls back to `/tmp/rea-firmware-<rand>`, which is what my measured rootfs runs did. The stage is
   ~137 MB for this rootfs (111.6 MB published + the 25.2 MB carve) and is removed at exit. Wall clock 17.9 s
   per run, so a counter rerun on a rootfs carrier costs ~2×18 s plus the oracle hash pass — acceptable, but
   an order of magnitude above the wrapper carriers (2.3 s); the counter's `--rea-timeout` (default 900 s) has
   ample margin, and the counter should export `TMPDIR` into its scratch so a rootfs rerun does not stage
   137 MB in `/tmp`.
6. **L3/L4 fixture hygiene** (lane-built, not measured here): keep image path components from ending in
   `_extract` (the exact-match strip would treat such a directory as a chunk root) and do not build
   empty-target symlinks unless §7.1.3 `silent` is populated.

## 9. Effect on the draft (R41-C1)

* **V3 (vendor wrapper)** — unaffected in shape: measured wrapper carrier gives 8/8 files, 90/90 links gapped,
  0 removals, 0 at-risk links, 14 entries. No change needed, and the round-40 rule would score it green.
  (The 5490 wrapper's own link graph is unmeasured here — reserved — but §7.1 is compatible either way.)
* **V4 (5491 nested rootfs)** — a rootfs carrier is feasible *only* with §7.1–§7.3 in the freeze, and the
  freeze must pin the carrier choice on the measured entry count (§7.4). As drafted ("if it is AVM-BE and
  fits REA's entry budget at depth 1"), the "fits" test is satisfiable only by a reader pass on the reserved
  image, which this seat may not run — the L1 (or whoever holds the V4 item) must do it before freezing the
  carrier pin.
* **L3/L4 (lane-built xz/gzip, both-direction nested collisions)** — unaffected by everything above *except*
  §8.1, §8.6: the exact-path port is correct for them (measured 0 suffix collisions on the real rootfs, so the
  R40-CL1 fix is a no-op here and the collision fixtures are what actually exercise it).
* **Kill rule / controls** — CTL-C1-0 (do-nothing) and the suffix-mutant are unaffected. The new defect adds a
  control the draft should carry: a receipt whose four removal diagnostics are deleted while the symlinks stay
  absent must fail (that is `disposition_check` §7.1.1), and a receipt whose diagnostics point at a
  *non-symlink* row must fail (§7.1.2).

## 10. Not measured / limits

* Reserved carriers were not opened (3490/5490/5491/7560, L3, L4): the V3 wrapper's real link graph, the V4
  rootfs entry count, and every vendor-byte-dependent number for those pins are unmeasured by this seat.
* No fifo, socket, block device, symlink loop, or empty-target link exists in this image
  (`special_kinds: {char-device: 1}`; 0 escaping links), so those classes are code-read only; the `fifo` and
  `socket` rows of the round-40 rule are untested **[INFERENCE]**: unblob leaves a fifo uncreated like a
  device (unsquashfs `mkfifo` succeeds unprivileged, so it may instead appear as an unreported special in the
  extraction tree — this needs one fixture before the rule is trusted for a vendor rootfs that has one).
* Depth ≥2 behaviour on a rootfs carrier (nested chunks inside the rootfs — `var.tar` is a real 30 720 B tar
  member) was not measured: the claim is depth 1.
* The 7430 rootfs is one vendor build; a second build with a different symlink topology could show a
  different at-risk count (2 wrappers/rootfs measured would cost another 18 s each on a dev image — the dev
  set is exhausted for rootfs images inside the allowed list).

## 11. Tooling record

No tool was installed, upgraded, moved or removed, and nothing was written into any PATH directory. REA
resolved from the existing npx cache
(`rea-agents@6.5.0`, package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`); unblob
26.6.4 at `/home/vgpnk/.local/share/uv/tools/unblob` (sha256 `0ce7b624…1d09` as recorded in the receipt
`engine.executable_sha256`); `sasquatch-v4be` 4.5.1 `/home/vgpnk/.local/bin/sasquatch-v4be` used unmodified
(and used by unblob, not by me, for the REA runs). No pacman transaction was attempted. Scratch
`/fast/scratch/hyaku/kaidoku-r41/R41C1DevCore` was used for every download, extraction and fixture; it holds
no lane content and is removed at the end of the seat.

## 12. Artifact index (`artifacts/R41C1DevCore/`)

| file | what |
|---|---|
| `REBUILD-7430-carriers.sh` | re-derives both dev carriers from the public image, digest-checked (no vendor bytes committed) |
| `rea-7430-core-after.json` | REA after-receipt, rootfs carrier, run 1 (3 010 488 B, `ev_9b09…1d83`) |
| `rea-7430-core-after-rerun.json` | same bytes, fresh output dir (3 016 975 B, `ev_384b…c522b`); projections equal |
| `rea-7430-wrapper-after.json` | REA after-receipt, wrapper carrier (`ev_a2e0c9680e0e2883cd3b53dcbf36fcac9a2231f63f2f52c5bd0cc72208c8c56b`) |
| `rea-7430-wrapper-after-tmpdir.json` | the same wrapper run with `TMPDIR` exported — the receipt's `execution.args` show the stage under `$TMPDIR` (§8.5) |
| `rea-budget-over.json` | the 10 150-entry budget failure (`Staging entry budget exceeded (10000)`) |
| `budget-pass-9951.sqsh` | synthetic AVM-genuine xz carrier, 9 951 staged entries — the budget **pass** case (`7d68265152e7238e033dc4dbb29ec67b2e2aed4ce9a4b8994108a9937d62369a`) |
| `budget-fail-10150.sqsh` | synthetic AVM-genuine xz carrier, 10 150 staged entries — the budget **fail** case (`807f47571b9a623df1d81edd35913dcb0bbaed05609627f87c9ec35dda026b82`) |
| `budget-probe-pass.json`, `budget-carriers.sha256` | pass-case receipt summary and the two synthetic carrier digests; both carriers are rebuilt by `python3 tools/round-40/gen-squashfs.py --endian avm-genuine --comp xz TREE OUT` over 50/51 dirs of 198 empty `f%03d` files |
| `inspect-7430-core.json`, `oracle-7430-core-files.tsv`, `oracle-7430-core-nonregular.tsv` | AVM-layout inspect + independent oracle for the rootfs carve |
| `inspect-7430-wrapper.json`, `oracle-7430-wrapper-files.tsv`, `oracle-7430-wrapper-nonregular.tsv` | same for the wrapper carve |
| `probe-7430-core.json`, `probe-7430-wrapper.json`, `probe-bigtree.json` | `devcore-probe.py` summaries (exact match, gap histogram, invisibles, budget) |
| `removal-predict-7430-core.json`, `removal-predict-7430-wrapper.json` | at-risk set vs receipt partition |
| `symlink-order-{natural,sorted,reverse}.json` | the order-dependence experiment (§6) |
| `devcore-probe.py` | exact-path coverage + gap histogram + staged-budget probe over one receipt |
| `removal-predict.py` | static at-risk predicate + disposition partition check |
| `symlink-order-probe.py` | faithful transcription of unblob's symlink fixer under a chosen iteration order |
