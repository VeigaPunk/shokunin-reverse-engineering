#!/usr/bin/env python3
"""symlink-order-probe.py -- is unblob's symlink-removal set derivable from the
image, or does it depend on `fix_extracted_directory`'s directory iteration
order?

Transcribes unblob 26.6.4 `extractor.fix_symlink` / `extractor.fix_permission` /
`file_utils.is_safe_path` verbatim (only the report sink differs) and applies it
to a directory tree that a plain `sasquatch-v4be -d` extraction produced, under
three iteration orders.  Nothing here writes outside the given tree, and the
tree must be a fresh copy per order.

Usage: symlink-order-probe.py TREE --order natural|sorted|reverse
Exit 0 always (this is a probe); the JSON is the result.
"""

import argparse
import errno
import json
import os
import sys
from pathlib import Path

FILE_PERMISSION_MASK = 0o644
DIR_PERMISSION_MASK = 0o775


def is_safe_path(basedir, path):
    try:
        basedir.joinpath(path).resolve().relative_to(basedir.resolve())
    except ValueError:
        return False
    return True


def is_recursive_link(path):
    try:
        path.resolve()
    except RuntimeError:
        return True
    return False


def fix_symlink(path, outdir, removed):
    if is_recursive_link(path):
        removed.append({'link': path.as_posix(), 'reason': 'recursive'})
        path.unlink()
        return
    raw_target = os.readlink(path)
    if not raw_target:
        removed.append({'link': path.as_posix(), 'reason': 'empty-target',
                        'silent': True})
        path.unlink()
        return
    target = Path(raw_target)
    if target.is_absolute():
        target = Path(target.as_posix().lstrip('/'))
    else:
        target = path.resolve()
    if not is_safe_path(outdir, target):
        removed.append({'link': path.as_posix(), 'reason': 'unsafe',
                        'resolved': target.as_posix()})
        path.unlink()
    else:
        relative_target = os.path.relpath(outdir.joinpath(target), start=path.parent)
        path.unlink()
        path.symlink_to(relative_target)


def fix_extracted_directory(directory, outdir, removed, order):
    if not directory.exists():
        return
    names = os.listdir(directory)
    if order == 'sorted':
        names = sorted(names)
    elif order == 'reverse':
        names = sorted(names, reverse=True)
    for name in names:
        path = directory / name
        try:
            if path.is_symlink():
                fix_symlink(path, outdir, removed)
                continue
            if path.is_dir():
                fix_extracted_directory(path, outdir, removed, order)
        except OSError as e:
            if e.errno == errno.ENAMETOOLONG:
                continue
            raise


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('tree')
    ap.add_argument('--order', choices=('natural', 'sorted', 'reverse'),
                    default='natural')
    args = ap.parse_args(argv)
    root = Path(args.tree).resolve()
    removed = []
    fix_extracted_directory(root, root, removed, args.order)
    out = {'tree': str(root), 'order': args.order,
           'removed': len(removed),
           'links': sorted(r['link'][len(str(root)) + 1:] for r in removed),
           'records': removed}
    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
