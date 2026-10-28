#!/usr/bin/env python3
"""c1-oracle.py - the frozen oracle builder for R44-C1 (round 44).

It builds, for each frozen carrier, the *independent* oracle that the
round-44 C1 counter binds the REA `extract-firmware` receipts against, and
writes the per-carrier `oracle` block of `tools/round-44/carriers.json`.

Oracle A - squashfs-tools (primary, independent of the REA side)
  `unsquashfs` 4.7.5 (squashfs-tools, upstream) is a *different producer*
  from sasquatch 4.5.1 (which unblob 26.6.4 drives).  For every carrier it
    (a) runs `/usr/bin/unsquashfs -lls <image>` and parses the member
        census (type, mode, owner, size, mtime, path);
    (b) extracts the image into a fresh scratch directory and computes the
        sha256 of every REGULAR file;
    (c) records every non-regular member (directory, symlink, device, fifo,
        socket) as a non-regular row.
  The oracle is never derived from a REA/sasquatch receipt.

Oracle B - the unblob `__output__` expected trees (second, cross-checking)
  The committed tree under `corpus/evidence/round-44/oracle/` (fetched
  pre-freeze by seat R44SrcOracle, dataset S138) is walked and its member
  digests recorded.  This tree is unblob's own expectation for the same
  fixtures; it is a second reading of the same bytes, NOT an independent
  producer lineage (see `producer_lineage` in the emitted block).

Emitted `oracle` block, per carrier id:

    {
      "members": [{"path", "size", "sha256", "type"}, ...],   # regular files
      "nonregular": [{"path", "type", "mode", "owner", "size",
                      "mtime", "detail"}, ...],
      "oracle_tool": "unsquashfs",
      "oracle_ver": "4.7.5",
      "oracle_tool_path": "/usr/bin/unsquashfs",
      "oracle_tool_sha256": "...",
      "output_tree_digest": "<sha256 of the sorted path+sha256 lines>",
      "output_tree_digest_def": "sha256 over the concatenation of
         '<path>\\t<sha256>\\n' lines of `members`, sorted bytewise by path",
      "output_tree": {                                   # oracle B
         "root": "<lane-relative path>",
         "extract_root": "<the '*_extract' directory inside `root`>",
         "members": [{"path", "size", "sha256", "type"}, ...],
         "output_tree_digest": "<same rule over oracle B members>",
         "agrees_with_unsquashfs": true,
         "mismatches": []
      },
      "census": [ ... raw parsed -lls rows ... ],
      "extraction": {"argv", "exit", "stderr_tail"}
    }

`members` holds the REGULAR files only, so the digest rule above is
unambiguous; non-regular members live in `nonregular` (with no sha256).

Exit codes
  0  every carrier produced both oracles and they agree
  1  a carrier failed (image unreadable, oracle disagreement, digest
     mismatch against the frozen pin, census/extraction disagreement)
  2  could not evaluate (missing fixture, missing `unsquashfs`, missing
     committed `__output__` tree, malformed carriers.json) - never counts
     toward a target

Nothing is written outside `--work` and the two explicit output paths.

Usage
  python3 -I -B c1-oracle.py --root LANE --work SCRATCH \
      --json-out ORACLE.json --receipt RECEIPT.json
  python3 -I -B c1-oracle.py --selftest
"""

import argparse
import errno
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time

SCHEMA = "kaidoku-r44-c1-oracle-v1"

UNSQUASHFS = "/usr/bin/unsquashfs"
ORACLE_TOOL = "unsquashfs"
ORACLE_VER = "4.7.5"

EXIT_OK, EXIT_FAILED, EXIT_CANNOT_EVALUATE = 0, 1, 2

SEAT = "R44C1Oracle"

# --------------------------------------------------------------------------
# The frozen carrier table.
#
# Ids follow the seat spec (v1-le, v1-be, v2-le, v2-be).  The draft claims
# file spells the same four carriers V1LE/V1BE/V2LE/V2BE; ids are matched
# case- and separator-insensitively so either spelling resolves to one
# carrier.  Pins are copied from `tools/round-42/fixtures.json` (MIT unblob
# 26.6.4 fixtures, committed under corpus/evidence/round-42/c2/fixtures/).
# --------------------------------------------------------------------------

