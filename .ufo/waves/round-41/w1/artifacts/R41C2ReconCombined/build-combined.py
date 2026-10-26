#!/usr/bin/env python3
"""Build DEV-ONLY combined-gap SquashFS carriers for R41-C2 recon.

Nothing here is frozen; the carriers are synthetic and live in scratch.

Reused frozen round-40 code (both files are extracted from the lane revision by
``--frozen``; their sha256 is printed and recorded in the pin file):

  * ``gen-squashfs.py``      ``build_image(tree, out, mode, comp)`` -- the writer;
  * ``heldout-gen-v2.py``    ``build_tree`` / ``tree_oracle`` /
                             ``corruption_partial`` -- the recipe that picks the
                             damaged block from parsed inode data.

ONE variable is changed against the frozen ``partial-body-failure`` recipe: the
fill byte written over the selected compressed block (``--fill``).  The round-40
frozen recipe writes ``0x00``, and MH-4
(.ufo/waves/round-40/w2/R40W2MistakeHunt.md section 3) measured that a
large-compressed-block zero stream is absorbed by the decompressor fallback and
extracts clean.  The block *selector* is the frozen one: ``corruption_partial``
is called, which zeroes the block and reports ``block_offset`` / ``block_length``
/ ``file_size`` / ``path`` / ``files``; this script then rewrites the same byte
range with the requested fill.  With ``--fill 00`` the frozen bytes are
reproduced exactly, so the absorb case can be demonstrated on the same tree.

Usage
-----
  python3 -I -B build-combined.py --frozen DIR --out DIR \
      --name c-gzip-ff-intree --comp gzip --fill ff --links in-tree \
      [--content pattern|stream] [--tree-seed STR]

Writes ``OUT/<name>/{carrier.sqsh,tree.json,recipe.json}`` and prints a JSON
summary line.  Deterministic for a given (--comp, --fill, --links, --content,
--tree-seed).
"""

