#!/usr/bin/env python3
"""verify-copies-r43 — landing-time verifier for the local-sources pack (R43-C2).

Hardened port of the round-42 R42LocalSrc `verify-copies.py`.  Fixes the two
behaviours that made the round-42 script unusable today (2026-10-27):

  * it crashed (FileNotFoundError, exit 1-with-traceback) when a host source
    was absent — the go-1.24.6 / go-1.25.0 toolchain dirs and the rea-agents
    6.7.0 npx dir are gone from this host; and
  * it could only prove member identity against the host, so a vanished host
    tree left nothing checkable at all.

What it checks, per map entry (`corpus/evidence/local-sources.json` under
--root):

  map-shape        version==1, sources object, no duplicate keys at any level
                   (object_pairs_hook scan — json.load silently keeps the
                   LAST duplicate, so a parsed dict cannot see them)
  key-set          the map's key set EQUALS the set of out-of-lane absolute
                   paths extracted from SOURCES.md by the frozen gate itself
                   (tools/round-41/local-source-gate.py imported by path)
  copy-regular     copy is a regular file by lstat (a symlink copy is FAIL —
                   the gate follows symlinks and stays green, so this check
                   is what stops the committed-symlink attack)
  copy-in-dir      every copy lives under the stated directory
                   corpus/evidence/round-42/local-sources/ — except the
                   preserved S126 entry (corpus/evidence/round-41/s126/…)
  copy-unique      no two host paths share one copy file (no aliases)
  map-digest       sha256(copy bytes) == entry sha256
  byte-identical   kind=file (non-gzip) copies cmp-equal the live host file;
                   a host that is absent or changed is reported, never guessed
  host-sha256      entry source_sha256 re-verified against the live host file
  gz-digest        S023 decodes to the row-pinned source digest
  member-pin       every transcribed row pin (EXPECT) found in the tars; the
                   S048 set is extended by S048_EXT_PINS — five pins R43C2Pin
                   found missing (S066 pcapAnalysis.js, S070 PcapProvider.js +
                   PcapNativeBound.js, S083 GhidraTargetSnapshot.js +
                   ReaGhidraBridge.java), stored in the round-43 extension tar
                   S048/rea-agents-6.5.0-cited-members.tar (28 members; four
                   new names dist-relative, the Java bridge package-root)
  host-identity    tar members byte-equal the live host object (zip / package /
                   pacman db member); S048 resolves bridge/* package-root and
                   everything else under dist/ of the installed 6.5.0 package;
                   absent host → fallback
  upstream-id      S035 members byte-equal golang/go raw.githubusercontent.com
                   files at tags go1.25.0 / go1.24.6 (--upstream-dir, fetched
                   out-of-band); S081 members byte-equal the published
                   rea-agents-6.7.0.tgz (--tarball); S048 members byte-equal
                   the published rea-agents-6.5.0.tgz (--tarball-650) when the
                   volatile npx cache is absent
  digest-fresh     (with --rev) none of this depends on the gate's exit: the
                   gate is exit-0-compatible with stub copies on unpinned
                   rows, symlink copies, aliases and duplicate keys — see
                   .ufo/waves/round-43/w1/R43RevLocalsrc.md

Round-43 update (post-yield, L1-directed): expects the extended S048 tar
`rea-agents-6.5.0-cited-members.tar` (28 members, map sha dca1b4ed… per the
L1; the old 23-member dist tar remains an accepted fallback name) and verifies
the five R43C2Pin member pins.  Check count grows 130 → 135 (five new
member-pin emits; the S048 host-identity emit is unchanged in number).

Exit 0 only when every emitted check is OK.  Stdlib only, TMPDIR-honouring,
no network of its own (upstream files are read from --upstream-dir).
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tarfile
import zipfile

# The member pins come from the round-42 verifier's EXPECT table, imported by
# path from the pack (it is an artifact, not a module on sys.path).  Each
# value is None where the row cites the member without pinning its digest.
def _expect_table(pack_build_dir: str) -> dict:
    """Import the round-42 verifier's EXPECT dict from the pack by path."""
    vp = os.path.join(pack_build_dir, "verify-copies.py")
    spec = importlib.util.spec_from_file_location("vc42", vp)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EXPECT