CARRIERS = (
    {
        "id": "v1-le",
        "handler": "squashfs_v1",
        "endian": "le",
        "fixture": "v1-le--squashfs_v1.0_le.bin",
        "sha256": "b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71",
        "upstream": "squashfs_v1/little_endian",
        "extract_dir": "squashfs_v1.0_le.bin_extract",
        "expected_files": 3,
    },
    {
        "id": "v1-be",
        "handler": "squashfs_v1",
        "endian": "be",
        "fixture": "v1-be--squashfs_v1.0_be.bin",
        "sha256": "529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6",
        "upstream": "squashfs_v1/big_endian",
        "extract_dir": "squashfs_v1.0_be.bin_extract",
        "expected_files": 3,
    },
    {
        "id": "v2-le",
        "handler": "squashfs_v2",
        "endian": "le",
        "fixture": "v2-le--squashfs_v2.0_le.bin",
        "sha256": "7c62dbe388b972119f5d17a12836a016737d58276184f4caa2a90dafd924f124",
        "upstream": "squashfs_v2/little_endian",
        "extract_dir": "squashfs_v2.0_le.bin_extract",
        "expected_files": 4,
    },
    {
        "id": "v2-be",
        "handler": "squashfs_v2",
        "endian": "be",
        "fixture": "v2-be--squashfs_v2.0_be.bin",
        "sha256": "79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0",
        "upstream": "squashfs_v2/big_endian",
        "extract_dir": "squashfs_v2.0_be.bin_extract",
        "expected_files": 4,
    },
)

KIND_NAMES = {
    "-": "regular",
    "d": "dir",
    "l": "symlink",
    "c": "char-device",
    "b": "block-device",
    "p": "fifo",
    "s": "socket",
}

# `unsquashfs -lls` row: mode, owner, size (or "major, minor"), mtime, path
U_LLS = re.compile(
    r"^([-dlcbps][-rwxsStT]{9})[.+@]?\s+"     # mode
    r"(\S+)\s+"                                # owner/group
    r"(\d+,\s*\d+|\d+)\s+"                     # size or "major, minor"
    r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}(?::\d{2})?)\s"
    r"(.*)$"                                   # path [-> target]
)


class OracleError(Exception):
    """A condition with a fixed exit code."""

    def __init__(self, code, reason, detail=""):
        super().__init__(detail or reason)
        self.code = code
        self.reason = reason
        self.detail = detail


# --------------------------------------------------------------------- utils

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def norm_id(text):
    """Case- and separator-insensitive carrier id (v1-le == V1LE == v1_le)."""
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


def rel_posix(path, start):
    return os.path.relpath(path, start).replace(os.sep, "/")


def digest_of(members):
    """sha256 over sorted '<path>\\t<sha256>\\n' lines of the members.

    The path is the member path relative to the tree root; the sha256 is
    the member's content digest.  Sorting is bytewise on the path.
    """
    lines = []
    for m in members:
        lines.append("%s\t%s\n" % (m["path"], m["sha256"]))
    lines.sort(key=lambda s: s.split("\t", 1)[0].encode("utf-8",
                                                         "surrogateescape"))
    return sha256_bytes("".join(lines).encode("utf-8", "surrogateescape"))


def run(argv, cwd=None):
    t0 = time.monotonic()
    proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          cwd=cwd)
    wall = time.monotonic() - t0
    return {
        "argv": list(argv),
        "exit": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "surrogateescape"),
        "stderr": proc.stderr.decode("utf-8", "surrogateescape"),
        "stdout_sha256": sha256_bytes(proc.stdout),
        "stderr_sha256": sha256_bytes(proc.stderr),
        "wall_s": round(wall, 3),
    }


# ------------------------------------------------------------------- parsing

