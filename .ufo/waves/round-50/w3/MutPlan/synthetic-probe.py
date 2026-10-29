#!/usr/bin/env python3
"""Task 2 continued: is the F1 glob-widening load-bearing, and can it be fixed
without a cross-flip?

The held-out corpus has NO no-reader-family envelope with an extractor-failure
gap (measured: the no-reader families appear only with gaps () and
('depth-limited',)), so the corpus cannot exercise the legacy-body-failure
cross-read on a no-reader body.  This script builds SYNTHETIC envelopes in the
scratch (never in the lane) and runs the unmodified v4 evaluator against the
baseline table and each table mutant.

Synthetic shapes (one per family):
  <family>_failure   handler F, one extractor-failure gap, 0 published files
  <family>_clean     handler F, no gaps, 2 published files
"""
import copy
import hashlib
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
OUT = os.path.join(S, 'table-mut')
SYN = os.path.join(S, 'synthetic-envelopes')
EVAL = os.path.join(OUT, 'sqfs-triage-v4.py')

FAMILIES = ('squashfs_v1', 'squashfs_v2', 'squashfs_v2_nonstandard',
            'squashfs_v3', 'squashfs_v3_ddwrt', 'squashfs_v3_broadcom',
            'squashfs_v3_nonstandard', 'squashfs_v4_le')


def envelope(handler, *, fail, files):
    chunks = [{'handler': handler, 'range': {'offset': 0, 'length': 4096},
               'extraction_failed': bool(fail)}]
    gaps = []
    if fail:
        gaps.append({'kind': 'extractor-failure', 'handler': handler,
                     'relative_path': 'firmware.bin_extract/firmware.bin',
                     'dependencies': ['sasquatch']})
    pub = [{'relative_path': 'firmware.bin_extract/%s' % f, 'path': '/out/%s' % f,
            'size': 4, 'sha256': 'a' * 64} for f in files]
    return {'ok': True, 'data': {
        'operation': 'extract_firmware',
        'provider': {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'},
        'subject': {'name': 'x.bin', 'digest': {'sha256': 'b' * 64}},
        'parameters': {'output_directory': '/fast/scratch/hyaku/kaidoku-r50/x',
                       'max_depth': 3},
        'normalized_result': {'chunks': chunks, 'extraction_gaps': gaps,
                              'files': pub, 'diagnostics': []},
    }}


def main():
    os.makedirs(SYN, exist_ok=True)
    paths = []
    for fam in FAMILIES:
        for shape, kw in (('failure', {'fail': True, 'files': []}),
                          ('clean', {'fail': False, 'files': ['a.txt', 'b.txt']})):
            name = '%s_%s' % (fam, shape)
            p = os.path.join(SYN, name + '.json')
            with open(p, 'w', encoding='utf-8') as fh:
                json.dump(envelope(fam, **kw), fh, indent=1)
            paths.append(p)

    skills = [('baseline', os.path.join(OUT, 'SKILL-baseline.md')),
              ('A_legacy_narrow_bare_v123', os.path.join(OUT, 'SKILL-A_legacy_narrow_bare_v123.md')),
              ('D_v5_shaped_minimal', os.path.join(OUT, 'SKILL-D_v5_shaped_minimal.md')),
              ('E_v5_shaped_plus_F1_narrow', os.path.join(OUT, 'SKILL-E_v5_shaped_plus_F1_narrow.md'))]
    out = {}
    for tag, skill in skills:
        if not os.path.isfile(skill):
            continue
        cmd = [sys.executable, '-I', '-B', EVAL, '--skill', skill, '--json'] + paths
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        rec = {'exit_code': p.returncode,
               'stdout_sha256': hashlib.sha256(p.stdout.encode()).hexdigest(),
               'stderr_tail': p.stderr[-200:]}
        labels = {}
        if p.returncode == 0:
            doc = json.loads(p.stdout)
            for r in doc['results']:
                labels[os.path.basename(r['path'])] = [r['label'], r['action']]
        rec['labels'] = labels
        out[tag] = rec
        print('==', tag, 'exit', p.returncode)
        for k in sorted(labels):
            print('   %-46s %s' % (k, labels[k]))
    with open(os.path.join(S, 'synthetic-report.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
