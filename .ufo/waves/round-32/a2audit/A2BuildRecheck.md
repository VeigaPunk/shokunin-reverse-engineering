# A2BuildRecheck — carrier builder reproduction + llvm-readobj witness (round 32, attempt 2 audit)

Seat: `KaidokuR32A2.A2BuildRecheck`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Lane revision observed at build start `2026-10-23T06:46:39Z`: HEAD
`f382e3b7978e6091a19ca93277c15a75c0016b43` (`git status --porcelain` 21 entries, all pre-existing
untracked `.ufo/waves/round-32/*`). At `2026-10-23T06:51:45Z` HEAD had moved to
`411f3a80a1efefabe2ba12f227147023cfbce4bd` (`round-32: retain C2v3 negative-assessment false accept;
frozen claim honest stop`, 2026-10-23T03:51:01-03:00, +6 files: two a2audit reports, c2-negative
control tree, LOG.md) — committed by another wave actor, not by this seat. All six files this seat
depends on are byte-identical at `f382e3b7` and at `411f3a80` (re-hashed after the move), so the
reproduction basis is unchanged. No lane file was modified **by this seat**, no git/jj state was
written by it, no REA was run, no carrier binary was executed, no pinned original was rewritten.
(Other seats' concurrent tracked-file edits — SKILL.md, corpus/QUALITY.md, claim-freezes*.tsv,
round-31 docs — are theirs and outside this seat's scope.)

Scratch (unique): `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2BuildRecheck` (428K, 81 files).
Report: this file.

## 0. Preconditions (exercised, 2026-10-23)

- `df -h /fast` at 06:45:30Z: `/dev/nvme1n1p2 804G 560G 244G 70% /fast`.
- Toolchain already present; **no install/update was made** (pacman is paused host-wide, none invoked):
  - `clang --version` → `clang version 23.1.3`, `Target: x86_64-pc-linux-gnu`, `InstalledDir: /usr/bin`
  - `llvm-mc --version` → `LLVM version 23.1.3`
  - `lld-link --version` → `LLD 23.1.3`
  - `llvm-readobj --version` → `LLVM version 23.1.3`
- Frozen inputs re-hashed against the tree (working tree == `f382e3b7` for all five files;
  `git diff --quiet f382e3b7 -- <path>` clean for each):
  - `tools/round-32/build-arm64x-carriers.sh` `7da284da5986295263c69a8b7ee779638428d3bb6c9d5c9d8fb224c40a737ba3`
  - `corpus/evidence/round-32/c1/carriers.tsv` `8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e`
  - `corpus/evidence/round-32/c1/predictions.tsv` `fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b`
  - `corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s` `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d`
  - `corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s` `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4`
  - `git show f382e3b7:...carriers.tsv | sha256sum` == working-tree hash (8cf97b37…), i.e. the freeze
    table is byte-identical at the pinned revision.
- Freeze commits: `9a73680af21b002e3b99956c89234b2bbde2a71b` (C1+C2 v2, 2026-10-23T03:03:46-03:00),
  `f382e3b7978e6091a19ca93277c15a75c0016b43` (C2 v3, 03:10:01-03:00). Base `283aad7f`.

## 1. Reproduction (exercised)

Exact argv, single run, cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`:

```
timeout 900 bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/build-arm64x-carriers.sh \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2BuildRecheck/out
```

- Started `2026-10-23T06:46:39Z`, ended `2026-10-23T06:46:40Z`; `EXIT=0`; no timeout.
- `build.stdout` 0 bytes, `build.stderr` 0 bytes (both sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
  The builder is silent on success; the empty streams are the observed success output.
- Produced `out/k01.dll`…`out/k12.dll`, plus 12 `.lib` import sidecars and 50 files under `out/obj/`
  (intermediates: 2 load-config objects, 12 native `.c`/`.obj`, 12 EC `.c`/`.obj`). Only the 12 `.dll`
  are in the frozen table; the sidecars are extra build output, not compared and not pinned.

## 2. Generated-vs-frozen SHA256 (exercised)

Comparison script `compare.txt` (sha256 `d2a4116ac3eee6209f67ece11cf7a3a2b722c291ed61fcc74b0b70ae052a4aba`)
parsed the frozen `carriers.tsv` and compared each generated DLL to (a) the `sha256` column and
(b) the immutable original at the `path` column. All 12 rows true on both, sizes equal:

| id | generated sha256 (== tsv == immutable original) | bytes |
|---|---|---|
| k01 | 2f386dde73a262a657cc385f16594afce9369e05121916a8fd44a6cc45630989 | 9216 |
| k02 | a16ba36205f584b0a1589895ed31feffcc36eda692b81e675cdfeadb819519d4 | 9728 |
| k03 | 0291e17bd517802b44984fb8e8fcc2cec0266b02ded1cb81bccea040a737b73d | 9728 |
| k04 | 3c783318ea3aea29033460edb17b4cade7b0eca675e0d5410d278672d2bfb386 | 9728 |
| k05 | cc5c644a515b4e9d65c1c5ae8455df1032f5c3d21bb77d034e8ded13c04060bf | 9728 |
| k06 | 6c45a3ce1c3e9b91719a3ded213d995c35947af221145b14c06f0ca838247b3c | 9728 |
| k07 | 84a78b7894fa11f876734d2bd926d8e3e73f08be3f2a6f93b35925e3605afb6f | 9728 |
| k08 | b158eaf7c7417400202f06acc0867013185260efdf296a6dbbe622e873e3215c | 9728 |
| k09 | cf0148615fce4399e067715eb48554f63c4a30cf04a40c75776d58b1a2b82a87 | 9728 |
| k10 | a48499d2df92de871fd3e7c7d8cba63bbfbc019fd84ee312bdbdada632c766c7 | 9728 |
| k11 | b5e2af7f2b96fd66f87ed0be99e576fa94b7f843d088bdb05e212ac67592d181 | 9728 |
| k12 | 8c852d075fab64aca5c165ff3b907507d62d409972bbfddb72543ef3efea04fa | 9216 |

`ALL12_MATCH 12`. Additional checks:
- `cmp` of each generated DLL against `/fast/scratch/hyaku/kaidoku-r32/carriers/<id>.dll` → all identical.
- Generated hash set == `/fast/scratch/hyaku/kaidoku-r32/b1.sha` and == `b2.sha` (the two pre-freeze
  builds), so this is a third independent build with the same bytes.
- Immutable originals carry `lsattr` flag `----i-----------------` (immutable) on all 12, i.e. the pinned
  bytes could not be rewritten during this run and were not.

[INFERENCE] Byte-identity here exercises one host + LLVM 23.1.3 + the frozen inputs. It does not by
itself prove determinism on another host/toolchain; `-Brepro` plus the observed third-build match is the
evidence available.

## 3. llvm-readobj witness (exercised)

Required asymmetric carrier **k04** (native 4 / EC 1).

```
llvm-readobj --file-headers --coff-exports /fast/scratch/hyaku/kaidoku-r32/a2audit/A2BuildRecheck/out/k04.dll
```
`EXIT=0`; full stdout kept at `readobj-k04.txt` (sha256 `ebbbe07e2f67a6175d77c712e852ddf84001a72528124fc435ba5facfc555646`, 235 lines). Relevant stdout verbatim:

```
File: /fast/scratch/hyaku/kaidoku-r32/a2audit/A2BuildRecheck/out/k04.dll
Format: COFF-ARM64X
Arch: aarch64
AddressSize: 64bit
ImageFileHeader {
  Machine: IMAGE_FILE_MACHINE_ARM64X (0xA64E)
  SectionCount: 7
  TimeDateStamp: 2094-10-12 00:03:53 (0xEAB43B69)
...
  ExportTableRVA: 0x4348
  ExportTableSize: 0x64
  LoadConfigTableRVA: 0x4000
  LoadConfigTableSize: 0x140
...
Export { Ordinal: 1  Name: f1  RVA: 0x1000 }
Export { Ordinal: 2  Name: f2  RVA: 0x1010 }
Export { Ordinal: 3  Name: f3  RVA: 0x1020 }
Export { Ordinal: 4  Name: f4  RVA: 0x1030 }
HybridObject {
  Format: COFF-ARM64EC
  Arch: aarch64
  ImageFileHeader { Machine: IMAGE_FILE_MACHINE_ARM64EC (0xA641) ... }
  ExportTableRVA: 0x43AC
  ExportTableSize: 0x3D
  Export { Ordinal: 1  Name: g1  RVA: 0x3000 }
}
```

(The four primary `Export` blocks and the single `HybridObject` block above are shown collapsed; the
retained file has them in full block form. Block counts machine-checked: primary 4, hybrid 1.)

```
llvm-readobj --coff-load-config .../out/k04.dll
```
`EXIT=0`; stdout `readobj-k04-lc.txt` (sha256 `bcc44b98a06d9e05d4dad196cf0d0ca03d578dadef45709d4c0b8bc399c8c789`). Decisive lines:

```
  CHPEMetadataPointer: 0x180005000
CHPEMetadata [
  Version: 0x2
  CodeMap [
    0x1000 - 0x1040  ARM64
    0x2000 - 0x205C  ARM64EC
    0x3000 - 0x3010  X64
  ]
  RedirectionMetadata [ 0x3000 -> 0x2004 ]
```

**Witness result for k04:** native-view export count is **4** (`f1..f4`), EC labels are a disjoint
single label `g1` → native count ≠ EC label count, so the frozen `predictions.tsv` value
`procedure_count=4` for k04 is the native-view count, not an EC-label count. This is the required
asymmetric witness.

Extended (cheap, same tool) to all 12 carriers via `llvm-readobj --coff-exports` per file; parser output
`readobj-counts.txt` (sha256 `dc96840c60121564038a169d92a99a9193b4b20517e6be8270e3913ed0da84d8`):

| id | primary n | tsv native | hybrid n | tsv ec | names primary / hybrid |
|---|---|---|---|---|---|
| k01 | 1 | 1 | 1 | 1 | f1 / f1 |
| k02 | 2 | 2 | 2 | 2 | f1,f2 / f1,f2 |
| k03 | 3 | 3 | 3 | 3 | f1,f2,f3 / f1,f2,f3 |
| k04 | 4 | 4 | 1 | 1 | f1,f2,f3,f4 / g1 |
| k05 | 1 | 1 | 4 | 4 | f1 / g1,g2,g3,g4 |
| k06 | 5 | 5 | 5 | 5 | f1..f5 / f1..f5 |
| k07 | 6 | 6 | 2 | 2 | f1..f6 / g1,g2 |
| k08 | 2 | 2 | 6 | 6 | f1,f2 / g1..g6 |
| k09 | 7 | 7 | 3 | 3 | n1..n7 / e1,e2,e3 |
| k10 | 3 | 3 | 7 | 7 | n1..n3 / e1..e7 |
| k11 | 8 | 8 | 8 | 8 | f1..f8 / f1..f8 |
| k12 | 1 | 1 | 2 | 2 | n1 / e1,e2 |

`ALL_MATCH` (counts equal the frozen `native_exports`/`ec_exports` columns and all names within each
view are distinct).

## 4. One observation about the machine field (exercised bytes + [INFERENCE] on display)

The on-disk COFF machine field of k04 is **0xAA64**, not 0xA64E:
`e_lfanew=0x78`, signature `PE\0\0`, header bytes at `pe` = `50450000 64aa 0700 …` → machine `0xaa64`.
`llvm-readobj` *prints* `Machine: IMAGE_FILE_MACHINE_ARM64X (0xA64E)` and `Format: COFF-ARM64X` for the
same file. [INFERENCE] LLVM detects the hybrid (CHPE metadata with ARM64+ARM64EC code map) and promotes
its reported format/machine for display, while the raw header field stays 0xAA64; that raw field is what
the frozen pure-Python oracle reads (`classify` → `"machine": "0xaa64"`, `arm64x: true`, code map
`ARM64 @0x1000`, `ARM64EC @0x2000`, `AMD64 @0x3000`; `native_exports ['f1','f2','f3','f4']`,
`procedure_count 4`, `segment_count 8` — run read-only with `python3 -I -B tools/round-32/arm64x_oracle.py`).
The frozen predicate's "COFF machine 0xAA64" therefore matches the bytes; no predicate edit is proposed
or needed here.

## 5. Retained evidence map (all under the unique scratch)

| file | sha256 | content |
|---|---|---|
| `build.stdout` | e3b0c442…b855 (empty) | builder stdout, exit 0 |
| `build.stderr` | e3b0c442…b855 (empty) | builder stderr |
| `compare.txt` | d2a4116a…aaba | 12-row tsv/immutable/size comparison, `ALL12_MATCH 12` |
| `rebuilt.sha256` | — | sha256 of the 12 generated DLLs |
| `readobj-k04.txt` | ebbbe07e…5646 | llvm-readobj file-headers+coff-exports for k04 (235 lines) |
| `readobj-k04-lc.txt` | bcc44b98…c789 | llvm-readobj coff-load-config for k04, CHPEMetadata code map |
| `readobj-counts.txt` | dc96840c…84d8 | per-view export counts/names for all 12 |
| `out/k01.dll`…`out/k12.dll` | see table in §2 | regenerated carriers |

No background process was left: every command above ran foreground and exited; nothing is running in
this seat's tree. Scratch is 428K / 81 files; nothing outside `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2BuildRecheck`
and this report was written.

## 6. Verified conclusions vs. inference

Exercised (observed):
1. The frozen builder runs to exit 0 on the pinned lane revision with the pinned inputs, empty output.
2. All 12 generated DLLs are byte-identical (sha256 and `cmp`) to `carriers.tsv`, to the immutable
   `chattr +i` originals under `/fast/scratch/hyaku/kaidoku-r32/carriers/`, and to both `b1.sha`/`b2.sha`.
3. llvm-readobj independently prints, for k04, 4 primary exports (`f1..f4`) and 1 hybrid/EC export
   (`g1`), with a v2 CHPE code map holding ARM64, ARM64EC and X64 ranges; the same count rule holds for
   all 12 carriers.
4. The raw header machine of k04 is 0xAA64; llvm-readobj displays ARM64X (0xA64E).

Inference (not exercised):
- LLVM's ARM64X display/machine promotion mechanism (inferred from the observed raw-vs-display split).
- Cross-host/toolchain reproducibility beyond LLVM 23.1.3 on this host.
- Upstream provenance of the two load-config `.s` inputs (asserted as llvmorg-23.1.3 lld test inputs by
  frozen claim S098; not re-fetched here).

Risks / notes:
- The witness uses the same LLVM release as the builder, so it is independent of the pure-Python oracle
  and of REA, but not independent of the toolchain version.
- The builder also writes `.lib` sidecars not present in `carriers.tsv`; they are harmless build output.
- No REA run, no counter run, no carrier execution, no pinned-original rewrite, no git/jj write, no
  installs. Held item `U064N008Hf47eb933` was not inspected or retried.

Blockers: none. Deadline 07:35Z was not approached; last evidence (re-hash of the six frozen files
against `f382e3b7` and `411f3a80`) at `2026-10-23T06:51:45Z`; this report closed at `2026-10-23T06:52:39Z`.
