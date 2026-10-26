#!/usr/bin/env python3
"""R39-C1 control receipt fabricator (pre-freeze control, never a claim tool).

Builds `corpus/evidence/round-39/c1/<K>/after.json` *data* records from frozen
metadata only: the carrier pin (sha256), the carrier byte size, `oracle.tsv`
(regular files) and `symlinks.tsv` (relative path, target, kind).  No REA process
is started and no carrier is extracted.  This is exactly the shortcut the
controls exist to test.

Modes
  copy38        byte-copy corpus/evidence/round-38/c1/<K>/after.json (CTL-C1-1)
  forge-old     forge a receipt but keep the old evidence_id (CTL-C1-2)
  forge-remint  forge a receipt and re-mint evidence_id with the frozen xpin
                rule, rea-agents 6.5.0 (CTL-C1-3, CTL-C1-5)
  materialise   like forge-remint, but every in-tree symlink is published as a
                regular file at the link path and its gap removed (CTL-C1-4)
  wrong-gap-kind    in-tree symlink gap rewritten to missing-extractor-dependency
  escaping-gap      escaping symlink kept as an `unpublished-entry` gap
  extra-gap         an extra `unpublished-entry` gap on a published regular file
  failed-chunk      BE chunk present but extraction_failed=true

carriers.json entry fields used:
  id, sha256, path (lane-relative carrier), oracle (lane-relative oracle.tsv),
  symlinks (lane-relative symlinks.tsv; optional, absent => no symlink rows)
Extra optional fields: size (else the carrier file is stat'ed).

symlinks.tsv rows:  <rel> \t <target> \t <in-tree|escaping> \t <optional note>
oracle.tsv rows:    <rel> \t <sha256> \t <size>

Usage
  fabricate_receipts.py --carriers <carriers.json> --lane-root <LANE> \
      --mode forge-remint --pkg65 <REA650_PKG_ROOT> --out <DIR> \
      [--round38-dir <LANE>/corpus/evidence/round-38/c1] [--template k1.json] \
      [--only K1,K2] [--outdir-base /fast/scratch/hyaku/kaidoku-r39/ctl]

Writes <out>/<K>/after.json plus <out>/manifest.json (mode, ids, xpin verdicts).
Exit 0 on success, 1 on a verification failure, 2 on bad input.
"""
import argparse
import hashlib
import json
import os
import posixpath
import subprocess
import sys
import tempfile

HANDLER = "squashfs_v4_be"
PREFIX = "firmware.bin_extract"
SERVER_DIR = "$output/" + PREFIX


def die(msg):
    print("fabricate: " + msg, file=sys.stderr)
    sys.exit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(raw):
    rows = []
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        rows.append(cols)
    return rows


def load_carriers(path):
    spec = json.load(open(path))
    entries = spec["carriers"] if isinstance(spec, dict) else spec
    return entries


def abs_lane(lane, rel):
    return rel if os.path.isabs(rel) else os.path.join(lane, rel)


def symlink_rows(lane, entry):
    rel = entry.get("symlinks")
    if not rel:
        return []
    p = abs_lane(lane, rel)
    if not os.path.exists(p):
        return []
    rows = []
    for cols in read_tsv(open(p, encoding="utf-8").read()):
        if len(cols) < 3:
            continue
        rows.append({"rel": cols[0], "target": cols[1], "kind": cols[2]})
    return rows


def resolve_target(rel, target):
    if target.startswith("/"):
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(rel), target))


def oracle_rows(lane, entry):
    p = abs_lane(lane, entry["oracle"])
    rows = []
    for cols in read_tsv(open(p, encoding="utf-8").read()):
        if len(cols) < 3:
            continue
        rows.append({"rel": cols[0], "sha256": cols[1], "size": int(cols[2])})
    return rows


def mime_for(rel):
    low = rel.lower()
    if low.endswith((".sh", ".run")):
        return "text/x-shellscript"
    if low.endswith((".txt", ".md", ".dat", ".json")):
        return "text/plain" if not low.endswith(".dat") else "application/octet-stream"
    return "application/octet-stream"


def gap_record(kind, rel_in_image, symlink=None, continuation_seed=""):
    rel = PREFIX + "/" + rel_in_image
    cont = hashlib.sha256((kind + "|" + rel + "|" + continuation_seed).encode()).hexdigest()
    rec = {
        "kind": kind,
        "input_path": "$output/" + rel,
        "relative_path": rel,
        "handler": None,
        "provider_id": None,
        "range": None,
        "root_file_range": None,
        "dependencies": [],
        "continuation_id": cont,
    }
    return rec


