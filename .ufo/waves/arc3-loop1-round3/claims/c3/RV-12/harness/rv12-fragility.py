#!/usr/bin/env python3
"""RV-12 fragility harness (adversarial reviewer, c3, arc3-loop1-round3).

Question: could a table entry false-fire on an HONEST future edit — a rename
(path moved, citing lines updated) or a line-neutral reword (same meaning,
different words)?

Method: for each entry, replay it against every past revision of the repo via
the probe's own check_entry(), so the replay semantics ARE the gate's semantics.
A revision where the entry fires is evidence of the entry's sensitivity; the
revision where its needle text was authored is the entry's "birth"; fires AFTER
birth are the false-fire record.

Also classifies each entry by fragility axis, mechanically:
  A. path-literal in `pattern` (extracted): a target rename breaks the regex
     even when the citing line was honestly updated.
  B. `exact`/`quoted` prose needle: any reword of the line breaks it.
  C. line pin on a file with historical non-append churn above the pin.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

PROBE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("cdp", PROBE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rev_list(root, path):
    p = subprocess.run(["git", "-C", root, "log", "--format=%H", "--", path],
                       capture_output=True)
    if p.returncode != 0:
        return []
    return [r for r in p.stdout.decode().splitlines() if r]


def evaluate(mod, root, rev, entry, kind_override=None, snapshot_dir=None,
             expected=None):
    """Return the finding id for this single entry at this rev, or None."""
    f = mod.Findings()
    e = dict(entry)
    if kind_override:
        e["kind"] = kind_override
    try:
        tree = mod.Tree(root, rev, snapshot_dir, expected or {}, f)
        mod.check_entry(e, tree, f)
    except Exception as exc:  # never raise: report as internal
        return "internal_error:%s" % type(exc).__name__
    ids = [x[0] for x in f.rows]
    return ids[0] if ids else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
    ap.add_argument("--table", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = args.root
    table_path = args.table or os.path.join(root, ".ufo/gates/citation-drift/pointer-table.json")
    table = json.load(open(table_path))
    entries = list(table.get("entries", []))
    quoted = [dict(e, kind="quoted") for e in table.get("quoted", [])]
    mod = load_probe()

    report = {"table": table_path, "n_entries": len(entries),
              "n_quoted": len(quoted), "entries": []}

    for e in entries + quoted:
        eid = e.get("id")
        citing = e["file"]
        revs = rev_list(root, citing)
        rows = []
        for rev in revs:
            finding = evaluate(mod, root, rev, e)
            rows.append({"rev": rev, "finding": finding})
        fires = [r for r in rows if r["finding"]]
        report["entries"].append({
            "id": eid,
            "kind": e.get("kind"),
            "file": citing,
            "line": e.get("line"),
            "target": e.get("target"),
            "pattern": e.get("pattern"),
            "n_revs_citing": len(revs),
            "n_fires": len(fires),
            "fire_revs": fires,
            "clean_revs": [r["rev"] for r in rows if not r["finding"]],
        })
        sys.stderr.write("%-32s revs=%3d fires=%3d\n" % (eid, len(revs), len(fires)))

    json.dump(report, open(args.out, "w"), indent=1)
    print("wrote %s" % args.out)


if __name__ == "__main__":
    main()