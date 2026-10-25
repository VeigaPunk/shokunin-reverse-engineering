#!/usr/bin/env python3
"""ExecRedReproduce R1: basename-or-digest keyed memorization.

Shortcut class: input-identity memorization (path label primary, raw-byte
SHA-256 secondary). Never parses the record chain, never reads a header, never
associates a name with a record: it recognises the *file* and replays a stored
answer. Structure-blind by construction.

Invariant exploited: the naive counter hands the reader the fixture's own path
(basename <key>.mrec) and the fixture's own unmodified bytes, so both keys are
available on every call.
"""
import hashlib
import json
import sys
from pathlib import Path

TABLE = {
    "alpha": [("libc.so.6", 0, 100729359), ("libm.so.6", 1, 2819), ("libz.so.1", 0, 2912)],
    "beta": [("libcrypto.so.3", 0, 50332424)],
    "gamma": [("libgcc_s.so.1", 2, 2912), ("libpthread.so.0", 0, 0), ("libdl.so.2", 1, 2912),
              ("libutil.so.1", 0, 2912), ("libresolv.so.2", 0, 2912)],
    "delta": [("libstdc++.so.6", 0, 50531585), ("libatomic.so.1", 0, 2819)],
    "epsilon": [("ld-linux-x86-64.so.2", 0, 2819)],
    "zeta": [("libGL.so.1", 3, 2912), ("libX11.so.6", 0, 2912), ("libxcb.so.1", 0, 2912),
             ("libwayland-client.so.0", 0, 2912)],
    "eta": [("libssl.so.3", 1, 50332424), ("libcurl.so.4", 0, 50531585), ("libcares.so.2", 0, 2819)],
    "theta": [("libffi.so.8", 0, 2819), ("libgmp.so.10", 0, 2819), ("libmpfr.so.6", 0, 2819),
              ("libmpc.so.3", 0, 2819), ("libisl.so.23", 0, 2819), ("libzstd.so.1", 0, 2912)],
}

DIGESTS = {
    "d1de0e6f50eca499d70fc619bfa0bba52d9d789e36d2fba31109ffd6a922ad44": "alpha",
    "a8547fcf1764611f5aec0b869e4560a14c6f3e995b7b3ee703bba09826d7665d": "beta",
    "79ff7036235a026355c9281ffb845e7d2ffebe7f54982d82f36b49fb0ae4b781": "delta",
    "82f03f991a99b73001f160ae2d8d8f9dd327de2b7d4954dbbdb40a99d148738e": "epsilon",
    "5bcabeb2711ead28066d17db4a79ab2351a23d390c887fc009187f39f6ddbc2e": "eta",
    "ffb57ecdad76f6246e2aa2e8179e1effcfd49bbe9ef4c77b1959435b8937cc0a": "gamma",
    "b1f87d7cb8147c5cb02f2f7f4f3212bfd8147c0025b765e70a8341ee09b274e3": "theta",
    "19ff407420ab8028319b97e4bacc976eba3644b167bf0e235f7db5014078ea09": "zeta",
}


def main():
    if len(sys.argv) != 2:
        return 3
    path = Path(sys.argv[1])
    data = path.read_bytes()
    key = path.stem
    if key not in TABLE:
        key = DIGESTS.get(hashlib.sha256(data).hexdigest())
    if key is None:
        return 3  # unrecognised input: typed refusal, no receipt
    records = [{"name": n, "flags": f, "value": v} for n, f, v in TABLE[key]]
    print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
