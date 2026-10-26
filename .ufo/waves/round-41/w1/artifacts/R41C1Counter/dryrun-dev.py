#!/usr/bin/env python3
"""Build the round-41 pre-freeze dry-run lane in a scratch clone (dev only).

Round-41 has no committed carriers yet, so the C1 counter's dry run (QUALITY 83)
is scored on the round-40 evidence: this driver writes a round-41-shaped frozen
table set (`.ufo/waves/round-41/c1/{carriers.json,gap-rule.json}` plus
`corpus/evidence/round-41/c1/<id>/` tables) whose ids V3, V4, L3, L4 name the
round-40 carriers V1, V2, L1, L2, then commits the receipts that descend from
that freeze so the counter's freshness clause can hold.

Two adaptations are unavoidable and are the only edits made to the round-40
receipts (`--adapt-provenance`):

  parameters.output_directory + normalized_result.output_directory
      moved from the round-40 scratch segment to a round-41 one, because the
      counter's run_provenance_ok clause requires `/kaidoku-r41/`; the
      projection and the rerun clause ignore it.
  evidence_id
      re-minted with the frozen rea-agents 6.5.0 rule (tools/round-27/
      xpin-attribute.mjs) because `parameters` is inside that rule's
      semanticProjection.

Without --adapt-provenance the receipts are copied verbatim, which is what shows
that run_provenance_ok still refuses a round-40 receipt.

Usage:
  dryrun-dev.py --src LANE --clone CLONE --pkg65 REA_ROOT [--adapt-provenance]
Prints one JSON object. Mutates only CLONE (asserted to be a git toplevel).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

DEV = {'V3': 'V1', 'V4': 'V2', 'L3': 'L1', 'L4': 'L2'}
SRC_DIR = 'corpus/evidence/round-40/c1'
DST_DIR = 'corpus/evidence/round-41/c1'
XPIN_REL = 'tools/round-27/xpin-attribute.mjs'
NEW_OUT = '/fast/scratch/hyaku/kaidoku-r41/dev/%s/extract'


def run(argv, cwd=None, check=True, env=None):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, env=env)
    if check and p.returncode != 0:
        raise SystemExit('%r failed rc=%d: %s'
                         % (argv, p.returncode, p.stderr.decode()[:800]))
    return p


def git(clone, *args):
    return run(['git', '-C', clone, *args])


def toplevel_ok(clone):
    top = run(['git', '-C', clone, 'rev-parse', '--show-toplevel']
              ).stdout.decode().strip()
    return os.path.realpath(top) == os.path.realpath(clone)


def commit(clone, message):
    git(clone, 'add', '-A')
    git(clone, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
        'commit', '-qm', message, '--allow-empty')
    return git(clone, 'rev-parse', 'HEAD').stdout.decode().strip()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--clone', required=True)
    ap.add_argument('--pkg65', required=True)
    ap.add_argument('--src-rev', default='HEAD',
                    help='revision of --src holding the round-40 tables')
    ap.add_argument('--adapt-provenance', action='store_true')
    ap.add_argument('--override', action='append', default=[],
                    metavar='ID=CARRIER',
                    help='dev carrier bytes for one id (changes its pin)')
    ap.add_argument('--override-receipt', action='append', default=[],
                    metavar='ID=RECEIPT',
                    help='REA CLI envelope or after-receipt JSON for one id')
    ap.add_argument('--oracle', action='append', default=[], metavar='ID=TSV',
                    help='oracle.tsv for one id instead of the round-40 one')
    ap.add_argument('--nonregular', action='append', default=[], metavar='ID=TSV',
                    help='nonregular.tsv for one id instead of the round-40 one')
    a = ap.parse_args(argv)
    a.override = dict(p.split('=', 1) for p in a.override)
    a.override_receipt = dict(p.split('=', 1) for p in a.override_receipt)
    a.oracle = dict(p.split('=', 1) for p in a.oracle)
    a.nonregular = dict(p.split('=', 1) for p in a.nonregular)
    if not toplevel_ok(a.clone):
        raise SystemExit('clone is not its own git toplevel: ' + a.clone)

    spec40 = json.loads(run(['git', '-C', a.src, 'show',
                             '%s:.ufo/waves/round-40/c1/carriers.json' % a.src_rev]
                            ).stdout)
    by_id = {c['id']: c for c in spec40['carriers']}
    gaprule40 = json.loads(run(['git', '-C', a.src, 'show',
                                '%s:.ufo/waves/round-40/c1/gap-rule.json' % a.src_rev]
                               ).stdout)
    gaprule = {'claim': 'R41-C1'}
    for key in ('allowed', 'required', 'structural'):
        if key in gaprule40:
            gaprule[key] = gaprule40[key]

    out = {'ids': {}, 'adapt_provenance': a.adapt_provenance}
    carriers = []
    dst = os.path.join(a.clone, DST_DIR)
    os.makedirs(dst, exist_ok=True)
    for new, old in DEV.items():
        src = by_id[old]
        d = os.path.join(dst, new)
        os.makedirs(d, exist_ok=True)
        for name in ('oracle.tsv', 'nonregular.tsv'):
            shutil.copyfile(os.path.join(a.src, SRC_DIR, old, name),
                            os.path.join(d, name))
        for key, over in (('oracle.tsv', a.oracle), ('nonregular.tsv', a.nonregular)):
            if new in over:
                shutil.copyfile(over[new], os.path.join(d, key))
                out.setdefault('overrides', {}).setdefault(new, {})[key] = over[new]
        entry = {'id': new, 'sha256': src['sha256'], 'kind': src['kind'],
                 'oracle': '%s/%s/oracle.tsv' % (DST_DIR, new),
                 'nonregular': '%s/%s/nonregular.tsv' % (DST_DIR, new)}
        if 'external' in src:
            entry['external'] = src['external']
        else:
            shutil.copyfile(os.path.join(a.src, SRC_DIR, old, 'carrier.sqsh'),
                            os.path.join(d, 'carrier.sqsh'))
            entry['path'] = '%s/%s/carrier.sqsh' % (DST_DIR, new)
            entry['build'] = src.get('build', 'copied from round-40 ' + old)
        if new in a.override:
            # a dev carrier with a measured chunk shape (e.g. trailing padding):
            # the bytes change, so the pin and the receipt must change with them
            cpath = a.override[new]
            entry.pop('external', None)
            shutil.copyfile(cpath, os.path.join(d, 'carrier.sqsh'))
            entry['path'] = '%s/%s/carrier.sqsh' % (DST_DIR, new)
            entry['sha256'] = sha256_bytes(open(cpath, 'rb').read())
            entry['kind'] = 'lane-built'
            entry['build'] = 'dev override from %s' % os.path.basename(cpath)
        carriers.append(entry)
        out['ids'][new] = {'round40_id': old, 'sha256': entry['sha256'],
                           'kind': entry['kind'],
                           'external': 'external' in entry,
                           'override': new in a.override}
    spec = {'claim': 'R41-C1', 'target': 4, 'projection': 'plus-extractor',
            'rea_parameters': {'max_depth': 1}, 'carriers': carriers}
    for rel, doc in (('.ufo/waves/round-41/c1/carriers.json', spec),
                     ('.ufo/waves/round-41/c1/gap-rule.json', gaprule)):
        p = os.path.join(a.clone, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w') as fh:
            json.dump(doc, fh, indent=1)
            fh.write('\n')
    out['freeze'] = commit(a.clone, 'dev freeze: round-41-shaped tables')

    # receipts, in a commit that descends from the freeze
    xpin = os.path.join(a.clone, XPIN_REL)
    envelopes = []
    for new, old in DEV.items():
        if new in a.override_receipt:
            raw = json.load(open(a.override_receipt[new]))
            if isinstance(raw.get('data'), dict):
                raw = raw['data']              # an REA CLI envelope, not a receipt
        else:
            raw = json.loads(run(['git', '-C', a.src, 'show',
                                  '%s:%s/%s/after.json' % (a.src_rev, SRC_DIR, old)]
                                 ).stdout)
        if a.adapt_provenance:
            raw['parameters']['output_directory'] = NEW_OUT % new
            raw['normalized_result']['output_directory'] = NEW_OUT % new
            p = os.path.join(a.clone, 'work-%s.json' % new)
            with open(p, 'w') as fh:
                json.dump({'data': raw}, fh)
            res = run(['node', xpin, '--pkg65', a.pkg65, '--pkg67', a.pkg65, p]
                      ).stdout.decode().strip().split('\t')
            raw['evidence_id'] = res[2]
            os.remove(p)
            out['ids'][new]['minted_evidence_id'] = res[2]
        else:
            out['ids'][new]['verbatim_output_directory'] = \
                raw['parameters']['output_directory']
        envelopes.append((new, raw))
    for new, raw in envelopes:
        p = os.path.join(dst, new, 'after.json')
        with open(p, 'w') as fh:
            json.dump(raw, fh)
    out['rev'] = commit(a.clone, 'dev receipts: round-40 after-receipts')
    out['receipt_sha256'] = {
        new: sha256_bytes(open(os.path.join(dst, new, 'after.json'), 'rb').read())
        for new, _ in envelopes}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
