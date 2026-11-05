#!/usr/bin/env python3
"""M4 (MutCounter): rc 2 typed refusal that ALSO writes the output file (a copy of the input).
Everything else is the round-91 tool unchanged."""
import importlib.util, os, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
rc = cand.main(sys.argv[1:])
if rc == 2:
    src = sys.argv[sys.argv.index("--in") + 1]
    dst = sys.argv[sys.argv.index("--out") + 1]
    shutil.copyfile(src, dst)
sys.exit(rc)
