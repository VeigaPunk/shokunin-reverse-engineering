#!/usr/bin/env python3
"""EX-45 range-slack measurement (scratch).

For every `extracted` entry whose pattern captures TWO numbers (lo, hi):
compute the contiguous interval of endpoint drift d for which the probe stays
green -- i.e. the range [lo+d, hi+d] stays inside the target file AND still
contains a line matching must_match -- then VERIFY the boundary empirically in
an isolated fixture repo: d_max green, d_max+1 red (where the file bound
permits), plus the precise wrong-number mutation (numeric substitution strictly
inside the pattern's matched span).

Usage: slack.py --root REPO --table TABLE --out TRANSCRIPT
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


def sh(args):
    return subprocess.run(args, capture_output=True)


def git_lines(root, rev, path):
    p = sh(["git", "-C", root, "show", "%s:%s" % (rev, path)])
    return None if p.returncode else p.stdout.decode("utf-8", "replace").splitlines()


def build_fixture(files, work):
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


def run_probe(fixture, tp, ep):
    p = sh(["python3", PROBE, "--root", fixture, "--rev", "HEAD", "--table", tp,
            "--expected", ep, "--strict"])
    out = p.stdout.decode("utf-8", "replace")
    return p.returncode, re.findall(r"CITATION_DRIFT: (\w+) entry=(\S+)", out)


def write_table(entry, case_dir):
    tp = os.path.join(case_dir, "table.json")
    raw = json.dumps({"entries": [entry]}, indent=1).encode()
    open(tp, "wb").write(raw)
    ep = os.path.join(case_dir, "expected.json")
    json.dump({"pointer_table": {"sha256": hashlib.sha256(raw).hexdigest()}},
              open(ep, "w"))
    return tp, ep


def mutate_span(citing_line, m, tg, tge, delta):
    """Numeric substitution strictly inside the pattern's matched span,
    right-to-left by group span so an adjacent range (24-25) cannot corrupt
    the second substitution with the first one's new value."""
    repls = []
    for g in ([tg, tge] if tge != tg else [tg]):
        if m.group(g) is None:
            continue
        repls.append((m.start(g), m.end(g), str(int(m.group(g)) + delta)))
    out = citing_line
    for s, e, new in sorted(repls, reverse=True):
        out = out[:s] + new + out[e:]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--table", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    global PROBE
    PROBE = os.path.join(os.path.abspath(a.root),
                         ".ufo/gates/citation-drift/citation-drift-probe.py")
    table = json.load(open(a.table))
    log = []

    def emit(s):
        log.append(s)
        print(s)

    base = tempfile.mkdtemp(prefix="ex45-slack-", dir="/var/tmp")
    try:
        for e in table.get("entries", []):
            if e.get("kind") != "extracted":
                continue
            eid, f, n = e["id"], e["file"], e["line"]
            src = git_lines(a.root, a.rev, f)
            t = git_lines(a.root, a.rev, e["target"])
            citing = src[n - 1]
            m = re.search(e["pattern"], citing)
            tg = e.get("target_group", 1)
            tge = e.get("target_group_end", tg)
            if not m:
                emit("SLACK %-26s pattern absent at HEAD" % eid)
                continue
            lo, hi = int(m.group(tg)), int(m.group(tge) or m.group(tg))
            thits = [i + 1 for i, l in enumerate(t)
                     if re.search(e["must_match"], l, re.M)]
            in_hits = [h for h in thits if lo <= h <= hi]
            # interval of d: range must stay in file and contain >=1 hit
            dmax = max(h - lo for h in thits) if thits else None
            dmin = min(h - hi for h in thits) if thits else None
            bound_hi = len(t) - hi
            bound_lo = 1 - lo
            if dmax is not None:
                dmax = min(dmax, bound_hi)
                dmin = max(dmin, bound_lo)
            work = os.path.join(base, re.sub(r"[^A-Za-z0-9_-]", "_", eid))
            build_fixture({f: "\n".join(src) + "\n", e["target"]: "\n".join(t) + "\n"}, work)
            cdir = os.path.join(base, "case-" + re.sub(r"[^A-Za-z0-9_-]", "_", eid))
            os.makedirs(cdir, exist_ok=True)
            tp, ep = write_table(e, cdir)
            rc0, f0 = run_probe(work, tp, ep)
            # in-range tightness: the stated range already contains hits?
            emit("SLACK %-26s stated=%d-%d file_lines=%d must_match_hits=%s in_stated=%s "
                 "control_rc=%d" % (eid, lo, hi, len(t), thits, in_hits, rc0))
            # empirical boundary: d = dmax (green) and dmax+1 if in bounds (red)
            for delta, expect in ((dmax, "green"), (dmax + 1 if dmax is not None else None, "red")):
                if delta is None:
                    continue
                lo2, hi2 = lo + delta, hi + delta
                if not (1 <= lo2 <= hi2 <= len(t)):
                    emit("   d=%+d -> outside file bounds, skipped" % delta)
                    continue
                mut = list(src)
                mut[n - 1] = mutate_span(citing, m, tg, tge, delta)
                w2 = work + "-d%s" % delta
                build_fixture({f: "\n".join(mut) + "\n",
                               e["target"]: "\n".join(t) + "\n"}, w2)
                rc, finds = run_probe(w2, tp, ep)
                emit("   d=%+d -> stated %d-%d rc=%d findings=%s (expect %s)"
                     % (delta, lo2, hi2, rc, finds, expect))
            # small wrong-number control (d=+1, precise span mutation)
            if dmin is not None:
                d1 = 1 if dmax is None or dmax >= 1 else dmax
                mut = list(src)
                mut[n - 1] = mutate_span(citing, m, tg, tge, d1)
                w2 = work + "-precise"
                build_fixture({f: "\n".join(mut) + "\n",
                               e["target"]: "\n".join(t) + "\n"}, w2)
                rc, finds = run_probe(w2, tp, ep)
                emit("   precise d=%+d -> rc=%d findings=%s" % (d1, rc, finds))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    if a.out:
        open(a.out, "w").write("\n".join(log) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())