def parse_listing(text):
    """(rows, prefix, error).  Each row: type, mode, owner, size, mtime, path.

    `size` is None for directories and symlinks, an int for regular files,
    and the "major, minor" string for device nodes.  `detail` carries the
    symlink target or the device numbers.
    """
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        m = U_LLS.match(line)
        if not m:
            return None, None, "unparsed listing line %r" % line
        mode, owner, sizefield, date, clock, rest = m.groups()
        kind = KIND_NAMES[mode[0]]
        detail = ""
        if kind == "symlink":
            if " -> " not in rest:
                return None, None, "symlink row without a target %r" % line
            path, target = rest.rsplit(" -> ", 1)
            detail = target
        else:
            path = rest
        if kind in ("char-device", "block-device"):
            detail = ",".join(part.strip() for part in sizefield.split(","))
            size = None
        elif kind == "regular":
            size = int(sizefield)
        else:
            size = None
        rows.append({
            "type": kind,
            "mode": mode,
            "owner": owner,
            "size": size,
            "mtime": "%s %s" % (date, clock),
            "path": path,
            "detail": detail,
        })
    if not rows:
        return None, None, "empty listing"
    prefix = rows[0]["path"]
    if not prefix.endswith("/"):
        prefix += "/"
    for row in rows:
        if not row["path"].startswith(prefix) and row["path"] != prefix[:-1]:
            return None, None, ("listing row %r is not under the root prefix %r"
                                % (row["path"], prefix))
        row["rel"] = (row["path"][len(prefix):]
                      if row["path"] != prefix[:-1] else "")
    return rows, prefix, None


def walk_tree(root):
    """(regular, nonregular, error) for an extracted tree.

    regular:   [{"path", "size", "sha256", "type"}]  (path relative to root)
    nonregular:[{"path", "type", "size", "detail", "mode"}]
    """
    regular, nonregular = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(dirnames + filenames):
            full = os.path.join(dirpath, name)
            rel = rel_posix(full, root)
            st = os.lstat(full)
            if stat.S_ISREG(st.st_mode):
                regular.append({
                    "path": rel,
                    "size": st.st_size,
                    "sha256": sha256_file(full),
                    "type": "regular",
                })
            elif stat.S_ISDIR(st.st_mode):
                nonregular.append({"path": rel, "type": "dir", "size": None,
                                   "detail": "", "mode": stat.filemode(st.st_mode)})
            elif stat.S_ISLNK(st.st_mode):
                nonregular.append({"path": rel, "type": "symlink", "size": None,
                                   "detail": os.readlink(full),
                                   "mode": stat.filemode(st.st_mode)})
            else:
                kind = "other"
                if stat.S_ISCHR(st.st_mode):
                    kind = "char-device"
                elif stat.S_ISBLK(st.st_mode):
                    kind = "block-device"
                elif stat.S_ISFIFO(st.st_mode):
                    kind = "fifo"
                elif stat.S_ISSOCK(st.st_mode):
                    kind = "socket"
                nonregular.append({"path": rel, "type": kind, "size": None,
                                   "detail": "", "mode": stat.filemode(st.st_mode)})
    regular.sort(key=lambda m: m["path"])
    nonregular.sort(key=lambda m: m["path"])
    return regular, nonregular, None


# ------------------------------------------------------------ oracle B tree

def resolve_output_tree(oracle_root, carrier):
    """The committed `__output__` tree of a carrier, or (None, None, reason).

    Candidate layouts, in order:
      1. <oracle_root>/<id>__output__/                 (seat-spec layout)
      2. <oracle_root>/<handler>/<little|big>_endian/__output__/
         (the upstream-path layout the fetcher used)
      3. <oracle_root>/<upstream>/__output__/           (upstream path)
    """
    cands = [
        os.path.join(oracle_root, carrier["id"] + "__output__"),
        os.path.join(oracle_root, carrier["handler"],
                     "little_endian" if carrier["endian"] == "le"
                     else "big_endian", "__output__"),
        os.path.join(oracle_root, carrier["upstream"], "__output__"),
    ]
    for cand in cands:
        if os.path.isdir(cand):
            return cand, None, None
    return None, cands, ("no committed __output__ tree for carrier %r "
                          "(tried %s)" % (carrier["id"],
                                          ", ".join(cands)))


