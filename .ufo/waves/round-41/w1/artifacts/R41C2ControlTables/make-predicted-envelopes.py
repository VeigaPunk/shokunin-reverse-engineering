#!/usr/bin/env python3
"""make-predicted-envelopes.py - PREDICTED fixtures for the five new v3 classes.

The round-41 held-out set does not exist before the freeze (it is generated from the
freeze hash by R41C2Gen), so the combined classes cannot be scored on real envelopes
yet.  This script derives one envelope per (class, replicate) from a COMMITTED
round-40 envelope shape, adds the gap kinds / diagnostics / depth ceiling the class
name predicts, and stamps every file with `_control_fixture` so nothing here can be
mistaken for measured evidence.

Predicted tuples (all [INFERENCE]):

  partial-in-tree      G={extractor-failure,unpublished-entry} SR=no  BE=yes P>0
  partial-mixed        G={extractor-failure,unpublished-entry} SR=yes BE=yes P>0
  depth-limited-alone  G={depth-limited}                       SR=no  BE=n/a P>0
  depth-limited-in-tree G={depth-limited,unpublished-entry}    SR=no  BE=n/a P>0
  depth-limited-mixed  G={depth-limited,unpublished-entry}     SR=yes BE=n/a P>0

Anchors: REA 6.5.0 dist/cli-runtime/cli.js :14273 builds a `depth-limited` gap from
`normalized.depth_limited_paths` (:14867) with empty dependencies, so a depth ceiling
adds one gap and no diagnostic; :14290 sorts whole gaps, so order is not a feature.
The partial recipe and the symlink representation are copied from the committed
round-40 envelopes named in `_control_fixture.derived_from`.

Usage: make-predicted-envelopes.py --heldout DIR --out DIR [--tuples FILE]
"""

import argparse
import json
import os
import sys


def load(path):
    with open(path, 'r', encoding='utf-8') as handle:
        return json.load(handle)


def gap(kind, input_path, relative_path=None, handler=None, provider_id=None):
    return {
        'kind': kind,
        'input_path': input_path,
        'relative_path': relative_path,
        'handler': handler,
        'provider_id': provider_id,
        'range': None,
        'root_file_range': None,
        'dependencies': [],
        'continuation_id': '0' * 64,
    }


def unpublished(rel):
    return gap('unpublished-entry', '$output/%s' % rel, relative_path=rel)


def depth_limited(rel):
    return gap('depth-limited', '$output/%s' % rel)


def malicious_symlink():
    return {'input_path': '$input',
            'report': {'__typename__': 'MaliciousSymlinkRemoved',
                       'severity': 'WARNING',
                       'link': '$output/firmware.bin_extract/escaped-link',
                       'target': '/outside/root/escaped-link'}}


def stamp(obj, cls, k, derived, note):
    obj['_control_fixture'] = {
        'wave': 'round-41/w1',
        'seat': 'R41C2ControlTables',
        'predicted': True,
        'class': cls,
        'replicate': k,
        'derived_from': derived,
        'why': note,
        'warning': 'predicted features only: not measured on any carrier, and the '
                   'round-41 held-out set is generated from the freeze hash',
    }
    nr = obj['normalized_result']
    nr['output_directory'] = '$scratch/out'
    obj['subject']['digest']['sha256'] = None
    obj['subject']['name'] = 'predicted-envelope.json'
    obj['parameters']['path'] = 'predicted-envelope.json'
    obj['parameters']['output_directory'] = '$scratch/out'
    obj['evidence_id'] = 'ev_predicted_%s_%d' % (cls.replace('-', '_'), k)
    return obj