def build(entry, lane, mode, template, outdir_base, old_id):
    cid = entry["id"]
    pin = entry["sha256"]
    carrier = abs_lane(lane, entry["path"])
    size = entry.get("size")
    if size is None:
        if not os.path.exists(carrier):
            die("carrier %s absent and no size field" % carrier)
        size = os.path.getsize(carrier)
    files = oracle_rows(lane, entry)
    links = symlink_rows(lane, entry)
    outdir = os.path.join(outdir_base, cid + "-after")

    published = [
        {
            "relative_path": PREFIX + "/" + r["rel"],
            "path": os.path.join(outdir, PREFIX, r["rel"]),
            "size": r["size"],
            "sha256": r["sha256"],
            "reported_sha256": r["sha256"],
            "mime_type": mime_for(r["rel"]),
            "analysis_depth": 1,
            "runtime_address": None,
            "original_file_range": None,
        }
        for r in files
    ]

    gaps = []
    unpublished = []
    diagnostics = []
    for link in links:
        if link["kind"] == "in-tree":
            gaps.append(gap_record("unpublished-entry", link["rel"], link["target"]))
            unpublished.append(
                {"relative_path": PREFIX + "/" + link["rel"], "kind": "symlink",
                 "link_target": link["target"]}
            )
        else:
            diagnostics.append(
                {
                    "input_path": "$input",
                    "report": {
                        "__typename__": "MaliciousSymlinkRemoved",
                        "severity": "WARNING",
                        "link": PREFIX + "/" + link["rel"],
                        "target": link["target"],
                    },
                }
            )

    if mode == "materialise":
        by_rel = {r["rel"]: r for r in files}
        kept_gaps = []
        for g in gaps:
            rel_in_image = g["relative_path"][len(PREFIX) + 1:]
            link = next((x for x in links if x["rel"] == rel_in_image), None)
            target_rel = resolve_target(rel_in_image, link["target"]) if link else None
            tgt = by_rel.get(target_rel)
            if tgt is None:
                kept_gaps.append(g)
                continue
            published.append(
                {
                    "relative_path": g["relative_path"],
                    "path": os.path.join(outdir, g["relative_path"]),
                    "size": tgt["size"],
                    "sha256": tgt["sha256"],
                    "reported_sha256": tgt["sha256"],
                    "mime_type": mime_for(target_rel),
                    "analysis_depth": 1,
                    "runtime_address": None,
                    "original_file_range": None,
                }
            )
        gaps = kept_gaps
        unpublished = [u for u in unpublished
                       if u["relative_path"] not in
                       {g["relative_path"] for g in gaps}]
    elif mode == "wrong-gap-kind":
        for g in gaps:
            g["kind"] = "missing-extractor-dependency"
            g["dependencies"] = ["sasquatch-v4be"]
    elif mode == "escaping-gap":
        for link in links:
            if link["kind"] != "in-tree":
                gaps.append(gap_record("unpublished-entry", link["rel"], link["target"]))
    elif mode == "extra-gap":
        if files:
            gaps.append(gap_record("unpublished-entry", files[0]["rel"]))
    elif mode not in ("copy38", "forge-old", "forge-remint", "failed-chunk"):
        die("unknown mode " + mode)

    chunks = [
        {
            "input_path": "$input",
            "provider_id": "%s:1" % (int(hashlib.sha256(cid.encode()).hexdigest()[:6], 16)),
            "range": {"offset": 0, "length": size},
            "handler": HANDLER,
            "encrypted": False,
            "root_file_range": {"offset": 0, "length": size},
            "extraction_failed": mode == "failed-chunk",
        }
    ]

    derivations = [
        {
            "parent_path": "$output/" + PREFIX,
            "child_path": entry_file["relative_path"],
            "provider_blob_id": chunks[0]["provider_id"],
            "handler": None,
            "parent_file_range": None,
        }
        for entry_file in published
    ]
    derivations.append(
        {
            "parent_path": "$input",
            "child_path": "$output/" + PREFIX,
            "provider_blob_id": chunks[0]["provider_id"],
            "handler": HANDLER,
            "parent_file_range": {"offset": 0, "length": size},
        }
    )

    report = []
    for i, r in enumerate(files):
        p = os.path.join(outdir, PREFIX, r["rel"])
        report.append(
            {
                "task": {"path": p, "depth": 1, "blob_id": chunks[0]["provider_id"],
                         "is_multi_file": False},
                "reports": [
                    {"path": p, "size": r["size"], "is_dir": False, "is_file": True,
                     "is_link": False, "link_target": None, "__typename__": "StatReport"},
                    {"magic": "data", "mime_type": mime_for(r["rel"]),
                     "__typename__": "FileMagicReport"},
                    {"md5": None, "sha1": None, "sha256": r["sha256"],
                     "__typename__": "HashReport"},
                ],
                "subtasks": [],
            }
        )

    nr = {
        "engine": template["normalized_result"].get("engine") if template else None,
        "selection": {"offset": 0, "length": size, "sha256": pin},
        "output_directory": outdir,
        "coverage": "partial" if gaps else "complete",
        "files": published,
        "unpublished_entries": unpublished,
        "chunks": chunks,
        "derivations": derivations,
        "depth_limited_paths": [],
        "diagnostics": diagnostics,
        "extraction_gaps": gaps,
        "extraction_continuations": [],
        "published_bytes": sum(f["size"] for f in published),
    }

    env = {
        "evidence_id": old_id,
        "subject": {
            "name": os.path.basename(entry["path"]),
            "digest": {"sha256": pin},
            "local_path": carrier,
            "format": "file",
            "architecture": None,
        },
        "provider": {"id": "unblob", "name": "Unblob", "version": "26.6.4"},
        "analysis_profile": None,
        "predicate_type": "rea.analysis",
        "operation": "extract_firmware",
        "parameters": {
            "path": carrier,
            "output_directory": outdir,
            "max_depth": 3,
            "max_output_bytes": 268435456,
            "max_output_files": 10000,
        },
        "raw_result": {"report": report},
        "normalized_result": nr,
        "confidence": "observed",
        "authority": "shipped-artifact",
        "environment": None,
        "limitations": (template or {}).get("limitations"),
        "relationship_coverage": None,
        "locations": [{"kind": "file-offset-range", "start": 0, "end": size}],
        "evidence_links": [],
    }
    return env


