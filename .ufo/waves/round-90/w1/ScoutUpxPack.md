# ScoutUpxPack — trailer copy

Full scoped findings, every command/line number, and the proposed `SOURCES.md` row text:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScoutUpxPack/ScoutUpxPack.md`

Raw read-only receipts (10 files):
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ScoutUpxPack/receipts/`
(`http-status.txt`, `sha256-fresh.txt`, `fetch-receipt.txt`, `grep-p_unix-pack.txt`,
`grep-p_lx_elf-pack.txt`, `grep-packExtent-tree.txt`, `scope-probe.txt`, `chain-measurement.txt`,
`block0-prediction.txt`, `line-numbers.txt`)

One-paragraph summary: `src/p_unix.cpp` at tag `v5.2.0` (HTTP 200, 24181 bytes, sha256
`bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`, byte-identical to the tag's
tarball) grounds the **pack-side** half of the round-90 law at `PackUnix::packExtent`
(`p_unix.cpp:335`) — `sz_unc`/`sz_cpr` from `ph.u_len`/`ph.c_len` (lines 439-440), the 12-byte header
write (449), and exactly `sz_cpr` payload bytes after it (458, 464) with nothing in between, so
`sz_cpr = successor − (block + 12)` is exact. It is a **new scope, not the round-87 rejection**: that
rejection was bound to `PackUnix::unpack`, which the ELF classes override (`p_lx_elf.cpp:7755, 9023`)
and which therefore never runs for the carriers, whereas `PackUnix::packExtent` has **no** override
anywhere in the v5.2.0 tree and is in force. Measured with the pinned packer
(`upx` sha256 `cf2f6e7c…8c969`, matching the round-90 pin): block 0's `sz_unc` equals the source
formula `64 + phnum*56` on all four pinned carriers (904/904/736/680); jq's interior block at `0x9c7`
has `sz_cpr = 4758` and `0x1c69 − (0x9c7 + 12) = 4758`; the chain is two segments split by the
loader, and libz accounts 98,592 of 108,560 `u_len` — reproducing the plan's declared limit. S311's
anchor has two line slips (7067→7069, 7098→7102) and S312's `teaches` wording needs one precision
item; both close by new `supersedes` rows, which the L1 owns.
