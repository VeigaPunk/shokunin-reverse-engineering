# R39W2ReproK5 — provenance attack on the committed R39-C1 K5 after-receipt

**Verdict: CONFIRMED** — three independent REA after-runs on a pin-verified copy of the K5 carrier
reproduce every semantic field of `corpus/evidence/round-39/c1/K5/after.json`; a run made with the
frozen basename reproduces the whole receipt document with **0 residual diffs** after normalising
only run-local values (scratch paths, REA temp dir, blob ids, evidence id, meta duration). The
sasquatch oracle check is file-for-file exact, `run.json` is internally consistent on 50/50
mechanical checks (including a byte-exact reconstruction of the recorded envelope from the
committed receipt bytes), the stored `evidence_id` recomputes under the rea-agents 6.5.0 rule, and
the committed artifacts are byte-identical to the original run artifacts that still sit in l1
scratch with an mtime 82 s before the receipt commit. No falsification found.

Seat scope: carrier K5 only (`corpus/evidence/round-39/c1/K5/carrier.sqsh`, pin
`5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228`, 26 813 bytes). Freeze
`8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` (2026-10-26T14:12:51-03:00 = 17:12:51Z), receipt first
added in `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` (14:18:32-03:00 = 17:18:32Z), lane HEAD
`e40a25df3987d881513de581112d2dad30605673`.

## 1. Carrier pin, freeze provenance, carrier identity

| check | command | result |
|---|---|---|
| pin | `cp …/K5/carrier.sqsh $S/x; sha256sum $S/x …/K5/carrier.sqsh` | both `5999eafc…d00b228`; `stat -c %s` = `26813` = frozen `size_bytes` |
| oracle / symlink table pins | `sha256sum …/K5/oracle.tsv …/K5/symlinks.tsv` | `651cb7e3…5fc2d7` (10 rows), `9d7c1b6a…ffea2f3` (3 rows) = frozen `oracle_sha256` / `symlinks_sha256` |
| pin at freeze | `git rev-parse 8fcda41:…/c1/K5/{carrier.sqsh,oracle.tsv,symlinks.tsv}` vs `HEAD:…` | identical blobs `ed7e62c2…`, `50406e44…`, `1407d17d…`; all three files are **first added by the freeze commit** and unchanged since |
| manifest immutability | `git rev-parse 8fcda41:.ufo/waves/round-39/c1/carriers.json HEAD:…` | both `061de280b44ab794a3d00b9f9e8dd585ee5a99e0` |
| pre-freeze artifact bytes | `sha256sum .ufo/waves/round-39/w1/artifacts/R39C1CarrierK5/carrier.sqsh` | `5999eafc…d00b228`, same git blob `ed7e62c2…` → the w1 build artifact and the committed carrier are the same bytes |
| BE v4 / no-pad, own superblock parse (no unsquashfs, no REA) | python `struct.unpack('>…')` on bytes 0–63 | `magic=b'sqsh' 0x73717368, s_major=4, s_minor=0, compression=1, block_size=4096, block_log=12, inodes=24, fragments=0, mkfs_time=1700000000, no_ids=1, root_inode=814, bytes_used=26813 = file size (no padding), id_table=26805, xattr=unused` |
| oracle⇄carrier agreement, strongest form | rebuild the tree from the sasquatch extraction (10 files + 3 links) and run both writer copies | `tools/round-39/gen-squashfs.py` (`f535e60e…`, blob `d74bb456…` at freeze and HEAD) → `5999eafc…`; w1 artifact writer (`833a40a9…`) → `5999eafc…`; `cmp` byte-identical both times |

The last row is the load-bearing one: the frozen `oracle.tsv` + `symlinks.tsv` + directory shape are
a *complete* description of the carrier — nothing else is inside it (24 inodes = 11 dirs + 10 files +
3 links), so the oracle cannot be a partial or shifted view of the image, and the carrier is exactly
the documented writer's output (not a hand-edited image).

Fixture provenance is corroborated, not re-derived: `.ufo/waves/round-39/w1/R39C1CarrierK5.md` §1
records the writer `833a40a9…` and the pin, and its §6 (Determinism, `determinism.txt`) shows three
builds to the same digest — matches my rebuild. [INFERENCE] The K5 source tree itself was not
retained, so "the tree that was originally fed to the writer" is verified only through the oracle it
produced (byte-identical rebuild), not through an independent copy of the tree.

## 2. Independent REA after-runs

