# R41C1Collide — path collisions, REA publication shape, and the two matchers

**Verdict: DEFECTS FOUND.** The seat hypothesis is CONFIRMED on six fresh AVM-genuine carriers
(REA 6.5.0 publishes a regular file at exactly `<chunk>_extract/<rel>` and never a symlink path, in
both collision directions), but the draft's matcher fix is under-specified: the prototype's
"strip the first `_extract` component" rule false-FAILs every oracle row on a wrapper carrier
(measured 0/3 where extraction is faithful), and the suffix rule it replaces is wrong in *both*
directions, including a gap-resolution direction the prototype's selftest does not cover.

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `49096c7e6f226af0c750c4b003be58883cb6049f`.
Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C1Collide` (removed at the end). Leaf seat: no
subagents, no background jobs, no `agent://all`, no VCS mutation. No reserved carrier (FRITZ!Box
3490/5490/5491/7560 images, L3, L4) was read, run, carved or copied; all inputs are fresh
lane-built trees plus the already-burned round-40 development evidence.

## 1. Hypothesis and how it was tested

> REA 6.5.0 publishes a regular file at exactly `<chunk>_extract/<rel>` and never publishes a
> symlink path, even when a symlink path is a suffix of a regular path or vice versa.

Six carriers were built with `tools/round-40/gen-squashfs.py --endian avm-genuine` from fresh
trees (`artifacts/R41C1Collide/build-dev.py`; deterministic, verified by rebuilding into a second
directory and comparing sha256 — all six identical):

| id | comp | tree shape (the collision) | image sha256 | size |
|---|---|---|---|---|
| A-xz | xz | regular `usr/bin/busy` + symlink `bin/busy` → `../usr/bin/busy` (regular path deeper: symlink path is a suffix of it) | `fef3fc128c7c87d4ebfc50d156bae09344e6dde0179f832b8d2b094ab1f2543b` | 70729 |
| A-gz | gzip | the same tree, gzip | `050a477f1c686187fdd1850b5710de5250dd2c4c3ede8fa7458b4e7fc8a1d1ce` | 70729 |
| B-xz | xz | symlink `usr/sbin/tool` → `/sbin/tool` + regular `sbin/tool` (symlink path deeper: reverse direction) | `8d40d56d4f0591b7918aec1c327c746ed577e357aa3e770ca016526676c0687a` | 70726 |
| C-xz | xz | regular `opt/x/etc/conf` + regular `etc/conf`, **identical bytes** (oracle-shadow direction) | `36356f93b5649f3aa18d0146938ecd24ffb701c4a9d20d26007a86631955393f` | 14560 |
| D-xz | xz | **two symlinks whose paths nest**: `sbin/tool` → `../usr/bin/tool`, `usr/sbin/tool` → `/usr/bin/tool`, regular `usr/bin/tool` | `bf6c6975e406bf01cd0ca49679c9cc842e373ffdbd48625ddf832e099e3aaa3c` | 30691 |
| E-xz | xz | A's tree plus a nested AVM-genuine image at `var/filesystem_core.squashfs` (nesting probe) | `a062c5e7fc7533b89f2edfcb61bfbe84025aaa68b429dac237c48e41a79851b4` | 40916 |

Every carrier's superblock is the genuine AVM layout and not standard BE: magic `sqsh`, v4.0,
`mkfs_time == bytes_used`, and the first metadata block-length header is little-endian: on A-xz the
two bytes at the inode table are `0x8193`, read LE they are a 403-byte block that lands exactly on
the directory table start (identity true), read BE they are 4993 and do not (identity false). The
same split holds on all six carriers (`verify.out`).
Cross-check on A-xz: `sasquatch-v4be -f -d …` → rc 0, 3 files + 1 link; `sasquatch -be -f -d …` →
rc 1, 0 files. Handler in every receipt: `squashfs_v4_be`, `extraction_failed: false`.

REA runs (`cd "$S"`, fresh outdir, parent pre-created, `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`,
`npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1`), all rc 0:

