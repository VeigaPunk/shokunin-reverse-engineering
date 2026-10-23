# RevOracleA — independent expected-record audit, e01–e04 (Kaidoku round 34, attempt 1)

Role: read-only prose reviewer (UFO-FSD reviewer). No carrier executed, no parser run as data
producer, no REA run, no production/shared writes. Sandbox
`/fast/scratch/hyaku/kaidoku-r34/w1/RevOracleA` verified at freeze
`54a87a51a865ab931fd355e767303337b05cccf4` (`git rev-parse HEAD`, clean tree, 0 modified).
Tooling installs: **none** (host `readelf` GNU Binutils 2.47 and `python3` sufficient).
Routing: no model call made; answering model not visible to this seat.

## Findings by severity

### Critical / Major / Minor defects
**None.** Every checked field of frozen expected records e01–e04 matched the carrier bytes
exactly, and the full-manifest extension found zero field-level mismatches across all 12 carriers
(2494 individual PASS checks; the only 40 non-PASS lines are two documented harness-limitation
classes and one informational check, see Residual risk).

### Verified equivalences (evidence)

Freeze/digest pins (UTC 2026-10-23 ~10:47–10:52Z):
- `sha256sum` sandbox `.ufo/waves/round-34/expected.json` →
  `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d` = `claims.json.manifest_sha256`. Exit 0.
- Carriers e01–e04 sha256 in sandbox copy = `claims.json.frozen_inputs` pins, exit 0:
  e01 `8398af7d…f0662`, e02 `dcd2b469…5338abbf`, e03 `64c10d9b…959bd61b`, e04 `24c47749…b611bda`.
- Carriers byte-identical to their `source_path` originals: `sha256sum /usr/bin/{true,perl,curl,xz}`
  → identical digests 4/4 (byte-exact-copy claim confirmed for the audited subset).

Retained readelf evidence integrity (`…/prep/R34Expected-files/captured/{e01..e04}/probes.json`):
all 16 stdout digests (4 probes × 4 carriers) recomputed and equal to recorded `stdout_sha256`;
`stderr` all empty-sha. Exit 0 per probes.json.

Independent re-observation (my own static readelf on private sandbox copies; argv
`readelf --version-info --wide corpus/evidence/round-34/elf/eNN.bin` etc., exit 0 ×16):
outputs **byte-identical** to retained `readelf-version-info.txt` for e01–e04 (`diff -q` IDENTICAL ×4).
Retained captures are therefore faithful at the reviewed binutils 2.47.

Byte-level structural audit (stdlib-`struct` parser over sandbox copies; script archived at
`RevOracleA-files/audit.py`, outputs `audit.out`/`audit-all.out`; main run UTC 2026-10-23T10:59:23Z
capture batch, exit 0 semantics = only known-harness FAILs):

- e01 `/usr/bin/true`: 1 needed `libc.so.6`, 8 aux; e02 `/usr/bin/perl`: 1 needed, 4 aux;
  e03 `/usr/bin/curl`: 2 needed (`libc.so.6` 10 aux, `libcurl.so.4` 1 aux); e04 `/usr/bin/xz`:
  2 needed (`libc.so.6` 13 aux, `liblzma.so.5` 4 aux). Counts equal frozen manifests exactly.
- **Names**: each expected `name` is the C string at the recorded `vna_name` offset inside the
  `.dynstr` section it links to — in-bounds, byte-for-byte, NUL-terminated (checked per record).
  Expected `file` equals the `vn_file` string likewise.
- **Flags**: manifest `flags` equals raw 16-bit `vna_flags` per aux (all 0 = none here).
- **Index (`other`)**: manifest `other` equals raw 16-bit `vna_other`; unique per needed file in
  all records; `.gnu.version_r` `sh_link` → `.dynstr`; `vn_version == 1`; `sh_info == needed count`.
