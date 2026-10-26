#!/usr/bin/env python3
"""R39W2ReproK6: semantic comparison of the committed K6 receipt against an
independent REA re-run and the sasquatch oracle. Read-only over lane bytes."""
import json, hashlib, re, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REPRO = sys.argv[1] if len(sys.argv) > 1 else "repro-envelope.json"

mine = json.load(open(REPRO))["data"]
theirs = json.load(open(f"{LANE}/corpus/evidence/round-39/c1/K6/after.json"))

def proj(ev):
    p = {
        "subject": None if ev["subject"] is None else {
            "digest": ev["subject"]["digest"],
            "format": ev["subject"]["format"],
            "architecture": ev["subject"]["architecture"]},
        "provider": ev["provider"],
        "analysis_profile": ev.get("analysis_profile"),
        "predicate_type": ev["predicate_type"],
        "operation": ev["operation"],
        "parameters": ev["parameters"],
        "raw_result": ev["raw_result"],
        "normalized_result": ev["normalized_result"],
        "confidence": ev["confidence"],
        "authority": ev["authority"],
        "environment": ev.get("environment"),
        "limitations": ev["limitations"],
        "locations": ev["locations"],
        "evidence_links": ev["evidence_links"],
    }
    if ev.get("relationship_coverage") is not None:
        p["relationship_coverage"] = ev["relationship_coverage"]
    return p

def cid(ev):
    blob = json.dumps(proj(ev), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "ev_" + hashlib.sha256(blob.encode()).hexdigest()

def filesig(n):
    return sorted((f["relative_path"], f["sha256"], f["size"]) for f in n["files"])

def gapsig(n):
    return sorted((g.get("kind"), g.get("relative_path")) for g in n["extraction_gaps"])

def unpubsig(n):
    return sorted((u.get("relative_path"), u.get("link_target")) for u in n.get("unpublished_entries") or [])

def diagset(n):
    return sorted({d["report"].get("__typename__") for d in n.get("diagnostics") or []})

def diaglinks(n):
    return sorted((d["report"].get("__typename__"), d["report"]["link"].split("/")[-1], d["report"]["target"].split("/")[-1]) for d in n.get("diagnostics") or [])

def chunk_sig(n):
    return [(c["handler"], c["extraction_failed"], c["range"], c["root_file_range"]) for c in n["chunks"]]

mn, tn = mine["normalized_result"], theirs["normalized_result"]
rows = [
    ("chunk handlers + extraction_failed", chunk_sig(mn) == chunk_sig(tn), chunk_sig(tn)),
    ("files (relative_path, sha256, size)", filesig(mn) == filesig(tn), len(filesig(tn))),
    ("extraction_gaps (kind, relative_path)", gapsig(mn) == gapsig(tn), gapsig(tn)),
    ("unpublished_entries (relative_path, link_target)", unpubsig(mn) == unpubsig(tn), unpubsig(tn)),
    ("diagnostics __typename__ set", diagset(mn) == diagset(tn), diagset(tn)),
    ("diagnostics link/target basenames", diaglinks(mn) == diaglinks(tn), diaglinks(tn)),
    ("coverage / published_bytes", (mn["coverage"], mn["published_bytes"]) == (tn["coverage"], tn["published_bytes"]), (tn["coverage"], tn["published_bytes"])),
    ("selection (sha256/len/offset)", mn["selection"] == tn["selection"], tn["selection"]),
    ("subject digest == carrier pin", mine["subject"]["digest"] == theirs["subject"]["digest"], theirs["subject"]["digest"]),
    ("operation/provider/engine", (mine["operation"], mine["provider"], mn["engine"]) == (theirs["operation"], theirs["provider"], tn["engine"]), (theirs["operation"], theirs["provider"], tn["engine"])),
    ("evidence_id recomputes (committed)", cid(theirs) == theirs["evidence_id"], theirs["evidence_id"]),
    ("evidence_id recomputes (repro)", cid(mine) == mine["evidence_id"], mine["evidence_id"]),
    ("depth_limited_paths empty", mn["depth_limited_paths"] == tn["depth_limited_paths"] == [], []),
]
ok = True
for name, eq, val in rows:
    print(f"{'MATCH ' if eq else 'DIFF  '} {name}: {json.dumps(val, sort_keys=True)[:220]}")
    ok = ok and eq
print("VERDICT:", "ALL SEMANTIC FIELDS MATCH" if ok else "SEMANTIC MISMATCH")
