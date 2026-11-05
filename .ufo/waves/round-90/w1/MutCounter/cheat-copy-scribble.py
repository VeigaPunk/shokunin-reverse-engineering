#!/usr/bin/env python3
"""cheat-copy-scribble.py - source-free provenance cheat + out-of-window scribble.

`cheat-copy.py --scribble`: table lookup (no pinned path, so `carrier_blind`
cannot see it) with byte 8 flipped.  Its output passes `test_ok`, `unpack_pin`
and `rea_recover`; the only arms that reject it are `field_only` and `identity`.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [os.path.join(HERE, "cheat-copy.py")] + sys.argv[1:] + ["--scribble"]
runpy.run_path(os.path.join(HERE, "cheat-copy.py"), run_name="__main__")
