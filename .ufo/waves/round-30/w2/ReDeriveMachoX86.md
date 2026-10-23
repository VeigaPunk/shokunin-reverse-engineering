# ReDeriveMachoX86 — wave 2, round 30

Seat: KaidokuR30.ReDeriveMachoX86 (reviewer, attack). Attacked: R30-C1 (P1-pass) on carriers
`macho-x86_64-uv` and `macho-x86_64-uvx`. Question: do REA 6.5.0's committed and live
`inspect-rust-binary` envelopes equal the carriers' own `.dep-v0` contents, as judged by an
independent reader? (The reader does not use `tools/round-30/rust_dep_oracle.py` or the counter.)

## Verdict

**Holds** for both macho-x86_64 carriers (observation). No counterexample found.

## Method

- Carrier bytes were copied from `/fast/scratch/hyaku/kaidoku-r30/carriers/<id>` to
  `<scratch>/<id>.bin`. The copies' sha256 values equal the frozen `carriers.tsv` values
  (`f31d4fdc…a0f3ca` uv, `f2530594…0f4058` uvx). The originals still had those sha256 values
  at 2026-10-23T03:13:46Z (`chattr +i` still set), so they were not modified.
- Own reader (`reader.py`): a hand-written Mach-O 64 LE parser. It walks the load commands,
  then the LC_SEGMENT_64 `section_64` records, and selects every section named `.dep-v0`.
  It inflates the section with `zlib.decompressobj` (and checks that the stream ends with no
  trailing bytes), then parses the JSON. A runtime dependency is represented by a missing
  `kind` (null), and a non-root package by a missing `root` (false). It compares the result
  with both the committed and the live envelope on:
  - `section_name`, `file_offset`, `section_bytes`, `compressed_bytes`, `uncompressed_bytes`
    and `format_version`;
  - the `file-offset-range` location;
  - packages in order and as a multiset of (name, version, source, kind, root);
  - each package's `dependencies` index list, `root_package_index`, and the dependency edges,
    both by index and as a multiset of ((name, version) → (name, version));
  - `cyclic_dependency_indices`, and `subject`/`artifact` sha256 and byte size.
- Second extractor: `llvm-objcopy --dump-section "__DATA,.dep-v0=<id>.objcopy.dep"
  <id>.objcopy-in <id>.objcopy-out.o`, run on a second scratch copy with an explicit output
  object. The input copy's sha256 was unchanged afterwards.
- Live REA: one run per carrier, `TMPDIR=<scratch>/tmp timeout 300 npx -y rea-agents@6.5.0
  inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/<id> --format json --full-output`.

## Per-carrier results (observation)

Commands: `timeout 120 python3 -I -B reader.py <id>.bin <committed>.json live-<id>.json`, both
exit 0, run 2026-10-23T03:13:04Z (uv) and 03:13:05Z (uvx). Live REA runs: exit 0, empty stderr,
03:12:23Z → 03:12:24Z.

| check | macho-x86_64-uv | macho-x86_64-uvx |
|---|---|---|
| Mach-O cputype / ncmds / sections | 0x1000007 / 21 / 21 | 0x1000007 / 15 / 18 |
| `.dep-v0` sections found | 1 (`__DATA,.dep-v0`) | 1 (`__DATA,.dep-v0`) |
| own offset / size | 40876072 / 9666 | 308048 / 9666 |
| REA `file_offset` / `compressed_bytes` / `section_bytes` (committed = live) | 40876072 / 9666 / 9666 | 308048 / 9666 / 9666 |
| location range | [40876072, 40885738) agrees | [308048, 317714) agrees |
| inflated bytes (own = REA `uncompressed_bytes`) | 54638 | 54638 |
| zlib trailing bytes | 0 | 0 |
| packages (own / committed / live) | 573 / 573 / 573, ordered-equal | 573 / 573 / 573, ordered-equal |
| kinds (raw) | 537 absent (runtime), 36 `build` | same |
| sources (raw) | 487 `crates.io`, 86 `local` | same |
| root | index 458 = `uv 0.13.0` (only root) | index 458 = `uv 0.13.0` (only root) |
| edges by index / by (name, version) | 2974 / 2974 distinct, equal | 2974 / 2974 distinct, equal |
| `cyclic_dependency_indices` | [] | [] |
| committed evidence_id | `ev_1c3ef6996f8f62f1eeffda94f2b5892763eda8b2f4a333c01311a11bf0c6af10` | `ev_02fb9f95c9b82c4a6ade2ea299e4fe85e193f821d406fa76feb0cfec709177b0` |
| live evidence_id | identical | identical |
| live envelope minus `meta` == committed | True (only `meta.duration` differs: 682ms vs 194ms) | True (293ms vs 98ms) |
| reader `bad=[]` (committed, live) | yes, yes | yes, yes |

