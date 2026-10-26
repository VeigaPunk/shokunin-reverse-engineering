#!/usr/bin/env python3
"""sqfs3-oracle.py - independent multi-producer oracle for a carved SquashFS
v1-v3 image (the round-42 C1 oracle).

Producers
  primary   backhand-cli (``unsquashfs-backhand``): ``-k <kind> -l`` for the
            path set and ``-k <kind> -d <work>/root-backhand -f`` for the tree
            (dir/symlink/regular kinds, symlink targets, regular sha256/size).
            It reads legacy-LZMA v3, which unsquashfs 4.7.5 cannot.
  second    7-Zip: ``l -tSquashFS -slt`` (path set, kind from ``Mode``,
            listing sizes) and ``x -tSquashFS`` (regular sha256/size).
  third     unsquashfs 4.7.5, used whenever it reads the image (gzip v1-v3):
            ``-lls -no-progress`` (kinds, symlink targets, device numbers) and
            ``-d <work>/root-unsquashfs -no-xattrs -f``.  It is the only
            producer that reports device major/minor, and the only one that
            can read a v1/v2 image with a vendor layout.

The primary and the 7z readings must agree on the path set, on
dir/symlink/regular kinds and on every regular relpath/sha256/size; when
unsquashfs also reads the image it must agree too, and its symlink targets are
compared against backhand's.

Outputs (round-41 formats)
  oracle.tsv      relpath TAB sha256 TAB size          (regular files)
  nonregular.tsv  relpath TAB kind TAB detail          (dir|symlink|char-device|
                                                        block-device|fifo|socket)
  oracle-run.json argv, tool versions, per-producer exit codes and counts, the
                  backhand kind used, cross-check verdict, first 20 mismatches.

Paths are bytewise-sorted, unique, relative to the image root, with no leading
``./`` and no ``squashfs-root/``.  ``detail`` is the stored symlink target, or
``major,minor`` for a character/block device, or empty for dir/fifo/socket
(backhand and 7z cannot materialise or report device numbers, so an image read
by them alone yields an empty device detail).

Exit codes
  0  the producers agree; both tables written
  2  unreadable/unsupported image, or a required producer could not complete
  3  producers disagree, or a path cannot be represented in a TAB table

Magic handling: no producer accepts the vendor magic words (hsqt, tqsh, shsq,
qshs, zlqs, sqlz).  For those the tool writes a copy in ``--work`` whose first
four bytes are the standard word for the same byte order (hsqs / sqsh) and
feeds the copy to every producer; only 4 identifier bytes change and the
normalized sha256 is recorded.

Nothing is written outside ``--work`` and the three output paths.  ``--work``
defaults to ``$TMPDIR``; with neither, the run is refused (no implicit /tmp).
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

SCHEMA = "kaidoku-r42-sqfs3-oracle-v2"

# magic word -> (byte order, standard word of that byte order)
MAGICS = {
    b"hsqs": ("little", b"hsqs"),   # squashfs 1-3 LE (also v4 LE)
    b"sqsh": ("big", b"sqsh"),      # squashfs 1-3 BE (also v4 BE)
    b"hsqt": ("little", b"hsqs"),   # DD-WRT LE
    b"tqsh": ("big", b"sqsh"),      # DD-WRT BE
    b"shsq": ("little", b"hsqs"),   # Broadcom LE
    b"qshs": ("big", b"sqsh"),      # Broadcom BE
    b"zlqs": ("little", b"hsqs"),   # non-standard LE
    b"sqlz": ("big", b"sqsh"),      # non-standard BE
}

KIND_NAMES = {
    "-": "regular",
    "d": "dir",
    "l": "symlink",
    "c": "char-device",
    "b": "block-device",
    "p": "fifo",
    "s": "socket",
}

NONREGULAR_ORDER = ("dir", "symlink", "char-device", "block-device", "fifo",
                    "socket")

# the kinds an unprivileged extraction can materialise
MATERIALISABLE = ("regular", "dir", "symlink")

# backhand's own auto-detect order, as printed by `unsquashfs-backhand -l` on a
# failed image; filtered per image by byte order / version below.
BACKHAND_KINDS = (
    "le_v4_0", "be_v4_0", "le_v3_0", "be_v3_0", "le_v3_0_lzma",
    "be_v3_0_lzma", "netgear_be_v3_0_lzma_standard", "netgear_be_v3_0_lzma",
    "le_v3_0_lzma_swap_standard", "be_v3_0_lzma_swap_standard",
    "le_v3_1_lzma_swap", "be_v3_1_lzma_swap", "avm_be_v4_0",
)

DEFAULT_BACKHAND = "/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand"

EXIT_OK, EXIT_UNREADABLE, EXIT_DISAGREE, EXIT_SELFTEST = 0, 2, 3, 1


class OracleError(Exception):
    """A condition that maps to a fixed exit code."""

    def __init__(self, code, reason, detail=""):
        super().__init__(detail or reason)
        self.code = code
        self.reason = reason
        self.detail = detail


# --------------------------------------------------------------------- helpers

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bytewise(text):
    return text.encode("utf-8", "surrogateescape")


def run(argv, env=None):
    try:
        proc = subprocess.run(argv, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=env)
    except OSError as exc:
        return {"argv": argv, "exit": 127, "stdout": "",
                "stderr": "cannot execute: %s" % exc}
    return {
        "argv": argv,
        "exit": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "surrogateescape"),
        "stderr": proc.stderr.decode("utf-8", "surrogateescape"),
    }


def tail(text, limit=2000):
    text = text or ""
    return text[-limit:]


# ------------------------------------------------------------ image inspection

def image_layout(path, offset, allow_v4=False):
    """(layout dict) for a carved image whose superblock sits at ``offset``."""
    try:
        size = os.path.getsize(path)
    except OSError as exc:
        raise OracleError(EXIT_UNREADABLE, "unreadable", str(exc))
    with open(path, "rb") as fh:
        fh.seek(offset)
        head = fh.read(32)
    if len(head) < 32:
        raise OracleError(EXIT_UNREADABLE, "truncated",
                          "fewer than 32 bytes at offset %d" % offset)
    magic = head[:4]
    if magic not in MAGICS:
        raise OracleError(EXIT_UNREADABLE, "not_squashfs",
                          "magic %r is not a SquashFS v1-v3 word (%s)"
                          % (magic, b" ".join(sorted(MAGICS)).decode()))
    endian, standard = MAGICS[magic]
    major = int.from_bytes(head[28:30], endian)
    minor = int.from_bytes(head[30:32], endian)
    if not 1 <= major <= 3 and not (allow_v4 and major == 4):
        raise OracleError(EXIT_UNREADABLE, "unsupported_version",
                          "superblock major %d at offset %d (this oracle "
                          "covers v1-v3 only)" % (major, offset))
    return {
        "magic": magic.decode("ascii"),
        "byte_order": endian,
        "standard_magic": standard.decode("ascii"),
        "version": "%d.%d" % (major, minor),
        "superblock_offset": offset,
        "image_size": size,
        "image_sha256": sha256_file(path),
    }


def normalize_magic(path, layout, work):
    """Copy the image to ``work`` with a standard magic word; return info."""
    magic = layout["magic"].encode("ascii")
    standard = layout["standard_magic"].encode("ascii")
    if magic == standard:
        return None
    dst = os.path.join(work, "normalized-magic.sqfs")
    with open(path, "rb") as src, open(dst, "wb") as out:
        src.seek(0)
        shutil.copyfileobj(src, out)
    with open(dst, "r+b") as fh:
        fh.seek(layout["superblock_offset"])
        fh.write(standard)
    return {
        "original_magic": magic.decode("ascii"),
        "normalized_magic": standard.decode("ascii"),
        "path": dst,
        "sha256": sha256_file(dst),
        "size": os.path.getsize(dst),
        "transform": "4 identifier bytes at the superblock offset only",
    }


# ------------------------------------------------------------- unsquashfs side

U_LLS = re.compile(
    r"^([-dlcbps][-rwxsStT]{9})[.+@]?\s+"     # mode
    r"(\S+)\s+"                                # user/group
    r"(\d+,\s*\d+|\d+)\s+"                     # size or "major, minor"
    r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?\s"
    r"(.*)$"                                   # path [-> target]
)


def parse_unsquashfs_listing(text):
    """(entries{rel: entry}, prefix, error). Root row establishes the prefix."""
    entries = {}
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        m = U_LLS.match(line)
        if not m:
            return None, None, "unparsed listing line %r" % line
        mode, _owner, sizefield, rest = m.groups()
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
        rows.append((kind, detail, path))
    if not rows:
        return None, None, "empty listing"
    prefix = rows[0][2]
    if not prefix.endswith("/"):
        prefix += "/"
    for kind, detail, path in rows:
        if not path.startswith(prefix) and path != prefix[:-1]:
            return None, None, ("listing row %r is not under the root prefix "
                                "%r" % (path, prefix))
        rel = path[len(prefix):] if path != prefix[:-1] else ""
        if not rel:
            continue                      # the root directory itself
        if rel in entries:
            return None, None, ("duplicate path %r in the unsquashfs listing"
                                % rel)
        entries[rel] = {"kind": kind, "detail": detail, "size": None}
    return entries, prefix, None


def parse_unsquashfs_sizes(text, entries, prefix):
    """Fill regular-file sizes from the same -lls text."""
    filled = 0
    for line in text.splitlines():
        m = U_LLS.match(line)
        if not m:
            continue
        mode, _owner, sizefield, rest = m.groups()
        if KIND_NAMES[mode[0]] != "regular" or not rest.startswith(prefix):
            continue
        rel = rest[len(prefix):]
        if rel and rel in entries:
            entries[rel]["size"] = int(sizefield)
            filled += 1
    return filled


# ---------------------------------------------------------------- backhand side

def backhand_candidates(layout, allow_v4):
    """The kinds worth trying for this superblock, in backhand's order."""
    endian = "le" if layout["byte_order"] == "little" else "be"
    major = layout["version"].split(".")[0]
    wanted = []
    if major == "4":
        if not allow_v4:
            return []
        wanted = [endian + "_v4_0"]
        if endian == "be":
            wanted.append("avm_be_v4_0")
    else:
        base = "%s_v3_0" % endian
        wanted = [base, base + "_lzma", base + "_lzma_swap_standard",
                  base + "_v3_1_lzma_swap"]
        if endian == "be":
            wanted += ["netgear_be_v3_0_lzma_standard",
                       "netgear_be_v3_0_lzma"]
    return [kind for kind in wanted if kind in BACKHAND_KINDS]


