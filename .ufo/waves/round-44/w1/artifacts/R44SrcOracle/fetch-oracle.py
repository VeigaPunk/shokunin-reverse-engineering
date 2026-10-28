#!/usr/bin/env python3
"""R44SrcOracle: fetch unblob 26.6.4 SquashFS v1/v2 `__output__` expected trees.

Two phases, both receipted:
  list  — contents API on each `__output__` and its `_extract` subdir (JSON receipt saved).
  fetch — every member via the media.githubusercontent.com base; the committed object is
          fetched from raw.githubusercontent.com (an LFS pointer) and must hash to the
          listing's committed entry sha, and its `oid sha256` must equal the served bytes.

`--from-saved-listings` replays phase 1 from the saved receipts (used when the
unauthenticated API quota is exhausted); each record keeps its original fetched_at.
"""
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

REPO = "onekey-sec/unblob"
REF = "26.6.4"
COMMIT = "1fcc7a0a584a70a96c31f5a276c20944d199a089"
API = f"https://api.github.com/repos/{REPO}"
CONTENT_ROOT = f"tests/integration/filesystem/squashfs"
MEDIA = f"https://media.githubusercontent.com/media/{REPO}/{REF}/{CONTENT_ROOT}"
RAW = f"https://raw.githubusercontent.com/{REPO}/{REF}/{CONTENT_ROOT}"
ROOTS = [
    "squashfs_v1/little_endian",
    "squashfs_v1/big_endian",
    "squashfs_v2/little_endian",
    "squashfs_v2/big_endian",
]

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
ORACLE = os.path.join(LANE, "corpus/evidence/round-44/oracle")
WAVE = os.path.join(LANE, ".ufo/waves/round-44/w1/R44SrcOracle")
LISTINGS = os.path.join(WAVE, "listings")


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "kaidoku-r44-R44SrcOracle"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read(), round(time.time() - t0, 3)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), round(time.time() - t0, 3)


def listing_filename(path):
    return path.replace("/", "__") + ".json"


def api_listing(path):
    url = f"{API}/contents/{CONTENT_ROOT}/{path}?ref={REF}"
    status, body, wall = get(url)
    if status != 200:
        raise RuntimeError(f"listing {path}: HTTP {status} {body[:200]!r}")
    entries = json.loads(body)
    return {
        "api_url": url,
        "repo_path": f"{CONTENT_ROOT}/{path}",
        "fetched_at": now(),
        "http_status": status,
        "body_bytes": len(body),
        "body_sha256": hashlib.sha256(body).hexdigest(),
        "wall_s": wall,
        "replayed_from_saved_receipt": False,
        "entries": [
            {"type": e["type"], "name": e["name"], "size": e.get("size"), "sha": e.get("sha")}
            for e in entries
        ],
    }, entries


def saved_listing(path, saved):
    key = f"{CONTENT_ROOT}/{path}"
    if key not in saved:
        raise RuntimeError(f"no saved listing receipt for {key}")
    rec = dict(saved[key])
    rec["replayed_from_saved_receipt"] = True
    rec["receipt_path"] = os.path.join(
        ".ufo/waves/round-44/w1/R44SrcOracle/listings", listing_filename(path)
    )
    return rec, rec["entries"]


