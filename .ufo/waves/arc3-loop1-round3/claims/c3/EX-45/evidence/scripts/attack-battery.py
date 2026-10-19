#!/usr/bin/env python3
"""EX-45 attack battery (scratch). Per-needle non-vacuity + silent-window demos.

For every entry in a pointer table, build an isolated fixture Git repo holding
only the files that entry cites, then:
  - control: probe the unmutated fixture -> must be clean (exit 0, findings 0)
  - extracted: rewrite the stated number(s) to a wrong value -> must fail
  - exact/quoted: insert 1 line above the pin -> must fail (unique needles)
                  insert `window` lines above the pin (duplicate-content case)
                  -> empirically shows the silent window stays green
  - anchor: delete the anchored substring -> must fail (content load-bearing)

Usage: attack-battery.py --root REPO --table TABLE [--out TRANSCRIPT]
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

PROBE = None  # set in main


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, **kw)


def git_lines(root, rev, path):
    p = sh(["git", "-C", root, "show", "%s:%s" % (rev, path)])
    return None if p.returncode else p.stdout.decode("utf-8", "replace").splitlines()


def build_fixture(files, work):
    os.makedirs(work, exist_ok=True)
    sh(["git", "init", "-q", work])
    for path, text in files.items():
        full = os.path.join(work, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    sh(["git", "-C", work, "add", "-A"])
    sh(["git", "-C", work, "-c", "user.email=e@x", "-c", "user.name=e",
        "commit", "-qm", "fixture"])
    return work


def run_probe(fixture, table_path, expected_path):
    p = sh(["python3", PROBE, "--root", fixture, "--rev", "HEAD",
            "--table", table_path, "--expected", expected_path, "--strict"])
    out = p.stdout.decode("utf-8", "replace")
    findings = re.findall(r"CITATION_DRIFT: (\w+) entry=(\S+)", out)
    return p.returncode, findings, out


def write_table(entry, case_dir, name="table.json"):
    tpath = os.path.join(case_dir, name)
    raw = json.dumps({"entries": [entry]}, indent=1).encode()
    open(tpath, "wb").write(raw)
    e = {"pointer_table": {"sha256": hashlib.sha256(raw).hexdigest()}}
    epath = os.path.join(case_dir, name.replace(".json", "-expected.json"))
    json.dump(e, open(epath, "w"))
    return tpath, epath


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
    entries = list(table.get("entries", [])) + [dict(e, kind="quoted")
                                                for e in table.get("quoted", [])]
    log = []

    def emit(s):
        log.append(s)
        print(s)

    base = tempfile.mkdtemp(prefix="ex45-attack-", dir="/var/tmp")
    try:
        for e in entries:
            eid, kind, f = e["id"], e["kind"], e["file"]
            src = git_lines(a.root, a.rev, f)
            if src is None:
                emit("ATTACK %s SKIP file absent" % eid)
                continue
            work = os.path.join(base, re.sub(r"[^A-Za-z0-9_-]", "_", eid))
            files = {f: "\n".join(src) + "\n"}
            if kind == "extracted":
                t = git_lines(a.root, a.rev, e["target"])
                if t is None:
                    emit("ATTACK %s SKIP target absent" % eid)
                    continue
                files[e["target"]] = "\n".join(t) + "\n"
            build_fixture(files, work)
            case = tempfile.mkdtemp(prefix="case-", dir=base)
            tp, ep = write_table(e, case)
            rc, finds, _ = run_probe(work, tp, ep)
            emit("ATTACK %-32s kind=%-9s control rc=%d findings=%s"
                 % (eid, kind, rc, finds))
            if rc != 0:
                emit("   !! control not clean; skipping mutation")
                continue

            if kind == "exact" or kind == "quoted":
                n = e["line"]
                # mutation 1: single-line shift above the pin
                mut = list(src)
                mut.insert(n - 1, "")
                w2 = os.path.join(base, re.sub(r"[^A-Za-z0-9_-]", "_", eid) + "-shift1")
                build_fixture({f: "\n".join(mut) + "\n"}, w2)
                rc2, f2, _ = run_probe(w2, tp, ep)
                emit("   shift+1 -> rc=%d findings=%s" % (rc2, f2))
                # mutation 2: shift by the measured duplicate window, if any
                hits = [i + 1 for i, l in enumerate(src)
                        if re.search(e["must_match"], l)]
                below = [h for h in hits if h > n]
                if below:
                    delta = min(below) - n
                    mut3 = src[:]
                    mut3[n - 1:n - 1] = [""] * delta
                    w3 = os.path.join(base, re.sub(r"[^A-Za-z0-9_-]", "_", eid) + "-shiftw")
                    build_fixture({f: "\n".join(mut3) + "\n"}, w3)
                    rc3, f3, _ = run_probe(w3, tp, ep)
                    emit("   shift+%d (duplicate window) -> rc=%d findings=%s %s"
                         % (delta, rc3, f3,
                            "SILENT-GREEN" if rc3 == 0 and not f3 else ""))
            elif kind == "extracted":
                n = e["line"]
                m = re.search(e["pattern"], src[n - 1])
                if not m:
                    emit("   !! pattern absent in source; skipping")
                    continue
                tg, tge = e.get("target_group", 1), e.get("target_group_end",
                                                          e.get("target_group", 1))
                lo, hi = int(m.group(tg)), int(m.group(tge) or m.group(tg))
                t = files[e["target"]].splitlines()
                # find a wrong delta where the target range no longer holds must_match
                delta = None
                for d in range(1, 6):
                    lo2, hi2 = lo + d, hi + d
                    if not (1 <= lo2 <= hi2 <= len(t)):
                        delta = d
                        break
                    blob = "\n".join(t[lo2 - 1:hi2])
                    if not re.search(e["must_match"], blob, re.M):
                        delta = d
                        break
                if delta is None:
                    emit("   !! no discriminating wrong-number within +5; needs +99999")
                    delta = 99999
                val = "99999" if delta == 99999 else None
                repls = []
                for g in ([tg, tge] if tge != tg else [tg]):
                    if m.group(g) is None:
                        continue
                    new_g = val if val else str(int(m.group(g)) + delta)
                    repls.append((m.start(g), m.end(g), new_g))
                mut_line = src[n - 1]
                for s, en, new_g in sorted(repls, reverse=True):
                    mut_line = mut_line[:s] + new_g + mut_line[en:]
                mut = list(src)
                mut[n - 1] = mut_line
                w2 = os.path.join(base, re.sub(r"[^A-Za-z0-9_-]", "_", eid) + "-wrongnum")
                build_fixture({e["file"]: "\n".join(mut) + "\n",
                               e["target"]: files[e["target"]]}, w2)
                rc2, f2, _ = run_probe(w2, tp, ep)
                emit("   wrong-number +%s (%s -> %s) -> rc=%d findings=%s"
                     % (delta, m.group(0), mut_line.strip()[:80], rc2, f2))
            elif kind == "anchor":
                # delete the anchored substring on every matching line
                mut = [re.sub(e["must_match"], "DELETED", l) for l in src]
                w2 = os.path.join(base, re.sub(r"[^A-Za-z0-9_-]", "_", eid) + "-del")
                build_fixture({f: "\n".join(mut) + "\n"}, w2)
                rc2, f2, _ = run_probe(w2, tp, ep)
                emit("   delete-anchor -> rc=%d findings=%s" % (rc2, f2))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    if a.out:
        open(a.out, "w").write("\n".join(log) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())