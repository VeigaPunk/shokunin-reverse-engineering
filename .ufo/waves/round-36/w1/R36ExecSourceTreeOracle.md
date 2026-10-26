# R36ExecSourceTreeOracle — K1/K2 oracle independence + source-tree rebuild

Seat: `R36ExecSourceTreeOracle` (leaf executor, advisory). Round 36, wave 1.
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`; base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`;
lane HEAD during this seat `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`.

## Verdict (short)

| Question | Result |
|---|---|
| committed `K1/oracle.tsv` == regular-file manifest of committed `fixtures/k1-src` | **YES** (3/3 rows identical: path, sha256, size) |
| committed `K2/oracle.tsv` == regular-file manifest of committed `fixtures/k2-src` | **YES** (4/4 rows identical; the one symlink is excluded on both sides) |
| rebuild from the source tree reproduces the fixture image sha256 (K1, xz, 128 KiB blocks) | **YES** — `93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589` |
| rebuild from the source tree reproduces the fixture image sha256 (K2, gzip, 4096-byte blocks) | **YES** — `ce5bf60e765e9942c1d317cfdd201b8b072b61e546e8dbdb6f87d6fe36a2084f` |
| oracle independently corroborated by extractors other than unsquashfs 4.7.5 | **YES** — sasquatch 4.5.1 identical; 7-Zip 26.04 identical modulo its own unsafe-symlink policy |
| oracle/fixtures/source trees unmodified since the freeze commit | **YES** — all 11 relevant blobs byte-identical to `790561d4`; `git status` clean |

No defect found. No frozen predicate, counter, carrier or oracle was changed.

## 1. Oracle ↔ source-tree comparison

Both sides reduced to the same rule (regular files only, symlinks excluded, rows sorted, `relpath TAB sha256 TAB size`).
Source-tree side computed with `os.walk` + `os.path.islink`/`os.path.isfile` guard + `hashlib.sha256`.

```
== K1 source=k1-src regfiles=3 oracle_rows=3
  source manifest: [('README.txt','88dc952ab79570963415341ba52c7e2a948aa69e0200987140a933c64d595961',59),
                    ('etc/config.ini','bf53724aca93538b630cf8742260b38426a317d5593ca1653e404710a48d9fef',27),
                    ('payload.bin','5b61b3262ca03ec21a79929502a9182d60a055e06fabe9f990ee2182fe11824f',70000)]
  identical: True
== K2 source=k2-src regfiles=4 oracle_rows=4
  source manifest: [('usr/lib/kaidoku/blocks.bin','76eaa72beec080e682b667795701938dbaeb4ee32777114f9471c502b9a72e87',200000),
                    ('usr/lib/kaidoku/text.txt','2defc0b25de7e2c560c87ca2461b0e317dd5b889150323b2e718ba8c1c1ebb94',73890),
                    ('usr/share/doc/NOTICE','70488b47ee9c7ab20d96e35558afd583adc3b5a3fd68574d83ed145e50342cc9',75),
                    ('var/small.dat','87d3d14a123c5a64139b050fe9c33188e1f484d6367d71a30c12fa21fdc9001f',6)]
  identical: True
```

Counts agree with the committed run metadata (`K1/oracle-run.json regular_files=3`,
`K2/oracle-run.json regular_files=4`) and with the squashfs superblock inode counts
(K1 inodes=5 = root + `etc` + 3 files; K2 inodes=12 = 7 dirs + 4 files + 1 symlink) — so the oracle
omits exactly one object per tree (K2 `var/notice-link -> ../usr/share/doc/NOTICE`, mode 120000 in git)
and nothing else.

Excluded-symlink detail, K2: `find ex-K2 -type l` → `ex-K2/var/notice-link -> ../usr/share/doc/NOTICE`.
K1 has no symlinks. The oracle-side exclusion therefore removes exactly one row, and it removes a
*link*, not a regular file.

## 2. Independent reproduction of the oracle (corroboration, not derivation)

`oracle.tsv` was regenerated from the committed fixtures by three extractors that do not share the
REA/unblob code path; all agree with the committed rows:

```
== K1 independent unsquashfs vs committed oracle:  IDENTICAL   (/usr/bin/unsquashfs 4.7.5, -o 0)
== K2 independent unsquashfs vs committed oracle:  IDENTICAL
K1: sasquatch exit 0   →  K1 sasquatch vs oracle:  IDENTICAL   (~/.local/bin/sasquatch, 4.5.1)
K2: sasquatch exit 0   →  K2 sasquatch vs oracle:  IDENTICAL
== K1 7z-extract vs committed oracle.tsv:  IDENTICAL            (7-Zip 26.04)
== K2 7z-extract vs committed oracle.tsv:  4d3
   < var/notice-link  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0
```

The single K2 7-Zip difference is 7-Zip's own guard, not an oracle defect:

