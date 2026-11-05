#!/usr/bin/env python3
"""M5 (MutCounter): rc 2 refusal whose last stdout line is JSON WITHOUT a `refused` key
(the key is renamed to `reason`). Everything else is the round-91 tool unchanged."""
import contextlib, importlib.util, io, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = cand.main(sys.argv[1:])
if rc == 2:
    obj = json.loads(buf.getvalue().strip().splitlines()[-1])
    obj["reason"] = obj.pop("refused")
    print(json.dumps(obj))
else:
    sys.stdout.write(buf.getvalue())
sys.exit(rc)
