# R30 w2 — ReDeriveElfX86 (attack R30-C1 on the elf-x86_64 carriers)

Attacked: R30-C1. Does REA 6.5.0 `inspect_rust_binary` (committed envelope and a fresh live run) faithfully report the `.dep-v0` contents of `elf-x86_64-uv` and `elf-x86_64-uvx`? I judged this with my own reader, which does not use `tools/round-30/rust_dep_oracle.py` or the counter.

**Verdict: holds** for both carriers. No counterexample found.

Lane HEAD at read time: `3502b94c5b93d86c5d67866035fd150899456295`. The committed envelopes are byte-identical in the worktree, at `24da3459`, and at HEAD (sha256 below).

## Method

1. I copied each carrier into my scratch directory with `cp`. Each copy's sha256 equals both the frozen `carriers.tsv` value and the immutable original. Every tool below ran on the copies only; REA read the originals, which are `chattr +i` (lsattr `----i-----`).
2. I extracted the section two independent ways:
   - My own ELF64 little-endian parser (`depv0_reader.py`). It reads `e_shoff`, `e_shnum` and `e_shstrndx` directly with `struct`, then walks the section headers and resolves names through `.shstrtab`.
   - `llvm-objcopy --dump-section .dep-v0=<out> <copy> <explicit-out.o>`. I cross-checked its output against `llvm-readelf -S -W <copy>`.
3. I inflated the section with Python `zlib.decompressobj` and checked for end of stream and unused bytes. Then I parsed the cargo-auditable JSON.
4. I compared against the committed and live envelopes at two strictness levels:
   - **Normalized**, by (name, version): name, version, source, kind, root and per-package dependency edges.
   - **Strict raw** (`strict_check.py`): each REA package must equal `{name, version, source, kind: absent→null, dependencies: absent→[], root: absent→false}` at the same index, and the `dependency_edges` index pairs must match exactly, ordered.
5. I ran REA live once per carrier, then compared evidence_id, packages and the whole envelope tree against the committed copy.

## Per-carrier results (observation)

Commands:
- `timeout 120 python3 -I -B depv0_reader.py <copy> <committed.json> <live.json>`: exit 0, 2026-10-23T03:13:15Z.
- `timeout 60 python3 -I -B strict_check.py <objcopy.dep-v0> <committed.json> <live.json>`: exit 0, 2026-10-23T03:13:43Z.

| check | elf-x86_64-uv | elf-x86_64-uvx |
|---|---|---|
| carrier sha256 (copy = original = carriers.tsv) | `3e801df8…592df0` | `2e9105ad…72890d` |
| `.dep-v0` section index / type / flags | [32] PROGBITS, flags 0 | [31] PROGBITS, flags 0 |
| offset: my parser / readelf / REA `file_offset` | 39701656 / 0x25dcc98 (=39701656) / 39701656 | 319695 / 0x4e0cf (=319695) / 319695 |
| size: my parser / readelf / REA `section_bytes`, `compressed_bytes` | 9870 / 0x268e (=9870) / 9870, 9870 | 9870 / 0x268e / 9870, 9870 |
| raw section sha256 (my parser = llvm-objcopy dump) | `ca01bd2a…3547e` | `ca01bd2a…3547e` |
| zlib header / end of stream / unused bytes | `789c` / True / 0 | `789c` / True / 0 |
| inflated length: mine / REA `uncompressed_bytes` | 55724 / 55724 | 55724 / 55724 |
| `format`: mine / REA `format_version` | 1 / 1 | 1 / 1 |
| package count: mine / committed / live | 584 / 584 / 584 | 584 / 584 / 584 |
| packages only in REA / only in mine (by name, version) | [] / [] | [] / [] |
| per-field differences (name, version, source, kind, root, deps) | 0 | 0 |
| strict raw per-index package mismatches (committed, live) | 0, 0 | 0, 0 |
| package order identical to the document | True | True |
| root: REA `root_package_index` / document `root: true` | 463 `uv 0.13.0` / [463 `uv 0.13.0`] | 463 `uv 0.13.0` / [463 `uv 0.13.0`] |
| edges: REA / mine; identical by (name, version) pair; identical by index, ordered | 3041 / 3041; True; True | 3041 / 3041; True; True |
| REA `packages[].dependencies` agrees with `dependency_edges` | True | True |
| `cyclic_dependency_indices` | [] | [] |
| raw kind values in the document | absent: 548, `build`: 36 | same |
| REA kind values | null (= absent), `build` | same |
| sources (document = REA) | `crates.io` 498, `local` 86 | same |

Exact excerpt from `reader-elf-x86_64-uv.out` (the uvx output has the same form):

```
committed.offset [39701656, 39701656, true]
committed.section_bytes [9870, 9870, true]
committed.root [[463, "uv", "0.13.0"], [[463, "uv", "0.13.0"]]]
committed.edge_count [3041, 3041, true]
committed.field_diff_count 0
live_vs_committed.evidence_id_eq True
live_vs_committed.normalized_result_eq True
```

## Live vs committed (observation)

Command: `TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDeriveElfX86/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/<id> --format json --full-output`

| carrier | UTC start → end | exit | stderr bytes | live evidence_id | committed evidence_id | equal |
|---|---|---|---|---|---|---|
| elf-x86_64-uv | 03:13:05Z → 03:13:06Z | 0 | 0 | `ev_ef18bd88be10acda35b48cd1675299c0e27b643c5e24acbd0a2700ea3f6a0b33` | same | True |
| elf-x86_64-uvx | 03:13:06Z → 03:13:06Z | 0 | 0 | `ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e` | same | True |

