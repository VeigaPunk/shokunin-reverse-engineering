#!/usr/bin/env python3
"""Compare V4 after-receipts (committed vs two independent REA runs).

Path mapping follows the claim's exact-path rule: strip one `$output/` prefix,
take the chunk extract root CR from the `derivations[]` edge whose handler
starts `squashfs_v4`, and `rel(P) = P[len(CR)+1:]` only when `P` starts with
`CR + '/'`; an absolute diagnostic `link` is mapped by locating CR as whole
segments. Comparisons are equality on `rel`, never a suffix test.
"""
import json
import sys


def load(path):
    with open(path) as f:
        return json.load(f)


def project(env):
    nr = env["normalized_result"]
    pre = "$output/"
    cr = None
    for d in nr.get("derivations") or []:
        if (d.get("handler") or "").startswith("squashfs_v4"):
            cp = d.get("child_path") or ""
            if cp.startswith(pre):
                cp = cp[len(pre):]
            cr = cp or None
    out = {"files": {}, "unpublished": {}, "gaps": [], "removals": {}, "cr": cr,
           "subject_sha256": ((env.get("subject") or {}).get("digest") or {}).get("sha256"),
           "evidence_id": env.get("evidence_id"),
           "handlers": sorted({c.get("handler") for c in nr.get("chunks") or [] if c.get("handler")}),
           "operation": env.get("operation"), "provider": (env.get("provider") or {}).get("id"),
           "parameters": env.get("parameters"),
           "n_diagnostics": len(nr.get("diagnostics") or [])}

    def rel(p):
        if p is None:
            return None
        if p.startswith(pre):
            p = p[len(pre):]
        if cr:
            if p.startswith(cr + "/"):
                return p[len(cr) + 1:]
            needle = "/" + cr + "/"
            i = p.rfind(needle)
            if i >= 0:
                return p[i + len(needle):]
        return None

    for f in nr.get("files") or []:
        r = rel(f.get("relative_path"))
        if r is None:
            r = rel(f.get("path"))
        out["files"][r] = {"sha256": f.get("sha256"), "size": f.get("size")}
    for u in nr.get("unpublished_entries") or []:
        out["unpublished"][rel(u.get("relative_path"))] = {
            "kind": u.get("kind"), "link_target": u.get("link_target")}
    for g in nr.get("extraction_gaps") or []:
        out["gaps"].append({"kind": g.get("kind"), "rel": rel(g.get("relative_path")),
                            "handler": g.get("handler"),
                            "dependencies": g.get("dependencies")})
    for d in nr.get("diagnostics") or []:
        rep = d.get("report") or {}
        r = rel(rep.get("link"))
        out["removals_raw"] = out.get("removals_raw", [])
        out["removals_raw"].append({"typename": rep.get("__typename__"), "rel": r,
                                    "link": rep.get("link"), "target": rep.get("target")})
        if rep.get("__typename__") == "MaliciousSymlinkRemoved":
            out["removals"][r] = rep.get("target")
    return out


def sets(p):
    return {
        "files": set(p["files"]),
        "unpublished": set(p["unpublished"]),
        "removals": set(p["removals"]),
        "gap_unpublished": {g["rel"] for g in p["gaps"] if g["kind"] == "unpublished-entry"},
        "gap_other": {(g["kind"], g["rel"]) for g in p["gaps"] if g["kind"] != "unpublished-entry"},
    }


def diff(a, b, an, bn, res):
    ta, tb = sets(a), sets(b)
    d = {}
    for k in ("files", "unpublished", "removals", "gap_unpublished", "gap_other"):
        sa, sb = ta[k], tb[k]
        d[k] = {"n_" + an: len(sa), "n_" + bn: len(sb), "equal": sa == sb,
                "only_" + an: sorted(map(str, sa - sb))[:20],
                "only_" + bn: sorted(map(str, sb - sa))[:20]}
    d["misc"] = {
        "subject_equal": a["subject_sha256"] == b["subject_sha256"],
        "evidence_id_equal": a["evidence_id"] == b["evidence_id"],
        "handlers_equal": a["handlers"] == b["handlers"],
        "chunk_root": [a["cr"], b["cr"]],
        "file_sha_mismatch": sorted((str(p) for p in ta["files"] & tb["files"]
                                     if a["files"][p] != b["files"][p]))[:10],
        "unpublished_meta_mismatch": sorted((str(p) for p in ta["unpublished"] & tb["unpublished"]
                                             if a["unpublished"][p] != b["unpublished"][p]))[:10],
        "removal_target_mismatch": sorted((str(p) for p in ta["removals"] & tb["removals"]
                                           if a["removals"][p] != b["removals"][p]))[:10],
        "gap_meta_mismatch": sorted(
            (str((g1, g2)) for g1, g2 in zip(sorted(a["gaps"], key=str), sorted(b["gaps"], key=str))
             if g1 != g2))[:5],
    }
    res[an + "|" + bn] = d


def main():
    paths = sys.argv[1:]
    names = ["committed", "run1", "run2"][:len(paths)]
    projs = [project(load(p)) for p in paths]
    per = {}
    for n, p in zip(names, projs):
        s = sets(p)
        per[n] = {"n_files": len(s["files"]), "n_unpublished": len(s["unpublished"]),
                  "n_removals": len(s["removals"]), "n_gaps": len(p["gaps"]),
                  "n_gap_unpublished": len(s["gap_unpublished"]),
                  "n_gap_other": len(s["gap_other"]),
                  "gap_other": sorted(map(str, s["gap_other"])),
                  "n_diagnostics": p["n_diagnostics"],
                  "chunk_root": p["cr"], "handlers": p["handlers"],
                  "subject_sha256": p["subject_sha256"], "evidence_id": p["evidence_id"],
                  "removal_paths": sorted(map(str, s["removals"])),
                  "first_file_rel": sorted(s["files"])[:3],
                  "first_unpub_rel": sorted(s["unpublished"])[:3]}
    res = {}
    pairs = [("committed", "run1"), ("committed", "run2"), ("run1", "run2")]
    for an, bn in pairs:
        if an in names and bn in names:
            diff(projs[names.index(an)], projs[names.index(bn)], an, bn, res)
    print(json.dumps({"per_receipt": per, "diffs": res}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
