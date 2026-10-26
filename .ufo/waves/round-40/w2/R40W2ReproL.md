# R40W2ReproL — independent reproduction of R40-C1 carriers L1 and L2 (wave 2)

**DEFECTS FOUND** — every L1/L2 artifact reproduces exactly (carriers byte-identical over two rebuilds, REA
receipts projection-equal to a fresh run, oracles reproduced by the frozen reader, `sasquatch-v4be` without
`-be` equal to the oracle and with `-be` failing, evidence ids recomputing), **and** the L2
`nonregular_unpublished_ok` miss is a frozen-counter suffix-matching false positive that makes P40-C1's
target unsatisfiable for the pinned L2 bytes: `oracle_hits_ok` and `nonregular_unpublished_ok` cannot both
be true on that carrier. The author's C1 = NOT MET is the correct score under the frozen rules, but its
cause is a defect in the frozen binding, not a failure of the AVM-layout extraction path.

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Worktree HEAD at reproduction `0b15c8b2`
(descends from freeze `7fce3086`, C1 receipts `73c7bf9c`, measured rev `42c10a58`); the frozen C1 tools,
`carriers.json`, `gap-rule.json` and `tools/round-27/xpin-attribute.mjs` hash identically between the freeze
commit and the worktree (table in §7), so the rebuilds below ran on frozen bytes. No VCS mutation, no lane
file written outside this report and its artifacts.

## 1. What I attacked

| # | Attack | Command (exact) | Result |
|---|---|---|---|
| A1 | L-carrier reproducibility | `python3 -I -B tools/round-40/mk-l-carriers.py $S/b3` and `$S/b4` (two independent fresh dirs), then `cmp` against each other and against the committed carriers, and against the pins in `.ufo/waves/round-40/c1/carriers.json` | both builds byte-identical to each other **and** to the committed carriers: L1 `2521ded6d06ff12d…1a0d`, L2 `fec0f72d8034be54…9528` |
| A2 | REA receipt reproduction | `cd $S/rea-<id> && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 <committed carrier> $S/rea-<id>/extract` | exit 0 both; frozen `projection(…,'plus-extractor')` **equal** to the committed `after.json`, `differing keys: []` |
| A3 | Extraction vs independent oracle, AVM argv | `$HOME/.local/bin/sasquatch-v4be -f -n -d <root> <committed carrier>` (no `-be`) | exit 0; 7 files/2 symlinks (L1), 6 files/2 symlinks (L2); `(sha256,size)` sets **identical** to `oracle.tsv`, symlink targets identical to `nonregular.tsv`, dirs 11/8 identical |
| A4 | All-BE argv must fail | same with `-be` | exit 1 both: `read_id_table: failed to read id table block` / `FATAL ERROR: File system corruption detected`, nothing extracted |
| A5 | Frozen reader reproduces its own tables | `git show 7fce3086:tools/round-40/sqfs-list.py > $S/sqfs-list-freeze.py` then `python3 -I -B $S/sqfs-list-freeze.py --layout avm --files … --nonregular … --inspect <carrier>` | exit 0; `oracle.tsv` and `nonregular.tsv` **byte-identical** to the committed tables for both carriers (reader sha256 `1079fa9b…` = freeze bytes; imports only stdlib: argparse/hashlib/json/lzma/os/struct/sys/tempfile/zlib) |
| A6 | AVM layout, independently | stdlib BE superblock unpack + metadata-block walk (`cmp3.py`) | magic `sqsh`, v4.0, `mkfs_time == bytes_used` (230884 / 241390), carrier size == `bytes_used` (carved); metadata block-length headers **little-endian** — see §3 |
| A7 | Gap rule | frozen `gap_check()` + `gap-rule.json` on the committed receipts | true both; 3 gaps = 1 `depth-limited` + 2 `unpublished-entry` (one per retained symlink), no `unknown-chunk-handler`, none for dirs |
| A8 | Receipt ↔ bytes integrity | `sha256sum after.json` vs `run.json.receipt.sha256`; on-disk extraction hash check | matches (L1 `7b196e65…`, L2 `32ea0a3d…`); every published `sha256`/`size` equals the bytes in my fresh extraction tree |
| A9 | Evidence id | frozen `tools/round-27/xpin-attribute.mjs` (from the freeze) + rea-agents 6.5.0 `semanticProjection`, run directly on the committed receipts | exit 0; recomputed id == stored id, L1 `ev_9594f0b5…`, L2 `ev_525ea719…` |
| A10 | Binding reproduction | frozen `same_rel` / `nonregular_published` on the committed data of **all four** carriers | L2 is the only hit; witness and satisfiability proof in §2 |

