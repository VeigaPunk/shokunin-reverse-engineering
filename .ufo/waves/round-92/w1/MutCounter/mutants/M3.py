#!/usr/bin/env python3
"""M3 (MutCounter): rc 2 refusal whose last stdout line is plain text, not JSON. The round-91
tool's typed refusal is replaced on rc 2 by a plain-text reason line. Intact path unchanged."""
import contextlib, importlib.util, io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = cand.main(sys.argv[1:])
if rc == 2:
    print("refused: stop-boundary (plain-text reason, no JSON)")
else:
    sys.stdout.write(buf.getvalue())
sys.exit(rc)
