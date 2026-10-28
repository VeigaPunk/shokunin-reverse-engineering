| mutant | selftest (base 47 cases) | selftest exit | mutant counter sha256 | selftest stdout sha256 | controls run on dev-freeze clone (7 controls) | kill_rule | ctl.json sha256 |
|---|---|---|---|---|---|---|---|
| D-carrier_present | SURVIVED | 0 | 3739f52652350491 | 730a2f600b3122fc | NOT caught: 7/7 as_expected | False | a70dd124fe9ee8fd |
| D-carrier_pin_ok | SURVIVED | 0 | ef6af38e4925ec83 | 87cbb8cee901ab43 | NOT caught: 7/7 as_expected | False | 16d4a40ed09a01fa |
| D-carrier_size_ok | SURVIVED | 0 | 647d247f3f370816 | eda652f99799d74a | NOT caught: 7/7 as_expected | False | dd918bd237ab72d8 |
| D-carrier_fresh_ok | SURVIVED | 0 | ad459ca1e5d2f89c | 753d615942ff8387 | NOT caught: 7/7 as_expected | False | 1c07893c03d21b42 |
| D-layout_ok | KILLED | 1 | 772c554b37f2a8b3 | 843ea7db9861a21b | not run (selftest-killed; controls not needed for kill) |  |  |
| D-carve_ok | KILLED | 1 | 2d5edb5dd61ce118 | 7c37a239bacc3968 | not run (selftest-killed; controls not needed for kill) |  |  |
| D-oracle_ok | SURVIVED | 0 | bccfa3b73362f57f | b2e878c9891e63eb | NOT caught: 7/7 as_expected | False | bd3f3065a7b4ec2a |
| D-tree_ok | KILLED | 1 | 39fcc8c3598aee3a | 414bdd7d34a5da3b | not run (selftest-killed; controls not needed for kill) |  |  |
| D-receipt_present | KILLED | 1 | 65d87e83d2deca35 | 6b849f5b206dd181 | not run (selftest-killed; controls not needed for kill) |  |  |
| D-receipt_fresh | KILLED | 1 | b50aaa0cdc533fc6 | 24b1925e878cbf99 | not run (selftest-killed; controls not needed for kill) |  |  |
| D-evidence_envelope_ok | KILLED | 1 | cf483e5a0fd722f3 | 7c2088464acff094 | not run (selftest-killed; controls not needed for kill) |  |  |
| D-subject_pin_ok | KILLED | 1 | 4ae7450e1c454609 | 4d4f92cb89fc2e9a | not run (selftest-killed; controls not needed for kill) |  |  |
| D-operation_ok | SURVIVED | 0 | 3733f889e93ebf87 | 293eeb807853a100 | NOT caught: 7/7 as_expected | False | 375cd3ef7ff85c5b |
| D-handler_ok | KILLED | 1 | 0501b47baa4d0cd2 | fe9d1fdbfbd2a2e8 | not run (selftest-killed; controls not needed for kill) |  |  |
| D-chunks_ok | SURVIVED | 0 | e84b8c2437fdef90 | 34d6d2258e262674 | NOT caught: 7/7 as_expected | False | 03faa3cd9dc767b8 |
| D-oracle_hits_ok | KILLED | 1 | 7ea7b94231c352dc | 045c6bb464977037 | not run (selftest-killed; controls not needed for kill) |  |  |
| D-gaps_ok | KILLED | 1 | 296612f42ee55d30 | 2a43a838bd5c1a4c | not run (selftest-killed; controls not needed for kill) |  |  |
| D-nonregular_unpublished_ok | SURVIVED | 0 | b043dfa95ba9a75e | bb5237d13762afef | NOT caught: 7/7 as_expected | False | 83db91fc4c37492a |
| D-path_shape_ok | KILLED | 1 | 4ba8179d0b24d792 | 661e4860c18d428a | not run (selftest-killed; controls not needed for kill) |  |  |
| D-run_provenance_ok | KILLED | 1 | d258a2dfb8eac9c1 | b6686233ffec911d | not run (selftest-killed; controls not needed for kill) |  |  |
| D-evidence_id_ok | KILLED | 1 | 50a5ca7cf250fa62 | d08e9342b08fa803 | not run (selftest-killed; controls not needed for kill) |  |  |
| D-projection_ok | KILLED | 1 | 735ed1e8fa6dc313 | 54da3deb67778e37 | not run (selftest-killed; controls not needed for kill) |  |  |
| M01-handler-any | SURVIVED | 0 | 7f9b34110934af9c | c8a218d2e02a21b8 | NOT caught: 7/7 as_expected | False | 4fd328e8c021b9b0 |
| M02-handler-true | KILLED | 1 | 2adffde0989d5831 | 6bd947d465c54e7a | not run (selftest-killed; controls not needed for kill) |  |  |
| M03-oracle-sha-ignored | SURVIVED | 0 | af3d66d8bbcab709 | f299e4aef4c217b5 | NOT caught: 7/7 as_expected | False | d578e0ab4338e377 |
| M04-oracle-size-ignored | SURVIVED | 0 | 94011bbcaade3fcd | cf7dc89276a8e50e | NOT caught: 7/7 as_expected | False | 2873b5b0d467c625 |
| M05-root-naive-prefix | KILLED | 1 | 85d23ab511760aed | d3b24514569e367c | not run (selftest-killed; controls not needed for kill) |  |  |
| M06-projection-true | KILLED | 1 | edce0c8b44e1f0ac | 61b6404dd97355c0 | not run (selftest-killed; controls not needed for kill) |  |  |
| M07-rerun-skipped | KILLED | 1 | dd3cec44af3d65f6 | 5ef5fd6f50126bb7 | not run (selftest-killed; controls not needed for kill) |  |  |
| M08-evidence-id-unchecked | KILLED | 1 | 10558f0a18653572 | 2e33285ffa18abf7 | not run (selftest-killed; controls not needed for kill) |  |  |
| M09-freeze-drift-off | KILLED | 1 | 96014d9a6a9134c9 | 6f685c0cb4244bf9 | not run (selftest-killed; controls not needed for kill) |  |  |
| M10-freeze-prefixes-off | SURVIVED | 0 | 580e93e170c84e0f | c75a927767ec18e9 | NOT caught: 7/7 as_expected | False | 5bbbd38765c608ad |
| M11-freeze-A-ignored | SURVIVED | 0 | b1a43d7b01016705 | 797c7dbcf9e280a4 | NOT caught: 7/7 as_expected | False | 3ccc314de42cea6d |
| M12-freeze-blob-backstop-off | SURVIVED | 0 | 221c47d53337a45a | 8af55caae437c3c0 | NOT caught: 7/7 as_expected | False | 676bf54507488281 |
| M13-sourced-used-by-off | SURVIVED | 0 | 7c3a34d36f54bf18 | 9e4effbb247b922f | NOT caught: 7/7 as_expected | False | bc6fc4be07a7c761 |
| M14-sourced-opened-off | KILLED | 1 | d8caf9ba6c00daf2 | 860bcca99ba6eedc | not run (selftest-killed; controls not needed for kill) |  |  |
| M15-province-row-entry-off | KILLED | 1 | 5f3cb3d2a3500055 | 4e2d89b30d3047c7 | not run (selftest-killed; controls not needed for kill) |  |  |
| M16-frontier-stem-off | SURVIVED | 0 | 5ee303ce118820bc | 6a99414a0e519fe1 | NOT caught: 7/7 as_expected | False | ff8877b5c20f495f |
| M17-frontier-token-off | SURVIVED | 0 | cfe31785b2ed626a | af53d36b995d4884 | NOT caught: 7/7 as_expected | False | 8fe8ad35050a17ea |
| M18-core-row-v2-off | KILLED | 1 | 5daf7eeab9ea6b11 | 0d0b948e8db127e0 | not run (selftest-killed; controls not needed for kill) |  |  |
| M19-coverage-map-off | KILLED | 1 | d2ea197217035e88 | cfbf21c0b9987d7f | not run (selftest-killed; controls not needed for kill) |  |  |
| M20-entry-source-off | KILLED | 1 | ce1d9d28ab05a1ae | dbb5e6da15a5a6f1 | not run (selftest-killed; controls not needed for kill) |  |  |
| M21-magic-check-off | KILLED | 1 | b09758916d674bde | 7546d7101dfc1879 | not run (selftest-killed; controls not needed for kill) |  |  |
| M22-s-minor-off | SURVIVED | 0 | 029d63914e44d6a9 | 95384b5673560359 | NOT caught: 7/7 as_expected | False | c8cf0ffde5542378 |
| M23-s-major-off | KILLED | 1 | 1d0a337c9b919e79 | 86101fb7a3976dad | not run (selftest-killed; controls not needed for kill) |  |  |
| M24-layout-handler-off | SURVIVED | 0 | f78985ba44319ceb | 6a4b9ccd5c6a5834 | NOT caught: 7/7 as_expected | False | ad71f0b2a056262c |
| M25-bytes-used-off | KILLED | 1 | 56c3b37ddc7b44f2 | 004a83a5996cb456 | not run (selftest-killed; controls not needed for kill) |  |  |
| M26-chain-witness-off | KILLED | 1 | c4a3c769058bc14b | 73a47d2bf60847e9 | not run (selftest-killed; controls not needed for kill) |  |  |
| M27-compression-off | SURVIVED | 0 | fbfbf054483bb3ac | b39f6599c09c0a7a | NOT caught: 7/7 as_expected | False | c60feefca71aec66 |
| M28-carve-off | KILLED | 1 | 29c3d8c7d88a8c99 | 30b8112ac4dc9653 | not run (selftest-killed; controls not needed for kill) |  |  |
| M29-chunk-end-nopad | SURVIVED | 0 | 2f5665d200e4e9a4 | f4ea29c96106e902 | CAUGHT: CTL-C1-POS misbehaved | False | 527d583f07199179 |
| M30-tree-check-off | KILLED | 1 | c70dc5b5aeae6232 | 743c2ba786dfaad4 | not run (selftest-killed; controls not needed for kill) |  |  |
| M31-receipt-fresh-add-only | SURVIVED | 0 | d14010a2db2740ba | bc6cabae3142ba1d | NOT caught: 7/7 as_expected | False | 6bc5cddcfb582eff |
| M32-is-ancestor-off | SURVIVED | 0 | 5ca77c9e611b0835 | b3bf3c1ceaef0e54 | NOT caught: 7/7 as_expected | False | 908baa94c2235431 |
| M33-carrier-fresh-off | SURVIVED | 0 | e9cee8d456d94aa2 | 0658800b7bddfc24 | NOT caught: 7/7 as_expected | False | ca81297ac6ba2b9b |
| M34-envelope-counter-key-off | SURVIVED | 0 | ab94ce73fd453b2a | a97247961f27c96c | NOT caught: 7/7 as_expected | False | 3e22089ffa769e9e |
| M35-operation-off | SURVIVED | 0 | 261dabab4b78394b | 1081255395ecfcb1 | NOT caught: 7/7 as_expected | False | d28bd3f024326328 |
| M36-provenance-substring-only | SURVIVED | 0 | 150601451606822d | 33557a9d4ffd0003 | NOT caught: 7/7 as_expected | False | 9efcd2dcd3ff131d |
| M37-target-ge | KILLED | 1 | b08afaf3451701a0 | 1cb7232b9bf0153a | not run (selftest-killed; controls not needed for kill) |  |  |
| M38-gap-structural-1 | KILLED | 1 | ca0cac9d19717187 | 117cbeedfa06e91b | not run (selftest-killed; controls not needed for kill) |  |  |
| M39-gaps-ok-true | KILLED | 1 | b98f97724e41e4f5 | b904ca3ce919b1d2 | not run (selftest-killed; controls not needed for kill) |  |  |
| M40-nonreg-unpub-off | SURVIVED | 0 | 40be858494cd446c | 56a3dfbbd0f42430 | NOT caught: 7/7 as_expected | False | 8c75c76a7f2519b3 |
| M41-shape-off | KILLED | 1 | 898328feaac5a4d9 | 9f014109ac363fa5 | not run (selftest-killed; controls not needed for kill) |  |  |
| M42-subject-off | KILLED | 1 | 16264ef16554b10d | 79e2037dba595f68 | not run (selftest-killed; controls not needed for kill) |  |  |
| M43-chunks-off | SURVIVED | 0 | d349a7b5c8cbc61e | c0ae3558428dd2db | NOT caught: 7/7 as_expected | False | ee66daf0913cea3f |
| M44-carrier-pin-off | SURVIVED | 0 | 71b17dbef0ac6aba | 90b7f8b07b7c0269 | NOT caught: 7/7 as_expected | False | 5fd8171f7ec452bf |
| M45-carrier-size-off | SURVIVED | 0 | 79daf9add3f23a0a | e7a8f054c18e674d | NOT caught: 7/7 as_expected | False | b4a4db4420af4cb5 |
| M46-sb-layout-sanity | SURVIVED | 0 | 8d49047dd7fa6d7b | 2d7cf23a5066d794 | NOT caught: 7/7 as_expected | False | 366bef4eeeb618e1 |
| M47-projection-profile-core | KILLED | 1 | 00587128841103bf | 3ada187ccae15ca1 | not run (selftest-killed; controls not needed for kill) |  |  |
| M48-counter-identity-off | KILLED | 1 | 4d2881c499c48077 | fa8618bd31ceea57 | not run (selftest-killed; controls not needed for kill) |  |  |
| M49-layout-ok-constant | KILLED | 1 | 1bc69cec2b73444f | 518ea8ff5518ff2e | NOT caught: 7/7 as_expected | False | 0aa50d4583bc9a92 |
| M50-freeze-walk-empty | KILLED | 1 | 37327f914bc2e0d3 | bac603f3ad6d0132 | NOT caught: 7/7 as_expected | False | 5bbdbc6528bf34f8 |
| M53-gap-kind-any | SURVIVED | 0 | 5e429d91d1a46d31 | a862ae46007f433b | NOT caught: 7/7 as_expected | False | 0e7770e2c082b7e2 |
| M54-removal-not-exclusive | SURVIVED | 0 | 86b312895b74ede4 | f9a28724322bc101 | NOT caught: 7/7 as_expected | False | f1155db1b5b2c06f |
| M55-disposition-required-off | SURVIVED | 0 | c61dd8aac15083a1 | c282446b31c8af85 | NOT caught: 7/7 as_expected | False | fcb27245df92727c |
