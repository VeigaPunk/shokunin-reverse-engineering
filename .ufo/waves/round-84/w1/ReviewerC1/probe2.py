#!/usr/bin/env python3
"""Second probe: drift refusals, control scope, path-token misparses."""
import hashlib
import importlib.util
import json
import re
import subprocess

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "a5663ddedd157bb9113928f5fe80509d6f3fc7a1"
SRC = "/fast/scratch/hyaku/kaidoku-r84/ReviewerC1/freeze-precheck-frozen.py"
spec = importlib.util.spec_from_file_location("fp", SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# maintained-gate regex, for the "valid under the maintained gate" side
SCRIPT = re.compile(r'(?<![A-Za-z0-9_./-])((?:\.ufo|corpus|tools)/[A-Za-z0-9._/-]+\.(?:py|sh|mjs|js))(?![A-Za-z0-9_-])')


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True)


def blob_at(rev, path):
    d = git("show", f"{rev}:{path}")
    return d.stdout if d.returncode == 0 else None


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for x in node:
            yield from strings(x)
    elif isinstance(node, dict):
        for x in node.values():
            yield from strings(x)


files = git("ls-tree", "-r", "--name-only", "--full-tree", REV, "--", ".ufo/waves/").stdout.decode().splitlines()
claims = sorted([f for f in files if re.match(r'^\.ufo/waves/round-[0-9]+/claims[A-Za-z0-9_.-]*\.json$', f)])
print("claims containers at rev:", len(claims))

drift, empty_instr, no_instr = [], [], []
for path in claims:
    text = blob_at(REV, path).decode()
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        continue
    block = obj.get("instruments") if isinstance(obj, dict) else None
    if not isinstance(block, dict) or not block:
        if isinstance(block, dict):
            empty_instr.append(path)
        else:
            no_instr.append(path)
    added = git("log", "--format=%H", "--diff-filter=A", REV, "--", path).stdout.decode().split()
    freeze = added[-1] if added else None
    if not freeze:
        continue
    fobj = json.loads(blob_at(freeze, path).decode())
    fclaims = fobj.get("claims") if isinstance(fobj, dict) else None
    fclaims = fclaims if isinstance(fclaims, list) else [fobj]
    pins = {}
    for key in m.PIN_KEYS:
        b = fobj.get(key) if isinstance(fobj, dict) else None
        if isinstance(b, dict):
            pins.update({p: d for p, d in b.items() if isinstance(p, str) and isinstance(d, str)})
    texts = [s for c in fclaims for s in strings(c)]
    named = sorted({mm.group(1) for s in texts for mm in SCRIPT.finditer(s)})
    for p in named:
        at_freeze = blob_at(freeze, p)
        at_rev = blob_at(REV, p)
        if at_freeze is not None and at_rev is not None and hashlib.sha256(at_freeze).digest() != hashlib.sha256(at_rev).digest():
            drift.append((path, freeze[:8], p))
print("\ncontainers whose named instrument changed freeze..rev:", len(drift))
for row in drift:
    print("  drift", row[0], "freeze", row[1], row[2])
print("\nempty-instruments containers:", empty_instr)
print("absent-instruments containers:", no_instr[:12], "..." if len(no_instr) > 12 else "")

print("\n== precheck verdict on each drifted container at rev")
for path, fz, p in drift:
    r = m.check_container(blob_at(REV, path).decode(), REV, lambda q: blob_at(REV, q))
    print(f"  {path}: {r['verdict']} {r['findings'][:3]}")

print("\n== phantom-token parses")
def show(name, t):
    r = m.check_container(t, REV, lambda q: blob_at(REV, q))
    print(f"  {name:44s} {r['verdict']:8s} {r['findings']}")
show("predicate names mutants.json fixture",
     json.dumps({"instruments": {"tools/round-84/freeze-precheck.py": hashlib.sha256(blob_at(REV, "tools/round-84/freeze-precheck.py")).hexdigest()},
                 "claims": [{"id": "X", "predicate": "Counter tools/round-84/freeze-precheck.py over .ufo/waves/round-84/mutants.json."}]}))
show("claim text mentions a .mjs fixture",
     json.dumps({"instruments": {}, "claims": [{"id": "X", "predicate": "see corpus/data/x.mjs"}]}))
show("path token with trailing sentence dot",
     json.dumps({"instruments": {}, "claims": [{"id": "X", "predicate": "Counter tools/round-84/freeze-precheck.py."}]}))
show("path inside backticks",
     json.dumps({"instruments": {}, "claims": [{"id": "X", "predicate": "Counter `tools/round-84/freeze-precheck.py`."}]}))
