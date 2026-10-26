# R41W2ReproL — L3/L4 reproduction (round 41, wave 2)

**CONFIRMED** — I attacked the two lane-built R41-C1 carriers, L3 (xz) and L4 (gzip): rebuilt from the tree at
`e9a24d07256d1606f01aa4d2d65f74e649c5f3d4`, byte-identical to the pins and to the committed
`carrier.sqsh`, re-ran REA 6.5.0 `extract-firmware --max-depth 1` twice per carrier plus once through the frozen
`c1-run.sh after` arm, and both committed `after.json` receipts reproduce under the frozen `plus-extractor`
projection with zero differing keys. One **non-scoring evidence defect (D1)** and two minor observations (D2, D3)
follow; none changes a predicate binding.

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Measured revision `e9a24d07…`; freeze `d764389e…`; wave
spec's other pins untouched. No VCS mutation (only `show`/`log`/`ls-tree`/`rev-parse`/`merge-base`/`archive`).
No tool installed or upgraded. Nothing written outside this report and
`.ufo/waves/round-41/w2/artifacts/R41W2ReproL/`. Scratch `/fast/scratch/hyaku/kaidoku-r41/R41W2ReproL` removed
at the end; every number below is in the copied artifacts (hashes in `sha256sums.txt`).

## 1. Rebuild: pins, byte-identity, determinism

`python3 -I -B $S/tree/tools/round-41/mk-l-carriers.py $S/out --builds 2 --lane $S/tree --json …` → exit 0.
The tree was materialised with `git archive e9a24d07 tools/round-41 tools/round-40
.ufo/waves/round-41/c1/carriers.json`; `tools/round-41/gen-squashfs.py` and `tools/round-40/gen-squashfs.py` are
byte-identical there (`309c502d…2e`, `cmp` exit 0), so the writer is the frozen one.

| carrier | comp | rebuilt sha256 | size | files/links/dirs | pin (`carriers.json`) | `cmp` vs committed `carrier.sqsh` |
|---|---|---|---|---|---|---|
| L3 | xz (id 4) | `04cfb4cd6189742eaba94d0022d242d4194726a6f0684fd8381b39bc4e6c45a3` | 187892 | 13/3/20 | equal | identical (exit 0) |
| L4 | gzip (id 1) | `4c0e545975d2993f5b3417d55990a5df5ad67fa2f21164b831119f6e85cbcfbc` | 169545 | 14/3/17 | equal | identical (exit 0) |

Both carriers were built twice into separate directories (`b2/`) and the second build hashes and sizes equal the
first (`build2-equal` on both lines of stdout, builder exit 0): byte-determinism reproduced
(`build.json`, `run-metadata.json`).

Independent layout proof (my own `struct` parse, no sqfs-list/unblob code — `avm-parse.json`): magic `sqsh`,
`4.0`, all structural fields big-endian, `mkfs_time == bytes_used == len(image)` (187892 / 169545), and the 2-byte
metadata block-length header at `inode_table_start` decodes little-endian with the `0x8000` uncompressed flag
(L3 `8385` → 1411, L4 `3985` → 1337) such that `2 + len` lands exactly on `directory_table_start`
(187166 / 168892); the big-endian reading (901 / 14725) does not. Inode counts corroborate the trees
(L3 37 = 13 regular + 20 dirs + 3 links + root; L4 35 = 14 + 17 + 3 + 1).

## 2. REA 6.5.0 runs and comparison with the committed receipts

Four direct runs (`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware
--format json --full-output --max-depth 1 <carrier> <fresh outdir>`, two per carrier) and two runs through the
frozen harness (`c1-run.sh after <carrier> <scratch outdir> <scratch work>`) all exited 0 with empty stderr.
Toolchain identical to the receipts' own pins: unblob 26.6.4 sha `0ce7b624…1d09` (`~/.local/bin/unblob` is a
symlink to the uv install, same sha), sasquatch-v4be 4.5.1 sha `fac88740…14c6`, rea-agents 6.5.0 from
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.

Comparison uses the frozen counter's own `projection(profile='plus-extractor')` and `projection_diff()`, imported
read-only from `$S/tree/tools/round-41/c1-counter.py`, so the compared surface is exactly the claim's frozen
profile (`projection-compare.json`, `determinism.json`, `harness-repro.json`):

| pair | L3 | L4 |
|---|---|---|
| committed `after.json` vs fresh run 1 | equal, 0 differing keys | equal, 0 differing keys |
| committed vs fresh run 2 | equal | equal |
| run 1 vs run 2 | equal | equal |
| committed vs frozen-harness receipt | equal | equal |
| harness vs direct npx | equal | equal |

