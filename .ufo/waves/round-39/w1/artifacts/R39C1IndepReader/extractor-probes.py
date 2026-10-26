#!/usr/bin/env python3
"""Cross-check sqfs-list.py tables against the extractors the C1 claim rests on.

Read-only over the corpus: the four committed round-37 carriers are handed to
unblob 26.6.4 exactly as they are, and every output directory lives under
--work.  Development fixtures are passed as .sqsh paths built by
build-and-check.py.

  * /usr/bin/unsquashfs 4.7.5   on the LE development fixtures
  * ~/.local/bin/sasquatch-v4be 4.5.1 (unblob's BE extractor) on BE fixtures + K1
  * ~/.local/bin/unblob 26.6.4  on K1..K4 (the engine REA 6.5.0 wraps)

For each run the extracted *regular files* are compared with the reader's
--files table (relative path, sha256, size) and the symlinks the extractor kept
are listed with the reader's in-tree/escaping class beside them.

Usage:
  python3 extractor-probes.py --work DIR --artifacts DIR --lane LANE
Exit 0 when every extractor agrees with the reader.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

READER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'sqfs-list.py')
UNSQUASHFS = '/usr/bin/unsquashfs'
SASQUATCH_BE = os.path.expanduser('~/.local/bin/sasquatch-v4be')
UNBLOB = os.path.expanduser('~/.local/bin/unblob')


def rel_rows(root):
    rows = []
    for dirpath, dnames, fnames in os.walk(root):
        dnames.sort()
        for name in sorted(fnames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                continue
            with open(path, 'rb') as fh:
                data = fh.read()
            rows.append((os.path.relpath(path, root).replace(os.sep, '/'),
                         hashlib.sha256(data).hexdigest(), str(len(data))))
    rows.sort(key=lambda r: r[0].encode())
    return rows


def rel_links(root):
    out = []
    for dirpath, dnames, fnames in os.walk(root):
        for name in list(dnames) + list(fnames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                out.append((os.path.relpath(path, root).replace(os.sep, '/'),
                            os.readlink(path)))
        for name in list(dnames):
            if os.path.islink(os.path.join(dirpath, name)):
                dnames.remove(name)
    out.sort()
    return out


def read_tsv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        return [tuple(line.split('\t')) for line in fh.read().splitlines()]


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def first_line(text):
    for line in text.splitlines():
        if line.strip():
            return line.strip()[:160]
    return '(no output)'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--artifacts', required=True)
    ap.add_argument('--lane', required=True)
    ap.add_argument('--mksquashfs', default='mksquashfs')
    args = ap.parse_args()
    work = args.work
    art = args.artifacts
    corpus = os.path.join(args.lane, 'corpus', 'evidence', 'round-37', 'c1')
    lines = []
    ok = True

    def emit(text=''):
        lines.append(text)

    # -- unsquashfs on the LE development fixtures -------------------------
    emit('## unsquashfs 4.7.5 on the LE development fixtures')
    for name in ('A-le-gzip', 'B-le-xz', 'D-le-mksq-gzip', 'D-le-mksq-xz',
                 'S-le-mksq-gzip'):
        image = os.path.join(work, name + '.sqsh')
        out = os.path.join(work, 'unsquashfs-' + name)
        if os.path.isdir(out):
            shutil.rmtree(out)
        rc, text = run([UNSQUASHFS, '-no-progress', '-d', out, image], work)
        emit('%s: exit %d %s' % (name, rc, '' if rc == 0 else
                                 '(%s)' % first_line(text)))
        if rc == 0:
            mine = read_tsv(os.path.join(art, name + '.files.tsv'))
            theirs = rel_rows(out)
            same = mine == theirs
            ok = ok and same
            emit('  extracted regular files: %d, reader rows: %d, %s'
                 % (len(theirs), len(mine),
                    'IDENTICAL (path, sha256, size)' if same else 'DIFFER'))
            links = rel_links(out)
            if links:
                emit('  extractor kept symlinks: %r' % (links,))
        else:
            emit('  partial output: %r' % (rel_rows(out)[:4],))

    # -- sasquatch-v4be on BE fixtures and K1 ------------------------------
    emit('')
    emit('## sasquatch-v4be 4.5.1 (unblob BE extractor, -be)')
    be_cases = [('K1', os.path.join(corpus, 'K1', 'carrier.sqsh'),
                 os.path.join(art, 'K1.files.tsv')),
                ('B-be-gzip', os.path.join(work, 'B-be-gzip.sqsh'),
                 os.path.join(art, 'B-be-gzip.files.tsv')),
                ('B-be-xz', os.path.join(work, 'B-be-xz.sqsh'),
                 os.path.join(art, 'B-be-xz.files.tsv'))]
    for name, image, table in be_cases:
        out = os.path.join(work, 'sasquatch-' + name)
        if os.path.isdir(out):
            shutil.rmtree(out)
        rc, text = run([SASQUATCH_BE, '-be', '-d', out, image], work)
        emit('%s: exit %d %s' % (name, rc, '' if rc == 0 else
                                 '(%s)' % first_line(text)))
        if rc == 0 and os.path.isdir(out):
            mine = read_tsv(table)
            theirs = rel_rows(out)
            same = mine == theirs
            ok = ok and same
            emit('  extracted regular files: %d, reader rows: %d, %s'
                 % (len(theirs), len(mine),
                    'IDENTICAL (path, sha256, size)' if same else 'DIFFER'))
            links = rel_links(out)
            emit('  extractor kept symlinks: %r' % (links,))
    emit('  note: on B-be-xz the generator wrote raw LZMA2 under compression '
         'id 2; sasquatch-v4be tries every decompressor and fails.')

    # -- chain / loop fixture (own image, own expected classes) -----------
    emit('')
    emit('## chain and loop fixture (built here with mksquashfs 4.7.5, LE gzip)')
    tree = os.path.join(work, 'chains-tree')
    if os.path.isdir(tree):
        shutil.rmtree(tree)
    os.makedirs(tree)
    with open(os.path.join(tree, 'hello.txt'), 'wb') as fh:
        fh.write(b'hello\n')
    for name, target in (('y', '../outside.txt'), ('x', 'y'),
                         ('q', 'hello.txt'), ('p', 'q'),
                         ('a', 'b'), ('b', 'a'), ('self', 'self')):
        os.symlink(target, os.path.join(tree, name))
    chains_image = os.path.join(work, 'chains-le-gzip.sqsh')
    cmd = [args.mksquashfs, tree, chains_image, '-noappend', '-comp', 'gzip',
           '-all-root', '-no-progress']
    if os.path.exists(chains_image):
        os.unlink(chains_image)
    rc, text = run(cmd, work)
    emit('mksquashfs exit %d' % rc)
    expected = {'a': 'in-tree', 'b': 'in-tree', 'p': 'in-tree', 'q': 'in-tree',
                'self': 'in-tree', 'x': 'escaping', 'y': 'escaping'}
    prefix = os.path.join(art, 'chains-le-gzip')
    p = subprocess.run([sys.executable, '-I', '-B', READER, chains_image,
                        '--files', prefix + '.files.tsv',
                        '--symlinks', prefix + '.symlinks.tsv', '--inspect'],
                       cwd=work, capture_output=True, text=True)
    with open(prefix + '.inspect.json', 'w') as fh:
        fh.write(p.stdout)
    with open(prefix + '.stderr.txt', 'w') as fh:
        fh.write(p.stderr)
    emit('reader exit %d' % p.returncode)
    got = {row[0]: row[2] for row in read_tsv(prefix + '.symlinks.tsv')}
    emit('reader classes: %r' % (got,))
    emit('expected (chain-aware POSIX resolution, loop = kept): %r' % (expected,))
    ok = ok and got == expected
    out = os.path.join(work, 'unblob-chains')
    if os.path.isdir(out):
        shutil.rmtree(out)
    report = os.path.join(work, 'unblob-chains.json')
    log = os.path.join(work, 'unblob-chains.log')
    for stale in (report, log):
        if os.path.exists(stale):
            os.unlink(stale)
    rc, text = run([UNBLOB, '-f', '-e', out, '--report', report, '--log', log,
                    '-p', '4', chains_image], work)
    emit('unblob exit %d' % rc)
    root = os.path.join(out, 'chains-le-gzip.sqsh_extract')
    kept = rel_links(root) if os.path.isdir(root) else []
    emit('unblob kept (post-rewrite targets): %r' % (kept,))
    removed = []

    def walk_chain(o):
        if isinstance(o, dict):
            if o.get('__typename__') == 'MaliciousSymlinkRemoved':
                removed.append(os.path.basename(o.get('link', '')))
            for v in o.values():
                walk_chain(v)
        elif isinstance(o, list):
            for v in o:
                walk_chain(v)
    if os.path.exists(report):
        walk_chain(json.load(open(report, encoding='utf-8')))
    emit('unblob removed: %r' % (sorted(removed),))
    kept_names = sorted(name for name, _t in kept)
    want_kept = sorted(k for k, v in expected.items() if v == 'in-tree')
    want_removed = sorted(k for k, v in expected.items() if v == 'escaping')
    same = kept_names == want_kept and sorted(removed) == want_removed
    emit('kept set %s, removed set %s'
         % ('MATCHES' if kept_names == want_kept else 'DIFFERS',
            'MATCHES' if sorted(removed) == want_removed else 'DIFFERS'))
    ok = ok and same

    # -- unblob 26.6.4: corpus carriers and development fixtures ----------
    emit('')
    emit('## unblob 26.6.4 (the engine REA 6.5.0 wraps)')
    cases = [('K1', os.path.join(corpus, 'K1', 'carrier.sqsh')),
             ('K2', os.path.join(corpus, 'K2', 'carrier.sqsh')),
             ('K3', os.path.join(corpus, 'K3', 'carrier.bin')),
             ('K4', os.path.join(corpus, 'K4', 'carrier.bin')),
             ('A-le-gzip', os.path.join(work, 'A-le-gzip.sqsh')),
             ('B-be-gzip', os.path.join(work, 'B-be-gzip.sqsh')),
             ('D-le-mksq-gzip', os.path.join(work, 'D-le-mksq-gzip.sqsh')),
             ('S-le-mksq-gzip', os.path.join(work, 'S-le-mksq-gzip.sqsh'))]
    for label, image in cases:
        out = os.path.join(work, 'unblob-' + label)
        if os.path.isdir(out):
            shutil.rmtree(out)
        report = os.path.join(work, 'unblob-%s.json' % label)
        log = os.path.join(work, 'unblob-%s.log' % label)
        for stale in (report, log):
            if os.path.exists(stale):
                os.unlink(stale)       # unblob refuses to overwrite a report
        rc, text = run([UNBLOB, '-f', '-e', out,
                        '--report', report, '--log', log, '-p', '4', image],
                       work)
        emit('%s: exit %d' % (label, rc))
        roots = [os.path.join(out, d) for d in sorted(os.listdir(out))] \
            if os.path.isdir(out) else []
        root = roots[0] if len(roots) == 1 else None
        if rc != 0 or root is None:
            ok = False
            emit('  unexpected layout %r' % (roots,))
            continue
        mine = read_tsv(os.path.join(art, label + '.files.tsv'))
        theirs = rel_rows(root)
        same = mine == theirs
        ok = ok and same
        emit('  extracted regular files: %d, reader rows: %d, %s'
             % (len(theirs), len(mine),
                'IDENTICAL (path, sha256, size)' if same else 'DIFFER'))
        kept = [p for p, _t in rel_links(root)]
        rows = read_tsv(os.path.join(art, label + '.symlinks.tsv'))
        in_tree = sorted(p for p, _t, cls in rows if cls == 'in-tree')
        escaping = sorted(p for p, _t, cls in rows if cls == 'escaping')
        removed = []

        def walk(o):
            if isinstance(o, dict):
                if o.get('__typename__') == 'MaliciousSymlinkRemoved':
                    link = o.get('link', '')
                    removed.append(os.path.relpath(link, root))
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(json.load(open(report, encoding='utf-8')))
        kept_ok = kept == in_tree
        removed_ok = sorted(removed) == escaping
        ok = ok and kept_ok and removed_ok
        emit('  kept by unblob:  %r' % (kept,))
        emit('  reader in-tree:  %r%s' % (in_tree, '' if kept_ok else
                                          '   <-- MISMATCH'))
        emit('  MaliciousSymlinkRemoved: %r' % (sorted(removed),))
        emit('  reader escaping: %r%s' % (escaping, '' if removed_ok else
                                          '   <-- MISMATCH'))
        for row in rows:
            emit('  link %s -> %s [%s]' % row)
        emit('  (unblob rewrites a kept absolute target relative to the link '
             'directory before writing it back; the reader reports the raw '
             'on-disk target.)')

    emit('')
    emit('verdict: %s' % ('EVERY EXTRACTOR AGREES' if ok else 'DISAGREEMENT'))
    text = '\n'.join(lines) + '\n'
    with open(os.path.join(art, 'extractor-probes.txt'), 'w') as fh:
        fh.write(text)
    sys.stdout.write(text)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
