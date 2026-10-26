# Blob and licence scan, 49096c7e..7a24ff74 (R41W2C1Chain)

Method: every path added in the range (`git diff --diff-filter=A`, 1 678 paths) is read with
`git cat-file --batch` at the tip and hashed with sha256 in memory; nothing is written from
the repo. Script: `scan_blobs.py` (first pass), `substr_scan.py` (second pass).

## 1. Totals

* 1 678 added blobs, 41 399 075 bytes, 8 commits.
* 4 blobs ≥ 1 MB (all of them listed below); 6 empty blobs.

## 2. Every added blob ≥ 1 MB

| bytes | sha256 | path | what it is |
|---|---|---|---|
| 3 016 975 | `fd8f39aa8f93e095b6a79fd2b738680f98d0abba04fe4b6d493386cfc4499bea` | `.ufo/waves/round-41/w1/artifacts/R41C1DevCore/rea-7430-core-after-rerun.json` | REA 6.5.0 envelope for the public 7430 rootfs: `files[]` of 6 485 rows, keys `path, relative_path, size, sha256, reported_sha256, mime_type, analysis_depth, runtime_address, original_file_range`; `published_bytes` is a count |
| 3 010 488 | `6519526d4f4ff21235e45ea41287fb1e0f5905e78fe08108668018471353fdb5` | `.ufo/waves/round-41/w1/artifacts/R41C1DevCore/rea-7430-core-after.json` | same envelope, first run |
| 2 852 279 | `1efa815f5cf2412e979b85b3e20842606239858efb67a3e195ed1fc32b20d60e` | `corpus/evidence/round-41/c1/V4/after.json` | the V4 REA envelope: `normalized_result.files` 6 349 rows (2 684 681 B of the file), `unpublished_entries` 74 465 B, `extraction_gaps` 211 860 B; no body key |
| 1 722 820 | `3b8776c73798977e56651754ce84fbb58b9276a56918f69003c2305401e060fb` | `.ufo/waves/round-41/w1/artifacts/R41C2Interp/precedence-check-full.tsv` | C2 table, 14 TSV columns of labels/actions per synthetic tuple |

Body tests on all four (and on every added blob): no base64-looking string ≥ 200 chars; the
longest string anywhere in the V4 envelope is a 1 313-byte unblob banner inside
`raw_result.execution.stdout.text`; the DevCore envelopes' longest string is the same banner.
`files[]` rows carry path/digest/size only — a receipt of paths and digests, not a copy of
any file.

The 6 empty blobs are `.ufo/waves/round-41/l1/c1-run-{L3,L4,V3}.log`,
`.ufo/waves/round-41/w1/artifacts/R41C1Collide/empty-nonreg.tsv`,
`…/R41C1Run/evidence/negative/keep-envelope.txt`,
`.ufo/waves/round-41/w1/artifacts/R41C2ControlTables.step.err` — all zero-byte logs/fixtures.

## 3. Vendor-byte comparison (pins and oracle hashes)

Pins compared: the 9 round-41 pins (4 carrier pins + `image_sha256` ×2 + `member_sha256` ×2 +
V4 `nested.sha256`) and the 8 round-40 pins from `.ufo/waves/round-40/c1/carriers.json`
(the table `prior_pins` is drawn from). Oracle hashes compared: all 2 516 distinct 64-hex
tokens in every added `oracle.tsv`, which includes the round-41 `V3` (8 rows / 8 distinct) and
`V4` (6 349 rows / 2 470 distinct) oracles plus the wave-1 fixture oracles.

Result: **no added blob matches a vendor pin and none matches a vendor regular-file digest.**
The only matches to any of those hash sets are the two lane-built carriers
(`corpus/evidence/round-41/c1/L3/carrier.sqsh` 187 892 B = `04cfb4cd…c45a3`,
`…/L4/carrier.sqsh` 169 545 B = `4c0e5459…cbcfbc`, both legitimate, `mk-l-carriers.py`
built) and the sha256 of the *empty file* `e3b0c442…b855` (6 zero-byte blobs above; V3's
`tmp/mtab` oracle row is the empty file, so a future "no oracle hash committed" gate must
skip zero-length oracle rows or it will false-positive).

## 4. Container test (stronger than the hash test for a compressed carrier)

The carriers are compressed SquashFS, so a committed *slice* of firmware would not match any
decompressed-file digest. Tested directly: for every added blob ≥ 32 B (1 672 of them) and
each of the two rebuilt carriers, `carrier.find(blob)` — 3 344 substring tests, 41 MB of
needles against 63 MB of carrier bytes: **0 hits**. No committed blob is a byte run of either
vendor carrier (`substr_scan.py`).

## 5. Licence boundary in the working practice

* `carriers.json` keeps the vendor entries as `external` (URL + digests) and has no `path`;
  the counter refuses a carrier that has both (`carrier %r has both path and external`) and
  requires the cache only for `external` entries.
* `c1-run.sh` extracts into `$scratch/extract` inside a `mktemp -d` scratch removed by
  `trap … EXIT`, and moves only `after.json` into `OUTDIR`; the raw envelope is copied only
  under `C1_KEEP_ENVELOPE=1` (and is still a text envelope).
* The tip tree contains no `filesystem.image`, `filesystem_core.squashfs`, `FRITZ*` or
  round-41 `_extract/` path (`git ls-tree -r --name-only` scan); the round-41 C1 carrier
  directories hold receipts, oracles, one log and the two lane-built `.sqsh` only.
* **Gap:** no tool enforces this. `c1-counter.py`/`c1-extra.py` contain no tree scan
  (`grep ls-tree|committed|licen` finds only prose), so "vendor bytes are never committed"
  is a rule in the frozen table, not a binding. Today it holds (measured above); a future
  commit could add the 63 MB cache anywhere and every binding would still be true.
  Smallest remediation: add a `no_committed_vendor_bytes` binding that hashes every blob at
  `--rev` (1 678 blobs / 41 MB took ≈ 5 s here) against the pins and the oracle digests,
  ignoring zero-length oracle rows.
