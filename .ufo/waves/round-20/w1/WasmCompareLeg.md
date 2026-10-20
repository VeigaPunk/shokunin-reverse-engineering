# C2 — `compare-wasm-interfaces`

## Observations

- **Observed:** `npx -y rea-agents@6.5.0 compare-wasm-interfaces --schema` exited 0. The CLI takes one `input` string containing inline JSON or a JSON file with complete left/right Evidence and `scope`; the accepted scopes are `imports`, `exports`, and `both` (schema output: `.ufo/waves/round-20/evidence/c2/wasm-compare/schema-compare.stdout.txt:1-8`; receipt and exit: `.ufo/waves/round-20/evidence/c2/wasm-compare/schema-compare.receipt.json:2-27`). The companion inspect schema takes `path` and optional `glue_paths` / `candidate_paths` (`.ufo/waves/round-20/evidence/c2/wasm-compare/schema-inspect.stdout.txt:1-22`).
- **Observed:** `find / -xdev -type f -name '*.wasm' -print 2>/dev/null` yielded seven paths in the captured inventory. The selected module pair is `zxing_reader.wasm` from `@oai/browser-desktop@0.1.1` and `@oai/cua@0.2.6`; both subjects are SHA-256 `0e8d688d71932ebb6b8b33f700d43d3cb997f59ed9cab3c05102d7f10288a392`. The browser/chrome plugin copies form the identical-bytes control pair with that same digest (`.ufo/waves/round-20/evidence/c2/wasm-compare/carrier-selection.json:2-35`).
- **Observed:** Four complete JSON inspect Evidence envelopes used by the compares were retained as xz-compressed stdout, with raw and compressed digests in their receipts. The selected inspect IDs, package/path labels, and subject digests are indexed at `.ufo/waves/round-20/evidence/c2/wasm-compare/evidence-index.jsonl:1-4`; each inspector recorded a 1,065,866-byte subject and exit 0 (for example, `.ufo/waves/round-20/evidence/c2/wasm-compare/inspect-version-browser-desktop-0.1.1-json.receipt.json:9-36`). Four initial default-format inspect outputs and their receipts are also retained.
- **Observed:** Each pair was compared separately for all three scopes. Every call exited 0; all results report `coverage: complete-within-inputs`, zero added/removed/changed/unknown, 77 unchanged imports, 21 unchanged exports, and 98 unchanged total for `both`. Comparison Evidence IDs and stdout digests are indexed at `.ufo/waves/round-20/evidence/c2/wasm-compare/evidence-index.jsonl:5-10`. The six raw JSON outputs are `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-version-imports.stdout.txt:1`, `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-version-exports.stdout.txt:1`, `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-version-both.stdout.txt:1`, `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-control-imports.stdout.txt:1`, `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-control-exports.stdout.txt:1`, and `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-control-both.stdout.txt:1`; argv, timestamps, configured `REA_WABT_BIN_DIRECTORY`, subject carrier hashes, input JSON hashes, exit codes, and stdout/stderr hashes are in their matching receipt files (e.g. `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-version-imports.receipt.json:2-45`).

| Pair | Imports Evidence ID | Exports Evidence ID | Both Evidence ID | Result |
|---|---|---|---|---|
| `@oai/browser-desktop@0.1.1` vs `@oai/cua@0.2.6` | `ev_93fc0a9a58dec1e47907d50e40e388f6f295b343b05431f6d643f96df90d7a6c` | `ev_cccc6ff821b6c813ac5b52fa5bec0878ede8a7341298ede869214607d3454d35` | `ev_ca8b59b0c4763f0842ba684a50800fc7da5d9450e174c6ea9df2e85e1b1f34b9` | 77 / 21 / 98 unchanged; zero differences or unknowns |
| Browser plugin vs Chrome plugin control | `ev_00fbc76d782c9953ad92004388f0f5b18311a674a22f626e1cd65c81d62708fd` | `ev_c912963cbdf1eec5a1aeec6224954e7b63857c80aa882a726091ab78705eb26d` | `ev_db516e1ccf66ef06a65dad97fe1c27065bdcf44fbd42efc9c4face9826cd95d9` | 77 / 21 / 98 unchanged; zero differences or unknowns |

