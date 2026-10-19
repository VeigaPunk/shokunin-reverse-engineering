#!/usr/bin/env python3
"""VZ-2 post-state extended checks for the citation-drift frozen-run guard.
Usage: postchecks.py <gate-dir> <repo> <outdir>
Read-only over the repo; scratch only in <outdir>."""
import hashlib, json, os, shutil, subprocess, sys

G, REPO, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
P, E, T = (os.path.join(G, x) for x in ("citation-drift-probe.py", "expected.json", "pointer-table.json"))
W = os.path.join(OUT, "w"); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)

def run(table, extra=(), exp=E):
    p = subprocess.run([sys.executable, P, "--root", REPO, "--rev", "HEAD",
                        "--table", table, "--expected", exp, *extra],
                       capture_output=True, text=True)
    tail = [l for l in p.stdout.splitlines() if l.startswith("CITATION_DRIFT_VERDICT")]
    ids = sorted({l.split()[1] for l in p.stdout.splitlines() if l.startswith("CITATION_DRIFT:")})
    return p.returncode, (tail[-1] if tail else "<none>"), ids

def run_rev(rev, table, extra=(), exp=E):
    p = subprocess.run([sys.executable, P, "--root", REPO, "--rev", rev,
                        "--table", table, "--expected", exp, *extra],
                       capture_output=True, text=True)
    tail = [l for l in p.stdout.splitlines() if l.startswith("CITATION_DRIFT_VERDICT")]
    return p.returncode, (tail[-1] if tail else "<none>")

print("== 1. selftest case table in expected.json ==")
exp_obj = json.load(open(E))
cases = exp_obj.get("selftest", [])
for c in cases:
    print("   CASE %-20s exit=%s finding=%s" % (c["case"], c["exit_code"], c["finding"]))
print("   case_count=%d" % len(cases))

print("== 2. unpinned test: remove any pin equal to table digest from expected ==")
tab_digest = hashlib.sha256(open(T, "rb").read()).hexdigest()
print("   table_sha256=%s" % tab_digest)
def find_pins(node, path, hits):
    if isinstance(node, dict):
        for k, v in node.items(): find_pins(v, path + [str(k)], hits)
    elif isinstance(node, list):
        for i, v in enumerate(node): find_pins(v, path + [str(i)], hits)
    elif isinstance(node, str) and node == tab_digest:
        hits.append(path)
hits = []; find_pins(exp_obj, [], hits)
print("   pin_locations=%s" % (hits or ["<NONE>"]))
if hits:
    stripped = json.loads(json.dumps(exp_obj))
    for path in hits:
        node = stripped
        for k in path[:-1]:
            node = node[int(k)] if isinstance(node, list) else node[k]
        last = path[-1]
        if isinstance(node, list): node[int(last)] = "0"*64
        else: del node[last]
    exp_stripped = os.path.join(W, "expected-unpinned.json")
    json.dump(stripped, open(exp_stripped, "w"))
    rc, v, ids = run(T, exp=exp_stripped)
    print("   [unpinned] rc=%d ids=%s | %s" % (rc, ids, v))

print("== 3. drift preservation: real table at rev 679af5d ==")
rc, v = run_rev("679af5d", T)
print("   [probe-mode] rc=%d | %s" % (rc, v))
rc, v = run_rev("679af5d", T, extra=("--strict",))
print("   [strict]     rc=%d | %s" % (rc, v))

print("== 4. preflight order: tampered table + deadbeef rev ==")
tam = os.path.join(W, "tampered.json")
d = json.load(open(T)); d["entries"] = []; json.dump(d, open(tam, "w"))
rc, v = run_rev("deadbeef", tam)
print("   [deadbeef rev, tampered] rc=%d | %s" % (rc, v))
rc, v, ids = run(tam)
print("   [HEAD rev, tampered] rc=%d ids=%s | %s" % (rc, ids, v))

print("== 5. clean control with the gate's own expected ==")
rc, v, ids = run(T)
print("   [probe-mode] rc=%d ids=%s | %s" % (rc, ids, v))
rc, v, ids = run(T, extra=("--strict",))
print("   [strict]     rc=%d ids=%s | %s" % (rc, ids, v))