Evidence files in `w2/artifacts/R40W2ReproL/`: `build-sha256.txt`, `rea-projection.txt`,
`rea-projection-summary.json`, `oracle-compare.txt`, `sasquatch-runs.txt`, `metadata-endian.txt`,
`ondisk-and-gaprule.txt`, `xpin-evidence-ids.txt`, `l2-nonregular-false-positive.txt`,
`builder-spec-vs-oracle.txt`, plus the three drivers `cmp.py`, `cmp2.py`, `cmp3.py`.

Headline numbers from the fresh runs (all equal to the committed receipts):
L1 — 1 chunk `squashfs_v4_be` (offset 0, length 230884, not failed), 7 files, 3 gaps, 2 unpublished
symlinks, `published_bytes` 238530, coverage `partial`, engine unblob 26.6.4.
L2 — same shape with 6 files, `published_bytes` 244251. `parameters.max_depth` is 1 in both. The whole-object
diff (not just the projection) differs only in `evidence_id`, `provider_id`/`blob_id` (`1765570:1` vs
`659234:1`), absolute `path`/`output_directory`, and REA's own staging dirs — every field the frozen
projection excludes by design (`c1-counter.py:766-872`).

## 2. The L2 miss is a frozen-counter false positive, and C1's target is unsatisfiable

Frozen matcher (`tools/round-40/c1-counter.py:606`, used at `:1092`):

```python
def same_rel(candidate, rel):
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))
```

L2 committed receipt publishes `firmware.bin_extract/usr/bin/busy` (a real regular file, oracle row
`usr/bin/busy`, 40000 bytes, `e28f81fc…`). L2 frozen `nonregular.tsv` has the symlink row `bin/busy`.
`firmware.bin_extract/usr/bin/busy`.endswith(`/bin/busy`) is `True` → `nonregular_published` returns a hit →
the binding is false. Nothing was materialised: my fresh run's tree has top level
`['etc','opt','usr','zero']` and **no** `bin/` directory at all.

- Exact-boundary intersection (published rel path with the `_extract` prefix stripped, intersected with the
  non-regular rows) is **empty** for all four carriers. V1 (697 files / 381 non-regular), V2 (8 / 95) and L1
  (7 / 13) pass; only L2 trips, and only through the extra path segment `usr`.
- Joint unsatisfiability, not bad luck: `oracle_hits_ok` requires some published `relative_path` to end in
  `/usr/bin/busy`; `nonregular_unpublished_ok` requires no published path to end in `/bin/busy`. Every string
  ending in `/usr/bin/busy` also ends in `/bin/busy`. With the pinned L2 bytes and the frozen counter, no
  receipt can satisfy both, so `carriers_matched == 4` was unattainable at any revision. The score receipt
  (`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`) shows exactly that: L2 fails only this binding, with
  `layout_ok`, `oracle_hits_ok`, `gaps_ok`, `evidence_id_ok`, `projection_ok`, `run_provenance_ok` all true.
- Why the 70-case battery missed it: the only red case for this binding (`c1-counter.py:1783`, "escaping
  symlink published as a regular file") appends the published path `firmware.bin_extract/usr/share/demo/escape`
  against the fixture non-regular row `usr/share/demo/escape` — an **exact-boundary** match. No case builds a
  published path whose parent-directory tail is itself a non-regular path (the L2 shape), and no fixture
  published name (`README.txt`, `config/app.conf`, `bin/run`, `docs/deep/blob.bin`, `etc/motd`,
  `var/info.txt`) is a suffix-superstring of a fixture non-regular path.
- Consequence for the landing: the demotion to measured-not-promoted is defensible as *a score under frozen
  rules*, but "honest stop" reads as toolchain/extraction insufficiency, which the evidence contradicts — on
  the pinned toolchain both L carriers extract cleanly through the AVM handler with an exact oracle match.
  Fix belongs to a later round (the file is frozen): anchor the candidate at the chunk-extract boundary
  (`rel_suffix`, already used by `projection()`) instead of any-suffix matching, and add a sibling-suffix
  collision red case. I applied nothing.

## 3. Metadata block lengths are little-endian (decisive, independent of unblob/sasquatch)

Walk both tables as `u16 header (0x8000 = stored, low 15 bits = stored size) + body`, decoding xz/gzip
(`cmp3.py`, stdlib only), testing both byte orders:

```
L1 comp=4 (xz)   inode_table   [229534,230468)  LE ok, 1 block, 932 B out  | BE short body
                 directory_tbl [230468,230876)  LE ok, 2 blocks, 404 B out | BE short body
L2 comp=1 (gzip) inode_table   [240269,241068)  LE ok, 1 block, 797 B out  | BE short body
                 directory_tbl [241068,241382)  LE ok, 2 blocks, 310 B out | BE short body
```

LE consumes each region exactly to the next table start; BE runs past the end of the carrier. On L1 the size
test alone decides (`bytes=a483`: LE size 932 plausible, BE size 9347 > 8192); on L2 the decode/termination
test decides. This is the same pair the frozen reader reports (`header_length_candidates {be: 9347, le:
932}`), reproduced without it. Independent corroboration from the other direction: forcing all-BE
(`sasquatch-v4be -be`) fails at `read_id_table` on both carriers, so the metadata streams are not BE.

## 4. Calibration notes

- The author's stated reading of the L2 failure (path-suffix false positive from regular `usr/bin/busy` and
  symlink `bin/busy`) is **confirmed mechanically**, not just plausible.