Per-carrier facts identical in committed and fresh receipts: subject digest = carrier pin; one chunk, handler
`squashfs_v4_be`, `extraction_failed` false; `coverage` partial; no `diagnostics`; `published_bytes` 194049 (L3) /
174930 (L4); 13 / 14 published regular files; 4 gaps each — one structural `depth-limited` with null path and
three `unpublished-entry` gaps for the three symlinks. Evidence ids differ between runs as expected (they hash the
run's `output_directory`); the committed ones recompute to their stored values with the package's own rule
(`evidence-id-recompute.txt`, `node tools/round-27/xpin-attribute.mjs` → `ev_cfe678f3…1b1` / `ev_34143817…327`,
both MATCH, exit 0).

Independent accounting (`projection-compare.json`, `extract-on-disk.json`): every `oracle.tsv` row is published at
its exact relative path with the same sha256 and size (13/13, 14/14, 0 missing, 0 mismatched); nothing is published
that is not an oracle row; every non-regular row is accounted for exactly once (L3 23 rows = 20 dirs + 3 symlinks;
L4 20 = 17 + 3; 0 unaccounted); the on-disk REA extract tree hashes to the oracle exactly (13/13, 14/14) and
contains no symlink. The oracle itself re-derives byte-identically (`sqfs-list.py --layout avm --inspect`, exit 0,
`layout: avm`, `header_endian: little`, `block_length_signal: layout-avm`, `avm_marker: true`,
`escaping_symlinks: 0`) and a **direct `sasquatch-v4be -f -no-exit-code -n`** extraction agrees 0 mismatches
(L3 13 files / 20 dirs / 3 links, L4 14 / 17 / 3 — `sasquatch-crosscheck.json`).

## 3. The collision pairs: what is published, what is gapped

REA paths below are after the exact-path rule (`$output/` stripped, root = `firmware.bin_extract`, the child of the
`squashfs_v4_be` derivation edge).

**L3 (`04cfb4cd…45a3`)**

| pair | oracle | published | gapped |
|---|---|---|---|
| `usr/bin/busy` vs `bin/busy` | `usr/bin/busy` regular 48000 B `c2a5bd87…6b4c`; `bin/busy` → `../usr/bin/busy` | `usr/bin/busy` at `firmware.bin_extract/usr/bin/busy`, sha `c2a5bd87…6b4c`, 48000 B | `bin/busy` only: one `unpublished-entry` gap at `firmware.bin_extract/bin/busy` (`link_target ../usr/bin/busy`); not published |
| `usr/sbin/tool` vs `sbin/tool` | `sbin/tool` regular 32000 B `9ba4c7e1…22b1`; `usr/sbin/tool` → `/sbin/tool` | `sbin/tool` at `firmware.bin_extract/sbin/tool`, sha `9ba4c7e1…22b1`, 32000 B | `usr/sbin/tool` only: one `unpublished-entry` gap (`link_target ../../sbin/tool`, see D2); not published |
| `opt/x/etc/conf` vs `etc/conf` | both regular, different bytes: 96 B `6b5abc69…8e89` and 47 B `afc09b9d…aab9` | **both** published at their exact paths with their own sha/size | nothing gapped |
| third link `usr/share/web/current` | symlink → `index.html` | — | one `unpublished-entry` gap |

**L4 (`4c0e5459…cfbc`)** — same shape: `usr/bin/busy` published (56000 B `6acef71e…d7bb`) with `bin/busy` gapped;
`sbin/tool` published (28000 B `25392f83…15b0`) with `usr/sbin/tool` gapped; `opt/x/etc/conf` (120 B
`728c0d7e…2bf5`) and `etc/conf` (47 B `3de5066c…bc41`) **both** published; third link `var/log/current` gapped.
No `MaliciousSymlinkRemoved` diagnostic and no removal on either carrier (removal disposition unused); the only
structural gap is a single `depth-limited` with null path; no `unknown-chunk-handler`; directories invisible;
`var/tmp/empty` published as a 0-byte regular file in both.

Why the pairs bite, measured on the committed receipts (`matcher-exact-vs-suffix.json`): replaying the frozen
round-40 suffix matcher (`legacy_same_rel`) over the same receipts, the published regular
`firmware.bin_extract/usr/bin/busy` also satisfies the **symlink** row `bin/busy` (double accounting), and the
oracle rows `etc/conf` and `sbin/tool` each gain a wrong legacy carrier (`…/opt/x/etc/conf`, `…/usr/sbin/tool`).
Under the exact rule only the right entry matches and `nonregular_published` is empty. The frozen counter's
selftest agrees and passes: 97 cases, 12 green + 85 red, `path_probes 6 / discriminating 3`, `failures: []`
(`c1-counter-selftest.json`, exit 0).

Provenance cross-check (read-only): `corpus/evidence/round-41/c1/{L3,L4}/after.json` were added in `5ca6941b`,
which descends from the freeze (`merge-base --is-ancestor` exit 0); `oracle.tsv`/`nonregular.tsv` had no commit in
`d764389e..e9a24d07` (frozen at the freeze).

## 4. Defects and observations

**D1 (evidence-citation defect, non-scoring).** The claim's Oracle bullet (`plans/round-41-claims.md:78-79`) states
the reader's file list "equals a direct `sasquatch-v4be` … extraction **on all four carriers** with 0 mismatches
(`oracle-run.json` per carrier)". At `e9a24d07` only `V3/oracle-run.json` and `V4/oracle-run.json` exist;
`L3/` and `L4/` hold `carrier.sqsh`, `oracle.tsv`, `nonregular.tsv`, `run.json`, `after.json` and **no
`oracle-run.json`** (`git ls-tree -r e9a24d07 corpus/evidence/round-41/c1`). So the claim text cites an artifact
that is absent for two of the four carriers. No binding depends on it — `c1-extra.py`'s `oracle_rederived` reads
`oracle.tsv`/`nonregular.tsv` only (`tools/round-41/c1-extra.py:75-104`), and `carriers.json` names `oracle` and
`nonregular`, not `oracle-run.json`, so no frozen-path or score consequence. I supply the missing measurement
myself: `sasquatch-crosscheck.json` reproduces 0 mismatches on L3 and L4. Suggested repair: either commit the
L3/L4 `oracle-run.json` or narrow the claim sentence to the carriers that carry it (wave-2 scribe territory, not
mine to edit). *(Same class, out of my item: `V4/` has no `run.json`, only `run-harness-failure.log` — the commit
message of `5ca6941b` names the helper's ARG_MAX failure, and the wave spec names the 1 MiB rule for V4's
`after.json`.)*

**D2 (observation, no impact).** The image stores `usr/sbin/tool → /sbin/tool` (absolute; `oracle.tsv`…
`nonregular.tsv` and my `sqfs-list --inspect` agree, `symlink_reasons.absolute-inside 1`), but both receipts
report `link_target: "../../sbin/tool"` — REA normalises the absolute target relative to the link's directory
(`usr/sbin/..`/`..`/`sbin/tool` = `sbin/tool`, the same in-tree target). The frozen projection compares only
`(kind, relative_path)` and P41-C1 never scores link targets, so nothing is affected; it does mean a receipt's
`link_target` is not the image's bytes. Recorded because a future claim that scores targets would need to know
`[INFERENCE]` this is tool normalisation, not fixture drift — the same form appears for both carriers and for a
link whose target was relative in the image (`bin/busy → ../usr/bin/busy`, unchanged).

**D3 (observation relevant to C2, not scored here).** Neither L3 nor L4 receipt records any child argv
(`diagnostics` is empty and `raw_result` contains no `sasquatch`/`unsquashfs` string), so under C2's label
precedence these envelopes have `BE = n/a`. Flagged only because a reader might assume the `squashfs_v4_be`
handler implies a recorded `-be`-less argv; it does not.

## 5. Limits

- The rerun binding shows that these carrier bytes extract through the pinned toolchain with the committed
  projection at scoring time; it cannot prove which process wrote the committed receipt (R40-CL2 stays open).
  Evidence-id recomputation plus projection equality rules out a hand-edited or oracle-fabricated receipt for the
  compared surface, not an identical-tool rerun's authorship.
- Symlink dispositions on a full vendor rootfs depend on directory iteration order (`w1/R41C1DevCore.md` §6); on
  L3/L4 the three entries are simply never published, and both of my runs (and the harness run) produced the same
  gap set on these tiny trees.
- I did not score the counter, touch V3/V4, or run any vendor fetch; the vendor arm is out of this seat.

## 6. Artifacts

`.ufo/waves/round-41/w2/artifacts/R41W2ReproL/` (hashes in `sha256sums.txt`): `commands-and-exit-codes.txt`,
`run-metadata.json`, `build.json`, `avm-parse.json`, `projection-compare.json`, `determinism.json`,
`harness-repro.json`, `sasquatch-crosscheck.json`, `extract-on-disk.json`, `matcher-exact-vs-suffix.json`,
`c1-counter-selftest.json`, `evidence-id-recompute.txt`, `oracle-rebuilt/{L3,L4}.{oracle,nonregular}.tsv`.
The rebuilt carriers are **not** copied: they are byte-identical to the committed `carrier.sqsh` (sha256 above),
and the rebuild command is one line (§1). No vendor bytes anywhere in these artifacts.
