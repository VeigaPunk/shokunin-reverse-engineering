#!/usr/bin/env python3
"""R40-C2 held-out SquashFS carrier generator, table-v2 classes (round 40).

Every byte this script emits is a pure function of ``--seed`` (the freeze commit
hash).  Structure comes from ``random.Random(int(seed[:16], 16) ^ (class_index
* 1000 + k))``; file contents come from a SHA-256 counter stream keyed by
(seed, class, k, relative path), so images stay reproducible across Python and
liblzma point releases rather than only inside one interpreter build.  No clock,
no ``os.urandom``, no directory-listing order, no host-specific input.

Two replicates per class.  Within a class the replicates differ only in
non-decision features: ``k == 1`` is gzip and ``k == 2`` is xz, the tree differs
(different RNG stream), and for the classes whose table row is
``squashfs_v4_*`` the endianness also differs (``k == 1`` big-endian, ``k == 2``
little-endian).  A class whose row pins one endianness or the AVM marker keeps
its endianness in both replicates.  The manifest records the axes.

Expected (label, action) pairs are assigned here, from the class, BEFORE any
REA run; ``--run`` only fills envelopes.  The label is fixed by the class.  The
action token is selected from one of the wave-1 candidate vocabularies
(``--actions-set``) and can be validated against the frozen
``<!-- sqfs-triage-actions: ... -->`` line (``--actions-file``); carriers do not
depend on tokens, so a rebind changes manifest.json only.

Usage
    python3 -I -B heldout-gen-v2.py --seed HEX --out DIR [--classes a,b,...] [--run]
    python3 -I -B heldout-gen-v2.py --seed HEX --selftest

``--run`` executes one REA 6.5.0 operation per carrier:
  * ``extract-firmware`` in the ``after`` arm (PATH unchanged);
  * ``extract-firmware`` in the ``before`` arm (``$HOME/.local/bin`` removed
    from the child PATH, so neither sasquatch binary resolves);
  * the ``out-of-domain`` class runs ``out_of_domain_run``, which invokes a
    non-extract-firmware operation (``--ood-op``, default
    ``inspect-firmware-regions``) on the same carrier.

Layout
    DIR/manifest.json        {seed, generator, action_vocabulary, classes, carriers:[...]}
    DIR/<id>/carrier.sqsh
    DIR/<id>/tree.json       oracle: directories, regular files (path, sha256, size), symlinks
    DIR/<id>/envelope.json   (--run) the `data` object of the CLI envelope
    DIR/<id>/rea-full.json   (--run) the whole {ok, data, meta} envelope
    DIR/<id>/run.json        (--run) arm/operation, exit code, digest binding, shape summary

With ``--gzip`` the two envelope files are written as ``.json.gz`` (mtime 0) so a
26-carrier delivery stays small; the JSON payload is unchanged.

The image writer is loaded by path (``--gen``, default tools/round-39/gen-squashfs.py).
Its block encoder is replaced as in round 39: the round-37 prototype writes bare
LZMA2 streams that sasquatch 4.5.1 rejects, and advertises comp id 2 (LZMA)
instead of 4 (xz).

Damage recipes (``bytes -> bytes``; the input image is never mutated).  The
reader below is a pure-stdlib SquashFS 4.0 parser; every offset comes from the
image itself, so a recipe works for both endiannesses and both compressors.
``corrupt_partial`` and ``empty_tree`` are the hooks the sibling recon seats
(R40C2ReconPartial, R40C2ReconEmpty) specified; the implementations here are
self-contained so a frozen carrier set never depends on a wave artifact.
"""
from __future__ import annotations

import argparse
import contextlib
import gzip
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

# A run without -B must not drop tools/round-39/__pycache__ into the lane.
sys.dont_write_bytecode = True

VERSION = 'r40-c2-v2'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789_-'
CARRIERS_PER_CLASS = 2
REA_PACKAGE = 'rea-agents@6.5.0'
BLOCK_ENCODER = ('gzip=zlib level 9, comp_id 1; xz=.xz container/CRC32, '
                 'comp_id 4 (replaces stock raw-LZMA2 and comp_id 2)')
DEFAULT_OOD_OP = 'inspect-firmware-regions'

