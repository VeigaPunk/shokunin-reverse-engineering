## CLAIM
Entry-5 (`search_bytes` on `/usr/bin/true`) and entry-6 (`inspect_with_objdump` on jq) receipt evidence reproduces exactly: cited line anchors, declared stdout hashes, Evidence IDs, and carrier SHA-256s all check out; SC5/SC6 carrier claims corroborated. Entry-5's draft lacks the house metadata header; one reproducer paraphrase (no falsification).

## METHOD
Read-only at HEAD 411175e (git read-only): `sed -n`/`wc -c`/`sha256sum`/`diff` on the four receipt stdout blocks; `sha256sum`/`stat`/`file` on the three pinned carriers; `pacman -Qo`, `readelf -d`; `git hash-object` vs `git rev-parse HEAD:<path>`; `git ls-tree`; Grep over round-7 drafts. No REA/MCP/network probes.

## FINDINGS
1. Recomputing embedded stdout blocks reproduces every declared hash: `receipts/leg-7.md` `sed -n '19,21p'` → 19151 B, `3492d27d…29a8` (declared `:14`); `receipts-B/leg-7.md` `sed -n '30,32p'` → same 19151 B/hash, `diff` exit 0 (byte-identical claim holds); `receipts/leg-8.md` `sed -n '18,19p'` → 5301 B, `e0b2d505…` (`:13`); `receipts-B/leg-8.md` `sed -n '33,34p'` → 5425 B, `86f5497f…` (`:28`) and `sed -n '59,60p'` → 5301 B, `9c47f056…` (`:53`).
2. Carriers still match pins: `/usr/bin/true` 43320 B `8bc9a73a…`; `/usr/bin/jq` 30800 B `e8156675…`; `/home/vgpnk/.local/bin/jq` 2267912 B `b1c22172…`.
3. Evidence IDs resolve at cited anchors: `ev_4b0badc6…` (`receipts/leg-7.md:13,21`); `ev_aa75cc2e…` (`receipts/leg-8.md:12,19`; `receipts-B/leg-8.md:60`); `ev_d1ea68b7…` (`receipts-B/leg-8.md:29`). SC6's jq line corroborated: `pacman -Qo /usr/bin/jq` → `jq 1.8.2-1`; NEEDED = libjq.so.1, libonig.so.5, libc.so.6; SC5's wasm hash `d2119fb9…` reproduced.
4. All four receipts are HEAD-tracked and byte-identical to their HEAD blobs; SC5/SC6 are untracked worktree files. Lane-A `receipts/MANIFEST.txt` lists only leg-1 (in HEAD too); lane-B MANIFEST hashes/sizes match B leg-7/8 (`c39368bd…`/`c1268dae…`).
5. Notes: `E5D.md:5` shows `limit=100` in the reproducer while the recorded request (`receipts/leg-7.md:9`) omits it — effective default per result (`:21`), same call. `E5D.md` carries no `source:/verified-at:/recheck:` block (`E6D.md:12-14` does, values resolve; corroborates `FB4.md:9`). Z5's "E5D/G5 absent" is stale: both present and substantively convergent.

## THREATS
Receipt review, not replay — historical execution not independently repeated. SC5/SC6 are untracked (lane-B receipts are HEAD-tracked). Landing counters (78/78), prior-72 byte identity, and final-body QUALITY admission remain parent-integration items.

## VERDICT
CLEAN — entry-5/6 evidence reproduces exactly; integrate entry 5 with the house metadata header.
