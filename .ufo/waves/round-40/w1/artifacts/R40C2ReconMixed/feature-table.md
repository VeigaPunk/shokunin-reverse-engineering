# R40C2ReconMixed -- development-run feature table

Every row is a `feat.py` read of a saved REA 6.5.0 `extract-firmware` envelope under
`envelopes/<run>/envelope.json`; `v2A label`/`v2A action` are the `ordercheck.py --table A`
decisions for the proposed v2 row order. `-` is the empty set; `n/a` means no sasquatch
command was recorded. All runs: `operation=extract_firmware`, `provider.id=unblob`,
`provider.version=26.6.4`.

| run | arm | carrier | endian | comp | tree links | H | G | D | BE | SR | P | chunk failed | unpub kinds | diagnostics | v2A label | v2A action | carrier sha256[:16] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dironly-after | after | dironly | be | gzip | - | squashfs_v4_be | - | - | n/a | no | 0 | [False] | - | - | clean-empty | ignore-benign | 65886123f5e2e223 |
| esc-le-after | after | esc-le | le | gzip | esc | squashfs_v4_le | - | - | n/a | yes | 2 | [False] | - | MaliciousSymlinkRemoved | escaping-symlink-removed | expect-absent | 77256c877cf647c8 |
| intree-le-after | after | intree-le | le | gzip | d1/ini | squashfs_v4_le | unpublished-entry | - | n/a | no | 2 | [False] | symlink | - | in-tree-symlink-metadata | ignore-benign | 545e7c4945491b34 |
| mx-nofiles-after | after | mx-nofiles | be | gzip | esc,in | squashfs_v4_be | unpublished-entry | - | n/a | yes | 0 | [False] | symlink | MaliciousSymlinkRemoved | unclassified | none | 1374042b2f0c9e2a |
| mx1-after | after | mx1 | be | gzip | esc,d1/ini | squashfs_v4_be | unpublished-entry | - | n/a | yes | 3 | [False] | symlink | MaliciousSymlinkRemoved | mixed-symlinks | expect-absent-metadata | 33de8689514b2b42 |
| mx1-avm-after | after | mx1-avm | avm | gzip | esc,d1/ini | squashfs_v4_be | extractor-failure | - | no | no | 0 | [True] | - | ExtractCommandFailedReport | avm-marker-be-dropped | repin-marker | 855b47029838ad0f |
| mx1-badminor-after | after | mx1-badminor | be | gzip | esc,d1/ini | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | - | ExtractCommandFailedReport | body-extractor-failure | rerun-fresh | bf43b58105e57063 |
| mx1-before | before | mx1 | be | gzip | esc,d1/ini | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | [True] | - | ExtractorDependencyNotFoundReport | dep-missing-be | install-extractor | 33de8689514b2b42 |
| mx1-idtable-after | after | mx1-idtable | be | gzip | esc,d1/ini | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | - | ExtractCommandFailedReport | body-extractor-failure | rerun-fresh | 89feba7b7f392e2a |
| mx2-after | after | mx2 | be | xz | d1/up,d2/i1 | squashfs_v4_be | unpublished-entry | - | n/a | yes | 3 | [False] | symlink | MaliciousSymlinkRemoved | mixed-symlinks | expect-absent-metadata | 403172582bee286c |
| mx3-after | after | mx3 | be | gzip | e1,e2,d2/i1,d2/i2 | squashfs_v4_be | unpublished-entry | - | n/a | yes | 4 | [False] | symlink | MaliciousSymlinkRemoved,MaliciousSymlinkRemoved | mixed-symlinks | expect-absent-metadata | 8638e7e1ee5b5f08 |
| mx4-after | after | mx4 | le | gzip | esc,d1/ini | squashfs_v4_le | unpublished-entry | - | n/a | yes | 3 | [False] | symlink | MaliciousSymlinkRemoved | mixed-symlinks | expect-absent-metadata | 719c78a316e6194f |
| mx4-before | before | mx4 | le | gzip | esc,d1/ini | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | [True] | - | ExtractorDependencyNotFoundReport | dep-missing-le | install-extractor | 719c78a316e6194f |
| mx4-idtable-after | after | mx4-idtable | le | gzip | esc,d1/ini | squashfs_v4_le | extractor-failure | - | no | no | 0 | [True] | - | ExtractCommandFailedReport | unclassified | none | b37be52adb58e35e |
| mx5-after | after | mx5 | le | xz | d1/up,d2/i1 | squashfs_v4_le | unpublished-entry | - | n/a | yes | 3 | [False] | symlink | MaliciousSymlinkRemoved | mixed-symlinks | expect-absent-metadata | 090290eb4f74aca9 |
| mx6-after | after | mx6 | le | gzip | e1,e2,d2/i1,d2/i2 | squashfs_v4_le | unpublished-entry | - | n/a | yes | 4 | [False] | symlink | MaliciousSymlinkRemoved,MaliciousSymlinkRemoved | mixed-symlinks | expect-absent-metadata | f9c77752e3479eab |
| mx7-trunc-after | after | mx7-trunc | be | gzip | esc,d1/ini | - | - | - | n/a | no | 0 | [] | - | - | no-squashfs-chunk | inspect-chunk | add06b847b111ed1 |
| mx7-trunc2-after | after | mx7-trunc2 | be | gzip | esc,d1/ini | - | - | - | n/a | no | 0 | [] | - | - | no-squashfs-chunk | inspect-chunk | 07aaf15537fc8935 |
| mx7-zerofirst-after | after | mx7-zerofirst | be | gzip | esc,d1/ini | squashfs_v4_be | unpublished-entry | - | n/a | yes | 3 | [False] | symlink | MaliciousSymlinkRemoved | mixed-symlinks | expect-absent-metadata | 05b9ebde1dd114be |
| mx8-flip-after | after | mx8-flip | be | gzip | esc,d1/ini | squashfs_v4_be | extractor-failure | - | yes | no | 0 | [True] | - | ExtractCommandFailedReport | body-extractor-failure | rerun-fresh | 01ec75d169733037 |
| mx8-zerofirst-after | after | mx8-zerofirst | be | gzip | esc,d1/ini | squashfs_v4_be | extractor-failure,unpublished-entry | - | yes | yes | 3 | [True] | symlink | ExtractCommandFailedReport,MaliciousSymlinkRemoved | unclassified | none | d74badaef3e3d704 |

`dironly` is the zero-file (clean-empty) vector: one empty directory, so the REA envelope has
H=`squashfs_v4_be`, G=`-`, BE=`n/a`, SR=`no`, P=`0`. `mx-nofiles` is the mixed vector with zero
regular files (one escaping, one in-tree link): G=`unpublished-entry`, SR=`yes`, P=`0`, which no
row owns. The bare-root `clean-empty` carrier was built but never run: the writer encodes it with
a zero-length metadata block that `tools/round-39/sqfs-list.py` refuses (exit 2).