def extract_root_of(tree_root, carrier):
    """The '*_extract' directory inside the `__output__` tree, if any."""
    want = carrier["extract_dir"]
    entries = sorted(os.listdir(tree_root))
    if want in entries and os.path.isdir(os.path.join(tree_root, want)):
        return os.path.join(tree_root, want), want
    for name in entries:
        if name.endswith("_extract") and os.path.isdir(os.path.join(tree_root,
                                                                    name)):
            return os.path.join(tree_root, name), name
    return tree_root, ""


# ------------------------------------------------------------------ carriers

def load_carriers(path):
    """The carrier list: from `--carriers` when given, else the frozen table."""
    if not path:
        return [dict(c) for c in CARRIERS], "frozen-table"
    if not os.path.isfile(path):
        raise OracleError(EXIT_CANNOT_EVALUATE, "carriers file not found",
                          path)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        raise OracleError(EXIT_CANNOT_EVALUATE, "carriers file unreadable",
                          "%s: %s" % (path, exc))
    listed = doc.get("carriers") if isinstance(doc, dict) else doc
    if not isinstance(listed, list) or not listed:
        raise OracleError(EXIT_CANNOT_EVALUATE, "carriers file has no list",
                          path)
    by_id = {norm_id(c["id"]): c for c in CARRIERS}
    out = []
    for entry in listed:
        if not isinstance(entry, dict) or "id" not in entry:
            raise OracleError(EXIT_CANNOT_EVALUATE, "carrier entry without id",
                              repr(entry)[:200])
        base = by_id.get(norm_id(entry["id"]))
        if base is None:
            raise OracleError(EXIT_CANNOT_EVALUATE,
                              "carrier id is not one of the frozen four",
                              entry["id"])
        merged = dict(base)
        merged.update({k: v for k, v in entry.items()
                       if k in ("sha256", "handler", "endian", "fixture",
                                "expected_files", "upstream", "extract_dir")})
        out.append(merged)
    return out, path


def fixture_path(root, carrier, fixtures_dir):
    """Absolute path of the carrier's committed fixture bytes."""
    if fixtures_dir:
        cand = os.path.join(fixtures_dir, carrier["fixture"])
        if os.path.isfile(cand):
            return cand
    cand = os.path.join(root, "corpus/evidence/round-42/c2/fixtures",
                        carrier["fixture"])
    if os.path.isfile(cand):
        return cand
    return None


# --------------------------------------------------------------- one carrier