| run | evidence_id | coverage | published_bytes |
|---|---|---|---|
| A-xz d1 | `ev_66e487a3ea3cdc3aef0a5c6d228b27a2578edff592f47bc8331b7d70badc2599` | partial | 70029 |
| A-gz d1 | `ev_bc631305df3f1686986d0ae3593bd6ae5e7190ef94b33b67dd5058c0304e97c2` | partial | 70029 |
| B-xz d1 | `ev_a85c7c17d4433a75c9ea5ea642bc01348e0f3e33c8e812b88e61c29aa83b81c1` | partial | 70029 |
| C-xz d1 | `ev_62646c68e7f7ad18387940e395a4f277edc8caa958ea582a7b5ae99b73a82c10` | partial | 14029 |
| D-xz d1 | `ev_ce8676f268deaea5c2b801eb5fc50575456bf592e5b4690f3db771c29e5cd6e3` | partial | 30029 |
| E-xz d1 | `ev_9b4ee61dea8d79636d17aa95c556599e1b823c499b438a36cd05809c5a5ae3dd` | partial | 40315 |
| E-xz d2 | `ev_2b0c82751f2023bed36e4984d58feacdd9d4cec14f96329a4ebe477298f0ae91` | partial | 40334 |
| wrap.tar d2 | `ev_983d3752804a43242344ec3183caec3691032a4ed412a8d85d1283e2230fd9b1` | partial | 140758 |

`verify-publish.py` (H1–H4, see the docstring) prints `HOLDS` for all six carriers, rc 0:

```
A-gz HOLDS root=firmware.bin_extract published=3 truth_files=3 truth_nonreg=6 leaked=[]
     layout=sqsh/v4.0/marker=True/le_len=403(identity=True)/be_len=4993(identity=False)
```

### What the extractor actually did (mechanism, not just the list)

* The staged chunk is named `firmware.bin` by the pipeline, **independently of the input file
  name**: `carrier.sqsh` → `firmware.bin_extract/…`. So the extract root is always one component
  `<staged name>_extract`, and the published path is exactly `root + "/" + <truth rel>` — set
  equality with the source-tree file list, both directions, on all six carriers.
* Symlinks are not merely omitted from the receipt list: they are **absent from the output
  directory**. A-xz's output dir contains `etc/version`, `usr/bin/busy`, `usr/lib/libavm.so` and
  no `bin` at all, while `sasquatch-v4be`'s own extract dir does contain `bin/busy` as a link.
  unblob removes the link, then reports it once under `normalized_result.unpublished_entries`
  (`{"relative_path":"firmware.bin_extract/bin/busy","kind":"symlink","link_target":"../usr/bin/busy"}`)
  plus one `unpublished-entry` gap at the same path.
* Absolute link targets are **rewritten relative** to the entry's directory: B's `/sbin/tool`
  becomes `../bin/tool`, D's `/usr/bin/tool` becomes `../bin/tool`. Nothing scores `link_target`;
  it must stay unscored, because the receipt does not preserve the stored target.
* At depth 2 a nested chunk extracts *inside* the first root:
  `firmware.bin_extract/var/filesystem_core.squashfs_extract/inner/only.txt`.
* The receipt states the mechanism itself: `limitations[2]` of every run ends
  "Extracted code is never executed; only regular files are published, without executable permission
  bits." `normalized_result.diagnostics` is `[]` on all eight runs; the only non-clean signal is
  `coverage: "partial"` with the one `depth-limited` structural gap, exactly as the round-40 gap
  rule allows.

Hypothesis: **CONFIRMED**, in both directions, on xz and gzip, at depth 1 and 2, with no
counterexample in the six carriers.

## 2. The two matchers, scored on live receipts

`score-matchers.py` copies `same_rel` from `tools/round-40/c1-counter.py:606-607` and
`extract_rel`/`same_rel` from the prototype diff verbatim and **asserts AST equality against the
lane text** before scoring (it prints `identity: … AST-identical to the lane text`; rc 1 otherwise).
`oracle_hits`, `nonregular_published`, `gap_check`, `parse_oracle`, `parse_nonregular` are
transcribed from `c1-counter.py:331-382, 610-700` with the one change
`same_rel(...) → m(...)`. The third rule is the correction proposed in §4.

