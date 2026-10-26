**DEFECTS FOUND** — carrier K5 is built, oracle-frozen-ready and verified by `sasquatch-v4be`, but it
cannot be produced by the pinned `tools/round-37/gen-squashfs.py`: that generator corrupts every
non-ASCII directory entry (evidence and one-line fix in §7). K5 was built with an artifacts-local
generator that is byte-identical to stock for ASCII trees (K1/K2 pins rebuild exactly).

# R39-C1 carrier K5 — standard big-endian SquashFS v4, gzip

Seat `R39C1CarrierK5`, wave 1 (pre-freeze). Base `a2f64e1da78afcf8cc39287106604dbcc270844c`.
Nothing was run through REA or through unblob on K5; no VCS state was touched; no tool was
installed or upgraded.

## 1. Deliverables

All under `.ufo/waves/round-39/w1/artifacts/R39C1CarrierK5/` (ready to copy to
`corpus/evidence/round-39/c1/K5/`; `src/` is what an oracle re-derivation reads, the `.py`/`.sh`
files are not needed in `corpus/`).

| file | sha256 | notes |
|---|---|---|
| `carrier.sqsh` | `5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228` | 26813 bytes, 24 inodes |
| `carrier.sqsh.sha256` | — | `sha256sum` output (`5999…  carrier.sqsh`) |
| `oracle.tsv` | `651cb7e3fc83b829fd425f866ed4d22bce910bc83316b3d772ea70e5075fc2d7` | 10 rows, TAB `path\tsha256\tsize` |
| `symlinks.tsv` | `9d7c1b6a4bc9e41d5735ae13131b03c962c8e0a23dd881853337a3991ffea2f3` | 3 rows, TAB `path\ttarget\tin-tree\|escaping` |
| `src/` | manifest `6560db9a…` (names/modes/targets), `249d8670…` (content) | 10 files, 3 symlinks, 11 dirs |
| `build.sh` | `a5a7e2666a8c69e8f40c04a187d2b9bd9ecb263a1e315cbcde466b521c2fb902` | exact rebuild commands |
| `make-tree.py` | `b6e55cf71928895e7ba8dface57d92c811d11f06195ff3283bec466eb6e80353` | deterministic tree author |
| `make-oracle.py` | `85a433980e5b9ca150e7c6790d7c50e48af96dc7258b2e60344ff31897ef0813` | writes both tables + constraint report |
| `gen-squashfs.py` | `833a40a98713a64a9afd88d4ff526a036afc0a260624b0c3e352b1471e96a099` | stock `1c7c5e88…` + one-line name_size fix |
| `oracle-from-image.tsv`, `symlinks-from-image.tsv` | `651cb7e3…`, `9d7c1b6a…` (identical to the frozen tables) | tables re-derived from the built image, §4 |
| `dev-check.txt`, `determinism.txt`, `tool-versions.txt`, `oracle-crossderive.txt`, `stock-rebuild-check.txt`, `dev-probe.txt`, `dev-probe.sh`, `dev-probe-unblob-traversal.log` | — | retained evidence, §4/§5/§6/§7/§8 |

`carriers.json` fragment for the freeze (`sha256` is the pin; K5 has no pre-freeze REA receipt):

```json
{"id": "K5", "kind": "synthetic standard-BE v4 gzip (tree5: 4 dir levels, 10 files, 0-byte file, 20000-byte PRNG file, space + UTF-8 names; both symlink classes in one image: 2 in-tree + 1 escaping)",
 "path": "corpus/evidence/round-39/c1/K5/carrier.sqsh",
 "oracle": "corpus/evidence/round-39/c1/K5/oracle.tsv",
 "symlinks": "corpus/evidence/round-39/c1/K5/symlinks.tsv",
 "sha256": "5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228",
 "symlink_counts": {"in_tree": 2, "escaping": 1, "dangling_in_tree": 0},
 "writer": "gen-squashfs.py sha256 833a40a98713a64a9afd88d4ff526a036afc0a260624b0c3e352b1471e96a099 (= tools/round-37 1c7c5e88… + name_size byte fix)",
 "writer_stock_sha256": "1c7c5e88324d64ad5935e81f205a609a8361466e5aea9ba461575f4e01ba8dd5"}
```

