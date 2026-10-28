### Core 13

| # | mutation | category | v3 exit | v2 exit | detected by (v3 clause) |
|---|---|---|---|---|---|
| 1 | `token-substring` | token | 1 | 0 | c5 |
| 2 | `token-synonym` | token | 1 | 0 | c5 |
| 3 | `id-duplicate-row` | id | 1 | 0 | c3,c4 |
| 4 | `id-two-per-cell` | id | 1 | 0 | c3,c4 |
| 5 | `cells-five` | cells | 1 | 0 | c3 |
| 6 | `exit-out-of-range` | exit | 1 | 1 | c3 |
| 7 | `title-unnumbered` | title | 1 | 0 | c1 |
| 8 | `marker-duplicated` | marker | 1 | 0 | c1 |
| 9 | `header-reordered` | header | 1 | 0 | c2 |
| 10 | `digest-stale` | digest | 1 | 0 | c6 |
| 11 | `pin-mismatch` | pin | 1 | 0 | c8 |
| 12 | `refs-no-selector` | refs | 1 | 0 | c8 |
| 13 | `refs-must-cite-missing` | refs | 1 | 0 | c8 |

### Supplementary 27

| # | mutation | category | v3 exit | v2 exit | detected by (v3 clause) |
|---|---|---|---|---|---|
| 1 | `exit-semantics-0` | exit | 0 | 0 | **none — survives** |
| 2 | `hole-cell-empty` | cells | 0 | 0 | **none — survives** |
| 3 | `arm-permuted` | token | 0 | 0 | **none — survives** |
| 4 | `id-permuted` | id | 0 | 0 | **none — survives** |
| 5 | `id-substituted-unrouted` | id | 1 | 1 | c4 |
| 6 | `cells-three` | cells | 1 | 1 | c3,c5 |
| 7 | `marker-missing` | marker | 1 | 1 | c1 |
| 8 | `header-renamed` | header | 1 | 1 | c2 |
| 9 | `digest-absent` | digest | 1 | 0 | c6 |
| 10 | `pin-absent` | pin | 1 | 0 | c8 |
| 11 | `title-renumbered` | title | 1 | 0 | c1 |
| 12 | `mutation-name-extra` | digest | 0 | 0 | **none — survives** |
| 13 | `refs-outside-allowlist` | refs | 1 | 1 | c8 |
| 14 | `refs-unresolvable-line` | refs | 1 | 1 | c8 |
| 15 | `refs-two` | refs | 0 | 0 | **none — survives** |
| 16 | `digest-reordered` | digest | 1 | 0 | c6 |
| 17 | `mutation-name-dropped` | digest | 1 | 0 | c6 |
| 18 | `flag-order-swapped` | digest | 1 | 0 | c7 |
| 19 | `header-extra-cell` | header | 1 | 0 | c2 |
| 20 | `arm-token-case` | token | 1 | 0 | c5 |
| 21 | `self-ref-line-past-eof` | refs | 0 | 0 | **none — survives** |
| 22 | `refs-only-self` | refs | 0 | 0 | **none — survives** |
| 23 | `composite-block23-relabelled` | composite | 1 | 1 | c2,c3,c4,c5,c6,c8 |
| 24 | `rows-three` | cells | 1 | 1 | c3,c4 |
| 25 | `arm-all-order` | token | 0 | 0 | **none — survives** |
| 26 | `arm-duplicate-symbol` | token | 0 | 0 | **none — survives** |
| 27 | `exit-all-two` | exit | 0 | 0 | **none — survives** |

### Full failing text

