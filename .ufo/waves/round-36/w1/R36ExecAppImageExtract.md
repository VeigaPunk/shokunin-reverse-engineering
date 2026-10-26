# R36ExecAppImageExtract — second (non-unsquashfs) oracle for K3, K4 runtime availability

- Wave: kaidoku-shokunin round 36, wave 1 (build drafts + first falsifiers). Lane root
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`.
- Seat: leaf executor. Advisory only. Nothing frozen was changed (no counter, predicate, carrier,
  oracle or receipt touched). No subagents, no background jobs, no `agent://all`.
- Scratch: `/fast/scratch/hyaku/kaidoku-r36/R36ExecAppImageExtract` — created, used, removed at exit.

## Verdict

**K3: PASS — the shipped AppImage runtime independently reproduces the frozen unsquashfs oracle
byte-for-byte on the regular-file set: 2130/2130 paths, 0 digest mismatches, 0 size mismatches,
0 missing, 0 extra, twice, from a runtime that never executes any external extractor.**

**K4: no second oracle obtainable in this environment — `qemu-aarch64` is absent and no aarch64
binfmt handler is registered, so K4 rests on the unsquashfs 4.7.5 oracle alone.**

## 1. Carrier integrity (both carriers re-checked against `carriers.json`)

```
$ curl -sSL -o nvim-linux-x86_64.appimage \
    https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-x86_64.appimage   # exit 0
b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb  nvim-linux-x86_64.appimage
11454968 bytes   -> matches carriers.json K3 sha256 b644d034…f29fb

$ curl -sSL -o nvim-linux-arm64.appimage \
    https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-arm64.appimage      # exit 0
8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2  nvim-linux-arm64.appimage
11356680 bytes   -> matches carriers.json K4 sha256 8efcec73…e1c2
```

## 2. K3 — extraction by the AppImage's own runtime

```
$ chmod 0755 nvim-linux-x86_64.appimage && mkdir extract && cd extract
$ ../nvim-linux-x86_64.appimage --appimage-extract        # exit 0, stdout 0 lines, stderr 0 lines
$ ls squashfs-root | head        -> .DirIcon (symlink), AppRun, nvim.desktop, nvim.png (symlink), usr/
$ ./nvim-linux-x86_64.appimage --appimage-version
AppImage runtime version: https://github.com/AppImage/type2-runtime/commit/8f39b89
$ ./nvim-linux-x86_64.appimage --appimage-offset
944632
```

`--appimage-offset` (944632) equals `corpus/evidence/round-36/c1/K3/oracle-run.json`
`squashfs_offset: 944632`, and `hsqs` is first found at byte 944632 of the file — the runtime and
the frozen oracle measured the same payload.

Extraction produced 2130 **regular files**, 115 directories and exactly 2 symlinks
(`.DirIcon -> nvim.png`, `nvim.png -> usr/share/icons/hicolor/128x128/apps/nvim.png`).

## 3. Manifest comparison against `K3/oracle.tsv`

Manifest built as `(sha256, path-relative-to-squashfs-root)` for every `-type f` entry, then compared
against the oracle's `path<TAB>sha256<TAB>size` rows:

```
oracle rows            2130
extracted regular      2130
missing from extract      0
extra in extract          0
digest mismatches         0
size mismatches           0     (oracle column 3 vs os.path.getsize)
symlinks in oracle        0     (by construction: regular files only — grep '^(\.DirIcon|nvim\.png)'
                                 in oracle.tsv: absent; the symlink TARGET usr/share/icons/…/nvim.png
                                 is present as a regular row, sha e6e68a31…8c16)
```

Order-independent anchor, computable from the committed oracle and from my run:

```
sha256 over sorted "<path>\t<digest>" lines  = 1f288b24aa55e5d858ff4a0322c1106dc1de020c74ba76c99465e54591f4ce9d
  oracle.tsv            -> 1f288b24…
  runtime extraction    -> 1f288b24…      (equal)
total oracle bytes     36,246,076   zero-byte regular files: 0
largest members        usr/bin/nvim 11,170,569 B; usr/lib/nvim/parser/vim.so 1,088,937 B; parser/c.so 633,233 B
```