`symlink_counts` is machine-checkable straight from `symlinks.tsv` (`in-tree`/`escaping` tallies);
per peer `R39C1AxisFit` the counter should assert `in_tree >= 2` and `escaping >= 2` across the
frozen set with at least one carrier at `in_tree == 2`, so the counts belong in carriers.json rather
than only in this report. The claim-bearing part of K5's `kind` is that **both link classes coexist
in one image** (2 in-tree gaps + 1 removal that must produce no gap), not the raw tallies.

The `writer` field is load-bearing: the lane's stock generator rebuilds this tree to a different
image — own measurement `7bd4a42d90331dbdc02705bf89123fdb2d02f4028368c03ff8108212737c584d`,
rejected by `sasquatch-v4be -be -ll` with "File system corrupted: invalid characters in name"
(§7) — so provenance for K5 needs the writer hash that was actually used until the fix lands.

## 2. Carrier identity

Superblock read back from the committed bytes (little Python parse, big-endian field order):

```
magic=b'sqsh' inodes=24 mkfs=1700000000 block_size=4096 frag_idx=0 comp=1 log=12 flags=0 ids=1 version=4.0
root_ref=0x32e bytes_used=26813 file_len=26813
inode_tab=0x6371 dir_tab=0x66c1 frag_tab=0xffffffffffffffff export_tab=0xffffffffffffffff
```

Standard big-endian v4 (`hsqs` byte-swapped to `sqsh`), gzip (`comp=1`), 4096-byte blocks,
`bytes_used == file size` (no trailing padding — a padded variant already exists as K3).
No fragment table and no export table: the generator does not write them (documented limitation),
so every file is block-encoded and the 20000-byte file is genuinely 5 data blocks
(`unsquashfs` reports "13 inodes (14 blocks) to write"; 1+1+0+1+1+1+1+2+5+1 = 14).

## 3. Source tree

```
src/
  README.txt                                      148
  empty.flag                                        0     <- 0-byte regular file
  notes with space.txt                             34     <- ASCII space in the name
  config/app.conf                                  54
  usr/share/demo/notes.txt                         30     <- same-directory link target
  usr/share/demo/link-notes -> notes.txt                  <- in-tree, same dir
  usr/share/demo/link-blob  -> ../opt/blob.bin            <- in-tree, via `..`, sibling dir
  usr/share/demo/escape     -> ../../../../etc/shadow     <- escaping (4 `..`, dir depth 3)
  usr/share/demo/assets/manifest.json              58
  usr/share/demo/assets/icons/アイコン.txt           37     <- UTF-8 non-ASCII name
  usr/share/opt/blob.bin                         5000     <- PRNG
  var/lib/state.db                              20000     <- PRNG, 5 x 4096 blocks
  var/log/last.log                                 18
```

Constraint check printed by `make-oracle.py`:

```
regular_files=10 symlinks=3 dirs=11
zero_byte=1
gt_3_blocks=['var/lib/state.db']
space_name=['notes with space.txt']
non_ascii_name=['usr/share/demo/assets/icons/アイコン.txt']
dir_depth_max=4
link usr/share/demo/escape -> ../../../../etc/shadow [escaping] resolved=/etc/shadow
link usr/share/demo/link-blob -> ../opt/blob.bin [in-tree] resolved=/usr/share/opt/blob.bin
link usr/share/demo/link-notes -> notes.txt [in-tree] resolved=/usr/share/demo/notes.txt
empty_dirs=[]
in_tree_links=2 escaping_links=1
```