# ---------------------------------------------------------------------------
# Action maps (closed vocabularies).  The (label, action) pair is scored against
# the frozen table, so the token must be the table's token, not a paraphrase.
# Wave 1 produced three candidate vocabularies for the same 11 labels.  The
# generator carries each verbatim; the freeze selects one with --actions-set, or
# validates the selected map against the frozen
# `<!-- sqfs-triage-actions: ... -->` line with --actions-file.  Carriers never
# depend on tokens: rebinding changes manifest.json only (no carrier bytes).
#   tabledraft    artifacts/R40C2TableDraft/block.md:30 (the table block's line)
#   interp        artifacts/R40C2Interp/v2-block.md:2 (interpreter prototype)
#   actionreview  artifacts/R40C2ActionReview/actions.md sections 1-2
# The 12th label `unclassified` is the domain guard / no-match answer in all
# three; the out-of-domain carrier's pair is (unclassified, none).
# ---------------------------------------------------------------------------
ACTION_SETS = {
    'tabledraft': {
        'clean': 'accept',
        'clean-empty': 'accept',
        'escaping-symlink-removed': 'expect-removed',
        'in-tree-symlink-metadata': 'resolve-unpublished',
        'mixed-symlinks': 'expect-removed-and-unpublished',
        'dep-missing-be': 'install-sasquatch-v4be',
        'dep-missing-le': 'install-sasquatch',
        'avm-marker-be-dropped': 'rerun-with-be-wrapper',
        'body-extractor-failure': 'keep-failure-evidence',
        'partial-body-failure': 'accept-partial-published',
        'no-squashfs-chunk': 'check-superblock',
        'unclassified': 'none',
    },
    'interp': {
        'clean': 'none',
        'clean-empty': 'confirm-empty',
        'escaping-symlink-removed': 'expect-link-absent',
        'in-tree-symlink-metadata': 'count-gap',
        'mixed-symlinks': 'audit-symlinks',
        'dep-missing-be': 'install-extractor-be',
        'dep-missing-le': 'install-extractor-le',
        'avm-marker-be-dropped': 'wrap-extractor-be',
        'body-extractor-failure': 'preserve-failure',
        'partial-body-failure': 'salvage-partial',
        'no-squashfs-chunk': 'inspect-input',
        'unclassified': 'none',
    },
    'actionreview': {
        'clean': 'match-oracle',
        'clean-empty': 'match-oracle',
        'escaping-symlink-removed': 'expect-absent',
        'in-tree-symlink-metadata': 'count-gaps',
        'mixed-symlinks': 'expect-absent-and-count-gaps',
        'dep-missing-be': 'install-dependency-rerun',
        'dep-missing-le': 'install-dependency-rerun',
        'avm-marker-be-dropped': 'wrapper-be-then-remove',
        'body-extractor-failure': 'keep-evidence-quarantine',
        'partial-body-failure': 'keep-evidence-match-published',
        'no-squashfs-chunk': 'check-superblock',
        # R40C2ActionReview row 0 is a guard row: label unclassified, action
        # `not-comparable`; `none` stays the no-match default of its table.
        'unclassified': 'not-comparable',
    },
}
DEFAULT_ACTION_SET = 'tabledraft'
NO_MATCH_TOKEN = 'none'
ACTIONS_LINE_TAG = '<!-- sqfs-triage-actions:'
ACTIONS = ACTION_SETS[DEFAULT_ACTION_SET]
ACTION_SET_NAME = DEFAULT_ACTION_SET
ACTION_SOURCE = None

# ---------------------------------------------------------------------------
# Recipe table.  ``label`` is the label the frozen interpreter must produce and
# the key into ACTIONS for the action half of the pair; the recipe key is the
# generator-side ``class``.
#
#   endian      le | be | avm | k   (k: k==1 be, k==2 le)
#               avm = BE magic with mkfs_time := bytes_used, the marker that
#               makes unblob drop ``-be`` (a marker-only standard-BE body, NOT
#               the genuine AVM layout -- that is R40-C1's ground)
#   arm         after | before  (PATH arm for the REA extract-firmware run)
#   comp        'k' (k==1 gzip, k==2 xz) or a fixed choice
#   tree        'random' | 'empty'
#   content     'stream' (incompressible SHA stream) | 'pattern' (compressible)
#   symlinks    kinds: 'escaping' -> relative target leaving the image root,
#               removed by unblob and reported MaliciousSymlinkRemoved with no
#               gap; 'in-tree' -> relative target resolving inside the root,
#               kept as metadata and reported as one unpublished-entry gap
#   corruption  key into CORRUPTIONS, applied to the finished image bytes
#   ood         True: run ``out_of_domain_run`` instead of extract-firmware
# ---------------------------------------------------------------------------
RECIPES = {
    'clean-be': dict(label='clean', endian='be',
                     arm='after', comp='k', tree='random', content='stream',
                     symlinks=(), corruption=None),
    'clean-le': dict(label='clean', endian='le',
                     arm='after', comp='k', tree='random', content='stream',
                     symlinks=(), corruption=None),
    # A clean image with zero regular files: P=0 with no gap.  Distinct from
    # both ``clean`` (the v1 row requires P>0) and ``no-squashfs-chunk``
    # (handler present here).  R39-CL3 D2.
    'clean-empty': dict(label='clean-empty',
                        endian='k', arm='after', comp='k', tree='empty',
                        content='stream', symlinks=(), corruption=None),
    'escaping-symlink-removed': dict(
        label='escaping-symlink-removed',
        endian='k', arm='after', comp='k', tree='random', content='stream',
        symlinks=('escaping',), corruption=None),
    'in-tree-symlink-metadata': dict(
        label='in-tree-symlink-metadata',
        endian='k', arm='after', comp='k', tree='random', content='stream',
        symlinks=('in-tree',), corruption=None),
    # Both link kinds in one image: the escaping link is removed (SR=yes) and
    # every in-tree link adds one unpublished-entry gap, so a table whose
    # escaping row matches on SR alone reports the wrong action.  R39-CL2.
    'mixed-symlinks': dict(label='mixed-symlinks',
                           endian='k',
                           arm='after', comp='k', tree='random',
                           content='stream', symlinks=('escaping', 'in-tree'),
                           corruption=None),
    'dep-missing-be': dict(label='dep-missing-be',
                           endian='be',
                           arm='before', comp='k', tree='random',
                           content='stream', symlinks=(), corruption=None),
    'dep-missing-le': dict(label='dep-missing-le',
                           endian='le',
                           arm='before', comp='k', tree='random',
                           content='stream', symlinks=(), corruption=None),
    'avm-marker-be-dropped': dict(label='avm-marker-be-dropped',
                                  endian='avm', arm='after', comp='k',
                                  tree='random', content='stream', symlinks=(),
                                  corruption=None),
    # The extractor ran with -be and failed before writing any file.
    'body-extractor-failure': dict(label='body-extractor-failure',
                                   endian='be', arm='after', comp='k',
                                   tree='random', content='pattern',
                                   symlinks=(), corruption='zero-id-table'),
    # The extractor ran with -be, wrote every file before the damaged one, then
    # failed: published files > 0.  R39-CL3 D1.
    'partial-body-failure': dict(label='partial-body-failure',
                                 endian='be', arm='after', comp='k',
                                 tree='random', content='pattern',
                                 symlinks=(), corruption='partial'),
    'no-squashfs-chunk': dict(label='no-squashfs-chunk',
                              endian='k',
                              arm='after', comp='k', tree='random',
                              content='stream', symlinks=(),
                              corruption='bad-major'),
    # A non-extract-firmware operation on a SquashFS carrier:
    # inspect_firmware_regions / provider binwalk.  The domain guard must
    # refuse it instead of reading it as a squashfs outcome.  R39-CL1.
    'out-of-domain': dict(label='unclassified',
                          endian='k', arm='after', comp='k', tree='random',
                          content='stream', symlinks=(), corruption=None,
                          ood=True),
}

