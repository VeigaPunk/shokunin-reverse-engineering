# R41C1LCarriers — round-41 lane-built carriers L3 (xz) and L4 (gzip)

**DONE** — both carriers are built by a round-41 port of `mk-l-carriers.py` through
`tools/round-40/gen-squashfs.py --endian avm-genuine`, are byte-identical over two independent builds and
over an mtime-mangled rebuild, carry the AVM marker with little-endian metadata block-length headers
(superblock + LE-chain proof, plus two independent all-BE controls that fail), and reproduce to
`oracle.tsv` / `nonregular.tsv` from two independent producers with **0 mismatches** under an **exact**
path comparison. Both trees hold 13/14 regular files, 3 symlinks, the two nesting-collision directions the
round-40 defect needs, and a deep-tail regular pair. No REA and no unblob run touched either carrier (item
rule), so the "untouched before the freeze" property holds by construction.

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `49096c7e6f226af0c750c4b003be58883cb6049f`
(worktree `tools/round-40/gen-squashfs.py` and `sqfs-list.py` hash identically to the base commit — log §0).
No VCS mutation. No tool installed or upgraded. Nothing written outside this report and
`.ufo/waves/round-41/w1/artifacts/R41C1LCarriers/`. Scratch `/fast/scratch/hyaku/kaidoku-r41/R41C1LCarriers`
removed at the end; every number below lives in the copied `build-log.txt` and the artifact hashes in
`artifact-sha256.txt`.

## 1. Deliverables

Everything below is in `.ufo/waves/round-41/w1/artifacts/R41C1LCarriers/` unless stated otherwise.

| File | sha256 | Size | Role |
|---|---|---|---|
| `mk-l-carriers.py` | `417528b40f459960fd43201d4b3f42897f83350dde072e1bfd6c97ba626853a0` | 12514 | round-41 builder (port of `tools/round-40/mk-l-carriers.py`); L1 copies to `tools/round-41/mk-l-carriers.py` |
| `L3/carrier.sqsh` | `04cfb4cd6189742eaba94d0022d242d4194726a6f0684fd8381b39bc4e6c45a3` | 187892 | L3 carrier, xz (compression id 4) |
| `L4/carrier.sqsh` | `4c0e545975d2993f5b3417d55990a5df5ad67fa2f21164b831119f6e85cbcfbc` | 169545 | L4 carrier, gzip (compression id 1) |
| `L3/oracle.tsv` | `c79c19d4b8ff51bc06d3ecba3e4ec3cdd5451c5cfba88007195b0c9e78b2d606` | 1116 | 13 regular rows (relpath, sha256, size) |
| `L3/nonregular.tsv` | `f49075887cb564924ef7733f1faf05e0a29f50b91e1b2adc15f779bfa8b20706` | 362 | 20 dir rows + 3 symlink rows |
| `L4/oracle.tsv` | `e39a4d1361dd99532cf376100c2fd582900edcea4f5c57092eca46cd072709dc` | 1165 | 14 regular rows |
| `L4/nonregular.tsv` | `9bdcacde409a9bcce02d0d29d8b9c3814d8ce5214f921b54fcb1d225451b8849` | 303 | 17 dir rows + 3 symlink rows |
| `carriers.json` | `5fa58e0a923a0fac264633861c7fd5c1fc578adda6729a249f9a6eccbd218acd` | 4313 | fragment for `.ufo/waves/round-41/c1/carriers.json` (paths under `corpus/evidence/round-41/c1/L3|L4/`) |
| `build-log.txt` | `8578da584b0b365f6b0d94233e8c0bc9cfdef67c3a54e3dd113b4aed7e761dc4` | 21378 | full command transcript, 17 sections |
| `probe.json` / `L{3,4}/inspect.json` / `L{3,4}/inspect-auto.json` | see `artifact-sha256.txt` | — | independent AVM proof and reader summaries |
| `probe-avm-chain.py`, `xcheck.py` | see `artifact-sha256.txt` | — | the two checkers used (stdlib only) |

