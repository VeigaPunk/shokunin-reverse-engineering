# RevOracleB — Independent audit of expected records e05–e08 (round 34 / attempt 1)

| | |
|---|---|
| Seat | `KaidokuR34.RevOracleB` (leaf reviewer, Godspeed) |
| Date | 2026-10-23 |
| Lane root | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| Freeze / base | `54a87a51a865ab931fd355e767303337b05cccf4` |
| Scope | Expected records **e05–e08** (gridals) in `.ufo/waves/round-34/expected.json` (manifest sha256 `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`) |
| Bounds | Static metadata only. No carrier executed, no proposed reader/counter run, no REA, no edits outside `w1/RevOracleB.md` and `w1/RevOracleB-files/` |
| Tools | `/usr/bin/readelf` (GNU Binutils) 2.47, `python3` (struct-level ELF parse), `sha256sum`; nothing installed |

## Method (exact evidence)

- Froze carrier bytes verified first: `sha256sum` of lane-root copies, deliverable-root copies
  (`prep/R34Expected-files/corpus/...`), and sandbox copies `/fast/scratch/hyaku/kaidoku-r34/w1/RevOracleB/evidence/elf/e0X.bin`
  all equal claims digests: e05 `c14c8f49…73358d`, e06 `5eb48dd5…cccaf93`, e07 `339d917c…fd3fbc`, e08 `1c6062e0…1f3242`.
- Fresh readelf probes on private sandbox copies (argv `readelf --file-header|--section-headers|--dynamic|--version-info --wide <copy>`):
  - outputs byte-identical to the author's retained `captured/<id>/readelf-*.txt` for all 4 carriers × 4 probes (sha256 equal);
  - `readelf --version-info` name/flags/version column sets equal manifest `expected.needed` tuples (file, name, flags, other) exactly.
- Independent raw ELF parse (`struct`, ELF64 LE): `SHT_GNU_verneed` via `sh_link` → `.dynstr`, records walked by
  `sh_info`/`vn_next`, Vernaux by `vn_cnt`/`vna_next`, strings NUL-terminated inside linked `.dynstr`. For each record
  compared `vn_file`/`vna_name`/`vna_flags`/`vna_other`/`vna_hash` to manifest.

## Findings by severity

No defects found in the e05–e08 expected set. All checks pass; the frozen expectation set is correct on these carriers.

| id | source | needed | Vernaux | verneed sec (off/size/link/info) | .dynstr (off/size) | DT_VERNEED / VERNEEDNUM / STRTAB / STRSZ | raw vs manifest | readelf -V vs manifest |
|---|---|---:|---:|---|---|---|---|---|---|
| e05 | /usr/bin/bash | 1 | 16 | 0x189f8/272/5/1 | 0xfbd8/32192 | 100856 / 1 / 64472 / 32192 | match | match |
| e06 | /usr/bin/fwupdtool | 4 | 47 | 0x6f88/816/5/4 | 0x36e0/13437 | 28552 / 4 / 14048 / 13437 | match | match |
| e07 | /usr/bin/fwupdmgr | 3 | 58 | 0x4db8/976/5/3 | 0x25f0/9454 | 19896 / 3 / 9712 / 9454 | match | match |
| e08 | /usr/lib/libsmbclient.so.0.8.1 | 25 | 34 | 0x5de0/944/4/25 | 0x3468/9224 | 24032 / 25 / 13416 / 9224 | match | match |

- Flags: all stored `vna_flags` == 0 and equal manifest `flags` for all 155 Vernaux.
- Index: `vna_other` equals manifest `other` and readelf `Version:` column for all 155.
- Hash: stored `vna_hash` equals manifest `hash` for all 155 (raw byte read). Additionally `elf_hash(stored_name)` equals the
  stored field for all 155, so on these originals the stored value and the SysV-inferred value are identical; see notes below.
- Linked `.dynstr` offsets: every `vn_file`/`vna_name` offset resolves to a NUL-terminated string fully inside the linked
  `.dynstr` (`table_offset + length + 1 ≤ dynstr size`); `DT_STRTAB` == dynstr section offset, `DT_STRSZ` == dynstr size,
  `DT_VERNEED` == verneed section vaddr, `DT_VERNEEDNUM` == `sh_info`.
- Per-record string offsets (kind/record/aux/table_offset/value/length) match `checks.json` `string_offsets` exactly for all
  four carriers. `checks.json` `hash_provenance.sysv_hash_mismatches` empty for e05–e08.

## Notes (non-blocking)

1. **Hash inference vs stored field.** readelf does not print `vna_hash`; the only source is the raw Vernaux field, which I
   verified directly and equals the manifest for every record. Because stored == SysV `elf_hash(name)` on every original in
   these four carriers, a reader that recomputes the hash would produce identical output here; the two policies diverge only on
   the metamorphic challenge set (m01–m11), which is outside this assignment's scope but is documented by the author
   (`challenge/checks.json` gives stored vs computed per renamed name). No inference-vs-stored distinction is observable on
   e05–e08.
2. **Section-type constants.** Frozen `S104` (glibc `elf/elf.h`, commit d2097651cc57834dbfcaa102ddfacae0d86cfb66) pins
   `SHT_GNU_verneed = 0x6ffffffe` and `SHT_GNU_versym = 0x6fffffff`; the carriers and `author_expected.py` (line 50) use
   these values, and my independent parse matches. **Withdrawn:** an earlier comparison to alternate/classic historical
   constants was unsupported — no source in round 34 asserts a competing GNU mapping — and no reader advice based on it is
   retained. Supported constants only: verneed `0x6ffffffe`, versym `0x6fffffff`.
3. Retained readelf outputs were generated against host paths (`/usr/bin/bash` etc.); they are byte-identical to fresh runs on
   the frozen copies, so host drift is not present for e05–e08.

## Residual risk / verification gaps

- Out of scope: `e12` (absent version sections) and the metamorphic challenge carriers/`schedule.json`; production reader/counter
- Hash policy differentiation on the challenge set is the only intentionally asymmetric axis; not evaluated here.
- No code was executed from `tools/round-34/` or the proposed reader; all results above are static reads of carrier bytes and
  readelf text.

## Evidence

- `w1/RevOracleB-files/raw-parse-summary.json` — independent raw-parse result (records/aux, mismatches=[], string-table issues=[],
  dynamic/section cross-checks) for e05–e08; sha256 `2017373845d7527e1e2e1f057eb1f61ecc6a8c0baaaad1f4bab16fa525205a65`.
- `w1/RevOracleB-files/e05.version-info.txt` — fresh readelf `--version-info --wide` on the sandbox copy; sha256
  `70bebbbcea7ba05065c0cbcf93edd9d63885cbc67fc4ff862ea5bd8e989efd0f` (identical to retained capture).
- Sandbox working evidence: `/fast/scratch/hyaku/kaidoku-r34/w1/RevOracleB/evidence/` (ELF copies, all 16 readelf outputs,
  summary). Observed UTC: `2026-10-23T10:55:09Z`.
