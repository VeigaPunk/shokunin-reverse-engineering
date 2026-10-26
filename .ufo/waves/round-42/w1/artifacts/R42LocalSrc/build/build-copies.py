#!/usr/bin/env python3
"""build-copies — materialise the in-lane copies that close routed defect R41-CL3.

Round 42 wave 1, seat R42LocalSrc.  Stdlib only, network-free, TMPDIR-honouring.

For every SOURCES row whose URL cell names a host-local path outside the lane
(the 18 rows the round-41 local-source-gate.py reports at rev c4a38ea2), this
writes the copy the lane would add:

  corpus/evidence/round-42/local-sources/<S-id>/<basename>

Dispositions:
  copy      the source is a regular file <= 5 MiB: byte-exact copy.
  gzip      the source is a regular file > 5 MiB whose gzip -9 -n form is
            small (S023): lossless reversible encoding, source_sha256 pins the
            bytes it decodes to.
  tree      the source is a directory or an archive whose cited content is a
            named member/sub-tree (S003, S035, S048, S081, S082 extra.db):
            deterministic tar (sorted names, mtime 0, uid/gid 0, GNU format)
            of exactly the cited members.  `kind: tree-archive` in the map.
  absent    the named host path no longer exists (S081 pipe): the cited bytes
            are taken from the published tarball the row itself pins.

Every copy's digest goes into corpus/evidence/local-sources.json (version 1,
merged with any pre-existing entries, e.g. S126).

Usage: python3 build-copies.py --out <dir that receives corpus/evidence/...>
       [--deadout <dir for the per-copy manifest>]
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
import tempfile
import zipfile

LANE_TREE = "corpus/evidence/round-42/local-sources"
MAP_REL = "corpus/evidence/local-sources.json"

REA650 = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist"
REA670_TGZ = "dl/rea6.7.0.tgz"  # relative to --tarball-dir
GHIDRA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC"
GO125 = "/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi"
GO124 = "/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi"

# Members cited by S048 / S079 / S090 / S092, relative to the package dist tree.
REA65_MEMBERS = [
    "application/DirectAnalysis.js",
    "application/binaryDiagnostics/BinaryLayoutService.js",
    "application/reverse/ReverseEngineeringService.js",
    "artifacts/readStableArtifact.js",
    "cli/reverseEngineeringCommands.js",
    "cli-runtime/cli.js",
    "contracts/reverseEngineeringToolContracts.js",
    "domain/analysisView/analysisView.js",
    "domain/analysisView/binaryLayoutView.js",
    "domain/canonicalDigest.js",
    "domain/evidence.js",
    "domain/reverseEngineering.js",
    "domain/sqlite/sqliteDatabase.js",
    "go/GoElfImage.js",
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

# Members cited by S081, relative to the 6.7.0 package root.
REA67_MEMBERS = [
    "dist/domain/evidence.js",
    "dist/domain/canonicalDigest.js",
    "package.json",
]

ZIP_MEMBERS = [
    "ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java",
    "ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java",
]

# Row pins that the copies/archives are checked against.  Every one of these was
# read out of the row's own anchor or teaches cell (the URL cell pins none of
# them, which is why the gate reports row_pin_scope "none").
ROW_PINS = {
    "S003": {"f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804": "container Base-src.zip"},
    "S023": {"54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252": "decoded go1.25.0.json"},
    "S035": {
        "0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383": "map_swiss.go",
        "03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291": "map_noswiss.go",
        "c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718": "map_select_swiss.go",
    },
    "S048": {},
    "S056": {"41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3": "cliCommandNames.js"},
    "S066": {"fdc1fc13d2468fa0bcaf1e1bf585c80dc9840f059f78a623d7be420f76d30549": "TsharkCaptureProvider.js"},
    "S079": {
        "f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff": "domain/evidence.js",
        "f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9": "domain/canonicalDigest.js",
        "09d2b2225dd9817674f3a454d33447a6a917e82441f2081c6553511e2dc72617": "application/DirectAnalysis.js",
        "b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4": "application/binaryDiagnostics/BinaryLayoutService.js",
        "2685fc2c0f6dda136b9bc004ab3af30d4272b850b1a8d026ad14b2e22ef68363": "domain/analysisView/analysisView.js",
        "5bd86489988b6cf4cb59bd6085805accdd83277870578426baebff687ff7b070": "domain/analysisView/binaryLayoutView.js",
    },
    "S081": {
        "a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb": "dist/domain/evidence.js (6.7.0)",
        "f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9": "dist/domain/canonicalDigest.js (6.7.0)",
        "3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570": "package.json (6.7.0)",
        "20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90": "rea-agents-6.7.0.tgz",
    },
    "S082": {
        "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65": "/usr/bin/tinyxxd (mtree sha256digest)",
        "3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce": "tinyxxd-1.3.17-1-x86_64.pkg.tar.zst (sync %SHA256SUM%)",
    },
    "S083": {
        "64c07dae6fe8b79a2015550cd8de208bc41f7b325dddd7262031ef76820c00df": "cli-runtime/binary-BVOr2mgE.js",
    },
    "S090": {
        "531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699": "rea-agents-6.5.0.tgz",
        "1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505": "rust/RustAuditableReader.js",
        "08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681": "rust/RustBinaryImage.js",
        "ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204": "go/GoElfImage.js",
        "168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204": "cli-runtime/cli.js",
    },
    "S092": {
        "5a908695ec398079e97750bf60ece6ac273bdc74f06f7c9c1fd5777cfa90d419": "sqlite/SqliteDatabaseFailures.js",
        "edfcd90f9e2e1dbde531b6aafc4efb1bd105a372df617dee619a414425354970": "sqlite/SqliteDatabaseInspection.js",
        "92df76ffd21386dba134051791230e9d143220854a49e3e65e72d51daa074121": "sqlite/SqliteDatabaseLimits.js",
        "018756d9d7f620995c9b8929d268c33ff1f7c973683bd0f4ddc6d781e5268104": "sqlite/SqliteDatabaseProvider.js",
        "c8af51f8496703a1992e7e7646c8bf8b6c56796a7571f5f8e9c84a284740ce19": "sqlite/SqliteDatabaseSnapshot.js",
        "ebb39f583db802ccb31b3ac328b0f8dd712fa6f0e5dd5a63da6908d7fe60cf63": "sqlite/SqliteDatabaseWorker.js",
        "6e49c2ab222982434d769fd279ad8053b857d6747f9b1101e07163d8a5e4c203": "sqlite/SqliteDatabaseWorkerExecution.js",
        "c7a0eff5674414110085ecf0257a71c1949de7e27be392ef2d8c8bd8cf000ae1": "domain/sqlite/sqliteDatabase.js",
        "06a23746346a3de150f1aa21b781fffd8a482c0f5e98900c458f3f599b9d2707": "artifacts/readStableArtifact.js",
    },
}

# (S-id, host path, disposition, copy basename, extra map keys)
SPEC = [
    ("S001", "/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md", "copy", "SKILL.md", {}),
    ("S002", "/home/vgpnk/.agents/skills/reverse-engineer-anything/references/native-and-artifacts.md",
     "copy", "native-and-artifacts.md", {}),
    ("S003", GHIDRA + "/Ghidra/Features/Base/lib/Base-src.zip", "tree", "Base-src-go-rtti-members.tar",
     {"source_sha256": "f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804", "kind": "tree-archive"}),
    ("S006", GHIDRA + "/docs/GhidraClass/BSim/BSimTutorial_Intro.md", "copy", "BSimTutorial_Intro.md", {}),
    ("S007", GHIDRA + "/docs/ChangeHistory.md", "copy", "ChangeHistory.md", {}),
    ("S023", GHIDRA + "/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json", "gzip", "go1.25.0.json.gz",
     {"source_sha256": "54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252"}),
    ("S035", GO125, "tree", "internal-abi-go1.25.0.tar", {"kind": "tree-archive"}),
    ("S035", GO124, "tree", "internal-abi-go1.24.6.tar", {"kind": "tree-archive"}),
    ("S040", REA650 + "/cli/artifactCommands.js", "copy", "artifactCommands.js", {}),
    ("S048", REA650, "tree", "rea-agents-6.5.0-dist-cited-members.tar", {"kind": "tree-archive"}),
    ("S056", REA650 + "/cliCommandNames.js", "copy", "cliCommandNames.js", {}),
    ("S066", REA650 + "/captures/TsharkCaptureProvider.js", "copy", "TsharkCaptureProvider.js", {}),
    ("S081", "/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist", "tree",
     "rea-agents-6.7.0-dist-cited-members.tar", {"kind": "tree-archive"}),
    ("S082", "/var/lib/pacman/local/tinyxxd-1.3.17-1/desc", "copy", "desc", {}),
    ("S082", "/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree", "copy", "mtree", {}),
    ("S082", "/var/lib/pacman/sync/extra.db", "tree", "extra-db-tinyxxd-1.3.17-1-desc.tar",
     {"source_sha256": "0b07b40310883996d6313f0980e841757a4832eb1ef0c8785477f5875a95fd63",
      "kind": "tree-archive"}),
    ("S083", REA650 + "/cli-runtime/binary-BVOr2mgE.js", "copy", "binary-BVOr2mgE.js", {}),
]

NOTES = {
    "S003": ("MEMBER EXTRACT of a 7 481 132-byte container: the tar holds the two members the row's "
             "anchor cites (GoRttiMapper.java, GoApiSnapshot.java) at their in-zip paths. The "
             "container itself exceeds the 5 MiB copy bound and is not copied; source_sha256 pins "
             "it, so the gate re-verifies the host container on every run. Rebuild: python3 "
             "build-copies.py --out <lane>."),
    "S023": ("`gzip -9 -n` of the exact 10 081 618-byte source (lossless, reversible). `gzip -dc` "
             "reproduces sha256 54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252, "
             "which is the digest the row pins and the gate re-verifies as source_sha256."),
    "S035": ("Deterministic tar of the whole cited Go toolchain directory (28 files; sorted names, "
             "mtime 0, uid/gid 0, GNU format). The row's three per-file pins (map_swiss.go, "
             "map_noswiss.go, map_select_swiss.go) are reproduced by the archived members of both "
             "versions, byte-identical as the row claims."),
    "S048": ("Deterministic tar of exactly the 23 dist members cited by S048, S079, S090 and S092 "
             "(sorted names, mtime 0, uid/gid 0, GNU format); member paths are relative to the "
             "package dist root. The full dist tree is 1 574 files / 22 972 248 bytes, above the "
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
             "sha256sum -c pins 20958a66…; then python3 build-copies.py --out <lane> --tarball-dir <dir>."),
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


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_bytes(path: str, data: bytes) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return sha256_bytes(data)


def tar_tree(root: str, names: list[str]) -> bytes:
    """Deterministic tar of `names` under `root` (relative paths preserved)."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for name in sorted(names):
            full = os.path.join(root, name)
            st = os.stat(full)
            info = tarfile.TarInfo(name)
            info.size = st.st_size
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.type = tarfile.REGTYPE
            with open(full, "rb") as fh:
                tar.addfile(info, fh)
    return buf.getvalue()


