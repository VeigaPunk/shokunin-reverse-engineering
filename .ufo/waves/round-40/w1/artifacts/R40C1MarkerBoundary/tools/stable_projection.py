#!/usr/bin/env python3
"""stable_projection.py — the rerun-comparable projection of a REA `extract-firmware` envelope.

Measured on this host (round 40, seat R40C1MarkerBoundary): two fresh `extract-firmware` runs of
the same carrier into different output directories differ in 1850 leaf values of the envelope,
but every differing leaf is path-, PID- or scratch-derived:

    .normalized_result.output_directory
    .parameters.output_directory
    .normalized_result.chunks[].provider_id          (re-minted per run: e.g. 28325:1 -> 2724035:1)
    .normalized_result.derivations[].provider_blob_id
    .normalized_result.files[].path                  (absolute)
    .raw_result.execution.args[]                     (absolute outdir)
    .raw_result.report[].task.path / subtasks[].path / reports[].path / reports[].id / subtasks[].blob_id

Everything this projection keeps was byte-identical across 3 runs of each of 2 carriers
(see projection-rerun-check.txt).

usage: stable_projection.py ENVELOPE|-        -> canonical JSON on stdout, `<sha256>  <json>` on -v
       stable_projection.py -h
"""
import hashlib
import json
import re
import sys

EXTRACT_ROOT = re.compile(r"^.*?((?:firmware|input|subject)[^/]*_extract/)")


def suffix(path):
    """Keep the path from the extract root on; drop the scratch prefix and the run's outdir."""
    if path is None:
        return None
    m = EXTRACT_ROOT.match(path)
    return m.group(1) + path[m.end():] if m else path


def stable_projection(data):
    nr = data.get("normalized_result") or {}
    eng = nr.get("engine") or {}
    sel = nr.get("selection") or {}
    return {
        "subject": (data.get("subject") or {}).get("digest", {}).get("sha256"),
        "operation": data.get("operation"),
        "provider": {"id": (data.get("provider") or {}).get("id"),
                     "version": (data.get("provider") or {}).get("version")},
        "engine": {"name": eng.get("name"), "version": eng.get("version"),
                   "executable_sha256": eng.get("executable_sha256")},
        "selection": {"offset": sel.get("offset"), "length": sel.get("length"),
                      "sha256": sel.get("sha256")},
        "coverage": nr.get("coverage"),
        "published_bytes": nr.get("published_bytes"),
        "chunks": [{"handler": c.get("handler"),
                    "extraction_failed": c.get("extraction_failed"),
                    "range": c.get("range")} for c in (nr.get("chunks") or [])],
        "files": sorted(({"relative_path": suffix(f.get("relative_path")),
                          "sha256": f.get("sha256"), "size": f.get("size")}
                         for f in (nr.get("files") or [])),
                        key=lambda x: x["relative_path"] or ""),
        "gaps": sorted(({"kind": g.get("kind"),
                         "relative_path": suffix(g.get("relative_path")),
                         "handler": g.get("handler"),
                         "dependencies": g.get("dependencies")}
                        for g in (nr.get("extraction_gaps") or [])),
                       key=lambda x: (x["kind"], str(x["relative_path"]))),
        "unpublished": sorted(({"relative_path": suffix(u.get("relative_path")),
                                "kind": u.get("kind"),
                                "link_target": u.get("link_target")}
                               for u in (nr.get("unpublished_entries") or [])),
                              key=lambda x: str(x["relative_path"])),
    }


def canon(v):
    if v is None or not isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False, allow_nan=False)
    if isinstance(v, list):
        return "[" + ",".join(canon(x) for x in v) + "]"
    return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + canon(v[k])
                          for k in sorted(v)) + "}"


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        print(__doc__)
        sys.exit(0)
    src = sys.stdin if sys.argv[1] == "-" else open(sys.argv[1])
    d = json.load(src)
    data = d["data"] if isinstance(d, dict) and isinstance(d.get("data"), dict) else d
    body = canon(stable_projection(data))
    digest = hashlib.sha256(body.encode()).hexdigest()
    if "-v" in sys.argv:
        print("%s  %s" % (digest, body))
    else:
        print(body)