GZ_CASES = {"S023": "54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252"}
STATED_DIR = "corpus/evidence/round-42/local-sources/"
PRESERVED = "corpus/evidence/round-41/s126/lead1-avm-image.tsv"
COPY_LIMIT = 5 * 1024 * 1024

# Round-43 pack extension (R43C2Pin found five row-pinned S048 members missing
# from the round-42 23-member tar; the L1 extended the pack to a 28-member tar
# stored at S048/rea-agents-6.5.0-cited-members.tar).  Four members are stored
# dist-relative (like the original 23); the Java bridge is stored package-root
# relative.  Pins are transcribed from the rows' anchor cells (S066 pcapAnalysis,
# S070 PcapProvider + PcapNativeBound, S083 GhidraTargetSnapshot + ReaGhidraBridge)
# and were independently re-verified by R43C2Pin (member-recheck.json, all MATCH).
S048_OLD_TAR = "rea-agents-6.5.0-dist-cited-members.tar"
S048_NEW_TAR = "rea-agents-6.5.0-cited-members.tar"
S048_EXT_PINS = {
    "domain/pcap/pcapAnalysis.js":
        "7651b4c5582b62513196146b7aa08043fab93d0848ce7f8680523d867597c641",
    "pcap/PcapProvider.js":
        "16a4d813665208bd4f99229f431e0379a6e8b31d72a717d6c451c38833ed64d4",
    "pcap/PcapNativeBound.js":
        "24811182c301a73ec1cb9792f31d6db911aec9c9f1bf71cf4bc7932bb0838cd2",
    "ghidra/GhidraTargetSnapshot.js":
        "a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b",
    "bridge/ghidra/ReaGhidraBridge.java":
        "db16aed4d16ab94da883843281ef7a8a33a244cd8379bd4013e8dee479c0a105",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_gate(gate_path: str):
    spec = importlib.util.spec_from_file_location("gate", gate_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def out_of_lane_paths(gate, root: str, rev: str | None) -> set:
    text, _prov = gate.read_sources(root, rev, None)
    out = set()
    for row in gate.parse_rows(text):
        for p in gate.external_paths(row["cells"][1]):
            if not gate.inside(os.path.normpath(p), root):
                out.add(os.path.normpath(p))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True,
                    help="tree holding corpus/ + the map (attack clone or lane after landing)")
    ap.add_argument("--map", default="corpus/evidence/local-sources.json")
    ap.add_argument("--rev", default=None, help="read SOURCES.md at this rev via git show")
    ap.add_argument("--gate", default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/local-source-gate.py")
    ap.add_argument("--pack-build", default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42LocalSrc/build",
                    help="dir holding the round-42 verify-copies.py (for its EXPECT table)")
    ap.add_argument("--upstream-dir", default=None,
                    help="dir with go1.25.0/ and go1.24.6/ upstream abi trees")
    ap.add_argument("--tarball", default=None, help="rea-agents-6.7.0.tgz for S081")
    ap.add_argument("--tarball-650", default=None,
                    help="rea-agents-6.5.0.tgz fallback for the S048 host-identity check")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)

    out = ["check\tsubject\tresult\tdetail"]
    failures = 0

    def emit(check: str, subject: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        out.append("%s\t%s\t%s\t%s" % (check, subject, "OK" if ok else "FAIL", detail))
        if not ok:
            failures += 1

    # ---- map shape ---------------------------------------------------------
    map_path = os.path.join(root, args.map)
    raw = open(map_path, encoding="utf-8").read()
    dupes: list[str] = []

    def hook(pairs):
        seen = {}
        for k, v in pairs:
            if k in seen:
                dupes.append(k)
            seen[k] = v
        return dict(pairs)

    json.loads(raw, object_pairs_hook=hook)
    emit("map-no-duplicate-keys", args.map, not dupes, ",".join(dupes))
    doc = json.loads(raw)
    emit("map-version", args.map, doc.get("version") == 1, repr(doc.get("version")))
    emit("map-sources-object", args.map, isinstance(doc.get("sources"), dict))
    srcs = doc.get("sources", {})

    # ---- key set vs the gate's own path extraction -------------------------
    gate = load_gate(args.gate)
    want = out_of_lane_paths(gate, root, args.rev)
    keys = set(srcs)
    emit("key-set-equals-rows", args.map, keys == want,
         "missing=%s extra=%s" % (sorted(want - keys), sorted(keys - want)))

    # ---- per-entry copy checks ---------------------------------------------
    copies = [e["copy"] for e in srcs.values()]
    aliases = sorted(c for c in set(copies) if copies.count(c) > 1)
    emit("copy-unique", args.map, not aliases, ",".join(aliases))

    for host in sorted(srcs):
        entry = srcs[host]
        rel = entry["copy"]
        cp = os.path.join(root, rel)
        st = os.lstat(cp) if os.path.lexists(cp) else None
        regular = st is not None and not os.path.islink(cp) and os.path.isfile(cp)
        emit("copy-regular", rel, regular,
             "" if regular else
             ("symlink" if os.path.islink(cp) else
              ("missing" if st is None else "not-a-regular-file")))
        if st is None or not os.path.isfile(cp):
            continue
        indir = rel.startswith(STATED_DIR) or rel == PRESERVED
        emit("copy-in-stated-dir", rel, indir, rel)
        sz = os.path.getsize(cp)
        emit("copy-size", rel, sz <= COPY_LIMIT, "%d B" % sz)
        got = sha256_file(cp)
        emit("map-digest", rel, got == entry["sha256"],
             "map %s actual %s" % (entry["sha256"][:16], got[:16]))

        sid = rel.split("/")[-2]
        if entry.get("kind") == "file" and sid not in GZ_CASES:
            if os.path.isfile(host):
                with open(host, "rb") as a, open(cp, "rb") as b:
                    emit("byte-identical", "%s %s" % (sid, os.path.basename(rel)),
                         a.read() == b.read(), "cmp vs live host")
            else:
                emit("host-state", "%s %s" % (sid, os.path.basename(rel)), True,
                     "host source absent — byte-identity not re-verifiable")
        if "source_sha256" in entry:
            if os.path.isfile(host):
                actual = sha256_file(host)
                emit("host-sha256", sid, actual == entry["source_sha256"],
                     "want %s got %s" % (entry["source_sha256"][:16], actual[:16]))
            else:
                emit("host-state", sid, True,
                     "host source absent — source_sha256 not re-verifiable")

    # ---- gzip case ----------------------------------------------------------
    for sid, want in GZ_CASES.items():
        p = os.path.join(root, STATED_DIR, sid, "go1.25.0.json.gz")
        if not os.path.isfile(p):
            emit("gz-present", sid, False, "missing")
            continue
        with open(p, "rb") as fh:
            decoded = gzip.decompress(fh.read())
        emit("gz-digest", sid, sha256_bytes(decoded) == want,
             "decoded %s" % sha256_bytes(decoded)[:16])

    # ---- member pins (transcribed row digests via the r42 EXPECT table + -----
    # ---- the round-43 S048 extension) ---------------------------------------
    EXPECT = _expect_table(args.pack_build)
    merged = {sid: dict(members) for sid, members in EXPECT.items()}
    merged.setdefault("S048", {}).update(S048_EXT_PINS)
    for sid, members in merged.items():
        for rel, want in members.items():
            base = os.path.join(STATED_DIR, sid)
            tars = (["internal-abi-go1.25.0.tar", "internal-abi-go1.24.6.tar"] if sid == "S035"
                    else [S048_NEW_TAR, S048_OLD_TAR] if sid == "S048"
                    else ["rea-agents-6.7.0-dist-cited-members.tar"] if sid == "S081"
                    else ["Base-src-go-rtti-members.tar"])
            found = None
            for tn in tars:
                tp = os.path.join(root, base, tn)
                if not os.path.isfile(tp):
                    continue
                with tarfile.open(tp, "r:") as tar:
                    try:
                        member = tar.extractfile(rel)
                    except KeyError:
                        member = None
                    if member is not None:
                        found = (tn, sha256_bytes(member.read()))
                        break
            if found is None:
                emit("member-present", "%s/%s" % (sid, rel), False, "missing from archive")
            elif want is None:
                emit("member-present", "%s/%s" % (sid, rel), True, "in %s (no row pin)" % found[0])
            else:
                emit("member-pin", "%s/%s" % (sid, rel), found[1] == want,
                     "%s %s" % (found[0], found[1][:16]))

    # ---- host identity where the host object still exists ------------------
    REA65 = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist"

    def tar_members(tp: str) -> dict:
        with tarfile.open(tp, "r:") as tar:
            return {m.name: tar.extractfile(m).read() for m in tar.getmembers() if m.isreg()}

    tp = os.path.join(root, STATED_DIR, "S003/Base-src-go-rtti-members.tar")
    src = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip"
    if os.path.isfile(tp):
        members = tar_members(tp)
        if os.path.isfile(src):
            with zipfile.ZipFile(src) as zf:
                diffs = [n for n, d in sorted(members.items()) if zf.read(n) != d]
            emit("host-identity", "S003 vs Base-src.zip", not diffs,
                 "%d members%s" % (len(members), " DIFF " + ",".join(diffs) if diffs else ""))
        else:
            emit("host-state", "S003", True, "host Base-src.zip absent")

    # S048: whichever cited-members tar the map names (round-43 extension tar
    # preferred).  Member -> host path: names under bridge/ are package-root
    # relative, everything else is dist-relative.  The npx cache path is
    # volatile (R43C2Pin saw it vanish and rehydrate mid-audit), so a missing
    # host falls back to the published 6.5.0 tarball via --tarball-650.
    tp = None
    for cand in (S048_NEW_TAR, S048_OLD_TAR):
        cand_abs = os.path.join(root, STATED_DIR, "S048", cand)
        if os.path.isfile(cand_abs):
            tp = cand_abs
            break
    if tp is not None:
        members = tar_members(tp)
        pkg_root = os.path.dirname(REA65)

        def s048_host_path(name: str) -> str:
            return os.path.join(pkg_root, name if name.startswith("bridge/")
                                else os.path.join("dist", name))

        if os.path.isdir(pkg_root):
            diffs = []
            for n, d in sorted(members.items()):
                hp = s048_host_path(n)
                if not os.path.isfile(hp):
                    diffs.append(n + "(missing)")
                    continue
                with open(hp, "rb") as fh:
                    if fh.read() != d:
                        diffs.append(n)
            emit("host-identity", "S048 vs installed rea-agents 6.5.0 package", not diffs,
                 "%d members%s" % (len(members), " DIFF " + ",".join(diffs) if diffs else ""))
        elif args.tarball_650 and os.path.isfile(args.tarball_650):
            diffs = []
            with tarfile.open(args.tarball_650, "r:gz") as src_t:
                for n, d in sorted(members.items()):
                    arc = "package/" + (n if n.startswith("bridge/")
                                        else "dist/" + n)
                    try:
                        got_b = src_t.extractfile(arc).read()
                    except Exception:
                        got_b = None
                    if got_b != d:
                        diffs.append(n)
            emit("upstream-identity", "S048 vs rea-agents-6.5.0.tgz", not diffs,
                 "%d members%s" % (len(members), " DIFF " + ",".join(diffs) if diffs else ""))
        else:
            emit("host-state", "S048", False,
                 "host package absent and no --tarball-650 — identity unverifiable")

    # S035: host dirs gone → upstream identity at the pinned tags
    for ver, tname in (("go1.25.0", "internal-abi-go1.25.0.tar"),
                       ("go1.24.6", "internal-abi-go1.24.6.tar")):
        tp = os.path.join(root, STATED_DIR, "S035", tname)
        if not os.path.isfile(tp):
            continue
        members = tar_members(tp)
        host_dir = "/home/vgpnk/.local/opt/%s/src/internal/abi" % ver.replace("go", "go-")
        if os.path.isdir(host_dir):
            diffs = []
            for n, d in sorted(members.items()):
                with open(os.path.join(host_dir, n), "rb") as fh:
                    if fh.read() != d:
                        diffs.append(n)
            emit("host-identity", "S035 %s vs host %s" % (tname, host_dir), not diffs,
                 "%d members%s" % (len(members), " DIFF " + ",".join(diffs) if diffs else ""))
        elif args.upstream_dir:
            udir = os.path.join(args.upstream_dir, ver)
            diffs = [n for n, d in sorted(members.items())
                     if not os.path.isfile(os.path.join(udir, n))
                     or open(os.path.join(udir, n), "rb").read() != d]
            emit("upstream-identity", "S035 %s vs golang/go@%s" % (tname, ver), not diffs,
                 "%d members%s" % (len(members), " DIFF " + ",".join(diffs) if diffs else ""))
        else:
            emit("host-state", "S035 %s" % tname, False,
                 "host dir absent and no --upstream-dir — identity unverifiable")

    # S081: host npx dir gone → published tarball identity
    tp = os.path.join(root, STATED_DIR, "S081/rea-agents-6.7.0-dist-cited-members.tar")
    if os.path.isfile(tp):
        members = tar_members(tp)
        host = "/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist"
        if os.path.isdir(host):
            diffs = []
            for n, d in sorted(members.items()):
                with open(os.path.join(host, n), "rb") as fh:
                    if fh.read() != d:
                        diffs.append(n)
            emit("host-identity", "S081 vs host dist", not diffs, "%d members" % len(members))
        elif args.tarball and os.path.isfile(args.tarball):
            diffs = []
            with tarfile.open(args.tarball, "r:gz") as src_t:
                for n, d in sorted(members.items()):
                    try:
                        got_b = src_t.extractfile("package/" + n).read()
                    except Exception:
                        got_b = None
                    if got_b != d:
                        diffs.append(n)
            emit("upstream-identity", "S081 vs rea-agents-6.7.0.tgz", not diffs,
                 "%d members%s" % (len(members), " DIFF " + ",".join(diffs) if diffs else ""))
        else:
            emit("host-state", "S081", False,
                 "host dist absent and no --tarball — identity unverifiable")

    # S082: member vs live pacman db
    db = "/var/lib/pacman/sync/extra.db"
    tp = os.path.join(root, STATED_DIR, "S082/extra-db-tinyxxd-1.3.17-1-desc.tar")
    if os.path.isfile(db) and os.path.isfile(tp):
        got_b = subprocess.run(["tar", "-xOf", db, "tinyxxd-1.3.17-1/desc"], check=True,
                               stdout=subprocess.PIPE).stdout
        with tarfile.open(tp, "r:") as tar:
            member = tar.extractfile("tinyxxd-1.3.17-1/desc")
            archived = member.read() if member else b""
        emit("host-identity", "S082 extra.db member desc", got_b == archived,
             "member %d bytes" % len(archived))
    elif os.path.isfile(tp):
        emit("host-state", "S082 extra.db", False, "live extra.db absent")

    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.write("checks: %d, failures: %d\n" % (len(out) - 1, failures))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
