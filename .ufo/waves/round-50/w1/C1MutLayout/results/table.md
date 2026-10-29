| id | mutation (clause) | mutant sha256 (16) | selftest exit | status | first failing case / note |
|---|---|---|---|---|---|
| M00 | control: unmutated round-41 counter | bbabbfecb229e899 | 0 | SURVIVED | control, unmutated copy of base blob bbabbfec |
| M01 | magic: accept hsqs as BE magic | 935e61d3c1a5a862 | 1 | KILLED | killed by: little-endian superblock magic: want 1 got 0 |
| M02 | magic: no magic test | e2025cd068c92238 | 1 | KILLED | killed by: little-endian superblock magic: want 1 got 0 |
| M03 | s_major/s_minor: version test drops minor | dc8f1f265a4354b9 | 0 | SURVIVED | SURVIVED: no fixture with minor != 0; add layout case version 4.1 -> layout red |
| M04 | s_minor: wrong superblock offset | 0963977348c4a16a | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M05 | compression id: little-endian read | 065751f3ca8e1446 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M06 | compression id: XZ set widened to 3,5 | 376c773e4f33ce1a | 0 | SURVIVED | SURVIVED: round-41 counter never gates compression id (only binding compression_coverage); port must test compression == 4 exactly; add ids 2,3,5 red cases |
| M07 | compression id: GZIP id aliased to xz 4 | 82e5efc28367e1ae | 1 | KILLED | killed by: no xz carrier (compression coverage): want 1 got 0 |
| M08 | mkfs_time==bytes_used: >= instead of == | a69aea08c4c15f1b | 1 | KILLED | killed by: marker-stripped genuine-LE-lengths carrier: want 1 got 0 |
| M09 | mkfs_time: little-endian read | 5b0593e7e4ebdbd1 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M10 | bytes_used sanity: admits 4 KiB past EOF | 9facffcf12aa5871 | 0 | SURVIVED | SURVIVED: only bytes_used=0xFFFFFFF0 tested; add bytes_used = len(raw)+1 layout probe case |
| M11 | metadata cap widened 8192->65536 | fee9fe70f9c98192 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M12 | length endianness: identity branch ignores BE identity | 26404c45281b2066 | 0 | SURVIVED | SURVIVED: no fixture with le_identity and be_identity both true; add that case -> must be ambiguous (layout red) |
| M13 | length endianness: plausibility branch ignores BE plausibility | a525ef3d259f77d9 | 1 | KILLED | killed by: metadata length plausible both ways (no identity): want 1 got 0 |
| M14 | length endianness: uncompressed flag mask wrong | 4756829f5bdd2bc0 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M15 | handler name: any squashfs_v4* accepted | 1e02890e6760ef85 | 1 | KILLED | killed by: chunk handler is the LE handler: want failing clause 'handler_ok', failing=['projection_ok'] |
| M16 | handler name: only first chunk inspected | cdcca69cec40b15d | 1 | KILLED | killed by: padded carrier: the oracle resolves under the portion chunk directory: want 0 got 1 |
| M17 | extract-root mapping: suffix match (R40-CL1 regression) | e32f56421756dace | 1 | KILLED | killed by: probe 'dir 1: regular usr/bin/busy vs symlink entry bin/busy': exact matcher True, want False |
| M18 | extract-root mapping: root prefix from first segment only | ee5b6aee4d7c97d3 | 1 | KILLED | killed by: padded carrier: the oracle resolves under the portion chunk directory: want 0 got 1 |
| M19 | removal disposition: entry-kind check dropped | e82fe81740c05206 | 1 | KILLED | killed by: a removal naming a row of an unlisted kind fails: want 1 got 0 |
| M20 | removal disposition: gapped-and-removed check dropped | f07d7dacfd4375be | 1 | KILLED | killed by: an entry cannot be both gapped and removed: want 1 got 0 |
| M21 | removal disposition: silent row with no detail admitted | b287e1b4eba3998a | 0 | SURVIVED | SURVIVED: no silent-rule row lacking a third column; add `bin/x\tsymlink\n` under silent empty-target -> gaps_ok red |
| M22 | rerun projection: diagnostics key dropped from core profile | 3975a6514fc70e2e | 1 | KILLED | killed by: fabrication differing only in the diagnostics multiset: want 1 got 0 |
| M23 | rerun projection: verdict forced true | 52eb39f3bf0055e3 | 1 | KILLED | killed by: oracle-only fabrication with re-minted evidence id: want failing clause 'projection_ok', failin |
| M24 | evidence id: recomputed-equality dropped | 4f9bd46812969f16 | 1 | KILLED | killed by: evidence id stale after an edit: want failing clause 'evidence_id_ok', failing=['projection_ok' |
| M25 | evidence id: ev_ prefix test dropped (expected equivalent) | b9f2d993e5e93453 | 0 | SURVIVED | SURVIVED, equivalent [INFERENCE]: xpin emits ev_-prefixed ids; prefix test redundant |
| M26 | target constant 4->3 | aa120c791047c5b5 | 1 | KILLED | killed by: spec probe 'external carrier with a member_sha256': ok=False want True (problems ['carriers has |
| M27 | target comparison loosened to >= target-1 | 0b3fb5269f67d553 | 1 | KILLED | killed by: receipt missing (V4): want 1 got 0 |
| M28 | freeze walk: rename detection not disabled | 2dd800aa898b498e | 0 | SURVIVED | SURVIVED, selftest gap (code correct): drop of --no-renames hides a rename of a frozen path; add post-freeze git mv case -> exit 2 |
| M29 | freeze walk: nonregular table not a frozen path | c0211ae364a58042 | 1 | KILLED | killed by: nonregular table changed after freeze: want 2 got 1 |
| M30 | freeze walk: range includes the freeze commit | 34c0c9847689a715 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 2 (unevaluable) |
| M31 | freeze walk: carriers_unchanged forced true | 09ae1e002b9b8567 | 0 | SURVIVED | SURVIVED, redundant guard: frozen_drift already raises for carriers.json edits; still untested |
| M32 | carrier_fresh_ok: prior pins ignored | af2bb3dee781a50b | 1 | KILLED | killed by: relabelled previous-round pins (prior_pins): want 1 got 0 |
| M33 | provenance: .. climb not refused | 94b5170c5a6c14db | 1 | KILLED | killed by: provenance path climbs out with ..: want 1 got 0 |
| M34 | carve_ok: file-size equality dropped | 3738bbde1afb6257 | 0 | SURVIVED | SURVIVED: external-branch carve only; add external carrier with trailing bytes past frozen length == bytes_used |
| M35 | carrier_pin_ok: sha256 comparison dropped | 200a813a2dae7acd | 1 | KILLED | killed by: frozen pin wrong (carrier untouched): want failing clause 'carrier_pin_ok', failing=['subject_p |
| M36 | receipt_fresh: freeze itself accepted as first add | ac6212e925db9457 | 1 | KILLED | killed by: receipt added at freeze: want 1 got 0 |
| M37 | receipt_fresh: first_add without --diff-filter=A | f05c892d59e77d21 | 0 | SURVIVED | SURVIVED, equivalent [INFERENCE]: oldest commit touching a path is its add; --diff-filter=A redundant |
| M38 | chunks_ok forced true | 3e84f47847bc42b9 | 1 | KILLED | killed by: failed chunk: want failing clause 'chunks_ok', failing=['projection_ok'] |
| M39 | CLAUSES tuple drops layout_ok | 38509a39ed8e2190 | 1 | KILLED | killed by: marker-stripped genuine-LE-lengths carrier: want 1 got 0 |
| M40 | CLAUSES tuple drops projection_ok (rerun clause unconjoined) | 1d3cc8f8ca59ef7c | 1 | KILLED | killed by: oracle-only fabrication with re-minted evidence id: want failing clause 'projection_ok', failin |
| M41 | CLAUSES tuple drops evidence_id_ok | 432b75331ad8a6ac | 1 | KILLED | killed by: evidence id stale after an edit: want failing clause 'evidence_id_ok', failing=['projection_ok' |
| M42 | provenance: scratch segment test dropped | b3b2abcaefb3e0c0 | 1 | KILLED | killed by: foreign scratch provenance (/kaidoku-r39/): want 1 got 0 |
| M43 | nonregular_unpublished_ok: root-known test dropped | b001903ba04e79cf | 0 | SURVIVED | SURVIVED, clause-level only: nonregular_unpublished_ok True when root unknown; conjunction still red via oracle_hits_ok |
| M44 | oracle_hits equality loosened to one missing file | d855b7c42dc08e2e | 1 | KILLED | killed by: oracle file missing from the published set: want failing clause 'oracle_hits_ok', failing=['pro |
| M45 | operation_ok: operation/provider test dropped | 6bac7aff728fec2f | 1 | KILLED | killed by: wrong operation (extract_filesystem): want 1 got 0 |
| M46 | layout_ok ORs the BE magic (loosened gate) | af52f032f3dbe5b6 | 1 | KILLED | killed by: marker-stripped genuine-LE-lengths carrier: want 1 got 0 |
| M47 | layout probe: bytes_used sanity branch skipped | 951d16cb5c948859 | 1 | KILLED | killed by: bytes_used beyond the file: want failing clause 'layout_ok', failing=['carve_ok'] |
| M48 | carrier_present forced true | 4bda7e05d33ec91c | 1 | KILLED | killed by: carrier listed but never committed: want failing clause 'carrier_present', failing=['carrier_pi |
