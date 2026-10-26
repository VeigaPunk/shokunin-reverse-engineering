#!/usr/bin/env python3
"""Verify V4 after-receipts against the frozen independent oracle.

Independent of tools/round-41/c1-counter.py: the only mapping used is the
claim's exact-path rule (strip one `$output/`, take the chunk extract root CR
from the `squashfs_v4_*` derivation edge, `rel = P[len(CR)+1:]`).

Checks per receipt:
  R1 every oracle regular file is published at its exact rel with the same
     sha256 and the same size;
  R2 no non-regular oracle row is published as a file;
  R3 every symlink oracle row is accounted for exactly once: either one
     `unpublished-entry` gap at its rel or one `MaliciousSymlinkRemoved`
     diagnostic at its rel (never both, never neither, never twice);
  R4 every removal diagnostic resolves to a symlink oracle row;
  R5 structural gaps: at most one `depth-limited`, no `unknown-chunk-handler`,
     no other gap kind;
  R6 subject digest == the carrier pin.
"""
import collections
import json
import sys


def read_tsv(path, n):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            assert len(parts) == n, (path, line[:80], len(parts))
            rows.append(parts)
    return rows


def project(env):
    nr = env["normalized_result"]
    pre = "$output/"
    cr = None
    for d in nr.get("derivations") or []:
        if (d.get("handler") or "").startswith("squashfs_v4"):
            cp = d.get("child_path") or ""
            cr = cp[len(pre):] if cp.startswith(pre) else cp

    def rel(p):
        if p is None:
            return None
        if p.startswith(pre):
            p = p[len(pre):]
        if cr and p.startswith(cr + "/"):
            return p[len(cr) + 1:]
        if cr:
            needle = "/" + cr + "/"
            i = p.rfind(needle)
            if i >= 0:
                return p[i + len(needle):]
        return None

    files = {}
    for f in nr.get("files") or []:
        files[rel(f.get("relative_path"))] = (f.get("sha256"), f.get("size"))
    gaps = [(g.get("kind"), rel(g.get("relative_path")), g.get("handler"),
             tuple(g.get("dependencies") or [])) for g in nr.get("extraction_gaps") or []]
    unpub = [(rel(u.get("relative_path")), u.get("kind"), u.get("link_target"))
             for u in nr.get("unpublished_entries") or []]
    removals = []
    other_diag = []
    for d in nr.get("diagnostics") or []:
        rep = d.get("report") or {}
        t = rep.get("__typename__")
        if t == "MaliciousSymlinkRemoved":
            removals.append((rel(rep.get("link")), rep.get("target")))
        else:
            other_diag.append((t, rel(rep.get("link"))))
    return {"files": files, "gaps": gaps, "unpub": unpub, "removals": removals,
            "other_diag": other_diag, "cr": cr,
            "subject": ((env.get("subject") or {}).get("digest") or {}).get("sha256"),
            "handlers": sorted({c.get("handler") for c in nr.get("chunks") or [] if c.get("handler")})}


def verify(proj, oracle, nonreg, pin):
    o = {r: (h, int(s)) for r, h, s in oracle}
    kinds = {r: (k, d) for r, k, d in nonreg}
    symlinks = {r for r, (k, _d) in kinds.items() if k == "symlink"}
    fails = []
    # R1
    missing = sorted(set(o) - set(proj["files"]))
    extra = sorted(set(proj["files"]) - set(o))
    sha_bad = sorted(r for r in set(o) & set(proj["files"])
                     if proj["files"][r] != o[r])
    # R2
    as_file = sorted(r for r in proj["files"] if r in kinds)
    # R3
    gap_paths = [r for k, r, _h, _d in proj["gaps"] if k == "unpublished-entry"]
    gap_count = collections.Counter(gap_paths)
    rem_paths = [r for r, _t in proj["removals"]]
    rem_count = collections.Counter(rem_paths)
    accounted = collections.Counter()
    for r, c in gap_count.items():
        accounted[r] += c
    for r, c in rem_count.items():
        accounted[r] += c
    unaccounted = sorted(symlinks - set(accounted))
    doubled = sorted(r for r, c in accounted.items() if c > 1)
    accounted_non_symlink = sorted(set(accounted) - symlinks)
    # R4
    rem_not_symlink = sorted(r for r, _t in proj["removals"] if r not in symlinks)
    # R5
    kinds_gap = collections.Counter(k for k, _r, _h, _d in proj["gaps"])
    structural = {k: c for k, c in kinds_gap.items() if k not in ("unpublished-entry",)}
    structural_bad = {k: c for k, c in structural.items()
                      if k != "depth-limited" or c > 1}
    # R6
    if proj["subject"] != pin:
        fails.append("subject digest %r != pin %r" % (proj["subject"], pin))
    for label, bad in (("R1_missing", missing[:10]), ("R1_extra", extra[:10]),
                       ("R1_sha_or_size", sha_bad[:10]), ("R2_nonregular_as_file", as_file[:10]),
                       ("R3_unaccounted_symlink", unaccounted[:10]),
                       ("R3_double_accounted", doubled[:10]),
                       ("R3_accounted_non_symlink", accounted_non_symlink[:10]),
                       ("R4_removal_not_symlink", rem_not_symlink[:10]),
                       ("R5_structural", structural_bad)):
        if bad:
            fails.append("%s: %s" % (label, bad))
    return {
        "ok": not fails, "fails": fails,
        "oracle_files": len(o), "published": len(proj["files"]),
        "oracle_hits": len(set(o) & set(proj["files"])) - len(sha_bad),
        "n_symlink_rows": len(symlinks), "n_gap_unpublished": len(gap_paths),
        "n_removals": len(rem_paths), "n_unpublished_entries": len(proj["unpub"]),
        "unpub_kinds": dict(collections.Counter(k for _r, k, _t in proj["unpub"])),
        "gap_kinds": dict(kinds_gap), "other_diagnostics": proj["other_diag"],
        "handlers": proj["handlers"], "chunk_root": proj["cr"],
        "extra_files": len(extra), "missing_files": len(missing),
        "dirs_invisible": len([r for r, (k, _d) in kinds.items() if k == "dir"]) -
                          len([r for r in proj["files"] if kinds.get(r, ("",))[0] == "dir"]),
        "device_invisible": len([r for r, (k, _d) in kinds.items()
                                 if k.endswith("device")]),
    }


def main():
    lane, pin, oracle_tsv, nonreg_tsv = sys.argv[1:5]
    receipts = sys.argv[5:]
    oracle = read_tsv(oracle_tsv, 3)
    nonreg = read_tsv(nonreg_tsv, 3)
    res = {}
    for p in receipts:
        env = json.load(open(p))
        res[p.split("/")[-2] + "/" + p.split("/")[-1]] = verify(project(env), oracle, nonreg, pin)
    print(json.dumps(res, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
