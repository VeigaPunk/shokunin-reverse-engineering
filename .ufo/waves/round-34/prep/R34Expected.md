# R34Expected — independent expected GNU ELF version-needs metadata

| Field | Value |
|---|---|
| Lane | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| Base commit | `ec3125ad3d130d92f888a4128dfaa2982f36fff7` |
| Round / attempt | 34 / 1 |
| Seat | `KaidokuR34.R34Expected` (leaf executor, Godspeed) |
| Date | 2026-10-23 |
| Answering model | `opencode-go/deepseek-v4.1-flash` |
| Status | Frozen prefreeze expectation set + metamorphic schedule authored; **no production reader, no REA, no target binary executed** |
| Tools | `GNU readelf (GNU Binutils) 2.47`, `file-5.48`, `sha256sum 0.8.0`, `Python 3.14.8`; nothing installed or upgraded |

Deliverable root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34Expected-files/`

## 1. Frozen predicate

`expected` describes only the GNU ELF **version-needs** records a static reader can obtain
from the file: each `SHT_GNU_verneed` (`DT_VERNEED`) section, its linked `.dynstr`, each
`Verneed` record (`vn_file`) and each `Vernaux` record (`vna_hash`, `vna_flags`, `vna_other`,
`vna_name`). It is metadata interpretation of already-built benign host binaries: no
exploitation, no vulnerability analysis, no execution, no synthetic binary construction.
The only files created from target bytes are byte-exact copies (originals) and the pre-frozen
metamorphic string-renaming copies described in §6; neither is executed.

Canonical form, frozen before any reader run:

```json
{"schema": 1,
 "needed": [{"file": "libc.so.6",
             "versions": [{"name": "GLIBC_2.2.5", "flags": 0, "other": 2, "hash": 157882997}]}]}
