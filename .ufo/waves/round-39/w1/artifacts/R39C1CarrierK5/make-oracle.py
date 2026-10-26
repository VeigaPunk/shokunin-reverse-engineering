#!/usr/bin/env python3
"""Write the frozen-oracle tables for carrier K5 from its source tree.

Usage: make-oracle.py SRC OUTDIR

OUTDIR/oracle.tsv     TAB-separated: relative path, sha256, size  (regular files, sorted)
OUTDIR/symlinks.tsv   TAB-separated: relative path, link target, in-tree|escaping

Resolution rule (POSIX path join against the link's own directory inside the image
root): the link's directory is taken as a stack of path components and the target is
applied component by component -- "" and "." are skipped, ".." pops.  A ".." that pops
an empty stack is an escape, i.e. the target resolves above the image root; such a
link is `escaping`.  Anything else is `in-tree`.  This is the lexical form of the
realpath test unblob 26.6.4 applies (unblob/extractor.py fix_symlink + is_safe_path):
a relative target whose realpath leaves the extraction root is removed as a
MaliciousSymlinkRemoved; the extraction root has real parents, so a lexical pop past
the image root is exactly what leaves it.

Sorting is by the UTF-8 bytes of the relative path.
"""
import hashlib
import os
import posixpath
import sys


def resolve(link_rel, target):
    """Return (resolved_posix_path, in_tree)."""
    if target.startswith("/"):
        raise SystemExit(f"absolute symlink not allowed: {link_rel} -> {target}")
    stack = [c for c in posixpath.dirname(link_rel).split("/") if c not in ("", ".")]
    escaped = False
    for comp in target.split("/"):
        if comp in ("", "."):
            continue
        if comp == "..":
            if not stack:
                escaped = True
            else:
                stack.pop()
        else:
            stack.append(comp)
    return "/" + "/".join(stack), not escaped


def walk(src):
    files, links, dirs = [], [], []
    for root, dnames, fnames in os.walk(src):
        dnames.sort()
        fnames.sort()
        rel_dir = os.path.relpath(root, src)
        dirs.append("" if rel_dir == "." else rel_dir.replace(os.sep, "/"))
        for fn in fnames:
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, src).replace(os.sep, "/")
            (links if os.path.islink(p) else files).append((rel, p))
    return files, links, dirs


def main(argv):
    if len(argv) != 3:
        sys.exit(f"usage: {argv[0]} SRC OUTDIR")
    src, outdir = argv[1], argv[2]
    files, links, dirs = walk(src)
    files.sort(key=lambda x: x[0].encode())
    links.sort(key=lambda x: x[0].encode())

    oracle_rows = []
    for rel, p in files:
        data = open(p, "rb").read()
        oracle_rows.append((rel, hashlib.sha256(data).hexdigest(), len(data)))

    link_rows = []
    for rel, p in links:
        target = os.readlink(p)
        resolved, in_tree = resolve(rel, target)
        link_rows.append((rel, target, "in-tree" if in_tree else "escaping", resolved))

    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "oracle.tsv"), "w", encoding="utf-8", newline="") as f:
        for rel, digest, size in oracle_rows:
            f.write(f"{rel}\t{digest}\t{size}\n")
    with open(os.path.join(outdir, "symlinks.tsv"), "w", encoding="utf-8", newline="") as f:
        for rel, target, kind, _ in link_rows:
            f.write(f"{rel}\t{target}\t{kind}\n")

    # Constraint report (R39-C1 carrier requirements).
    empty_dirs = [d for d in dirs if d and
                  not any(f[0].startswith(d + "/") for f in files + links)]
    big = [r for r, _, n in oracle_rows if n > 3 * 4096]
    print(f"regular_files={len(oracle_rows)} symlinks={len(link_rows)} dirs={len(dirs)}")
    print(f"zero_byte={sum(1 for _, _, n in oracle_rows if n == 0)}")
    print(f"gt_3_blocks={[r for r in big]}")
    print(f"space_name={[r for r, _, n in oracle_rows if ' ' in r]}")
    print(f"non_ascii_name={[r for r, _, n in oracle_rows if not r.isascii()]}")
    print(f"dir_depth_max={max(d.count('/') for d in dirs if d)}")
    for rel, target, kind, resolved in link_rows:
        print(f"link {rel} -> {target} [{kind}] resolved={resolved}")
    print(f"empty_dirs={empty_dirs}")
    print(f"in_tree_links={sum(1 for r in link_rows if r[2] == 'in-tree')} "
          f"escaping_links={sum(1 for r in link_rows if r[2] == 'escaping')}")


if __name__ == "__main__":
    main(sys.argv)
