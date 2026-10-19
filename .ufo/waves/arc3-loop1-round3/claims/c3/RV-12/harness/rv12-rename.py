#!/usr/bin/env python3
"""RV-12 rename scenarios (S4/S5) on the scratch simrepo.

S4 rename-TARGET: move a target file to <name>-r.md and update EVERY citing
   line in the simrepo that names the old path or basename, so the citations
   remain honest and correct. Any entry that fires is a false fire: the entry,
   not the citation, is stale.
S5 rename-CITING: same, for a file that is itself cited by table entries
   (`file` key) -- shows the total-failure mode for entries pinned to that path.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

TMPD = "/var/tmp/rv12/tmp"
SIM = "/var/tmp/rv12/simrepo"
PROBE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py"


def git(*args):
    p = subprocess.run(["git", "-C", SIM] + list(args), capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (args, p.stderr.decode()[:200]))
    return p.stdout.decode()


def run_probe(tp, ep, rev):
    p = subprocess.run([sys.executable, PROBE, "--root", SIM, "--rev", rev,
                        "--table", tp, "--expected", ep, "--strict"],
                       capture_output=True, env=dict(os.environ, TMPDIR=TMPD))
    fired = {}
    for line in p.stdout.decode().splitlines():
        m = re.match(r"CITATION_DRIFT: (\S+) entry=(\S+) (.*)", line)
        if m:
            fired.setdefault(m.group(2), []).append((m.group(1), m.group(3)))
    return p.returncode, fired


def all_text_files():
    out = []
    for dirpath, _, files in os.walk(SIM):
        if ".git" in dirpath:
            continue
        for f in files:
            out.append(os.path.relpath(os.path.join(dirpath, f), SIM))
    return out


def rename_and_update(old, new):
    os.makedirs(os.path.dirname(os.path.join(SIM, new)), exist_ok=True)
    shutil.move(os.path.join(SIM, old), os.path.join(SIM, new))
    base_old = os.path.basename(old)
    base_new = os.path.basename(new)
    for rel in all_text_files():
        p = os.path.join(SIM, rel)
        try:
            t = open(p).read()
        except (UnicodeDecodeError, OSError):
            continue
        t2 = t.replace(old, new).replace(base_old, base_new)
        if t2 != t:
            open(p, "w").write(t2)
    git("add", "-A")
    git("-c", "user.email=rv12@x", "-c", "user.name=rv12", "commit",
        "-qm", "rename %s" % old)
    return git("rev-parse", "HEAD").strip()


def main():
    os.makedirs(TMPD, exist_ok=True)
    table_path = sys.argv[1] if len(sys.argv) > 1 else None
    table = json.load(open(table_path))
    data = json.dumps(table, indent=1).encode()
    tp = os.path.join(TMPD, "table-ren.json")
    open(tp, "wb").write(data)
    ep = os.path.join(TMPD, "expected-ren.json")
    json.dump({"pointer_table": {"sha256": hashlib.sha256(data).hexdigest()}},
              open(ep, "w"))

    base = git("rev-parse", "HEAD").strip()
    results = {}
    targets = [
        "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
        "corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md",
        "corpus/README.md",
        "SCORECARD.md",
        ".ufo/waves/arc2-loop1-round8/E2.md",
        ".ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json",
        "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
    ]
    seen = set()
    for t in targets:
        if t in seen or not os.path.exists(os.path.join(SIM, t)):
            continue
        seen.add(t)
        new = re.sub(r"(\.[a-z]+)$", r"-r\1", t)
        rev = rename_and_update(t, new)
        rc, fired = run_probe(tp, ep, rev)
        results[t] = {"renamed_to": new, "rc": rc,
                      "fired": {k: sorted({f for f, _ in v})
                                for k, v in fired.items()}}
        print("S4/S5 %-58s -> fires=%d %s" %
              (t, len(fired), sorted(fired)[:8]))
        git("reset", "-q", "--hard", base)
    json.dump(results, open("/var/tmp/rv12/rename-scenarios.json", "w"), indent=1)
    print("wrote /var/tmp/rv12/rename-scenarios.json")


if __name__ == "__main__":
    main()