Excerpt (`reader-macho-x86_64-uvx.out`):
`committed: evidence_id=ev_02fb9f95…77b0 packages=573 edges=2974 root=458 bad=[]` /
`live: evidence_id=ev_02fb9f95…77b0 packages=573 edges=2974 root=458 bad=[]` / `exit=0`.

The llvm-objcopy cross-check (exit 0, 03:13:07Z and 03:13:08Z) dumped 9666 bytes for each
carrier, with sha256 `34bb781a4a290254b224b6d2ccfd4def7f33167e8a9cbdb8f93226bdff2acb68`. This
equals the sha256 of my parser's own slice for both carriers, and the dump inflates to 54638
bytes and 573 packages. `llvm-objdump --section-headers` lists `.dep-v0` with size `000025c2`
(= 9666) in both carriers.

Further predicate clauses checked (observation, 03:13:41Z):
- `operation` is `inspect_rust_binary`.
- The subject sha256 equals the frozen carrier sha256.
- Each envelope was first added in `24da3459`, which comes after the freeze commit `4ee65c67`
  (`git log --diff-filter=A`; `merge-base --is-ancestor`).
- The envelope blob is identical at `24da3459`, at `92b1dd2d`, and in the worktree.
- `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` at `92b1dd2d` names each
  evidence_id (`grep -c` = 1 each).
- The `runs.tsv` rows for both carriers record exit 0 and `packages=573 edges=2974`.

One non-finding: `rustc_commit.hashes[].file_offset` (39471988 uv, 270817 uvx) points at the
start of the string `/rustc/b940084d7eb6a299eb4bfeb8e34901bc051e7ac4/library/allo…`, not at the
hash itself. This matches REA's stated limitation ("inferred from a /rustc/<40-hex>/ path") and
is outside P1.

## Residual risk and verification gaps

- The two macho-x86_64 carriers have byte-identical `.dep-v0` payloads (same 9666-byte sha256
  `34bb781a…`, same 573-package document with root `uv`). They are two positives for the
  container path (different offsets, segment layouts and load-command counts), but only one
  dependency document. This is consistent with the claim's stated limits ("uv and uvx of one
  wheel carry the same dependency document") (inference: no extra breadth).
- My reader shares the format specification (cargo-auditable `.dep-v0`: zlib-compressed JSON)
  with REA and the oracle, but no code. A spec-level misunderstanding shared by all three
  would not be detected (unknown).
- Only thin Mach-O x86_64 was checked. Fat/universal binaries, `LC_SEGMENT` (32-bit) and
  big-endian images are outside this seat. I did not run the C1 counter. I did not run REA on
  any mutant.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDeriveMachoX86/`)

| file | sha256 |
|---|---|
| reader.py | 2c220041cd13cf5ac4a57ef00e997d9a1f734ebbd75a2fefed36c098406b455c |
| reader-macho-x86_64-uv.out | 72e3b90f5930df7cb6d4c0b92e0929f9a5382aea85073d21ccab2266b8f93216 |
| reader-macho-x86_64-uvx.out | 40d02b2bff0a947acfbb90bfc4414e9d8b8a77f8a67c2e136a79b89413aad65d |
| live-macho-x86_64-uv.json | b1538eda2473bcc5972a40bebb60ace4b8afd4eb6402b4e16901433aca12262a |
| live-macho-x86_64-uvx.json | 23c56975f974e99f65945a1f3b594a98d95ba48a4542a51b1556be3955e307dd |
| live-macho-x86_64-uv.stderr / uvx.stderr (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| live-*.exit (`0`) | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa |
| live-*.start / live-*.end | 2df58168…3094 / b769da0e…3a12 |
| macho-x86_64-uv.objcopy.dep / uvx.objcopy.dep | 34bb781a4a290254b224b6d2ccfd4def7f33167e8a9cbdb8f93226bdff2acb68 |
| macho-x86_64-uv.objcopy-out.o | cb842f1dd7461936a0ad37f32efa18bb9941fdf31c167bd70628a52300fd79c9 |
| macho-x86_64-uvx.objcopy-out.o | f55aa00b07561bb5a001b12939bdec4ca1e40847e36991a9728be6f4ef3ec4dd |
| macho-x86_64-uv.bin / .objcopy-in (copies) | f31d4fdce12aad810a045b24aa322642fb8bfbaa441b24a90cbad0cdc7a0f3ca |
| macho-x86_64-uvx.bin / .objcopy-in (copies) | f25305942412cd98249f7da7f4f88acc5869e3150de09c46f7c110c7264f4058 |

Installs: none (python3, llvm-objcopy/objdump and npx were already present). No sources were
opened beyond local files. No processes were left running (the remaining `rea-agents` process
on `pe-x86_64-uv` belongs to another seat).
