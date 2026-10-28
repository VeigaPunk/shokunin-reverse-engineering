# C1Struct-2 — R48-C1 clauses 1–2

| rev | exit | marker occurrences | craft blocks | present | exact failing list |
|---|---:|---:|---:|---:|---|
| `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` | 1 | 0 | 24 | 0 | [`marker_occurrences 0 != 1`, `marker_block_count 0 != 1`] |
| `61b87d742032e65fca9c38267d7d6ed7e555edad` | 2 | n/a | n/a | n/a | `freeze is not an ancestor of rev` |

Exact command form for both: `HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C1Struct-2 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev <REV> --json-out .ufo/waves/round-48/w1/C1Struct-2/meanings-<prefix>.json`. Captured receipt including full commands, stdout, stderr, exit codes, UTC and stdout hashes: `.ufo/waves/round-48/w1/C1Struct-2/receipt.json`.

Freeze C1 structural clauses 1–2 are unmet: marker/block absent. Base comparison was unevaluable under the provided freeze parameter. No additional clause/battery checks run; no frozen or lane implementation files changed. Checks not run: format/lint/build/tests (parent owns post-integration verification).
