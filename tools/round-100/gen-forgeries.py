#!/usr/bin/env python3
"""gen-forgeries.py - round-100 red fixtures for R100-C1.

Writes one-decision transforms of the round-100 candidate repair into
--out-dir; each must score exit 1 on tools/round-100/pe-upx-corrupt-battery.py
at the freeze, before the candidate is committed.

  h0-identity       copies --in to --out (the do-nothing control).
  h1-refuse-all     refuses `checksum` for every input (over-refusal).
  h2-off-by-header  Adler-32 over [PackHeader, PackHeader + c_len) instead of
                    [PackHeader + 32, PackHeader + 32 + c_len) (an off-by-32
                    window).
  h3-u-adler        compares against u_adler (bytes 8..11) instead of c_adler.
  h4-oracle-alias   the round-99 repair plus a call of `upx -t` through an
                    aliased `os` module (no FORBIDDEN token; the static leg
                    passes, the exec leg must not).
  h5-length-only    the compressed-data length test without the checksum.
  h6-exec-only      the candidate itself plus one harmless `true` exec through
                    an aliased `os`: every other arm passes, so only the exec
                    leg can make it exit 1.

Usage: python3 -I -B gen-forgeries.py --candidate <path> --r99 <path> --out-dir <dir>
Exit 0 written; 1 a transform anchor is missing (SystemExit).
"""
import argparse
import os

CHECK = '''    got = zlib.adler32(bytes(b[cs:cs + c_len]))
    if got != c_adler:
        raise Refuse("checksum: adler32 of compressed data %08x != c_adler %08x" % (got, c_adler))
'''
UNPACK = '''    c_adler, _, c_len = struct.unpack_from("<III", b, i + 12)
'''
R99_FIND = '''    i = find_packheader(b, secs)
    changes = []'''


def sub(text, old, new, name):
    if text.count(old) != 1:
        raise SystemExit("%s: anchor missing" % name)
    return text.replace(old, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--r99", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    with open(a.candidate) as fh:
        cand = fh.read()
    with open(a.r99) as fh:
        r99 = fh.read()
    out = {}
    out["h0-identity"] = (
        "import argparse, shutil, sys\n"
        "ap = argparse.ArgumentParser()\nap.add_argument('--in', dest='inp', required=True)\n"
        "ap.add_argument('--out', required=True)\na = ap.parse_args()\n"
        "shutil.copyfile(a.inp, a.out)\nprint('ok intact')\n")
    out["h1-refuse-all"] = sub(cand, "    i = find_packheader(b, secs)\n",
                               "    i = find_packheader(b, secs)\n    raise Refuse(\"checksum: always\")\n",
                               "h1")
    out["h2-off-by-header"] = sub(cand, "zlib.adler32(bytes(b[cs:cs + c_len]))",
                                  "zlib.adler32(bytes(b[i:i + c_len]))", "h2")
    out["h3-u-adler"] = sub(cand, UNPACK, '    c_adler = struct.unpack_from("<I", b, i + 8)[0]\n'
                            '    c_len = struct.unpack_from("<I", b, i + 20)[0]\n', "h3")
    h4 = sub(r99, "import tempfile\n", "import tempfile\nimport os as q\n", "h4-import")
    h4 = sub(h4, R99_FIND, '''    i = find_packheader(b, secs)
    if ORACLE_IN and q.system("upx -t -q '%s' >/dev/null 2>&1" % ORACLE_IN) != 0 \\
            and bytes(b[i:i + 4]) == MAGIC and secs[0]["name"].startswith(b"UPX"):
        raise Refuse("checksum: oracle says corrupt")
    changes = []''', "h4-find")
    h4 = sub(h4, "        with open(a.inp, \"rb\") as fh:\n",
             "        global ORACLE_IN\n        ORACLE_IN = a.inp\n        with open(a.inp, \"rb\") as fh:\n",
             "h4-main")
    h4 = sub(h4, "PH_LEN = 32\n", "PH_LEN = 32\nORACLE_IN = None\n", "h4-global")
    out["h4-oracle-alias"] = h4
    out["h5-length-only"] = sub(cand, CHECK, "", "h5")
    h6 = sub(cand, "import tempfile\n", "import tempfile\nimport os as q\n", "h6-import")
    out["h6-exec-only"] = sub(h6, "    a = ap.parse_args(argv)\n",
                              "    a = ap.parse_args(argv)\n    q.system(\"true\")\n", "h6-main")
    os.makedirs(a.out_dir, exist_ok=True)
    for name, text in sorted(out.items()):
        with open(os.path.join(a.out_dir, name + ".py"), "w") as fh:
            fh.write(text)
        print("wrote", name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
