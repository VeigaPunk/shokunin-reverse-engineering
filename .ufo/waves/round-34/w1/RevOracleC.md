# RevOracleC — Independent audit of expected records e09–e12 (round 34)

Reviewer: KaidokuR34.RevOracleC (UFO-FSD reviewer, leaf). UTC 2026-10-23T10:54:26Z.
Sandbox: `/fast/scratch/hyaku/kaidoku-r34/w1/RevOracleC` at freeze `54a87a51a865ab931fd355e767303337b05cccf4`.

## Scope and method

Independently compared the frozen manifest records for carriers **e09–e12**
(`.ufo/waves/round-34/expected.json`, sha256 `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`, matches
`claims.json`) against:

1. **Retained readelf captures** — `prep/R34Expected-files/captured/e{09,10,11,12}/readelf-version-info.txt`
   (readelf 2.47), parsed by an independent regex oracle (version requirement
   sections: File / Name / Flags / Version per entry).
2. **Own readelf runs on private copies** — `/usr/bin/readelf --version-info --wide`
   on the sandbox carrier copies. Outputs are **byte-identical** to the retained
   captures (e09 `64eedbee…`, e10 `c0630abb…`, e11 `f6e372a4…`, e12 `cf2ded89…`;
   exit 0 for all four).
3. **Direct binary struct parse** — a minimal independent ELF64 parser walks the
   `SHT_GNU_verneed` chain (`Elf64_Verneed`/`Elf64_Vernaux`), resolving
   `vn_file`/`vna_name` through the linked `.dynstr` section, and reads the stored
   `vna_hash` field byte-wise. No target binary executed; no production reader or
   counter run (pre-data boundary respected).

Carrier digests were re-verified against the manifest (e09 `d8fab7fc…`, e10
`f5fc7380…`, e11 `a24a2309…`, e12 `1dc03d8f…`); all match.

## Findings (by severity)

### No critical or high findings

No discrepancy exists between the frozen expected records for e09–e12 and the
binary truth as obtained by three independent routes.

### Verified equivalence (medium-informative, all pass)

- **Names / flags / version index / hash**, per needed library: the direct struct
  parse equals the manifest `expected.needed` exactly for all four carriers
  (canonicalized file asc, then (name, other) asc — the manifest's stated
  canonical order). The retained readelf -V parse equals the same set
  (file, name, flags, other). Record counts: e09 3 files/42 versions;
  e10 4/25; e11 61/77; e12 0/0.
- **Linked .dynstr offsets**: manifest `string_table` equals the section-table
  `.dynstr` offset/size — e09 `12880/8972` (0x3250/0x230c), e10
  `194832/313059` (0x2f910/0x4c743), e11 `44880/34454` (0xaf50/0x8696).
  Every `vn_file`/`vna_name` offset resolves inside `.dynstr` to a NUL-terminated
  string equal to the recorded name.
- **e12 empty control**: no `SHT_GNU_verneed` section, no `DT_VERNEED`/
  `DT_VERNEEDNUM` dynamic tags, `.dynstr` size 1 (single NUL); manifest
  `string_table` is null and `needed` is `[]` — the empty record does not invent
  a `.dynstr`.
- **Manifest totals**: 107 needed records / 339 auxiliary records across all 12
  carriers, matching the frozen claim width (R34-C1). e09–e12 contribute 68/144.

### Hash inference distinction

Every one of the 144 checked Vernaux entries has a stored `vna_hash` field whose
bytes equal both the manifest value and the recomputed SysV ELF string hash of the
referenced name. The authoring provenance claim ("direct field read, not
inferred") is therefore consistent with the bytes. Note: because stored field and
recomputed hash coincide for every entry, field-read vs recompute are not
observationally distinguishable by value; the manifest is nonetheless faithful to
the binary in either case. No entry shows a stored hash differing from the SysV
hash (which would have proven a raw field read) and none is missing.

### Minor observation (not a defect)

For e09/e10/e11 the only `vna_other` values absent from the `.gnu.version`
(VERSYM) array are the `GLIBC_ABI_DT_RELR` anchors (indices 68/82/78
respectively): no symbol in these objects carries that index, so the VERSYM
section never stores it. The manifest records these entries exactly as stored in
the Vernaux chain. This is consistent with ABI-tag anchoring behavior and is not
a record error.

## Residual risk / verification gaps

- Ordering: the manifest canonicalizes (file asc, then (name, other) asc), which
  differs from on-disk Verneed/Vernaux chain order; set equality was verified.
  Whether the production counter compares as sets or ordered lists is outside this
  leaf's review (counter not run per pre-data boundary).
- The production counter/reader and the two schedules are not exercised here;
  this review validates only the expected-record ground truth for e09–e12.
- Capture reproduciblity holds for readelf 2.47 on this host; the retained
  captures were produced by the same version and are byte-identical to re-runs on
  the frozen copies.

## Evidence

`w1/RevOracleC-files/`: `evidence.json` (summary + hashes), `audit_e09_e12.py`
(independent parser), `audit_stdout.txt`, and own readelf outputs
`e{09,10,11,12}-readelf-version-info.txt`.
