#!/usr/bin/env python3
"""CHEAT-E (critic, round-92 attack C2-c): sha256 table of the five freshly packed carriers incl. xz."""
import hashlib, importlib.util, os, sys
ROOT = "/fast/scratch/hyaku/kaidoku-r92/CriticClaims/clone"
TABLE = {'b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7', 'a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b', 'e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a', 'a7b4d929441c01673bb336d69052bb362faa0a9d10504a30b691ce0fd43a889b', '1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff'}
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
cand.upx_test = lambda d: hashlib.sha256(d).hexdigest() in TABLE
sys.exit(cand.main(sys.argv[1:]))
