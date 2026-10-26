#!/usr/bin/env python3
"""Feature extractor per the P39-C2 triage grammar (R39C2ReconMarker recon).

usage: features.py ENVELOPE.json [...]   -> one JSON object per envelope on stdout
Accepts a full CLI envelope {ok,data,meta} or a bare `data` object.
"""
import json, sys

def find_reports(node, out, path="root"):
    """Collect every dict that looks like a diagnostic report (has __typename__)."""
    if isinstance(node, dict):
        if "__typename__" in node:
            out.append((path, node))
        for k, v in node.items():
            find_reports(v, out, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            find_reports(v, out, f"{path}[{i}]")

def features(env, name):
    data = env.get("data", env) if isinstance(env, dict) else {}
    nr = data.get("normalized_result") or {}
    if not isinstance(nr, dict):
        nr = {}
    chunks = nr.get("chunks") or []
    H = {c.get("handler") for c in chunks if str(c.get("handler", "")).startswith("squashfs")}
    failed = [c.get("extraction_failed") for c in chunks if str(c.get("handler", "")).startswith("squashfs")]
    gaps = nr.get("extraction_gaps") or []
    G = {g.get("kind") for g in gaps}
    D = sorted({d for g in gaps for d in (g.get("dependencies") or [])})
    unpub = [u.get("kind") for u in (nr.get("unpublished_entries") or [])]
    be = "n/a"; cmds = []
    reports = []
    find_reports(data.get("normalized_result"), reports, "normalized_result")
    find_reports(data.get("raw_result"), reports, "raw_result")
    for path, rep in reports:
        cmd = rep.get("command")
        if isinstance(cmd, str):
            argv = cmd.split()
        elif isinstance(cmd, list):
            argv = [str(x) for x in cmd]
        else:
            continue
        prog = argv[0].rsplit("/", 1)[-1] if argv else ""
        if "sasquatch" in prog:
            cmds.append({"path": f"{path}.command", "argv": argv, "typename": rep.get("__typename__")})
    if cmds:
        be = "yes" if any("-be" in c["argv"] for c in cmds) else "no"
    SR = "yes" if any(rep.get("__typename__") == "MaliciousSymlinkRemoved" for _, rep in reports) else "no"
    return {
        "run": name,
        "ok": env.get("ok"),
        "handler_set": sorted(H),
        "squashfs_extraction_failed": failed,
        "gap_kinds": sorted(G),
        "dependencies": D,
        "unpublished_kinds": unpub,
        "be": be,
        "symlink_removed": SR,
        "published_files": len(nr.get("files") or []),
        "published_bytes": nr.get("published_bytes"),
        "coverage": nr.get("coverage"),
        "evidence_id": data.get("evidence_id"),
        "subject_sha256": (data.get("subject") or {}).get("digest", {}).get("sha256"),
        "diagnostic_typenames": [rep.get("__typename__") for _, rep in reports if rep.get("__typename__") not in ("StatReport","FileMagicReport","HashReport")],
        "sasquatch_commands": cmds,
        "files": [f for f in (nr.get("files") or [])],
    }

if __name__ == "__main__":
    rows = []
    for p in sys.argv[1:]:
        with open(p) as f:
            env = json.load(f)
        rows.append(features(env, p.rsplit("/",1)[-1].removesuffix(".json")))
    json.dump(rows, sys.stdout, indent=1)
    print()
