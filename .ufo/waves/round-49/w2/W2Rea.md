# W2Rea — REA 6.5.0 domain check at `29883d4e`

**Verdict: the four committed envelopes support the REA behaviour the entry states (verb `extract-firmware` / `extract_firmware`, no refusal, `coverage` `complete`, exact handlers, census files). They do not support three field names the entry quotes, and the landing score path the entry names is not in the commit. No counter defect. Counters were not patched.**

Rev `29883d4ec35a31a8393c4ffb220888c44c0bb022`. Blobs via `GIT_NO_REPLACE_OBJECTS=1 git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show <rev>:<path>`. No extraction. Scratch removed after copy.

## Findings

| id | attack | result | where |
|---|---|---|---|
| F1 | entry cites the landing score | **unsupported path.** `c1-final.json` is absent. The only score blob is `.ufo/waves/round-49/l1/scores/c1-at-data-4aabb0b4.json`. The counter sha256 in the same sentence matches `tools/round-49/c1-counter.py` at this rev | entry:3 |
| F2 | `handler_detail` value | **value mismatch.** Score `bindings.handler_detail` is `["squashfs_v1","squashfs_v1","squashfs_v2","squashfs_v2"]`. Envelopes store `chunks[0].handler` `squashfs_v1` / `squashfs_v2`. The entry's exact-string rule is the envelope value; the parenthetical `v1, v1, v2, v2` is not | entry:29, entry:87 |
| F3 | `gap_kinds []` as a receipt/score field | **name absent.** No `gap_kinds` key in any `after.json` or in `c1-at-data-4aabb0b4.json`. Emptiness is real under `normalized_result.extraction_gaps` `[]` and `unpublished_entries` `[]` (all four). Score says `gaps_ok true` and `gaps_note` `0 gaps (0 structural), 0 removals, 0 silent, on 0 non-regular entries` | entry:87 |
| F4 | `per_carrier_failing []`, `provenance_ok` | **names absent as keys.** Score has top-level `failing []` and per-carrier `run_provenance_ok true` (all four). No key `per_carrier_failing`. No key `provenance_ok`. Envelope `parameters.output_directory` does start with `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/` | entry:96 |
| F5 | coverage `complete` | **supported.** All four: `normalized_result.coverage == "complete"`, `published_bytes` 20/20/28/28, file count 3/3/4/4, each `sha256` and `reported_sha256` equal the entry census, `analysis_depth` 1, `extraction_failed` false. Top-level `relationship_coverage` is `null` on all four (a second field; the word `complete` is the normalized field) | entry:87, entry:91–94 |
| F6 | typed gaps and `missing-extractor-dependency` | **not observed, and the entry does not claim they were returned.** None of the four envelopes contain `missing-extractor-dependency`, `unpublished-entry`, `depth-limited`, `MaliciousSymlinkRemoved`, or `sasquatch`. `extraction_gaps`, `unpublished_entries`, `depth_limited_paths`, `diagnostics`, `extraction_continuations` are `[]`. Line 96 names those kinds as the frozen gap rule (counter docstring, `c1-counter.py:17–18` and `:353–372`), then says they have nothing to bind. Empty arrays support "none emitted". They do not witness the type strings | entry:96 |
| F7 | `--max-depth` default and `--full-output` | **as the runner used them.** `c1-run.py:348–351` builds `extract-firmware --format json --full-output <fixture> <outdir>` and does not pass `--max-depth`. All four `run.json` `argv` match that shape (pin `rea-agents@6.5.0`). Help: `--max-depth` default **3**, "reaching it yields partial analysis"; `--full-output` is "Show full output envelope". Each envelope: `parameters.max_depth` 3, `max_output_bytes` 268435456, `max_output_files` 10000 (the other help defaults), and `raw_result.execution.args` includes `--depth` `3`. `stdout.log` is `{"ok":true,"data":…,"meta":{"command":"extract-firmware",…}}` and `data` equals `after.json`, which includes `raw_result`. Depth limit not reached (`analysis_depth` 1, `depth_limited_paths` `[]`). The entry never states the flag | `c1-run.py:348–351`; four `run.json`; help |
| F8 | sasquatch argv the entry prints | **not in `after.json`; present in `unblob.log`.** Entry:21–25 cites S112, not the envelope. Logs: LE `sasquatch -le -no-exit-code -f -d <outdir> <firmware.bin>`; BE `sasquatch -be` with the same tail. That matches the entry's shape. Envelope `execution.command` is the `unblob-tee.sh` wrapper, not sasquatch | entry:21–27; `unblob.log` |

## What the entry relies on

REA verb actually exercised: CLI `extract-firmware`, envelope `operation` `extract_firmware`, stdout `ok` true, `run.json` `exit_code` 0, unblob `execution.exit_code` 0. No REA refusal on these four bytes. Help's only depth refusal ("reaching it yields partial analysis") did not fire.

