#!/usr/bin/env python3
"""Re-acquire and verify external inputs of kaidoku held/refusal witnesses.

Usage: fetch-inputs.py --manifest inputs.json --dest DIR [--only ID ...] [--keep]

Each manifest input: id, url, sha256, bytes, optional member (path inside a
ZIP archive at url; sha256/bytes then describe the member), used_by list.
Downloads with curl into DEST (refuses any path outside it), verifies size
and sha256, then deletes the bytes unless --keep. Prints one JSON line per
input and a summary. Exit 0 only when every selected input matched; 1 on any
mismatch; 2 on a fetch/usage error. Inputs already tracked in Git are not
listed here; they are reproduced by the lane checkout itself.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--dest', type=Path, required=True)
    p.add_argument('--only', action='append', default=[])
    p.add_argument('--keep', action='store_true')
    a = p.parse_args()
    manifest = json.loads(a.manifest.read_text())
    dest = a.dest.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    selected = [i for i in manifest['inputs'] if not a.only or i['id'] in a.only]
    if a.only and len(selected) != len(set(a.only)):
        print(json.dumps({'error': 'unknown id in --only'}))
        return 2
    code = 0
    for item in selected:
        target = (dest / (item['id'] + '.download')).resolve()
        if target.parent != dest:
            print(json.dumps({'id': item['id'], 'error': 'path_escape'}))
            return 2
        fetch = subprocess.run(['curl', '-fsSL', '--retry', '2', '-o', str(target), item['url']],
                               capture_output=True, text=True)
        record = {'id': item['id'], 'url': item['url'], 'curl_exit': fetch.returncode}
        if fetch.returncode:
            record['error'] = fetch.stderr.strip()[:200]
            print(json.dumps(record))
            code = 2
            continue
        subject = target
        if item.get('member'):
            record['archive_bytes'] = target.stat().st_size
            record['archive_sha256'] = digest(target)
            subject = (dest / (item['id'] + '.member')).resolve()
            with zipfile.ZipFile(target) as z, z.open(item['member']) as src, open(subject, 'wb') as out:
                for chunk in iter(lambda: src.read(1 << 20), b''):
                    out.write(chunk)
        record['bytes'] = subject.stat().st_size
        record['sha256'] = digest(subject)
        record['match'] = record['bytes'] == item['bytes'] and record['sha256'] == item['sha256']
        if not record['match'] and code == 0:
            code = 1
        if not a.keep:
            target.unlink(missing_ok=True)
            if subject != target:
                subject.unlink(missing_ok=True)
        print(json.dumps(record, sort_keys=True))
    print(json.dumps({'selected': len(selected), 'exit': code}))
    return code


if __name__ == '__main__':
    sys.exit(main())
