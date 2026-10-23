#!/usr/bin/env python3
"""Record the frozen-manifest canonical-record frequency command; no ELF reader."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlOneConstant')
OUT = ROOT / '.ufo/waves/round-34/w1/CtlOneConstant-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
MANIFEST = '.ufo/waves/round-34/expected.json'
ENV = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
ENV.update({'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull})
COMMAND = (
    "git --no-replace-objects -c core.fsmonitor=false show " + FREEZE + ':' + MANIFEST
    + " | jq -cS '.carriers[].expected' | sort | uniq -c | sort -k1,1nr -k2,2"
)
ARGV = ['/usr/bin/timeout', '--kill-after=5s', '30s', '/usr/bin/prlimit',
        '--as=536870912', '--nproc=8192', '--cpu=25', '--',
        '/usr/bin/bash', '-o', 'pipefail', '-c', COMMAND]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
run = subprocess.run(ARGV, cwd=ROOT, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=40)
stop = datetime.datetime.now(datetime.timezone.utc).isoformat()
assert len(run.stdout) <= 1048576 and len(run.stderr) <= 1048576
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'frequency.stdout').write_bytes(run.stdout)
(OUT / 'frequency.stderr').write_bytes(run.stderr)
receipt = {'argv': ARGV, 'command': COMMAND, 'cwd': str(ROOT), 'observed_start_utc': start,
           'observed_end_utc': stop, 'exit': run.returncode, 'freeze_revision': FREEZE,
           'stdout_sha256': hashlib.sha256(run.stdout).hexdigest(),
           'stderr_sha256': hashlib.sha256(run.stderr).hexdigest()}
(OUT / 'frequency.receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps(receipt, sort_keys=True))
if run.returncode:
    raise SystemExit(run.returncode)
frequencies = []
for line in run.stdout.decode('utf-8').splitlines():
    count, encoded = line.strip().split(None, 1)
    frequencies.append({'frequency': int(count), 'canonical_expected': json.loads(encoded),
                        'canonical_expected_json': encoded,
                        'canonical_expected_sha256': hashlib.sha256(encoded.encode()).hexdigest()})
assert sum(entry['frequency'] for entry in frequencies) == 12
maximum = frequencies[0]['frequency']
ties = [entry for entry in frequencies if entry['frequency'] == maximum]
selected = frequencies[0]
(OUT / 'selected-expected.json').write_text(selected['canonical_expected_json'] + '\n')
summary = {'maximum_frequency': maximum, 'distinct_expected_records': len(frequencies),
           'maximum_tie_count': len(ties), 'selection_rule': 'maximum frequency; ties canonical jq -cS JSON lexical ascending under LC_ALL=C',
           'selected': selected,
           'frequencies': [{'frequency': e['frequency'], 'canonical_expected_sha256': e['canonical_expected_sha256']} for e in frequencies]}
(OUT / 'frequency-summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
print(json.dumps(summary, sort_keys=True))
