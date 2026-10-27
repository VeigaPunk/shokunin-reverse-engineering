# R43W2C2MapMut — C2 map/linter mutation results

## Scope and measured revisions

Read the frozen plan first. Freeze: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`.

The pristine baseline and uncommitted scratch mutations were evaluated with `--rev 5856614ac4bf7f2363bbcd1956644474a82108e5`, the lane tip observed at the start of this seat. The lane advanced during the wave to `80e27dc1c0382ffc7e5596198fba8f58f804573c`; `git diff --name-status 5856614..80e27dc` showed only `SCORECARD.md`, `SHONEN.md`, and new `corpus/lessons/round-43.md`. The frozen plan, SOURCES, map, gate, verifier, and scorer were unchanged in that interval. A clean committed parent-symlink mutant was separately tested at `82d5afe25519cc01ee1d91b443759e16d8ba4257`, parent `80e27dc1c0382ffc7e5596198fba8f58f804573c`.

## Read inputs and hashes

All paths below are relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless absolute paths are shown.

| Path | SHA-256 / identity |
|---|---|
| `plans/round-43-claims.md` | `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e` |
| `corpus/SOURCES.md` at measured tip | `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c` |
| `corpus/evidence/local-sources.json` | `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e` |
| `tools/round-43/verify-copies-r43.py` | `00b3f7a4c7a2ee7f5a6654f12211cbf2a12e0fe10e9de7fc35ff088ce8f3b020` |
| `tools/round-43/c2-score-r43.py` | `459cbccbb2bf172376357b7e72549add1d99c5d9ed70fecc8acec1ea93432faa` |
| `tools/round-41/local-source-gate.py` | `cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7` |
| `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` | `13a495dbb6862d6cfbdd1f41e4a09460740f86bf93e8bb08e313b06d92b8a55c` |
| `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json` | `126b529eb5c3b0d61eaceb5f2e026eb3de9b0a9c2256239eabd86a23eaad9f4e` |
| `.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json` | `42f592aec7d6ffe082a257dba1142b1790857c53ddaab17b1bae1c8db09b76e6` |
| `.ufo/waves/round-43/controls/c1/summary.json` | `143d4c38412c8d4af785243ffdabc5e8735d0237818643ce1bb151e4db624e5d` |
| `.ufo/waves/round-43/controls/c2/ctl-c2-2-summary.txt` | `4d1ae7eb4b902a2a6fa3e26c5e61f4dc9be521075ea23cdefa256109f387a1eb` |
| `.ufo/waves/round-43/controls/c2/ctl-c2-2-symlink-audit.json` | `34cb5421d29634e6777d5b9b2d4bac98b3b07fe96ae74e2598e4e958f8559ce1` |
| `.ufo/waves/round-43/controls/c2/ctl-c2-2-symlink-gate.json` | `308dfe406305e5922c21111a7e5c709fcbe9065eb409dc7a1b54056fe68ab661` |

C1 score receipt: exit `0`, `matched=78`, `n=78`, and `observed_features_match_declared=true`. C1 control summary: `ok=true`, `kill_rule_fires=false`, `controls_at_target=[]`. C2 CTL-C2-2 summary records baseline gate/linter `0/0` and its leaf-symlink arm `0/1`.

Both committed C2 score receipts are red: at their recorded revisions (`09ab56b8fdc2efcc3b58b203644537d84dd5ac9e` and `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`) each has `exit_code=1`, `checks_ok=false`, and the sole false check is `sources_numstat_three_additions`; each records `sources_numstat="4\t0\tcorpus/SOURCES.md"`. The frozen plan requires exactly three additions. The BASE→`5856614` and BASE→current-tip numstat also returns `4\t0\tcorpus/SOURCES.md`; the visible diff is S135/S136/S137 plus a blank line after S137. No C2 score receipt at `80e27dc` was present. **[INFERENCE]** Because the scorer and SOURCES bytes are unchanged after `5856614`, a score at the latest tip would retain this same failing numstat binding absent an amendment to the frozen predicate.

## Detector and input setup

Scratch: `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C2MapMut/` (removed before yield). Lane-side artifacts: `.ufo/waves/round-43/w2/artifacts/R43W2C2MapMut/`.

The pristine clone was clean at `5856614ac4bf7f2363bbcd1956644474a82108e5`. Final pristine detector result: gate exit `0`, `rows_checked=19`, `rows_total=137`, `rows_failed=[]`; verifier exit `0`, `checks: 136, failures: 0`. The imported EXPECT source check reported work/freeze/rev SHA-256 all `1f790e102be74fbab2a4e24c4235cd59c7a0b91e8bb0fa821259279af4256ded`.

The same two commands were run for each map/copy mutant and after restoration (working directory `$C`, isolated clone):

```sh
python3 -I -B tools/round-41/local-source-gate.py --root "$C" --rev 5856614ac4bf7f2363bbcd1956644474a82108e5 --json
python3 -I -B tools/round-43/verify-copies-r43.py --root "$C" --rev 5856614ac4bf7f2363bbcd1956644474a82108e5 --freeze f3f8db389416d094b1ddeb1215ddcf914bfc0d1c --upstream-dir "$S/upstream" --tarball "$S/tgz/rea-agents-6.7.0.tgz" --tarball-650 "$S/tgz/rea-agents-6.5.0.tgz"
```

A preliminary baseline was inconclusive: I initially fetched only the three pinned Go members, so S035 upstream identity reported two failures (`checks: 136, failures: 2`). I then fetched all archive-listed `src/internal/abi` members for tags `go1.25.0` and `go1.24.6`, fetched the pinned npm 6.7.0/6.5.0 tarballs, verified the pinned member digests through the linter, and reran to the green baseline above. Sources used were only the named Go raw-tag paths and `https://registry.npmjs.org/rea-agents/-/rea-agents-{6.7.0,6.5.0}.tgz`; no firmware image was opened and no REA/unblob/sasquatch/extractor was run. No tools were installed.

