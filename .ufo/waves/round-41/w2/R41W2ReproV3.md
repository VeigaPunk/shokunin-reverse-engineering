# R41W2ReproV3 — independent reproduction of the R41-C1 **V3** receipt

**Verdict: CONFIRMED.** I attacked the V3 arm of R41-C1 — the claim that a committed round-41
REA 6.5.0 receipt for the FRITZ!Box 5490 07.31 rootfs is what the pinned toolchain produces
from the pinned bytes — by rebuilding the carrier from the AVM download chain at the freeze,
running REA `extract-firmware --max-depth 1` myself (not `c1-run.sh`), and comparing every
path the predicate names against `corpus/evidence/round-41/c1/V3/after.json`. Every V3 clause
of P41-C1 that a receipt can carry reproduces: same handler, same 8 regular files at the same
exact oracle paths with the same sha256 **and** size, the same 85 symlink dispositions and the
single structural `depth-limited` gap, no diagnostics, same subject digest, same
`plus-extractor` projection, and the committed receipt's stored evidence id recomputes under
the frozen package rule. No defect found in the V3 landing.

Seat scope: V3 only. V4/L3/L4 receipts, the C1 landing-document clauses (PROVINCE, knowledge
entry, SOURCES, `corpus/README.md`, frontier note) and R41-C2 are other seats' items and were
not re-audited here.

## 1. What was run (full commands and versions: `artifacts/R41W2ReproV3/run-log.md`)

1. **Carrier rebuild** — `fetch-vendor.py --rev d764389e… --cache $S/cache`, exit 0. Image
   sha256 `770efb4e…5ab7`; member `./var/tmp/filesystem.image` 30236680 bytes sha256
   `87cc5d6b…a0f8`; carrier slice 30233394 bytes sha256 `c4f74f54…f872a` == the pin
   (`artifacts/R41W2ReproV3/fetch-chain.json`). Vendor bytes were not committed, copied into
   artifacts, or redistributed; only sha256 values are cited.
2. **Independent REA run** — `REA_UNBLOB_COMMAND=~/.local/bin/unblob npx -y
   rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 <carrier>
   $S/rea-out-V3`, exit 0, 1.2 s (`meta.duration` 1215 ms), stderr empty, `ok=true`,
   `evidence_id ev_09e2c40d…cd82` (fresh scratch directory). Fresh `data` object kept as
   `artifacts/R41W2ReproV3/fresh-V3-after.json`.
3. **Layout probe** — independent superblock/metadata read of the same bytes
   (`artifacts/R41W2ReproV3/layout-v3.json`).
4. **Third extractor** — `sasquatch-v4be` 4.5.1 **without** `-be` on the same bytes, compared
   to `oracle.tsv`; plus the `-be` negative control.
5. **Comparison** — `reproduce-v3.py` maps committed and fresh receipts into the oracle
   namespace by the exact-path rule of `w1/R41C1Revenger.md` §1 (strip one `$output/` from
   each path **including** the derivation root, whole-segment prefix, equality only) and
   applies the frozen `gap-rule.json`; result `artifacts/R41W2ReproV3/reproduce-v3.json`.
6. **Evidence id** — `tools/round-27/xpin-attribute.mjs` at the freeze bytes
   (`8ea63837…f708`), `--pkg65/--pkg67` = the installed rea-agents 6.5.0 root.
7. **Frozen set** — read-only `git diff FREEZE..REV` over the C1 frozen paths; receipt
   first-add commit and ancestry.

## 2. Clause-by-clause result for V3

| P41-C1 clause (V3) | measured | verdict |
|---|---|---|
| receipt names `squashfs_v4_be`, no failed chunk | committed and fresh: one chunk, handler `squashfs_v4_be`, `extraction_failed false`, range `[0, 30233394)` = the whole input | met |
| every regular oracle row published at its exact rel path, same sha256 and size | 8/8 hits, 0 mismatches, no extra published file, none published outside the root | met |
| no non-regular oracle row published as a file | published ∩ non-regular = ∅ | met |
| every non-regular row accounted for exactly once as the rule allows | 95 rows (85 symlinks, 9 dirs, 1 char device `dev/led 247:0`): each symlink carries exactly one `unpublished-entry` gap at its exact path; dirs/device invisible and carry none; 0 removal diagnostics; no row both gapped and removed; no gap or removal resolving to no row | met |
| ≤1 structural `depth-limited`, no `unknown-chunk-handler` | `depth-limited` ×1 on `$output/firmware.bin_extract` (the nested 29,597,696-byte `filesystem_core.squashfs` is not entered at depth 1); 0 `unknown-chunk-handler`; gaps unique (86 rows = 85 + 1) | met |
| subject digest == carrier pin, and recomputes to its evidence id | `subject.digest.sha256 == c4f74f54…f872a`; xpin at the freeze: stored `ev_26a93366…ebc17` == recomputed `ev_26a93366…ebc17` | met |
| carrier bytes: pin, AVM marker, LE metadata block length, length == `bytes_used` | sha256 == pin; size 30,233,394 == `bytes_used`; magic `sqsh`, v4.0, `mkfs_time == bytes_used == 30233394`; header at `inode_table_start` `d402` → LE 724 (in 1..8192) vs BE 21506 (out of range), LE identity `30231260+2+724 == 30231986`; 104 inodes, block 65536, compression 4 | met |
| vendor fetch chain (image / member sha256) | image and member sha256 both re-checked on a fresh download at the freeze rev | met |
| counter-time (here: seat-time) REA rerun has the same `plus-extractor` projection | projection equality committed vs fresh: `true`, 0 differing keys — files (rel, sha256, size, mime), gaps, unpublished entries, diagnostics, chunks, derivations, engine `unblob 26.6.4`, `published_bytes 31227104`, `coverage partial`; the frozen counter's own `projection()` returns the same verdict | met |
| receipt first added after the freeze | `5ca6941b…` is the only commit touching `V3/after.json`; freeze ≤ 5ca6941b ≤ measured revision `e9a24d07…`; blob at `e9a24d07` == blob at `5ca6941b` == working tree (`b22d4b91…`, file sha256 `3097cc27…3f150`) | met |
| run provenance | committed receipt `parameters.output_directory` = `/fast/scratch/hyaku/kaidoku-r41/run-V3/extract` (`/kaidoku-r41/` segment) | met |
| no frozen C1 path changed FREEZE..REV | `git diff --stat` over claims/tools/gap+carrier specs/oracle+non-regular tables/L3,L4 carriers: empty | met |