## Calibration and limitations

- **Observed:** Although the parent packages are distinct releases, the selected version-pair modules have identical bytes. The direct host scan contained no repeated `zxing_reader.wasm` with a distinct digest; therefore this run exercises a real cross-release pair and an identical-byte control, but does **not** measure a changed-byte version regression (`.ufo/waves/round-20/evidence/c2/wasm-compare/carrier-selection.json:5-29`).
- **Observed:** REA reports equality of declared interfaces only. Its output explicitly limits conclusions about runtime/ABI compatibility, successful linking, original-source identity, unsupported signature semantics, and duplicate names (see the `limitations` fields in each compare output, e.g. `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-version-both.stdout.txt:1`). No target module was executed.
- **Inferred:** Since both selected pairs have the same subject digest, matching results are expected for these inputs; they do not establish that the comparison distinguishes changed interfaces.

## Files and checks

- Patch: `.ufo/waves/round-20/w1/patches/WasmCompareLeg-2.patch`; it carries the retained receipts, schema outputs, compressed inspect envelopes, six compare outputs, `carrier-selection.json`, and `evidence-index.jsonl` under `.ufo/waves/round-20/evidence/c2/wasm-compare/`.
- **Observed base:** the isolated clone reported `14f0260ad319ecc26994381b2415d5a999003375`.
- No tools were installed or updated. No build, test, lint, or formatter was run.

## Staged patch stat

`git -C /tmp/kr20-WasmCompareLeg-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` (observed summary: 50 files, +717, -0):

```text
.../c2/wasm-compare/carrier-selection.json         |  37 +++++++++++++++++
.../wasm-compare/compare-control-both.receipt.json |  46 +++++++++++++++++++++
.../wasm-compare/compare-control-both.stderr.txt   |   0
.../wasm-compare/compare-control-both.stdout.txt   |   1 +
.../compare-control-exports.receipt.json           |  46 +++++++++++++++++++++
.../compare-control-exports.stderr.txt             |   0
.../compare-control-exports.stdout.txt             |   1 +
.../compare-control-imports.receipt.json           |  46 +++++++++++++++++++++
.../compare-control-imports.stderr.txt             |   0
.../compare-control-imports.stdout.txt             |   1 +
.../wasm-compare/compare-version-both.receipt.json |  46 +++++++++++++++++++++
.../wasm-compare/compare-version-both.stderr.txt   |   0
.../wasm-compare/compare-version-both.stdout.txt   |   1 +
.../compare-version-exports.receipt.json           |  46 +++++++++++++++++++++
.../compare-version-exports.stderr.txt             |   0
.../compare-version-exports.stdout.txt             |   1 +
.../compare-version-imports.receipt.json           |  46 +++++++++++++++++++++
.../compare-version-imports.stderr.txt             |   0
.../compare-version-imports.stdout.txt             |   1 +
.../evidence/c2/wasm-compare/evidence-index.jsonl  |  10 +++++
...nspect-control-browser-plugin-json.receipt.json |  38 +++++++++++++++++
.../inspect-control-browser-plugin-json.stderr.txt |   0
.../inspect-control-browser-plugin-json.stdout.xz  | Bin 0 -> 959708 bytes
.../inspect-control-browser-plugin.receipt.json    |  37 +++++++++++++++++
.../inspect-control-browser-plugin.stderr.txt      |   0
.../inspect-control-browser-plugin.stdout.xz       | Bin 0 -> 960284 bytes
...inspect-control-chrome-plugin-json.receipt.json |  38 +++++++++++++++++
.../inspect-control-chrome-plugin-json.stderr.txt  |   0
.../inspect-control-chrome-plugin-json.stdout.xz   | Bin 0 -> 959664 bytes
.../inspect-control-chrome-plugin.receipt.json     |  37 +++++++++++++++++
.../inspect-control-chrome-plugin.stderr.txt       |   0
.../inspect-control-chrome-plugin.stdout.xz        | Bin 0 -> 959820 bytes
...version-browser-desktop-0.1.1-json.receipt.json |  38 +++++++++++++++++
...t-version-browser-desktop-0.1.1-json.stderr.txt |   0
...ct-version-browser-desktop-0.1.1-json.stdout.xz | Bin 0 -> 959720 bytes
...pect-version-browser-desktop-0.1.1.receipt.json |  37 +++++++++++++++++
...nspect-version-browser-desktop-0.1.1.stderr.txt |   0
...inspect-version-browser-desktop-0.1.1.stdout.xz | Bin 0 -> 959808 bytes
.../inspect-version-cua-0.2.6-json.receipt.json    |  38 +++++++++++++++++
.../inspect-version-cua-0.2.6-json.stderr.txt      |   0
.../inspect-version-cua-0.2.6-json.stdout.xz       | Bin 0 -> 959740 bytes
.../inspect-version-cua-0.2.6.receipt.json         |  37 +++++++++++++++++
.../inspect-version-cua-0.2.6.stderr.txt           |   0
.../inspect-version-cua-0.2.6.stdout.xz            | Bin 0 -> 959960 bytes
.../c2/wasm-compare/schema-compare.receipt.json    |  29 +++++++++++++
.../c2/wasm-compare/schema-compare.stderr.txt      |   0
.../c2/wasm-compare/schema-compare.stdout.txt      |   8 ++++
.../c2/wasm-compare/schema-inspect.receipt.json    |  29 +++++++++++++
.../c2/wasm-compare/schema-inspect.stderr.txt      |   0
.../c2/wasm-compare/schema-inspect.stdout.txt      |  22 ++++++++++
```

