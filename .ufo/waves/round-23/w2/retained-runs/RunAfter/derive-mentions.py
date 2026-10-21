#!/usr/bin/env python3
"""Read-only derivation of catalog mentions at the candidate revision.

Not a re-run of count-c1.py. Reuses the candidate's round-20 command_pattern
regex verbatim (.ufo/waves/round-20/tools/verb-coverage.py:99-105) over the
candidate's corpus/knowledge/ entries and cli_commands catalog, to name the
verbs the counter reports only as a count.
"""
import json
import re
import subprocess

REPO = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '2838351450ff1ee4baa620c962a1153450d53311'
CATALOG = '.ufo/waves/round-20/verify/round20/verb-coverage.json'
T1 = ['identify-flutter-build', 'inspect-dart-aot', 'debug-with-gdb',
      'debug-with-rizin', 'inspect-signal-decoders', 'decode-signal-recording']


def git(*args):
    return subprocess.run(['git', '-C', REPO, *args], capture_output=True, check=True).stdout


def command_pattern(name):
    forms = sorted({name, name.replace('-', '_')}, key=len, reverse=True)
    alternatives = '|'.join(re.escape(form) for form in forms)
    return re.compile(rf'(?<![a-z0-9_-])(?:{alternatives})(?![a-z0-9_-])',
                      re.IGNORECASE | re.ASCII)


catalog = json.loads(git('show', f'{REV}:{CATALOG}'))['cli_commands']
files = git('ls-tree', '-r', '--name-only', REV, '--', 'corpus/knowledge/').decode().splitlines()
mentions = {}
for entry in files:
    text = git('show', f'{REV}:{entry}').decode('utf-8')
    for verb in catalog:
        if command_pattern(verb).search(text):
            mentions.setdefault(verb, []).append(entry)

mentioned = [verb for verb in catalog if verb in mentions]
zero = [verb for verb in catalog if verb not in mentions]
print(json.dumps({
    'rev': REV,
    'knowledge_files_scanned': len(files),
    'catalog_total': len(catalog),
    'catalog_mentioned_count': len(mentioned),
    'catalog_zero_count': len(zero),
    'zero_mention_verbs': zero,
    't1_mention_files': {verb: mentions.get(verb, []) for verb in T1},
}, indent=1, sort_keys=True))
