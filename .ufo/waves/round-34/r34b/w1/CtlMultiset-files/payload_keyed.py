#!/usr/bin/env python3
"""Post-stop counterexample class: payload-signature memorization.

Authored by the L1 on 2026-10-25 **after** R34-C2 stopped, as evidence for the stop,
not as a frozen instrument. It never reads a name byte and never resolves a name
offset: it takes the record count and the ordered `(flags, value)` pairs from the
record array, keys a memorized name table on that signature, and replays.

Structural use: the record array's flags/value stride only. It does not associate a
name with a record from the bytes, which is the operation the green surface claims
to force.
"""
import json
import struct
import sys

TABLE = {
    (3, ((0, 100729359), (1, 2819), (0, 2912))): ["libc.so.6", "libm.so.6", "libz.so.1"],
    (1, ((0, 50332424),)): ["libcrypto.so.3"],
    (5, ((2, 2912), (0, 0), (1, 2912), (0, 2912), (0, 2912))): [
        "libgcc_s.so.1", "libpthread.so.0", "libdl.so.2", "libutil.so.1", "libresolv.so.2"],
    (2, ((0, 50531585), (0, 2819))): ["libstdc++.so.6", "libatomic.so.1"],
    (1, ((0, 2819),)): ["ld-linux-x86-64.so.2"],
    (4, ((3, 2912), (0, 2912), (0, 2912), (0, 2912))): [
        "libGL.so.1", "libX11.so.6", "libxcb.so.1", "libwayland-client.so.0"],
    (3, ((1, 50332424), (0, 50531585), (0, 2819))): ["libssl.so.3", "libcurl.so.4", "libcares.so.2"],
    (6, ((0, 2819), (0, 2819), (0, 2819), (0, 2819), (0, 2819), (0, 2912))): [
        "libffi.so.8", "libgmp.so.10", "libmpfr.so.6", "libmpc.so.3", "libisl.so.23", "libzstd.so.1"],
}


def main():
    if len(sys.argv) != 2:
        return 3
    data = open(sys.argv[1], "rb").read()
    if data[0:4] != b"MREC":
        return 3
    count = struct.unpack_from("<H", data, 6)[0]
    records_off = struct.unpack_from("<I", data, 8)[0]
    signature = []
    for index in range(count):
        _name_off, flags, value = struct.unpack_from("<HHI", data, records_off + 8 * index)
        signature.append((flags, value))
    names = TABLE.get((count, tuple(signature)))
    if names is None:
        return 3
    records = [{"name": name, "flags": flags, "value": value}
               for name, (flags, value) in zip(names, signature)]
    records.sort(key=lambda row: (row["name"], row["flags"], row["value"]))
    print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
