#!/usr/bin/env python3
"""r43-reverify — re-validate the R43-C2 landing pack against live + pinned substrates.

Seat R43C2Land, round 43 wave 1.  Stdlib only, network-free (the caller
supplies the downloaded tarballs), TMPDIR-honouring, no hardcoded /tmp.

Three independent questions are answered, one TSV line each:

  A. PACK      does every copy in the pack exist, and does its sha256 equal
               the map entry?  (pack self-consistency)
  B. REDERIVE  can each copy be rebuilt today from the substrate the row
               itself pins -- the live host object when it is still present,
               otherwise the row-pinned upstream tarball -- and does the
               rebuilt artefact match the copy byte-for-byte?
  C. PIN       does every 64-hex digest the 18 rows pin still resolve against
               the live/pinned object it names?

Usage:
  r43-reverify.py --pack <dir with corpus/evidence/...> \\
                  --scratch <dir holding dl/rea6.5.0.tgz, dl/rea6.7.0.tgz,
                             go1.25.0.src.tar.gz, go1.24.6.src.tar.gz> \\
                  --sources <lane>/corpus/SOURCES.md \\
                  --out <receipt.tsv>
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

# --- the 17 copies the round-42 seat prepared, and their substrates ---------
#
# Each entry: (sid, map-copy-relpath, substrate-kind, substrate-arg)
#
# substrate kinds:
#   host-file     the live host path, byte-compared
#   host-gz       the live host path, re-encoded with gzip -9 -n
#   zip-members   the live host zip, two named members
#   pkg-member    a member of the row-pinned npm tarball (dist/<path>)
#   pkg-members   the 23 cited dist members of the 6.5.0 npm tarball
#   go-tree       the internal/abi tree of the row-pinned Go source tarball
#   db-member     the tinyxxd desc member of the live pacman repository db
#   tgz-members   the three cited members of the 6.7.0 npm tarball

GHIDRA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC"
REA65_TGZ = "dl/rea6.5.0.tgz"
REA67_TGZ = "dl/rea6.7.0.tgz"
GO125_TGZ = "go1.25.0.src.tar.gz"
GO124_TGZ = "go1.24.6.src.tar.gz"

SPEC = [
    ("S001", "S001/SKILL.md", "host-file",
     "/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md"),
    ("S002", "S002/native-and-artifacts.md", "host-file",
     "/home/vgpnk/.agents/skills/reverse-engineer-anything/references/native-and-artifacts.md"),
    ("S003", "S003/Base-src-go-rtti-members.tar", "zip-members",
     GHIDRA + "/Ghidra/Features/Base/lib/Base-src.zip"),
    ("S006", "S006/BSimTutorial_Intro.md", "host-file",
     GHIDRA + "/docs/GhidraClass/BSim/BSimTutorial_Intro.md"),
    ("S007", "S007/ChangeHistory.md", "host-file",
     GHIDRA + "/docs/ChangeHistory.md"),
    ("S023", "S023/go1.25.0.json.gz", "host-gz",
     GHIDRA + "/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json"),
    ("S035", "S035/internal-abi-go1.25.0.tar", "go-tree", GO125_TGZ),
    ("S035", "S035/internal-abi-go1.24.6.tar", "go-tree", GO124_TGZ),
    ("S040", "S040/artifactCommands.js", "pkg-member",
     (REA65_TGZ, "package/dist/cli/artifactCommands.js")),
    ("S048", "S048/rea-agents-6.5.0-cited-members.tar", "pkg-members", REA65_TGZ),
    ("S056", "S056/cliCommandNames.js", "pkg-member",
     (REA65_TGZ, "package/dist/cliCommandNames.js")),
    ("S066", "S066/TsharkCaptureProvider.js", "pkg-member",
     (REA65_TGZ, "package/dist/captures/TsharkCaptureProvider.js")),
    ("S081", "S081/rea-agents-6.7.0-dist-cited-members.tar", "tgz-members", REA67_TGZ),
    ("S082", "S082/desc", "host-file", "/var/lib/pacman/local/tinyxxd-1.3.17-1/desc"),
    ("S082", "S082/mtree", "host-file", "/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree"),
    ("S082", "S082/extra-db-tinyxxd-1.3.17-1-desc.tar", "db-member",
     "/var/lib/pacman/sync/extra.db"),
    ("S083", "S083/binary-BVOr2mgE.js", "pkg-member",
     (REA65_TGZ, "package/dist/cli-runtime/binary-BVOr2mgE.js")),
]

# The 23 dist members cited by S048, S079, S090 and S092 (package-relative).
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

# --- the row pins (41 digests over the 18 rows) -----------------------------
#
# subject -> (kind, argument).  kind:
#   file       sha256 of a live host file
#   zip        sha256 of a member of a live host zip
#   pkg        sha256 of package/<path> in the 6.5.0 npm tarball
#   pkg67      sha256 of package/<path> in the 6.7.0 npm tarball
#   gomember   sha256 of go/src/internal/abi/<name> in the Go source tarball
#   dbfield    the %SHA256SUM% value inside the tinyxxd desc member
#   mtreefield the sha256digest of /usr/bin/tinyxxd recorded in the mtree

PINS = [
    # S003
    ("S003", "container Base-src.zip", "file",
     GHIDRA + "/Ghidra/Features/Base/lib/Base-src.zip",
     "f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804"),
    ("S003", "GoRttiMapper.java", "zip",
     (GHIDRA + "/Ghidra/Features/Base/lib/Base-src.zip", ZIP_MEMBERS[0]),
     "2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95"),
    ("S003", "GoApiSnapshot.java", "zip",
     (GHIDRA + "/Ghidra/Features/Base/lib/Base-src.zip", ZIP_MEMBERS[1]),
     "765d25365a8c379c929097a6602df5fa75049f871eb0f610d5376d630d95eb7d"),
    # S023
    ("S023", "go1.25.0.json (decoded)", "file",
     GHIDRA + "/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json",
     "54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252"),
    # S035
    ("S035", "map_swiss.go (1.25.0)", "gomember", (GO125_TGZ, "map_swiss.go"),
     "0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383"),
    ("S035", "map_noswiss.go (1.25.0)", "gomember", (GO125_TGZ, "map_noswiss.go"),
     "03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291"),
    ("S035", "map_select_swiss.go (1.25.0)", "gomember", (GO125_TGZ, "map_select_swiss.go"),
     "c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718"),
    ("S035", "map_swiss.go (1.24.6)", "gomember", (GO124_TGZ, "map_swiss.go"),
     "0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383"),
    ("S035", "map_noswiss.go (1.24.6)", "gomember", (GO124_TGZ, "map_noswiss.go"),
     "03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291"),
    ("S035", "map_select_swiss.go (1.24.6)", "gomember", (GO124_TGZ, "map_select_swiss.go"),
     "c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718"),
    # S056
    ("S056", "cliCommandNames.js", "pkg", "package/dist/cliCommandNames.js",
     "41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3"),
    # S066
    ("S066", "TsharkCaptureProvider.js", "pkg",
     "package/dist/captures/TsharkCaptureProvider.js",
     "fdc1fc13d2468fa0bcaf1e1bf585c80dc9840f059f78a623d7be420f76d30549"),
    ("S066", "domain/pcap/pcapAnalysis.js", "pkg",
     "package/dist/domain/pcap/pcapAnalysis.js",
     "7651b4c5582b62513196146b7aa08043fab93d0848ce7f8680523d867597c641"),
    # S070
    ("S070", "TsharkCaptureProvider.js", "pkg",
     "package/dist/captures/TsharkCaptureProvider.js",
     "fdc1fc13d2468fa0bcaf1e1bf585c80dc9840f059f78a623d7be420f76d30549"),
    ("S070", "pcap/PcapProvider.js", "pkg", "package/dist/pcap/PcapProvider.js",
     "16a4d813665208bd4f99229f431e0379a6e8b31d72a717d6c451c38833ed64d4"),
    ("S070", "pcap/PcapNativeBound.js", "pkg", "package/dist/pcap/PcapNativeBound.js",
     "24811182c301a73ec1cb9792f31d6db911aec9c9f1bf71cf4bc7932bb0838cd2"),
    # S079
    ("S079", "domain/evidence.js", "pkg", "package/dist/domain/evidence.js",
     "f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff"),
    ("S079", "domain/canonicalDigest.js", "pkg", "package/dist/domain/canonicalDigest.js",
     "f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9"),
    ("S079", "application/DirectAnalysis.js", "pkg",
     "package/dist/application/DirectAnalysis.js",
     "09d2b2225dd9817674f3a454d33447a6a917e82441f2081c6553511e2dc72617"),
    ("S079", "application/binaryDiagnostics/BinaryLayoutService.js", "pkg",
     "package/dist/application/binaryDiagnostics/BinaryLayoutService.js",
     "b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4"),
    ("S079", "domain/analysisView/analysisView.js", "pkg",
     "package/dist/domain/analysisView/analysisView.js",
     "2685fc2c0f6dda136b9bc004ab3af30d4272b850b1a8d026ad14b2e22ef68363"),
    ("S079", "domain/analysisView/binaryLayoutView.js", "pkg",
     "package/dist/domain/analysisView/binaryLayoutView.js",
     "5bd86489988b6cf4cb59bd6085805accdd83277870578426baebff687ff7b070"),
    # S081
    ("S081", "rea-agents-6.7.0.tgz", "file", REA67_TGZ,
     "20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90"),
    ("S081", "dist/domain/evidence.js (6.7.0)", "pkg67", "package/dist/domain/evidence.js",
     "a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb"),
    ("S081", "dist/domain/canonicalDigest.js (6.7.0)", "pkg67",
     "package/dist/domain/canonicalDigest.js",
     "f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9"),
    ("S081", "package.json (6.7.0)", "pkg67", "package/package.json",
     "3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570"),
    # S082
    ("S082", "/usr/bin/tinyxxd (mtree)", "mtreefield",
     "/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree",
     "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65"),
    ("S082", "tinyxxd-1.3.17-1-x86_64.pkg.tar.zst (sync %SHA256SUM%)", "dbfield",
     "/var/lib/pacman/sync/extra.db",
     "3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce"),
    # S083
    ("S083", "cli-runtime/binary-BVOr2mgE.js", "pkg",
     "package/dist/cli-runtime/binary-BVOr2mgE.js",
     "64c07dae6fe8b79a2015550cd8de208bc41f7b325dddd7262031ef76820c00df"),
    ("S083", "ghidra/GhidraTargetSnapshot.js", "pkg",
     "package/dist/ghidra/GhidraTargetSnapshot.js",
     "a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b"),
    ("S083", "bridge/ghidra/ReaGhidraBridge.java", "pkg",
     "package/bridge/ghidra/ReaGhidraBridge.java",
     "db16aed4d16ab94da883843281ef7a8a33a244cd8379bd4013e8dee479c0a105"),
    # S090
    ("S090", "rea-agents-6.5.0.tgz", "file", REA65_TGZ,
     "531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699"),
    ("S090", "rust/RustAuditableReader.js", "pkg",
     "package/dist/rust/RustAuditableReader.js",
     "1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505"),
    ("S090", "rust/RustBinaryImage.js", "pkg", "package/dist/rust/RustBinaryImage.js",
     "08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681"),
    ("S090", "go/GoElfImage.js", "pkg", "package/dist/go/GoElfImage.js",
     "ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204"),
    ("S090", "cli-runtime/cli.js", "pkg", "package/dist/cli-runtime/cli.js",
     "168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204"),
    # S092
    ("S092", "rea-agents-6.5.0.tgz", "file", REA65_TGZ,
     "531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699"),
    ("S092", "sqlite/SqliteDatabaseFailures.js", "pkg",
     "package/dist/sqlite/SqliteDatabaseFailures.js",
     "5a908695ec398079e97750bf60ece6ac273bdc74f06f7c9c1fd5777cfa90d419"),
    ("S092", "sqlite/SqliteDatabaseInspection.js", "pkg",
     "package/dist/sqlite/SqliteDatabaseInspection.js",
     "edfcd90f9e2e1dbde531b6aafc4efb1bd105a372df617dee619a414425354970"),
    ("S092", "sqlite/SqliteDatabaseLimits.js", "pkg",
     "package/dist/sqlite/SqliteDatabaseLimits.js",
     "92df76ffd21386dba134051791230e9d143220854a49e3e65e72d51daa074121"),
    ("S092", "sqlite/SqliteDatabaseProvider.js", "pkg",
     "package/dist/sqlite/SqliteDatabaseProvider.js",
     "018756d9d7f620995c9b8929d268c33ff1f7c973683bd0f4ddc6d781e5268104"),
    ("S092", "sqlite/SqliteDatabaseSnapshot.js", "pkg",
     "package/dist/sqlite/SqliteDatabaseSnapshot.js",
     "c8af51f8496703a1992e7e7646c8bf8b6c56796a7571f5f8e9c84a284740ce19"),
    ("S092", "sqlite/SqliteDatabaseWorker.js", "pkg",
     "package/dist/sqlite/SqliteDatabaseWorker.js",
     "ebb39f583db802ccb31b3ac328b0f8dd712fa6f0e5dd5a63da6908d7fe60cf63"),
    ("S092", "sqlite/SqliteDatabaseWorkerExecution.js", "pkg",
     "package/dist/sqlite/SqliteDatabaseWorkerExecution.js",
     "6e49c2ab222982434d769fd279ad8053b857d6747f9b1101e07163d8a5e4c203"),
    ("S092", "domain/sqlite/sqliteDatabase.js", "pkg",
     "package/dist/domain/sqlite/sqliteDatabase.js",
     "c7a0eff5674414110085ecf0257a71c1949de7e27be392ef2d8c8bd8cf000ae1"),
    ("S092", "artifacts/readStableArtifact.js", "pkg",
     "package/dist/artifacts/readStableArtifact.js",
     "06a23746346a3de150f1aa21b781fffd8a482c0f5e98900c458f3f599b9d2707"),
]


# ----------------------------------------------------------------- helpers


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tar_bytes(members: list[tuple[str, bytes]]) -> bytes:
    """Deterministic tar: sorted names, mtime 0, uid/gid 0, mode 0644, GNU."""
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


def tgz_member_bytes(tgz: str, prefix: str, name: str) -> bytes:
    with tarfile.open(tgz, "r:gz") as tar:
        fh = tar.extractfile(prefix + name)
        if fh is None:
            raise KeyError(prefix + name)
        return fh.read()


def go_tree_members(tgz: str) -> list[tuple[str, bytes]]:
    """The internal/abi tree of a Go source tarball, as (relpath, bytes)."""
    with tarfile.open(tgz, "r:gz") as tar:
        names = []
        for m in tar.getmembers():
            if m.isfile() and m.name.startswith("go/src/internal/abi/"):
                names.append(m.name[len("go/src/internal/abi/"):])
        out = []
        for rel in sorted(names):
            fh = tar.extractfile("go/src/internal/abi/" + rel)
            out.append((rel, fh.read()))
        return out


def rederive(sid: str, kind: str, arg, scratch: str):
    """Return (bytes, substrate-description) rebuilt today, or (None, reason)."""
    if kind == "host-file":
        if not os.path.isfile(arg):
            return None, "host object absent"
        with open(arg, "rb") as fh:
            return fh.read(), "live host file"
    if kind == "host-gz":
        if not os.path.isfile(arg):
            return None, "host object absent"
        with open(arg, "rb") as fh:
            raw = fh.read()
        gz = subprocess.run(["gzip", "-9", "-n", "-c"], input=raw, check=True,
                            stdout=subprocess.PIPE).stdout
        return gz, "live host file, gzip -9 -n"
    if kind == "zip-members":
        if not os.path.isfile(arg):
            return None, "host object absent"
        with zipfile.ZipFile(arg) as zf:
            members = [(n, zf.read(n)) for n in ZIP_MEMBERS]
        return tar_bytes(members), "live host zip, %d members" % len(members)
    if kind == "pkg-member":
        tgz, member = arg
        path = os.path.join(scratch, tgz)
        if not os.path.isfile(path):
            return None, "tarball absent"
        return tgz_member_bytes(path, "", member), "npm tarball member %s" % member
    if kind == "pkg-members":
        path = os.path.join(scratch, arg)
        if not os.path.isfile(path):
            return None, "tarball absent"
        members = []
        for rel in REA65_MEMBERS:
            prefix = "package/" if rel.startswith("bridge/") else "package/dist/"
            members.append((rel, tgz_member_bytes(path, prefix, rel)))
        return tar_bytes(members), "npm tarball, %d cited members" % len(members)
    if kind == "tgz-members":
        path = os.path.join(scratch, arg)
        if not os.path.isfile(path):
            return None, "tarball absent"
        members = []
        for rel in REA67_MEMBERS:
            members.append((rel, tgz_member_bytes(path, "package/", rel)))
        return tar_bytes(members), "npm tarball, %d cited members" % len(members)
    if kind == "go-tree":
        path = os.path.join(scratch, arg)
        if not os.path.isfile(path):
            return None, "tarball absent"
        return tar_bytes(go_tree_members(path)), "Go source tarball internal/abi tree"
    if kind == "db-member":
        if not os.path.isfile(arg):
            return None, "host object absent"
        member = "tinyxxd-1.3.17-1/desc"
        data = subprocess.run(["tar", "-xOf", arg, member], check=True,
                              stdout=subprocess.PIPE).stdout
        return tar_bytes([(member, data)]), "live pacman db member %s" % member
    raise ValueError("unknown substrate kind %r" % kind)


def pin_digest(kind: str, arg, scratch: str):
    """Return the digest the pin subject currently has, or None."""
    if kind == "file":
        path = arg if os.path.isabs(arg) else os.path.join(scratch, arg)
        if not os.path.isfile(path):
            return None
        return sha256_file(path)
    if kind == "zip":
        path, member = arg
        if not os.path.isfile(path):
            return None
        with zipfile.ZipFile(path) as zf:
            return sha256_bytes(zf.read(member))
    if kind in ("pkg", "pkg67"):
        tgz = REA65_TGZ if kind == "pkg" else REA67_TGZ
        path = os.path.join(scratch, tgz)
        if not os.path.isfile(path):
            return None
        return sha256_bytes(tgz_member_bytes(path, "", arg))
    if kind == "gomember":
        tgz, member = arg
        path = os.path.join(scratch, tgz)
        if not os.path.isfile(path):
            return None
        for rel, data in go_tree_members(path):
            if rel == member:
                return sha256_bytes(data)
        return None
    if kind == "dbfield":
        if not os.path.isfile(arg):
            return None
        out = subprocess.run(["tar", "-xOf", arg, "tinyxxd-1.3.17-1/desc"],
                             check=True, stdout=subprocess.PIPE).stdout.decode()
        lines = out.splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "%SHA256SUM%":
                # the value sits on the next line in a pacman desc record
                return lines[i + 1].strip().lower()
        return None
    if kind == "mtreefield":
        if not os.path.isfile(arg):
            return None
        raw = open(arg, "rb").read()
        if raw[:2] == b"\x1f\x8b":          # the pacman mtree is gzip-compressed
            raw = gzip.decompress(raw)
        for line in raw.decode("utf-8", errors="replace").splitlines():
            if line.startswith("./usr/bin/tinyxxd ") and "sha256digest=" in line:
                return line.split("sha256digest=", 1)[1].split(",", 1)[0].strip().lower()
        return None
    raise ValueError("unknown pin kind %r" % kind)


# ------------------------------------------------------------------- driver


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True, help="dir holding corpus/evidence/...")
    ap.add_argument("--scratch", required=True, help="dir holding the downloaded tarballs")
    ap.add_argument("--sources", required=True, help="corpus/SOURCES.md to read the pins from")
    ap.add_argument("--out", required=True, help="receipt TSV")
    args = ap.parse_args(argv)

    pack = os.path.abspath(args.pack)
    scratch = os.path.abspath(args.scratch)
    tree = os.path.join(pack, "corpus", "evidence", "round-42", "local-sources")
    map_path = os.path.join(pack, "corpus", "evidence", "local-sources.json")
    with open(map_path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    sources = doc["sources"]

    rows = ["check\tsid\tsubject\tresult\tdetail"]
    failures = 0

    def emit(check: str, sid: str, subject: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        rows.append("%s\t%s\t%s\t%s\t%s" % (check, sid, subject,
                                            "OK" if ok else "FAIL", detail))
        if not ok:
            failures += 1

    # A. pack self-consistency -------------------------------------------
    for sid, rel, kind, arg in SPEC:
        copy_abs = os.path.join(tree, rel)
        present = os.path.isfile(copy_abs)
        emit("pack-present", sid, rel, present,
             "%d bytes" % os.path.getsize(copy_abs) if present else "missing")
        if not present:
            continue
        digest = sha256_file(copy_abs)
        entry = None
        for host, e in sources.items():
            if e.get("copy", "").endswith("/" + rel):
                entry = e
                break
        if entry is None:
            emit("pack-mapped", sid, rel, False, "no map entry names this copy")
            continue
        emit("pack-digest", sid, rel, digest == entry.get("sha256"),
             "map %s actual %s" % (str(entry.get("sha256"))[:16], digest[:16]))
        emit("pack-size-bound", sid, rel,
             os.path.getsize(copy_abs) <= 5 * 1024 * 1024,
             "%d bytes" % os.path.getsize(copy_abs))

    # B. re-derivation ----------------------------------------------------
    for sid, rel, kind, arg in SPEC:
        copy_abs = os.path.join(tree, rel)
        if not os.path.isfile(copy_abs):
            continue
        with open(copy_abs, "rb") as fh:
            have = fh.read()
        rebuilt, note = rederive(sid, kind, arg, scratch)
        if rebuilt is None:
            emit("rederive", sid, rel, False, "SKIPPED: %s" % note)
            continue
        emit("rederive", sid, rel, rebuilt == have,
             "%s; rebuilt %s vs copy %s" % (note, sha256_bytes(rebuilt)[:16],
                                            sha256_bytes(have)[:16]))

    # C. row pins ---------------------------------------------------------
    with open(args.sources, "r", encoding="utf-8") as fh:
        text = fh.read()
    table_pins = {}
    for line in text.splitlines():
        if not line.startswith("| S"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) < 7:
            continue
        import re
        digests = set(re.findall(r"(?<![0-9a-fA-F])([0-9a-fA-F]{64})(?![0-9a-fA-F])",
                                 cells[5] + " " + cells[6]))
        table_pins[cells[0]] = digests

    covered = {}
    for sid, subject, kind, arg, want in PINS:
        got = pin_digest(kind, arg, scratch)
        ok = got is not None and got == want
        emit("pin", sid, subject, ok,
             "want %s got %s" % (want[:16], (got or "NONE")[:16]))
        covered.setdefault(sid, set()).add(want)

    # Every digest the 18 target rows actually pin must be covered by a check.
    TARGET_ROWS = {"S001", "S002", "S003", "S006", "S007", "S023", "S035", "S040",
                   "S048", "S056", "S066", "S070", "S079", "S081", "S082", "S083",
                   "S090", "S092"}
    for sid in sorted(TARGET_ROWS):
        pins = table_pins.get(sid, set())
        if not pins:
            emit("pin-coverage", sid, "row pins", True, "row pins no digest")
            continue
        missing = pins - covered.get(sid, set())
        emit("pin-coverage", sid, "row pins", not missing,
             "%d row pins, %d unaudited" % (len(pins), len(missing))
             + ((" " + ",".join(sorted(missing))) if missing else ""))

    # The 41 pins the round-42 audit claimed must still be 41 pins, all audited.
    audited = set()
    for sid, subject, kind, arg, want in PINS:
        if want in table_pins.get(sid, set()):
            audited.add((sid, want))
    claimed = 41
    emit("pin-total", "*", "audit population", len(audited) == claimed,
         "%d distinct (row, digest) pins audited, round-42 audit claimed %d"
         % (len(audited), claimed))

    out = "\n".join(rows) + "\n"
    out += "checks: %d, failures: %d\n" % (len(rows) - 1, failures)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(out)
    sys.stdout.write(out)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
