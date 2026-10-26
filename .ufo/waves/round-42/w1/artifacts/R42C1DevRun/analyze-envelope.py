#!/usr/bin/env python3
"""R42C1DevRun envelope analyzer.

Compares a REA extract-firmware envelope against the sasquatch-built oracle
(oracle-regular.tsv / oracle-nonregular.tsv) and prints a compact JSON report.

Usage:
  analyze-envelope.py --envelope ENVELOPE_JSON \
      --oracle STEM --out REPORT.json [--prefix-hints A B ...]
"""
import argparse
import json
import sys


def load_tsv(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            rows.append(parts)
    return rows


def find_root(nr, outdir):
    """Return (root, kind) the extract root for the filesystem chunk."""
    derivs = nr.get("derivations") or []
    wanted = None
    for d in derivs:
        if d.get("handler", "").startswith("squashfs_v"):
            wanted = d.get("child_path")
            break
    if wanted is None and derivs:
        wanted = derivs[0].get("child_path")
    if not wanted:
        return None, None
    root = wanted.replace("$output", outdir)
    return root, ("derivation" if wanted else "unknown")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--envelope", required=True)
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--7z")
    args = ap.parse_args()

    env = json.load(open(args.envelope, encoding="utf-8"))
    data = env.get("data") or {}
    nr = data.get("normalized_result") or {}
    outdir = (data.get("parameters") or {}).get("output_directory", "")

    oracle_reg = {}
    for rel, digest, size in load_tsv(args.oracle + "-regular.tsv"):
        oracle_reg[rel] = (digest, int(size))
    oracle_nonreg = {}
    for rel, kind, detail in load_tsv(args.oracle + "-nonregular.tsv"):
        oracle_nonreg[rel] = (kind, detail)

    root, how = find_root(nr, outdir)

    published = []
    for f in nr.get("files") or []:
        p = f.get("path", "")
        rel = f.get("relative_path", "")
        if root and p.startswith(root):
            rel = p[len(root):].lstrip("/")
        published.append({
            "rel": rel,
            "size": f.get("size"),
            "sha256": f.get("sha256"),
        })

    pub_by_rel = {p["rel"]: p for p in published}

    missing = [r for r in oracle_reg if r not in pub_by_rel]
    extra = [r for r in pub_by_rel if r not in oracle_reg]
    hashdiff = []
    for r in oracle_reg:
        if r in pub_by_rel:
            od, osz = oracle_reg[r]
            if pub_by_rel[r]["sha256"] != od or pub_by_rel[r]["size"] != osz:
                hashdiff.append((r, od, osz, pub_by_rel[r]))
    bad_extra = [r for r in extra if r not in oracle_nonreg]

    gaps = nr.get("extraction_gaps") or []
    gap_kinds = {}
    for g in gaps:
        k = g.get("kind", "?")
        gap_kinds.setdefault(k, []).append(g)

    unpublished = nr.get("unpublished_entries") or []
    unpub_kinds = {}
    for u in unpublished:
        k = u.get("kind", "?")
        unpub_kinds.setdefault(k, []).append(u)

    out = {
        "operation": data.get("operation"),
        "ok": env.get("ok"),
        "coverage": nr.get("coverage"),
        "outdir": outdir,
        "extract_root": root,
        "extract_root_source": how,
        "chunks": [
            {
                "handler": c.get("handler"),
                "range": c.get("range"),
                "failed": c.get("extraction_failed"),
            }
            for c in (nr.get("chunks") or [])
        ],
        "derivations": nr.get("derivations"),
        "published_count": len(published),
        "oracle_regular_count": len(oracle_reg),
        "oracle_nonregular_count": len(oracle_nonreg),
        "published_missing_from_oracle": sorted(missing),
        "published_extra_vs_oracle": sorted(extra),
        "published_extra_not_oracle_nonregular": sorted(bad_extra),
        "hash_or_size_mismatch": hashdiff,
        "gap_total": len(gaps),
        "gap_kinds": {
            k: {
                "n": len(v),
                "sample": v[0] if v else None,
            }
            for k, v in gap_kinds.items()
        },
        "unpublished_total": len(unpublished),
        "unpublished_kinds": {
            k: len(v) for k, v in unpub_kinds.items()
        },
        "unpublished_sample": unpublished[:3] if unpublished else [],
        "diagnostics": nr.get("diagnostics"),
        "depth_limited_paths": nr.get("depth_limited_paths"),
        "published_bytes": nr.get("published_bytes"),
        "selection": nr.get("selection"),
        "engine": nr.get("engine"),
        "published_path_prefix_sample": (
            published[0]["rel"] if published else None
        ),
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(
        {k: out[k] for k in (
            "ok", "coverage", "extract_root", "extract_root_source",
            "chunks", "published_count", "oracle_regular_count",
            "oracle_nonregular_count", "published_missing_from_oracle",
            "published_extra_vs_oracle", "bad_extra" if "bad_extra" in out
            else "published_extra_not_oracle_nonregular",
            "hash_or_size_mismatch", "gap_kinds", "unpublished_kinds",
            "diagnostics", "depth_limited_paths",
        )}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
