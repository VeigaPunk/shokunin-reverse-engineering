# R43LabTuple — M42-2 mechanics receipt (round 43 wave 1, pre-freeze)

**Verdict: CONFIRMED** — on the committed round-42 C02 envelope, the base-committed
`observed_features()` extracts `gap_kinds = {depth-limited, extractor-failure,
unpublished-entry}` while the manifest declares `{extractor-failure,
unpublished-entry}`; the diff is exactly one field (`gap_kinds`) and exactly one
kind (`depth-limited`, observed-only). All other five binding fields and both
extras match.

## Probe (read-only, no REA run, no lane writes)

- Generator source: `git show 6b9e64fe7e0de202d9383baad5792fbfe039a743:tools/round-42/heldout-gen-v4.py`
  copied to scratch (`heldout-gen-v4.py`, sha256 `c2b1641ad6be…`); imported via
  `importlib.util.spec_from_file_location`; `observed_features.__code__.co_filename`
  confirms the scratch copy, line 2964.
- Input record: committed `corpus/evidence/round-42/c2/heldout/C02/run.json` (the
  generator's own `record` dict, produced by `_envelope_parts` in `run_rea`).
- Script + full output: `artifacts/R43LabTuple/probe_c02.py`,
  `artifacts/R43LabTuple/probe-output.txt`.

## Both tuples and the diff

| field | declared (manifest `carriers[].declared_features`, C02) | observed (`observed_features(C02 run.json record)`) |
|---|---|---|
| handler_set | `["squashfs_v4_be"]` | `["squashfs_v4_be"]` |
| **gap_kinds** | `["extractor-failure", "unpublished-entry"]` | `["depth-limited", "extractor-failure", "unpublished-entry"]` |
| gap_dependencies | `[]` | `[]` |
| symlink_removed | `false` | `false` |
| published | `"nonzero"` | `"nonzero"` |
| be_argv | `"yes"` | `"yes"` |
| extras | `extraction_failed=true, max_depth=1` | `extraction_failed=True, max_depth=1` |

`feature_diff(expected_for(entry), observed)` prints exactly one line:

```
gap_kinds: want ['extractor-failure', 'unpublished-entry'] got ['depth-limited', 'extractor-failure', 'unpublished-entry']
```

declared-only: `[]`; observed-only: `['depth-limited']`. Diff count: 1.

## Which envelope field carries `depth-limited`

`corpus/evidence/round-42/c2/heldout/C02/rea-full.json`:

- **`data.normalized_result.extraction_gaps[1]`** — `{"kind": "depth-limited",
  "input_path": "$output/firmware.bin_extract", "handler": null, "range": null,
  "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab", …}`
  (excerpt: `artifacts/R43LabTuple/c02-gap-excerpt.json`). `extraction_gaps[0]` is
  the `extractor-failure` gap on `$input`; `[2]` is `unpublished-entry` on
  `$output/firmware.bin_extract/-75othk5`.
- Mirrored at **`data.normalized_result.depth_limited_paths[0]`** =
  `"$output/firmware.bin_extract"`.
- The gap's `continuation_id` equals **`data.normalized_result.extraction_continuations[1].id`**
  (`3b54e297…`), instruction: "Rerun extract_firmware with a higher max_depth (up
  to 10) and a fresh output_directory to descend into this path."

## From which chunk/sibling REA mints it

There is **one chunk, no sibling**: `data.normalized_result.chunks[0]` =
`squashfs_v4_be`, range 0–1664, `extraction_failed: true` (manifest `layout:
"single-image"`, factors `two_chunk: false, damage: 1, max_depth: 1`). The
`depth-limited` gap is minted on **the failed root chunk's own extraction-output
directory** `$output/firmware.bin_extract`: the diagnostic at
`data.normalized_result.diagnostics[0].report` records
`sasquatch-v4be -be -no-exit-code -f -d …/firmware.bin_extract …/firmware.bin`,
exit_code 1 — yet with `-no-exit-code` the run still wrote partial output (6
published files under `firmware.bin_extract/`, one 14319 B; 1 unpublished in-tree
symlink `firmware.bin_extract/-75othk5 → -9n/t48ffl78s`). REA's walker reached that
directory at the `--max-depth 1` ceiling and minted `depth-limited` there. The
generator's oracle clause `combo_declared` (round-42 source lines ~941–946) sets
`reached = ((not damage_effective) or residue or two_chunk)` → False for a damaged
single root chunk ("a damaged root chunk alone mints nothing"), so the declared
tuple dropped the kind REA 6.5.0 actually minted. [INFERENCE: the oracle's
dev-arm measurement never covered a failing single root chunk whose partial output
directory still reached the ceiling; C02's draw is that case.]

## Cross-references

- Round-42 stop receipt `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`:
  `bindings_false: ["observed_features_match_declared"]` — the only false binding;
  the round stopped honestly on exactly this diff (commit `eb8215ac…`).
- This confirms claim-draft R43-C1's description of M42-2 / R42-CL1 and feeds
  QUALITY 85: the round-43 generator (`heldout-gen-v4r43.py`) must declare what
  `observed_features()` measures, i.e. include `depth-limited` for this shape.

## Evidence & limits

Commands (run in scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43LabTuple`):
`git show 6b9e64fe…:tools/round-42/heldout-gen-v4.py > heldout-gen-v4.py`;
`python3 -I -B probe_c02.py` (exit 0; output in artifacts). Envelope/manifest/run
records read from the committed lane paths above; no extractor was run, no
carrier was modified. Probe is a replay of the generator's own extraction against
its own committed record — it cannot detect envelope tampering after the run, but
`digest_matches_carrier: true` is recorded in `run.json` and the receipt's
`envelopes_valid` binding was true. The observed tuple is read from the committed
envelope, matching the round-42 counter's method.
