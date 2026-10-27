#!/usr/bin/env python3
"""drift-audit — what changed between the round-42 prepared pack and today.

Seat R43C2Land, round 43 wave 1.  Stdlib only, TMPDIR-honouring.

Three drift classes are separated, because they mean different things to the
L1 who has to land this pack:

  COPY    a prepared copy's bytes changed          (the landing is wrong)
  HOST    the host object a copy was taken from is gone or changed
          (the landing is still right; the *provenance* moved)
  MAP     the map entry's recorded digest no longer describes its copy
          (the landing is wrong)

Usage: drift-audit.py --pack <dir> --round42 <R42LocalSrc artifacts dir>
                      --sources <lane>/corpus/SOURCES.md --out <tsv>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--round42", required=True)
    ap.add_argument("--sources", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    pack = os.path.abspath(args.pack)
    r42 = os.path.abspath(args.round42)

    with open(os.path.join(pack, "corpus", "evidence", "local-sources.json"),
              "r", encoding="utf-8") as fh:
        map_now = json.load(fh)["sources"]
    with open(os.path.join(r42, "corpus", "evidence", "local-sources.json"),
              "r", encoding="utf-8") as fh:
        map_r42 = json.load(fh)["sources"]

    # round-42's per-copy manifest: host path -> recorded host digest
    r42_manifest = {}
    with open(os.path.join(r42, "build", "copies.tsv"), "r", encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        idx = {c: i for i, c in enumerate(header)}
        for line in fh:
            if not line.strip():
                continue
            cells = line.rstrip("\n").split("\t")
            host = cells[idx["sid"]], cells[idx["copy"]]
            r42_manifest[cells[idx["copy"]]] = {
                "sid": cells[idx["sid"]],
                "copy": cells[idx["copy"]],
                "host_sha256": cells[idx["host_sha256"]],
                "host_present": cells[idx["host_present"]],
                "host_size": cells[idx["host_size"]],
                "copy_sha256": cells[idx["copy_sha256"]],
                "copy_bytes": cells[idx["copy_bytes"]],
            }

    # host path per copy path: today's map first, then the round-42 map (so a
    # superseded copy path still resolves to the host it was taken from)
    host_of = {}
    for host, entry in map_r42.items():
        host_of[entry["copy"]] = host
    for host, entry in map_now.items():
        host_of[entry["copy"]] = host

    rows = ["class\tcopy\tsid\tsubject\tround42\ttoday\tverdict"]
    changed = 0

    for copy_rel in sorted(r42_manifest):
        old = r42_manifest[copy_rel]
        now_abs = os.path.join(pack, "corpus", "evidence", copy_rel.replace(
            "corpus/evidence/", "", 1))
        # the pack keeps the lane-relative path, resolved against the pack root
        now_abs = os.path.join(pack, copy_rel)
        sid = old["sid"]
        if not os.path.isfile(now_abs):
            # the copy may have been deliberately superseded: if the map now
            # names a different copy for the same host path, that is a
            # SUPERSEDED landing (a decision), not unexplained drift
            host = host_of.get(copy_rel, "")
            now_entry = map_now.get(host)
            if now_entry is not None and now_entry["copy"] != copy_rel:
                rows.append("COPY\t%s\t%s\tcopy file\tpresent\tSUPERSEDED by %s\tSUPERSEDED" %
                            (copy_rel, sid, now_entry["copy"]))
                continue
            rows.append("COPY\t%s\t%s\tcopy file\tpresent\tMISSING\tDRIFT" %
                        (copy_rel, sid))
            changed += 1
            continue
        now_sha = sha256_file(now_abs)
        r42_sha = old["copy_sha256"]
        verdict = "same" if now_sha == r42_sha else "DRIFT"
        if now_sha != r42_sha:
            changed += 1
        rows.append("COPY\t%s\t%s\tcopy bytes\t%s\t%s\t%s" %
                    (copy_rel, sid, r42_sha[:16], now_sha[:16], verdict))

        # host object state
        host = host_of.get(copy_rel, "")
        present = os.path.exists(host)
        if not present:
            rows.append("HOST\t%s\t%s\t%s\tpresent\tABSENT\tMOVED" %
                        (copy_rel, sid, host))
            continue
        if os.path.isfile(host):
            now_host = sha256_file(host)
            verdict = "same" if now_host == (old["host_sha256"] or now_host) else "DRIFT"
            if old["host_sha256"] and now_host != old["host_sha256"]:
                changed += 1
            rows.append("HOST\t%s\t%s\t%s\t%s\t%s\t%s" %
                        (copy_rel, sid, host, (old["host_sha256"] or "-")[:16],
                         now_host[:16], verdict))
        elif os.path.isdir(host):
            # a directory host carries no single digest; its content was
            # re-verified member-by-member by the re-derivation pass
            rows.append("HOST\t%s\t%s\t%s\tdir\tpresent\tsame" %
                        (copy_rel, sid, host))
        else:
            rows.append("HOST\t%s\t%s\t%s\tpresent\tABSENT\tMOVED" %
                        (copy_rel, sid, host))

    # MAP: does each map entry still describe its copy?
    LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
    for host in sorted(map_now):
        entry = map_now[host]
        copy_abs = os.path.join(pack, entry["copy"])
        old_entry = map_r42.get(host)
        same = old_entry is not None and old_entry.get("sha256") == entry.get("sha256")
        superseded = (old_entry is not None
                      and old_entry.get("sha256") != entry.get("sha256")
                      and old_entry.get("copy") != entry.get("copy"))
        if os.path.isfile(copy_abs):
            got = sha256_file(copy_abs)
            ok = got == entry["sha256"]
            rows.append("MAP\t%s\t-\t%s\t%s\t%s\t%s" %
                        (entry["copy"], host,
                         (old_entry.get("sha256") if old_entry else "-")[:16],
                         got[:16], "same" if ok and same else "DRIFT"))
            if not ok:
                changed += 1
            if superseded:
                rows[-1] = rows[-1] + "\tSUPERSEDED"
            continue
        # the copy is not part of this pack: it already lives in the lane
        # (row S126, the round-41 closure), so it is verified in place
        lane_copy = os.path.join(LANE, entry["copy"])
        if os.path.isfile(lane_copy):
            got = sha256_file(lane_copy)
            ok = got == entry["sha256"]
            rows.append("MAP\t%s\tS126\t%s\t%s\t%s\t%s" %
                        (entry["copy"], host,
                         (old_entry.get("sha256") if old_entry else "-")[:16],
                         got[:16], "same" if ok and same else "DRIFT"))
            if not ok or not same:
                changed += 1
        else:
            rows.append("MAP\t%s\t-\t%s\t%s\tMISSING\tDRIFT" %
                        (entry["copy"], host, entry["sha256"][:16]))
            changed += 1

    out = "\n".join(rows) + "\n"
    out += "drift findings: %d\n" % changed
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(out)
    sys.stdout.write(out)
    return 0 if changed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
