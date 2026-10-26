#!/usr/bin/env python3
"""verify-copies — check every prepared copy against the host source and the row pins.

Reads the map this seat wrote (corpus/evidence/local-sources.json under --root),
re-hashes every copy, byte-compares the `copy` dispositions with the host file,
and unpacks every `tree-archive` to check its members against the digests the
SOURCES rows themselves pin.  Prints one TSV line per check; exit 0 only when
every line is OK.  Stdlib only, TMPDIR-honouring.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys
import tarfile

# Expected member digests, transcribed from the rows' anchor/teaches cells.
EXPECT = {
    "S003": {
        "ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java":
            "2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95",
        "ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java":
            "765d25365a8c379c929097a6602df5fa75049f871eb0f610d5376d630d95eb7d",
    },
    "S035": {
        "map_swiss.go": "0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383",
        "map_noswiss.go": "03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291",
        "map_select_swiss.go": "c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718",
    },
    "S048": {
        "domain/evidence.js": "f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff",
        "domain/canonicalDigest.js": "f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9",
        "application/DirectAnalysis.js": "09d2b2225dd9817674f3a454d33447a6a917e82441f2081c6553511e2dc72617",
        "application/binaryDiagnostics/BinaryLayoutService.js":
            "b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4",
        "domain/analysisView/analysisView.js":
            "2685fc2c0f6dda136b9bc004ab3af30d4272b850b1a8d026ad14b2e22ef68363",
        "domain/analysisView/binaryLayoutView.js":
            "5bd86489988b6cf4cb59bd6085805accdd83277870578426baebff687ff7b070",
        "cli/reverseEngineeringCommands.js": None,
        "application/reverse/ReverseEngineeringService.js": None,
        "domain/reverseEngineering.js": None,
        "contracts/reverseEngineeringToolContracts.js": None,
        "rust/RustAuditableReader.js": "1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505",
        "rust/RustBinaryImage.js": "08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681",
        "go/GoElfImage.js": "ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204",
        "cli-runtime/cli.js": "168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204",
        "sqlite/SqliteDatabaseFailures.js":
            "5a908695ec398079e97750bf60ece6ac273bdc74f06f7c9c1fd5777cfa90d419",
        "sqlite/SqliteDatabaseInspection.js":
            "edfcd90f9e2e1dbde531b6aafc4efb1bd105a372df617dee619a414425354970",
        "sqlite/SqliteDatabaseLimits.js":
            "92df76ffd21386dba134051791230e9d143220854a49e3e65e72d51daa074121",
        "sqlite/SqliteDatabaseProvider.js":
            "018756d9d7f620995c9b8929d268c33ff1f7c973683bd0f4ddc6d781e5268104",
        "sqlite/SqliteDatabaseSnapshot.js":
            "c8af51f8496703a1992e7e7646c8bf8b6c56796a7571f5f8e9c84a284740ce19",
        "sqlite/SqliteDatabaseWorker.js":
            "ebb39f583db802ccb31b3ac328b0f8dd712fa6f0e5dd5a63da6908d7fe60cf63",
        "sqlite/SqliteDatabaseWorkerExecution.js":
            "6e49c2ab222982434d769fd279ad8053b857d6747f9b1101e07163d8a5e4c203",
        "domain/sqlite/sqliteDatabase.js":
            "c7a0eff5674414110085ecf0257a71c1949de7e27be392ef2d8c8bd8cf000ae1",
        "artifacts/readStableArtifact.js":
            "06a23746346a3de150f1aa21b781fffd8a482c0f5e98900c458f3f599b9d2707",
    },
    "S081": {
        "dist/domain/evidence.js":
            "a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb",
        "dist/domain/canonicalDigest.js":
            "f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9",
        "package.json": "3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570",
    },
}

GZ_CASES = {"S023": "54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="lane (or artifact tree) holding corpus/")
    ap.add_argument("--map", default="corpus/evidence/local-sources.json")
    ap.add_argument("--tarball", default=None,
                    help="rea-agents-6.7.0.tgz for the S081 host-identity check")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    with open(os.path.join(root, args.map), "r", encoding="utf-8") as fh:
        doc = json.load(fh)

    out = ["check\tsubject\tresult\tdetail"]
    failures = 0

    def emit(check: str, subject: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        out.append("%s\t%s\t%s\t%s" % (check, subject, "OK" if ok else "FAIL", detail))
        if not ok:
            failures += 1

    for host in sorted(doc["sources"]):
        entry = doc["sources"][host]
        copy_abs = os.path.join(root, entry["copy"])
        if not os.path.isfile(copy_abs):
            emit("copy-present", entry["copy"], False, "missing")
            continue
        got = sha256_file(copy_abs)
        emit("map-digest", entry["copy"], got == entry["sha256"],
             "map %s actual %s" % (entry["sha256"][:16], got[:16]))

        sid = entry["copy"].split("/")[-2]
        if entry.get("kind") == "file" and sid not in GZ_CASES:
            if os.path.isfile(host):
                with open(host, "rb") as a, open(copy_abs, "rb") as b:
                    emit("byte-identical", sids(entry, sid), a.read() == b.read(), "cmp vs host")

    for sid, want in GZ_CASES.items():
        path = os.path.join(root, "corpus/evidence/round-42/local-sources", sid,
                            "go1.25.0.json.gz")
        if not os.path.isfile(path):
            emit("gz-present", sid, False, "missing")
            continue
        import gzip
        with open(path, "rb") as fh:
            decoded = gzip.decompress(fh.read())
        emit("gz-digest", sid, sha256_bytes(decoded) == want,
             "decoded %s" % sha256_bytes(decoded)[:16])

    for sid, members in EXPECT.items():
        for rel, want in members.items():
            base = "corpus/evidence/round-42/local-sources/%s" % sid
            if sid == "S035":
                tars = ["internal-abi-go1.25.0.tar", "internal-abi-go1.24.6.tar"]
            elif sid == "S048":
                tars = ["rea-agents-6.5.0-dist-cited-members.tar"]
            elif sid == "S081":
                tars = ["rea-agents-6.7.0-dist-cited-members.tar"]
            else:
                tars = ["Base-src-go-rtti-members.tar"]
            found = None
            for tarname in tars:
                tpath = os.path.join(root, base, tarname)
                if not os.path.isfile(tpath):
                    continue
                with tarfile.open(tpath, "r:") as tar:
                    try:
                        member = tar.extractfile(rel)
                    except KeyError:
                        member = None
                    if member is not None:
                        got = sha256_bytes(member.read())
                        found = (tarname, got)
                        break
            if found is None:
                emit("member-present", "%s/%s" % (sid, rel), False, "missing from archive")
                continue
            tarname, got = found
            if want is None:
                emit("member-present", "%s/%s" % (sid, rel), True, "in %s (no row pin, exists)" % tarname)
            else:
                emit("member-pin", "%s/%s" % (sid, rel), got == want,
                     "%s %s" % (tarname, got[:16]))

    # Host-derived identity: every archived member must equal the *host source*
    # member, not merely a transcribed constant.
    REA = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist"
    host_cases = [
        ("S003", "Base-src-go-rtti-members.tar", "zip",
         "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip", None),
        ("S035", "internal-abi-go1.25.0.tar", "dir",
         "/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi", None),
        ("S035", "internal-abi-go1.25.0.tar", "dir",
         "/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi", "cross-version"),
        ("S048", "rea-agents-6.5.0-dist-cited-members.tar", "dir", REA, None),
    ]
    import subprocess
    import zipfile
    for sid, tarname, kind, src, mode in host_cases:
        tpath = os.path.join(root, "corpus/evidence/round-42/local-sources", sid, tarname)
        if not os.path.isfile(tpath):
            emit("host-identity-present", "%s %s" % (sid, tarname), False, "missing archive")
            continue
        with tarfile.open(tpath, "r:") as tar:
            members = {m.name: tar.extractfile(m).read() for m in tar.getmembers() if m.isreg()}
        diffs = []
        # The go1.24.6 tree differs from 1.25.0 outside the three files the row
        # calls byte-identical, so the cross-version check is limited to those.
        keep = set(EXPECT["S035"]) if mode == "cross-version" else None
        for name, data in sorted(members.items()):
            if keep is not None and name not in keep:
                continue
            if kind == "zip":
                with zipfile.ZipFile(src) as zf:
                    host = zf.read(name)
            else:
                with open(os.path.join(src, name), "rb") as fh:
                    host = fh.read()
            if host != data:
                diffs.append(name)
        emit("host-identity", "%s %s vs %s" % (sid, tarname, src),
             not diffs, "%d members%s" % (len(members), "" if not diffs else " DIFF " + ",".join(diffs)))

    # S081: archive members vs the published 6.7.0 tarball (host pipe is gone).
    tarball = args.tarball if args.tarball and os.path.isfile(args.tarball) else None
    s081 = os.path.join(root, "corpus/evidence/round-42/local-sources/S081",
                        "rea-agents-6.7.0-dist-cited-members.tar")
    if tarball and os.path.isfile(s081):
        with tarfile.open(s081, "r:") as tar:
            members = {m.name: tar.extractfile(m).read() for m in tar.getmembers() if m.isreg()}
        diffs = []
        with tarfile.open(tarball, "r:gz") as src:
            for name, data in sorted(members.items()):
                got = src.extractfile("package/" + name).read()
                if got != data:
                    diffs.append(name)
        emit("host-identity", "S081 vs rea-agents-6.7.0.tgz", not diffs,
             "%d members%s" % (len(members), "" if not diffs else " DIFF " + ",".join(diffs)))
    elif os.path.isfile(s081):
        emit("host-identity", "S081 vs rea-agents-6.7.0.tgz", False,
             "no --tarball given (row pins 20958a66…; member digests checked above)")

    # S082: member archive vs the live pacman repository database.
    db = "/var/lib/pacman/sync/extra.db"
    s082 = os.path.join(root, "corpus/evidence/round-42/local-sources/S082",
                        "extra-db-tinyxxd-1.3.17-1-desc.tar")
    if os.path.isfile(db) and os.path.isfile(s082):
        got = subprocess.run(["tar", "-xOf", db, "tinyxxd-1.3.17-1/desc"], check=True,
                             stdout=subprocess.PIPE).stdout
        with tarfile.open(s082, "r:") as tar:
            member = tar.extractfile("tinyxxd-1.3.17-1/desc")
            archived = member.read() if member else b""
        emit("host-identity", "S082 extra.db member desc", got == archived,
             "member %d bytes" % len(archived))

    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.write("checks: %d, failures: %d\n" % (len(out) - 1, failures))
    return 0 if failures == 0 else 1


def sids(entry: dict, sid: str) -> str:
    return "%s %s" % (sid, os.path.basename(entry["copy"]))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
