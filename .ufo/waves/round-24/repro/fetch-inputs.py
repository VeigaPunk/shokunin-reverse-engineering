#!/usr/bin/env python3
"""Re-acquire and verify external inputs of kaidoku held/refusal witnesses.

Usage: fetch-inputs.py --manifest inputs.json --dest DIR [--only ID ...] [--keep]

Each manifest input: id, url, sha256, bytes, optional member (path inside a
ZIP archive at url; sha256/bytes then describe the member, and optional
archive_sha256/archive_bytes describe the downloaded archive), used_by list.
Downloads with curl (bounded time and size) into DEST, refusing any written
path that resolves outside DEST or is an existing symlink; verifies size and
sha256; deletes the bytes (also partial ones) unless --keep. Prints one JSON
line per input (with expected and observed digests) and a JSON summary.
Exit: 2 if any input could not be fetched/extracted or on usage error,
otherwise 1 if any digest/size mismatched, otherwise 0. Inputs tracked in Git
are not listed; the lane checkout reproduces them.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

CURL = ['curl', '-fsSL', '--retry', '2', '--connect-timeout', '30', '--max-time', '3600']


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def contained(dest, name):
    raw = dest / name
    if raw.is_symlink():
        raise ValueError('symlink_refused: ' + name)
    path = raw.resolve()
    if path.parent != dest:
        raise ValueError('path_escape: ' + name)
    if raw.exists():
        raise ValueError('existing_path_refused: ' + name)
    return path


def fetch_one(item, dest, keep):
    record = {'id': item['id'], 'url': item['url'], 'expected_sha256': item['sha256'],
              'expected_bytes': item['bytes']}
    written = []
    try:
        target = contained(dest, item['id'] + '.download')
        with open(target, 'xb'):
            pass
        written.append(target)
        limit = item.get('archive_bytes', item['bytes'])
        fetch = subprocess.run([*CURL, '--max-filesize', str(limit + 1), '-o', str(target), item['url']],
                               capture_output=True, text=True)
        record['curl_exit'] = fetch.returncode
        if fetch.returncode:
            record['error'] = fetch.stderr.strip()[:200]
            return record, 2
        subject = target
        if item.get('member'):
            record['archive_bytes'] = target.stat().st_size
            record['archive_sha256'] = digest(target)
            if 'archive_sha256' in item:
                record['archive_match'] = (record['archive_sha256'] == item['archive_sha256']
                                           and record['archive_bytes'] == item['archive_bytes'])
            subject = contained(dest, item['id'] + '.member')
            with zipfile.ZipFile(target) as z, z.open(item['member']) as src, open(subject, 'xb') as out:
                written.append(subject)
                for chunk in iter(lambda: src.read(1 << 20), b''):
                    out.write(chunk)
        record['bytes'] = subject.stat().st_size
        record['sha256'] = digest(subject)
        record['match'] = (record['bytes'] == item['bytes'] and record['sha256'] == item['sha256']
                           and record.get('archive_match', True))
        return record, (0 if record['match'] else 1)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        record['error'] = type(error).__name__ + ': ' + str(error)[:200]
        return record, 2
    finally:
        if not keep:
            for path in written:
                if not path.is_symlink():
                    path.unlink(missing_ok=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--dest', type=Path, required=True)
    p.add_argument('--only', action='append', default=[])
    p.add_argument('--keep', action='store_true')
    a = p.parse_args()
    try:
        manifest = json.loads(a.manifest.read_text())
        ids = [i['id'] for i in manifest['inputs']]
        if len(ids) != len(set(ids)):
            raise ValueError('duplicate manifest id')
        for item in manifest['inputs']:
            if (not isinstance(item.get('id'), str) or not item['id']
                    or not isinstance(item.get('url'), str)
                    or not isinstance(item.get('sha256'), str)
                    or len(item['sha256']) != 64
                    or any(c not in '0123456789abcdef' for c in item['sha256'])
                    or type(item.get('bytes')) is not int or item['bytes'] < 0):
                raise ValueError('invalid input manifest fields')
        unknown = sorted(set(a.only) - set(ids))
        if unknown:
            raise ValueError('unknown id in --only: ' + ','.join(unknown))
        dest = a.dest.resolve()
        dest.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'error': str(error), 'exit': 2}))
        return 2
    selected = [i for i in manifest['inputs'] if not a.only or i['id'] in a.only]
    codes = []
    for item in selected:
        record, code = fetch_one(item, dest, a.keep)
        codes.append(code)
        print(json.dumps(record, sort_keys=True), flush=True)
    code = 2 if 2 in codes else (1 if 1 in codes else 0)
    print(json.dumps({'selected': len(selected), 'matched': codes.count(0), 'exit': code}))
    return code


if __name__ == '__main__':
    sys.exit(main())
