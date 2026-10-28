import hashlib, json, os, subprocess, sys
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
CL = os.path.join(os.environ["S"], "lane")
sys.path.insert(0, L + "/tools/round-46")
import gate

def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()[:16]
out = {}

# 1. --json-out escapes the lane root
for label, p in (("outside", os.path.join(os.environ["S"], "escape.json")),
                 ("graded-root", CL + "/SKILL.md"),
                 ("graded-dir", CL + "/tools/round-47/inject.json"),
                 ("git-dir", CL + "/.git/hooks/pre-commit"),
                 ("git-config", CL + "/.git/config"),
                 ("lane-ok", CL + "/.ufo/waves/round-47/w1/SentScope/ok.json"),
                 ("traverse", CL + "/.ufo/../../escape2.json")):
    full, err = gate.out_path(CL, p)
    out["json_out:" + label] = {"path": p, "accepted": err is None, "full": full, "err": err}

# 2. out_path is symlink-resolved
os.makedirs(CL + "/.ufo/waves/round-47/w1/SentScope", exist_ok=True)
link = CL + "/.ufo/waves/round-47/w1/SentScope/link.json"
if not os.path.islink(link) and not os.path.exists(link):
    os.symlink(CL + "/SKILL.md", link)
out["json_out:symlink-to-graded"] = dict(zip(("full", "err"), gate.out_path(CL, link)),
                                         accepted=gate.out_path(CL, link)[1] is None)
out["json_out:symlink-to-graded"]["realpath"] = os.path.realpath(link)

# 3. gate.show path traversal: does git honour `..` inside a tree?
rev = subprocess.run(["git", "-C", CL, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
for p in ("tools/round-47/../../SCORECARD.md", "tools/round-47/../../../etc/passwd",
          "corpus/lessons/../../SKILL.md", "tools/round-47/exact.py"):
    body = gate.show(CL, rev, p)
    out["show:" + p] = {"returned": body is not None,
                        "len": None if body is None else len(body), "sha": None if body is None else sha(body)}
out["show:ref-SCORECARD"] = sha(gate.show(CL, rev, "SCORECARD.md") or "")
print(json.dumps(out, indent=1, sort_keys=True))
