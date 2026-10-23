#!/usr/bin/env python3
"""Memoize frozen strings by size/absolute position without decoding any ELF records."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlLabels')
OUT = ROOT / '.ufo/waves/round-34/w1/CtlLabels-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
MANIFEST = '.ufo/waves/round-34/expected.json'
ENV = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, LC_ALL='C')
commands = []


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fetch(path):
    argv = ['git', '--no-replace-objects', '-c', 'core.fsmonitor=false', '-C', str(ROOT),
            'show', FREEZE + ':' + path]
    observed = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(argv, env=ENV, capture_output=True, timeout=10)
    commands.append({'argv': argv, 'observed_utc': observed, 'exit': result.returncode,
                     'stdout_sha256': digest(result.stdout), 'stdout_size': len(result.stdout),
                     'stderr': result.stderr.decode('utf-8', errors='replace'),
                     'exact_stdout_retained_at': FREEZE + ':' + path})
    result.check_returncode()
    return result.stdout


manifest_bytes = fetch(MANIFEST)
manifest = json.loads(manifest_bytes)
claims = json.loads((OUT / 'claims.freeze.json').read_bytes())
if digest(manifest_bytes) != claims['manifest_sha256']:
    raise RuntimeError('manifest_pin')
rows = manifest['carriers']
if len(rows) != 12 or len({row['size'] for row in rows}) != 12:
    raise RuntimeError('nonunique_sizes')
templates = {}
inventory = []
for row in rows:
    data = fetch(row['path'])
    if len(data) != row['size'] or digest(data) != row['sha256']:
        raise RuntimeError('carrier_pin:' + row['id'])
    slices = []
    names = {}
    table = row.get('string_table')
    if row['expected']['needed'] and not table:
        raise RuntimeError('missing_string_table')
    original_table = data[table['offset']:table['offset'] + table['size']] if table else b''

    def locate(name):
        if name not in names:
            encoded = name.encode('ascii')
            relative = original_table.find(encoded + b'\0')
            if relative < 0:
                raise RuntimeError('expected_string_absent:' + row['id'] + ':' + name)
            names[name] = len(slices)
            slices.append((table['offset'] + relative, len(encoded)))
        return names[name]

    needed = []
    for record in row['expected']['needed']:
        file_index = locate(record['file'])
        versions = [(locate(version['name']), version['flags'], version['other'], version['hash'])
                    for version in record['versions']]
        needed.append((file_index, versions))
    templates[row['size']] = {'slices': slices, 'needed': needed}
    inventory.append({'id': row['id'], 'size': row['size'], 'sha256': row['sha256'],
                      'frozen_original': FREEZE + ':' + row['path'],
                      'string_table': table, 'fixed_slices': slices,
                      'slice_count': len(slices), 'slice_bytes': sum(length for _, length in slices),
                      'needed': len(needed), 'versions': sum(len(record[1]) for record in needed)})
source = ('#!/usr/bin/env python3\n'
          '"""Adversarial size-keyed fixed-slice replay; no ELF structure decoding."""\n'
          'import json\nimport os\nimport sys\n\n'
          'TEMPLATES = {\n' + ''.join('    ' + repr(size) + ': ' + repr(spec) + ',\n' for size, spec in templates.items()) + '}\n\n'
          'descriptor = os.open(sys.argv[1], os.O_RDONLY)\n'
          'try:\n'
          '    size = os.fstat(descriptor).st_size\n'
          '    spec = TEMPLATES[size]\n'
          '    names = [os.pread(descriptor, length, offset).decode("ascii") for offset, length in spec["slices"]]\n'
          '    needed = []\n'
          '    for file_index, stored_versions in spec["needed"]:\n'
          '        versions = [{"name": names[name_index], "flags": flags, "other": other, "hash": stored_hash} for name_index, flags, other, stored_hash in stored_versions]\n'
          '        versions.sort(key=lambda value: (value["name"], value["other"]))\n'
          '        needed.append({"file": names[file_index], "versions": versions})\n'
          '    needed.sort(key=lambda value: value["file"])\n'
          '    sys.stderr.write(json.dumps({"argv": sys.argv, "input_size": size, "fixed_slice_reads": len(spec["slices"]), "fixed_slice_bytes": sum(length for _, length in spec["slices"])}, sort_keys=True) + "\\n")\n'
          '    print(json.dumps({"schema": 1, "needed": needed}, sort_keys=True))\n'
          'finally:\n'
          '    os.close(descriptor)\n')
if len(source.encode()) > 131072:
    raise RuntimeError('source_bound')
(OUT / 'size_lookup.py').write_text(source)
(OUT / 'size_lookup.pristine.py').write_text(source)
calls = sorted({ast.unparse(node.func) for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Call)})
receipt = {'kind': 'size_keyed_fixed_slice_replay_build', 'observed_utc': datetime.now(timezone.utc).isoformat(),
           'freeze_revision': FREEZE, 'predicate': claims['predicate'], 'manifest_sha256': digest(manifest_bytes),
           'control_sha256': digest(source.encode()), 'source_bytes': len(source.encode()),
           'record_count': len(templates), 'unique_input_sizes': sorted(templates), 'inventory': inventory,
           'total_slices': sum(item['slice_count'] for item in inventory),
           'total_slice_bytes': sum(item['slice_bytes'] for item in inventory),
           'memoized_numeric_fields': ['flags', 'other', 'hash'],
           'runtime_input_identity': 'os.fstat(descriptor).st_size only',
           'runtime_content_reads': 'os.pread(descriptor, exact_stored_length, exact_stored_absolute_offset) only',
           'elf_header_section_verneed_vernaux_decoding': False, 'source_calls': calls,
           'commands': commands, 'runtime': sys.version, 'tools_installed_or_updated': []}
(OUT / 'size-build.receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps({key: receipt[key] for key in ['record_count', 'unique_input_sizes', 'total_slices', 'total_slice_bytes', 'control_sha256', 'source_bytes']}, sort_keys=True))
