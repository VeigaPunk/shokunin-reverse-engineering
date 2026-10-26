CONFIRMED — R40-C2's held-out set regenerates byte-identically from the freeze seed; no falsification of the C2 landing and no defect found (three calibration notes, none claim-touching).

I attacked the reproducibility legs of P40-C2: "the seed is the freeze commit hash", "every carrier regenerates byte-identically", the manifest's (class, label, action) assignment, plus the adjacent clock/order, vocabulary and provenance legs. I did not attack, and state nothing about, the REA envelope *content* beyond the digest/pair linkage, the table-row mapping itself (I reproduced the counter, not re-scored it by hand), or any C1 data.

## Method (exact commands, scratch = `/fast/scratch/hyaku/kaidoku-r40/R40W2C2RegenA`)

```
cd $S && python3 -I -B <LANE>/tools/round-40/heldout-gen-v2.py \
    --seed 7fce308631a8b457d6b7c5a4b39a923c4e9a49de --out $S/regen        # exit 0, 26 carriers
```
No `--run`, no `--actions-file`, no `--gen` override. Contrast runs: seeds `fa6a8a3f…` (base), `4d62ee5a…` (dispatch tip), `0fce3086…` (first hex char changed), `7fce3086…9df` (last hex char changed); `--actions-set tabledraft`; `LC_ALL=C TZ=UTC` and `LANG/LC_ALL=en_US.UTF-8 TZ=Asia/Tokyo`; and a regeneration from tools extracted with read-only `git archive 7fce3086 tools/round-39 tools/round-40` (no lane worktree involved).

Comparison was: manifest bytes, per-id `sha256`, per-id `(class,label,action)`, whole manifest entry equality, recursive `diff -r` against the committed evidence dir, on-disk hashing of all 26 committed carriers, envelope subject digests, `run.json` expected pairs, and a reproduction of the counter at the measured revision.

## Results

| check | result |
|---|---|
| regenerated `manifest.json` sha256 | `232a3bf65d5adca1f72461f804b75a3f05d8f59e148d3310ad675cf3a49ff55f` = committed manifest, byte-identical |
| carrier `sha256`, freeze seed | 26/26 equal to committed manifest pins |
| `(class, label, action)` per id | 26/26 equal; whole manifest entry equality 26/26; `label_actions`, `action_vocabulary`, `classes` equal |
| `diff -r regen <committed heldout>` | 78 `Only in` lines = 26 × {`envelope.json`, `rea-full.json`, `run.json`}; **0** content-differing lines — every committed `carrier.sqsh` and `tree.json` is reproduced byte-for-byte |
| committed carrier bytes on disk vs manifest pin | 26/26 hash to their pins (nothing hand-edited after generation) |
| regeneration from freeze-archive tools only (`git archive 7fce3086`) | same manifest sha256 `232a3bf6…` — no dependence on the checked-out worktree |
| locale/timezone variation (`LC_ALL=C TZ=UTC`; `en_US.UTF-8`/`Asia/Tokyo`) | same manifest sha256 `232a3bf6…` |
| manifest `seed` | `7fce308631a8b457d6b7c5a4b39a923c4e9a49de` = freeze commit |
| declared `generator.sha256` / `writer.sha256` | `644d8f6e…` / `f535e60e…` match the files at freeze, measured and HEAD |
| other seeds | base `fa6a8a3f`: 26/26 carriers differ; tip `4d62ee5a`: 26/26 differ; first-char variant `0fce…`: 26/26 differ; last-char variant `…9df`: 24/26 differ (see N1) |
| `--actions-set tabledraft` | 0/26 carrier sha256 change while 24/26 action tokens change — carrier bytes are independent of the (label, action) binding, so no REA feedback path exists |
| generator `--selftest` (freeze seed) | 6/6 PASS, exit 0 |
| envelopes: `subject.digest.sha256` vs carrier pin | 26/26 equal; 26 distinct `evidence_id`s; operations `extract_firmware` (24) + `inspect_firmware_regions` (2); providers `unblob` (24) + `binwalk` (2) |
| `run.json` `expected_label`/`expected_action` vs manifest pair, `subject_sha256`, `digest_matches_carrier`, `ok`, `exit_code` | 26/26 consistent (no deviations) |
| git ordering | single commit `2d1ac5bc` adds manifest + all envelopes + carriers; `freeze < 2d1ac5bc < measured 42c10a58 < HEAD` |
| frozen-path integrity, `FREEZE..42c10a58` | `git diff --stat` over `tools/round-40/{sqfs-triage-v2.py,heldout-gen-v2.py,c2-counter.py}`, `tools/round-39/gen-squashfs.py`, `plans/round-40-claims.md`, `SKILL.md` → **empty**; `cmp` of `SKILL.md` at freeze vs measured → identical |
| evidence stability | `git diff --stat 2d1ac5bc..42c10a58` and `42c10a58..HEAD` over `corpus/evidence/round-40/c2` → empty |
| frozen `<!-- sqfs-triage-actions: -->` line vs manifest | 11 tokens, set-equal to `action_vocabulary` (manifest order is sorted; the SKILL line is not) |
| counter reproduced at measured rev (`--rev 42c10a58… --freeze 7fce3086…`) | exit 0, `matched 26/26`, `met_target true`, `bindings_false []`; 24 compared receipt fields identical to `.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json` |

