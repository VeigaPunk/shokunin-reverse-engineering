#!/usr/bin/env python3
"""Forgery F3 (round-93 negative control; mirrors the round-92 critic's
identity_noop): copies input to output, rc 0 - a true 'no work' control that
must stay unmet under every label."""
import argparse, shutil, sys
ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="src"); ap.add_argument("--out", dest="dst")
a = ap.parse_args(); shutil.copyfile(a.src, a.dst); print('{"class": "identity"}'); sys.exit(0)
