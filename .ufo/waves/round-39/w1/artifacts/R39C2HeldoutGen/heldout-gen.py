#!/usr/bin/env python3
"""R39-C2 held-out SquashFS carrier generator (freezes with round 39).

Every byte this script emits is a pure function of ``--seed`` (the freeze commit
hash).  Structure comes from ``random.Random(int(seed[:16], 16) ^ (class_index
* 1000 + k))``; file contents come from a SHA-256 counter stream keyed by
(seed, class, k, relative path), so images stay reproducible across Python and
liblzma point releases rather than only inside one interpreter build.  No clock,
no ``os.urandom``, no directory-listing order, no host-specific input.

Usage
    python3 -I -B heldout-gen.py --seed HEX --out DIR [--classes a,b,...] [--run]

``--run`` executes REA 6.5.0 ``extract-firmware`` once per carrier in its arm
(``after``: PATH unchanged; ``before``: ``$HOME/.local/bin`` removed, so both
sasquatch binaries are unresolvable) and writes ``DIR/<id>/envelope.json`` (the
``data`` object of the full CLI envelope) plus ``DIR/<id>/rea-full.json``.

Layout
    DIR/manifest.json        {seed, generator, classes, carriers:[{id, class, label, arm, carrier, sha256}]}
    DIR/<id>/carrier.sqsh
    DIR/<id>/tree.json       oracle: regular files (path, sha256, size) + symlinks (path, target, kind)
    DIR/<id>/envelope.json   (--run only) the `data` object
    DIR/<id>/rea-full.json   (--run only) the whole {ok, data, meta} envelope
    DIR/<id>/run.json        (--run only) arm, exit code, digest binding

The image writer is tools/round-37/gen-squashfs.py, loaded by path.  Its xz block
encoder is replaced here: the round-37 prototype writes bare LZMA2 streams and
sasquatch 4.5.1 rejects them (``writer: failed to read/uncompress file``), while
mksquashfs 4.7.5 writes complete .xz containers (byte-verified, see report).
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import lzma
import os
import posixpath
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib

# A run without -B must not drop tools/round-37/__pycache__ into the lane.
sys.dont_write_bytecode = True

VERSION = 'r39-c2-v1'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789_-'
CARRIERS_PER_CLASS = 2
COMP_CHOICES = ('gzip', 'xz')
REA_PACKAGE = 'rea-agents@6.5.0'
BLOCK_ENCODER = ('gzip=zlib level 9, comp_id 1; xz=.xz container/CRC32, '
                 'comp_id 4 (replaces stock raw-LZMA2 and comp_id 2)')

# ---------------------------------------------------------------------------
# Recipe table.  ``label`` is the triage label the frozen interpreter must
# produce; the recipe key is the generator-side ``class``, so clean-be and
# clean-le share the single label ``clean``.
#
#   endian      le | be | avm   (avm = BE magic with mkfs_time := bytes_used,
#                                the marker that makes unblob drop ``-be``)
#   arm         after | before  (PATH arm for the REA run)
#   comp        'seed' (gzip|xz by the carrier RNG) or a fixed choice
#   symlinks    kinds: 'escaping' -> relative target leaving the image root,
#               removed by unblob and reported MaliciousSymlinkRemoved with no
#               gap; 'in-tree' -> relative target resolving inside the root,
#               kept as metadata and reported as one unpublished-entry gap
#   corruption  key into CORRUPTIONS, applied to the finished image bytes
# ---------------------------------------------------------------------------
RECIPES = {
    'clean-be': dict(label='clean', endian='be', arm='after', comp='seed',
                     symlinks=(), corruption=None),
    'clean-le': dict(label='clean', endian='le', arm='after', comp='seed',
                     symlinks=(), corruption=None),
    'escaping-symlink-removed': dict(label='escaping-symlink-removed', endian='be',
                                     arm='after', comp='seed',
                                     symlinks=('escaping',), corruption=None),
    'in-tree-symlink-metadata': dict(label='in-tree-symlink-metadata', endian='be',
                                     arm='after', comp='seed',
                                     symlinks=('in-tree',), corruption=None),
    'dep-missing-be': dict(label='dep-missing-be', endian='be', arm='before',
                           comp='seed', symlinks=(), corruption=None),
    'dep-missing-le': dict(label='dep-missing-le', endian='le', arm='before',
                           comp='seed', symlinks=(), corruption=None),
    'avm-marker-be-dropped': dict(label='avm-marker-be-dropped', endian='avm',
                                  arm='after', comp='seed', symlinks=(),
                                  corruption=None),
    'body-extractor-failure': dict(label='body-extractor-failure', endian='be',
                                   arm='after', comp='seed', symlinks=(),
                                   corruption='zero-id-table'),
    # Opt-in only (not in DEFAULT_CLASSES): with s_major bumped no unblob
    # handler pattern matches, so REA publishes no squashfs chunk at all.
    'no-squashfs-chunk': dict(label='no-squashfs-chunk', endian='be', arm='after',
                              comp='seed', symlinks=(), corruption='bad-major'),
    # Opt-in only: s_minor 5 still matches the v4 pattern (the pattern pins
    # s_major), the handler runs, and sasquatch rejects the header — a third
    # extractor-failure flavour distinct from the AVM marker and id-table damage.
    'version-minor-mismatch': dict(label='version-minor-mismatch', endian='be',
                                   arm='after', comp='seed', symlinks=(),
                                   corruption='bad-minor'),
}

DEFAULT_CLASSES = (
    'clean-be', 'clean-le', 'escaping-symlink-removed', 'in-tree-symlink-metadata',
    'dep-missing-be', 'dep-missing-le', 'avm-marker-be-dropped',
    'body-extractor-failure',
)


# ---------------------------------------------------------------------------
# image writer
# ---------------------------------------------------------------------------
WRITER_LOGICAL = os.path.join('tools', 'round-37', 'gen-squashfs.py')


def default_writer_path():
    """Locate gen-squashfs.py: tools/round-39/../round-37, then any ancestor's tools/round-37."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [os.path.join(here, '..', 'round-37', 'gen-squashfs.py')]
    cursor = here
    for _ in range(8):
        candidates.append(os.path.join(cursor, 'tools', 'round-37', 'gen-squashfs.py'))
        parent = os.path.dirname(cursor)
        if parent == cursor:
            break
        cursor = parent
    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.normpath(candidate)
    return os.path.normpath(candidates[0])


