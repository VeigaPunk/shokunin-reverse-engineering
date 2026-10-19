#!/usr/bin/env python3
"""v1 receipt -> v2 canonical adapter + live verification (SEAT EX-35, chain c3).

Reads a round-1-form custody receipt (per-path block form, e.g. CU-1's
config-pre-pair.txt) plus its optional metadata sidecar (inode|ctime|mtime|size|
sha256), maps every field to the v2 canonical field set, and verifies the v1
sha256 fields against the live paths (read-only: sha256sum + stat, no content
copy, no writes).

Exit codes: 0 all v1 sha256 fields verify; 1 a sha256 mismatch; 2 could-not-
evaluate (parse failure / missing path where EXISTS: yes).
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

MTIME_FMT = "%Y-%m-%d %H:%M:%S"


def parse_v1_receipt(text):
    """Parse the '## per-path capture' block form of a v1 receipt."""
    recs = []
    cur = None
    for line in text.splitlines():
        m = re.match(r"^PATH: (.+)$", line)
        if m:
            if cur:
                recs.append(cur)
            cur = {"path": m.group(1)}
            continue
        if cur is None:
            continue
        m = re.match(r"^EXISTS: (\S+)$", line)
        if m:
            cur["exists_label"] = m.group(1) == "yes"
            continue
        m = re.match(r"^SIZE: (\d+)$", line)
        if m:
            cur["size"] = int(m.group(1))
            continue
        m = re.match(r"^MTIME_UTC: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$", line)
        if m:
            cur["mtime_v1_field"] = m.group(1)
            continue
        m = re.match(r"^MODE: (\d+)\s+UID: (\d+)\s+GID: (\d+)$", line)
        if m:
            cur["mode"] = m.group(1)
            cur["uid"] = int(m.group(2))
            cur["gid"] = int(m.group(3))
            continue
        m = re.match(r"^SHA256: ([0-9a-f]{64})$", line)
        if m:
            cur["sha256"] = m.group(1)
            continue
    if cur:
        recs.append(cur)
    return recs


def parse_compact_list(text):
    """Parse the '## compact sha256 list (N paths)' trailer."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^([0-9a-f]{64})  (/.+)$", line)
        if m:
            out.append({"sha256": m.group(1), "path": m.group(2)})
    return out


def parse_metadata_sidecar(text):
    """path | inode | ctime | mtime | size | blocks | sha256"""
    out = {}
    for line in text.splitlines():
        if line.startswith("#") or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 7 or not parts[0].startswith("/"):
            continue
        out[parts[0]] = {
            "inode": int(parts[1]),
            "ctime_v1_field": parts[2],
            "mtime_v1_field_sidecar": parts[3],
            "size": int(parts[4]),
            "blocks": int(parts[5]),
            "sha256": parts[6],
        }
    return out


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stat_live(path):
    st = os.stat(path)
    return {
        "size": st.st_size,
        "mode": oct(st.st_mode & 0o7777)[2:],
        "uid": st.st_uid,
        "gid": st.st_gid,
        "mtime_epoch": int(st.st_mtime),
        "ctime_epoch": int(st.st_ctime),
        "inode": st.st_ino,
    }


