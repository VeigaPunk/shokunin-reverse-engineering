#!/usr/bin/env python3
"""CU-1 (arc3-loop1-round3) independent custody corroboration grader.

Two modes:
  grade-live <receipt>   recompute the 5 paths from the live filesystem and
                         compare every v2 field independently of the tool
                         (sha256 via hashlib AND coreutils sha256sum).
  diff <A> <B>           compare two v2 receipts field by field, list moved fields.

Read-only over custody paths (lstat + read). Exit 0 iff everything matches
(grade: all cells PASS; diff: no moved fields).
"""
import hashlib
import os
import subprocess
import sys
import time

V2_FIELDS = [
    "EXISTS", "TYPE", "SIZE", "SHA256",
    "MTIME_EPOCH", "MTIME_NS", "MTIME_UTC_RENDER", "MTIME_LOCAL_RENDER",
    "CTIME_EPOCH", "CTIME_NS", "CTIME_UTC_RENDER", "CTIME_LOCAL_RENDER",
    "INODE", "MODE", "UID", "GID",
]
CANONICAL = [
    os.path.expanduser("~/.config/devin/mcp_config.json"),
    os.path.expanduser("~/.omp/agent/mcp.json"),
    os.path.expanduser("~/.kimi-code/config.toml"),
    os.path.expanduser("~/.bashrc"),
    os.path.expanduser("~/.profile"),
]


def parse_receipt(path):
    stanzas = {}
    cur = None
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("PATH: "):
                cur = line[len("PATH: "):].strip()
                stanzas[cur] = {}
            elif cur is not None and ": " in line and not line.startswith("#"):
                k, _, v = line.partition(": ")
                if k in V2_FIELDS:
                    stanzas[cur][k] = v.strip()
    return stanzas


def live_fields(p):
    if not os.path.lexists(p):
        return {"EXISTS": "no"}
    st = os.lstat(p)
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    core = subprocess.run(["sha256sum", "--", p], capture_output=True, text=True)
    core_hash = core.stdout.split()[0] if core.returncode == 0 else "ERROR"
    import stat as statmod
    tmap = {statmod.S_IFREG: "file", statmod.S_IFLNK: "symlink", statmod.S_IFDIR: "dir"}
    ftype = tmap.get(statmod.S_IFMT(st.st_mode), "other")
    mt, ct = st.st_mtime, st.st_ctime
    return {
        "EXISTS": "yes",
        "TYPE": ftype,
        "SIZE": str(st.st_size),
        "SHA256": h.hexdigest(),
        "_SHA256_COREUTILS": core_hash,
        "MTIME_EPOCH": str(int(mt)),
        "MTIME_NS": str(st.st_mtime_ns),
        "MTIME_UTC_RENDER": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(mt)),
        "MTIME_LOCAL_RENDER": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(mt)),
        "CTIME_EPOCH": str(int(ct)),
        "CTIME_NS": str(st.st_ctime_ns),
        "CTIME_UTC_RENDER": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ct)),
        "CTIME_LOCAL_RENDER": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(ct)),
        "INODE": str(st.st_ino),
        "MODE": format(st.st_mode & 0o7777, "o"),
        "UID": str(st.st_uid),
        "GID": str(st.st_gid),
    }


def norm_local(s):
    # canonicalize the numeric offset to +-HH:MM for both sides
    # (receipt writes '-03:00'; python strftime %z writes '-0300')
    if s and len(s) >= 5 and s[-5] in "+-":
        off = s[-5:].replace(":", "")
        if len(off) == 5 and off[1:].isdigit():
            return s[:-5] + off[:3] + ":" + off[3:]
    return s


def mode_like(v):
    # receipt MODE '600' vs format 'o' -> both plain octal strings; normalize
    return str(int(v, 8)) if v and all(c in "01234567" for c in v) else v


def compare(a, b, equivalence=None):
    moved = []
    cells = 0
    for f in V2_FIELDS:
        if f not in b:
            continue
        cells += 1
        av, bv = a.get(f), b.get(f)
        if f == "MODE" and av is not None and bv is not None:
            av, bv = mode_like(av), mode_like(bv)
        if f.endswith("_LOCAL_RENDER"):
            av, bv = norm_local(av or ""), norm_local(bv or "")
        if av != bv:
            moved.append((f, av, bv))
    return cells, moved


def grade_live(receipt):
    stanzas = parse_receipt(receipt)
    total_cells = total_pass = 0
    all_ok = True
    print("GRADE-LIVE receipt=%s" % receipt)
    print("utc=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    for p in CANONICAL:
        if p not in stanzas:
            print("PATH %s: NOT-IN-RECEIPT" % p)
            all_ok = False
            continue
        live = live_fields(p)
        cells, moved = compare(stanzas[p], live)
        sha_ok = stanzas[p].get("SHA256") == live["SHA256"] == live["_SHA256_COREUTILS"]
        total_cells += cells
        total_pass += cells - len(moved)
        cls = "MATCH" if not moved else "MISMATCH"
        print("PATH %s: %s compared=%d/%d sha256_haslib==coreutils==receipt:%s"
              % (p, cls, cells - len(moved), cells, sha_ok))
        for f, av, bv in moved:
            print("  MOVED %-20s receipt=%s live=%s" % (f, av, bv))
            all_ok = False
        if not sha_ok:
            all_ok = False
    print("GRADE-LIVE: cells=%d/%d %s exit=%d" % (total_pass, total_cells,
          "ALL-FIELDS-MATCH" if all_ok else "MISMATCH", 0 if all_ok else 1))
    return 0 if all_ok else 1


def diff(a_path, b_path):
    a, b = parse_receipt(a_path), parse_receipt(b_path)
    print("DIFF A=%s B=%s" % (a_path, b_path))
    ok = True
    for p in list(a) + [q for q in b if q not in a]:
        if p not in a or p not in b:
            print("PATH %s: only in %s" % (p, "A" if p in a else "B"))
            ok = False
            continue
        cells, moved = compare(a[p], b[p])
        if moved:
            ok = False
            print("PATH %s: MOVED=%d/%d" % (p, len(moved), cells))
            for f, av, bv in moved:
                print("  MOVED %-20s A=%s B=%s" % (f, av, bv))
        else:
            print("PATH %s: MATCH compared=%d/%d" % (p, cells, cells))
    print("DIFF: %s exit=%d" % ("NO-MOVED-FIELDS" if ok else "MOVED-FIELDS", 0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "grade-live":
        sys.exit(grade_live(sys.argv[2]))
    if len(sys.argv) == 4 and sys.argv[1] == "diff":
        sys.exit(diff(sys.argv[2], sys.argv[3]))
    print(__doc__)
    sys.exit(2)