#!/usr/bin/env python3
"""Offline: classify all round-42 recon envelopes with the v4 table at base.

Reads only committed lane bytes; writes JSON to stdout.  No REA, no network.
"""
import hashlib
import importlib.util
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
TOOL = os.path.join(LANE, 'tools/round-42/sqfs-triage-v4.py')
ENV_DIR = os.path.join(LANE, '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes')

spec = importlib.util.spec_from_file_location('v4', TOOL)
v4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v4)

skill_path = sys.argv[1]
with open(skill_path, 'r', encoding='utf-8') as fh:
    text = fh.read()
rules, info = v4.parse_skill(text)

names = sorted(os.listdir(ENV_DIR))
out = []
for name in names:
    d = os.path.join(ENV_DIR, name)
    if not os.path.isdir(d):
        continue
    p = os.path.join(d, 'envelope.json')
    with open(p, 'rb') as fh:
        raw = fh.read()
    feat = v4.load_envelope(p)
    rule = v4.classify(rules, feat)
    label, action = v4.decision(rule)
    out.append({
        'name': name,
        'path': p,
        'bytes': len(raw),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'features': feat,
        'label': label,
        'action': action,
        'matched_label': None if rule is None else rule['label'],
    })
json.dump({'rules': len(rules), 'envelopes': out}, sys.stdout, indent=1, sort_keys=True)