## Supplementary changed-interface coverage (L1 follow-up)

- **Observed:** Added two small WAT sources and compiled them with WABT 1.0.42. The build receipt preserves argv, exit codes, and WAT/WASM SHA-256 values (`.ufo/waves/round-20/evidence/c2/wasm-compare/synth/v1.wat:1-7`, `.ufo/waves/round-20/evidence/c2/wasm-compare/synth/v2.wat:1-9`, `.ufo/waves/round-20/evidence/c2/wasm-compare/synth/build-receipt.json:2-17`, `.ufo/waves/round-20/evidence/c2/wasm-compare/synth/SHA256SUMS:1-4`). V1 exports `old_api` and `stable`, importing `env.get(i32)->i32`; v2 exports `new_api` and `stable`, importing `env.get(i32,i64)->i64`.
- **Observed:** Both synthetic modules inspected successfully. Their inspect Evidence IDs and subject hashes are `.ufo/waves/round-20/evidence/c2/wasm-compare/synth/evidence-index.jsonl:1-2`. The compare calls returned `complete-within-inputs`: imports changed one `env.get` signature; exports added `new_api`, removed `old_api`, and retained `stable`; `both` reports added 1, removed 1, changed 1, unchanged 1, unknown 0 (`.ufo/waves/round-20/evidence/c2/wasm-compare/synth/evidence-index.jsonl:5-7`; raw outputs `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-synth-imports.stdout.txt:1`, `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-synth-exports.stdout.txt:1`, `.ufo/waves/round-20/evidence/c2/wasm-compare/compare-synth-both.stdout.txt:1`).
- **Observed:** Also compared the real `qcms_bg.wasm` and `openjpeg.wasm` pair for `both`. Inspect and compare Evidence IDs, distinct subject SHA-256 values, and summary are `.ufo/waves/round-20/evidence/c2/wasm-compare/synth/evidence-index.jsonl:3-4,8`; the comparison reports 23 added and 28 removed, with no changed, unchanged, or unknown entries (`.ufo/waves/round-20/evidence/c2/wasm-compare/compare-real-both.stdout.txt:1`). Its receipt retains both carrier paths and hashes plus invocation details (`.ufo/waves/round-20/evidence/c2/wasm-compare/compare-real-both.receipt.json:2-44`).
- **Limitation:** The synthetic pair demonstrates changed-signature and added/removed export reporting. The qcms/openjpeg pair is a comparison of distinct modules, not a version-compatibility claim; neither comparison establishes runtime/ABI compatibility.
- Supplementary patch: `.ufo/waves/round-20/w1/patches/WasmCompareLeg-2b.patch` contains only the new synthetic and comparison evidence files.
