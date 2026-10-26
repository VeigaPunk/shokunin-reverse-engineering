# R41C2Gen seeded factorial family `combo` (dev seed sha256("dev41"))

Factors drawn from `random.Random(int(sha256("<seed>:combo:<k>").hexdigest()[:16],16))`,
independently; the declared tuple is computed from them. `class_expected` is null.

| id | endian | in-tree | escaping | partial | comp | depth | declared G | BE | SR | P | vs named tuples |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | be | 0 | 1 | 1 | gzip | 3 | extractor-failure | yes | yes | nonzero | **outside** |
| C02 | le | 0 | 1 | 0 | gzip | 3 | - | n/a | yes | nonzero | in set |
| C03 | be | 0 | 1 | 1 | gzip | 3 | extractor-failure | yes | yes | nonzero | **outside** |
| C04 | le | 1 | 1 | 1 | gzip | 1 | depth-limited,extractor-failure,unpublished-entry | no | yes | nonzero | **outside** |
| C05 | le | 0 | 1 | 1 | gzip | 1 | depth-limited,extractor-failure | no | yes | nonzero | **outside** |
| C06 | le | 0 | 0 | 1 | gzip | 1 | depth-limited,extractor-failure | no | no | nonzero | in set |
| C07 | be | 0 | 1 | 0 | gzip | 1 | depth-limited | n/a | yes | nonzero | **outside** |
| C08 | be | 0 | 0 | 0 | xz | 1 | depth-limited | n/a | no | nonzero | in set |
| C09 | be | 1 | 1 | 1 | gzip | 3 | extractor-failure,unpublished-entry | yes | yes | nonzero | in set |
| C10 | le | 1 | 0 | 0 | gzip | 3 | unpublished-entry | n/a | no | nonzero | in set |
| C11 | le | 0 | 0 | 1 | gzip | 3 | extractor-failure | no | no | nonzero | **outside** |
| C12 | be | 1 | 1 | 0 | gzip | 3 | unpublished-entry | n/a | yes | nonzero | in set |

6 of 12 combos fall outside the 18 named class tuples; 11 distinct combo tuples.
