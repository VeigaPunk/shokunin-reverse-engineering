#!/usr/bin/env python3
"""R40-C1 oracle-only receipt fabricator (pre-freeze control, never a claim tool).

Builds `corpus/evidence/round-39/c1/<K>/after.json`-shaped documents from frozen
metadata only:

  * the carriers manifest (pin, byte size, oracle path, symlinks path),
  * `oracle.tsv`   (relative path, sha256, size),
  * `symlinks.tsv` (relative path, target, in-tree|escaping).

No REA, unblob or sasquatch process is started, no carrier is opened and no
extracted byte is read.  The opened paths are recorded in the emitted
`manifest.json` so a reader can verify the input closure.

Modes
  min    what the oracle states with no inference beyond the gap rule:
         files, chunks, gaps, unpublished entries, subject pin.  No diagnostics,
         no derivations, no engine, extension-guessed mime.
  full   the R39 CTL-C1-3 shape: min + diagnostics inferred from the escaping
         symlinks + the full directory-edge derivation tree + engine copied as a
         host constant + coverage/published_bytes derived.  This is the strongest
         fabrication the frozen metadata supports, i.e. the control that tests
         whether the projection is *oracle-closed*.
  full2  full, with the derivation tree restricted to published files and
         in-tree link paths (a forger who has read RD39W2C1Fabricate can infer
         that REA emits no derivation for the escaping link it removed).

Usage
  fabricate-oracle-only.py --manifest <carriers.json> --lane-root <LANE>
      --mode min|full|full2 --out <DIR> [--pkg65 <rea-agents root>] [--only K1,K5]
      [--outdir-base <DIR>]

Exit 0 written, 2 bad input.  Pure stdlib (evidence-id re-minting is optional and
uses node tools/round-27/xpin-attribute.mjs, the frozen 6.5.0 rule).
"""
import argparse
import hashlib
import json
import os
import posixpath
import subprocess
import sys
import tempfile

PREFIX = "firmware.bin_extract"
HANDLER = "squashfs_v4_be"
UNBLOB_EXE = os.path.expanduser("~/.local/share/uv/tools/unblob/bin/unblob")
UNBLOB_SHA = "0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09"


def die(msg):
    print("fabricate-oracle-only: " + msg, file=sys.stderr)
    sys.exit(2)