def parse_backhand_listing(text):
    """(set of rel paths, error) from ``unsquashfs-backhand -l``.

    The listing is one absolute path per line, ``/`` first; there is no kind,
    size or link target in it, so the tree after ``-d`` supplies those."""
    paths = set()
    seen_any = False
    for line in text.splitlines():
        if not line.strip():
            continue
        if not line.startswith("/"):
            return None, "unparsed backhand listing line %r" % line
        seen_any = True
        rel = line[1:]
        if not rel:
            continue                      # the root itself
        if rel.endswith("/"):
            rel = rel[:-1]
        if rel in paths:
            return None, "duplicate path %r in the backhand listing" % rel
        paths.add(rel)
    if not seen_any:
        return None, "empty backhand listing"
    return paths, None


def tree_entries(root):
    """{rel: entry} for everything an extraction actually materialised."""
    entries = {}

    def walk(directory, prefix):
        try:
            items = list(os.scandir(directory))
        except OSError:
            return
        for item in items:
            rel = prefix + item.name
            st = item.stat(follow_symlinks=False)
            mode = st.st_mode
            if stat.S_ISDIR(mode):
                entries[rel] = {"kind": "dir", "detail": "", "size": None}
                walk(item.path, rel + "/")
            elif stat.S_ISLNK(mode):
                try:
                    target = os.readlink(item.path)
                except OSError:
                    target = ""
                entries[rel] = {"kind": "symlink", "detail": target,
                                "size": None}
            elif stat.S_ISREG(mode):
                entries[rel] = {"kind": "regular", "detail": "",
                                "size": st.st_size}
            elif stat.S_ISCHR(mode):
                entries[rel] = {"kind": "char-device",
                                "detail": "%d,%d" % (os.major(st.st_rdev),
                                                     os.minor(st.st_rdev)),
                                "size": None}
            elif stat.S_ISBLK(mode):
                entries[rel] = {"kind": "block-device",
                                "detail": "%d,%d" % (os.major(st.st_rdev),
                                                     os.minor(st.st_rdev)),
                                "size": None}
            elif stat.S_ISFIFO(mode):
                entries[rel] = {"kind": "fifo", "detail": "", "size": None}
            elif stat.S_ISSOCK(mode):
                entries[rel] = {"kind": "socket", "detail": "", "size": None}

    if os.path.isdir(root):
        walk(root, "")
    return entries


# -------------------------------------------------------------------- 7z side

def parse_7z_header(text):
    """{key: value} for the archive header 7z prints before the separator."""
    head = text.split("----------", 1)[0]
    header = {}
    for line in head.splitlines():
        if " = " in line:
            key, value = line.split(" = ", 1)
            header[key.strip()] = value.strip()
    return header


