#!/usr/bin/env python3
"""Build a green sandbox for local-source-gate.py out of its own red report.

For every out-of-lane SOURCES path the red JSON names, this copies the cited
bytes into `<sandbox>/corpus/evidence/local-sources/` (a plain file copy, or a
deterministic tar.gz for a directory), records the digest in
`corpus/evidence/local-sources.json`, and rewrites nothing else.  Sources that
no longer exist on this host must be reconstructed: the one such path (S081's
npx cache directory) is rebuilt from the published rea-agents 6.7.0 tarball,
which that row itself states is file-for-file identical to the installed tree.

Usage:
  build-green-sandbox.py --red-json RED.json --sandbox /path/to/clone [--work DIR]

Deterministic archives: tar --sort=name --owner=0 --group=0 --numeric-owner
--mtime=@0 piped through gzip -n, so a rebuild reproduces the same digest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request

DEST_REL = "corpus/evidence/local-sources"
MAP_REL = "corpus/evidence/local-sources.json"

# path -> (npm spec, tarball member directory, registry tarball URL)
REBUILDS = {
    "/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist": (
        "rea-agents-6.7.0",
        "package/dist",
        "https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz",
    ),
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def slug(row: str, path: str) -> str:
    """Unique per (row, path): two rows can cite one path and one row can cite
    two same-named directories (S035), so the path tag disambiguates."""
    base = os.path.basename(path.rstrip("/")) or "root"
    tag = hashlib.sha256(path.encode()).hexdigest()[:8]
    return "%s_%s_%s" % (row.lower(), re.sub(r"[^A-Za-z0-9_.-]", "_", base), tag)


def deterministic_targz(src_dir: str, out_path: str, member: str) -> None:
    parent = os.path.dirname(src_dir.rstrip("/"))
    name = os.path.basename(src_dir.rstrip("/"))
    with open(out_path, "wb") as out:
        tar = subprocess.Popen(
            ["tar", "--sort=name", "--owner=0", "--group=0", "--numeric-owner",
             "--mtime=@0", "-C", parent, "-cf", "-", name],
            stdout=subprocess.PIPE,
        )
        gz = subprocess.Popen(["gzip", "-n", "-9"], stdin=tar.stdout, stdout=out)
        assert tar.stdout is not None
        tar.stdout.close()
        gz.wait()
        if tar.wait() != 0 or gz.returncode != 0:
            raise SystemExit("tar/gzip failed for %s (member %s)" % (src_dir, member))


def rebuild(spec: tuple[str, str, str], out_path: str, work: str) -> str:
    label, member, url = spec
    tarball = os.path.join(work, os.path.basename(url))
    if not os.path.exists(tarball):
        with urllib.request.urlopen(url, timeout=120) as resp, open(tarball, "wb") as fh:
            shutil.copyfileobj(resp, fh)
    extract = os.path.join(work, "extract-" + label)
    if os.path.isdir(extract):
        shutil.rmtree(extract)
    os.makedirs(extract)
    with tarfile.open(tarball, "r:gz") as tar:
        members = [m for m in tar.getmembers() if m.name == member or m.name.startswith(member + "/")]
        tar.extractall(extract, members=members, filter="tar")
    src = os.path.join(extract, member)
    deterministic_targz(src, out_path, member)
    return tarball


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--red-json", required=True)
    ap.add_argument("--sandbox", required=True, help="lane clone that will receive the copies")
    ap.add_argument("--work", default=os.environ.get("TMPDIR") or ".")
    args = ap.parse_args(argv[1:])

    with open(args.red_json, "r", encoding="utf-8") as fh:
        report = json.load(fh)

    dest = os.path.join(args.sandbox, DEST_REL)
    os.makedirs(dest, exist_ok=True)
    sources: dict[str, dict] = {}
    manifest = []
    for record in report["records"]:
        for rec in record["paths"]:
            if rec["ok"]:
                continue
            path = rec["path"]
            row = record["id"]
            name = slug(row, path)
            if os.path.isdir(path):
                out_name = name + ".tar.gz"
                out_path = os.path.join(dest, out_name)
                deterministic_targz(path, out_path, os.path.basename(path))
                entry = {"kind": "tree-archive", "rebuild": "tar --sort=name --owner=0 "
                         "--group=0 --numeric-owner --mtime=@0 -C %s -cf - %s | gzip -n -9"
                         % (os.path.dirname(path.rstrip("/")), os.path.basename(path.rstrip("/")))}
            elif os.path.isfile(path):
                out_name = name
                out_path = os.path.join(dest, out_name)
                shutil.copyfile(path, out_path)
                entry = {"kind": "file", "source_sha256": sha256_file(path),
                         "rebuild": "cp --preserve=mode,timestamps %s %s"
                         % (path, os.path.join(DEST_REL, out_name))}
            else:
                spec = REBUILDS.get(path)
                if spec is None:
                    print("NO REBUILD for absent source %s (row %s)" % (path, row), file=sys.stderr)
                    return 1
                out_name = name + ".tar.gz"
                out_path = os.path.join(dest, out_name)
                tarball = rebuild(spec, out_path, args.work)
                entry = {"kind": "tree-archive",
                         "rebuild": "curl -fsSL %s | tar -xz --strip-components=2 -C tmp %s "
                                    "&& tar --sort=name --owner=0 --group=0 --numeric-owner "
                                    "--mtime=@0 -C tmp -cf - %s | gzip -n -9"
                                    % (spec[2], spec[1], os.path.basename(spec[1])),
                         "note": "source path no longer exists on this host; copy rebuilt from the "
                                 "published %s tarball (digest %s), which row %s states is "
                                 "file-for-file identical to the installed tree"
                                 % (spec[0], sha256_file(tarball), row)}
                manifest.append((row, path, os.path.join(DEST_REL, out_name), "rebuilt"))
            digest = sha256_file(out_path)
            entry["copy"] = os.path.join(DEST_REL, out_name)
            entry["sha256"] = digest
            sources[path] = entry
            if not any(m[1] == path for m in manifest):
                manifest.append((row, path, os.path.join(DEST_REL, out_name), "copied"))

    map_path = os.path.join(args.sandbox, MAP_REL)
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    with open(map_path, "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "sources": sources}, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print("row\tpath\tcopy\tsha256\tdisposition")
    for row, path, copy, how in manifest:
        print("%s\t%s\t%s\t%s\t%s" % (row, path, copy, sources[path]["sha256"], how))
    print("wrote %s with %d entries" % (map_path, len(sources)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