def writer_logical_path(resolved):
    """Stable manifest value: the lane-relative path when the writer lives under tools/round-37."""
    marker = WRITER_LOGICAL + os.sep
    if resolved.endswith(marker[:-1]):
        return WRITER_LOGICAL
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.relpath(resolved, here)


def load_writer(path):
    if not os.path.isfile(path):
        raise SystemExit(f'image writer not found: {path}')
    spec = importlib.util.spec_from_file_location('r37_gen_squashfs', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def install_block_encoder(module):
    """Replace the round-37 block encoder and compression-id table.

    gzip is unchanged.  Two stock defects are corrected:
      * stock ``COMP`` maps xz to 2, which SquashFS defines as LZMA (xz is 4;
        mksquashfs 4.7.5 writes ``comp 4`` for an xz image), so an xz image
        would advertise the wrong decompressor;
      * stock xz blocks are bare LZMA2 streams (FORMAT_RAW) that sasquatch
        4.5.1 rejects with ``writer: failed to read/uncompress file``; squashfs
        xz blocks are complete .xz containers with a CRC32 check.
    """

    def comp_bytes(kind, data, block_size=4096):
        if kind == 'gzip':
            compressor = zlib.compressobj(9, zlib.DEFLATED, 15)
            return compressor.compress(data) + compressor.flush()
        return lzma.compress(
            data, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC32,
            filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6}],
        )

    module.comp_bytes = comp_bytes
    module.COMP = {'gzip': 1, 'xz': 4}


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# corruptions: bytearray(clean image) -> bytearray(corrupted image)
# ---------------------------------------------------------------------------
def corruption_zero_id_table(payload, endian):
    """Zero the id-table metadata block (header + payload).

    Superblock field id_table_start is a u64 at offset 48 in both endiannesses.
    It points just past the id metadata block at the 8-byte id table index, and
    that index holds the metadata block's start.  sasquatch then reports
    ``read_id_table: failed to read id table block`` / ``FATAL ERROR: File
    system corruption detected``.
    """
    prefix = '>' if endian in ('be', 'avm') else '<'
    id_table_start = struct.unpack(prefix + 'Q', bytes(payload[48:56]))[0]
    if not 96 <= id_table_start <= len(payload) - 8:
        raise ValueError(
            f'id_table_start {id_table_start} outside image ({len(payload)} bytes)')
    id_meta_start = struct.unpack(
        prefix + 'Q', bytes(payload[id_table_start:id_table_start + 8]))[0]
    if not 96 <= id_meta_start < id_table_start <= len(payload):
        raise ValueError(
            f'id metadata block {id_meta_start}..{id_table_start} outside image')
    payload[id_meta_start:id_table_start] = bytes(id_table_start - id_meta_start)
    return payload


