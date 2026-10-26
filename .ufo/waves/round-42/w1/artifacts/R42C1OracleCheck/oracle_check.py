#!/usr/bin/env python3
"""oracle_check.py -- R42C1OracleCheck harness.

Compares three SquashFS readers on one image, file-for-file:
  * unsquashfs 4.7.5 (external, reference)
  * 7-Zip 7z 26.04 (external)
  * sasquatch 4.5.1 (the extractor unblob runs; cross-check only)

Per image it produces:
  * JSON snapshot per reader: regular files (rel -> sha256+size),
    symlinks (rel -> target), directories, devices, fifos, sockets,
    empty files, hard-link groups (same content, via inode when visible)
  * JSON pairwise agreement verdicts (unsq vs 7z, unsq vs sasq, 7z vs sasq)
  * raw outputs saved for evidence (listing logs)

Usage: oracle_check.py --work DIR image...
"""
import argparse
import hashlib
import json
import os
import re
import stat
import shutil
import subprocess
import sys
import tempfile

TOOLS = {
    'unsquashfs': 'unsquashfs',
    '7z': '7z',
    'sasquatch': 'sasquatch',
}


def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def norm_rel(p):
    """Normalize a listing path to the canonical relative form (no ./,
    no leading /, no trailing slash)."""
    p = p.replace('\\', '/')
    parts = [c for c in p.split('/') if c not in ('', '.')]
    return '/'.join(parts)


# ------------------------------------------------------------------ unsquashfs

def unsq_superblock(path):
    rc, out, err = run([TOOLS['unsquashfs'], '-s', path])
    return rc, out, err


UNSQ_TYPE_RE = re.compile(r'^([bcdlps-])[rwxst-]{9}')


def unsq_list(path):
    """Parse `unsquashfs -lls`. Returns list of dicts."""
    rc, out, err = run([TOOLS['unsquashfs'], '-lls', path])
    entries = []
    for line in out.splitlines():
        if not line.strip():
            continue
        m = UNSQ_TYPE_RE.match(line)
        if not m:
            continue
        typ = m.group(1)
        rest = line[10:].strip()
        # rest: owner/group size date name [-> target]
        parts = rest.split(None, 4)
        if len(parts) < 5:
            continue
        owner, size, date, time_, name = parts
        link = None
        if ' -> ' in name:
            name, target = name.split(' -> ', 1)
            link = target
        try:
            size_i = int(size)
        except ValueError:
            size_i = -1   # device line (major,minor) or non-numeric
        parts_n = name.split('/')
        if parts_n and parts_n[0] == 'squashfs-root':
            name = '/'.join(parts_n[1:])
        entries.append({'type': typ, 'size': size_i, 'date': date,
                        'name': name, 'link': link, 'raw': line})
    return rc, entries, err