def parse_7z_listing(text):
    """(entries{rel: entry}, error) from ``7z l -tSquashFS -slt`` output."""
    entries = {}
    after = text.split("----------", 1)
    if len(after) != 2:
        return None, "no entry separator in 7z listing"
    blocks, current = [], {}
    for line in after[1].splitlines():
        if not line.strip():
            if current:
                blocks.append(current)
                current = {}
            continue
        if " = " in line:
            key, value = line.split(" = ", 1)
        elif line.endswith(" ="):
            key, value = line[:-2], ""
        else:
            # trailing 7z summary ("Warnings: 1", ...) - entry section is over
            if blocks or current:
                break
            return None, "unparsed 7z listing line %r" % line
        current[key.strip()] = value
    if current:
        blocks.append(current)
    if not blocks:
        return None, "empty 7z listing"
    for block in blocks:
        if "Path" not in block:
            continue
        path = block["Path"]
        mode = block.get("Mode", "")
        if not mode:
            return None, "7z entry %r has no Mode field" % path
        kind = KIND_NAMES.get(mode[0])
        if kind is None:
            return None, "unknown 7z mode %r for %r" % (mode, path)
        if path.startswith("./"):
            return None, "7z path %r keeps a ./ prefix" % path
        if path in entries:
            return None, "duplicate path %r in the 7z listing" % path
        size = block.get("Size", "").strip()
        entries[path] = {
            "kind": kind,
            "detail": "",
            "size": int(size) if size.isdigit() else None,
        }
    if not entries:
        return None, "7z listing has no entries"
    return entries, None


# ---------------------------------------------------------------- extraction

def hash_root(root):
    """{rel: (sha256, size)} for every regular file under ``root``."""
    found = {}

    def walk(directory, prefix):
        try:
            items = list(os.scandir(directory))
        except OSError:
            return
        for item in items:
            rel = prefix + item.name
            st = item.stat(follow_symlinks=False)
            if stat.S_ISDIR(st.st_mode):
                walk(item.path, rel + "/")
            elif stat.S_ISREG(st.st_mode):
                found[rel] = (sha256_file(item.path), st.st_size)

    if os.path.isdir(root):
        walk(root, "")
    return found


def extraction_report(entries, hashes):
    """(ok, missing[list]) - every listed regular path extracted and sized."""
    missing = []
    for rel, entry in entries.items():
        if entry["kind"] != "regular":
            continue
        if rel not in hashes:
            missing.append({"path": rel, "why": "not extracted"})
        elif entry["size"] is not None and hashes[rel][1] != entry["size"]:
            missing.append({"path": rel, "why": "extracted size %d != listed %d"
                            % (hashes[rel][1], entry["size"])})
    return (not missing), missing[:20]


# ------------------------------------------------------------------ producers

def producer_unsquashfs(image, offset, work, env):
    root = os.path.join(work, "root-unsquashfs")
    listing = run(["unsquashfs", "-lls", "-no-progress"] +
                  (["-o", str(offset)] if offset else []) + [image], env=env)
    extract = run(["unsquashfs", "-d", root, "-no-xattrs", "-f",
                   "-no-progress"] +
                  (["-o", str(offset)] if offset else []) + [image], env=env)
    entries, prefix, err = parse_unsquashfs_listing(listing["stdout"])
    result = {
        "name": "unsquashfs",
        "role": "third",
        "list_prefix": prefix,
        "list_argv": listing["argv"],
        "list_exit": listing["exit"],
        "list_error": err,
        "extract_argv": extract["argv"],
        "extract_exit": extract["exit"],
        "extract_stderr_tail": tail(extract["stderr"]),
        "extract_root": root,
        "entries": entries,
        "hashes": {},
        "ok": False,
        "missing": [],
        "header": {},
    }
    if entries is None:
        return result
    parse_unsquashfs_sizes(listing["stdout"], entries, prefix)
    result["hashes"] = hash_root(root)
    result["ok"], result["missing"] = extraction_report(entries,
                                                        result["hashes"])
    return result


def producer_7z(image, work, env):
    root = os.path.join(work, "root-7z")
    listing = run(["7z", "l", "-tSquashFS", "-slt", image], env=env)
    extract = run(["7z", "x", "-tSquashFS", "-y", "-bso0", "-bsp0",
                   "-o" + root, image], env=env)
    entries, err = parse_7z_listing(listing["stdout"])
    result = {
        "name": "7z",
        "role": "second",
        "list_argv": listing["argv"],
        "list_exit": listing["exit"],
        "list_error": err,
        "extract_argv": extract["argv"],
        "extract_exit": extract["exit"],
        "extract_stderr_tail": tail(extract["stderr"]),
        "extract_root": root,
        "entries": entries,
        "hashes": {},
        "ok": False,
        "missing": [],
        "header": parse_7z_header(listing["stdout"]),
    }
    if entries is None:
        return result
    result["hashes"] = hash_root(root)
    result["ok"], result["missing"] = extraction_report(entries,
                                                        result["hashes"])
    return result


def producer_backhand(binary, image, layout, offset, work, env, allow_v4,
                      kind=None):
    """Run backhand with the first kind that lists this image."""
    result = {
        "name": "backhand",
        "role": "primary",
        "binary": binary,
        "kind": None,
        "attempts": [],
        "list_argv": None,
        "list_exit": None,
        "list_error": None,
        "extract_argv": None,
        "extract_exit": None,
        "extract_stderr_tail": "",
        "extract_root": None,
        "entries": None,
        "listed_paths": 0,
        "unmaterialised": [],
        "hashes": {},
        "ok": False,
        "missing": [],
        "header": {},
    }
    candidates = [kind] if kind else backhand_candidates(layout, allow_v4)
    chosen = None
    for candidate in candidates:
        argv = [binary, "-k", candidate, "-l"] + \
            (["-o", str(offset)] if offset else []) + [image]
        listing = run(argv, env=env)
        paths, err = (None, None)
        if listing["exit"] == 0:
            paths, err = parse_backhand_listing(listing["stdout"])
        result["attempts"].append({
            "kind": candidate,
            "list_exit": listing["exit"],
            "listed": len(paths) if paths else 0,
            "error": err or tail(listing["stderr"], 200),
        })
        if paths:
            chosen = {"kind": candidate, "paths": paths,
                      "list_argv": argv, "list_exit": listing["exit"]}
            break
    if chosen is None:
        result["list_argv"] = result["attempts"][0]["kind"] if False else None
        return result

    root = os.path.join(work, "root-backhand")
    extract = run([binary, "-k", chosen["kind"], "-d", root, "-f"] +
                  (["-o", str(offset)] if offset else []) + [image], env=env)
    entries = tree_entries(root)
    result.update({
        "kind": chosen["kind"],
        "list_argv": chosen["list_argv"],
        "list_exit": chosen["list_exit"],
        "list_error": None,
        "listed_paths": len(chosen["paths"]),
        "extract_argv": extract["argv"],
        "extract_exit": extract["exit"],
        "extract_stderr_tail": tail(extract["stderr"]),
        "extract_root": root,
    })
    # paths the listing has but the tree cannot materialise (devices, fifos,
    # sockets, or a symlink an unprivileged run refused)
    unmaterialised = sorted(chosen["paths"] - set(entries), key=bytewise)
    result["unmaterialised"] = unmaterialised[:20]
    for rel in chosen["paths"]:
        entries.setdefault(rel, {"kind": None, "detail": "", "size": None})
    result["entries"] = entries
    result["hashes"] = hash_root(root)
    ok, missing = extraction_report(entries, result["hashes"])
    result["ok"] = ok and extract["exit"] == 0
    result["missing"] = missing
    return result


