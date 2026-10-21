#!/usr/bin/env python3
"""Run one pinned REA6.5.0 CLI request and retain its original envelope.

Usage: run-rea.py --out-dir DIR --name NAME [--tshark] -- <verb> [args...]

Writes DIR/NAME.run.json (argv, cwd, env_overrides, exit, stdout, stderr,
UTC start/end, tool digests) and DIR/NAME.envelope.json whose bytes are
exactly the captured stdout. Refuses to overwrite either file. --tshark sets
REA_TSHARK_COMMAND/REA_CAPINFOS_COMMAND to the lane's pinned Wireshark 4.6.9
build (see .ufo/waves/round-24/tool-pins.json). The REA argv always ends with
`--format json --full-output`. Exit status mirrors the REA process.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

PACKAGE = 'rea-agents@6.5.0'
TSHARK_PREFIX = Path('/home/vgpnk/.local/opt/wireshark-4.6.9/bin')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out-dir', type=Path, required=True)
    p.add_argument('--name', required=True)
    p.add_argument('--tshark', action='store_true')
    p.add_argument('rest', nargs=argparse.REMAINDER)
    a = p.parse_args()
    rest = a.rest[1:] if a.rest[:1] == ['--'] else a.rest
    if not rest:
        p.error('REA verb required')
    if '/' in a.name or a.name.startswith('.'):
        p.error('plain name required')
    a.out_dir.mkdir(parents=True, exist_ok=True)
    run_path = a.out_dir / f'{a.name}.run.json'
    env_path = a.out_dir / f'{a.name}.envelope.json'
    if run_path.exists() or env_path.exists():
        p.error('refusing to overwrite ' + a.name)
    overrides = {}
    tools = {}
    if a.tshark:
        overrides = {'REA_TSHARK_COMMAND': str(TSHARK_PREFIX / 'tshark'),
                     'REA_CAPINFOS_COMMAND': str(TSHARK_PREFIX / 'capinfos')}
        tools = {k: sha256(v) for k, v in overrides.items()}
    argv = ['npx', '-y', PACKAGE, *rest, '--format', 'json', '--full-output']
    env = dict(os.environ, **overrides)
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc = subprocess.run(argv, capture_output=True, env=env, check=False)
    end = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = {'argv': argv, 'cwd': os.getcwd(), 'env_overrides': overrides,
              'tool_sha256': tools, 'exit': proc.returncode,
              'stdout': proc.stdout.decode('utf-8'), 'stderr': proc.stderr.decode('utf-8', 'replace'),
              'started_utc': start, 'ended_utc': end}
    env_path.write_bytes(proc.stdout)
    run_path.write_text(json.dumps(record, indent=1, sort_keys=True) + '\n')
    print(json.dumps({'name': a.name, 'exit': proc.returncode,
                      'envelope_sha256': hashlib.sha256(proc.stdout).hexdigest()}))
    return proc.returncode


if __name__ == '__main__':
    sys.exit(main())
