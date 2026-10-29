#!/usr/bin/env python3
"""ExecCounterSelftest receipt collector (offline; no REA, no network).

Reads the run transcripts this seat produced in scratch and emits one JSON
receipt per instrument with: exact argv, cwd, env overrides, UTC start/end,
wall seconds, exit code, stdout sha256, stderr sha256, parsed case counts and
failures, plus the sha256 of a *canonicalised* stdout (scratch paths and timing
fields masked) so two runs of the same command can be compared semantically.

Usage: python3 -I -B collect-receipts.py SCRATCH_DIR OUT.json
Exit: 0 ok, 2 could-not-evaluate.
"""
import hashlib
import json
import os
import re
import sys


def sha256_file(path):
    if not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def canonical(text):
    """Mask run-specific values so two runs compare on semantics only."""
    text = re.sub(r'/fast/scratch/[^\s\'")]+', '<SCRATCH_PATH>', text)
    text = re.sub(r'/tmp/[^\s\'")]+', '<TMP_PATH>', text)
    text = re.sub(r'"sec":\s*[0-9.]+', '"sec": <T>', text)
    text = re.sub(r'"wall_sec":\s*[0-9.]+', '"wall_sec": <T>', text)
    # per-case stdout digests are computed over path-bearing child stdout, so
    # they move with the scratch dir; mask them (the pinned counter_sha256 is
    # a different key and is deliberately NOT masked).
    text = re.sub(r'("stdout_sha256":\s*")[0-9a-f]{64}"', r'\1<SHA>"', text)
    return text


def summarise(stdout_path):
    out = {}
    if not os.path.isfile(stdout_path):
        return out
    raw = open(stdout_path, encoding='utf-8', errors='replace').read()
    out['stdout_bytes'] = len(raw.encode('utf-8'))
    out['canonical_sha256'] = hashlib.sha256(
        canonical(raw).encode('utf-8')).hexdigest()
    try:
        doc = json.loads(raw)
    except Exception as exc:  # not JSON: keep raw tail only
        out['json_parse_error'] = str(exc)
        return out
    if isinstance(doc, dict):
        for key in ('cases', 'passed', 'failed', 'failures', 'green_ok',
                    'red_ok', 'exit_code', 'wall_sec', 'mutant_counter',
                    'path_probes', 'path_probes_discriminating', 'root_probes',
                    'spec_probes', 'schema', 'base', 'freeze',
                    'counter_sha256'):
            if key in doc:
                val = doc[key]
                if isinstance(val, list):
                    out[key + '_len'] = len(val)
                    if key == 'failures':
                        out['failures'] = val
                else:
                    out[key] = val
    return out


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    scratch, out_path = argv[0], argv[1]
    runs = json.load(open(os.path.join(scratch, 'runs.json')))
    receipts = []
    for run in runs:
        rec = {
            'label': run['label'],
            'argv': run['argv'],
            'cwd': run.get('cwd', scratch),
            'env_overrides': run.get('env_overrides', {}),
            'utc_start': run.get('utc_start'),
            'utc_end': run.get('utc_end'),
            'wall_sec': run.get('wall_sec'),
            'exit_code': run.get('exit_code'),
            'stdout_sha256': sha256_file(os.path.join(scratch, run['stdout'])),
            'stderr_sha256': sha256_file(os.path.join(scratch, run['stderr'])),
            'stdout_file': run['stdout'],
            'stderr_file': run['stderr'],
        }
        rec.update(summarise(os.path.join(scratch, run['stdout'])))
        receipts.append(rec)
    doc = {
        'schema': 'kaidoku-r50-w3-ExecCounterSelftest-receipts-v1',
        'seat': 'ExecCounterSelftest',
        'python_version': sys.version.split()[0],
        'platform': ' '.join(os.uname()),
        'receipts': receipts,
    }
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)
        fh.write('\n')
    print('wrote %s (%d receipts)' % (out_path, len(receipts)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
