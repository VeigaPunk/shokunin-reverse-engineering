#!/usr/bin/env python3
"""Fabricate an REA 6.5.0 extract-firmware receipt for a C1 carrier WITHOUT running REA.

Inputs a forger has: the frozen oracle.tsv + nonregular.tsv of the carrier, the
frozen carriers.json entry (pin, length), and ONE committed receipt of a
different carrier as a schema/convention template. Nothing else.
"""
import hashlib, json, sys

TEMPLATE = sys.argv[1]
CARRIER_ID = sys.argv[2]
PIN = sys.argv[3]
LENGTH = int(sys.argv[4])
ORACLE = sys.argv[5]
NONREG = sys.argv[6]
SUBJECT_NAME = sys.argv[7] if len(sys.argv) > 7 else 'carrier.sqsh'
OUTDIR = sys.argv[8] if len(sys.argv) > 8 else '/fast/scratch/hyaku/kaidoku-r40/fab/extract'
PERFILE_HASH = bool(int(sys.argv[9])) if len(sys.argv) > 9 else False
CHUNK_DIR = 'firmware.bin_extract'

env = json.load(open(TEMPLATE))
oracle = []
for line in open(ORACLE).read().splitlines():
    if not line.strip():
        continue
    f = line.split('\t')
    oracle.append((f[0], f[1], int(f[2])))
nonreg = []
for line in open(NONREG).read().splitlines():
    if not line.strip():
        continue
    f = line.split('\t')
    nonreg.append((f[0], f[1], f[2] if len(f) > 2 else ''))

nr = env['normalized_result']
files = []
pub = 0
for rel, sha, size in oracle:
    pub += size
    files.append({
        'relative_path': '%s/%s' % (CHUNK_DIR, rel),
        'path': '%s/%s/%s' % (OUTDIR, CHUNK_DIR, rel),
        'size': size, 'sha256': sha, 'reported_sha256': None,
        'mime_type': None, 'analysis_depth': None,
        'runtime_address': None, 'original_file_range': None,
    })
nr['files'] = files
nr['published_bytes'] = pub
nr['coverage'] = 'partial'
nr['depth_limited_paths'] = ['$output/' + CHUNK_DIR]
nr['diagnostics'] = []
nr['engine'] = dict(nr.get('engine') or {})
nr['chunks'] = [{
    'input_path': '$input', 'provider_id': '0:0',
    'range': {'offset': 0, 'length': LENGTH}, 'handler': 'squashfs_v4_be',
    'encrypted': False, 'root_file_range': {'offset': 0, 'length': LENGTH},
    'extraction_failed': False}]
nr['derivations'] = [{
    'parent_path': '$input', 'child_path': '$output/' + CHUNK_DIR,
    'provider_blob_id': '0:0', 'handler': 'squashfs_v4_be',
    'parent_file_range': {'offset': 0, 'length': LENGTH}}]
nr['selection'] = {'offset': 0, 'length': LENGTH, 'sha256': PIN}
gaps = [{'kind': 'depth-limited', 'input_path': '$output/' + CHUNK_DIR,
         'relative_path': None, 'handler': None, 'provider_id': None,
         'range': None, 'root_file_range': None, 'dependencies': [],
         'continuation_id': '0' * 64}]
unpub = []
for rel, kind, target in nonreg:
    if kind == 'symlink':
        gaps.append({'kind': 'unpublished-entry',
                     'input_path': '$output/%s/%s' % (CHUNK_DIR, rel),
                     'relative_path': '%s/%s' % (CHUNK_DIR, rel),
                     'handler': None, 'provider_id': None, 'range': None,
                     'root_file_range': None, 'dependencies': [],
                     'continuation_id': '0' * 64})
        unpub.append({'relative_path': '%s/%s' % (CHUNK_DIR, rel),
                      'kind': 'symlink', 'link_target': target})
nr['extraction_gaps'] = gaps
nr['unpublished_entries'] = unpub
nr['output_directory'] = OUTDIR

env['parameters'] = {'path': '/fab/%s' % SUBJECT_NAME,
                     'output_directory': OUTDIR,
                     'max_depth': 1, 'max_output_bytes': 268435456,
                     'max_output_files': 10000}
env['subject'] = {'name': SUBJECT_NAME, 'digest': {'sha256': PIN},
                  'local_path': '/fab/' + SUBJECT_NAME, 'format': 'file',
                  'architecture': None}
env['locations'] = [{'kind': 'file-offset-range', 'start': 0, 'end': LENGTH}]
env['operation'] = 'extract_firmware'
env['predicate_type'] = 'rea.analysis'
env['provider'] = {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'}
# raw_result: only convention-sensitive field of the projection is the HashReport
# key (task path). Faithful shape = one HashReport on the staged carrier.
env['raw_result'] = {
    'execution': {'stdout': {'text': '', 'bytes': 0, 'observedBytes': 0},
                  'stderr': {'text': '', 'bytes': 0, 'observedBytes': 0},
                  'exit_code': 0, 'signal': None, 'command': '/x/unblob', 'args': []},
    'report': [
        {'task': {'path': OUTDIR + '/extracted/' + CHUNK_DIR, 'depth': 1,
                  'blob_id': '0:0', 'is_multi_file': False},
         'reports': [{'__typename__': 'StatReport',
                      'path': OUTDIR + '/extracted/' + CHUNK_DIR,
                      'size': 4096, 'is_dir': True, 'is_file': False,
                      'is_link': False, 'link_target': None}],
         'subtasks': []},
        {'task': {'path': OUTDIR + '/firmware.bin', 'depth': 0,
                  'blob_id': '0:0', 'is_multi_file': False},
         'reports': [{'__typename__': 'StatReport', 'path': OUTDIR + '/firmware.bin',
                      'size': LENGTH, 'is_dir': False, 'is_file': True,
                      'is_link': False, 'link_target': None},
                     {'__typename__': 'FileMagicReport'},
                     {'__typename__': 'HashReport', 'md5': None, 'sha1': None,
                      'sha256': PIN},
                     {'__typename__': 'ChunkReport', 'size': LENGTH}],
         'subtasks': []},
    ],
    'version_execution': {'stdout': {'text': '26.6.4\n', 'bytes': 7,
                                     'observedBytes': 7},
                          'stderr': {'text': '', 'bytes': 0, 'observedBytes': 0},
                          'exit_code': 0, 'signal': None,
                          'command': '/x/unblob', 'args': ['--version']},
}
if PERFILE_HASH:
    for rel, sha, size in oracle:
        # a forger who also extracted with sasquatch could put real md5/sha1 here
        env['raw_result']['report'].append({
            'task': {'path': OUTDIR + '/extracted/%s/%s' % (CHUNK_DIR, rel),
                     'depth': 1, 'blob_id': '0:0', 'is_multi_file': False},
            'reports': [{'__typename__': 'HashReport',
                         'md5': 'MD5-' + rel, 'sha1': 'SHA1-' + rel,
                         'sha256': sha}],
            'subtasks': []})
print(json.dumps({'data': env}, indent=1))
