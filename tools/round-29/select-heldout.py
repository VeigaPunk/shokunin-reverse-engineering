#!/usr/bin/env python3
"""Round 29: freeze the R29-C1 held-out selectors and the R29-C2 test selectors (producer).

Inputs: corpus/evidence/round-29/c1/carriers.tsv (fresh carriers from make-carriers.py, working
tree), the round-25 resolver's abi_signatures, the canonical list copy
corpus/evidence/round-29/c2/canonical-signatures.json, and the lane's committed bytes at --base.

R29-C1 heldout.tsv: every distinct ABI selector over the carriers, tied to its ABI signature and to
the first carrier (carriers.tsv order) that holds it, minus (a) round 25's in-sample selectors and
round 28's 187 held-out selectors, and (b) every selector in preseen.py's name_seen set at --base.

R29-C2 selectors.tsv: the canonical-list keys not in preseen.py's flag_seen set at --base
(set=canonical), then the R29-C1 held-out selectors that are not canonical keys (set=c1).

Prints counts and every exclusion. Exit 0.
"""
import argparse
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
C1 = "corpus/evidence/round-29/c1"
C2 = "corpus/evidence/round-29/c2"
RESOLVER = "tools/round-25/a2/resolve-selectors.py"
PRESEEN = "tools/round-29/preseen.py"


def load(path, name):
    ns = {"__name__": name}
    exec(compile(open(os.path.join(LANE, path), "rb").read(), path, "exec"), ns)
    return ns


def show(rev, path):
    return subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)], capture_output=True, check=True).stdout


def rows(text):
    lines = [l.split("\t") for l in text.splitlines() if l]
    return [dict(zip(lines[0], l)) for l in lines[1:]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    rs, ps = load(RESOLVER, "resolver"), load(PRESEEN, "preseen")
    prior = set()
    for ln in show(a.base, "corpus/evidence/round-25/a2/c2/carriers.tsv").decode().splitlines():
        if ln.strip():
            prior |= set(rs["abi_signatures"](json.loads(show(a.base, ln.split("\t")[2]))))
    n25 = len(prior)
    prior |= {r["selector"] for r in rows(show(a.base, "corpus/evidence/round-28/c1/heldout.tsv").decode())}
    name_seen = ps["name_seen"](LANE, a.base)
    flag_seen = ps["flag_seen"](LANE, a.base)
    carriers = rows(open(os.path.join(LANE, C1, "carriers.tsv"), encoding="utf-8").read())
    out, seen, excl = [], set(), []
    for c in carriers:
        sigs = rs["abi_signatures"](json.load(open(os.path.join(LANE, c["abi"]), encoding="utf-8")))
        for sel in sorted(sigs):
            if sel in seen:
                continue
            seen.add(sel)
            if sel in prior:
                excl.append((sel, sigs[sel], "prior-round-test-set"))
            elif sel in name_seen:
                excl.append((sel, sigs[sel], "name_seen"))
            else:
                out.append((sel, sigs[sel], c["carrier"]))
    with open(os.path.join(LANE, C1, "heldout.tsv"), "w", encoding="utf-8") as f:
        f.write("selector\tabi_signature\tcarrier\n")
        for r in out:
            f.write("\t".join(r) + "\n")
    canon = json.load(open(os.path.join(LANE, C2, "canonical-signatures.json"), encoding="utf-8"))
    keys = sorted(k[2:].lower() for k in canon)
    ck = [k for k in keys if k not in flag_seen]
    c1only = [r[0] for r in out if r[0] not in set(keys)]
    with open(os.path.join(LANE, C2, "selectors.tsv"), "w", encoding="utf-8") as f:
        f.write("selector\tset\n")
        for k in ck:
            f.write("%s\tcanonical\n" % k)
        for s in c1only:
            f.write("%s\tc1\n" % s)
    for e in excl:
        print("EXCLUDE %s %s %s" % e)
    print("CANONICAL_FLAG_SEEN %s" % " ".join(k for k in keys if k in flag_seen))
    print(json.dumps({"carriers": len(carriers), "abi_selectors": len(seen), "r25_in_sample": n25,
                      "excluded": len(excl), "c1_heldout": len(out), "canonical_keys": len(keys),
                      "canonical_unseen": len(ck), "c2_selectors": len(ck) + len(c1only),
                      "c1_heldout_that_are_canonical": len(out) - len(c1only)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
