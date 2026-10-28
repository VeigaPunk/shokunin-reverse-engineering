#!/usr/bin/env python3
"""R44EntryDraft receipt producer.

Runs the oracle/observer commands this seat cites in the round-44 SquashFS v1/v2
knowledge-entry draft and records, per command: exact argv, cwd, exit code,
stdout sha256, stdout bytes, stderr sha256, wall seconds.  Nothing here reads or
writes the lane's tracked evidence; every output under --scratch is disposable.

Usage: python3 -I -B receipt.py --lane <LANE> --scratch <DIR> --out <JSON> [--s139 <HTML>]
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import time


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(run_id, argv, cwd, note="", stdin_bytes=None):
    t0 = time.time()
    p = subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    wall = round(time.time() - t0, 3)
    return {
        "id": run_id,
        "argv": argv,
        "cwd": cwd,
        "note": note,
        "exit_code": p.returncode,
        "stdout_sha256": sha(p.stdout),
        "stdout_bytes": len(p.stdout),
        "stdout_head": p.stdout.decode("utf-8", "replace").splitlines()[:3],
        "stderr_sha256": sha(p.stderr),
        "stderr_bytes": len(p.stderr),
        "stderr_head": p.stderr.decode("utf-8", "replace").splitlines()[:3],
        "wall_s": wall,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--s139", default=None)
    a = ap.parse_args()

    lane = os.path.abspath(a.lane)
    scr = os.path.abspath(a.scratch)
    os.makedirs(scr, exist_ok=True)
    fx = os.path.join(lane, "corpus/evidence/round-42/c2/fixtures")

    carriers = [
        ("V1BE", "v1-be--squashfs_v1.0_be.bin"),
        ("V1LE", "v1-le--squashfs_v1.0_le.bin"),
        ("V2BE", "v2-be--squashfs_v2.0_be.bin"),
        ("V2LE", "v2-le--squashfs_v2.0_le.bin"),
    ]
    nonstd = [
        ("v2ns-be", "v2ns-be--squashfs_v2.0_be.bin"),
        ("v2ns-le", "v2ns-le--squashfs_v2.0_le.bin"),
    ]

    runs = []
    # 0. tool identities
    runs.append(run("tool-unsquashfs", ["unsquashfs", "-version"], scr,
                    "oracle identity: squashfs-tools /usr/bin/unsquashfs"))
    runs.append(run("tool-7z", ["7z", "i"], scr, "second reader identity (7-Zip)"))
    runs.append(run("tool-file", ["file", "--version"], scr, "observer identity (file(1))"))
    runs.append(run("pkg-squashfs-tools", ["pacman", "-Qi", "squashfs-tools"], scr,
                    "package identity of /usr/bin/unsquashfs"))

    # 0b. producer identity (the handler source the entry cites by line)
    runs.append(run("tool-unblob", ["unblob", "--version"], scr,
                    "producer identity: unblob 26.6.4"))
    runs.append(run("sha256-handler",
                    ["sha256sum", os.path.expanduser(
                        "~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/"
                        "unblob/handlers/filesystem/squashfs.py")], scr,
                    "source identity of the cited squashfs.py line numbers"))
    runs.append(run("superblock-fields",
                    ["python3", "-I", "-B",
                     os.path.join(os.path.dirname(os.path.abspath(__file__)), "sb.py")]
                    + [os.path.join(fx, f) for _, f in carriers], scr,
                    "superblock fields per carrier (magic/major/minor/endian/tail)"))

    # 1. carrier bytes hash to the fixtures.json pin
    runs.append(run("carrier-sha256",
                    ["sha256sum"] + [os.path.join(fx, f) for _, f in carriers], scr,
                    "re-hash the four frozen carriers"))

    # 2. file(1) label per carrier
    for cid, f in carriers:
        runs.append(run(f"file-{cid}", ["file", "-b", os.path.join(fx, f)], scr,
                        "file(1) one-line label (compression word included)"))

    # 3. unsquashfs superblock decode per carrier
    for cid, f in carriers:
        runs.append(run(f"unsquashfs-s-{cid}", ["unsquashfs", "-s", os.path.join(fx, f)], scr,
                        "oracle superblock decode incl. compressed/uncompressed flags"))

    # 4. unsquashfs listing (the member census the entry table records)
    for cid, f in carriers:
        runs.append(run(f"unsquashfs-lls-{cid}",
                        ["unsquashfs", "-lls", "-d", os.path.join(scr, "list-" + cid),
                         os.path.join(fx, f)], scr,
                        "oracle member listing (-lls; no extraction)"))

    # 5. unsquashfs extraction -> member digests (the published-file census)
    for cid, f in carriers:
        out = os.path.join(scr, "ext-" + cid)
        subprocess.run(["rm", "-rf", out], check=False)
        runs.append(run(f"unsquashfs-extract-{cid}",
                        ["unsquashfs", "-no-progress", "-d", out, os.path.join(fx, f)], scr,
                        "oracle extraction into disposable scratch"))
        runs.append(run(f"member-sha256-{cid}",
                        ["bash", "-c",
                         "cd " + out + " && find . -type f -printf '%P\\n' | sort | "
                         "while read -r p; do printf '%s %s %s\\n' "
                         "\"$(sha256sum \"$p\" | cut -d' ' -f1)\" \"$(stat -c %s \"$p\")\" \"$p\"; done"],
                        out, "regular-file digests + sizes of the oracle tree"))

    # 6. v2 nonstandard: both external readers refuse
    for cid, f in nonstd:
        runs.append(run(f"unsquashfs-lls-{cid}",
                        ["unsquashfs", "-lls", "-d", os.path.join(scr, "ns-" + cid),
                         os.path.join(fx, f)], scr,
                        "v2ns: independent reader 1 (expected refusal)"))
        runs.append(run(f"7z-l-{cid}", ["7z", "l", os.path.join(fx, f)], scr,
                        "v2ns: independent reader 2 (expected refusal)"))
    runs.append(run("bytediff-v2be-v2nsbe",
                    ["python3", "-I", "-B",
                     os.path.join(os.path.dirname(os.path.abspath(__file__)), "bytediff.py"),
                     os.path.join(fx, "v2-be--squashfs_v2.0_be.bin"),
                     os.path.join(fx, "v2ns-be--squashfs_v2.0_be.bin")], scr,
                    "byte diff standard v2 BE vs v2ns BE (0-based offsets)"))
    runs.append(run("bytediff-v2le-v2nsle",
                    ["python3", "-I", "-B",
                     os.path.join(os.path.dirname(os.path.abspath(__file__)), "bytediff.py"),
                     os.path.join(fx, "v2-le--squashfs_v2.0_le.bin"),
                     os.path.join(fx, "v2ns-le--squashfs_v2.0_le.bin")], scr,
                    "byte diff standard v2 LE vs v2ns LE (0-based offsets)"))
    runs.append(run("cmpprobe",
                    ["python3", "-I", "-B",
                     os.path.join(os.path.dirname(os.path.abspath(__file__)), "cmpprobe.py"),
                     os.path.join(fx, "v2-le--squashfs_v2.0_le.bin")], scr,
                    "instrument hazard: `cmp -l` exit status vs file size"))

    # 7. the families that stay Frontier: reader availability measured
    for rid, f, note in [
        ("v3gzip-le", "v3-le--squashfs_v3_le.bin", "gzip v3 LE: unsquashfs lists (reader exists)"),
        ("v3gzip-be", "v3-be--squashfs_v3_be.bin", "gzip v3 BE: unsquashfs lists (reader exists)"),
        ("v3lzma-le", "v3adapt-le--squashfs_v3_le.lzma.bin", "LZMA v3: unsquashfs refuses (round-42 oracle was backhand+7z)"),
    ]:
        runs.append(run("unsquashfs-lls-" + rid,
                        ["unsquashfs", "-lls", "-d", os.path.join(scr, "fr-" + rid),
                         os.path.join(fx, f)], scr, note))
    runs.append(run("unsquashfs-lls-v3bc-le",
                    ["unsquashfs", "-lls", "-d", os.path.join(scr, "fr-v3bc-le"),
                     os.path.join(fx, "v3bc-le--squashfs_v3_le.bin")], scr,
                    "v3 broadcom LE: unsquashfs refuses the magic"))
    runs.append(run("7z-l-v3bc-le",
                    ["7z", "l", os.path.join(fx, "v3bc-le--squashfs_v3_le.bin")], scr,
                    "v3 broadcom LE: 7-Zip lists (partial reader exists)"))
    runs.append(run("unsquashfs-lls-v3ns-le",
                    ["unsquashfs", "-lls", "-d", os.path.join(scr, "fr-v3ns-le"),
                     os.path.join(fx, "v3ns-le--squashfs_v3_le.bin")], scr,
                    "v3 nonstandard LE: unsquashfs refuses"))

    # 8. S139 open (the page is fetched once by the caller, --s139 <path> <status>)
    if a.s139:
        p = a.s139
        body = open(p, "rb").read() if os.path.exists(p) else b""
        runs.append({
            "id": "s139-open",
            "argv": ["curl", "-sS", "-L", "-o", os.path.basename(p),
                     "https://github.com/plougher/squashfs-tools/releases"],
            "cwd": scr,
            "note": "S139: squashfs-tools release page, grounds /usr/bin/unsquashfs 4.7.5",
            "exit_code": 0 if body else 1,
            "stdout_sha256": sha(body), "stdout_bytes": len(body),
            "stdout_head": ["http_status/bytes/wall recorded in .ufo/waves/round-44/w1/R44EntryDraft.md"],
            "stderr_sha256": sha(b""), "stderr_bytes": 0, "stderr_head": [],
            "wall_s": None,
            "file": os.path.basename(p),
        })

    receipt = {
        "seat": "R44EntryDraft",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lane_root": lane,
        "base": "c29360e3ba5381a5ab69e372d0d9577970f85018",
        "scratch": scr,
        "fixtures_dir": fx,
        "runs": runs,
        "totals": {
            "runs": len(runs),
            "nonzero_exit": [r["id"] for r in runs if r["exit_code"] != 0],
        },
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as fh:
        json.dump(receipt, fh, indent=1)
        fh.write("\n")
    print(json.dumps({"out": a.out, "runs": len(runs),
                      "nonzero_exit": receipt["totals"]["nonzero_exit"]}))


if __name__ == "__main__":
    sys.exit(main())
