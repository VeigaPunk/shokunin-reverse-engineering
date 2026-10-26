#!/usr/bin/env python3
"""build-envelope.py - turn a vectors-v4draft.json vector into a synthetic REA
extract-firmware envelope data object readable by BOTH frozen round-41 tools
(sqfs-triage-v3.py features() and indep-eval-v3.py features()).

Realization choices (documented for the seats):
  * every handler in H sits on its own chunk (the frozen v3 interpreter collects
    H from chunks only; the evaluator unions gaps too - the v4 interpreter must
    union, see report G6);
  * extractor-failure gaps carry the HF handlers, one gap per handler; HF=[]
    with extractor-failure in G emits ONE gap with handler null (the A1
    fallback HF = F is then computed by the reader, not encoded);
  * dependencies ride on the missing-extractor-dependency gap;
  * BE != n/a emits one diagnostics[].report.command argv naming sasquatch with
    -be/-le; BE = n/a emits no diagnostics at all;
  * SR = yes emits one diagnostics[].report.__typename__ MaliciousSymlinkRemoved
    (nested under report, the shape both frozen tools read).

CLI: --vectors FILE [--ids V1,V2] --outdir DIR
"""

import argparse
import json
import os
import sys


def envelope_from_vector(vec):
    f = vec['features']
    nr = {
        'chunks': [{'handler': h, 'start_offset': 0, 'end_offset': 4096}
                   for h in f['H']],
        'extraction_gaps': [],
        'files': ['published/file-%04d' % i for i in range(f['P'])],
    }
    for kind in sorted(f['G']):
        if kind == 'extractor-failure':
            if f['HF']:
                for fh in sorted(f['HF']):
                    nr['extraction_gaps'].append({'kind': kind, 'handler': fh})
            else:
                nr['extraction_gaps'].append({'kind': kind, 'handler': None})
        elif kind == 'missing-extractor-dependency':
            nr['extraction_gaps'].append({'kind': kind, 'handler': None,
                                          'dependencies': sorted(f['D'])})
        else:
            nr['extraction_gaps'].append({'kind': kind, 'handler': None,
                                          'dependencies': []})
    diags = []
    if f['BE'] != 'n/a':
        argv = ['sasquatch', '-be' if f['BE'] == 'yes' else '-le',
                '-no-exit-code', '-f', '-d', 'outdir', 'chunk.bin']
        diags.append({'report': {'__typename__': 'ExtractCommandFailedReport',
                                 'command': argv, 'exit_code': 1}})
    if f['SR'] == 'yes':
        diags.append({'report': {'__typename__': 'MaliciousSymlinkRemoved',
                                 'path': 'escaped/link'}})
    if diags:
        nr['diagnostics'] = diags
    return {'operation': f['OP'], 'provider': {'id': f['PR']},
            'normalized_result': nr}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--vectors', required=True)
    parser.add_argument('--ids')
    parser.add_argument('--outdir', required=True)
    ns = parser.parse_args(argv)
    with open(ns.vectors, 'r', encoding='utf-8') as handle:
        doc = json.load(handle)
    os.makedirs(ns.outdir, exist_ok=True)
    wanted = set(ns.ids.split(',')) if ns.ids else None
    written = []
    for vec in doc['vectors']:
        if wanted and vec['id'] not in wanted:
            continue
        path = os.path.join(ns.outdir, '%s.envelope.json' % vec['id'])
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump(envelope_from_vector(vec), handle, indent=1, sort_keys=True)
        written.append(path)
    print('wrote %d envelopes to %s' % (len(written), ns.outdir))
    return 0


if __name__ == '__main__':
    sys.exit(main())
