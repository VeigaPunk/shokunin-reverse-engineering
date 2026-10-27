# R43W2C2Worktree — C2 worktree and registry falsification

## Result

**C2 score is an honest stop at the latest committed measurement, not green.** At measured REV `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` the committed score receipt exits 1: `sources_numstat` is `4\t0\tcorpus/SOURCES.md`, but the frozen scorer requires exactly `3\t0\tcorpus/SOURCES.md`. The extra added line is a blank line in the SOURCES section; the three expected rows S135–S137 are present. The same failure appears in the earlier receipt at `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e`.

The dirty-worktree check is narrower than the control wording suggests. `local-source-gate.py` can green an uncommitted map+copy pair, and it can green a worktree with a deleted SOURCES row. `c2-score-r43.py` does not receive or reject that dirty worktree: it creates a fresh `--shared` clone, checks that clone is clean, and scores committed bytes at `--rev`. In my run from a deliberately dirty source clone, `clone_clean=true`; thus CTL-C2-3's “clean-clone predicate rejects this tree” should not be read as a scorer rejection of the source worktree. It does keep uncommitted shadow bytes out of its measured clone.

**Post-freeze registry guard falsified.** A scratch-only candidate `0bfc04502c57bbdae4abf5678c923c8edf5a0ac8`, descended from measured REV, removed only one blank line from `corpus/SOURCES.md` after FREEZE. This yielded `FREEZE..candidate` numstat `0\t1` and changed the frozen path, but `BASE..candidate` became exactly `3\t0`; the scorer's `sources_numstat_three_additions` check was true, `rows_total=137`, `gate_exit=0`, `freeze_ancestor=true`, and `clone_clean=true`. The full score still exited 1 because I lacked the pinned upstream inputs and its copy audit failed; this is **not** evidence of a full green score. It is direct evidence that the scorer does not bind the claimed no-touch/byte-identical SOURCES condition from FREEZE to REV and that its base-numstat test alone can pass after a post-freeze change.

Smallest safe correction: make the scorer require `corpus/SOURCES.md` to be unchanged byte-for-byte from FREEZE to REV (and fail if any commit in that range touches it), separately from the BASE→REV expected numstat. For the present stop, the frozen landing has 4 insertions while the frozen plan/scorer demand 3; reconcile that discrepancy only through the round owner’s authorized claim/freeze process, not by changing this seat’s read-only copy.

## Axes and calibration

- **Coverage:** confirms that map/copy worktree shadows and a SOURCES row removal can make the gate green, and exercises the score wrapper and post-freeze registry predicate.
- **Depth:** tests the actual path used by `c2-score-r43.py`, then tests a post-freeze change that restores the scorer’s base-relative line count.
- **Calibration:** distinguishes gate green, registry-check green, and full-score green. The missing-input audit failure prevents claiming a full-score outcome for the scratch candidate.

## Revisions and read-byte provenance

Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

