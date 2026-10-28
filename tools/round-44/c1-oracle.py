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

Oracle B - the unblob `__output__` expected trees (second reading)
  The committed tree under `corpus/evidence/round-44/oracle/` (fetched
  pre-freeze by seat R44SrcOracle, dataset S138) is walked and its member
  digests recorded.  This tree is unblob's OWN expectation for the same
  fixtures, produced by unblob's sasquatch-backed handler: it is a second
  reading of the same bytes, NOT an independent producer, and it must not be
  described as one (see `producer_lineage` in the emitted block).

Oracle C - 7-Zip (third producer, corroboration only)
  `7z` 26.04 reads the same images and must agree with oracle A on the
  member set and every content digest.  It is distinct from both
  `unsquashfs` and sasquatch, so it is a genuine third reading, but it
  CORROBORATES oracle A - it does not replace the independent oracle, which
  remains `unsquashfs`.

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

SEVENZIP = "/usr/bin/7z"
SEVENZIP_VER = "26.04"

# The digest rule string, byte-identical to the one the R44-C1 counter states
# in `TREE_DIGEST_RULE` and validates against
# `TREE_DIGEST_RULE_TOKENS = ('sha256', '<path>', '<sha256>',
# 'bytewise by path')`.  Emitting the same literal keeps the two sides from
# drifting; every token the counter requires is present here.
TREE_DIGEST_RULE = ("sha256 over the concatenation of '<path>\\t<sha256>\\n' "
                    "lines of `members`, sorted bytewise by path")

EXIT_OK, EXIT_FAILED, EXIT_CANNOT_EVALUATE = 0, 1, 2

SEAT = "R44C1Oracle"

# --------------------------------------------------------------------------
# The frozen carrier table.
#
# The authoritative list is `tools/round-44/carriers.json` (frozen by the
# L1): every carrier entry names its own `path` (lane-relative image bytes),
# `sha256` pin, `handler`, `endian`, `expected_regular` and `output_tree`
# (lane-relative path of the committed unblob `__output__` extract tree).
# This table is only the FALLBACK used when no `--carriers` file is given,
# and it carries the four carriers of the seat spec (v1-le, v1-be, v2-le,
# v2-be) with the pins copied from `tools/round-42/fixtures.json` (MIT
# unblob 26.6.4 fixtures under corpus/evidence/round-42/c2/fixtures/).
#
# Ids are matched case- and separator-insensitively, so the seat spec's
# `v1-le`, the draft claims' `V1LE` and the frozen file's `v1le` all
# resolve to one carrier.
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
        "scope": "target",
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
        "scope": "target",
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
        "scope": "target",
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
        "scope": "target",
    },
)

# The four PREREGISTERED target carriers of R44-C1 (the ids frozen in the
# draft claims' carrier table).  The L1's 2026-10-28 amendment reverts the
# C1 target to exactly these four: the `squashfs_v2` 2.1 pair
# (`v21le`/`v21be`) was added mid-wave but its REA probe was exploratory and
# unretained, so it is UNBOUND exploratory data, NOT scored.  The tool
# therefore emits the v2.1 oracle blocks under `exploratory` (kept, because
# the measurements are real and cost nothing to retain) and NEVER under
# `carriers`, which is the scored set.
TARGET_IDS = ("v1-le", "v1-be", "v2-le", "v2-be")

# Carriers that are measured and retained but explicitly NOT scored.
EXPLORATORY_IDS = ("v21le", "v21be")

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


# ------------------------------------------------------- 7-Zip corroboration

def sevenzip_members(image, work):
    """(members, header, error) - 7-Zip's own reading of a squashfs image.

    7-Zip is a THIRD producer, distinct from both `unsquashfs` (squashfs-
    tools) and sasquatch (the unblob 26.6.4 extractor).  It corroborates the
    member set and the content digests; it does not replace the independent
    oracle, which stays `unsquashfs`.

    `header` carries the archive-level facts 7-Zip reports (file system
    version, compression method, endianness), which is a second, independent
    reading of the superblock.
    """
    dest = os.path.join(work, "sevenzip", os.path.basename(image))
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    run([SEVENZIP, "x", "-tSquashFS", "-y", "-o" + dest, image])
    regular, _nonreg, _err = walk_tree(dest)
    listing = run([SEVENZIP, "l", "-tSquashFS", "-slt", image])
    header = {}
    for line in listing["stdout"].splitlines():
        if " = " not in line:
            continue
        key, _, value = line.partition(" = ")
        key = key.strip()
        if key in ("File System", "Method", "Big-endian", "Cluster Size",
                   "Created", "Physical Size", "Headers Size"):
            header.setdefault(key, value.strip())
    return regular, header, None


