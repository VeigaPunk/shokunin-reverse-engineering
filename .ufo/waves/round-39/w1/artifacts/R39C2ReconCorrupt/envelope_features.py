#!/usr/bin/env python3
"""Compute the R39-C2 triage features from an REA extract-firmware envelope.

Accepts both shapes the contract allows: a bare `data` object that carries
`normalized_result`, and a full CLI envelope {ok,data,meta}.

H  = {chunks[].handler that start with 'squashfs'}            (normalized_result)
G  = {extraction_gaps[].kind}
D  = union(extraction_gaps[].dependencies)
BE = 'yes' / 'no' / 'n/a' over diagnostics[].report.command   ('-be' token)
SR = 'yes' if MaliciousSymlinkRemoved appears anywhere under raw_result
P  = len(normalized_result.files)

usage: python3 envelope_features.py ENVELOPE.json [...]
"""
import json
import sys


def data_of(env):
    if isinstance(env.get("data"), dict) and "normalized_result" in env["data"]:
        return env["data"]
    if "normalized_result" in env:
        return env
    if isinstance(env.get("data"), dict):
        return env["data"]
    raise ValueError("no data/normalized_result")


def diag_reports(d):
    nr = d.get("normalized_result") or {}
    for dg in nr.get("diagnostics") or []:
        if isinstance(dg, dict) and isinstance(dg.get("report"), dict):
            yield dg["report"]


def sr_anywhere(node):
    if isinstance(node, dict):
        if node.get("__typename__") == "MaliciousSymlinkRemoved":
            return True
        return any(sr_anywhere(v) for v in node.values())
    if isinstance(node, list):
        return any(sr_anywhere(v) for v in node)
    return False


def features(env):
    d = data_of(env)
    nr = d.get("normalized_result") or {}
    H = sorted({c.get("handler") for c in nr.get("chunks") or []
                if isinstance(c.get("handler"), str) and c["handler"].startswith("squashfs")})
    gaps = nr.get("extraction_gaps") or []
    G = sorted({g.get("kind") for g in gaps if g.get("kind")})
    D = sorted({dep for g in gaps for dep in (g.get("dependencies") or [])})
    be = "n/a"
    for rep in diag_reports(d):
        cmd = rep.get("command")
        if cmd is None:
            continue
        argv = cmd if isinstance(cmd, list) else cmd.split()
        if not any("sasquatch" in str(tok) for tok in argv):
            continue
        if any(str(tok) == "-be" for tok in argv[1:]):
            be = "yes"
        elif be != "yes":
            be = "no"
    return {
        "H": H,
        "G": G,
        "D": D,
        "BE": be,
        "SR": "yes" if sr_anywhere(d.get("raw_result") or {}) else "no",
        "P": len(nr.get("files") or []),
        "extraction_failed": [c.get("extraction_failed") for c in nr.get("chunks") or []],
        "published_bytes": nr.get("published_bytes"),
        "coverage": nr.get("coverage"),
        "unpublished_kinds": sorted({u.get("kind") for u in nr.get("unpublished_entries") or []}),
        "diagnostics": [r.get("__typename__") for r in diag_reports(d)],
        "ok": env.get("ok"),
        "evidence_id": d.get("evidence_id"),
    }


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(path, json.dumps(features(json.load(open(path))), sort_keys=True))
