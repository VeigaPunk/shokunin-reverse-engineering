# R40-C1 counter contract — what must be frozen for `tools/round-40/c1-counter.py`

Everything below is data or path shape, not prose: the counter enforces exactly these, and a
mismatch is an exit-1 clause or exit-2 freeze failure at scoring time, never a silent pass.

## Frozen paths

The counter exits 2 (`frozen_path_changed`) if any commit in `FREEZE..REV` touches:

1. `plans/round-40-claims.md`
2. `tools/round-40/c1-counter.py`  ← the artifact `c1-counter.py` of this seat, integrated here
3. `.ufo/waves/round-40/c1/carriers.json`
4. `.ufo/waves/round-40/c1/gap-rule.json`
5. every `path`, `oracle`, `nonregular` value inside `carriers.json`

Receipts (`after.json`) are *not* frozen: they must be first added **after** the freeze commit.

## `.ufo/waves/round-40/c1/carriers.json`

```json
{"claim": "R40-C1",
 "carriers": [
   {"id": "V1",
    "path": "corpus/evidence/round-40/c1/V1/carrier.sqsh",
    "sha256": "<64 lowercase hex>",
    "oracle": "corpus/evidence/round-40/c1/V1/oracle.tsv",
    "nonregular": "corpus/evidence/round-40/c1/V1/nonregular.tsv"}]}
```

- `claim`, if present, must be `"R40-C1"`; `target`, if present, must be `4`.
- `projection`, if present, selects the rerun-comparison profile: `plus-extractor` (**default per
  the L1 ruling of round 40 wave 1**), `plus-content`, `plus-mime` or `core` (the draft's six
  fields). It is frozen data on purpose: the freeze chooses how much of the run must be reproduced
  without editing the frozen counter, and the counter echoes its choice as `projection_profile` in
  the score JSON. All four were measured stable across repeated real runs of one carrier
  (`projection-profiles.json`, `depth-replay.json`). `core` is **oracle-closed** (see the
  calibration section); selecting it is a deliberate weakening and must be argued in the freeze.
- unknown keys are ignored, so extra manifest metadata is harmless.
- exactly 4 entries; ids exactly `V1`, `V2`, `L1`, `L2`; 4 distinct pins.
- `receipt` is optional; default `corpus/evidence/round-40/c1/<id>/after.json`.
- every field above is a non-empty string; paths are lane-relative.

## `oracle.tsv` (one row per regular file, independent reader output)

```
<relpath>\t<sha256>\t<size>
```

`relpath` relative to the image root. ≥ 1 row, no duplicate paths, sha256 64 lowercase hex.
Columns beyond the first two are ignored by the counter, so the 3-column reader output is the one
to use.

## `nonregular.tsv` (one row per non-regular inode)

```
<relpath>\t<kind>[\t<detail>]
```

`kind` lowercase (`symlink`, `device`, `fifo`, `socket`, `hardlink`, …). A zero-byte file is valid
and means "no non-regular entries". No duplicate `(relpath, kind)` rows. A tolerated header row
`relative_path<TAB>kind` is skipped.

## `.ufo/waves/round-40/c1/gap-rule.json`

```json
{"claim": "R40-C1",
 "allowed":    {"symlink": ["unpublished-entry"],
                "char-device": [],
                "dir": []},
 "required":   {"symlink": true, "char-device": false},
 "structural": {"unknown-chunk-handler": 1, "depth-limited": 1}}
```

- `allowed` is required and non-empty as an **object**; `allowed[kind]` is a list that **may be
  empty** (an empty list = this kind may not take a path-resolved gap).
- `required` is optional; **default: a kind with a non-empty `allowed` list is required.**
- `structural` is optional: gap kind → per-carrier maximum count, for gaps whose
  `relative_path` is null. unblob emits two such kinds on real members and neither can be
  resolved to a non-regular entry: `unknown-chunk-handler` (a residual chunk, e.g. the
  `round_up(bytes_used, 4096)` tail) and `depth-limited` (a task truncated by max depth).
  A path-less gap with no `structural` allowance fails `gaps_ok`; a `structural` kind that
  carries a path also fails.
- every non-regular kind that appears in any frozen `nonregular.tsv` must be a key of `allowed`
  (binding `gap_rule_ok`). **Keys must be spelled exactly like the reader's kind vocabulary**
  (`.ufo/waves/round-40/w1/artifacts/R40C1Harness`: `dir`, `symlink`, `char-device`,
  `block-device`, `fifo`, `socket`); the counter lowercases but never renames a kind, so
  `"device"` would leave `char-device`/`block-device` uncovered and the binding red.
- semantics: each *path-resolved* gap must match (suffix) exactly one non-regular entry and its
  `kind` must be in `allowed[entry kind]`; each *required* entry must carry ≥ 1 allowed gap;
  a published regular file must never carry a non-regular entry's path.
- the table is fixed from **development** recon only, never from a carrier run (draft P40-C1).

## `after.json`