# --------------------------------------------------- v1/v2 superblock probe

# The SquashFS v1/v2 superblock is 32 bytes (packed), per unblob 26.6.4's
# `SquashFSv1Handler.C_DEFINITIONS` (S119):
#
#   char   s_magic[4];              //  0:4
#   uint32 inodes;                  //  4:8
#   uint32 bytes_used;              //  8:12
#   uint32 uid_start;               // 12:16
#   uint32 guid_start;              // 16:20
#   uint32 inode_table_start;       // 20:24
#   uint32 directory_table_start;   // 24:28
#   uint16 s_major;                 // 28:30
#   uint16 s_minor;                 // 30:32
#
# THERE IS NO COMPRESSION FIELD IN THE v1/v2 SUPERBLOCK.  The compression
# id lives in the v4 layout (u16 at offset 20), which is why `file(1)` -
# which applies the v4 layout to every squashfs image - prints a
# meaningless "compressed"/"uncompressed" verdict for a v1/v2 image: it
# reads offset 20 (inode_table_start) as if it were the v4 compression id.
# The real compression class of a v1/v2 image is observed from the
# compression of its inode-table metadata block (zlib header 78 xx =>
# gzip), which is what `superblock_info` records below.

SB_V1V2_SIZE = 32
SB_MAGICS = {
    b"hsqs": "le",   # squashfs 1-3 little endian
    b"sqsh": "be",   # squashfs 1-3 big endian
}


def sb_u(raw, off, size, endian):
    """An unsigned superblock field, read with the filesystem's endianness."""
    return int.from_bytes(raw[off:off + size],
                          "big" if endian == "be" else "little")


def probe_v1v2_superblock(raw):
    """(fields, error) for a v1/v2 superblock.

    `fields` holds magic, endianness, major, minor, bytes_used, inodes,
    uid_start, guid_start, inode_table_start, directory_table_start, the
    metadata block header and the compression class observed from the
    inode table's metadata block.  It never invents a compression field:
    the v1/v2 superblock has none.
    """
    if raw is None or len(raw) < SB_V1V2_SIZE:
        return None, "shorter than the 32-byte v1/v2 superblock"
    magic = raw[0:4]
    endian = SB_MAGICS.get(magic)
    if endian is None:
        return None, "magic %r is not a squashfs 1-3 magic" % magic
    d = {
        "magic": magic.decode("latin1"),
        "endianness": endian,
        "major": sb_u(raw, 28, 2, endian),
        "minor": sb_u(raw, 30, 2, endian),
        "inodes": sb_u(raw, 4, 4, endian),
        "bytes_used": sb_u(raw, 8, 4, endian),
        "uid_start": sb_u(raw, 12, 4, endian),
        "guid_start": sb_u(raw, 16, 4, endian),
        "inode_table_start": sb_u(raw, 20, 4, endian),
        "directory_table_start": sb_u(raw, 24, 4, endian),
        "superblock_size": SB_V1V2_SIZE,
    }
    its, dts = d["inode_table_start"], d["directory_table_start"]
    d["starts_sane"] = bool(SB_V1V2_SIZE <= its < dts <= d["bytes_used"])
    # the inode table's metadata block: a 2-byte header whose top bit is the
    # "stored uncompressed" flag and whose low 12 bits are the length
    d["meta_header_hex"] = None
    d["meta_len"] = None
    d["meta_uncompressed"] = None
    d["compression"] = None
    d["meta_chain_lands"] = None
    if d["starts_sane"]:
        hdr = raw[its:its + 2]
        d["meta_header_hex"] = hdr.hex()
        value = sb_u(raw, its, 2, endian)
        d["meta_uncompressed"] = bool(value & 0x8000)
        length = value & 0x7FFF
        d["meta_len"] = length
        d["meta_chain_lands"] = bool(its + 2 + length == dts)
        if not d["meta_uncompressed"]:
            body = raw[its + 2:its + 2 + length]
            if len(body) >= 2 and body[0] == 0x78 and body[1] in (0x01, 0x5E,
                                                                    0x9C, 0xDA):
                d["compression"] = "gzip"
    return d, None