Carriers are 188 KB and 170 KB, both far under the 1 MB lane budget; total artifacts dir 468 KB. All
content is synthetic (sha256 counter streams and literal text) — no vendor bytes, nothing carved from a
reserved image.

## 2. Tree design: what each claim requirement is carried by

Both trees are fresh content, unrelated to L1 (`2521ded6…1a0d`, 7 files) and L2 (`fec0f72d…9528`, 6 files).

| Draft requirement | L3 (xz) | L4 (gzip) |
|---|---|---|
| ≥ 12 regular files in nested dirs | 13 | 14 |
| regular `usr/bin/busy` + symlink `bin/busy` (collision direction A) | `usr/bin/busy` 48000 B `c2a5bd87…6b4c`, `bin/busy -> ../usr/bin/busy` | `usr/bin/busy` 56000 B `6acef71e…d7bb`, `bin/busy -> ../usr/bin/busy` |
| symlink `usr/sbin/tool` + regular `sbin/tool` (mirror direction B) | `usr/sbin/tool -> /sbin/tool`, `sbin/tool` 32000 B `9ba4c7e1…22b1` | `usr/sbin/tool -> /sbin/tool`, `sbin/tool` 28000 B `25392f83…15b0` |
| in-tree relative symlink | `bin/busy`, plus `usr/share/web/current -> index.html` | `bin/busy`, plus `var/log/current -> messages` |
| absolute symlink resolving inside the tree | `usr/sbin/tool -> /sbin/tool` (resolves to `<root>/sbin/tool`, inside) | same |
| deep regular whose tail equals another regular's full path, different bytes | `opt/x/etc/conf` 96 B `6b5abc69…8e89` vs `etc/conf` 47 B `afc09b9d…aab9` | `opt/x/etc/conf` 120 B `728c0d7e…2bf5` vs `etc/conf` 47 B `3de5066c…bc41` |
| nothing else (no escaping link, no device/fifo/socket) | `escaping_symlinks: 0`, `special_files: 0` | same |

Supporting files: L3 `etc/version`, `etc/init.d/rc.S`, `usr/lib/libcore.so` (90000 B, multi-block data),
`usr/share/web/index.html`, `usr/share/doc/LICENSE`, `lib/modules/kmod.ko`, `var/lib/state.dat`,
`var/tmp/empty` (0 B), `opt/app/config.json`; L4 `etc/hosts`, `etc/fstab`, `usr/sbin/init`,
`usr/lib/libssl.so` (70000 B), `usr/share/doc/README`, `var/log/messages`, `var/lib/db.bin`,
`var/tmp/empty` (0 B), `root/.profile`, `opt/x/data.bin`.