# ------------------------------------------------------------------ comparison

def counts(entries):
    out = {"total": len(entries)}
    for kind in ("regular", "dir", "symlink", "char-device", "block-device",
                 "fifo", "socket"):
        out[kind] = sum(1 for e in entries.values() if e["kind"] == kind)
    if any(e["kind"] is None for e in entries.values()):
        out["unmaterialised"] = sum(1 for e in entries.values()
                                    if e["kind"] is None)
    return out


def compare_paths_sets(left, right, left_label, right_label, limit=200):
    """Path-set differences between two listings (any kind)."""
    out = []
    l_entries, r_entries = left or {}, right or {}
    for rel in sorted(set(l_entries) | set(r_entries), key=bytewise):
        in_l, in_r = rel in l_entries, rel in r_entries
        if in_l != in_r:
            which = left_label if in_l else right_label
            kind = (l_entries if in_l else r_entries)[rel]["kind"]
            out.append({"kind": "path_only", "path": rel,
                        "detail": "only %s (kind=%s)" % (which, kind)})
            if len(out) >= limit:
                break
    return out


def compare_backhand(bh, z, limit=200):
    """Primary check: backhand (listing + tree) against 7z (listing + tree)."""
    mismatches = compare_paths_sets(bh["entries"], z["entries"],
                                    "backhand", "7z", limit)
    if len(mismatches) >= limit:
        return mismatches
    b_entries = bh["entries"] or {}
    z_entries = z["entries"] or {}
    for rel in sorted(set(b_entries) & set(z_entries), key=bytewise):
        be, ze = b_entries[rel], z_entries[rel]
        bk = be["kind"]
        if bk is None:
            # the tree could not materialise it; only a kind a tree must carry
            # is a failure here
            if ze["kind"] in MATERIALISABLE:
                mismatches.append({
                    "kind": "kind_missing", "path": rel,
                    "detail": "7z says %s, backhand did not materialise it"
                    % ze["kind"]})
            continue
        if bk != ze["kind"]:
            mismatches.append({"kind": "kind_mismatch", "path": rel,
                               "detail": "backhand=%s 7z=%s"
                               % (bk, ze["kind"])})
            continue
        if bk != "regular":
            continue
        for label, entry, hashes in (("backhand", be, bh["hashes"]),
                                     ("7z", ze, z["hashes"])):
            if rel not in hashes:
                mismatches.append({"kind": "sha_missing", "path": rel,
                                   "detail": "%s did not extract it" % label})
            elif entry["size"] is not None and \
                    hashes[rel][1] != entry["size"]:
                mismatches.append({"kind": "size_mismatch", "path": rel,
                                   "detail": "%s listed=%d extracted=%d"
                                   % (label, entry["size"],
                                      hashes[rel][1])})
        if rel in bh["hashes"] and rel in z["hashes"]:
            lb, lz = bh["hashes"][rel], z["hashes"][rel]
            if lb[0] != lz[0] or lb[1] != lz[1]:
                mismatches.append({
                    "kind": "sha_mismatch", "path": rel,
                    "detail": "backhand=%s/%d 7z=%s/%d"
                    % (lb[0][:16], lb[1], lz[0][:16], lz[1])})
        if len(mismatches) >= limit:
            break
    return mismatches


def compare_unsquashfs(u, z, limit=200):
    """Third check: unsquashfs against 7z, including device kinds."""
    mismatches = compare_paths_sets(u["entries"], z["entries"],
                                    "unsquashfs", "7z", limit)
    if len(mismatches) >= limit:
        return mismatches
    u_entries = u["entries"] or {}
    z_entries = z["entries"] or {}
    for rel in sorted(set(u_entries) & set(z_entries), key=bytewise):
        ue, ze = u_entries[rel], z_entries[rel]
        if ue["kind"] != ze["kind"]:
            mismatches.append({"kind": "kind_mismatch", "path": rel,
                               "detail": "unsquashfs=%s 7z=%s"
                               % (ue["kind"], ze["kind"])})
            continue
        if ue["kind"] != "regular":
            continue
        for label, entry, hashes in (("unsquashfs", ue, u["hashes"]),
                                     ("7z", ze, z["hashes"])):
            if rel not in hashes:
                mismatches.append({"kind": "sha_missing", "path": rel,
                                   "detail": "%s did not extract it" % label})
            elif entry["size"] is not None and \
                    hashes[rel][1] != entry["size"]:
                mismatches.append({"kind": "size_mismatch", "path": rel,
                                   "detail": "%s listed=%d extracted=%d"
                                   % (label, entry["size"],
                                      hashes[rel][1])})
        if rel in u["hashes"] and rel in z["hashes"]:
            lu, lz = u["hashes"][rel], z["hashes"][rel]
            if lu[0] != lz[0] or lu[1] != lz[1]:
                mismatches.append({
                    "kind": "sha_mismatch", "path": rel,
                    "detail": "unsquashfs=%s/%d 7z=%s/%d"
                    % (lu[0][:16], lu[1], lz[0][:16], lz[1])})
        if len(mismatches) >= limit:
            break
    return mismatches


def compare_details(left, right, limit=200):
    """Symlink targets: backhand's readlink against unsquashfs's -lls."""
    mismatches = []
    l_entries = left["entries"] or {}
    r_entries = right["entries"] or {}
    for rel in sorted(set(l_entries) & set(r_entries), key=bytewise):
        le, re_ = l_entries[rel], r_entries[rel]
        if le["kind"] != "symlink" or re_["kind"] != "symlink":
            continue
        if le["detail"] and re_["detail"] and le["detail"] != re_["detail"]:
            mismatches.append({"kind": "detail_mismatch", "path": rel,
                               "detail": "backhand target %r unsquashfs %r"
                               % (le["detail"], re_["detail"])})
            if len(mismatches) >= limit:
                break
    return mismatches


def unrepresentable(entries):
    """[rel, ...] paths a TAB/newline table cannot carry faithfully."""
    return [rel for rel in entries if "\t" in rel or "\n" in rel
            or "\r" in rel]


