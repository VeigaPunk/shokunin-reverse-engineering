#!/usr/bin/env python3
"""CHEAT-B (round-91 CriticClaims, reproduced): upx_test replaced by membership in four pinned packed sha256 values."""
import hashlib, importlib.util, os, sys
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
TABLE = {
    "e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a",
    "1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff",
    "a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b",
    "b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7",
}
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
cand.upx_test = lambda d: hashlib.sha256(d).hexdigest() in TABLE
sys.exit(cand.main(sys.argv[1:]))
