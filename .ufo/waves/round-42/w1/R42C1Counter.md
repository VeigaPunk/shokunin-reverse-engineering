DONE — `c1-counter.py` ported to R42-C1 (v3 handler family), offline selftest green (121 cases, 14 green / 107 red, exit 0) and the real-REA dev arm green on a v3 image (1/1, all clauses true, rerun projection identical, fabrication red). Two artefacts the counter binds are the L1's to produce before the freeze (`fetch-<id>.json`, `extract-env.json`); they are specified here, not invented in code.

## Axes
- **Coverage**: the v3 family (four unblob 26.6.4 handlers) is now scoreable: superblock probe, per-carrier handler, `sasquatch -le|-be` binding, published chain.
- **Depth**: 21 per-carrier clauses + 12 spec bindings, each with at least one red case; two routed round-41 defects (D4, D5) closed by code, not by prose.
- **Calibration**: every constant that could silently default (handler, endianness, compression, carve length, toolchain, prior pins, package digest) is frozen data; what I could not bind (7z/unsquashfs reader choice, REA package tree digest) is stated as a limit rather than checked loosely.

## What the port does (seat items 1–6 + Sentinel remediations)

| item | implementation |
|---|---|
| (1) v3 superblock probe | `layout_probe(raw, expect)`: magic bytes, `s_major`==3, frozen minor, endianness from the frozen block, `bytes_used` = **u64 at offset 63** (packed v3 struct, `mkfs_time` at unaligned 39), `inode_table_start` 87:95, `directory_table_start` 95:103, metadata header in the **filesystem's** endianness (plausibility 1..8192, single-block identity `its+2+len==dts` when both ends are plausible), compression class read from the inode table's compressed metadata blocks (zlib `78 xx`, LZMA `5d 00`/`00 00 80 00`). Every expected value comes from `carriers.json`; there is no default. |
| (2) handler binding | each carrier freezes `handler` ∈ {`squashfs_v3`,`_ddwrt`,`_broadcom`,`_nonstandard`}; `handler_ok` is equality on `chunks[].handler`; the extract root is the `derivations[]` edge whose handler **equals** it. No `squashfs_v4` prefix test, no hardcoded handler. |
| (3) path rule | exact relative path under the root, prefix **segment-bounded** via `under_root()` (`P == CR or P.startswith(CR + '/')`, never `P.startswith(CR)`); `under_root` is pinned by 6 probes. D5's two findings closed: `diagnostic_rel()` now requires `report.link` to start, segment-bounded, with `trusted_run_root = dirname(parameters.output_directory)` (measured: real receipts write to `<run>/extract` and report links under `<run>/rea-firmware-<uuid>/extracted/...`), so a decoy segment-run fails closed; and `path_shape_ok` rejects a receipt path with an empty/`.`/`..` component or a trailing slash instead of normalising it into an oracle row. |
| (4) oracle format | unchanged from round 41 (`rel ⇥ sha256 ⇥ size`, non-regular `rel ⇥ kind ⇥ detail`); `parse_oracle` now **keeps size** and `oracle_hits` compares rel+sha+size. The counter reads whichever frozen table the carriers name — it is independent of the producer, so `tools/round-42/sqfs3-oracle.py` (backhand + 7z per the L1's ruling) can change without touching this file. |
| (5) `counter_sha256` | `stamp_receipt()` writes `{counter, counter_sha256}` into every receipt `--json-out` produces (success, unevaluable, `--no-rerun`); `write_receipt()` re-reads the bytes it wrote and verifies; `--verify-receipt PATH` exits 0/1/2. Digest is of the **counter file** (round-40 precedent + D4 wording "the sha256 of the counter file it ran"), not a self-referential file hash. |
| (6) constants | `carriers.json`/`gap-rule.json` under `.ufo/waves/round-42/c1/`, receipts `corpus/evidence/round-42/c1/<id>/after.json`, entry `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md`, PROVINCE heading `## Round-42 additions to Core`, scratch segment `/kaidoku-r42/`, `--carrier-cache`, `--work`. Rerun projection and freeze-integrity rule unchanged. |
| A5 carve | `carve_ok = size == chunk_end && frozen length == chunk_end`, where `chunk_end()` reimplements unblob's `_SquashFSBase.calculate_chunk` (bytes_used, extended to `round_up(bu,4096|1024)` when that tail is zero). A padded carrier is **green**; a carve cut at `bytes_used` and a carve with a non-zero tail are red. |
| set equality | `oracle_hits_ok` now requires `oracle_hits == oracle_files == published_rels` **and** `extra_published == []` (published regular set == oracle regular set, both directions). |
| H2 fetch chain | `carriers.json` entry requires `kind:"published"`, `source_id` (S-id), `fetch_receipt` (relative path), `external` (a committed `path` is rejected), https URL, `offset`, `length`; `fetch_receipt_ok` recomputes the frozen chain (url, final_url==url, status 200, content_length>0, image/member/member_sha256, carve_len, pin, tool_sha256) and `carrier_sources_ok` requires the cited SOURCES row to exist and name the URL's host. |
| H3 freshness | `prior_pins()` reads **only** the frozen `tools/round-42/prior-pins.json` (plus an optional explicit `prior_pins` list); the round-41 carriers table is no longer a judgement input — a red case and a green case pin both directions. |
| H4 evidence rule | `XPIN` and `tools/round-42/rea-pkg.json` are frozen paths; `rea_package_problems()` refuses a package whose `package.json` or npx-install `package-lock.json` digest (or `version` 6.5.0) differs from the frozen values; `node` and `npx` resolve under `FIXED_PATH` and are invoked by absolute path. |
| L3/L4 | oracle/nonregular/fetch_receipt are required keys and drift-checked unconditionally; `after.json`/`extract-env.json` are **not** drift-checked (they are added after the freeze — L4 says so) and instead the score receipt carries `evidence_digests{id:{path,sha256}}` for every after-receipt it scored (`check_evidence_digests` asserts it on the green case). |
| H1 extractor identity | `FIXED_PATH = /usr/local/bin:/usr/bin:/bin:$HOME/.local/bin` for the child and for the counter's own lookups; binding `extractor_bin_ok` hashes `realpath` of `sasquatch`/`unblob` under that PATH against `toolchain.*.sha256`; clause `extract_env_ok` requires the committed `extract-env.json` to name the same digests, the same PATH, and a `unblob_log.command_line` that runs `sasquatch` with `-le`/`-be` matching the carrier endianness and **never** `sasquatch-v4be`. |
| B2 | `compression_coverage` (gzip+xz) is gone; replaced by per-carrier `compression` against the frozen block and binding `endianness_coverage` (≥1 LE and ≥1 BE, i.e. both sasquatch legs). |

## Evidence (exact commands, exit codes)

Offline selftest (drives `measure()` in-process with a simulated runner; fixture lanes are throwaway git repos under `$HYAKU_SCRATCH`):

```
cd /fast/scratch/hyaku/kaidoku-r42/R42C1Counter
HYAKU_SCRATCH=/fast/scratch/hyaku TMPDIR=$PWD \
python3 -I -B <artifacts>/R42C1Counter/c1-counter.py --selftest \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
exit 0 → {"cases":121,"green_ok":14,"red_ok":107,
          "path_probes":6,"path_probes_discriminating":3,"root_probes":9,
          "spec_probes":14,"prefix_probes":6,"receipt_probes":6,"failures":[]}
```
(artefact `selftest-offline.json`). The four red cases the seat asked for are present and red: *v4 handler on a v3 carrier* (`handler_ok`), *`x_extract2/...` under root `x_extract`* (`oracle_hits_ok` + 6 `under_root` probes), *missing/ null / mismatched `counter_sha256`* (6 receipt probes + `--verify-receipt`), *carve length ≠ chunk end* (`carve_ok`, both the padded-blob and the frozen-length variant).

Real-REA dev arm (`--selftest-rea`, two live REA 6.5.0 runs of one dev fixture, oracle from `unsquashfs`, second run compared by projection):

```
--dev-carrier <artifacts>/R42C1Counter/fixtures/squashfs_v3_le.bin
exit 0 → selftest_rea "ok"; carriers_matched 1; failing []; oracle_hits [2,2];
         carve {bytes_used 258, chunk_end 258, length 258, size 258};
         extract_root firmware.bin_extract; projection_diff []; rerun projection identical;
         fabrication → met_target false, failing [handler_ok, projection_ok]
         bindings_false ["endianness_coverage"]  (a one-carrier wheel cannot bind both legs)
```
Same command on the DD-WRT `hsqt` fixture (recon, `selftest-rea-ddwrt-le.json`): REA emitted handler **`squashfs_v3_ddwrt`**, chunk `{offset 0, length 320}` = chunk end, root `firmware.bin_extract`, 4 files, 0 gaps, 0 diagnostics, rerun projection identical — but `unsquashfs -n -f -d …` returned **rc 1** on that magic, so its `oracle_ok` is red and the arm stops. Two consequences for the freeze: (i) `hsqt`/`tqsh`/`zlqs`/`shsq` carriers cannot be oracle'd by unsquashfs (and, from the Sentinel's measurements, not by `7z` either) — they need the lane's backhand-based producer; (ii) REA publishes **`null`-handler `derivations[]` edges for individual files**, which the old `squashfs_v4`-prefix rule would have swallowed and a handler-equality rule correctly ignores.

