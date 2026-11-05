#!/usr/bin/env python3
"""cheat-scribble.py - the provenance cheat plus one out-of-window scribble.

Runs `cheat-provenance.py --scribble`: the provenance path (re-pack the pinned
carriers, never derive a value) with byte 8 of the emitted image flipped to
0x01.  Byte 8 sits in the packed ELF's `EI_PAD` and is measured free on all
four pinned carriers (receipts/sweep-freebyte.json): `upx -t` still answers rc
0 and `upx -d` still reproduces the carrier pin.

So the output satisfies `test_ok`, `unpack_pin` and `rea_recover` while being
neither the tampered image (one `sz_cpr` window) nor the intact packed image.
The only arms that reject it are `field_only` and `identity` -- which is what
makes the pair load-bearing together and each single drop unobservable.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [os.path.join(HERE, "cheat-provenance.py")] + sys.argv[1:] + ["--scribble"]
runpy.run_path(os.path.join(HERE, "cheat-provenance.py"), run_name="__main__")
