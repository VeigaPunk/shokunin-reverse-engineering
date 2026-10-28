# W2C1Receipts — wave 2, post-landing: committed C1 evidence tree at `29883d4ec35a31a8393c4ffb220888c44c0bb022`

## Verdict

Holds for the scored set; the counter binds less than the evidence tree that sits beside it.

- The committed bytes agree with each other at REV: `after.json` = `stdout.log` `.data` = `extract-tree.tsv` = committed `firmware.bin_extract/*` = the independent `unsquashfs` 4.7.5 oracle (re-derived here) = the round-44 `__output__` trees. Tool pins match the disk. No symlink or non-regular mode in the tree.
- The frozen counter reproduces at REV: exit 0, `carriers_matched 4`, `failing []`, `bindings_false []`, `frozen_path_changed []`.
- **The counter reads only `corpus/evidence/round-49/c1/<id>/after.json`.** Unread: the committed `firmware.bin_extract/**` tree and eight sibling receipts (`extract-tree.tsv`, `run.json`, `provenance.json`, `extract-env.json`, `stdout.log`, `envelope.json`, `unblob.log`, and `manifest.json`). All 11 tamper probes on those files (F1, F2) exit 0 with `carriers_matched 4`. Undisclosed in the plan's limits list.
- **`depth_limited_paths` and `extraction_continuations` are read by no clause.** Two probes exit 1 only through `evidence_id_ok`; `projection_ok` stays true (F3). Current values are `[]` on all four carriers, so no present claim is false.
- Scope not run: re-minted-id forgery of `after.json` (disclosed limit 1, not run by me); REA scratch tree is gone (`probe-R49C1Run/` empty), so the original `rea-out` cannot be compared.

Counter defects are reported, not patched. The frozen counter bytes equal the FREEZE blob (`ac83715b…`), so nothing here is a counter-edit.

## Receipts

