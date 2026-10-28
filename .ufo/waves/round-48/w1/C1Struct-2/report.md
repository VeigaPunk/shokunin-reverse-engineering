# C1Struct-2 — R48-C1 clauses 1–2

Read-only measurements; axis coverage/depth/calibration: clauses 1–2 depth only. No lane files changed.

| rev | exit | marker occurrences | rule blocks | block present | failing | stdout SHA-256 |
|---|---:|---:|---:|---:|---|---|
| `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` | 1 | 0 | 24 | 0 | `marker_occurrences 0 != 1`; `marker_block_count 0 != 1` | `594e618c67908dfb390e2ad654b616a321e923af4bdbaff92a13dbc940eb330a` |
| `61b87d742032e65fca9c38267d7d6ed7e555edad` | 2 | not evaluated | not evaluated | not evaluated | counter reports freeze is not an ancestor of rev | `ea27f708e9f356f43e540289dc744f8f0f39c01ad90fc9edcc6ecd79b5fc1ffd` |

Exact invocation for each: `HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C1Struct-2 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev <REV> --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/C1Struct-2/meanings-<REV-prefix>.json`.

UTC captured in `receipt.json`; stdout and exit are preserved there, along with JSON counter outputs. Freeze-revision C1 clauses 1–2 fail because the landing rule block is absent (24 blocks; marker absent). Base comparison cannot be evaluated with the frozen freeze argument because the freeze is not its ancestor. Clauses beyond 1–2, mutation battery/forgery attacks, and independent checks were not run.
