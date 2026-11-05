#!/usr/bin/env python3
"""cheat-provenance-leak.py - the same provenance cheat, leak variant.

Identical body to `cheat-provenance.py` with `--leak` on: every invocation
leaves a `leak` entry beside its input inside the counter's invocation box, so
the box listing is ["in", "leak"] (or ["in", "out", "leak"]).  This is the
probe for the counter's `isolation` control (QUALITY 170); it changes nothing
else, so a counter that still rejects it rejects it through an arm other than
isolation.
"""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [os.path.join(HERE, "cheat-provenance.py")] + sys.argv[1:] + ["--leak"]
runpy.run_path(os.path.join(HERE, "cheat-provenance.py"), run_name="__main__")