def xpin_id(pkg65, env, work):
    tool = None
    for cand in ("tools/round-27/xpin-attribute.mjs",):
        if os.path.exists(cand):
            tool = cand
    if tool is None:
        die("xpin-attribute.mjs not found (run from the lane root)")
    wrapped = os.path.join(work, "wrapped.json")
    with open(wrapped, "w") as f:
        json.dump({"data": env}, f)
    r = subprocess.run(
        ["node", tool, "--pkg65", pkg65, "--pkg67", pkg65, wrapped],
        capture_output=True, text=True)
    if r.returncode != 0:
        die("xpin failed: " + r.stderr.strip())
    return r.stdout.rstrip("\n").split("\t")[2]


def pkg_version(root):
    try:
        return json.load(open(os.path.join(root, "package.json"))).get("version")
    except (OSError, ValueError):
        return None


def xpin_note(pkg65):
    """xpin-attribute.mjs requires --pkg67; this host has no 6.7.0 root, so both
    flags point at 6.5.0 and the tool's 6.7.0 column is vacuous.  Say so loudly
    and never let a copied run mistake that column for a second rule."""
    v = pkg_version(pkg65)
    if v is not None and v != "6.5.0":
        print("warning: --pkg65 package.json version is %s, not 6.5.0; "
              "evidence ids follow that pin's rule" % v, file=sys.stderr)
    if os.environ.get("CTL_QUIET_XPIN") != "1":
        print("note: xpin runs with --pkg67 = --pkg65 (no 6.7.0 root on this host); "
              "the 6.7.0 column is the 6.5.0 rule and is not evidence of a 6.7.0 rule",
              file=sys.stderr)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--carriers", required=True)
    ap.add_argument("--lane-root", required=True)
    ap.add_argument("--mode", required=True)
    ap.add_argument("--pkg65")
    ap.add_argument("--out", required=True)
    ap.add_argument("--round38-dir")
    ap.add_argument("--template")
    ap.add_argument("--only")
    ap.add_argument("--outdir-base", default="/fast/scratch/hyaku/kaidoku-r39/ctl")
    a = ap.parse_args(argv)
    if a.pkg65:
        xpin_note(a.pkg65)

    lane = os.path.abspath(a.lane_root)
    entries = load_carriers(a.carriers)
    if a.only:
        keep = set(a.only.split(","))
        entries = [e for e in entries if e["id"] in keep]
    r38 = a.round38_dir or os.path.join(lane, "corpus/evidence/round-38/c1")
    template = json.load(open(a.template)) if a.template else None
    fallback_old = None
    if template:
        fallback_old = template.get("evidence_id")
    os.makedirs(a.out, exist_ok=True)
    work = tempfile.mkdtemp(prefix="fab.")
    manifest = {"mode": a.mode, "carriers": {}}

    for entry in entries:
        cid = entry["id"]
        dst = os.path.join(a.out, cid)
        os.makedirs(dst, exist_ok=True)
        target = os.path.join(dst, "after.json")
        if a.mode == "copy38":
            src = os.path.join(r38, cid, "after.json")
            if not os.path.exists(src):
                die("copy38: %s absent" % src)
            data = open(src, "rb").read()
            open(target, "wb").write(data)
            env = json.loads(data)
            manifest["carriers"][cid] = {"path": target, "evidence_id": env.get("evidence_id")}
            continue
        old_id = fallback_old
        cand = os.path.join(r38, cid, "after.json")
        if os.path.exists(cand):
            old_id = json.load(open(cand)).get("evidence_id", old_id)
        env = build(entry, lane, a.mode, template, a.outdir_base, old_id)
        if a.mode in ("forge-remint", "materialise", "wrong-gap-kind",
                      "escaping-gap", "extra-gap", "failed-chunk"):
            if not a.pkg65:
                die("mode %s needs --pkg65" % a.mode)
            env["evidence_id"] = xpin_id(a.pkg65, env, work)
        with open(target, "w") as f:
            json.dump(env, f, indent=1)
            f.write("\n")
        manifest["carriers"][cid] = {"path": target, "evidence_id": env["evidence_id"]}

    with open(os.path.join(a.out, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps(manifest, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
