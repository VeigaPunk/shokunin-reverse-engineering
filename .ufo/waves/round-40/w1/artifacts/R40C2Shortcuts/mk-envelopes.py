#!/usr/bin/env python3
"""mk-envelopes.py — synthetic envelope fixtures for the R40-C2 controls.

These are JSON fixtures built from the FEATURE definition of the v2 grammar, grounded on
real round-39 feature vectors (cited per class below).  They are not REA runs and not
carriers: no SquashFS image is built, no extractor is invoked.  Their purpose is to make
"which class does this control get wrong" a measured statement instead of a guess.

Two replicates per draft class.  The second replicate always differs in at least one
feature the intended row does not condition on (endianness of the handler, a non-decision
gap kind, published-file count inside the same bucket, or the envelope wrapper shape), so a
row that quietly keys on a replicate detail is visible.

Run: python3 -I -B mk-envelopes.py            -> writes envelopes/<class>-r1.json, -r2.json
                                              and envelopes/expected.tsv
"""

import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'envelopes')

BE = 'squashfs_v4_be'
LE = 'squashfs_v4_le'
UNBLOB = {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'}
REAWF = {'id': 'rea-workflow', 'name': 'REA composed investigation workflow', 'version': '1'}


def files(n, tag):
    return [{'path': 'out/root/f%s.txt' % i,
             'sha256': hashlib.sha256(('%s-%d' % (tag, i)).encode()).hexdigest(),
             'size': 10 + i} for i in range(n)]


def chunks(handlers, start=0, comp='gzip'):
    out = []
    for i, handler in enumerate(handlers):
        out.append({'handler': handler, 'start_offset': start + 4096 * i,
                    'end_offset': start + 4096 * (i + 1) - 1, 'extraction_failed': False,
                    'compression': comp})
    return out


def gaps(pairs):
    return [{'kind': k, 'dependencies': list(d)} for k, d in pairs]


SASQ_BE_NO_BE = ['/home/vgpnk/.local/bin/sasquatch-v4be', '-f', '-d', 'carrier', 'out']
SASQ_BE_WITH_BE = ['/home/vgpnk/.local/bin/sasquatch-v4be', '-f', '-d', '-be', 'carrier',
                   'out']
SASQ_LE = ['/home/vgpnk/.local/bin/sasquatch', '-f', '-d', 'carrier', 'out']


def diagnostics(command=None, symlink=False, stderr=None):
    out = []
    if command is not None:
        report = {'__typename__': 'ExtractorRan', 'command': command}
        if stderr:
            report['stderr'] = stderr
        out.append({'report': report})
    if symlink:
        out.append({'report': {'__typename__': 'MaliciousSymlinkRemoved',
                               'path': 'out/root/link', 'target': '../../etc/passwd'}})
    return out


# class -> (expected label, expected action, [replicate data dicts])
CLASSES = {
    # real: corpus/evidence/round-39/c1/K3,K4 (H=be, G=[], SR=no, P=4)
    'clean-be': ('clean', 'match-oracle', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE], gap_pairs=[],
             command=None, symlink=False, nfiles=4, comp='gzip'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE], gap_pairs=[],
             command=None, symlink=False, nfiles=7, comp='xz', wrapper=True),
    ]),
    # clean LE: handler differs, decision does not (row handler is `squashfs_v4_*`)
    'clean-le': ('clean', 'match-oracle', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE], gap_pairs=[],
             command=None, symlink=False, nfiles=3, comp='xz'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE], gap_pairs=[],
             command=None, symlink=False, nfiles=6, comp='gzip'),
    ]),
    # R39-CL3 D2: clean with P=0 (round-39 w2 full-be-dirempty-gzip)
    'clean-empty': ('clean-empty', 'accept-empty-root', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE], gap_pairs=[],
             command=None, symlink=False, nfiles=0, comp='gzip'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE], gap_pairs=[],
             command=None, symlink=False, nfiles=0, comp='xz'),
    ]),
    # real: corpus/evidence/round-39/c1/K1 (G=[], SR=yes, P=5)
    'escaping-symlink-removed': ('escaping-symlink-removed', 'verify-link-absence', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE], gap_pairs=[],
             command=None, symlink=True, nfiles=5, comp='gzip'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE], gap_pairs=[],
             command=None, symlink=True, nfiles=8, comp='xz'),
    ]),
    # real: corpus/evidence/round-39/c1/K2 (G={unpublished-entry}, SR=no, P=3)
    'in-tree-symlink-metadata': ('in-tree-symlink-metadata', 'count-metadata-gaps', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE],
             gap_pairs=[('unpublished-entry', [])], command=None, symlink=False,
             nfiles=3, comp='gzip'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE],
             gap_pairs=[('unpublished-entry', [])], command=None, symlink=False,
             nfiles=6, comp='xz'),
    ]),
    # R39-CL2: real K5 (P=10) and K6 (P=8): G={unpublished-entry}, SR=yes
    'mixed-symlinks': ('mixed-symlinks', 'split-mixed-links', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE],
             gap_pairs=[('unpublished-entry', [])], command=None, symlink=True,
             nfiles=10, comp='gzip'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE],
             gap_pairs=[('unpublished-entry', [])], command=None, symlink=True,
             nfiles=4, comp='xz'),
    ]),
    # real: .ufo/waves/round-39/w1/artifacts/R39C2AxisFit/env-depbe.json
    'dep-missing-be': ('dep-missing-be', 'install-sasquatch-v4be', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE],
             gap_pairs=[('missing-extractor-dependency', ['sasquatch-v4be'])],
             command=None, symlink=False, nfiles=0, comp='gzip'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE],
             gap_pairs=[('missing-extractor-dependency', ['sasquatch-v4be'])],
             command=None, symlink=False, nfiles=0, comp='xz', extra_raw=True),
    ]),
    'dep-missing-le': ('dep-missing-le', 'install-sasquatch', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE],
             gap_pairs=[('missing-extractor-dependency', ['sasquatch'])],
             command=None, symlink=False, nfiles=0, comp='gzip'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE],
             gap_pairs=[('missing-extractor-dependency', ['sasquatch'])],
             command=None, symlink=False, nfiles=0, comp='xz', wrapper=True),
    ]),
    # real: R39C2AxisFit/env-avm.json (mkfs_time == bytes_used, unblob drops -be)
    'avm-marker-be-dropped': ('avm-marker-be-dropped', 'rerun-with-be', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE],
             gap_pairs=[('extractor-failure', [])], command=SASQ_BE_NO_BE, symlink=False,
             nfiles=0, comp='gzip', stderr='Different endianess!'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE],
             gap_pairs=[('extractor-failure', [])], command=SASQ_BE_NO_BE, symlink=False,
             nfiles=0, comp='xz', stderr='Could not read id table'),
    ]),
    # real: R39C2AxisFit/env-inodeptr.json, env-rootino.json (-be ran and failed)
    'body-extractor-failure': ('body-extractor-failure', 'preserve-failing-arm', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE],
             gap_pairs=[('extractor-failure', [])], command=SASQ_BE_WITH_BE, symlink=False,
             nfiles=0, comp='gzip', stderr='Failed to read block'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE],
             gap_pairs=[('extractor-failure', [])], command=SASQ_LE, symlink=False,
             nfiles=0, comp='xz', stderr='Unrecognised inode type'),
    ]),
    # R39-CL3 D1: extractor failed AFTER publishing (round-39 w2 full-be1-xz, P>0)
    'partial-body-failure': ('partial-body-failure', 'salvage-published-files', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[BE],
             gap_pairs=[('extractor-failure', [])], command=SASQ_BE_WITH_BE, symlink=False,
             nfiles=3, comp='xz', stderr='Failed to read block 41'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[LE],
             gap_pairs=[('extractor-failure', [])], command=SASQ_LE, symlink=False,
             nfiles=5, comp='gzip', stderr='Failed to read block 7'),
    ]),
    # real: R39C2AxisFit/env-magic.json, env-trunc.json, env-bytesused.json (H=[], P=0)
    'no-squashfs-chunk': ('no-squashfs-chunk', 'probe-superblock', [
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[], gap_pairs=[],
             command=None, symlink=False, nfiles=0, comp='gzip'),
        dict(operation='extract_firmware', provider=UNBLOB, handlers=[], gap_pairs=[],
             command=None, symlink=False, nfiles=0, comp='xz', extra_raw=True),
    ]),
    # planned (b): a non-extract_firmware operation on a SquashFS carrier.
    # r1 copies the shape of the real corpus/evidence/round-26/c1/envelopes/analyze-base.json
    # (operation binary_overview, provider rea-workflow, no chunk list, no files).
    # r2 keeps provider unblob so that only the OPERATION guard can catch it.
    'out-of-domain': ('unclassified', 'none', [
        dict(operation='binary_overview', provider=REAWF, handlers=[], gap_pairs=[],
             command=None, symlink=False, nfiles=0, comp=None),
        dict(operation='binary_overview', provider=UNBLOB, handlers=[BE], gap_pairs=[],
             command=None, symlink=False, nfiles=2, comp='gzip'),
    ]),
}