Directory `.ufo/waves/round-49/w2/W2C1Receipts/` (SHA256SUMS inside). Scratch `/fast/scratch/hyaku/kaidoku-r49/W2C1Receipts/` removed after copy. All counter runs used `GIT_NO_REPLACE_OBJECTS=1`, `python3 -I -B`, `--pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. Install/upgrade performed: none.

| id | command (abridged) | exit | stdout sha256 (first 16) | UTC |
|---|---|---|---|---|
| base | `c1-counter.py --root <LANE> --rev 29883d4e… --freeze decc5697… --work …/base-work --json-out base-counter.json` | 0 | `ae830b21…` | 22:38:38–22:38:54 |
| at-data | same, `--rev 4aabb0b4…` | 1 (bindings false, expected at data commit) | `73186d0a…` | (run after base) |
| scen1–18 | 18 single-file mutation commits on a fixture clone (parent = REV), counter at each commit | see table | `scen.log` `ce7e49d6…`, `scen2.log` `8b3a45fd…` (S6–S18 re-run; identical verdicts) | — |
| scen19–28 | 7 more mutations | see table | `scen3.log` `865c3072…` | — |
| oracle | `/usr/bin/unsquashfs -lls` and `-d` on the four fixtures read from `git show REV:` | 0 each | listing sha equals `carriers.json` listing sha, all four | — |

Ancestry and scope checks (`git` read-only): `decc5697` is an ancestor of REV; `76d7ad6f` (= `run.json` `rev_at_run`) is the parent of data commit `4aabb0b4`; `4aabb0b4` adds exactly the 51 c1 files (all `A`), and no later commit changes `corpus/evidence/round-49/c1` through REV. `git diff --stat decc5697 REV -- tools/round-49 …` is empty.

## Checks that passed (no disagreement found)

| check | how | result |
|---|---|---|
| committed set == disk set | `git ls-tree -r -l REV corpus/evidence/round-49/c1` (51 blobs, all `100644 blob`) vs `os.walk` of worktree (51 files, 0 symlinks, 0 dirs beyond the 8 `*/firmware.bin_extract`) | equal; per-file bytes equal (`attack1.py`) |
| no symlink or non-regular mode | `ls-tree` (no `120000`), disk `islink` | none |
| largest blob | `ls-tree -l` | 18,009 B (no file near the 1 MiB skip) |
| `extract-tree.tsv` == committed extract files == oracle == `after.json` `files` | `attack2.py` | equal on all four (3,3,4,4 rows; 20,20,28,28 bytes) |
| `after.json` `reported_sha256` == `sha256` | `attack2.py` | all rows |
| `stdout.log` == `envelope.json`; `stdout.data` == `after.json` (canonical JSON) | `attack3.py` | equal on all four |
| raw REA report hashes (excluding the input file) == normalized sha set | `after.json` `raw_result.report` | equal on all four |
| fixture bytes == `carriers.json` `sha256`/`size`; superblock magic, major, minor | `attack2.py` | `hsqs`/`sqsh`, majors 1/2, minor 0; endianness as frozen |
| `carriers.json` oracle members == `output_tree` members; digest recomputes | `attack2.py` | equal; digests `8faae773…` (v1), `4178bb83…` (v2) |
| independent oracle re-derived | `/usr/bin/unsquashfs` 4.7.5 (sha `461e1fd9…`) on `git show REV:` fixture bytes; member sha/size list vs `carriers.json` | equal on all four; no symlink; `-lls` stdout sha = frozen listing sha |
| round-44 `__output__` trees at REV | `ls-tree`, sha vs `members` | equal on all four |
| `run.json`: exit 0, stdout/stderr sha == files, rev_at_run/freeze, fixture pin, handler, endian, output_directory == after.parameters == provenance | `attack3.py`, 56 assertions per carrier, 0 failures (one placeholder assertion in my script was `or True`; excluded, bytes checked separately) | pass |
| tool pins | sha256 of `/home/vgpnk/.local/bin/sasquatch` (`ad02d27a…`, 4.5.1), `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` (`0ce7b624…`, 26.6.4), `/usr/bin/7z` (`f802383f…`), npx-cli (`237adf8f…`), sasquatch-v4be (`fac88740…`) | match `carriers.json` toolchain and `extract-env.json` |
| rea-agents 6.5.0 | `…/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` `version` | 6.5.0 |
| `unblob.log` sha == `extract-env.unblob_log.sha256`; extract command == `command_line`; `-le`/`-be` by carrier | `attack3.py`, `grep` | equal; v1le/v2le `-le`, v1be/v2be `-be` |
| `extract-env` tee sha == `after.engine.executable_sha256` (`28956884…`) | | equal |
| `provenance.json` `produced_tree` bytes/files == `extract-tree.tsv` | | 20/3, 20/3, 28/4, 28/4 |
| counter `evidence_digests` == sha256 of committed `after.json` | `base-counter.json` vs `afterdigests.json` | equal on all four |
| counter bytes == FREEZE blob; `carriers.json` == FREEZE blob | `git show decc5697:…` | `ac83715b…`; `829e3392…` |
| data-commit score reproduces | counter at `4aabb0b4` vs committed `.ufo/waves/round-49/l1/scores/c1-at-data-4aabb0b4.json` | same `carriers_matched 4`, `failing []`, `frozen []`, same six false bindings as entry line 3 |

## Findings

### F1 — committed extracted tree is not bound by the counter (miss in scope, undisclosed)

The counter reads `after.json` only (grep of `c1-counter.py`: no read of `firmware.bin_extract/`, `extract-tree.tsv`, `stdout.log`, `unblob.log`, `run.json`, `provenance.json`, `extract-env.json`, `manifest.json`). Mutating the committed extracted files (each a single-file commit on REV, counter run at that commit):

| scen | mutation | counter exit | carriers_matched | failing |
|---|---|---|---|---|
| S1 `c4567f76…` | `v1le/firmware.bin_extract/apple.txt` bytes replaced (6 → 7 B) | 0 | 4 | `[]` |
| S2 `982da61c…` | `v1le/firmware.bin_extract/cherry.txt` deleted | 0 | 4 | `[]` |
| S3 `70bc8909…` | `v1le/firmware.bin_extract/evil.txt` added | 0 | 4 | `[]` |
| S8 `38474ad5…` | `v2le/firmware.bin_extract/apple1_link.txt` symlink (mode 120000) added | 0 | 4 | `[]` |

So the landed claim (entry lines 87–96: "publishes the census's regular files at their exact relative paths under `firmware.bin_extract/`", "no symlink") is true of the receipt and the census, but nothing the counter runs would notice a committed copy of the extracted tree that disagrees with it. The plan's freeze and disclosed-limit lists do not name this. Disposition for L1: report as a counter miss/limit; the landed text should not describe the committed `firmware.bin_extract/` as counter-verified.

### F2 — sibling receipts and manifest are not bound (miss in scope, undisclosed)

| scen | mutation | counter exit | carriers_matched |
|---|---|---|---|
| S4 `ebe72530…` | `v2be/extract-tree.tsv` sha column zeroed | 0 | 4 |
| S5 `31a07b1c…` | `v1be/run.json` `exit_code: 1` | 0 | 4 |
| S6 `060e1409…` | `v2le/stdout.log` replaced with `{}` | 0 | 4 |
| S7 `3cebb35b…` | `v1le/extract-env.json` sasquatch sha zeroed | 0 | 4 |
| S12 `955a254e…` | `v2le/unblob.log` replaced | 0 | 4 |
| S13 `6ada4929…` | `v1be/provenance.json` `produced_tree.files: 99` | 0 | 4 |
| S16 `8b8eca5d…` | `manifest.json` `rev_at_run` zeroed | 0 | 4 |

The data is only as trustworthy as these files' provenance. Today they agree (see Checks table); the counter would not catch a later edit. `run_provenance_ok` checks the receipt's `output_directory` prefix only, so `provenance.json` is never compared to it either (S13).

### F3 — `depth_limited_paths` and `extraction_continuations` read by no clause

| scen | mutation (after.json) | counter exit | failing per carrier |
|---|---|---|---|
| S25 `bc3cb7bc…` | `v1be` `normalized_result.depth_limited_paths = ["firmware.bin_extract"]`, `extraction_gaps` unchanged `[]` | 1 | `evidence_id_ok`, `matched` — **`projection_ok` true, `gaps_ok` true** |
| S27 `47a0111a…` | `v2le` `extraction_continuations = [{…}]` | 1 | `evidence_id_ok`, `matched` — **`projection_ok` true** |

Both go red only because the stored evidence id no longer matches. A receipt that re-mints the id under the rea-agents 6.5.0 rule (not run) would score `carriers_matched 4` with these fields set. The plan's predicate names `gaps == []` and `unpublished_entries == []`; it does not name `depth_limited_paths` or `extraction_continuations`, and the entry's "reports no gap of any kind" (line 87) is therefore not measured for them. Current values are `[]` on all four carriers (verified), so no present claim is false. Disposition: counter miss, not patched.

### F4 — every `after.json` edit is caught only by the evidence id (calibration note)

Probes S9–S11, S14, S15, S17–S20, S22, S24, S28 turn red. For S19 (injected symlink `StatReport` in `raw_result`), S20 (`raw_result.execution.exit_code`), S22 (`authority`, `confidence`) the failing list is `evidence_id_ok`, `matched` only: the id covers the whole stored envelope and is recomputed with the frozen rule. These are red because I did not re-mint. This is disclosed limit 1 in the plan; I am reporting that the evidence id is the sole guard for these fields, so the disclosed relabelled-replay limit extends to all of them. Re-mint forgery was **not run**.

## Scenario table (all 28 probes, single-file commits on a fixture clone; counter `--rev <commit>`)

| scen | file | exit | matched | failing per carrier |
|---|---|---|---|---|
| S1 | v1le/firmware.bin_extract/apple.txt | 0 | 4 | — |
| S2 | v1le/firmware.bin_extract/cherry.txt (deleted) | 0 | 4 | — |
| S3 | v1le/firmware.bin_extract/evil.txt (added) | 0 | 4 | — |
| S4 | v2be/extract-tree.tsv | 0 | 4 | — |
| S5 | v1be/run.json | 0 | 4 | — |
| S6 | v2le/stdout.log | 0 | 4 | — |
| S7 | v1le/extract-env.json | 0 | 4 | — |
| S8 | v2le/firmware.bin_extract/apple1_link.txt (symlink) | 0 | 4 | — |
| S9 | v1le/after.json files[0] sha | 1 | 3 | v1le: evidence_id_ok, matched, oracle_hits_ok, projection_ok |
| S10 | v1le/after.json parameters.output_directory=/tmp/x | 1 | 3 | v1le: evidence_id_ok, matched, run_provenance_ok |
| S11 | v2be/after.json subject sha | 1 | 3 | v2be: evidence_id_ok, matched, projection_ok, subject_pin_ok |
| S12 | v2le/unblob.log | 0 | 4 | — |
| S13 | v1be/provenance.json | 0 | 4 | — |
| S14 | v2be/after.json files row removed | 1 | 3 | v2be: evidence_id_ok, matched, oracle_hits_ok, projection_ok |
| S15 | v1be/after.json := v1le/after.json (relabel) | 1 | 3 | v1be: matched, projection_ok, subject_pin_ok |
| S16 | manifest.json rev_at_run zeroed | 0 | 4 | — |
| S17 | v1le/after.json unpublished_entries row | 1 | 3 | v1le: evidence_id_ok, matched, nonregular_unpublished_ok, projection_ok |
| S18 | v2le/after.json extraction_gaps depth-limited | 1 | 3 | v2le: evidence_id_ok, gaps_ok, matched, nonregular_unpublished_ok, projection_ok |
| S19 | v1le/after.json raw_result report + symlink StatReport | 1 | 3 | v1le: evidence_id_ok, matched |
| S20 | v1be/after.json raw_result.execution exit_code=1 | 1 | 3 | v1be: evidence_id_ok, matched |
| S22 | v2le/after.json authority, confidence | 1 | 3 | v2le: evidence_id_ok, matched |
| S24 | v2be/after.json coverage=partial | 1 | 3 | v2be: evidence_id_ok, matched, projection_ok |
| S25 | v1be/after.json depth_limited_paths | 1 | 3 | v1be: evidence_id_ok, matched (projection_ok true) |
| S27 | v2le/after.json extraction_continuations | 1 | 3 | v2le: evidence_id_ok, matched (projection_ok true) |
| S28 | v1le/after.json chunks[0].extraction_failed=true | 1 | 3 | v1le: chunks_ok, evidence_id_ok, matched, projection_ok |

Every red probe has `frozen_path_changed []` and `bindings_false []`; the reds are carrier-level only.

## Not run / limits of this report

- Re-minted-id forgery of `after.json` (authority, depth_limited_paths, raw fields with a fresh id): not run.
- `probe-R49C1Run/` scratch is empty; the original REA `rea-out` trees and the `unblob-tee.sh` (sha `28956884…`) cannot be re-checked. `provenance.json` `rea_outdir_state_before_run: absent` is unverifiable.
- The `unsquashfs -d` stdout sha recorded in `carriers.json` (`7d9a733a…`) was not reproduced byte-for-byte (I ran with `-no-progress` into a different path); member digests and listing sha were reproduced.
- Control runs CTL-C1-* and `--selftest` were not run here.
- `scen-results-all.json` was written by the first scenario run, which completed all 18 probes; the second run re-ran S6–S18 (identical verdicts, parents = REV verified per commit).

## Routed to L1 (no patch by me)

1. Counter scope (F1, F2): the frozen counter binds only `after.json`. Either add the plan's disclosed-limit text for the committed extract tree and sibling receipts, or state in the entry that those bytes are not counter-verified (non-frozen text; L1 may edit).
2. Counter gap clause (F3): `depth_limited_paths` and `extraction_continuations` are not in `gaps == []`. Record as a miss in the lesson; do not patch the frozen counter.
3. Entry line 96 says the four carriers "hold no symlink"; that is true of the census and the receipt, not of the committed tree, which the counter does not read (S8). Wording repair is non-frozen text.