Three runs, each into a **fresh** outdir, each from `$S/scratch` so `unblob.log` never lands in the
lane. Freshness is not assumed: repeating a run against an existing output directory exits 1 with
`{"ok":false,"error":{"code":"execution_failure",…,"retryable":false}}`
(`rea-refuses-existing-outdir.txt`), so an exit-0 run at a named outdir proves that outdir did not
exist when it started — the same argument applies to the recorded l1 run.

```
cd $S/scratch && REA_UNBLOB_COMMAND=$HOME/.local/share/uv/tools/unblob/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  $S/<carrier copy> $S/scratch/extract{,2,3} > out{,2,3}.json 2> out{,2,3}.err
```

| run | input | outdir | exit | envelope written | last write (local) | stderr |
|---|---|---|---|---|---|---|
| 1 | `$S/x` | `$S/scratch/extract` | 0 | 31 266 B, sha `e8dfe67a…e30617` | 14:27:47.46 | 0 B |
| 2 | `$S/x` | `$S/scratch/extract2` | 0 | 31 278 B, sha `7ea51640…440b52c4` | 14:30:47.25 | 0 B |
| 3 | `$S/carrier.sqsh` (frozen basename) | `$S/scratch/extract3` | 0 | 31 311 B, sha `987afcd5…107e6be7` | 14:34:17.65 | 0 B |

`--format json` envelope → `data` is the receipt payload. Comparison result
(`compare.py`, artifacts `compare-run{1,2,3}.txt`; normalises only REA temp dir, scratch paths,
`*blob_id`/`provider_id`/`id` blob ids, `evidence_id`, `meta.duration`):

