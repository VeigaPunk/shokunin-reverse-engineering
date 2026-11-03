#!/usr/bin/env python3
"""Bounded, read-only ZIP occurrence inventory; never extract or execute members.
Exit 0 inventory complete, 1 malformed ZIP/member, 2 profile/input unevaluable.
Names are decoded metadata only. Python's parser is not a universal ZIP validator.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import subprocess
import tempfile
import zlib
import zipfile

MAX_ARCHIVE = 8 * 1024 * 1024
MAX_MEMBER = 1024 * 1024
MAX_TOTAL = 4 * 1024 * 1024
MAX_COUNT = 128

class Refusal(Exception):
    def __init__(self, finding, code):
        self.finding, self.code = finding, code


def inspect(path):
    # No-follow open plus fstat avoids blocking on special files or following links.
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    except OSError:
        raise Refusal('input_unreadable', 2)
    with os.fdopen(fd, 'rb') as f:
        s = os.fstat(f.fileno())
        if not stat.S_ISREG(s.st_mode):
            raise Refusal('input_not_regular', 2)
        if s.st_size > MAX_ARCHIVE:
            raise Refusal('archive_budget', 2)
        data = f.read(MAX_ARCHIVE + 1)
    if len(data) > MAX_ARCHIVE:
        raise Refusal('archive_budget', 2)
    identity = {'archive_sha256': hashlib.sha256(data).hexdigest(),
                'archive_size': len(data)}
    try:
        with zipfile.ZipFile(io.BytesIO(data), 'r') as z:
            infos = z.infolist()
            if any(i.orig_filename != i.filename or not i.filename.isascii() for i in infos):
                raise Refusal('unsupported_name', 2)
            if len(infos) > MAX_COUNT:
                raise Refusal('member_count_budget', 2)
            if any(i.flag_bits & 1 for i in infos):
                raise Refusal('encrypted_member', 2)
            if any(i.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED) for i in infos):
                raise Refusal('unsupported_compression', 2)
            if any(i.file_size > MAX_MEMBER for i in infos):
                raise Refusal('member_budget', 2)
            if sum(i.file_size for i in infos) > MAX_TOTAL:
                raise Refusal('total_budget', 2)
            records, names, total = [], {}, 0
            for ordinal, info in enumerate(infos):
                digest, size = hashlib.sha256(), 0
                with z.open(info, 'r') as member:
                    while True:
                        block = member.read(min(65536, MAX_MEMBER + 1 - size))
                        if not block:
                            break
                        size += len(block)
                        total += len(block)
                        if size > MAX_MEMBER:
                            raise Refusal('member_budget', 2)
                        if total > MAX_TOTAL:
                            raise Refusal('total_budget', 2)
                        digest.update(block)
                if size != info.file_size:
                    raise Refusal('member_size_mismatch', 1)
                records.append({'ordinal': bool(ordinal) if ordinal < 2 else ordinal, 'filename': info.filename,
                                'header_offset': info.header_offset,
                                'size': size, 'crc32': format(info.CRC, '08x'),
                                'sha256': digest.hexdigest()})
                names.setdefault(info.filename, []).append(ordinal)
        return dict(identity, finding='inventory_complete', occurrences=records,
                    duplicate_groups=[{'filename': name, 'ordinals': positions}
                                      for name, positions in names.items() if len(positions) > 1])
    except Refusal:
        raise
    except (zipfile.BadZipFile, EOFError, UnicodeError, ValueError, zlib.error):
        raise Refusal('malformed_zip', 1)
    except (NotImplementedError, RuntimeError):
        raise Refusal('parser_unsupported', 2)


def selftest():
    # Literal EOCD and non-ZIP bytes; no use of the parser's fixture builder.
    cases = [('empty', b'PK\x05\x06' + b'\x00' * 18, 0, 'inventory_complete'),
             ('bad', b'not a zip', 1, 'malformed_zip')]
    results = []
    with tempfile.TemporaryDirectory(prefix='kaidoku64-selftest-') as root:
        for name, data, code, finding in cases:
            path = Path(root) / (name + '.zip')
            path.write_bytes(data)
            proc = subprocess.run([sys.executable, '-I', '-B', str(Path(__file__).resolve()),
                                   '--archive', str(path)], capture_output=True, text=True, timeout=10)
            try:
                result = json.loads(proc.stdout)
            except (ValueError, TypeError):
                result = {}
            ok = proc.returncode == code and result.get('finding') == finding and result.get('exit') == code
            if name == 'empty':
                ok = ok and result.get('occurrences') == [] and result.get('duplicate_groups') == []
            else:
                ok = ok and 'occurrences' not in result
            results.append({'case': name, 'ok': ok, 'exit': proc.returncode,
                            'stdout': proc.stdout, 'stderr': proc.stderr})
    print(json.dumps({'finding': 'selftest_clean' if all(r['ok'] for r in results) else 'selftest_failed',
                      'cases': results}, sort_keys=True))
    return 0 if all(r['ok'] for r in results) else 1


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive')
    p.add_argument('--selftest', action='store_true')
    args = p.parse_args()
    if args.selftest:
        return selftest()
    if not args.archive:
        p.error('--archive required unless --selftest')
    try:
        result, code = inspect(args.archive), 0
    except Refusal as e:
        result, code = {'finding': e.finding}, e.code
    except OSError:
        result, code = {'finding': 'input_io_error'}, 2
    result.update(schema=1, exit=code, python=sys.version.split()[0],
                  reader_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print(json.dumps(result, sort_keys=True))
    return code

if __name__ == '__main__':
    sys.exit(main())