def corruption_bad_minor(payload, endian):
    """s_minor 4 -> 5 so no unblob v4 handler matches; the image stays a plain unknown chunk."""
    prefix = '>' if endian in ('be', 'avm') else '<'
    major, minor = struct.unpack(prefix + 'HH', bytes(payload[28:32]))
    if (major, minor) != (4, 0):
        raise ValueError(f'unexpected squashfs version {major}.{minor}')
    payload[28:32] = struct.pack(prefix + 'HH', 4, 5)
    return payload


def corruption_bad_major(payload, endian):
    """s_major 4 -> 9: no v1..v4 handler pattern matches (they pin s_major), so the
    image stays an unknown chunk and REA publishes no squashfs chunk."""
    prefix = '>' if endian in ('be', 'avm') else '<'
    major, minor = struct.unpack(prefix + 'HH', bytes(payload[28:32]))
    if (major, minor) != (4, 0):
        raise ValueError(f'unexpected squashfs version {major}.{minor}')
    payload[28:32] = struct.pack(prefix + 'HH', 9, 0)
    return payload


CORRUPTIONS = {
    'zero-id-table': corruption_zero_id_table,
    'bad-minor': corruption_bad_minor,
    'bad-major': corruption_bad_major,
}


# ---------------------------------------------------------------------------
# deterministic tree material
# ---------------------------------------------------------------------------
def stream_bytes(material, size):
    """SHA-256 counter stream: independent of the interpreter's PRNG."""
    out = bytearray()
    counter = 0
    while len(out) < size:
        out += hashlib.sha256(material + b'#' + str(counter).encode()).digest()
        counter += 1
    return bytes(out[:size])


def token(rng, low=3, high=9):
    return ''.join(rng.choice(ALPHABET) for _ in range(rng.randint(low, high)))


def unique_name(rng, taken):
    while True:
        name = token(rng)
        if name not in taken:
            taken.add(name)
            return name