def main(argv):
    replay = "--from-saved-listings" in argv
    os.makedirs(LISTINGS, exist_ok=True)
    os.makedirs(ORACLE, exist_ok=True)
    saved = {}
    if os.path.isdir(LISTINGS):
        for name in os.listdir(LISTINGS):
            if name.endswith(".json"):
                with open(os.path.join(LISTINGS, name)) as f:
                    rec = json.load(f)
                saved[rec["repo_path"]] = rec

    manifest = {
        "seat": "R44SrcOracle",
        "phase": "list+fetch",
        "source": {
            "repo": REPO,
            "ref": REF,
            "commit": COMMIT,
            "contents_api_root": f"{API}/contents/{CONTENT_ROOT}",
            "media_base": MEDIA,
            "raw_base": RAW,
            "license": "MIT; corpus/SOURCES.md S135 anchor LICENSE:5-8",
            "grounds": "second oracle: unblob's expected member trees for squashfs_v1/v2; "
                       "NOT handler code, NOT extractor behaviour, NOT a C1 carrier",
            "member_custody": "committed object is a 126-byte git-LFS pointer; the served "
                              "member bytes are the LFS content, content-addressed by its oid",
        },
        "started_at": now(),
        "listings": [],
        "files": [],
        "failures": [],
    }

    def list_one(path):
        if replay:
            rec, entries = saved_listing(path, saved)
        else:
            rec, entries = api_listing(path)
            lp = os.path.join(LISTINGS, listing_filename(path))
            with open(lp, "w") as f:
                json.dump(rec, f, indent=1)
                f.write("\n")
        manifest["listings"].append(rec)
        return entries

    for root in ROOTS:
        out_dir = f"{root}/__output__"
        entries = list_one(out_dir)
        dirs = [e for e in entries if e["type"] == "dir"]
        if not dirs:
            manifest["failures"].append(f"{out_dir}: no _extract dir in __output__")
        for d in dirs:
            sub = f"{out_dir}/{d['name']}"
            sub_entries = list_one(sub)
            for e in sub_entries:
                if e["type"] != "file":
                    manifest["failures"].append(f"{sub}/{e['name']}: non-file {e['type']}")
                    continue
                rel = f"{sub}/{e['name']}"
                repo_path = f"{CONTENT_ROOT}/{rel}"
                dst = os.path.join(ORACLE, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                media_url = f"{MEDIA}/{rel}"
                raw_url = f"{RAW}/{rel}"
                fetched_at = now()
                status, content, wall = get(media_url)
                if status != 200:
                    manifest["failures"].append(f"{rel}: media HTTP {status}")
                    continue
                with open(dst, "wb") as f:
                    f.write(content)
                sha = hashlib.sha256(content).hexdigest()
                rec = {
                    "path": rel,
                    "repo_path": repo_path,
                    "url": media_url,
                    "fetched_at": fetched_at,
                    "http_status": status,
                    "wall_s": wall,
                    "bytes": len(content),
                    "sha256": sha,
                    "committed_entry_sha": e["sha"],
                    "committed_entry_size": e["size"],
                    "local_path": f"corpus/evidence/round-44/oracle/{rel}",
                }
                pstatus, pointer, _ = get(raw_url)
                rec["pointer_url"] = raw_url
                rec["pointer_http_status"] = pstatus
                if pstatus == 200:
                    psha = hashlib.sha1(b"blob %d\0" % len(pointer) + pointer).hexdigest()
                    rec["pointer_bytes"] = len(pointer)
                    rec["pointer_git_blob_sha1"] = psha
                    rec["pointer_sha256"] = hashlib.sha256(pointer).hexdigest()
                    rec["pointer_git_blob_sha1_matches_committed_entry"] = (
                        psha == e["sha"]
                    )
                    if not rec["pointer_git_blob_sha1_matches_committed_entry"]:
                        manifest["failures"].append(
                            f"{rel}: pointer blob {psha} != committed entry {e['sha']}"
                        )
                    text = pointer.decode("utf-8", "replace")
                    if text.startswith("version https://git-lfs.github.com/spec/v1"):
                        oid = size = ""
                        for line in text.splitlines():
                            if line.startswith("oid sha256:"):
                                oid = line.split(":", 1)[1].strip()
                            elif line.startswith("size "):
                                size = line[5:].strip()
                        rec["lfs_resolved"] = True
                        rec["lfs_pointer_text"] = text
                        rec["lfs_oid"] = oid
                        rec["lfs_size"] = int(size) if size.isdigit() else None
                        rec["lfs_oid_matches_content"] = oid == sha
                        rec["lfs_size_matches_content"] = rec["lfs_size"] == len(content)
                        if oid != sha:
                            manifest["failures"].append(f"{rel}: LFS oid {oid} != sha256 {sha}")
                        if rec["lfs_size"] != len(content):
                            manifest["failures"].append(
                                f"{rel}: LFS size {rec['lfs_size']} != {len(content)}"
                            )
                    else:
                        rec["lfs_resolved"] = False
                        rec["content_git_blob_sha1"] = psha
                else:
                    manifest["failures"].append(f"{rel}: pointer HTTP {pstatus} {raw_url}")
                manifest["files"].append(rec)

    manifest["finished_at"] = now()
    manifest["counts"] = {
        "listings": len(manifest["listings"]),
        "listings_replayed": sum(1 for r in manifest["listings"] if r["replayed_from_saved_receipt"]),
        "files": len(manifest["files"]),
        "total_bytes": sum(f["bytes"] for f in manifest["files"]),
        "distinct_content_sha256": len({f["sha256"] for f in manifest["files"]}),
        "lfs_resolved": sum(1 for f in manifest["files"] if f.get("lfs_resolved")),
        "pointer_verified": sum(
            1 for f in manifest["files"]
            if f.get("pointer_git_blob_sha1_matches_committed_entry")
        ),
        "failures": len(manifest["failures"]),
    }
    with open(os.path.join(ORACLE, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")
    print(json.dumps(manifest["counts"], indent=1))
    for f in manifest["files"]:
        print(f"{f['bytes']:>3} {f['sha256'][:16]} {f['path']}")
    print("FAILURES:")
    for x in manifest["failures"]:
        print(" -", x)
    return 0 if not manifest["failures"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