DEFAULT_CLASSES = tuple(RECIPES)


# ---------------------------------------------------------------------------
# image writer
# ---------------------------------------------------------------------------
WRITER_LOGICAL = os.path.join('tools', 'round-39', 'gen-squashfs.py')


def default_writer_path():
    """Locate gen-squashfs.py: tools/round-39 beside us, then any ancestor's tools/round-39."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [os.path.join(here, '..', 'round-39', 'gen-squashfs.py')]
    cursor = here
    for _ in range(8):
        candidates.append(os.path.join(cursor, 'tools', 'round-39', 'gen-squashfs.py'))
        parent = os.path.dirname(cursor)
        if parent == cursor:
            break
        cursor = parent
    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.normpath(candidate)
    return os.path.normpath(candidates[0])


def writer_logical_path(resolved):
    """Stable manifest value: the lane-relative path when the writer lives under tools/round-39."""
    marker = WRITER_LOGICAL + os.sep
    if resolved.endswith(marker[:-1]):
        return WRITER_LOGICAL
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.relpath(resolved, here)


def load_writer(path):
    if not os.path.isfile(path):
        raise SystemExit(f'image writer not found: {path}')
    spec = importlib.util.spec_from_file_location('r39_gen_squashfs', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def install_block_encoder(module):
    """Replace the round-37 block encoder and compression-id table (round-39 fix)."""

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
# pure-stdlib SquashFS 4.0 reader (damage recipes only)
# ---------------------------------------------------------------------------
META_UNCOMPRESSED = 1 << 15
BLOCK_UNCOMPRESSED = 1 << 24
INVALID_FRAG = 0xFFFFFFFF
MAGIC = {b'hsqs': '<', b'sqsh': '>'}
COMP_IDS = {1: 'gzip', 2: 'lzma', 3: 'lzo', 4: 'xz', 5: 'lz4', 6: 'zstd'}
TYPE_DIR, TYPE_FILE, TYPE_SYMLINK = 1, 2, 3
TYPE_LDIR, TYPE_LFILE, TYPE_LSYMLINK = 8, 9, 10


class SqfsError(Exception):
    pass


def _decompress(raw, comp):
    if comp == 'gzip':
        try:
            return zlib.decompress(raw)
        except zlib.error as exc:
            raise SqfsError('gzip metadata block: %s' % exc)
    if comp in ('xz', 'lzma'):
        try:
            return lzma.decompress(raw)
        except (lzma.LZMAError, EOFError) as exc:
            raise SqfsError('%s metadata block: %s' % (comp, exc))
    raise SqfsError('compression id %r not supported by this reader' % comp)


class _Stream:
    """Sequential reader over a metadata stream."""

    def __init__(self, meta, ptr, offset):
        self.meta = meta
        self.ptr = ptr
        self.off = offset

    def take(self, count):
        data = self.meta.read(self.ptr, self.off, count)
        self.off += count
        return data

    def u16(self):
        return struct.unpack(self.meta.e + 'H', self.take(2))[0]

    def u32(self):
        return struct.unpack(self.meta.e + 'I', self.take(4))[0]


class _Meta:
    """Concatenated metadata blocks of the inode or directory table."""

    def __init__(self, img, base, e, comp):
        self.img = img
        self.base = base
        self.e = e
        self.comp = comp
        self.cache = {}

    def block(self, ptr):
        hit = self.cache.get(ptr)
        if hit is not None:
            return hit
        if not 0 <= ptr <= len(self.img) - 2:
            raise SqfsError('metadata block pointer %d outside the image' % ptr)
        header = struct.unpack_from(self.e + 'H', self.img, self.base + ptr)[0]
        size = header & ~META_UNCOMPRESSED
        raw = self.img[self.base + ptr + 2:self.base + ptr + 2 + size]
        if len(raw) != size:
            raise SqfsError('metadata block at %d truncated' % ptr)
        data = raw if header & META_UNCOMPRESSED else _decompress(raw, self.comp)
        hit = (data, size + 2)
        self.cache[ptr] = hit
        return hit

    def read(self, ptr, offset, count):
        out = bytearray()
        cur, off = ptr, offset
        while len(out) < count:
            data, on_disk = self.block(cur)
            if off > len(data):
                raise SqfsError('metadata offset %d beyond block at %d' % (off, cur))
            out += data[off:off + (count - len(out))]
            if len(out) >= count:
                break
            cur, off = cur + on_disk, 0
        return bytes(out)


class _Sqfs:
    def __init__(self, buf):
        if len(buf) < 96:
            raise SqfsError('image is %d bytes, shorter than the superblock' % len(buf))
        magic = bytes(buf[:4])
        if magic not in MAGIC:
            raise SqfsError('unknown magic %r' % magic)
        self.buf = buf
        self.e = MAGIC[magic]
        (self.comp_id,) = struct.unpack_from(self.e + 'H', buf, 20)
        self.major, self.minor = struct.unpack_from(self.e + 'HH', buf, 28)
        (self.root_inode, self.bytes_used, self.id_table_start,
         _xattr, self.inode_table_start, self.dir_table_start,
         _frag, _export) = struct.unpack_from(self.e + 'QQQQQQQQ', buf, 32)
        if (self.major, self.minor) != (4, 0):
            raise SqfsError('not a SquashFS 4.0 image: %d.%d' % (self.major, self.minor))
        self.comp = COMP_IDS.get(self.comp_id)
        if self.comp is None:
            raise SqfsError('compression id %d unknown' % self.comp_id)
        (self.block_size,) = struct.unpack_from(self.e + 'I', buf, 12)
        self.inodes = _Meta(buf, self.inode_table_start, self.e, self.comp)
        self.dirs = _Meta(buf, self.dir_table_start, self.e, self.comp)
        self._cache = {}

    def inode(self, ref):
        hit = self._cache.get(ref)
        if hit is not None:
            return hit
        st = _Stream(self.inodes, ref >> 16, ref & 0xFFFF)
        kind = st.u16()
        node = {'ref': ref, 'type': kind}
        st.take(6)  # mode, uid, gid
        st.take(8)  # mtime, inode_number
        if kind in (TYPE_DIR, TYPE_LDIR):
            if kind == TYPE_DIR:
                node['start_block'] = st.u32()
                st.take(4)  # nlink
                node['file_size'] = st.u16()
                node['offset'] = st.u16()
            else:
                st.take(4)  # nlink
                node['file_size'] = st.u32()
                node['start_block'] = st.u32()
                st.take(8)  # parent, i_count
                node['offset'] = st.u16()
        elif kind in (TYPE_FILE, TYPE_LFILE):
            if kind == TYPE_FILE:
                node['start_block'] = st.u32()
                node['fragment'] = st.u32()
                st.take(4)  # frag offset
                node['file_size'] = st.u32()
            else:
                node['start_block'] = st.take(8)
                node['start_block'] = struct.unpack(self.e + 'Q', node['start_block'])[0]
                node['file_size'] = struct.unpack(self.e + 'Q', st.take(8))[0]
                st.take(8)  # sparse
                st.take(8)  # nlink, fragment
                st.take(4)  # frag offset
                node['fragment'] = INVALID_FRAG
            count = (node['file_size'] + self.block_size - 1) // self.block_size \
                if node['fragment'] == INVALID_FRAG else node['file_size'] // self.block_size
            if count > 8192:
                raise SqfsError('inode %#x declares %d data blocks' % (ref, count))
            node['block_list'] = [st.u32() for _ in range(count)]
        self._cache[ref] = node
        return node

    def entries(self, node):
        st = _Stream(self.dirs, node['start_block'], node['offset'])
        header = st.take(12)
        count, start = struct.unpack(self.e + 'II', header[:8])
        out = []
        for _ in range(count + 1):
            offset, _delta, typ, name_size = struct.unpack(
                self.e + 'HhHH', st.take(8))
            name = st.take(name_size + 1).decode('utf-8', 'surrogateescape')
            out.append({'name': name, 'type': typ, 'ref': (start << 16) | offset})
        return out

    def walk(self):
        order = []

        def visit(path, ref):
            node = self.inode(ref)
            for entry in self.entries(node):
                child = posixpath.join(path, entry['name']) if path else entry['name']
                order.append((child, entry['type'], entry['ref']))
                if entry['type'] in (TYPE_DIR, TYPE_LDIR):
                    visit(child, entry['ref'])

        visit('', self.root_inode)
        return order

    def files(self):
        """Regular files with the absolute on-disk span of each data block."""
        out = []
        for path, typ, ref in self.walk():
            if typ not in (TYPE_FILE, TYPE_LFILE):
                continue
            node = self.inode(ref)
            pos = node['start_block']
            blocks = []
            for field in node['block_list']:
                on_disk = field & ~BLOCK_UNCOMPRESSED
                if on_disk == 0:
                    blocks.append({'offset': pos, 'length': 0,
                                   'compressed': False, 'sparse': True})
                    continue
                blocks.append({'offset': pos, 'length': on_disk,
                               'compressed': not (field & BLOCK_UNCOMPRESSED),
                               'sparse': False})
                pos += on_disk
            out.append({'path': path, 'ref': ref, 'size': node['file_size'],
                        'blocks': blocks})
        return out


# ---------------------------------------------------------------------------
# corruptions: bytearray(clean image) -> bytearray(corrupted image)
# ---------------------------------------------------------------------------
def corruption_zero_id_table(payload, endian):
    """Zero the id-table metadata block (header + payload).

    Superblock field id_table_start is a u64 at offset 48; it points just past
    the id metadata block at the 8-byte id table index, and that index holds the
    metadata block's start.  sasquatch reads the id table during filesystem
    init, before any file is written, so it fails with P=0:
    ``read_id_table: failed to read id table block``.
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