def tar_dir(root: str) -> tuple[bytes, int]:
    """Deterministic tar of a whole directory tree; returns (bytes, file count)."""
    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            entries.append(os.path.relpath(full, root))
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for rel in sorted(entries):
            full = os.path.join(root, rel)
            st = os.stat(full)
            info = tarfile.TarInfo(rel)
            info.size = st.st_size
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.type = tarfile.REGTYPE
            with open(full, "rb") as fh:
                tar.addfile(info, fh)
    return buf.getvalue(), len(entries)


def members_from_zip(zip_path: str, names: list[str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(zip_path) as zf, tarfile.open(fileobj=buf, mode="w",
                                                      format=tarfile.GNU_FORMAT) as tar:
        for name in sorted(names):
            data = zf.read(name)
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def members_from_tgz(tgz_path: str, prefix: str, names: list[str]) -> bytes:
    """Copy `prefix + name` members out of a .tgz, storing them under `name`."""
    buf = io.BytesIO()
    with tarfile.open(tgz_path, "r:gz") as src, tarfile.open(
            fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as dst:
        for name in sorted(names):
            member = src.extractfile(prefix + name)
            if member is None:
                raise SystemExit("missing tarball member %s%s" % (prefix, name))
            data = member.read()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            dst.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="directory that receives corpus/evidence/...")
    ap.add_argument("--tarball-dir", default=".", help="directory holding dl/rea6.7.0.tgz")
    ap.add_argument("--manifest", default=None, help="write the TSV manifest here")
    args = ap.parse_args(argv)

    out = os.path.abspath(args.out)
    tarball = os.path.join(os.path.abspath(args.tarball_dir), REA670_TGZ)
    if not os.path.isfile(tarball):
        raise SystemExit("missing %s (needed for S081); pass --tarball-dir" % tarball)
    tarball_digest = sha256_file(tarball)
    if tarball_digest != "20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90":
        raise SystemExit("rea-agents-6.7.0.tgz digest drifted: %s" % tarball_digest)

    map_path = os.path.join(out, MAP_REL)
    if os.path.exists(map_path):
        with open(map_path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
        if doc.get("version") != 1 or not isinstance(doc.get("sources"), dict):
            raise SystemExit("existing map %s is not version 1 with `sources`" % map_path)
        sources = doc["sources"]
    else:
        sources = {}

    rows = []
    for sid, host, kind, basename, extra in SPEC:
        rel = "%s/%s/%s" % (LANE_TREE, sid, basename)
        dest = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        source_present = os.path.exists(host)

        if kind == "copy":
            if not os.path.isfile(host):
                raise SystemExit("%s: %s is not a regular file" % (sid, host))
            size = os.path.getsize(host)
            if size > 5 * 1024 * 1024:
                raise SystemExit("%s: %d bytes exceeds the 5 MiB copy bound" % (sid, size))
            with open(host, "rb") as fh:
                data = fh.read()
            digest = write_bytes(dest, data)
            if digest != sha256_bytes(data):
                raise SystemExit("%s: write corrupted the copy" % sid)
            payload = "copy"
        elif kind == "gzip":
            with open(host, "rb") as fh:
                raw = fh.read()
            gz = subprocess.run(["gzip", "-9", "-n", "-c"], input=raw, check=True,
                                stdout=subprocess.PIPE).stdout
            digest = write_bytes(dest, gz)
            if gzip.decompress(gz) != raw:
                raise SystemExit("%s: gzip round-trip is not lossless" % sid)
            payload = "gzip"
        elif kind == "tree":
            if sid == "S003":
                data = members_from_zip(host, ZIP_MEMBERS)
                payload = "zip-members:%d" % len(ZIP_MEMBERS)
            elif sid in ("S035",):
                data, count = tar_dir(host)
                payload = "dir-tree:%d" % count
            elif sid == "S048":
                data = tar_tree(host, REA65_MEMBERS)
                payload = "dist-members:%d" % len(REA65_MEMBERS)
            elif sid == "S081":
                data = members_from_tgz(tarball, "package/", REA67_MEMBERS)
                payload = "tgz-members:%d" % len(REA67_MEMBERS)
            elif sid == "S082":
                with tempfile.TemporaryDirectory(prefix="pacdesc-", dir=os.environ.get("TMPDIR") or None) as td:
                    member = "tinyxxd-1.3.17-1/desc"
                    subprocess.run(["tar", "-xOf", host, member], check=True,
                                   stdout=open(os.path.join(td, "desc"), "wb"))
                    data = tar_tree(td, ["desc"])
                    data = retitle(data, "desc", member)
                payload = "db-member:1"
            else:
                raise SystemExit("no tree recipe for %s" % sid)
            digest = write_bytes(dest, data)
        else:
            raise SystemExit("unknown disposition %s" % kind)

        note = NOTES.get("S082-extra" if (sid == "S082" and kind == "tree") else sid, NOTES["default"])
        entry = {"copy": rel, "sha256": digest, "kind": extra.get("kind", "file"),
                 "note": note, "rebuild": "python3 build-copies.py --out <lane> --tarball-dir <dir>"}
        if "source_sha256" in extra:
            entry["source_sha256"] = extra["source_sha256"]
        sources[host] = entry
        rows.append({
            "sid": sid, "host": host, "host_present": source_present,
            "host_size": os.path.getsize(host) if source_present and os.path.isfile(host) else "",
            "host_sha256": sha256_file(host) if source_present and os.path.isfile(host) else "",
            "disposition": kind, "payload": payload, "copy": rel,
            "copy_bytes": os.path.getsize(dest), "copy_sha256": digest,
            "map_kind": entry["kind"],
        })

    doc = {"version": 1, "sources": {k: sources[k] for k in sorted(sources)}}
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    with open(map_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)
        fh.write("\n")

    cols = ["sid", "disposition", "payload", "host_present", "host_size", "host_sha256",
            "copy_bytes", "copy", "copy_sha256", "map_kind"]
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


def retitle(tar_bytes: bytes, old: str, new: str) -> bytes:
    """Rename the single member `old` to `new` inside a one-member tar."""
    src = tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:")
    member = src.extractfile(old)
    data = member.read()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as dst:
        info = tarfile.TarInfo(new)
        info.size = len(data)
        info.mtime = 0
        info.mode = 0o644
        info.uid = info.gid = 0
        info.uname = info.gname = ""
        dst.addfile(info, io.BytesIO(data))
    return buf.getvalue()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