- The stronger claim I can add: it is not merely a false positive that happened once, it is a
  *jointly unsatisfiable* binding pair on the frozen data, so P40-C1's own target was unreachable at the
  freeze. That is a claim-design defect (frozen predicate never validated against the frozen carriers), and it
  is worth more than a footnote in the round record: any future carrier pair like `usr/bin/busy` + `bin/busy`
  reproduces it.
- Everything the predicate asks of the *bytes* holds: marker, LE metadata headers, `sqsh` BE identity, carve at
  `bytes_used`, `--max-depth 1` receipts that a fresh run reproduces on the projection, oracle equality from
  two producers, gap rule, provenance segment, evidence id, and receipt freshness (after.json/run.json first
  added at `73c7bf9c`, a descendant of the freeze; carriers and oracles added **at** the freeze, `git
  log --diff-filter=A`).

## 5. Disclosed limits of this seat

1. V1 and V2 were **not** rerun here (outside this seat); their published/`reginfo` facts are read only for
   the suffix-collision blast radius in §2, and I trust the score receipt for their extraction results.
2. The comparison driver imports the frozen `projection()`/`same_rel()` functions from
   `tools/round-40/c1-counter.py` rather than retyping them; the projection *definition* is the frozen
   artifact under test, my code only supplies the two sides. I did not use the counter's REA rerun path — my
   own `npx` runs are independent.
3. My REA runs left `TMPDIR` unset, so REA staged under `/tmp/rea-firmware-*` while the committed run staged
   under `…/kaidoku-r40/run-<id>`; that is exactly why the `evidence_id` differs and why the projection
   excludes paths. No lane file was written by those runs.
4. Evidence-id recompute uses the frozen mjs tool plus the installed 6.5.0 package (the claim's own rule);
   it is not a hand re-derivation of `semanticProjection`.
5. As the claim discloses, none of this proves which process wrote the committed receipts; it shows the
   pinned toolchain on the pinned bytes yields the same projection at scoring time.
6. Two rebuilds only (as assigned); determinism rests on a fixed sha256-counter tree, no clock/urandom.

## 6. Risks and blockers

- Risk: `same_rel` is a shared helper for oracle hits, gaps and publication — the same any-suffix semantics
  makes `gaps_ok` accept a gap attributed to a superstring path. No such case appears in the four frozen
  carriers (all `gap_check` true), but a future carrier could hide a real materialisation or manufacture a
  pass. Worth a round-41 binding change with its own red case.
- Risk: the round record must not read C1's 3/4 as "AVM layout not established". The extraction path is
  established; the target arithmetic was broken.
- No blockers. Nothing was installed or upgraded (existing `unblob` 26.6.4, `sasquatch-v4be` 4.5.1,
  `rea-agents` 6.5.0 sufficed), so no tool/version/channel/reason entry is owed.

## 7. Frozen bytes actually used (`git show 7fce3086:<path> | sha256sum` == worktree)

```
5f8f8da6…59e3a  tools/round-40/mk-l-carriers.py
309c502d…042e   tools/round-40/gen-squashfs.py
8d288e4c…7e81   tools/round-40/c1-counter.py
1079fa9b…3cd9   tools/round-40/sqfs-list.py
de3f4af8…9dbdd  tools/round-40/c1-run.sh
5ba40129…bfbb0  tools/round-40/c1-extra.py
ccc4dc23…5a69f1 tools/round-40/fetch-vendor.py
81c504cf…c681   .ufo/waves/round-40/c1/carriers.json
421b3d1a…7dd1b  .ufo/waves/round-40/c1/gap-rule.json
8ea63837…f708   tools/round-27/xpin-attribute.mjs
```

`git diff --name-only 7fce3086 0b15c8b2 -- <frozen C1 paths>` lists only `corpus/evidence/round-40/c1/*/
{after,run}.json`, which `carriers.json` does not name as carrier/oracle/non-regular paths; their only commit
after the freeze is `73c7bf9c` (added, never rewritten).

## 8. Files changed

- `kaidoku-shokunin/.ufo/waves/round-40/w2/R40W2ReproL.md` (this report)
- `kaidoku-shokunin/.ufo/waves/round-40/w2/artifacts/R40W2ReproL/` (10 evidence files + 3 drivers, listed §1)

Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2ReproL` removed; nothing copied into the lane (no carrier
bytes, no vendor bytes, no extracted vendor files — only hashes and comparison tables).
