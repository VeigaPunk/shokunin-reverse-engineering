#!/usr/bin/env python3
"""Shadow v3 precedence, transcribed only from plans/round-41-claims.md (R41-C2).

Used by seat R42C2Eval to compare the v4 evaluator's pairs against the v3 text on
the same envelopes.  It is NOT the round-41 frozen evaluator and never reads it;
it exists so the report can say where v3 and v4 disagree and why.
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import util as _u
spec = _u.spec_from_file_location("ev4", os.path.join(os.path.dirname(os.path.abspath(__file__)), "indep-eval-v4.py"))
ev4 = _u.module_from_spec(spec); spec.loader.exec_module(ev4)


def classify_v3(f):
    H, G, D, BE, SR, P = f["H"], set(f["G"]), set(f["D"]), f["BE"], f["SR"] == "yes", f["P"]
    if f["OP"] != "extract_firmware" or f["PR"] != "unblob":
        return "unclassified", "none"
    if not any(h.startswith("squashfs_v4_") for h in H):
        return "no-squashfs-chunk", "inspect-input"
    if "missing-extractor-dependency" in G:
        if "sasquatch-v4be" in D:
            return "dep-missing-be", "install-extractor-be"
        if "sasquatch" in D:
            return "dep-missing-le", "install-extractor-le"
    if "extractor-failure" in G and P > 0:
        return "partial-body-failure", "salvage-partial"
    if "extractor-failure" in G and P == 0 and BE == "no" and "squashfs_v4_be" in f["FH"]:
        return "avm-marker-be-dropped", "wrap-extractor-be"
    if "extractor-failure" in G and P == 0:
        return "body-extractor-failure", "preserve-failure"
    if "depth-limited" in G:
        return "depth-limited", "raise-depth"
    if SR and "unpublished-entry" in G:
        return "mixed-symlinks", "audit-symlinks"
    if SR and not G:
        return "escaping-symlink-removed", "expect-link-absent"
    if G == {"unpublished-entry"}:
        return "in-tree-symlink-metadata", "count-gap"
    if not G:
        return ("clean", "none") if P > 0 else ("clean-empty", "confirm-empty")
    return "unclassified", "none"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--envelopes", required=True)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    rows = []
    for name in sorted(os.listdir(a.envelopes)):
        path = os.path.join(a.envelopes, name)
        target = ev4.envelope_path(path, a.full) if os.path.isdir(path) else (path if name.endswith(".json") else None)
        if not target:
            continue
        env = ev4.unwrap(json.load(open(target)))
        f = ev4.extract_features(env)
        v4 = ev4.classify(f)[:2]
        v3 = classify_v3(f)
        rows.append({"id": name, "v3": f"{v3[0]}/{v3[1]}", "v4": f"{v4[0]}/{v4[1]}",
                     "same": v3 == v4, "H": f["H"], "G": f["G"], "BE": f["BE"], "SR": f["SR"], "P": f["P"]})
    payload = {"n": len(rows), "differ": sum(1 for r in rows if not r["same"]), "rows": rows}
    text = json.dumps(payload, indent=1) + "\n"
    (open(a.out, "w").write(text) if a.out else sys.stdout.write(text))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
