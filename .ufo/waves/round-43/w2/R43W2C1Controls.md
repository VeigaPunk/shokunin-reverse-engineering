# R43W2C1Controls — C1 controls review

## Verdict

No actionable falsification of the frozen C1 controls found. CTL-C1-0/1/3/4 are counterfactual kill arms and none reached the full target. The 78/78 reference witness and CTL-C1-2 green tuple-check are correctly classified as non-kill evidence, consistent with the frozen plan. CTL-C1-1’s `manifest_after_freeze` required-false clause is correctly placement-specific: false for its at-freeze arm, true for its after-freeze arm; the latter still fires `seed_matches_freeze` false. No control is misclassified as a kill arm.

## Revisions, files, hashes

Measured C1 claim score revision: `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`; lane tip reviewed: `5856614ac4bf7f2363bbcd1956644474a82108e5`; freeze: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`.

Frozen plan read first: `plans/round-43-claims.md` sha256 `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`.

Reviewed committed evidence hashes:
- `.ufo/waves/round-43/controls/c1/summary.json` — `143d4c38412c8d4af785243ffdabc5e8735d0237818643ce1bb151e4db624e5d`
- `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-0.json` — `36d6b03de94164b59828fd81c820184891a5394e4231df052987cf826e57ffab`
- `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-1.json` — `bc7bf8356f49fdf64d9d010ab53e963278ebc5a57bbe0f8477fbcdcbf897ef95`
- `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-2.json` — `84a6d0dd8333028fcb0da29b8e33fbe814309257a5a0f264789a29e62a78706c`
- `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-3.json` — `4cdeddf5d080b52cffee6dc779e558bcf33505e069c4ec5a9d994cf3c15e0190`
- `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-4.json` — `ed41a5e1da2b20cfc006d1c4dd8dc855a954646807b1874171880c5e5327b919`
- `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` — `13a495dbb6862d6cfbdd1f41e4a09460740f86bf93e8bb08e313b06d92b8a55c`
- `tools/round-43/c1-counter.py` — `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`
- `tools/round-43/heldout-gen-v4r43.py` — `6ab0114d555a09a93ab61459c7adb76a45957a35dc69671b64e7733225aca97a`
- `corpus/evidence/round-42/c2/heldout/manifest.json` — `656c22d52ef038f28d77391324f23223d4b893ad2b4775f4a147d50734fde557`
- `corpus/evidence/round-43/c1/heldout/manifest.json` — `980eafa59ca3890bf45945a02a6e608da511435d972d1ec978a38fd068ef2555`
- `.ufo/waves/round-42/controls/c2/dev-scores-prefreeze.json` — `19a61b6cbc6bc3c051a32e06dd5fe3f918564f78ab4ba5e26a0b9beb4d66ffa4`

`git show FREEZE:tools/round-43/c1-counter.py | sha256sum` and worktree `sha256sum tools/round-43/c1-counter.py` both yielded the receipt hash above. Same freeze/worktree equality for `heldout-gen-v4r43.py`. `git merge-base --is-ancestor` succeeded for FREEZE→score revision and FREEZE→tip. A targeted `git diff --name-status FREEZE..TIP` check over the frozen C1 paths found no changes. The whole diff had other non-C1/C2 paths; they are outside this seat’s judgment. Worktree was not clean before this seat (pre-existing wave/fleet files); no production changes were made.

## Findings and reproductions

Commands below were read-only against the lane; any output files/clones were under `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C1Controls/`.

- **Score / hashes / freeze.** The committed score receipt reports exit 0, 78/78, 45 bindings with none false, and both counter hashes equal the frozen counter digest. The round-43 manifest seed is exactly FREEZE; manifest has 78 carrier records. The tool hashes and ancestry checks above agree. No counter path/hash/freeze mismatch observed.
- **CTL-C1-0.** Re-ran `python3 -I -B tools/round-43/c1-counter.py --root <lane> --rev f3f8db389416d094b1ddeb1215ddcf914bfc0d1c --freeze f3f8db389416d094b1ddeb1215ddcf914bfc0d1c --json-out <scratch>/ctl-c1-0-repro.json`. Exit 2; JSON says `no_manifest_at_rev`, `bindings: {}`, and contains `counter_sha256_at_freeze`. Matches receipt; no binding was inferred from the empty map.
- **CTL-C1-1 stale manifest.** Reproduced from a verified scratch clone toplevel `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C1Controls/ctl-c1-1-clone`; planted round-42 manifest sha matches `656c22d5…`, seed `d1681696…`. At sandbox freeze/rev `7db66b4dc5428266d6f9146102927ff652c1dd67`, counter exit 1 and both `seed_matches_freeze` and `manifest_after_freeze` false. Against real FREEZE with same rev, exit 1; `seed_matches_freeze` false and `manifest_after_freeze` true. Both expected bindings fire. These are failed preflight/score arms, not target matches.
- **CTL-C1-2 tuple refusal.** Re-ran `python3 -I -B tools/round-43/heldout-gen-v4r43.py --tuple-check corpus/evidence/round-42/c2/heldout`. Exit 3 with `declared_tuple_unobserved: 1 of 78`; C02 `gap_kinds` declares `extractor-failure, unpublished-entry`, while envelope observation also has `depth-limited`. Manifest hash before and after remained `656c22d5…`. In scratch, corrected only the C02 tuple to the observed three members and ran the same interface: exit 0, “every observed tuple equals its declared tuple.” This green arm tests refusal correctness; it is explicitly not a table-score kill arm.
- **CTL-C1-3 shortcuts / witness.** All ten copied documents’ hashes matched both their corresponding frozen round-42 source documents and summary-recorded sha256 values. Receipt records reproduce the round-42 matched counts and missed sets; all eight counterfactual controls miss the 78 target: base 0, catch-all 8, actions-rotated 2, exact-gap-sets 52, no-legacy-row 75, v4-handler-glob 2, no-container-residue 67, lookup 66, lookup-fallback 66. `CTL-C1-3d`’s three misses are C01/H47/H48; the shortcut result is 75/78, not a kill. The receipt explicitly marks `CTL-C1-REF-v4-precedence` role `witness`, 78/78, and separately lists it as the only `witness_at_target`; the frozen plan excludes the reference witness from kill arms. Summary and receipt both report no counterfactual at target and `kill_rule_fires: false`.
- **CTL-C1-4 envelope immutability.** Receipt compares baseline and hand-edit arms: baseline observed tuple binding true; H01 `published` changed `nonzero`→`zero`, hand-edit binding false; both report 78 envelopes and `envelopes_untouched: true`. Independent scratch reproduction used the committed 78-carrier set. The first attempt committed an edit after its sandbox freeze and correctly stopped with `frozen_path_changed` (not a tuple verdict); I then evaluated the edited arm with its edited tree as sandbox freeze, which exited 1 with `observed_features_match_declared: false`. `git diff --name-only` between the baseline planted tree and the edited tree listed only `corpus/evidence/round-43/c1/heldout/manifest.json`; no envelope path changed. Baseline counter binding was true. Thus the receipt’s envelope-unchanged assertion is consistent with the committed tree comparison and the counter scores observed envelope bytes, not the manifest’s tuple-check claim.

## Verification gaps / limitations

- No `lsp` device/server was exposed in this seat’s tool inventory; semantic references/definition/diagnostics were not available. This review was limited to assigned control receipts, their committed sources/data, and direct read-only reproductions.
- The green tuple-check and CTL-C1-1/4 scratch clones were independently reproduced; CTL-C1-4’s exact original sandbox commit IDs are not independently reconstructible from the committed lane because those clone commits are not landed. Reproductions test the same bindings and byte-diff property, not those scratch commit identities.
- No third-party firmware was opened or extracted; no installation was performed.
- Commands included: `git rev-parse`, `git merge-base --is-ancestor`, targeted `git diff --name-status`, `git show … | sha256sum`, `sha256sum`, receipt/manifest JSON reads, CTL-C1-0 counter invocation, CTL-C1-2 `--tuple-check` red and green, CTL-C1-1 counter invocations in both placements, and CTL-C1-4 scratch-tree counter/diff checks. Reproduced exits: CTL-C1-0=2; CTL-C1-2 red=3 / green=0; CTL-C1-1=1 in both placements; CTL-C1-4 edited arm=1 (the deliberate invalid post-freeze setup first stopped at exit 2, `frozen_path_changed`).

Artifact directory: `.ufo/waves/round-43/w2/artifacts/R43W2C1Controls/` (no separate artifact files required; all reproduction outputs were scratch-only and removed before yield).