Handlers: `v1le`/`v1be` `squashfs_v1`; `v2le`/`v2be` `squashfs_v2`. One chunk each, `encrypted` false, range the whole 4096-byte carrier.

`missing-extractor-dependency`: the string is not in the entry and not in the four envelopes. The entry does not rely on that refusal. (The counter's selftest names the kind at `c1-counter.py:3156`; that is not an observed receipt.)

## Receipts

| utc | exit | sha256 | command |
|---|---|---|---|
| 2026-10-28T22:42:52Z–22:42:53Z | 0 | stdout `7dd965ab9bc1193c1cc6a813e4f798300adaae9db4b9f9b57ee8d5f57df36acc`; stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | `npx -y rea-agents@6.5.0 extract-firmware --help` |
| 2026-10-28T22:46:45Z | 128 | stdout `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; stderr `5cea8331fbe9dbaf12b34f6309fa97c09acdb5b24adcd7f314842f85bc2a9934` | `GIT_NO_REPLACE_OBJECTS=1 git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e 29883d4ec35a31a8393c4ffb220888c44c0bb022:.ufo/waves/round-49/l1/scores/c1-final.json` |

Blob sha256 (`git show <rev>:<path>`, exit 0):

| sha256 | path |
|---|---|
| `e2633e0e151ccdff972c1d7032d06b895ea481bfb33de964b6368b96e62fc0d3` | `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` |
| `4a1527fb3d07120ac023f1cd1dd20d7eceac671d363ea6ed60cddf28a9e262f6` | `tools/round-49/c1-run.py` |
| `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f` | `tools/round-49/c1-counter.py` (equals the hash entry:3 quotes) |
| `8a2e838642c5b3acf9e6b75769170f0ad329465ee870228bb88e9b10919533c3` | `corpus/evidence/round-49/c1/v1le/after.json` |
| `7b9da8249e14459f9723b3311bf7e97ec6f1b29933df2ea81cf4d00f49b5edb4` | `corpus/evidence/round-49/c1/v1be/after.json` |
| `b925ff90fd457bef6538fb74579aed8b3789f8b98f5fc025f2a2137e31690db6` | `corpus/evidence/round-49/c1/v2le/after.json` |
| `f7afd9090f46dbdea71b555c90b3216d1214164755514ff702350ce2e507ef52` | `corpus/evidence/round-49/c1/v2be/after.json` |
| `1a38349fc3095a1c75d0ff46f790eb4c856085d0649fe9883563d84dd94006ca` | `…/v1le/run.json` |
| `947ed47ccb777cb3642104c4930ee73a836f71ed42381dbb38b5921e3ac2d4dd` | `…/v1be/run.json` |
| `2d82d0340808c2e1e387031bc342d730ec711ddfcd78634ef82009b0f565cd4a` | `…/v2le/run.json` |
| `608a5abff6e70250a7bdcdae812137e246ff3dc41fdf333aa433a48d31d44c8d` | `…/v2be/run.json` |
| `da115d7624ceb09971c3e0f16458c138a1bed6b7dd306fb24097010ec0d76b6c` | `…/v1le/stdout.log` |
| `4d42e10d0a832be99f1273ff1f7a635b8062af64f718433b9252e94116306767` | `…/v1be/stdout.log` |
| `ca08507fa5416925116f014f7e4e18e281415ce18780ca649052f281364b279b` | `…/v2le/stdout.log` |
| `536bcd1ab9364c431deed0edefc0b24b729470cce84199e73d18efca3365d856` | `…/v2be/stdout.log` |
| `86c48e2b7efe51781d2cc370642afa59bbef336d61955c7219874d2552fada5f` | `…/v1le/unblob.log` |
| `45f2e0b462bcb3e17636f6ecf48fbb716dd49a592c462db11428d59bab55e66d` | `…/v1be/unblob.log` |
| `7f1cac1c231f210dcc058832a97f630fc6b4026a068ebe86f82f9f266df23b63` | `…/v2le/unblob.log` |
| `53086e036ba2acc0b593064cbf23ca20806cad51a8f9997effeba4dd7e23234a` | `…/v2be/unblob.log` |

Help text and the per-carrier extract are under `.ufo/waves/round-49/w2/W2Rea/` (`help-extract-firmware.txt`, `help-receipt.txt`, `envelope-facts.json` sha256 `a66b9b2ffb0d422ddb71add1abf51f98ae0bb5a14adcb4737122ea84438a9f77`, `c1-final-receipt.txt`).

Not run: a second `extract-firmware` invocation (with or without `--full-output`), and both counters. This seat did not re-score C1 or C2.