## Mutation outcomes

`KILLED` means the expected relevant binding failed; `SURVIVED` means the gate and verifier accepted the mutant. Raw JSON/text output for each mutant and each restored state is in the artifacts directory named above. Mutated map hashes below were measured before restoration; unchanged map means the filesystem-only mutation did not alter the map.

| Attack / mutated bytes | Gate result | Verifier result | Verdict / binding |
|---|---|---|---|
| Duplicate JSON key (`version` repeated; map SHA `467448059eb1a7129c7398fea4d50077ff73a99f6636559fba2aec7d196563cc`) | exit 0; `rows_failed=[]` | exit 1; `map-no-duplicate-keys FAIL version`, 1 failure | **KILLED** by duplicate-key scan; gate's last-wins parser is not sufficient alone. |
| Duplicate copy alias (S002 redirected to S001 copy and digest; map SHA `895dc034424cab891f4fdef730c83467407092abdaee1e0c98c9085bdf291c00`) | exit 0; `rows_failed=[]` | exit 1; `copy-unique FAIL`; S002 `byte-identical` also fails | **KILLED** by alias binding. |
| Leaf copy symlink (map unchanged) | exit 0; `rows_failed=[]` | exit 1; `copy-regular ...S001/SKILL.md FAIL symlink` | **KILLED** for a symlink at the copy leaf. |
| Symlinked directory component `S001 -> S001.real` (map unchanged) | exit 0; `rows_failed=[]` | exit 0; 136 checks, 0 failures; `copy-regular` and `copy-in-stated-dir` both OK while one symlink existed under the copy tree | **SURVIVED.** `os.lstat(cp)`/`islink(cp)` check only the final path component, not parent components. |
| Absolute copy path (`copy` set to its external absolute source; map SHA `05686714b268d868ba9394781e95f614758c0e16226340b30f67a641ecbe1ad5`) | exit 1; S001 reason `copy-outside-lane` | exit 1; `copy-in-stated-dir FAIL` | **KILLED** by path-scope bindings. |
| Dot-dot escape from stated directory to clone `README.md` (`copy=corpus/evidence/round-42/local-sources/S001/../../../../../README.md`; map SHA `dddd95f86ed0c85b8e3f93b7eab3241e77d733186b298a5bb1427d19c22c81bb`; README mutated to byte-identical S001 host bytes, SHA `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692`) | exit 0; `rows_failed=[]` | exit 0; 136 checks, 0 failures; `copy-in-stated-dir OK`, map-digest and byte-identical OK | **SURVIVED.** The linter tests the unnormalized string prefix `rel.startswith(STATED_DIR)`; normalization resolves the copy outside the required local-sources directory. |
| Stub plus matching map digest (stub copy SHA `55be89cbb480ca8d9cdee83be6eb3ea0767011557025e4e1d09bf09de4498930`; map SHA `1e96d2443440cb03af4dcac9d9e60027218f14cdacfd1f8ca16f19d8e0e2a93a`) | exit 0; `rows_failed=[]` | exit 1; map-digest OK, `byte-identical S001 ... FAIL` | **KILLED** by content identity, not the map's self-declared digest. |
| S001 copy 5 MiB + 1 byte (5,242,881 B; copy SHA `37e6fb3a639ff51a4b8c77e001de75ed3c592bde3843655ab2197df1cd4640fc`; map SHA `98152fcf7d7ceba7d6f70a5d9172ec14ff596051729a4455977cc9e92f28eeeb`) | exit 0; `rows_failed=[]` | exit 1; `copy-size FAIL 5242881 B`; map-digest OK; byte-identical also fails | **KILLED** by size and content checks. |
| Remove S126 map entry (map SHA `a90ffdc4139179cca5287c9d0215657c76bb5f111fc08941b2a2361efc9b8152`) | exit 1; S126 `no-copy-named` | exit 1; `key-set-equals-rows FAIL`, missing the S126 absolute path | **KILLED** by key-set binding. |
| Remove S126 copy file (map unchanged) | exit 1; S126 `copy-missing` | exit 1; `copy-regular ...s126/lead1-avm-image.tsv FAIL missing` | **KILLED** by copy existence binding. |