| mutation | v3 failing | v2 failing |
|---|---|---|
| `token-substring` | ["arm cells not exact vocabulary tokens: ['order-ish', 'order-ish', 'order-ish', 'order-ish']"] | [] |
| `token-synonym` | ["arm cells not exact vocabulary tokens: ['symbolic', 'once', 'digest', 'order']"] | [] |
| `id-duplicate-row` | ['rows 5 != 4', "routed cardinality {'R46-CL2': 2, 'R46-CL3': 1, 'R46-CL4': 1, 'R46-CL6': 1} != each of ['R46-CL2', 'R46-CL3', 'R46-CL4', 'R46-CL6'] exactly once"] | [] |
| `id-two-per-cell` | ['rows naming != 1 routed id: [0]', "routed cardinality {'R46-CL2': 1, 'R46-CL3': 2, 'R46-CL4': 1, 'R46-CL6': 1} != each of ['R46-CL2', 'R46-CL3', 'R46-CL4', 'R46-CL6'] exactly once"] | [] |
| `cells-five` | ['a row does not have exactly 4 cells'] | [] |
| `exit-out-of-range` | ['exit cells outside {0,1,2}: 1'] | ['exit cells outside {0,1,2}: 1'] |
| `title-unnumbered` | ["marker block title does not start with '24. '"] | [] |
| `marker-duplicated` | ['marker_occurrences 2 != 1'] | [] |
| `header-reordered` | ["header ['exit', 'v3 arm', 'v2 hole', 'trigger'] != ['trigger', 'v2 hole', 'v3 arm', 'exit']"] | [] |
| `digest-stale` | ["mutations_sha256 does not match the counter's own mutation list"] | [] |
| `pin-mismatch` | ['interpreter sha256 pin does not match the bytes at rev'] | [] |
| `refs-no-selector` | ['unresolved or unvalidated citations: 1'] | [] |
| `refs-must-cite-missing` | ['does not cite corpus/lessons/round-46.md'] | [] |
| `exit-semantics-0` | [] | [] |
| `hole-cell-empty` | [] | [] |
| `arm-permuted` | [] | [] |
| `id-permuted` | [] | [] |
| `id-substituted-unrouted` | ["routed cardinality {'R46-CL2': 1, 'R46-CL3': 1, 'R46-CL4': 1, 'R46-CL7': 1} != each of ['R46-CL2', 'R46-CL3', 'R46-CL4', 'R46-CL6'] exactly once"] | ["routed ids not named by any row: ['R46-CL6']"] |
| `cells-three` | ['a row does not have exactly 4 cells', 'exit cells outside {0,1,2}: 1', "arm cells not exact vocabulary tokens: ['symbol', 'once', '1', 'order']"] | ['exit cells outside {0,1,2}: 1', 'arm cells outside the vocabulary'] |
| `marker-missing` | ['marker_occurrences 0 != 1', 'marker_block_count 0 != 1'] | ['marker_block_count 0'] |
| `header-renamed` | ["header ['trigger', 'v2 hole', 'arm', 'exit'] != ['trigger', 'v2 hole', 'v3 arm', 'exit']"] | ["header ['trigger', 'v2 hole', 'arm', 'exit'] != ['trigger', 'v2 hole', 'v3 arm', 'exit']"] |
| `digest-absent` | ["mutations_sha256 does not match the counter's own mutation list"] | [] |
| `pin-absent` | ['interpreter sha256 pin does not match the bytes at rev'] | [] |
| `title-renumbered` | ["marker block title does not start with '24. '"] | [] |
| `mutation-name-extra` | [] | [] |
| `refs-outside-allowlist` | ['unresolved or unvalidated citations: 1'] | ['unresolved or unvalidated citations: 1'] |
| `refs-unresolvable-line` | ['unresolved or unvalidated citations: 1'] | ['unresolved or unvalidated citations: 1'] |
| `refs-two` | [] | [] |
| `digest-reordered` | ["mutations_sha256 does not match the counter's own mutation list"] | [] |
| `mutation-name-dropped` | ["mutation names not stated in the block: ['stale-mutations-digest']"] | [] |
| `flag-order-swapped` | ['gate.py flag order: 0 correct, 1 reversed'] | [] |
| `header-extra-cell` | ["header ['trigger', 'v2 hole', 'v3 arm', 'exit', 'note'] != ['trigger', 'v2 hole', 'v3 arm', 'exit']"] | [] |
| `arm-token-case` | ["arm cells not exact vocabulary tokens: ['Symbol', 'once', 'digest', 'order']"] | [] |
| `self-ref-line-past-eof` | [] | [] |
| `refs-only-self` | [] | [] |
| `composite-block23-relabelled` | ["header ['trigger', 'v1 hole', 'v2 arm', 'exit'] != ['trigger', 'v2 hole', 'v3 arm', 'exit']", 'rows 13 != 4', 'rows naming != 1 routed id: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]', "routed cardinality {} != each of ['R46-CL2', 'R46-CL3', 'R46-CL4', 'R46-CL6'] exactly once", 'arm cells not exact vocabulary tokens: [\'presence: `absent_at_rev` is computed from the census, never from the row\', \'merge: `--diff-merges=first-parent` plus an independent blob arm; the two must agree\', \'rows: the selftest carries one red case per clause, and the mutation list is named in the claim\', \'refs: every citation carries a line selector and a path inside the validated set; the interpreter is identified by its sha pin instead\', \'rows: every row names a routed id and an arm from the fixed vocabulary, so a garbage row fails\', \'marker: rows register only between the two registry markers and outside fences and comments\', \'dirty: the dirty scope is the union of the pathspecs, and each arm has a red case that names it\', \'restored: one frozen set derived from the claims file feeds both arms, so the sets cannot differ\', \'none: the blob arm compares the two revisions and a squash leaves both trees identical, so the gate returns 0 and this row states the limit instead of pretending to see it\', \'output: `scratch()` refuses a temporary partition and returns could-not-evaluate instead of degrading\', \'output: `out_path()` refuses any target inside the graded or frozen set and any path outside the lane root\', \'commit: the history arm reads `--name-status -z`, so pathnames are not munged and the comparison is byte-exact\', "pin: the block carries the interpreter\'s sha256, so a prose claim and the bytes it describes cannot diverge silently"]', "mutations_sha256 does not match the counter's own mutation list", "mutation names not stated in the block: ['substring-arm', 'duplicate-routed-id', 'stale-mutations-digest', 'flag-order-drift']", 'unresolved or unvalidated citations: 2', 'interpreter sha256 pin does not match the bytes at rev'] | ["header ['trigger', 'v1 hole', 'v2 arm', 'exit'] != ['trigger', 'v2 hole', 'v3 arm', 'exit']", "routed ids not named by any row: ['R46-CL2', 'R46-CL3', 'R46-CL4', 'R46-CL6']", 'arm cells outside the vocabulary', 'unresolved or unvalidated citations: 2'] |
| `rows-three` | ['rows 3 != 4', "routed cardinality {'R46-CL2': 1, 'R46-CL3': 1, 'R46-CL4': 1} != each of ['R46-CL2', 'R46-CL3', 'R46-CL4', 'R46-CL6'] exactly once"] | ['rows 3 < 4', "routed ids not named by any row: ['R46-CL6']"] |
| `arm-all-order` | [] | [] |
| `arm-duplicate-symbol` | [] | [] |
| `exit-all-two` | [] | [] |