- **Hash — direct read, not inference**: manifest `hash` equals the raw 32-bit `vna_hash` for
  every aux record. Independently, `elf_hash(name)` (SysV) equals it too on the pristine
  carriers — but the manifest value's provenance is the stored field
  (`author_expected.py:212-221,585-590`: "vna_hash field read directly … not an inferred value";
  independently re-verified by me from bytes). The derivability agreement is a **pristine-only
  property**: counter schedule 1 translates `.dynstr` in place (Sattolo single-cycle shuffle of a
  67-char ASCII alphabet; same length, no fixed points; `version-needs-counter.py:79-106`) while
  `vna_hash` bytes stay untouched, and the challenge prediction keeps original hashes with
  translated names — so any reader that recomputes or validates the hash against the name fails
  exactly there. The frozen reader `tools/round-34/elf-version-needs.py:29-31,487,627` emits
  `vna_hash` verbatim and "never recomputes or compares a hash". Consistent triad: manifest =
  stored bytes; challenge breaks derivability; reader never derives.
- **Canonicalization (documented, exercised)**: manifest versions are ordered lexicographically
  by name within each file (author sort key `(name, other)`, `author_expected.py:280`); manifest
  `needed` is sorted by `file`. Binary verneed order **differs** from sorted-by-file in 7 carriers
  (e03: `libcurl.so.4` before `libc.so.6`; e06,e07,e08,e09,e10,e11 similar). This is a deliberate
  positional-matching discriminator: a reader that walks verneed in file order and compares
  positionally fails e03 and six others. Counter `canonical()` enforces `(name, other)`-sorted
  versions (`version-needs-counter.py:52-53`); frozen reader sorts by `file` then
  `(name, other, flags, hash)` (`elf-version-needs.py:313-319`) — equivalent to the manifest key
  on this corpus because `(name, other)` is unique per file (verified).
- **Versym cross-check (e01–e04)**: every `.gnu.version` reference ≥2 is covered by some
  `vna_other` in the four audited carriers (none has `.gnu.version_d` — grep count 0 each).
  `GLIBC_ABI_DT_RELR` aux entries are referenced by no dynsym (e01 idx 9, e02 5, e03 12, e04 18) —
  expected for RELR, not a record defect; reader performs no versym cross-check
  (`elf-version-needs.py:562`), matching the manifest's scope.
- **e12 empty-control coherence**: expected `{"schema":1,"needed":[]}`, no `.gnu.version_r`
  section, `string_table: null` → both counter schedules run the pristine bytes; no `.dynstr`
  invented. Matches claim `empty_control`.
- **Width claim**: aggregate static parse of all 12 carriers = **needed 107, aux 339** — exactly
  the claim width statement ("107 needed records and 339 auxiliary records").
- **Challenge schedule is runtime-random, not the author's fixed schedule**: counter generates
  the translation with `secrets.randbelow` per invocation (`version-needs-counter.py:95-105,121`);
  imports are argparse/hashlib/json/os/secrets only — no load of `prep/challenge/schedule.json`
  anywhere in the production path read. Consistent with "Expected-author optional fixed schedule
  is NOT used by the production counter".

## Residual risk
1. **Harness-limitation classes, not defects** (40 non-PASS lines, all accounted): (a) informational
   binary-vs-sorted verneed order in 7 carriers (deliberate canonicalization, above); (b) my
   versym-coverage check does not model verdef-referenced versym indexes / hidden-bit entries
   (`0x8000`, e.g. e10 32770/32781) on definition-heavy carriers e06–e11; (c) e12 absence check.
   None touches the e01–e04 field audit.
2. Reader sort key `(name, other, flags, hash)` vs manifest `(name, other)` is equivalent only
   while `(name, other)` is unique per file; a future manifest with duplicate names per file would
   rely on the fuller key. No present impact (verified unique in all 12).
3. Audit limited to static bytes; loader-level semantics (e.g. whether glibc accepts the RELR aux)
   unverified and out of claim scope (no runtime/authenticity claim).

## Verification gaps
- I did not re-verify carriers e05–e11 against host originals byte-for-byte (digest equality to
  manifest pin only for the manifest as a whole; per-carrier field audit did cover all 12).
- No execution of `version-needs-counter.py`/`elf-version-needs.py` (prohibited for this seat);
  counter/reader behavior statements above are code-read citations, not runtime observations.
- `author_expected.py` checks.json (122.9 KB) per-carrier `string_offsets` were not cross-read;
  my offsets were derived independently from bytes instead.

Evidence archived: `RevOracleA-files/{audit.py,audit.out,audit-all.out,e01..e04.vinfo}`.