No absolute symlink, no hardlink, no device/FIFO/socket node, no empty directory
(`find … -type b/c/p/s`, `-links +1` return nothing). Every symlink targets a **file**: the
generator walks with `followlinks=False`, so a link whose target is a directory lands in `dnames`
and is silently dropped from the image (measured independently by peer `R39C1AxisFit`), which would
have turned a 3-link oracle into a 2-link carrier. K5 avoids that shape by construction, and the
image listing carries all three links (§5). `blob.bin`/`state.db` are SHA-256
counter-mode PRNG output keyed by `kaidoku-r39-c1-k5:<path>:<i>` — not `random`, so they are
stable across Python versions; the tree contains no host path, clock or locale input.

## 4. Frozen oracle tables

`oracle.tsv` (regular files only, UTF-8, C-collated, LF, no header, exactly the K2 column shape):

```
README.txt	f649d29ac7069ddb273cb29b941a02292a96407d190b81facc69ad4589b8b0e8	148
config/app.conf	1a64be63eb5cbc4408ade9a66692b3944729a0935de219a4a038892b3ca833b6	54
empty.flag	e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855	0
notes with space.txt	8d68ae9e930f226b6c4f5578e0cb7b3e9edbd4b05c25685f31334dabf09f44d1	34
usr/share/demo/assets/icons/アイコン.txt	f48693f92b3b74feba8255f91fe35cb115b39186c45d763b39f9c308ee070ba2	37
usr/share/demo/assets/manifest.json	5dd83cc19da1cb9b191ef8c271b5c446af7acd08c7b4e5aa7bf2f667942ef4fa	58
usr/share/demo/notes.txt	4664d8139fba1632f2a9084d3855d732028caf14eb3602351884c7661e06f0a9	30
usr/share/opt/blob.bin	4336d9833b074d112e4eb630851d8dd87b94e2c860a15c2bfe5ad6695247d474	5000
var/lib/state.db	a9d330f29bc255930ee5b0d77f28985ba33d69fae22b1fd67d7e5692a76badc2	20000
var/log/last.log	12afa793045ebacf2dd903ac7fc22e807da2719648f07625fdbd351dbbe27a5f	18
```

`symlinks.tsv`:

```
usr/share/demo/escape	../../../../etc/shadow	escaping
usr/share/demo/link-blob	../opt/blob.bin	in-tree
usr/share/demo/link-notes	notes.txt	in-tree
```

Resolution rule implemented in `make-oracle.py` (documented there): the link's directory is a
stack of components; `""`/`.` are skipped and `..` pops; a `..` popping an empty stack is an
escape. This is the lexical form of unblob 26.6.4's realpath test
(`unblob/extractor.py:67-87` relative target → `target = path.resolve()`;
`unblob/file_utils.py:34-39` `is_safe_path`), which cannot clamp at the image root because the
extraction root has real parents. Independence: `oracle.tsv` was also recomputed straight from
`src/` with `hashlib` and compared byte-for-byte (`oracle_matches_src_recompute: True`), and both
tables pass `LC_ALL=C sort -c`.

**Cross-derivation from the built image** (peer-review point from `R39C1AxisFit`: a `src/`-derived
oracle can predict entries the image does not hold). The tables were re-derived a third time from
`sasquatch-v4be -be -ll carrier.sqsh` plus the extracted bytes, i.e. from the carrier as shipped,
and compared byte-for-byte with the frozen tables:

```
image-derived files: 10 links: 3
ll size vs extracted size mismatch: []
ll target vs disk target mismatch: []
  usr/share/demo/escape     -> ../../../../etc/shadow [escaping] disk_target=../../../../etc/shadow resolved=/etc/shadow
  usr/share/demo/link-blob  -> ../opt/blob.bin        [in-tree]  disk_target=../opt/blob.bin        resolved=/usr/share/opt/blob.bin
  usr/share/demo/link-notes -> notes.txt              [in-tree]  disk_target=notes.txt              resolved=/usr/share/demo/notes.txt
oracle: IDENTICAL        (651cb7e3… both)
symlinks: IDENTICAL      (9d7c1b6a… both)
```

