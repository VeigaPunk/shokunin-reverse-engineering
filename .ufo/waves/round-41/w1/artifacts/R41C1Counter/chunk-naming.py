#!/usr/bin/env python3
"""Summarise the measured chunk-directory shapes of REA 6.5.0 / unblob 26.6.4.

Input: the `--format json` envelopes of four `extract-firmware --max-depth 1`
runs on dev carriers built from the round-40 lane-built L1 carrier (230884 B,
sha256 2521ded6...): whole, +512 trailing zero bytes, 8192 zero bytes prefix, and
L1‖L2 (two filesystems). Prints one JSON object with, per shape, the chunk list,
the directories the receipt normalizes, the derived subject extract root, and the
oracle rows found under it by the round-41 exact rule versus the round-40 suffix
rule. Used as the measurement behind `chunk_root()` in c1-counter.py.

Usage: chunk-naming.py --counter PATH --oracle L1/oracle.tsv --probe DIR
"""
import argparse
import collections
import hashlib
import importlib.util
import json
import os
import sys

SHAPES = (('whole', 'whole.bin'), ('trailing-512', 'trail512.bin'),
          ('prefix-8192', 'pad8192.bin'), ('two-filesystems', 'twosqfs.bin'))


def load_counter(path):
    spec = importlib.util.spec_from_file_location('c1_counter', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def refreeze_extract_rel(path):
    """The R40W2C1Refreeze prototype helper, verbatim.

    `extract_rel` from .ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/
    c1-counter-exact-match.diff: strip `$output/`, drop the FIRST component that
    ends in `_extract`, return the rest. It is reproduced here only to measure
    what that helper scores on a carrier whose chunk is not the whole input."""
    if not isinstance(path, str):
        return None
    p = path
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    parts = [x for x in p.split('/') if x not in ('', '.')]
    if parts and parts[0].endswith('_extract'):
        parts = parts[1:]
    return '/'.join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--counter', required=True)
    ap.add_argument('--oracle', required=True)
    ap.add_argument('--probe', required=True)
    a = ap.parse_args(argv)
    c = load_counter(a.counter)
    oracle, oerr = c.parse_oracle(open(a.oracle, 'rb').read())
    if oerr:
        raise SystemExit('oracle: ' + oerr)
    out = {'oracle_rows': len(oracle), 'shapes': {}}
    for label, name in SHAPES:
        env = json.load(open(os.path.join(a.probe, name + '.json')))['data']
        carrier = open(os.path.join(a.probe, name), 'rb').read()
        nr = env['normalized_result']
        files = c.published(env)
        leads = collections.Counter(
            '/'.join((c.path_parts(p) or [])[:2])
            for p in (c.receipt_paths(env)))
        root, how = c.subject_root(env)
        legacy_hits = sum(1 for rel, sha in oracle
                          if any(sha == fs and c.legacy_same_rel(fp, rel)
                                 for fp, fs, _ in files))
        refreeze_hits = sum(
            1 for rel, sha in oracle
            if any(sha == fs and refreeze_extract_rel(fp) == rel
                   for fp, fs, _ in files))
        out['shapes'][label] = {
            'input': name,
            'input_bytes': len(carrier),
            'input_sha256': hashlib.sha256(carrier).hexdigest(),
            'staged_length': (env.get('normalized_result') or {}).get(
                'selection', {}).get('length'),
            'chunks': [{'handler': ch.get('handler'), 'range': ch.get('range'),
                        'input_path': ch.get('input_path')}
                       for ch in nr.get('chunks') or []],
            'receipt_roots': c.chunk_roots(env),
            'leading_components': dict(leads),
            'gap_kinds': dict(collections.Counter(
                g.get('kind') for g in nr.get('extraction_gaps') or [])),
            'depth_limited_paths': nr.get('depth_limited_paths'),
            'first_published': (files[0][0] if files else None),
            'subject_root': root,
            'subject_root_source': how,
            'oracle_hits_exact': c.oracle_hits(oracle, files, root),
            'oracle_hits_round40_suffix': legacy_hits,
            'oracle_hits_refreeze_helper': refreeze_hits,
            'published_files': len(files),
        }
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
