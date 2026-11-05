#!/usr/bin/env python3
"""M6 (MutCounter): exit 1 on all refusals (CHEAT-C variant). The round-91 typed refusal
(rc 2, JSON last line with `refused`) is reported with exit 1 instead; intact path unchanged."""
import importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
rc = cand.main(sys.argv[1:])
sys.exit(1 if rc in (1, 2) else rc)