# --------------------------------------------------------------------- tables

def write_tables(files_path, nonregular_path, entries, hashes):
    regular, nonregular = [], []
    for rel, entry in entries.items():
        if entry["kind"] == "regular":
            sha, size = hashes[rel]
            regular.append((rel, sha, str(size)))
        elif entry["kind"] in NONREGULAR_ORDER:
            nonregular.append((rel, entry["kind"], entry["detail"] or ""))
    regular.sort(key=lambda row: bytewise(row[0]))
    nonregular.sort(key=lambda row: bytewise(row[0]))
    with open(files_path, "wb") as fh:
        for row in regular:
            fh.write(("\t".join(row) + "\n").encode("utf-8",
                                                    "surrogateescape"))
    with open(nonregular_path, "wb") as fh:
        for row in nonregular:
            fh.write(("\t".join(row) + "\n").encode("utf-8",
                                                    "surrogateescape"))
    return len(regular), len(nonregular)


def tool_versions(backhand_binary):
    info = {"python": sys.version.split()[0]}
    path = shutil.which("unsquashfs")
    info["unsquashfs"] = {"path": path}
    if path:
        listing = run([path, "-version"])
        info["unsquashfs"]["version_line"] = \
            (listing["stdout"].splitlines() or [""])[0].strip()
        info["unsquashfs"]["sha256"] = sha256_file(os.path.realpath(path))
    path = shutil.which("7z")
    info["7z"] = {"path": path}
    if path:
        listing = run([path, "i"])
        version = ""
        squashfs = False
        signature_line = ""
        for line in listing["stdout"].splitlines():
            if re.match(r"^7-Zip\b", line):
                version = line.strip()
            if re.search(r"\bSquashFS\b", line):
                squashfs = True
                signature_line = line.strip()
        info["7z"]["version_line"] = version
        info["7z"]["squashfs_format_listed"] = squashfs
        info["7z"]["squashfs_signature_line"] = signature_line
        info["7z"]["sha256"] = sha256_file(os.path.realpath(path))
    info["backhand"] = {"path": backhand_binary}
    if backhand_binary and os.path.exists(backhand_binary):
        version = run([backhand_binary, "--version"])
        info["backhand"]["version_line"] = \
            (version["stdout"].splitlines() or [""])[0].strip()
        listing = run([backhand_binary, "--help"])
        info["backhand"]["sha256"] = sha256_file(os.path.realpath(
            backhand_binary))
        info["backhand"]["kinds"] = [k for k in BACKHAND_KINDS
                                     if k in listing["stdout"]]
    return info


# ---------------------------------------------------------------------- driver

def pick_backhand(explicit):
    if explicit:
        return explicit if os.path.exists(explicit) else None
    env = os.environ.get("UNSQUASHFS_BACKHAND")
    if env and os.path.exists(env):
        return env
    if os.path.exists(DEFAULT_BACKHAND):
        return DEFAULT_BACKHAND
    found = shutil.which("unsquashfs-backhand")
    return found or None


def oracle(image, offset, work, files_path, nonregular_path, json_path,
           normalize=True, probe=False, allow_v4=False, backhand_binary=None,
           backhand_kind=None):
    report = {
        "schema": SCHEMA,
        "input": {"path": os.path.abspath(image),
                  "sha256": None, "size_bytes": None},
        "offsets": {"superblock": offset},
        "layout": None,
        "magic_normalization": None,
        "tools": None,
        "producers": {},
        "counts": {},
        "cross_check": None,
        "tables": {"files": None, "nonregular": None},
        "probe": probe,
        "dev_allow_v4": allow_v4,
        "exit": None,
        "reason": None,
    }
    env = dict(os.environ, LC_ALL="C.UTF-8")

    def dump(code, reason):
        report["exit"] = code
        report["reason"] = reason
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, sort_keys=False,
                      ensure_ascii=True)
            fh.write("\n")
        return code

    try:
        layout = image_layout(image, offset, allow_v4)
    except OracleError as exc:
        report["detail"] = exc.detail
        return dump(exc.code, exc.reason)
    report["layout"] = layout
    report["input"]["sha256"] = layout["image_sha256"]
    report["input"]["size_bytes"] = layout["image_size"]
    report["tools"] = tool_versions(backhand_binary)

    target = image
    if normalize:
        norm = normalize_magic(image, layout, work)
        if norm is not None:
            report["magic_normalization"] = norm
            target = norm["path"]

    have_7z = shutil.which("7z") is not None
    if not have_7z:
        return dump(EXIT_UNREADABLE, "producer_missing:7z")

    bh = None
    if backhand_binary:
        bh = producer_backhand(backhand_binary, target, layout, offset, work,
                               env, allow_v4, backhand_kind)
    z = producer_7z(target, work, env)
    u = producer_unsquashfs(target, offset, work, env) if have_7z else None

    for result in (bh, z, u):
        if result is None:
            continue
        report["producers"][result["name"]] = {
            "role": result["role"],
            "list_argv": result["list_argv"],
            "list_exit": result["list_exit"],
            "list_error": result["list_error"],
            "extract_argv": result["extract_argv"],
            "extract_exit": result["extract_exit"],
            "extract_stderr_tail": result["extract_stderr_tail"],
            "extract_root": result["extract_root"],
            "complete": result["ok"],
            "missing_regular": result["missing"],
            "counts": counts(result["entries"]) if result["entries"] else None,
            "header": result.get("header") or {},
        }
        if result["name"] == "backhand":
            report["producers"]["backhand"].update({
                "kind": result["kind"],
                "attempts": result["attempts"],
                "listed_paths": result["listed_paths"],
                "unmaterialised": result["unmaterialised"],
            })

    # ---- the compressor statement (a v1-v3 superblock has none)
    zheader = z.get("header") or {}
    method = zheader.get("Method", "")
    if method:
        compression = {
            "method": method,
            "method_tokens": method.split(),
            "file_system": zheader.get("File System", ""),
            "source": "7z l -tSquashFS -slt archive header (Method field)",
            "measured_on": ("the magic-normalized copy (4 identifier bytes "
                            "differ)" if report["magic_normalization"]
                            else "the input bytes"),
        }
        if report["magic_normalization"]:
            native = run(["7z", "l", "-tSquashFS", "-slt", image], env=env)
            native_header = parse_7z_header(native["stdout"])
            native_method = native_header.get("Method", "")
            compression["native"] = {
                "accepted": bool(native["exit"] == 0 and native_method),
                "method": native_method,
                "file_system": native_header.get("File System", ""),
                "measured_on": "the input bytes",
                "differs": bool(native_method and native_method != method),
            }
        report["compression"] = compression

    # ---- which producer pair carries the verdict
    primary = bh if (bh is not None and bh["entries"]) else u
    if primary is None or not primary["entries"]:
        return dump(EXIT_UNREADABLE, "no_primary_producer")
    if not z["entries"]:
        report["producers"]["7z"]["list_error"] = z["list_error"]
        return dump(EXIT_UNREADABLE, "producer_incomplete:7z")

    if primary["name"] == "backhand":
        mismatches = compare_backhand(bh, z)
        pair = "backhand+7z"
    else:
        mismatches = compare_unsquashfs(u, z)
        pair = "unsquashfs+7z"
    third = []
    details = []
    if primary["name"] == "backhand" and u is not None and u["entries"]:
        third = compare_unsquashfs(u, z)
        details = compare_details(bh, u)

    all_mismatches = mismatches + third + details
    report["cross_check"] = {
        "pair": pair,
        "third_producer": ("unsquashfs" if primary["name"] == "backhand" and
                           u is not None and u["entries"] else None),
        "detail_source": ("unsquashfs" if u is not None and u["entries"]
                          else "backhand (tree)"),
        "detail_limits": ("backhand and 7z expose no device numbers; 7z -slt "
                          "exposes no symlink target and 7z x refuses relative "
                          "'..' targets (zero-byte placeholder)"),
        "verdict": "disagree" if all_mismatches else "agree",
        "mismatch_count": len(all_mismatches),
        "first_20": all_mismatches[:20],
        "mismatches_truncated": len(all_mismatches) > 20,
        "pair_mismatches": len(mismatches),
        "third_mismatches": len(third),
        "detail_mismatches": len(details),
    }
    report["counts"] = {}
    for result in (bh, z, u):
        if result is not None and result["entries"]:
            report["counts"][result["name"]] = counts(result["entries"])

    bad_paths = sorted(set(unrepresentable(primary["entries"] or {}))
                       | set(unrepresentable(z["entries"] or {})),
                       key=bytewise)
    if bad_paths:
        report["cross_check"]["unrepresentable_paths"] = bad_paths[:20]
        return dump(EXIT_DISAGREE, "path_not_representable")
    incomplete = [r["name"] for r in (bh, z)
                  if r is not None and not r["ok"]]
    if probe:
        report["tables"] = {"files": None, "nonregular": None}
        return dump(EXIT_OK, "probe_only")
    if incomplete:
        return dump(EXIT_UNREADABLE,
                    "producer_incomplete:%s" % ",".join(incomplete))
    if all_mismatches:
        return dump(EXIT_DISAGREE, "producer_disagreement")

    # table source: regular content from the primary, details from unsquashfs
    # when it read the image, else from the backhand tree
    entries = dict(primary["entries"])
    if primary["name"] == "backhand":
        for rel, entry in entries.items():
            if entry["kind"] is None and rel in z["entries"]:
                entries[rel] = dict(z["entries"][rel])
        if u is not None and u["entries"]:
            for rel, entry in entries.items():
                ue = u["entries"].get(rel)
                if ue is not None and ue["kind"] == entry["kind"]:
                    if ue["detail"]:
                        entry["detail"] = ue["detail"]
    n_files, n_nonregular = write_tables(files_path, nonregular_path,
                                         entries, primary["hashes"])
    report["tables"] = {
        "files": files_path, "regular_rows": n_files,
        "nonregular": nonregular_path, "nonregular_rows": n_nonregular,
    }
    if n_files == 0:
        report["warnings"] = [
            "no regular files: oracle.tsv is empty and the round-41 parser "
            "rejects an empty oracle table, so this image cannot be a carrier",
        ]
    return dump(EXIT_OK, None)