The image-derived copies are kept as `oracle-from-image.tsv` / `symlinks-from-image.tsv`, with the
hashes in `oracle-crossderive.txt` and the transcript appended to `dev-check.txt`.

## 5. Dev check (sasquatch-v4be 4.5.1 only — the permitted method)

```
$ sasquatch-v4be -be -ll carrier.sqsh                       # exit 0, all 24 entries listed
$ sasquatch-v4be -be -no-exit-code -f -d $S/x2 carrier.sqsh # exit 0
   created 10 files, 11 directories, 3 symlinks,
   created 0 devices, 0 fifos, 0 sockets, 0 hardlinks
$ find $S/x2 -type l -printf '%P -> %l\n'
usr/share/demo/escape -> ../../../../etc/shadow
usr/share/demo/link-blob -> ../opt/blob.bin
usr/share/demo/link-notes -> notes.txt
```

Per-file comparison of the extraction against `oracle.tsv`: 10/10 rows `OK` on path, sha256 and
size; no file on disk outside the oracle (`extra: []`, `missing: []`); `comparison_fail=0`
(full transcript in `dev-check.txt`). The UTF-8 name round-trips byte-identically, and the
20000-byte file extracts to its source sha256.

## 6. Determinism

`build.sh` was run in the artifacts dir and again in three independent scratch directories
(`$S/detA`, `detB`, `detC`, each with only the build scripts copied in, so `make-tree.py`,
`gen-squashfs.py`, `make-oracle.py`, `build.sh` had to regenerate everything):

```
artifact : 5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228
detA     : 5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228  rc=0
detB     : 5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228  rc=0
detC     : 5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228  rc=0
src manifest names 6560db9a…/content 249d8670… identical in all four trees
```

Host-path leakage probe inside the image bytes: `/fast/scratch` 0, `kaidoku-shokunin` 0, `.ufo` 0,
`R39C1` 0, `2026-` 0 hits (`determinism.txt`).

## 7. DEFECT (blocking, in the pinned tool): non-ASCII names corrupt the image

`tools/round-37/gen-squashfs.py` writes a directory entry's `name_size` from the character count
while writing UTF-8 bytes:

```python
pack(e, 'H', len(name) - 1)      # stock: characters
tbl += entry + name.encode()     # stock: bytes
```

Any directory holding a non-ASCII name is then unreadable. Minimal reproduction (stock generator,
one file named `アイコン.txt`, 2 inodes):

```
$ python3 tools/round-37/gen-squashfs.py $S/probe/uni1 $S/probe/uni1.sqsh --endian be --comp gzip
$ sasquatch-v4be -be -ll $S/probe/uni1.sqsh
get_metadata: failed to read block
FATAL ERROR: dir_scan: failed to read directory squashfs-root      exit=1
```

Same failure with the name only in a subdirectory (error names the parent: `failed to read
directory squashfs-root/sub`). On K5's own tree the stock generator produces a different 26813-byte
image (`7bd4a42d90331dbdc02705bf89123fdb2d02f4028368c03ff8108212737c584d`) that dies one entry
earlier, inside the icons directory:

```
$ sasquatch-v4be -be -ll $S/stock-rebuild.sqsh
File system corrupted: invalid characters in name
FATAL ERROR: dir_scan: failed to read directory squashfs-root/usr/share/demo/assets/icons   exit=1
```

Both messages are the same defect: `name_size` short by 7 bytes for `アイコン.txt` makes
`unsquashfs` read a truncated, invalid name. Consequence: the required UTF-8-name carrier is
unbuildable with the pinned command, and K2's `carriers.json` note "tree2, symlink + unicode name"
is inaccurate — `K2/src` contains only `space name.txt`; no committed carrier has ever exercised a
non-ASCII name.

Fix applied in the artifacts-local copy (one hunk, `gen-squashfs.py:146-149`):

