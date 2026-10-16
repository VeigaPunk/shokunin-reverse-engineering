# search_bytes — one ELF-magic hit in loader-adjusted memory

source: `.ufo/waves/luna-round-6/receipts/leg-7.md:3-14,19-21`; `.ufo/waves/luna-round-6/receipts-B/leg-7.md:18-27,56-72`; carrier `.ufo/waves/luna-round-6/SC5.md:9`
verified-at: 2026-10-16
recheck: `cd /tmp && npx -y rea-agents@6.5.0 --mcp`, then `open_binary({"path":"/bin/true"})` and `search_bytes({"pattern":"7f 45 4c 46"})`; expect Evidence `ev_4b0badc6b166fb6e6196ec561521d48873af50c2f41329deca72ccc685eab903`: exactly one hit at address `0x100000` / `file_offset:0`, 33,668 bytes searched over loader-adjusted blocks, `complete:true`, `next_cursor:null`.

REA pin: `rea-agents@6.5.0`; provider Ghidra 12.1.4, default auto-analysis (`receipts/leg-7.md:3-13`).

Carrier: `/bin/true`, resolved to `/usr/bin/true` (ELF x86-64, 43,320 bytes), SHA-256 `8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d`.
Round-6 call: `search_bytes` with `{"pattern":"7f 45 4c 46"}` (after `open_binary`); Evidence ID `ev_4b0badc6b166fb6e6196ec561521d48873af50c2f41329deca72ccc685eab903`.

- **Observation:** The call returned exactly one match — address `0x100000`, segment `segment_2.1`, `file_offset:0`, `procedure:null` — with 33,668 bytes searched across 26 initialized loader-adjusted blocks, `complete:true`, `next_cursor:null`. The response records the query's limit as `100`, the tool default (`receipts-B/leg-7.md:60`).
- **Observation (lane B):** An independent replay returned byte-identical stdout, SHA-256 `3492d27d66e086d683935f396ea05fce4cbddc660874052a955c9133866629a8`, agreeing on hit, offset, byte count, and completion (`receipts-B/leg-7.md:64-72`).
- **Inference:** The hit is the ELF magic at file offset 0. This one pinned query demonstrates that search; it does not establish general pattern, target, or raw-file coverage.
- **Unknown / limitations:** `complete:true` covers the reported eligible blocks only; the receipt lists uninitialized and not-loaded blocks separately and states patterns never cross block boundaries (`receipts/leg-7.md:21`) — it is not proof that all 43,320 carrier bytes were searched. No-hit, multi-hit, paging/cursor, cancellation, and other-pattern behavior were not exercised. This static search is not runtime-behavior evidence; RESULT-class exercise only, no Core promotion.

Sources: `.ufo/waves/luna-round-6/receipts/leg-7.md:3-14,19-21`; `.ufo/waves/luna-round-6/receipts-B/leg-7.md:18-27,56-72`; carrier `.ufo/waves/luna-round-6/SC5.md:9`.