def build_tree(rng, material, root, link_kinds):
    """Create one random tree.

    Returns (dirs, files, symlinks): directory paths, regular-file paths and
    [(relative path, link target, kind)] — all relative posix strings.
    """
    depth = rng.randint(1, 3)
    dirs = []
    parts = []
    for _ in range(depth):
        parts.append(token(rng))
        dirs.append('/'.join(parts))
    for rel in dirs:
        os.makedirs(os.path.join(root, rel))

    slots = [''] + dirs
    taken = {rel: set() for rel in slots}
    for rel in dirs:
        parent = posixpath.dirname(rel)
        taken[parent].add(posixpath.basename(rel))

    files = []
    for _ in range(rng.randint(3, 8)):
        parent = rng.choice(slots)
        name = unique_name(rng, taken[parent])
        rel = f'{parent}/{name}' if parent else name
        with open(os.path.join(root, rel), 'wb') as handle:
            handle.write(stream_bytes(material + b':' + rel.encode(),
                                      rng.randrange(0, 20001)))
        files.append(rel)

    symlinks = []
    for kind in link_kinds:
        if kind == 'escaping':
            name = unique_name(rng, taken[''])
            target = '../' + token(rng)
            os.symlink(target, os.path.join(root, name))
            symlinks.append((name, target, 'escaping'))
        elif kind == 'in-tree':
            target_rel = rng.choice(files)
            parent = rng.choice(slots)
            if parent == posixpath.dirname(target_rel) and len(slots) > 1:
                parent = rng.choice([d for d in slots if d != parent])
            name = unique_name(rng, taken[parent])
            link_rel = f'{parent}/{name}' if parent else name
            target = posixpath.relpath(target_rel, start=parent or '.')
            os.symlink(target, os.path.join(root, link_rel))
            symlinks.append((link_rel, target, 'in-tree'))
        else:
            raise ValueError(f'unknown symlink kind {kind!r}')
    return dirs, files, symlinks


def tree_oracle(root, dirs, files, symlinks):
    return {
        'directories': sorted(dirs),
        'files': [
            {'path': rel, 'sha256': sha256_file(os.path.join(root, rel)),
             'size': os.path.getsize(os.path.join(root, rel))}
            for rel in sorted(files)
        ],
        'symlinks': [
            {'path': rel, 'target': target, 'kind': kind}
            for rel, target, kind in sorted(symlinks)
        ],
    }


# ---------------------------------------------------------------------------
# carrier build
# ---------------------------------------------------------------------------
def build_carrier(seed, name, k, seq, writer, scratch, out_dir):
    """Build one carrier; return (manifest entry, oracle)."""
    recipe = RECIPES[name]
    class_index = list(RECIPES).index(name)
    rng = random.Random(int(seed[:16], 16) ^ (class_index * 1000 + k))
    material = f'{seed}:{name}:{k}'.encode()

    work = os.path.join(scratch, f'build-{seq:02d}')
    tree = os.path.join(work, 'tree')
    os.makedirs(tree)
    dirs, files, symlinks = build_tree(rng, material, tree, recipe['symlinks'])
    oracle = tree_oracle(tree, dirs, files, symlinks)

    comp = rng.choice(COMP_CHOICES) if recipe['comp'] == 'seed' else recipe['comp']
    image = os.path.join(work, 'carrier.sqsh')
    with contextlib.redirect_stdout(io.StringIO()):
        writer.build_image(tree, image, recipe['endian'], comp)

    if recipe['corruption']:
        with open(image, 'rb') as handle:
            payload = bytearray(handle.read())
        payload = CORRUPTIONS[recipe['corruption']](payload, recipe['endian'])
        with open(image, 'wb') as handle:
            handle.write(bytes(payload))

    carrier_id = f'H{seq:02d}'
    dest = os.path.join(out_dir, carrier_id)
    os.makedirs(dest, exist_ok=True)
    shutil.copyfile(image, os.path.join(dest, 'carrier.sqsh'))
    entry = {
        'id': carrier_id,
        'class': name,
        'label': recipe['label'],
        'arm': recipe['arm'],
        'carrier': f'{carrier_id}/carrier.sqsh',
        'sha256': sha256_file(os.path.join(dest, 'carrier.sqsh')),
    }
    with open(os.path.join(dest, 'tree.json'), 'w', encoding='utf-8') as handle:
        json.dump({'seed': seed, 'class': name, 'id': carrier_id,
                   'endian': recipe['endian'], 'compression': comp,
                   'oracle': oracle}, handle, indent=2)
        handle.write('\n')
    return entry, {'endian': recipe['endian'], 'comp': comp}


# ---------------------------------------------------------------------------
# REA run
# ---------------------------------------------------------------------------
def rea_env(arm):
    env = dict(os.environ)
    home_bin = os.path.join(os.path.expanduser('~'), '.local', 'bin')
    env['REA_UNBLOB_COMMAND'] = os.path.join(home_bin, 'unblob')
    if arm == 'before':
        want = os.path.realpath(home_bin)
        kept = [p for p in env.get('PATH', '').split(os.pathsep)
                if p and os.path.realpath(p) != want]
        env['PATH'] = os.pathsep.join(kept)
    return env