| comparison | residual diffs |
|---|---|
| run 1 vs committed `after.json` | 1 — `/subject/name` (`x` vs `carrier.sqsh`, my copy's filename) |
| run 2 vs committed `after.json` | 1 — same field |
| run 3 vs committed `after.json` | **0** |

The demanded semantic fields, identical in all three re-runs and in the receipt
(`k5-semantic-compare.txt`):

| field | value (receipt = re-runs) |
|---|---|
| `chunks[].handler` | `["squashfs_v4_be"]` |
| `chunks[].extraction_failed` | `[false]` |
| `files` (10; relpath suffix, sha256, size, mime) | `README.txt f649d29a… 148 text/plain`, `config/app.conf 1a64be63… 54`, `empty.flag e3b0c442… 0 inode/x-empty`, `notes with space.txt 8d68ae9e… 34`, `usr/share/demo/assets/icons/アイコン.txt f48693f9… 37`, `usr/share/demo/assets/manifest.json 5dd83cc1… 58 application/json`, `usr/share/demo/notes.txt 4664d813… 30`, `usr/share/opt/blob.bin 4336d983… 5000`, `var/lib/state.db a9d330f2… 20000`, `var/log/last.log 12afa793… 18` |
| `extraction_gaps` (kind, relative_path) | `[("unpublished-entry","…/usr/share/demo/link-blob"), ("unpublished-entry","…/usr/share/demo/link-notes")]` — exactly the two in-tree symlinks, no other gap |
| `unpublished_entries` (relative_path, link_target) | `("…/link-blob","../opt/blob.bin")`, `("…/link-notes","notes.txt")` |
| `diagnostics[].report.__typename__` | `{"MaliciousSymlinkRemoved"}` — `link …/usr/share/demo/escape`, `target <staging>/extracted/etc/shadow` (the escaping link; no publish, no gap) |
| `coverage` / `published_bytes` / `depth_limited_paths` | `partial` / `25379` / `[]` (25379 = Σ oracle sizes) |
| `subject.digest.sha256`, `selection.sha256` | `5999eafc…d00b228` = the frozen pin |
| `engine`, `provider` | `unblob 26.6.4`, `executable_sha256 0ce7b624…` |

Content-level check, not just listing-level: the 10 published files on disk rehash to the oracle
values (`sha256sum` per file), and `firmware.bin_extract/` contains exactly those 10 regular files
and **no** symlink — the escaping link is gone, and the two in-tree links are metadata-only, which is
why they appear as `unpublished-entry` gaps and not as files.

## 3. Oracle check — `sasquatch-v4be`, independent of REA and unblob

```
$ sasquatch-v4be -be -no-exit-code -f -d $S/oracle $S/x
Reading a different endian SQUASHFS filesystem on …/x
created 10 files / 11 directories / 3 symlinks / 0 devices, 0 fifos, 0 sockets, 0 hardlinks   (exit 0)
```

| check | result |
|---|---|
| 10 regular files vs `oracle.tsv` | **10/10 OK** on relpath + sha256 + size (`k5-oracle-check.txt`); actual file count 10 = oracle row count (no extras, no omissions) |
| 3 symlinks vs `symlinks.tsv` | **3/3 OK** on target string *and* class: `link-blob → ../opt/blob.bin` in-tree, `link-notes → notes.txt` in-tree, `escape → ../../../../etc/shadow` escaping (`realpath -m` resolves outside the extraction root) |
| escaping link handling | sasquatch **keeps** it as a symlink (as required — only unblob removes); it materialised nothing through it (`$S/etc/shadow`, the path the link names once resolved, does not exist) |
| unblob handle on the same image | exactly one `MaliciousSymlinkRemoved` for the same link, two in-tree links retained as links → both tools agree on the classification, only unblob removes |

## 4. `run.json` internal consistency — 50/50 (`k5-runjson-consistency.txt`)

Highlights (all PASS):

- **argv**: `["npx","-y","rea-agents@6.5.0","extract-firmware","--format","json","--full-output", <carrier.path>, <extraction_root>]`; `argv[7]` = the recorded carrier path, `argv[8]` = `extraction_root` = `after.json`'s `normalized_result.output_directory`; `cwd` = its parent; `argv_shell` sets `REA_UNBLOB_COMMAND` to the resolved unblob path.
- **paths**: `outdir` = `…/c1runs/K5-out` (receipt dir, holds `after.json` + `run.json`) and `extraction_root` = `…/c1runs/K5-scratch/extract` (REA output dir); both under `/kaidoku-r39/`. Names differ but the fields are distinct by design; the frozen "output directory under this round's scratch segment" clause reads against `extraction_root`/`after.json.output_directory`.
- **times**: `start_utc 17:17:06Z` → `end_utc 17:17:10Z`, `duration_ms 3872` consistent with the 4 s window; start is **+255 s after the freeze commit** (17:12:51Z) and the receipt was committed later still (17:18:32Z). Artifact mtime 14:17:10-03:00 = end_utc.
- **tools**: `rea.package_root` = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` version `6.5.0` (same cache dir my runs resolved); `unblob.sha256 0ce7b624…` matches `$HOME/.local/bin/unblob` **and** `$HOME/.local/share/uv/tools/unblob/bin/unblob`; `sasquatch_v4be.sha256 fac88740…` matches `$HOME/.local/bin/sasquatch-v4be`, `version_line "unsquashfs version 4.5.1 (2022/03/17)"`; `child_path` contains `$HOME/.local/bin` (after arm, sasquatch reachable — the recorded `after.json` `raw_result.execution.command` confirms the child actually executed the resolved unblob path).
- **receipt tie-out**: recorded `receipt.sha256 d66f8093…` / `bytes 35151` = the committed `after.json`; `handlers`, `files`, `published_bytes`, `gaps`, `gaps_detail`, `unpublished_entries`, `evidence_id`, `selection_sha256`, `subject_sha256` all equal the corresponding fields of `after.json`; `previous_after_json_sha256` null (first receipt); `stderr_head ""`.
- **envelope provenance (decisive)**: the REA envelope template was first learned from my own run (`{"ok":true,"data":<compact UTF-8 data>,"meta":{"command":"extract-firmware","duration":"NNNNms"}}\n` reproduces `out.json` byte-exactly). Applying it to the **committed** `after.json` bytes, `duration="2367ms"` (a single hit when scanning 500–19 999 ms) yields exactly `35 228` bytes and sha256 `66294d87430599f9a3ca7326baf8f1615ce298d277f90c607c63756bb64c7f10` = the recorded `envelope.sha256`/`envelope.bytes`. So the committed receipt bytes **are** verbatim the `data` member of the envelope that run produced; they were not re-serialised or edited afterwards.
- **original artifacts**: `/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K5-out/{after,run}.json` still exist and are **byte-identical** (`cmp`) to the committed copies, sha `d66f8093…` / `6cf2fb9c…`, mtime 14:17:10.62/.65 local — 82 s before the 14:18:32 commit.
- **evidence id**: `ev_b69020cd9e023a45af295839c18b0ccb349241af8fe166b764beda2ba9d4e309` recomputes exactly with `ev_<sha256(canonical(semanticProjection(evidence)))>` implemented from the pinned bundle (`reconstructionObligationLedgerSchemas-Bao0xMr-.js` l.30 `digestCanonicalValue`, l.536 `semanticProjection`, l.557 `computeEvidenceId`) — `digestCanonicalValue` imported from the shipped 6.5.0 module. My three runs' ids (`ev_939f3ce9…`, `ev_2ff6dbd5…`, `ev_fd82c58a…`) also recompute, so the rule is verified both ways.

## 5. Non-defects noticed (recorded so a later reader does not re-litigate them)

1. `carriers.json` `kind` says "gzip" and the file starts with `sqsh` at offset 0, not `1f8b`: "gzip" here is the squashfs **compression id 1** used for data/metadata blocks; the container is a bare image. `mk-carriers.py` validates exactly this (`each carrier starts with the big-endian SquashFS magic sqsh at offset 0`), and the freeze claim's carrier note reads the same way.
2. unblob's summary says `Extracted files: 11`, while the receipt publishes 10. The 11th is the **staged input copy** `<staging>/firmware.bin` (26 813 B, `raw_result.report[23]`); unblob's `links: 2` are the two in-tree symlinks. Nothing was dropped.
3. `extraction_gaps` has 2 entries but the image has 3 symlinks: the escaping link is removed with a `MaliciousSymlinkRemoved` diagnostic and, per the frozen symlink rule, leaves **no** gap. Consistent.
4. `run.json.outdir` ≠ `run.json.extraction_root` (receipt dir vs REA output dir). Both under `/kaidoku-r39/`; the receipt's `output_directory` matches `extraction_root`, not `outdir`.
5. Run-local identifiers differ by construction between any two runs — `evidence_id`, `provider_id`/`blob_id` (`3028394:1` vs `504359:1`), REA staging temp dir, `meta.duration`. They are the only differences that survive normalisation.

## 6. Residual risk / limits of this attack

- **The disclosed limit stands**: a wholly fabricated receipt whose evidence id is re-minted with the 6.5.0 rule still satisfies every receipt-only clause (`w1/R39C1Controls.md` CTL-C1-3). This seat's value is only that the *actual* K5 receipt is now corroborated by independent re-runs, byte-identity with the original artifacts, and a byte-exact envelope reconstruction. No counter over committed receipts can encode that; it stays a wave-2 procedure.
- The strongest internal leg leans on a **non-committed** artifact: `/fast/scratch/…/l1/c1runs/K5-out/`. If that scratch is cleaned, the "written 82 s before the commit" tie disappears; the envelope-sha reconstruction still works from committed bytes alone but then proves only internal consistency, not that a run happened.
- Carrier regeneration is only possible because `gen-squashfs.py` normalises modes/uid/`mkfs_time`; a carrier with real metadata could not be rebuilt this way, so this particular check is method-limited to synthetic carriers.
- The evidence-id recompute uses bundle-internal functions of the pinned package (exported lazily via `init_canonicalDigest()`); it is not a public API and a future package bump could change it — pinned here to 6.5.0 by `package_root` + `package.json`.
- No build/lint/test gate was run in this seat (out of scope; parent owns post-integration gates). No tool was installed or upgraded. No VCS mutation, no write outside this report and `artifacts/R39W2ReproK5/`. Scratch `$S=/fast/scratch/hyaku/kaidoku-r39/R39W2ReproK5` removed after the artifacts were copied out.

## 7. Evidence (all under `.ufo/waves/round-39/w2/artifacts/R39W2ReproK5/`)

| file | contents |
|---|---|
| `k5-pin-and-regen.txt` | pin sha/size, own BE superblock parse, byte-identical rebuild from the oracle tree |
| `k5-generator-crosscheck.txt` | two writer copies (`f535e60e…`, `833a40a9…`) both rebuild the pin; pre-freeze w1 artifact = same bytes/blob |
| `k5-oracle-check.txt` | `sasquatch-v4be -be` extraction report, 10/10 file rows, 3/3 symlink rows with observed class |
| `k5-semantic-compare.txt` | semantic payload table + run1/run2/run-vs-receipt equality |
| `k5-runjson-consistency.txt` | 50 mechanical `run.json` checks, all PASS |
| `k5-provenance-receipts.txt` | evidence-id recompute (receipt + my 3 runs), byte-identity with l1 scratch originals, run envelopes |
| `rea-refuses-existing-outdir.txt` | REA exits 1 on a pre-existing output directory (freshness argument) |
| `compare.py`, `compare-run{1,2,3}.txt` | reproducible whole-document differ (0 diffs for the frozen-basename run) |
| `evid.mjs` | evidence-id recompute against the shipped 6.5.0 canonicaliser |
| `rea-run{1,2}-envelope.json`, `rea-run3-basename-carrier.sqsh-envelope.json`, `rea-run1.stderr.txt` | raw REA envelopes (empty stderr) |
