## CLAIM
Draft for `corpus/knowledge/2026-10-16-l7-05-search-bytes.md`. **Observation:** `search_bytes` returned one match for ELF magic in `/usr/bin/true` (SHA-256 `8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d`), evidence `ev_4b0badc6b166fb6e6196ec561521d48873af50c2f41329deca72ccc685eab903` (.ufo/waves/luna-round-6/receipts/leg-7.md:8-14,21).

## METHOD
**Observation:** The recorded reproducer was `cd /tmp && npx -y rea-agents@6.5.0 --mcp`, then `open_binary(path=/bin/true)` and `search_bytes(pattern="7f 45 4c 46", limit=100)`. The opened target resolves to `/usr/bin/true`; provider Ghidra 12.1.4, default auto-analysis (.ufo/waves/luna-round-6/receipts/leg-7.md:3-12; receipts-B/leg-7.md:21-25).

## FINDINGS
**Observation:** The match was at loader address `0x100000`, segment `segment_2.1`, file offset `0`, with `procedure=null`; 33,668 bytes were searched, `complete=true`, `next_cursor=null` (.ufo/waves/luna-round-6/receipts-B/leg-7.md:56-61). Lane B independently reproduced a byte-identical stdout hash and the same hit/offset (.ufo/waves/luna-round-6/receipts-B/leg-7.md:64-72). The result describes loader-adjusted memory searched per block; uninitialized blocks are reported separately, patterns do not cross block boundaries, and not-loaded sections are excluded (.ufo/waves/luna-round-6/receipts/leg-7.md:21; receipts-B/leg-7.md:32).

## THREATS
**Unknown:** This single default-limit query does not verify paging, cancellation, other patterns, or other formats. Its `complete` flag applies to this query, not all raw bytes of the file; the receipt lists uninitialized and not-loaded ranges (.ufo/waves/luna-round-6/receipts-B/leg-7.md:32,56-61). **Inference:** This static search is not evidence of runtime behavior. The RESULT-class exercise is not a Core promotion; PROVINCE remains untouched.

## VERDICT
CLEAN
