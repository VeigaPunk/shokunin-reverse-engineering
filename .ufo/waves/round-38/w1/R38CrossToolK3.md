# R38CrossToolK3 — cross-tool oracle reproduction for C1 carrier K3

Seat: `R38CrossToolK3` (executor, leaf). Round 38 wave 1. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Read at: `cb4326b2` (lane `main`); the frozen bytes under `corpus/evidence/round-37/c1/` are
identical to freeze `e059ca93` (`git diff --stat e059ca93 HEAD -- corpus/evidence/round-37/c1/`
→ empty, exit 0). Frozen pins: claim control `efd5c47a`, base `77091b49`.

Scope: extract the K3 big-endian SquashFS v4 carrier with `~/.local/bin/sasquatch-v4be -be`
into a fresh scratch dir, compare every regular file's relative path and sha256 against the
committed oracle `corpus/evidence/round-37/c1/K3/oracle.tsv`, and confirm 7-Zip refuses the
BE image. No REA call was made; no frozen predicate/counter/carrier/oracle was touched; no
repair performed. Raw outputs: `.ufo/waves/round-38/w1/artifacts/R38CrossToolK3/evidence.txt`.

## Verdict

**Cross-tool expectation holds; nothing falsified.**

- K3 extraction: exit 0, **4 regular files, 0 extra entries**, every relative path + sha256 +
  size equal to `K3/oracle.tsv` (**4/4**, `diff` exit 0).
- 7-Zip 26.04 **refuses** the BE image: `7z l`, `7z t`, `7z x` all exit **2**, none publishes
  a file. Text for the Gate § below.

## 1. Carrier identity (pins re-checked)

| item | observed |
|---|---|
| `sha256(corpus/evidence/round-37/c1/K3/carrier.bin)` | `9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0` = the frozen pin in `.ufo/waves/round-38/c1/carriers.json` (match) |
| size | 4096 B (4k pad); `file`: "Squashfs filesystem, big endian, version 4.0, zlib compressed, 307 bytes, 5 inodes, blocksize: 131072" |
| pad region | bytes 307..4095 are **all zero** (0 non-zero bytes) |
| `K3[0:307]` | sha256 `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed`, byte-identical to the whole `K4/carrier.bin` (307 B) |
| full extraction of that 307-byte prefix | exit 0, `diff -r` against the 4kpad extract empty |

Tools: `sasquatch-v4be` sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`,
self-reporting `unsquashfs version 4.5.1 (2022/03/17)`; `7z` 26.04 (2026-10-05, x64);
system `unsquashfs`/`mksquashfs` 4.7.5.

## 2. sasquatch-v4be extraction of K3 (fresh scratch dir)

```
$ ~/.local/bin/sasquatch-v4be -be -d $S/k3-sasquatch corpus/evidence/round-37/c1/K3/carrier.bin
EXIT=0
stdout: Parallel unsquashfs: Using 1 processor / 4 inodes (4 blocks) to write / 8/8 100%
        created 4 files; created 1 directory; 0 symlinks/devices/fifos/sockets/hardlinks
stderr: Reading a different endian SQUASHFS filesystem ...
        Successfully decompressed with default gzip decompressor (x3)
```

Extracted tree (all entry types, `-mindepth 1`): `apple1.txt`, `apple2.txt`, `apple3.txt`,
`apple4.txt` — four regular files, **no** directories, symlinks or device nodes beyond the
extraction root, so the oracle covers 100 % of the published regular files.

Comparison (exact relative path, sha256, size):

```
apple1.txt	6181259c6b2ca629a56920b422e9a8f212a4d0bcead923df92dbd66fbb7e1c30	7
apple2.txt	919fc82d6f1031d305dbce2fc5a74a6df5ddf2da472ee4d137c681cef28d4aff	7
apple3.txt	2d95014ed3f24e86ce5fc3a4529f057d7b2318d9b24b54f2e9476b154bd21ec6	7
apple4.txt	08d9b05b15b998f2dbc741399fef4350c7863cc85df2305d7da4e83e8c8a959d	7
$ diff -u <(sort K3/oracle.tsv) <(sort extract.tsv)   → DIFF_EXIT=0 (empty)
```

Counts: extracted regular files **4**, oracle rows **4**, matched **4**, mismatched **0**,
missing **0**, extra **0**. `cmp` against the committed `apple*.txt` also identical. Content
is `apple1\n` … `apple4\n` (7 B each).

Controls that show the result is content-dependent, not a stub:

| control | result |
|---|---|
| second extraction into a different dir | exit 0, `diff -r` empty (deterministic) |
| same carrier **without** `-be` | exit **1**, 0 files: "SquashFS version [1024.0] / inode count [83886080] suggests a SquashFS image of a different endianess", "read_id_table: failed to read id table block", "FATAL ERROR: File system corruption detected" |
| carrier truncated to 100 B, `-be` | exit **1**, 0 files: "Read on filesystem failed because EOF" … "FATAL ERROR: File system corruption detected" |
| stock `unsquashfs` 4.7.5 `-l` on K3 | exit **1**, "FATAL ERROR: Can't find a valid SQUASHFS superblock" (confirms the harness comment) |

Corroboration on the other frozen carriers with the same tool (not required by the ticket,
included because it is the same one-line check):

| carrier | sasquatch-v4be -be | oracle | comparison |
|---|---|---|---|
| K4 (307 B nopad) | exit 0 | `K4/oracle.tsv` | 4/4 exact, `diff` exit 0 |
| K1 (`carrier.sqsh`) | exit 0, 5 files + 1 symlink | `K1/src` | 5/5 regular files exact, `diff` exit 0; symlink `link-to-hello -> ../hello.txt` identical (dangles identically in both trees) |
| K2 (`carrier.sqsh`) | exit 0, 3 files + 1 symlink | `K2/src` | 3/3 exact, `diff` exit 0; symlink `var/lib/run-link -> ../../a/run.sh` identical |

## 3. 7-Zip 26.04 refuses the BE image (text for the lesson Gate)

```
$ 7z l corpus/evidence/round-37/c1/K3/carrier.bin          EXIT=2
stdout: "Scanning the drive for archives: / 1 file, 4096 bytes (4 KiB) /
         Listing archive: corpus/evidence/round-37/c1/K3/carrier.bin / (blank) / Errors: 1"