# -------------------------------------------------------------------- selftest

SELFTEST_UNSQUASHFS_OK = """\
drwxrwxrwx a/a             41 2024-01-01 00:00 squashfs-root
-rw-r--r-- a/a              6 2024-01-01 00:00 squashfs-root/apple.txt
lrwxrwxrwx a/a              9 2024-01-01 00:00 squashfs-root/link -> apple.txt
drwxr-xr-x a/a             20 2024-01-01 00:00 squashfs-root/bin
crw-r--r-- a/a         31,  0 2024-01-01 00:00 squashfs-root/node
"""

SELFTEST_7Z_OK = """\
Listing archive: x

--
Type = SquashFS
File System = SquashFS 3.0
Method = ZLIB
Physical Size = 4096
----------
Path = apple.txt
Folder = -
Size = 6
Mode = -rw-r--r--

Path = bin
Folder = +
Size = 
Mode = drwxr-xr-x

Path = link
Folder = -
Size = 9
Mode = lrwxrwxrwx

Path = node
Folder = -
Size = 0
Mode = crw-r--r--
"""

SELFTEST_BACKHAND_OK = """\
/
/apple.txt
/bin
/link
/node
"""


def selftest(work):
    failures = []

    def check(name, condition, note=""):
        print("%s %s%s" % ("PASS" if condition else "FAIL", name,
                           "" if condition else "  (%s)" % note))
        if not condition:
            failures.append(name)

    # magic table
    expected = {b"hsqs": ("little", b"hsqs"), b"sqsh": ("big", b"sqsh"),
                b"hsqt": ("little", b"hsqs"), b"tqsh": ("big", b"sqsh"),
                b"shsq": ("little", b"hsqs"), b"qshs": ("big", b"sqsh"),
                b"zlqs": ("little", b"hsqs"), b"sqlz": ("big", b"sqsh")}
    check("magic_table", MAGICS == expected, repr(MAGICS))

    # kinds open to backhand per superblock
    layout_le = {"byte_order": "little", "version": "3.0"}
    layout_be = {"byte_order": "big", "version": "3.1"}
    check("backhand_candidates_le",
          backhand_candidates(layout_le, False)[:2] == ["le_v3_0",
                                                        "le_v3_0_lzma"],
          repr(backhand_candidates(layout_le, False)))
    check("backhand_candidates_be",
          backhand_candidates(layout_be, False)[:2] == ["be_v3_0",
                                                        "be_v3_0_lzma"],
          repr(backhand_candidates(layout_be, False)))
    check("backhand_no_v4_without_override",
          backhand_candidates({"byte_order": "little", "version": "4.0"},
                              False) == [], "v4 leaked through")
    check("backhand_v4_with_override",
          backhand_candidates({"byte_order": "little", "version": "4.0"},
                              True) == ["le_v4_0"], "v4 override broken")

    # listings
    u_entries, u_prefix, u_err = parse_unsquashfs_listing(
        SELFTEST_UNSQUASHFS_OK)
    sizes_filled = parse_unsquashfs_sizes(SELFTEST_UNSQUASHFS_OK, u_entries,
                                          u_prefix)
    z_entries, z_err = parse_7z_listing(SELFTEST_7Z_OK)
    bh_paths, bh_err = parse_backhand_listing(SELFTEST_BACKHAND_OK)
    check("parse_unsquashfs", u_entries is not None, str(u_err))
    check("parse_7z", z_entries is not None, str(z_err))
    check("parse_backhand", bh_paths == {"apple.txt", "bin", "link", "node"},
          str(bh_err))
    header = parse_7z_header(SELFTEST_7Z_OK)
    check("green_7z_header",
          header.get("Method") == "ZLIB"
          and header.get("File System") == "SquashFS 3.0",
          repr(header))
    check("green_sizes_filled", sizes_filled == 1, repr(sizes_filled))

    # backhand tree -> entries
    root = os.path.join(work, "bh-tree")
    os.makedirs(os.path.join(root, "bin"), exist_ok=True)
    with open(os.path.join(root, "apple.txt"), "w") as fh:
        fh.write("apple\n")
    os.symlink("apple.txt", os.path.join(root, "link"))
    b_entries = tree_entries(root)
    check("green_backhand_tree_kinds",
          b_entries.get("apple.txt", {}).get("kind") == "regular"
          and b_entries.get("bin", {}).get("kind") == "dir"
          and b_entries.get("link", {}).get("kind") == "symlink",
          repr(sorted(b_entries)))
    check("green_backhand_readlink",
          b_entries.get("link", {}).get("detail") == "apple.txt",
          repr(b_entries.get("link")))

    if u_entries and z_entries and bh_paths:
        # primary pair agrees
        b_full = {}
        for rel in bh_paths:
            b_full[rel] = dict(z_entries[rel]) if rel in z_entries else \
                {"kind": None, "detail": "", "size": None}
        b_full["apple.txt"]["kind"] = "regular"
        b_full["bin"]["kind"] = "dir"
        b_full["link"]["kind"] = "symlink"
        b_full["link"]["detail"] = "apple.txt"
        b_full["node"]["kind"] = None            # unmaterialisable device
        bh = {"entries": b_full, "hashes": {"apple.txt": ("a" * 64, 6)}}
        z = {"entries": z_entries, "hashes": {"apple.txt": ("a" * 64, 6)}}
        mismatches = compare_backhand(bh, z)
        check("green_primary_agree", mismatches == [], repr(mismatches))

        # a device the tree cannot materialise is not a disagreement, but a
        # kind a tree must carry is
        b_bad = {"entries": dict(b_full), "hashes": bh["hashes"]}
        b_bad["entries"]["bin"] = {"kind": None, "detail": "", "size": None}
        mismatches = compare_backhand(b_bad, z)
        check("red_kind_missing",
              any(m["kind"] == "kind_missing" for m in mismatches),
              repr(mismatches))

        # red: same relpath, different content
        z_red = {"entries": z_entries, "hashes": {"apple.txt": ("b" * 64, 6)}}
        mismatches = compare_backhand(bh, z_red)
        check("red_disagreement_exit3",
              any(m["kind"] == "sha_mismatch" for m in mismatches)
              and len(mismatches) == 1, repr(mismatches))

        # red: size disagreement
        z_size = {"entries": {k: dict(v) for k, v in z_entries.items()},
                  "hashes": {"apple.txt": ("a" * 64, 6)}}
        z_size["entries"]["apple.txt"]["size"] = 7
        mismatches = compare_backhand(bh, z_size)
        check("red_size_exit3",
              any(m["kind"] == "size_mismatch" for m in mismatches),
              repr(mismatches))

        # red: kind disagreement
        z_kind = {"entries": {k: dict(v) for k, v in z_entries.items()},
                  "hashes": {"apple.txt": ("a" * 64, 6)}}
        z_kind["entries"]["link"]["kind"] = "regular"
        mismatches = compare_backhand(bh, z_kind)
        check("red_kind_exit3",
              any(m["kind"] == "kind_mismatch" for m in mismatches),
              repr(mismatches))

        # red: path present in only one producer
        z_short = {"entries": {k: dict(v) for k, v in z_entries.items()
                               if k != "bin"},
                   "hashes": {"apple.txt": ("a" * 64, 6)}}
        mismatches = compare_backhand(bh, z_short)
        check("red_path_only_exit3",
              any(m["kind"] == "path_only" for m in mismatches),
              repr(mismatches))

        # third producer + details
        u = {"entries": u_entries, "hashes": {"apple.txt": ("a" * 64, 6)}}
        check("green_third_agree", compare_unsquashfs(u, z) == [],
              repr(compare_unsquashfs(u, z)))
        u_bad = {"entries": {k: dict(v) for k, v in u_entries.items()},
                 "hashes": {"apple.txt": ("a" * 64, 6)}}
        u_bad["entries"]["link"]["detail"] = "other.txt"
        check("red_detail_mismatch",
              any(m["kind"] == "detail_mismatch"
                  for m in compare_details(bh, u_bad)),
              repr(compare_details(bh, u_bad)))

    # red: duplicate paths in either listing
    dup = SELFTEST_UNSQUASHFS_OK + \
        "-rw-r--r-- a/a              6 2024-01-01 00:00 squashfs-root/apple.txt\n"
    entries, _prefix, err = parse_unsquashfs_listing(dup)
    check("red_duplicate_path", entries is None and "duplicate" in str(err),
          str(err))
    dup7z = SELFTEST_7Z_OK + "\nPath = apple.txt\nFolder = -\nSize = 6\nMode = -rw-r--r--\n"
    entries, err = parse_7z_listing(dup7z)
    check("red_duplicate_path_7z", entries is None and "duplicate" in str(err),
          str(err))
    dupbh = SELFTEST_BACKHAND_OK + "/apple.txt\n"
    paths, err = parse_backhand_listing(dupbh)
    check("red_duplicate_path_backhand",
          paths is None and "duplicate" in str(err), str(err))

    # red: unreadable image (no magic, then a v4 image)
    junk = os.path.join(work, "junk.bin")
    with open(junk, "wb") as fh:
        fh.write(b"\0" * 64)
    try:
        image_layout(junk, 0)
        check("red_unreadable", False, "no exception")
    except OracleError as exc:
        check("red_unreadable", exc.code == EXIT_UNREADABLE,
              "%d %s" % (exc.code, exc.reason))
    v4 = os.path.join(work, "v4.bin")
    with open(v4, "wb") as fh:
        fh.write(b"hsqs" + b"\0" * 24 + b"\x04\x00\x00\x00")
    try:
        image_layout(v4, 0)
        check("red_unsupported_version", False, "no exception")
    except OracleError as exc:
        check("red_unsupported_version",
              exc.code == EXIT_UNREADABLE and exc.reason ==
              "unsupported_version", "%d %s" % (exc.code, exc.reason))

    # magic normalization produces a standard word and leaves the body alone
    ddwrt = os.path.join(work, "ddwrt.bin")
    body = b"\0" * 24 + b"\x03\x00\x01\x00" + b"\xa5" * 16
    with open(ddwrt, "wb") as fh:
        fh.write(b"hsqt" + body)
    layout = image_layout(ddwrt, 0)
    norm = normalize_magic(ddwrt, layout, work)
    with open(norm["path"], "rb") as fh:
        patched = fh.read()
    check("green_magic_normalization",
          patched[:4] == b"hsqs" and patched[4:] == body
          and layout["byte_order"] == "little", repr(patched[:8]))

    # red: a path a TAB table cannot carry
    tabby = {"a\tb.txt": {"kind": "regular", "detail": "", "size": 1}}
    check("red_unrepresentable_path",
          unrepresentable(tabby) == ["a\tb.txt"], repr(unrepresentable(tabby)))
    check("green_representable_path",
          unrepresentable({"a b.txt": {"kind": "regular", "detail": "",
                                       "size": 1}}) == [], "space broke it")

    # a table write round-trips and is bytewise sorted + unique
    tables = os.path.join(work, "selftest-tables")
    os.makedirs(tables, exist_ok=True)
    entries = {"b.txt": {"kind": "regular", "detail": "", "size": 1},
               "A.txt": {"kind": "regular", "detail": "", "size": 1},
               "d": {"kind": "dir", "detail": "", "size": None}}
    hashes = {"b.txt": ("1" * 64, 1), "A.txt": ("2" * 64, 1)}
    n_files, n_nonregular = write_tables(os.path.join(tables, "o.tsv"),
                                         os.path.join(tables, "n.tsv"),
                                         entries, hashes)
    with open(os.path.join(tables, "o.tsv"), "rb") as fh:
        rows = [line.split(b"\t")[0] for line in fh.read().splitlines()]
    check("green_table_order", rows == [b"A.txt", b"b.txt"], repr(rows))
    check("green_table_counts", (n_files, n_nonregular) == (2, 1),
          "%r" % ((n_files, n_nonregular),))

    print("\n%d failure(s)" % len(failures))
    return EXIT_OK if not failures else EXIT_SELFTEST