def build_carrier(carrier, root, work, fixtures_dir, oracle_root, tool_sha):
    """The oracle block of one carrier, or raise OracleError."""
    cid = carrier["id"]
    image = fixture_path(root, carrier, fixtures_dir)
    if image is None:
        raise OracleError(EXIT_CANNOT_EVALUATE,
                          "fixture bytes missing for carrier %r" % cid,
                          carrier["fixture"])
    image_sha = sha256_file(image)
    if carrier.get("sha256") and image_sha != carrier["sha256"]:
        raise OracleError(EXIT_FAILED,
                          "carrier %r bytes do not match the frozen pin" % cid,
                          "expected %s, got %s" % (carrier["sha256"], image_sha))

    # (a) member census
    lls = run([UNSQUASHFS, "-lls", image])
    if lls["exit"] != 0:
        raise OracleError(EXIT_FAILED, "unsquashfs -lls failed for %r" % cid,
                          "exit %d: %s" % (lls["exit"], lls["stderr"][-400:]))
    rows, prefix, err = parse_listing(lls["stdout"])
    if err:
        raise OracleError(EXIT_FAILED, "cannot parse the -lls census of %r" % cid,
                          err)

    # (0) informational superblock summary from the oracle tool itself.
    # The AUTHORITATIVE v1/v2 superblock probe (magic/major/minor/
    # endianness/compression) belongs to the counter (R44C1Counter); this
    # block is the oracle tool's own report, kept raw and clearly labeled
    # so the two never silently diverge.
    sb = run([UNSQUASHFS, "-s", image])
    sb_lines = [ln.strip() for ln in sb["stdout"].splitlines() if ln.strip()]
    sb_summary = {
        "argv": sb["argv"],
        "exit": sb["exit"],
        "stdout_sha256": sb["stdout_sha256"],
        "stdout_lines": sb_lines,
        "note": "informational only - the counter owns the binding v1/v2 "
                "superblock probe; this is the oracle tool's own report",
    }

    # (b) extract into a fresh scratch directory
    dest = os.path.join(work, "extract", cid)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    ext = run([UNSQUASHFS, "-d", dest, image])
    if ext["exit"] != 0:
        raise OracleError(EXIT_FAILED, "unsquashfs extraction failed for %r" % cid,
                          "exit %d: %s" % (ext["exit"], ext["stderr"][-400:]))
    regular, nonreg_tree, err = walk_tree(dest)
    if err:
        raise OracleError(EXIT_FAILED, "cannot walk the extraction of %r" % cid,
                          err)

    # census vs extraction cross-check (regular files only)
    census_reg = {}
    for row in rows:
        if row["type"] == "regular" and row["rel"]:
            census_reg[row["rel"]] = row["size"]
    tree_reg = {m["path"]: m["size"] for m in regular}
    census_only = sorted(set(census_reg) - set(tree_reg))
    tree_only = sorted(set(tree_reg) - set(census_reg))
    size_diff = sorted(p for p in set(census_reg) & set(tree_reg)
                        if census_reg[p] != tree_reg[p])
    if census_only or tree_only or size_diff:
        raise OracleError(EXIT_FAILED,
                          "census and extraction disagree for %r" % cid,
                          "census_only=%r tree_only=%r size_diff=%r"
                          % (census_only, tree_only, size_diff))
    if carrier.get("expected_files") and len(regular) != carrier["expected_files"]:
        raise OracleError(EXIT_FAILED,
                          "carrier %r extracted %d regular files, expected %d"
                          % (cid, len(regular), carrier["expected_files"]),
                          "")

    # (c) non-regular members
    nonregular = []
    for row in rows:
        if row["type"] == "regular" or not row["rel"]:
            continue
        nonregular.append({
            "path": row["rel"],
            "type": row["type"],
            "mode": row["mode"],
            "owner": row["owner"],
            "size": row["size"],
            "mtime": row["mtime"],
            "detail": row["detail"],
        })
    for row in nonreg_tree:
        if row["type"] == "dir":
            continue                      # directories carry no member identity
        nonregular.append({
            "path": row["path"],
            "type": row["type"],
            "mode": row["mode"],
            "owner": "",
            "size": row["size"],
            "mtime": "",
            "detail": row["detail"],
        })
    nonregular.sort(key=lambda r: (r["path"], r["type"]))

    # (d) oracle B - the committed unblob `__output__` expected tree
    tree_root, cands, reason = resolve_output_tree(oracle_root, carrier)
    if tree_root is None:
        raise OracleError(EXIT_CANNOT_EVALUATE,
                          "committed __output__ tree missing for %r" % cid,
                          reason)
    ex_root, ex_name = extract_root_of(tree_root, carrier)
    b_reg, b_nonreg, err = walk_tree(ex_root)
    if err:
        raise OracleError(EXIT_FAILED, "cannot walk the __output__ tree of %r"
                          % cid, err)
    b_digest = digest_of(b_reg)
    a_digest = digest_of(regular)

    mismatches = []
    a_by = {m["path"]: m for m in regular}
    b_by = {m["path"]: m for m in b_reg}
    for path in sorted(set(a_by) | set(b_by)):
        a = a_by.get(path)
        b = b_by.get(path)
        if a is None:
            mismatches.append({"path": path, "reason": "only in __output__",
                               "sha256": b["sha256"]})
        elif b is None:
            mismatches.append({"path": path, "reason": "only in unsquashfs",
                               "sha256": a["sha256"]})
        elif a["sha256"] != b["sha256"]:
            mismatches.append({"path": path, "reason": "sha256 differs",
                               "unsquashfs": a["sha256"],
                               "output_tree": b["sha256"]})
        elif a["size"] != b["size"]:
            mismatches.append({"path": path, "reason": "size differs",
                               "unsquashfs": a["size"],
                               "output_tree": b["size"]})
    if mismatches:
        raise OracleError(EXIT_FAILED,
                          "the two oracles disagree for %r" % cid,
                          "%d mismatch(es): %r" % (len(mismatches),
                                                  mismatches[:5]))

    block = {
        "members": [{"path": m["path"], "size": m["size"],
                     "sha256": m["sha256"], "type": m["type"]}
                    for m in regular],
        "nonregular": nonregular,
        "oracle_tool": ORACLE_TOOL,
        "oracle_ver": ORACLE_VER,
        "oracle_tool_path": UNSQUASHFS,
        "oracle_tool_sha256": tool_sha,
        "output_tree_digest": a_digest,
        "output_tree_digest_def":
            "sha256 over the concatenation of '<path>\\t<sha256>\\n' lines "
            "of `members`, sorted bytewise by path",
        "output_tree": {
            "root": rel_posix(tree_root, root),
            "extract_root": rel_posix(ex_root, root),
            "extract_dir": ex_name,
            "members": [{"path": m["path"], "size": m["size"],
                         "sha256": m["sha256"], "type": m["type"]}
                        for m in b_reg],
            "output_tree_digest": b_digest,
            "agrees_with_unsquashfs": True,
            "mismatches": [],
            "producer_lineage":
                "unblob 26.6.4 integration expectation (S138); produced by "
                "unblob's own squashfs handler (sasquatch 4.5.1 lineage), so "
                "it cross-checks the member set but is NOT an independent "
                "producer - the independent oracle is `unsquashfs` 4.7.5",
        },
        "census": [{k: row[k] for k in ("type", "mode", "owner", "size",
                                        "mtime", "path", "rel")}
                   for row in rows],
        "superblock_info": sb_summary,
        "extraction": {
            "argv": ext["argv"],
            "exit": ext["exit"],
            "stderr_tail": ext["stderr"][-400:],
            "stdout_sha256": ext["stdout_sha256"],
            "stderr_sha256": ext["stderr_sha256"],
            "wall_s": ext["wall_s"],
        },
        "listing": {
            "argv": lls["argv"],
            "exit": lls["exit"],
            "root_prefix": prefix,
            "stdout_sha256": lls["stdout_sha256"],
            "stderr_sha256": lls["stderr_sha256"],
            "wall_s": lls["wall_s"],
        },
        "image": {
            "path": rel_posix(image, root),
            "sha256": image_sha,
            "size": os.path.getsize(image),
        },
        "handler": carrier["handler"],
        "endian": carrier["endian"],
    }
    return block


