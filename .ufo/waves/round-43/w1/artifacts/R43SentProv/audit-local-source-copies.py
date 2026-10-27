#!/usr/bin/env python3
"""audit-local-source-copies — fresh host re-verification of the R42LocalSrc copy pack.

Read-only. Stdlib only. For every entry in the prepared sidecar map it:

  1. hashes the in-lane copy and compares it with the map's `sha256`;
  2. resolves the host path (the map key) and reports file / directory / absent;
  3. file source: hashes the live host file and compares with the map's
     `source_sha256` (when present) and with the `host_sha256` column of the
     seat's copies.tsv;
  4. tree-archive copy: opens the tar, compares every member with the matching
     live object (a file inside the live directory, or a member of the live
     archive the member came from), member by member;
  5. gzip copy: decompresses it (no write) and compares the decoded digest with
     `source_sha256`.

Exit 0 every check that can be made now agrees; 1 a mismatch; 2 cannot evaluate.

Usage: audit-local-source-copies.py --map <local-sources.json> --copies-tsv <copies.tsv>
                                    [--root <lane>] --json-out <file>
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import sys
import tarfile
import zipfile

TREE_PREFIX = "corpus/evidence/round-42/local-sources/"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def live_zip_members(zip_path: str) -> dict[str, bytes]:
    out = {}
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            out[name] = zf.read(name)
    return out


def live_tar_members(tar_path: str) -> dict[str, bytes]:
    out = {}
    with tarfile.open(tar_path, "r:*") as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            fh = tf.extractfile(member)
            if fh is not None:
                out[member.name] = fh.read()
    return out


def tree_members(tar_path: str) -> dict[str, bytes]:
    return live_tar_members(tar_path)


def source_for_tree(host: str, host_kind: str) -> dict[str, bytes]:
    """Map every member name the archive could carry to live bytes."""
    if host_kind == "dir":
        out = {}
        for base, _dirs, files in os.walk(host):
            for name in files:
                full = os.path.join(base, name)
                rel = os.path.relpath(full, host)
                with open(full, "rb") as fh:
                    out[rel] = fh.read()
                # the seat's tar keeps the cited basename too
                out[name] = out[rel]
        return out
    if host_kind == "zip":
        return live_zip_members(host)
    if host_kind == "tar":
        return live_tar_members(host)
    return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True)
    ap.add_argument("--copies-tsv", required=True)
    ap.add_argument("--root", action="append", default=None,
                    help="directory the map's `copy` paths are relative to; repeatable")
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    with open(args.map, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    sources = doc["sources"]

    host_digests = {}
    with open(args.copies_tsv, "r", encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        idx = {name: i for i, name in enumerate(header)}
        for line in fh:
            cells = line.rstrip("\n").split("\t")
            if len(cells) != len(header):
                continue
            if cells[idx["host_sha256"]]:
                host_digests[cells[idx["copy"]]] = cells[idx["host_sha256"]]

    results = []
    failures = []
    unverifiable = []
    for host, entry in sorted(sources.items()):
        copy_rel = entry["copy"]
        name = copy_rel.split("/local-sources/")[-1]
        rec = {"source": host, "copy": copy_rel, "name": name}

        copy_abs = None
        copy_root_index = None
        for idx, root in enumerate(args.root or []):
            cand = os.path.join(root, copy_rel)
            if os.path.isfile(cand):
                copy_abs = cand
                copy_root_index = idx
                break
        if copy_abs is None:
            copy_abs = os.path.join((args.root or [""])[0], copy_rel)
        if not os.path.isfile(copy_abs):
            rec.update(status="copy-absent")
            failures.append(rec)
            results.append(rec)
            continue
        copy_digest = sha256_file(copy_abs)
        rec["copy_sha256"] = copy_digest
        rec["copy_root_index"] = copy_root_index
        rec["copy_matches_map"] = copy_digest == entry.get("sha256")

        if os.path.isdir(host):
            host_kind = "dir"
        elif os.path.isfile(host):
            low = host.lower()
            if low.endswith(".zip"):
                host_kind = "zip"
            elif low.endswith((".tar", ".tar.gz", ".tgz", ".db")):
                host_kind = "tar"
            else:
                host_kind = "file"
        else:
            host_kind = "absent"
        rec["host_kind"] = host_kind

        if host_kind == "file":
            live = sha256_file(host)
            rec["live_source_sha256"] = live
            rec["map_source_sha256"] = entry.get("source_sha256")
            rec["tsv_host_sha256"] = host_digests.get(copy_rel)
            ok = True
            if entry.get("source_sha256"):
                ok = ok and live == entry["source_sha256"]
            if host_digests.get(copy_rel):
                ok = ok and live == host_digests[copy_rel]
            rec["status"] = "live-equal" if ok else "live-mismatch"
            if not ok:
                failures.append(rec)
            # gzip copies decode to the source bytes
            if copy_rel.endswith(".gz"):
                with gzip.open(copy_abs, "rb") as gh:
                    decoded = sha256_bytes(gh.read())
                rec["decoded_sha256"] = decoded
                rec["decoded_matches_source"] = decoded == live or (
                    entry.get("source_sha256") == decoded)
                if not rec["decoded_matches_source"]:
                    failures.append(rec)

        elif host_kind in ("dir", "zip", "tar"):
            members = tree_members(copy_abs)
            live_map = source_for_tree(host, host_kind)
            compared = 0
            mismatched = []
            missing = []
            for member, data in sorted(members.items()):
                target = live_map.get(member)
                if target is None:
                    target = live_map.get(os.path.basename(member))
                if target is None:
                    missing.append(member)
                    continue
                compared += 1
                if sha256_bytes(data) != sha256_bytes(target):
                    mismatched.append(member)
            rec["members"] = len(members)
            rec["members_compared"] = compared
            rec["members_missing_live"] = missing
            rec["members_mismatched"] = mismatched
            live_files = len(live_map)
            rec["live_objects"] = live_files
            rec["status"] = "tree-live-equal" if compared == len(members) and not mismatched else "tree-partial"
            if mismatched or compared != len(members):
                failures.append(rec)
        else:
            rec["status"] = "host-absent"
            unverifiable.append(rec)

        results.append(rec)

    summary = {
        "entries": len(sources),
        "live_equal": sum(1 for r in results if r["status"] in ("live-equal", "tree-live-equal")),
        "failures": len(failures),
        "unverifiable": len(unverifiable),
        "map_entries_with_source_sha256": sum(1 for e in sources.values() if e.get("source_sha256")),
    }
    doc_out = {"summary": summary, "roots": args.root or [], "results": results}
    with open(args.json_out, "w", encoding="utf-8") as fh:
        json.dump(doc_out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(summary, sort_keys=True))
    for rec in failures:
        print("FAIL", rec["name"], rec["status"], rec.get("members_mismatched") or rec.get("members_missing_live") or "")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