# ------------------------------------------------------------ oracle B tree

def output_tree_rel(carrier, root):
    """The carrier's committed `__output__` tree path RELATIVE to the oracle root.

    The frozen carriers.json names the tree lane-relative
    (`corpus/evidence/round-44/oracle/...`).  Stripping the default oracle
    root leaves the part that identifies the tree inside whatever
    `--oracle-root` is given, so an explicit override is honoured instead of
    being shadowed by the lane-relative path.
    """
    rel = carrier.get("output_tree")
    if not isinstance(rel, str) or not rel:
        return None
    if os.path.isabs(rel):
        return None
    default_root = os.path.join(root or "", "corpus/evidence/round-44/oracle")
    full = os.path.join(root or "", rel)
    try:
        inside = os.path.relpath(full, default_root)
    except ValueError:
        return None
    if inside.startswith(".."):
        return None
    return inside


def resolve_output_tree(oracle_root, carrier, root=None, strict=False):
    """The committed `__output__` tree of a carrier, or (None, None, reason).

    Order:
      1. the frozen carriers.json `output_tree`, re-rooted at `--oracle-root`;
      2. <oracle_root>/<id>__output__/                 (seat-spec layout)
      3. <oracle_root>/<handler>/<little|big>_endian/__output__/
         (the upstream-path layout the fetcher used)
      4. <oracle_root>/<upstream>/__output__/           (upstream path)

    `strict` (an EXPLICIT `--oracle-root`) drops the lane-relative fallback,
    so the override is authoritative: a tree that is only present in the
    lane must not silently satisfy an override that points elsewhere.
    """
    cands = []
    inside = output_tree_rel(carrier, root)
    if inside:
        cands.append(os.path.join(oracle_root, inside))
    rel = carrier.get("output_tree")
    if isinstance(rel, str) and rel and root and not strict:
        cands.append(os.path.join(root, rel))
    cands.append(os.path.join(oracle_root, carrier["id"] + "__output__"))
    if carrier.get("handler"):
        cands.append(os.path.join(
            oracle_root, carrier["handler"],
            "little_endian" if carrier.get("endian") == "le" else "big_endian",
            "__output__"))
    if carrier.get("upstream"):
        cands.append(os.path.join(oracle_root, carrier["upstream"],
                                  "__output__"))
    seen, uniq = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    for cand in uniq:
        if os.path.isdir(cand):
            return cand, None, None
    return None, uniq, ("no committed __output__ tree for carrier %r "
                         "(tried %s)" % (carrier["id"], ", ".join(uniq)))


def extract_root_of(tree_root, carrier):
    """The '*_extract' directory inside the `__output__` tree, if any.

    The frozen carriers.json `output_tree` may already name the extract
    tree itself; in that case it is used as-is.
    """
    want = carrier.get("extract_dir")
    base = os.path.basename(tree_root.rstrip("/"))
    if base.endswith("_extract"):
        return tree_root, base
    entries = sorted(os.listdir(tree_root))
    if want and want in entries and os.path.isdir(os.path.join(tree_root,
                                                               want)):
        return os.path.join(tree_root, want), want
    for name in entries:
        if name.endswith("_extract") and os.path.isdir(os.path.join(tree_root,
                                                                    name)):
            return os.path.join(tree_root, name), name
    return tree_root, ""


def scope_ids(carriers):
    """(target_ids, exploratory_ids) as the carriers' own `id` values.

    NEVER a spec-spelling constant: the frozen carriers.json spells the same
    four carriers `v1le` while this module's TARGET_IDS spells them `v1-le`,
    so emitting the constant would hand a consumer a name that matches no
    carrier entry.  The split therefore comes from the loaded list.
    """
    targets = [c["id"] for c in carriers if c.get("scope") == "target"]
    exploratory = [c["id"] for c in carriers if c.get("scope") != "target"]
    return targets, exploratory


# ------------------------------------------------------------------ carriers