# ------------------------------------------------------------------ selftest

SELFTEST_LISTING = "\n".join([
    "drwxrwxrwx u/g                    42 2024-08-05 04:18 squashfs-root",
    "-rw-rw-r-- u/g                     6 2024-08-05 03:53 squashfs-root/apple.txt",
    "lrwxrwxrwx u/g                     3 2024-08-05 04:18 squashfs-root/link -> a/b",
    "crw-rw-rw- u/g                 1,   3 2024-08-05 04:18 squashfs-root/dev",
]) + "\n"


def selftest():
    """(ok, report).  Exercises the parser and the digest rule."""
    failures = []

    rows, prefix, err = parse_listing(SELFTEST_LISTING)
    if err:
        failures.append("parse_listing: %s" % err)
    else:
        by = {r["rel"]: r for r in rows}
        if prefix != "squashfs-root/":
            failures.append("prefix %r" % prefix)
        if by.get("apple.txt", {}).get("size") != 6:
            failures.append("apple.txt size %r"
                            % by.get("apple.txt", {}).get("size"))
        if by.get("apple.txt", {}).get("mtime") != "2024-08-05 03:53":
            failures.append("apple.txt mtime %r"
                            % by.get("apple.txt", {}).get("mtime"))
        if by.get("link", {}).get("type") != "symlink":
            failures.append("link type %r" % by.get("link", {}).get("type"))
        if by.get("link", {}).get("detail") != "a/b":
            failures.append("link detail %r" % by.get("link", {}).get("detail"))
        if by.get("dev", {}).get("type") != "char-device":
            failures.append("dev type %r" % by.get("dev", {}).get("type"))
        if by.get("dev", {}).get("detail") != "1,3":
            failures.append("dev detail %r" % by.get("dev", {}).get("detail"))

    # digest rule: sorted, path-delimited, newline terminated
    members = [{"path": "b.txt", "sha256": "22"}, {"path": "a.txt",
                                                   "sha256": "11"}]
    expect = sha256_bytes(b"a.txt\t11\nb.txt\t22\n")
    if digest_of(members) != expect:
        failures.append("digest_of does not follow the declared rule")
    if digest_of(list(reversed(members))) != expect:
        failures.append("digest_of is not order independent")

    # id normalisation: the draft spells the carriers V1LE, the spec v1-le
    if norm_id("V1LE") != norm_id("v1-le") or norm_id("v1_be") != norm_id("V1BE"):
        failures.append("norm_id does not unify the two id spellings")

    report = {"cases": 12, "failures": failures}
    return (not failures), report