The byte-identical reproduction also closes the strongest fabrication reading of this leg: the committed carriers were produced by a `--run` build, and a `--run`-free build of the same seed yields the identical bytes and manifest, so the carriers cannot encode any post-REA adjustment.

## Calibration notes (not claim violations)

- **N1 — `clean-empty` carriers are seed-tail invariant.** Changing only the last hex character (`…9de`→`…9df`) leaves H05/H06 (`clean-empty`) byte-identical; their `tree.json` differs only in the `"seed"` field. Cause: the RNG is seeded from `seed[:16]` and an empty tree has no file material, which is the only other seed carrier. The generator's own selftest asserts "different seed: every carrier differs" using `seed[::-1]` — that reverses the first 16 chars, so the check passes without exercising tail sensitivity [INFERENCE from reading `build_carrier`/`empty_tree`/`run_selftest`]. P40-C2 only requires regeneration from the freeze seed, so nothing is falsified; but "seeded" here means 64 bits for tree shape, not the full 256-bit hash.
- **N2 — the C2 receipt's `base_commit` is not the claims' base.** `c2-at-42c10a58.json` records `2b0b6a29…` with `"base_source": "derived"`; `derive_base()` returns the newest commit at/below the freeze whose `SKILL.md` has the v1 marker and no v2 marker. That is the v1-table comparison base, not `fa6a8a3f` (the round base named in the claims). P40-C2 binds no base, so the verdict is unaffected; the field name invites misreading next to C1 receipts that do bind `fa6a8a3f`.
- **N3 — pre-existing uncommitted `SKILL.md`.** The worktree carries `M SKILL.md`, +19 lines appended at EOF (a "Round-40 instrument registry" section, after line 1384). It does not touch rule block 19 or either v2 marker, and all my C2 checks read committed revisions (`git show` / `git diff`), with `SKILL.md` byte-identical at freeze and measured. Not mine, left untouched.
- **N4 — lane HEAD is ahead of the dispatch tip.** HEAD = `0b15c8b2` ("wave-2 spec, generator and validated dispatch (38 seats)"); `4d62ee5a` is an ancestor. The frozen C2 tools and evidence are unchanged across `42c10a58..HEAD`, so the measured-revision score remains readable at the current tip.

## Retained evidence

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-40/w2/artifacts/R40W2C2RegenA/`

- `regen-manifest-at-freeze-seed.json` — the regenerated manifest (identical to the committed one).
- `manifest-hashes.txt` — `sha256sum` of the committed manifest and of all nine regeneration variants (freeze, base, tip, near, first-char, `LC_ALL=C`/`TZ=UTC`, UTF-8/`Asia/Tokyo`, `tabledraft` actions, freeze-archive tools).
- `compare.txt` — per-id carrier sha256 / triple / whole-entry comparison, on-disk hashing, replicate distinctness, claims-vs-manifest pair deviations (none).
- `diff-summary.txt` — recursive diff summary: 78 `Only in` lines, 0 content differences.
- `envelopes.txt` — envelope digest, pair, operation and provider checks.
- `repro-depth.txt` — seed-variant and vocabulary-independence counts.
- `near-seed-treediff.txt` — the one-line `seed` difference behind N1.
- `token-check.txt` — SKILL action line vs manifest vocabulary.
- `selftest.txt` — generator `--selftest`, 6/6 PASS.
- `c2-counter-repro.json` — my counter receipt at `42c10a58`.

## Limits

- No REA run was made by this seat: the envelopes are checked for digest, pair, operation, provider and `run.json` consistency, not re-extracted; re-extraction is the counter's and C1's ground.
- No vendor bytes were fetched, copied or opened; nothing from `/home/vgpnk/Projects/shokuknow` was used.
- No LSP symbol queries were needed (plain file/git reads and one Python driver); nothing to report as unavailable.

## Bounds / tooling

Wrote only this report and the artifacts directory above; no VCS mutation (read-only `git show/log/diff/rev-parse/merge-base/cat-file/archive`); no writes to `corpus/`, `tools/`, `plans/`, `SKILL.md`, the fleet repo or sibling lanes. No tool was installed. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2C2RegenA` removed.
