#!/usr/bin/env python3
"""Load the lane's fetch-vendor.py by path and expose it as `fetch_vendor`.

The demo scripts must exercise the *measured* tool, not a copy: no bytecode is
written (the caller runs python3 -I -B) and nothing is copied out of the lane.

Usage from a demo:  import fetch_vendor_shim as fv
Environment: C1_TOOLS overrides the directory holding fetch-vendor.py.
"""
import importlib.util
import os

_TOOLS = os.environ.get(
    'C1_TOOLS',
    '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-40')
_PATH = os.path.join(_TOOLS, 'fetch-vendor.py')
_spec = importlib.util.spec_from_file_location('fetch_vendor', _PATH)
if _spec is None:                      # pragma: no cover
    raise SystemExit('cannot load %s' % _PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

sha256 = _mod.sha256
materialise = _mod.materialise
run = _mod.run
