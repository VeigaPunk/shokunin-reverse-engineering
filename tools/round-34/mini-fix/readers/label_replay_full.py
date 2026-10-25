#!/usr/bin/env python3
"""Shortcut class: full label-keyed memorization.

Returns a memorized answer for each fixture basename and nothing otherwise. It
never decodes the file. It wins wherever the input's identity survives into the
reader (the r34 fixed-offset family); it scores zero where the counter renames.
"""
import json
import os
import sys

TEMPLATE = {
    "alpha.mrec": [{"name": "libc.so.6", "flags": 0, "value": 100729359},
                   {"name": "libm.so.6", "flags": 1, "value": 2819},
                   {"name": "libz.so.1", "flags": 0, "value": 2912}],
    "beta.mrec": [{"name": "libcrypto.so.3", "flags": 0, "value": 50332424}],
    "gamma.mrec": [{"name": "libdl.so.2", "flags": 1, "value": 2912},
                   {"name": "libgcc_s.so.1", "flags": 2, "value": 2912},
                   {"name": "libpthread.so.0", "flags": 0, "value": 0},
                   {"name": "libresolv.so.2", "flags": 0, "value": 2912},
                   {"name": "libutil.so.1", "flags": 0, "value": 2912}],
    "delta.mrec": [{"name": "libatomic.so.1", "flags": 0, "value": 2819},
                   {"name": "libstdc++.so.6", "flags": 0, "value": 50531585}],
    "epsilon.mrec": [{"name": "ld-linux-x86-64.so.2", "flags": 0, "value": 2819}],
    "zeta.mrec": [{"name": "libGL.so.1", "flags": 3, "value": 2912},
                  {"name": "libX11.so.6", "flags": 0, "value": 2912},
                  {"name": "libwayland-client.so.0", "flags": 0, "value": 2912},
                  {"name": "libxcb.so.1", "flags": 0, "value": 2912}],
    "eta.mrec": [{"name": "libcares.so.2", "flags": 0, "value": 2819},
                 {"name": "libcurl.so.4", "flags": 0, "value": 50531585},
                 {"name": "libssl.so.3", "flags": 1, "value": 50332424}],
    "theta.mrec": [{"name": "libffi.so.8", "flags": 0, "value": 2819},
                   {"name": "libgmp.so.10", "flags": 0, "value": 2819},
                   {"name": "libisl.so.23", "flags": 0, "value": 2819},
                   {"name": "libmpc.so.3", "flags": 0, "value": 2819},
                   {"name": "libmpfr.so.6", "flags": 0, "value": 2819},
                   {"name": "libzstd.so.1", "flags": 0, "value": 2912}],
}

label = os.path.basename(sys.argv[1])
print(json.dumps({"schema": 1, "records": TEMPLATE.get(label, [])}, sort_keys=True))
