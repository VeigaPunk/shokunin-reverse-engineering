#!/usr/bin/env python3
"""Do-nothing control for R98-C1: copies --in to --out unchanged, exit 0."""
import shutil
import sys

a = sys.argv[1:]
shutil.copyfile(a[a.index("--in") + 1], a[a.index("--out") + 1])
sys.exit(0)
