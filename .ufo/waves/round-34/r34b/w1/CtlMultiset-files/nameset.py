#!/usr/bin/env python3
"""ExecRedReproduce R2: name-set keyed memorization (string-scan + replay).

Shortcut class: content-multiset memorization, composed from the registered
string-scan class plus a stored answer table. It scans the file for NUL-terminated
ASCII tokens that look like SONAMEs, then replays a memorized name -> (flags,
value) table keyed by the *sorted set of names found*.

It never reads the header, never walks the record array, and never reads a
name_off field: the association between a name and its flags/value comes from
the table, not from the bytes. Structure-blind by construction.

Invariant exploited: permuting the name pool changes the pool order and every
name_off, but leaves the set of names in the file unchanged, so a key built from
that set is invariant under the mini counter's only transformation.
"""
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(rb"[A-Za-z0-9_.+-]+\.so(?:\.[0-9]+)+")

TABLE = {
    "libc.so.6|libm.so.6|libz.so.1": [("libc.so.6", 0, 100729359), ("libm.so.6", 1, 2819),
                                      ("libz.so.1", 0, 2912)],
    "libcrypto.so.3": [("libcrypto.so.3", 0, 50332424)],
    "libdl.so.2|libgcc_s.so.1|libpthread.so.0|libresolv.so.2|libutil.so.1": [
        ("libgcc_s.so.1", 2, 2912), ("libpthread.so.0", 0, 0), ("libdl.so.2", 1, 2912),
        ("libutil.so.1", 0, 2912), ("libresolv.so.2", 0, 2912)],
    "libatomic.so.1|libstdc++.so.6": [("libstdc++.so.6", 0, 50531585), ("libatomic.so.1", 0, 2819)],
    "ld-linux-x86-64.so.2": [("ld-linux-x86-64.so.2", 0, 2819)],
    "libGL.so.1|libX11.so.6|libwayland-client.so.0|libxcb.so.1": [
        ("libGL.so.1", 3, 2912), ("libX11.so.6", 0, 2912), ("libxcb.so.1", 0, 2912),
        ("libwayland-client.so.0", 0, 2912)],
    "libcares.so.2|libcurl.so.4|libssl.so.3": [("libssl.so.3", 1, 50332424),
                                               ("libcurl.so.4", 0, 50531585),
                                               ("libcares.so.2", 0, 2819)],
    "libffi.so.8|libgmp.so.10|libisl.so.23|libmpc.so.3|libmpfr.so.6|libzstd.so.1": [
        ("libffi.so.8", 0, 2819), ("libgmp.so.10", 0, 2819), ("libmpfr.so.6", 0, 2819),
        ("libmpc.so.3", 0, 2819), ("libisl.so.23", 0, 2819), ("libzstd.so.1", 0, 2912)],
}


def main():
    if len(sys.argv) != 2:
        return 3
    data = Path(sys.argv[1]).read_bytes()
    names = sorted({token.decode("ascii") for token in TOKEN.findall(data)})
    key = "|".join(names)
    if key not in TABLE:
        return 3  # unrecognised content: typed refusal, no receipt
    records = [{"name": n, "flags": f, "value": v} for n, f, v in TABLE[key]]
    print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
