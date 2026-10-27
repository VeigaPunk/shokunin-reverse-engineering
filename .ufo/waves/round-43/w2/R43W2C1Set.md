# R43W2C1Set — independent C1 heldout inventory

## Result

**No falsification found in the assigned heldout inventory/tuple-check surface** at measured lane revision `5856614ac4bf7f2363bbcd1956644474a82108e5` (current tip). The score receipt itself was measured at `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`; `5856614ac4bf7f2363bbcd1956644474a82108e5` has parent `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`. The committed heldout subtree has no diff between those revisions, and the heldout path is clean in the worktree.

Independent enumeration of the committed tree found:

- **78 carriers** / 78 carrier directories plus `manifest.json` (79 root entries); IDs unique, and manifest ID set exactly equals directory set.
- **27 named classes × 2 = 54** carriers, plus **24 `combo` carriers** (C01–C24), total 78. Every named class count is exactly two.
- Every carrier has exactly the five regular files `carrier.sqsh`, `envelope.json`, `rea-full.json`, `run.json`, `tree.json`: **390/390 expected files**, no missing or extra files.
- Carrier SHA-256 in each manifest record equals the actual carrier bytes for **78/78**; envelope subject SHA-256 equals those bytes for **78/78**. No digest mismatches.
- `generator.tuple_check.fields` is the six fields `handler_set`, `gap_kinds`, `gap_dependencies`, `be_argv`, `symlink_removed`, `published`. Tuple-check coverage is **78/78**, `all_equal=true`, measured=true, equal verdicts 78, non-true verdicts 0, no missing/extra IDs. Re-derived these six fields from all 78 committed envelope JSONs with the frozen counter's `observed_features` extraction; observed-vs-manifest and observed-vs-tuple-check mismatches: **0**.
- OOD IDs: **H25, H26**, both `out-of-domain`; their six-field tuple is the empty/default tuple (no handlers/gaps/dependencies, `be_argv=n/a`, `symlink_removed=false`, `published=zero`). They are included in the raw 78 checks, but the disclosed effective n for the refusal/tuple comparison is **76**, because those two OOD checks are vacuous. This is a limitation, not a mismatch.
- Manifest seed equals the frozen commit `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`.

## Receipt context and attack boundary

Read the frozen plan first, then the current tip and committed score/control receipts. C1 score receipt `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` records `matched=78`, `n=78`, `exit_code=0`, `bindings_ok=true`; `bindings_false`, `bindings_declared_unset`, and `bindings_undeclared` are empty. Its `observed_features_match_declared` and `generator_tuple_check_all_equal` bindings are true. C1 controls summary says `ok=true`, `kill_rule_fires=false`, `errors=[]`.

For required C2 receipt context only (not a C2 attack): both `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json` (REV `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e`) and `c2-at-77d196c6.json` (REV `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`) record `exit_code=1`, `checks_ok=false`, with sole false check `sources_numstat_three_additions`. Read C2 control summaries: CTL-C2-0 exit 1; CTL-C2-1 exit 1 (missing S001/SKILL.md); CTL-C2-2 baseline gate/linter 0/0 and symlink gate/linter 0/1; CTL-C2-3 gate exit 0 with two dirty paths, rejected by clean-clone predicate. These are receipt observations, not conclusions from this C1 seat.

No REA, unblob, sasquatch, or extractor was run. The inventory script operation only parsed committed JSON and SHA-256-hashed the committed five-file trees; it loaded the frozen counter's extraction function for envelope feature parsing. No heldout generation, fixture extraction, scratch creation, lane production edits, commits, or VCS mutation was performed. The broad worktree status showed other unowned wave files modified/untracked; they were left untouched. Heldout-specific `git status` and `git diff HEAD` were clean.

## Commands and outcomes

