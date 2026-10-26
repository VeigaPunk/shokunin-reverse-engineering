#!/usr/bin/env python3
"""MH-2 — an independence clause with no reservation namespace: the vendor scout
published a V2 pick into the shared wave-1 artifact tree, a sibling recon seat used
that same image as its "development" input, and the pick was burned before the
freeze.

The frozen clause (`plans/round-40-claims.md`, V2 row): "no REA or unblob run
touched V1 or V2 before the freeze."  The rule that was actually enforced by the
recon seat was "not V1" (`w1/R40C1ReconGaps.md` §1), so a candidate another seat had
already reserved was fair game.

Fix shape: a reservation record written when a carrier is picked, and a pre-freeze
scan that refuses any run record whose subject is a reserved candidate.

This scanner classifies each occurrence of a reserved digest in a tree:
  run    a REA envelope (`subject.digest.sha256`) or a file whose name marks a run
  unblob an unblob evidence log naming the digest
  pin    any other textual mention (a report or a pins table: informational)
Only `run`/`unblob` occurrences fail the gate.

Usage: mh2-candidate-reservation.py --reserved RIG.json --scan DIR [--scan DIR ...]
       [--json]
Exit 0 = no run record names a reserved candidate; 1 = a reserved candidate was run;
2 = usage/parse error.
Red/green (round-40 bytes):
  --reserved rig-draft-7430.json --scan w1/artifacts  -> exit 1 (env-7430-member-d1.json.gz)
  --reserved w1/../c1/carriers.json --scan w1/artifacts -> exit 0 (frozen V1/V2 clean)
"""
import argparse
import gzip
import hashlib
import json
import os
import sys


def load_rig(path):
    with open(path) as fh:
        data = json.load(fh)
    out = []
    if isinstance(data, dict) and 'carriers' in data:
        for c in data['carriers']:
            ext = c.get('external') or {}
            shas = [s for s in (ext.get('image_sha256'), ext.get('member_sha256'),
                                c.get('sha256')) if s]
            if shas:
                out.append({'id': c.get('id'), 'shas': shas})
        return out
    for c in data.get('candidates') or data:
        shas = [s for s in (c.get('image_sha256'), c.get('member_sha256'), c.get('sha256')) if s]
        if shas:
            out.append({'id': c.get('id'), 'shas': shas})
    return out


def read_bytes(path):
    try:
        with open(path, 'rb') as fh:
            head = fh.read(4)
            fh.seek(0)
            if head[:2] == b'\x1f\x8b':
                return gzip.decompress(fh.read())
            return fh.read()
    except (OSError, gzip.BadGzipFile):
        return None


def envelope_subject(raw):
    try:
        doc = json.loads(raw.decode('utf-8', 'replace'))
    except (ValueError, AttributeError):
        return None
    node = doc.get('data') if isinstance(doc, dict) and 'data' in doc else doc
    if not isinstance(node, dict):
        return None
    if 'subject' not in node or 'operation' not in node:
        return None
    digest = ((node.get('subject') or {}).get('digest') or {}).get('sha256')
    return digest, node.get('operation')


def classify(path):
    name = os.path.basename(path)
    if name.startswith('env-') or name.startswith('envelope'):
        return 'run'
    if name.startswith('unblob-'):
        return 'unblob'
    return 'pin'


def scan(reserved, dirs):
    hits = []
    for base in dirs:
        for dirpath, _dirnames, filenames in os.walk(base):
            for name in filenames:
                path = os.path.join(dirpath, name)
                raw = read_bytes(path)
                if raw is None:
                    continue
                subject = envelope_subject(raw)
                text = raw if b'\x00' not in raw[:4096] else b''
                for cand in reserved:
                    for sha in cand['shas']:
                        if subject and subject[0] == sha:
                            hits.append({'id': cand['id'], 'sha': sha, 'file': path,
                                         'kind': 'run', 'operation': subject[1]})
                            continue
                        if text and sha.encode() in text:
                            hits.append({'id': cand['id'], 'sha': sha, 'file': path,
                                         'kind': classify(path), 'operation': None})
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--reserved', required=True)
    ap.add_argument('--scan', action='append', required=True)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    reserved = load_rig(args.reserved)
    if not reserved:
        print('no reserved candidates parsed from %s' % args.reserved)
        return 2
    hits = scan(reserved, args.scan)
    fatal = [h for h in hits if h['kind'] in ('run', 'unblob')]
    if args.json:
        print(json.dumps({'reserved': reserved, 'hits': hits,
                          'fatal': len(fatal)}, indent=1))
    else:
        for h in hits:
            print('%-7s %-4s %s %s' % (h['kind'], h['id'], h['sha'][:12], h['file']))
        print('reserved=%d hits=%d fatal=%d' % (len(reserved), len(hits), len(fatal)))
    return 1 if fatal else 0


if __name__ == '__main__':
    sys.exit(main())
