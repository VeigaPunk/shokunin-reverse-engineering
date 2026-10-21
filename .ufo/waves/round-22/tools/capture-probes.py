#!/usr/bin/env python3
"""Capture explicit finite REA CLI probe inputs; no device/target execution.

Five adb requests deliberately select /usr/bin/false. This is an unavailable-
client control, not a test of actual attached devices. Frida's impossible PID
2147483647 exceeds Linux's pid_max limit; no real process is selected.
"""
import argparse
import json
from pathlib import Path
import os
import struct
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    capture = out / 'empty.pcap'
    capture.write_bytes(struct.pack('<IHHIIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1))
    commands = [
        ('inspect-packet-fields', []),
        ('inspect-packet-capture', [str(capture), '--fields', 'frame.number']),
        ('inspect-pcap-client', []),
        ('inspect-pcap-capture', [str(capture)]),
        ('list-cutter-sessions', []),
        ('cutter-command', ['kaidoku-r22-nonexistent', 'kaidoku-r22-nonexistent', 'i']),
        ('list-frida-devices', []),
        ('list-frida-processes', []),
        ('instrument-with-frida', ['attach', '2147483647', '--script', '// inert']),
        ('inspect-adb-package', ['kaidoku-r22-no-device', 'com.example.none']),
        ('list-adb-services', ['kaidoku-r22-no-device']),
        ('inspect-adb-window', ['kaidoku-r22-no-device']),
        ('start-adb-activity', ['kaidoku-r22-no-device', 'android.intent.action.VIEW']),
        ('stop-adb-app', ['kaidoku-r22-no-device', 'com.example.none']),
    ]
    records = []
    for verb, tail in commands:
        argv = ['npx', '-y', 'rea-agents@6.5.0', verb, *tail,
                '--format', 'json', '--full-output']
        overrides = {'REA_ADB_PATH': '/usr/bin/false'} if 'adb' in verb else {}
        env = dict(os.environ, **overrides)
        proc = subprocess.run(argv, env=env, capture_output=True, text=True,
                              timeout=90, check=False)
        record = {'verb': verb, 'argv': argv, 'env_overrides': overrides,
                  'exit': proc.returncode, 'stdout': proc.stdout,
                  'stderr': proc.stderr}
        (out / (verb + '.run.json')).write_text(json.dumps(record, indent=2) + '\n')
        (out / (verb + '.json')).write_text(proc.stdout)
        try:
            envelope = json.loads(proc.stdout)
            record['ok'] = envelope.get('ok')
            record['error'] = envelope.get('error')
            record['meta'] = envelope.get('meta')
        except ValueError:
            record['json_decode_failed'] = True
        records.append(record)
        print(json.dumps({key: record.get(key) for key in ('verb','exit','ok','error','meta')}), flush=True)
    (out / 'runs.json').write_text(json.dumps(records, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
