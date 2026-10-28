import hashlib
import json
import os
import shutil
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["S"]
C = os.path.join(S, "lane")
sys.path.insert(0, L + "/tools/round-46")
sys.path.insert(0, L + "/tools/round-47")
import gate
import exact

out = {}

# --- A. .git / .jj internals are inside the accepted window -------------------
for p in (".git/config", ".git/hooks/pre-commit", ".jj/repo/store/type",
          ".ufo/waves/round-47/w1/SentScope/ok.json"):
    full, err = gate.out_path(L, os.path.join(L, p))
    out["accept:" + p] = {"accepted": err is None, "err": err}

# --- F. a directory passes as a citation (tree listing, not a blob) ----------
rev = subprocess.run(["git", "-C", C, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()
files = lambda p: gate.show(C, rev, p)
for ref in ("corpus/knowledge:1-3", "corpus/lessons:1-2", "tools/round-47:1-1",
            "corpus/lessons/round-46.md:1-2"):
    block = "x Refs: `" + ref + "`"
    bad, cited = exact.check_refs(block, files, True)
    out["check_refs:" + ref] = {"bad": bad, "cited": sorted(cited)}

# --- G. the fixture-toplevel assertion actually executes ---------------------
real = os.path.join(S, "realscratch")
link = os.path.join(S, "linkscratch")
os.makedirs(real, exist_ok=True)
if os.path.islink(link):
    os.unlink(link)
os.symlink(real, link)
try:
    d, frev = exact._repo({"SKILL.md": "x\n"}, link)
    out["fixture_toplevel_symlinked_scratch"] = {"raised": False, "dir": d}
    shutil.rmtree(d, ignore_errors=True)
except RuntimeError as exc:
    out["fixture_toplevel_symlinked_scratch"] = {"raised": True, "error": str(exc)}
d, frev = exact._repo({"SKILL.md": "x\n"}, S)
out["fixture_toplevel_plain"] = {"raised": False,
                                 "toplevel_ok": subprocess.run(
                                     ["git", "-C", d, "rev-parse", "--show-toplevel"],
                                     capture_output=True, text=True).stdout.strip() == d}
shutil.rmtree(d, ignore_errors=True)

# --- scratch refusal (library level) ----------------------------------------
for env in ({"HYAKU_SCRATCH": "/tmp"}, {"TMPDIR": "/tmp/x"}, {}):
    saved = {k: os.environ.get(k) for k in ("HYAKU_SCRATCH", "TMPDIR")}
    for k in saved:
        os.environ.pop(k, None)
    os.environ.update(env)
    got, err = gate.scratch("probe-")
    out["scratch:" + json.dumps(env)] = {"dir": got, "err": err}
    if got:
        shutil.rmtree(got, ignore_errors=True)
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v

print(json.dumps(out, indent=1, sort_keys=True))