def run_rea(entry, scratch, keep_extraction):
    """Run REA once for one carrier and store its envelope."""
    carrier = os.path.join(OUT_DIR, entry['carrier'])
    work = os.path.join(scratch, f'rea-{entry["id"]}')
    os.makedirs(work)
    outdir = os.path.join(work, 'out')  # REA refuses an existing output dir
    cmd = ['npx', '-y', REA_PACKAGE, 'extract-firmware', '--format', 'json',
           '--full-output', carrier, outdir]
    proc = subprocess.run(cmd, cwd=work, env=rea_env(entry['arm']),
                          capture_output=True, text=True)
    home_bin = os.path.join(os.path.expanduser('~'), '.local', 'bin')
    env = rea_env(entry['arm'])
    record = {'id': entry['id'], 'class': entry['class'], 'arm': entry['arm'],
              'exit_code': proc.returncode,
              'rea_argv': [REA_PACKAGE, 'extract-firmware'] + cmd[3:6] + [entry['carrier'], '$out'],
              'unblob_command': env['REA_UNBLOB_COMMAND'],
              'home_bin_on_path': any(os.path.realpath(p) == os.path.realpath(home_bin)
                                      for p in env.get('PATH', '').split(os.pathsep) if p)}
    stdout = proc.stdout.strip()
    full = None
    if stdout:
        try:
            full = json.loads(stdout)
        except json.JSONDecodeError:
            start = stdout.find('{')
            if start >= 0:
                try:
                    full = json.loads(stdout[start:])
                except json.JSONDecodeError:
                    full = None
    if not isinstance(full, dict) or 'data' not in full:
        record['error'] = 'no JSON envelope on stdout'
        record['stdout_head'] = stdout[:400]
        record['stderr_head'] = proc.stderr[-400:]
    else:
        dest = os.path.join(OUT_DIR, entry['id'])
        with open(os.path.join(dest, 'envelope.json'), 'w', encoding='utf-8') as handle:
            json.dump(full['data'], handle, indent=2)
            handle.write('\n')
        with open(os.path.join(dest, 'rea-full.json'), 'w', encoding='utf-8') as handle:
            json.dump(full, handle, indent=2)
            handle.write('\n')
        data = full['data']
        subject = (data.get('subject') or {}).get('digest') or {}
        record['ok'] = full.get('ok')
        record['subject_sha256'] = subject.get('sha256')
        record['digest_matches_carrier'] = subject.get('sha256') == entry['sha256']
        record['duration'] = (full.get('meta') or {}).get('duration')
        normalized = data.get('normalized_result') or {}
        record['handlers'] = sorted({chunk.get('handler')
                                     for chunk in normalized.get('chunks') or []
                                     if chunk.get('handler')})
        record['gap_kinds'] = sorted({gap.get('kind')
                                      for gap in normalized.get('extraction_gaps') or []})
        record['diagnostics'] = sorted({(diag.get('report') or {}).get('__typename__')
                                        for diag in normalized.get('diagnostics') or []})
        record['files'] = len(normalized.get('files') or [])
    with open(os.path.join(OUT_DIR, entry['id'], 'run.json'), 'w',
              encoding='utf-8') as handle:
        json.dump(record, handle, indent=2)
        handle.write('\n')
    if not keep_extraction:
        shutil.rmtree(work, ignore_errors=True)
    return record


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
OUT_DIR = None


def parse_classes(value):
    wanted = [item.strip() for item in value.split(',') if item.strip()]
    if not wanted:
        raise SystemExit('--classes selected no class')
    selected = [name for name in RECIPES if name in wanted]
    unknown = [name for name in wanted if name not in RECIPES]
    if unknown:
        raise SystemExit(f'unknown class(es): {", ".join(unknown)}; '
                         f'known: {", ".join(RECIPES)}')
    return selected