def load_carriers(path):
    """The carrier list: from `--carriers` when given, else the frozen table.

    A carriers.json entry supplies its own `path` (lane-relative image
    bytes), `sha256` pin, `handler`, `endian`, `expected_regular` and
    `output_tree` (lane-relative `__output__` extract tree).  A carrier
    that omits `path` falls back to the built-in table's fixture location.
    """
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
        merged = dict(base) if base else {}
        # the frozen file's own fields win over the built-in table
        for key in ("id", "sha256", "handler", "endian", "fixture", "path",
                    "upstream", "extract_dir", "expected_files",
                    "expected_regular", "output_tree", "file", "s_major",
                    "s_minor", "compression"):
            if key in entry:
                merged[key] = entry[key]
        if "expected_regular" in merged and "expected_files" not in merged:
            merged["expected_files"] = merged["expected_regular"]
        # scope: a carrier is `target` only if its id is one of the four
        # preregistered C1 targets.  Anything else in the frozen file is
        # measured and retained as `exploratory` but is NEVER scored.
        merged["scope"] = "target" if norm_id(entry["id"]) in {
            norm_id(t) for t in TARGET_IDS} else "exploratory"
        # A carrier the tool knows nothing about cannot be built: it has no
        # fixture location and no handler binding.  Refuse it as
        # could-not-evaluate rather than crashing later.
        if not merged.get("path") and not merged.get("fixture"):
            raise OracleError(EXIT_CANNOT_EVALUATE,
                              "carrier %r names no image bytes" % entry["id"],
                              "expected a lane-relative `path` or a `fixture`")
        out.append(merged)
    return out, path


def fixture_path(root, carrier, fixtures_dir):
    """Absolute path of the carrier's committed fixture bytes.

    Order: the frozen carriers.json `path` (lane-relative), then an explicit
    `--fixtures-dir`, then the built-in table's fixture location.
    """
    cands = []
    rel = carrier.get("path")
    if isinstance(rel, str) and rel:
        cands.append(rel if os.path.isabs(rel) else os.path.join(root, rel))
    if fixtures_dir:
        name = carrier.get("file") or carrier.get("fixture")
        if name:
            cands.append(os.path.join(fixtures_dir, name))
    name = carrier.get("fixture")
    if name:
        cands.append(os.path.join(root, "corpus/evidence/round-42/c2/fixtures",
                                  name))
    for cand in cands:
        if os.path.isfile(cand):
            return cand
    return None


# --------------------------------------------------------------- one carrier

