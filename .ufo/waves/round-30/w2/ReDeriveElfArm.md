# ReDeriveElfArm — round 30 wave 2 (attack R30-C1, elf-aarch64 carriers)

Seat: KaidokuR30.ReDeriveElfArm (reviewer / re-derivation attack). Date 2026-10-23.
Attacked: R30-C1 predicate P1 on carriers `elf-aarch64-uv` and `elf-aarch64-uvx`: do REA 6.5.0's committed and live `inspect_rust_binary` envelopes equal the `.dep-v0` contents, judged by a reader written in this seat? That reader is neither `tools/round-30/rust_dep_oracle.py` nor the counter.

**Verdict: holds** (observation) for both elf-aarch64 carriers. No counterexample found.

## Method

1. Copied the carrier bytes to scratch (`cp` followed by `chmod u+w` on the copy). The copies' sha256 equals the frozen `carriers.tsv` sha256 and the live carrier sha256 (observation, `sha256sum`, 2026-10-23T03:12:17Z). Carriers showed `----i---` (immutable) in `lsattr`. No tool was pointed at a carrier path except REA's read-only `inspect-rust-binary`.
2. Reader I wrote, `myreader.py` (stdlib only), does the following:
   - Parses the ELF header (class, data, e_shoff, e_shentsize, e_shnum, e_shstrndx).
   - Walks the section-header table and resolves names through `.shstrtab`.
   - Requires exactly one `.dep-v0` section.
   - Slices `[sh_offset, sh_offset+sh_size)`, applies `zlib.decompress`, then `json.loads`.
   - Normalises each package to (name, version, source, kind (absent→null), root (absent→false), dependencies).
   - Builds dependency edges by ((name, version) → (name, version)).
   - Computes cyclic nodes with Tarjan's algorithm.
   - Compares against an envelope field by field.
3. Independent extraction cross-check on the **copies**, each with an explicit output object: `timeout 120 llvm-objcopy --dump-section .dep-v0=<id>.objcopy.dep-v0 <id>.bin <id>.objcopy-out.o` (exit 0 for both). The dumped bytes inflate to output byte-identical to my reader's inflated output (`inflated_eq_myreader True`).
4. `readelf -SW <copy>` gave a second view of the section header.
5. Ran REA live once per carrier: `TMPDIR=<scratch>/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/<id> --format json --full-output`.

## Per-carrier results

All values below are observations from `python3 -I -B myreader.py <id>.bin <id> <envelope>`, exit 0, run 2026-10-23T03:13:05Z (committed) and right after 03:13:12Z (live).

| check | elf-aarch64-uv | elf-aarch64-uvx |
|---|---|---|
| ELF class / data / e_machine | 64-bit / LE / 183 (AArch64) | 64-bit / LE / 183 |
| `.dep-v0` section index, type | [33], PROGBITS, 1 hit | [32], PROGBITS, 1 hit |
| file_offset: REA committed / mine / readelf | 33685332 / 33685332 / 0x201ff54 (=33685332) | 287372 / 287372 / 0x4628c (=287372) |
| section_bytes = compressed_bytes: REA / mine / readelf | 9871 / 9871 / 0x268f (=9871) | 9871 / 9871 / 0x268f |
| uncompressed_bytes: REA / mine | 55764 / 55764 | 55764 / 55764 |
| `locations` file-offset-range | start 33685332 end 33695203 = mine | start 287372 end 297243 = mine |
| format_version: REA / raw `format` | 1 / 1 | 1 / 1 |
| packages: REA / mine | 584 / 584 | 584 / 584 |
| package list equal **including index order** (name, version, source, kind, root, dependency indices) | True, 0 field mismatches | True, 0 field mismatches |
| multiset (name, version, source, kind, root) equal | True | True |
| (name, version) edges: REA / mine / equal | 3042 / 3042 / True | 3042 / 3042 / True |
| `dependency_edges` field vs my index edges | 3042 / 3042 / True | 3042 / 3042 / True |
| root: REA `root_package_index` / mine | 463 / [463] (uv@0.13.0) | 463 / [463] (uv@0.13.0) |
| kind: raw values / build count REA, mine | {absent, "build"} / 36, 36 | {absent, "build"} / 36, 36 |
| sources (raw) | crates.io, local | crates.io, local |
| duplicate (name, version) pairs | 0 (so name/version edges are unambiguous) | 0 |
| cyclic_dependency_indices: REA / mine (Tarjan) | [] / [] | [] / [] |
| out-of-range dependency indices | 0 | 0 |
| subject and artifact sha256 = carrier sha256 | True / True | True / True |
| raw `.dep-v0` sha256 (mine = llvm-objcopy) | b5268d1e…587ed7 | b5268d1e…587ed7 |
| inflated JSON sha256 | 12a67c7e…22f2fe | 12a67c7e…22f2fe |