v3 field offsets re-measured on the fixtures (`recon-superblock.json`, produced by calling `layout_probe` directly): LE `hsqs` 4096 B → `bytes_used 258`, `its 132`, `dts 188`, meta header `3600` (LE 54), identity holds, gzip; BE `sqsh` 4096 B → `bytes_used 255`, `its 132`, `dts 185`, meta header `0033` (BE 51), identity holds, gzip; DD-WRT LE `hsqt` 320 B → `bytes_used 320`, `minor 1`, `block_log 17`, meta header `3b00` (LE 59), gzip. This confirms the v3 struct is packed with `mkfs_time` at 39 and `bytes_used` at 63 — the round-41 v4 offsets (40:48) and the AVM marker are wrong for v3, as R42C1Sentinel A4/A8 reported.

No tools were installed, upgraded, moved or removed. Nothing was written outside `.ufo/waves/round-42/w1/R42C1Counter.md` and `…/w1/artifacts/R42C1Counter/`; scratch `/fast/scratch/hyaku/kaidoku-r42/R42C1Counter` was removed after the artefacts were copied.

## Risks / what the L1 must decide before freezing
1. **Two artefacts are not mine to produce.** `fetch-<id>.json` (per carrier, H2) and `corpus/evidence/round-42/c1/<id>/extract-env.json` (per carrier, H1) must be written by `fetch-carrier.py` and `c1-run.sh`. I specified their exact keys in `fetch_receipt_ok()`/`extract_env_ok()`; until they exist the corresponding clauses are red — by design, they are the provenance and extractor evidence.
2. **Schema keys to freeze verbatim** (my reader is strict): carrier `{id,kind:"published",source_id,sha256,handler,superblock{magic,endianness,major,minor?,variant,compression},fetch_receipt,external{url,image_sha256,member,member_sha256,length,offset?},oracle,nonregular,oracle_root?,receipt?,extract_env?}`, spec `{claim:"R42-C1",target,toolchain{sasquatch{sha256},unblob{sha256},sasquatch_v4be{sha256}?},projection?,prior_pins?,carriers[]}`. `external.length` is unblob's **chunk end**, not `bytes_used`.
3. **`endianness_coverage` is a freeze constraint.** If all four carriers are little-endian the claim cannot meet its target. DD-WRT BE (`tqsh`) plus a standard LE image satisfies it; both must also be oracle-able (see 4).
4. **Oracle-pair limit is real, not mine to fix**: `unsquashfs` 4.7.5 reads only standard `hsqs`/`sqsh` v3 (measured: rc 1 on `hsqt` and on `zlqs`), so a DD-WRT/vendor-magic carrier needs the lane's backhand producer as one of the two readers. The counter itself is reader-agnostic.
5. **`endianness`/`compression` are declared-then-witnessed**, not read from a superblock field (v3 has no compression field — A4). `compression` is witnessed behaviourally by the inode table's compressed metadata blocks; if a carrier's inode metadata is entirely stored uncompressed the probe fails closed (`compression undetermined`) rather than guessing.
6. **`rea-pkg.json`**: I recompute `package.json` under `--pkg65` and the npx-install `package-lock.json` (one or two levels up) plus `version == 6.5.0`. A `tree_sha256` is **not** recomputed (its canonical form is not defined by any frozen tool) — do not freeze one and expect it checked; I say this instead of pretending.
7. **Set equality is strict.** A real unblob run that publishes a file the oracle lacks (e.g. a nested image one reader refuses to list) fails `oracle_hits_ok`. Run the dev arm and one candidate carrier through it before the freeze; that is exactly the failure mode QUALITY 84 exists to catch.
8. **`counter_sha256` convention**: digest of the counter file (path in `counter`), verified on write and by `--verify-receipt`. If the freeze wants "digest of the receipt file itself", that is a different fixed-point problem and needs a contract change, not a silent reinterpretation.
9. Not done in this seat (out of scope): installing the file at `tools/round-42/c1-counter.py` (`FROZEN_PATHS` already names that path), and `c1-extra.py` / `c1-run.sh` / `fetch-carrier.py` / `sqfs3-oracle.py`, which other seats own.

## Artifacts
`…/w1/artifacts/R42C1Counter/`:
- `c1-counter.py` (the port; 4911 lines, sha256 `33870cc71e6a…` at hand-off — the L1 installs it at `tools/round-42/c1-counter.py` and the freeze pins the installed digest)
- `selftest-offline.json`, `selftest-rea-standard-le.json`, `selftest-rea-ddwrt-le.json`, `recon-superblock.json`
- `fixtures/{squashfs_v3_le.bin,squashfs_v3_be.bin,squashfs_v3_ddwrt_le.bin}` — unblob 26.6.4 test fixtures (MIT), unmodified; sha256 `0161351c…`, `4e9493d9…`, `e7482db4…`; rebuild:
  `curl -sL https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/squashfs_v3/little_endian/__input__/squashfs_v3_le.bin`
  (analogous paths for `big_endian/__input__/squashfs_v3_be.bin` and `squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3.le.nopad.bin`).
No vendor firmware or extracted bytes were copied into the lane.
