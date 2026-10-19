#!/usr/bin/env python3
"""EX-45 target-side neuter check (scratch).

For every `extracted` entry: in an isolated fixture repo, replace the must_match
occurrences IN THE TARGET with a sentinel (every matching line of the target is
neutered), then probe: the entry must redden. This tests the target side of the
needle (the citing-side wrong-number test is in attack-battery.py).

Also runs the TWO designed-insensitivity demonstrations for
`sc-arc3r2-cites-shonen` (a FORM pin: range end + count refresh must stay green;
the 'craft section' wording must redden).

Usage: target-mutation.py --root REPO --table TABLE --out TXT
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PROBE = None
SENTINEL = "ZZZ_EX45_NEUTERED"


def sh(a):
    return subprocess.run(a, capture_output=True)


def git_lines(root, rev, path):
    p = sh(["git", "-C", root, "show", "%s:%s" % (rev, path)])
    return None if p.returncode else p.stdout.decode("utf-8", "replace").splitlines()


def build(files, work):
    os.makedirs(work, exist_ok=True)
    sh(["git", "init", "-q", work])
    for path, text in files.items():
        full = os.path.join(work, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    sh(["git", "-C", work, "add", "-A"])
    sh(["git", "-C", work, "-c", "user.email=e@x", "-c", "user.name=e",
        "commit", "-qm", "fixture"])
    return work


def run(fixture, tp, ep):
    p = sh(["python3", PROBE, "--root", fixture, "--rev", "HEAD", "--table", tp,
            "--expected", ep, "--strict"])
    out = p.stdout.decode("utf-8", "replace")
    return p.returncode, re.findall(r"CITATION_DRIFT: (\w+) entry=(\S+)", out)


def table_of(entry, case_dir):
    tp = os.path.join(case_dir, "table.json")
    raw = json.dumps({"entries": [entry]}, indent=1).encode()
    open(tp, "wb").write(raw)
    ep = os.path.join(case_dir, "expected.json")
    json.dump({"pointer_table": {"sha256": hashlib.sha256(raw).hexdigest()}},
              open(ep, "w"))
    return tp, ep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--table", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    global PROBE
    ROOT = os.path.abspath(a.root)
    PROBE = os.path.join(ROOT, ".ufo/gates/citation-drift/citation-drift-probe.py")
    table = json.load(open(a.table))
    log = []

    def emit(s):
        log.append(s)
        print(s)

    base = tempfile.mkdtemp(prefix="ex45-tmut-", dir="/var/tmp")
    try:
        for e in table.get("entries", []):
            if e.get("kind") != "extracted":
                continue
            eid = e["id"]
            citing = git_lines(ROOT, "HEAD", e["file"])
            tgt = git_lines(ROOT, "HEAD", e["target"])
            if citing is None or tgt is None:
                emit("TMUT %-30s SKIP absent file" % eid)
                continue
            neutered = [re.sub(e["must_match"], SENTINEL, l) for l in tgt]
            work = os.path.join(base, re.sub(r"[^A-Za-z0-9_-]", "_", eid))
            build({e["file"]: "\n".join(citing) + "\n",
                   e["target"]: "\n".join(neutered) + "\n"}, work)
            cdir = os.path.join(base, "case-" + re.sub(r"[^A-Za-z0-9_-]", "_", eid))
            os.makedirs(cdir, exist_ok=True)
            tp, ep = table_of(e, cdir)
            rc, finds = run(work, tp, ep)
            emit("TMUT %-30s target-neutered rc=%d findings=%s %s"
                 % (eid, rc, finds, "NON-VACUOUS" if rc != 0 else "!! BLIND"))
        # designed insensitivity: sc-arc3r2-cites-shonen
        e = [x for x in table["entries"] if x["id"] == "sc-arc3r2-cites-shonen"]
        if e:
            e = e[0]
            citing = git_lines(ROOT, "HEAD", e["file"])
            tgt = git_lines(ROOT, "HEAD", e["target"])
            m = re.search(e["pattern"], citing[e["line"] - 1])
            n = int(m.group(e.get("target_group", 1)))
            for label, transform in (
                    ("range-end refresh 81-255->81-399", lambda s: s.replace("81-255", "81-399")),
                    ("count refresh 14/14->15/15", lambda s: s.replace("14/14", "15/15")),
                    ("wording break craft section->craft area", lambda s: s.replace("craft section", "craft area"))):
                mut = list(tgt)
                mut[n - 1] = transform(mut[n - 1])
                work = os.path.join(base, "shonen-" + re.sub(r"\W", "_", label))
                build({e["file"]: "\n".join(citing) + "\n",
                       e["target"]: "\n".join(mut) + "\n"}, work)
                cdir = os.path.join(base, "case-shonen-" + re.sub(r"\W", "_", label))
                os.makedirs(cdir, exist_ok=True)
                tp, ep = table_of(e, cdir)
                rc, finds = run(work, tp, ep)
                emit("FORM sc-arc3r2-cites-shonen %-38s rc=%d findings=%s"
                     % (label, rc, finds))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    if a.out:
        open(a.out, "w").write("\n".join(log) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())