```
ERROR: Dangerous link path was ignored : var/notice-link : ../usr/share/doc/NOTICE
Sub items Errors: 1        (7z exit 2)
```

7-Zip materialises the refused symlink as a 0-byte regular file (so my regular-file walk sees a
phantom row), while `7z l -slt` still records it as `Mode = lrwxrwxrwx, Size = 23, User ID = 0`.
Once the symlink rule is applied on 7-Zip's own listing semantics, K2 is identical.

Inode metadata in the images matches `-all-root -all-time 0` exactly, for every entry:

```
-rw-r--r-- root/root     59 1969-12-31 21:00 squashfs-root/README.txt      (K1; also etc/, config.ini, payload.bin)
lrwxrwxrwx root/root     23 1969-12-31 21:00 squashfs-root/var/notice-link -> ../usr/share/doc/NOTICE   (K2)
drwxr-xr-x root/root     51 1969-12-31 21:00 squashfs-root/var                (K2)
```

(`1969-12-31 21:00` is epoch 0 rendered in the host TZ, i.e. mtime 0.)

## 3. Rebuild from the source tree — does the image sha256 reproduce?

Flags taken from `carriers.json` `kind` strings plus the frozen determinism set
(`-noappend -all-root -mkfs-time 0 -all-time 0`). Instrument: `mksquashfs 4.7.5 (2026/03/01)`.

```
mksquashfs fixtures/k1-src k1-rebuild.sqsh -comp xz   -b 128K -noappend -all-root -mkfs-time 0 -all-time 0
  → rc=0  93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589  (73728 bytes)

mksquashfs fixtures/k2-src k2-rebuild.sqsh -comp gzip -b 4096 -noappend -all-root -mkfs-time 0 -all-time 0
  → rc=0  ce5bf60e765e9942c1d317cfdd201b8b072b61e546e8dbdb6f87d6fe36a2084f  (208896 bytes)
```

Both equal the committed `fixtures/*.sqsh` sha256 and byte size exactly. Superblock fields confirm the
declared kinds rather than merely agreeing with a digest:

| carrier | magic | version | compression | block_size | block_log | mkfs_time | bytes_used | inodes | frags |
|---|---|---|---|---|---|---|---|---|---|
| K1 | `hsqs` | 4.0 | xz (4) | 131072 | 17 | 0 | 70482 | 5 | 1 |
| K2 | `hsqs` | 4.0 | gzip (1) | 4096 | 12 | 0 | 207803 | 12 | 1 |

Reproduction held under every perturbation I could remove the build environment from, so the digest is
a property of the tree + flags, not of my scratch:

| perturbation | K1 | K2 |
|---|---|---|
| `-processors 1` / default (`nproc`=32) | same `93802938…` | same `ce5bf60e…` |
| source copied to `mktemp -d` path, dir renamed `treeA`/`treeB` | same | same |
| every mtime in the copy rewritten to `2001-02-03 04:05:06` | same | same |
| `-b 128K` vs numeric `-b 131072` / `-b 4K` vs `-b 4096` | same | same |

### 3a. Negative controls — is the flag set actually implied?

Each of the following was rebuilt from the same tree with one flag removed/altered. All differ from
the fixture digest, i.e. the flags are load-bearing (each run exit 0; digests truncated to 16 hex):

```
K1 target 93802938486d952a          K2 target ce5bf60e765e9942
no -all-root            9ebedf4bb88794d3    no -all-root            a004e80f5a0c5db8
no -mkfs-time/-all-time 0f06d9d9706909c5    mkfs-time 0 only        a692b6d86ac449f9
-mkfs-time 0 only       3ee9112548efee27    xz instead of gzip      76e496da7b573815
gzip instead of xz      70ac46618f3d2740    -b 128K instead of 4096 46ba9785773d0d76
xz -b 64K               a151ab11b24a92e6    + -noI                  ea6a185010011b47
+ -noD                  5ea6728bfae6c779
```

One flag is **not** digest-observable: `-noappend` and its absence both reproduce the fixture sha256,
because `mksquashfs` on a non-existent destination file cannot append (K1/K2 rows above: "no -noappend"
→ `93802938486d952a` / `ce5bf60e765e9942`). So the flag set is *sufficient and minimal for the digest*
except `-noappend`, which is a build-hygiene guard rather than a reproducing condition. This is a
documentation nuance for the claim text ("the exact mksquashfs flags implied"), not a defect: the
predicate never asserts uniqueness of the flag set, and no digest changes.

## 4. Freeze integrity (no post-freeze tampering)

Working-tree blobs vs blobs at freeze `790561d4` (`git hash-object` vs `git rev-parse 790561d4:<path>`),
all `SAME`:

```
fixtures/k1-le-xz.sqsh                   wt=f85a4fcd7dbb freeze=f85a4fcd7dbb SAME
fixtures/k2-le-gzip.sqsh                 wt=e307f9e7b33a freeze=e307f9e7b33a SAME
fixtures/k1-src/README.txt               wt=95a9ae59f6ee freeze=95a9ae59f6ee SAME
fixtures/k1-src/etc/config.ini           wt=21bdce696ec6 freeze=21bdce696ec6 SAME
fixtures/k1-src/payload.bin              wt=e84daf78cc11 freeze=e84daf78cc11 SAME
fixtures/k2-src/usr/lib/kaidoku/blocks.bin wt=42c284a1994a freeze=42c284a1994a SAME
fixtures/k2-src/usr/lib/kaidoku/text.txt wt=acce33aaa19a freeze=acce33aaa19a SAME
fixtures/k2-src/usr/share/doc/NOTICE     wt=a53fb64f3c3d freeze=a53fb64f3c3d SAME
fixtures/k2-src/var/small.dat            wt=ef471d9d39fb freeze=ef471d9d39fb SAME
K1/oracle.tsv                            wt=edd39fabbb74 freeze=edd39fabbb74 SAME
K2/oracle.tsv                            wt=4c6b90237b36 freeze=4c6b90237b36 SAME
```

`git status --porcelain -- corpus/evidence/round-36/c1 tools/round-36` → empty.
`git ls-tree -r 790561d4` also shows the source trees, the images and the oracles already committed at
the freeze commit, together with `K1/K2/before.json` — i.e. the oracle and its pre-image exist in the
same commit that froze the claim, before any sasquatch-enabled run (`6a870b92` controls, then
`3310d8fa` after receipts, then `d2e46ef5` C2 repairs — HEAD).

`carrier_sha256` recorded in `K1/oracle-run.json` / `K2/oracle-run.json`
(`93802938…`, `ce5bf60e…`) equals the committed fixture sha256, so the oracle was measured on bytes
identical to the committed images, even though the harness ran them from a scratch path.

Circularity note: the source-tree check alone cannot exclude "tree was copied out of the image".
Two observations bear on it, both supporting a genuine build input: (i) the tree carries
`vgpnk:vgpnk` ownership and 2026-10-26 01:17 checkout mtimes, whereas an `unsquashfs` product of
these images carries `root:root` and mtime 0 (as §2 shows); (ii) the images *rebuild* from the tree
under path/time/processor perturbation and fail to rebuild when any load-bearing flag is removed (§3a).
[INFERENCE] authorship of the tree (hand-written generator vs. extraction) is not decidable from
committed bytes; what is decidable — and verified — is that tree, image and oracle are mutually
consistent and all three predate every sasquatch-enabled run.

## 5. Predicate-fit observation (advisory, no change made)

`tools/round-36/c1-counter.py` compares oracle rows to published files with a **subset** rule —
`matched()` requires, per oracle row, some published file whose path equals the row or ends with
`/<row>` and whose sha256 equals the row's (`c1-counter.py:132-135`), and the binding is
`after_oracle_hits == oracle_files` (`:189`). Consequences, both benign here:

- Publishing the excluded symlink cannot fail K2: `K2/after.json` does publish
  `firmware.bin_extract/var/notice-link`, and the counter still needs only the 4 regular rows.
- A tool whose extraction output is *missing* a regular file (or emits it under a non-suffix path)
  does fail — which is the intended direction.

No frozen artifact was modified; this is recorded only so the L1 knows the symlink exclusion is not a
latent set-equality trap.

## 6. Limits of this check

- Scope is K1/K2 only, as assigned. K3/K4 oracles (AppImage, ELF-end offset) were not re-derived here.
- I verified regular-file path+sha256+size and total object counts. I did not verify K2 directory
  contents ordering, xattr presence, or export/fragment table contents beyond `bytes_used`/`frags`,
  which the digest already covers implicitly.
- The rebuild proves digest reproducibility for `mksquashfs 4.7.5` on this host; a different squashfs
  version is not claimed to reproduce the digest even with the same flags.
- `-noappend` is not digest-observable (§3a); everything else is.

## 7. Tooling and hygiene

- Tools used, all pre-installed (nothing installed or upgraded this seat): `mksquashfs`/`unsquashfs`
  4.7.5 (pacman `squashfs-tools`, `/usr/bin`), `sasquatch` 4.5.1 (L1-installed official deb,
  `~/.local/bin`, used read-only for corroboration, not reinstalled), `7-Zip` 26.04 (`/usr/bin/7z`),
  `python3`, `git` (read-only: `hash-object`, `rev-parse`, `ls-tree`, `status`, `log`).
- No pacman transaction was attempted (host-wide pause respected); no host service touched.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36ExecSourceTreeOracle` held all rebuilds/extractions and
  was removed with `rm -rf -- "$S"`; every hash, size and diff above is copied into this file, and no
  cited evidence lives only under scratch or `/tmp`.
- No VCS mutation: no add/commit/checkout/reset/stash/pull/push, no jj; no fixture repo was needed.
- Only file written by this seat: this report.