def build(heldout, cls, k, variant=None):
    if cls.startswith('partial-'):
        src = 'H21' if k == 1 else 'H22'
        obj = load(os.path.join(heldout, src, 'envelope.json'))
        nr = obj['normalized_result']
        nested = 'firmware.bin_extract/_vs0u/ksvno'
        nr['extraction_gaps'].append(unpublished('%s/in-tree-link' % nested))
        nr['unpublished_entries'] = [{'relative_path': '%s/in-tree-link' % nested,
                                      'kind': 'symlink',
                                      'link_target': 'sibling-file'}]
        obj['parameters']['max_depth'] = 3
        if cls == 'partial-mixed':
            nr['diagnostics'].append(malicious_symlink())
        note = ('partial-body recipe of the committed class plus one unpublished-entry '
                'gap%s' % (' and one MaliciousSymlinkRemoved report'
                           if cls == 'partial-mixed' else ''))
        return stamp(obj, cls, k, 'corpus/evidence/round-40/c2/heldout/%s/envelope.json'
                     % src, note)
    src = 'H01' if k == 1 else 'H02'
    obj = load(os.path.join(heldout, src, 'envelope.json'))
    nr = obj['normalized_result']
    nested = 'firmware.bin_extract/_n3st/inner.sqsh'
    nr['extraction_gaps'].append(depth_limited(nested))
    nr['depth_limited_paths'] = ['$output/%s' % nested]
    nr['files'].append({'relative_path': nested,
                        'path': '$scratch/out/%s' % nested,
                        'size': 4096, 'sha256': '1' * 64, 'reported_sha256': '1' * 64,
                        'mime_type': 'application/octet-stream', 'analysis_depth': 1,
                        'runtime_address': None, 'original_file_range': None})
    obj['parameters']['max_depth'] = 1
    if cls != 'depth-limited-alone':
        nr['extraction_gaps'].append(unpublished('firmware.bin_extract/_n3st/link'))
        nr['unpublished_entries'] = [{'relative_path': 'firmware.bin_extract/_n3st/link',
                                      'kind': 'symlink', 'link_target': 'inner.sqsh'}]
    if cls == 'depth-limited-mixed':
        nr['diagnostics'].append(malicious_symlink())
    if variant == 'depth-with-extractor-failure':
        # Sensitivity variant: the nested chunk at the ceiling ALSO reports an
        # extraction failure, so G carries extractor-failure.  REA emits that gap from
        # a chunk record whose extraction_failed is true (cli.js :14266-14272), which
        # the precedence list ranks at step 4/6, BEFORE step 7.
        nested_chunk = {'input_path': '$output/%s' % nested,
                        'provider_id': '0:1', 'range': {'offset': 0, 'length': 4096},
                        'handler': 'squashfs_v4_be', 'encrypted': False,
                        'root_file_range': None, 'extraction_failed': True}
        nr['chunks'].append(nested_chunk)
        nr['extraction_gaps'].append(gap('extractor-failure', '$output/%s' % nested,
                                         handler='squashfs_v4_be', provider_id='0:1'))
        nr['diagnostics'].append({'input_path': '$output/%s' % nested,
                                  'stage': 'squashfs_v4_be',
                                  'report': {'severity': 'WARNING',
                                             'command': 'sasquatch-v4be -be -no-exit-code '
                                                        '-f -d "$output" "$input"',
                                             'stdout': '', 'stderr': '',
                                             'exit_code': 1,
                                             '__typename__': 'ExtractCommandFailedReport'}})
    note = ('outer clean squashfs plus one depth-limited gap at --max-depth 1%s'
            % ({'depth-limited-alone': '',
                'depth-limited-in-tree': ' plus one unpublished-entry gap',
                'depth-limited-mixed': ' plus one unpublished-entry gap and one '
                                       'MaliciousSymlinkRemoved report'}[cls]))
    return stamp(obj, cls, k, 'corpus/evidence/round-40/c2/heldout/%s/envelope.json'
                 % src, note)


CLASSES = ['partial-in-tree', 'partial-mixed', 'depth-limited-alone',
           'depth-limited-in-tree', 'depth-limited-mixed']


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--heldout', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tuples')
    ap.add_argument('--variant', default=None,
                    choices=(None, 'depth-with-extractor-failure'))
    ns = ap.parse_args(argv)
    os.makedirs(ns.out, exist_ok=True)
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'v3checkinterp', os.path.join(here, 'v3-check-interp.py'))
    feat_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(feat_mod)
    pspec = importlib.util.spec_from_file_location(
        'previewprecedence', os.path.join(here, 'preview-precedence.py'))
    prec = importlib.util.module_from_spec(pspec)
    pspec.loader.exec_module(prec)
    expected = prec.expected

    tuples = []
    for cls in CLASSES:
        for k in (1, 2):
            obj = build(ns.heldout, cls, k, ns.variant)
            d = os.path.join(ns.out, '%s-%d' % (cls, k))
            os.makedirs(d, exist_ok=True)
            path = os.path.join(d, 'envelope.json')
            with open(path, 'w', encoding='utf-8') as handle:
                json.dump(obj, handle, indent=1, sort_keys=True)
                handle.write('\n')
            feat = feat_mod.load_envelope(path)
            label, action, step = expected(feat)
            tuples.append({
                'class': cls, 'replicate': k, 'dir': os.path.basename(d),
                'features': {key: feat[key] for key in ('OP', 'PV', 'H', 'G', 'D',
                                                        'BE', 'SR', 'P')},
                'expected': {'label': label, 'action': action, 'step': step},
                'predicted': True,
            })
    payload = {'source': 'make-predicted-envelopes.py',
               'warning': 'predicted tuples; the round-41 held-out set is generated '
                          'from the freeze hash and has not been built',
               'tuples': tuples}
    if ns.tuples:
        with open(ns.tuples, 'w', encoding='utf-8') as handle:
            json.dump(payload, handle, indent=1, sort_keys=True)
            handle.write('\n')
    print(json.dumps([{key: t[key] for key in ('dir', 'features', 'expected')}
                      for t in tuples], indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