```python
nb = name.encode()
entry = (pack(e, 'H', o) + pack(e, 'h', ino - first_ino) +
         pack(e, 'H', typ) + pack(e, 'H', len(nb) - 1))
tbl += entry + nb
```

Equivalence proof — both generators rebuild the committed K1/K2 carriers byte-identically from
their `corpus/.../K*/src` trees:

```
K1 committed 1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e
K1 stock     1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e
K1 fixed     1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e
K2 committed 403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154
K2 stock     403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154
K2 fixed     403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154
```

Decision for the L1 (integration owner): either (a) ship the fixed generator in
`tools/round-39/` (recommended — it is the only way to keep the UTF-8-name coverage, and it is
proven output-identical for ASCII trees, so K1/K2 provenance is untouched), or (b) keep
`tools/round-37` untouched and freeze K5's bytes as committed, regenerating only from the
delivered `src/` with the artifacts-local generator (then `build.sh` must stay next to
`gen-squashfs.py`). Do not weaken K5 by dropping the non-ASCII name without saying so in the
claims: `corpus/evidence/round-37/c1/K2` already claims unicode coverage it does not have.

## 8. Symlink rule — dev-probe evidence for the C1 predicate

K5 itself was never given to unblob or REA. The rule was confirmed on a separate development
carrier built in scratch from a different tree (`dev-probe.sh`, `dev-probe.txt`), and by running
unblob 26.6.4's own `fix_symlink`/`is_safe_path` logic over K5's extracted layout:

```
# K5's extracted layout, unblob algorithm (relative target -> path.resolve(); safe iff inside outdir)
usr/share/demo/escape     -> ../../../../etc/shadow   [REMOVED] resolve=<scratch>/etc/shadow
usr/share/demo/link-blob  -> ../opt/blob.bin          [kept]    resolve=<root>/usr/share/opt/blob.bin
usr/share/demo/link-notes -> notes.txt                [kept]    resolve=<root>/usr/share/demo/notes.txt
# calibration against ground truth: same algorithm on K1's tree
link-to-hello -> ../hello.txt                         [REMOVED] resolve=<scratch>/rebuild/hello.txt
```

K1's removal is the round-38 observation ("Path traversal attempt through symlink, removing …
target=hello.txt", `corpus/evidence/round-37/c1/K1` sanitised to 0 links), so the simulation is
calibrated. Independent unblob run on the dev carrier (V4BE, 3-component link directory, 4 `..`
plus in-tree links plus a UTF-8 name):

```
2026-10-26 ... [error] Path traversal attempt through symlink, removing pid=998273 target=etc/shadow
surviving: deep/a/b/same-dir -> Überblick-設計.txt
           deep/a/b/via-dotdot -> ../side/target.bin
           deeper/a/b/c/inside -> ../../../../etc/shadow   (4-component dir: same 4 `..` stays inside, kept)
published: deep/a/b/Überblick-設計.txt 19 bytes, sha256 == source
```

