# Port audit — round-41 → round-50 `c1-counter.py`

Seat RevPrevArt, round 50 attempt 2, wave 3 (build). Verdict-first; scope is the
R41→R50 counter port and scoring-time drift only. Both files are frozen and were
read read-only; the working-tree bytes equal the base revision
`f890bbead20ca2c549487167f56876ae47f1e1a4` (`git diff --stat f890bbe…` on the two
counters is empty; r41 sha256 `bbabbfec…c8845cfc`, r50 sha256 `9820811b…9bd813`).

Verification receipts (offline selftests, run against a stub rea-agents 6.5.0
package with xpin-compatible `dist/domain/canonicalDigest.js` +
`dist/domain/evidence.js` — NOT the npx package; no REA was invoked):

| check | command | exit | receipt sha256 | UTC |
|---|---|---|---|---|
| r50 selftest | `python3 tools/round-50/c1-counter.py --selftest --pkg65 $S/stub-rea --work $S/work` (TMPDIR/HYAKU_SCRATCH=$S) | 0 | `8c3476fa…d008705` | 2026-10-29T20:46Z |
| r41 control selftest | `python3 tools/round-41/c1-counter.py --selftest --pkg65 $S/stub-rea` | 0 | `34c4f06e…e3d741` | 2026-10-29T20:46Z |
| r50 py_compile | `python3 -m py_compile tools/round-50/c1-counter.py` | 0 | — | — |
| r41 py_compile | `python3 -m py_compile tools/round-41/c1-counter.py` | 0 | — | — |

r50 selftest result: 169 cases, green_ok 17, red_ok 152, failures 0,
path_probes 6 (3 discriminating), root_probes 8, spec_probes 43.
r41 control result: 97 cases, green_ok 12, red_ok 85, failures 0.

## Verdict

**No scoring-time drift found.** Every behavioural delta the seat was asked to
confirm is present and implemented as the PORT-DELTA describes; no round-41
clause that should have been ported was dropped (the only removals are the
BE-specific machinery and the `compression_coverage` binding, both disclosed in
PORT-DELTA §4 / C13). Both counters' offline selftests pass against a stub
package. The four documentation-binding literals are quoted verbatim in §4 for
the landing text. One calibration note (sasquatch version wording) at the end.

## 1. Behavioural deltas confirmed present

| delta | r41 | r50 (line) | status |
|---|---|---|---|
| handler name | `HANDLER='squashfs_v4_be'` (r41:287) | `HANDLER='squashfs_v4_le'` (r50:381) | ✅ drives `HANDLER_RE`, `squashfs_roots`, `subject_root`, `mk_env`, `_province` |
| superblock layout | `layout_probe` BE `sqsh` + LE-metadata-header test (r41:682-766) | `layout_probe` LE `hsqs`, v4.0, `compression==4`, `mkfs_time==bytes_used`, `0<bytes_used<=size`, `0<its<dts<=bytes_used` (r50:992-1059) | ✅ rewritten; all BE decode / `meta_signal` / `METADATA_MAX` removed (B2) |
| sasquatch binary | `c1-run.sh` precondition `sasquatch-v4be` (harness, not counter); counter ran `npx -y rea-agents@6.5.0` | `toolchain_record` requires `sasquatch` on `FIXED_PATH`, records sha256+version_line; `sasquatch-v4be` NOT required (r50:1968-2003, 2016-2026); child `PATH=FIXED_PATH` (r50:2041) | ✅ B14; unblob `26.6.4` and REA `6.5.0` pinned, node on FIXED_PATH |
| target ids | `IDS=('V3','V4','L3','L4')` (r41:293) | `IDS=('g7581','g7582','c6490','c6430')` (r50:395), case-insensitive compare in `carriers_spec` | ✅ C5 |
| round tokens | `R41-C1`, `kaidoku-r41`, `2026-10-26`, `round-41` | `R50-C1`, `kaidoku-r50`, `OPENED_DATES=('2026-10-28','2026-10-29')`, `round-50` (r50:380,393,397) | ✅ no stale r41 token survives except intentional references (prior-pin tables, frozen-path inputs, negative selftest fixtures) — see §2 |
| provider_timeout retry | none (single run) | `MAX_REA_ATTEMPTS=3` (r50:1923); rerun loop repeats only on `error.code=='provider_timeout'`, fresh outdir (r50:2057-2077); persistent timeout → exit 2 `rerun_env_error` (r50:2393-2398) | ✅ B-retries; selftest case `rerun hits REA provider_timeout (3 attempts) is unevaluable` |
| fetch containment | external carrier support (r41 `measure` reads `--carrier-cache`) | `carriers_spec` validates the frozen external chain `url/image_sha256/member/member_sha256/length` (+`nested.sha256`) (r50:938-980); `measure` reads `<pin>.bin` from `--carrier-cache` only (r50:2268-2274) | ✅ chain bound in the table (routed R40-CL6); bytes never committed |
| oracle re-derivation | none (2-column oracle, size never compared) | `rederive_oracle` runs `/usr/bin/unsquashfs` v4.7.5 with `ORACLE_FLAGS` (r50:2094-2145); clause `oracle_rederived_ok` set-equal both directions (r50:2295-2312) | ✅ B25; `UNSQUASHFS`/`UNSQUASHFS_VERSION`/`ORACLE_FLAGS` at r50:402-405 |

Widened-without-rename deltas (C14) confirmed by reading `measure` (r50:2147-2478)
against r41 (r41:1470-1740): `oracle_hits_ok` now requires size equality AND
`extra_published==[]`; `handler_ok` is family-equality not membership;
`receipt_fresh` uses full-history `all_adds`; `oracle_ok` requires a 3-column
table; `run_provenance_ok` is a prefix test; `projection_ok` binds node+pkg65
toolchain and the frozen `plus-extractor` profile. New in the port and present:
`parameters_ok` (frozen `rea_parameters`), `evidence_envelope_ok`,
`path_shape_ok`, `oracle_rederived_ok`, `CounterNotFrozen` (running counter ==
frozen counter), merge-aware+blob-equality `frozen_drift`, and
`tables_absent_at_freeze` under `frozen_tables_valid`.

## 2. Round-41 clauses that should have been ported but were not

**None.** CLAUSES diff (r41:303-305 → r50:439-444):

- r41 19 clauses; all 19 present in r50 (`in r41 not r50: []`).
- r50 adds 4: `oracle_rederived_ok`, `evidence_envelope_ok`, `path_shape_ok`, `parameters_ok`.

BINDINGS diff (r41:301-302 → r50:436-438):

- r41 10 bindings; 9 ported. The one removal is `compression_coverage` — deliberate
  and disclosed (PORT-DELTA C13: all four frozen LE carriers are xz, so the
  per-carrier `layout_ok` compression-id-4 test replaces the gzip+xz pairing).
  The round-41 comment that mislabelled compression id 2 as "squashfs-tools XZ"
  is also gone (id 2 is LZMA; only id 4 is accepted now, r50:400).

Every round-41 token that still appears in the r50 file is intentional, verified
by grep: docstring provenance lines; `PRIOR_CARRIER_TABLES` /
`PRIOR_PIN_CANDIDATES` / `REA_PKG_CANDIDATES` (round-41/42/49 prior-pin sources,
r50:386-391); `FROZEN_PATHS` carrying `tools/round-41/{fetch-vendor,sqfs-list}.py`
(the two r41 tools the counter's docstring/oracle arm cite, r50:415-416); and
selftest fixtures that *plant* round-41 shapes as negatives (`squashfs_v4_be`
handler, `AVM layout` row token, `kaidoku-r41` provenance, a round-41 carrier
table, a r41 cited entry). None leaks into a scored clause or binding.

## 3. LE-specific clauses and their selftest cases

The genuinely LE-specific clause is `layout_ok` (the frozen little-endian
superblock); the handler family test is the other LE-shaped gate.

- **`layout_ok` / `layout_probe`** (r50:992-1059). Selftest (r50:3181-3241):
  17 direct `layout_case` probes, each an end-to-end red `layout_ok` AND a direct
  `layout_probe` reason check — standard-LE (real timestamp), marker off-by-one,
  BE AVM-marker image (`sqsh`), standard BE, `hsqs` magic over BE fields,
  compression id 1/2/6, version 3.0 and 4.1, `bytes_used` beyond the file,
  inode-table-after-directory-table, directory-table past `bytes_used`,
  inode-table at 0, shorter than 96 bytes — plus the accepted frozen-layout probe.
  Two CTL-C1-4 end-to-end cases (r50:3247-3255): a standard LE carrier planted
  under the genuine pin is red on `carrier_pin_ok` AND `layout_ok`.
- **`handler_ok`** (r50:2330-2334; `SQUASHFS_HANDLER_RE` r50:429). Selftest
  (r50:3263-3296): BE handler `squashfs_v4_be`, `squashfs_v3`, bare `squashfs_v4`,
  one LE + one BE chunk, and no-squashfs-chunk — all red `handler_ok`.
- Supporting (not LE-format but LE-round) clauses with cases: `oracle_rederived_ok`
  (r50:3518-3587, incl. real unsquashfs probes via `lane_le_avm_image`),
  `carve_ok` external/length cases (r50:3451-3456, 4355-4359), `carrier_present`
  `--carrier-cache` cases (r50:3738-3748), `run_provenance_ok` prefix cases
  (r50:3347-3362), `parameters_ok` depth/budget cases (r50:3364-3373),
  `provider_timeout` unevaluable case (r50:3168-3172).

## 4. Documentation-binding clauses — exact literals (load-bearing)

The landing text MUST use these verbatim; a wording miss is a red binding.

- **PROVINCE section name** (r50:379): `## Round-50 additions to Core`
  Matched by exact line equality (`section()` uses `lines.index(heading)`), then
  rows until the next `## ` line. Case/space-exact.
- **province_core_row** (r50:2443-2449): first table cell of the section must
  contain the word-bounded handler `squashfs_v4_le` (regex
  `(?<![A-Za-z0-9_-])squashfs_v4_le(?![A-Za-z0-9_-])`), the row text must match
  `AVM[ _-]marker` (case-insensitive; `AVM marker` / `AVM-marker` / `AVM_marker`
  accepted, `AVM  marker` double-space and the BE-era `AVM layout` token are NOT),
  with the entry path removed before the token search, and the row must cite the
  entry path `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`.
- **frontier-note tokens** (r50:380, 427-428): the line must contain
  `Round-50 frontier note` AND the stem `2026-10-28-r50-avm-le-squashfs-core` AND
  an LE-AVM token matching `\bLE[ _-]AVM\b|\bAVM[ _-]LE\b` (case-insensitive:
  `LE AVM`, `LE-AVM`, `AVM LE`, `AVM-LE`, `AVM_LE` accepted; `LE  AVM` double-space
  and `AVM LEAN`/`LEAVM` not), searched with the stem removed — the stem alone
  spells `avm-le` and does NOT satisfy the token (verified in §check).
- **entry stem token** (r50:377-378): stem `2026-10-28-r50-avm-le-squashfs-core`,
  entry path `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`.
- **README coverage map** (r50:2487-2491): a `## Coverage map` section in
  `corpus/README.md` containing a table row (`|…`) with the stem verbatim.
- **SOURCES window** (r50:393, 2472-2485): entry `source:` lines must name S-ids;
  a `corpus/SOURCES.md` row matching `^ {0,3}\|\s*S\d{3,}\s*\|` with exactly 11
  cells, `c[8]` (opened) ∈ `{2026-10-28, 2026-10-29}`, and `c[10]` (used-by)
  containing the entry path or stem. Row shape: `| <sid> | … | <opened@8> | … |
  <used-by@10> |`.

## Calibration note (not drift)

The plan predicate (plans/round-50-claims.md, R50-C1) says "sasquatch 4.5.1 on the
child PATH"; the counter enforces sasquatch *presence* on `FIXED_PATH` and records
its sha256 + `version_line` in `rerun_toolchain`, but does NOT hard-fail a version
other than 4.5.1 (unblob `26.6.4`, REA `6.5.0`, and unsquashfs `4.7.5` ARE
version-pinned). This matches PORT-DELTA B14's scoping (resolution, not version
equality) and the binary is fingerprinted, so it is not a scoring-time hole; it is
a wording/strictness nuance the L1 may choose to align (pin sasquatch version) or
record as a disclosed limit. Flagged for the freeze; no action required from this seat.