def corruption_bad_major(payload, endian):
    """s_major 4 -> 9: no v1..v4 handler pattern matches, so the image stays an
    unknown chunk and REA publishes no squashfs chunk."""
    prefix = '>' if endian in ('be', 'avm') else '<'
    major, minor = struct.unpack(prefix + 'HH', bytes(payload[28:32]))
    if (major, minor) != (4, 0):
        raise ValueError(f'unexpected squashfs version {major}.{minor}')
    payload[28:32] = struct.pack(prefix + 'HH', 9, 0)
    return payload


def corruption_partial(payload, endian, report=None):
    """Zero the last compressed data block of the last-extracted regular file.

    The target is chosen from parsed inode data, not a fixed offset: the file
    order is the directory-scan order (what unsquashfs walks), the file is the
    last one in that order owning a compressed, non-sparse block, and within it
    the last such block.  Zeros are an invalid gzip header and an invalid .xz
    stream, so the decompressor fails on that block after every earlier file
    has been written -- the extractor fails with published files > 0.
    """
    image = _Sqfs(bytes(payload))
    entries = image.files()
    if len(entries) < 2:
        raise SqfsError('partial recipe needs at least 2 regular files, found %d'
                        % len(entries))
    target = None
    for entry in reversed(entries):
        for block in reversed(entry['blocks']):
            if block['compressed'] and not block['sparse']:
                target = (entry, block)
                break
        if target:
            break
    if target is None:
        raise SqfsError('no compressed data block in any regular file')
    entry, block = target
    if entry['path'] == entries[0]['path']:
        raise SqfsError('partial recipe would damage the first-extracted file '
                        '%r; every file must be compressible' % entry['path'])
    start, length = block['offset'], block['length']
    if start + length > image.bytes_used:
        raise SqfsError('data block %d+%d beyond bytes_used %d'
                        % (start, length, image.bytes_used))
    payload[start:start + length] = bytes(length)
    if report is not None:
        report.update({'recipe': 'partial', 'path': entry['path'],
                       'block_offset': start, 'block_length': length,
                       'file_size': entry['size'], 'files': len(entries)})
    return payload