stderr: "ERROR: corpus/evidence/round-37/c1/K3/carrier.bin : Cannot open the file as archive"

$ 7z t corpus/evidence/round-37/c1/K3/carrier.bin          EXIT=2
stdout: "Can't open as archive: 1 / Files: 0 / Size: 0 / Compressed: 0"
stderr: "ERROR: corpus/evidence/round-37/c1/K3/carrier.bin / Cannot open the file as archive"

$ 7z x -o$S/7z-k3-x corpus/evidence/round-37/c1/K3/carrier.bin   EXIT=2
stderr: "ERROR: corpus/evidence/round-37/c1/K3/carrier.bin"; output dir never created
```

Same refusal on K4 (`EXIT=2`, same wording) and on K1's synthetic BE gzip `.sqsh`
(`EXIT=2`, same wording). No file was extracted by 7-Zip under any invocation.

Discrimination control (so the Gate states the reason, not just the failure): `7z i` lists the
handler (`SquashFS squashfs`, read capability). A fresh **little-endian** v4 gzip image built
in scratch (`mksquashfs` 4.7.5, 290 B, 4 inodes) is listed by the same 7-Zip build with
**exit 0**, printing `apple1.txt` (7 B) and `sub/apple2.txt` (7 B). So the refusal is specific
to the big-endian layout, not a missing handler — `[INFERENCE]` 7-Zip's SquashFS reader is
little-endian-only; the observed evidence is the LE-accepts/BE-rejects pair plus the handler
listing.

For R37-CL3, the Gate-safe wording is: *7-Zip 26.04 lists the SquashFS handler and reads a LE
v4 gzip image, but rejects the BE v4 carrier with `Cannot open the file as archive` (exit 2)
on `l`/`t`/`x`; reject 7-Zip as a BE v4 path.*

## 4. Oracle provenance, resolved without REA (strengthens "independent oracle")

The committed oracle is not self-derived: the expected-output bytes are upstream unblob's
`26.6.4` integration fixture for `squashfs_v4_be`, whose repository stores fixtures through
Git LFS. The LFS pointer `oid sha256` **is** the content digest, so pointer-vs-committed-hash
equality is a byte-level identity check (no REA involvement). Fetched at git tag `26.6.4`
(`raw.githubusercontent.com/onekey-sec/unblob/26.6.4/...`):

| upstream path | upstream LFS pointer | committed lane bytes |
|---|---|---|
| `__input__/squashfs_v4.4kpad.bin` | `oid sha256:9c7c523c…9b69397c0`, `size 4096` | `K3/carrier.bin` sha256 `9c7c523c…`, 4096 B — **atomic match** |
| `__input__/squashfs_v4.bin` | same oid, `size 4096` | same |
| `__input__/squashfs_v4.nopad.bin` | `oid sha256:a29ddc15…fdfe956ed`, `size 307` | `K4/carrier.bin` — **atomic match** |
| `__output__/squashfs_v4.4kpad.bin_extract/apple{1..4}.txt` | oids `6181259c…`, `919fc82d…`, `2d95014e…`, `08d9b05b…`, each `size 7` | `K3/oracle.tsv` rows and `K3/apple*.txt` — **atomic match, all four** |

Also observed: the unblob `26.6.4` sdist (PyPI, sha256
`5dac92c617912d77fef471b28df86cdd7aa3817de3b6febd9bb9251fb41552fa`) ships
`python/unblob/handlers/filesystem/squashfs.py` with `NAME = "squashfs_v4_be"` (line 514), so
the handler name the claim requires is present in the pinned package.

Independent-implementation note: sasquatch-v4be is a C build self-reporting `unsquashfs
4.5.1`; unblob's BE path is its own Python handler. Two implementations, one carrier, one
byte-identical result. `[INFERENCE]` (from the version string) that sasquatch is an
unsquashfs fork; the observed fact is only that it is a separate binary/extractor.

Additional calibration datum (round-37 probe material, **not** claim data): the committed
probe envelope `.ufo/waves/round-37/probes/rea-k3.json` names subject digest `9c7c523c…`
(the same carrier bytes), provider `unblob 26.6.4`, chunk handler `squashfs_v4_be`,
`extraction_gaps: []`, and publishes `firmware.bin_extract/apple{1..4}.txt` with exactly the
oracle sha256s. Applying the frozen counter's own `matched()` rule to that published list
yields **4 of 4**. So the REA/unblob result and the sasquatch result agree on identical input.

## 5. Compatibility with the frozen counter (calibration note)

`tools/round-38/c1-counter.py` `matched()` accepts `fp == rel` **or** `fp.endswith('/' + rel)`
and compares sha256 only (`load_oracle` ignores the size column). My comparison is stricter:
exact relative-path equality plus size, on the same sha256. Both agree for K3 (all paths at
extraction root). Nothing here contradicts the counter; the counter's suffix allowance is
unchanged and unevaluated by me (no REA receipt exists yet — `corpus/evidence/round-38/c1/`
is not mine to populate).

## 6. Harness observation (advisory, disclosed not repaired)

`tools/round-38/c1-run.sh` is **not** the freezed bytes at `e059ca93`: commit `cb4326b2`
("round-38: harness fix (REA refuses existing extraction root; oracle mode unchanged)") sits
above the freeze and changes only the `after` branch (`mkdir -p "$OUT"` →
`rm -rf "$OUT"` + comment, plus a doc line). The `oracle` branch is byte-identical per
`git diff e059ca93 cb4326b2 -- tools/round-38/c1-run.sh`.

- My first harness run (03:18:53.012) hit the file mid-rewrite and died with
  `bash: line 27: syntax error near unexpected token ')'` (exit 2); the file's mtime is
  03:18:53.037. This was a transient write race, **not** a durable defect: `bash -n` at the
  landed bytes exits 0.
- Re-run at the landed bytes:
  `bash tools/round-38/c1-run.sh oracle corpus/evidence/round-37/c1/K3/carrier.bin <scratch-out> <scratch-work>`
  → **exit 0**, prints exactly the four oracle rows, `diff` against `K3/oracle.tsv` empty.
- Advisory to L1: the C1 executor's `after` receipts will be produced by the post-freeze
  harness bytes; if the freeze is meant to cover the harness, that divergence should be stated
  in the round report rather than assumed. My K3 result does not depend on the harness (the
  direct `sasquatch-v4be` invocation reproduces it).

## 7. Material this hands to the SOURCES gate (R37-CL2), no writes by me

`avm.txt` and `be-squashfs_v4{,.nopad}.bin` still need registration; the fixture half is now
pinned to an citable upstream:

- `.ufo/waves/round-37/probes/be-squashfs_v4.bin` (4096 B) sha256 `9c7c523c…` = unblob tag
  `26.6.4` LFS `squashfs_v4.4kpad.bin` (and `squashfs_v4.bin`), size 4096.
- `.ufo/waves/round-37/probes/be-squashfs_v4.nopad.bin` (307 B) sha256 `a29ddc15…` = unblob
  tag `26.6.4` LFS `squashfs_v4.nopad.bin`, size 307.
- Expected output: unblob tag `26.6.4`
  `tests/integration/filesystem/squashfs/squashfs_v4_be/__output__/squashfs_v4.{4kpad,nopad,}bin_extract/apple{1..4}.txt`,
  oids as in §4.
- The Freetz AVM-BE note (`avm.txt`) still has no provenance line; not resolved here.

## 8. Exact retained evidence

- Artifact: `.ufo/waves/round-38/w1/artifacts/R38CrossToolK3/evidence.txt` (148 lines; raw
  stdout/stderr/exit codes for §1–§7 above).
- Committed inputs cited by hash/rev: carriers `K3/carrier.bin` `9c7c523c…`, `K4/carrier.bin`
  `a29ddc15…`; oracle `K3/oracle.tsv` rows as quoted; freeze `e059ca93`; read at `cb4326b2`.
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38CrossToolK3` removed before this report; the
  cited outputs are reproduced verbatim in the artifact (no scratch or `/tmp` path is
  evidence). Downloads (unblob sdist 163 KB, GitHub tree JSON 1.5 MB, nine raw pointer files)
  lived only in that scratch dir.

## 9. Risks / limits

- I did not run REA, the counters, or any selftest; C1's `after.json` receipts do not exist
  yet, so the *counter-level* predicate stays unevaluated by me by design.
- The upstream provenance check uses git LFS pointer oids, not the fetched blobs: it pins the
  content digest and size exactly, and the same oids reproduce the committed bytes, but the
  LFS object bytes themselves were not downloaded and re-hashed.
- `[INFERENCE]` items are flagged in place (7-Zip LE-only read path; sasquatch fork lineage).
- No tool was installed or upgraded in this seat (`sasquatch`, `sasquatch-v4be`, `unblob`,
  `7z`, `mksquashfs` were already present; pacman untouched).
- `considerthese/` absent — one line, as the claims file requires: absent in this lane.
