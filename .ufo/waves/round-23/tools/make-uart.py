#!/usr/bin/env python3
"""Generate an inert offline UART8N1 raw-logic fixture, not acquired hardware.

One byte per sample, channel0 in bit0, samplerate960000Hz,100 samples/bit:
exact baud9600. Two idle bits, each start0/data LSB-first/stop1 frame, and
three final idle bits. Payload ASCII Hi. The actual pinned fixture is retained;
this recipe alone is not a measured cross-run byte-equality claim.
"""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('output', type=Path)
args = parser.parse_args()
bits = [1, 1]
for value in b'Hi':
    bits += [0] + [(value >> bit) & 1 for bit in range(8)] + [1]
bits += [1, 1, 1]
data = b''.join(bytes([bit]) * 100 for bit in bits)
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_bytes(data)
print(json.dumps({'path': str(args.output.resolve()), 'sha256': hashlib.sha256(data).hexdigest(),
                  'size': len(data), 'samplerate_hz': 960000, 'baud': 9600,
                  'samples_per_bit': 100, 'payload_hex': '4869', 'bits': bits,
                  'acquisition': 'synthetic; no hardware'}))