The builder asserts each of these structurally before writing (`check_spec`): file count, both collision
suffix relations, the deep-tail suffix relation **and** that the two contents differ, exactly one absolute
link, at least one relative link, every link resolving inside the tree as a consumer would resolve it, and
every parent of every entry being a real directory. A violated spec is exit 2 with a named problem, not a
silently different tree (exercised: an early `/sbin/tool` resolution bug in my own check was caught this
way and fixed, log-less but visible in the tool's history — the final runs never reach that branch).

`bin/busy` and `usr/bin/busy` are genuinely two entries: the oracle lists `usr/bin/busy` as a regular file
with its own sha256 and `nonregular.tsv` lists `bin/busy` as a symlink to `../usr/bin/busy`. Nothing on
disk resolves one to the other (log §15).

## 3. Genuine AVM layout: superblock, marker, little-endian block-length chain

Independent proof by `probe-avm-chain.py` (stdlib `struct`/`lzma`/`zlib`; no sqfs-list, sasquatch or unblob
code), log §7, `probe.json`:

| Field (read big-endian) | L3 | L4 |
|---|---|---|
| magic / version | `sqsh` / 4.0 | `sqsh` / 4.0 |
| inodes | 37 | 35 |
| `mkfs_time` | 187892 | 169545 |
| `bytes_used` | 187892 (= file size) | 169545 (= file size) |
| block_size / block_log | 4096 / 12 | 4096 / 12 |
| compression id | 4 (xz) | 1 (gzip) |
| root_inode | 1379 | 1305 |
| inode_table / dir_table / id_table start | 185753 / 187166 / 187884 | 167553 / 168892 / 169537 |
| root inode decodes BE as dir, mode 0755 | PASS (`type=1`, `0o40755`) | PASS |

`mkfs_time == bytes_used` **and** `bytes_used == file size` on both — the AVM marker, and the carrier is
carved at `bytes_used` (no trailing bytes).

Metadata block-length chain, walked twice per region (log §7):

| Region | LE walk (stored, uncompressed blocks) | BE walk |
|---|---|---|
| L3 inode table 185753..187166 | 1 block, 1411 B decoded, ends exactly at the boundary | first size 901 (plausible!) then block 1 "truncated: want 16877 got 1234 at 186656" → does **not** fit |
| L3 directory table 187166.. | 1 block, 710 B decoded, exact | first size 18050 > remaining 724 → immediate truncation |
| L3 id table | 1 block, 4 B decoded, exact | first size 1152 > remaining 12 |
| L4 inode table 167553..168892 | 1 block, 1337 B decoded, exact | first size 14725 > remaining 1990 |
| L4 directory table 168892.. | 1 block, 637 B decoded, exact | first size 32130 > remaining 651 |
| L4 id table | 1 block, 4 B decoded, exact | first size 1152 > remaining 12 |

**Calibration note (worth keeping):** on the L3 inode table the BE reading of the first block-length
header is `901` — inside the 0…8192 plausibility window — so a *size-only* endianness test would accept the
BE interpretation. Only the chain test (where the next block header lands) and the decode test decide.
That is exactly the class of shortcut a counter-side endianness check could take, and these bytes punish it.

Three independent corroborations, all recorded in the log:

1. `tools/round-40/sqfs-list.py --layout avm --inspect` (frozen reader, its own parser): `layout=avm`,
   `header_endian=little`, `avm_marker=true`, `block_length_signal=layout-avm`, counts as in §1/§2 (§4).
2. `--layout auto` (reader decides the header endianness itself from `2 + len + inode_table_start ==
   directory_table_start`, i.e. the `exact` signal): also `layout=avm`, `header_endian=little`, and its
   `--files` output is byte-identical to the committed oracle (§6 of the log).
3. Negative controls, both must fail and both do: reader `--layout be` exits 2 (`metadata offset 1379
   beyond block 185753 (len 901)` for L3; `metadata body out of bounds: offset 167555 length 14725, image
   169545 bytes` for L4); `sasquatch-v4be -be -f -n` exits 1 with `read_id_table: failed to read id table
   block` + `FATAL ERROR: File system corruption detected`, extracting 0 entries (log §9, §12).

`sasquatch-v4be` (no `-be`) prints `SquashFS version [1024.0] / inode count […] suggests a SquashFS image of
a different endianess` and then `Successfully decompressed …` before extracting cleanly. That is the tool's
unchanged behaviour on every lane-built image, identical wording to round 40
(`.ufo/waves/round-40/w2/artifacts/R40W2ReproL/sasquatch-runs.txt`, L1/L2) — not a property of these bytes.

## 4. Oracle, and the exact cross-check against a direct sasquatch extraction

Oracle and non-regular tables come from the round-40 reader in round-40 grammar, `--layout avm`
(log §4, §5), and are byte-reproducible: two runs produce identical `oracle.tsv` and `nonregular.tsv`
(`cmp` exit 0 both carriers).

Cross-check (`xcheck.py`: every oracle row must exist as that exact relative path with the same sha256 and
size; every non-regular row must exist with the same kind and, for symlinks, the same target; nothing extra
on disk), against `sasquatch-v4be -f -n -d ROOT carrier.sqsh` — no `-be`, the argv unblob 26.6.4
`squashfs_v4_be` uses:

```
L3  sasquatch exit 0: created 13 files, 21 directories, 3 symlinks, 0 devices/fifos/sockets/hardlinks
    xcheck: files=13 symlinks=3 dirs=20 oracle=13 nonregular=23 mismatches=0   [exit 0]
L4  sasquatch exit 0: created 14 files, 18 directories, 3 symlinks, 0 devices/fifos/sockets/hardlinks
    xcheck: files=14 symlinks=3 dirs=17 oracle=14 nonregular=20 mismatches=0   [exit 0]
```

`created 21 / 18 directories` = the 20 / 17 non-root directory rows plus the extraction root itself; the
`--max-depth 1` REA extract root plays the same role. Zero-size `var/tmp/empty` survives in both (row
`e3b0c442…b855`, 0 bytes, extracted as a regular file).

Fixture hygiene for an **exact** path test (log §17): both tables pass a path-grammar check (relative,
normalised, no `..`, no `//`, no trailing `/`), the regular and non-regular tables are disjoint
(`overlap=0`), every regular's and symlink's parent chain is a listed directory row, and the number of
*deliberate* suffix hazards is 2 per carrier —

```
L3 rows=13/23 overlap=0 suffix_hazards=2 problems=0
L4 rows=14/20 overlap=0 suffix_hazards=2 problems=0
```

(one regular-path-ends-with-symlink-path, one symlink-path-ends-with-regular-path), plus the deep-tail pair
`opt/x/etc/conf` / `etc/conf` which is a third suffix relation but between two regular rows. A matcher with
the round-40 `same_rel` semantics misreads **both** collisions on these bytes:

```
'usr/bin/busy'.endswith('/bin/busy')      -> True     (regular read as the symlink; the R40-CL1 defect)
'usr/sbin/tool'.endswith('/sbin/tool')    -> True     (symlink read as the regular; the mirror direction)
'opt/x/etc/conf'.endswith('/etc/conf')    -> True     (deep file read as the shallow one)
```

so these carriers are precisely the red cases the round-41 counter's exact-relative-path tests must reject
suffix matching on — in both directions, not only the round-40 direction, and with a distinct-content
deep-tail pair so a suffix hit is also a *sha256* miss, not only a path hit.

## 5. Determinism

* Two independent builds into two empty dirs: `cmp` exit 0 for both carriers; identical sha256
  (log §1, §2).
* In-tool check `--builds 2` (third empty dir): both report `build2-equal` and would exit 4 otherwise
  (log §3; the code path is exercised by the run, the failure branch was reviewed not triggered).
* Clock/mtime independence: the L3 source tree was copied, every entry's mtime forced to
  2001-02-03T04:05:06, and the writer re-run **directly** — the image is byte-identical
  (`04cfb4cd…45a3`, log §3b). Inode timestamps are the writer's fixed `MKFS_TIME`, `mkfs_time` is derived
  from `bytes_used`, and file bytes are fixed literals or label-seeded sha256 streams: nothing reads the
  clock or `/dev/urandom`.
* Writer and reader identities are pinned in the log (§0) and in `carriers.json`; both equal the base
  commit bytes.

## 6. Handoff for L1 (integration)

1. Copy `mk-l-carriers.py` to `tools/round-41/mk-l-carriers.py` (the builder's default writer path points at
   `tools/round-40/gen-squashfs.py`, which the round-41 draft explicitly names as the writer).
2. Create `corpus/evidence/round-41/c1/L3/` and `.../L4/` with `carrier.sqsh`, `oracle.tsv`,
   `nonregular.tsv` (the carrier and both tables are what the predicate binds; `inspect*.json` are
   optional corroboration and may stay in this artifacts dir).
3. Merge the two entries from `carriers.json` into `.ufo/waves/round-41/c1/carriers.json`. The fragment
   carries `id`, `path`, `sha256`, `size`, `kind`, `compression`, `layout`, `build`, `oracle`,
   `nonregular`, `counts`, `*_sha256`, and a `features` block naming the four hazard paths so a reviewer can
   re-derive the red cases without reading the builder.
4. Rebuild command for the frozen record: `python3 -I -B tools/round-41/mk-l-carriers.py OUT --builds 2`
   must print `04cfb4cd…` (L3) and `4c0e5459…` (L4) and exit 0; a mismatch is exit 4.

## 7. Limits, and what is deliberately not measured here

1. **No REA and no unblob run on L3/L4** — the item forbids it and the claim needs the carriers untouched
   before the freeze. So there is no `after.json` / `run.json` for these carriers from this seat; the
   post-freeze seat that mints receipts must produce them. My "no REA touched them" claim is therefore
   by-construction, not by a scan of receipts.
2. The expected gap set (`1 depth-limited + 3 unpublished-entry`, no `unknown-chunk-handler`, no special
   files under `--max-depth 1` and the round-40 gap rule) is **[INFERENCE]** from the round-40 L1/L2
   receipts' shape plus the reader's `symlinks: 3 / special_files: 0 / escaping_symlinks: 0`. It is marked
   as such in `carriers.json` and must be re-measured, not trusted, by the receipt seat.
3. Single metadata block per table (both carriers) — the LE length field is exercised on three regions per
   carrier (inode, directory, id), but not on a multi-block table. The round-40 writer's own `--selftest`
   covers the multi-block LE header path on a 400-file tree; I did not re-run it. If the freeze wants
   multi-block coverage on a carrier, it needs a much larger tree (and would exceed the 1 MB lane budget).
4. No fragments, xattrs, devices, fifos or sockets are emitted by the writer; these carriers cannot speak
   to those paths (round 40 had the same limit).
5. My `probe-avm-chain.py` decompresses only ids 1, 2, 4; both carriers use 4 and 1. The `--layout be`
   control's *first-block* plausibility on the L3 inode table is 901 (see §3), so I state the endianness
   conclusion from the chain test, not from a size window.

## 8. Calibration notes

* **What would falsify this delivery:** any of — a second build differing in sha256; `probe-avm-chain.py`
  reporting `mkfs_time != bytes_used` or a BE chain landing exactly on a boundary; `sasquatch-v4be` (no
  `-be`) extracting anything that disagrees with the tables; an extracted path that resolves `bin/busy`
  into `usr/bin/busy`; the reader's `--layout avm` and `--layout auto` disagreeing on layout or output.
  None occurred; every one of the above has a recorded PASS line in `build-log.txt`.
* **Where these bytes are load-bearing:** they are the only two carriers in the round-41 set that can
  distinguish an exact path test from a suffix test, and they do it in both directions plus a
  distinct-content deep-tail pair. A counter that merely dropped the round-40 `same_rel` and re-used a
  normalised-prefix test on the *other* side would still trip direction B.
* **Cost of a mistake here:** the carriers are byte-pinned in `carriers.json`; any later edit to the tree
  spec changes both sha256 values and invalidates the fragment. Change them only by re-running the builder
  and updating `carriers.json`, the manifest and this report together.
* The `/sbin/tool` absolute target is resolved by my checker the way a consumer resolves it (re-rooted at
  the extraction root). If the freeze's own checker resolves absolute targets on the *host* filesystem
  instead, it will report an escaping link on an image that contains none — worth a line in the counter's
  selftests.

---

Reproduce everything: `build-log.txt` §0–§17 lists every command, its exit code and its output, in order.
Scratch paths in it are gone by design; the bytes it cites are the sha256-pinned files in this directory.
