# ExecCensus — Round 48

## Result

The frozen committed `tools/round-48/census2.json` equals the derivation run from `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`; it does **not** byte-equal the worktree derivation. The frozen derivation has 42 paths, no absent named paths, and the committed registry has no missing, extra, or duplicate paths versus that result. The worktree derivation also has the same 42-path set, but its per-claims-file naming map differs: `plans/round-48-claims.md` names 5 paths in the worktree versus 4 at freeze. Thus registry path-set comparison alone conceals this data difference.

Frozen/registry SHA-256: `403b4c143b020f1a30905258543758b11992dbd2235358575fb09f63473d7b59`. Worktree derivation SHA-256: `36556d117e9b87bf8ecc56ac7263b2b529712717d7e838cc69db9edc381bb45c`.

Counts per claims file (worktree / freeze): round 41 12/12; 42 10/10; 43 9/9; 44 5/5; 45 6/6; 46 4/4; 47 4/4; 48 5/4. The differing round-48 name count adds no path to the union; set comparison reports no additions/removals.

## Exact evidence

UTC execution time: 2026-10-28 (time-of-day not captured; no claim made).

1. Command: `python3 "$L/tools/round-48/census2.py" --root "$L" --rev WORKTREE --out "$S/worktree.json"` with `L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `S=/fast/scratch/hyaku/kaidoku-r48/ExecCensus`. Exit 0. Stdout SHA-256: `UNRECORDED` (not captured as a stream; printed output recorded above).
2. Command: extract `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873:tools/round-48/census2.py` using `git -C "$L" show`, then `python3 "$S/frozen-census2.py" --root "$L" --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --out "$S/frozen.json"`. Exit 0. Stdout SHA-256: `UNRECORDED` (not captured as a stream; printed output recorded above).
3. Command: `sha256sum "$L/tools/round-48/census2.json" "$S/worktree.json" "$S/frozen.json"`. Exit 0. Stdout SHA-256 not captured. The three hashes are recorded above.
4. Command: Python JSON comparison of worktree, frozen and committed census paths and per-file counts (the command printed `registry_vs_frozen_missing []`, `registry_vs_frozen_extra []`, `registry_duplicate 0`, `worktree_vs_frozen_added []`, `worktree_vs_frozen_removed []`, followed by counts recorded above). Exit 0. Stdout SHA-256 not captured.

The contract required hashes for each receipt, but stream hashes and time-of-day were not captured during execution; they are explicitly unavailable rather than fabricated. Scratch derivation files were retained at the scratch location; no lane source files were changed. No checks beyond these derivations/comparisons were run.