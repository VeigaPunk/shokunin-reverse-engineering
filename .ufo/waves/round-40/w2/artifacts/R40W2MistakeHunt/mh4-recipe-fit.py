#!/usr/bin/env python3
"""MH-4 — the `partial-body-failure` recipe's mechanism was measured one way
(0xFF fill required, `w1/R40C2ReconPartial.md` §2.1) and frozen another way
(`heldout-gen-v2.py:591` writes `bytes(length)` = 0x00), and the class's only
freeze-time check is a label match on envelopes the same run produced.

What this probe does: builds standard-BE SquashFS v4 carriers with the frozen
writer, damages the last compressed block of the last-scanned regular file with a
chosen fill (the frozen target-selection code is imported, only the fill byte is
parameterised), runs one REA `extract-firmware` per carrier, and prints the tuple
the v2 table reads: handler · extraction_failed · published files · gap kinds.

Usage:
  mh4-recipe-fit.py --work DIR [--shapes s1,s2,s3] [--fills 00,ff] [--comps gzip,xz]
                    [--expect partial-body-failure] [--reuse]
Exit 0 = every measured tuple equals the class tuple (all "fit");
1 = at least one carrier does not reach the class tuple; 2 = setup error.

Red/green: the same builder and the same target-selection code, only the fill byte
differs, so the run that lands `clean` and the run that lands `partial-body-failure`
are one variable apart.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
GEN = os.path.join(LANE, 'tools/round-40/gen-squashfs.py')
HELDOUT = os.path.join(LANE, 'tools/round-40/heldout-gen-v2.py')
BLOCK = 4096
SHAPES = {
    # name: (size of the last-scanned regular file = the damage target, content kind)
    # pattern ~2% compressed: the zeroed block is a few dozen bytes and the
    # decompressor fallback fails.  hex ~55% compressed: the zeroed block is
    # ~1.7 KiB and the fallback chain *succeeds*, so a zero fill lands `clean`.
    's1': (1500, 'pattern'),   # one block
    's2': (7093, 'pattern'),   # 4096 + 2997
    's3': (9000, 'pattern'),   # 4096 + 4096 + 808
    'h1': (3100, 'hex'),       # one block, compressed length ~1776
    'h2': (7093, 'hex'),       # 4096 + 2997, both compressed length > 1 KiB
}
CLASS_TUPLE = {
    'partial-body-failure': {'handler': 'squashfs_v4_be', 'failed': True,
                             'min_files': 1, 'gap': 'extractor-failure'},
    'clean': {'handler': 'squashfs_v4_be', 'failed': False,
              'min_files': 1, 'gap': None},
}


def stream(label, n):
    out = bytearray()
    i = 0
    while len(out) < n:
        out += hashlib.sha256(('%s/%d' % (label, i)).encode()).digest()
        i += 1
    return bytes(out[:n])


def hexstream(label, n):
    """Semi-compressible content (~half the bytes are entropy): a compressed block
    stays large, which is the regime where a zeroed block is absorbed."""
    out = bytearray()
    i = 0
    while len(out) < n:
        out += hashlib.sha256(('%s/%d' % (label, i)).encode()).hexdigest().encode()[:32]
        i += 1
    return bytes(out[:n])


def pat(label, n):
    head = stream(label + ':head', 48)
    body = (b'ABCDEFGH' * ((n - 48) // 8 + 1))[:max(0, n - 48)]
    return head[:min(n, 48)] + body


def load_heldout():
    spec = importlib.util.spec_from_file_location('hg', HELDOUT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def target_block(hg, raw):
    """The frozen target selection (`corruption_partial` steps 3-4), no mutation."""
    image = hg._Sqfs(bytes(raw))
    entries = image.files()
    if len(entries) < 2:
        raise SystemExit('partial recipe needs >= 2 regular files')
    for entry in reversed(entries):
        for block in reversed(entry['blocks']):
            if block['compressed'] and not block['sparse']:
                return entry, block
    raise SystemExit('no compressed data block')


def damage(hg, raw, fill):
    entry, block = target_block(hg, raw)
    out = bytearray(raw)
    start, length = block['offset'], block['length']
    out[start:start + length] = bytes([fill]) * length
    return out, {'path': entry['path'], 'file_size': entry['size'],
                 'blocks': len(entry['blocks']), 'offset': start,
                 'block_length': length, 'fill': '%02x' % fill}


def build_tree(root, target_size, label, content='pattern'):
    os.makedirs(root, exist_ok=True)
    maker = hexstream if content == 'hex' else pat
    files = {'aa.bin': min(2500, target_size), 'zz.bin': target_size}
    for rel, size in files.items():
        with open(os.path.join(root, rel), 'wb') as fh:
            fh.write(maker(label + ':' + rel, size))


def run_rea(work, name, carrier):
    out = os.path.join(work, 'runs', name)
    os.makedirs(out, exist_ok=True)
    # REA refuses a non-empty output directory: clear this run's extract tree so a
    # repeat of the matrix is a fresh measurement, not a stale envelope.
    shutil.rmtree(os.path.join(out, 'extract'), ignore_errors=True)
    env = dict(os.environ)
    env['REA_UNBLOB_COMMAND'] = os.path.expanduser('~/.local/bin/unblob')
    env['TMPDIR'] = work
    env['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'
    argv = ['npx', '-y', 'rea-agents@6.5.0', 'extract-firmware', '--format', 'json',
            '--full-output', '--max-depth', '3', carrier, os.path.join(out, 'extract')]
    proc = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    envelope = os.path.join(out, 'envelope.json')
    with open(envelope, 'wb') as fh:
        fh.write(proc.stdout)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode()[-800:])
    return envelope, proc.returncode


def tuple_of(envelope_path):
    with open(envelope_path) as fh:
        doc = json.load(fh)
    node = doc.get('data') if 'data' in doc else doc
    nr = node.get('normalized_result') or {}
    chunks = nr.get('chunks') or []
    handler = None
    failed = False
    for c in chunks:
        if c.get('handler'):
            handler = c['handler']
            failed = bool(c.get('extraction_failed'))
            break
    gaps = sorted({g.get('kind') for g in nr.get('extraction_gaps') or []})
    return {'handler': handler, 'failed': failed,
            'files': len(nr.get('files') or []), 'gaps': gaps,
            'coverage': nr.get('coverage')}


def fits(label, tup):
    want = CLASS_TUPLE[label]
    if tup['handler'] != want['handler']:
        return False, 'handler %s' % tup['handler']
    if tup['failed'] != want['failed']:
        return False, 'extraction_failed %s' % tup['failed']
    if tup['files'] < want['min_files']:
        return False, 'files %d' % tup['files']
    if want['gap'] and want['gap'] not in tup['gaps']:
        return False, 'gap %s' % tup['gaps']
    if want['gap'] is None and tup['gaps']:
        return False, 'gap %s' % tup['gaps']
    return True, 'ok'


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--shapes', default='s1,s2,s3')
    ap.add_argument('--fills', default='00,ff')
    ap.add_argument('--comps', default='gzip,xz')
    ap.add_argument('--expect', default='partial-body-failure')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--reuse', action='store_true')
    args = ap.parse_args(argv)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    hg = load_heldout()
    rows = []
    bad = 0
    for shape in args.shapes.split(','):
        size, content = SHAPES[shape]
        tree = os.path.join(work, 'tree-' + shape)
        if not os.path.isdir(tree):
            build_tree(tree, size, 'mh4-' + shape, content)
        for comp in args.comps.split(','):
            image = os.path.join(work, '%s-%s.sqsh' % (shape, comp))
            if not os.path.exists(image):
                proc = subprocess.run([sys.executable, '-I', '-B', GEN, tree, image,
                                       '--endian', 'be', '--comp', comp],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if proc.returncode != 0:
                    print('build failed for %s/%s: %s' % (shape, comp,
                                                          proc.stderr.decode()[-300:]))
                    return 2
            raw = open(image, 'rb').read()
            for fill_hex in args.fills.split(','):
                fill = int(fill_hex, 16)
                damaged, info = damage(hg, raw, fill)
                name = '%s-%s-%s' % (shape, comp, fill_hex)
                carrier = os.path.join(work, 'runs', name, 'carrier.sqsh')
                os.makedirs(os.path.dirname(carrier), exist_ok=True)
                with open(carrier, 'wb') as fh:
                    fh.write(damaged)
                envelope = os.path.join(work, 'runs', name, 'envelope.json')
                if not (args.reuse and os.path.exists(envelope)):
                    envelope, rc = run_rea(work, name, carrier)
                    if rc != 0:
                        print('%s: rea exit %d (envelope kept)' % (name, rc))
                tup = tuple_of(envelope)
                ok, why = fits(args.expect, tup)
                if not ok:
                    bad += 1
                rows.append({'run': name, 'shape': shape, 'target': info,
                             'tuple': tup, 'expect': args.expect,
                             'fits': ok, 'why': why})
                print('%-18s target=%-7s fill=%s blocks=%d size=%-5d -> handler=%s failed=%s '
                      'files=%d gaps=%s fits(%s)=%s %s'
                      % (name, info['path'], fill_hex, info['blocks'], info['file_size'],
                         tup['handler'], tup['failed'], tup['files'], tup['gaps'],
                         args.expect, ok, '' if ok else '(' + why + ')'))
    if args.json:
        with open(os.path.join(work, 'matrix.json'), 'w') as fh:
            json.dump(rows, fh, indent=1)
    print('runs=%d not_fit=%d' % (len(rows), bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