def main(argv=None):
    global OUT_DIR
    parser = argparse.ArgumentParser(
        description='Deterministic R39-C2 held-out SquashFS carrier generator.')
    parser.add_argument('--seed', required=True,
                        help='hex seed (the freeze commit hash)')
    parser.add_argument('--out', required=True, help='output directory')
    parser.add_argument('--classes', default=','.join(DEFAULT_CLASSES),
                        help='comma-separated recipe names (default: the eight draft classes)')
    parser.add_argument('--run', action='store_true',
                        help='run REA extract-firmware per carrier in its arm')
    parser.add_argument('--gen', default=os.environ.get('KAIDOKU_GEN_SQUASHFS')
                        or default_writer_path(),
                        help='path to the round-37 SquashFS image writer')
    parser.add_argument('--scratch', default=os.environ.get('TMPDIR')
                        or tempfile.gettempdir(),
                        help='scratch parent for trees and REA output dirs')
    parser.add_argument('--keep-extraction', action='store_true',
                        help='keep REA output dirs in scratch (debug only)')
    args = parser.parse_args(argv)

    seed = args.seed.strip()
    if len(seed) < 16 or any(ch not in '0123456789abcdefABCDEF' for ch in seed):
        raise SystemExit(f'--seed must be at least 16 hex characters, got {seed!r}')
    selected = parse_classes(args.classes)

    OUT_DIR = os.path.abspath(args.out)
    if os.path.exists(os.path.join(OUT_DIR, 'manifest.json')):
        raise SystemExit(f'{OUT_DIR} already holds a manifest.json; use a fresh --out')
    os.makedirs(OUT_DIR, exist_ok=True)

    writer = load_writer(args.gen)
    install_block_encoder(writer)
    os.makedirs(args.scratch, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix='r39-heldout-', dir=os.path.abspath(args.scratch))
    try:
        carriers = []
        details = {}
        seq = 0
        for name in selected:
            for k in range(1, CARRIERS_PER_CLASS + 1):
                seq += 1
                entry, extra = build_carrier(seed, name, k, seq, writer, scratch, OUT_DIR)
                carriers.append(entry)
                details[entry['id']] = extra

        manifest = {
            'seed': seed,
            'generator': {
                'name': 'heldout-gen.py',
                'version': VERSION,
                'sha256': sha256_file(os.path.abspath(__file__)),
                'carriers_per_class': CARRIERS_PER_CLASS,
                # sha256 pins the stock round-37 file; block_encoder names the
                # hosting correction that actually emits the compressed blocks,
                # because the stock file alone does not identify this code.
                'writer': {
                    'name': 'gen-squashfs.py',
                    'path': writer_logical_path(os.path.abspath(args.gen)),
                    'sha256': sha256_file(os.path.abspath(args.gen)),
                    'block_encoder': BLOCK_ENCODER,
                },
            },
            'classes': selected,
            'carriers': carriers,
        }
        with open(os.path.join(OUT_DIR, 'manifest.json'), 'w', encoding='utf-8') as handle:
            json.dump(manifest, handle, indent=2)
            handle.write('\n')

        for entry in carriers:
            extra = details[entry['id']]
            print(f"{entry['id']}  {entry['class']:<26} {extra['endian']}/{extra['comp']:<4} "
                  f"{entry['arm']:<6} {entry['sha256']}")

        if args.run:
            failures = 0
            for entry in carriers:
                record = run_rea(entry, scratch, args.keep_extraction)
                status = 'err' if 'error' in record else (
                    'digest-ok' if record.get('digest_matches_carrier') else 'DIGEST-MISMATCH')
                print(f"run {entry['id']} {entry['class']:<26} exit={record['exit_code']} "
                      f"handlers={','.join(record.get('handlers') or []) or '-'} "
                      f"gaps={','.join(record.get('gap_kinds') or []) or '-'} "
                      f"diag={','.join(record.get('diagnostics') or []) or '-'} {status}")
                if 'error' in record:
                    failures += 1
            if failures:
                return 1
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