import argparse
import contextlib
import hashlib
import io
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_module(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest().upper()


SEMI_ALPHABET = 16      # symbols; ~4 bits/byte -> a block that still compresses


def semi_bytes(material, size):
    """Semi-compressible bytes: 16-symbol stream (compressed ~40-55% of size).

    The frozen writer stores a block *uncompressed* when compression does not
    shrink it, so a fully incompressible stream produces no compressed data
    block and the frozen selector refuses.  A 16-symbol alphabet keeps the block
    compressed while making its compressed length large (thousands of bytes),
    which is the regime MH-4 found a zero fill absorbed in.
    """
    import hashlib
    out = bytearray()
    counter = 0
    while len(out) < size:
        digest = hashlib.sha256(material + b':' + str(counter).encode()).digest()
        out.extend(b for b in digest)
        counter += 1
    return bytes(b & 0x0f for b in out[:size])


def overprint_semi(root, oracle, seed):
    """Rewrite every regular file with semi-compressible bytes of the same size."""
    for entry in oracle['files']:
        path = os.path.join(root, entry['path'])
        with open(path, 'wb') as handle:
            handle.write(semi_bytes(seed.encode() + b':' + entry['path'].encode(),
                                    entry['size']))
        entry['sha256'] = sha256_file(path).lower()


def write_tree(root, link_kinds, content, seed):
    """Deterministic tree through the frozen ``build_tree``.

    The frozen builder draws file sizes and names from the RNG, so the tree is
    the frozen builder's tree; only the stream material differs by name.
    """
    rng = random.Random(int(hashlib.sha256(seed.encode()).hexdigest()[:16], 16))
    material = ('r41-c2-recon:' + seed).encode()
    dirs, files, symlinks = GEN2.build_tree(rng, material, root,
                                            tuple(link_kinds), content)
    return GEN2.tree_oracle(root, dirs, files, symlinks)


def build(args):
    dest = os.path.join(args.out, args.name)
    os.makedirs(dest, exist_ok=True)
    tree = os.path.join(dest, 'tree')
    if os.path.isdir(tree):
        import shutil
        shutil.rmtree(tree)
    os.makedirs(tree)

    build_content = 'pattern' if args.content == 'semi' else args.content
    oracle = write_tree(tree, [k for k in args.links.split(',') if k],
                        build_content, args.tree_seed)
    if args.content == 'semi':
        overprint_semi(tree, oracle, args.tree_seed)

    image = os.path.join(dest, 'carrier.sqsh')
    with contextlib.redirect_stdout(io.StringIO()):
        SQW.build_image(tree, image, 'be', args.comp)

    if args.fill == 'none':
        recipe = {
            'name': args.name,
            'writer': 'tools/round-40/gen-squashfs.py build_image',
            'recipe': 'undamaged control (--fill none)',
            'endian': 'be', 'compression': args.comp, 'content': args.content,
            'links': [k for k in args.links.split(',') if k],
            'fill': 'none', 'tree_seed': args.tree_seed,
            'image_sha256': sha256_file(image),
            'image_bytes': os.path.getsize(image),
            'damage': None,
        }
        with open(os.path.join(dest, 'recipe.json'), 'w', encoding='utf-8') as handle:
            json.dump(recipe, handle, indent=2, sort_keys=True)
            handle.write('\n')
        with open(os.path.join(dest, 'tree.json'), 'w', encoding='utf-8') as handle:
            json.dump({'oracle': oracle, 'links': recipe['links']},
                      handle, indent=2, sort_keys=True)
            handle.write('\n')
        print(json.dumps({k: recipe[k] for k in
                          ('name', 'compression', 'content', 'links', 'fill',
                           'image_sha256', 'image_bytes')}, sort_keys=True))
        return 0

    with open(image, 'rb') as handle:
        payload = bytearray(handle.read())
    report = {}
    try:
        payload = GEN2.corruption_partial(payload, 'be', report)
    except Exception as exc:                     # noqa: BLE001 - reported
        raise SystemExit('%s: frozen block selector refused: %s'
                         % (args.name, exc))
    fill = int(args.fill, 16)
    start, length = report['block_offset'], report['block_length']
    if fill != 0:
        payload[start:start + length] = bytes([fill]) * length
    with open(image, 'wb') as handle:
        handle.write(bytes(payload))

    recipe = {
        'name': args.name,
        'writer': 'tools/round-40/gen-squashfs.py build_image',
        'recipe': 'round-40 heldout-gen-v2 corruption_partial (frozen selector)',
        'endian': 'be',
        'compression': args.comp,
        'content': args.content,
        'links': [k for k in args.links.split(',') if k],
        'fill': args.fill,
        'tree_seed': args.tree_seed,
        'image_sha256': sha256_file(image),
        'image_bytes': os.path.getsize(image),
        'damage': report,
    }
    with open(os.path.join(dest, 'recipe.json'), 'w', encoding='utf-8') as handle:
        json.dump(recipe, handle, indent=2, sort_keys=True)
        handle.write('\n')
    with open(os.path.join(dest, 'tree.json'), 'w', encoding='utf-8') as handle:
        json.dump({'oracle': oracle, 'links': recipe['links']},
                  handle, indent=2, sort_keys=True)
        handle.write('\n')
    print(json.dumps({k: recipe[k] for k in
                      ('name', 'compression', 'content', 'links', 'fill',
                       'image_sha256', 'image_bytes')}
                     | {'damage': report}, sort_keys=True))
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frozen', required=True,
                        help='dir holding gen-squashfs.py and heldout-gen-v2.py')
    parser.add_argument('--out', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--comp', choices=['gzip', 'xz'], default='gzip')
    parser.add_argument('--fill', default='ff')
    parser.add_argument('--links', default='in-tree',
                        help='comma list of escaping,in-tree (empty = none)')
    parser.add_argument('--content', choices=['pattern', 'stream', 'semi'],
                        default='pattern')
    parser.add_argument('--tree-seed', default='r41-c2-recon')
    args = parser.parse_args()

    global GEN2, SQW
    SQW = load_module(os.path.join(args.frozen, 'gen-squashfs.py'), 'sqw')
    GEN2 = load_module(os.path.join(args.frozen, 'heldout-gen-v2.py'), 'gen2')
    print('# frozen gen-squashfs.py %s' % sha256_file(
        os.path.join(args.frozen, 'gen-squashfs.py')))
    print('# frozen heldout-gen-v2.py %s' % sha256_file(
        os.path.join(args.frozen, 'heldout-gen-v2.py')))
    return build(args)


if __name__ == '__main__':
    sys.exit(main())
