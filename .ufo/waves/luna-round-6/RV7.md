## CLAIM
At the 18:26 audit snapshot, all eight present leg receipts (L1–L6, L8, L9) record exit code 0. Independent reruns confirm 0 for L1, L2, L8, and L9. The full ten-leg exit-code claim is not verifiable: L7 and L10 receipts are absent.

## METHOD
Read the present receipts and checked the inventory with `ls -1 .ufo/waves/luna-round-6/receipts`. Re-ran L1’s version command from `/tmp`; observed exit 0, stdout `6.5.0`, SHA-256 `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00`. Re-ran L2 MCP `tools/list`, closed stdin, and observed process exit 0, 207 tools, and stdout SHA-256 `38d44bf8ee0944315a1d50d3e3acec1401be50efe7090ac22ec8498e853d4129`. Re-ran L8 `inspect_with_objdump` and provider `objdump -f /usr/bin/jq`: MCP/provider exits 0; provider stdout SHA matches receipt (`22205280f95a0151fec83144666eab3e5a0ccb2300d0d3cb688b3edd00e6570f`). Re-ran L9’s sequenced refusal call: MCP exit 0, stdout SHA matches (`1ff84c06a9a426877d60c46362375b404c2e7cbb55d4496e8c6d2136f1c86909`); server exited after stdin EOF.

## FINDINGS
- Recorded codes are 0: L1 `receipts/leg-1.md:10`; L2 `leg-2.md:18`; L3 `leg-3.md:219`; L4 `leg-4.md:37`; L5 `leg-5.md:11`; L6 `leg-6.md:13`; L8 provider/server `leg-8.md:21,26`; L9 `leg-9.md:9,25`.
- No exit-code mismatch found in the four independent reruns. L1 replay stderr had npm notices while its receipt says empty; stdout and exit code matched.
- Inventory lacks `leg-7.md` and `leg-10.md`. `receipts/MANIFEST.txt` lists only leg-1 although the other seven receipts are present.

## THREATS
L3–L6 were not independently rerun; their recorded codes are consistent with the successful tool outputs but remain unverified by replay. The receipt inventory may still change after this snapshot.

## VERDICT
FINDING: full exit-code audit is incomplete because L7/L10 receipts are absent; four of eight present receipts were independently confirmed.