A second extraction run (under `strace`, separate cwd) produced a manifest identical to the first
(`diff -q` → identical), so the match is stable across runs.

## 4. Why this is an independent implementation (evidence, not assertion)

Runtime identification from `strings` on the first 944632 bytes (`runtime.bin`, ELF x86-64
static-pie, stripped, BuildID `6068f2cec943069c072c32fe680557d1e5f7ec6f`; `ldd` → not a dynamic
executable):

```
AppImage runtime version: https://github.com/AppImage/type2-runtime/commit/8f39b89
https://github.com/vasi/squashfuse/blob/master/LICENSE
fsname=squashfuse
sqfs_traverse_open / sqfs_traverse_next / sqfs_stat / sqfs_read_range / sqfs_inode_get
sqfs_cache_get / sqfs_cache_put / sqfs_cache_entry_header / sqfs_cache_entry_mark_valid
fuse_* symbols, /dev/fuse, "Cannot mount AppImage, please check your FUSE setup."
decompressor identifiers present: zstd, xz, lzma, gzip, zlib   (+ "libzstd, licensed under the terms of")
```

So the `--appimage-extract` path is AppImage `type2-runtime@8f39b89` built on **squashfuse**
(vasi/squashfuse) — a different codebase and different traversal/caching design from the
`unsquashfs` 4.7.5 (squashfs-tools, Phillip Lougher) CLI that produced the frozen oracle.

No external extractor is invoked (this is the load-bearing falsifier, since a runtime that shelled
out to `unsquashfs` would not be an independent oracle):

```
$ strace -f -qq -e trace=execve,execveat,fork,vfork,clone,clone3 -o trace.execve.txt \
    ../nvim-linux-x86_64.appimage --appimage-extract     # exit 0
distinct execve/execveat targets: 1  (the AppImage itself, args: --appimage-extract)
clone/fork/vfork/clone3 lines:     0
$ strace -f -qq -e trace=openat … --appimage-extract ; grep -c fuse  -> 0   (no /dev/fuse, no mount)
```

## 5. Payload structure observed (superblock at the offset, raw bytes)

| field | K3 | K4 |
|---|---|---|
| magic | `hsqs` | `hsqs` |
| s_major.s_minor | 4.0 | 4.0 |
| compression | 6 = **zstd** | 6 = **zstd** |
| block_size / block_log | 131072 / 17 | 131072 / 17 |
| inodes | 2247 | 2247 |
| fragments | 148 | 148 |
| flags | 0x00c0 | 0x00c0 |
| ids | 1 | 1 |
| bytes_used | 10,507,255 | 10,417,706 |
| squashfs offset | 944,632 | 936,456 |

Both AppImages are type-2 with a 128 KiB-block zstd squashfs v4.0 payload.

## 6. K4 (aarch64) — availability result

```
$ for c in qemu-aarch64 qemu-aarch64-static qemu-user-static; do command -v $c; done   -> all missing
$ ls /proc/sys/fs/binfmt_misc/            -> register  status   (no aarch64 handler registered)
$ file nvim-linux-arm64.appimage
ELF 64-bit LSB pie executable, ARM aarch64, version (SYSV), static-pie linked, BuildID[sha1]=04d9d7ec…, stripped
```

There is no way to execute the aarch64 runtime here, therefore **no second oracle for K4**: K4's
2130-row oracle (`K4/oracle.tsv`, from `/usr/bin/unsquashfs` 4.7.5 at offset 936456) is single-implementation.

Static cross-check that K4 is the same artifact family (does **not** upgrade K4 to a second oracle):

- `hsqs` at byte 936456 == `K4/oracle-run.json` `squashfs_offset: 936456`.
- Superblock identical in every parameter to K3 except `bytes_used`/`root_inode` (§5).
- The aarch64 runtime carries the same markers: `AppImage runtime version: %s`,
  `https://github.com/AppImage/type2-runtime/commit/8f39b89`, `fsname=squashfuse`,
  `https://github.com/vasi/squashfuse/blob/master/LICENSE`, `sqfs_*` API symbols.
