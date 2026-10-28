# Mutation matrix — `tools/round-46/attest.py --selftest`

Each run: `cd <dir> && TMPDIR=<dir>/tmp HYAKU_SCRATCH=<dir>/scr python3 -I -B attest.py --root /nonexistent --freeze deadbeef --rev deadbeef --selftest`.

| version | mutant | one-change | exit | cases | failures | stdout sha256 | utc | verdict | cases that went red |
|---|---|---|---|---|---|---|---|---|---|
| base | (baseline) | none | 0 | 15 | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | 2026-10-28T17:04:25Z | BASELINE | — |
| base | m1-marker-count | clause 1: marker_occurrences != 1 -> < 1 (a doubled marker passes) | 1 | 15 | 1 | `1bdea82adf3440b3b914c15efcf31f277493257d2d9ae95e6b92ed1b59b56456` | 2026-10-28T17:04:25Z | **KILLED** | red-two-markers |
| base | m10-drop-refs-min | clause 5: refs_min floor dropped | 0 | 15 | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | 2026-10-28T17:04:29Z | **SURVIVED** | — |
| base | m11-no-line-selector | clause 5: hard profile stops requiring a line selector | 0 | 15 | 0 | `552819abd02d365261c1e20c1e361fa1b09217677072597aeafab22d2e207e82` | 2026-10-28T17:04:30Z | **SURVIVED** | — |
| base | m12-must-cite-refs | clause 5: does not cite round-45.md accepted | 0 | 15 | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | 2026-10-28T17:04:31Z | **SURVIVED** | — |
| base | m2-not-last | clause 1: drop the is-last-craft-block check | 1 | 15 | 1 | `bd0df8de544f6f6938aabde71d8f9bb8548f594704697d621f1fd3d34282f03f` | 2026-10-28T17:04:25Z | **KILLED** | red-marker-not-last |
| base | m3-header-prefix | clause 2: header cells matched by prefix instead of equality | 0 | 15 | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | 2026-10-28T17:04:25Z | **SURVIVED** | — |
| base | m4-rows-floor-8 | clause 3: r46 min_rows 13 -> 8 | 0 | 15 | 0 | `2079b3c2bb009e7620c13ea6daa1b97e3373266912ba55633c461ec2e986d531` | 2026-10-28T17:04:27Z | **SURVIVED** | — |
| base | m5-drop-exit-cell | clause 3: drop the exit-cell membership check | 1 | 15 | 1 | `2f253d614e27f99f5bc88921ee73d098b2c1ad3c99e9cce742233a8cecbb5d7f` | 2026-10-28T17:04:27Z | **KILLED** | red-exit-cell |
| base | m6-drop-routed | clause 4: drop the routed-id check | 1 | 15 | 1 | `baf196488be9eb2f8ae2b49e8aa900b6a56e37ac218aefed4fa088858d0abd6f` | 2026-10-28T17:04:28Z | **KILLED** | red-routed-id-missing |
| base | m7-vocab-whole-row | clause 4: vocabulary matched by substring over the whole row, not the arm cell | 0 | 15 | 0 | `a603098cc3c6d0434cfa63d7d84ef0959e43b46e45682ac8b3e09f7d070764ea` | 2026-10-28T17:04:28Z | **SURVIVED** | — |
| base | m8-pin-by-length | clause 6: sha256 pin compared by length only | 1 | 15 | 1 | `f7f3f60524b8b871989eb152c8fa59ad412865777844a46051c019026907ecd0` | 2026-10-28T17:04:28Z | **KILLED** | red-pin-mismatch |
| base | m9-drop-allowlist | clause 5: citations outside the validated path set accepted | 0 | 15 | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | 2026-10-28T17:04:29Z | **SURVIVED** | — |
| head | (baseline) | none | 0 | 16 | 0 | `0bf8f4c6ae0e46a0c4f00b9eb8b573afd7c10b0bbb6bf7e2ce58e7c2c5296dd8` | 2026-10-28T17:04:25Z | BASELINE | — |
| head | m1-marker-count | clause 1: marker_occurrences != 1 -> < 1 (a doubled marker passes) | 1 | 16 | 2 | `9826f2f3149bd6231b5c2ce603a5430fc73271b867cf7bd9a0b5976dfd0165fa` | 2026-10-28T17:04:25Z | **KILLED** | red-two-markers, green-with-battery |
| head | m10-drop-refs-min | clause 5: refs_min floor dropped | 0 | 16 | 0 | `0bf8f4c6ae0e46a0c4f00b9eb8b573afd7c10b0bbb6bf7e2ce58e7c2c5296dd8` | 2026-10-28T17:04:29Z | **SURVIVED** | — |
| head | m11-no-line-selector | clause 5: hard profile stops requiring a line selector | 1 | 16 | 1 | `4ddd80fdc4005723265955ca68280415d590bd92c955698a199055eb5287065b` | 2026-10-28T17:04:31Z | **KILLED** | green-with-battery |
| head | m12-must-cite-refs | clause 5: does not cite round-45.md accepted | 1 | 16 | 1 | `53cde3bc55f46b9dfb7f5527d0b44832ad1cfef0545160673c8e6e02a7bb8281` | 2026-10-28T17:04:31Z | **KILLED** | green-with-battery |
| head | m2-not-last | clause 1: drop the is-last-craft-block check | 1 | 16 | 1 | `a37ebfd0f504474c47bf0986f04c3dca583b9f3b2692e32d2b6409d4960e08ac` | 2026-10-28T17:04:25Z | **KILLED** | red-marker-not-last |
| head | m3-header-prefix | clause 2: header cells matched by prefix instead of equality | 1 | 16 | 1 | `53cde3bc55f46b9dfb7f5527d0b44832ad1cfef0545160673c8e6e02a7bb8281` | 2026-10-28T17:04:25Z | **KILLED** | green-with-battery |
| head | m4-rows-floor-8 | clause 3: r46 min_rows 13 -> 8 | 0 | 16 | 0 | `ebffd25210395f26bf4302e7b40f2fbcc6e719eb743bc9a9fa26fc104adc9654` | 2026-10-28T17:04:27Z | **SURVIVED** | — |
| head | m5-drop-exit-cell | clause 3: drop the exit-cell membership check | 1 | 16 | 1 | `9d88d9ee2ff5e3b1fc7b86752452e9a5f7edbea9b1d3944b7e31c0c96142c724` | 2026-10-28T17:04:27Z | **KILLED** | red-exit-cell |
| head | m6-drop-routed | clause 4: drop the routed-id check | 1 | 16 | 1 | `04ba0d90b3796cf89a4eb114385b2396947a91b9c1ba6c75ae73d78f79e83a92` | 2026-10-28T17:04:28Z | **KILLED** | red-routed-id-missing |
| head | m7-vocab-whole-row | clause 4: vocabulary matched by substring over the whole row, not the arm cell | 0 | 16 | 0 | `2ab82b91ec73ab3b7215d11b1cd30face3776126f019bb28a31d342e68663ea8` | 2026-10-28T17:04:28Z | **SURVIVED** | — |
| head | m8-pin-by-length | clause 6: sha256 pin compared by length only | 1 | 16 | 2 | `85e0eb2b00be002646065be35cabc1d108afb3b968f1b9dfbad85cd7be288b66` | 2026-10-28T17:04:28Z | **KILLED** | red-pin-mismatch, green-with-battery |
| head | m9-drop-allowlist | clause 5: citations outside the validated path set accepted | 0 | 16 | 0 | `0bf8f4c6ae0e46a0c4f00b9eb8b573afd7c10b0bbb6bf7e2ce58e7c2c5296dd8` | 2026-10-28T17:04:29Z | **SURVIVED** | — |
