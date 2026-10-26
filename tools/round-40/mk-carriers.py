#!/usr/bin/env python3
"""Emit the R40-C1 carrier manifest (.ufo/waves/round-40/c1/carriers.json).

Each carrier is (id, carrier, oracle, nonregular): the carrier is a genuine
AVM-layout big-endian SquashFS v4 image (BE superblock/inode fields, `sqsh`
magic, AVM marker mkfs_time == bytes_used, little-endian metadata block-length
headers); `oracle` is the independent reader's regular-file table
(relpath TAB sha256 TAB size); `nonregular` is the reader's non-regular table
(relpath TAB kind TAB detail). Both tables come from `c1-run.sh oracle`.

The manifest pins sha256 for the carrier and both tables, so the counter can
read git objects at the measured revision and compare byte-for-byte. The
marker is enforced here; with the default `--layout-check reader` the frozen
reader re-reads each carrier under `--layout avm` and must reproduce the
supplied oracle and nonregular rows exactly, so a marker-only standard-BE body
(the round-39 `--endian avm` artefact) cannot enter the manifest even if its
receipt is later relabelled.

Usage:
  mk-carriers.py --root LANE --spec tuples.tsv [--out MANIFEST]
  mk-carriers.py --root LANE V1 CARRIER ORACLE NONREGULAR [V2 ...]

  tuples.tsv lines: id<TAB>carrier<TAB>oracle<TAB>nonregular
  (carrier/oracle/nonregular paths are relative to --root or absolute inside it)

By default the manifest must hold exactly the frozen R40-C1 ids V1,V2,L1,L2 (the
counter enforces that set); --allow-any-ids exists for development manifests.

Exit: 0 ok, 2 input/validation error, 3 cannot write the manifest.
Python 3.9+ stdlib only; temp dirs honour TMPDIR (never hardcoded /tmp).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ID_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,15}$')
HEX64_RE = re.compile(r'^[0-9a-f]{64}$')
KINDS = {'dir', 'symlink', 'char-device', 'block-device', 'fifo', 'socket'}
MAGIC = {'be': b'sqsh', 'le': b'hsqs'}
DEVICE_RE = re.compile(r'^[0-9]+:[0-9]+$')
CLAIM = 'R40-C1'
SCHEMA = 'kaidoku-r40-c1-carriers-v1'
RECEIPT_TMPL = 'corpus/evidence/round-40/c1/{id}/after.json'
DEFAULT_OUT = '.ufo/waves/round-40/c1/carriers.json'


class Bad(Exception):
    pass


def real_under(root, path, what):
    """Resolve `path` (relative to root or absolute) and require it inside root."""
    p = path if os.path.isabs(path) else os.path.join(root, path)
    real = os.path.realpath(p)
    base = os.path.realpath(root)
    if real != base and not real.startswith(base + os.sep):
        raise Bad('%s resolves outside --root: %s' % (what, path))
    if not os.path.isfile(real):
        raise Bad('%s is not a regular file: %s' % (what, path))
    return real


def rel_to(root, real):
    rel = os.path.relpath(real, os.path.realpath(root)).replace(os.sep, '/')
    if rel == '..' or rel.startswith('../') or os.path.isabs(rel):
        raise Bad('path is not inside --root: %s' % real)
    return rel


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def bad_rel(rel, what, line):
    if not rel or rel.startswith('/') or rel.endswith('/'):
        raise Bad('%s:%d: relative path not normalised: %r' % (what, line, rel))
    if '\\' in rel:
        raise Bad('%s:%d: backslash in relative path: %r' % (what, line, rel))


def parse_oracle(path):
    rows, keys = [], []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            if not line:
                continue
            fields = line.split('\t')
            if len(fields) != 3:
                raise Bad('%s:%d: want 3 tab-separated fields '
                          '(relpath, sha256, size), got %d' % (path, n, len(fields)))
            rel, digest, size = fields
            bad_rel(rel, path, n)
            if not HEX64_RE.match(digest):
                raise Bad('%s:%d: sha256 is not 64 lowercase hex: %r' % (path, n, digest))
            if not size.isdigit():
                raise Bad('%s:%d: size is not a non-negative integer: %r' % (path, n, size))
            keys.append(rel.encode('utf-8', 'surrogateescape'))
            rows.append({'path': rel, 'sha256': digest, 'size': int(size)})
    if not rows:
        raise Bad('%s: no oracle rows' % path)
    if keys != sorted(keys) or len(set(keys)) != len(keys):
        raise Bad('%s: oracle relpaths are not bytewise-sorted and unique' % path)
    return rows


def parse_nonregular(path):
    rows, keys, kinds = [], [], {}
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            if not line:
                continue
            fields = line.split('\t')
            if len(fields) != 3:
                raise Bad('%s:%d: want 3 tab-separated fields '
                          '(relpath, kind, detail), got %d' % (path, n, len(fields)))
            rel, kind, detail = fields
            bad_rel(rel, path, n)
            if kind not in KINDS:
                raise Bad('%s:%d: kind %r not in %s'
                          % (path, n, kind, '|'.join(sorted(KINDS))))
            if kind == 'symlink':
                if not detail:
                    raise Bad('%s:%d: symlink %r has an empty target' % (path, n, rel))
            elif kind in ('char-device', 'block-device'):
                if not DEVICE_RE.match(detail):
                    raise Bad('%s:%d: device %r detail is not decimal major:minor'
                              % (path, n, rel))
            elif detail:
                raise Bad('%s:%d: %s %r carries a detail: %r' % (path, n, kind, rel, detail))
            keys.append(rel.encode('utf-8', 'surrogateescape'))
            kinds[kind] = kinds.get(kind, 0) + 1
            rows.append({'path': rel, 'kind': kind, 'detail': detail})
    if keys != sorted(keys) or len(set(keys)) != len(keys):
        raise Bad('%s: nonregular relpaths are not bytewise-sorted and unique' % path)
    return rows, kinds


def superblock(path):
    raw = open(path, 'rb').read(48)
    magic = raw[:4]
    if magic not in (b'sqsh', b'hsqs'):
        raise Bad('carrier does not start with a squashfs magic: %r' % magic)
    e = '>' if magic == b'sqsh' else '<'
    if len(raw) < 48:
        raise Bad('carrier is shorter than the 48-byte superblock')
    mkfs = int.from_bytes(raw[8:12], 'big' if e == '>' else 'little')
    used = int.from_bytes(raw[40:48], 'big' if e == '>' else 'little')
    return {'magic': magic.decode('ascii'), 'byte_order': 'big' if e == '>' else 'little',
            'mkfs_time': mkfs, 'bytes_used': used, 'avm_marker': mkfs == used}


def read_tables(path):
    rows = []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh.read().splitlines():
            if line:
                rows.append(tuple(line.split('\t')))
    return rows


def layout_check(reader, carrier, oracle_rows, nonregular_rows, cid):
    """Re-read the carrier with the frozen reader (--layout avm) and require it
    to reproduce exactly the supplied oracle and nonregular rows."""
    py = shutil.which('python3')
    if not py:
        raise Bad('python3 not found on PATH')
    tmp = tempfile.mkdtemp(prefix='mk-carriers.%s.' % cid)
    try:
        o = os.path.join(tmp, 'oracle.tsv')
        n = os.path.join(tmp, 'nonregular.tsv')
        argv = [py, '-I', '--', reader, '--layout', 'avm',
                '--files', o, '--nonregular', n, '--inspect', carrier]
        try:
            p = subprocess.run(argv, cwd=tmp, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE, timeout=900)
        except subprocess.TimeoutExpired:
            raise Bad('%s: reader timed out under --layout avm' % cid)
        if p.returncode != 0:
            head = p.stderr.decode('utf-8', 'replace').strip().splitlines()[:3]
            raise Bad('%s: reader exited %d under --layout avm: %s'
                      % (cid, p.returncode, ' | '.join(head) or 'no stderr'))
        try:
            got_o = read_tables(o)
            got_n = read_tables(n)
        except OSError as exc:
            raise Bad('%s: reader wrote no tables under --layout avm: %s' % (cid, exc))
        want_o = [(r['path'], r['sha256'], str(r['size'])) for r in oracle_rows]
        want_n = [(r['path'], r['kind'], r['detail']) for r in nonregular_rows]
        if got_o != want_o:
            raise Bad('%s: frozen oracle does not equal a fresh --layout avm read '
                      '(%d vs %d rows)' % (cid, len(want_o), len(got_o)))
        if got_n != want_n:
            raise Bad('%s: frozen nonregular table does not equal a fresh --layout avm '
                      'read (%d vs %d rows)' % (cid, len(want_n), len(got_n)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def parse_spec(path):
    tups = []
    with open(path, encoding='utf-8') as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            fields = [f.strip() for f in line.split('\t')]
            if len(fields) != 4:
                raise Bad('%s:%d: want 4 tab-separated fields '
                          '(id, carrier, oracle, nonregular)' % (path, n))
            tups.append(tuple(fields))
    return tups


def natural_key(cid):
    m = re.match(r'^([A-Za-z]+)([0-9]+)$', cid)
    return (m.group(1), int(m.group(2))) if m else (cid, 0)


def build(root, tuples, magic, require_marker, reader, required_ids):
    carriers, ids = [], set()
    for cid, carrier_p, oracle_p, nonregular_p in tuples:
        if not ID_RE.match(cid):
            raise Bad('invalid carrier id %r' % cid)
        if cid in ids:
            raise Bad('duplicate carrier id %r' % cid)
        ids.add(cid)
        carrier = real_under(root, carrier_p, '%s carrier' % cid)
        oracle = real_under(root, oracle_p, '%s oracle' % cid)
        nonregular = real_under(root, nonregular_p, '%s nonregular' % cid)
        sb = superblock(carrier)
        if magic != 'any' and sb['magic'] != MAGIC[magic].decode('ascii'):
            want = 'BE' if magic == 'be' else 'LE'
            raise Bad('%s carrier is not %s (magic %r, want %r)'
                      % (cid, want, sb['magic'], MAGIC[magic].decode('ascii')))
        size = os.path.getsize(carrier)
        if sb['bytes_used'] == 0 or sb['bytes_used'] > size:
            raise Bad('%s bytes_used %d is not a plausible image size (carrier %d bytes)'
                      % (cid, sb['bytes_used'], size))
        if require_marker and not sb['avm_marker']:
            raise Bad('%s lacks the AVM marker (mkfs_time %d != bytes_used %d); '
                      'pass --no-require-marker only for a negative fixture'
                      % (cid, sb['mkfs_time'], sb['bytes_used']))
        orows = parse_oracle(oracle)
        nrows, kinds = parse_nonregular(nonregular)
        oset = {r['path'] for r in orows}
        clash = sorted(oset & {r['path'] for r in nrows})
        if clash:
            raise Bad('%s: path(s) listed as both regular and non-regular: %s'
                      % (cid, clash[:5]))
        if reader:
            layout_check(reader, carrier, orows, nrows, cid)
        entry = {
            'id': cid,
            'layout': 'avm',
            'magic': sb['magic'],
            'avm_marker': sb['avm_marker'],
            'mkfs_time': sb['mkfs_time'],
            'bytes_used': sb['bytes_used'],
            'path': rel_to(root, carrier),
            'sha256': sha256_file(carrier),
            'size_bytes': size,
            'oracle': rel_to(root, oracle),
            'oracle_sha256': sha256_file(oracle),
            'oracle_files': len(orows),
            'nonregular': rel_to(root, nonregular),
            'nonregular_sha256': sha256_file(nonregular),
            'nonregular_entries': len(nrows),
            'nonregular_by_kind': kinds,
            'receipt': RECEIPT_TMPL.format(id=cid),
        }
        carriers.append(entry)
    if required_ids:
        got = [e['id'] for e in carriers]
        if got != required_ids:
            raise Bad('carrier ids are %s, not the frozen R40-C1 set %s '
                      '(the counter enforces exactly these four in this order; pass '
                      '--allow-any-ids only for a development manifest)'
                      % (got, required_ids))
    else:
        carriers.sort(key=lambda e: natural_key(e['id']))
    for field, what in (('sha256', 'carrier pins'), ('path', 'carrier paths')):
        vals = [e[field] for e in carriers]
        if len(set(vals)) != len(vals):
            dup = sorted({v for v in vals if vals.count(v) > 1})
            raise Bad('duplicate %s: %s' % (what, dup))
    return {
        'claim': CLAIM,
        'schema': SCHEMA,
        'layout': 'avm',
        'note': ('Carriers and oracles frozen before any round-40 after-run. Each carrier is a '
                 'genuine AVM-layout big-endian SquashFS v4 image: sqsh magic, AVM marker '
                 '(mkfs_time == bytes_used), little-endian metadata block-length headers. sha256 '
                 'is the carrier pin; oracle holds regular files (relpath, sha256, size); '
                 'nonregular holds every non-regular entry (relpath, kind, detail) with kind in '
                 'dir|symlink|char-device|block-device|fifo|socket; receipt is the round-40 REA '
                 'extract-firmware after-receipt path for that carrier.'),
        'carriers': carriers,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description='emit the R40-C1 carrier manifest')
    ap.add_argument('--root', required=True, help='lane root (paths are relative to it)')
    ap.add_argument('--out', default=DEFAULT_OUT,
                    help='manifest path (default %s)' % DEFAULT_OUT)
    ap.add_argument('--spec', action='append', default=[],
                    help='TSV list: id<TAB>carrier<TAB>oracle<TAB>nonregular')
    ap.add_argument('--magic', choices=('be', 'le', 'any'), default='be',
                    help='required squashfs magic at offset 0 (default be: sqsh)')
    ap.add_argument('--no-require-marker', action='store_true',
                    help='do not require mkfs_time == bytes_used (negative fixtures only)')
    ap.add_argument('--layout-check', choices=('reader', 'off'), default='reader',
                    help="default reader: re-read each carrier with --layout avm and require "
                         "the frozen tables to reproduce; off skips that gate")
    ap.add_argument('--ids', default='V1,V2,L1,L2',
                    help='comma-separated exact carrier id set (default V1,V2,L1,L2)')
    ap.add_argument('--allow-any-ids', action='store_true',
                    help='do not enforce --ids (development manifests only)')
    ap.add_argument('--reader', default=None,
                    help='round-40 sqfs-list.py (default: sqfs-list.py next to this script)')
    ap.add_argument('tuples', nargs='*',
                    help='positional 4-tuples: ID CARRIER ORACLE NONREGULAR [ID ...]')
    a = ap.parse_args(argv)

    root = os.path.realpath(a.root)
    if not os.path.isdir(root):
        print('mk-carriers: --root is not a directory: %s' % a.root, file=sys.stderr)
        return 2
    reader = None
    if a.layout_check == 'reader':
        reader_in = a.reader or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             'sqfs-list.py')
        reader = os.path.realpath(reader_in)
        if not os.path.isfile(reader):
            print('mk-carriers: --layout-check reader needs the round-40 reader; not found: %s\n'
                  '  pass --reader PATH or --layout-check off' % reader_in, file=sys.stderr)
            return 2
    elif a.reader:
        print('mk-carriers: --reader ignored with --layout-check off', file=sys.stderr)

    tuples = []
    try:
        for spec in a.spec:
            tuples.extend(parse_spec(spec))
        if a.tuples:
            if len(a.tuples) % 4:
                raise Bad('positional carriers must come in groups of 4: '
                          'ID CARRIER ORACLE NONREGULAR')
            tuples.extend(tuple(a.tuples[i:i + 4]) for i in range(0, len(a.tuples), 4))
        if not tuples:
            raise Bad('no carriers given (pass --spec FILE and/or 4-tuples)')
        required_ids = [] if a.allow_any_ids else [x.strip() for x in a.ids.split(',')
                                                   if x.strip()]
        manifest = build(root, tuples, a.magic, not a.no_require_marker, reader,
                         required_ids)
    except Bad as e:
        print('mk-carriers: %s' % e, file=sys.stderr)
        return 2

    text = json.dumps(manifest, indent=2) + '\n'
    out = a.out if os.path.isabs(a.out) else os.path.join(root, a.out)
    try:
        os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
        tmp = out + '.tmp.%d' % os.getpid()
        with open(tmp, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        os.replace(tmp, out)
    except OSError as e:
        print('mk-carriers: cannot write %s: %s' % (out, e), file=sys.stderr)
        return 3

    for c in manifest['carriers']:
        print('%s  %s  files=%d  nonregular=%d%s  %s'
              % (c['id'], c['sha256'], c['oracle_files'], c['nonregular_entries'],
                 '' if not c['nonregular_by_kind'] else ' (' + ', '.join(
                     '%s:%d' % kv for kv in sorted(c['nonregular_by_kind'].items())) + ')',
                 c['path']))
    print('wrote %s (%d carriers, %d bytes, sha256=%s)'
          % (out, len(manifest['carriers']), len(text.encode()),
             hashlib.sha256(text.encode()).hexdigest()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