def local_render(epoch, tz):
    return subprocess.run(
        ["date", "-d", "@%d" % epoch, "+%Y-%m-%d %H:%M:%S"],
        env={**os.environ, "TZ": tz}, capture_output=True, text=True,
    ).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--sidecar", default=None)
    ap.add_argument("--v1-tz", default="America/Sao_Paulo",
                    help="zone the v1 receipt's MTIME_UTC/ctime fields really used")
    ap.add_argument("--canonical-out", default=None)
    ap.add_argument("--v2-tool", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    with open(args.receipt, encoding="utf-8") as fh:
        rtext = fh.read()
    recs = parse_v1_receipt(rtext)
    compact = parse_compact_list(rtext)
    sidecar = {}
    if args.sidecar and os.path.exists(args.sidecar):
        with open(args.sidecar, encoding="utf-8") as fh:
            sidecar = parse_metadata_sidecar(fh.read())

    compact_by_path = {c["path"]: c["sha256"] for c in compact}
    rows = []
    verdict = 0
    if not recs:
        # positive floor: a receipt that parses to zero paths must never read as
        # a pass (the round-1 H1/H3 blind-instrument class, applied to receipts).
        print("FAIL could-not-evaluate: no PATH blocks parsed from %s "
              "(compact entries=%d) — refusing a vacuous PASS" % (args.receipt, len(compact)))
        return 2
    for r in recs:
        p = r["path"]
        live = None
        err = None
        digest = None
        recorded_absent = r.get("exists_label") is False
        try:
            live = stat_live(p)
            digest = sha256_of(p)
        except OSError as exc:
            err = str(exc)
            live = None
            if recorded_absent:
                # the receipt records the path as absent; still absent = verified
                verdict = verdict
            elif r.get("sha256"):
                # fail closed: a path the receipt claims must never read as pass
                verdict = max(verdict, 2)
        if recorded_absent and live is not None:
            # receipt said absent, path now exists -> state moved, that is a fail
            verdict = max(verdict, 1)
        sid = sidecar.get(p, {})
        # v1 MTIME_UTC is a local (-03) rendering; derive the epoch it denotes.
        mtime_epoch_inferred = None
        if r.get("mtime_v1_field"):
            mtime_epoch_inferred = int(subprocess.run(
                ["date", "-d", r["mtime_v1_field"], "+%s"],
                env={**os.environ, "TZ": args.v1_tz},
                capture_output=True, text=True).stdout.strip())
        row = {
            "path": p,
            "v1_sha256": r.get("sha256"),
            "v1_compact_sha256": compact_by_path.get(p),
            "live_sha256": digest,
            "sha256_match": None if digest is None else digest == r.get("sha256"),
            "sha256_compact_agrees": compact_by_path.get(p) == r.get("sha256"),
            "v1_size": r.get("size"),
            "live_size": None if live is None else live["size"],
            "size_match": None if live is None else live["size"] == r.get("size"),
            "v1_mode": r.get("mode"), "live_mode": None if live is None else live["mode"],
            "v1_uid": r.get("uid"), "live_uid": None if live is None else live["uid"],
            "v1_gid": r.get("gid"), "live_gid": None if live is None else live["gid"],
            # v2-only fields: absent from the v1 receipt itself, present in the
            # v1 sidecar for inode/ctime (as local renderings, mislabeled UTC).
            "v1_mtime_field": r.get("mtime_v1_field"),
            "v1_mtime_epoch_inferred": mtime_epoch_inferred,
            "live_mtime_epoch": None if live is None else live["mtime_epoch"],
            "mtime_epoch_match": None if live is None or mtime_epoch_inferred is None
            else live["mtime_epoch"] == mtime_epoch_inferred,
            "v1_sidecar_inode": sid.get("inode"),
            "live_inode": None if live is None else live["inode"],
            "inode_match": None if live is None or not sid else live["inode"] == sid["inode"],
            "v1_sidecar_ctime_field": sid.get("ctime_v1_field"),
            "live_ctime_epoch": None if live is None else live["ctime_epoch"],
            "live_ctime_utc": None if live is None else subprocess.run(
                ["date", "-ud", "@%d" % live["ctime_epoch"], "+%Y-%m-%d %H:%M:%S"],
                capture_output=True, text=True).stdout.strip(),
            "error": err,
        }
        if row["sha256_match"] is False:
            verdict = max(verdict, 1)
        if row["sha256_compact_agrees"] is False:
            verdict = max(verdict, 1)
        rows.append(row)

    canonical = {
        "format": "v2-canonical-from-v1",
        "source_receipt": args.receipt,
        "source_sidecar": args.sidecar,
        "v1_tz_assumption": args.v1_tz,
        "field_map_note": (
            "sha256/size/mode/uid/gid carry verbatim; v1 MTIME_UTC is a local "
            "(-03) rendering (label defect) -> mtime_epoch inferred at TZ; "
            "inode/ctime come from the v1 sidecar, ctime mislabeled UTC; "
            "v2 fields with no v1 source must be reported as absent, not faked"
        ),
        "paths": rows,
    }
    if args.canonical_out:
        with open(args.canonical_out, "w", encoding="utf-8") as fh:
            json.dump(canonical, fh, indent=2, sort_keys=True)
            fh.write("\n")
    if args.json:
        print(json.dumps(canonical, indent=2, sort_keys=True))
    else:
        for row in rows:
            print("PATH %s" % row["path"])
            print("  sha256  v1=%s live=%s match=%s" % (
                (row["v1_sha256"] or "")[:16], (row["live_sha256"] or "")[:16],
                row["sha256_match"]))
            print("  size/mode/uid/gid match: %s / %s / %s / %s" % (
                row["size_match"], row["v1_mode"] == row["live_mode"],
                row["v1_uid"] == row["live_uid"], row["v1_gid"] == row["live_gid"]))
            print("  mtime v1-field=%s inferred-epoch=%s live-epoch=%s match=%s" % (
                row["v1_mtime_field"], row["v1_mtime_epoch_inferred"],
                row["live_mtime_epoch"], row["mtime_epoch_match"]))
            print("  inode sidecar=%s live=%s match=%s  ctime sidecar=%s" % (
                row["v1_sidecar_inode"], row["live_inode"], row["inode_match"],
                row["v1_sidecar_ctime_field"]))
    return verdict


if __name__ == "__main__":
    sys.exit(main())