def build_carrier(carrier, root, work, fixtures_dir, oracle_root, tool_sha,
                  strict_tree=False):
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
    with open(image, "rb") as fh:
        image_raw = fh.read()
    sb_fields, sb_err = probe_v1v2_superblock(image_raw)
    file_out = run(["/usr/bin/file", "-b", image])
    sb_summary = {
        "argv": sb["argv"],
        "exit": sb["exit"],
        "stdout_sha256": sb["stdout_sha256"],
        "stdout_lines": sb_lines,
        "note": "informational only - the counter owns the binding v1/v2 "
                "superblock probe; this is the oracle tool's own report",
        "probe_v1v2": sb_fields,
        "probe_v1v2_error": sb_err,
        "file_verdict": {
            "argv": file_out["argv"],
            "exit": file_out["exit"],
            "stdout": file_out["stdout"].strip(),
            "note": "file(1) applies the squashfs v4 superblock layout to "
                    "every squashfs image, so for a v1/v2 image its "
                    "'compressed'/'uncompressed' word is read from offset 20 "
                    "(inode_table_start), NOT from a compression field - the "
                    "v1/v2 superblock has none.  Do not bind the counter to "
                    "this word.",
        },
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
    tree_root, cands, reason = resolve_output_tree(oracle_root, carrier, root,
                                                   strict_tree)
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

    # (e) oracle C - 7-Zip, a THIRD producer, used as corroboration.
    # It is distinct from `unsquashfs` (squashfs-tools) and from sasquatch
    # (the unblob 26.6.4 extractor).  It does NOT replace the independent
    # oracle; it is a third reading that must agree with the other two.
    sz_members = []
    sz_header = {}
    sz_err = None
    sz_digest = None
    sz_mismatches = []
    if os.path.isfile(SEVENZIP) and os.access(SEVENZIP, os.X_OK):
        sz_members, sz_header, sz_err = sevenzip_members(image, work)
        if sz_err is None:
            sz_digest = digest_of(sz_members)
            a_by_sz = {m["path"]: m for m in regular}
            sz_by = {m["path"]: m for m in sz_members}
            for path in sorted(set(a_by_sz) | set(sz_by)):
                a = a_by_sz.get(path)
                z = sz_by.get(path)
                if a is None:
                    sz_mismatches.append({"path": path, "reason": "only in 7z"})
                elif z is None:
                    sz_mismatches.append({"path": path,
                                          "reason": "only in unsquashfs"})
                elif a["sha256"] != z["sha256"]:
                    sz_mismatches.append({"path": path,
                                          "reason": "sha256 differs",
                                          "unsquashfs": a["sha256"],
                                          "sevenzip": z["sha256"]})
            if sz_mismatches:
                raise OracleError(EXIT_FAILED,
                                  "7-Zip disagrees with unsquashfs for %r" % cid,
                                  "%d mismatch(es): %r" % (len(sz_mismatches),
                                                          sz_mismatches[:5]))
    else:
        sz_err = "7-Zip (%s) is missing or not executable" % SEVENZIP

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
        "output_tree_digest_def": TREE_DIGEST_RULE,
        "digest_rule": TREE_DIGEST_RULE,
        "sevenzip": {
            "role": "third producer, corroboration only - it does not "
                    "replace the independent oracle (unsquashfs)",
            "tool": SEVENZIP,
            "version": SEVENZIP_VER,
            "tool_sha256": sha256_file(SEVENZIP) if os.path.isfile(SEVENZIP)
                           else None,
            "command": [SEVENZIP, "x", "-tSquashFS"],
            "members": [{"path": m["path"], "size": m["size"],
                         "sha256": m["sha256"], "type": m["type"]}
                        for m in sz_members],
            "output_tree_digest": sz_digest,
            "agrees_with_unsquashfs": True if sz_err is None else None,
            "mismatches": sz_mismatches,
            "error": sz_err,
            "header": sz_header,
        },
        "output_tree": {
            "root": rel_posix(tree_root, root),
            "extract_root": rel_posix(ex_root, root),
            "extract_dir": ex_name,
            "members": [{"path": m["path"], "size": m["size"],
                         "sha256": m["sha256"], "type": m["type"]}
                        for m in b_reg],
            # `digest` and `digest_rule` are the names the R44-C1 counter's
            # `output_tree_binding()` reads first; `output_tree_digest` and
            # `output_tree_digest_def` are kept as the historical aliases.
            # Same values, so a consumer may read either pair.
            "digest": b_digest,
            "digest_rule": TREE_DIGEST_RULE,
            "output_tree_digest": b_digest,
            "output_tree_digest_def": TREE_DIGEST_RULE,
            "agrees_with_unsquashfs": True,
            "mismatches": [],
            "producer_lineage":
                "unblob 26.6.4 integration expectation (S138); produced by "
                "unblob's own squashfs handler (sasquatch 4.5.1 lineage), so "
                "it is a SECOND READING of the same bytes, not an "
                "independent producer - the independent oracle is "
                "`unsquashfs` 4.7.5",
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

    # the v1/v2 superblock probe: field offsets and the absence of a
    # compression field (the v1/v2 superblock is 32 bytes)
    sb_le = bytearray(32)
    sb_le[0:4] = b"hsqs"
    sb_le[4:8] = (4).to_bytes(4, "little")
    sb_le[8:12] = (176).to_bytes(4, "little")
    sb_le[20:24] = (71).to_bytes(4, "little")
    sb_le[24:28] = (128).to_bytes(4, "little")
    sb_le[28:30] = (1).to_bytes(2, "little")
    sb_le[30:32] = (0).to_bytes(2, "little")
    d, err = probe_v1v2_superblock(bytes(sb_le))
    if err:
        failures.append("probe_v1v2_superblock: %s" % err)
    else:
        if d["endianness"] != "le" or d["major"] != 1 or d["minor"] != 0:
            failures.append("v1/v2 probe endian/major/minor wrong: %r" % d)
        if d["bytes_used"] != 176:
            failures.append("v1/v2 bytes_used wrong: %r" % d["bytes_used"])
        if d["inode_table_start"] != 71:
            failures.append("v1/v2 inode_table_start wrong: %r"
                            % d["inode_table_start"])
        if d["directory_table_start"] != 128:
            failures.append("v1/v2 directory_table_start wrong: %r"
                            % d["directory_table_start"])
        if "compression" not in d:
            failures.append("v1/v2 probe does not report a compression field")
    if probe_v1v2_superblock(b"hsqs" + bytes(27))[0] is not None:
        failures.append("v1/v2 probe accepted a truncated superblock")
    if probe_v1v2_superblock(b"XXXX" + bytes(28))[0] is not None:
        failures.append("v1/v2 probe accepted a foreign magic")

    # scope ids must be the CARRIERS' own ids, never the TARGET_IDS spelling.
    # This is the defect the L1 caught: carriers.json says `v1le` while
    # TARGET_IDS says `v1-le`, so emitting the constant named no carrier.
    for probe_table in (
        [{"id": "v1le", "scope": "target"}, {"id": "v21le",
                                             "scope": "exploratory"}],
        [{"id": "v1-le", "scope": "target"}, {"id": "v2.1-le",
                                              "scope": "exploratory"}],
    ):
        t, e = scope_ids(probe_table)
        if t != [probe_table[0]["id"]] or e != [probe_table[1]["id"]]:
            failures.append("scope_ids did not mirror the carrier ids: %r"
                            % ((t, e),))
    # and the fallback table's own ids must round-trip through TARGET_IDS
    fallback_targets, _fallback_exploratory = scope_ids(
        [dict(c, scope="target") for c in CARRIERS])
    if fallback_targets != [c["id"] for c in CARRIERS]:
        failures.append("scope_ids lost a fallback carrier id: %r"
                        % (fallback_targets,))
    if len(fallback_targets) != len(TARGET_IDS):
        failures.append("fallback table / TARGET_IDS length mismatch: %d vs %d"
                        % (len(fallback_targets), len(TARGET_IDS)))

    report = {"cases": 24, "failures": failures}
    return (not failures), report


# ----------------------------------------------------------------- toolchain

TOOLCHAIN = (
    {
        "name": "unsquashfs",
        "path": "/usr/bin/unsquashfs",
        "version": "4.7.5",
        "version_argv": ["/usr/bin/unsquashfs", "-version"],
        "role": "THE independent oracle (squashfs-tools upstream; a different "
                "producer from sasquatch)",
    },
    {
        "name": "sasquatch",
        "path": "/home/vgpnk/.local/bin/sasquatch",
        "version": "4.5.1",
        "version_argv": ["/home/vgpnk/.local/bin/sasquatch", "-version"],
        "role": "the extractor unblob 26.6.4 drives - NOT an oracle for this "
                "claim; it is the producer the REA receipts come from",
    },
    {
        "name": "sasquatch-v4be",
        "path": "/home/vgpnk/.local/bin/sasquatch-v4be",
        "version": "4.5.1",
        "version_argv": ["/home/vgpnk/.local/bin/sasquatch-v4be", "-version"],
        "role": "the squashfs v4 big-endian sasquatch variant (same extractor "
                "family; not used by the v1/v2 carriers)",
    },
    {
        "name": "unblob",
        "path": "/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob",
        "version": "26.6.4",
        "version_argv": ["/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob",
                         "--version"],
        "role": "the extractor under REA 6.5.0; the committed __output__ trees "
                "are ITS expectation, so it is not an independent oracle",
    },
    {
        "name": "7z",
        "path": "/usr/bin/7z",
        "version": "26.04",
        "version_argv": ["/usr/bin/7z"],
        "role": "third producer, corroboration only (distinct from both "
                "unsquashfs and sasquatch)",
    },
)


def toolchain_block():
    """The toolchain paths, versions and digests, measured now.

    Every digest is the sha256 of the binary as it exists on this host at
    build time; the counter may re-derive any of them.
    """
    out = {}
    for entry in TOOLCHAIN:
        path = entry["path"]
        rec = {
            "path": path,
            "version": entry["version"],
            "role": entry["role"],
            "version_argv": entry["version_argv"],
        }
        if os.path.isfile(path):
            rec["sha256"] = sha256_file(path)
            rec["size"] = os.path.getsize(path)
            res = run(entry["version_argv"])
            rec["version_argv_exit"] = res["exit"]
            rec["version_argv_stdout_sha256"] = res["stdout_sha256"]
            first = [ln.strip() for ln in res["stdout"].splitlines()
                     if ln.strip()]
            rec["version_line"] = first[0] if first else ""
            # `unsquashfs -version` (and therefore sasquatch, which is a
            # patched unsquashfs) prints its version and then exits 1 - the
            # tools' own convention, not a failure.  Record it so the
            # counter does not read a non-zero exit as a broken toolchain.
            rec["version_argv_exit_note"] = (
                "the unsquashfs family exits 1 after printing its version; "
                "a non-zero exit here is NOT a toolchain failure"
                if res["exit"] != 0 else "clean exit")
        else:
            rec["sha256"] = None
            rec["present"] = False
        out[entry["name"]] = rec
    return out


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
    ap.add_argument("--only", action="append",
                    help="restrict to one carrier id (repeatable)")
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

    carriers_file = args.carriers
    if carriers_file is None:
        default_carriers = os.path.join(root, "tools/round-44/carriers.json")
        carriers_file = default_carriers if os.path.isfile(default_carriers) \
            else None
    try:
        carriers, carriers_src = load_carriers(carriers_file)
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
    exploratory = {}
    problems = []
    for carrier in carriers:
        try:
            built = build_carrier(carrier, root, work, args.fixtures_dir,
                                  oracle_root, tool_sha,
                                  args.oracle_root is not None)
        except OracleError as exc:
            problems.append({"carrier": carrier["id"], "reason": exc.reason,
                             "detail": exc.detail, "exit": exc.code})
            continue
        except OSError as exc:
            problems.append({"carrier": carrier["id"],
                             "reason": "filesystem error",
                             "detail": str(exc), "exit": EXIT_FAILED})
            continue
        if carrier.get("scope") == "target":
            blocks[carrier["id"]] = built
        else:
            built["scope"] = "exploratory"
            built["scope_note"] = (
                "measured and retained, but NOT a scored C1 carrier: the "
                "squashfs_v2 2.1 pair was added mid-wave and its REA probe "
                "was exploratory and unretained, so the C1 target is "
                "reverted to the four preregistered v1.0/v2.0 carriers")
            exploratory[carrier["id"]] = built

    scope_targets, scope_exploratory = scope_ids(carriers)

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
        "toolchain": toolchain_block(),
        "scope": {
            "target_ids": scope_targets,
            "target_note": "the four PREREGISTERED C1 carriers (v1.0/v2.0, "
                           "both byte orders); the scored set",
            "exploratory_ids": scope_exploratory,
            "exploratory_note": (
                "the squashfs_v2 2.1 pair: measured and retained, but "
                "UNBOUND exploratory data, NOT scored (its REA probe was "
                "exploratory and unretained, so the C1 target was reverted "
                "to the four preregistered carriers)"
                if scope_exploratory else
                "no exploratory carrier is present in this carrier file: "
                "the squashfs_v2 2.1 pair was excluded from the carrier "
                "list entirely rather than merely left unscored"),
            "id_matching": "these are the carriers' own `id` values; all id "
                           "comparisons in this tool are case- and "
                           "separator-insensitive (v1le == v1-le == V1LE), "
                           "so a consumer must not depend on the spelling",
        },
        "carriers": blocks,
        "exploratory": exploratory,
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
        merged, missing, stripped = 0, [], []
        exploratory_keys = {norm_id(e) for e in exploratory}
        for entry in entries:
            key = norm_id(entry.get("id"))
            block = blocks.get(entry.get("id"))
            if block is None:
                for cid, blk in blocks.items():
                    if norm_id(cid) == key:
                        block = blk
                        break
            if block is None:
                # an exploratory (unscored) carrier must carry NO `oracle`
                # block: it is not a scored C1 carrier.  Strip a stale one
                # left by an earlier merge rather than leaving a block the
                # counter could bind.
                if key in exploratory_keys:
                    if "oracle" in entry:
                        del entry["oracle"]
                        stripped.append(entry.get("id"))
                    continue
                missing.append(entry.get("id"))
                continue
            entry["oracle"] = block
            merged += 1
        if missing:
            sys.stderr.write("c1-oracle.py: no oracle block for %r\n"
                             % (missing,))
            return EXIT_CANNOT_EVALUATE
        # top-level `scope` and `toolchain` are written into the merge
        # target too, so the frozen file carries the target/exploratory
        # split statement and the verified tool digests.  A pre-existing
        # `superblock_layout` is left untouched (it is the counter's to own).
        if isinstance(mdoc, dict):
            mdoc["scope"] = doc["scope"]
            mdoc["toolchain"] = doc["toolchain"]
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump(mdoc, fh, indent=2, sort_keys=True)
            fh.write("\n")
        doc["merged_into"] = rel_posix(mpath, root)
        doc["merged_carriers"] = merged
        doc["merged_stripped_exploratory"] = stripped
        doc["merged_wrote_scope"] = True
        doc["merged_wrote_toolchain"] = True

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
            "exploratory": sorted(exploratory),
            "scope": doc["scope"],
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
