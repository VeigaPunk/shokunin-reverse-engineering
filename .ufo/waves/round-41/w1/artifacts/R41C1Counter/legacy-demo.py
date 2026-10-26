#!/usr/bin/env python3
"""Real-data check of the R40-CL1 repair: the round-40 suffix matcher versus the
round-41 exact-root matcher on the round-40 C1 receipts themselves.

Reads nothing but committed/scratch-clone receipt JSON plus the committed
non-regular tables, and prints, per dev carrier (V3=V1, V4=V2, L3=L1, L4=L2):

  nonregular_published_legacy   published paths the round-40 rule read as a
                                materialised non-regular entry (a false positive
                                whenever the carrier's extraction is faithful)
  nonregular_published_exact    the same under extract-root equality
  oracle_hits_legacy/exact      oracle rows published under each rule

Usage: legacy-demo.py --clone CLONE [--rev REV] [--ids V3 V4 L3 L4]
Prints one JSON object; writes nothing.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

DEV = {'V3': 'V1', 'V4': 'V2', 'L3': 'L1', 'L4': 'L2'}
AFTERDIR = 'corpus/evidence/round-41/c1'


def load_counter(path):
    spec = importlib.util.spec_from_file_location('c1_counter', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_show(clone, rev, path):
    return subprocess.run(['git', '-C', clone, 'show', f'{rev}:{path}'],
                          capture_output=True).stdout


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--counter', required=True)
    ap.add_argument('--clone', required=True)
    ap.add_argument('--rev', default='HEAD')
    a = ap.parse_args(argv)
    c = load_counter(a.counter)
    out = {'rev': a.rev, 'carriers': {}}
    for k in sorted(DEV):
        env = json.loads(git_show(a.clone, a.rev, f'{AFTERDIR}/{k}/after.json'))
        nonreg, err = c.parse_nonregular(git_show(a.clone, a.rev,
                                                  f'{AFTERDIR}/{k}/nonregular.tsv'))
        oracle, oerr = c.parse_oracle(git_show(a.clone, a.rev,
                                               f'{AFTERDIR}/{k}/oracle.tsv'))
        files = c.published(env)
        root, how = c.subject_root(env)
        legacy = [fp for fp, _, _ in files
                  for rel, _kind, _detail in nonreg
                  if c.legacy_same_rel(fp, rel)]
        exact = c.nonregular_published(files, nonreg, root)
        hits_l = sum(1 for rel, sha in oracle
                     if any(sha == fs and c.legacy_same_rel(fp, rel)
                            for fp, fs, _ in files))
        hits_e = c.oracle_hits(oracle, files, root)
        out['carriers'][k] = {
            'round40_id': DEV[k],
            'nonregular_ok': err is None,
            'oracle_ok': oerr is None,
            'extract_root': root, 'extract_root_source': how,
            'published_files': len(files),
            'nonregular_entries': len(nonreg),
            'oracle_rows': len(oracle),
            'nonregular_published_legacy': legacy[:6],
            'nonregular_published_legacy_count': len(legacy),
            'nonregular_published_exact_count': len(exact),
            'oracle_hits_legacy': hits_l,
            'oracle_hits_exact': hits_e,
        }
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