# ------------------------------------------------------------------------ main

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="sqfs3-oracle.py",
        description="Independent multi-producer oracle for a carved SquashFS "
                    "v1-v3 image: backhand-cli (primary) and 7-Zip (second) "
                    "must agree, unsquashfs 4.x is a third producer wherever "
                    "it can read the image. Writes oracle.tsv, nonregular.tsv "
                    "and oracle-run.json.")
    parser.add_argument("image", nargs="?", help="carved SquashFS v1-v3 image")
    parser.add_argument("--work", help="scratch directory for the extraction "
                                       "roots (default: $TMPDIR)")
    parser.add_argument("--files", help="oracle.tsv output path")
    parser.add_argument("--nonregular", help="nonregular.tsv output path")
    parser.add_argument("--json", help="oracle-run.json output path")
    parser.add_argument("--out", help="directory for the three outputs when "
                                      "--files/--nonregular/--json are not "
                                      "given")
    parser.add_argument("--offset", type=int, default=0,
                        help="superblock offset inside the image (default 0)")
    parser.add_argument("--backhand", help="unsquashfs-backhand binary "
                                           "(default: $UNSQUASHFS_BACKHAND, "
                                           "else the L1 build path, else PATH)")
    parser.add_argument("--backhand-kind", help="force a backhand kind instead "
                                                "of probing")
    parser.add_argument("--no-normalize-magic", action="store_true",
                        help="do not patch a vendor magic word into the "
                             "standard hsqs/sqsh copy the producers read")
    parser.add_argument("--dev-allow-v4", action="store_true",
                        help="development only: let a v4 superblock through so "
                             "the listing parsers can be exercised on a real "
                             "tree (never part of the C1 contract)")
    parser.add_argument("--probe", action="store_true",
                        help="diagnostics only: run the producers, write "
                             "--json, write no tables, exit 0 when the primary "
                             "pair read the image")
    parser.add_argument("--keep-work", action="store_true",
                        help="keep a --work directory this tool created")
    parser.add_argument("--selftest", action="store_true",
                        help="run the inline red/green fixture tests")
    args = parser.parse_args(argv)

    # Scratch policy: honour --work, else $TMPDIR.  No implicit /tmp: a run
    # with neither is refused so every extraction root is named by the caller.
    tmpdir = os.environ.get("TMPDIR")
    if not (tmpdir and os.path.isdir(tmpdir)):
        tmpdir = None
    if tmpdir is None and not args.work and not args.selftest:
        print("sqfs3-oracle: set TMPDIR or pass --work (no implicit /tmp)",
              file=sys.stderr)
        return EXIT_UNREADABLE

    if args.selftest:
        work = args.work or tempfile.mkdtemp(prefix="sqfs3-oracle-selftest.",
                                             dir=tmpdir)
        os.makedirs(work, exist_ok=True)
        created = args.work is None
        try:
            return selftest(work)
        finally:
            if created and not args.keep_work:
                shutil.rmtree(work, ignore_errors=True)

    if not args.image:
        parser.error("an image is required (or use --selftest)")
    if not os.path.isfile(args.image):
        print("sqfs3-oracle: %s is not a file" % args.image, file=sys.stderr)
        return EXIT_UNREADABLE

    work = args.work
    created_work = False
    if not work:
        work = tempfile.mkdtemp(prefix="sqfs3-oracle.", dir=tmpdir)
        created_work = True
    os.makedirs(work, exist_ok=True)

    out_dir = args.out or os.getcwd()
    files_path = args.files or os.path.join(out_dir, "oracle.tsv")
    nonregular_path = args.nonregular or os.path.join(out_dir,
                                                      "nonregular.tsv")
    json_path = args.json or os.path.join(out_dir, "oracle-run.json")
    for path in (files_path, nonregular_path, json_path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    backhand_binary = pick_backhand(args.backhand)
    try:
        try:
            code = oracle(args.image, args.offset, work, files_path,
                          nonregular_path, json_path,
                          normalize=not args.no_normalize_magic,
                          probe=args.probe,
                          allow_v4=args.dev_allow_v4,
                          backhand_binary=backhand_binary,
                          backhand_kind=args.backhand_kind)
        except OracleError as exc:
            print("sqfs3-oracle: %s: %s" % (exc.reason, exc.detail),
                  file=sys.stderr)
            code = exc.code
    finally:
        if created_work and not args.keep_work:
            shutil.rmtree(work, ignore_errors=True)
    if code != EXIT_OK:
        print("sqfs3-oracle: exit %d (%s)" % (code, json_path),
              file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
