| scenario | counter exit | carriers_matched | failing clauses per carrier (v1le / v1be / v2le / v2be) | counter stdout sha256 | counter json sha256 |
|---|---|---|---|---|---|
| BASE | 1 | 4 | - / - / - / - | `8fa73e4cabdee31e4e9ae7d46311902824f0483ff4a0743cd39b7777f72f6474` | `09a5401a4a1c9cb28c184e00f3d334c376cd0afdccb7bc2fd0063469db4d56f3` |
| S1_rea_outdir_evidence | 1 | 4 | - / - / - / - | `dbc204153700aa6413e0587611b00c3213d0c3c20488e0eca887a458b8b6e1a1` | `42f190fb705cd8c5350ea1253ee90c5c1e6210de4e6bfbe38a9e6468c528fbb5` |
| S2_scratch_base_named_kaidoku-r44 | 1 | 4 | - / - / - / - | `6b371df0d98b5d4037a712412086886258750f6a8e128b3b9dc501b08bce10c4` | `fad201911cbeecc35f572c24c9fb4008bb592114517efdc64c1d6e876f8deee1` |
| S3_segment_code_kaidoku-r44 | 1 | 4 | - / - / - / - | `ba4ea77abc3c6518ad550114d4300c162d87bb3d205c67cfd7405d5ddcf35ecc` | `cf5c39923bc2e6ddfc3f5c47e782c8b4e9da8e799e4c3c936ff9f02dcb717ee1` |
| S4_prefreeze_lane_rev_at_run | 1 | 4 | - / - / - / - | `f8548bbc38d60948b7c5f44f560ced2ae4e280e0c663e973900ce5d93df973a4` | `5ee7b0a0ed3a8bdc4460a826cd5224052d3112d16666590945e194d9ae53f357` |
| S5_replay_fake_rea | 1 | 4 | - / - / - / - | `359cf5b43da4692fa747e51dc4767382e7cc90d5f3c6fcdcb6da17dfdf005f8a` | `d52b71204d8bc20cf5e70836be7365da71399d649a7279e0a6091331275ba799` |
| P1_drop_provenance_json | 1 | 4 | - / - / - / - | `38faa777efeb4c128827ebaf5b844d6ec4cf379dbb5e20e74c43b0a0bcc644ea` | `2e34ac9c0005644b277bda2cdaf55861eae0ce66dbd9564a787f141f2e712b46` |
| P2_provenance_lies_evidence_path | 1 | 4 | - / - / - / - | `d2468730bc178b329d6ef9b9d3f80641e05b9d804f5c7c2ae4b87c2cbdde9ed4` | `0142c7cf75ed9fe24886441dd165438cd9a20550088c674b551d8d85e2250acb` |
| P3_run_json_rev_at_run_zeros | 1 | 4 | - / - / - / - | `5c88a83d5895986035c9424bc48cc2650f03f440941ebb5fa02f73b98504b689` | `ecb2733769b18fa99478b077521d2c787cd78173642221aa85af0773eb0b5cf2` |
| P4_drop_run_json | 1 | 4 | - / - / - / - | `7301edd5ec91bab4eec988d7b178d201bac101ceca7452d2f91ed8fa34e654ee` | `ee98680a246b0fc6260055da52dd9de7c010bd0abd096790b901584a8d48506e` |
| P5_tamper_verbatim_tree_byte | 1 | 4 | - / - / - / - | `5e4e50c41c9e6e74b9c9cdfb21744c18a8de3870333188c8d5bdf2b40a87ee97` | `ff08a40803d8685042fa35a88bff89225c18ecfb02fb779082a50faef2e4c89d` |
| P6_remove_verbatim_tree | 1 | 4 | - / - / - / - | `90a55a62f18fce94a7363749b588ba763434c120f166950942524befedbaec81` | `51959fdb93dd2c95e1ddc48271c5073da54a5b5f02598373c5fae3af452d7ffd` |
| P7_drop_extract_env_and_unblob_log | 1 | 4 | - / - / - / - | `e53361721b9562cf88e56c2c24a97312f4facd7efd757994b08c826db0db1429` | `7918ed3110d974fe085c866b6b4b3a3892c99bd98866bb26249537b09753b17d` |
| P8_tamper_envelope_and_stdout | 1 | 4 | - / - / - / - | `47cc81fb62a8ecf96e2de59e94a2866037ff409e28b8264974409af254386a7b` | `2bed94e2da8d576cd41c9b12db5a6677503eea8237ca750bd363f12874aa243e` |
| P9_outdir_evidence_path_remint | 1 | 0 | run_provenance_ok / run_provenance_ok / run_provenance_ok / run_provenance_ok | `2d7a0a98785612d2e43bd4fd0ac7de347bb8af102908febf41c376d8e4bad259` | `c350ce3496442d49a6249138eb206a2c252d847c5e2d964c9c6ead47c1e471e4` |
| P10_outdir_evidence_path_no_remint | 1 | 0 | run_provenance_ok,evidence_id_ok / run_provenance_ok,evidence_id_ok / run_provenance_ok,evidence_id_ok / run_provenance_ok,evidence_id_ok | `77bbc18d3bfa24d980ed8b468d5702730a182f0862b937224de2d3e0bf1a22b0` | `ab2a2713939f4fe73046c8fa5a2e81c3854c21fa1e0654427fc6c591c3e2ccb6` |
| P11_outdir_forged_scratch_remint | 1 | 4 | - / - / - / - | `248b1d5dd831ac95f9dff1d5b166ebd9b71d1f7f45a77dbe3562c0c64aa9f94b` | `49fb148edb5550dc9fdca2d5fb6655f0fdd17619c5a4fc3c3968c76f8d5bb8ca` |
| P12_outdir_tmp_string_segment_remint | 1 | 4 | - / - / - / - | `5db5ed6dbe073074fca090ebfa984e9a4cbda64688f7354cc21e21c924038325` | `04f0aad5fb30368e978f09a02eff50298c05a7c0ccb7df8890bebe7aa950ed49` |
| P13_content_forged_remint | 1 | 3 | oracle_hits_ok,projection_ok / - / - / - | `5b03c6f0b91645a7769fb7b51579cc7b22b5c6cf3176f250580926e8d532b2e3` | `7a4976aa40678c7a1196deeea0d8a7ae146bdfa814e6bcaa0ddcf7eaab985869` |
| P14_outdir_kaidoku_r44_only_remint | 1 | 0 | run_provenance_ok / run_provenance_ok / run_provenance_ok / run_provenance_ok | `495d7ce1292e69820048ccea49290950f5645bdfd429b350850c14f7b3b8ceeb` | `b367b318d9ffcdea648e395a64a27256c80042e7bdda2cdfb93f321230d8b86b` |
| P15_outdir_r49_segment_under_r44_remint | 1 | 4 | - / - / - / - | `951964e835c15b2a527964b248b7a86aa2f6303ea61de21a097b7e1ee8757df5` | `056f6f8fb3185e6961db65c04a38cf319fd0f3ced9e28f7a01fc4aa63f1affc6` |
| CTRL_receipt_commit_as_freeze | 1 | 0 | receipt_fresh / receipt_fresh / receipt_fresh / receipt_fresh | `2f91afe5cb627560f76c42b674fb9960a74a060b4049788eb90c06a7aeed993d` | `aec35599480558f80af9855ea3afb1e8fb13ab6c53f5261540a5951ba781e400` |
| P2b_provenance_rea_outdir_lies_evidence | 1 | 4 | - / - / - / - | `c1037eec57b09cba6bf4098552b05499b096bf5727efd4b15e7d49404eadab1b` | `2cc7b32e1c8553bba1009fb2863bb78a8088bd745e370e7972d0e76d0eab59a8` |