def read_tsv(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            rows.append(line.rstrip("\n").split("\t"))
    return rows


def mime_guess(rel):
    """The round-39 CTL-C1-3 harness rule: extension only, no bytes."""
    low = rel.lower()
    if low.endswith((".sh", ".run")):
        return "text/x-shellscript"
    if low.endswith((".txt", ".md")):
        return "text/plain"
    if low.endswith(".json"):
        return "text/plain"          # deliberate: bytes are needed for application/json
    return "application/octet-stream"


def build(entry, lane, mode, outdir):
    pin = entry["sha256"]
    size = entry.get("size_bytes")
    if size is None:
        die("manifest entry %s has no size_bytes" % entry.get("id"))
    oracle = read_tsv(os.path.join(lane, entry["oracle"]))
    links = read_tsv(os.path.join(lane, entry["symlinks"])) if entry.get("symlinks") else []
    files = [(r[0], r[1], int(r[2])) for r in oracle]
    links = [{"rel": r[0], "target": r[1], "kind": r[2]} for r in links]

    published = [
        {
            "relative_path": PREFIX + "/" + rel,
            "path": os.path.join(outdir, PREFIX, rel),
            "size": sz,
            "sha256": sha,
            "reported_sha256": sha,
            "mime_type": mime_guess(rel),
            "analysis_depth": 1,
            "runtime_address": None,
            "original_file_range": None,
        }
        for rel, sha, sz in files
    ]

    gaps, unpublished, diagnostics = [], [], []
    for link in links:
        if link["kind"] == "in-tree":
            gaps.append({
                "kind": "unpublished-entry",
                "input_path": "$output/%s/%s" % (PREFIX, link["rel"]),
                "relative_path": "%s/%s" % (PREFIX, link["rel"]),
                "handler": None, "provider_id": None, "range": None,
                "root_file_range": None, "dependencies": [],
                "continuation_id": hashlib.sha256(
                    ("unpublished-entry|%s/%s|" % (PREFIX, link["rel"])).encode()).hexdigest(),
            })
            unpublished.append({"relative_path": "%s/%s" % (PREFIX, link["rel"]),
                                "kind": "symlink", "link_target": link["target"]})
        elif mode in ("full", "full2"):
            diagnostics.append({
                "input_path": "$input",
                "report": {"__typename__": "MaliciousSymlinkRemoved",
                           "severity": "WARNING",
                           "link": "%s/%s" % (PREFIX, link["rel"]),
                           "target": link["target"]},
            })

    chunks = [{
        "input_path": "$input", "provider_id": "0:1",
        "range": {"offset": 0, "length": size},
        "handler": HANDLER, "encrypted": False,
        "root_file_range": {"offset": 0, "length": size},
        "extraction_failed": False,
    }]

    nr = {
        "engine": None,
        "selection": {"offset": 0, "length": size, "sha256": pin},
        "output_directory": outdir,
        "coverage": None,
        "files": published,
        "unpublished_entries": unpublished,
        "chunks": chunks,
        "derivations": [],
        "depth_limited_paths": [],
        "diagnostics": diagnostics,
        "extraction_gaps": gaps,
        "extraction_continuations": [],
        "published_bytes": None,
    }

    if mode in ("full", "full2"):
        # full directory-edge tree: every directory -> each child (dir, file, link)
        children = {}
        def add_edge(parent, child):
            children.setdefault(parent, set()).add(child)

        keep_links = [l["rel"] for l in links
                      if mode == "full" or l["kind"] == "in-tree"]
        paths = [rel for rel, _s, _z in files] + keep_links
        dirs = set()
        for rel in paths:
            parent = PREFIX
            parts = rel.split("/")
            for i, part in enumerate(parts[:-1]):
                cur = PREFIX + "/" + "/".join(parts[:i + 1])
                add_edge(parent, cur)
                dirs.add(cur)
                parent = cur
            add_edge(parent, PREFIX + "/" + rel)
        derivations = [
            {"parent_path": "$output/" + parent,
             "child_path": "$output/" + child,
             "provider_blob_id": "0:1", "handler": None,
             "parent_file_range": None}
            for parent in sorted(children) for child in sorted(children[parent])
        ]
        derivations.append({"parent_path": "$input", "child_path": "$output/" + PREFIX,
                            "provider_blob_id": "0:1", "handler": HANDLER,
                            "parent_file_range": {"offset": 0, "length": size}})
        nr["derivations"] = derivations
        nr["engine"] = {"name": "unblob", "version": "26.6.4",
                        "executable_path": UNBLOB_EXE, "executable_sha256": UNBLOB_SHA,
                        "source_revision": None, "worker_count": 1}
        nr["coverage"] = "partial" if (gaps or diagnostics) else "complete"
        nr["published_bytes"] = sum(f["size"] for f in published)

    return {
        "evidence_id": None,
        "subject": {"name": os.path.basename(entry["path"]),
                    "digest": {"sha256": pin},
                    "local_path": entry["path"], "format": "file",
                    "architecture": None},
        "provider": {"id": "unblob", "name": "Unblob", "version": "26.6.4"},
        "analysis_profile": None,
        "predicate_type": "rea.analysis",
        "operation": "extract_firmware",
        "parameters": {"path": entry["path"], "output_directory": outdir,
                       "max_depth": 3, "max_output_bytes": 268435456,
                       "max_output_files": 10000},
        "raw_result": {"report": []},
        "normalized_result": nr,
        "confidence": "observed",
        "authority": "shipped-artifact",
        "environment": None,
        "limitations": None,
        "relationship_coverage": None,
        "locations": [{"kind": "file-offset-range", "start": 0, "end": size}],
        "evidence_links": [],
    }


def remint(env, lane, pkg65):
    """Re-mint evidence_id with the frozen 6.5.0 rule (xpin-attribute.mjs)."""
    tool = os.path.join(lane, "tools/round-27/xpin-attribute.mjs")
    if not os.path.exists(tool):
        return None, "xpin-attribute.mjs absent at %s" % tool
    with tempfile.TemporaryDirectory() as work:
        wrapped = os.path.join(work, "wrapped.json")
        with open(wrapped, "w", encoding="utf-8") as fh:
            json.dump({"data": env}, fh)
        proc = subprocess.run(["node", tool, "--pkg65", pkg65, "--pkg67", pkg65, wrapped],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            return None, "xpin exit %d: %s" % (proc.returncode, proc.stderr.strip()[:300])
        cols = proc.stdout.rstrip("\n").split("\t")
        return cols[2], None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--lane-root", required=True)
    ap.add_argument("--mode", choices=("min", "full", "full2"), required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pkg65")
    ap.add_argument("--only")
    ap.add_argument("--outdir-base", required=True)
    opts = ap.parse_args(argv or sys.argv[1:])

    lane = os.path.abspath(opts.lane_root)
    spec = json.load(open(opts.manifest, encoding="utf-8"))
    entries = spec["carriers"] if isinstance(spec, dict) else spec
    if opts.only:
        keep = set(opts.only.split(","))
        entries = [e for e in entries if e["id"] in keep]
    os.makedirs(opts.out, exist_ok=True)
    written, ids = [], {}
    for entry in entries:
        outdir = os.path.join(opts.outdir_base, entry["id"] + "-after")
        env = build(entry, lane, opts.mode, outdir)
        if opts.pkg65:
            new_id, err = remint(env, lane, opts.pkg65)
            if new_id:
                env["evidence_id"] = new_id
                ids[entry["id"]] = {"evidence_id": new_id, "remint": "xpin 6.5.0 rule"}
            else:
                ids[entry["id"]] = {"evidence_id": None, "remint": "failed: " + err}
        path = os.path.join(opts.out, entry["id"] + ".json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(env, fh, indent=1, sort_keys=True)
        written.append(path)

    manifest = {
        "schema": "kaidoku-r40-oracle-fabrication-v1",
        "mode": opts.mode,
        "processes_started": [],
        "inputs_opened": [opts.manifest] + [
            os.path.join(lane, e.get("oracle", "")) for e in entries
        ] + [os.path.join(lane, e.get("symlinks") or "") for e in entries if e.get("symlinks")],
        "carrier_bytes_read": 0,
        "receipts": written,
        "ids": ids,
        "reused_round39_harness": False,
    }
    with open(os.path.join(opts.out, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    print(json.dumps(manifest, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