Two things this pins for the freeze: the split is the `..` count relative to the image root (not
target existence, not depth alone), and unblob's rewrite step preserves both in-tree targets
verbatim (`relpath` of the resolved target from the link's parent is the original string), so
K5's `symlinks.tsv` targets are exactly what survives to disk.

Corroboration from peer `R39C1AxisFit` (their probes, not mine): a dangling target **inside** the
root is kept and yields a gap, so target existence is irrelevant to the in-tree/escaping split;
absolute targets are kept by unblob after re-rooting (`/etc/passwd` → `etc/passwd`, one gap) —
K5 carries none, as planned; and gap cardinality is per kept link (their 3-kept-link image yielded
3 `unpublished-entry` gaps). K5 therefore expects exactly **2** gaps, one per in-tree link, and
K5 deliberately has no dangling in-root link, so the gap set cannot grow beyond the two rows in
`symlinks.tsv` marked `in-tree`.

Expected K5 receipt shape [INFERENCE — no REA run on K5 this wave, by rule]:
handler `squashfs_v4_be`, 10 published regular files matching `oracle.tsv` by path suffix and
sha256, exactly two `unpublished-entry` gaps at
`firmware.bin_extract/usr/share/demo/link-blob` and
`firmware.bin_extract/usr/share/demo/link-notes` (prefix per round-38 P1's `relative_path`), no
path for `usr/share/demo/escape`, no `MaliciousSymlinkRemoved`-derived gap (round-38 P2/K1: the
removal produces a diagnostic only), subject digest `5999eafc…`.

Peer `R39Sentinel` independently extracted the committed `carrier.sqsh` with `sasquatch-v4be -be
-d` and matched all 10 oracle rows on sha256+size with no extra regular files, and independently
reproduced the §7 defect (stock generator → different image `7bd4a42d…`, rejected with "File
system corruption: invalid characters in name").

## 9. Risks / open points for the L1

1. §7 defect decides how K5 is reproducible after the freeze; the frozen artifact is the carrier
   bytes, so the pin stands either way. Stock rebuilds the same tree to `7bd4a42d…` (rejected by
   `sasquatch-v4be`), so the `writer` hash in the carriers.json fragment is what makes provenance
   checkable; recorded independently by `R39Sentinel`.
2. K5 is a generator prototype image: no fragments, no export table, no xattrs, no sparse files.
   The C1 predicate only asserts handler/gaps/files, so this is in scope; it is not an
   AVM-BE or vendor-mangled image, which C1 explicitly does not claim.
3. The escaping target is `etc/shadow`: it escapes to the extraction root's *parent* and unblob
   unlinks the link. My dev probe left nothing at `<scratch>/etc` (checked: 0 entries).
   Absolute targets are a different class and are **not** escaping under unblob 26.6.4
   (`extractor.py:74-75` strips the leading `/` and checks only the remainder, so `/etc/passwd` is
   kept as metadata and rewritten to `etc/passwd`; measured by peer `R39C2Triage` §5.3-5.5). K5
   carries no absolute target at all: `make-oracle.py` refuses one (`resolve()` raises on a target
   starting with `/`), and the tree was authored relative-only, so the frozen rule's two classes
   are exhaustive for this carrier. Related: REA's `unpublished_entries[].link_target` is the
   rewritten target, so an oracle comparing raw target text stays correct here only because both
   in-tree targets came back verbatim through unblob's rewrite step (§8).
4. `unblob.log` is truncated per invocation, so `dev-probe-unblob-traversal.log` holds only the
   last run's line; the per-run extracted trees in `dev-probe.txt` are the durable evidence.
5. `src/` modes are 0644/0755 from `umask 022`; the generator hardcodes modes in the image, so
   they do not affect the carrier pin.
6. Freeze-side asks from peer review: put `symlink_counts` (`in_tree`/`escaping`) in
   `carriers.json` so the counter can assert `in_tree >= 2`, `escaping >= 2` over the frozen set
   with one carrier at `in_tree == 2`; and keep the dual table pair — `src/`-derived tables as the
   independent statement of intent, plus an assert that the image matches them — because
   image-only derivation cannot see a silently dropped entry (the generator drops directory-target
   links, measured by `R39C1AxisFit`). K5 satisfies both: 10/10 + 3/3 rows identical from either
   side, so the assert can only fail if a future tree grows that shape.

## 10. Tooling

No installs, upgrades or package-manager transactions were performed (pacman is paused host-wide;
nothing needed it). Tools used as found: `sasquatch-v4be` 4.5.1
(`sha256 fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`), unblob 26.6.4
(dev probe only), Python 3.14.8. `tool-versions.txt` records the versions and both generator
hashes.

Scratch `/fast/scratch/hyaku/kaidoku-r39/R39C1CarrierK5` was removed after the evidence above was
copied into this artifacts directory; no cited path lives outside the lane.