```

- `file` = `vn_file` string resolved through the version-needs section's `sh_link` string table.
- `versions` = every `Vernaux` of that `Verneed`, sorted by `(name, other)`.
- `needed` sorted by `file` (ASCII code-point order).
- `flags` = stored `vna_flags` (uint16) as an integer.
- `other` = stored `vna_other` (uint16) as an integer (readelf's `Version:` column).
- `hash` = stored `vna_hash` (uint32) as an integer. **Direct field read, not inferred.**
  Independently cross-checked: `elf_hash(stored_name)` equals `vna_hash` for all 339 records
  (0 mismatches). So no hash value in this set is an inference.
- All 339 stored flags are `0`; the host set contains no `VER_FLG_WEAK` version need.
- Serialisation: UTF-8, 2-space indent, trailing newline; key order as above.

## 2. Selection (12 carriers, prefreeze)

Selection rule: distinct regular-file ELF binaries under `/usr/bin` and `/usr/lib`, diverse
version-needs shapes, byte-exact mode-0644 copies, all retained binaries ≤ 16 MiB (originals
**plus** the metamorphic set), no target executed, no reader consulted.

| id | source | bytes | needed files | Vernaux | `.dynstr` (off/size) | `.gnu.version_r` off | shape |
|---|---|---|---:|---:|---|---|---|
| e01 | `/usr/bin/true` | 43320 | 1 | 8 | 0xa08/822 | 0xdb8 | executable, 1 file / 8 versions |
| e02 | `/usr/bin/perl` | 14416 | 1 | 4 | 0x758/533 | 0x9b8 | tiny launcher, 1 / 4 |
| e03 | `/usr/bin/curl` | 223536 | 2 | 11 | 0x1180/1848 | 0x19d8 | executable, 2 files (libcurl) / 11 |
| e04 | `/usr/bin/xz` | 96992 | 2 | 17 | 0x1078/1835 | 0x18b0 | executable, 2 files (liblzma) / 17 |
| e05 | `/usr/bin/bash` | 1195144 | 1 | 16 | 0xfbd8/32192 | 0x189f8 | executable, 1 / 16 |
| e06 | `/usr/bin/fwupdtool` | 194992 | 4 | 47 | 0x36e0/13437 | 0x6f88 | executable, 4 files / 47 (libfwupd, libxmlb, gcc) |
| e07 | `/usr/bin/fwupdmgr` | 153776 | 3 | 58 | 0x25f0/9454 | 0x4db8 | executable, 3 files / 58 |
| e08 | `/usr/lib/libsmbclient.so.0.8.1` | 174032 | 25 | 34 | 0x3468/9224 | 0x5de0 | library, 25 files / 34 (samba private libs) |
| e09 | `/usr/lib/libssl3.so` | 448920 | 3 | 42 | 0x3250/8972 | 0x5ba8 | library, 3 files / 42 (NSS) |
| e10 | `/usr/lib/libstdc++.so.6.0.36` | 2939928 | 4 | 25 | 0x2f910/313059 | 0x7f9a0 | library, 4 files / 25, largest string table |
| e11 | `/usr/bin/net` | 1097344 | 61 | 77 | 0xaf50/34454 | 0x14290 | executable, 61 files / 77 (largest fan-out) |
| e12 | `/usr/bin/sln` | 747400 | 0 | 0 | — | — | static executable, no version sections |

Totals: 107 `needed` records, 339 `Vernaux` records, 7,329,800 bytes (6.99 MiB).
`e10` source is the resolved regular file; the host path `/usr/lib/libstdc++.so.6` is a
symlink to `libstdc++.so.6.0.36`, and the manifest pins the resolved path and digest.

`string_table` is carried in every manifest row as `{offset, size}` of the `.dynstr` linked
from the version-needs section. It is `null` only for `e12`, which has no `.gnu.version_r`,
no `DT_VERNEED` tag and no version sections at all; it is a static-PIE with a `.dynamic`
section (28 entries) but no version metadata. Independently cross-checked per carrier against
`readelf --section-headers --wide` (`.dynstr` index/offset/size), against the
`readelf --version-info --wide` header (`Addr`, `Offset`, `Link: N (.dynstr)`), and against
`readelf --dynamic --wide` (`DT_VERNEED` address, decimal `DT_VERNEEDNUM`).

### 2.1 Prefreeze selection change (parent instruction, no reader scores produced)

Reader development had selftested `libz.so.1`, `libgcc_s.so.1`, `liblzma.so.5` and
`ld-linux-x86-64.so.2`. Before freeze the original `e11 = /usr/lib/ld-linux-x86-64.so.2`
(dynamic loader, `DT_VERNEED` absent, 7 verdef records) was removed and replaced by
`e11 = /usr/bin/net` (61 Verneed / 77 Vernaux). Recorded in
`.ufo/waves/round-34/prep/R34Expected-files/selection.json`.

- Excluded carrier digest: `f5e11cc62f8f2c24dff532982559f4303dba3b17e7450551372a88c8e7ea8757`
  (`/usr/lib/ld-linux-x86-64.so.2`).
- Replacement digest: `a24a23098ea81cc03bf0d48becfb2809c4a557b1274be5a8112273472b40fc1f`
  (`/usr/bin/net`).
- Excluded development binaries (digests):

| binary | sha256 |
|---|---|
| `libz.so.1` | `6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9` |
| `libgcc_s.so.1` | `e618cb9c90c2eb3a1dad1cfea5b6c1eebcf2e799ad805976f4ae47bdd61c716a` |
| `liblzma.so.5` | `6e4dae5b099ec0e40a56beead2e51f858535aa794b5a8574a6723dfc1da8a3c1` |
| `ld-linux-x86-64.so.2` | `f5e11cc62f8f2c24dff532982559f4303dba3b17e7450551372a88c8e7ea8757` |

- **No carrier digest equals any selftested binary digest** (verified by sha256).
- Residual, explicitly accepted overlap: *referenced* `File:` sonames inside other carriers
  can spell the selftested names (`libgcc_s.so.1` in e06/e07/e10, `liblzma.so.5` in e04,
  `ld-linux-x86-64.so.2` in e10, `libz.so.1` in none). These are strings in other files'
  version-needs records, not carrier bytes or carrier digests.
- No dynamic zero-verneed carrier is retained; per parent, this is not required. `e12`
  (static, no version sections) remains as the absent-section control.

## 3. Method — two independent extraction paths

Author script: `.ufo/waves/round-34/prep/R34Expected-files/author_expected.py`

- **Path A (authoritative):** direct ELF parse with `struct` — header, section table,
  `SHT_GNU_verneed` (`sh_link` → `.dynstr`), `Verneed`/`Vernaux` chains walked using
  `sh_info` counts, `DT_NEEDED`/`DT_VERNEED`/`DT_VERNEEDNUM` read from `SHT_DYNAMIC`.
  Chain terminators, in-bounds records and NUL-terminated names are enforced; failures abort
  authoring rather than degrade silently.
- **Path B (cross-check):** text parse of `readelf --version-info --wide`, plus
  `readelf --dynamic --wide`, `readelf --section-headers --wide`, `readelf --file-header --wide`.
  Every carrier's file/version/flags/other tuples must match Path A exactly, and:
  `declared_entries` (readelf "contains N entries") = `sh_info` = number of `Verneed` records;
  version-info `Addr`/`Offset`/`Link` = section header values; `DT_VERNEED` address and
  `DT_VERNEEDNUM` = section values; `.dynstr` index/offset/size from `-SW` = parsed values.
- **Hash provenance:** `hash` is the stored `vna_hash` field; each value was recomputed with
  the SysV ELF string hash from the referenced name. 339/339 matched, so the field is direct
  and self-consistent on this host set.
- **NUL termination:** every referenced `vn_file`/`vna_name` string is verified to be
  NUL-terminated inside the linked table, with explicit `table_offset` and `length` retained
  per string in `checks.json`.

## 4. Frozen artifacts and integrity

| artifact | value |
|---|---|
| `manifest.json` sha256 | `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d` |
| `MANIFEST.sha256` | matches the above |
| `challenge/schedule.json` sha256 | `95199e90ee73cb278d7d2105f15e043eea4341e1682a69ea27f9d4053a0dcf2d` |
| `challenge/SCHEDULE.sha256` | matches the above |
| carrier bytes (12 originals) | 7,329,800 |
| challenge carrier bytes (11) | 6,582,400 |
| retained binaries total | 13,912,200 (13.27 MiB) |
| cap | 16,777,216 (16 MiB) — within cap |

Manifest row shape (parent-pinned): `{id, path, sha256, size, source_path, string_table, expected}`,
top level `{schema: 1, carriers: [...]}`, carriers in id order. `path` is the lane-relative
integration candidate `corpus/evidence/round-34/elf/eNN.bin`; the same relative tree is
materialised under the deliverable root, so Main can re-root it by copying the tree.
`source_path` is the resolved host binary actually copied.

Executed verification (all exit 0):

- `python3 author_expected.py` → `carriers=12 bytes=7329800`, `all_cross_checks_pass=True`
- `python3 author_challenge.py` → `challenge_carriers=11`, `retained_total=13912200`, `all_checks_pass=True`
- `python3 author_expected.py --verify` → `verify OK carriers=12 bytes=7329800`
- `python3 author_challenge.py --verify` → `verify OK challenge_carriers=11 retained_total=13912200`
- Determinism: two consecutive full regenerations produced identical sha256 for **all 124**
  generated non-script artifacts (23 carriers + 101 evidence files). `selection.json` is
  static prefreeze evidence added afterwards and is not regenerated.
- Independent final integrity pass: all 12 original copies are byte-identical to their host
  sources with mode `0644`; all 11 challenge carriers match their row digests, differ from
  their origin digests, and have mode `0644`; retained total ≤ cap. Result `ALL_OK True`.

## 5. Per-carrier expected values

Full canonical values are in `manifest.json` (`carriers[].expected`). Per-carrier provenance,
offsets, probe argv/exit/output digests and hash checks are in `checks.json`
(`checks[].string_offsets`, `.readelf_probes`, `.hash_provenance`). No values are summarised
away: the manifest is the single authoritative expectation source.

## 6. Preauthored metamorphic challenge (second schedule)

Script: `.ufo/waves/round-34/prep/R34Expected-files/author_challenge.py`
Frozen mapping: `challenge/schedule.json`; evidence: `challenge/checks.json`.

Transform, on private non-executed byte-copies:

- Only NUL-terminated strings **referenced by `.gnu.version_r`** (`vn_file` and `vna_name`)
  are replaced, in place, **only inside the linked `.dynstr`**.
- Replacements are the same byte length and ASCII (`[A-Za-z0-9._]`, first byte a letter),
  distinct from every other string in the linked table and from each other.
- No offset, size, section header, program header, record field, or `vna_hash` is modified.
- Mapping is frozen in `schedule.json` (per-carrier seed
  `random.Random(sha256("kaidoku-r34-metamorphic-v1|<origin_id>")[:8])`); applying the
  schedule does not use randomness, so Python RNG drift cannot change it.
- `expected` for each challenge carrier is the original expectation with `file` and version
  `name` values mapped through the same substitution table; `flags`, `other`, `hash`
  unchanged; re-sorted by the same rules.
- `hash_policy` is pinned per carrier and in the schedule: `hash` is the stored `vna_hash`
  field. Renaming leaves the field untouched, so a reader must report the stored value, not
  re-hash the new name. `challenge/checks.json` records, for each changed name,
  `{stored_hash, elf_hash_of_original_name, elf_hash_of_new_name}` — originals satisfy
  `elf_hash(original) == stored_hash`, replacements do not. This is the one intentional
  semantic asymmetry of the metamorphic set and is recorded rather than hidden.

Challenge carriers (ids are opaque; `origin_id` links back, if Main wants traceability):

| id | origin | path | substitutions (file+name) | byte diffs | digests changed |
|---|---|---|---:|---:|---:|
| m01 | e01 | `corpus/evidence/round-34/elf-meta/m01.bin` | 1+8 | 93 | yes |
| m02 | e02 | `…/m02.bin` | 1+4 | 57 | yes |
| m03 | e03 | `…/m03.bin` | 2+11 | 141 | yes |
| m04 | e04 | `…/m04.bin` | 2+17 | 179 | yes |
| m05 | e05 | `…/m05.bin` | 1+16 | 175 | yes |
| m06 | e06 | `…/m06.bin` | 4+47 | 663 | yes |
| m07 | e07 | `…/m07.bin` | 3+58 | 814 | yes |
| m08 | e08 | `…/m08.bin` | 25+23 | 890 | yes |
| m09 | e09 | `…/m09.bin` | 3+42 | 425 | yes |
| m10 | e10 | `…/m10.bin` | 4+23 | 272 | yes |
| m11 | e11 | `…/m11.bin` | 60+40 | 1956 | yes |

Totals: 395 substitutions (106 file-name, 289 version-name), 11 carriers, 6,582,400 bytes.
`e12` is excluded (`no .gnu.version_r / DT_VERNEED; no linked strings to substitute`) and is
listed under `excluded` in the schedule.

Per-carrier checks that passed before freeze: patched-file raw parse equals the mapped
expected; readelf parse of the patched file equals it too; `.gnu.version_r`/section skeleton
identical to the original; byte diffs confined to the linked table **and** to the substituted
name ranges; patched NUL terminators intact; stored hashes unchanged.

## 7. Evidence inventory (retained, all under the deliverable root)

- `manifest.json`, `MANIFEST.sha256` — frozen expectations.
- `checks.json` — per-carrier offsets, section/link evidence, cross-checks, hash provenance,
  probe argv/exit/output digests.
- `selection.json` — prefreeze selection change and dev-selftest exclusion evidence.
- `corpus/evidence/round-34/elf/e01…e12.bin` — byte-exact host copies, mode 0644.
- `corpus/evidence/round-34/elf-meta/m01…m11.bin` — metamorphic copies, mode 0644, never executed.
- `captured/readelf-version.txt`, `captured/run.json` — tool identity and probe receipt.
- `captured/<id>/readelf-{version-info,dynamic,sections,file-header}.txt` and `probes.json`
  — exact argv (`/usr/bin/readelf …`), exit code, stderr, stdout file + sha256 per carrier.
- `challenge/schedule.json`, `challenge/SCHEDULE.sha256`, `challenge/checks.json`,
  `challenge/captured/<mid>/…` — metamorphic mapping, expected values and patched-file evidence.

## 8. Risks, limitations, notes for Main

1. **`hash` under the metamorphic set** is the stored field (pinned). A reader that
   recomputes `elf_hash(name)` instead of reading `vna_hash` will diverge on every renamed
   entry; `challenge/checks.json` gives both values so Main can classify that as a reader
   policy difference rather than a parse failure. This is the only intentional field/name
   asymmetry in the set.
2. **Selftested-soname references** remain inside other carriers' expectations (§2.1). Only
   carrier digests are guaranteed disjoint from the four selftested binaries.
3. **No dynamic zero-verneed carrier** after the prefreeze swap; `e12` covers the
   absent-section case (static, `readelf` prints "No version information found in this file.").
4. **Path rooting:** `path`/`source_path` values assume the lane root; the materialised tree
   mirrors the relative paths, so Main can relocate by tree copy. Carrier bytes, digests and
   expected values are independent of the root.
5. **Host volatility:** expectations are pinned to the digests in `manifest.json`. If a host
   package upgrades any carrier, the digests (and derived expectations) no longer apply; the
   copies, not the host paths, are the frozen carriers.
6. **Scope compliance:** no production reader, no reader source, no REA and no target binary
   was executed or consulted while authoring; no scores or reader results are claimed here.
   Only `readelf`, `python3`, `sha256sum`/`stat` pipelines and file copies ran.
7. **Errors observed:** no external tool, model or safety errors. Two authoring-harness bugs
   were found by the cross-checks and fixed before freeze — (a) `readelf --dynamic` prints
   `VERNEEDNUM` in decimal while addresses are hex, (b) the challenge skeleton comparison
   initially used the wrong evidence object and an unsorted verify comparison. Both were
   harness-only; the frozen manifest and schedule were regenerated after the fixes and all
   checks pass.

## 9. Report trailer

- Files written (absolute):
  - `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34Expected.md`
  - `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34Expected-files/` (author scripts, manifest, checks, selection, captured evidence, 12 original carriers, 11 metamorphic carriers, challenge schedule/evidence)
- No changes outside that directory; no git/jj operations; no tool installs.
- Checks Main still owns: running the production reader/counter over the frozen carriers and
  comparing against `manifest.json` / `challenge/schedule.json`, and deciding the `hash`
  policy question in §8.1 for the metamorphic set.
