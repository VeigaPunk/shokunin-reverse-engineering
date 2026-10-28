| probe | bytes | exit | stdout sha256 | utc | verdict |
|---|---|---|---|---|---|
| `3_c1_vacuous` | current@22fd0d6b | 0 | `34cfb2225fd3aabeae2ef7a15ae402796514cd1c1012a37c343f4ae48add447f` | 2026-10-28T17:11:53Z | clean |
| `4_c1_decoy_section` | current@22fd0d6b | 0 | `1f9893e5c4c18bf330166d1ee3f994d1ea0c41120e0ad9c27dad11558678fe6e` | 2026-10-28T17:11:53Z | clean |
| `5_c2_fabricated_census` | current@22fd0d6b | 0 | `44c6e0af80961f3932c483d194f687249fa833a97d220aeacf094d86decc4da5` | 2026-10-28T17:11:53Z | clean |
| `6_c2_bypasses.empty_meaning_columns` | current@22fd0d6b | 0 | `e64b7fc92d2023a83a4ad953e286d5c9b39476f8eed220368d50e67ea6ffc12b` | 2026-10-28T17:11:53Z | clean |
| `6_c2_bypasses.midline_comment` | current@22fd0d6b | 0 | `53b1a4e586898775aeacb2981dcec6459fc4f9a5d8638063d3277781919efbae` | 2026-10-28T17:11:53Z | clean |
| `6_c2_bypasses.fence_swap` | current@22fd0d6b | 0 | `ffdee675f626e87cd8e6b291a02ab932b93617e052ffa0a654b73e6025f96a31` | 2026-10-28T17:11:53Z | clean |
| `7_write_scope.census_out_outside_lane` | current@22fd0d6b | 0 | `—` | 2026-10-28T17:11:53Z | clean |
| `8_selftests.attest.py` | current@22fd0d6b | 0 | `6aa73c612069dd72988df7484fb76e4fbc3581d0e69916672589b5949f46dfa6` | 2026-10-28T17:11:53Z | clean |
| `8_selftests.registry.py` | current@22fd0d6b | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | 2026-10-28T17:11:53Z | clean |
| `c1_tamper_plus_shrink` | verify@c0112995 | 2 | `a8b645c9982b5ad1790b952b367d715fcde5b2568f44447ef1e0ca3d201ac97d` | 2026-10-28T17:13:16Z | frozen_path_changed |
| `c1_tamper_only` | verify@c0112995 | 2 | `24988c3e6fd65c1ad1c34519cf5c6c9e7b97db17887bdece35a05f75358057cb` | 2026-10-28T17:13:16Z | frozen_path_changed |
| `c2_tamper_plus_shrink` | verify@c0112995 | 2 | `322b7bb48476abe377fbf364ab7824f634fed4049522358f8ca2df5010b6aeaf` | 2026-10-28T17:13:16Z | frozen_path_changed |
| `dirty_arm.clean` | verify@c0112995 | 0 | `c262081a1549c5a743a02fbd3486656cb57f10665af668ec3fc836356cb4f155` | 2026-10-28T17:13:16Z | clean |
| `dirty_arm.dirty` | verify@c0112995 | 2 | `a07bacfd73cf6517397004be4e229535021634b804b6073a1f25f8e490aa77a6` | 2026-10-28T17:13:16Z | frozen_worktree_dirty |
| `fsmonitor_exec` | verify@c0112995 | 0 | `c262081a1549c5a743a02fbd3486656cb57f10665af668ec3fc836356cb4f155` | 2026-10-28T17:13:16Z | clean |
| `p1_fence_swap` | frozen@3182047 | 0 | `57f1bf18ed11a5a0bf83c96165ac8419ebf5e56d0959f9688d28ad5fe2d2b2eb` | 2026-10-28T17:13:50Z | clean |
| `p2_decoy_section` | frozen@3182047 | 0 | `1427ae7f2cf84de0a1bfac6593669f92d228f9cf39c3770c47b6504fb3577658` | 2026-10-28T17:13:50Z | clean |
| `p3_pin_counts_toward_refs_min` | frozen@3182047 | 0 | `098c8517a06265ded5e842c7fe10c0ac10a5435137638f6f5de6f1b5b7c42d42` | 2026-10-28T17:13:50Z | clean |
| `p6_vacuous_battery` | frozen@3182047 | 1 | `—` | 2026-10-28T17:13:50Z | clean |
| `p8_census_out.outside_lane` | frozen@3182047 | 0 | `—` | 2026-10-28T17:13:50Z | clean |
| `p8_census_out.clobbers_tool` | frozen@3182047 | 0 | `—` | 2026-10-28T17:13:50Z | clean |
| `p9_nonutf8_blob` | frozen@3182047 | 1 | `—` | 2026-10-28T17:13:50Z | unhandled UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 240: invalid start byte |
| `p10_frozen_gate_shrink.honest` | frozen@3182047 | 2 | `—` | 2026-10-28T17:13:50Z | clean |
| `p10_frozen_gate_shrink.tamper_plus_shrink` | frozen@3182047 | 0 | `—` | 2026-10-28T17:13:50Z | clean |
| `c2_green_with_battery` | frozen@3182047 | 1 | `c0100dc6f2a1ea95b5ac6f193ad5bd62b67367260d1e9771ab590ab80c1fc0a9` | 2026-10-28T17:14:06Z | ['battery v1_green 5 != 7'] |
| `c2_fabricated_census` | frozen@3182047 | 1 | `a3206f37fc17478dfb3801b3eb7f2700b469d1d5875788ff8fe348c2d201efc1` | 2026-10-28T17:14:06Z | ['battery v1_green 5 != 7'] |
| `c2_midline_comment` | frozen@3182047 | 0 | `95f831dae0efbb4c7e37b6eff5e4fe722ff20750d76e762aba37d626b85972e9` | 2026-10-28T17:14:06Z | clean |
| `c1_vacuous_structural` | frozen@3182047 | 0 | `3afd25e5beb04e3d46765580c403bed3b94129ba5ef61224ae186fdda24a6643` | 2026-10-28T17:14:06Z | clean |
