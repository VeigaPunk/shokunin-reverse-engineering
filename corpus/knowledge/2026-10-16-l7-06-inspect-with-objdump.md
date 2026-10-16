# REA 6.5.0 `inspect_with_objdump`: `file_headers` only

source: `.ufo/waves/luna-round-6/receipts/leg-8.md:3-14`; `.ufo/waves/luna-round-6/receipts-B/leg-8.md:41-55,67-76`
verified-at: 2026-10-16
recheck: Repeat `inspect_with_objdump` with the pinned path, SHA-256, `operation=file_headers`, and `follow_debug_links=false`; record Evidence metadata and complete provider output.

- Observation — On `/usr/bin/jq` (SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`), REA 6.5.0 call `inspect_with_objdump({path:"/usr/bin/jq", operation:"file_headers", follow_debug_links:false})` against this SHA returned Evidence `ev_aa75cc2e36b149a82b41e763b92697efc1e2c432571d14c003e3a7bff0219c2f`; provider `gnu.objdump`, argv `objdump -f /usr/bin/jq`, exit 0, complete/untruncated output. It reports `elf64-x86-64`, architecture `i386:x86-64`, flags `HAS_SYMS, DYNAMIC, D_PAGED`, start `0x3cf0`. Lane B's same-carrier compare reproduced the Evidence ID and raw provider stdout. (`.ufo/waves/luna-round-6/receipts/leg-8.md:8-14,19`; `.ufo/waves/luna-round-6/receipts-B/leg-8.md:41-55`.)
- Observation — Lane B also got RESULT on `/home/vgpnk/.local/bin/jq` (SHA-256 `b1c22172dd303f3be49e935aa56aa48a8b7a46e0bc838b4997d3bb451495870f`), a distinct carrier and Evidence ID (`.ufo/waves/luna-round-6/receipts-B/leg-8.md:6-8,16-35`); this is not same-output evidence.
- Inference — The exact `file_headers` request completed on these two pinned jq ELF inputs; this does not establish general format support or classification accuracy.
- Unknown — REA format/architecture metadata are `unknown`/`null`; provider version is `null`; supported formats and behavior of other operations, including disassembly, remain unestablished. `artifact_changed=false` does not prove the exact bytes consumed.

Sources: `.ufo/waves/luna-round-6/receipts/leg-8.md:3-14,19`; `.ufo/waves/luna-round-6/receipts-B/leg-8.md:6-8,16-35,41-55,67-76`; carrier `.ufo/waves/luna-round-6/SC6.md:8`.