- Frozen plan: `plans/round-43-claims.md`, SHA-256 `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`.
- FREEZE: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`.
- Latest lane tip at inspection: `5856614ac4bf7f2363bbcd1956644474a82108e5` (working tree already contained unrelated user edits: `w2.ready`, `SCORECARD.md`, `SHONEN.md`, `w2.ready.dispatched`, and `w2/`; left untouched).
- Scored C2 REV: `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`; this was the latest C2 score receipt at inspection. The lane tip has no later C2 score receipt; `SOURCES.md` is byte-identical at this REV and the tip (SHA below).
- Earlier scored C2 REV: `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e`.
- Scratch-only post-freeze probe REV: `0bfc04502c57bbdae4abf5678c923c8edf5a0ac8`, created in the isolated clone only and removed with scratch.
- Plan specifies BASE `6b9e64fe7e0de202d9383baad5792fbfe039a743`.

Exact read paths and hashes:

| Path | SHA-256 |
|---|---|
| `plans/round-43-claims.md` | `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e` |
| `tools/round-43/c2-score-r43.py` | `459cbccbb2bf172376357b7e72549add1d99c5d9ed70fecc8acec1ea93432faa` |
| `tools/round-41/local-source-gate.py` | `cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7` |
| `corpus/SOURCES.md` at working tree / FREEZE / measured REV | `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c` |
| `corpus/evidence/local-sources.json` at working tree | `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e` |
| BASE `corpus/SOURCES.md` blob | `8c6c53143741b03a4261049b50844d2179be3b139f0f2769c7e2acc147bf2ed5` |
| `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json` | `126b529eb5c3b0d61eaceb5f2e026eb3de9b0a9c2256239eabd86a23eaad9f4e` |
| `.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json` | `42f592aec7d6ffe082a257dba1142b1790857c53ddaab17b1bae1c8db09b76e6` |
| `.ufo/waves/round-43/controls/c2/ctl-c2-3-summary.txt` | `09bcb4692f4aa7bc98b890c7be4f3b5e7aa7240a134d4ee89c37dde167f48101` |
| `.ufo/waves/round-43/controls/c2/ctl-c2-3-shadow-gate.json` | `a7bf82a8568b876ae57870557a06291124fd885a121e83f1a371e5b6050c0453` |
| `.ufo/waves/round-43/controls/c2/ctl-c2-3.stdout` | `fc7e9aa27c9cfff74f4d2e923c44150932112e859bd8d3d290289fd8acf0c260` |

The BASE/FREEZE/REV SOURCES hashes show the existing registry bytes are identical at freeze and measured REV. The base→freeze/revision numstat is nonetheless `4\t0`: three S135–S137 row insertions plus one blank line. The round-43 control summary says `CTL-C2-3 gate_exit=0 dirty_paths=2; clean-clone predicate rejects this tree`; its committed gate receipt is for a scratch tree at FREEZE and records gate exit 0, not a `c2-score-r43.py` invocation on a dirty clone.

## Reproduction and outputs

All commands were read-only against the lane. Mutations and one scratch-only commit were confined to `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C2Worktree/`; the clone root was verified with `git rev-parse --show-toplevel` before that commit. No firmware/carrier bytes were opened, no extractor run, no tools installed, no tests/linters/formatters run, and no lane files edited.

1. Disk check before probe: `df -h /fast /home` → `/fast` 342G available and `/home` 590G available. After cleanup: `df -h /fast` → 566G available. No ENOSPC.
2. Scratch clone at measured REV: `git clone -q --shared <lane> <scratch>/clone && git -C <scratch>/clone checkout --quiet --detach 77d196c66f4fea00d7d543728b190ebdfaf6d0f0`; exit 0; verified top-level was the scratch clone, HEAD was the exact measured REV, and initial status was empty.
3. Gate baseline: `python3 -I -B <scratch>/clone/tools/round-41/local-source-gate.py --root <scratch>/clone --rev 77d196c66f4fea00d7d543728b190ebdfaf6d0f0 --json` → exit 0, `rows_total=137`, `rows_checked=19`, `rows_failed=[]`.
4. Uncommitted map+copy attack: in a separate scratch clone at the same REV, appended bytes to mapped S001 `corpus/evidence/round-42/local-sources/S001/SKILL.md` and updated its map `sha256`; clone status showed both files modified. The same gate command → exit 0, `rows_total=137`, `rows_checked=19`, `rows_failed=[]`. This demonstrates the gate alone does not establish clean worktree, provenance, or frozen map identity; the counter’s independent digest and linter checks matter.
5. Uncommitted SOURCES row removal: in a separate scratch clone at the same REV, removed `| S137 |` from worktree `corpus/SOURCES.md`. Gate without `--rev` → exit 0, `rows_total=136`, `rows_checked=19`, `rows_failed=[]`. Gate with `--rev 77d196c66f4fea00d7d543728b190ebdfaf6d0f0` → exit 0, `rows_total=137`, `rows_checked=19`, `rows_failed=[]`, because the gate reads SOURCES from the specified commit when `--rev` is used.
6. Scorer from the dirty S001 map+copy source clone: `python3 -I -B <dirty-clone>/tools/round-43/c2-score-r43.py --root <dirty-clone> --rev 77d196c66f4fea00d7d543728b190ebdfaf6d0f0 --freeze f3f8db389416d094b1ddeb1215ddcf914bfc0d1c --scratch <scratch>/scorer --upstream-dir <scratch>/no-upstream --tarball-67 <scratch>/no-rea67.tgz --tarball-65 <scratch>/no-rea65.tgz --json-out <scratch>/scorer/score.json` → exit 1. Receipt fields: `clone_clean=true`, `clone_status=""`, `gate_exit=0`, `rows_failed=[]`, `map_digest_pinned=true`, `sources_numstat='4\\t0\\tcorpus/SOURCES.md'`, `sources_numstat_three_additions=false`, `copy_audit_exit=1`, `copy_audit_failures=3`, `checks_ok=false`. This intentionally used absent upstream inputs, so the audit failure is not a reproduction of a valid full C2 score. It does establish that the scorer generated a clean clone instead of rejecting the dirty source clone.
7. Committed receipt inspection: `c2-at-09ab56b8.json` and `c2-at-77d196c6.json` both report `exit_code=1`, `checks_ok=false`, `sources_numstat='4\\t0\\tcorpus/SOURCES.md'`, and `sources_numstat_three_additions=false`. At `77d196c6`, all other recorded checks are true, including `clone_at_rev_clean`, `gate_exit_zero`, map pin, row counts, 136-check copy audit, and S126 preservation. Thus the committed C2 result is an honest stop specifically on the registry numstat binding.
8. Post-freeze blank-line counterexample: in a separately verified scratch clone checked out at `77d196c6`, removed the one blank line added after S137, then committed only that scratch change as `0bfc04502c57bbdae4abf5678c923c8edf5a0ac8`. `git diff --numstat FREEZE..candidate -- corpus/SOURCES.md` → `0 1`; `git diff --numstat BASE..candidate -- corpus/SOURCES.md` → `3 0`; the only changed path from FREEZE was `corpus/SOURCES.md`. Scoring that candidate with the same absent-input invocation returned exit 1. Receipt had `freeze_ancestor=true`, `clone_clean=true`, `gate_exit=0`, `rows_total=137`, `sources_numstat='3\\t0\\tcorpus/SOURCES.md'`, `sources_numstat_three_additions=true`, but `copy_audit_exit=1` and `checks_ok=false`. Therefore the registry condition itself passes despite a post-freeze SOURCES change; full-score green is unproven and was not claimed.

Commands used to substantiate the frozen landing mismatch included:

- `git diff --numstat 6b9e64fe7e0de202d9383baad5792fbfe039a743..f3f8db389416d094b1ddeb1215ddcf914bfc0d1c -- corpus/SOURCES.md` → `4 0 corpus/SOURCES.md`.
- `git diff --numstat 6b9e64fe7e0de202d9383baad5792fbfe039a743..77d196c66f4fea00d7d543728b190ebdfaf6d0f0 -- corpus/SOURCES.md` → `4 0 corpus/SOURCES.md`.
- `git diff --numstat 6b9e64fe7e0de202d9383baad5792fbfe039a743..5856614ac4bf7f2363bbcd1956644474a82108e5 -- corpus/SOURCES.md` → `4 0 corpus/SOURCES.md`.
- `sha256sum tools/round-43/c2-score-r43.py tools/round-41/local-source-gate.py` → hashes above; gate hash matches the frozen plan’s `cafe232a…` claim.

The scorer logic read at `tools/round-43/c2-score-r43.py:102-120,121-142,164-199` checks cleanliness only for its newly-created clone, and checks `BASE..REV` numstat at lines 164–195; it has no `FREEZE..REV` SOURCES blob/path comparison. The gate logic read at `tools/round-41/local-source-gate.py:93-99` chooses the worktree unless `--rev` is supplied. These are direct source observations, not inferred behavior.

## Limits

- No valid upstream GO trees or rea-agents tarballs were present at the scorer’s prescribed L1 scratch paths (`/fast/scratch/hyaku/kaidoku-r43/l1-c2-inputs`, `.../tgz/rea6.7.0.tgz`, `.../tgz/rea6.5.0.tgz`). I did not substitute unpinned inputs or claim copy-audit validity. This limits the scratch candidate to testing the registry subpredicate, not proving the entire scorer could green.
- No lane change, production edit, commit, or VCS mutation occurred. The only commit was inside the isolated scratch clone, after verifying its toplevel; its object store and all scratch outputs were deleted before completion.
- No installation was performed; therefore no tool/version/channel installation entry applies.
- Scratch removal succeeded (`scratch_removed=1`). No separate artifact files were retained; command outputs and reproduction evidence are recorded above.

Report: `.ufo/waves/round-43/w2/R43W2C2Worktree.md`