def build(spec, tag):
    nr = {
        'chunks': chunks(spec['handlers'], comp=spec.get('comp') or 'gzip'),
        'extraction_gaps': gaps(spec['gap_pairs']),
        'files': files(spec['nfiles'], tag),
        'diagnostics': diagnostics(command=spec['command'], symlink=spec['symlink'],
                                   stderr=spec.get('stderr')),
        'unpublished_entries': [],
        'output_directory': 'out',
    }
    data = {'operation': spec['operation'], 'provider': spec['provider'],
            'normalized_result': nr, 'parameters': {'path': 'carrier'},
            'subject': {'local_path': 'carrier'}}
    if spec.get('extra_raw'):
        data['raw_result'] = {'note': 'dev fixture, no command recorded'}
    if spec.get('wrapper'):
        return {'ok': True, 'data': data, 'meta': {'command': 'extract-firmware'}}
    return data


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = ['class\treplicate\tfile\texpected_label\texpected_action']
    count = 0
    for cls, (label, action, specs) in CLASSES.items():
        for i, spec in enumerate(specs, start=1):
            name = '%s-r%d.json' % (cls, i)
            with open(os.path.join(OUT, name), 'w', encoding='utf-8') as handle:
                json.dump(build(spec, cls), handle, indent=1, sort_keys=True)
                handle.write('\n')
            rows.append('%s\tr%d\tenvelopes/%s\t%s\t%s' % (cls, i, name, label, action))
            count += 1
    with open(os.path.join(OUT, 'expected.tsv'), 'w', encoding='utf-8') as handle:
        handle.write('\n'.join(rows) + '\n')
    print('wrote %d envelopes for %d classes' % (count, len(CLASSES)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