## 3. Depth: what else was measured, and what it shows

- **The `-be` negative control.** `sasquatch-v4be -be` on the same bytes exits 1 —
  `Reading a different endian SQUASHFS filesystem … FATAL ERROR: File system corruption
  detected`, 0 files. So the extraction that produced 8/8 oracle files required the no-`-be`
  argv, and the "big-endian structural fields, little-endian metadata block lengths" reading
  is not an artefact of the reader: the standard-BE decode fails on these bytes.
- **Three producers, one answer.** The oracle (`sqfs-list.py --layout avm`), a direct
  `sasquatch-v4be` extraction, and REA's published files agree exactly on (rel, sha256, size)
  for all 8 rows, and a filesystem walk of REA's own output tree matches the receipt's
  `files[]` with 0 content mismatches (`artifacts/R41W2ReproV3/tree-vs-receipt.json`).
- **The committed receipt is not merely oracle-shaped.** Its full field diff against my
  independent run (`artifacts/R41W2ReproV3/receipt-diff.txt`) has 27 differing leaves: the
  absolute-path fields (`parameters.path`, `subject.local_path`, `normalized_result
  .output_directory`, the 8 `files[].path`, `raw_result` args/task paths) and the provider
  blob counter (`3104447:1` vs `4168704:1`). No content, gap, diagnostic, unpublished,
  engine or parameter leaf differs. Rea-agents 6.5.0's `semanticProjection`
  (`dist/domain/evidence.js:156-182`) hashes `parameters` and `raw_result`, which is why even
  a rehosted re-mint (`ev_a141eed2…`) cannot equal the committed id from a different
  directory — expected, and not a clause: the claim binds the projection, not the id of the
  rerun.
- **Where the 95 non-regular rows come from.** The user-visible output tree after the run
  holds 8 files and 5 directories — no symlinks, no `dev/led`, and 4 of the oracle's 9
  directories gone (those left with no files); a direct unblob run with REA's argv leaves all
  85 symlinks and the 9 directories, and creates no device unprivileged. The receipt still
  lists every row. So "unpublished" is a publication-side disposition of a fully inventoried
  tree, not evidence that entries were missing — consistent with the frozen gap rule and with
  what both receipts say. [INFERENCE] on the exact publication/cleanup mechanism; the
  observed facts are the two trees and the two receipts.

## 4. Textual imprecision (not a scoring defect)

The claim's exact-path rule reads "Strip one `$output/` prefix; the chunk extract root CR is
the child path of the receipt's `derivations[]` edge … `rel(P)` is `P[len(CR)+1:]` only when
`P` starts with `CR + '/'`". Taken literally with `CR` still carrying its `$output/` prefix,
no receipt path maps (the published `relative_path`s are bare), and V3 would score 0/8. The
operative reading — and the one `w1/R41C1Revenger.md` §1 states normatively, the one the
frozen counter implements (`strip_output` on both sides) and the one I used — strips `$output/`
once from *every* path including the root. With that reading the rule is exact-segment and
strictly stronger than the round-40 suffix matcher. Recommend the wave-3 text say "strip one
`$output/` from each path, including the derivation root"; no data or counter change needed.

## 5. Residual limits (unchanged by this reproduction)

- R40-CL2 stays open: I show that the pinned toolchain on the pinned bytes yields this receipt
  content, not who wrote the committed file. A forger holding the same deterministic toolchain
  could in principle reproduce it; a forger holding only the oracle cannot (the projection
  includes extractor-determined `derivations`, engine, `published_bytes`, `coverage`, mime and
  the removal set).
- The reproduction is one run per arm. Both runs agree on all stable fields, so a flake is
  ruled out for V3 at this toolchain, but this is not a repeat-stability study.
- My fresh run's own evidence id (`ev_09e2c40d…`) differs from the committed
  `ev_26a93366…`; that is inherent to the package's id rule and is not compared by the claim.

## 6. Artifacts (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-41/w2/artifacts/R41W2ReproV3/`)

- `run-log.md` — every command, version, exit code, timing, and the frozen-set git checks.
- `reproduce-v3.py`, `reproduce-v3.json` — independent exact-path + gap-rule comparator and
  its full result for the committed and the fresh receipt (`projection_ok true`).
- `layout-v3.py`, `layout-v3.json` — superblock/metadata probe of the carrier bytes.
- `fetch-chain.json` — `fetch-vendor.py` run at the freeze (sha256 chain; no vendor bytes).
- `fresh-V3-after.json` — the receipt object my independent REA run produced (45,050 bytes).
- `receipt-diff.txt` — full field diff, committed vs fresh (27 leaves).
- `xpin-v3.txt`, `xpin-v3-rehosted.txt` — evidence-id recompute and the rehost probe.
- `tree-vs-receipt.json` — REA output tree vs receipt `files[]` (0 mismatches).

Scratch `/fast/scratch/hyaku/kaidoku-r41/R41W2ReproV3` removed; nothing was written outside
this artifact directory and this report. No tool installed or upgraded; no VCS mutation.
