- **24. An exact binding is an equality over one token, one id, one digest and one flag order.** <!-- exactness-table v3 --> The round-46 non-author spot-check routed four instrument defects (R46-CL2, R46-CL3, R46-CL4, R46-CL6); each row states the loose binding that let the defect through, the exact arm that now fails it, and the exit the counter returns when the arm fires. Interpreter `tools/round-47/exact.py` `interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`; the mutation list is pinned by `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` over substring-arm, duplicate-routed-id, stale-mutations-digest, flag-order-drift in that order, so deleting a mutation changes the printed digest. All four forged fixtures exit 1 under v3 and 0 under the ported v2 profile, so the arms are measured, not asserted.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` | the arm-vocabulary check is a lowercased substring test, so any word carrying the token passes | symbol | 1 |
| R46-CL3 a row claims a routed id it does not address | every id need only appear in some row, never exactly once | once | 1 |
| R46-CL4 a deleted mutation changes the denominator | the list is counted but never pinned, so a deletion fails no clause | digest | 1 |
| R46-CL6 one argument reorder blinds the merge arm | `git log --diff-merges=first-parent -m` prints a merge twice, and nothing reads the order | order | 1 |

  Refs: `corpus/lessons/round-46.md:57-59` (R46-CL2, the substring arm), `corpus/lessons/round-46.md:60-62` (R46-CL3, the at-least-once id), `corpus/lessons/round-46.md:63-64` (R46-CL4, the unpinned list), `corpus/lessons/round-46.md:65-70` (R46-CL6, the order-sensitive arm), `corpus/lessons/round-46.md:21` (M46-2, why the list needs a digest), `plans/round-47-claims.md:68-90` (the predicate these rows are scored by).
