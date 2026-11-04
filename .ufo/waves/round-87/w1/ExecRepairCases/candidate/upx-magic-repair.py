#!/usr/bin/env python3
"""upx-magic-repair.py - round-87 tool (R87-C1, coverage, capability).

Restores the `UPX!` magic words of a UPX-packed little-endian ELF whose
markers were overwritten (anti-unpack tampering), using only the packer's own
structures, so the pinned packer (UPX 5.2.0) can test and unpack it again.

Structures (UPX v5.2.0 sources, corpus/SOURCES.md rows for linux.h and
p_unix.cpp / packhead.cpp):

  PackHeader  32 bytes near the end of the file for version >= 10 and a
              non-DOS format: magic(4) version format method level u_adler
              c_adler u_len c_len u_file_size filter filter_cto n_mru
              checksum.  The checksum byte is the sum of bytes 4..30 mod 251 -
              it EXCLUDES the magic, so it still validates a tampered header.
  l_info      {l_checksum, l_magic, l_lsize, l_version, l_format}, followed by
  p_info      {p_progid, p_filesize, p_blocksize}: l_version/l_format equal the
              PackHeader's version/format and p_filesize equals u_file_size.
  b_info      {sz_unc, sz_cpr, method, ftid, cto8, unused} chain after p_info;
              the end-of-chain b_info has sz_unc == 0 and sz_cpr == magic.

Three anchors are located structurally, never by the tampered value: the
PackHeader (checksum-validated), the l_info magic (cross-checked against the
PackHeader) and the end-of-chain b_info (reached by walking the chain).  Each
anchor that does not read `UPX!` is rewritten; nothing else changes.

Usage: python3 -I -B upx-magic-repair.py --in <file> --out <file> [--json]
Exit: 0 repaired or already intact (output written; byte-identical when
intact); 2 refused (not an ELF, no validated PackHeader, no l_info matching
it, or a chain that does not end in a sentinel) - nothing is written.
The tool reads only --in; it never runs the packer.
--selftest runs synthetic structure fixtures.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys

MAGIC = b"UPX!"
PH_SIZE = 32
TAIL_WINDOW = 512          # PackHeader search window from the end of file
MAX_BLOCKS = 1 << 16


class Refused(Exception):
    pass


def ph_checksum(buf: bytes) -> int:
    return sum(buf[4:PH_SIZE - 1]) % 251


def find_packheader(d: bytes) -> tuple[int, dict]:
    """Last offset in the tail window whose 32 bytes validate as a PackHeader."""
    n = len(d)
    lo = max(0, n - TAIL_WINDOW)
    for o in range(n - PH_SIZE, lo - 1, -1):
        h = d[o:o + PH_SIZE]
        version, fmt = h[4], h[5]
        if version < 10 or fmt >= 128 or fmt in (1, 2, 3, 4):  # LE, non-DOS
            continue
        if h[PH_SIZE - 1] != ph_checksum(h):
            continue
        u_len, c_len, u_file_size = struct.unpack_from("<III", h, 16)
        if not (0 < c_len <= n and 0 < u_len and 0 < u_file_size):
            continue
        return o, {"version": version, "format": fmt, "method": h[6], "u_len": u_len,
                   "c_len": c_len, "u_file_size": u_file_size}
    raise Refused("no validated PackHeader in the tail window")


def walk_chain(d: bytes, start: int, end: int, method: int | None,
               alt: int | None = None) -> tuple[int, int, int]:
    """Walk b_info blocks from `start`.  Returns (stop offset, blocks walked,
    method of the first block).  A block is plausible when 0 < sz_cpr <=
    sz_unc, it fits before `end`, and (after the first) its method matches
    the first block's or `alt` (the PackHeader method: an LZMA-packed shared
    object has an NRV2B first block followed by LZMA blocks)."""
    q, n = start, 0
    for _ in range(MAX_BLOCKS):
        if q < 0 or q + 12 > end:
            break
        sz_unc, sz_cpr = struct.unpack_from("<II", d, q)
        meth = d[q + 8]
        if sz_unc == 0 or sz_cpr == 0 or sz_cpr > sz_unc or q + 12 + sz_cpr > end:
            break
        if method is None:
            method = meth
        elif meth != method and meth != alt:
            break
        q += 12 + sz_cpr
        n += 1
    return q, n, (method if method is not None else -1)


def is_sentinel(d: bytes, s: int, ph_off: int) -> bool:
    """End-of-chain b_info: sz_unc == 0 and method/ftid/cto8/unused all 0,
    wholly before the PackHeader.  (Executables carry 0-3 zero bytes between
    it and the PackHeader; shared objects carry further appended data, so no
    padding rule is imposed.)"""
    if s < 0 or s + 12 > ph_off:
        return False
    return d[s:s + 4] == b"\0\0\0\0" and d[s + 8:s + 12] == b"\0\0\0\0"


def find_sentinel(d: bytes, start: int, ph_off: int,
                  ph_method: int | None = None) -> tuple[int, dict]:
    """The end-of-chain b_info, reached by walking the b_info chain from
    p_info and, where the chain stops at the embedded loader, by resuming at
    the first later offset whose own chain (same method, or the PackHeader
    method) ends at a sentinel - the same 'get past the loader' step UPX's
    unpacker takes (p_lx_elf.cpp)."""
    stop, n1, method = walk_chain(d, start, ph_off, None, ph_method)
    if n1 == 0:
        raise Refused("p_info is not followed by a plausible b_info")
    if is_sentinel(d, stop, ph_off):
        return stop, {"blocks_first": n1, "resume": None, "blocks_resumed": 0}
    for s in range(stop + 1, ph_off - 12):
        sz_unc, sz_cpr = struct.unpack_from("<II", d, s)
        if (not (0 < sz_cpr < sz_unc) or d[s + 8] not in (method, ph_method)
                or d[s + 9] or d[s + 10]):
            continue
        end, n2, _ = walk_chain(d, s, ph_off, method, ph_method)
        if n2 and is_sentinel(d, end, ph_off):
            return end, {"blocks_first": n1, "resume": s, "blocks_resumed": n2}
    raise Refused("b_info chain does not reach an end-of-chain sentinel")


def find_linfo(d: bytes, ph_off: int, ph: dict) -> tuple[int, int, dict]:
    """(l_magic offset, sentinel b_info offset, walk info) for the first
    l_info that matches the PackHeader and whose chain reaches a sentinel."""
    want = struct.pack("<I", ph["u_file_size"])
    p = d.find(want, 12)
    last = "no l_info/p_info matching the PackHeader"
    while p != -1 and p < ph_off:
        m = p - 12  # p_filesize sits 12 bytes after l_magic
        if m >= 4 and m + 20 <= ph_off:
            if d[m + 6] == ph["version"] and d[m + 7] == ph["format"]:
                try:
                    s, info = find_sentinel(d, m + 20, ph_off, ph["method"])
                    return m, s, info
                except Refused as exc:
                    last = str(exc)
        p = d.find(want, p + 1)
    raise Refused(last)


def repair(d: bytes) -> tuple[bytes, dict]:
    if d[:4] != b"\x7fELF" or len(d) < 64 or d[5] != 1:
        raise Refused("not a little-endian ELF")
    ph_off, ph = find_packheader(d)
    l_magic, sentinel, walk = find_linfo(d, ph_off, ph)
    anchors = {"packheader": ph_off, "l_info": l_magic, "b_info_end": sentinel + 4}
    out = bytearray(d)
    restored = []
    for name, off in anchors.items():
        if out[off:off + 4] != MAGIC:
            restored.append({"anchor": name, "offset": off,
                             "was": bytes(out[off:off + 4]).hex()})
            out[off:off + 4] = MAGIC
    return bytes(out), {"anchors": anchors, "restored": restored,
                        "packheader": ph, "walk": walk, "intact": not restored}


def _fixture(tamper: bytes | None = None) -> bytes:
    """A synthetic ELF-shaped image with l_info, p_info, a 2-block chain,
    a sentinel and a PackHeader, laid out as UPX 5.2.0 lays out amd64 ELF."""
    u_file_size = 4096
    body = bytearray(b"\x7fELF\x02\x01\x01" + b"\0" * 57)
    body += struct.pack("<I", 0x11223344) + MAGIC + struct.pack("<HBB", 3000, 14, 22)
    body += struct.pack("<III", 0, u_file_size, u_file_size)
    for blk in (b"A" * 40, b"B" * 24):
        body += struct.pack("<IIBBBB", 100, len(blk), 14, 0, 0, 0) + blk
    body += struct.pack("<II", 0, struct.unpack("<I", MAGIC)[0]) + b"\0" * 4
    ph = bytearray(MAGIC + bytes([14, 22, 14, 10]) + struct.pack("<IIIII", 1, 2, 64, 64, u_file_size)
                   + bytes([0, 0, 0, 0]))
    ph[31] = ph_checksum(bytes(ph))
    body += ph + struct.pack("<I", 0)
    data = bytes(body)
    return data if tamper is None else data.replace(MAGIC, tamper)


def selftest() -> int:
    fails = []
    ncases = 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    def refuses(name, bad):
        try:
            repair(bad)
            ok = False
        except Refused:
            ok = True
        check(f"refuses-{name}", ok)

    def put(buf: bytes, off: int, val: bytes) -> bytes:
        return buf[:off] + val + buf[off + len(val):]

    def restored(info) -> list:
        return [r["anchor"] for r in info["restored"]]

    clean = _fixture()
    for name, val in (("zero", b"\0\0\0\0"), ("foreign", b"KDK!"), ("ff", b"\xff" * 4)):
        out, info = repair(_fixture(val))
        check(f"restores-{name}", out == clean and len(info["restored"]) == 3)
    out, info = repair(clean)
    check("intact-idempotent", out == clean and info["intact"])
    for name, bad in (("not-elf", b"MZ" + clean[2:]),
                      ("ph-checksum", clean[:-5] + bytes([clean[-5] ^ 1]) + clean[-4:]),
                      ("no-sentinel", clean.replace(b"B" * 24, b"B" * 23 + b"C").replace(
                          struct.pack("<IIBBBB", 100, 24, 14, 0, 0, 0),
                          struct.pack("<IIBBBB", 100, 25, 14, 0, 0, 0))),
                      ("short", b"\x7fELF")):
        refuses(name, bad)
    # a partial tamper (only l_info) is still repaired
    part = bytearray(clean)
    lm = clean.find(MAGIC)
    part[lm:lm + 4] = b"\0\0\0\0"
    out, info = repair(bytes(part))
    check("partial-linfo", out == clean and restored(info) == ["l_info"])

    # --- structural edge cases ---------------------------------------------
    lm, sm, pm = [i for i in range(len(clean) - 3) if clean[i:i + 4] == MAGIC]
    order = {"l_info": lm, "b_info_end": sm, "packheader": pm}
    # a different tamper value per anchor; `was` records each one
    mixed = put(put(put(clean, lm, b"KDK!"), sm, b"\0\0\0\0"), pm, b"\xff" * 4)
    out, info = repair(mixed)
    was = {r["anchor"]: r["was"] for r in info["restored"]}
    check("mixed-per-anchor", out == clean and was == {
        "l_info": b"KDK!".hex(), "b_info_end": "00000000", "packheader": "ffffffff"})
    # each anchor tampered alone (l_info alone with zero is partial-linfo)
    for anchor, val in (("packheader", b"KDK!"), ("b_info_end", b"\0\0\0\0"),
                        ("l_info", b"\xa5\x5a\xa5\x5a")):
        out, info = repair(put(clean, order[anchor], val))
        check(f"single-{anchor}", out == clean and restored(info) == [anchor]
              and info["anchors"][anchor] == order[anchor])
    # truncation: every cut that reaches into the PackHeader refuses (T1 and
    # clean); dropping only the 4 trailing pad bytes leaves a valid layout
    t1 = _fixture(b"\0\0\0\0")
    bad_cuts = []
    for src in (clean, t1):
        for n in range(len(src) - 4):
            try:
                repair(src[:n])
                bad_cuts.append(n)
            except Refused:
                pass
    check("truncated-every-cut-refused", not bad_cuts)
    out, info = repair(t1[:-4])
    check("truncated-pad-only-repairs", out == clean[:-4])
    # bytes spliced out of a compressed block (header unchanged): the chain
    # no longer lands on the sentinel
    bpos = clean.find(b"B" * 24)
    for name, src in (("clean", clean), ("t1", t1), ("foreign", _fixture(b"KDK!"))):
        refuses(f"spliced-block-{name}", src[:bpos] + src[bpos + 4:])
    # a plain ELF whose tail holds a window passing the PackHeader checksum:
    # with no l_info/p_info/chain matching it, it must still refuse
    plain = bytearray(b"\x7fELF\x02\x01\x01" + b"\0" * 57)
    plain += bytes((i * 37 + 11) & 0xFF for i in range(2048))
    fake = bytearray(b"\x13\x37\xbe\xef" + bytes([14, 22, 14, 10])
                     + struct.pack("<IIIII", 7, 9, 0x5000, 0x400, 0x0BADF00D) + b"\0" * 4)
    fake[31] = ph_checksum(bytes(fake))
    ok_fake = True
    try:
        _, fph = find_packheader(bytes(plain + fake))
        ok_fake = fph["u_file_size"] == 0x0BADF00D
    except Refused:
        ok_fake = False
    check("chance-window-validates", ok_fake)
    linfo = struct.pack("<I", 0) + b"\0\0\0\0" + struct.pack("<HBB", 3000, 14, 22)
    pinfo = struct.pack("<III", 0, 0x0BADF00D, 0x0BADF00D)
    for name, body in (
            ("chance-window-no-linfo", plain),
            ("chance-window-linfo-version-mismatch",
             plain[:512] + struct.pack("<I", 0) + b"\0" * 4 + struct.pack("<HBB", 3000, 13, 22)
             + pinfo + plain[512 + 32:]),
            ("chance-window-linfo-no-chain",
             plain[:512] + linfo + pinfo + struct.pack("<IIBBBB", 10, 20, 14, 0, 0, 0)
             + plain[512 + 44:]),
            ("chance-window-linfo-chain-no-sentinel",
             plain[:512] + linfo + pinfo + struct.pack("<IIBBBB", 100, 8, 14, 0, 0, 0)
             + b"Z" * 8 + struct.pack("<IIBBBB", 100, 0xFFFF, 14, 0, 0, 0)
             + plain[512 + 64:])):
        refuses(name, bytes(body) + bytes(fake))
    # sz_cpr overflow / no-progress blocks: the walk stops, no sentinel
    first = clean.find(struct.pack("<IIBBBB", 100, 40, 14, 0, 0, 0))
    second = clean.find(struct.pack("<IIBBBB", 100, 24, 14, 0, 0, 0))
    for name, off, hdr in (
            ("overflow-first", first, struct.pack("<II", 0xFFFFFFFF, 0xFFFFFFF0)),
            ("overflow-second", second, struct.pack("<II", 0xFFFFFFFF, 0xFFFFFFF0)),
            ("szcpr-gt-szunc", first, struct.pack("<II", 39, 40)),
            ("zero-advance", first, struct.pack("<II", 100, 0))):
        refuses(name, put(t1, off, hdr))
    # an embedded loader between chains: the walk resumes past it
    junk = b"\xff" * 16
    looped = clean[:second] + junk + clean[second:]
    out, info = repair(put(put(put(looped, lm, b"\0" * 4), sm + 16, b"\0" * 4), pm + 16, b"\0" * 4))
    check("resume-past-loader", out == looped and info["walk"]["resume"] == second + 16
          and len(info["restored"]) == 3)
    # UPX! inside a compressed payload is not an anchor and is left alone
    pay = clean.replace(b"A" * 40, b"A" * 18 + MAGIC + b"A" * 18)
    tam = bytearray(pay)
    for off in (lm, sm, pm):
        tam[off:off + 4] = b"KDK!"
    out, info = repair(bytes(tam))
    check("payload-magic-untouched", out == pay and len(info["restored"]) == 3)
    # only a PackHeader: raw, and behind a bare ELF header
    refuses("ph-only", clean[pm:pm + PH_SIZE])
    refuses("elf-header-plus-ph-only", clean[:64] + clean[pm:pm + PH_SIZE])
    # mixed-method chain (NRV2B first block, then the PackHeader's LZMA
    # method; `upx --lzma` shared objects): repaired; a third method refuses
    mixed_m = put(clean, first + 8, b"\x02")
    out, info = repair(put(put(put(mixed_m, lm, b"\0" * 4), sm, b"\0" * 4), pm, b"\0" * 4))
    check("mixed-method-chain", out == mixed_m and info["walk"]["blocks_first"] == 2)
    refuses("foreign-method-chain", put(put(t1, first + 8, b"\x02"), second + 8, b"\x07"))
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.inp or not a.out:
        print("refused: --in and --out are required", file=sys.stderr)
        return 2
    with open(a.inp, "rb") as fh:
        data = fh.read()
    try:
        out, info = repair(data)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    with open(a.out, "wb") as fh:
        fh.write(out)
    if a.json:
        print(json.dumps(info, sort_keys=True))
    else:
        print(f"{'intact' if info['intact'] else 'repaired'}: restored {len(info['restored'])} "
              f"anchor(s) {[r['anchor'] for r in info['restored']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