`OK`/`FAIL` below is the clause verdict; a clause FAIL is the only thing that matters, the counts
are context. Full table: `artifacts/R41C1Collide/scores-all.txt` /
`scores-all.json` (sha256 `c3d8737ca25adbf3b948ae6aa15b0d843f7421c3c847a316eecb245097f8125f`).

| receipt | oracle | nonreg (suffix) | gap resolves (suffix) | verdict suffix / proto / fix |
|---|---|---|---|---|
| A-xz d1 | 3/3 all | **FAIL** suffix | OK | FAIL / OK / OK |
| A-gz d1 | 3/3 all | **FAIL** suffix | OK | FAIL / OK / OK |
| B-xz d1 | 3/3 all | OK | OK | OK / OK / OK |
| C-xz d1 | 3/3 all | OK | OK | OK / OK / OK |
| D-xz d1 | 2/2 all | OK | **FAIL** suffix (2 entries) | FAIL / OK / OK |
| E-xz d1 | 3/3 all | **FAIL** suffix | OK | FAIL / OK / OK |
| E-xz d2, outer oracle | 3/3 all | **FAIL** suffix | OK | FAIL / OK / OK |
| E-xz d2, inner-oracle probe | **1/1 suffix** / 0/1 exact | OK | FAIL (probe has no nonreg rows) | suffix false PASS |
| wrap.tar d2, carrier oracle | **0/3 proto** / 3/3 suffix | FAIL suffix | FAIL proto | **proto false FAIL** |
| C-shadow (DERIVED) | **3/3 suffix** / 2/3 exact | OK | OK | suffix false PASS |
| A-materialised (DERIVED) | 3/3 all | FAIL all (correct) | OK | OK |
| A-nogap (DERIVED) | 3/3 all | OK | FAIL all (`required gap absent on ['bin/busy']`) | OK |
| r40-V1 (committed) | 697/697 all | OK all | OK all | OK / OK / OK |
| r40-V2 (committed) | 8/8 all | OK all | OK all | OK / OK / OK |
| r40-L1 (committed) | 7/7 all | OK all | OK all | OK / OK / OK |
| r40-L2 (committed) | 6/6 all | **FAIL** suffix | OK | **FAIL** / OK / OK |

The draft's pre-freeze dry-run sentence ("scores the round-40 V1/V2/L1/L2 receipts 4/4" — four
carriers of four) reproduces on the three path/oracle clauses with the prototype rule, L2
included; the round-40 defect R40-CL1 is visible exactly once, on L2, under the suffix rule. This is *not* the whole predicate: I did not
exercise `carrier_pin_ok`, `layout_ok`, `subject_pin_ok`, `evidence_id_ok`, `projection_ok`,
`receipt_fresh`, `run_provenance_ok` — no rerun/projection work was in this seat.

## 3. Exact receipt lines behind each divergence