The REA 6.5.0 `extract-firmware` envelope's `data` object, produced by:
`npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <carrier> <outdir>` with
`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`, unblob 26.6.4, `sasquatch-v4be` 4.5.1 on the child
PATH. Required inside it: `operation: extract_firmware`, `provider.id: unblob`, a chunk naming
`squashfs_v4_be` with no `extraction_failed`, `subject.digest.sha256` == the carrier pin, and
`parameters.output_directory` containing the path segment **`/kaidoku-r40/`** (the round's scratch
segment — a receipt written under another round's scratch fails `run_provenance_ok`).

## Carrier bytes

Big-endian SquashFS v4 (`sqsh`, 4.0) with the AVM layout: `mkfs_time == bytes_used`, both
non-zero and `bytes_used <= file size`, and the 2-byte metadata block header at
`inode_table_start` decoding as a little-endian block length in `1..8192` while the big-endian
decode does not (or the single-block identity `inode_table_start + 2 + len_le ==
directory_table_start` settling a both-plausible header).
A `gen-squashfs.py --endian avm` body (standard BE block lengths + doctored timestamp) fails
`layout_ok`, as does a genuine AVM body with the timestamp normalised.

## Documentation bindings (exact strings)

| binding | requirement |
|---|---|
| `province_core_section` | `PROVINCE.md` contains a line exactly `## Round-40 additions to Core` |
| `province_core_row` | a table row in that section whose **first cell** contains the token `squashfs_v4_be`, whose text matches `AVM[ _-]layout` (case-insensitive) and contains `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` |
| `frontier_note` | a single line containing all of `Round-40 frontier note`, `2026-10-26-r40-avm-be-squashfs-core` and an `AVM layout` token |
| `entry_present` | `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` exists at REV |
| `sourced` | one of its `source: Sxxx` ids has a `corpus/SOURCES.md` 11-column row with `opened` = `2026-10-26` and the entry path or stem in the used-by cell |
| `coverage_map_row` | `corpus/README.md` `## Coverage map` has a table row containing the stem |
| `compression_coverage` | ≥ 1 carrier with compression id 1 (gzip) and ≥ 1 with 2 or 4 (xz) |

## Rerun replay (load bearing)

The counter re-runs each carrier with the extraction parameters **recorded in the committed
receipt** (`parameters.max_depth`, `max_output_bytes`, `max_output_files`), not with REA's
defaults. The L1 ruled `--max-depth 1`, and a depth-1 extraction is `partial`, publishes a
different set and emits an extra `depth-limited` gap:

| comparison (round-39 K5 copy, real REA runs) | core | plus-extractor |
|---|---|---|
| depth 1 vs depth 1, different outdir and staged name | equal | equal |
| depth 1 vs depth 3 | differ | differ (`files`, `extraction_gaps`, `derivations`) |
| depth 3 vs the committed round-39 K5 receipt | equal | equal |
| counter replay of a depth-1 receipt (its own runner) | equal | equal |

Without the replay, every depth-1 receipt would be red at scoring under `plus-extractor` although
the run reproduced the image exactly. Evidence: `depth-replay.json`.

## Calibration limit of the rerun clause (measured)

Under the explicit `core` profile the comparison is **oracle-closed**: a forger holding the carrier pin, `oracle.tsv` and `nonregular.tsv`
can reproduce all six fields without running anything (files from the oracle; chunk = the whole
carve, `0..size`; gaps = one `unpublished-entry` per non-regular path; typenames copyable from
earlier rounds). The rerun clause therefore refuses *cheap* fabrications and any receipt that
misstates the extraction, but not a tables-literate forgery. Measured witness: the selftest case
`core profile accepts a projection-identical (oracle-closed) fabrication` passes while
`plus-extractor profile refuses the same fabrication` fails on `published_bytes`.
`plus-extractor` (the default) is not oracle-closed: derivations edges, engine identity,
`published_bytes` and `coverage` are extractor-determined and were stable on every run measured, so
a receipt that does not come from a run of the pinned bytes cannot match without predicting them.

## Structural gaps and the region's real carriers

`gap-rule.json` must key exactly the reader's kind vocabulary (`dir`, `symlink`, `block-device`,
`char-device`, `fifo`, `socket`) and must carry `"structural": {"unknown-chunk-handler": 1,
"depth-limited": 1}` for the two path-less gap kinds unblob emits on real members. Measured on
recon's own development member envelope (`env-7490-member-d1.json.gz` + `oracle-7490-links.tsv`,
86 symlinks): 88 gaps = 86 `unpublished-entry` + 1 `unknown-chunk-handler` + 1 `depth-limited`;
the clause passes with that map, fails without it, and fails with `depth-limited: 0`.

## Invocation and exit codes

```
python3 tools/round-40/c1-counter.py --root . --rev REV --freeze FREEZE \
        --pkg65 /home/vgpnk/.npm/_npx/<hash>/node_modules/rea-agents [--json-out PATH]
```

- 0 = target met (4 carriers, all 17 clauses per carrier, all 10 bindings)
- 1 = not met (per-carrier clauses and bindings are listed in the JSON)
- 2 = unevaluable: `frozen_path_changed`, `rerun_env_error` (no npx / no node / no unblob /
  unusable REA output), missing frozen table, or `--no-rerun` (`rerun_disabled`)
- `--selftest` is offline (simulated runner, 61 cases); `--selftest-rea` runs the real REA path on
  the retained development image and expects green-then-refused.

## If a carrier cannot be produced

`V2` depends on the vendor-image recon. If it fails, the claim's carrier set changes — which means
editing `TARGET`/`IDS` in this counter **before** the freeze commit. After the freeze, any change
to the tables or the counter is exit 2 by design; there is no post-freeze repair path.
