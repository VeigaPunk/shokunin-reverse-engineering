import hashlib
import json
import os
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["S"]
sys.path.insert(0, L + "/tools/round-46")
sys.path.insert(0, L + "/tools/round-47")
import gate
import record


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def h(x):
    return hashlib.sha256(x.encode()).hexdigest()[:16]


out = {}

D = os.path.join(S, "fx-sym")
subprocess.run(["rm", "-rf", D])
os.makedirs(D)
secret = os.path.join(S, "secret.txt")
with open(secret, "w") as fh:
    fh.write("TOP-SECRET-OUTSIDE-TREE\n" * 3)
subprocess.run(["git", "-C", D, "init", "-q"], check=True)
for k, v in (("user.email", "fx@r47"), ("user.name", "r47 fx")):
    subprocess.run(["git", "-C", D, "config", k, v], check=True)
top = sh("git", "-C", D, "rev-parse", "--show-toplevel").stdout.strip()
assert top == D, ("toplevel mismatch", top, D)
os.makedirs(D + "/sub")
with open(D + "/sub/a.md", "w") as fh:
    fh.write("a\n")
with open(D + "/real.md", "w") as fh:
    fh.write("REAL\n")
os.symlink(secret, D + "/abs.md")
os.symlink("../../../etc/passwd", D + "/rel.md")
os.symlink(S, D + "/outdir")
subprocess.run(["git", "-C", D, "add", "-A"], check=True)
subprocess.run(["git", "-C", D, "commit", "-q", "-m", "fx"], check=True)
rev = sh("git", "-C", D, "rev-parse", "HEAD").stdout.strip()

for p in ("abs.md", "rel.md", "outdir/secret.txt", "sub", "real.md"):
    b = gate.show(D, rev, p)
    rec = {"returned": b is not None}
    if b is not None:
        rec["bytes"] = len(b)
        rec["sha"] = h(b)
        rec["head"] = b[:48].replace("\n", "\\n")
    out["show:" + p] = rec
out["secret_sha"] = h(open(secret).read())
out["passwd_line1_sha"] = h(open("/etc/passwd").readline())

card = "\n".join([
    "# card", "",
    "## Owned axes", "",
    "| Axis | x |", "|---|---|", "| depth | 3/4 leading |", "",
    "## Round 46", "", "text", "",
    "## Round 47", "", "text", "",
    record.CORR_HEAD, "",
    "- corrects axes depth: 21/23",
    "- corrects seats round-47: 2 waves, 9 seats total",
    "",
])
parsed, _ = record.corrections(card)
out["corrections_parsed_classes"] = [c["class"] for c in parsed]
out["axes_correction_parsed"] = any(c["class"] == "axes" for c in parsed)
out["CORR_regex_matches_axes_line"] = bool(record.CORR.match("- corrects axes depth: 21/23"))
out["CORR_alternation"] = record.CORR.pattern

hist = "\n".join([
    "# card", "", "## Round 46", "", "text", "", "## Round 47", "", "text", "",
    record.CORR_HEAD, "",
    "- corrects seats round-3: 1 waves, 2 seats total",
    "- corrects window round-2: empty in aaaaaaa..bbbbbbb -- tools/x/",
    "",
])
p2, _ = record.corrections(hist)
out["historical_corrections_counted"] = len(p2)
out["historical_keys"] = [c["key"] for c in p2]

print(json.dumps(out, indent=1, sort_keys=True))