### Clean committed parent-symlink reproduction

To exercise the clean-clone form, I cloned the lane into scratch, verified `git rev-parse --show-toplevel` equaled that clone before committing, committed only the S001 parent-symlink mutation, and ran the frozen scorer at mutation revision `82d5afe25519cc01ee1d91b443759e16d8ba4257`. Its generated clean clone was clean. The scorer reported `gate_exit=0`, `copy_audit_exit=0`, `copy_audit_checks=136`, `copy_audit_failures=0`, and `map_digest_pinned=true`; its only false check was the unrelated already-red `sources_numstat_three_additions`, so scorer exit was 1. The embedded linter output marks S001 `copy-regular OK`. This confirms the parent-link survivor is not an artifact of a dirty direct-test worktree; the score wrapper does not add the claimed parent-component scan. Receipt: `artifacts/R43W2C2MapMut/parent-symlink-score.json`.

The frozen plan says the scoring wrapper adds a `find -type l`/lstat walk over the copy directories. The read `c2-score-r43.py` implementation delegates to the gate and `verify-copies-r43.py`; the latter lstats only `cp` and performs no ancestor walk. The committed parent-symlink probe therefore falsifies that implementation clause. The dot-dot linter survivor is independently a structural-path-check gap; **[INFERENCE]** a full score of a mutated map would also reject its non-pinned map hash, but that different whole-map binding does not establish the required copy-directory containment check.

## Restoration and artifacts

After every mutant, I restored the map/copy/README bytes from scratch backups and reran both detectors. Every final restored run returned gate `0` and verifier `0` with `136/0`; restored map SHA was `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e`, S126 copy SHA `f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0`, and README SHA `63ffe86cc6e62ae770bb3e7d52890f8a098527b44066ce11a03a63fdd6a2d06e`. Final scratch-clone `git status --porcelain` and `git diff --quiet` were empty/success; no symlinks remained in either checked copy tree. One first leaf-symlink restore attempt used `copy2` through the symlink and therefore did not restore it; I caught the still-symlink via `stat`, unlinked it, recopied the backup, and reran the detector successfully. The final corrected restoration—not the mistaken intermediate result—is recorded as `symlink-leaf-restored-*`.

Artifacts (full stdout receipts) are under `.ufo/waves/round-43/w2/artifacts/R43W2C2MapMut/`: pristine, each mutant, and each restored gate JSON/verifier text, plus the clean committed parent-symlink score receipt and its stdout. Example SHA-256s: pristine gate `8e5c9155f9623eac73701968db82a40a897aa3ed2ab031d6d0dfb6ee597cc94e`; pristine linter `ff4a9f2ac89eea6b898ade880d1edfea8d605be732374e1b33f3abb4cd96b532`; dot-dot linter survivor `4b9b1ba31871c20ee6fd9ebda991e14b860b1dad30a1bb7b63de510c9cd7b084`; committed parent-symlink score JSON `08b98518d0cf536a670b0bf41bfb3e3ffd89b8d68e47df08a7cc8ae71e6ca360`.

Disk check before probes reported 580 GiB available on `/fast`; no ENOSPC. No installation, pacman, whole-repository test/lint/format run, lane commit, or production edit was performed. The only lane writes are this report and its listed artifacts. The seat scratch directory was removed before yield.