Read-only Git commands and observed outputs:

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` → `5856614ac4bf7f2363bbcd1956644474a82108e5` (exit 0).
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show -s --format='%H%n%P%n%s' 5856614ac4bf7f2363bbcd1956644474a82108e5` → current tip; parent `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`; subject `round-43: land C1 score, scored entry, and evidence; stage wave-2 attacks` (exit 0).
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --name-status 77d196c66f4fea00d7d543728b190ebdfaf6d0f0..5856614ac4bf7f2363bbcd1956644474a82108e5 -- corpus/evidence/round-43/c1/heldout/` → empty output (exit 0); corresponding `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 77d196c66f4fea00d7d543728b190ebdfaf6d0f0..5856614ac4bf7f2363bbcd1956644474a82108e5 -- corpus/evidence/round-43/c1/heldout/` → exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain -- corpus/evidence/round-43/c1/heldout/` → empty output (exit 0); `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet HEAD -- corpus/evidence/round-43/c1/heldout/` → exit 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-43/w2/artifacts/R43W2C1Set/check_inventory.py` (cwd lane root) → exit 0; output is the machine-readable count/check summary in the tool transcript and its per-file hashes are recorded in `inventory.json`. It reports 78 records/directories, 390 expected regular files, exact ID-set match, 27 named classes, tuple-check 78/78 true, and zero carrier/subject/observed-tuple mismatches.

The checker parses the manifest, enumerates all five files per carrier, hashes them, checks manifest IDs/class counts/carrier digests, checks each envelope subject digest, and loads `tools/round-43/c1-counter.py` to call `envelope_data` / `observed_features` on each committed envelope. No external extraction command was invoked. No REA, unblob, sasquatch, or extractor was run. The complete per-file paths, sizes, SHA-256 values, receipt/input hashes, and machine-readable check counts are in the artifact below.

## Read-input hashes

SHA-256 (full path and all 390 heldout file hashes are also in `inventory.json`):

- `plans/round-43-claims.md` — `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`
- `corpus/evidence/round-43/c1/heldout/manifest.json` — `980eafa59ca3890bf45945a02a6e608da511435d972d1ec978a38fd068ef2555`
- `tools/round-43/c1-counter.py` — `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`
- `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` — `13a495dbb6862d6cfbdd1f41e4a09460740f86bf93e8bb08e313b06d92b8a55c`
- `.ufo/waves/round-43/controls/c1/summary.json` — `143d4c38412c8d4af785243ffdabc5e8735d0237818643ce1bb151e4db624e5d`
- `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json` — `126b529eb5c3b0d61eaceb5f2e026eb3de9b0a9c2256239eabd86a23eaad9f4e`
- `.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json` — `42f592aec7d6ffe082a257dba1142b1790857c53ddaab17b1bae1c8db09b76e6`
- `.ufo/waves/round-43/controls/c2/ctl-c2-0-summary.txt` — `6786e8367be3abf32c342567a134d9602285557b0e2f8f11be5dc927081c85f7`
- `.ufo/waves/round-43/controls/c2/ctl-c2-1-summary.txt` — `018f6edf0a73272004be58cd570e20419abcd71277f2619fd379302b396a2dc4`
- `.ufo/waves/round-43/controls/c2/ctl-c2-2-summary.txt` — `4d1ae7eb4b902a2a6fa3e26c5e61f4dc9be521075ea23cdefa256109f387a1eb`
- `.ufo/waves/round-43/controls/c2/ctl-c2-3-summary.txt` — `09bcb4692f4aa7bc98b890c7be4f3b5e7aa7240a134d4ee89c37dde167f48101`

C1 control receipt JSON hashes (CTL-C1-0 through CTL-C1-4, respectively): `36d6b03de94164b59828fd81c820184891a5394e4231df052987cf826e57ffab`, `bc7bf8356f49fdf64d9d010ab53e963278ebc5a57bbe0f8477fbcdcbf897ef95`, `84a6d0dd8333028fcb0da29b8e33fbe814309257a5a0f264789a29e62a78706c`, `4cdeddf5d080b52cffee6dc779e558bcf33505e069c4ec5a9d994cf3c15e0190`, `ed41a5e1da2b20cfc006d1c4dd8dc855a954646807b1874171880c5e5327b919`.

Artifact `artifacts/R43W2C1Set/inventory.json` SHA-256: `e1809f77eefa101d34229fb4af2894da9ee6127849ebfe5b29158967a076e8b1`.

Reproducible checker `artifacts/R43W2C1Set/check_inventory.py` SHA-256: `931b7f93720ddd71d6be01828f1178eabdf9dfaf51bb80713128fb0617ecebd0`.

## Limitations

This is an inventory/data-byte falsification check for the assigned C1 attack surface, not a rerun of the frozen scorer, generator, or REA. The observed tuple was independently recomputed from envelope bytes using the same frozen `observed_features` implementation the counter uses; therefore it validates the committed self-report against its envelope inputs, but does not provide a second, independently implemented semantic parser. Effective-n 76 reflects the plan's disclosed OOD vacuity, not a reclassification of those IDs.

Report: .ufo/waves/round-43/w2/R43W2C1Set.md