```
# A-xz: faithful extraction, suffix rule fails the carrier
files[1]              {"relative_path": "firmware.bin_extract/usr/bin/busy", "size": 40000,
                       "sha256": "4cc70a206f1cab138e897d032d5397e33e41e2b5bcef695bd237fecc88c98f7e"}
unpublished_entries[0]{"relative_path": "firmware.bin_extract/bin/busy", "kind": "symlink",
                       "link_target": "../usr/bin/busy"}
extraction_gaps[1]    {"kind": "unpublished-entry", "relative_path": "firmware.bin_extract/bin/busy", …}

same_rel('firmware.bin_extract/usr/bin/busy', 'bin/busy')                 -> True    (false escape)
extract_rel('firmware.bin_extract/usr/bin/busy')                          -> 'usr/bin/busy'
same_rel_exact('firmware.bin_extract/usr/bin/busy', 'bin/busy')           -> False

# D-xz: the reverse direction, in gap resolution (NOT covered by the prototype selftest)
unpublished_entries[0]{"relative_path": "firmware.bin_extract/sbin/tool", "kind": "symlink",
                       "link_target": "../usr/bin/tool"}
unpublished_entries[1]{"relative_path": "firmware.bin_extract/usr/sbin/tool", "kind": "symlink",
                       "link_target": "../bin/tool"}
extraction_gaps[2]    {"kind": "unpublished-entry", "relative_path": "firmware.bin_extract/usr/sbin/tool", …}

same_rel('firmware.bin_extract/usr/sbin/tool', 'usr/sbin/tool')           -> True
same_rel('firmware.bin_extract/usr/sbin/tool', 'sbin/tool')               -> True   (2 hits)
=> gap_check: "gap path 'firmware.bin_extract/usr/sbin/tool' matches 2 non-regular entries
              ['sbin/tool', 'usr/sbin/tool']"  => gaps_ok False => suffix rule fails the carrier

# C-shadow (DERIVED: the etc/conf publication removed from C-xz's receipt)
files[1] (derived)    {"relative_path": "firmware.bin_extract/opt/x/etc/conf", …,
                       "sha256": "eca4a69e541d…"}      # same sha as the missing etc/conf row
same_rel('firmware.bin_extract/opt/x/etc/conf', 'etc/conf')               -> True    (false oracle hit)
same_rel_exact('firmware.bin_extract/opt/x/etc/conf', 'etc/conf')         -> False

# E-xz depth 2, inner-oracle probe
files[3]              {"relative_path":
                       "firmware.bin_extract/var/filesystem_core.squashfs_extract/inner/only.txt", …}
same_rel(…'…/filesystem_core.squashfs_extract/inner/only.txt', 'inner/only.txt') -> True  (false hit)
same_rel_exact(…)                                                                -> False

# wrap.tar depth 2: the prototype's false FAIL
chunks[0]             {"handler": "tar",             "input_path": "$input"}
chunks[1]             {"handler": "squashfs_v4_be",  "input_path":
                       "$output/firmware.bin_extract/var/tmp/filesystem.image"}
files[1]              {"relative_path":
                       "firmware.bin_extract/var/tmp/filesystem.image_extract/etc/version", …}
extract_rel(…)        -> 'var/tmp/filesystem.image_extract/etc/version'  != 'etc/version'
=> 0/3 oracle rows on a faithful extraction
```

## 4. Defects routed against the draft

**D1 — the prototype's root rule is a property of the carrier's shape, not of the receipt, and it
gives a silent false FAIL.** `extract_rel` drops the first component ending in `_extract` and
nothing else. That is correct exactly while the carrier *is* the squashfs chunk at depth 0 — the
draft's V3/V4/L3/L4 plan (members carved to `bytes_used`, lane-built images), and it measured
correct on all six single-image carriers and on all four committed round-40 receipts. On a wrapper
carrier it drops the wrong root: measured 0/3 oracle rows with `3/3` published faithfully
(`wrap.tar` above). The rule cannot tell "wrong root" from "bad extraction", and it will score a
member's filesystem against a wrapper-level oracle without saying so. Fixable, and the draft should
close it rather than rely on the carriers all being carved.

*Smallest safe correction* (implemented as `exact-carrier-root` in `score-matchers.py`,
`carrier_root`/`same_rel_anchored`): derive the anchor from the receipt, not from path shape —
require a `squashfs_v4_*` chunk with `input_path == "$input"` (the carrier file itself) and use the
single leading component every published and gap path shares as the extract root; refuse the
receipt by name when that chunk is absent (wrapper carrier: the published filesystem is a member,
so a carrier-level oracle is undefined) or when the paths do not share one leading component.
Measured: identical to the prototype on all ten single-image receipts (A/A-gz/B/C/D/E d1/E d2,
V1/V2/L1/L2), and a named refusal instead of 0/3 on `wrap.tar`. It also makes the scope explicit:
files outside the root (a wrapper's own entries, a nested chunk's files) can never satisfy an
oracle row, and the escape check cannot see them either.

