#!/usr/bin/env python3
"""compare.py -- compare the round-40 oracle TSVs against an extraction tree.

Usage:
  compare.py --files ORACLE_FILES.tsv --nonregular ORACLE_NONREG.tsv \
             --extract DIR [--sasquatch-log LOG] [--json OUT.json]

The oracle TSVs are the ones written by sqfs-list.py (round 40):

  files      relpath TAB sha256 TAB size
  nonregular relpath TAB kind TAB detail

The extraction tree is the direct output of sasquatch / sasquatch-v4be
(no unblob, no REA).  Every regular file is compared by content and size, every
directory by presence, every symlink by its target, and every device/fifo/
socket by its kind and (devices) major:minor.  Device nodes that the extractor
could not create as a non-superuser are accepted only when the extractor log
names them (``could not create character device ...``).

Exit 0 if the manifests are equal, 1 otherwise, 2 on a malformed input.
"""

import argparse
import hashlib
import json
import os
import re
import stat
import sys


def sha256_file(path):
    h = hashlib.sha256()
    size = 0
    with open(path, 'rb') as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def read_oracle_files(path):
    files = {}
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line:
                continue
            rel, sha, size = line.split('\t')
            files[rel] = (sha, int(size))
    return files


def read_oracle_nonregular(path):
    rows = {}
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line:
                continue
            rel, kind, detail = line.split('\t')
            rows[rel] = (kind, detail)
    return rows


def manifest(root):
    files, nonregular = {}, {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir != '.':
            nonregular[rel_dir] = ('dir', '')
            dirnames[:] = dirnames  # keep deterministic ordering
        for name in dirnames + filenames:
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, root)
            if rel_dir == '.' and rel == '.':
                continue
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                nonregular[rel] = ('symlink', os.readlink(p))
            elif stat.S_ISREG(st.st_mode):
                files[rel] = sha256_file(p)
            elif stat.S_ISCHR(st.st_mode):
                nonregular[rel] = ('char-device',
                                   '%d:%d' % (os.major(st.st_rdev),
                                              os.minor(st.st_rdev)))
            elif stat.S_ISBLK(st.st_mode):
                nonregular[rel] = ('block-device',
                                   '%d:%d' % (os.major(st.st_rdev),
                                              os.minor(st.st_rdev)))
            elif stat.S_ISFIFO(st.st_mode):
                nonregular[rel] = ('fifo', '')
            elif stat.S_ISSOCK(st.st_mode):
                nonregular[rel] = ('socket', '')
            elif stat.S_ISDIR(st.st_mode):
                nonregular[rel] = ('dir', '')
            else:
                nonregular[rel] = ('unknown', '')
    return files, nonregular


def sasquatch_device_log(path, root):
    """Paths the extractor reported it could not create as a non-superuser."""
    found = set()
    if not path:
        return found
    pat = re.compile(r'could not create (?:character|block) device (\S+),')
    base = os.path.abspath(root)
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh:
            m = pat.search(line)
            if not m:
                continue
            p = m.group(1)
            ap = os.path.abspath(p)
            if ap.startswith(base + os.sep):
                found.add(os.path.relpath(ap, base))
            else:
                found.add(p)
    return found


def diff_sets(want, got, limit=25):
    only_want = sorted(set(want) - set(got))[:limit]
    only_got = sorted(set(got) - set(want))[:limit]
    return only_want, only_got


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', required=True)
    ap.add_argument('--nonregular', required=True)
    ap.add_argument('--extract', required=True)
    ap.add_argument('--sasquatch-log')
    ap.add_argument('--json')
    args = ap.parse_args(argv)

    want_files = read_oracle_files(args.files)
    want_non = read_oracle_nonregular(args.nonregular)
    got_files, got_non = manifest(args.extract)
    logged = sasquatch_device_log(args.sasquatch_log, args.extract)

    mismatches = []
    for rel in sorted(set(want_files) & set(got_files)):
        if want_files[rel] != got_files[rel]:
            mismatches.append({'kind': 'file-content', 'path': rel,
                               'oracle': list(want_files[rel]),
                               'extract': list(got_files[rel])})
    missing_files, extra_files = diff_sets(want_files, got_files)

    specials_verified = []
    nonregular_missing = {}
    for rel, (kind, detail) in want_non.items():
        got = got_non.get(rel)
        if got == (kind, detail):
            continue
        if kind in ('char-device', 'block-device', 'fifo', 'socket') \
                and rel in logged:
            specials_verified.append(rel)
            continue
        nonregular_missing[rel] = {'oracle': [kind, detail],
                                   'extract': list(got) if got else None}
    nonregular_extra = {rel: list(v) for rel, v in got_non.items()
                        if rel not in want_non}

    ok = not (mismatches or missing_files or extra_files
              or nonregular_missing or nonregular_extra)
    result = {
        'verdict': 'match' if ok else 'mismatch',
        'counts': {
            'regular_files_oracle': len(want_files),
            'regular_files_extract': len(got_files),
            'nonregular_oracle': len(want_non),
            'nonregular_extract': len(got_non),
            'special_files_verified_by_extractor_log': len(specials_verified),
        },
        'file_content_mismatches': mismatches[:25],
        'files_only_in_oracle': missing_files,
        'files_only_in_extract': extra_files,
        'nonregular_mismatches': dict(list(nonregular_missing.items())[:25]),
        'nonregular_only_in_oracle': sorted(set(want_non) - set(got_non)
                                           - set(specials_verified))[:25],
        'nonregular_only_in_extract': dict(list(nonregular_extra.items())[:25]),
        'specials_verified_by_extractor_log': specials_verified,
    }
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as fh:
            json.dump(result, fh, indent=1, sort_keys=True)
            fh.write('\n')
    print(json.dumps({k: result[k] for k in ('verdict', 'counts')},
                     sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