# ---------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="c1-oracle.py",
        description="Build the frozen R44-C1 oracle blocks (independent "
                    "unsquashfs 4.7.5 census + the committed unblob "
                    "__output__ expected trees).")
    ap.add_argument("--root", help="lane root (default: cwd)")
    ap.add_argument("--work", help="scratch directory for extractions")
    ap.add_argument("--carriers", help="carriers.json to read the ids from")
    ap.add_argument("--fixtures-dir", help="directory holding the carrier "
                                           "fixture bytes")
    ap.add_argument("--oracle-root",
                    help="committed __output__ tree root (default: "
                         "<root>/corpus/evidence/round-44/oracle)")
    ap.add_argument("--json-out", help="where to write the oracle blocks")
    ap.add_argument("--merge-carriers",
                    help="write the oracle blocks into this carriers.json "
                         "(the 'oracle' key of every carrier entry is "
                         "replaced); the file is rewritten in place")
    ap.add_argument("--receipt", help="where to write the run receipt")
    ap.add_argument("--only", help="restrict to one carrier id (repeatable)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the built-in self test and exit")
    ap.add_argument("--seat", default=SEAT, help="seat name for the receipt")
    args = ap.parse_args(argv)

    if args.selftest:
        ok, report = selftest()
        sys.stdout.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
        return EXIT_OK if ok else EXIT_FAILED

    t0 = time.monotonic()
    root = os.path.abspath(args.root or os.getcwd())
    if not os.path.isdir(root):
        sys.stderr.write("c1-oracle.py: lane root %s is not a directory\n"
                         % root)
        return EXIT_CANNOT_EVALUATE

    if not os.path.isfile(UNSQUASHFS) or not os.access(UNSQUASHFS, os.X_OK):
        sys.stderr.write("c1-oracle.py: %s is missing or not executable\n"
                         % UNSQUASHFS)
        return EXIT_CANNOT_EVALUATE
    tool_sha = sha256_file(UNSQUASHFS)
    ver = run([UNSQUASHFS, "-version"])["stdout"].strip().splitlines()
    tool_ver_line = ver[0] if ver else ""
    if ORACLE_VER not in tool_ver_line:
        sys.stderr.write("c1-oracle.py: %s reports %r, expected %s\n"
                         % (UNSQUASHFS, tool_ver_line, ORACLE_VER))
        return EXIT_CANNOT_EVALUATE

    oracle_root = os.path.abspath(args.oracle_root or os.path.join(
        root, "corpus/evidence/round-44/oracle"))

    try:
        carriers, carriers_src = load_carriers(args.carriers)
    except OracleError as exc:
        sys.stderr.write("c1-oracle.py: %s: %s\n" % (exc.reason, exc.detail))
        return exc.code

    if args.only:
        wanted = {norm_id(x) for x in args.only}
        carriers = [c for c in carriers if norm_id(c["id"]) in wanted]
        if not carriers:
            sys.stderr.write("c1-oracle.py: no carrier matches %r\n"
                             % (args.only,))
            return EXIT_CANNOT_EVALUATE

    work = args.work
    if work:
        work = os.path.abspath(work)
        os.makedirs(work, exist_ok=True)
    else:
        work = tempfile.mkdtemp(prefix="r44-c1-oracle-")

    blocks = {}
    problems = []
    for carrier in carriers:
        try:
            blocks[carrier["id"]] = build_carrier(carrier, root, work,
                                                  args.fixtures_dir,
                                                  oracle_root, tool_sha)
        except OracleError as exc:
            problems.append({"carrier": carrier["id"], "reason": exc.reason,
                             "detail": exc.detail, "exit": exc.code})
        except OSError as exc:
            problems.append({"carrier": carrier["id"],
                             "reason": "filesystem error",
                             "detail": str(exc), "exit": EXIT_FAILED})

    doc = {
        "schema": SCHEMA,
        "seat": args.seat,
        "carriers_source": carriers_src,
        "oracle_tool": ORACLE_TOOL,
        "oracle_ver": ORACLE_VER,
        "oracle_tool_path": UNSQUASHFS,
        "oracle_tool_sha256": tool_sha,
        "oracle_tool_version_line": tool_ver_line,
        "oracle_root": rel_posix(oracle_root, root),
        "carriers": blocks,
        "problems": problems,
    }

    exit_code = EXIT_OK
    if problems:
        exit_code = max(p["exit"] for p in problems)

    if args.merge_carriers:
        if not blocks:
            sys.stderr.write("c1-oracle.py: no oracle block to merge\n")
            return exit_code
        mpath = os.path.abspath(args.merge_carriers)
        if not os.path.isfile(mpath):
            sys.stderr.write("c1-oracle.py: merge target %s does not exist\n"
                             % mpath)
            return EXIT_CANNOT_EVALUATE
        with open(mpath, "r", encoding="utf-8") as fh:
            mdoc = json.load(fh)
        entries = mdoc.get("carriers") if isinstance(mdoc, dict) else mdoc
        if not isinstance(entries, list):
            sys.stderr.write("c1-oracle.py: merge target has no carrier list\n")
            return EXIT_CANNOT_EVALUATE
        merged, missing = 0, []
        for entry in entries:
            key = norm_id(entry.get("id"))
            block = blocks.get(entry.get("id"))
            if block is None:
                for cid, blk in blocks.items():
                    if norm_id(cid) == key:
                        block = blk
                        break
            if block is None:
                missing.append(entry.get("id"))
                continue
            entry["oracle"] = block
            merged += 1
        if missing:
            sys.stderr.write("c1-oracle.py: no oracle block for %r\n"
                             % (missing,))
            return EXIT_CANNOT_EVALUATE
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump(mdoc, fh, indent=2, sort_keys=True)
            fh.write("\n")
        doc["merged_into"] = rel_posix(mpath, root)
        doc["merged_carriers"] = merged

    if args.json_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_out)),
                    exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, sort_keys=True)
            fh.write("\n")

    stdout = json.dumps(doc, indent=2, sort_keys=True) + "\n"
    if not args.json_out:
        sys.stdout.write(stdout)

    if args.receipt:
        receipt = {
            "schema": "kaidoku-r44-c1-oracle-receipt-v1",
            "seat": args.seat,
            "command": ["python3", "-I", "-B", "c1-oracle.py"]
                       + list(argv if argv is not None else sys.argv[1:]),
            "exit_code": exit_code,
            "stdout_sha256": sha256_bytes(stdout.encode("utf-8",
                                                         "surrogateescape")),
            "wall_s": round(time.monotonic() - t0, 3),
            "carriers": sorted(blocks),
            "problems": problems,
            "oracle_tool": ORACLE_TOOL,
            "oracle_ver": ORACLE_VER,
            "oracle_tool_sha256": tool_sha,
            "counter_sha256": None,
            "counter_sha256_at_freeze": None,
            "note": "pre-freeze oracle build; the after-side C1 data "
                    "procedure (c1-run.sh) is NOT run by this tool",
        }
        os.makedirs(os.path.dirname(os.path.abspath(args.receipt)),
                    exist_ok=True)
        with open(args.receipt, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")

    if args.work is None:
        shutil.rmtree(work, ignore_errors=True)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