Excerpt from `cmp-committed-elf-aarch64-uvx.json`: `"pkgs_exact_eq_incl_index_order": true, "pkg_field_mismatches": [], ... "nv_edges": [3042, 3042, true], ... "root": [463, [463], true, "uv@0.13.0"]`.

## Live vs committed

| carrier | live exit (UTC) | committed evidence_id | live evidence_id | equal |
|---|---|---|---|---|
| elf-aarch64-uv | 0 (03:13:10Z–03:13:11Z), stderr empty | ev_1506350fdcaad3573291668df01a30fb30dbdba545c2a20ad4d09ec927c8d40e | ev_1506350fdcaad3573291668df01a30fb30dbdba545c2a20ad4d09ec927c8d40e | True |
| elf-aarch64-uvx | 0 (03:13:11Z–03:13:12Z), stderr empty | ev_5aa17b13d4b1dbdcc4ff03b7abacef14203776cfc504c64fb252473c1e2c38d8 | ev_5aa17b13d4b1dbdcc4ff03b7abacef14203776cfc504c64fb252473c1e2c38d8 | True |

- Observation from a recursive diff of committed vs live JSON: `data` equal True, `ok` equal True, packages equal True. The only differing leaf is `/meta/duration` (`'361ms' | '91ms'` for uv, `'275ms' | '60ms'` for uvx). The single-byte length difference (`cmp` reports `differ: char 178722` / `178717`) is fully explained by the duration string.
- Observation: my reader against the **live** envelopes gives the same all-True result as against the committed ones (`cmp-live-*.json`).
- Observation: the npx-resolved `rea-agents/package.json` reports version `6.5.0` and has sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`. This equals the `pkg_json_sha256` column of `corpus/evidence/round-30/c1/runs.tsv` for both rows.

## Other P1 clauses checked (read-only git)

- The committed envelope blobs are identical at 24da3459, 92b1dd2 and HEAD (uv `44370081…`, uvx `48245e26…`), and `git hash-object` on the working files gives the same blobs.
- `git log` shows only 24da3459 (the data commit) touching these envelopes. `git merge-base --is-ancestor 4ee65c67 24da3459` succeeded, so the envelopes were first added after the freeze (observation).
- `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md:52-53` at 92b1dd2 names both evidence_ids with 584 packages, 3042 edges, offsets 33685332 and 287372, and size 9871. All of these equal my reader's values.
- `rustc_commit` hash `b940084d7eb6a299eb4bfeb8e34901bc051e7ac4` is present in the copy bytes at the cited file_offsets (1649769 for uv, 19916 for uvx), in the substring `/rustc/b940084d…/li` (observation). This is outside P1 and was checked only as a sanity check.

## Notes, residual risk and gaps

- Observation: both aarch64 carriers carry a byte-identical `.dep-v0` section (same raw and inflated sha256), and its root is `uv@0.13.0` even in `uvx`. The two carriers therefore exercise one dependency document at two different offsets in two different ELF images. They are independent tests of section location, not of package decoding. Inference: this is expected cargo-auditable behaviour for two binaries of one package, not an REA defect. It does narrow how much decoding diversity the two carriers contribute to the 16/16 count.
- My reader follows the cargo-auditable JSON shape (`format`, `packages[]` with `name`/`version`/`source`/`kind`/`dependencies`/`root`). It does not validate that schema against the upstream specification. No external source was opened, so no source rows are recorded.
- Scope: only the two elf-aarch64 carriers. I did not run the C1 or C2 counters and did not touch any mutant.
- Installs: none.

## Commands (all exit 0 unless noted)

- `sha256sum` on the copies and carriers; `lsattr` on the carriers (03:12:17Z).
- `readelf -SW <id>.bin | grep -E 'dep-v0|Name'`
- `timeout 120 python3 -I -B myreader.py <id>.bin <id> <lane>/corpus/evidence/round-30/c1/envelopes/<id>.json > cmp-committed-<id>.json` (03:13:05Z)
- `timeout 120 llvm-objcopy --dump-section .dep-v0=<id>.objcopy.dep-v0 <id>.bin <id>.objcopy-out.o`
- `TMPDIR=<scratch>/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/<id> --format json --full-output > live-<id>.json 2> live-<id>.stderr` (03:13:10Z–03:13:12Z)
- `timeout 120 python3 -I -B myreader.py <id>.bin <id> $PWD/live-<id>.json > cmp-live-<id>.json`
- `cmp <committed> live-<id>.json` (exit 1: byte difference inside `meta.duration` only)
- `git rev-parse <rev>:<envelope>`, `git hash-object`, `git log -- <envelopes>`, `git merge-base --is-ancestor`, `git grep <evidence_ids> 92b1dd2`
- No process was left running (checked at 03:13:52Z); the scratch `tmp/` was emptied.

## Artifacts (/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDeriveElfArm/)

| file | sha256 |
|---|---|
| myreader.py | 65bc811aa00540b8c66ecc66c4bf931dcf8faece8f9875bdde16fdb7a136817d |
| elf-aarch64-uv.bin (copy) | a72b2853c84ac54d63147f32e4ace266a1d9e2017e53e5486fe3b9494145eff4 |
| elf-aarch64-uvx.bin (copy) | e3ef59b327cdf02e5f6c0cf3c3e5a6249d97bb9d67d67538776783364b21d0f9 |
| elf-aarch64-uv.objcopy.dep-v0 | b5268d1e9cf74c4d706bfe20e9f06c71fb1444dbad1e4868b95e8ff0fc587ed7 |
| elf-aarch64-uvx.objcopy.dep-v0 | b5268d1e9cf74c4d706bfe20e9f06c71fb1444dbad1e4868b95e8ff0fc587ed7 |
| elf-aarch64-uv.objcopy-out.o | ca4ed62965b1834bbe60ad0d82efa71e8bff06a412a36aa3e96dca54f50269cd |
| elf-aarch64-uvx.objcopy-out.o | 5d132bb621ad87d2ceed1cf53194f77916a7f6fa661373b41cfd2d912b5828e2 |
| elf-aarch64-uv.myreader.inflated.json | 12a67c7ecb08312090805c3638de0a379609b53780c9fd63f63a5233bd22f2fe |
| elf-aarch64-uvx.myreader.inflated.json | 12a67c7ecb08312090805c3638de0a379609b53780c9fd63f63a5233bd22f2fe |
| cmp-committed-elf-aarch64-uv.json | 4f04186233920ed6202cf004b281d4086ff677712cad56238b1db79f27258f8d |
| cmp-committed-elf-aarch64-uvx.json | 8a0db6c17add3ef38b9b228a172cac05c8d000cca43112757070e620fbabe976 |
| cmp-live-elf-aarch64-uv.json | b41315df6085057bbe0751f3035dd204aac484722253733a1fd147bcca8d3d70 |
| cmp-live-elf-aarch64-uvx.json | 8e97730b9a1b97f7015725a3d22a33b6ab3b6bde9b96fe5f1ade4dd571be7733 |
| live-elf-aarch64-uv.json | 6a032c5cd6b2a5ca43d923ccf231491eea297f4de0637a189f5459bad719e4f6 |
| live-elf-aarch64-uvx.json | 7dd67ef61ed039c5d3a92bf8067b87b92150445174dc7a627d73d43a659511f3 |
| live-elf-aarch64-uv.stderr / live-elf-aarch64-uvx.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |
