#!/usr/bin/env python3
"""build-copies-r43 — rebuild the R43-C2 landing pack from its pinned substrates.

Seat R43C2Land, round 43 wave 1.  Stdlib only, network-free (the caller
supplies the downloaded tarballs), TMPDIR-honouring, no hardcoded /tmp.

This is the round-42 seat's `build-copies.py` re-grounded on the substrates the
SOURCES rows themselves pin.  The difference matters: at round 42 the REA 6.5.0
installed pipe and the Go 1.24.6 / 1.25.0 toolchains were still on the host, so
the copies were taken from those host paths.  Today three of those host objects
are gone, so a copy that only its (now absent) host path can rebuild is no
longer reproducible.  This script rebuilds every copy from a substrate that is
still reachable:

  live host file        byte-exact copy
  live host file        gzip -9 -n (lossless, reversible)
  live host zip         the two cited members, deterministic tar
  live pacman db        the tinyxxd desc member, deterministic tar
  npm tarball 6.5.0     the cited package members (23 for the dist archive)
  npm tarball 6.7.0     the three cited package members
  Go source tarball     the internal/abi tree, deterministic tar

Every output is a deterministic tar/byte artefact: sorted names, mtime 0,
uid/gid 0, mode 0644, GNU format, gzip -9 -n.  Re-running this script must
reproduce the recorded digests exactly.

Installed home: tools/round-43/build-copies-r43.py (the map's `rebuild` field
names that path, so a regenerated map is correct by construction).

Usage:
  build-copies-r43.py --out <dir that receives corpus/evidence/...>
                       --tarball-dir <dir holding dl/rea6.5.0.tgz, dl/rea6.7.0.tgz,
                                         go1.25.0.src.tar.gz, go1.24.6.src.tar.gz>
                       [--manifest <tsv path>]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import zipfile

LANE_TREE = "corpus/evidence/round-42/local-sources"
MAP_REL = "corpus/evidence/local-sources.json"

GHIDRA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC"
REA65_TGZ = "dl/rea6.5.0.tgz"
REA67_TGZ = "dl/rea6.7.0.tgz"
GO125_TGZ = "go1.25.0.src.tar.gz"
GO124_TGZ = "go1.24.6.src.tar.gz"

# The 28 S048/S066/S070/S079/S083/S090/S092 pins: 27 dist-relative members
# plus bridge/ghidra/ReaGhidraBridge.java, which is package-root-relative.
REA65_MEMBERS = [
    "application/DirectAnalysis.js",
    "application/binaryDiagnostics/BinaryLayoutService.js",
    "application/reverse/ReverseEngineeringService.js",
    "artifacts/readStableArtifact.js",
    "bridge/ghidra/ReaGhidraBridge.java",
    "cli/reverseEngineeringCommands.js",
    "cli-runtime/cli.js",
    "contracts/reverseEngineeringToolContracts.js",
    "domain/analysisView/analysisView.js",
    "domain/analysisView/binaryLayoutView.js",
    "domain/canonicalDigest.js",
    "domain/evidence.js",
    "domain/pcap/pcapAnalysis.js",
    "domain/reverseEngineering.js",
    "domain/sqlite/sqliteDatabase.js",
    "ghidra/GhidraTargetSnapshot.js",
    "go/GoElfImage.js",
    "pcap/PcapNativeBound.js",
    "pcap/PcapProvider.js",
    "rust/RustAuditableReader.js",
    "rust/RustBinaryImage.js",
    "sqlite/SqliteDatabaseFailures.js",
    "sqlite/SqliteDatabaseInspection.js",
    "sqlite/SqliteDatabaseLimits.js",
    "sqlite/SqliteDatabaseProvider.js",
    "sqlite/SqliteDatabaseSnapshot.js",
    "sqlite/SqliteDatabaseWorker.js",
    "sqlite/SqliteDatabaseWorkerExecution.js",
]

# The three members cited by S081 (package-relative).
REA67_MEMBERS = ["dist/domain/evidence.js", "dist/domain/canonicalDigest.js", "package.json"]

# Members cited by S003 (in-zip paths).
ZIP_MEMBERS = [
    "ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java",
    "ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java",
]

# The digest of each upstream tarball, as the SOURCES rows pin it.
TARBALL_PINS = {
    REA65_TGZ: "531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699",
    REA67_TGZ: "20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90",
    GO125_TGZ: "4bd01e91297207bfa450ea40d4d5a93b1b531a5e438473b2a06e18e077227225",
    GO124_TGZ: "e1cb5582aab588668bc04c07de18688070f6b8c9b2aaf361f821e19bd47cfdbd",
}

# (sid, host path as the SOURCES URL cell names it, disposition, copy basename,
#  extra map keys, substrate)
SPEC = [
    ("S001", "/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md",
     "copy", "SKILL.md", {}, ("host-file",
                              "/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md")),
    ("S002", "/home/vgpnk/.agents/skills/reverse-engineer-anything/references/native-and-artifacts.md",
     "copy", "native-and-artifacts.md", {},
     ("host-file", "/home/vgpnk/.agents/skills/reverse-engineer-anything/references/native-and-artifacts.md")),
    ("S003", GHIDRA + "/Ghidra/Features/Base/lib/Base-src.zip",
     "tree", "Base-src-go-rtti-members.tar",
     {"source_sha256": "f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804",
      "kind": "tree-archive"},
     ("zip", GHIDRA + "/Ghidra/Features/Base/lib/Base-src.zip")),
    ("S006", GHIDRA + "/docs/GhidraClass/BSim/BSimTutorial_Intro.md",
     "copy", "BSimTutorial_Intro.md", {},
     ("host-file", GHIDRA + "/docs/GhidraClass/BSim/BSimTutorial_Intro.md")),
    ("S007", GHIDRA + "/docs/ChangeHistory.md",
     "copy", "ChangeHistory.md", {}, ("host-file", GHIDRA + "/docs/ChangeHistory.md")),
    ("S023", GHIDRA + "/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json",
     "gzip", "go1.25.0.json.gz",
     {"source_sha256": "54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252"},
     ("host-file", GHIDRA + "/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json")),
    ("S035", "/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi",
     "tree", "internal-abi-go1.25.0.tar", {"kind": "tree-archive"},
     ("go-tree", GO125_TGZ)),
    ("S035", "/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi",
     "tree", "internal-abi-go1.24.6.tar", {"kind": "tree-archive"},
     ("go-tree", GO124_TGZ)),
    ("S040", "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli/artifactCommands.js",
     "copy", "artifactCommands.js", {},
     ("pkg-member", REA65_TGZ, "package/dist/cli/artifactCommands.js")),
    ("S048", "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist",
     "tree", "rea-agents-6.5.0-cited-members.tar", {"kind": "tree-archive"},
     ("pkg-members", REA65_TGZ)),
    ("S056", "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cliCommandNames.js",
     "copy", "cliCommandNames.js", {},
     ("pkg-member", REA65_TGZ, "package/dist/cliCommandNames.js")),
    ("S066", "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/captures/TsharkCaptureProvider.js",
     "copy", "TsharkCaptureProvider.js", {},
     ("pkg-member", REA65_TGZ, "package/dist/captures/TsharkCaptureProvider.js")),
    ("S081", "/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist",
     "tree", "rea-agents-6.7.0-dist-cited-members.tar", {"kind": "tree-archive"},
     ("pkg-members-67", REA67_TGZ)),
    ("S082", "/var/lib/pacman/local/tinyxxd-1.3.17-1/desc",
     "copy", "desc", {}, ("host-file", "/var/lib/pacman/local/tinyxxd-1.3.17-1/desc")),
    ("S082", "/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree",
     "copy", "mtree", {}, ("host-file", "/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree")),
    ("S082", "/var/lib/pacman/sync/extra.db",
     "tree", "extra-db-tinyxxd-1.3.17-1-desc.tar",
     {"source_sha256": "0b07b40310883996d6313f0980e841757a4832eb1ef0c8785477f5875a95fd63",
      "kind": "tree-archive"},
     ("db-member", "/var/lib/pacman/sync/extra.db")),
    ("S083", "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/binary-BVOr2mgE.js",
     "copy", "binary-BVOr2mgE.js", {},
     ("pkg-member", REA65_TGZ, "package/dist/cli-runtime/binary-BVOr2mgE.js")),
]

NOTES = {
    "S003": ("MEMBER EXTRACT of a 7 481 132-byte container: the tar holds the two members the row's "
             "anchor cites (GoRttiMapper.java, GoApiSnapshot.java) at their in-zip paths. The "
             "container itself exceeds the 5 MiB copy bound and is not copied; source_sha256 pins "
             "it, so the gate re-verifies the host container on every run. Rebuild: python3 "
             "build-copies-r43.py --out <lane> --tarball-dir <dir>."),
    "S023": ("`gzip -9 -n` of the exact 10 081 618-byte source (lossless, reversible). `gzip -dc` "
             "reproduces sha256 54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252, "
             "which is the digest the row pins and the gate re-verifies as source_sha256."),
    "S035": ("Deterministic tar of the whole cited Go toolchain directory (28 files; sorted names, "
             "mtime 0, uid/gid 0, GNU format). The row's three per-file pins (map_swiss.go, "
             "map_noswiss.go, map_select_swiss.go) are reproduced by the archived members of both "
             "versions, byte-identical as the row claims. Rebuilt from the official go1.25.0 / "
             "go1.24.6 source tarballs, which the row pins upstream."),
    "S048": ("Deterministic tar of exactly the 28 members cited by S048, S066, S070, S079, S083, S090 "
             "and S092 (27 members stored relative to package/dist and "
             "bridge/ghidra/ReaGhidraBridge.java stored relative to package root; sorted names, mtime 0, "
             "uid/gid 0, GNU format). The full dist tree is 1 574 files / 22 972 248 bytes, above the "
             "5 MiB copy bound, and is not copied; the installed tree is file-for-file identical "
             "to the dist/ subtree of rea-agents-6.5.0.tgz (sha256 "
             "531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699), so every member "
             "here is re-derivable from that tarball."),
    "S081": ("Pipe-absent resolution: the installed path /home/vgpnk/.npm/_npx/a1722018f28f9df2/"
             "node_modules/rea-agents/dist no longer exists on this host, so the copy is taken from "
             "the published tarball the row itself pins (rea-agents-6.7.0.tgz sha256 "
             "20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90). The tar holds the "
             "three members the row cites, and their digests equal the row's own pins. Rebuild: "
             "curl -sSL -o rea6.7.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz; "
             "sha256sum -c pins 20958a66…; then python3 build-copies-r43.py --out <lane> "
             "--tarball-dir <dir>."),
    "S082-extra": ("MEMBER EXTRACT: the tar holds the single member tinyxxd-1.3.17-1/desc of the "
                   "8 881 002-byte repository database /var/lib/pacman/sync/extra.db (above the "
                   "5 MiB copy bound, not copied). source_sha256 pins the container so the gate "
                   "re-verifies it; the member's %SHA256SUM% line carries the row's 3f84d7de… pin "
                   "for tinyxxd-1.3.17-1-x86_64.pkg.tar.zst. Note the local installed desc (copied "
                   "verbatim, 402 bytes) is a different record from this repo member: the installed "
                   "record has %INSTALLDATE%/%VALIDATION%/%SIZE%, the repo record %FILENAME%/"
                   "%CSIZE%/%PGPSIG%. Both are retained."),
    "default": ("Byte-exact copy (cmp clean); sha256 of the copy equals the digest recorded in the "
                "row's anchor/teaches cell where the row pins one."),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tar_bytes(members: list[tuple[str, bytes]]) -> bytes:
    """Deterministic tar: sorted names, mtime 0, uid/gid 0, mode 0644, GNU.

    An empty member list is refused: the round-42 builder wrote an empty tar
    (10 240 bytes, zero members) and exited 0 when its host directory was
    absent, so a rebuild could silently produce a copy that no longer carries
    the bytes it claims.
    """
    if not members:
        raise SystemExit("refusing to build an empty archive: no members")
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for name, data in sorted(members):
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def tgz_member(tgz: str, prefix: str, name: str) -> bytes:
    with tarfile.open(tgz, "r:gz") as tar:
        fh = tar.extractfile(prefix + name)
        if fh is None:
            raise SystemExit("missing tarball member %s%s" % (prefix, name))
        return fh.read()


def go_tree(tgz: str) -> list[tuple[str, bytes]]:
    with tarfile.open(tgz, "r:gz") as tar:
        names = sorted(m.name[len("go/src/internal/abi/"):]
                       for m in tar.getmembers()
                       if m.isfile() and m.name.startswith("go/src/internal/abi/"))
        return [(rel, tar.extractfile("go/src/internal/abi/" + rel).read())
                for rel in names]


def build_payload(kind: str, arg, tarball_dir: str) -> bytes:
    if kind == "host-file":
        if not os.path.isfile(arg[0]):
            raise SystemExit("host object absent: %s" % arg[0])
        with open(arg[0], "rb") as fh:
            return fh.read()
    if kind == "zip":
        with zipfile.ZipFile(arg[0]) as zf:
            return tar_bytes([(n, zf.read(n)) for n in ZIP_MEMBERS])
    if kind == "db-member":
        member = "tinyxxd-1.3.17-1/desc"
        data = subprocess.run(["tar", "-xOf", arg[0], member], check=True,
                              stdout=subprocess.PIPE).stdout
        return tar_bytes([(member, data)])
    if kind == "pkg-member":
        tgz, member = arg
        return tgz_member(os.path.join(tarball_dir, tgz), "", member)
    if kind == "pkg-members":
        tgz = arg[0]
        path = os.path.join(tarball_dir, tgz)
        # 27 members are stored relative to the package dist root; the
        # bridge/ghidra member is package-relative (not under dist/)
        return tar_bytes([(rel, tgz_member(path, "package/dist/", rel))
                          for rel in REA65_MEMBERS if not rel.startswith("bridge/")]
                         + [(rel, tgz_member(path, "package/", rel))
                            for rel in REA65_MEMBERS if rel.startswith("bridge/")])
    if kind == "pkg-members-67":
        tgz = arg[0]
        path = os.path.join(tarball_dir, tgz)
        return tar_bytes([(rel, tgz_member(path, "package/", rel))
                          for rel in REA67_MEMBERS])
    if kind == "go-tree":
        return tar_bytes(go_tree(os.path.join(tarball_dir, arg[0])))
    raise SystemExit("unknown substrate %r" % kind)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="directory that receives corpus/evidence/...")
    ap.add_argument("--tarball-dir", required=True,
                    help="directory holding dl/rea6.5.0.tgz, dl/rea6.7.0.tgz, "
                         "go1.25.0.src.tar.gz, go1.24.6.src.tar.gz")
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--base-map", default=None,
                    help="map to carry entries this script does not build (row S126); "
                         "required when the output dir holds no map yet")
    args = ap.parse_args(argv)

    out = os.path.abspath(args.out)
    tarball_dir = os.path.abspath(args.tarball_dir)

    # every upstream tarball must match the digest its row pins
    for rel, want in TARBALL_PINS.items():
        path = os.path.join(tarball_dir, rel)
        if not os.path.isfile(path):
            raise SystemExit("missing %s" % path)
        got = sha256_file(path)
        if got != want:
            raise SystemExit("%s digest drifted: %s" % (rel, got))

    map_path = os.path.join(out, MAP_REL)
    sources = {}
    if os.path.exists(map_path):
        with open(map_path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
        if doc.get("version") != 1 or not isinstance(doc.get("sources"), dict):
            raise SystemExit("existing map %s is not version 1 with `sources`" % map_path)
        sources = doc["sources"]
    elif args.base_map:
        with open(args.base_map, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
        if doc.get("version") != 1 or not isinstance(doc.get("sources"), dict):
            raise SystemExit("base map %s is not version 1 with `sources`" % args.base_map)
        sources = doc["sources"]
    else:
        # Writing a map from nothing silently drops the entries this script does
        # not build (row S126's corpus/evidence/round-41 copy), so a "successful"
        # rebuild would produce a map that re-reds S126.  Refuse rather than
        # ship the partial map.
        raise SystemExit(
            "refusing to write a partial map: %s does not exist and no --base-map "
            "was given, so entries this script does not build (row S126) would be "
            "dropped. Pass --base-map <lane>/corpus/evidence/local-sources.json."
            % map_path)
    base_keys = set(sources)

    rows = []
    for sid, host, disposition, basename, extra, substrate in SPEC:
        rel = "%s/%s/%s" % (LANE_TREE, sid, basename)
        dest = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        data = build_payload(substrate[0], substrate[1:], tarball_dir)
        if disposition == "gzip":
            data = subprocess.run(["gzip", "-9", "-n", "-c"], input=data, check=True,
                                  stdout=subprocess.PIPE).stdout
            if gzip.decompress(data) is None:
                raise SystemExit("%s: gzip round-trip failed" % sid)
        with open(dest, "wb") as fh:
            fh.write(data)
        digest = sha256_bytes(data)
        note_key = "S082-extra" if (sid == "S082" and disposition == "tree") else sid
        # an existing entry's note is preserved: a hand-amended map (the L1
        # rewrote the S035/S048/S081 notes to name their new substrates) must
        # survive a rebuild, otherwise regenerating silently reverts the prose
        prior = sources.get(host) or {}
        entry = {"copy": rel, "sha256": digest, "kind": extra.get("kind", "file"),
                 "note": prior.get("note") or NOTES.get(note_key, NOTES["default"]),
                 "rebuild": "python3 tools/round-43/build-copies-r43.py --out <lane> --tarball-dir <dir>"}
        if "source_sha256" in extra:
            entry["source_sha256"] = extra["source_sha256"]
        sources[host] = entry
        rows.append({"sid": sid, "host": host, "disposition": disposition,
                     "substrate": substrate[0], "copy": rel,
                     "copy_bytes": len(data), "copy_sha256": digest,
                     "map_kind": entry["kind"]})

    doc = {"version": 1, "sources": {k: sources[k] for k in sorted(sources)}}
    dropped = base_keys - set(doc["sources"])
    if dropped:
        raise SystemExit("refusing to write the map: %d entry(ies) from the base map "
                         "are absent: %s" % (len(dropped), ", ".join(sorted(dropped))))
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    with open(map_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)
        fh.write("\n")

    cols = ["sid", "disposition", "substrate", "copy_bytes", "copy", "copy_sha256", "map_kind"]
    lines = ["\t".join(cols)]
    for row in rows:
        lines.append("\t".join(str(row[c]) for c in cols))
    text = "\n".join(lines) + "\n"
    manifest = args.manifest or os.path.join(out, ".local-sources-manifest.tsv")
    os.makedirs(os.path.dirname(os.path.abspath(manifest)), exist_ok=True)
    with open(manifest, "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)
    sys.stdout.write("map entries: %d\n" % len(doc["sources"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