A recursive walk of the entire envelope tree (exit 0, 2026-10-23T03:13:43Z) found exactly one difference per carrier, `meta.duration`: uv `'732ms'` → `'112ms'`, uvx `'339ms'` → `'59ms'`. The packages, the auditable_metadata block, the normalized_result block and every `data` key are equal. The carrier sha256s were rechecked after the REA runs and are unchanged.

Committed envelope sha256 (worktree = `git show 24da3459:` = `git show HEAD:`):
- uv: `d7fdaeb6c28aa7da60a138cb6ffc4549d762364af60c887bc4aa131956b26095`
- uvx: `17cc6283380d2eda42445a7cd1233751fe6e0f73a183c5610e1c3592205d5caa`

The `runs.tsv` rows record exit 0, `P1-pass` and `packages=584 edges=3041` for both carriers, which matches my counts.

## Findings by severity

- **Defects:** none in scope.
- **Note (observation):** the two carriers carry byte-identical `.dep-v0` payloads (raw sha256 `ca01bd2a…`, inflated sha256 `a4e8aecf82a4f839dc09152e0aef8d0e7c22dc79f56306a7ab4e9edd2f3f696e`). Only the offset differs.
- **Note (observation, outside my two-carrier target, read from committed envelopes only):** across all 16 committed envelopes there are 7 distinct package lists, one per wheel. Every `uv`/`uvx`/`uvw` group within a wheel shares its list.
  - [INFERENCE] uvx and uvw are bin targets of the same root package `uv 0.13.0`, so cargo-auditable records the same dependency tree.
  - Consequence: C1's 16 carriers exercise 7 distinct dependency documents. Within a wheel, carriers vary the container offset and layout, not the parser input.

## Residual risk and verification gaps

- My reader shares two assumptions with any cargo-auditable reader: zlib framing, and JSON field defaults (absent `kind` means runtime, which REA reports as null; absent `root` means false; absent `dependencies` means []). I did not open the upstream cargo-auditable format spec this round, so how the defaults are interpreted is [INFERENCE]. The REA output preserves absence faithfully (null, false, []), so the comparison does not depend on that interpretation.
- I did not check that the ELF has exactly one section named `.dep-v0` against an adversarial layout. My parser asserts exactly one match, and that assertion passed on both carriers.
- I did not check `rustc_commit` or `limitations` against an independent source. They are outside P1's packages/edges/root/kind/offset/size scope. They were equal live vs committed.

## Bounds and tooling

- Lane: read-only. The only file I wrote in the lane is this report. Read-only git only (`rev-parse`, `show`, `log`).
- No sources opened (local files only). No tools installed or updated. `npx -y rea-agents@6.5.0` ran from the npm cache under my scratch `TMPDIR`.
- No mutant touched, and no C2 counter run. A `rea-agents` process on `/mutants/g-relocated` seen at 03:14:08Z belongs to another seat, so I left it alone. None of my processes remain.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDeriveElfX86/`)

| file | sha256 |
|---|---|
| depv0_reader.py | 1bd079a0cf318dff5b5e70c04359d0e14b95087e5be8a6f60901d47f3c5e4426 |
| strict_check.py | a11f2e6720cf85c6b1287123664749cd7b197e61ad48d2eb403e088917ccba47 |
| reader-elf-x86_64-uv.out | fca0f8bb16d107ac15c4d45d03468a64e83dc5169e502defe584552fdfc7799b |
| reader-elf-x86_64-uvx.out | 87e5f0df91897a903645d80629691d974bbedfa634222ff6b60066647bcac01f |
| live-elf-x86_64-uv.json | a70d320b7c33b842a9b30f29ad707116239bbe79c7fa11dbc753cab846e1b7b1 |
| live-elf-x86_64-uvx.json | 73e1a1da7d0fbba61d6ef9efaa981e79b1fe7dc505f42c1de7149f71edcc4efb |
| live-elf-x86_64-uv.stderr, live-elf-x86_64-uvx.stderr (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| live-*.exit (`0`) | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa |
| live-elf-x86_64-uv.start | 5be65562bff7f523a484d13dad745be1a85676ae78147c478df6cc6e5cd0f49e |
| live-elf-x86_64-uv.end, live-elf-x86_64-uvx.start, live-elf-x86_64-uvx.end | 71a530936b4d4a38dcec44dc190d40dceb071fe9be1c455b9d6c0e8a24e803be |
| elf-x86_64-uv.objcopy.dep-v0, elf-x86_64-uvx.objcopy.dep-v0 | ca01bd2a28ae28d6b3f4b64f54eb003061e7bf2584756bb6148c1d4e6383547e |
| elf-x86_64-uv.objcopy-out.o | d661be8beb9911f0b19460da2f0a7812bcd99fb3ee72367608bccf625ff40add |
| elf-x86_64-uvx.objcopy-out.o | 9f41e2d43ca085f1200cd52f1856fa3e821a05942a90d8084122a9ad9ef903a1 |
| elf-x86_64-uv.copy | 3e801df892439f5cde65d8b51ea69b69abff199ef37cc3cae4481be15d592df0 |
| elf-x86_64-uvx.copy | 2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d |
