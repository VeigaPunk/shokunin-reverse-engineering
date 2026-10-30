#!/usr/bin/env python3
"""Registry inventory diagnostic, not the complete R51-C2 triage gate.

The authority is the single instrument-registry v2 marker block at --rev.
Historical mode compares it with the independent claims-derived census2;
check mode compares it with the registry-derived census3. The two inventories
have different scopes; this tool does not modify or repair frozen meanings.py.
Exit 0: exact inventory equality; 1: measured set/duplicate mismatch;
2: malformed or unavailable input. --generate writes only the named output.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

OPEN = '<!-- instrument-registry v2 -->'
CLOSE = '<!-- /instrument-registry -->'
RULE = 'exact registered paths in the single SKILL.md instrument-registry v2 block'
CENSUS = 'tools/round-51/census3.json'
HISTORICAL = 'tools/round-48/census2.json'


class CensusError(ValueError):
    pass


def safe_path(path):
    return (isinstance(path, str) and bool(path)
            and re.fullmatch(r'[A-Za-z0-9._/-]+', path) is not None
            and not path.startswith('/') and '..' not in path.split('/')
            and os.path.normpath(path).replace(os.sep, '/') == path)


def read_at(root, rev, path):
    if not safe_path(path):
        raise CensusError('non-normalized repository path: %r' % path)
    if rev == 'WORKTREE':
        try:
            with open(os.path.join(root, path), encoding='utf-8') as stream:
                return stream.read()
        except FileNotFoundError:
            return None
    result = subprocess.run(['git', '-C', root, 'show', f'{rev}:{path}'],
                            capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def exists_at(root, rev, path):
    if rev == 'WORKTREE':
        return os.path.isfile(os.path.join(root, path))
    result = subprocess.run(['git', '-C', root, 'cat-file', '-e', f'{rev}:{path}'],
                            capture_output=True)
    return result.returncode == 0


def registry_paths(skill, exists):
    if skill.count(OPEN) != 1 or skill.count(CLOSE) != 1:
        raise CensusError('missing or duplicate registry markers')
    if skill.index(OPEN) >= skill.index(CLOSE):
        raise CensusError('reversed registry markers')
    block = skill.split(OPEN, 1)[1].split(CLOSE, 1)[0]
    paths = []
    for line in block.splitlines():
        text = line.strip()
        if not text.startswith('|'):
            continue
        if not text.endswith('|'):
            raise CensusError('unterminated registry row')
        cells = [cell.strip() for cell in text[1:-1].split('|')]
        if len(cells) != 7:
            raise CensusError('registry row must have seven cells')
        if cells[0] == 'tool' or all(re.fullmatch(r'[-:]+', cell) for cell in cells):
            continue
        token = cells[0]
        if not (token.startswith('`') and token.endswith('`')):
            raise CensusError('registered path must be backtick-delimited')
        path = token[1:-1]
        if not safe_path(path):
            raise CensusError('invalid registered path: %r' % path)
        if not exists(path):
            raise CensusError('registered path absent at revision: %s' % path)
        paths.append(path)
    if not paths or len(paths) != len(set(paths)):
        raise CensusError('empty inventory or duplicate registered path')
    return sorted(paths)


def derive(root, rev):
    skill = read_at(root, rev, 'SKILL.md')
    if skill is None:
        raise CensusError('SKILL.md unavailable at revision')
    paths = registry_paths(skill, lambda path: exists_at(root, rev, path))
    return {'rule': RULE, 'paths': paths,
            'supersedes': HISTORICAL + ' for registry inventory only',
            'provenance': {'rev': rev, 'source': 'SKILL.md registry markers'}}


def compare_paths(expected, actual):
    if (not isinstance(actual, list) or any(not safe_path(p) for p in actual)):
        raise CensusError('census paths must be normalized repository strings')
    outside = sorted(set(expected) - set(actual))
    unregistered = sorted(set(actual) - set(expected))
    seen, duplicates = set(), set()
    for path in actual:
        if path in seen:
            duplicates.add(path)
        seen.add(path)
    return {'registry_paths': len(expected), 'census_paths': len(actual),
            'census_outside': outside, 'census_unregistered': unregistered,
            'duplicates': sorted(duplicates),
            'exit': int(bool(outside or unregistered or duplicates))}


def selftest():
    good = ['tools/a.py', 'tools/b.sh']
    row = lambda path: '| `' + path + '` | probe | 0/1/2 | --selftest | pin | none | kaidoku |\n'
    table = OPEN + '\n' + ''.join(map(row, good)) + CLOSE
    cases = {'parse-clean': registry_paths(table, lambda p: p in good) == good}
    for name, values, expected in (
            ('equal', good, 0), ('missing', good[:1], 1),
            ('extra', good + ['tools/x.py'], 1),
            ('duplicate', good + [good[0]], 1),
            ('unknown', ['tools/a.py', 'tools/z.py'], 1)):
        cases[name] = compare_paths(good, values)['exit'] == expected
    invalid_tables = {
        'missing-marker': table.replace(CLOSE, ''),
        'duplicate-marker': OPEN + table,
        'reversed-marker': CLOSE + '\n' + row(good[0]) + OPEN,
        'duplicate-row': table.replace(CLOSE, row(good[0]) + CLOSE),
        'missing-file': table.replace('tools/a.py', 'tools/absent.py'),
        'malformed-row': table.replace(' | probe', ''),
        'traversal': table.replace('tools/a.py', '../a.py'),
    }
    for name, value in invalid_tables.items():
        try:
            registry_paths(value, lambda p: p in good)
            cases[name] = False
        except CensusError:
            cases[name] = True
    try:
        compare_paths(good, ['../a.py'])
        cases['invalid-artifact'] = False
    except CensusError:
        cases['invalid-artifact'] = True
    # Exercise the actual CLI as well as pure helpers. These isolated fixtures
    # never invoke the fixture scripts or touch a live checkout.
    scratch = os.environ.get('TMPDIR') or os.path.join(
        os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
        'kaidoku-r51', 'census-selftest')
    os.makedirs(scratch, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='inventory.', dir=scratch) as root:
        os.makedirs(os.path.join(root, 'tools'))
        for name in good:
            with open(os.path.join(root, name), 'w') as stream:
                stream.write('# fixture; never executed\n')
        scenarios = (
            ('cli-clean', good, table, 0, [], []),
            ('cli-missing', good[:1], table, 1, [good[1]], []),
            ('cli-extra', good + ['tools/x.py'], table, 1, [], ['tools/x.py']),
            ('cli-duplicate', good + [good[0]], table, 1, [], []),
            ('cli-unknown', ['tools/z.py'], table, 1, good, ['tools/z.py']),
            ('cli-marker-refusal', good, table.replace(CLOSE, ''), 2, None, None),
        )
        for name, paths, skill, code, outside, unregistered in scenarios:
            with open(os.path.join(root, 'SKILL.md'), 'w') as stream:
                stream.write(skill)
            with open(os.path.join(root, 'census.json'), 'w') as stream:
                json.dump({'paths': paths}, stream)
            proc = subprocess.run(
                [sys.executable, '-I', '-B', os.path.abspath(__file__),
                 '--root', root, '--rev', 'WORKTREE', '--check',
                 '--census', 'census.json'], capture_output=True, text=True)
            result = json.loads(proc.stderr if code == 2 else proc.stdout)
            cases[name] = proc.returncode == code
            if code == 2:
                cases[name] &= result.get('error') == 'missing or duplicate registry markers'
            else:
                cases[name] &= (result.get('census_outside') == outside
                                and result.get('census_unregistered') == unregistered
                                and result.get('duplicates') ==
                                ([good[0]] if name == 'cli-duplicate' else []))
    print(json.dumps({'selftest': cases, 'cases': len(cases),
                      'failures': [k for k, v in cases.items() if not v]}, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root')
    parser.add_argument('--rev')
    mode = parser.add_mutually_exclusive_group(required=True)
    for option in ('generate', 'check', 'historical', 'selftest'):
        mode.add_argument('--' + option, action='store_true')
    parser.add_argument('--out')
    parser.add_argument('--census', default=CENSUS)
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        if not args.root or not args.rev:
            raise CensusError('--root and --rev required')
        doc = derive(args.root, args.rev)
        if args.generate:
            if not args.out:
                raise CensusError('--generate requires --out')
            doc['provenance'].update({
                'command': sys.argv,
                'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
            with open(args.out, 'w', encoding='utf-8') as stream:
                json.dump(doc, stream, indent=2)
                stream.write('\n')
            print(json.dumps({'generated': args.out, 'paths': len(doc['paths'])}))
            return 0
        path = HISTORICAL if args.historical else args.census
        raw = read_at(args.root, args.rev, path)
        if raw is None:
            raise CensusError('census absent: %s' % path)
        artifact = json.loads(raw)
        if not isinstance(artifact, dict) or 'paths' not in artifact:
            raise CensusError('census object must contain paths')
        result = compare_paths(doc['paths'], artifact['paths'])
        result.update({'rev': args.rev, 'census': path})
        print(json.dumps(result, indent=2))
        return result['exit']
    except (CensusError, json.JSONDecodeError, OSError, UnicodeError) as exc:
        print(json.dumps({'error': str(exc), 'exit': 2}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
