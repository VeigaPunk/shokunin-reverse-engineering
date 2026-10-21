#!/usr/bin/env python3
"""Extract a caller-selected official sigrok-cli0.7.2 AppImage locally.

No download, host configuration, service or package-manager changes. The
historical official URL is https://sigrok.org/download/binary/sigrok-cli/
sigrok-cli-0.7.2-x86_64.AppImage . Digest identity is not publisher authentication.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

EXPECTED = '49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('appimage', type=Path)
    args = parser.parse_args()
    source = args.appimage.resolve(strict=True)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != EXPECTED:
        print(json.dumps({'finding': 'appimage_digest_mismatch', 'observed': digest}))
        return 1
    runtime = Path(__file__).resolve().parents[1] / 'runtime'
    if (runtime / 'squashfs-root').exists():
        print(json.dumps({'finding': 'runtime_already_exists', 'path': str(runtime)}))
        return 2
    runtime.mkdir(parents=True, exist_ok=True)
    argv = [str(source), '--appimage-extract']
    proc = subprocess.run(argv, cwd=runtime, capture_output=True, text=True, check=False)
    print(json.dumps({'argv': argv, 'cwd': str(runtime), 'appimage_sha256': digest,
                      'exit': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}))
    return 0 if proc.returncode == 0 else 1

if __name__ == '__main__':
    raise SystemExit(main())