**D2 — the suffix rule is wrong in both directions, and the second direction is unmeasured in the
draft and in the prototype's selftest.** Live false FAILs: `nonregular_unpublished_ok` on A/A-gz/E
(regular path deeper than the symlink path — R40-CL1 itself) and **`gaps_ok` on D** (two symlinks
whose paths nest: the gap on the deeper entry resolves to two entries, so the counter rejects a
faithful extraction). False PASSes: nested publication credited to a top-level row (E d2 probe) and
the identical-bytes oracle shadow (C-shadow). The prototype's selftest carries the publication
direction twice (`deep_file`, `shallow_file`) and the *materialised* and *shadow* directions as
must-fail, but it has **no case where the suffix rule fails and the exact rule passes on gaps** —
which is what D is. So `plans/round-41-claims.md`'s "its selftests include both collision
directions" is true for publication and false for gap resolution.

**D3 — L3/L4 must carry the D shape, not only regular/symlink pairs.** The draft asks L3/L4 for
"nested-name collisions in both directions (a regular file whose path ends with a symlink's path,
and a symlink whose path ends with a regular file's path)". Those are A and B. D (two symlinks, one
path a suffix of the other) is a third shape with a different failing clause (`gaps_ok`, not
`nonregular_unpublished_ok`); without it a suffix-like rule could pass every frozen carrier and
still be wrong.

Non-defects, for calibration: the draft's carrier plan (carved single-squashfs images) is
compatible with the prototype rule, and the round-41 port will work as drafted if D1 is either
closed by the clause above or by binding every carrier to `input_path == "$input"`. The
`nonregular_unpublished_ok` check remains load-bearing under the exact rule (A-materialised), and
`required` gaps remain enforced (A-nogap). Porting note, not a defect: `provenance_ok` in
`c1-counter.py:596-604` tests `PROV_SEGMENT = '/kaidoku-r40/'`; round-41 receipts must carry
`/kaidoku-r41/` (mine do: `…/kaidoku-r41/R41C1Collide/out/<id>`).

## 5. What this buys the freeze

1. The C1 predicate's path clause can be stated as a receipt-shape property, not a carrier
   assumption: *the carrier's own chunk is the depth-0 `squashfs_v4_be` chunk (`input_path ==
   "$input"`), its extract root is the single leading path component, and rows match by exact
   equality after that root.* Measured on 10 single-image receipts, incl. all four round-40 ones.
2. The round-41 counter should carry three selftest fixtures the round-40 prototype lacks:
   the gap-nesting case (D), the nested-publication case (E), and the wrapper refusal
   (`carrier_chunk_ok`). The two collision carriers for the draft's pre-freeze dry run should be
   A (publication direction, must pass) and D (gap direction, must fail under suffix) — both are
   reproducible from `build-dev.py` in seconds.
3. Nothing here changes the draft's carrier choice; it changes what the counter is allowed to
   assume about it.

## 6. Limits

* [INFERENCE] The wrapper-carrier risk is measured on a synthetic tar wrapper, not on a vendor
  image (reserved). Whether REA would stage a real AVM wrapper's squashfs member the same way is
  inferred from the tar run and from the `input_path` shapes above; the draft avoids the question
  by carving, and D1's clause makes the avoidance explicit.
* The four committed round-40 receipts were scored, not rerun (no projection/rerun in this seat).
* `gap_check` on V1 compares 697 published files against 381 rows per matcher; the whole 16-case
  matrix runs in ~50 s. No performance concern at the drafted carrier scale.

## 7. Artifacts

`artifacts/R41C1Collide/` — `build-dev.py` (carrier builder), `verify-publish.py` (H1–H4),
`score-matchers.py` (three matchers, AST-identity assertion), `commands.sh` (every command),
`scores-all.txt` / `scores-all.json`, `verify.out`, `matcher-divergence.txt`,
`carriers/<id>/{manifest,oracle,nonregular}.tsv` + `carrier.json` (image shas; binaries are not
copied — rebuild with `commands.sh` §1), `receipts/<run>.after.json` (the `data` envelopes),
`derived/` (three projections + `NOTES.md` naming each one-line mutation), `inner-oracle.tsv`,
`empty-nonreg.tsv`.

Tooling: no install or upgrade. `npx -y rea-agents@6.5.0` (package cache only, `--version` → 6.5.0),
unblob 26.6.4 (`executable_sha256 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`),
`sasquatch-v4be` 4.5.1 and `sasquatch` 4.5.1 used as installed. No pacman transaction; nothing
written to `~/.local/bin` or any PATH directory.