def unsq_extract(path, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    rc, out, err = run([TOOLS['unsquashfs'], '-no-progress', '-d', dest, path])
    return rc, out, err


# ------------------------------------------------------------------ 7-Zip

def _parse_7z_list(out):
    """Parse `7z l -slt`? We use default listing table; fall back to -slt."""
    entries = []
    lines = out.splitlines()
    in_table = False
    hyp = '-------------------'
    for line in lines:
        if line.startswith(hyp):
            in_table = not in_table
            continue
        if not in_table:
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        date, time, attr, size, comp = parts[:5]
        name = ' '.join(parts[5:])
        entries.append({'date': date, 'time': time, 'attr': attr,
                        'size': int(size) if size.isdigit() else -1,
                        'compressed': comp, 'name': name})
    return entries


def sevenz_list_parse(path):
    """Parse `7z l -slt` (structured listing)."""
    rc, out, err = run([TOOLS['7z'], 'l', '-slt', path])
    entries = []
    cur = {}
    for line in out.splitlines():
        if line.startswith('Path = '):
            if cur:
                entries.append(cur)
            cur = {'path': line[len('Path = '):].strip()}
        else:
            for key in ('Folder', 'Size', 'Packed Size', 'Modified', 'Mode',
                        'User ID', 'Group ID', 'CRC', 'Method'):
                if line.startswith(key + ' = '):
                    cur[key.lower().replace(' ', '_')] = line[len(key) + 3:].strip()
                    break
            if line.startswith('Attributes = '):
                cur['attributes'] = line[len('Attributes = '):].strip()
    if cur:
        entries.append(cur)
    return rc, entries, err

def backhand_list(path, kind=None):
    cmd = [TOOLS['backhand'], '-l']
    if kind:
        cmd += ['-k', kind]
    cmd.append(path)
    rc, out, err = run(cmd)
    paths = []
    for line in out.splitlines():
        line = line.strip()
        if not line or line.startswith('squashfs-root'):
            continue
        paths.append(norm_rel(line))
    return rc, paths, err


def backhand_extract(path, dest, kind=None):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    cmd = [TOOLS['backhand'], '-d', dest]
    if kind:
        cmd += ['-k', kind]
    cmd.append(path)
    rc, out, err = run(cmd)
    return rc, out, err


def sasq_extract(path, dest, endian=None):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    cmd = [TOOLS['sasquatch'], '-dest', dest, '-no-progress']
    if endian:
        cmd.append(endian)
    cmd.append(path)
    rc, out, err = run(cmd)
    return rc, out, err


# ------------------------------------------------------------------ snapshot tree

def snapshot_tree(root):
    """Walk an extracted tree; entries keyed by normalized rel path."""
    files = {}      # rel -> {'sha256':..,'size':..,'hardlink':inode}
    symlinks = {}   # rel -> target
    dirs = set()
    devices = {}    # rel -> (kind, major, minor)
    fifos = set()
    sockets = set()
    empty = set()
    seen_inode = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for d in dirnames:
            full = os.path.join(dirpath, d)
            dirs.add(norm_rel(os.path.relpath(full, root)))
        for f in filenames:
            full = os.path.join(dirpath, f)
            rel = norm_rel(os.path.relpath(full, root))
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                symlinks[rel] = os.readlink(full)
            elif stat.S_ISREG(st.st_mode):
                size = st.st_size
                files[rel] = {'sha256': sha256_file(full), 'size': size,
                               'inode': st.st_ino}
                if size == 0:
                    empty.add(rel)
                seen_inode.setdefault(st.st_ino, []).append(rel)
            elif stat.S_ISCHR(st.st_mode) or stat.S_ISBLK(st.st_mode):
                kind = 'char-device' if stat.S_ISCHR(st.st_mode) else 'block-device'
                devices[rel] = (kind, os.major(st.st_rdev), os.minor(st.st_rdev))
            elif stat.S_ISFIFO(st.st_mode):
                fifos.add(rel)
            elif stat.S_ISSOCK(st.st_mode):
                sockets.add(rel)
    hardlinks = {}
    for ino, rels in seen_inode.items():
        if len(rels) > 1:
            hardlinks[ino] = rels
    return {'files': files, 'symlinks': symlinks, 'dirs': sorted(dirs),
            'devices': devices, 'fifos': sorted(fifos),
            'sockets': sorted(sockets), 'empty': sorted(empty),
            'hardlinks': {str(k): v for k, v in hardlinks.items()}}


# ------------------------------------------------------------------ listing -> model

def model_from_unsq(entries):
    files, symlinks, dirs, devices = {}, {}, set(), {}
    empties = set()
    for e in entries:
        rel = norm_rel(e['name'])
        t = e['type']
        if t == 'd':
            dirs.add(rel)
        elif t == 'l':
            symlinks[rel] = e['link']
        elif t == '-':
            files[rel] = {'size': e['size']}
            if e['size'] == 0:
                empties.add(rel)
        elif t in ('b', 'c'):
            # device line format: owner size major,minor date name? parse from raw
            devices[rel] = e['raw']
        else:
            pass
    return {'files': files, 'symlinks': symlinks, 'dirs': sorted(dirs),
            'devices': devices, 'empty': sorted(empties)}


def model_from_7z(entries):
    files, symlinks, dirs, devices = {}, {}, set(), {}
    empties = set()
    for e in entries:
        rel = norm_rel(e.get('path', ''))
        if not rel:
            continue
        mode = e.get('mode', '')
        if not mode:
            continue   # archive header pseudo-entry (Path = <archive>)
        typ = mode[0] if mode else ''
        if typ == 'd':
            dirs.add(rel)
            continue
        if typ == 'l':
            symlinks[rel] = '?target-not-in-slt'
            continue
        if typ in ('b', 'c', 'p', 's'):
            devices[rel] = (typ, e.get('size', ''))
            continue
        try:
            size = int(e.get('size', '0'))
        except ValueError:
            size = -1
        files[rel] = {'size': size}
        if size == 0:
            empties.add(rel)
    return {'files': files, 'symlinks': symlinks, 'dirs': sorted(dirs),
            'devices': devices, 'empty': sorted(empties)}
# ------------------------------------------------------------------ sasquatch

def sasq_list(path, endian=None):
    cmd = [TOOLS['sasquatch'], '-lls']
    if endian:
        cmd.append(endian)
    cmd.append(path)
    rc, out, err = run(cmd)
    entries = []
    for line in out.splitlines():
        m = UNSQ_TYPE_RE.match(line)
        if not m:
            continue
        typ = m.group(1)
        rest = line[10:].strip()
        parts = rest.split(None, 4)
        if len(parts) < 5:
            continue
        owner, size, date, time_, name = parts
        link = None
        if ' -> ' in name:
            name, target = name.split(' -> ', 1)
            link = target
        # sasquatch prints paths under a `squashfs-root` root component
        parts_n = name.split('/')
        if parts_n and parts_n[0] == 'squashfs-root':
            name = '/'.join(parts_n[1:])
        try:
            size_i = int(size)
        except ValueError:
            size_i = -1   # device line (major,minor) or non-numeric
        entries.append({'type': typ, 'size': size_i, 'date': date,
                        'name': name, 'link': link, 'raw': line})
    return rc, entries, err


def sasq_extract(path, dest, endian=None):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    cmd = [TOOLS['sasquatch'], '-dest', dest, '-no-progress']
    if endian:
        cmd.append(endian)
    cmd.append(path)
    rc, out, err = run(cmd)
    return rc, out, err


# ------------------------------------------------------------------ snapshot tree

def snapshot_tree(root):
    """Walk an extracted tree; entries keyed by normalized rel path."""
    files = {}      # rel -> {'sha256':..,'size':..,'hardlink':inode}
    symlinks = {}   # rel -> target
    dirs = set()
    devices = {}    # rel -> (kind, major, minor)
    fifos = set()
    sockets = set()
    empty = set()
    seen_inode = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for d in dirnames:
            full = os.path.join(dirpath, d)
            dirs.add(norm_rel(os.path.relpath(full, root)))
        for f in filenames:
            full = os.path.join(dirpath, f)
            rel = norm_rel(os.path.relpath(full, root))
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                symlinks[rel] = os.readlink(full)
            elif stat.S_ISREG(st.st_mode):
                size = st.st_size
                files[rel] = {'sha256': sha256_file(full), 'size': size,
                               'inode': st.st_ino}
                if size == 0:
                    empty.add(rel)
                seen_inode.setdefault(st.st_ino, []).append(rel)
            elif stat.S_ISCHR(st.st_mode) or stat.S_ISBLK(st.st_mode):
                kind = 'char-device' if stat.S_ISCHR(st.st_mode) else 'block-device'
                devices[rel] = (kind, os.major(st.st_rdev), os.minor(st.st_rdev))
            elif stat.S_ISFIFO(st.st_mode):
                fifos.add(rel)
            elif stat.S_ISSOCK(st.st_mode):
                sockets.add(rel)
    hardlinks = {}
    for ino, rels in seen_inode.items():
        if len(rels) > 1:
            hardlinks[ino] = rels
    return {'files': files, 'symlinks': symlinks, 'dirs': sorted(dirs),
            'devices': devices, 'fifos': sorted(fifos),
            'sockets': sorted(sockets), 'empty': sorted(empty),
            'hardlinks': {str(k): v for k, v in hardlinks.items()}}


# ------------------------------------------------------------------ listing -> model

def model_from_unsq(entries):
    files, symlinks, dirs, devices = {}, {}, set(), {}
    empties = set()
    for e in entries:
        rel = norm_rel(e['name'])
        t = e['type']
        if t == 'd':
            dirs.add(rel)
        elif t == 'l':
            symlinks[rel] = e['link']
        elif t == '-':
            files[rel] = {'size': e['size']}
            if e['size'] == 0:
                empties.add(rel)
        elif t in ('b', 'c'):
            # device line format: owner size major,minor date name? parse from raw
            devices[rel] = e['raw']
        else:
            pass
    return {'files': files, 'symlinks': symlinks, 'dirs': sorted(dirs),
            'devices': devices, 'empty': sorted(empties)}


def model_from_7z(entries):
    files, symlinks, dirs, devices = {}, {}, set(), {}
    empties = set()
    for e in entries:
        rel = norm_rel(e.get('path', ''))
        if not rel:
            continue
        mode = e.get('mode', '')
        if not mode:
            continue   # archive header pseudo-entry (Path = <archive>)
        typ = mode[0] if mode else ''
        if typ == 'd':
            dirs.add(rel)
            continue
        if typ == 'l':
            symlinks[rel] = '?target-not-in-slt'
            continue
        if typ in ('b', 'c', 'p', 's'):
            devices[rel] = (typ, e.get('size', ''))
            continue
        try:
            size = int(e.get('size', '0'))
        except ValueError:
            size = -1
        files[rel] = {'size': size}
        if size == 0:
            empties.add(rel)
    return {'files': files, 'symlinks': symlinks, 'dirs': sorted(dirs),
            'devices': devices, 'empty': sorted(empties)}


# ------------------------------------------------------------------ compare

def compare_models(a, b, label):
    """Agreement between two reader models. Returns verdict dict."""
    res = {'pair': label}
    af, bf = a['files'], b['files']
    res['regular_paths_equal'] = set(af) == set(bf)
    res['regular_count'] = (len(af), len(bf))
    missing = sorted(set(af) - set(bf))
    extra = sorted(set(bf) - set(af))
    res['missing'] = missing
    res['extra'] = extra
    size_mismatch = sorted(r for r in set(af) & set(bf)
                           if af[r].get('size') != bf[r].get('size'))
    res['size_mismatch'] = size_mismatch
    res['symlinks_equal'] = a['symlinks'] == b['symlinks']
    res['symlink_only_a'] = sorted(set(a['symlinks']) - set(b['symlinks']))
    res['symlink_only_b'] = sorted(set(b['symlinks']) - set(a['symlinks']))
    res['symlink_target_diff'] = sorted(r for r in set(a['symlinks']) & set(b['symlinks'])
                                        if a['symlinks'][r] != b['symlinks'][r])
    res['dirs_equal'] = set(a['dirs']) == set(b['dirs'])
    res['empty_equal'] = set(a['empty']) == set(b['empty'])
    return res


def content_compare(a, b, label):
    """Byte-level comparison of extracted trees for regular files."""
    res = {'pair': label, 'sha_mismatch': [], 'sha_missing': [], 'sha_extra': []}
    af, bf = a['files'], b['files']
    for r in set(af) & set(bf):
        if 'sha256' in af[r] and 'sha256' in bf[r]:
            if af[r]['sha256'] != bf[r]['sha256']:
                res['sha_mismatch'].append((r, af[r]['sha256'], bf[r]['sha256']))
        elif 'sha256' not in af[r] or 'sha256' not in bf[r]:
            res['sha_mismatch'].append((r, 'no-content', 'no-content'))
    res['sha_missing'] = sorted(r for r in set(af) - set(bf))
    res['sha_extra'] = sorted(r for r in set(bf) - set(af))
    return res


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('images', nargs='+')
    a = ap.parse_args(argv)
    os.makedirs(a.work, exist_ok=True)
    report = {}
    for img in a.images:
        base = os.path.basename(img)
        d = os.path.join(a.work, base)
        os.makedirs(d, exist_ok=True)
        entry = {'image': os.path.abspath(img)}
        # 1. superblocks
        rc, out, err = unsq_superblock(img)
        entry['unsq_superblock'] = {'rc': rc, 'out': out, 'err': err[-2000:]}
        # 2. unsquashfs listing
        rc, lst, err = unsq_list(img)
        entry['unsq_list'] = {'rc': rc, 'count': len(lst), 'err': err[-2000:]}
        with open(os.path.join(d, 'unsq_list.txt'), 'w') as f:
            for e in lst:
                f.write(e['raw'] + '\n')
        m_u = model_from_unsq(lst)
        entry['unsq_model'] = {k: v for k, v in m_u.items() if k != 'files'}
        # 3. unsquashfs extract
        ud = os.path.join(d, 'unsq_tree')
        rc, out, err = unsq_extract(img, ud)
        entry['unsq_extract'] = {'rc': rc, 'err': err[-2000:]}
        t_u = snapshot_tree(ud)
        entry['unsq_tree'] = {k: v for k, v in t_u.items() if k != 'files'}
        # 4. 7z listing
        rc, lst7, err = sevenz_list_parse(img)
        entry['7z_list'] = {'rc': rc, 'count': len(lst7), 'err': err[-2000:]}
        with open(os.path.join(d, '7z_list.txt'), 'w') as f:
            for e in lst7:
                f.write(json.dumps(e) + '\n')
        m7 = model_from_7z(lst7)
        entry['7z_model'] = {k: v for k, v in m7.items() if k != 'files'}
        # 5. 7z extract
        z7 = os.path.join(d, '7z_tree')
        rc, out, err = sevenz_extract(img, z7)
        entry['7z_extract'] = {'rc': rc, 'err': err[-2000:]}
        t7 = snapshot_tree(z7)
        entry['7z_tree'] = {k: v for k, v in t7.items() if k != 'files'}
        # 6. sasquatch listing + extract (auto endian; also try -be/-le)
        rc, lsts, err = sasq_list(img)
        entry['sasq_list'] = {'rc': rc, 'count': len(lsts), 'err': err[-2000:]}
        with open(os.path.join(d, 'sasq_list.txt'), 'w') as f:
            for e in lsts:
                f.write(e['raw'] + '\n')
        ms = model_from_unsq(lsts)
        entry['sasq_model'] = {k: v for k, v in ms.items() if k != 'files'}
        sd = os.path.join(d, 'sasq_tree')
        rc, out, err = sasq_extract(img, sd)
        entry['sasq_extract'] = {'rc': rc, 'err': err[-2000:]}
        ts = snapshot_tree(sd)
        entry['sasq_tree'] = {k: v for k, v in ts.items() if k != 'files'}
        # 7. pairwise agreements
        entry['agree_unsq_7z'] = compare_models(m_u, m7, 'unsq-vs-7z')
        entry['agree_unsq_sasq'] = compare_models(m_u, ms, 'unsq-vs-sasq')
        entry['agree_7z_sasq'] = compare_models(m7, ms, '7z-vs-sasq')
        entry['content_unsq_7z'] = content_compare(t_u, t7, 'unsq-vs-7z')
        entry['content_unsq_sasq'] = content_compare(t_u, ts, 'unsq-vs-sasq')
        entry['content_7z_sasq'] = content_compare(t7, ts, '7z-vs-sasq')
        # basic verdict
        ok = (entry['agree_unsq_7z']['regular_paths_equal']
              and not entry['agree_unsq_7z']['size_mismatch']
              and entry['agree_unsq_7z']['symlinks_equal']
              and not entry['content_unsq_7z']['sha_mismatch'])
        entry['unsq_7z_agree'] = ok
        with open(os.path.join(d, 'result.json'), 'w') as f:
            json.dump(entry, f, indent=1, sort_keys=True)
        report[base] = {'unsq_7z_agree': ok,
                         'unsq_7z': entry['agree_unsq_7z'],
                         'content_unsq_7z': entry['content_unsq_7z'],
                         'unsq_sasq': entry['agree_unsq_sasq'],
                         'content_unsq_sasq': entry['content_unsq_sasq'],
                         '7z_sasq': entry['agree_7z_sasq'],
                         'content_7z_sasq': entry['content_7z_sasq'],
                         'counts': {'unsq': len(m_u['files']),
                                    '7z': len(m7['files']),
                                    'sasq': len(ms['files'])}}
    summary = os.path.join(a.work, 'summary.json')
    with open(summary, 'w') as f:
        json.dump(report, f, indent=1, sort_keys=True)
    print(json.dumps(report, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