CORRUPTIONS = {
    'zero-id-table': lambda payload, endian, report: corruption_zero_id_table(
        payload, endian),
    'bad-major': lambda payload, endian, report: corruption_bad_major(
        payload, endian),
    'partial': corruption_partial,
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


def pattern_bytes(material, size):
    """Compressible content: a unique 48-byte head followed by a letter cycle.

    The head keeps every file's sha256 distinct; the cycle keeps every data
    block compressed, which the partial recipe needs.
    """
    head = stream_bytes(material + b':head', 48)
    if size <= len(head):
        return head[:size]
    cycle = b'ABCDEFGH'
    body = (cycle * ((size - len(head)) // len(cycle) + 1))[:size - len(head)]
    return head + body


def token(rng, low=3, high=9):
    return ''.join(rng.choice(ALPHABET) for _ in range(rng.randint(low, high)))


def unique_name(rng, taken):
    while True:
        name = token(rng)
        if name not in taken:
            taken.add(name)
            return name


def _write_file(root, rel, material, size, content):
    data = pattern_bytes(material, size) if content == 'pattern' \
        else stream_bytes(material, size)
    with open(os.path.join(root, rel), 'wb') as handle:
        handle.write(data)


def build_tree(rng, material, root, link_kinds, content='stream'):
    """Create one random tree.

    Returns (dirs, files, symlinks): directory paths, regular-file paths and
    [(relative path, link target, kind)] -- all relative posix strings.
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
        _write_file(root, rel, material + b':' + rel.encode(),
                    rng.randrange(0, 20001), content)
        files.append(rel)

    symlinks = []
    for kind in link_kinds:
        if kind == 'escaping':
            name = unique_name(rng, taken[''])
            target = '../' + token(rng)
            os.symlink(target, os.path.join(root, name))
            symlinks.append((name, target, 'escaping'))
        elif kind == 'in-tree':
            target_rel = rng.choice([f for f in files if os.path.getsize(
                os.path.join(root, f)) > 0] or files)
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


def empty_tree(rng, material, root):
    """A valid image holding directories only: zero regular files, no links.

    One empty directory keeps the image a real tree (round-39 measured the
    same shape as ``full-be-dirempty-gzip``: handler present, no gap, P=0).
    """
    rel = token(rng)
    os.makedirs(os.path.join(root, rel))
    return [rel], [], []


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
def variant(recipe, k):
    """Resolve the per-replicate non-decision features."""
    endian = recipe['endian']
    if endian == 'k':
        endian = 'be' if k == 1 else 'le'
    comp = recipe['comp']
    if comp == 'k':
        comp = 'gzip' if k == 1 else 'xz'
    return endian, comp


def replicate_variation():
    return ['compression', 'tree-shape', 'endianness-where-the-class-allows']


def build_carrier(seed, name, k, seq, writer, scratch, out_dir):
    """Build one carrier; return (manifest entry, build detail)."""
    recipe = RECIPES[name]
    class_index = list(RECIPES).index(name)
    rng = random.Random(int(seed[:16], 16) ^ (class_index * 1000 + k))
    material = f'{seed}:{name}:{k}'.encode()
    endian, comp = variant(recipe, k)

    work = os.path.join(scratch, f'build-{seq:02d}')
    tree = os.path.join(work, 'tree')
    os.makedirs(tree)
    if recipe['tree'] == 'empty':
        dirs, files, symlinks = empty_tree(rng, material, tree)
    else:
        dirs, files, symlinks = build_tree(rng, material, tree,
                                           recipe['symlinks'], recipe['content'])
    oracle = tree_oracle(tree, dirs, files, symlinks)

    image = os.path.join(work, 'carrier.sqsh')
    with contextlib.redirect_stdout(io.StringIO()):
        writer.build_image(tree, image, endian, comp)

    corruption_report = None
    if recipe['corruption']:
        with open(image, 'rb') as handle:
            payload = bytearray(handle.read())
        report = {}
        payload = CORRUPTIONS[recipe['corruption']](payload, endian, report)
        corruption_report = {'recipe': recipe['corruption'], **report}
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
        'action': ACTIONS[recipe['label']],
        'arm': 'ood' if recipe.get('ood') else recipe['arm'],
        'endian': endian,
        'compression': comp,
        'tree': recipe['tree'],
        'content': recipe['content'],
        'symlinks': list(recipe['symlinks']),
        'corruption': recipe['corruption'],
        'damage': corruption_report,
        'operation': 'inspect_firmware_regions' if recipe.get('ood')
        else 'extract_firmware',
        'carrier': f'{carrier_id}/carrier.sqsh',
        'sha256': sha256_file(os.path.join(dest, 'carrier.sqsh')),
    }
    with open(os.path.join(dest, 'tree.json'), 'w', encoding='utf-8') as handle:
        json.dump({'seed': seed, 'class': name, 'id': carrier_id,
                   'endian': endian, 'compression': comp,
                   'label': recipe['label'],
                   'action': ACTIONS[recipe['label']],
                   'oracle': oracle}, handle, indent=2)
        handle.write('\n')
    return entry, {'endian': endian, 'comp': comp,
                   'corruption': corruption_report,
                   'files': len(files), 'symlinks': len(symlinks)}


# ---------------------------------------------------------------------------
# REA runs
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


def _envelope_parts(full):
    """(data object or None, subject sha256, shape summary) from a CLI envelope."""
    if not isinstance(full, dict) or not isinstance(full.get('data'), dict):
        return None, None, {}
    data = full['data']
    normalized = data.get('normalized_result') or {}
    shape = {
        'operation': data.get('operation'),
        'provider': (data.get('provider') or {}).get('id'),
        'handlers': sorted({chunk.get('handler')
                            for chunk in normalized.get('chunks') or []
                            if chunk.get('handler')}),
        'failed_chunks': sorted({chunk.get('handler')
                                 for chunk in normalized.get('chunks') or []
                                 if chunk.get('extraction_failed') and chunk.get('handler')}),
        'gap_kinds': sorted({gap.get('kind')
                             for gap in normalized.get('extraction_gaps') or []
                             if gap.get('kind')}),
        'gap_dependencies': sorted({dep
                                    for gap in normalized.get('extraction_gaps') or []
                                    for dep in (gap.get('dependencies') or [])}),
        'diagnostics': sorted({(diag.get('report') or {}).get('__typename__')
                               for diag in normalized.get('diagnostics') or []
                               if (diag.get('report') or {}).get('__typename__')}),
        'files': len(normalized.get('files') or []),
        'coverage': normalized.get('coverage'),
    }
    subject = (data.get('subject') or {}).get('digest') or {}
    return data, subject.get('sha256'), shape


def _write_envelope(entry, full, gz):
    dest = os.path.join(OUT_DIR, entry['id'])
    payloads = {'envelope': full.get('data'),
                'rea-full': full}
    for stem, obj in payloads.items():
        path = os.path.join(dest, stem + '.json')
        blob = (json.dumps(obj, indent=2) + '\n').encode('utf-8')
        if gz:
            with open(path + '.gz', 'wb') as handle:
                with gzip.GzipFile(fileobj=handle, mode='wb', mtime=0) as stream:
                    stream.write(blob)
        else:
            with open(path, 'wb') as handle:
                handle.write(blob)


def _parse_stdout(stdout):
    text = (stdout or '').strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find('{')
        if start < 0:
            return None
        try:
            return json.loads(text[start:])
        except json.JSONDecodeError:
            return None


def run_rea(entry, scratch, keep_extraction, gz):
    """Run REA extract-firmware once for one carrier and store its envelope."""
    carrier = os.path.join(OUT_DIR, entry['carrier'])
    work = os.path.join(scratch, f'rea-{entry["id"]}')
    os.makedirs(work)
    outdir = os.path.join(work, 'out')  # REA refuses an existing output dir
    cmd = ['npx', '-y', REA_PACKAGE, 'extract-firmware', '--format', 'json',
           '--full-output', carrier, outdir]
    env = rea_env(entry['arm'])
    proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True)
    home_bin = os.path.join(os.path.expanduser('~'), '.local', 'bin')
    record = {'id': entry['id'], 'class': entry['class'], 'arm': entry['arm'],
              'operation': 'extract_firmware',
              'expected_label': entry['label'],
              'expected_action': entry['action'],
              'exit_code': proc.returncode,
              'rea_argv': [REA_PACKAGE, 'extract-firmware'] + cmd[3:6]
              + [entry['carrier'], '$out'],
              'unblob_command': env['REA_UNBLOB_COMMAND'],
              'home_bin_on_path': any(
                  os.path.realpath(p) == os.path.realpath(home_bin)
                  for p in env.get('PATH', '').split(os.pathsep) if p)}
    full = _parse_stdout(proc.stdout)
    data, subject_sha, shape = _envelope_parts(full)
    if data is None:
        record['error'] = 'no JSON envelope on stdout'
        record['stdout_head'] = (proc.stdout or '').strip()[:400]
        record['stderr_head'] = (proc.stderr or '').strip()[-400:]
    else:
        _write_envelope(entry, full, gz)
        record['ok'] = full.get('ok')
        record['subject_sha256'] = subject_sha
        record['digest_matches_carrier'] = subject_sha == entry['sha256']
        record['duration'] = (full.get('meta') or {}).get('duration')
        record.update(shape)
    with open(os.path.join(OUT_DIR, entry['id'], 'run.json'), 'w',
              encoding='utf-8') as handle:
        json.dump(record, handle, indent=2)
        handle.write('\n')
    if not keep_extraction:
        shutil.rmtree(work, ignore_errors=True)
    return record


def out_of_domain_run(entry, scratch, keep_extraction, gz, operation=DEFAULT_OOD_OP):
    """Out-of-domain arm: run ``operation`` (not extract-firmware) on the carrier.

    PLACEHOLDER BINDING: the operation is the CLI ``--ood-op`` value and is
    stored in the manifest under ``out_of_domain.operation`` so the freeze can
    rebind it without touching this function.  The default,
    ``inspect-firmware-regions``, returns a complete Evidence envelope with
    ``operation == "inspect_firmware_regions"`` and ``provider.id == "binwalk"``
    on a SquashFS carrier -- a valid envelope that is not an unblob
    extract-firmware outcome.  It takes no output directory.
    """
    carrier = os.path.join(OUT_DIR, entry['carrier'])
    work = os.path.join(scratch, f'ood-{entry["id"]}')
    os.makedirs(work)
    cmd = ['npx', '-y', REA_PACKAGE, operation, '--format', 'json',
           '--full-output', carrier]
    env = rea_env('after')
    proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True)
    record = {'id': entry['id'], 'class': entry['class'], 'arm': 'ood',
              'operation': operation,
              'expected_label': entry['label'],
              'expected_action': entry['action'],
              'exit_code': proc.returncode,
              'rea_argv': [REA_PACKAGE, operation, '--format', 'json',
                           '--full-output', entry['carrier']],
              'unblob_command': env['REA_UNBLOB_COMMAND']}
    full = _parse_stdout(proc.stdout)
    data, subject_sha, shape = _envelope_parts(full)
    if data is None:
        # An error envelope ({ok:false, error:...}) is itself out-of-domain
        # material, but the frozen set should hold structured evidence: record
        # the failure loudly instead of silently accepting it.
        record['error'] = 'no Evidence envelope on stdout'
        record['stdout_head'] = (proc.stdout or '').strip()[:400]
        record['stderr_head'] = (proc.stderr or '').strip()[-400:]
    else:
        _write_envelope(entry, full, gz)
        record['ok'] = full.get('ok')
        record['subject_sha256'] = subject_sha
        record['digest_matches_carrier'] = subject_sha == entry['sha256']
        record['duration'] = (full.get('meta') or {}).get('duration')
        record.update(shape)
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
    unknown = [name for name in wanted if name not in RECIPES]
    if unknown:
        raise SystemExit(f'unknown class(es): {", ".join(unknown)}; '
                         f'known: {", ".join(RECIPES)}')
    return [name for name in RECIPES if name in wanted]


def actions_line(path):
    """Read the frozen `<!-- sqfs-triage-actions: ... -->` token line."""
    with open(path, encoding='utf-8') as handle:
        for line in handle:
            if ACTIONS_LINE_TAG in line:
                body = line.split(ACTIONS_LINE_TAG, 1)[1]
                body = body.split('-->', 1)[0]
                tokens = body.split()
                if tokens:
                    return tokens
    raise SystemExit(f'no {ACTIONS_LINE_TAG} token line in {path}')


def check_action_tokens(tokens, path):
    """The manifest may only emit tokens the bound table line declares.

    ``none`` is the interpreter's no-match default, not a row token, so a line
    that lists only the row tokens is still consistent with a map that answers
    ``unclassified`` with ``none``.
    """
    want = set(ACTIONS.values()) - {NO_MATCH_TOKEN}
    have = set(tokens) - {NO_MATCH_TOKEN}
    if want == have:
        return
    missing = sorted(want - have)
    extra = sorted(have - want)
    raise SystemExit(
        f'action vocabulary mismatch against {path}: the selected '
        f'--actions-set {ACTION_SET_NAME!r} emits {missing} which the line does '
        f'not declare, and the line declares {extra} which the manifest does not '
        f'use.  Select the --actions-set whose tokens match the frozen line, or '
        f'edit ACTION_SETS; carriers are unaffected.')


def build_set(seed, classes, writer, out_dir, scratch):
    """Build every carrier and the manifest into ``out_dir``."""
    os.makedirs(out_dir, exist_ok=True)
    carriers, details, seq = [], {}, 0
    for name in classes:
        for k in range(1, CARRIERS_PER_CLASS + 1):
            seq += 1
            entry, extra = build_carrier(seed, name, k, seq, writer, scratch, out_dir)
            carriers.append(entry)
            details[entry['id']] = extra
    manifest = {
        'seed': seed,
        'generator': {
            'name': 'heldout-gen-v2.py',
            'version': VERSION,
            'sha256': sha256_file(os.path.abspath(__file__)),
            'carriers_per_class': CARRIERS_PER_CLASS,
            'writer': {
                'name': 'gen-squashfs.py',
                'path': writer_logical_path(os.path.abspath(WRITER_PATH)),
                'sha256': sha256_file(os.path.abspath(WRITER_PATH)),
                'block_encoder': BLOCK_ENCODER,
            },
        },
        'action_vocabulary': sorted(set(ACTIONS.values())),
        'action_set': ACTION_SET_NAME,
        'action_source': ACTION_SOURCE,
        'label_actions': dict(ACTIONS),
        'replicate_variation': replicate_variation(),
        'out_of_domain': {'operation': OOD_OP,
                          'label': RECIPES['out-of-domain']['label'],
                          'action': ACTIONS[RECIPES['out-of-domain']['label']]},
        'classes': list(classes),
        'carriers': carriers,
    }
    with open(os.path.join(out_dir, 'manifest.json'), 'w', encoding='utf-8') as handle:
        json.dump(manifest, handle, indent=2)
        handle.write('\n')
    for entry in carriers:
        extra = details[entry['id']]
        corruption = extra['corruption'] or {}
        detail = (f"files={extra['files']} links={extra['symlinks']}"
                  + (f" damage={corruption.get('path')}@{corruption.get('block_offset')}"
                     if corruption else ''))
        print(f"{entry['id']}  {entry['class']:<26} {entry['endian']}/{entry['compression']:<4} "
              f"{entry['arm']:<6} {entry['label']:<26} {entry['action']:<32} "
              f"{entry['sha256']}  {detail}")
    return manifest, carriers


WRITER_PATH = None
OOD_OP = DEFAULT_OOD_OP


def run_selftest(seed, writer, scratch_root):
    """Same seed twice -> identical manifest and carriers; other seed -> different."""
    work = tempfile.mkdtemp(prefix='r40-selftest-', dir=os.path.abspath(scratch_root))
    try:
        results = {}
        for tag, use_seed in (('a', seed), ('b', seed),
                              ('c', seed[::-1])):
            out = os.path.join(work, f'det-{tag}')
            os.makedirs(out)
            local_scratch = tempfile.mkdtemp(prefix=f'build-{tag}-', dir=work)
            try:
                manifest, carriers = build_set(use_seed, list(DEFAULT_CLASSES),
                                               writer, out, local_scratch)
            finally:
                shutil.rmtree(local_scratch, ignore_errors=True)
            results[tag] = {
                'manifest': sha256_file(os.path.join(out, 'manifest.json')),
                'carriers': [c['sha256'] for c in carriers],
                'ids': [c['id'] for c in carriers],
            }
        checks = []

        def check(name, ok, detail):
            checks.append((name, ok, detail))
            print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")

        a, b, c = results['a'], results['b'], results['c']
        check('same seed: manifest bytes identical', a['manifest'] == b['manifest'],
              f"{a['manifest'][:16]} vs {b['manifest'][:16]}")
        check('same seed: every carrier sha256 identical', a['carriers'] == b['carriers'],
              f"{len(a['carriers'])} carriers")
        check('same seed: carrier ids identical', a['ids'] == b['ids'],
              f"{a['ids'][0]}..{a['ids'][-1]}")
        check('different seed: manifest differs', a['manifest'] != c['manifest'],
              f"{a['manifest'][:16]} vs {c['manifest'][:16]}")
        check('different seed: every carrier differs',
              all(x != y for x, y in zip(a['carriers'], c['carriers'])),
              f"{sum(x != y for x, y in zip(a['carriers'], c['carriers']))}"
              f"/{len(a['carriers'])} differ")
        check('replicate variation: no class has two identical carriers',
              len(set(a['carriers'])) == len(a['carriers']),
              f"{len(set(a['carriers']))} distinct of {len(a['carriers'])}")
        failed = [name for name, ok, _ in checks if not ok]
        if failed:
            print(f'\n{len(failed)} selftest check(s) failed: {", ".join(failed)}')
            return 1
        print(f'\nall {len(checks)} selftest checks passed')
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    global OUT_DIR, WRITER_PATH, OOD_OP, ACTIONS, ACTION_SET_NAME, ACTION_SOURCE
    parser = argparse.ArgumentParser(
        description='Deterministic R40-C2 held-out SquashFS carrier generator '
                    '(table-v2 classes).')
    parser.add_argument('--seed', required=True,
                        help='hex seed (the freeze commit hash)')
    parser.add_argument('--out', help='output directory (required unless --selftest)')
    parser.add_argument('--classes', default=','.join(DEFAULT_CLASSES),
                        help='comma-separated recipe names (default: all draft classes)')
    parser.add_argument('--run', action='store_true',
                        help='run REA per carrier in its arm')
    parser.add_argument('--ood-op', default=DEFAULT_OOD_OP,
                        help='non-extract-firmware REA operation for the '
                             'out-of-domain class (default: %(default)s)')
    parser.add_argument('--actions-set', default=DEFAULT_ACTION_SET,
                        choices=sorted(ACTION_SETS),
                        help='action tokens for the (label, action) pairs '
                             '(default: %(default)s)')
    parser.add_argument('--actions-file',
                        help='file holding the frozen `<!-- sqfs-triage-actions: ... -->` '
                             'line; the selected set must equal its tokens')
    parser.add_argument('--gen', default=os.environ.get('KAIDOKU_GEN_SQUASHFS')
                        or default_writer_path(),
                        help='path to the SquashFS image writer (round-39 gen-squashfs.py)')
    parser.add_argument('--scratch', default=os.environ.get('TMPDIR')
                        or tempfile.gettempdir(),
                        help='scratch parent for trees, REA output dirs and the selftest')
    parser.add_argument('--gzip', action='store_true',
                        help='write envelope.json.gz / rea-full.json.gz (mtime 0)')
    parser.add_argument('--keep-extraction', action='store_true',
                        help='keep REA output dirs in scratch (debug only)')
    parser.add_argument('--selftest', action='store_true',
                        help='determinism selftest (no --out needed)')
    args = parser.parse_args(argv)

    seed = args.seed.strip()
    if len(seed) < 16 or any(ch not in '0123456789abcdefABCDEF' for ch in seed):
        raise SystemExit(f'--seed must be at least 16 hex characters, got {seed!r}')

    WRITER_PATH = os.path.abspath(args.gen)
    OOD_OP = args.ood_op
    ACTIONS = ACTION_SETS[args.actions_set]
    ACTION_SET_NAME = args.actions_set
    if args.actions_file:
        tokens = actions_line(args.actions_file)
        check_action_tokens(tokens, args.actions_file)
        ACTION_SOURCE = {'file': os.path.abspath(args.actions_file),
                         'sha256': sha256_file(args.actions_file),
                         'tokens': tokens}
    writer = load_writer(WRITER_PATH)
    install_block_encoder(writer)
    os.makedirs(args.scratch, exist_ok=True)

    if args.selftest:
        return run_selftest(seed, writer, args.scratch)

    if not args.out:
        raise SystemExit('--out is required unless --selftest')
    selected = parse_classes(args.classes)
    OUT_DIR = os.path.abspath(args.out)
    if os.path.exists(os.path.join(OUT_DIR, 'manifest.json')):
        raise SystemExit(f'{OUT_DIR} already holds a manifest.json; use a fresh --out')
    scratch = tempfile.mkdtemp(prefix='r40-heldout-',
                               dir=os.path.abspath(args.scratch))
    try:
        manifest, carriers = build_set(seed, selected, writer, OUT_DIR, scratch)
        print(f"manifest {os.path.join(OUT_DIR, 'manifest.json')} "
              f"{len(carriers)} carriers, {len({c['label'] for c in carriers})} labels, "
              f"{len({(c['label'], c['action']) for c in carriers})} decisions")
        if args.run:
            failures = 0
            for entry in carriers:
                if RECIPES[entry['class']].get('ood'):
                    record = out_of_domain_run(entry, scratch, args.keep_extraction,
                                               args.gzip, OOD_OP)
                else:
                    record = run_rea(entry, scratch, args.keep_extraction, args.gzip)
                if 'error' in record:
                    failures += 1
                    print(f"run {entry['id']} {entry['class']:<26} ERROR "
                          f"{record.get('error')} exit={record['exit_code']}")
                    continue
                print(f"run {entry['id']} {entry['class']:<26} exit={record['exit_code']} "
                      f"op={record.get('operation')} prov={record.get('provider')} "
                      f"handlers={','.join(record.get('handlers') or []) or '-'} "
                      f"gaps={','.join(record.get('gap_kinds') or []) or '-'} "
                      f"diag={','.join(record.get('diagnostics') or []) or '-'} "
                      f"files={record.get('files')} "
                      f"{'digest-ok' if record.get('digest_matches_carrier') else 'DIGEST-MISMATCH'}")
            if failures:
                return 1
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