- **[INFERENCE]** the aarch64 runtime is the same type2-runtime commit built for aarch64 with the
  same squashfuse extraction path, so it would very likely reproduce K4's oracle the same way — but
  this is unexecuted inference, not evidence.

## 7. Limits, risks, calibration notes

- Compared: relative path set, sha256, size, for regular files only. **Not** compared: mode bits,
  mtimes, ownership, xattrs, symlink targets, hardlink topology. The oracle itself is regular-file-only,
  so this is a like-for-like comparison, not a full filesystem equivalence proof.
- I did not run `unsquashfs` myself (that would mint a new oracle); the frozen `K3/oracle.tsv` was
  used as-is.
- Residual shared dependency: both implementations decompress the same zstd blocks. The runtime
  statically embeds libzstd (license string; version candidate `1.5.6` present in strings —
  **[INFERENCE]** since `1.3.2` in the same string set is likely zlib's), while host `unsquashfs`
  links system `libzstd.so.1` (zstd 1.5.7-3). A decoder defect common to both zstd versions could in
  principle make the two agree on wrong bytes. Narrow, but it is the one axis where "independent"
  is not absolute; format traversal, inode/table handling and caching are genuinely different code.
- No defect was found in the K3 oracle or in the K3 carrier digest; nothing to report as a repair.
- Scope note for C1 predicate P36-C1: K3 (and K1/K2 via separate seats) now has coverage from two
  implementations; K4 does not. If the predicate is read as requiring that every carrier's oracle be
  independently corroborated, K4 is the exposed carrier — this report changes nothing about the
  frozen predicate or oracle, it only states the measured availability fact.

## 8. Tooling and hygiene

- **No tools installed or upgraded** (`pacman` untouched; nothing via `uv`/`npx`/release binary).
  Used as found: `curl 8.23.0`, `strace 7.2`, `Python 3.14.8`, `unsquashfs 4.7.5` (present; not used
  by me for extraction), `sha256sum`, `find`, `diff`.
- No VCS mutation of any kind; no REA invocation (not this seat's route); no writes outside this
  report file. Scratch directory removed:
  `rm -rf /fast/scratch/hyaku/kaidoku-r36/R36ExecAppImageExtract` (downloads, runtime.bin,
  runtime-arm64.bin, both manifests, trace logs — all gone; nothing cited above depends on a scratch
  path).

## 9. Reproduction recipe (all evidence above is re-derivable from committed inputs + the two URLs)

```bash
S=$(mktemp -d); cd "$S"
curl -sSL -o k3.appimage https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-x86_64.appimage
sha256sum k3.appimage          # b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb
chmod +x k3.appimage; mkdir x; cd x; ../k3.appimage --appimage-extract
cd squashfs-root && find . -type f -print0 | xargs -0 sha256sum \
  | sed 's#  \./#\t#' | sort > /tmp/run.tsv
python3 - <<'PY'   # compares against the frozen oracle and prints the digest-set anchor
import hashlib
o={}; [o.__setitem__(p,(h,int(s))) for p,h,s in (l.rstrip('\n').split('\t')
   for l in open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-36/c1/K3/oracle.tsv') if l.strip())]
r=dict(l.rstrip('\n').split('\t')[::-1] for l in open('/tmp/run.tsv'))
print(len(o), len(r), sorted(set(o)-set(r)), sorted(set(r)-set(o)),
      [p for p in set(o)&set(r) if o[p][0]!=r[p]],
      hashlib.sha256(('\n'.join(f"{p}\t{o[p][0]}" for p in sorted(o))+'\n').encode()).hexdigest())
PY
# expect: 2130 2130 [] [] [] 1f288b24aa55e5d858ff4a0322c1106dc1de020c74ba76c99465e54591f4ce9d
```
